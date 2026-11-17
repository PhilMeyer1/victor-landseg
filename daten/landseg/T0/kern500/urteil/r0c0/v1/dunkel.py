"""Dunkle bzw. helle Flecken innerhalb eines Segments: dunkel.py <id> x0 y0 x1 y1 [hell]
Glättet die Helligkeit (5x5), Schwelle dunkel < 62 bzw. hell > 125, Flecken ab 80 px."""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

sys.stdout.reconfigure(encoding="utf-8")
B = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500"
lab = np.array(Image.open(B + "/vorstufe/r0c0/labels.tif")).astype(np.int64)
img = np.array(Image.open(B + "/teilkacheln/r0c0.png").convert("RGB")).astype(float)
sid = int(sys.argv[1])
x0, y0, x1, y1 = map(int, sys.argv[2:6])
hell = "hell" in sys.argv
g = ndi.uniform_filter(img.mean(2), 5)
m = np.zeros(lab.shape, bool)
m[y0:y1, x0:x1] = True
m &= lab == sid
sel = (g > 125) if hell else (g < 62)
sel &= m
sel = ndi.binary_opening(sel, iterations=1)
L, n = ndi.label(sel)
out = []
for k in range(1, n + 1):
    ys, xs = np.nonzero(L == k)
    if len(xs) < 80:
        continue
    out.append((len(xs), int(xs.mean()), int(ys.mean()), xs.min(), xs.max(), ys.min(), ys.max(), g[L == k].mean()))
for o in sorted(out, reverse=True):
    print(f"fl={o[0]} mitte={o[1]}/{o[2]} box x{o[3]}-{o[4]} y{o[5]}-{o[6]} hell={o[7]:.0f}")
print("Mittel Segment im Fenster:", round(g[m].mean(), 1))
