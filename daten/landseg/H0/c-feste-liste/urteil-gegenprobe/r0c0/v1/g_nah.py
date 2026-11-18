"""Eigene Nahansichten des aktuellen Kartenstands (Gegenprobe v1, Neufassung)."""
import json
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASIS = "C:/Users/Phil/Developement/Victor/daten/landseg/H0"
KARTE = BASIS + "/c-feste-liste/gegenprobe/r0c0/labels.tif"
BILD = BASIS + "/teilkacheln/r0c0.png"
ZIEL = BASIS + "/c-feste-liste/urteil-gegenprobe/r0c0/v1/"


def lade():
    try:
        import tifffile
        lab = tifffile.imread(KARTE)
    except ImportError:
        lab = np.array(Image.open(KARTE))
    img = np.array(Image.open(BILD).convert("RGB"))
    return lab.astype(np.int64), img


def font(gr):
    for f in ("C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"):
        try:
            return ImageFont.truetype(f, gr)
        except OSError:
            pass
    return ImageFont.load_default()


def render(x0, y0, w, h, f, name, eigene, kontrast=False, nummern=True):
    lab, img = lade()
    sub = img[y0:y0 + h, x0:x0 + w].astype(float)
    if kontrast:
        lo, hi = np.percentile(sub, 2), np.percentile(sub, 98)
        sub = np.clip((sub - lo) / max(hi - lo, 1) * 255, 0, 255)
    sub = sub.astype(np.uint8)
    L = lab[y0:y0 + h, x0:x0 + w]
    big = np.kron(sub, np.ones((f, f, 1), dtype=np.uint8))
    if nummern:
        Lb = np.kron(L, np.ones((f, f), dtype=np.int64))
        rand = np.zeros(Lb.shape, bool)
        rand[:-1, :] |= Lb[:-1, :] != Lb[1:, :]
        rand[:, :-1] |= Lb[:, :-1] != Lb[:, 1:]
        big[rand] = (255, 230, 0)
    im = Image.fromarray(big)
    d = ImageDraw.Draw(im)
    # Viertel v1: x 64-313, y 64-313
    vx0, vy0 = (64 - x0) * f, (64 - y0) * f
    vx1, vy1 = (314 - x0) * f, (314 - y0) * f
    d.rectangle([vx0, vy0, vx1, vy1], outline=(0, 230, 230), width=2)
    if nummern:
        fo = font(max(12, f * 2 + 2))
        for i in np.unique(L):
            m = L == i
            ys, xs = np.nonzero(m)
            # Punkt nahe Schwerpunkt, aber im Segment
            cy, cx = ys.mean(), xs.mean()
            k = np.argmin((ys - cy) ** 2 + (xs - cx) ** 2)
            px, py = xs[k] * f, ys[k] * f
            t = str(i % 100000)
            col = (255, 255, 255) if i in eigene else (170, 170, 170)
            d.text((px, py), t, fill=col, font=fo, anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0))
    im.save(ZIEL + name, quality=90)
    print(name, im.size)


if __name__ == "__main__":
    eigene = set(json.loads(sys.argv[1])) if len(sys.argv) > 1 else set()
    f = 6
    teile = [(52, 52), (177, 52), (52, 177), (177, 177)]
    for n, (x, y) in enumerate(teile, 1):
        render(x, y, 149, 149, f, f"nah_{n}.jpg", eigene)
        render(x, y, 149, 149, f, f"nah_{n}_roh.jpg", eigene, nummern=False)
    render(52, 52, 274, 274, 3, "kontrast_1.jpg", eigene, kontrast=True)
