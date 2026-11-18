import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
F = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 14)
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/"
OUT = "C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde2/abgaben/C-03/"
img = np.array(Image.open(H + "H0.png").convert("L"))
lab = None
try:
    import tifffile
    lab = tifffile.imread(H + "c-feste-liste/zusammen/labels.tif")
except Exception as e:
    print("tifffile", e)
    lab = np.array(Image.open(H + "c-feste-liste/zusammen/labels.tif"))
print("lab", lab.shape, lab.dtype)
x0, y0, x1, y1 = 460, 470, 545, 545
sub = lab[y0:y1, x0:x1]
ids, cnt = np.unique(sub, return_counts=True)
for i, c in zip(ids, cnt):
    print(i, c)
# print id grid near the corner, every px, region x 478..506, y 494..534
for y in range(494, 535):
    print(y, " ".join("%6d" % lab[y, x] for x in range(478, 506)))
S = 10
crop = img[y0:y1, x0:x1]
# contrast stretch
lo, hi = np.percentile(crop, 1), np.percentile(crop, 99)
c2 = np.clip((crop.astype(float) - lo) / max(hi - lo, 1) * 255, 0, 255).astype(np.uint8)
big = Image.fromarray(c2).resize(((x1 - x0) * S, (y1 - y0) * S), Image.NEAREST).convert("RGB")
d = ImageDraw.Draw(big)
# grid line for naht
d.line([(0, (500 - y0) * S), (big.width, (500 - y0) * S)], fill=(255, 255, 0), width=1)
d.line([((500 - x0) * S, 0), ((500 - x0) * S, big.height)], fill=(255, 255, 0), width=1)
for gx in range(x0, x1, 10):
    d.text(((gx - x0) * S + 2, 2), str(gx), fill=(255, 0, 0), font=F)
for gy in range(y0, y1, 10):
    d.text((2, (gy - y0) * S + 2), str(gy), fill=(255, 0, 0), font=F)
d.rectangle([0, big.height - 24, 560, big.height], fill=(0, 0, 0))
d.text((6, big.height - 20), "H0 x 460-545, y 470-545, 10-fach, Kontrast gestreckt; gelb: Kerngrenzen x=500, y=500", fill=(255, 255, 255), font=F)
big.save(OUT + "einigung_01.jpg", quality=90)
# raw (no stretch) grayscale values
for y in range(494, 535, 2):
    print("g", y, " ".join("%3d" % img[y, x] for x in range(476, 512, 2)))
