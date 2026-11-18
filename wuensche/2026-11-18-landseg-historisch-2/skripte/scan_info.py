"""Kopfdaten des 1968er Scans und Vorschaubilder des Fensters H0 (nur lesen).

Aufruf: PY -I scan_info.py <BASIS> <D>
Schreibt D/vorschau/scan_1968_klein.jpg (ganzer Scan verkleinert, Fenster H0 rot) und
D/vorschau/h0_umgebung.jpg (Fenster mit 500 px Umgebung, halbe Größe).
"""
import sys
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image, ImageDraw

BASIS = Path(sys.argv[1])
D = Path(sys.argv[2])
SCAN = BASIS / "daten" / "luftbilder" / "historisch" / "1968105_0014_0228.tif"
X, Y, B, H = 1500, 2000, 1000, 1000

with tifffile.TiffFile(SCAN) as tif:
    s = tif.pages[0]
    print("Form", s.shape, s.dtype, "photometric", s.photometric, "compression", s.compression,
          "gekachelt", s.is_tiled, "Seiten", len(tif.pages))
    for tag in s.tags.values():
        if tag.code in (282, 283, 296, 33550, 33922, 34735, 305, 306, 270):
            print("Tag", tag.code, tag.name, str(tag.value)[:120])
try:
    daten = tifffile.memmap(SCAN, page=0, mode="r")
except ValueError:
    daten = tifffile.imread(SCAN)
h, w = daten.shape[:2]
schritt = 16
klein = np.ascontiguousarray(daten[::schritt, ::schritt])
bild = Image.fromarray(klein).convert("RGB")
z = ImageDraw.Draw(bild)
z.rectangle([X // schritt, Y // schritt, (X + B) // schritt, (Y + H) // schritt], outline=(255, 0, 0), width=3)
ziel = D / "vorschau"
ziel.mkdir(parents=True, exist_ok=True)
bild.save(ziel / "scan_1968_klein.jpg", quality=85)
x0, y0 = max(0, X - 500), max(0, Y - 500)
x1, y1 = min(w, X + B + 500), min(h, Y + H + 500)
umg = Image.fromarray(np.ascontiguousarray(daten[y0:y1, x0:x1])).convert("RGB")
z = ImageDraw.Draw(umg)
z.rectangle([X - x0, Y - y0, X - x0 + B, Y - y0 + H], outline=(255, 0, 0), width=4)
umg = umg.resize((umg.width // 2, umg.height // 2))
umg.save(ziel / "h0_umgebung.jpg", quality=85)
fenster = np.asarray(daten[Y:Y + H, X:X + B])
print("Scan", w, "x", h, "Fenster min/mittel/max", int(fenster.min()), round(float(fenster.mean()), 1),
      int(fenster.max()))
