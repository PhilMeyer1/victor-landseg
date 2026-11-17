"""Erzeugt roh.jpg, umriss.jpg, maengel.jpg, vorschlag.jpg und Nahansichten für ein Viertel von r1c0.

Aufruf: PY bilder.py <konfig.json>
konfig: {"viertel": "v1", "ausgabe": "<ordner>", "punkte": [[nr, x, y, "text"], ...],
         "verschmelzen": {"<id>": <ziel-id>, ...}, "namen": {"<id>": "Name", ...},
         "nah": [[n, x0, y0, breite, hoehe, faktor], ...], "kontrast": [[n, x0, y0, b, h, f], ...]}
"""
import json
import sys
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont, ImageOps
from scipy import ndimage

B = Path("C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b")
VIERTEL = {"v1": (64, 64), "v2": (314, 64), "v3": (64, 314), "v4": (314, 314)}
FONT = "C:/Windows/Fonts/arial.ttf"
FONTB = "C:/Windows/Fonts/arialbd.ttf"

cfg = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
out = Path(cfg["ausgabe"])
lab0 = tifffile.imread(B / "vorstufe/r1c0/labels.tif").astype(np.int64)
img = Image.open(B / "teilkacheln/r1c0.png").convert("RGB")
H, W = lab0.shape
vx, vy = VIERTEL[cfg["viertel"]]
fx, fy, fw, fh, F = vx - 32, vy - 32, 314, 314, 3
seg = json.loads((B / "vorstufe/r1c0/segmente.json").read_text(encoding="utf-8"))["segmente"]
kern_ids = {s["id"] for s in seg if s.get("im_kern")}


def fenster(arr, x0, y0, w, h):
    return arr[max(y0, 0):min(y0 + h, H), max(x0, 0):min(x0 + w, W)]


def grenzen(lab):
    g = np.zeros(lab.shape, bool)
    g[:, 1:] |= lab[:, 1:] != lab[:, :-1]
    g[1:, :] |= lab[1:, :] != lab[:-1, :]
    return g


def basis(x0, y0, w, h, f, kontrast=False):
    x0c, y0c = max(x0, 0), max(y0, 0)
    w = min(x0 + w, W) - x0c
    h = min(y0 + h, H) - y0c
    im = img.crop((x0c, y0c, x0c + w, y0c + h))
    if kontrast:
        im = ImageOps.autocontrast(im, cutoff=1)
    return im.resize((w * f, h * f), Image.NEAREST), x0c, y0c, w, h


def zeichne_grenzen(im, lab, x0, y0, w, h, f, farbe=(255, 230, 0)):
    g = grenzen(lab[y0:y0 + h, x0:x0 + w])
    gg = np.kron(g, np.ones((f, f), bool))
    # nur eine dünne Linie: Rand der vergrößerten Grenzpixel
    a = np.asarray(im).copy()
    a[gg] = (0.35 * a[gg] + 0.65 * np.array(farbe)).astype(np.uint8)
    return Image.fromarray(a)


def rahmen(d, x0, y0, f):
    d.rectangle([(vx - x0) * f, (vy - y0) * f, (vx + 250 - x0) * f - 1, (vy + 250 - y0) * f - 1],
                outline=(0, 255, 255), width=3)
    kx0, ky0 = (64 - x0) * f, (64 - y0) * f
    d.rectangle([kx0, ky0, kx0 + 500 * f - 1, ky0 + 500 * f - 1], outline=(255, 255, 255), width=1)


def schrift(d, xy, text, size=18, farbe=(255, 255, 255), fett=True):
    fnt = ImageFont.truetype(FONTB if fett else FONT, size)
    x, y = xy
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            d.text((x + dx, y + dy), text, font=fnt, fill=(0, 0, 0), anchor="mm")
    d.text((x, y), text, font=fnt, fill=farbe, anchor="mm")


def innenpunkte(lab, x0, y0, w, h):
    sub = lab[y0:y0 + h, x0:x0 + w]
    pts = {}
    for i in np.unique(sub):
        m = sub == i
        dt = ndimage.distance_transform_edt(np.pad(m, 1))[1:-1, 1:-1]
        yy, xx = np.unravel_index(np.argmax(dt), dt.shape)
        pts[int(i)] = (xx, yy, dt[yy, xx], int(m.sum()))
    return pts


# roh
im, x0, y0, w, h = basis(fx, fy, fw, fh, F)
d = ImageDraw.Draw(im)
rahmen(d, x0, y0, F)
im.save(out / "roh.jpg", quality=90)

# umriss
im, x0, y0, w, h = basis(fx, fy, fw, fh, F)
im = zeichne_grenzen(im, lab0, x0, y0, w, h, F)
d = ImageDraw.Draw(im)
rahmen(d, x0, y0, F)
for i, (xx, yy, r, n) in innenpunkte(lab0, x0, y0, w, h).items():
    if r >= 2:
        schrift(d, (xx * F + F // 2, yy * F + F // 2), str(i % 100000), 16,
                (255, 255, 255) if i in kern_ids else (170, 170, 170))
im.save(out / "umriss.jpg", quality=90)

# maengel
im, x0, y0, w, h = basis(fx, fy, fw, fh, F)
im = zeichne_grenzen(im, lab0, x0, y0, w, h, F)
punkte = cfg.get("punkte", [])
fnt = ImageFont.truetype(FONT, 17)
zeilen = []
for nr, px, py, text in punkte:
    zeilen.append(f"{nr}: {text}")
leg_h = 30 + 24 * max(len(zeilen), 1)
canvas = Image.new("RGB", (im.width, im.height + leg_h), (255, 255, 255))
canvas.paste(im, (0, 0))
d = ImageDraw.Draw(canvas)
rahmen(d, x0, y0, F)
gesetzt = []
for nr, px, py, text in punkte:
    cx, cy = (px - x0) * F + F // 2, (py - y0) * F + F // 2
    for _ in range(8):
        if all(abs(cx - a) >= 27 or abs(cy - b) >= 27 for a, b in gesetzt):
            break
        cx += 27
    gesetzt.append((cx, cy))
    d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13], fill=(220, 0, 0), outline=(255, 255, 255), width=2)
    schrift(d, (cx, cy), str(nr), 15)
d.text((10, im.height + 6), "Mängel (Nummer im Bild):" if punkte else "keine Mängel",
       font=ImageFont.truetype(FONTB, 17), fill=(0, 0, 0))
for k, z in enumerate(zeilen):
    d.text((10, im.height + 30 + 24 * k), z, font=fnt, fill=(0, 0, 0))
canvas.save(out / "maengel.jpg", quality=90)

# vorschlag
lab = lab0.copy()
verschm = {int(k): int(v) for k, v in cfg.get("verschmelzen", {}).items()}
for k in list(verschm):
    z = verschm[k]
    while z in verschm:
        z = verschm[z]
    kernmaske = np.zeros(lab0.shape, bool)
    kernmaske[64:564, 64:564] = True
    lab[(lab0 == k) & kernmaske] = z  # nur im Kern (L2)
namen = {int(k): v for k, v in cfg.get("namen", {}).items()}
im, x0, y0, w, h = basis(fx, fy, fw, fh, F)
im = zeichne_grenzen(im, lab, x0, y0, w, h, F)
d = ImageDraw.Draw(im)
rahmen(d, x0, y0, F)
pts = innenpunkte(lab, x0, y0, w, h)
for i, name in namen.items():
    if i in pts:
        xx, yy, r, n = pts[i]
        schrift(d, (xx * F + F // 2, yy * F + F // 2 - 9), str(i % 100000), 15)
        schrift(d, (xx * F + F // 2, yy * F + F // 2 + 9), name, 14, (255, 255, 160), False)
for name, poly in cfg.get("skizzen", []):
    xy = [((x - x0) * F + F // 2, (y - y0) * F + F // 2) for x, y in poly]
    d.line(xy, fill=(255, 140, 0), width=3)
    mx = sum(a for a, b in xy) / len(xy)
    my = sum(b for a, b in xy) / len(xy)
    schrift(d, (mx, my), name, 14, (255, 190, 90), False)
if cfg.get("vermerk"):
    schrift(d, (im.width // 2, im.height - 20), cfg["vermerk"], 18)
im.save(out / "vorschlag.jpg", quality=90)

# eigene Nahansichten
for art in ("nah", "kontrast"):
    for n, ax, ay, aw, ah, af in cfg.get(art, []):
        im, x0, y0, w, h = basis(ax, ay, aw, ah, af, kontrast=(art == "kontrast"))
        if art == "nah":
            im = zeichne_grenzen(im, lab0, x0, y0, w, h, af)
        d = ImageDraw.Draw(im)
        for i, (xx, yy, r, cnt) in innenpunkte(lab0, x0, y0, w, h).items():
            if r >= 2 and art == "nah":
                schrift(d, (xx * af + af // 2, yy * af + af // 2), str(i % 100000), 15,
                        (255, 255, 255) if i in kern_ids else (170, 170, 170))
        d.rectangle([(vx - x0) * af, (vy - y0) * af, (vx + 250 - x0) * af - 1, (vy + 250 - y0) * af - 1],
                    outline=(0, 255, 255), width=2)
        schrift(d, (110, 14), f"x {x0}–{x0 + w - 1}, y {y0}–{y0 + h - 1}", 15)
        im.save(out / f"{art}_{n}.jpg", quality=90)
print("fertig", out)
