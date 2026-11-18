"""Overview crop with segment outlines (zusammen labels) and IDs; writes only into this folder or a given path."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

H0 = "C:/Users/Phil/Developement/Victor/daten/landseg/H0"
x0, y0, x1, y1, s = (int(v) for v in sys.argv[1:6])
out = sys.argv[6]
ids = set(int(v) for v in sys.argv[7].split(",")) if len(sys.argv) > 7 else set()

img = np.array(Image.open(f"{H0}/H0.png").convert("L"))
lab = np.array(Image.open(f"{H0}/b-kategorien-frei/zusammen/labels.tif"))
crop = img[y0:y1, x0:x1]
lc = lab[y0:y1, x0:x1]
big = np.kron(crop, np.ones((s, s), dtype=np.uint8))
lb = np.kron(lc, np.ones((s, s), dtype=np.int32))
edge = np.zeros_like(lb, dtype=bool)
edge[:-1, :] |= lb[:-1, :] != lb[1:, :]
edge[:, :-1] |= lb[:, :-1] != lb[:, 1:]
raw = Image.fromarray(big).convert("RGB")
rgb = np.array(raw)
ov = rgb.copy()
ov[edge] = (255, 220, 0)
for i in ids:
    m = lb == i
    ov[m] = (ov[m] * 0.6 + np.array([0, 200, 255]) * 0.4).astype(np.uint8)
# seam lines (kern borders at 500)
for c in (500,):
    if x0 <= c < x1:
        ov[:, (c - x0) * s, :] = (255, 0, 0)
    if y0 <= c < y1:
        ov[(c - y0) * s, :, :] = (255, 0, 0)
both = Image.new("RGB", (raw.width * 2 + 8, raw.height), (20, 20, 20))
both.paste(raw, (0, 0))
o = Image.fromarray(ov)
d = ImageDraw.Draw(o)
try:
    f = ImageFont.truetype("arial.ttf", 14)
except OSError:
    f = ImageFont.load_default()
for i in np.unique(lc):
    ys, xs = np.nonzero(lc == i)
    if len(xs) < 15:
        continue
    cx, cy = int(np.median(xs)) * s, int(np.median(ys)) * s
    d.text((cx, cy), str(i % 1000 if i < 200000 else i % 1000), fill=(255, 60, 60) if i < 200000 else (60, 255, 60), font=f)
both.paste(o, (raw.width + 8, 0))
w, h = both.size
k = min(1.0, 2000 / max(w, h))
if k < 1:
    both = both.resize((int(w * k), int(h * k)), Image.LANCZOS)
both.save(out, quality=90)
print(out, both.size)
