"""Vorschlag: Segment per Wasserscheide auf dunklen Linien zerlegen (nur Ansicht, schreibt nichts auf die Karte).

PY -B wscheide.py --id 400006 --h 20 --min 150 --ziel out.jpg --x 190 --y 64 --b 250 --hh 250 --f 4 [--npy out.npy]
"""
import argparse
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
from skimage import filters, morphology, segmentation, measure

sys.path.insert(0, "C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c1/v1")
import werkzeug as wz  # noqa: E402


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--id", type=int, required=True)
    p.add_argument("--h", type=float, default=20)
    p.add_argument("--sigma", type=float, default=1.2)
    p.add_argument("--min", type=int, default=150)
    p.add_argument("--ziel", required=True)
    p.add_argument("--x", type=int, required=True)
    p.add_argument("--y", type=int, required=True)
    p.add_argument("--b", type=int, required=True)
    p.add_argument("--hh", type=int, required=True)
    p.add_argument("--f", type=int, default=4)
    p.add_argument("--npy")
    p.add_argument("--stapel")
    a = p.parse_args()
    karte, _ = wz.laden(a.stapel, leise=True)
    img = np.asarray(Image.open(wz.BILD).convert("L")).astype(np.float32)
    g = filters.gaussian(img, a.sigma, preserve_range=True)
    maske = karte == a.id
    kern = np.zeros_like(maske)
    kern[64:564, 64:564] = True
    maske &= kern
    marker = morphology.h_maxima(np.where(maske, g, 0), a.h) & maske
    marker, n = ndimage.label(marker)
    reg = segmentation.watershed(-g, marker, mask=maske)
    # kleine Regionen dem größten Nachbarn geben
    changed = True
    while changed:
        changed = False
        groessen = np.bincount(reg.ravel())
        for r in range(1, len(groessen)):
            if 0 < groessen[r] < a.min:
                m = reg == r
                rand = ndimage.binary_dilation(m) & ~m & maske
                nb = reg[rand]
                nb = nb[nb != r]
                if len(nb):
                    reg[m] = np.bincount(nb).argmax()
                    changed = True
                    break
    print("Regionen:", len(np.unique(reg)) - 1)
    for r in np.unique(reg):
        if r == 0:
            continue
        m = reg == r
        ys, xs = np.nonzero(m)
        print(r, int(m.sum()), f"x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()} grau={img[m].mean():.0f}")
    if a.npy:
        np.save(a.npy, reg)
    x0, y0, w, h, f = a.x, a.y, a.b, a.hh, a.f
    crop = img[y0:y0 + h, x0:x0 + w]
    rgb = np.kron(np.stack([crop] * 3, -1).astype(np.uint8), np.ones((f, f, 1), np.uint8))
    lab = np.kron(reg[y0:y0 + h, x0:x0 + w], np.ones((f, f), np.int32))
    rnd = np.zeros(lab.shape, bool)
    rnd[:, 1:] |= lab[:, 1:] != lab[:, :-1]
    rnd[1:, :] |= lab[1:, :] != lab[:-1, :]
    rgb[rnd] = (255, 0, 255)
    im = Image.fromarray(rgb)
    d = ImageDraw.Draw(im)
    fn = wz.font(14)
    for r in np.unique(reg[y0:y0 + h, x0:x0 + w]):
        if r == 0:
            continue
        m = reg[y0:y0 + h, x0:x0 + w] == r
        dist = ndimage.distance_transform_edt(np.pad(m, 1))[1:-1, 1:-1]
        yy, xx = np.unravel_index(np.argmax(dist), dist.shape)
        d.text((xx * f, yy * f), str(r), fill=(0, 255, 0), font=fn, anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0))
    fs = wz.font(11)
    for xv in range((x0 // 10 + 1) * 10, x0 + w, 10):
        d.line([((xv - x0) * f, 0), ((xv - x0) * f, 6)], fill=(255, 0, 0), width=2)
        d.text(((xv - x0) * f + 2, 7), str(xv), fill=(255, 80, 80), font=fs)
    for yv in range((y0 // 10 + 1) * 10, y0 + h, 10):
        d.line([(0, (yv - y0) * f), (6, (yv - y0) * f)], fill=(255, 0, 0), width=2)
        d.text((8, (yv - y0) * f - 6), str(yv), fill=(255, 80, 80), font=fs)
    im.save(a.ziel, quality=90)


if __name__ == "__main__":
    main()
