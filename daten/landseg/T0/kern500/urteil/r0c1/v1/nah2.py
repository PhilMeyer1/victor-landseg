"""Eigene Nahansicht (roh + Grenzen/Nummern nebeneinander nicht, sondern zwei Dateien).
Aufruf: nah2.py <viertel> <name> x0 y0 w h faktor [kontrast]
Schreibt <name>.jpg (Grenzen gelb, Nummern) in den Ergebnisordner des Viertels."""
import sys, json
import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from scipy import ndimage

B = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500"
v = sys.argv[1]
OUT = B + "/urteil/r0c1/" + v + "/"
lab = tifffile.imread(B + "/vorstufe/r0c1/labels.tif").astype(np.int64)
img = Image.open(B + "/teilkacheln/r0c1.png").convert("RGB")
name, x0, y0, w, h, f = sys.argv[2], *map(int, sys.argv[3:8])
kontrast = "kontrast" in sys.argv[8:]
mine = {s["id"] for s in json.load(open(B + "/viertel/r0c1/" + v + "/viertel.json", encoding="utf-8"))["segmente"]}
crop = img.crop((x0, y0, x0 + w, y0 + h))
if kontrast:
    crop = ImageEnhance.Contrast(ImageEnhance.Brightness(crop).enhance(1.4)).enhance(1.6)
big = crop.resize((w * f, h * f), Image.NEAREST)
L = lab[y0:y0 + h, x0:x0 + w]
Lb = np.kron(L, np.ones((f, f), dtype=np.int64))
edge = np.zeros(Lb.shape, bool)
edge[:, 1:] |= Lb[:, 1:] != Lb[:, :-1]
edge[1:, :] |= Lb[1:, :] != Lb[:-1, :]
a = np.asarray(big).copy()
a[edge] = (255, 230, 0)
for vv in (64, 314, 564):
    xb = (vv - x0) * f
    if 0 <= xb < a.shape[1]:
        a[:, max(0, xb - 1):xb + 1] = (0, 255, 255)
    yb = (vv - y0) * f
    if 0 <= yb < a.shape[0]:
        a[max(0, yb - 1):yb + 1, :] = (0, 255, 255)
out = Image.fromarray(a)
d = ImageDraw.Draw(out)
font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 14)
for i in np.unique(L):
    m = L == i
    if m.sum() < 6:
        continue
    dt = ndimage.distance_transform_edt(np.pad(m, 1))[1:-1, 1:-1]
    yy, xx = np.unravel_index(dt.argmax(), dt.shape)
    col = (255, 255, 255) if i in mine else (170, 170, 170)
    d.text((xx * f + f // 2 - 8, yy * f + f // 2 - 7), str(i % 100000), fill=col, font=font,
           stroke_width=2, stroke_fill=(0, 0, 0))
for gx in range((x0 // 10 + 1) * 10, x0 + w, 10):
    xb = (gx - x0) * f
    d.line([(xb, 0), (xb, 6)], fill=(0, 255, 255))
    if gx % 20 == 0:
        d.text((xb + 2, 0), str(gx), fill=(0, 255, 255), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
for gy in range((y0 // 10 + 1) * 10, y0 + h, 10):
    yb = (gy - y0) * f
    d.line([(0, yb), (6, yb)], fill=(0, 255, 255))
    if gy % 20 == 0:
        d.text((2, yb + 1), str(gy), fill=(0, 255, 255), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
out.save(OUT + name, quality=90)
print(OUT + name, out.size)
