"""Teil 3 (Kopie aus Teil 2, erweitert: Abschnitt Nachsegmentieren wörtlich, Zeile Karte, Gegenprobe-Kopie,
Kopien bildpunktgleich, höchstens 800 Kernsegmente, Probe pruefe_urteil mit echtem Eingriff auf einer Kopie).

Unabhängige Prüfung von Teil 2 (H0): Viertel, Bilder, Aufträge, Kopien, Ergebnisordner, pruefe_urteil.

Aufruf: PY -I pruefe_h0.py <BASIS> <D>   (Exit 0 = ok, 1 = Mängel)
"""
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import tifffile

sys.path.insert(0, str(Path(sys.argv[2]) / "skripte"))
REPO = Path(sys.argv[1]) / "landseg"

BASIS, D = Path(sys.argv[1]), Path(sys.argv[2])
H0 = BASIS / "daten" / "landseg" / "H0"
PY = sys.executable
plan = json.loads((D / "auftraege.json").read_text(encoding="utf-8"))
m = json.loads((H0 / "manifest.json").read_text(encoding="utf-8"))
maengel, zahlen = [], {}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def nachseg_erwartet() -> str:
    quelle = (D / "skripte" / "baue_auftraege_h0.py").read_text(encoding="utf-8")
    a = quelle.index('NACHSEG = """') + len('NACHSEG = """')
    return quelle[a:quelle.index('"""', a)].replace("{{PY}}", plan["py"])


NACHSEG = nachseg_erwartet()
kern_gesamt = 0


def auftrag_ok(pfad: str, ids=None, karte=None):
    t = Path(pfad).read_text(encoding="utf-8")
    if karte is not None:
        if t.count(NACHSEG) != 1:
            maengel.append(f"Abschnitt Nachsegmentieren nicht genau einmal wörtlich in {pfad}")
        zeile = f"Karte zum Nachsegmentieren: `{karte}/labels.tif` und `{karte}/segmente.json`"
        if t.count(zeile) != 1:
            maengel.append(f"Zeile Karte fehlt oder falsch in {pfad}")
        if t.count("Karte zum Nachsegmentieren:") != 1:
            maengel.append(f"mehr als eine Karte genannt in {pfad}")
        if f"--segmente {karte}/segmente.json --fassung" not in t:
            maengel.append(f"Kontrollbefehl nicht auf der Karte in {pfad}")
    elif "Nachsegmentieren" in t:
        maengel.append(f"A-Auftrag mit Nachsegmentieren: {pfad}")
    if "{{" in t or "}}" in t and "{{" in t:
        maengel.append(f"Platzhalter übrig in {pfad}")
    if "Schwarz-Weiß-Scan" not in t:
        maengel.append(f"SW-Abschnitt fehlt in {pfad}")
    if re.search(r"\bT0\b", t):
        maengel.append(f"T0 genannt in {pfad}")
    for ref in re.findall(r"C:/Users/Phil/Developement/Victor/daten/landseg/H0/[\w./-]+\.(?:png|jpg|json)", t):
        if not Path(ref).exists() and "/urteil" not in ref and "/abgabe" not in ref and "nah_" not in ref:
            maengel.append(f"{pfad}: Datei fehlt {ref}")
    if ids is not None:
        zeile = re.search(r"--ids ([\d,]+)", t)
        if not zeile or [int(i) for i in zeile.group(1).split(",")] != ids:
            maengel.append(f"{pfad}: --ids passt nicht zur Liste")


for t in m["teilkacheln"]:
    tk, k = t["id"], t["kern_im_bild"]
    labels = tifffile.imread(H0 / "vorstufe" / tk / "labels.tif")
    seg = json.loads((H0 / "vorstufe" / tk / "segmente.json").read_text(encoding="utf-8"))
    im_kern = {s["id"] for s in seg["segmente"] if s.get("im_kern")}
    kern_gesamt += len(im_kern)
    im_kern_karte = set(np.unique(labels[k["y"]:k["y"] + k["hoehe"], k["x"]:k["x"] + k["breite"]]).tolist())
    if im_kern != im_kern_karte:
        maengel.append(f"{tk}: im_kern passt nicht zur Karte")
    # Kopien B und C bytegleich zur Vorstufe
    kopien = [H0 / f / tk for f in ("b-kategorien-frei", "c-feste-liste")]
    if tk == "r0c0":
        kopien.append(H0 / "c-feste-liste" / "gegenprobe" / "r0c0")
    for ordner in kopien:
        for name in ("labels.tif", "segmente.json", "kandidaten.json"):
            if sha(ordner / name) != sha(H0 / "vorstufe" / tk / name):
                maengel.append(f"{ordner}/{name} nicht bytegleich zur Vorstufe")
        if not np.array_equal(tifffile.imread(ordner / "labels.tif"), labels):
            maengel.append(f"{ordner}/labels.tif nicht bildpunktgleich")
    hb, hh = k["breite"] // 2, k["hoehe"] // 2
    vr = {1: (k["x"], k["y"], hb, hh), 2: (k["x"] + hb, k["y"], k["breite"] - hb, hh),
          3: (k["x"], k["y"] + hh, hb, k["hoehe"] - hh), 4: (k["x"] + hb, k["y"] + hh, k["breite"] - hb, k["hoehe"] - hh)}
    for fassung in ("c", "b"):
        vs = sorted((e for e in plan["viertel"] if e["fassung"] == fassung and e["teilkachel"] == tk), key=lambda e: e["viertel"])
        if [e["viertel"] for e in vs] != [1, 2, 3, 4]:
            maengel.append(f"{fassung} {tk}: Viertel {[e['viertel'] for e in vs]}")
            continue
        alle = [sid for e in vs for sid in e["segmente"]]
        if sorted(alle) != sorted(im_kern):
            maengel.append(f"{fassung} {tk}: Segmente doppelt/fehlend/fremd")
        for e in vs:
            for sid in e["segmente"]:
                anteil = {n: int((labels[y:y + h, x:x + b] == sid).sum()) for n, (x, y, b, h) in vr.items()}
                bester = max(anteil, key=lambda n: (anteil[n], -n))
                if bester != e["viertel"]:
                    maengel.append(f"{fassung} {tk}: {sid} in v{e['viertel']}, größter Anteil in v{bester}")
            auftrag_ok(e["auftrag"], e["segmente"], (H0 / ("c-feste-liste" if fassung == "c" else "b-kategorien-frei") / tk).as_posix())
            bilder = Path(e["bilder"])
            if len(list(bilder.glob("*.jpg"))) != 14 or not (bilder / "viertel.json").exists():
                maengel.append(f"{bilder}: nicht 14 JPEG + viertel.json")
            if any(Path(e["ergebnis"]).iterdir()):
                maengel.append(f"Ergebnisordner nicht leer: {e['ergebnis']}")
        zahlen[f"{fassung} {tk}"] = (len(im_kern), [len(e["segmente"]) for e in vs])
    for name in ("ganz_nummern.jpg", "ganz_roh.jpg", "ganz.json"):
        if not (H0 / "ganz" / tk / name).exists():
            maengel.append(f"ganz/{tk}/{name} fehlt")
for e in plan["frei_a"] + [plan["gegenprobe_a_alternative"]]:
    auftrag_ok(e["auftrag"])
    if any(Path(e["ergebnis"]).iterdir()):
        maengel.append(f"Ergebnisordner nicht leer: {e['ergebnis']}")
for e in plan["frei_a"]:
    if not (Path(e["bilder"]) / "ansicht.json").exists():
        maengel.append(f"ansicht für A fehlt: {e['bilder']}")
for e in plan["gegenprobe"]:
    auftrag_ok(e["auftrag"], e["segmente"], (H0 / "c-feste-liste" / "gegenprobe" / "r0c0").as_posix())
    if any(Path(e["ergebnis"]).iterdir()):
        maengel.append(f"Ergebnisordner nicht leer: {e['ergebnis']}")
    if "Unabhängig urteilen" not in Path(e["auftrag"]).read_text(encoding="utf-8"):
        maengel.append(f"Gegenprobe ohne Abschnitt: {e['auftrag']}")
ver = Path(plan["vereinheitlichung_b"]["auftrag"]).read_text(encoding="utf-8")
if ver.count("| `r") != 16:
    maengel.append("Vereinheitlichung nennt nicht 16 Viertel")
arten = {}
for e in plan["einheiten"]:
    arten[e["art"]] = arten.get(e["art"], 0) + 1
if arten != {"c": 16, "b": 16, "a": 4, "z": 4}:
    maengel.append(f"Einheiten {arten}")
if kern_gesamt > 800:
    maengel.append(f"Kernsegmente {kern_gesamt} > 800")
for name in ("vorstufe-fein", "viertel-fein", "ganz-fein", "a-alles-frei-fein", "b-kategorien-frei-fein", "c-feste-liste-fein"):
    if not (H0 / name).is_dir():
        maengel.append(f"feine Fassung fehlt: {name}")

# pruefe_urteil.py: gültiges Beispiel -> 0, ein Segment fehlt -> 1, ohne Übersicht -> 1
e = next(g for g in plan["viertel"] if g["fassung"] == "c" and g["teilkachel"] == "r1c0" and g["viertel"] == 4)
bilder = e["bilder"]
urteil = {"teilkachel": "r1c0", "viertel": "v4", "bearbeiter": "probe",
          "bilder_angesehen": {"uebersicht": [f"{bilder}/uebersicht_nummern.jpg"], "nah": [f"{bilder}/nah1_nummern.jpg"]},
          "segmente": [{"id": sid, "klasse_heute": None, "klasse_vorschlag": None, "sicher": False, "sauber": True,
                        "was_ist_es": "Probe", "bilder": [f"{bilder}/uebersicht_nummern.jpg"]} for sid in e["segmente"]],
          "unsicher": [], "nicht_geprueft": [], "offen": [], "eingriffe": []}
seg_pfad = H0 / "c-feste-liste" / "r1c0" / "segmente.json"
proben = {}
with tempfile.TemporaryDirectory() as tmp:
    for name, u in (("gueltig", urteil), ("fehlt", {**urteil, "segmente": urteil["segmente"][:-1]}),
                    ("ohne_uebersicht", {**urteil, "bilder_angesehen": {"uebersicht": [], "nah": []}})):
        pf = Path(tmp) / f"{name}.json"
        pf.write_text(json.dumps(u), encoding="utf-8")
        r = subprocess.run([PY, "-I", str(D / "skripte" / "pruefe_urteil.py"), "--urteil", str(pf), "--segmente", str(seg_pfad),
                            "--fassung", "c", "--viertel", "v4", "--ids", ",".join(map(str, e["segmente"])),
                            "--kategorien", str(BASIS / "landseg" / "kategorien.json")], capture_output=True, text=True)
        proben[name] = r.returncode
        if name == "gueltig" and r.returncode:
            print(r.stdout[-600:], r.stderr[-600:])
    import shutil
    kopie = Path(tmp) / "karte"
    kopie.mkdir()
    for name in ("labels.tif", "segmente.json"):
        shutil.copy2(H0 / "c-feste-liste" / "r1c0" / name, kopie / name)
    lab = tifffile.imread(kopie / "labels.tif")
    ziel_id = max(e["segmente"], key=lambda s: int((lab == s).sum()))
    ys, xs = np.nonzero(lab == ziel_id)
    xm = int(np.median(xs))
    (Path(tmp) / "erg").mkdir()
    (Path(tmp) / "erg" / "eingriffe.json").write_text(json.dumps(
        {"schritte": [{"op": "teilen", "id": ziel_id, "linie": [[xm, int(ys.min()) - 1], [xm, int(ys.max()) + 1]]}]}), encoding="utf-8")
    r = subprocess.run([plan["py"], "-B", "-m", "landseg", "eingriff", "--labels", str(kopie / "labels.tif"),
                        "--segmente", str(kopie / "segmente.json"), "--bearbeiter", "probe", "stapel",
                        "--datei", str(Path(tmp) / "erg" / "eingriffe.json")], cwd=REPO, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    proben["eingriff_rc"] = r.returncode
    seg_neu = json.loads((kopie / "segmente.json").read_text(encoding="utf-8"))
    neu = sorted({s["id"] for s in seg_neu["segmente"]} - {s["id"] for s in json.loads(seg_pfad.read_text(encoding="utf-8"))["segmente"]})
    proben["neue_ids"] = len(neu)
    eintrag = urteil["segmente"][0]
    u2 = {**urteil, "segmente": urteil["segmente"] + [{**eintrag, "id": i} for i in neu],
          "eingriffe": [{"schritt": "teilen", "vorher": [ziel_id], "nachher": [ziel_id] + neu, "grund": "Probe"}]}
    for name, u in (("eingriff_gueltig", u2), ("eingriff_neu_fehlt", {**u2, "segmente": urteil["segmente"]}),
                    ("eingriff_ohne_liste", {k: v for k, v in u2.items() if k != "eingriffe"})):
        pf = Path(tmp) / "erg" / "urteil.json"
        pf.write_text(json.dumps(u), encoding="utf-8")
        r = subprocess.run([PY, "-I", str(D / "skripte" / "pruefe_urteil.py"), "--urteil", str(pf), "--segmente",
                            str(kopie / "segmente.json"), "--fassung", "c", "--viertel", "v4", "--ids",
                            ",".join(map(str, e["segmente"])), "--kategorien", str(BASIS / "landseg" / "kategorien.json")],
                           capture_output=True, text=True)
        proben[name] = r.returncode
        if name == "eingriff_gueltig" and r.returncode:
            print(r.stdout[-800:], r.stderr[-400:])
if proben != {"gueltig": 0, "fehlt": 1, "ohne_uebersicht": 1, "eingriff_rc": 0, "neue_ids": proben.get("neue_ids") or -1,
              "eingriff_gueltig": 0, "eingriff_neu_fehlt": 1, "eingriff_ohne_liste": 1}:
    maengel.append(f"pruefe_urteil-Probe {proben}")
print("Kernsegmente gesamt:", kern_gesamt)
print("Zahlen (Kern, je Viertel):", json.dumps(zahlen))
print("pruefe_urteil-Probe:", proben)
print("\n".join(maengel[:40]) if maengel else "ok")
sys.exit(1 if maengel else 0)
