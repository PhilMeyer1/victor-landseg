"""Unabhängige Prüfung von Teil 2 (H0): Viertel, Bilder, Aufträge, Kopien, Ergebnisordner, pruefe_urteil.

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

BASIS, D = Path(sys.argv[1]), Path(sys.argv[2])
H0 = BASIS / "daten" / "landseg" / "H0"
PY = sys.executable
plan = json.loads((D / "auftraege.json").read_text(encoding="utf-8"))
m = json.loads((H0 / "manifest.json").read_text(encoding="utf-8"))
maengel, zahlen = [], {}


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def auftrag_ok(pfad: str, ids=None):
    t = Path(pfad).read_text(encoding="utf-8")
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
    im_kern_karte = set(np.unique(labels[k["y"]:k["y"] + k["hoehe"], k["x"]:k["x"] + k["breite"]]).tolist())
    if im_kern != im_kern_karte:
        maengel.append(f"{tk}: im_kern passt nicht zur Karte")
    # Kopien B und C bytegleich zur Vorstufe
    for f in ("b-kategorien-frei", "c-feste-liste"):
        for name in ("labels.tif", "segmente.json", "kandidaten.json"):
            if sha(H0 / f / tk / name) != sha(H0 / "vorstufe" / tk / name):
                maengel.append(f"{f}/{tk}/{name} nicht bytegleich zur Vorstufe")
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
            auftrag_ok(e["auftrag"], e["segmente"])
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
    auftrag_ok(e["auftrag"], e["segmente"])
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

# pruefe_urteil.py: gültiges Beispiel -> 0, ein Segment fehlt -> 1, ohne Übersicht -> 1
e = next(g for g in plan["viertel"] if g["fassung"] == "c" and g["teilkachel"] == "r1c0" and g["viertel"] == 4)
bilder = e["bilder"]
urteil = {"teilkachel": "r1c0", "viertel": "v4", "bearbeiter": "probe",
          "bilder_angesehen": {"uebersicht": [f"{bilder}/uebersicht_nummern.jpg"], "nah": [f"{bilder}/nah1_nummern.jpg"]},
          "segmente": [{"id": sid, "klasse_heute": None, "klasse_vorschlag": None, "sicher": False, "sauber": True,
                        "was_ist_es": "Probe", "bilder": [f"{bilder}/uebersicht_nummern.jpg"]} for sid in e["segmente"]],
          "unsicher": [], "nicht_geprueft": [], "offen": []}
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
if proben != {"gueltig": 0, "fehlt": 1, "ohne_uebersicht": 1}:
    maengel.append(f"pruefe_urteil-Probe {proben}")
print("Zahlen (Kern, je Viertel):", json.dumps(zahlen))
print("pruefe_urteil-Probe:", proben)
print("\n".join(maengel[:40]) if maengel else "ok")
sys.exit(1 if maengel else 0)
