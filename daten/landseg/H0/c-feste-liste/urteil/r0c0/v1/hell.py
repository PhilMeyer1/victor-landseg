"""Helle Teilflächen in einem Segment finden und als Polygon (konvexe Hülle) ausgeben; nur lesen."""
import sys
import numpy as np
import tifffile
from PIL import Image
from scipy import ndimage
from scipy.ndimage import gaussian_filter
from scipy.spatial import ConvexHull

lab = tifffile.imread("C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r0c0/labels.tif").astype(int)
img = np.array(Image.open("C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r0c0.png").convert("L")).astype(float)
g = gaussian_filter(img, 0.8)
sid, schwelle = int(sys.argv[1]), float(sys.argv[2])
fenster = [int(v) for v in sys.argv[3].split(",")] if len(sys.argv) > 3 else None
m = (lab == sid) & (g > schwelle)
if fenster:
    x0, y0, x1, y1 = fenster
    f = np.zeros_like(m)
    f[y0:y1, x0:x1] = True
    m &= f
m = ndimage.binary_opening(m, iterations=1)
t, n = ndimage.label(m)
for i in range(1, n + 1):
    ys, xs = np.nonzero(t == i)
    if len(ys) < 25:
        continue
    pts = np.c_[xs, ys]
    h = ConvexHull(pts)
    poly = pts[h.vertices].tolist()
    print(f"Teil {i}: {len(ys)} px, x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()}, Grau {img[t == i].mean():.0f}; Hülle {poly}")
