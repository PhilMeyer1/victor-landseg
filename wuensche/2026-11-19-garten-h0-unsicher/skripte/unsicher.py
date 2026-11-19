"""Garten-Kandidaten auf H0, die in landseg-garten-3 "unklar" bekamen, als Garten mit sicher: false eintragen.

Aufruf (Stitcher-venv, -I): python unsicher.py probe|sicherung|eintragen|zaehlen
- probe:     Liste der unklaren Kandidaten gegen die aktuellen segmente.json (nichts geschrieben)
- sicherung: labels.tif, segmente.json, naht.json je Teilkachel und zusammen/ nach sicherung-vor-garten-h0-unsicher/
- eintragen: je Teilkachel `landseg eingriff ... stapel` (klasse_setzen), danach unter der Kartensperre
             Bearbeitung.vermerken (sicher, grund) mit Verlauf
- zaehlen:   Garten-Segmente je Fassung (Teilkacheln und zusammen/), Abgleich mit den unklaren Kandidaten
"""
import json, shutil, subprocess, sys
from pathlib import Path

REPO = "C:/Users/Phil/Developement/Victor/landseg"
sys.path.insert(0, REPO)
from landseg import dateien, kategorien  # noqa: E402
from landseg.eingriff import Bearbeitung  # noqa: E402

D = Path("C:/Users/Phil/Developement/Victor/wuensche/2026-11-19-garten-h0-unsicher")
G3 = Path("C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten")
H0 = Path("C:/Users/Phil/Developement/Victor/daten/landseg/H0")
PY = "C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe"
ORD = {"A": ("a-alles-frei", "kategorien-a.json"), "B": ("b-kategorien-frei", "kategorien-b.json"),
       "C": ("c-feste-liste", "kategorien-c.json")}
CODE = {"A": "4.4", "B": "5.3", "C": "3.6"}
TK = ["r0c0", "r0c1", "r1c0", "r1c1"]
GRUND = "Garten wahrscheinlich, auf SW nicht sicher (Nutzer 2026-11-18)"
BEARBEITER = "umsetzer:garten-h0-unsicher"


def unklare():
    """{(fassung, tk): [(id, grund des Bestätigers)]} aus den H0-Einheiten von garten-3."""
    plan = {}
    for e in sorted(G3.glob("H0-*")):
        ent = json.loads((e / "entscheid.json").read_text(encoding="utf-8"))
        kd = json.loads((e / "kandidaten.json").read_text(encoding="utf-8"))
        for i, v in ent.items():
            if v["garten"] == "unklar":
                plan.setdefault((kd["fassung"], kd["teilkachel"]), []).append((int(i), v.get("grund", "")))
    return plan


def ist_garten(f, klasse):
    """Garten-Klasse der Fassung oder eine ihrer Unterklassen (A 4.4.1 "Garten / Grün im Ort", aus garten-4)."""
    return klasse == CODE[f] or str(klasse).startswith(CODE[f] + ".")


def segs(f, tk):
    return dateien.lese_segmente(H0 / ORD[f][0] / tk / "segmente.json")


def probe():
    plan = unklare()
    print("unklar je Fassung:", {f: sum(len(v) for (ff, _), v in plan.items() if ff == f) for f in "ABC"})
    for (f, tk), ids in sorted(plan.items()):
        s = {x["id"]: x for x in segs(f, tk)["segmente"]}
        kat = kategorien.laden(H0 / ORD[f][0] / ORD[f][1])
        print(f, tk, "Garten-Code gültig:", kat.gueltig(CODE[f]))
        for i, _ in ids:
            x = s.get(i)
            print("  ", i, "FEHLT" if x is None else
                  {k: x.get(k) for k in ("klasse", "sicher", "grund", "urteil", "begruendung", "warum")})
    beispiel = segs("A", "r0c0")["segmente"][0]
    print("Felder eines Segments:", sorted(beispiel))


def sicherung():
    ziel = D / "sicherung-vor-garten-h0-unsicher"
    for f, (o, k) in ORD.items():
        for t in TK + ["zusammen"]:
            src, dst = H0 / o / t, ziel / o / t
            dst.mkdir(parents=True, exist_ok=True)
            for n in ("labels.tif", "segmente.json", "naht.json"):
                if (src / n).exists() and not (dst / n).exists():
                    shutil.copy2(src / n, dst / n)
        shutil.copy2(H0 / o / k, ziel / o / k)
    print("ok", ziel)


def eintragen():
    log = open(D / "logs" / "eintragen.log", "a", encoding="utf-8")
    for (f, tk), ids in sorted(unklare().items()):
        o, k = ORD[f]
        d = H0 / o / tk
        vorher = {x["id"]: x for x in segs(f, tk)["segmente"]}
        umstellen = [i for i, _ in sorted(ids) if not ist_garten(f, vorher[i].get("klasse"))]
        sf = D / "logs" / f"schritte-H0-{f}-{tk}.json"
        sf.write_text(json.dumps({"schritte": [{"op": "klasse_setzen", "id": i, "klasse": CODE[f]}
                                               for i in umstellen]}), encoding="utf-8")
        log.write(f"{f} {tk}: unklar {len(ids)}, schon Garten {len(ids) - len(umstellen)}, umstellen {umstellen}\n")
        if umstellen:
            a = ["eingriff", "--labels", str(d / "labels.tif"), "--segmente", str(d / "segmente.json"),
                 "--kategorien", str(H0 / o / k), "--bearbeiter", BEARBEITER, "stapel", "--datei", str(sf)]
            r = subprocess.run([PY, "-B", "-m", "landseg"] + a, cwd=REPO, capture_output=True, text=True,
                               encoding="utf-8")
            log.write("$ " + " ".join(a) + "\n" + r.stdout + r.stderr + f"[exit {r.returncode}]\n\n"); log.flush()
            if r.returncode != 0:
                print(f, tk, "stapel Exit", r.returncode, r.stderr[-300:]); sys.exit(1)
        with dateien.karte_sperren(d / "labels.tif"):
            arbeit = Bearbeitung(dateien.lese_labels(d / "labels.tif"), segs(f, tk),
                                 kategorien.laden(H0 / o / k), BEARBEITER)
            for i, _ in sorted(ids):
                alt = {x["id"]: x for x in arbeit.segmente["segmente"]}[i].get("sicher")
                wert = "nein" if isinstance(alt, str) else False
                arbeit.vermerken(i, {"sicher": wert, "grund": GRUND}, op="vermerk")
                log.write(f"vermerk {f} {tk} {i}: sicher {alt!r} -> {wert!r}\n")
            dateien.schreibe_json(d / "segmente.json", arbeit.segmente)
        print(f, tk, len(ids), "eingetragen")
    log.close()


def zaehlen():
    plan = unklare()
    for f, (o, k) in ORD.items():
        fehl, n_kern = [], 0
        for (ff, tk), ids in plan.items():
            if ff != f:
                continue
            s = {x["id"]: x for x in segs(f, tk)["segmente"]}
            for i, _ in ids:
                x = s.get(i, {})
                if not (ist_garten(f, x.get("klasse")) and x.get("sicher") in (False, "nein") and x.get("grund") == GRUND):
                    fehl.append((tk, i, x.get("klasse"), x.get("sicher")))
        tk_garten = {tk: sum(ist_garten(f, x.get("klasse")) for x in segs(f, tk)["segmente"]) for tk in TK}
        z = H0 / o / "zusammen" / "segmente.json"
        zs = dateien.lese_segmente(z)["segmente"] if z.exists() else []
        zg = [x for x in zs if ist_garten(f, x.get("klasse"))]
        zu = [x for x in zg if x.get("sicher") in (False, "nein")]
        n = sum(len(v) for (ff, _), v in plan.items() if ff == f)
        print(f"H0 {f} ({CODE[f]}): unklar {n}, davon nicht korrekt eingetragen {len(fehl)} {fehl[:5]} | "
              f"Garten je Teilkachel {tk_garten} | zusammen: Garten {len(zg)}, davon unsicher {len(zu)}")


{"probe": probe, "sicherung": sicherung, "eintragen": eintragen, "zaehlen": zaehlen}[sys.argv[1]]()
