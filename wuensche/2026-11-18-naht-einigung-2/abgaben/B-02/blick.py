"""Eigene Kontrollbilder fuer Buendel B-02 (nur lesen, Bilder in diesen Ordner)."""
import sys
import numpy as np
import tifffile
from PIL import Image, ImageDraw

T0 = "C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/"
B = T0 + "b-kategorien-frei/"
OUT = "C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-naht-einigung-2/abgaben/B-02/"

img = np.array(Image.open(T0 + "T0.png").convert("RGB"))
H, W = img.shape[:2]
lab = np.zeros((H, W), dtype=np.int64)
for tid, (kx, ky) in {"r0c0": (0, 0), "r0c1": (500, 0), "r1c0": (0, 500), "r1c1": (500, 500)}.items():
    L = tifffile.imread(B + tid + "/labels.tif")
    lab[ky:ky + 500, kx:kx + 500] = L[64:564, 64:564]


def bild(name, x0, x1, y0, y1, ids, faktor):
    crop = img[y0:y1, x0:x1].astype(float)
    lc = lab[y0:y1, x0:x1]
    farben = [(0, 220, 220), (230, 0, 230), (255, 160, 0), (60, 220, 60), (80, 120, 255)]
    over = crop.copy()
    for i, sid in enumerate(ids):
        m = lc == sid
        over[m] = 0.55 * over[m] + 0.45 * np.array(farben[i % len(farben)])
    links = Image.fromarray(crop.astype(np.uint8)).resize(((x1 - x0) * faktor, (y1 - y0) * faktor), Image.NEAREST)
    rechts = Image.fromarray(over.astype(np.uint8)).resize(((x1 - x0) * faktor, (y1 - y0) * faktor), Image.NEAREST)
    # Segmentgrenzen weiss
    r = np.array(rechts)
    lb = np.kron(lc, np.ones((faktor, faktor), dtype=np.int64))
    kante = np.zeros(lb.shape, bool)
    kante[:, 1:] |= lb[:, 1:] != lb[:, :-1]
    kante[1:, :] |= lb[1:, :] != lb[:-1, :]
    r[kante] = (255, 255, 255)
    rechts = Image.fromarray(r)
    w, h = links.size
    ges = Image.new("RGB", (2 * w + 10, h + 30), (20, 20, 25))
    ges.paste(links, (0, 30))
    ges.paste(rechts, (w + 10, 30))
    d = ImageDraw.Draw(ges)
    d.text((5, 8), f"{name}: x {x0}-{x1}, y {y0}-{y1}, {faktor}-fach; Farben: " + ", ".join(str(i) for i in ids), fill=(255, 255, 0))
    if x0 < 500 < x1:
        nx = (500 - x0) * faktor
        d.line([(w + 10 + nx, 30), (w + 10 + nx, 30 + h)], fill=(255, 255, 0), width=1)
    ges.save(OUT + name + ".jpg", quality=90)
    print(name, ges.size)


if __name__ == "__main__":
    bild("einigung_02", 440, 600, 0, 140, [100061, 200043, 100074, 100040, 200058], 6)
    bild("einigung_06", 470, 560, 70, 140, [100099, 200100, 100059, 200099, 200080], 10)
    bild("einigung_10", 440, 600, 100, 290, [100122, 200116, 100109, 200145, 100114], 5)
