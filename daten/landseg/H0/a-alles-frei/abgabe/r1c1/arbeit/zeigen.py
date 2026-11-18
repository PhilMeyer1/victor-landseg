"""Klassenfarben + Grenzen (+ IDs) über einem Ausschnitt der Teilkachel.

Aufruf: zeigen.py x0 y0 x1 y1 faktor ausgabe.jpg [ids] [alpha]
"""
import json
import sys
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

AB = Path(__file__).resolve().parent.parent
BILD = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r1c1.png"
x0, y0, x1, y1, f = map(int, sys.argv[1:6])
aus = sys.argv[6]
mit_ids = len(sys.argv) > 7 and sys.argv[7] == "ids"
alpha = float(sys.argv[8]) if len(sys.argv) > 8 else 0.35

img = np.array(Image.open(BILD).convert("L")).astype(np.float32)
L = tifffile.imread(AB / "labels.tif")
segs = {s["id"]: s for s in json.loads((AB / "segmente.json").read_text(encoding="utf-8"))["segmente"]}
kat = {c["code"]: c for c in json.loads((AB / "kategorien-teil.json").read_text(encoding="utf-8"))["classes"]}


def hexrgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


farbe = np.zeros((L.max() + 1, 3), np.float32)
for sid, s in segs.items():
    farbe[sid] = hexrgb(kat[s["klasse"]]["color"])
c = img[y0:y1, x0:x1]
l = L[y0:y1, x0:x1]
rgb = np.stack([c] * 3, -1) * (1 - alpha) + farbe[l] * alpha
big = np.repeat(np.repeat(rgb, f, 0), f, 1)
lb = np.repeat(np.repeat(l, f, 0), f, 1)
rand = np.zeros(lb.shape, bool)
rand[:, 1:] |= lb[:, 1:] != lb[:, :-1]
rand[1:, :] |= lb[1:, :] != lb[:-1, :]
big[rand] = (255, 235, 0)
out = Image.fromarray(big.clip(0, 255).astype(np.uint8))
d = ImageDraw.Draw(out)
try:
    font = ImageFont.truetype("arialbd.ttf", 11 if f < 4 else 13)
except Exception:
    font = ImageFont.load_default()
d.rectangle([(64 - x0) * f, (64 - y0) * f, (564 - x0) * f, (564 - y0) * f], outline=(255, 0, 255), width=2)
for g in range((x0 // 50 + 1) * 50, x1, 50):
    d.text(((g - x0) * f + 2, 1), str(g), fill=(0, 255, 255), font=font)
for g in range((y0 // 50 + 1) * 50, y1, 50):
    d.text((1, (g - y0) * f + 1), str(g), fill=(0, 255, 255), font=font)
if mit_ids:
    for sid, sl in enumerate(ndimage.find_objects(l), start=1):
        if sl is None:
            continue
        m = l == sid
        if m.sum() < 15:
            continue
        # Punkt tief im Segment
        dt = ndimage.distance_transform_edt(np.pad(m, 1))[1:-1, 1:-1]
        yy, xx = np.unravel_index(np.argmax(dt), dt.shape)
        t = str(sid)
        tx, ty = xx * f - 3 * len(t), yy * f - 6
        d.text((tx, ty), t, fill=(255, 255, 255), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
out.save(aus, quality=88)
print(aus, out.size)
