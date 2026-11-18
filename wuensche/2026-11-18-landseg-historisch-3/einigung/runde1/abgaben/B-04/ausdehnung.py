import numpy as np, tifffile
from PIL import Image
B = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/"
img = np.array(Image.open(B + "H0.png").convert("L")).astype(float)
OFF = {"r0c0": (0, 0), "r0c1": (500, 0), "r1c0": (0, 500), "r1c1": (500, 500)}
for s in ["r0c0:100229", "r0c1:200100", "r0c1:200115", "r1c1:400037", "r1c1:400064", "r1c1:400072"]:
    t, i = s.split(":"); L = tifffile.imread(B + "b-kategorien-frei/" + t + "/labels.tif")
    ys, xs = np.nonzero(L == int(i)); gx = xs - 64 + OFF[t][0]; gy = ys - 64 + OFF[t][1]
    v = img[gy.clip(0, 999), gx.clip(0, 999)]
    print(s, "x", gx.min(), gx.max(), "y", gy.min(), gy.max(), "grau %.0f" % v.mean(), "p10 %.0f p90 %.0f" % tuple(np.percentile(v, [10, 90])))
