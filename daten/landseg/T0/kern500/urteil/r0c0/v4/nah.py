"""Eigene Nahansicht: nah.py <name> x0 y0 x1 y1 faktor [kontrast] [hervor=id,id]"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

B = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500"
O = B + "/urteil/r0c0/v4/"
lab = np.array(Image.open(B + "/vorstufe/r0c0/labels.tif"))
img = Image.open(B + "/teilkacheln/r0c0.png").convert("RGB")
name, x0, y0, x1, y1, f = sys.argv[1], *map(int, sys.argv[2:7])
kontrast = "kontrast" in sys.argv
hervor = set()
for a in sys.argv:
    if a.startswith("hervor="):
        hervor = {int(v) for v in a[7:].split(",")}
c = img.crop((x0, y0, x1, y1))
if kontrast:
    c = ImageEnhance.Contrast(ImageEnhance.Brightness(c).enhance(1.6)).enhance(1.6)
W, H = (x1 - x0) * f, (y1 - y0) * f
c = c.resize((W, H), Image.NEAREST)
L = lab[y0:y1, x0:x1]
up = np.repeat(np.repeat(L, f, 0), f, 1)
edge = np.zeros_like(up, bool)
edge[:-1, :] |= up[:-1, :] != up[1:, :]
edge[:, :-1] |= up[:, :-1] != up[:, 1:]
a = np.array(c)
a[edge] = (255, 255, 0)
for h in hervor:
    mm = up == h
    a[mm] = (a[mm] * 0.55 + np.array([255, 0, 255]) * 0.45).astype(np.uint8)
c = Image.fromarray(a)
d = ImageDraw.Draw(c)
try:
    font = ImageFont.truetype("arial.ttf", 13)
except Exception:
    font = ImageFont.load_default()
for i in np.unique(L):
    ys, xs = np.nonzero(L == i)
    if len(xs) < 4:
        continue
    k = np.argmin((xs - xs.mean()) ** 2 + (ys - ys.mean()) ** 2)
    px, py = xs[k] * f, ys[k] * f
    d.text((px - 10, py - 7), str(i % 100000), fill=(255, 255, 255), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
# Gitter-Beschriftung alle 20 px
for gx in range((x0 // 20 + 1) * 20, x1, 20):
    d.text(((gx - x0) * f + 2, 2), str(gx), fill=(0, 255, 255), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
for gy in range((y0 // 20 + 1) * 20, y1, 20):
    d.text((2, (gy - y0) * f + 2), str(gy), fill=(0, 255, 255), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
c.save(O + name, quality=90)
print(O + name, c.size)
