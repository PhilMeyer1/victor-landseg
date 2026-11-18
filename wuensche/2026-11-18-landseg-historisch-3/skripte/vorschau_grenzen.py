"""H0 mit den Segmentgrenzen der Vorstufe (Kerne zusammengesetzt), 1000 × 1000, und Klassenfarben.

Aufruf: PY -I vorschau_grenzen.py <BASIS> <D>
Schreibt D/vorschau/h0_vorstufe_grenzen.jpg und D/vorschau/h0_vorstufe_klassen.jpg (nur zum Ansehen).
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

BASIS, D = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(BASIS / "landseg"))
from landseg import dateien, kategorien  # noqa: E402
from landseg.ansicht import grenzen  # noqa: E402

H0 = BASIS / "daten" / "landseg" / "H0"
KAT = kategorien.laden(BASIS / "landseg" / "kategorien.json")
m = json.loads((H0 / "manifest.json").read_text(encoding="utf-8"))
B, H = m["ausschnitt"]["breite"], m["ausschnitt"]["hoehe"]
grau = np.asarray(Image.open(H0 / m["ausschnitt"]["bild"]).convert("RGB")).copy()
karte = np.zeros((H, B), np.uint32)
farbe = np.zeros((H, B, 3), np.uint8)
for t in m["teilkacheln"]:
    k, ki = t["kern"], t["kern_im_bild"]
    lab = dateien.lese_labels(H0 / "vorstufe" / t["id"] / "labels.tif")
    seg = dateien.segmente_nach_id(dateien.lese_segmente(H0 / "vorstufe" / t["id"] / "segmente.json"))
    teil = lab[ki["y"]:ki["y"] + ki["hoehe"], ki["x"]:ki["x"] + ki["breite"]]
    karte[k["y"]:k["y"] + k["hoehe"], k["x"]:k["x"] + k["breite"]] = teil
    lut = {sid: KAT.klassen[e["klasse"]].get("color", "#ff00ff") if KAT.gueltig(e.get("klasse")) else "#ff00ff" for sid, e in seg.items()}
    for sid, hexf in lut.items():
        rgb = tuple(int(hexf.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
        farbe[k["y"]:k["y"] + k["hoehe"], k["x"]:k["x"] + k["breite"]][teil == sid] = rgb
rand = grenzen(karte)
g = grau.copy()
g[rand] = (255, 235, 60)
g[499:501, :] = (0, 255, 255)
g[:, 499:501] = (0, 255, 255)
ziel = D / "vorschau"
ziel.mkdir(parents=True, exist_ok=True)
Image.fromarray(g).save(ziel / "h0_vorstufe_grenzen.jpg", quality=88)
k = (0.55 * grau + 0.45 * farbe).astype(np.uint8)
k[rand] = (255, 255, 255)
Image.fromarray(k).save(ziel / "h0_vorstufe_klassen.jpg", quality=88)
print("ok", ziel.as_posix())
