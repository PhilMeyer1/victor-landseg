"""Zoom crop with coordinate grid. usage: zoom.py x0 y0 w h scale out [labels.tif]"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import tifffile

BILD = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r0c1.png"
x0, y0, w, h, s = map(int, sys.argv[1:6])
out = sys.argv[6]
lab = sys.argv[7] if len(sys.argv) > 7 else None
a = np.array(Image.open(BILD)).astype(np.float32)
c = a[y0:y0 + h, x0:x0 + w]
lo, hi = np.percentile(c, 1), np.percentile(c, 99)
c = np.clip((c - lo) / (hi - lo) * 255, 0, 255).astype(np.uint8)
im = Image.fromarray(c).resize((w * s, h * s), Image.NEAREST).convert("RGB")
if lab:
    L = tifffile.imread(lab)[y0:y0 + h, x0:x0 + w]
    Lb = np.kron(L, np.ones((s, s), dtype=L.dtype))
    edge = np.zeros(Lb.shape, bool)
    edge[:, 1:] |= Lb[:, 1:] != Lb[:, :-1]
    edge[1:, :] |= Lb[1:, :] != Lb[:-1, :]
    arr = np.array(im)
    arr[edge] = (255, 255, 0)
    im = Image.fromarray(arr)
d = ImageDraw.Draw(im)
try:
    f = ImageFont.truetype("arial.ttf", 13)
except Exception:
    f = ImageFont.load_default()
step = 25
for gx in range((x0 // step + 1) * step, x0 + w, step):
    X = (gx - x0) * s
    d.line([(X, 0), (X, h * s)], fill=(0, 200, 255) if gx % 100 else (255, 60, 60), width=1)
    d.text((X + 2, 2), str(gx), fill=(0, 255, 255), font=f)
for gy in range((y0 // step + 1) * step, y0 + h, step):
    Y = (gy - y0) * s
    d.line([(0, Y), (w * s, Y)], fill=(0, 200, 255) if gy % 100 else (255, 60, 60), width=1)
    d.text((2, Y + 2), str(gy), fill=(0, 255, 255), font=f)
if lab and len(sys.argv) > 8:
    L = tifffile.imread(lab)
    for i in np.unique(L[y0:y0 + h, x0:x0 + w]):
        ys, xs = np.nonzero(L[y0:y0 + h, x0:x0 + w] == i)
        if len(ys) < 15:
            continue
        cy, cx = np.median(ys), np.median(xs)
        # choose point inside
        k = np.argmin((ys - cy) ** 2 + (xs - cx) ** 2)
        d.text((xs[k] * s - 6, ys[k] * s - 6), str(i), fill=(255, 0, 255), font=f)
im.save(out, quality=90)
