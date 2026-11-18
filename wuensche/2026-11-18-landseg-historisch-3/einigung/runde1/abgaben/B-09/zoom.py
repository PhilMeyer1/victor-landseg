import sys
import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont

D = "C:/Users/Phil/Developement/Victor/daten/landseg/H0"
OUT = "C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde1/abgaben/B-09"

x0, y0, x1, y1, f, name = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[6]
img = np.array(Image.open(D + "/H0.png"))
la = tifffile.imread(D + "/b-kategorien-frei/r0c1/labels.tif")
lb = tifffile.imread(D + "/b-kategorien-frei/r1c1/labels.tif")
lab = np.zeros((1000, 1000), np.int64)
# r0c1 context origin (436,-64), r1c1 context origin (436,436)
for y in range(0, 1000):
    for src, oy in ((la, -64), (lb, 436)):
        pass
ys = np.arange(1000)
xs = np.arange(436, 1000)
top = ys[ys < 500]
bot = ys[ys >= 500]
lab[np.ix_(top, xs)] = la[np.ix_(top + 64, xs - 436)]
bot2 = bot[bot - 436 < 628]
lab[np.ix_(bot2, xs)] = lb[np.ix_(bot2 - 436, xs - 436)]

crop = img[y0:y1, x0:x1].astype(float)
lo, hi = np.percentile(crop, 1), np.percentile(crop, 99)
st = np.clip((crop - lo) / (hi - lo) * 255, 0, 255).astype(np.uint8)
L = lab[y0:y1, x0:x1]
H, W = crop.shape
raw = Image.fromarray(img[y0:y1, x0:x1]).resize((W * f, H * f), Image.NEAREST).convert("RGB")
ov = Image.fromarray(st).resize((W * f, H * f), Image.NEAREST).convert("RGB")
d = ImageDraw.Draw(ov)
for yy in range(H):
    for xx in range(W):
        if xx + 1 < W and L[yy, xx] != L[yy, xx + 1]:
            d.line([((xx + 1) * f, yy * f), ((xx + 1) * f, (yy + 1) * f)], fill=(255, 0, 0))
        if yy + 1 < H and L[yy, xx] != L[yy + 1, xx]:
            d.line([(xx * f, (yy + 1) * f), ((xx + 1) * f, (yy + 1) * f)], fill=(255, 0, 0))
if y0 < 500 < y1:
    d.line([(0, (500 - y0) * f), (W * f, (500 - y0) * f)], fill=(255, 255, 0))
try:
    font = ImageFont.truetype("arial.ttf", 13)
except Exception:
    font = ImageFont.load_default()
for v in np.unique(L):
    yy, xx = np.nonzero(L == v)
    if len(yy) < 8:
        continue
    i = len(yy) // 2
    order = np.lexsort((xx, yy))
    cy, cx = yy[order[i]], xx[order[i]]
    d.text((cx * f, cy * f), str(v), fill=(0, 255, 0), font=font)
for x in range(x0 - x0 % 10 + 10, x1, 10):
    d.text(((x - x0) * f, 2), str(x), fill=(0, 200, 255), font=font)
out = Image.new("RGB", (W * f, H * f * 2 + 4), (0, 0, 0))
out.paste(raw, (0, 0))
out.paste(ov, (0, H * f + 4))
s = 2000 / max(out.size)
if s < 1:
    out = out.resize((int(out.size[0] * s), int(out.size[1] * s)), Image.LANCZOS)
out.save(OUT + "/" + name, quality=90)
print(out.size)
