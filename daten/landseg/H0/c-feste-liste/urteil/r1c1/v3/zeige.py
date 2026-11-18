"""Nahansicht aus Teilkachelbild und Label-Karte (nur lesen).

Aufruf: python -B zeige.py <ziel.jpg> x0 y0 breite hoehe faktor [modus] [hervorheben-IDs,komma]
modus: nummern (Grenzen + Nummern + Gitter), roh (nur Gitter am Rand), kontrast (Kontrast gestreckt + Grenzen)
Koordinaten im Teilkachelbild. Gitterlinien alle 10 px, beschriftet alle 20 px.
"""
import sys
import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont

BILD = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r1c1.png"
LABELS = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r1c1/labels.tif"


def main(a):
    ziel = a[0]
    x0, y0, w, h, f = (int(v) for v in a[1:6])
    modus = a[6] if len(a) > 6 else "nummern"
    hervor = {int(v) for v in a[7].split(",")} if len(a) > 7 and a[7] else set()
    img = np.array(Image.open(BILD).convert("L")).astype(np.float32)
    L = tifffile.imread(LABELS)
    H, W = L.shape
    x1, y1 = min(W, x0 + w), min(H, y0 + h)
    x0, y0 = max(0, x0), max(0, y0)
    sub = img[y0:y1, x0:x1]
    lab = L[y0:y1, x0:x1]
    if modus == "kontrast":
        lo, hi = np.percentile(sub, 2), np.percentile(sub, 98)
        sub = np.clip((sub - lo) / max(1, hi - lo) * 255, 0, 255)
    rgb = np.stack([sub] * 3, -1).astype(np.uint8)
    big = np.kron(rgb, np.ones((f, f, 1), dtype=np.uint8))
    labb = np.kron(lab, np.ones((f, f), dtype=lab.dtype))
    pad_l, pad_t = 40, 16
    out = np.zeros((big.shape[0] + pad_t, big.shape[1] + pad_l, 3), np.uint8)
    out[pad_t:, pad_l:] = big
    if modus != "roh":
        grenze = np.zeros(labb.shape, bool)
        grenze[:, 1:] |= labb[:, 1:] != labb[:, :-1]
        grenze[1:, :] |= labb[1:, :] != labb[:-1, :]
        o = out[pad_t:, pad_l:]
        o[grenze] = (255, 230, 0)
        if hervor:
            m = np.isin(labb, list(hervor))
            o[m] = (o[m] * 0.7 + np.array([255, 0, 0]) * 0.3).astype(np.uint8)
    im = Image.fromarray(out)
    d = ImageDraw.Draw(im)
    try:
        font = ImageFont.truetype("arial.ttf", 13)
        fontk = ImageFont.truetype("arialbd.ttf", 14)
    except OSError:
        font = fontk = ImageFont.load_default()
    for gx in range((x0 // 10 + 1) * 10, x1, 10):
        px = pad_l + (gx - x0) * f
        col = (0, 200, 255) if gx % 20 == 0 else (0, 110, 150)
        if modus == "roh":
            d.line([(px, pad_t), (px, pad_t + 6)], fill=col)
        else:
            for yy in range(pad_t, out.shape[0], 4):
                d.point((px, yy), fill=col)
        if gx % 20 == 0:
            d.text((px - 10, 1), str(gx), fill=(0, 220, 255), font=font)
    for gy in range((y0 // 10 + 1) * 10, y1, 10):
        py = pad_t + (gy - y0) * f
        col = (0, 200, 255) if gy % 20 == 0 else (0, 110, 150)
        if modus == "roh":
            d.line([(pad_l, py), (pad_l + 6, py)], fill=col)
        else:
            for xx in range(pad_l, out.shape[1], 4):
                d.point((xx, py), fill=col)
        if gy % 20 == 0:
            d.text((2, py - 7), str(gy), fill=(0, 220, 255), font=font)
    if modus != "roh":
        ids, inv = np.unique(lab, return_inverse=True)
        inv = inv.reshape(lab.shape)
        for k, sid in enumerate(ids):
            ys, xs = np.nonzero(inv == k)
            if len(xs) < 4:
                continue
            # Punkt im Segment nahe Schwerpunkt
            cx, cy = xs.mean(), ys.mean()
            j = np.argmin((xs - cx) ** 2 + (ys - cy) ** 2)
            tx, ty = pad_l + xs[j] * f + f // 2, pad_t + ys[j] * f + f // 2
            t = str(int(sid) % 100000)
            d.text((tx - 8, ty - 7), t, fill=(0, 0, 0), font=fontk)
            d.text((tx - 9, ty - 8), t, fill=(255, 255, 255), font=fontk)
    if max(im.size) > 2000:
        s = 2000 / max(im.size)
        im = im.resize((int(im.size[0] * s), int(im.size[1] * s)), Image.LANCZOS)
    im.save(ziel, quality=90)
    print(ziel, im.size)


if __name__ == "__main__":
    main(sys.argv[1:])
