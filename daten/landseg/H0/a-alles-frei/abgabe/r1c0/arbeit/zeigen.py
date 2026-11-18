import json
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi

ORD = r"C:/Users/Phil/Developement/Victor/daten/landseg/H0/a-alles-frei/abgabe/r1c0/arbeit/"
b = np.array(Image.open(r"C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r1c0.png")).astype(float)
if b.ndim == 3:
    b = b[..., 0]
import tifffile
karte = tifffile.imread(r"C:/Users/Phil/Developement/Victor/daten/landseg/H0/a-alles-frei/abgabe/r1c0/labels.tif").astype(np.int64) if len(sys.argv) > 7 else np.load(ORD + "karte_roh.npy")
x0, y0, x1, y1, s = map(int, sys.argv[1:6])
out = sys.argv[6]
lo, hi = np.percentile(b, 1), np.percentile(b, 99.5)
bb = np.clip((b - lo) / (hi - lo) * 255, 0, 255)
crop = bb[y0:y1, x0:x1]
k = karte[y0:y1, x0:x1]
rgb = np.repeat(crop[..., None], 3, -1)
big = np.kron(rgb, np.ones((s, s, 1)))
kb = np.kron(k, np.ones((s, s), int))
grenze = np.zeros(kb.shape, bool)
grenze[:-1, :] |= kb[:-1, :] != kb[1:, :]
grenze[:, :-1] |= kb[:, :-1] != kb[:, 1:]
big[grenze] = [255, 230, 0]
im = Image.fromarray(big.astype(np.uint8))
d = ImageDraw.Draw(im)
f = ImageFont.truetype("arial.ttf", 13)
# Kern
d.rectangle([(64 - x0) * s, (64 - y0) * s, (564 - x0) * s, (564 - y0) * s], outline=(0, 255, 255), width=1)
for v in range(0, 628, 50):
    if x0 < v < x1:
        d.text(((v - x0) * s + 2, 2), str(v), fill=(0, 255, 255), font=f)
    if y0 < v < y1:
        d.text((2, (v - y0) * s + 2), str(v), fill=(0, 255, 255), font=f)
for i in np.unique(k):
    m = k == i
    lab, n = ndi.label(m)
    gr = ndi.sum(m, lab, range(1, n + 1))
    j = int(np.argmax(gr)) + 1
    dist = ndi.distance_transform_edt(lab == j)
    yy, xx = np.unravel_index(np.argmax(dist), dist.shape)
    d.text((xx * s - 6, yy * s - 7), str(i), fill=(255, 60, 60), font=f, stroke_width=2, stroke_fill=(0, 0, 0))
im.save(ORD + out, quality=90)
