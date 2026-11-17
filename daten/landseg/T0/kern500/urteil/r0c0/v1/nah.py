"""Eigene Nahansicht: nah.py <ausgabe.jpg> x0 y0 x1 y1 faktor [kontrast] [ohne]  (Teilkachel-Koordinaten)
Grenzen gelb, Nummern weiß (ID mod 100000), Gitter alle 10 px cyan beschriftet, Kern weiß gestrichelt."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

B = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500"
lab = np.array(Image.open(B + "/vorstufe/r0c0/labels.tif"))
img = Image.open(B + "/teilkacheln/r0c0.png").convert("RGB")
out, x0, y0, x1, y1, f = sys.argv[1], *map(int, sys.argv[2:7])
kontrast = "kontrast" in sys.argv
ohne = "ohne" in sys.argv
c = img.crop((x0, y0, x1, y1))
if kontrast:
    c = ImageEnhance.Contrast(ImageEnhance.Brightness(c).enhance(1.7)).enhance(1.7)
W, H = (x1 - x0) * f, (y1 - y0) * f
c = c.resize((W, H), Image.NEAREST)
a = np.array(c)
L = lab[y0:y1, x0:x1]
if not ohne:
    up = np.repeat(np.repeat(L, f, 0), f, 1)
    edge = np.zeros_like(up, bool)
    edge[:-1, :] |= up[:-1, :] != up[1:, :]
    edge[:, :-1] |= up[:, :-1] != up[:, 1:]
    a[edge] = (255, 255, 0)
c = Image.fromarray(a)
d = ImageDraw.Draw(c)
try:
    font = ImageFont.truetype("arial.ttf", 14)
except Exception:
    font = ImageFont.load_default()
# Kerngrenze
for k in (64, 564):
    if x0 <= k < x1:
        d.line([((k - x0) * f, 0), ((k - x0) * f, H)], fill=(255, 255, 255), width=1)
    if y0 <= k < y1:
        d.line([(0, (k - y0) * f), (W, (k - y0) * f)], fill=(255, 255, 255), width=1)
for gx in range((x0 // 10 + 1) * 10, x1, 10):
    d.line([((gx - x0) * f, 0), ((gx - x0) * f, 6)], fill=(0, 255, 255), width=1)
    if gx % 20 == 0:
        d.text(((gx - x0) * f + 2, 2), str(gx), fill=(0, 255, 255), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
for gy in range((y0 // 10 + 1) * 10, y1, 10):
    d.line([(0, (gy - y0) * f), (6, (gy - y0) * f)], fill=(0, 255, 255), width=1)
    if gy % 20 == 0:
        d.text((2, (gy - y0) * f + 2), str(gy), fill=(0, 255, 255), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
if not ohne:
    for i in np.unique(L):
        ys, xs = np.nonzero(L == i)
        if len(xs) < 6:
            continue
        k = np.argmin((xs - xs.mean()) ** 2 + (ys - ys.mean()) ** 2)
        d.text((xs[k] * f - 10, ys[k] * f - 7), str(int(i) % 100000), fill=(255, 255, 255), font=font,
               stroke_width=2, stroke_fill=(0, 0, 0))
c.save(out, quality=90)
print(out, c.size)
