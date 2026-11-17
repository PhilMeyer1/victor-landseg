"""Eigene Nahansicht: links roh, rechts mit Grenzen und IDs; Ausschnitt im Teilkachelbild.

Aufruf: PY nah.py --x X --y Y --b B --h H --faktor F --aus <datei.jpg> [--kontrast]
"""
import argparse
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

BASIS = Path("C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500")
TK = "r1c0"


def main():
    p = argparse.ArgumentParser()
    for k in ("x", "y", "b", "h", "faktor"):
        p.add_argument("--" + k, type=int, required=True)
    p.add_argument("--aus", required=True)
    p.add_argument("--kontrast", action="store_true")
    a = p.parse_args()
    bild = np.asarray(Image.open(BASIS / "teilkacheln" / f"{TK}.png").convert("RGB")).astype(np.float32)
    lab = tifffile.imread(BASIS / "vorstufe" / TK / "labels.tif")
    sl = (slice(a.y, a.y + a.h), slice(a.x, a.x + a.b))
    b = bild[sl]
    if a.kontrast:
        lo, hi = np.percentile(b, 2), np.percentile(b, 98)
        b = np.clip((b - lo) / max(hi - lo, 1) * 255, 0, 255)
    b = b.astype(np.uint8)
    l = lab[sl]
    f = a.faktor
    big = np.repeat(np.repeat(b, f, 0), f, 1)
    g = np.zeros(l.shape, bool)
    g[:, 1:] |= l[:, 1:] != l[:, :-1]
    g[1:, :] |= l[1:, :] != l[:-1, :]
    gb = np.repeat(np.repeat(g, f, 0), f, 1)
    rechts = big.copy()
    rechts[gb] = (255, 255, 0)
    w = big.shape[1]
    out = Image.new("RGB", (2 * w + 10, big.shape[0] + 30), (255, 255, 255))
    out.paste(Image.fromarray(big), (0, 0))
    out.paste(Image.fromarray(rechts), (w + 10, 0))
    d = ImageDraw.Draw(out)
    font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 15)
    for sid in np.unique(l):
        m = l == sid
        if m.sum() < 8:
            continue
        dist = ndimage.distance_transform_edt(np.pad(m, 1))[1:-1, 1:-1]
        yy, xx = np.unravel_index(np.argmax(dist), dist.shape)
        x, y = w + 10 + xx * f + f // 2, yy * f + f // 2
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                d.text((x + dx, y + dy), str(int(sid)), font=font, fill=(0, 0, 0), anchor="mm")
        d.text((x, y), str(int(sid)), font=font, fill=(255, 255, 255), anchor="mm")
    d.text((6, big.shape[0] + 6),
           f"Ausschnitt x {a.x}–{a.x + a.b - 1}, y {a.y}–{a.y + a.h - 1} der Teilkachel {TK}, {f}fach; links roh, rechts Grenzen mit ID"
           + (" (Kontrast verstärkt)" if a.kontrast else ""), font=font, fill=(0, 0, 0))
    out.save(a.aus, quality=90)
    print("ok", a.aus)


if __name__ == "__main__":
    main()
