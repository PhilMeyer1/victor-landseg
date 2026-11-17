"""Zoom view: zoom.py <labels.tif> x0 y0 x1 y1 factor out.png [nolabels]
Draws label boundaries (yellow), ids (id-200000 if >200000) and a 20 px grid with coordinates."""
import sys
import numpy as np
import tifffile
from PIL import Image, ImageDraw

D = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c"
lab_p, x0, y0, x1, y1, f, out = sys.argv[1], *map(int, sys.argv[2:7]), sys.argv[7]
nolab = len(sys.argv) > 8
img = np.asarray(Image.open(f"{D}/teilkacheln/r0c1.png").convert("RGB"))
lab = tifffile.imread(lab_p)
sub = img[y0:y1, x0:x1]
L = lab[y0:y1, x0:x1]
big = np.kron(sub, np.ones((f, f, 1), dtype=np.uint8))
Lb = np.kron(L, np.ones((f, f), dtype=L.dtype))
edge = np.zeros(Lb.shape, bool)
edge[:, 1:] |= Lb[:, 1:] != Lb[:, :-1]
edge[1:, :] |= Lb[1:, :] != Lb[:-1, :]
out_img = big.copy()
if not nolab:
    out_img[edge] = (255, 255, 0)
im = Image.fromarray(out_img)
d = ImageDraw.Draw(im)
for gx in range((x0 // 20 + 1) * 20, x1, 20):
    X = (gx - x0) * f
    d.line([(X, 0), (X, 6)], fill=(0, 255, 255))
    d.line([(X, im.height - 6), (X, im.height)], fill=(0, 255, 255))
    d.text((X + 1, 7), str(gx), fill=(0, 255, 255))
    for gy in range((y0 // 20 + 1) * 20, y1, 20):
        Y = (gy - y0) * f
        d.point([(X, Y)], fill=(0, 255, 255))
        d.line([(X - 2, Y), (X + 2, Y)], fill=(0, 255, 255))
        d.line([(X, Y - 2), (X, Y + 2)], fill=(0, 255, 255))
for gy in range((y0 // 20 + 1) * 20, y1, 20):
    Y = (gy - y0) * f
    d.line([(0, Y), (6, Y)], fill=(0, 255, 255))
    d.text((7, Y + 1), str(gy), fill=(0, 255, 255))
if not nolab:
    for i in np.unique(L):
        m = L == i
        ys, xs = np.nonzero(m)
        # label position: pixel of the segment closest to its centroid
        cy, cx = ys.mean(), xs.mean()
        k = np.argmin((ys - cy) ** 2 + (xs - cx) ** 2)
        n = int(i) - 200000 if i > 200000 else int(i)
        if m.sum() < 30:
            continue
        d.text((xs[k] * f - 6, ys[k] * f - 5), str(n), fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
im.save(out)
print(im.size)
