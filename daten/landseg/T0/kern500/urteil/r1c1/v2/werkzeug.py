"""Eigene Hilfen fuer das Urteil r1c1/v2 (nur lesen der Eingaben, Bilder nur in diesen Ordner)."""
import json
import sys
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

BASIS = Path("C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500")
ZIEL = BASIS / "urteil/r1c1/v2"
LAB = tifffile.imread(str(BASIS / "vorstufe/r1c1/labels.tif")).astype(np.int64)
IMG = np.array(Image.open(BASIS / "teilkacheln/r1c1.png").convert("RGB"))
SEG = {s["id"]: s for s in json.load(open(BASIS / "vorstufe/r1c1/segmente.json", encoding="utf-8"))["segmente"]}
VX0, VY0, VX1, VY1 = 314, 64, 564, 314


def font(sz):
    for f in ("C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"):
        try:
            return ImageFont.truetype(f, sz)
        except OSError:
            pass
    return ImageFont.load_default()


def grenzen(lab):
    g = np.zeros(lab.shape, bool)
    g[:, 1:] |= lab[:, 1:] != lab[:, :-1]
    g[1:, :] |= lab[1:, :] != lab[:-1, :]
    return g


def ausschnitt(x0, y0, w, h, f, name, hervor=(), kontrast=False, nummern=True):
    sub = IMG[y0:y0 + h, x0:x0 + w]
    lab = LAB[y0:y0 + h, x0:x0 + w]
    im = Image.fromarray(sub).resize((w * f, h * f), Image.NEAREST)
    if kontrast:
        im = ImageEnhance.Contrast(ImageEnhance.Brightness(im).enhance(1.25)).enhance(1.8)
    big = np.kron(lab, np.ones((f, f), dtype=np.int64))
    g = grenzen(big)
    arr = np.array(im)
    arr[g] = (255, 230, 0)
    for hid in hervor:
        m = big == hid
        gm = np.zeros(m.shape, bool)
        gm[:, 1:] |= m[:, 1:] != m[:, :-1]
        gm[1:, :] |= m[1:, :] != m[:-1, :]
        gm2 = gm.copy()
        gm2[1:, :] |= gm[:-1, :]
        gm2[:, 1:] |= gm[:, :-1]
        arr[gm2] = (255, 40, 40)
    im = Image.fromarray(arr)
    d = ImageDraw.Draw(im)
    # viertel cyan
    d.rectangle([(VX0 - x0) * f, (VY0 - y0) * f, (VX1 - x0) * f, (VY1 - y0) * f], outline=(0, 255, 255), width=2)
    if nummern:
        fo = font(max(11, f * 2))
        for sid in np.unique(lab):
            ys, xs = np.nonzero(lab == sid)
            if len(xs) < 3:
                continue
            # punkt nahe Schwerpunkt im Segment
            cx, cy = xs.mean(), ys.mean()
            k = np.argmin((xs - cx) ** 2 + (ys - cy) ** 2)
            t = str(sid % 100000)
            px, py = xs[k] * f, ys[k] * f
            d.text((px, py), t, fill=(255, 255, 255), font=fo, anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0))
    # koordinaten-skala
    fo2 = font(12)
    for xx in range(x0 - x0 % 10 + 10, x0 + w, 10):
        d.line([((xx - x0) * f, 0), ((xx - x0) * f, 6)], fill=(255, 255, 255))
        if xx % 20 == 0:
            d.text(((xx - x0) * f + 2, 6), str(xx), fill=(255, 255, 255), font=fo2, stroke_width=1, stroke_fill=(0, 0, 0))
    for yy in range(y0 - y0 % 10 + 10, y0 + h, 10):
        d.line([(0, (yy - y0) * f), (6, (yy - y0) * f)], fill=(255, 255, 255))
        if yy % 20 == 0:
            d.text((8, (yy - y0) * f - 6), str(yy), fill=(255, 255, 255), font=fo2, stroke_width=1, stroke_fill=(0, 0, 0))
    im.save(ZIEL / name, quality=90)
    print("geschrieben", ZIEL / name, im.size)


def info(ids):
    for sid in ids:
        m = LAB == sid
        ys, xs = np.nonzero(m)
        kern = m[64:564, 64:564].sum()
        rgb = IMG[m].mean(0).round().astype(int)
        sd = IMG[m].std(0).mean().round(1)
        # nachbarn
        nb = {}
        for dy, dx in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            sh = np.roll(np.roll(LAB, dy, 0), dx, 1)
            r = sh[m]
            for v, c in zip(*np.unique(r[r != sid], return_counts=True)):
                nb[int(v)] = nb.get(int(v), 0) + int(c)
        nbs = sorted(nb.items(), key=lambda t: -t[1])[:6]
        s = SEG.get(sid, {})
        # zusammenhang
        import cv2
        n, _ = cv2.connectedComponents(m.astype(np.uint8), connectivity=4)
        print(sid, s.get("klasse"), s.get("herkunft"), "fl", int(m.sum()), "kern", int(kern),
              "bbox", xs.min(), ys.min(), xs.max(), ys.max(), "rgb", list(rgb), "sd", sd, "teile", n - 1,
              "nb", [(k % 100000, c, SEG.get(k, {}).get("klasse")) for k, c in nbs])


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "info":
        info([int(a) for a in sys.argv[2:]])
    elif cmd == "bild":
        x0, y0, w, h, f = map(int, sys.argv[2:7])
        name = sys.argv[7]
        hv = [int(a) for a in sys.argv[8:] if a.isdigit()]
        ausschnitt(x0, y0, w, h, f, name, hervor=hv, kontrast="kontrast" in sys.argv, nummern="ohne" not in sys.argv)
