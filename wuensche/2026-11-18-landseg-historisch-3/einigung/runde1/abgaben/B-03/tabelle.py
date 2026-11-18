import json
import numpy as np
from PIL import Image
import tifffile

B = "C:/Users/Phil/Developement/Victor/daten/landseg/H0"
img = np.array(Image.open(f"{B}/H0.png").convert("L")).astype(float)
l0 = tifffile.imread(f"{B}/b-kategorien-frei/r0c0/labels.tif")
l1 = tifffile.imread(f"{B}/b-kategorien-frei/r0c1/labels.tif")
lab = np.zeros((1000, 1000), dtype=np.int64)
lab[0:500, 0:500] = l0[64:564, 64:564]
lab[0:500, 500:1000] = l1[64:564, 64:564]
for y in range(0, 115):
    row = " ".join(f"{int(img[y, x]):3d}" for x in range(492, 508))
    print(f"y{y:3d} L{lab[y,499]} R{lab[y,500]} | {row}")

# mean gray per segment (kern parts)
ids = [100032, 100056, 100063, 100070, 100081, 100092, 100030, 100042, 100079, 200019, 200004, 200186, 200169, 200180, 200031, 200170, 200171, 200164, 200042, 200049]
for k in ids:
    m = lab == k
    if m.sum():
        ys, xs = np.nonzero(m)
        print(k, "n", m.sum(), "mean", round(img[m].mean(), 1), "p10/50/90", np.percentile(img[m], [10, 50, 90]).round(0), "x", xs.min(), xs.max(), "y", ys.min(), ys.max())
