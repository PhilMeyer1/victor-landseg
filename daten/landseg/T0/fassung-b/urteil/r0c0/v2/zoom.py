"""Eigene Nahansichten mit Grenzen und IDs (nur lesen, schreibt nur in diesen Ordner).
Aufruf: zoom.py <name> <x0> <y0> <breite> <hoehe> <faktor> [roh]
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASIS = Path("C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b")
AUS = BASIS / "urteil/r0c0/v2"
bild = np.array(Image.open(BASIS / "teilkacheln/r0c0.png").convert("RGB"))
lab = np.array(Image.open(BASIS / "vorstufe/r0c0/labels.tif")).astype(np.int64)

name, x0, y0, w, h, f = sys.argv[1], *map(int, sys.argv[2:7])
roh = len(sys.argv) > 7 and sys.argv[7] == "roh"
kontrast = len(sys.argv) > 7 and sys.argv[7] == "kontrast"
crop = bild[y0:y0 + h, x0:x0 + w].astype(np.float64)
if kontrast:
    lo, hi = np.percentile(crop, 2), np.percentile(crop, 98)
    crop = np.clip((crop - lo) / max(hi - lo, 1) * 255, 0, 255)
crop = crop.astype(np.uint8)
L = lab[y0:y0 + h, x0:x0 + w]
big = np.kron(crop, np.ones((f, f, 1), dtype=np.uint8))
if not roh:
    Lb = np.kron(L, np.ones((f, f), dtype=np.int64))
    edge = np.zeros(Lb.shape, bool)
    edge[:, 1:] |= Lb[:, 1:] != Lb[:, :-1]
    edge[1:, :] |= Lb[1:, :] != Lb[:-1, :]
    big[edge] = (255, 255, 0)
im = Image.fromarray(big)
d = ImageDraw.Draw(im)
try:
    font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 13)
except Exception:
    font = ImageFont.load_default()
# Kern / Viertel
def rect(x1, y1, x2, y2, col):
    d.rectangle([(x1 - x0) * f, (y1 - y0) * f, (x2 - x0) * f - 1, (y2 - y0) * f - 1], outline=col, width=2)
rect(314, 64, 564, 314, (0, 255, 255))
if not roh:
    from scipy import ndimage  # noqa
for sid in np.unique(L) if not roh else []:
    ys, xs = np.nonzero(L == sid)
    if len(xs) < 3:
        continue
    m = (L == sid)
    try:
        from scipy import ndimage
        dist = ndimage.distance_transform_edt(m)
        iy, ix = np.unravel_index(np.argmax(dist), dist.shape)
    except Exception:
        iy, ix = int(np.median(ys)), int(np.median(xs))
    t = str(sid % 100000)
    px, py = ix * f + f // 2, iy * f + f // 2
    d.text((px - 8, py - 7), t, fill=(0, 0, 0), font=font, stroke_width=2, stroke_fill=(255, 255, 255))
# Achsenmarken alle 10 px
for gx in range((x0 // 10 + 1) * 10, x0 + w, 10):
    d.line([((gx - x0) * f, 0), ((gx - x0) * f, 6)], fill=(255, 0, 255), width=1)
    if gx % 20 == 0:
        d.text(((gx - x0) * f + 1, 6), str(gx), fill=(255, 0, 255), font=font)
for gy in range((y0 // 10 + 1) * 10, y0 + h, 10):
    d.line([(0, (gy - y0) * f), (6, (gy - y0) * f)], fill=(255, 0, 255), width=1)
    if gy % 20 == 0:
        d.text((7, (gy - y0) * f - 7), str(gy), fill=(255, 0, 255), font=font)
im.save(AUS / name, quality=90)
print(AUS / name, im.size)
