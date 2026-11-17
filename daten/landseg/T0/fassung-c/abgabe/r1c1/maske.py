"""Zeigt ausgewaehlte Segmente farbig ueber dem Bild (Faktor f), mit Gitter.

Aufruf: python maske.py <labels.tif> <ids,komma> <x0> <y0> <b> <h> <f> <ziel.png>
"""
import sys

import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont

BILD = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c/teilkacheln/r1c1.png"
FARBEN = [(255, 0, 0), (0, 128, 255), (255, 0, 255), (255, 255, 0), (0, 255, 0), (255, 128, 0)]


def main():
    L = tifffile.imread(sys.argv[1])
    ids = [int(v) for v in sys.argv[2].split(",")]
    x0, y0, b, h, f = (int(v) for v in sys.argv[3:8])
    im = np.asarray(Image.open(BILD).convert("RGB")).astype(float)
    a = im[y0:y0 + h, x0:x0 + b].copy()
    Lc = L[y0:y0 + h, x0:x0 + b]
    for k, i in enumerate(ids):
        m = Lc == i
        a[m] = a[m] * 0.55 + np.array(FARBEN[k % len(FARBEN)]) * 0.45
    img = Image.fromarray(a.astype(np.uint8)).resize((b * f, h * f), Image.NEAREST)
    d = ImageDraw.Draw(img)
    try:
        fs = ImageFont.truetype("arial.ttf", 11)
    except OSError:
        fs = ImageFont.load_default()
    for x in range((x0 // 20 + 1) * 20, x0 + b, 20):
        d.line([(( x - x0) * f, 0), ((x - x0) * f, h * f)], fill=(0, 200, 255))
        d.text(((x - x0) * f + 2, 2), str(x), fill=(0, 255, 255), font=fs, stroke_width=2, stroke_fill=(0, 0, 0))
    for y in range((y0 // 20 + 1) * 20, y0 + h, 20):
        d.line([(0, (y - y0) * f), (b * f, (y - y0) * f)], fill=(0, 200, 255))
        d.text((2, (y - y0) * f + 2), str(y), fill=(0, 255, 255), font=fs, stroke_width=2, stroke_fill=(0, 0, 0))
    img.save(sys.argv[8])


if __name__ == "__main__":
    main()
