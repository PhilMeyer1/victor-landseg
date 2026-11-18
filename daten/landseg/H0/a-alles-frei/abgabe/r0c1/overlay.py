"""overlay.py labels.npy|tif x0 y0 w h scale out [nummern 0/1] [klassen.json]"""
import sys, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import tifffile

BILD = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r0c1.png"
src = sys.argv[1]
x0, y0, w, h, s = map(int, sys.argv[2:7])
out = sys.argv[7]
num = len(sys.argv) > 8 and sys.argv[8] == "1"
kl = json.load(open(sys.argv[9], encoding="utf-8")) if len(sys.argv) > 9 else None
L = np.load(src) if src.endswith(".npy") else tifffile.imread(src)
a = np.array(Image.open(BILD)).astype(np.float32)
c = a[y0:y0 + h, x0:x0 + w]
lo, hi = np.percentile(c, 1), np.percentile(c, 99.5)
c = np.clip((c - lo) / (hi - lo) * 255, 0, 255).astype(np.uint8)
rgb = np.stack([c] * 3, -1).astype(np.float32)
Lc = L[y0:y0 + h, x0:x0 + w]
if kl:
    farbe = kl["farben"]
    seg = kl["seg"]
    for i in np.unique(Lc):
        k = seg.get(str(int(i)))
        if k is None:
            continue
        col = np.array([int(farbe[k][j:j + 2], 16) for j in (1, 3, 5)], np.float32)
        m = Lc == i
        rgb[m] = 0.6 * rgb[m] + 0.4 * col
im = Image.fromarray(rgb.astype(np.uint8)).resize((w * s, h * s), Image.NEAREST)
Lb = np.kron(Lc, np.ones((s, s), dtype=Lc.dtype))
edge = np.zeros(Lb.shape, bool)
edge[:, 1:] |= Lb[:, 1:] != Lb[:, :-1]
edge[1:, :] |= Lb[1:, :] != Lb[:-1, :]
arr = np.array(im)
arr[edge] = (255, 255, 0)
im = Image.fromarray(arr)
d = ImageDraw.Draw(im)
try:
    f = ImageFont.truetype("arial.ttf", 11)
    fg = ImageFont.truetype("arial.ttf", 12)
except Exception:
    f = fg = ImageFont.load_default()
# kern frame
kx0, ky0, kx1, ky1 = 64, 64, 564, 564
d.rectangle([(kx0 - x0) * s, (ky0 - y0) * s, (kx1 - x0) * s - 1, (ky1 - y0) * s - 1], outline=(0, 255, 255), width=2)
step = 50
for gx in range((x0 // step + 1) * step, x0 + w, step):
    d.text(((gx - x0) * s + 1, 1), str(gx), fill=(0, 255, 255), font=fg)
    d.line([((gx - x0) * s, 0), ((gx - x0) * s, 8)], fill=(0, 255, 255), width=2)
for gy in range((y0 // step + 1) * step, y0 + h, step):
    d.text((1, (gy - y0) * s + 1), str(gy), fill=(0, 255, 255), font=fg)
    d.line([(0, (gy - y0) * s), (8, (gy - y0) * s)], fill=(0, 255, 255), width=2)
if num:
    for i in np.unique(Lc):
        m = Lc == i
        if m.sum() < 8:
            continue
        dt = __import__("scipy.ndimage", fromlist=["x"]).distance_transform_edt(np.pad(m, 1))[1:-1, 1:-1]
        yy, xx = np.unravel_index(np.argmax(dt), dt.shape)
        t = str(int(i))
        d.text((xx * s - 3 * len(t), yy * s - 5), t, fill=(255, 0, 255), font=f, stroke_width=1, stroke_fill=(0, 0, 0))
im.save(out, quality=88)
