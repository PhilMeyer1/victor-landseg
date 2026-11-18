"""Schritte 2-4: Garten-Kandidaten per Regel für T0 und H0 (Fassungen A, B, C), Einheiten mit Bildern und Auftrag.

Aufruf (im Ordner landseg): <py> -B kandidaten_garten.py [--ohne-bilder]
Liest nur; schreibt unter <wunsch>/einheiten/, <wunsch>/kandidaten.json und <wunsch>/kandidaten.md.

Regel für einen Kandidaten (je Segment im Kern, einmal je Bild und Fassung, zugeordnet der Teilkachel mit den
meisten Kernbildpunkten):
  - Klasse Dauergrünland außer Garten (in A/B: die eigene Grünland-Klasse samt den alten Garten-Klassen der Liste),
    oder Acker-Unterklasse mit Fläche unter 1000 m² (Beet), oder offener Boden;
  - und im Siedlungsgebiet: Merkmal im_siedlung = ja (Fassung A ohne Merkmal: Mehrheit der Bildpunkte in der Karte
    der Fassung C), sonst Grenze an ein Gebäude oder einen Hof;
  - nicht, wenn die Beschreibung einen Park, Friedhof oder Sportplatz nennt (ohne „kein“).
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

REPO = Path("C:/Users/Phil/Developement/Victor/landseg")
sys.path.insert(0, str(REPO))
from landseg import dateien  # noqa: E402

WUNSCH = Path("C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3")
DATEN = Path("C:/Users/Phil/Developement/Victor/daten/landseg")
BILDER = {
    "T0": {"pfad": DATEN / "uebergabe/landseg-t0/T0", "m": 0.2, "art": "T0 Farbe (Farb-Orthofoto, rund 0,2 m je Bildpunkt)"},
    "H0": {"pfad": DATEN / "H0", "m": 0.45, "art": "H0 SW (Schwarz-Weiß-Scan von 1968, rund 0,45 m je Bildpunkt)"},
}
ORDNER = {"A": ("a-alles-frei", "a"), "B": ("b-kategorien-frei", "b"), "C": ("c-feste-liste", "c")}
MAX_JE_EINHEIT = 30
ACKER_MAX_M2 = 1000.0

# Regeln je Liste: gruen (Teilbäume), acker_klein (Teilbäume), boden (Teilbäume), gebaeude/hof (Teilbäume), garten (Code)
FEST = {"gruen": ["3"], "acker": ["2", "2.1", "2.2", "2.3"], "acker_exakt": True, "boden": ["6", "6.1"],
        "boden_exakt": True, "geb": ["1.1", "1.2.4"], "garten": "3.6"}
REGELN = {
    ("T0", "A"): {"gruen": ["4", "3"], "acker": ["5", "5.1"], "acker_exakt": True, "boden": ["5.2"],
                  "boden_exakt": False, "geb": ["1.1", "2.1.2"], "garten": "4.4"},
    ("T0", "B"): {"gruen": ["2", "3.3"], "acker": ["3", "3.1"], "acker_exakt": False, "boden": ["3.2"],
                  "boden_exakt": False, "geb": ["4.1", "6.3", "6.4"], "garten": "2.4"},
    ("T0", "C"): FEST,
    ("H0", "A"): {"gruen": ["4", "2.2", "2.3"], "acker": ["5"], "acker_exakt": False, "boden": [],
                  "boden_exakt": False, "geb": ["1.1", "1.2", "2.1"], "garten": "4.4"},
    ("H0", "B"): {"gruen": ["5", "2.2"], "acker": ["6"], "acker_exakt": False, "boden": [],
                  "boden_exakt": False, "geb": ["1", "2.1"], "garten": "5.3"},
    ("H0", "C"): FEST,
}
AUSSCHLUSS = re.compile(r"\b(park(?!platz|ing)|friedhof|sportplatz|sportanlage|sportrasen|fußballplatz)", re.I)

GARTEN_REGELN = """- eine einzige Unterklasse „Garten“ unter Dauergrünland (feste Liste: Code 3.6; freie Listen A/B: ihre eigene Klasse Garten unter ihrer Dauergrünland-Klasse, Regel L14 im Skill);
- dazu gehört jede krautige Grünfläche und jedes Beet im Haus- oder Hofgarten (auch Vor-, Obst- und Gemüsegarten), ob gepflegter Rasen oder nicht — Rasen ist kein Kennzeichen;
- nur Haus- und Hofgärten: Parks, Friedhöfe, Sportrasen und Wiesen am Ortsrand bleiben Wiese/Weide;
- Bäume, Sträucher und Hecken im Garten bleiben Gehölz (von oben sieht man die Krone);
- auf dem Schwarz-Weiß-Bild H0 nur klar erkennbare Gärten am Haus; Unklares bleibt, wie es ist."""


def im_teilbaum(code, wurzeln, exakt=False):
    if exakt:
        return code in wurzeln
    return any(code == w or code.startswith(w + ".") for w in wurzeln)


def nachbarn(karte):
    paare = set()
    for a, b in ((karte[:, :-1], karte[:, 1:]), (karte[:-1, :], karte[1:, :])):
        m = a != b
        for x, y in zip(a[m].tolist(), b[m].tolist()):
            paare.add((x, y))
            paare.add((y, x))
    nb = {}
    for x, y in paare:
        nb.setdefault(x, set()).add(y)
    return nb


def viertel_von(cx, cy, b, h):
    return ("v1" if cx < b // 2 else "v2") if cy < h // 2 else ("v3" if cx < b // 2 else "v4")


def lade_bild(bild):
    info = BILDER[bild]
    manifest = dateien.lese_json(info["pfad"] / "manifest.json")
    tks = {t["id"]: t for t in manifest["teilkacheln"]}
    return info, tks


def siedlung_aus_c(info, tk, karte_kern_c, segs_c):
    """Bildpunkt-Maske im_siedlung aus der Karte der Fassung C."""
    ja = {sid for sid, s in segs_c.items() if s.get("im_siedlung") in ("ja", True)}
    return np.isin(karte_kern_c, list(ja))


def kandidaten_fassung(bild, fass):
    info, tks = lade_bild(bild)
    ordner, k = ORDNER[fass]
    regel = REGELN[(bild, fass)]
    kat = dateien.lese_json(info["pfad"] / ordner / f"kategorien-{k}.json")
    namen = {c["code"]: c["name"] for c in kat["classes"]}
    geb_codes = {c for c in namen if im_teilbaum(c, regel["geb"])}
    proben = {}  # id -> tk -> daten
    for tk, t in tks.items():
        karte = dateien.lese_labels(info["pfad"] / ordner / tk / "labels.tif")
        segs = dateien.segmente_nach_id(dateien.lese_segmente(info["pfad"] / ordner / tk / "segmente.json"))
        kb = t["kern_im_bild"]
        kern = karte[kb["y"]:kb["y"] + kb["hoehe"], kb["x"]:kb["x"] + kb["breite"]]
        nb = nachbarn(karte)
        if fass == "A":
            kc = dateien.lese_labels(info["pfad"] / "c-feste-liste" / tk / "labels.tif")
            sc = dateien.segmente_nach_id(dateien.lese_segmente(info["pfad"] / "c-feste-liste" / tk / "segmente.json"))
            smask = siedlung_aus_c(info, tk, kc[kb["y"]:kb["y"] + kb["hoehe"], kb["x"]:kb["x"] + kb["breite"]], sc)
        ids, anz = np.unique(kern, return_counts=True)
        for sid, n in zip(ids.tolist(), anz.tolist()):
            ys, xs = np.nonzero(kern == sid)
            cx, cy = float(xs.mean()), float(ys.mean())
            j = int(np.argmin((xs - cx) ** 2 + (ys - cy) ** 2))
            s = segs.get(sid, {})
            if fass == "A":
                siedl = "ja" if smask[ys, xs].mean() >= 0.5 else "nein"
                siedl_q = "Mehrheit der Bildpunkte in Fassung C"
            else:
                siedl = s.get("im_siedlung", "nein")
                siedl_q = "Merkmal im_siedlung"
            proben.setdefault(sid, {})[tk] = {
                "n": n, "klasse": s.get("klasse"), "siedlung": siedl, "siedlung_quelle": siedl_q,
                "geb": bool(nb.get(sid, set()) & {i for i, e in segs.items() if e.get("klasse") in geb_codes}),
                "text": " ".join(str(s.get(f, "")) for f in ("name", "was_ist_es", "klasse_teil_name")),
                "viertel": viertel_von(cx, cy, kb["breite"], kb["hoehe"]),
                "mitte": [int(xs[j]) + kb["x"], int(ys[j]) + kb["y"]],
            }
    kand = []
    for sid, je_tk in proben.items():
        tk = max(je_tk, key=lambda t: je_tk[t]["n"])
        p = je_tk[tk]
        code = p["klasse"]
        if code is None or code == regel["garten"]:
            continue
        flaeche = sum(v["n"] for v in je_tk.values()) * info["m"] ** 2
        if im_teilbaum(code, regel["gruen"]):
            art = "Grünland"
        elif im_teilbaum(code, regel["acker"], regel["acker_exakt"]) and flaeche < ACKER_MAX_M2:
            art = "Acker klein"
        elif regel["boden"] and im_teilbaum(code, regel["boden"], regel["boden_exakt"]):
            art = "offener Boden"
        else:
            continue
        siedl = any(v["siedlung"] in ("ja", True) for v in je_tk.values())
        geb = any(v["geb"] for v in je_tk.values())
        if not (siedl or geb):
            continue
        if AUSSCHLUSS.search(p["text"]) and not re.search(r"\bkein", p["text"], re.I):
            continue
        kand.append({
            "id": sid, "klasse": code, "klasse_name": namen.get(code, code), "flaeche_m2": round(flaeche, 1),
            "teilkachel": tk, "viertel": p["viertel"], "mitte": p["mitte"],
            "grund_kandidat": f"{art}; " + ("im Siedlungsgebiet (" + p["siedlung_quelle"] + ")" if siedl
                                            else "grenzt an Gebäude oder Hof"),
            "auch_in": sorted(t for t in je_tk if t != tk),
        })
    return sorted(kand, key=lambda c: (c["teilkachel"], c["viertel"], c["id"])), regel, namen


def einheiten_bilden(kand):
    einheiten = []
    for tk in sorted({c["teilkachel"] for c in kand}):
        akt, n = [], 0
        for v in ("v1", "v2", "v3", "v4"):
            vk = [c for c in kand if c["teilkachel"] == tk and c["viertel"] == v]
            if not vk:
                continue
            if akt and n + len(vk) > MAX_JE_EINHEIT:
                einheiten.append((tk, akt))
                akt, n = [], 0
            akt.append((v, vk))
            n += len(vk)
        if akt:
            einheiten.append((tk, akt))
    return einheiten


def zoom(info, ordner, tk, ids, ziel, roh, kat_pfad):
    cmd = [sys.executable, "-B", "-m", "landseg", "zoom", "--manifest", str(info["pfad"] / "manifest.json"),
           "--teilkachel", tk, "--labels", str(info["pfad"] / ordner / tk / "labels.tif"),
           "--kategorien", str(kat_pfad), "--ids", ",".join(map(str, ids)), "--ziel", str(ziel)]
    if roh:
        cmd.append("--roh")
    r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True, encoding="utf-8",
                       creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    if r.returncode != 0:
        raise RuntimeError(f"zoom {ziel}: {r.stdout}\n{r.stderr}")


def auftrag_text(name, bild, fass, tk, info, ordner, viertel_bilder, kand, regel, namen, kat_pfad):
    py = sys.executable.replace("\\", "/")
    garten_code = regel["garten"]
    zeilen = [
        f"# Garten-Bestätigung {name}",
        "",
        "Du bist ein Agent des Projekts landseg (Segmentierung von Luftbildern). Antworte auf Deutsch. Regeln: "
        "`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md` (lies sie zuerst, besonders L14 und L15).",
        "",
        "## Ziel",
        "",
        f"Entscheide für jeden der {len(kand)} Kandidaten unten am Bild, ob er ein Haus- oder Hofgarten ist und damit die "
        f"Klasse Garten bekommen soll (in dieser Liste Code `{garten_code}` „{namen.get(garten_code)}“). Du änderst keine Karte "
        "und keine Klasse; du schreibst nur die Ergebnisdatei.",
        "",
        "## Was „Garten“ ist (Entscheidungen des Nutzers vom 18.11.2026)",
        "",
        GARTEN_REGELN,
        "",
        "## Bild",
        "",
        f"- Bild: {info['art']}" + ("; auf diesem Schwarz-Weiß-Bild nur klar erkennbare Gärten am Haus mit „ja“, "
                                    "Unklares „unklar“ oder „nein“." if bild == "H0" else "."),
        f"- Fassung {fass} ({ordner}), Teilkachel {tk}; Kategorienliste `{kat_pfad.as_posix()}`.",
        f"- Karte: `{(info['pfad'] / ordner / tk / 'labels.tif').as_posix()}`, Teilkachelbild: "
        f"`{(info['pfad'] / 'teilkacheln' / (tk + '.png')).as_posix()}`.",
        "- Bilder je Viertel (gelb alle Grenzen, magenta die Kandidaten mit Nummer; weißer Rahmen = Kern); jedes nur einmal ansehen:",
    ]
    for v, (b1, b2) in viertel_bilder.items():
        zeilen.append(f"  - {v}: mit Umriss `{b1.as_posix()}`, roh daneben `{b2.as_posix()}`")
    zeilen += [
        f"- Kandidatenliste: `{(WUNSCH / 'einheiten' / name / 'kandidaten.json').as_posix()}` (id, Klasse, Fläche m², "
        "Viertel, Mittelpunkt x,y in Bildpunkten der Teilkachel, Grund der Auswahl).",
        "",
        "## Kandidaten",
        "",
        "| id | Klasse | Fläche m² | Viertel | Mitte x,y | Grund der Auswahl |",
        "|---|---|---|---|---|---|",
    ]
    for c in kand:
        zeilen.append(f"| {c['id']} | {c['klasse']} {c['klasse_name']} | {c['flaeche_m2']:.0f} | {c['viertel']} | "
                      f"{c['mitte'][0]},{c['mitte'][1]} | {c['grund_kandidat']} |")
    zeilen += [
        "",
        "## Bei Zweifel",
        "",
        "Eine Nahansicht (roh und mit Umriss nebeneinander) macht dieser Befehl im Ordner `C:/Users/Phil/Developement/Victor/landseg`:",
        "",
        "```",
        f"{py} -B -m landseg zoom --manifest {(info['pfad'] / 'manifest.json').as_posix()} --teilkachel {tk} "
        f"--labels {(info['pfad'] / ordner / tk / 'labels.tif').as_posix()} --ids <id> --roh "
        f"--ziel {(WUNSCH / 'einheiten' / name).as_posix()}/nah_<id>.jpg",
        "```",
        "",
        "Nahansichten nur in diesen Ordner schreiben. Kein Subagent, keine Fenster, nichts installieren, keine Karte ändern.",
        "",
        "## Ergebnis",
        "",
        f"Datei `{(WUNSCH / 'einheiten' / name / 'entscheid.json').as_posix()}` (UTF-8-JSON), genau ein Eintrag je Kandidaten-ID:",
        "",
        "```json",
        '{"<id>": {"garten": "ja" | "nein" | "unklar", "grund": "<ein Satz>"}}',
        "```",
        "",
        "„ja“ nur für krautige Grünfläche oder Beet in einem Haus- oder Hofgarten; Gehölz, Weg, Hof, Park, Friedhof, "
        "Sportrasen und Wiese oder Acker am Ortsrand ohne Haus „nein“; was du am Bild nicht sicher entscheiden kannst, "
        "„unklar“. Rückgabe: Zahl ja / nein / unklar.",
        "",
    ]
    return "\n".join(zeilen)


def main():
    ohne_bilder = "--ohne-bilder" in sys.argv
    gesamt, ausgabe, offen = {}, [], []
    for bild in BILDER:
        info = BILDER[bild]
        for fass, (ordner, k) in ORDNER.items():
            kand, regel, namen = kandidaten_fassung(bild, fass)
            kat_pfad = info["pfad"] / ordner / f"kategorien-{k}.json"
            gesamt[f"{bild}-{fass}"] = kand
            zaehler = {}
            for tk, gruppen in einheiten_bilden(kand):
                zaehler[tk] = zaehler.get(tk, 0) + 1
                name = f"{bild}-{fass}-{tk}-{zaehler[tk]}"
                ziel = WUNSCH / "einheiten" / name
                ziel.mkdir(parents=True, exist_ok=True)
                ek = [c for _, vk in gruppen for c in vk]
                if len(ek) > MAX_JE_EINHEIT:
                    offen.append(f"{name}: {len(ek)} Kandidaten in einem Viertel (über {MAX_JE_EINHEIT}, Viertel nicht geteilt)")
                bilder = {}
                for v, vk in gruppen:
                    ids = [c["id"] for c in vk]
                    b1, b2 = ziel / f"{v}_umriss.jpg", ziel / f"{v}_roh.jpg"
                    if not ohne_bilder:
                        zoom(info, ordner, tk, ids, b1, False, kat_pfad)
                        zoom(info, ordner, tk, ids, b2, True, kat_pfad)
                    bilder[v] = (b1, b2)
                (ziel / "kandidaten.json").write_text(json.dumps({
                    "einheit": name, "bild": bild, "fassung": fass, "teilkachel": tk,
                    "garten_code": regel["garten"], "kategorien": kat_pfad.as_posix(),
                    "kandidaten": [{"id": c["id"], "klasse": c["klasse"], "klasse_name": c["klasse_name"],
                                    "flaeche_m2": c["flaeche_m2"], "viertel": c["viertel"], "mitte": c["mitte"],
                                    "grund_kandidat": c["grund_kandidat"], "auch_in": c["auch_in"]} for c in ek],
                }, ensure_ascii=False, indent=1), encoding="utf-8")
                (ziel / "auftrag.md").write_text(auftrag_text(name, bild, fass, tk, info, ordner, bilder, ek, regel,
                                                              namen, kat_pfad), encoding="utf-8")
                ausgabe.append({"name": name, "bild": bild, "fassung": fass, "tk": tk, "n": len(ek),
                                "ordner": ziel.as_posix(), "viertel": [int(v[1]) for v, _ in gruppen]})
    (WUNSCH / "kandidaten.json").write_text(json.dumps({"einheiten": ausgabe, "offen": offen,
                                                        "kandidaten": gesamt}, ensure_ascii=False, indent=1),
                                            encoding="utf-8")
    # kandidaten.md
    z = ["# Garten-Kandidaten (landseg-garten-3)", "",
         f"Gesamt: **{sum(len(v) for v in gesamt.values())}** Kandidaten in **{len(ausgabe)}** Einheiten "
         f"(Skript `skripte/kandidaten_garten.py`, Regeln im Kopf des Skripts).", "",
         "| Bild | Fassung | Garten-Code | Kandidaten | Einheiten | davon Grünland / Acker klein / offener Boden |",
         "|---|---|---|---|---|---|"]
    for key, kand in gesamt.items():
        bild, fass = key.split("-")
        arten = [sum(c["grund_kandidat"].startswith(a) for c in kand) for a in ("Grünland", "Acker klein", "offener Boden")]
        z.append(f"| {bild} | {fass} | {REGELN[(bild, fass)]['garten']} | {len(kand)} | "
                 f"{sum(1 for e in ausgabe if e['bild'] == bild and e['fassung'] == fass)} | {' / '.join(map(str, arten))} |")
    z += ["", "## Einheiten", "", "| Einheit | Kandidaten | Viertel |", "|---|---|---|"]
    for e in ausgabe:
        z.append(f"| {e['name']} | {e['n']} | {', '.join('v' + str(v) for v in e['viertel'])} |")
    z += ["", "## Hinweise", "",
          "- Ein Segment, dessen Kern über mehrere Teilkacheln reicht (gleiche ID), ist nur einmal Kandidat: in der "
          "Teilkachel mit den meisten Kernbildpunkten (`auch_in` nennt die anderen); das Urteil gilt für alle (L6).",
          "- Fassung A trägt kein Merkmal `im_siedlung`; es kommt aus der Karte der Fassung C (Mehrheit der Bildpunkte).",
          "- Freie Listen: die eigene Grünland-Klasse heißt jetzt „Dauergrünland (…)“, darunter die neue Klasse Garten; "
          "H0 B: alte Klasse 2.2 „Garten“ unter „Hof und Garten“ heißt jetzt „Gartenfläche am Hof (bisher „Garten“)“ "
          "(Code unverändert) und ist Kandidat. Vorher-Stand der Listen unter `listen-vorher/`."]
    for o in offen:
        z.append(f"- Offen: {o}")
    (WUNSCH / "kandidaten.md").write_text("\n".join(z) + "\n", encoding="utf-8")
    print(json.dumps({"einheiten": len(ausgabe), "kandidaten": {k: len(v) for k, v in gesamt.items()},
                      "offen": offen}, ensure_ascii=False))


if __name__ == "__main__":
    main()
