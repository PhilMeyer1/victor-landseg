"""Ausschnitt mit halbtransparent eingefärbten Segmenten (je Segment eine Zufallsfarbe) und Nummer je Teil.

Aufruf: flaechen.py <name> <x0> <y0> <breite> <hoehe> <faktor>
"""
import sys
import numpy as np
import tifffile
from scipy import ndimage
from PIL import Image, ImageDraw, ImageFont

BASIS = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500"
AUS = BASIS + "/urteil/r1c1/v1"
name, x0, y0, w, h, f = sys.argv[1], *map(int, sys.argv[2:7])
lab = tifffile.imread(BASIS + "/vorstufe/r1c1/labels.tif").astype(np.int64)
img = np.array(Image.open(BASIS + "/teilkacheln/r1c1.png").convert("RGB")).astype(float)
ls = lab[y0:y0 + h, x0:x0 + w]
sub = img[y0:y0 + h, x0:x0 + w]
rng = np.random.default_rng(3)
farbe = {i: rng.integers(40, 255, 3) for i in np.unique(ls)}
col = np.zeros_like(sub)
for i, c in farbe.items():
    col[ls == i] = c
mix = (0.55 * sub + 0.45 * col).astype(np.uint8)
pic = Image.fromarray(mix).resize((w * f, h * f), Image.NEAREST)
big = np.kron(ls, np.ones((f, f), dtype=np.int64))
r = np.zeros_like(big, dtype=bool)
r[:, 1:] |= big[:, 1:] != big[:, :-1]
r[1:, :] |= big[1:, :] != big[:-1, :]
a = np.array(pic)
a[r] = (0, 0, 0)
pic = Image.fromarray(a)
d = ImageDraw.Draw(pic)
font = ImageFont.truetype("arial.ttf", 15)
for i in np.unique(ls):
    comp, n = ndimage.label(ls == i)
    for k in range(1, n + 1):
        ys, xs = np.nonzero(comp == k)
        if len(xs) < 6:
            continue
        my, mx = np.median(ys), np.median(xs)
        j = np.argmin((ys - my) ** 2 + (xs - mx) ** 2)
        px, py = xs[j] * f + f // 2, ys[j] * f + f // 2
        t = str(i % 100000)
        d.text((px + 1, py + 1), t, fill=(0, 0, 0), font=font, anchor="mm")
        d.text((px, py), t, fill=(255, 255, 255), font=font, anchor="mm")
pic.save(f"{AUS}/{name}.jpg", quality=92)
print("ok", name)
