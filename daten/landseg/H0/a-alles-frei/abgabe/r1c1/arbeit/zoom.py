"""Vergrößerte Ausschnitte der Teilkachel mit Koordinatengitter (Teilkachel-Bildpunkte).

Aufruf: zoom.py x0 y0 x1 y1 faktor ausgabe.jpg [labels.tif]
"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BILD = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r1c1.png"

x0, y0, x1, y1, f = map(int, sys.argv[1:6])
aus = sys.argv[6]
lab = sys.argv[7] if len(sys.argv) > 7 else None

img = np.array(Image.open(BILD).convert("L")).astype(np.float32)
crop = img[y0:y1, x0:x1]
# leichte Kontrastspreizung
lo, hi = np.percentile(crop, 1), np.percentile(crop, 99)
crop = np.clip((crop - lo) / max(hi - lo, 1) * 255, 0, 255).astype(np.uint8)
big = Image.fromarray(crop).resize(((x1 - x0) * f, (y1 - y0) * f), Image.NEAREST).convert("RGB")
d = ImageDraw.Draw(big)
try:
    font = ImageFont.truetype("arial.ttf", 13)
except Exception:
    font = ImageFont.load_default()

if lab:
    import tifffile
    L = tifffile.imread(lab)[y0:y1, x0:x1]
    rand = np.zeros_like(L, dtype=bool)
    rand[:, 1:] |= L[:, 1:] != L[:, :-1]
    rand[1:, :] |= L[1:, :] != L[:-1, :]
    ys, xs = np.nonzero(rand)
    for yy, xx in zip(ys, xs):
        d.rectangle([xx * f, yy * f, xx * f + f - 1, yy * f + f - 1], outline=(255, 230, 0))

step = 25
for gx in range((x0 // step + 1) * step, x1, step):
    px = (gx - x0) * f
    col = (0, 200, 255) if gx % 50 == 0 else (0, 110, 150)
    d.line([px, 0, px, big.height], fill=col, width=1)
    if gx % 50 == 0:
        d.text((px + 2, 2), str(gx), fill=(255, 80, 80), font=font)
for gy in range((y0 // step + 1) * step, y1, step):
    py = (gy - y0) * f
    col = (0, 200, 255) if gy % 50 == 0 else (0, 110, 150)
    d.line([0, py, big.width, py], fill=col, width=1)
    if gy % 50 == 0:
        d.text((2, py + 2), str(gy), fill=(255, 80, 80), font=font)
# Kern
kx0, ky0, kx1, ky1 = 64, 64, 564, 564
d.rectangle([(kx0 - x0) * f, (ky0 - y0) * f, (kx1 - x0) * f, (ky1 - y0) * f], outline=(255, 0, 255), width=2)
big.save(aus, quality=90)
print(aus, big.size)
