"""Teil eines Segments über Grauwert-Schwelle abtrennen (größte zusammenhängende Fläche, geglättet) als polygon_zuweisen.

PY -B schwelle_teil.py --stapel basis.json --id 400063 (--unter 90 | --ueber 200) [--sigma 1] [--oeffnen 1] --plan plan.json
Hängt den Schritt an plan.json an (legt die Datei an, wenn sie fehlt).
"""
import argparse
import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from scipy import ndimage
from skimage import filters

sys.path.insert(0, "C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c1/v1")
import werkzeug as wz  # noqa: E402
from landseg.eingriff import polygon_maske  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stapel")
    ap.add_argument("--id", type=int, required=True)
    ap.add_argument("--unter", type=float)
    ap.add_argument("--ueber", type=float)
    ap.add_argument("--sigma", type=float, default=1.0)
    ap.add_argument("--oeffnen", type=int, default=1)
    ap.add_argument("--klasse", default="1.1.1")
    ap.add_argument("--plan", required=True)
    a = ap.parse_args()
    karte, _ = wz.laden(a.stapel, leise=True)
    img = np.asarray(Image.open(wz.BILD).convert("L")).astype(np.float32)
    g = filters.gaussian(img, a.sigma, preserve_range=True)
    seg = karte == a.id
    seg[:64] = seg[564:] = False
    seg[:, :64] = seg[:, 564:] = False
    m = seg & ((g < a.unter) if a.unter is not None else (g > a.ueber))
    if a.oeffnen:
        m = ndimage.binary_opening(m, iterations=a.oeffnen)
    m = ndimage.binary_fill_holes(m) & seg
    lab, n = ndimage.label(m)
    if n == 0:
        print("keine Fläche")
        return
    gr = np.bincount(lab.ravel())[1:]
    m = lab == (np.argmax(gr) + 1)
    kont, _ = cv2.findContours(m.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    poly = max(kont, key=len)[:, 0, :].tolist()
    pm = polygon_maske(karte.shape, poly)
    fremd = int((pm & ~seg).sum())
    print(f"Fläche {int(m.sum())} von {int(seg.sum())}, Polygon {int(pm.sum())}, fremd {fremd}")
    if fremd:
        print("fremde Bildpunkte - nicht angehängt")
        return
    p = Path(a.plan)
    plan = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"schritte": []}
    plan["schritte"].append({"art": "roh", "schritt": {"op": "polygon_zuweisen", "flaeche": poly, "klasse": a.klasse}})
    p.write_text(json.dumps(plan), encoding="utf-8")
    print("angehängt, Schritte:", len(plan["schritte"]))


if __name__ == "__main__":
    main()
