"""Eigene Ansichten (Nachholer urt-c-r0c0-v1): aktuelle Karte, Fenster, Grenzen und Nummern."""
import json
import sys
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont

H0 = Path("C:/Users/Phil/Developement/Victor/daten/landseg/H0")
LAB = H0 / "c-feste-liste/r0c0/labels.tif"
BILD = H0 / "teilkacheln/r0c0.png"


def main():
    x0, y0, w, h, f = (int(v) for v in sys.argv[1:6])
    out = sys.argv[6]
    modus = sys.argv[7] if len(sys.argv) > 7 else "nummern"
    lab = tifffile.imread(str(LAB)).astype(np.int64)
    img = np.array(Image.open(BILD).convert("L")).astype(np.float64)
    sub = img[y0:y0 + h, x0:x0 + w]
    if "kontrast" in modus:
        lo, hi = np.percentile(sub, 2), np.percentile(sub, 98)
        sub = np.clip((sub - lo) / max(hi - lo, 1) * 255, 0, 255)
    rgb = np.stack([sub] * 3, -1).astype(np.uint8)
    big = np.array(Image.fromarray(rgb).resize((w * f, h * f), Image.BICUBIC))
    L = lab[y0:y0 + h, x0:x0 + w]
    if "roh" not in modus:
        Lb = np.kron(L, np.ones((f, f), dtype=L.dtype))
        edge = np.zeros(Lb.shape, bool)
        edge[:, 1:] |= Lb[:, 1:] != Lb[:, :-1]
        edge[1:, :] |= Lb[1:, :] != Lb[:-1, :]
        big[edge] = (255, 230, 0)
    im = Image.fromarray(big)
    d = ImageDraw.Draw(im)
    try:
        font = ImageFont.truetype("arial.ttf", 13)
    except OSError:
        font = ImageFont.load_default()
    for g in (64, 314, 564):
        if x0 <= g < x0 + w:
            d.line([((g - x0) * f, 0), ((g - x0) * f, h * f)], fill=(0, 255, 255), width=1)
        if y0 <= g < y0 + h:
            d.line([(0, (g - y0) * f), (w * f, (g - y0) * f)], fill=(0, 255, 255), width=1)
    if "roh" not in modus:
        for i in np.unique(L):
            m = L == i
            if m.sum() < 6:
                continue
            ys, xs = np.nonzero(m)
            # Punkt im Segment nahe Schwerpunkt
            cy, cx = ys.mean(), xs.mean()
            k = np.argmin((ys - cy) ** 2 + (xs - cx) ** 2)
            tx, ty = xs[k] * f, ys[k] * f
            t = str(int(i) % 1000)
            d.text((tx - 8, ty - 7), t, fill=(0, 0, 0), font=font, stroke_width=2, stroke_fill=(255, 255, 255))
    # Koordinatenmarken alle 25 px
    for g in range(0, 700, 25):
        if x0 <= g < x0 + w:
            d.text(((g - x0) * f + 1, 1), str(g), fill=(0, 255, 0), font=font)
        if y0 <= g < y0 + h:
            d.text((1, (g - y0) * f + 1), str(g), fill=(0, 255, 0), font=font)
    im.save(out, quality=90)


main()
