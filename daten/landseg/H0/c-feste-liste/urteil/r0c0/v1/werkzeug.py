"""Hilfswerkzeug urt-c-r0c0: Kennzahlen je Segment und eigene Nahansichten (nur lesen, schreibt nur Bilder)."""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont

H0 = Path("C:/Users/Phil/Developement/Victor/daten/landseg/H0")
LAB = H0 / "c-feste-liste/r0c0/labels.tif"
SEG = H0 / "c-feste-liste/r0c0/segmente.json"
BILD = H0 / "teilkacheln/r0c0.png"
K0, K1 = 64, 564


def lade():
    lab = tifffile.imread(str(LAB)).astype(np.int64)
    img = np.array(Image.open(BILD).convert("L")).astype(np.float64)
    seg = {s["id"]: s for s in json.loads(SEG.read_text(encoding="utf-8"))["segmente"]}
    return lab, img, seg


def stats(ids):
    lab, img, seg = lade()
    kern = np.zeros(lab.shape, bool)
    kern[K0:K1, K0:K1] = True
    for i in ids:
        m = lab == i
        if not m.any():
            print(i, "nicht auf Karte")
            continue
        mk = m & kern
        ys, xs = np.nonzero(m)
        v = img[m]
        # Nachbarn: Grenzlänge
        nb = {}
        for dy, dx in ((0, 1), (1, 0)):
            a = lab[: lab.shape[0] - dy, : lab.shape[1] - dx]
            b = lab[dy:, dx:]
            sel = (a == i) & (b != i)
            for j in b[sel]:
                nb[int(j)] = nb.get(int(j), 0) + 1
            sel = (b == i) & (a != i)
            for j in a[sel]:
                nb[int(j)] = nb.get(int(j), 0) + 1
        nbs = sorted(nb.items(), key=lambda t: -t[1])[:8]
        s = seg.get(i, {})
        print(f"{i}: {s.get('klasse')} sicher={s.get('sicher')} kern={int(mk.sum())} ges={int(m.sum())} "
              f"bbox x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()} grau={v.mean():.0f}±{v.std():.0f} "
              f"nb={','.join(f'{j % 100000}:{n}' for j, n in nbs)}")


def crop(x0, y0, w, h, f, out, roh=False, kontrast=False):
    lab, img, seg = lade()
    sub = img[y0:y0 + h, x0:x0 + w]
    if kontrast:
        lo, hi = np.percentile(sub, 2), np.percentile(sub, 98)
        sub = np.clip((sub - lo) / max(hi - lo, 1) * 255, 0, 255)
    rgb = np.stack([sub] * 3, -1).astype(np.uint8)
    big = np.array(Image.fromarray(rgb).resize((w * f, h * f), Image.NEAREST))
    if not roh:
        L = lab[y0:y0 + h, x0:x0 + w]
        Lb = np.kron(L, np.ones((f, f), dtype=L.dtype))
        edge = np.zeros(Lb.shape, bool)
        edge[:, 1:] |= Lb[:, 1:] != Lb[:, :-1]
        edge[1:, :] |= Lb[1:, :] != Lb[:-1, :]
        big[edge] = (255, 230, 0)
    im = Image.fromarray(big)
    d = ImageDraw.Draw(im)
    try:
        font = ImageFont.truetype("arial.ttf", 14)
    except OSError:
        font = ImageFont.load_default()
    # Kern- und Viertelgrenzen
    for g in (K0, 314, K1):
        if x0 <= g < x0 + w:
            d.line([((g - x0) * f, 0), ((g - x0) * f, h * f)], fill=(0, 255, 255), width=1)
        if y0 <= g < y0 + h:
            d.line([(0, (g - y0) * f), (w * f, (g - y0) * f)], fill=(0, 255, 255), width=1)
    if not roh:
        L = lab[y0:y0 + h, x0:x0 + w]
        for i in np.unique(L):
            ys, xs = np.nonzero(L == i)
            cy, cx = ys.mean(), xs.mean()
            k = np.argmin((ys - cy) ** 2 + (xs - cx) ** 2)
            t = str(int(i) % 100000)
            px, py = xs[k] * f, ys[k] * f
            d.text((px - 8, py - 7), t, fill=(0, 0, 0), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
            d.text((px - 8, py - 7), t, fill=(255, 255, 255), font=font)
    # Achsenbeschriftung alle 10 px
    for xx in range((x0 // 10 + 1) * 10, x0 + w, 10):
        d.text(((xx - x0) * f + 1, 1), str(xx), fill=(255, 80, 80), font=font)
        d.line([((xx - x0) * f, 0), ((xx - x0) * f, 5)], fill=(255, 80, 80))
    for yy in range((y0 // 10 + 1) * 10, y0 + h, 10):
        d.text((1, (yy - y0) * f + 1), str(yy), fill=(255, 80, 80), font=font)
        d.line([(0, (yy - y0) * f), (5, (yy - y0) * f)], fill=(255, 80, 80))
    im.save(out, quality=90)
    print(out, im.size)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser()
    p.add_argument("cmd")
    p.add_argument("--ids")
    p.add_argument("--fenster")
    p.add_argument("--f", type=int, default=6)
    p.add_argument("--out")
    p.add_argument("--roh", action="store_true")
    p.add_argument("--kontrast", action="store_true")
    a = p.parse_args()
    if a.cmd == "stats":
        stats([int(x) for x in a.ids.split(",")])
    else:
        x0, y0, w, h = map(int, a.fenster.split(","))
        crop(x0, y0, w, h, a.f, a.out, a.roh, a.kontrast)
