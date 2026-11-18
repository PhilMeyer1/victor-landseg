"""Hilfswerkzeug des Urteils r0c0 (Fassung B): Segmentzahlen und eigene Nahansichten.

stats  --ids a,b,...                     Kernfläche, Rahmen, Grauwert, Nachbarn
render --x X --y Y --w W --h H --f F --out datei.jpg [--roh] [--kontrast]
"""
import argparse
import json
import sys

import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

BASIS = "C:/Users/Phil/Developement/Victor/daten/landseg/H0"
LABELS = BASIS + "/b-kategorien-frei/r0c0/labels.tif"
SEG = BASIS + "/b-kategorien-frei/r0c0/segmente.json"
BILD = BASIS + "/teilkacheln/r0c0.png"
K0, K1 = 64, 564
FARBE = False


def lade():
    lab = tifffile.imread(LABELS).astype(np.int64)
    img = np.asarray(Image.open(BILD).convert("L")).astype(np.float64)
    seg = {s["id"]: s for s in json.load(open(SEG, encoding="utf-8"))["segmente"]}
    return lab, img, seg


def stats(ids):
    lab, img, seg = lade()
    kern = np.zeros(lab.shape, bool)
    kern[K0:K1, K0:K1] = True
    for i in ids:
        m = lab == i
        mk = m & kern
        if not m.any():
            print(i, "fehlt")
            continue
        ys, xs = np.nonzero(mk if mk.any() else m)
        v = img[m]
        dil = ndimage.binary_dilation(m, np.ones((3, 3), bool)) & ~m
        nb, cnt = np.unique(lab[dil], return_counts=True)
        order = np.argsort(-cnt)
        nbs = []
        for j in order[:6]:
            n = int(nb[j])
            nbs.append(f"{n % 100000}:{cnt[j]}:{img[lab == n].mean():.0f}")
        lbl, nlab = ndimage.label(mk)
        s = seg.get(i, {})
        print(f"{i % 100000:>4} kern={int(mk.sum()):>5} ges={int(m.sum()):>5} teile={nlab} "
              f"x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()} "
              f"grau={v.mean():.0f}+-{v.std():.0f} kl={s.get('klasse')} nb={' '.join(nbs)}")


def render(x, y, w, h, f, out, roh=False, kontrast=False, hell=None):
    lab, img, seg = lade()
    sub = img[y:y + h, x:x + w]
    if kontrast:
        lo, hi = np.percentile(sub, 2), np.percentile(sub, 98)
        sub = np.clip((sub - lo) / max(hi - lo, 1) * 255, 0, 255)
    rgb = np.stack([sub] * 3, -1).astype(np.uint8)
    big = np.kron(rgb, np.ones((f, f, 1), np.uint8))
    L = lab[y:y + h, x:x + w]
    if FARBE and not roh:
        Lb0 = np.kron(L, np.ones((f, f), np.int64))
        rng = np.random.default_rng(7)
        pal = rng.integers(40, 255, size=(int(lab.max()) + 1, 3))
        big = (big * 0.55 + pal[Lb0] * 0.45).astype(np.uint8)
    if hell and not roh:
        Lb0 = np.kron(L, np.ones((f, f), np.int64))
        tint = np.isin(Lb0, hell)
        big[tint] = (big[tint] * 0.6 + np.array([255, 0, 0]) * 0.4).astype(np.uint8)
    if not roh:
        Lb = np.kron(L, np.ones((f, f), np.int64))
        rand = np.zeros(Lb.shape, bool)
        rand[:, 1:] |= Lb[:, 1:] != Lb[:, :-1]
        rand[1:, :] |= Lb[1:, :] != Lb[:-1, :]
        big[rand] = (255, 230, 0)
    # Kernrand cyan
    im = Image.fromarray(big)
    d = ImageDraw.Draw(im)
    for kx in (K0, K1, 314, 313 + 1):
        pass
    for v in (K0, 314, K1):
        if x <= v <= x + w:
            d.line([((v - x) * f, 0), ((v - x) * f, h * f)], fill=(0, 255, 255), width=1)
        if y <= v <= y + h:
            d.line([(0, (v - y) * f), (w * f, (v - y) * f)], fill=(0, 255, 255), width=1)
    if not roh:
        try:
            font = ImageFont.truetype("arial.ttf", max(10, f * 3))
        except OSError:
            font = ImageFont.load_default()
        for i in np.unique(L):
            m = L == i
            if m.sum() < 6:
                continue
            dt = ndimage.distance_transform_edt(np.pad(m, 1))[1:-1, 1:-1]
            yy, xx = np.unravel_index(np.argmax(dt), dt.shape)
            t = str(int(i) % 100000)
            col = (255, 80, 80) if hell and int(i) in hell else (255, 255, 255)
            d.text((xx * f, yy * f), t, fill=col, font=font, anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0))
    # Gitterbeschriftung
    try:
        sf = ImageFont.truetype("arial.ttf", 11)
    except OSError:
        sf = ImageFont.load_default()
    for gx in range((x // 10 + 1) * 10, x + w, 10):
        d.text(((gx - x) * f, 1), str(gx), fill=(0, 255, 0), font=sf, anchor="mt")
    for gy in range((y // 10 + 1) * 10, y + h, 10):
        d.text((1, (gy - y) * f), str(gy), fill=(0, 255, 0), font=sf, anchor="lm")
    im.save(out, quality=90)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("cmd")
    p.add_argument("--ids")
    p.add_argument("--x", type=int)
    p.add_argument("--y", type=int)
    p.add_argument("--w", type=int)
    p.add_argument("--h", type=int)
    p.add_argument("--f", type=int, default=6)
    p.add_argument("--out")
    p.add_argument("--roh", action="store_true")
    p.add_argument("--kontrast", action="store_true")
    p.add_argument("--farbe", action="store_true")
    a = p.parse_args()
    FARBE = a.farbe
    if a.cmd == "stats":
        stats([int(s) if int(s) > 99999 else 100000 + int(s) for s in a.ids.split(",")])
    else:
        hell = [int(s) if int(s) > 99999 else 100000 + int(s) for s in a.ids.split(",")] if a.ids else None
        render(a.x, a.y, a.w, a.h, a.f, a.out, a.roh, a.kontrast, hell)
