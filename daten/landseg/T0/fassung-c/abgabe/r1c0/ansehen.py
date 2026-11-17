"""Kontrollbild: Segmentgrenzen, Nummern und Klassencode über dem Bild (Ausschnitt, Faktor)."""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi

HIER = Path(__file__).parent
A = HIER / "arbeit"
BILD = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c/teilkacheln/r1c0.png"
CODES = json.load(open(A / "codes.json"))["codes"]

x0, y0, x1, y1, f = map(int, sys.argv[1:6])
aus = sys.argv[6]
img = np.array(Image.open(BILD).convert("RGB"))
karte = np.load(A / "karte.npy")
k = np.load(A / "klassen_final.npy")
crop = img[y0:y1, x0:x1]
lab = karte[y0:y1, x0:x1]
big = np.repeat(np.repeat(crop, f, 0), f, 1).copy()
labb = np.repeat(np.repeat(lab, f, 0), f, 1)
rand = np.zeros(labb.shape, bool)
rand[:-1] |= labb[:-1] != labb[1:]
rand[:, :-1] |= labb[:, :-1] != labb[:, 1:]
big[rand] = (255, 255, 0)
im = Image.fromarray(big)
d = ImageDraw.Draw(im)
try:
    font = ImageFont.truetype("arialbd.ttf", 11)
except OSError:
    font = ImageFont.load_default()
for gx in range((x0 // 50 + 1) * 50, x1, 50):
    d.text(((gx - x0) * f, 0), str(gx), fill=(0, 255, 255), font=font)
    d.line([((gx - x0) * f, 0), ((gx - x0) * f, 6)], fill=(0, 255, 255))
for gy in range((y0 // 50 + 1) * 50, y1, 50):
    d.text((0, (gy - y0) * f), str(gy), fill=(0, 255, 255), font=font)
for sid in np.unique(lab):
    m = karte == sid
    ys, xs = np.nonzero(m)
    # Punkt im Segment, möglichst weit vom Rand
    dist = ndi.distance_transform_edt(m)
    cy, cx = np.unravel_index(dist.argmax(), m.shape)
    if not (x0 <= cx < x1 and y0 <= cy < y1):
        continue
    code = CODES[k[cy, cx]]
    t = f"{sid}:{code}"
    X, Y = (cx - x0) * f - 12, (cy - y0) * f - 6
    d.text((X + 1, Y + 1), t, fill=(0, 0, 0), font=font)
    d.text((X, Y), t, fill=(255, 80, 255), font=font)
im.save(aus, quality=90)
