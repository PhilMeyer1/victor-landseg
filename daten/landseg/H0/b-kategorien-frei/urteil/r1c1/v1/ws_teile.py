"""Große Stücke per Wasserscheide (dunkle Linien als Grenzen) zerlegen und als polygon_zuweisen-Schritte ausgeben.

PY -B ws_teile.py --stapel basis.json --ids 1,2 --h 25 --min 500 --aus plan_ws.json [--klasse 1.1.1]
Prüft im Speicher, dass jedes Polygon genau seine Region trifft (sonst wird die Region ausgelassen).
"""
import argparse
import json
import sys

import cv2
import numpy as np
from PIL import Image
from scipy import ndimage
from skimage import filters, morphology, segmentation

sys.path.insert(0, "C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c1/v1")
import werkzeug as wz  # noqa: E402
from landseg.eingriff import polygon_maske  # noqa: E402


def zerlegen(maske, g, h, mindest):
    marker = morphology.h_maxima(np.where(maske, g, 0), h) & maske
    marker, _ = ndimage.label(marker)
    reg = segmentation.watershed(-g, marker, mask=maske)
    while True:
        groessen = np.bincount(reg.ravel())
        klein = [r for r in range(1, len(groessen)) if 0 < groessen[r] < mindest]
        if not klein:
            break
        r = min(klein, key=lambda r: groessen[r])
        m = reg == r
        rand = ndimage.binary_dilation(m) & ~m & maske
        nb = reg[rand]
        nb = nb[(nb != r) & (nb > 0)]
        if not len(nb):
            reg[m] = 0
            continue
        reg[m] = np.bincount(nb).argmax()
    return reg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stapel")
    ap.add_argument("--ids", required=True)
    ap.add_argument("--h", type=float, default=25)
    ap.add_argument("--min", type=int, default=500)
    ap.add_argument("--sigma", type=float, default=1.2)
    ap.add_argument("--klasse", default="1.1.1")
    ap.add_argument("--aus", required=True)
    ap.add_argument("--rand_behalten", action="store_true")
    a = ap.parse_args()
    karte, _ = wz.laden(a.stapel, leise=True)
    img = np.asarray(Image.open(wz.BILD).convert("L")).astype(np.float32)
    g = filters.gaussian(img, a.sigma, preserve_range=True)
    kern = np.zeros(karte.shape, bool)
    kern[64:564, 64:564] = True
    schritte = []
    for sid in [int(i) for i in a.ids.split(",")]:
        maske = (karte == sid) & kern
        reg = zerlegen(maske, g, a.h, a.min)
        ids = [r for r in np.unique(reg) if r > 0]
        groessen = {r: int((reg == r).sum()) for r in ids}
        print(sid, "Regionen", groessen)
        if len(ids) < 2:
            continue
        groesste = max(ids, key=lambda r: groessen[r])
        aussen = (karte == sid) & ~kern
        nahe = ndimage.binary_dilation(aussen) & kern
        randreg = {r for r in ids if (nahe & (reg == r)).any()} if a.rand_behalten else set()
        if randreg:
            print('  am Kernrand mit Kontext verbunden, behalten:', sorted(int(r) for r in randreg))
        for r in ids:
            if (not randreg and r == groesste) or r in randreg:
                continue
            m = (reg == r).astype(np.uint8)
            m = ndimage.binary_fill_holes(m).astype(np.uint8)
            kont, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            if not kont:
                continue
            k = max(kont, key=len)[:, 0, :]
            poly = k.tolist()
            pm = polygon_maske(karte.shape, poly)
            fremd = int((pm & ~(karte == sid)).sum())
            if fremd:
                print(f"  Region {r}: Polygon trifft {fremd} fremde Bildpunkte, ausgelassen")
                continue
            schritte.append({"art": "roh", "schritt": {"op": "polygon_zuweisen", "flaeche": poly, "klasse": a.klasse}})
    json.dump({"schritte": schritte}, open(a.aus, "w", encoding="utf-8"))
    print("Schritte:", len(schritte))


if __name__ == "__main__":
    main()
