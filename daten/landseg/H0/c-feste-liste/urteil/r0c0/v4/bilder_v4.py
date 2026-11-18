"""Eigene Bilder des Viertels v4 aus der aktuellen Karte (urt-c-r0c0-v4).
Aufruf: bilder_v4.py <modus> [args]
  umriss <name> x0 y0 x1 y1 faktor   -> Grenzen + Nummern
  roh    <name> x0 y0 x1 y1 faktor   -> unverändert
  kontrast <name> x0 y0 x1 y1 faktor
"""
import json, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import tifffile
from scipy import ndimage as ndi

B = "C:/Users/Phil/Developement/Victor/daten/landseg/H0"
OUT = B + "/c-feste-liste/urteil/r0c0/v4/"
lab = tifffile.imread(B + "/c-feste-liste/r0c0/labels.tif").astype(np.int64)
img = np.array(Image.open(B + "/teilkacheln/r0c0.png").convert("L"))
FONT = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 15)
LISTE = {100172,100180,100143,100178,100165,100185,100187,100183,100189,100186,100194,100198,100196,100176,100207,100201,100209,100216,100195,100210,100214,100211,100218,100215,100224,100220,100225,100219,100228,100229}
V4 = (314, 314, 564, 564)
KERN = (64, 64, 564, 564)


def ausschnitt(x0, y0, x1, y1, f, kontrast=False):
    a = img[y0:y1, x0:x1].astype(float)
    if kontrast:
        lo, hi = np.percentile(a, 1), np.percentile(a, 99)
        a = np.clip((a - lo) / max(hi - lo, 1) * 255, 0, 255)
    a = a.astype(np.uint8)
    im = Image.fromarray(a).resize(((x1 - x0) * f, (y1 - y0) * f), Image.NEAREST).convert("RGB")
    return im


def rahmen(d, box, x0, y0, f, farbe, breite=2):
    bx0, by0, bx1, by1 = box
    d.rectangle([(bx0 - x0) * f, (by0 - y0) * f, (bx1 - x0) * f - 1, (by1 - y0) * f - 1], outline=farbe, width=breite)


def umriss(x0, y0, x1, y1, f, nummern=True, klassen=None):
    im = ausschnitt(x0, y0, x1, y1, f)
    L = lab[y0:y1, x0:x1]
    Lu = np.kron(L, np.ones((f, f), dtype=np.int64))
    g = np.zeros_like(Lu, bool)
    g[:, 1:] |= Lu[:, 1:] != Lu[:, :-1]
    g[1:, :] |= Lu[1:, :] != Lu[:-1, :]
    arr = np.array(im)
    arr[g] = (255, 230, 0)
    im = Image.fromarray(arr)
    d = ImageDraw.Draw(im)
    rahmen(d, KERN, x0, y0, f, (255, 255, 255), 1)
    rahmen(d, V4, x0, y0, f, (0, 230, 230), 3)
    if nummern:
        for i in np.unique(L):
            m = L == i
            dt = ndi.distance_transform_edt(np.pad(m, 1))[1:-1, 1:-1]
            yy, xx = np.unravel_index(np.argmax(dt), dt.shape)
            t = str(i % 100000)
            if klassen and i in klassen:
                t += " " + klassen[i]
            col = (255, 255, 255) if i in LISTE else (170, 170, 170)
            px, py = xx * f + f // 2, yy * f + f // 2
            bb = d.textbbox((px, py), t, font=FONT, anchor="mm")
            d.rectangle(bb, fill=(0, 0, 0))
            d.text((px, py), t, fill=col, font=FONT, anchor="mm")
    return im


if __name__ == "__main__":
    modus, name = sys.argv[1], sys.argv[2]
    x0, y0, x1, y1, f = map(int, sys.argv[3:8])
    if modus == "umriss":
        im = umriss(x0, y0, x1, y1, f)
    elif modus == "roh":
        im = ausschnitt(x0, y0, x1, y1, f)
        rahmen(ImageDraw.Draw(im), V4, x0, y0, f, (0, 230, 230), 2)
    else:
        im = ausschnitt(x0, y0, x1, y1, f, True)
        rahmen(ImageDraw.Draw(im), V4, x0, y0, f, (0, 230, 230), 2)
    im.save(OUT + name, quality=90)
    print(OUT + name, im.size)
