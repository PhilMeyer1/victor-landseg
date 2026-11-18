"""Klassenansicht fuer die Einigung A-02 (nur lesen).

Aufruf: klassen.py <name> x0 y0 x1 y1 fach
Links Rohbild, rechts Klassenfarben (Fassung A) halb deckend, Grenzen weiss,
Nummer (ID ohne Tausender-Praefix) und Klasse am Schwerpunkt jedes Segments.
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
kat = json.loads((A / "kategorien-a.json").read_text(encoding="utf-8"))
farbe = {c["code"]: tuple(int(c["color"][i:i + 2], 16) for i in (1, 3, 5)) for c in kat["classes"]}
bild = np.array(Image.open(D / "H0.png").convert("L"))
lab = np.zeros(bild.shape, dtype=np.uint32)
klasse = {}
for t in man["teilkacheln"]:
    k, ki = t["kern"], t["kern_im_bild"]
    l = tifffile.imread(A / t["id"] / "labels.tif")
    lab[k["y"]:k["y"] + k["hoehe"], k["x"]:k["x"] + k["breite"]] = \
        l[ki["y"]:ki["y"] + ki["hoehe"], ki["x"]:ki["x"] + ki["breite"]]
    seg = json.loads((A / t["id"] / "segmente.json").read_text(encoding="utf-8"))
    for s in seg["segmente"]:
        klasse[int(s["id"])] = s.get("klasse")

name = sys.argv[1]
x0, y0, x1, y1, f = map(int, sys.argv[2:7])
g = bild[y0:y1, x0:x1].astype(float)
lo, hi = np.percentile(g, 1), np.percentile(g, 99)
g = np.clip((g - lo) / max(hi - lo, 1) * 255, 0, 255).astype(np.uint8)
L = lab[y0:y1, x0:x1]
rgb = np.stack([g] * 3, -1).astype(float)
over = rgb.copy()
for sid in np.unique(L):
    m = L == sid
    c = farbe.get(klasse.get(int(sid)), (0, 0, 0))
    over[m] = over[m] * 0.6 + np.array(c) * 0.4
W, H = (x1 - x0) * f, (y1 - y0) * f
links = Image.fromarray(rgb.astype(np.uint8)).resize((W, H), Image.NEAREST)
rechts = Image.fromarray(over.astype(np.uint8)).resize((W, H), Image.NEAREST)
dr = ImageDraw.Draw(rechts)
rand = np.zeros(L.shape, bool)
rand[:, 1:] |= L[:, 1:] != L[:, :-1]
rand[1:, :] |= L[1:, :] != L[:-1, :]
ys, xs = np.nonzero(rand)
for y, x in zip(ys, xs):
    dr.rectangle([x * f, y * f, x * f + max(f // 4, 1), y * f + max(f // 4, 1)], fill=(255, 255, 255))
try:
    font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13)
except OSError:
    font = ImageFont.load_default()
for sid in np.unique(L):
    ys, xs = np.nonzero(L == sid)
    if len(ys) < 15:
        continue
    i = np.argmin((ys - ys.mean()) ** 2 + (xs - xs.mean()) ** 2)
    t = f"{int(sid) % 100000} {klasse.get(int(sid))}"
    X, Y = xs[i] * f, ys[i] * f
    dr.text((X - 1, Y - 1), t, fill=(0, 0, 0), font=font)
    dr.text((X, Y), t, fill=(255, 255, 0), font=font)
for img in (links, rechts):
    dd = ImageDraw.Draw(img)
    for lin in (250, 500, 750):
        if x0 < lin < x1:
            X = (lin - x0) * f
            for yy in range(0, H, 12):
                dd.line([X, yy, X, yy + 5], fill=(255, 40, 40))
        if y0 < lin < y1:
            Y = (lin - y0) * f
            for xx in range(0, W, 12):
                dd.line([xx, Y, xx + 5, Y], fill=(255, 40, 40))
out = Image.new("RGB", (W * 2 + 8, H + 22), (20, 20, 24))
out.paste(links, (0, 22))
out.paste(rechts, (W + 8, 22))
ImageDraw.Draw(out).text((4, 3), f"{name}: x {x0}–{x1}, y {y0}–{y1}, {f}-fach, Klassen Fassung A", fill=(255, 230, 120), font=font)
s = 2000 / max(out.size)
if s < 1:
    out = out.resize((int(out.width * s), int(out.height * s)), Image.LANCZOS)
out.save(OUT / f"{name}.jpg", quality=90)
print(OUT / f"{name}.jpg", out.size)
