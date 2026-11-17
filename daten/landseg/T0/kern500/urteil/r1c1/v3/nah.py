"""Eigene Nahansicht: Ausschnitt der Teilkachel r1c1 vergrößert, links roh, rechts mit Grenzen und Nummern.
Aufruf: python nah.py <ausgabe.jpg> x0 y0 breite hoehe faktor [kontrast]
"""
import sys
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont, ImageOps

K = Path("C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500")
out, x0, y0, w, h, f = sys.argv[1], *map(int, sys.argv[2:7])
kon = len(sys.argv) > 7
lab = tifffile.imread(K / "vorstufe/r1c1/labels.tif").astype(np.int64)
img = Image.open(K / "teilkacheln/r1c1.png").convert("RGB")
c = img.crop((x0, y0, x0 + w, y0 + h))
if kon:
    c = ImageOps.autocontrast(c, cutoff=1)
big = c.resize((w * f, h * f), Image.NEAREST)
L = lab[y0:y0 + h, x0:x0 + w]
Lb = np.kron(L, np.ones((f, f), dtype=np.int64))
edge = np.zeros(Lb.shape, bool)
edge[:, 1:] |= Lb[:, 1:] != Lb[:, :-1]
edge[1:, :] |= Lb[1:, :] != Lb[:-1, :]
arr = np.asarray(big).copy()
arr[edge] = (255, 255, 0)
ov = Image.fromarray(arr)
d = ImageDraw.Draw(ov)
try:
    font = ImageFont.truetype("arial.ttf", 14)
except OSError:
    font = ImageFont.load_default()
for i in np.unique(L):
    ys, xs = np.nonzero(L == i)
    if len(xs) < 4:
        continue
    # Punkt im Segment nahe Schwerpunkt
    cx, cy = xs.mean(), ys.mean()
    k = np.argmin((xs - cx) ** 2 + (ys - cy) ** 2)
    px, py = xs[k] * f + f // 2, ys[k] * f + f // 2
    t = str(i % 100000)
    d.text((px - 8, py - 7), t, fill=(255, 255, 255), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
# Kern- und Viertelgrenzen
for g in (64, 314, 564):
    for (a, b) in ((x0, w), (y0, h)):
        pass
def linie(v, achse):
    if achse == "x" and x0 <= v < x0 + w:
        X = (v - x0) * f
        d.line([(X, 0), (X, h * f)], fill=(0, 255, 255), width=2)
    if achse == "y" and y0 <= v < y0 + h:
        Y = (v - y0) * f
        d.line([(0, Y), (w * f, Y)], fill=(0, 255, 255), width=2)
for g in (64, 314, 564):
    linie(g, "x"); linie(g, "y")
# Gitterbeschriftung
lab_img = Image.new("RGB", (w * f * 2 + 10, h * f + 22), (0, 0, 0))
lab_img.paste(big, (0, 22))
lab_img.paste(ov, (w * f + 10, 22))
dd = ImageDraw.Draw(lab_img)
dd.text((4, 3), f"Ausschnitt x {x0}–{x0 + w - 1}, y {y0}–{y0 + h - 1} der Teilkachel r1c1, {f}fach; links roh{' (Kontrast)' if kon else ''}, rechts Grenzen und Nummern",
        fill=(255, 255, 255), font=font)
s = max(lab_img.size)
if s > 2000:
    r = 2000 / s
    lab_img = lab_img.resize((int(lab_img.size[0] * r), int(lab_img.size[1] * r)), Image.LANCZOS)
lab_img.save(out, quality=92)
print(out, lab_img.size)
