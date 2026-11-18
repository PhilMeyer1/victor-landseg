import sys
import numpy as np
from PIL import Image, ImageDraw
import tifffile
from PIL import ImageFont
F = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 14)
sys.stdout.reconfigure(encoding="utf-8")
H = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/"
OUT = "C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde2/abgaben/C-03/"
img = np.array(Image.open(H + "H0.png").convert("L"))
lab = tifffile.imread(H + "c-feste-liste/zusammen/labels.tif")
for sid in (300079, 400072, 400064, 100229, 300004, 300010):
    m = lab == sid
    v = img[m]
    ys, xs = np.nonzero(m)
    print(sid, "px", m.sum(), "bbox x", xs.min(), xs.max(), "y", ys.min(), ys.max(),
          "mean", round(float(v.mean()), 1), "<70", int((v < 70).sum()), "70-120", int(((v >= 70) & (v < 120)).sum()), ">=120", int((v >= 120).sum()))
# 300079 split upper/lower
m = lab == 300079
ys, xs = np.nonzero(m)
up = ys < 521
for name, sel in (("oben", up), ("unten", ~up)):
    v = img[ys[sel], xs[sel]]
    print("300079", name, sel.sum(), "<70", int((v < 70).sum()), "70-120", int(((v >= 70) & (v < 120)).sum()), ">=120", int((v >= 120).sum()))
x0, y0, x1, y1 = 470, 485, 540, 550
S = 12
crop = img[y0:y1, x0:x1].astype(float)
lo, hi = np.percentile(crop, 1), np.percentile(crop, 99)
c2 = np.clip((crop - lo) / max(hi - lo, 1) * 255, 0, 255).astype(np.uint8)
big = Image.fromarray(c2).resize(((x1 - x0) * S, (y1 - y0) * S), Image.NEAREST).convert("RGB")
d = ImageDraw.Draw(big)
L = lab[y0:y1, x0:x1]
col = {300079: (0, 220, 255), 400072: (255, 0, 255), 400064: (255, 140, 0), 100229: (0, 255, 0), 300010: (255, 255, 0)}
for yy in range(L.shape[0]):
    for xx in range(L.shape[1]):
        a = L[yy, xx]
        if xx + 1 < L.shape[1] and L[yy, xx + 1] != a:
            c = col.get(a, col.get(L[yy, xx + 1], (255, 0, 0)))
            d.line([((xx + 1) * S, yy * S), ((xx + 1) * S, (yy + 1) * S)], fill=c, width=2)
        if yy + 1 < L.shape[0] and L[yy + 1, xx] != a:
            c = col.get(a, col.get(L[yy + 1, xx], (255, 0, 0)))
            d.line([(xx * S, (yy + 1) * S), ((xx + 1) * S, (yy + 1) * S)], fill=c, width=2)
for gx in range(x0, x1, 10):
    d.text(((gx - x0) * S + 2, 2), str(gx), fill=(255, 60, 60), font=F)
for gy in range(y0 + 5, y1, 10):
    d.text((2, (gy - y0) * S + 2), str(gy), fill=(255, 60, 60), font=F)
d.rectangle([0, big.height - 60, 520, big.height], fill=(0, 0, 0))
d.text((6, big.height - 56), "Umrisse: türkis 300079, magenta 400072, orange 400064,", fill=(255, 255, 255), font=F)
d.text((6, big.height - 40), "grün 100229, gelb 300010, rot sonstige; 12-fach, Kontrast gestreckt", fill=(255, 255, 255), font=F)
d.text((6, big.height - 24), "Ausschnitt x 470-540, y 485-550", fill=(255, 255, 255), font=F)
big.save(OUT + "einigung_02.jpg", quality=90)
print(big.size)
