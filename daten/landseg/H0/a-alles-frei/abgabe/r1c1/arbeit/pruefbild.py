"""Prüfbild: links Rohbild (gespreizt) mit Gitter, rechts Klassenfarben + Grenzen + IDs.
Schreibt zusätzlich punkte.json (ID -> innerer Punkt) für Korrekturen per Punkt.

Aufruf: pruefbild.py x0 y0 groesse faktor ausgabe.jpg
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
x0, y0, g, f = map(int, sys.argv[1:5])
aus = sys.argv[5]
x1, y1 = min(x0 + g, 628), min(y0 + g, 628)
img = np.array(Image.open(BILD).convert("L")).astype(np.float32)
L = tifffile.imread(AB / "labels.tif")
segs = {s["id"]: s for s in json.loads((AB / "segmente.json").read_text(encoding="utf-8"))["segmente"]}
kat = {c["code"]: c for c in json.loads((AB / "kategorien-teil.json").read_text(encoding="utf-8"))["classes"]}
farbe = np.zeros((L.max() + 1, 3), np.float32)
for sid, s in segs.items():
    h = kat[s["klasse"]]["color"]
    farbe[sid] = [int(h[i:i + 2], 16) for i in (1, 3, 5)]
c = img[y0:y1, x0:x1]
lo, hi = np.percentile(c, 1), np.percentile(c, 99.5)
cs = np.clip((c - lo) / max(hi - lo, 1) * 255, 0, 255)
l = L[y0:y1, x0:x1]


def gross(a):
    return np.repeat(np.repeat(a, f, 0), f, 1)


roh = gross(np.stack([cs] * 3, -1))
ov = gross(np.stack([c] * 3, -1) * 0.72 + farbe[l] * 0.28)
lb = gross(l)
rand = np.zeros(lb.shape, bool)
rand[:, 1:] |= lb[:, 1:] != lb[:, :-1]
rand[1:, :] |= lb[1:, :] != lb[:-1, :]
ov[rand] = (255, 235, 0)
roh_r = roh.copy()
roh_r[rand] = roh_r[rand] * 0.55 + np.array([255, 235, 0]) * 0.45
w = roh.shape[1]
out = np.concatenate([roh_r, np.full((roh.shape[0], 8, 3), 255.0), ov], 1)
im = Image.fromarray(out.clip(0, 255).astype(np.uint8))
d = ImageDraw.Draw(im)
font = ImageFont.truetype("arialbd.ttf", 12)
for off in (0, w + 8):
    for gx in range((x0 // 25 + 1) * 25, x1, 25):
        d.line([off + (gx - x0) * f, 0, off + (gx - x0) * f, 6], fill=(0, 255, 255), width=2)
        d.text((off + (gx - x0) * f + 2, 6), str(gx), fill=(0, 255, 255), font=font)
    for gy in range((y0 // 25 + 1) * 25, y1, 25):
        d.line([off, (gy - y0) * f, off + 6, (gy - y0) * f], fill=(0, 255, 255), width=2)
        d.text((off + 8, (gy - y0) * f - 6), str(gy), fill=(0, 255, 255), font=font)
    d.rectangle([off + (64 - x0) * f, (64 - y0) * f, off + (564 - x0) * f, (564 - y0) * f], outline=(255, 0, 255), width=2)
punkte_p = AB / "arbeit" / "punkte.json"
try:
    punkte = json.loads(punkte_p.read_text(encoding="utf-8"))
except Exception:
    punkte = {}
for sid in np.unique(l):
    m = l == sid
    dt = ndimage.distance_transform_edt(np.pad(m, 1))[1:-1, 1:-1]
    yy, xx = np.unravel_index(np.argmax(dt), dt.shape)
    mg = L == sid
    dtg = ndimage.distance_transform_edt(np.pad(mg, 1))[1:-1, 1:-1]
    gy_, gx_ = np.unravel_index(np.argmax(dtg), dtg.shape)
    punkte[str(int(sid))] = [int(gx_), int(gy_)]
    if m.sum() < 6:
        continue
    t = str(int(sid))
    d.text((w + 8 + xx * f - 3 * len(t), yy * f - 6), t, fill=(255, 255, 255), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
punkte_p.write_text(json.dumps(punkte), encoding="utf-8")
im.save(aus, quality=88)
print(aus, im.size)
