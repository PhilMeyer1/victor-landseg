import sys
import numpy as np
from PIL import Image
import tifffile

D = "C:/Users/Phil/Developement/Victor/daten/landseg/H0"
OUT = "C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde1/abgaben/A-13"
img = np.array(Image.open(D + "/teilkacheln/r1c1.png").convert("L")).astype(float)
lab = tifffile.imread(D + "/a-alles-frei/r1c1/labels.tif")
name = sys.argv[1]
ids = [int(x) for x in sys.argv[2].split(",")]
x0, y0, w = [int(v) for v in sys.argv[3].split(",")]  # ausschnitt coords
off = 436
x0 -= off; y0 -= off
crop = img[y0:y0 + w, x0:x0 + w]
lo, hi = np.percentile(crop, 1), np.percentile(crop, 99)
c = np.clip((crop - lo) / (hi - lo) * 255, 0, 255)
rgb = np.stack([c, c, c], -1)
cols = [(0, 220, 220), (230, 0, 230), (255, 200, 0), (0, 200, 0)]
L = lab[y0:y0 + w, x0:x0 + w]
ov = rgb.copy()
for i, col in zip(ids, cols):
    m = L == i
    ov[m] = 0.5 * ov[m] + 0.5 * np.array(col)
k = max(1, 700 // w)
both = np.concatenate([rgb, ov], axis=1).astype(np.uint8)
im = Image.fromarray(both).resize((both.shape[1] * k, both.shape[0] * k), Image.NEAREST)
im.save(OUT + "/" + name, quality=90)
