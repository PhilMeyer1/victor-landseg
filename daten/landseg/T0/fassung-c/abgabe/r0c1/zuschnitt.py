"""Crop zoomed views (2x) of the teilkachel: numbered vorstufe view and raw view, 3x3 overlapping windows."""
import sys
from PIL import Image

G = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/ganz/r0c1"
O = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c/abgabe/r0c1/sicht"
import os
os.makedirs(O, exist_ok=True)
src = {"n": Image.open(f"{G}/ganz_nummern.jpg"), "r": Image.open(f"{G}/ganz_roh.jpg")}
# windows in teilkachel px (x0, y0), size 260 -> 520 px at 2x
for name, im in src.items():
    for r, y0 in enumerate([0, 184, 368]):
        for c, x0 in enumerate([0, 184, 368]):
            crop = im.crop((2 * x0, 2 * y0, 2 * (x0 + 260), 2 * (y0 + 260)))
            crop.save(f"{O}/{name}_{r}{c}.jpg", quality=92)
print("ok")
