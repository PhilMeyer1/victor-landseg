import sys, json
import numpy as np
from scipy import ndimage
sys.path.insert(0, "../v1")
import werkzeug as w
lab, img, seg = w.lade()
g = ndimage.gaussian_filter(img, 1.2)
m = lab == 100143
pts = []
for y in range(268, 396):
    xs = [x for x in range(428, 500) if m[y, x] and g[y, x] > 120]
    # nur zusammenhängendes Band vom linken Rand von 143 aus
    row = [x for x in range(428, 500) if m[y, x]]
    if not row:
        continue
    x0 = row[0]
    x = x0
    while x + 1 < 500 and m[y, x + 1] and g[y, x + 1] > 112:
        x += 1
    pts.append((y, x0, x))
for p in pts[::6]:
    print(p)
json.dump(pts, open("band_pts.json", "w"))
