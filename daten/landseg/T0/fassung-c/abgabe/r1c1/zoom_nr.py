"""Vergroesserter Ausschnitt mit Segmentgrenzen und Nummern (ID minus Basis) und Gitter.

Aufruf: python zoom_nr.py <labels.tif> <segmente.json|-> <x0> <y0> <breite> <hoehe> <faktor> <ziel.png> [basis] [--klasse]
"""
import json
import sys

import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont

BILD = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c/teilkacheln/r1c1.png"


def main():
    lab, segp = sys.argv[1], sys.argv[2]
    x0, y0, b, h, f = (int(v) for v in sys.argv[3:8])
    ziel = sys.argv[8]
    basis = int(sys.argv[9]) if len(sys.argv) > 9 and not sys.argv[9].startswith("--") else 0
    mit_klasse = "--klasse" in sys.argv
    klassen = {}
    if segp != "-":
        for s in json.load(open(segp, encoding="utf-8"))["segmente"]:
            klassen[s["id"]] = s["klasse"]
    im = np.asarray(Image.open(BILD).convert("RGB"))
    L = tifffile.imread(lab)
    a = im[y0:y0 + h, x0:x0 + b]
    Lc = L[y0:y0 + h, x0:x0 + b]
    gr = np.zeros(Lc.shape, bool)
    gr[:, 1:] |= Lc[:, 1:] != Lc[:, :-1]
    gr[1:, :] |= Lc[1:, :] != Lc[:-1, :]
    big = np.asarray(Image.fromarray(a).resize((b * f, h * f), Image.NEAREST)).copy()
    gb = np.asarray(Image.fromarray(gr.astype(np.uint8) * 255).resize((b * f, h * f), Image.NEAREST)) > 0
    big[gb] = (255, 255, 0)
    img = Image.fromarray(big)
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 12)
        fs = ImageFont.truetype("arial.ttf", 11)
    except OSError:
        font = fs = ImageFont.load_default()
    step = 20
    for x in range((x0 // step + 1) * step, x0 + b, step):
        X = (x - x0) * f
        d.line([(X, 0), (X, h * f)], fill=(0, 200, 255), width=1)
        d.text((X + 2, 2), str(x), fill=(0, 255, 255), font=fs, stroke_width=2, stroke_fill=(0, 0, 0))
    for y in range((y0 // step + 1) * step, y0 + h, step):
        Y = (y - y0) * f
        d.line([(0, Y), (b * f, Y)], fill=(0, 200, 255), width=1)
        d.text((2, Y + 2), str(y), fill=(0, 255, 255), font=fs, stroke_width=2, stroke_fill=(0, 0, 0))
    from scipy import ndimage
    ids = np.unique(Lc)
    for i in ids:
        m = Lc == i
        # Punkt im Inneren: Maximum der Distanztransformation
        dt = ndimage.distance_transform_edt(m)
        yy, xx = np.unravel_index(np.argmax(dt), dt.shape)
        t = str(int(i) - basis)
        if mit_klasse and int(i) in klassen:
            t += ":" + klassen[int(i)]
        d.text((xx * f, yy * f), t, fill=(255, 255, 255), font=font, anchor="mm", stroke_width=2,
               stroke_fill=(0, 0, 0))
    img.save(ziel)


if __name__ == "__main__":
    main()
