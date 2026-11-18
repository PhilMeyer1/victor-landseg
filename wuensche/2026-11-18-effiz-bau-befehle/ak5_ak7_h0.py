"""AK5 und AK7 (effiz-bau-befehle): zusammenfuehren gegen den Agent-Stand von H0, beide Befehle auf zwei Teilkacheln.

Aufruf: PY -B ak5_ak7_h0.py <Repo-Arbeitskopie> <Wegwerf-Ordner>
Liest nur unter BASIS/daten/landseg/H0 und dem Berichtsordner von landseg-historisch-3; schreibt nur in den
Wegwerf-Ordner. Ausgabe: Vergleich je Fassung und Teilkachel, Zeiten, SHA-256 der Scans vorher/nachher.
"""
import hashlib
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
from PIL import Image

BASIS = Path("C:/Users/Phil/Developement/Victor")
H0 = BASIS / "daten" / "landseg" / "H0"
D3 = BASIS / "wuensche" / "2026-11-18-landseg-historisch-3"
SCANS = BASIS / "daten" / "luftbilder" / "historisch"
REPO = Path(sys.argv[1])
TMP = Path(sys.argv[2])
sys.path.insert(0, str(REPO))
from landseg import dateien  # noqa: E402

FASSUNG = {"A": "a-alles-frei", "B": "b-kategorien-frei", "C": "c-feste-liste"}


def lies(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def hashes():
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(SCANS.glob("*.tif"))}


def kopiere(q: Path, z: Path):
    z.parent.mkdir(parents=True, exist_ok=True)
    if q.is_dir():
        shutil.copytree(q, z, dirs_exist_ok=True)
    else:
        shutil.copyfile(q, z)


def agent_stand(ziel: Path, tks):
    """Stand nach den Agents: Karten mit Eingriffen, segmente.json vor dem Zusammenführen, Urteile, Abgaben, Listen."""
    for k in "BC":
        o = FASSUNG[k]
        for tk in tks:
            for datei in ("labels.tif", "kandidaten.json"):
                if (H0 / o / tk / datei).is_file():
                    kopiere(H0 / o / tk / datei, ziel / o / tk / datei)
            kopiere(D3 / "sicherung" / o / tk / "segmente.json", ziel / o / tk / "segmente.json")
            kopiere(H0 / o / "urteil" / tk, ziel / o / "urteil" / tk)
    v = H0 / FASSUNG["B"] / "vereinheitlichung"
    kopiere(v / "codes.json", ziel / FASSUNG["B"] / "vereinheitlichung" / "codes.json")
    kopiere(v / "kategorien-b-entwurf.json", ziel / FASSUNG["B"] / "vereinheitlichung" / "kategorien-entwurf.json")
    for tk in tks:
        kopiere(H0 / FASSUNG["A"] / "abgabe" / tk, ziel / FASSUNG["A"] / "abgabe" / tk)
    kopiere(H0 / FASSUNG["A"] / "kategorien-a.json", ziel / FASSUNG["A"] / "vereinheitlichung" / "kategorien-entwurf.json")
    return angleichen(ziel, tks)


def angleichen(ziel: Path, tks) -> dict:
    """Nach dem Zusammenführen haben die Naht-Agents die Karten von B und C an Ort und Stelle geändert (neue Segmente
    ohne Urteil, verschwundene Segmente); eine Sicherung der Karten von damals gibt es nicht. Nur in der Wegwerf-Kopie:
    verschwundene Segmente aus segmente.json nehmen, neue mit ihrem heutigen Eintrag ergänzen und ihnen ein Urteil
    mit der heutigen Klasse geben (Viertel v1, B: Code in codes.json). Diese IDs zählen im Vergleich nicht."""
    neu_ids = {}
    codes_pfad = ziel / FASSUNG["B"] / "vereinheitlichung" / "codes.json"
    codes = lies(codes_pfad)
    for k in "BC":
        o = FASSUNG[k]
        for tk in tks:
            karte = dateien.lese_labels(ziel / o / tk / "labels.tif")
            da = set(np.unique(karte).tolist())
            seg = lies(ziel / o / tk / "segmente.json")
            heute = {s["id"]: s for s in lies(H0 / o / tk / "segmente.json")["segmente"]}
            alt = {s["id"] for s in seg["segmente"]}
            seg["segmente"] = [s for s in seg["segmente"] if s["id"] in da] + [heute[i] for i in sorted(da - alt)]
            dateien.schreibe_json(ziel / o / tk / "segmente.json", seg)
            urteile = set()
            for n in range(1, 5):
                urteile |= {s["id"] for s in lies(ziel / o / "urteil" / tk / f"v{n}" / "urteil.json")["segmente"]}
            m = next(t for t in lies(ziel / "manifest.json")["teilkacheln"] if t["id"] == tk)["kern_im_bild"]
            kern = set(np.unique(karte[m["y"]:m["y"] + m["hoehe"], m["x"]:m["x"] + m["breite"]]).tolist())
            fehlt = sorted(kern - urteile)
            neu_ids[(k, tk)] = fehlt
            if fehlt:
                p = ziel / o / "urteil" / tk / "v1" / "urteil.json"
                u = lies(p)
                for i in fehlt:
                    u["segmente"].append({"id": i, "klasse_heute": heute[i]["klasse"], "klasse_vorschlag": None,
                                          "urteil": "sauber", "sicher": heute[i].get("sicher") == "ja",
                                          "was_ist_es": "nach dem Zusammenführen von einem Naht-Agent angelegt"})
                    if k == "B":
                        codes["segmente"].setdefault(tk, {})[str(i)] = {"code": heute[i]["klasse"], "viertel": "v1"}
                dateien.schreibe_json(p, u)
    dateien.schreibe_json(codes_pfad, codes)
    return neu_ids


def ruf(*argv):
    t = time.perf_counter()
    r = subprocess.run([sys.executable, "-B", "-m", "landseg", *argv], cwd=REPO, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    return r.returncode, round(time.perf_counter() - t, 1), r.stdout, r.stderr


def vergleich(ziel: Path, tks, neu_ids: dict) -> list[str]:
    zeilen = []
    for k, o in FASSUNG.items():
        for tk in tks:
            neu = {s["id"]: s for s in lies(ziel / o / tk / "segmente.json")["segmente"]}
            alt = {s["id"]: s for s in lies(H0 / o / tk / "segmente.json")["segmente"]}
            karte_gleich = np.array_equal(dateien.lese_labels(ziel / o / tk / "labels.tif"),
                                          dateien.lese_labels(H0 / o / tk / "labels.tif"))
            weg = set(neu_ids.get((k, tk), []))
            anders = [i for i in neu if i in alt and i not in weg and neu[i].get("klasse") != alt[i].get("klasse")]
            durch_einigung = [i for i in anders if alt[i].get("einigung")]
            sicher_anders = [i for i in neu if i in alt and neu[i].get("sicher") != alt[i].get("sicher")]
            zeilen.append(f"{k} {tk}: Segmente neu {len(neu)} / Agent {len(alt)}, IDs gleich {set(neu) == set(alt)}, "
                          f"Karte bildpunktgleich {karte_gleich}, Klasse anders {len(anders)} (davon mit Einigung "
                          f"{len(durch_einigung)}: {sorted(set(anders) - set(durch_einigung))[:8]} ohne), sicher anders "
                          f"{len(sicher_anders)}; angeglichen (Naht-Agents, ohne Urteil) {len(weg)}")
    return zeilen


def main():
    vorher = hashes()
    if TMP.exists():
        shutil.rmtree(TMP)
    # ---------------------------------------------------------------- AK5: ganzer Ausschnitt H0
    voll = TMP / "h0-voll"
    for name in ("manifest.json", "H0.png", "teilkacheln"):
        kopiere(H0 / name, voll / name)
    tks = [t["id"] for t in lies(voll / "manifest.json")["teilkacheln"]]
    neu_ids = agent_stand(voll, tks)
    rc, s, aus, err = ruf("zusammenfuehren", "--manifest", str(voll / "manifest.json"), "--ziel", str(voll / "bericht"),
                          "--json")
    print(f"AK5 zusammenfuehren H0 (4 Teilkacheln): Exit {rc}, {s} s")
    if err.strip():
        print(err.strip()[-1500:])
    erg = json.loads(aus.strip().splitlines()[-1]) if aus.strip() else {}
    ref = lies(D3 / "fassungen-h0.json")
    for k, e in (erg.get("fassungen") or {}).items():
        r = ref[k]
        print(f"  {k}: Kern {e['segmente_kern']} (Agent {sum(x['kern'] for x in r.values())}), unsicher {e['unsicher']} "
              f"(Agent {sum(x['sicher_nein'] for x in r.values())}), Eingriffe {e['eingriffe_urteil']}/{e['eingriffe_verlauf']} "
              f"(Agent {sum(x.get('eingriffe_urteil', 0) for x in r.values())}/{sum(x.get('eingriffe_verlauf', 0) for x in r.values())}), "
              f"Nahtverstöße {e['nahtverstoesse']}, offen {e['einigung_offen']} Paare, Bündel {len(e['buendel'])}")
        for tk, z in e["teilkacheln"].items():
            gleich = all(z.get(f) == r[tk].get(f) for f in z if f in r[tk])
            if not gleich:
                print(f"    {tk}: neu {z} | Agent {r[tk]}")
    for z in vergleich(voll, tks, neu_ids):
        print("  " + z)
    # Nahtzahlen der heutigen Agent-Karten (gleiche Zusammentragung, nur gelesen)
    from landseg import kategorien, naht, zusammentragen as zt
    bild = naht.lese_bild(H0 / "H0.png")
    for k, o in FASSUNG.items():
        auftrag = TMP / "ref" / o / "zusammentragen.json"
        dateien.schreibe_json(auftrag, {"schema": "landseg-zusammentragen/1", "manifest": (H0 / "manifest.json").as_posix(),
                                        "einheiten": [{"teilkachel": tk, "labels": (H0 / o / tk / "labels.tif").as_posix(),
                                                       "segmente": (H0 / o / tk / "segmente.json").as_posix(), "runde": 0,
                                                       "name": f"{k}-{tk}"} for tk in tks], "ziel": "zusammen"})
        e = zt.zusammentragen(auftrag, kategorien.laden(H0 / o / f"kategorien-{k.lower()}.json"))
        nb = naht.pruefe_naehte(dateien.lese_labels(e.ziel / "labels.tif"), lies(H0 / "manifest.json"), bild)
        print(f"  Agent-Karten heute {k}: Nahtverstöße {len(nb.verstoesse)}")
    print("  Agent-Karten beim Zusammenführen (zusammentragen-h0.log): A 187, B 169, C 156")
    # ---------------------------------------------------------------- AK7: zwei Teilkacheln, beide Befehle
    zwei = TMP / "h0-zwei"
    m = lies(H0 / "manifest.json")
    m["teilkacheln"] = [t for t in m["teilkacheln"] if t["id"] in ("r0c0", "r0c1")]
    m["ausschnitt"]["hoehe"] = max(t["kern"]["y"] + t["kern"]["hoehe"] for t in m["teilkacheln"])
    dateien.schreibe_json(zwei / "manifest.json", m)
    with Image.open(H0 / m["ausschnitt"]["bild"]) as b:
        b.crop((0, 0, m["ausschnitt"]["breite"], m["ausschnitt"]["hoehe"])).save(zwei / m["ausschnitt"]["bild"])
    for t in m["teilkacheln"]:
        kopiere(H0 / t["bild"], zwei / t["bild"])
        kopiere(H0 / "vorstufe" / t["id"], zwei / "vorstufe" / t["id"])
    hinweis = TMP / "hinweis.md"
    hinweis.write_text("Schwarz-Weiß-Scan von 1968 ohne Lagedaten; ein Bildpunkt etwa 0,45 m.\n", encoding="utf-8")
    rc1, s1, aus1, err1 = ruf("vorbereiten", "--manifest", str(zwei / "manifest.json"), "--ziel", str(zwei / "bericht"),
                              "--hinweis", str(hinweis), "--lauf", "ak7")
    print(f"AK7 vorbereiten (2 Teilkacheln): Exit {rc1}, {s1} s: {(aus1 + err1).strip()[-600:]}")
    t0 = time.perf_counter()
    agent_stand(zwei, ["r0c0", "r0c1"])
    print(f"(Agent-Stand in die Kopie gelegt: {round(time.perf_counter() - t0, 1)} s, zählt nicht)")
    rc2, s2, aus2, err2 = ruf("zusammenfuehren", "--manifest", str(zwei / "manifest.json"), "--ziel",
                              str(zwei / "bericht"))
    print(f"AK7 zusammenfuehren (2 Teilkacheln): Exit {rc2}, {s2} s: {(aus2 + err2).strip()[-1500:]}")
    nachher = hashes()
    print("Scans SHA-256 vorher:", vorher)
    print("Scans SHA-256 nachher gleich:", vorher == nachher)


if __name__ == "__main__":
    main()
