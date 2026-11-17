"""Eigene Nahansicht: Ausschnitt der Teilkachel mit allen Segmentgrenzen (gelb) und Nummern.
Aufruf: nah.py <name> x0 y0 w h faktor [kontrast] [hervorheben=id,id]"""
import sys, json
import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from scipy import ndimage

B = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500"
OUT = B + "/urteil/r0c1/v1/"
lab = tifffile.imread(B + "/vorstufe/r0c1/labels.tif").astype(np.int64)
img = Image.open(B + "/teilkacheln/r0c1.png").convert("RGB")
name, x0, y0, w, h, f = sys.argv[1], *map(int, sys.argv[2:7])
rest = sys.argv[7:]
kontrast = "kontrast" in rest
hl = set()
for r in rest:
    if r.startswith("hervorheben="):
        hl = {int(t) for t in r.split("=")[1].split(",")}
mine = set(json.load(open(B + "/viertel/r0c1/v1/viertel.json", encoding="utf-8"))["segmente"] and
           [s["id"] for s in json.load(open(B + "/viertel/r0c1/v1/viertel.json", encoding="utf-8"))["segmente"]])
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
for i in hl:
    m = Lb == i
    e = m & ~ndimage.binary_erosion(m, iterations=2)
    a[e] = (255, 40, 40)
# Kern- und Viertelgrenzen
def vline(x, col):
    xb = (x - x0) * f
    if 0 <= xb < a.shape[1]:
        a[:, max(0, xb - 1):xb + 1] = col
def hline(y, col):
    yb = (y - y0) * f
    if 0 <= yb < a.shape[0]:
        a[max(0, yb - 1):yb + 1, :] = col
for v in (64, 314, 564):
    vline(v, (0, 255, 255)); hline(v, (0, 255, 255))
out = Image.fromarray(a)
d = ImageDraw.Draw(out)
try:
    font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 14)
except Exception:
    font = ImageFont.load_default()
for i in np.unique(L):
    m = L == i
    if m.sum() < 6:
        continue
    dt = ndimage.distance_transform_edt(np.pad(m, 1))[1:-1, 1:-1]
    yy, xx = np.unravel_index(dt.argmax(), dt.shape)
    t = str(i % 100000)
    col = (255, 255, 255) if i in mine else (170, 170, 170)
    px, py = xx * f + f // 2, yy * f + f // 2
    d.text((px - 8, py - 7), t, fill=col, font=font, stroke_width=2, stroke_fill=(0, 0, 0))
# Gitter-Beschriftung in Teilkachel-Bildpunkten am Rand
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
