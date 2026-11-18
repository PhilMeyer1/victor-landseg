# Crop helper: crop.py out.jpg x0 y0 w h faktor [kontrast] [labels]
import sys, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import tifffile
B = "C:/Users/Phil/Developement/Victor/daten/landseg/H0"
out, x0, y0, w, h, f = sys.argv[1], *map(int, sys.argv[2:7])
mode = sys.argv[7] if len(sys.argv) > 7 else "roh"
img = np.array(Image.open(B + "/teilkacheln/r1c0.png").convert("L")).astype(float)
lab = tifffile.imread(B + "/b-kategorien-frei/r1c0/labels.tif")
c = img[y0:y0+h, x0:x0+w]
if "kontrast" in mode:
    lo, hi = np.percentile(c, 2), np.percentile(c, 98)
    c = np.clip((c - lo) / max(hi - lo, 1) * 255, 0, 255)
rgb = np.stack([c]*3, -1).astype(np.uint8)
rgb = np.kron(rgb, np.ones((f, f, 1), dtype=np.uint8))
im = Image.fromarray(rgb)
d = ImageDraw.Draw(im)
if "lab" in mode:
    L = lab[y0:y0+h, x0:x0+w]
    Lb = np.kron(L, np.ones((f, f), dtype=L.dtype))
    e = np.zeros(Lb.shape, bool)
    e[:, 1:] |= Lb[:, 1:] != Lb[:, :-1]
    e[1:, :] |= Lb[1:, :] != Lb[:-1, :]
    a = np.array(im); a[e] = [255, 255, 0]; im = Image.fromarray(a); d = ImageDraw.Draw(im)
    for i in np.unique(L):
        ys, xs = np.nonzero(L == i)
        if len(xs) > 20:
            k = len(xs)//2
            o = np.argsort(ys*10000+xs)[k]
            d.text((xs[o]*f, ys[o]*f), str(i % 100000), fill=(255, 255, 255))
# grid ticks every 10 px
for gx in range((x0//10+1)*10, x0+w, 10):
    X = (gx-x0)*f
    d.line([(X, 0), (X, 6 if gx % 50 else 14)], fill=(0, 255, 255))
    if gx % 50 == 0: d.text((X+2, 14), str(gx), fill=(0, 255, 255))
for gy in range((y0//10+1)*10, y0+h, 10):
    Y = (gy-y0)*f
    d.line([(0, Y), (6 if gy % 50 else 14, Y)], fill=(0, 255, 255))
    if gy % 50 == 0: d.text((16, Y-6), str(gy), fill=(0, 255, 255))
im.save(out, quality=90)
print(im.size, img.shape, lab.shape)
