"""Ergebnisbilder roh/umriss/maengel/vorschlag eines Viertels. Aufruf: ergebnis.py <spec.json>
spec: {"viertel": "v1", "ziel": "<ordner>", "vorschlag": {"id": "code"}, "maengel": [[nr, x, y, "text"]],
       "vorschlag_vermerk": "..."}"""
import sys, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import tifffile

B = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/"
spec = json.load(open(sys.argv[1], encoding="utf-8"))
lab = tifffile.imread(B + "c-feste-liste/r1c0/labels.tif").astype(np.int64)
img = np.array(Image.open(B + "teilkacheln/r1c0.png").convert("L")).astype(float)
segs = {s["id"]: s for s in json.load(open(B + "c-feste-liste/r1c0/segmente.json", encoding="utf-8"))["segmente"]}
kat = {k["code"]: k for k in json.load(open("C:/Users/Phil/Developement/Victor/landseg/kategorien.json", encoding="utf-8"))["classes"]}
Q = {"v1": (64, 64), "v2": (314, 64), "v3": (64, 314), "v4": (314, 314)}
qx, qy = Q[spec["viertel"]]
x0, y0, w, h, f = qx - 32, qy - 32, 314, 314, 3
L = lab[y0:y0 + h, x0:x0 + w]
I = img[y0:y0 + h, x0:x0 + w]
try:
    font = ImageFont.truetype("arial.ttf", 15)
    fontk = ImageFont.truetype("arial.ttf", 13)
except Exception:
    font = fontk = ImageFont.load_default()


def basis(rgb):
    return Image.fromarray(np.repeat(np.repeat(rgb, f, 0), f, 1).astype(np.uint8))


def rahmen(im):
    d = ImageDraw.Draw(im)
    d.rectangle([(qx - x0) * f, (qy - y0) * f, (qx + 250 - x0) * f - 1, (qy + 250 - y0) * f - 1], outline=(0, 255, 255), width=2)
    return d


def grenzen(im):
    Lb = np.repeat(np.repeat(L, f, 0), f, 1)
    e = np.zeros(Lb.shape, bool)
    e[:, 1:] |= Lb[:, 1:] != Lb[:, :-1]
    e[1:, :] |= Lb[1:, :] != Lb[:-1, :]
    a = np.array(im); a[e] = (255, 255, 0)
    return Image.fromarray(a)


def ankerpunkt(i):
    ys, xs = np.nonzero(L == i)
    cx, cy = np.median(xs), np.median(ys)
    j = np.argmin((xs - cx) ** 2 + (ys - cy) ** 2)
    return xs[j] * f, ys[j] * f, len(xs)


rgb = np.stack([I] * 3, -1)
roh = basis(rgb); rahmen(roh); roh.save(spec["ziel"] + "/roh.jpg", quality=90)

um = grenzen(basis(rgb)); d = rahmen(um)
for i in np.unique(L):
    px, py, n = ankerpunkt(i)
    if n < 15: continue
    d.text((px, py), str(i), fill=(255, 255, 255), font=fontk, stroke_width=2, stroke_fill=(0, 0, 0), anchor="mm")
um.save(spec["ziel"] + "/umriss.jpg", quality=90)

# Mängel
ma = grenzen(basis(rgb * 0.8)); d = rahmen(ma)
mlist = spec.get("maengel", [])
leg = 22 * max(1, len(mlist)) + 10
out = Image.new("RGB", (ma.size[0], ma.size[1] + leg), (0, 0, 0)); out.paste(ma, (0, 0)); d = ImageDraw.Draw(out)
if not mlist:
    d.text((8, ma.size[1] + 6), "keine Mängel", fill=(255, 255, 255), font=font)
for k, (nr, mx, my, text) in enumerate(mlist):
    px, py = (mx - x0) * f, (my - y0) * f
    d.ellipse([px - 11, py - 11, px + 11, py + 11], fill=(220, 30, 30), outline=(255, 255, 255), width=2)
    d.text((px, py), str(nr), fill=(255, 255, 255), font=fontk, anchor="mm")
    d.text((8, ma.size[1] + 6 + 22 * k), f"{nr}: {text}", fill=(255, 255, 255), font=font)
out.save(spec["ziel"] + "/maengel.jpg", quality=90)

# Vorschlag
vs = {int(k): v for k, v in spec.get("vorschlag", {}).items()}
col = np.zeros(L.shape + (3,))
codes = {}
for i in np.unique(L):
    c = vs.get(int(i)) or segs.get(int(i), {}).get("klasse", "0")
    codes[int(i)] = c
    hx = kat[c]["color"].lstrip("#")
    col[L == i] = [int(hx[k:k + 2], 16) for k in (0, 2, 4)]
mix = rgb * 0.55 + col * 0.45
vo = grenzen(basis(mix)); d = rahmen(vo)
for i in np.unique(L):
    px, py, n = ankerpunkt(i)
    if n < 15: continue
    d.text((px, py), codes[int(i)], fill=(255, 255, 255), font=fontk, stroke_width=2, stroke_fill=(0, 0, 0), anchor="mm")
verm = spec.get("vorschlag_vermerk", "")
out = Image.new("RGB", (vo.size[0], vo.size[1] + 30), (0, 0, 0)); out.paste(vo, (0, 0)); d = ImageDraw.Draw(out)
d.text((8, vo.size[1] + 6), verm, fill=(255, 255, 255), font=font)
out.save(spec["ziel"] + "/vorschlag.jpg", quality=90)
print("fertig", spec["ziel"])
