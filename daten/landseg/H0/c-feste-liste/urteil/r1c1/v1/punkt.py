import sys, json, tifffile, numpy as np
from PIL import Image
L = tifffile.imread("C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r1c1/labels.tif")
img = np.array(Image.open("C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r1c1.png").convert("L")).astype(float)
seg = {s["id"]: s for s in json.load(open("C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r1c1/segmente.json", encoding="utf-8"))["segmente"]}
if sys.argv[1] == "ids":
    for a in sys.argv[2:]:
        i = int(a); m = L == i
        if not m.any():
            print(i, "nicht auf Karte"); continue
        ys, xs = np.nonzero(m)
        k = m[64:564, 64:564].sum()
        print(i, seg.get(i, {}).get("klasse"), "px", m.sum(), "kern", k, "bbox", xs.min(), xs.max(), ys.min(), ys.max(), "grau %.0f +- %.0f" % (img[m].mean(), img[m].std()))
else:
    for a in sys.argv[1:]:
        x, y = (int(v) for v in a.split("/"))
        print(a, L[y, x] % 100000)
