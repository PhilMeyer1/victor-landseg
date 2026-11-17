"""Render ergebnis.jpg (class colours + boundaries, kern frame, legend) and optional zoom with ids.
bild.py                -> ergebnis.jpg
bild.py x0 y0 x1 y1 f out.png  -> zoom with segment ids and class codes"""
import json
import sys
import numpy as np
import tifffile
from PIL import Image, ImageDraw

D = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c"
O = f"{D}/abgabe/r0c1"
img = np.asarray(Image.open(f"{D}/teilkacheln/r0c1.png").convert("RGB")).astype(float)
lab = tifffile.imread(f"{O}/labels.tif")
segs = {s["id"]: s for s in json.load(open(f"{O}/segmente.json", encoding="utf-8"))["segmente"]}
kat = json.load(open(f"{O}/kategorien-teil.json", encoding="utf-8"))["classes"]
col = {c["code"]: tuple(int(c["color"][i:i + 2], 16) for i in (1, 3, 5)) for c in kat}
lut = np.zeros((lab.max() + 1, 3))
for i, s in segs.items():
    lut[i] = col[s["klasse"]]
H, W = lab.shape

def edges(L):
    e = np.zeros(L.shape, bool)
    e[:, 1:] |= L[:, 1:] != L[:, :-1]
    e[1:, :] |= L[1:, :] != L[:-1, :]
    return e

if len(sys.argv) == 1:
    f = 2
    a = 0.45
    mix = img * (1 - a) + lut[lab] * a
    big = np.kron(mix, np.ones((f, f, 1)))
    Lb = np.kron(lab, np.ones((f, f), dtype=lab.dtype))
    big[edges(Lb)] = (255, 255, 0)
    im = Image.fromarray(big.clip(0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    d.rectangle([64 * f, 64 * f, 564 * f - 1, 564 * f - 1], outline=(0, 255, 255), width=3)
    used = sorted({s["klasse"] for s in segs.values()}, key=lambda c: [int(x) for x in c.split(".")])
    names = {c["code"]: c["name"] for c in kat}
    leg_w = 470
    canvas = Image.new("RGB", (im.width + leg_w, im.height), (255, 255, 255))
    canvas.paste(im, (0, 0))
    d2 = ImageDraw.Draw(canvas)
    from PIL import ImageFont
    try:
        fnt = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 13)
    except OSError:
        fnt = None
    y = 10
    d2.text((im.width + 10, y), "Fassung C r0c1 - Klassen (Kern cyan umrandet)", fill=(0, 0, 0), font=fnt)
    y += 22
    for c in used:
        n = sum(1 for s in segs.values() if s["klasse"] == c)
        nk = sum(1 for s in segs.values() if s["klasse"] == c and s["im_kern"])
        d2.rectangle([im.width + 10, y, im.width + 34, y + 16], fill=col[c], outline=(0, 0, 0))
        d2.text((im.width + 42, y + 1), f"{c}  {names[c]}  ({nk} im Kern / {n})", fill=(0, 0, 0), font=fnt)
        y += 22
    y += 10
    d2.text((im.width + 10, y), "gelb: Segmentgrenzen", fill=(0, 0, 0), font=fnt)
    canvas.save(f"{O}/ergebnis.jpg", quality=90)
    print("ergebnis.jpg", canvas.size)
else:
    x0, y0, x1, y1, f = map(int, sys.argv[1:6])
    out = sys.argv[6]
    sub = lab[y0:y1, x0:x1]
    a = 0.35
    mix = img[y0:y1, x0:x1] * (1 - a) + lut[sub] * a
    big = np.kron(mix, np.ones((f, f, 1)))
    Lb = np.kron(sub, np.ones((f, f), dtype=sub.dtype))
    big[edges(Lb)] = (255, 255, 0)
    im = Image.fromarray(big.clip(0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    for i in np.unique(sub):
        m = sub == i
        if m.sum() < 25:
            continue
        ys, xs = np.nonzero(m)
        kk = np.argmin((ys - ys.mean()) ** 2 + (xs - xs.mean()) ** 2)
        s = segs[int(i)]
        t = f"{i}:{s['klasse']}" + ("" if s["sicher"] else "?")
        d.text((xs[kk] * f - 10, ys[kk] * f - 5), t, fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0))
    for gx in range((x0 // 20 + 1) * 20, x1, 20):
        d.text(((gx - x0) * f + 1, 1), str(gx), fill=(0, 255, 255))
    for gy in range((y0 // 20 + 1) * 20, y1, 20):
        d.text((1, (gy - y0) * f + 1), str(gy), fill=(0, 255, 255))
    im.save(out)
    print(out, im.size)
