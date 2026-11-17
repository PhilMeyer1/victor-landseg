"""Teil 1 von landseg-test-t0: prüft gruppen.json, Aufträge, Viertelbilder und Ergebnisordner.

Aufruf: PY -I pruefe_viertel.py <BASIS> <Berichtsordner D> <Scratch-Ordner>
Geprüft: je Fassung A/B und Teilkachel jedes Kernsegment (im_kern) in genau einem Viertel, keins vom
Kontextrand; jedes Segment im Viertel mit dem größten Anteil (nachgerechnet); Auftrag vorhanden, ohne
übrige Platzhalter, nennt jede ID seines Viertels; Bilderordner mit 14 JPEG und viertel.json; B-Bilder
bytegleich zu A; Ergebnisordner vorhanden und leer; keine Bilder je Segment (Ordner `segmente/`) unter
daten/landseg/T0; Zweitagent und C vollständig; pruefe_urteil.py nimmt ein gültiges Beispiel-Urteil an
und lehnt zwei kaputte ab. Letzte Zeile `ok` oder `FEHLER`.
"""
import filecmp
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import tifffile

BASIS, D, S = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
T0 = BASIS / "daten" / "landseg" / "T0"
PY = sys.executable
plan = json.loads((D / "gruppen.json").read_text(encoding="utf-8"))
maengel = []
BILDER = sorted([f"uebersicht_{a}.jpg" for a in ("nummern", "roh", "vorschlag", "maengel", "kontrast", "gitter")]
                + [f"nah{k}_{a}.jpg" for k in range(1, 5) for a in ("roh", "nummern")])
ORDNER = {"a": "kern500", "b": "fassung-b"}
manifest = json.loads((T0 / "kern500" / "manifest.json").read_text(encoding="utf-8"))
kern = {t["id"]: t["kern_im_bild"] for t in manifest["teilkacheln"]}


def auftrag_pruefen(e):
    a = Path(e["auftrag"])
    if not a.is_file():
        maengel.append(f"Auftrag fehlt: {a}")
        return
    text = a.read_text(encoding="utf-8")
    if "{{" in text:
        maengel.append(f"Platzhalter übrig: {a}")
    for sid in e.get("segmente", []):
        if f"| {sid} |" not in text:
            maengel.append(f"{a}: ID {sid} fehlt in der Liste")


def leer(p: Path, wo):
    if not p.is_dir():
        maengel.append(f"Ergebnisordner fehlt: {wo}")
    elif any(p.iterdir()):
        maengel.append(f"Ergebnisordner nicht leer: {wo}")


zahlen = {}
for fassung, ordner in ORDNER.items():
    for tk, k in kern.items():
        seg = json.loads((T0 / ordner / "vorstufe" / tk / "segmente.json").read_text(encoding="utf-8"))
        labels = tifffile.imread(T0 / ordner / "vorstufe" / tk / "labels.tif")
        im_kern = {s["id"] for s in seg["segmente"] if s.get("im_kern")}
        viertel = [e for e in plan["gruppen"] if e["fassung"] == fassung and e["teilkachel"] == tk]
        if sorted(e["viertel"] for e in viertel) != [1, 2, 3, 4]:
            maengel.append(f"{fassung} {tk}: Viertel {sorted(e['viertel'] for e in viertel)}")
        hb, hh = k["breite"] // 2, k["hoehe"] // 2
        rechtecke = {1: (k["x"], k["y"], hb, hh), 2: (k["x"] + hb, k["y"], k["breite"] - hb, hh),
                     3: (k["x"], k["y"] + hh, hb, k["hoehe"] - hh),
                     4: (k["x"] + hb, k["y"] + hh, k["breite"] - hb, k["hoehe"] - hh)}
        gezaehlt = {}
        for e in viertel:
            for sid in e["segmente"]:
                gezaehlt[sid] = gezaehlt.get(sid, 0) + 1
                anteile = {n: int((labels[y:y + h, x:x + b] == sid).sum()) for n, (x, y, b, h) in rechtecke.items()}
                bester = max(anteile, key=lambda n: (anteile[n], -n))
                if bester != e["viertel"]:
                    maengel.append(f"{fassung} {tk}: {sid} in v{e['viertel']}, größter Anteil in v{bester}")
            auftrag_pruefen(e)
            b = Path(e["bilder"])
            da = sorted(x.name for x in b.glob("*.jpg"))
            if da != BILDER or not (b / "viertel.json").is_file():
                maengel.append(f"Bilder unvollständig: {b} ({len(da)} JPEG)")
            if fassung == "b":
                a_b = T0 / "kern500" / "viertel" / tk / f"v{e['viertel']}"
                for name in BILDER + ["viertel.json"]:
                    if not filecmp.cmp(a_b / name, b / name, shallow=False):
                        maengel.append(f"B-Bild nicht bytegleich zu A: {b / name}")
            leer(Path(e["ergebnis"]), e["ergebnis"])
        doppelt = sorted(s for s, n in gezaehlt.items() if n > 1)
        fehlt = sorted(im_kern - set(gezaehlt))
        fremd = sorted(set(gezaehlt) - im_kern)
        if doppelt or fehlt or fremd:
            maengel.append(f"{fassung} {tk}: doppelt {doppelt}, fehlt {fehlt}, Kontextrand/fremd {fremd}")
        zahlen[f"{fassung} {tk}"] = (len(im_kern), [len(e["segmente"]) for e in sorted(viertel, key=lambda e: e["viertel"])])

zw = plan["zweitagent"]
if sorted(e["viertel"] for e in zw) != [1, 2, 3, 4]:
    maengel.append("Zweitagent: nicht vier Viertel")
for e in zw:
    auftrag_pruefen(e)
    leer(Path(e["ergebnis"]), e["ergebnis"])
    erst = next(g for g in plan["gruppen"] if g["fassung"] == "a" and g["teilkachel"] == e["teilkachel"]
                and g["viertel"] == e["viertel"])
    if erst["segmente"] != e["segmente"]:
        maengel.append(f"Zweitagent v{e['viertel']}: andere Segmente als das Erst-Urteil")
    if "Unabhängig urteilen" not in Path(e["auftrag"]).read_text(encoding="utf-8"):
        maengel.append(f"Zweitagent v{e['viertel']}: Abschnitt „Unabhängig urteilen“ fehlt")
if len(plan["frei_c"]) != 4:
    maengel.append("C: nicht vier Aufträge")
for e in plan["frei_c"]:
    auftrag_pruefen(e)
    leer(Path(e["ergebnis"]), e["ergebnis"])
    if not (Path(e["bilder"]) / "ansicht.json").is_file() or (Path(e["bilder"]) / "segmente").exists():
        maengel.append(f"C-Bilder: {e['bilder']}")
vb = plan["vereinheitlichung_b"]
auftrag_pruefen(vb)
leer(Path(vb["ergebnis"]), vb["ergebnis"])
einzel = [p for p in T0.rglob("segmente") if p.is_dir()]
if einzel:
    maengel.append(f"Bilder je Segment vorhanden: {[str(p) for p in einzel][:5]}")

# Probe für pruefe_urteil.py an Viertel A r1c0 v2
e = next(g for g in plan["gruppen"] if g["fassung"] == "a" and g["teilkachel"] == "r1c0" and g["viertel"] == 2)
b = Path(e["bilder"])
gut = {"teilkachel": "r1c0", "viertel": "v2", "bearbeiter": "probe",
       "bilder_angesehen": {"uebersicht": [str(b / "uebersicht_nummern.jpg")], "nah": [str(b / "nah1_roh.jpg")]},
       "segmente": [{"id": sid, "klasse_heute": "3.1", "was_ist_es": "x", "urteil": "sauber",
                     "klasse_vorschlag": None, "sicher": True, "punkte": [],
                     "bilder": [str(b / "uebersicht_nummern.jpg")]} for sid in e["segmente"]],
       "naht": [], "unsicher": [], "nicht_geprueft": [], "offen": []}
schlecht1 = dict(gut, bilder_angesehen={"uebersicht": [], "nah": []})
schlecht2 = dict(gut, segmente=gut["segmente"][1:])
S.mkdir(parents=True, exist_ok=True)
seg_pfad = T0 / "kern500" / "vorstufe" / "r1c0" / "segmente.json"
probe = {}
for name, u in (("gut", gut), ("ohne_uebersicht", schlecht1), ("segment_fehlt", schlecht2)):
    pf = S / f"probe-{name}.json"
    pf.write_text(json.dumps(u, ensure_ascii=False), encoding="utf-8")
    r = subprocess.run([PY, "-I", str(D / "skripte" / "pruefe_urteil.py"), "--urteil", str(pf), "--segmente",
                        str(seg_pfad), "--fassung", "a", "--viertel", "v2", "--ids",
                        ",".join(str(i) for i in e["segmente"]),
                        "--kategorien", str(BASIS / "landseg" / "kategorien.json")],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    probe[name] = r.returncode
if probe != {"gut": 0, "ohne_uebersicht": 1, "segment_fehlt": 1}:
    maengel.append(f"pruefe_urteil.py Probe: {probe}")

sys.stdout.reconfigure(encoding="utf-8")
for k, (n, je) in zahlen.items():
    print(f"{k}: {n} Kernsegmente, je Viertel {je}")
print(f"Viertel-Aufträge: {len(plan['gruppen'])}, Zweitagent: {len(zw)}, C: {len(plan['frei_c'])}, "
      f"Vereinheitlichung B: 1, Probe pruefe_urteil: {probe}")
for m in maengel[:40]:
    print("- " + m)
print("ok" if not maengel else "FEHLER")
sys.exit(0 if not maengel else 1)
