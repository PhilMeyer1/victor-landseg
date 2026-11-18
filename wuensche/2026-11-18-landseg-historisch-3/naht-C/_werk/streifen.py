"""Streifenbilder entlang der Kerngrenzen von H0 (Fassung C) zum Ansehen der Nahtverstöße."""
import json
import sys
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont

H0 = Path("C:/Users/Phil/Developement/Victor/daten/landseg/H0")
ZU = H0 / "c-feste-liste" / sys.argv[1] if len(sys.argv) > 1 else H0 / "c-feste-liste" / "zusammen"
AUS = Path(__file__).parent / "streifen"
AUS.mkdir(exist_ok=True)

bild = np.asarray(Image.open(H0 / "H0.png").convert("L"), dtype=np.float32)
karte = tifffile.imread(ZU / "labels.tif")
seg = {e["id"]: e for e in json.load(open(ZU / "segmente.json", encoding="utf-8"))["segmente"]}
naht = json.load(open(ZU / "naht.json", encoding="utf-8"))
verst = naht["verstoesse"]
for n, v in enumerate(verst, 1):
    v["n"] = n
json.dump(verst, open(AUS / "verstoesse.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)

FONT = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 15)
S = 5          # Vergrößerung
QUER = 36      # Bildpunkte je Seite quer zur Grenze
LANG = 125     # Bildpunkte entlang je Bild


def kontrast(a):
    lo, hi = np.percentile(a, 1), np.percentile(a, 99)
    return np.clip((a - lo) / max(hi - lo, 1) * 255, 0, 255).astype(np.uint8)


def ränder(k):
    r = np.zeros(k.shape, bool)
    r[:, 1:] |= k[:, 1:] != k[:, :-1]
    r[1:, :] |= k[1:, :] != k[:-1, :]
    return r


GRENZEN = [("r0c0|r0c1", "senkrecht", 500, 0, 500), ("r0c0|r1c0", "waagrecht", 500, 0, 500),
           ("r0c1|r1c1", "senkrecht", 500, 500, 1000), ("r1c0|r1c1", "waagrecht", 500, 500, 1000)]
# Hinweis: r0c1|r1c1 ist waagrecht (y=500, x 500..1000), r1c0|r1c1 senkrecht (x=500, y 500..1000)
GRENZEN = [("r0c0|r0c1", "senkrecht", 500, 0, 500), ("r0c0|r1c0", "waagrecht", 500, 0, 500),
           ("r0c1|r1c1", "waagrecht", 500, 500, 1000), ("r1c0|r1c1", "senkrecht", 500, 500, 1000)]

for name, richtung, lage, von, bis in GRENZEN:
    for start in range(von, bis, LANG):
        ende = min(start + LANG, bis)
        if richtung == "senkrecht":
            y0, y1, x0, x1 = start, ende, lage - QUER, lage + QUER
        else:
            y0, y1, x0, x1 = lage - QUER, lage + QUER, start, ende
        y0c, x0c = max(y0, 0), max(x0, 0)
        y1c, x1c = min(y1, 1000), min(x1, 1000)
        roh = kontrast(bild[y0c:y1c, x0c:x1c])
        k = karte[y0c:y1c, x0c:x1c]
        h, w = roh.shape
        groß = np.kron(roh, np.ones((S, S), np.uint8))
        p1 = Image.fromarray(groß).convert("RGB")
        p2 = p1.copy()
        rgb = np.asarray(p2).copy()
        kg = np.kron(k, np.ones((S, S), k.dtype))
        rgb[ränder(kg)] = (255, 40, 40)
        p2 = Image.fromarray(rgb)
        d2 = ImageDraw.Draw(p2)
        # Kerngrenze
        if richtung == "senkrecht":
            gx = (lage - x0c) * S
            for yy in range(0, h * S, 8):
                d2.line([(gx, yy), (gx, yy + 4)], fill=(0, 220, 255), width=1)
        else:
            gy = (lage - y0c) * S
            for xx in range(0, w * S, 8):
                d2.line([(xx, gy), (xx + 4, gy)], fill=(0, 220, 255), width=1)
        legende = []
        for v in verst:
            if v["naht"] != name:
                continue
            ax = v["von"][1] if richtung == "senkrecht" else v["von"][0]
            bx = v["bis"][1] if richtung == "senkrecht" else v["bis"][0]
            if bx < start or ax >= ende:
                continue
            mitte = (ax + bx) / 2
            if richtung == "senkrecht":
                px, py = (lage - x0c) * S + 6, (mitte - y0c) * S - 8
                d2.line([(gx - 3, (ax - y0c) * S), (gx - 3, (bx - y0c + 1) * S)], fill=(255, 230, 0), width=3)
            else:
                px, py = (mitte - x0c) * S - 8, (lage - y0c) * S + 4
                d2.line([((ax - x0c) * S, gy - 3), ((bx - x0c + 1) * S, gy - 3)], fill=(255, 230, 0), width=3)
            d2.text((px, py), str(v["n"]), fill=(255, 255, 0), font=FONT, stroke_width=2, stroke_fill=(0, 0, 0))
            a, b = v["ids"]
            legende.append(f"{v['n']}: {a} ({seg[a]['klasse']}) | {b} ({seg[b]['klasse']}), "
                           f"{v['laenge']} px, Kante {v['kante_max']}")
        if richtung == "senkrecht":
            W, H = 2 * w * S + 20, h * S
            ges = Image.new("RGB", (W + 420, max(H, 20 * len(legende) + 40)), "white")
            ges.paste(p1, (0, 0)); ges.paste(p2, (w * S + 20, 0))
            tx, ty = W + 10, 10
        else:
            W, H = w * S, 2 * h * S + 20
            ges = Image.new("RGB", (W, H + 20 * len(legende) + 40), "white")
            ges.paste(p1, (0, 0)); ges.paste(p2, (0, h * S + 20))
            tx, ty = 10, H + 10
        d = ImageDraw.Draw(ges)
        d.text((tx, ty), f"Naht {name}, {richtung}, {start}..{ende - 1} (links/oben roh, rechts/unten Grenzen)",
               fill="black", font=FONT)
        for i, z in enumerate(legende):
            d.text((tx, ty + 20 * (i + 1)), z, fill="black", font=FONT)
        ges.save(AUS / f"{name.replace('|', '_')}_{start:03d}.jpg", quality=88)
print(len(verst))
