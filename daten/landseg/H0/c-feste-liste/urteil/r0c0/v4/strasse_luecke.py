"""Helles Straßenband zwischen 149 und 198, das in 143 und 183 steckt, als Polygon; nur lesen."""
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
g = gaussian_filter(img, 1.0)
thr = float(sys.argv[1])
box = np.zeros(lab.shape, bool)
box[340:402, 452:500] = True
quelle = np.isin(lab, [100143, 100183])
m = quelle & box & (g > thr)
m = ndimage.binary_opening(m, iterations=1)
# nur Teile, die an 149 oder 198 grenzen (über Nachbarschaft)
nah = ndimage.binary_dilation(np.isin(lab, [100149, 100198]), iterations=2)
t, n = ndimage.label(m)
keep = np.zeros_like(m)
for i in range(1, n + 1):
    if (nah & (t == i)).any() and (t == i).sum() > 20:
        keep |= t == i
keep = ndimage.binary_closing(keep, iterations=2) & quelle & box
keep = ndimage.binary_fill_holes(keep)
for sid in (100143, 100183):
    print(sid, int((keep & (lab == sid)).sum()), "px", file=sys.stderr)
ys, xs = np.nonzero(keep)
print(f"x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()} gesamt {len(ys)}", file=sys.stderr)
cs, _ = cv2.findContours(keep.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
print(len(cs), "Konturen", file=sys.stderr)
c = max(cs, key=cv2.contourArea)
print(json.dumps(c[:, 0, :].tolist()))
