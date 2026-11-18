import numpy as np
from PIL import Image
import tifffile
B = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/"
img = np.array(Image.open(B + "H0.png").convert("L")).astype(float)
OFF = {"r0c0": (0, 0), "r0c1": (500, 0), "r1c0": (0, 500), "r1c1": (500, 500)}
def lab(t):
    return tifffile.imread(B + "b-kategorien-frei/" + t + "/labels.tif")
cache = {}
segs = ["r0c0:100218", "r0c1:200100", "r0c1:200115", "r1c1:400037", "r0c0:100229", "r1c0:300004",
        "r1c0:300027", "r1c0:300032", "r1c0:300066", "r1c0:300010", "r1c1:400064", "r1c1:400072"]
for s in segs:
    t, i = s.split(":"); i = int(i)
    if t not in cache:
        cache[t] = lab(t)
    L = cache[t]
    ys, xs = np.nonzero(L == i)
    # Teilkachelbild: Kern beginnt bei 64
    ox, oy = OFF[t]
    gx = xs - 64 + ox; gy = ys - 64 + oy
    k = (xs >= 64) & (xs < 564) & (ys >= 64) & (ys < 564)
    gxk, gyk = gx[k], gy[k]
    v = img[gyk, gxk]
    print(s, "shape", L.shape, "n", len(xs), "kern", k.sum(),
          "x", gxk.min(), gxk.max(), "y", gyk.min(), gyk.max(),
          "grau mittel %.0f median %.0f p10 %.0f p90 %.0f" % (v.mean(), np.median(v), np.percentile(v, 10), np.percentile(v, 90)))
    # Grauwert am Kernstueck nahe Ecke 500,500
    near = (abs(gxk - 500) < 12) & (abs(gyk - 500) < 40)
    if near.any():
        print("    nahe Ecke: n", near.sum(), "grau %.0f" % img[gyk[near], gxk[near]].mean())
