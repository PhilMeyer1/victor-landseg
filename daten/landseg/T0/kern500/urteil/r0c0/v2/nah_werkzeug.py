"""Eigene Nahansichten (roh und mit Grenzen/Nummern) aus Teilkachelbild und Label-Karte.

Aufruf: PY nah_werkzeug.py x0 y0 breite hoehe faktor name
Schreibt <name>.jpg in diesen Ordner: links unverändert, rechts mit Grenzen (gelb), Nummern
(ID mod 100000) und Randmarken alle 10 Bildpunkte der Teilkachel (cyan).
"""
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

HIER = Path(__file__).resolve().parent
DATEN = Path("C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500")


def lade():
    roh = np.array(Image.open(DATEN / "teilkacheln" / "r0c0.png").convert("RGB"))
    import tifffile  # noqa
    lab = tifffile.imread(str(DATEN / "vorstufe" / "r0c0" / "labels.tif")).astype(np.int64)
    return roh, lab


def schrift(g):
    for f in ("C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"):
        try:
            return ImageFont.truetype(f, g)
        except OSError:
            pass
    return ImageFont.load_default()


def bild(x0, y0, w, h, fk, name, kontrast=False):
    roh, lab = lade()
    r = roh[y0:y0 + h, x0:x0 + w].copy()
    l = lab[y0:y0 + h, x0:x0 + w]
    if kontrast:
        lab_c = cv2.cvtColor(r, cv2.COLOR_RGB2LAB)
        cl = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(4, 4))
        lab_c[:, :, 0] = cl.apply(lab_c[:, :, 0])
        r = cv2.cvtColor(lab_c, cv2.COLOR_LAB2RGB)
    gr = np.kron(r, np.ones((fk, fk, 1), dtype=np.uint8))
    links = Image.fromarray(gr)
    lg = np.kron(l, np.ones((fk, fk), dtype=np.int64))
    rand = np.zeros(lg.shape, bool)
    rand[:, 1:] |= lg[:, 1:] != lg[:, :-1]
    rand[1:, :] |= lg[1:, :] != lg[:-1, :]
    out = gr.copy()
    out[rand] = (255, 255, 0)
    im = Image.fromarray(out)
    d = ImageDraw.Draw(im)
    f = schrift(max(12, min(22, fk * 4)))
    for sid in np.unique(l):
        m = l == sid
        dt = ndimage.distance_transform_edt(np.pad(m, 1))[1:-1, 1:-1]
        yy, xx = np.unravel_index(np.argmax(dt), dt.shape)
        t = str(sid % 100000)
        cx, cy = xx * fk + fk // 2, yy * fk + fk // 2
        d.text((cx, cy), t, fill=(255, 255, 255), font=f, anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0))
    # Gitter alle 10 px der Teilkachel als Randmarken
    f2 = schrift(12)
    for gx in range((x0 // 10 + 1) * 10, x0 + w, 10):
        px = (gx - x0) * fk
        d.line([(px, 0), (px, 6)], fill=(0, 255, 255), width=1)
        if gx % 20 == 0:
            d.text((px, 8), str(gx), fill=(0, 255, 255), font=f2, anchor="mt", stroke_width=1, stroke_fill=(0, 0, 0))
    for gy in range((y0 // 10 + 1) * 10, y0 + h, 10):
        py = (gy - y0) * fk
        d.line([(0, py), (6, py)], fill=(0, 255, 255), width=1)
        if gy % 20 == 0:
            d.text((8, py), str(gy), fill=(0, 255, 255), font=f2, anchor="lm", stroke_width=1, stroke_fill=(0, 0, 0))
    ges = Image.new("RGB", (im.width * 2 + 8, im.height), (0, 0, 0))
    ges.paste(links, (0, 0))
    ges.paste(im, (im.width + 8, 0))
    ges.save(HIER / f"{name}.jpg", quality=90)


if __name__ == "__main__":
    a = sys.argv[1:]
    bild(int(a[0]), int(a[1]), int(a[2]), int(a[3]), int(a[4]), a[5], kontrast=len(a) > 6 and a[6] == "k")
