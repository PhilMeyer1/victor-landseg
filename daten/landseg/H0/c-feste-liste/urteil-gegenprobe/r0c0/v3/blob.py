"""Schlägt eine geschlossene Teilungslinie für ein helles bzw. dunkles Teilstück eines Segments vor.

blob.py <id> <gt|lt> <schwelle> <ziel.jpg> [roi "x,y;x,y;..."] [sigma] [oeffnen]
Gibt die Linie als JSON aus (für teilen im Stapel) und schreibt eine Vorschau (Kontur rot).
"""
import json
import sys

import cv2
import numpy as np
import tifffile
from PIL import Image
from scipy import ndimage

B = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/"
img0 = np.array(Image.open(B + "teilkacheln/r0c0.png").convert("L"))
lab = tifffile.imread(B + "c-feste-liste/gegenprobe/r0c0/labels.tif")

sid = int(sys.argv[1])
art, t, ziel = sys.argv[2], float(sys.argv[3]), sys.argv[4]
roi = sys.argv[5] if len(sys.argv) > 5 and sys.argv[5] != "-" else None
sigma = float(sys.argv[6]) if len(sys.argv) > 6 else 1.0
oeff = int(sys.argv[7]) if len(sys.argv) > 7 else 1
img = ndimage.gaussian_filter(img0.astype(float), sigma)
seg = lab == sid
m = seg & ((img > t) if art == "gt" else (img < t))
if roi:
    pts = np.array([[int(v) for v in p.split(",")] for p in roi.split(";")], np.int32)
    r = np.zeros(lab.shape, np.uint8)
    cv2.fillPoly(r, [pts], 1)
    m &= r.astype(bool)
# Kern: nur 64..563
k = np.zeros(lab.shape, bool)
k[64:564, 64:564] = True
m &= k
if oeff:
    m = ndimage.binary_opening(m, iterations=oeff)
    m = ndimage.binary_closing(m, iterations=oeff) & seg
lb, n = ndimage.label(m)
if n == 0:
    print("leer")
    sys.exit(1)
gr = np.bincount(lb.ravel())[1:]
m = lb == (np.argmax(gr) + 1)
m = ndimage.binary_fill_holes(m)
cs, _ = cv2.findContours(m.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
c = max(cs, key=cv2.contourArea)
c = cv2.approxPolyDP(c, 0.8, True).reshape(-1, 2)
linie = c.tolist() + [c[0].tolist()]
print(json.dumps({"flaeche": int(m.sum()), "seg": int(seg.sum()), "linie": linie}))
ys, xs = np.nonzero(seg)
x0, x1, y0, y1 = max(0, xs.min() - 15), xs.max() + 16, max(0, ys.min() - 15), ys.max() + 16
f = max(4, min(10, 900 // max(x1 - x0, y1 - y0)))
sub = img0[y0:y1, x0:x1]
big = cv2.resize(sub, ((x1 - x0) * f, (y1 - y0) * f), interpolation=cv2.INTER_NEAREST)
rgb = np.stack([big] * 3, -1).copy()
sb = cv2.resize(seg[y0:y1, x0:x1].astype(np.uint8), ((x1 - x0) * f, (y1 - y0) * f), interpolation=cv2.INTER_NEAREST)
cs2, _ = cv2.findContours(sb, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
cv2.drawContours(rgb, cs2, -1, (255, 230, 0), 1)
pl = ((np.array(linie) - [x0, y0]) * f + f // 2).astype(np.int32)
cv2.polylines(rgb, [pl], False, (255, 40, 40), 2)
Image.fromarray(rgb).save(ziel, quality=90)
