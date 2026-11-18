"""Zoom view: raw (contrast stretched) left, segment outlines of the two segments right; seam ticks."""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

H0 = "C:/Users/Phil/Developement/Victor/daten/landseg/H0"
x0, y0, x1, y1, s = (int(v) for v in sys.argv[1:6])
out = sys.argv[6]
ids = [int(v) for v in sys.argv[7].split(",")]
titel = sys.argv[8] if len(sys.argv) > 8 else ""

img = np.array(Image.open(f"{H0}/H0.png").convert("L")).astype(float)
lab = np.array(Image.open(f"{H0}/b-kategorien-frei/zusammen/labels.tif"))
crop = img[y0:y1, x0:x1]
lo, hi = np.percentile(crop, 1), np.percentile(crop, 99)
crop = np.clip((crop - lo) / max(hi - lo, 1) * 255, 0, 255).astype(np.uint8)
lc = lab[y0:y1, x0:x1]
big = np.kron(crop, np.ones((s, s), dtype=np.uint8))
lb = np.kron(lc, np.ones((s, s), dtype=np.int32))
raw = np.array(Image.fromarray(big).convert("RGB"))
ov = raw.copy()
cols = [(0, 220, 255), (255, 0, 220)]
for i, c in zip(ids, cols):
    m = lb == i
    e = np.zeros_like(m)
    e[:-1, :] |= m[:-1, :] != m[1:, :]
    e[:, :-1] |= m[:, :-1] != m[:, 1:]
    ov[e] = c
sx = (500 - x0) * s if x0 <= 500 < x1 else None
sy = (500 - y0) * s if y0 <= 500 < y1 else None
H = raw.shape[0] + 24
W = raw.shape[1] * 2 + 8
both = Image.new("RGB", (W, H), (20, 20, 20))
both.paste(Image.fromarray(raw), (0, 24))
both.paste(Image.fromarray(ov), (raw.shape[1] + 8, 24))
d = ImageDraw.Draw(both)
try:
    f = ImageFont.truetype("arial.ttf", 14)
except OSError:
    f = ImageFont.load_default()
d.text((4, 4), titel + f"  x {x0}–{x1}, y {y0}–{y1}, {s}-fach, Kontrast gestreckt; rote Marken: Naht", fill=(255, 230, 120), font=f)
for off in (0, raw.shape[1] + 8):
    if sx is not None:
        d.line([(off + sx, 24), (off + sx, 34)], fill=(255, 0, 0), width=2)
        d.line([(off + sx, H - 10), (off + sx, H)], fill=(255, 0, 0), width=2)
    if sy is not None:
        d.line([(off, 24 + sy), (off + 10, 24 + sy)], fill=(255, 0, 0), width=2)
w, h = both.size
k = min(1.0, 2000 / max(w, h))
if k < 1:
    both = both.resize((int(w * k), int(h * k)), Image.LANCZOS)
both.save(out, quality=92)
print(out, both.size)
