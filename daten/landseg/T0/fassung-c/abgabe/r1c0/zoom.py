"""Zoom-Ausschnitte mit Koordinatengitter (25 px) aus dem Teilkachelbild, optional mit Label-Grenzen."""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HIER = Path(__file__).parent
BILD = Path("C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c/teilkacheln/r1c0.png")


def zoom(x0, y0, x1, y1, f, aus, labels=None, nummern=False):
    img = np.array(Image.open(BILD).convert("RGB"))
    crop = img[y0:y1, x0:x1].copy()
    if labels is not None:
        lab = labels[y0:y1, x0:x1]
        rand = np.zeros(lab.shape, bool)
        rand[:-1] |= lab[:-1] != lab[1:]
        rand[:, :-1] |= lab[:, :-1] != lab[:, 1:]
    im = Image.fromarray(crop).resize(((x1 - x0) * f, (y1 - y0) * f), Image.NEAREST)
    d = ImageDraw.Draw(im)
    if labels is not None:
        ys, xs = np.nonzero(rand)
        arr = np.array(im)
        for y, x in zip(ys, xs):
            arr[y * f:(y + 1) * f, x * f:(x + 1) * f] = (255, 255, 0)
        im = Image.fromarray(arr)
        d = ImageDraw.Draw(im)
    try:
        font = ImageFont.truetype("arial.ttf", 12)
    except OSError:
        font = ImageFont.load_default()
    for gx in range((x0 // 25 + 1) * 25, x1, 25):
        X = (gx - x0) * f
        d.line([(X, 0), (X, im.height)], fill=(0, 255, 255) if gx % 100 == 0 else (0, 140, 140), width=1)
        d.text((X + 2, 2), str(gx), fill=(255, 255, 255), font=font)
    for gy in range((y0 // 25 + 1) * 25, y1, 25):
        Y = (gy - y0) * f
        d.line([(0, Y), (im.width, Y)], fill=(0, 255, 255) if gy % 100 == 0 else (0, 140, 140), width=1)
        d.text((2, Y + 2), str(gy), fill=(255, 255, 255), font=font)
    if labels is not None and nummern:
        for sid in np.unique(lab):
            m = lab == sid
            if m.sum() < 30:
                continue
            ys, xs = np.nonzero(m)
            i = len(ys) // 2
            order = np.lexsort((xs, ys))
            cy, cx = ys[order[i]], xs[order[i]]
            d.text((cx * f, cy * f), str(int(sid)), fill=(255, 0, 255), font=font)
    im.save(aus, quality=90)


if __name__ == "__main__":
    x0, y0, x1, y1, f = map(int, sys.argv[1:6])
    aus = sys.argv[6]
    labels = None
    nummern = False
    if len(sys.argv) > 7:
        import tifffile
        labels = tifffile.imread(sys.argv[7])
        nummern = len(sys.argv) > 8
    zoom(x0, y0, x1, y1, f, aus, labels, nummern)
