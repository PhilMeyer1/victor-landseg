"""Streifenbilder entlang jeder Naht: Bild kontrastverstärkt, Segmentgrenzen, Verstöße nummeriert."""
import json
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont

H0 = Path("C:/Users/Phil/Developement/Victor/daten/landseg/H0")
D = H0 / "a-alles-frei"
W = Path("C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/naht-A/_werk")
OUT = W / "streifen"
OUT.mkdir(exist_ok=True)
tab = json.load(open(W / "tabelle.json", encoding="utf-8"))
bild = np.asarray(Image.open(H0 / "H0.png").convert("L"), dtype=np.float32)
karte = tifffile.imread(D / "zusammen/labels.tif")
try:
    font = ImageFont.truetype("arial.ttf", 16)
except OSError:
    font = ImageFont.load_default()

S = 6
QUER = 30
STUECK = 100


def kontrast(a):
    lo, hi = np.percentile(a, [1, 99])
    return np.clip((a - lo) / max(hi - lo, 1) * 255, 0, 255).astype(np.uint8)


def grenzmaske(k):
    m = np.zeros(k.shape, bool)
    m[:, 1:] |= k[:, 1:] != k[:, :-1]
    m[1:, :] |= k[1:, :] != k[:-1, :]
    return m


naehte = {"r0c0|r0c1": ("s", 500, 0), "r1c0|r1c1": ("s", 500, 500),
          "r0c0|r1c0": ("w", 500, 0), "r0c1|r1c1": ("w", 500, 500)}
for name, (richtung, lage, start) in naehte.items():
    for s0 in range(start, start + 500, STUECK):
        if richtung == "s":
            y0, y1, x0, x1 = s0, s0 + STUECK, lage - QUER, lage + QUER
        else:
            y0, y1, x0, x1 = lage - QUER, lage + QUER, s0, s0 + STUECK
        ys0, ys1 = max(0, y0 - 0), min(1000, y1)
        g = kontrast(bild[y0:y1, x0:x1])
        rgb = np.stack([g] * 3, -1)
        rgb = np.kron(rgb, np.ones((S, S, 1), np.uint8))
        p1 = Image.fromarray(rgb)
        k = karte[y0:y1, x0:x1]
        # Grenzen auf Pixelkanten zeichnen
        p2 = p1.copy()
        dr = ImageDraw.Draw(p2)
        h, w = k.shape
        for yy in range(h):
            for xx in range(1, w):
                if k[yy, xx] != k[yy, xx - 1]:
                    dr.line([(xx * S, yy * S), (xx * S, (yy + 1) * S)], fill=(255, 40, 40), width=2)
        for yy in range(1, h):
            for xx in range(w):
                if k[yy, xx] != k[yy - 1, xx]:
                    dr.line([(xx * S, yy * S), ((xx + 1) * S, yy * S)], fill=(255, 40, 40), width=2)
        # Kerngrenze
        if richtung == "s":
            X = (lage - x0) * S
            for yy in range(0, h * S, 12):
                dr.line([(X, yy), (X, yy + 6)], fill=(255, 230, 0), width=1)
        else:
            Y = (lage - y0) * S
            for xx in range(0, w * S, 12):
                dr.line([(xx, Y), (xx + 6, Y)], fill=(255, 230, 0), width=1)
        # Verstöße
        hier = [z for z in tab if z["naht"] == name and
                (s0 <= (z["von"][1] if richtung == "s" else z["von"][0]) < s0 + STUECK)]
        for z in hier:
            if richtung == "s":
                a, b = z["von"][1] - y0, z["bis"][1] - y0 + 1
                dr.rectangle([(X - 4, a * S), (X + 4, b * S - 1)], outline=(0, 200, 255), width=2)
            else:
                a, b = z["von"][0] - x0, z["bis"][0] - x0 + 1
                dr.rectangle([(a * S, Y - 4), (b * S - 1, Y + 4)], outline=(0, 200, 255), width=2)
        if richtung == "s":
            ges = Image.new("RGB", (w * S * 2 + 20 + 120, h * S), (255, 255, 255))
            ges.paste(p1, (0, 0)); ges.paste(p2, (w * S + 20, 0))
            d = ImageDraw.Draw(ges)
            letzte = -99
            for z in hier:
                yy = max((z["von"][1] - y0) * S, letzte + 17)
                letzte = yy
                d.text((w * S * 2 + 26, yy), str(z["n"]), fill=(0, 0, 0), font=font)
                d.line([(w * S * 2 + 20, (z["von"][1] - y0) * S + 3), (w * S * 2 + 25, yy + 8)], fill=(0, 120, 200))
        else:
            ges = Image.new("RGB", (w * S, h * S * 2 + 20 + 60), (255, 255, 255))
            ges.paste(p1, (0, 0)); ges.paste(p2, (0, h * S + 20))
            d = ImageDraw.Draw(ges)
            letzte = -99
            reihe = 0
            for z in hier:
                xx = (z["von"][0] - x0) * S
                if xx < letzte + 30:
                    reihe = (reihe + 1) % 3
                else:
                    reihe = 0
                letzte = xx
                d.text((xx, h * S * 2 + 22 + reihe * 18), str(z["n"]), fill=(0, 0, 0), font=font)
        ges.save(OUT / f"{name.replace('|', '_')}_{s0:03d}.jpg", quality=88)
print("ok")
