"""Eigene Ansichten fuer die Einigung A-01 (nur lesen, Bilder nur in diesen Ordner)."""
import sys
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

T0 = "C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0"
OUT = "C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-naht-einigung-2/abgaben/A-01"


def lade_labels():
    import tifffile
    glob_lab = np.zeros((1000, 1000), dtype=np.int64)
    for r in (0, 1):
        for c in (0, 1):
            t = f"r{r}c{c}"
            lab = tifffile.imread(f"{T0}/a-alles-frei/{t}/labels.tif")
            kern = lab[64:564, 64:564]
            glob_lab[r * 500:(r + 1) * 500, c * 500:(c + 1) * 500] = kern
    return glob_lab


def main():
    # args: name x0 y0 x1 y1 faktor [ids,...]
    name, x0, y0, x1, y1, f = sys.argv[1], *map(int, sys.argv[2:7])
    ids = [int(s) for s in sys.argv[7].split(",")] if len(sys.argv) > 7 else []
    img = np.asarray(Image.open(f"{T0}/T0.png").convert("RGB"))
    lab = lade_labels()
    crop = img[y0:y1, x0:x1].copy()
    lc = lab[y0:y1, x0:x1]
    roh = Image.fromarray(crop).resize(((x1 - x0) * f, (y1 - y0) * f), Image.NEAREST)
    ov = crop.astype(float)
    farben = [(0, 220, 220), (230, 0, 230), (255, 160, 0), (60, 120, 255), (120, 255, 60)]
    for i, sid in enumerate(ids):
        m = lc == sid
        ov[m] = ov[m] * 0.45 + np.array(farben[i % len(farben)]) * 0.55
    ov = Image.fromarray(ov.astype(np.uint8)).resize(roh.size, Image.NEAREST)
    big = np.kron(lc, np.ones((f, f), dtype=np.int64))
    rand = np.zeros(big.shape, bool)
    rand[:-1, :] |= big[:-1, :] != big[1:, :]
    rand[:, :-1] |= big[:, :-1] != big[:, 1:]
    a = np.asarray(ov).copy()
    a[rand] = (255, 255, 255)
    ov = Image.fromarray(a)
    W = roh.width * 2 + 8
    H = roh.height + 24
    if W > 2000:
        raise SystemExit("zu breit")
    out = Image.new("RGB", (W, H), (20, 20, 25))
    out.paste(roh, (0, 24))
    out.paste(ov, (roh.width + 8, 24))
    d = ImageDraw.Draw(out)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 14)
    except Exception:
        font = ImageFont.load_default()
    txt = f"Ausschnitt x {x0}–{x1}, y {y0}–{y1}, {f}-fach; Farben: " + ", ".join(
        f"{n}={sid}" for n, sid in zip(["türkis", "magenta", "orange", "blau", "grün"], ids))
    d.text((4, 3), txt, fill=(255, 230, 120), font=font)
    out.save(f"{OUT}/{name}", quality=90)
    print(out.size)


if __name__ == "__main__":
    main()
