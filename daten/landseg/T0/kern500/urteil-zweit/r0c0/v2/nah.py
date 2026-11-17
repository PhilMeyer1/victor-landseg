"""Eigene Nahansichten: links roh, rechts mit Grenzen und Nummern. Aufruf: nah.py n x0 y0 w h faktor [kontrast]"""
import sys, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import tifffile

B = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500"
O = B + "/urteil-zweit/r0c0/v2"
n, x0, y0, w, h, f = [int(v) for v in sys.argv[1:7]]
kontrast = len(sys.argv) > 7
img = np.asarray(Image.open(B + "/teilkacheln/r0c0.png").convert("RGB")).astype(float)
lab = tifffile.imread(B + "/vorstufe/r0c0/labels.tif")
mine = set(json.load(open(O + "/ids.json")))
c = img[y0:y0 + h, x0:x0 + w]
if kontrast:
    lo = np.percentile(c, 2, axis=(0, 1)); hi = np.percentile(c, 98, axis=(0, 1))
    c = np.clip((c - lo) / (hi - lo + 1e-6) * 255, 0, 255)
c = c.astype(np.uint8)
L = lab[y0:y0 + h, x0:x0 + w]
big = np.kron(c, np.ones((f, f, 1), dtype=np.uint8))
Lb = np.kron(L, np.ones((f, f), dtype=L.dtype))
edge = np.zeros(Lb.shape, bool)
edge[:, 1:] |= Lb[:, 1:] != Lb[:, :-1]
edge[1:, :] |= Lb[1:, :] != Lb[:-1, :]
ov = big.copy()
ov[edge] = [255, 255, 0]
# Viertelrand (cyan)
vx0, vy0, vx1, vy1 = 314, 64, 564, 314
im2 = Image.fromarray(ov)
d = ImageDraw.Draw(im2)
d.rectangle([(vx0 - x0) * f, (vy0 - y0) * f, (vx1 - x0) * f - 1, (vy1 - y0) * f - 1], outline=(0, 255, 255), width=2)
try:
    font = ImageFont.truetype("arial.ttf", 14)
except Exception:
    font = ImageFont.load_default()
for i in np.unique(L):
    ys, xs = np.nonzero(L == i)
    if len(ys) < 6:
        continue
    # Punkt im Segment nahe Schwerpunkt
    cy, cx = ys.mean(), xs.mean()
    k = np.argmin((ys - cy) ** 2 + (xs - cx) ** 2)
    px, py = xs[k] * f + f // 2, ys[k] * f + f // 2
    col = (255, 255, 255) if int(i) in mine else (170, 170, 170)
    t = str(int(i) % 100000)
    d.text((px - 8, py - 7), t, fill=col, font=font, stroke_width=2, stroke_fill=(0, 0, 0))
im1 = Image.fromarray(big)
d1 = ImageDraw.Draw(im1)
d1.rectangle([(vx0 - x0) * f, (vy0 - y0) * f, (vx1 - x0) * f - 1, (vy1 - y0) * f - 1], outline=(0, 255, 255), width=1)
W = im1.width * 2 + 10
out = Image.new("RGB", (W, im1.height + 24), (0, 0, 0))
out.paste(im1, (0, 24)); out.paste(im2, (im1.width + 10, 24))
dd = ImageDraw.Draw(out)
name = ("kontrast_%d" if kontrast else "nah_%d") % n
dd.text((4, 4), f"{name}: x {x0}–{x0 + w}, y {y0}–{y0 + h} (Teilkachel), {f}fach; links roh, rechts Grenzen", fill=(255, 255, 255), font=font)
out.save(f"{O}/{name}.jpg", quality=90)
print(name, out.size)
