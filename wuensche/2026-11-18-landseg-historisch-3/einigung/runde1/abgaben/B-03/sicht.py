import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import tifffile

B = "C:/Users/Phil/Developement/Victor/daten/landseg/H0"
OUT = "C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde1/abgaben/B-03"

x0, y0, x1, y1, s, name = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
ids_hl = set(int(v) for v in sys.argv[7].split(",")) if len(sys.argv) > 7 else set()

img = np.array(Image.open(f"{B}/H0.png").convert("L"))
l0 = tifffile.imread(f"{B}/b-kategorien-frei/r0c0/labels.tif")
l1 = tifffile.imread(f"{B}/b-kategorien-frei/r0c1/labels.tif")
lab = np.zeros((1000, 1000), dtype=np.int64)
lab[0:500, 0:500] = l0[64:564, 64:564]
lab[0:500, 500:1000] = l1[64:564, 64:564]

crop = img[y0:y1, x0:x1]
lc = lab[y0:y1, x0:x1]
h, w = crop.shape
big = np.kron(crop, np.ones((s, s), dtype=np.uint8))
rgb = np.stack([big] * 3, -1).astype(np.uint8)
lb = np.kron(lc, np.ones((s, s), dtype=np.int64))
edge = np.zeros_like(lb, dtype=bool)
edge[:, 1:] |= lb[:, 1:] != lb[:, :-1]
edge[1:, :] |= lb[1:, :] != lb[:-1, :]
right = rgb.copy()
right[edge] = [255, 220, 0]
if ids_hl:
    for k, col in zip(sorted(ids_hl), [(0, 200, 200), (220, 0, 220), (0, 200, 0), (255, 120, 0), (80, 80, 255), (255, 0, 0)]):
        m = lb == k
        right[m] = (right[m] * 0.55 + np.array(col) * 0.45).astype(np.uint8)
# naht line x=500
if x0 <= 500 < x1:
    nx = (500 - x0) * s
    right[:, nx:nx + 1] = [255, 0, 0]
canvas = np.concatenate([rgb, np.zeros((h * s, 8, 3), np.uint8), right], 1)
im = Image.fromarray(canvas)
d = ImageDraw.Draw(im)
try:
    f = ImageFont.truetype("arial.ttf", 13)
except Exception:
    f = None
off = w * s + 8
for k in np.unique(lc):
    ys, xs = np.nonzero(lc == k)
    if len(xs) < 6:
        continue
    cx, cy = int(np.median(xs)), int(np.median(ys))
    j = np.argmin((xs - cx) ** 2 + (ys - cy) ** 2)
    d.text((off + xs[j] * s, ys[j] * s), str(k), fill=(255, 60, 60), font=f)
print(im.size)
im.save(f"{OUT}/{name}", quality=90)
