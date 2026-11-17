"""ergebnis.jpg: Klassenfarben halbdurchsichtig, Grenzen, Kern umrandet, Legende.

Aufruf: python bild.py [ziel.jpg] [faktor] [--nummern] [x0 y0 b h]
"""
import json
import sys
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

HIER = Path(__file__).resolve().parent
BILD = HIER.parent.parent / "teilkacheln" / "r1c1.png"


def hexrgb(h):
    return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    ziel = Path(args[0]) if args else HIER / "ergebnis.jpg"
    f = int(args[1]) if len(args) > 1 else 2
    fen = [int(v) for v in args[2:6]] if len(args) >= 6 else [0, 0, 628, 628]
    nummern = "--nummern" in sys.argv
    L = tifffile.imread(HIER / "labels.tif")
    seg = {s["id"]: s for s in json.load(open(HIER / "segmente.json", encoding="utf-8"))["segmente"]}
    kat = json.load(open(HIER / "kategorien-teil.json", encoding="utf-8"))["classes"]
    farbe = {c["code"]: hexrgb(c["color"]) for c in kat}
    name = {c["code"]: c["name"] for c in kat}
    im = np.asarray(Image.open(BILD).convert("RGB")).astype(float)
    x0, y0, b, h = fen
    L = L[y0:y0 + h, x0:x0 + b]
    im = im[y0:y0 + h, x0:x0 + b]
    farbkarte = np.zeros(im.shape)
    for sid in np.unique(L):
        farbkarte[L == sid] = farbe[seg[int(sid)]["klasse"]]
    mix = im * 0.5 + farbkarte * 0.5
    gr = np.zeros(L.shape, bool)
    gr[:, 1:] |= L[:, 1:] != L[:, :-1]
    gr[1:, :] |= L[1:, :] != L[:-1, :]
    big = Image.fromarray(mix.astype(np.uint8)).resize((b * f, h * f), Image.NEAREST)
    arr = np.asarray(big).copy()
    g = np.asarray(Image.fromarray(gr.astype(np.uint8) * 255).resize((b * f, h * f), Image.NEAREST)) > 0
    arr[g] = (255, 255, 255)
    # unsichere Segmente: Grenze gelb
    uns = np.zeros(L.shape, bool)
    for sid in np.unique(L):
        if not seg[int(sid)]["sicher"]:
            uns |= L == sid
    gu = np.asarray(Image.fromarray((gr & uns).astype(np.uint8) * 255).resize((b * f, h * f), Image.NEAREST)) > 0
    arr[gu] = (255, 230, 0)
    img = Image.fromarray(arr)
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 14)
        fk = ImageFont.truetype("arial.ttf", 11)
    except OSError:
        font = fk = ImageFont.load_default()
    kx0, ky0 = (64 - x0) * f, (64 - y0) * f
    d.rectangle([kx0, ky0, kx0 + 500 * f, ky0 + 500 * f], outline=(0, 255, 255), width=3)
    if nummern:
        for sid in np.unique(L):
            m = L == sid
            dt = ndimage.distance_transform_edt(m)
            yy, xx = np.unravel_index(np.argmax(dt), dt.shape)
            d.text((xx * f, yy * f), f"{int(sid) - 400000}:{seg[int(sid)]['klasse']}", fill=(255, 255, 255),
                   font=fk, anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0))
    # Legende rechts
    benutzt = sorted({s["klasse"] for s in seg.values()}, key=lambda c: [int(t) for t in c.split(".")])
    breite_leg = 330
    zeile = 19
    hoehe = max(img.height, 40 + zeile * len(benutzt))
    out = Image.new("RGB", (img.width + breite_leg, hoehe), (255, 255, 255))
    out.paste(img, (0, 0))
    d2 = ImageDraw.Draw(out)
    d2.text((img.width + 10, 8), "Fassung C, r1c1 (Kern cyan; gelb = unsicher)", fill=(0, 0, 0), font=fk)
    for k, c in enumerate(benutzt):
        y = 30 + k * zeile
        d2.rectangle([img.width + 10, y, img.width + 30, y + 14], fill=farbe[c], outline=(0, 0, 0))
        d2.text((img.width + 36, y), f"{c} {name[c]}", fill=(0, 0, 0), font=fk)
    out.save(ziel, quality=90)


if __name__ == "__main__":
    main()
