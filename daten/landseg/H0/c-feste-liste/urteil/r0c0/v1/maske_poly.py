"""Polygon für polygon_zuweisen aus heller (oder dunkler) Teilfläche eines Segments, nur innerhalb
des Segments, ohne Reststücke abzuschneiden. Nur lesen; gibt die Polygonpunkte als JSON aus.
Aufruf: python -B maske_poly.py <id> <schwelle> <x0,y0,x1,y1> [dunkel]"""
import json
import sys

import cv2
import numpy as np
import tifffile
from PIL import Image
from scipy import ndimage
from scipy.ndimage import gaussian_filter

lab = tifffile.imread("C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r0c0/labels.tif").astype(int)
img = np.array(Image.open("C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r0c0.png").convert("L")).astype(float)
g = gaussian_filter(img, 0.8)
sid, thr = int(sys.argv[1]), float(sys.argv[2])
x0, y0, x1, y1 = map(int, sys.argv[3].split(","))
dunkel = len(sys.argv) > 4 and sys.argv[4] == "dunkel"
seg = lab == sid
box = np.zeros_like(seg)
box[y0:y1, x0:x1] = True
m = seg & box & ((g < thr) if dunkel else (g > thr))
m = ndimage.binary_opening(m, iterations=1)
t, n = ndimage.label(m)
if n == 0:
    sys.exit("keine Fläche")
gr = np.bincount(t.ravel())[1:]
m = t == (int(np.argmax(gr)) + 1)
m = ndimage.binary_closing(m, iterations=2) & seg
m = ndimage.binary_fill_holes(m)
# Rest des Segments: kleine abgeschnittene Teile zur Maske nehmen
rest = seg & ~m
t, n = ndimage.label(rest, structure=[[0, 1, 0], [1, 1, 1], [0, 1, 0]])
if n > 1:
    gr = np.bincount(t.ravel())[1:]
    gross = int(np.argmax(gr)) + 1
    for i in range(1, n + 1):
        if i != gross:
            m |= t == i
cs, _ = cv2.findContours(m.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
c = max(cs, key=cv2.contourArea)
poly = c[:, 0, :].tolist()
probe = np.zeros(lab.shape, np.uint8)
cv2.fillPoly(probe, [np.array(poly, np.int32)], 1)
fremd = (probe.astype(bool) & ~seg).sum()
print(f"# Fläche {int(m.sum())} px, Polygon {len(poly)} Punkte, fremde Bildpunkte im Polygon {int(fremd)}, "
      f"x{min(p[0] for p in poly)}-{max(p[0] for p in poly)} y{min(p[1] for p in poly)}-{max(p[1] for p in poly)}",
      file=sys.stderr)
print(json.dumps(poly))
