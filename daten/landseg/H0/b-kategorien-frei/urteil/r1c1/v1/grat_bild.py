"""Ansicht: Kontrastbild mit Gitterlinien alle 10 px und dunklen Graten (sato) magenta, Segmentgrenzen gelb.

PY -B grat_bild.py --x .. --y .. --b .. --hh .. --f 4 --ziel out.jpg [--schwelle 4] [--linien json] [--stapel s.json]
"""
import argparse
import json
import sys

import numpy as np
from PIL import Image, ImageDraw
from skimage import filters

sys.path.insert(0, "C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c1/v1")
import werkzeug as wz  # noqa: E402


def main():
    p = argparse.ArgumentParser()
    for k in ("x", "y", "b", "hh", "f"):
        p.add_argument("--" + k, type=int, required=True)
    p.add_argument("--ziel", required=True)
    p.add_argument("--schwelle", type=float, default=4)
    p.add_argument("--linien")
    p.add_argument("--stapel")
    p.add_argument("--ohne_grat", action="store_true")
    a = p.parse_args()
    karte, _ = wz.laden(a.stapel, leise=True)
    img = np.asarray(Image.open(wz.BILD).convert("L")).astype(np.float32)
    x0, y0, w, h, f = a.x, a.y, a.b, a.hh, a.f
    crop = img[y0:y0 + h, x0:x0 + w]
    lo, hi = np.percentile(crop, 1), np.percentile(crop, 99)
    crop = np.clip((crop - lo) / max(hi - lo, 1) * 255, 0, 255)
    rgb = np.kron(np.stack([crop] * 3, -1).astype(np.uint8), np.ones((f, f, 1), np.uint8))
    if not a.ohne_grat:
        r = filters.sato(img, sigmas=[1.0, 1.5], black_ridges=True)[y0:y0 + h, x0:x0 + w]
        rm = np.kron((r > a.schwelle).astype(np.uint8), np.ones((f, f), np.uint8)).astype(bool)
        rgb[rm] = (rgb[rm] * 0.4 + np.array([255, 0, 255]) * 0.6).astype(np.uint8)
    # Gitter
    for xv in range((x0 // 10 + 1) * 10, x0 + w, 10):
        rgb[:, (xv - x0) * f] = (0, 140, 255) if xv % 50 else (0, 255, 255)
    for yv in range((y0 // 10 + 1) * 10, y0 + h, 10):
        rgb[(yv - y0) * f, :] = (0, 140, 255) if yv % 50 else (0, 255, 255)
    lab = np.kron(karte[y0:y0 + h, x0:x0 + w], np.ones((f, f), np.uint32))
    rnd = np.zeros(lab.shape, bool)
    rnd[:, 1:] |= lab[:, 1:] != lab[:, :-1]
    rnd[1:, :] |= lab[1:, :] != lab[:-1, :]
    rgb[rnd] = (255, 230, 0)
    im = Image.fromarray(rgb)
    d = ImageDraw.Draw(im)
    fs = wz.font(11)
    for xv in range((x0 // 10 + 1) * 10, x0 + w, 10):
        d.text(((xv - x0) * f + 2, 2), str(xv), fill=(255, 255, 255), font=fs, stroke_width=2, stroke_fill=(0, 0, 0))
    for yv in range((y0 // 10 + 1) * 10, y0 + h, 10):
        d.text((2, (yv - y0) * f + 1), str(yv), fill=(255, 255, 255), font=fs, stroke_width=2, stroke_fill=(0, 0, 0))
    if a.linien:
        data = json.loads(open(a.linien, encoding="utf-8").read())
        for nr, lz in enumerate(data, 1):
            pts = [((px - x0) * f + f // 2, (py - y0) * f + f // 2) for px, py in lz]
            d.line(pts, fill=(0, 255, 0), width=2)
            d.text(pts[0], str(nr), fill=(0, 255, 0), font=wz.font(14), stroke_width=2, stroke_fill=(0, 0, 0))
    im.save(a.ziel, quality=90)
    print(a.ziel, im.size)


if __name__ == "__main__":
    main()
