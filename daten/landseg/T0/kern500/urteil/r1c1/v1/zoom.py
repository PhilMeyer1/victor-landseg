"""Eigene Nahansichten: Ausschnitt der Teilkachel mit Segmentgrenzen und Nummern.

Aufruf: zoom.py <name> <x0> <y0> <breite> <hoehe> <faktor> [kontrast]
Schreibt <name>.jpg (mit Grenzen) und <name>_roh.jpg in diesen Ordner.
"""
import sys
import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

BASIS = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500"
AUS = BASIS + "/urteil/r1c1/v1"

name, x0, y0, w, h, f = sys.argv[1], *map(int, sys.argv[2:7])
kontrast = len(sys.argv) > 7

lab = tifffile.imread(BASIS + "/vorstufe/r1c1/labels.tif").astype(np.int64)
img = np.array(Image.open(BASIS + "/teilkacheln/r1c1.png").convert("RGB"))
sub = img[y0:y0 + h, x0:x0 + w]
ls = lab[y0:y0 + h, x0:x0 + w]
pic = Image.fromarray(sub).resize((w * f, h * f), Image.NEAREST)
if kontrast:
    pic = ImageEnhance.Contrast(ImageEnhance.Brightness(pic).enhance(1.6)).enhance(1.5)
pic.save(f"{AUS}/{name}_roh.jpg", quality=92)
big = np.kron(ls, np.ones((f, f), dtype=np.int64))
rand = np.zeros_like(big, dtype=bool)
rand[:, 1:] |= big[:, 1:] != big[:, :-1]
rand[1:, :] |= big[1:, :] != big[:-1, :]
arr = np.array(pic)
arr[rand] = (255, 255, 0)
# Kern- und Viertelgrenze
for gx in (64, 314):
    if x0 <= gx < x0 + w:
        arr[:, (gx - x0) * f, :] = (0, 255, 255)
for gy in (64, 314):
    if y0 <= gy < y0 + h:
        arr[(gy - y0) * f, :, :] = (0, 255, 255)
pic = Image.fromarray(arr)
d = ImageDraw.Draw(pic)
try:
    font = ImageFont.truetype("arial.ttf", 16)
except OSError:
    font = ImageFont.load_default()
for sid in np.unique(ls):
    ys, xs = np.nonzero(ls == sid)
    if len(xs) < 4:
        cy, cx = ys[0], xs[0]
    else:
        # Punkt im Segment nahe dem Median
        my, mx = np.median(ys), np.median(xs)
        k = np.argmin((ys - my) ** 2 + (xs - mx) ** 2)
        cy, cx = ys[k], xs[k]
    t = str(sid % 100000)
    px, py = cx * f + f // 2, cy * f + f // 2
    d.text((px + 1, py + 1), t, fill=(0, 0, 0), font=font, anchor="mm")
    d.text((px, py), t, fill=(255, 255, 255), font=font, anchor="mm")
pic.save(f"{AUS}/{name}.jpg", quality=92)
print("ok", name, pic.size)
