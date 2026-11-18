"""Dunkle Linien (Schattenkanten) im Segment finden und als nummerierte Linienzüge zeigen (nur Ansicht).

PY -B grate.py --id 400006 --x .. --y .. --b .. --hh .. --f 4 --ziel out.jpg --json linien.json [--min 20]
"""
import argparse
import json
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
from skimage import filters, morphology

sys.path.insert(0, "C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c1/v1")
import werkzeug as wz  # noqa: E402


def ordnen(ys, xs):
    """Skelett-Pixel als Weg ordnen: von einem Endpunkt aus gierig zum nächsten Nachbarn."""
    pts = list(zip(xs.tolist(), ys.tolist()))
    s = set(pts)
    def nb(p):
        return [(p[0] + dx, p[1] + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx or dy) and (p[0] + dx, p[1] + dy) in s]
    ends = [p for p in pts if len(nb(p)) == 1] or [min(pts)]
    start = min(ends)
    weg, besucht, p = [start], {start}, start
    while True:
        kand = [q for q in nb(p) if q not in besucht]
        if not kand:
            break
        q = min(kand, key=lambda q: abs(q[0] - p[0]) + abs(q[1] - p[1]))
        weg.append(q)
        besucht.add(q)
        p = q
    return weg


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--id", type=int, required=True)
    p.add_argument("--x", type=int, required=True)
    p.add_argument("--y", type=int, required=True)
    p.add_argument("--b", type=int, required=True)
    p.add_argument("--hh", type=int, required=True)
    p.add_argument("--f", type=int, default=4)
    p.add_argument("--ziel", required=True)
    p.add_argument("--json")
    p.add_argument("--min", type=int, default=20)
    p.add_argument("--schwelle", type=float, default=6)
    p.add_argument("--stapel")
    a = p.parse_args()
    karte, _ = wz.laden(a.stapel, leise=True)
    img = np.asarray(Image.open(wz.BILD).convert("L")).astype(np.float32)
    maske = karte == a.id
    kern = np.zeros_like(maske)
    kern[64:564, 64:564] = True
    maske &= kern
    r = filters.sato(img, sigmas=[1.0, 1.5, 2.0], black_ridges=True)
    lin = (r > a.schwelle) & maske
    sk = morphology.skeletonize(lin)
    lab, n = ndimage.label(sk, structure=np.ones((3, 3)))
    linien = {}
    k = 0
    for i in range(1, n + 1):
        ys, xs = np.nonzero(lab == i)
        if len(xs) < a.min:
            continue
        k += 1
        weg = ordnen(ys, xs)
        linien[k] = weg
    print("Linien:", len(linien))
    for k, w in linien.items():
        print(k, len(w), w[0], w[-1])
    if a.json:
        json.dump({str(k): v for k, v in linien.items()}, open(a.json, "w"))
    x0, y0, w, h, f = a.x, a.y, a.b, a.hh, a.f
    crop = img[y0:y0 + h, x0:x0 + w]
    rgb = np.kron(np.stack([crop] * 3, -1).astype(np.uint8), np.ones((f, f, 1), np.uint8))
    lab6 = np.kron(maske[y0:y0 + h, x0:x0 + w].astype(np.int32), np.ones((f, f), np.int32))
    rnd = np.zeros(lab6.shape, bool)
    rnd[:, 1:] |= lab6[:, 1:] != lab6[:, :-1]
    rnd[1:, :] |= lab6[1:, :] != lab6[:-1, :]
    rgb[rnd] = (255, 230, 0)
    im = Image.fromarray(rgb)
    d = ImageDraw.Draw(im)
    fn = wz.font(14)
    for k, wg in linien.items():
        pts = [((px - x0) * f + f // 2, (py - y0) * f + f // 2) for px, py in wg]
        d.line(pts, fill=(255, 0, 255), width=2)
        mx, my = pts[len(pts) // 2]
        d.text((mx, my - 8), str(k), fill=(0, 255, 0), font=fn, anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0))
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
