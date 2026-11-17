"""Eigene Nahansicht: nah.py <name> <x0> <y0> <breite> <hoehe> <faktor> [kontrast]
Schreibt <name>.jpg in den Ordner dieses Skripts: oben roh, unten Grenzen gelb mit Nummern (weiß: eigenes Viertel),
Achsen in Bildpunkten der Teilkachel.
"""
import json
import sys
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageEnhance, ImageFont
from scipy import ndimage

B = Path("C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b")
OUT = Path(__file__).parent
V = OUT.name
lab = tifffile.imread(B / "vorstufe/r1c1/labels.tif").astype(np.int64)
img = Image.open(B / "teilkacheln/r1c1.png").convert("RGB")
vj = json.loads((B / "viertel/r1c1" / V / "viertel.json").read_text(encoding="utf-8"))
MEINE = {s["id"] for s in vj["segmente"]}

name = sys.argv[1]
x0, y0, w, h, f = (int(v) for v in sys.argv[2:7])
kontrast = len(sys.argv) > 7
crop = img.crop((x0, y0, x0 + w, y0 + h))
if kontrast:
    crop = ImageEnhance.Contrast(ImageEnhance.Brightness(crop).enhance(1.3)).enhance(1.6)
big = crop.resize((w * f, h * f), Image.LANCZOS)
L = lab[y0:y0 + h, x0:x0 + w]
Lb = np.kron(L, np.ones((f, f), dtype=np.int64))
edge = np.zeros_like(Lb, dtype=bool)
edge[:, 1:] |= Lb[:, 1:] != Lb[:, :-1]
edge[1:, :] |= Lb[1:, :] != Lb[:-1, :]
arr = np.asarray(big).copy()
arr[edge] = (255, 230, 0)
im2 = Image.fromarray(arr)
d = ImageDraw.Draw(im2)
font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 14)
font2 = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 12)
for sid in np.unique(L):
    m = L == sid
    if m.sum() < 5:
        continue
    dt = ndimage.distance_transform_edt(np.pad(m, 1))[1:-1, 1:-1]
    yy, xx = np.unravel_index(np.argmax(dt), dt.shape)
    col = (255, 255, 255) if sid in MEINE else (180, 180, 180)
    d.text((xx * f + f // 2, yy * f + f // 2), str(sid % 100000), font=font, fill=col, anchor="mm",
           stroke_width=2, stroke_fill=(0, 0, 0))
out = Image.new("RGB", (w * f, 2 * h * f + 40), (20, 20, 20))
out.paste(big, (0, 20))
out.paste(im2, (0, h * f + 40))
dd = ImageDraw.Draw(out)
for top in (20, h * f + 40):
    for gx in range((x0 // 10 + 1) * 10, x0 + w, 10):
        dd.line([((gx - x0) * f, top), ((gx - x0) * f, top + 5)], fill=(0, 255, 255), width=1)
        dd.text(((gx - x0) * f, top + 6), str(gx), font=font2, fill=(0, 255, 255), anchor="mt")
    for gy in range((y0 // 10 + 1) * 10, y0 + h, 10):
        dd.line([(0, top + (gy - y0) * f), (5, top + (gy - y0) * f)], fill=(0, 255, 255), width=1)
        dd.text((7, top + (gy - y0) * f), str(gy), font=font2, fill=(0, 255, 255), anchor="lm")
dd.text((4, 2), f"Teilkachel r1c1 x {x0}–{x0 + w}, y {y0}–{y0 + h}, {f}fach; oben roh, unten Grenzen (weiß: Viertel {V})",
        font=font2, fill=(255, 255, 255))
s = max(out.size)
if s > 2000:
    out = out.resize((out.size[0] * 2000 // s, out.size[1] * 2000 // s), Image.LANCZOS)
out.save(OUT / f"{name}.jpg", quality=90)
print("ok", out.size)
