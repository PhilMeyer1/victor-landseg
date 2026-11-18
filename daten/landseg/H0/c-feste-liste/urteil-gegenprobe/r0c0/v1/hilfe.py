"""Hilfsskript der Gegenprobe r0c0: Kennzahlen je Segment und eigene Nahansichten.

stats <id,id,...>                      Fläche (Kern), Rahmen, Grauwert, Streuung, Länge/Breite
crop <x> <y> <w> <h> <faktor> <ziel> [ids] [roh]  Ausschnitt mit Grenzen (gelb) und Nummern; ids rot hervorgehoben
"""
import json
import sys
from pathlib import Path

import cv2
import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont

BASIS = Path("C:/Users/Phil/Developement/Victor/daten/landseg/H0")
LABELS = BASIS / "c-feste-liste/gegenprobe/r0c0/labels.tif"
SEGJ = BASIS / "c-feste-liste/gegenprobe/r0c0/segmente.json"
BILD = BASIS / "teilkacheln/r0c0.png"
K0, K1 = 64, 564


def lade():
    lab = tifffile.imread(LABELS)
    img = np.array(Image.open(BILD).convert("L"))
    seg = {s["id"]: s for s in json.loads(SEGJ.read_text(encoding="utf-8"))["segmente"]}
    return lab, img, seg


def stats(ids):
    lab, img, seg = lade()
    kern = np.zeros_like(lab, bool)
    kern[K0:K1, K0:K1] = True
    for i in ids:
        m = lab == i
        mk = m & kern
        if not m.any():
            print(i, "nicht auf Karte")
            continue
        ys, xs = np.nonzero(mk if mk.any() else m)
        pts = np.stack([xs, ys], 1).astype(float)
        c = pts - pts.mean(0)
        if len(pts) > 2:
            ev, evec = np.linalg.eigh(np.cov(c.T))
            proj = c @ evec
            ext = proj.max(0) - proj.min(0) + 1
            breite, laenge = sorted(ext)
            ang = np.degrees(np.arctan2(evec[1, 1], evec[0, 1]))
        else:
            breite = laenge = 1
            ang = 0
        g = img[m]
        n, _ = cv2.connectedComponents(m.astype(np.uint8), connectivity=4)
        s = seg.get(i, {})
        # Nachbarn
        dil = cv2.dilate(m.astype(np.uint8), np.ones((3, 3), np.uint8)).astype(bool) & ~m
        nb, cnt = np.unique(lab[dil], return_counts=True)
        nbs = ",".join(f"{a % 100000}:{b}" for a, b in sorted(zip(nb, cnt), key=lambda t: -t[1])[:6])
        print(f"{i} k={s.get('klasse')} kern={mk.sum()} ges={m.sum()} bbox=x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()} "
              f"grau={g.mean():.0f}±{g.std():.0f} L={laenge:.0f} B={breite:.0f} w={ang:.0f} teile={n-1} nb={nbs}")


def crop(x, y, w, h, f, ziel, ids=(), roh=False):
    lab, img, seg = lade()
    H, W = lab.shape
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(W, x + w), min(H, y + h)
    sub = lab[y0:y1, x0:x1]
    im = img[y0:y1, x0:x1]
    big = cv2.resize(im, ((x1 - x0) * f, (y1 - y0) * f), interpolation=cv2.INTER_NEAREST)
    rgb = np.stack([big] * 3, -1).copy()
    if not roh:
        sb = cv2.resize(sub.astype(np.float32), ((x1 - x0) * f, (y1 - y0) * f), interpolation=cv2.INTER_NEAREST).astype(np.int64)
        rand = np.zeros(sb.shape, bool)
        rand[:, 1:] |= sb[:, 1:] != sb[:, :-1]
        rand[1:, :] |= sb[1:, :] != sb[:-1, :]
        rgb[rand] = (255, 230, 0)
        for i in ids:
            mi = sb == i
            e = mi & rand
            rgb[cv2.dilate(e.astype(np.uint8), np.ones((2, 2), np.uint8)).astype(bool)] = (255, 40, 40)
        # Kern
        pil = Image.fromarray(rgb)
        d = ImageDraw.Draw(pil)
        for kx in (K0, K1):
            if x0 <= kx <= x1:
                d.line([((kx - x0) * f, 0), ((kx - x0) * f, (y1 - y0) * f)], fill=(0, 255, 255), width=1)
        for ky in (K0, K1):
            if y0 <= ky <= y1:
                d.line([(0, (ky - y0) * f), ((x1 - x0) * f, (ky - y0) * f)], fill=(0, 255, 255), width=1)
        font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", max(12, 2 * f + 6))
        for i in np.unique(sub):
            m = (sub == i).astype(np.uint8)
            dt = cv2.distanceTransform(np.pad(m, 1), cv2.DIST_L2, 3)[1:-1, 1:-1]
            yy, xx = np.unravel_index(dt.argmax(), dt.shape)
            if dt.max() < 2:
                continue
            t = str(i % 100000)
            col = (255, 80, 80) if i in ids else (255, 255, 255)
            d.text((xx * f, yy * f), t, fill=col, font=font, anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0))
        rgb = np.array(pil)
    pil = Image.fromarray(rgb)
    pil.save(ziel, quality=90)
    print(ziel, pil.size)


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "stats":
        stats([int(t) for t in a[1].split(",")])
    elif a[0] == "crop":
        ids = [int(t) for t in a[7].split(",")] if len(a) > 7 and a[7] not in ("-", "roh") else []
        crop(int(a[1]), int(a[2]), int(a[3]), int(a[4]), int(a[5]), a[6], ids, roh="roh" in a[7:])
