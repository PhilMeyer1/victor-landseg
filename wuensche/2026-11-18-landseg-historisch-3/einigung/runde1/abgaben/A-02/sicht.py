"""Eigene Ansicht fuer die Einigung A-02 (nur lesen, Bilder nur im Ergebnisordner).

Aufruf: sicht.py <name> x0 y0 x1 y1 fach id1,id2,...
Zeigt links das Rohbild (Kontrast gespreizt), rechts alle Segmentgrenzen (weiss)
und die genannten Segmente eingefaerbt; Naht- und Viertellinien rot gestrichelt.
"""
import json
import sys
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont

D = Path("C:/Users/Phil/Developement/Victor/daten/landseg/H0")
A = D / "a-alles-frei"
OUT = Path(__file__).parent

man = json.loads((D / "manifest.json").read_text(encoding="utf-8"))
bild = np.array(Image.open(D / "H0.png").convert("L"))
lab = np.zeros(bild.shape, dtype=np.uint32)
for t in man["teilkacheln"]:
    k, ki = t["kern"], t["kern_im_bild"]
    l = tifffile.imread(A / t["id"] / "labels.tif")
    lab[k["y"]:k["y"] + k["hoehe"], k["x"]:k["x"] + k["breite"]] = \
        l[ki["y"]:ki["y"] + ki["hoehe"], ki["x"]:ki["x"] + ki["breite"]]

name = sys.argv[1]
x0, y0, x1, y1, f = map(int, sys.argv[2:7])
ids = [int(s.split(":")[-1]) for s in sys.argv[7].split(",")] if len(sys.argv) > 7 else []
farben = [(0, 220, 230), (240, 0, 240), (255, 160, 0), (60, 220, 60), (60, 100, 255), (255, 60, 60)]

g = bild[y0:y1, x0:x1].astype(float)
lo, hi = np.percentile(g, 1), np.percentile(g, 99)
g = np.clip((g - lo) / max(hi - lo, 1) * 255, 0, 255).astype(np.uint8)
L = lab[y0:y1, x0:x1]
rgb = np.stack([g] * 3, -1).astype(float)
over = rgb.copy()
for i, sid in enumerate(ids):
    m = L == sid
    over[m] = over[m] * 0.55 + np.array(farben[i % len(farben)]) * 0.45
rand = np.zeros(L.shape, bool)
rand[:, 1:] |= L[:, 1:] != L[:, :-1]
rand[1:, :] |= L[1:, :] != L[:-1, :]
links = Image.fromarray(rgb.astype(np.uint8)).resize(((x1 - x0) * f, (y1 - y0) * f), Image.NEAREST)
rechts = Image.fromarray(over.astype(np.uint8)).resize(((x1 - x0) * f, (y1 - y0) * f), Image.NEAREST)
dr = ImageDraw.Draw(rechts)
ys, xs = np.nonzero(rand)
for y, x in zip(ys, xs):
    dr.rectangle([x * f, y * f, x * f + max(f // 4, 1), y * f + max(f // 4, 1)], fill=(255, 255, 255))
for d in (rechts, ):
    pass
for lin in (250, 500, 750):
    for img in (links, rechts):
        dd = ImageDraw.Draw(img)
        if x0 < lin < x1:
            X = (lin - x0) * f
            for yy in range(0, img.height, 12):
                dd.line([X, yy, X, yy + 5], fill=(255, 40, 40), width=1)
        if y0 < lin < y1:
            Y = (lin - y0) * f
            for xx in range(0, img.width, 12):
                dd.line([xx, Y, xx + 5, Y], fill=(255, 40, 40), width=1)
W = links.width * 2 + 8
H = links.height + 24
out = Image.new("RGB", (W, H), (20, 20, 24))
out.paste(links, (0, 24))
out.paste(rechts, (links.width + 8, 24))
try:
    font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 14)
except OSError:
    font = ImageFont.load_default()
txt = f"{name}: x {x0}–{x1}, y {y0}–{y1}, {f}-fach; Farben: " + ", ".join(
    f"{['türkis','magenta','orange','grün','blau','rot'][i % 6]} {s}" for i, s in enumerate(sys.argv[7].split(",") if ids else []))
ImageDraw.Draw(out).text((4, 3), txt, fill=(255, 230, 120), font=font)
s = 2000 / max(out.size)
if s < 1:
    out = out.resize((int(out.width * s), int(out.height * s)), Image.LANCZOS)
out.save(OUT / f"{name}.jpg", quality=90)
print(OUT / f"{name}.jpg", out.size)
