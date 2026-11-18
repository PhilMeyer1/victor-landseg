"""Renders the current label map state for quarter v2 (own check image, not for submission)."""
import sys, json
import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont

B = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/"
L = tifffile.imread(B + "c-feste-liste/r0c0/labels.tif")
img = np.array(Image.open(B + "teilkacheln/r0c0.png").convert("RGB"))
x0, y0, w, h, f = [int(v) for v in sys.argv[1:6]]
out = sys.argv[6]
mode = sys.argv[7] if len(sys.argv) > 7 else "nummern"
sub = L[y0:y0 + h, x0:x0 + w]
im = img[y0:y0 + h, x0:x0 + w].astype(float)
if mode == "kontrast":
    lo, hi = np.percentile(im, 2), np.percentile(im, 98)
    im = np.clip((im - lo) / max(hi - lo, 1) * 255, 0, 255)
big = np.kron(im, np.ones((f, f, 1))).astype(np.uint8)
lab = np.kron(sub, np.ones((f, f), dtype=sub.dtype))
if mode in ("nummern", "kontrast_n"):
    edge = np.zeros(lab.shape, bool)
    edge[:, 1:] |= lab[:, 1:] != lab[:, :-1]
    edge[1:, :] |= lab[1:, :] != lab[:-1, :]
    big[edge] = [255, 230, 0]
pil = Image.fromarray(big)
d = ImageDraw.Draw(pil)
try:
    font = ImageFont.truetype("arial.ttf", 13)
except Exception:
    font = ImageFont.load_default()
# quarter frame
qx0, qy0, qx1, qy1 = 314, 64, 563, 313
d.rectangle([(qx0 - x0) * f, (qy0 - y0) * f, (qx1 + 1 - x0) * f, (qy1 + 1 - y0) * f], outline=(0, 255, 255), width=2)
if mode in ("nummern", "kontrast_n"):
    for i in np.unique(sub):
        ys, xs = np.nonzero(sub == i)
        if len(xs) < 15:
            continue
        cy, cx = np.median(ys), np.median(xs)
        k = np.argmin((ys - cy) ** 2 + (xs - cx) ** 2)
        t = str(int(i) % 100000)
        px, py = xs[k] * f, ys[k] * f
        d.text((px - 8, py - 7), t, fill=(255, 255, 255), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
pil.save(out, quality=90)
print(out, pil.size)
