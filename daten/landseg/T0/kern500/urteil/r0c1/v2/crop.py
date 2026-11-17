"""Eigene Nahansicht: Ausschnitt x0 y0 w h faktor ziel [hervorheben-ids]."""
import json
import sys
import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont

BASIS = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500"
lab = tifffile.imread(f"{BASIS}/vorstufe/r0c1/labels.tif").astype(np.int64)
man = json.load(open(f"{BASIS}/manifest.json", encoding="utf-8"))
tk = [t for t in man["teilkacheln"] if "r0c1" in (t.get("name"), t.get("id"))][0]
img = np.asarray(Image.open(f"{BASIS}/{tk['bild']}").convert("RGB"))
x0, y0, w, h, f = map(int, sys.argv[1:6])
ziel = sys.argv[6]
hl = [int(v) for v in sys.argv[7].split(",")] if len(sys.argv) > 7 and sys.argv[7] else []
kontrast = len(sys.argv) > 8 and sys.argv[8] == "k"
sub = img[y0:y0 + h, x0:x0 + w].astype(float)
if kontrast:
    lo, hi = np.percentile(sub, 2), np.percentile(sub, 98)
    sub = np.clip((sub - lo) / (hi - lo) * 255, 0, 255)
L = lab[y0:y0 + h, x0:x0 + w]
big = np.kron(sub, np.ones((f, f, 1))).astype(np.uint8)
Lb = np.kron(L, np.ones((f, f), dtype=np.int64))
edge = np.zeros(Lb.shape, bool)
edge[:-1, :] |= Lb[:-1, :] != Lb[1:, :]
edge[:, :-1] |= Lb[:, :-1] != Lb[:, 1:]
out = big.copy()
for i in hl:
    m = Lb == i
    out[m] = (out[m] * 0.6 + np.array([255, 0, 255]) * 0.4).astype(np.uint8)
out[edge] = [255, 255, 0]
im = Image.fromarray(out)
d = ImageDraw.Draw(im)
try:
    font = ImageFont.truetype("arial.ttf", 16)
except Exception:
    font = ImageFont.load_default()
for i in np.unique(L):
    ys, xs = np.nonzero(L == i)
    if len(xs) < 4:
        continue
    cy, cx = int(np.median(ys)), int(np.median(xs))
    if L[cy, cx] != i:
        k = np.argmin((ys - cy) ** 2 + (xs - cx) ** 2)
        cy, cx = ys[k], xs[k]
    t = str(i % 100000)
    d.text((cx * f - 8 + 1, cy * f - 8 + 1), t, fill=(0, 0, 0), font=font)
    d.text((cx * f - 8, cy * f - 8), t, fill=(255, 255, 255), font=font)
# Gitter-Beschriftung alle 10 px
for gx in range((x0 // 10 + 1) * 10, x0 + w, 10):
    d.text(((gx - x0) * f + 2, 2), str(gx), fill=(0, 255, 255), font=font)
    d.line([((gx - x0) * f, 0), ((gx - x0) * f, 10)], fill=(0, 255, 255))
for gy in range((y0 // 10 + 1) * 10, y0 + h, 10):
    d.text((2, (gy - y0) * f + 2), str(gy), fill=(0, 255, 255), font=font)
    d.line([(0, (gy - y0) * f), (10, (gy - y0) * f)], fill=(0, 255, 255))
im.save(ziel, quality=90)
print(ziel, im.size)
