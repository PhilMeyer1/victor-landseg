"""Vergroesserte Ausschnitte der Teilkachel mit Gitter (Bildpunkte der Teilkachel) zum Ansehen.

Aufruf: python zoom.py <x0> <y0> <breite> <hoehe> <faktor> <ziel.png> [labels.tif]
"""
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

BILD = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c/teilkacheln/r1c1.png"


def main():
    x0, y0, b, h, f = (int(v) for v in sys.argv[1:6])
    ziel = sys.argv[6]
    lab = sys.argv[7] if len(sys.argv) > 7 else None
    im = Image.open(BILD).convert("RGB")
    a = np.asarray(im)[y0:y0 + h, x0:x0 + b]
    if lab:
        import tifffile
        L = tifffile.imread(lab)[y0:y0 + h, x0:x0 + b]
        grenze = np.zeros(L.shape, bool)
        grenze[:, 1:] |= L[:, 1:] != L[:, :-1]
        grenze[1:, :] |= L[1:, :] != L[:-1, :]
    big = Image.fromarray(a).resize((b * f, h * f), Image.NEAREST)
    if lab:
        g = np.asarray(Image.fromarray(grenze.astype(np.uint8) * 255).resize((b * f, h * f), Image.NEAREST)) > 0
        arr = np.asarray(big).copy()
        arr[g] = (255, 255, 0)
        big = Image.fromarray(arr)
    d = ImageDraw.Draw(big)
    try:
        font = ImageFont.truetype("arial.ttf", 13)
    except OSError:
        font = ImageFont.load_default()
    step = 20
    for x in range((x0 // step + 1) * step, x0 + b, step):
        X = (x - x0) * f
        d.line([(X, 0), (X, h * f)], fill=(0, 255, 255) if x % 100 else (255, 0, 0), width=1)
        d.text((X + 2, 2), str(x), fill=(255, 255, 255), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
    for y in range((y0 // step + 1) * step, y0 + h, step):
        Y = (y - y0) * f
        d.line([(0, Y), (b * f, Y)], fill=(0, 255, 255) if y % 100 else (255, 0, 0), width=1)
        d.text((2, Y + 2), str(y), fill=(255, 255, 255), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
    big.save(ziel)


if __name__ == "__main__":
    main()
