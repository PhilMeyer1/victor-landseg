"""Eigene Nahansicht: bild.py x y w h faktor ziel.jpg [ids_hervorheben] [--roh] [--kontrast] [--gitter]"""
import sys, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import tifffile

B = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/"
LAB = sys.argv[sys.argv.index("--labels") + 1] if "--labels" in sys.argv else B + "c-feste-liste/r1c0/labels.tif"
lab = tifffile.imread(LAB).astype(np.int64)
img = np.array(Image.open(B + "teilkacheln/r1c0.png").convert("L")).astype(float)
x, y, w, h, f = [int(a) for a in sys.argv[1:6]]
ziel = sys.argv[6]
hl = [int(a) for a in sys.argv[7].split(",")] if len(sys.argv) > 7 and not sys.argv[7].startswith("--") else []
roh = "--roh" in sys.argv
kontrast = "--kontrast" in sys.argv
gitter = "--gitter" in sys.argv
x0, y0 = max(0, x), max(0, y)
x1, y1 = min(lab.shape[1], x + w), min(lab.shape[0], y + h)
L = lab[y0:y1, x0:x1]
I = img[y0:y1, x0:x1]
if kontrast:
    lo, hi = np.percentile(I, 1), np.percentile(I, 99)
    I = np.clip((I - lo) / max(1, hi - lo) * 255, 0, 255)
rgb = np.stack([I] * 3, -1)
for k, i in enumerate(hl):
    m = L == i
    col = [(255, 80, 80), (80, 160, 255), (80, 255, 80), (255, 200, 0), (255, 0, 255), (0, 255, 255)][k % 6]
    rgb[m] = rgb[m] * 0.6 + np.array(col) * 0.4
big = np.repeat(np.repeat(rgb, f, 0), f, 1).astype(np.uint8)
im = Image.fromarray(big)
d = ImageDraw.Draw(im)
if not roh:
    Lb = np.repeat(np.repeat(L, f, 0), f, 1)
    e = np.zeros(Lb.shape, bool)
    e[:, 1:] |= Lb[:, 1:] != Lb[:, :-1]
    e[1:, :] |= Lb[1:, :] != Lb[:-1, :]
    a = np.array(im); a[e] = (255, 255, 0); im = Image.fromarray(a); d = ImageDraw.Draw(im)
    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except Exception:
        font = ImageFont.load_default()
    for i in np.unique(L):
        ys, xs = np.nonzero(L == i)
        if len(ys) < 20: continue
        # point inside: median-closest
        cx, cy = np.median(xs), np.median(ys)
        j = np.argmin((xs - cx) ** 2 + (ys - cy) ** 2)
        d.text((xs[j] * f, ys[j] * f), str(i % 100000), fill=(255, 255, 255), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
# Kern und Viertel
for (qx, qy, qw, qh), c in [((64, 64, 500, 500), (255, 255, 255)), ((64, 64, 250, 250), (0, 255, 255)), ((314, 64, 250, 250), (0, 255, 255)), ((64, 314, 250, 250), (0, 255, 255)), ((314, 314, 250, 250), (0, 255, 255))]:
    d.rectangle([(qx - x0) * f, (qy - y0) * f, (qx + qw - x0) * f - 1, (qy + qh - y0) * f - 1], outline=c, width=1)
if gitter:
    try:
        font = ImageFont.truetype("arial.ttf", 12)
    except Exception:
        font = ImageFont.load_default()
    step = 10 if w <= 120 else 25
    for gx in range((x0 // step + 1) * step, x1, step):
        d.line([((gx - x0) * f, 0), ((gx - x0) * f, im.size[1])], fill=(255, 0, 255) if gx % 50 == 0 else (120, 0, 120), width=1)
        d.text(((gx - x0) * f + 2, 2), str(gx), fill=(255, 255, 255), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
    for gy in range((y0 // step + 1) * step, y1, step):
        d.line([(0, (gy - y0) * f), (im.size[0], (gy - y0) * f)], fill=(255, 0, 255) if gy % 50 == 0 else (120, 0, 120), width=1)
        d.text((2, (gy - y0) * f + 2), str(gy), fill=(255, 255, 255), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
im.save(ziel, quality=90)
print(ziel, im.size)
