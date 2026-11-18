import json, sys
import numpy as np, tifffile
from PIL import Image, ImageDraw, ImageFont
H0 = "C:/Users/Phil/Developement/Victor/daten/landseg/H0"
B = H0 + "/b-kategorien-frei"
OUT = "C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/naht-B/_werk/blatt"
bild = np.asarray(Image.open(H0 + "/H0.png").convert("L")).astype(np.float32)
karte = tifffile.imread(B + "/zusammen/labels.tif")
nd = json.load(open(B + "/zusammen/naht.json", encoding="utf-8"))
seg = json.load(open(B + "/zusammen/segmente.json", encoding="utf-8"))
kl = {e["id"]: e.get("klasse") for e in seg["segmente"]}
V = nd["verstoesse"]
font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 14)
S = 4; Q = 40; L = 125
def strecke(img):
    lo, hi = np.percentile(img, 1), np.percentile(img, 99)
    return np.clip((img - lo) / max(hi - lo, 1) * 255, 0, 255).astype(np.uint8)
naehte = {"r0c0|r0c1": ("s", 500, 0), "r1c0|r1c1": ("s", 500, 500), "r0c0|r1c0": ("w", 500, 0), "r0c1|r1c1": ("w", 500, 500)}
txt = []
for naht, (r, lage, start) in naehte.items():
    for t in range(4):
        a0 = start + t * L; a1 = a0 + L
        if r == "s":
            ys, xs = slice(a0, a1), slice(lage - Q, lage + Q)
        else:
            ys, xs = slice(lage - Q, lage + Q), slice(a0, a1)
        g = strecke(bild[ys, xs]); k = karte[ys, xs]
        rgb = np.stack([g] * 3, -1)
        rgb = np.repeat(np.repeat(rgb, S, 0), S, 1)
        kk = np.repeat(np.repeat(k, S, 0), S, 1)
        rand = np.zeros(kk.shape, bool)
        rand[:, 1:] |= kk[:, 1:] != kk[:, :-1]; rand[1:, :] |= kk[1:, :] != kk[:-1, :]
        rgb[rand] = (255, 220, 0)
        im = Image.fromarray(rgb)
        pad = 170
        W, H = im.size
        can = Image.new("RGB", (W + pad, H + 20), (255, 255, 255)) if r == "s" else Image.new("RGB", (W + 20, H + pad), (255, 255, 255))
        can.paste(im, (0, 0))
        d = ImageDraw.Draw(can)
        # Kerngrenze
        if r == "s":
            x = Q * S
            for yy in range(0, H, 12): d.line([(x, yy), (x, yy + 5)], fill=(0, 200, 255), width=1)
        else:
            y = Q * S
            for xx in range(0, W, 12): d.line([(xx, y), (xx + 5, y)], fill=(0, 200, 255), width=1)
        for n, v in enumerate(V, 1):
            if v["naht"] != naht: continue
            if r == "s":
                p0, p1 = v["von"][1], v["bis"][1]
            else:
                p0, p1 = v["von"][0], v["bis"][0]
            if p1 < a0 or p0 >= a1: continue
            q0, q1 = max(p0, a0) - a0, min(p1, a1 - 1) - a0
            if r == "s":
                d.rectangle([W + 2, q0 * S, W + 8, q1 * S + S - 1], fill=(230, 0, 0))
                d.text((W + 12, q0 * S + (q1 - q0) * S / 2 - 7), f"{n}", fill=(200, 0, 0), font=font)
            else:
                d.rectangle([q0 * S, H + 2, q1 * S + S - 1, H + 8], fill=(230, 0, 0))
                d.text((q0 * S + (q1 - q0) * S / 2 - 6, H + 12 + (n % 4) * 15), f"{n}", fill=(200, 0, 0), font=font)
            txt.append(f"{n:3d} {naht} ids {v['ids']} kl {kl.get(v['ids'][0])} | {kl.get(v['ids'][1])} L{v['laenge']} {v['von']}-{v['bis']} k{v['kante_max']}")
        name = f"{OUT}/{naht.replace('|','_')}_{t}.jpg"
        can.save(name, quality=90)
open(OUT + "/liste.txt", "w", encoding="utf-8").write("\n".join(txt))
