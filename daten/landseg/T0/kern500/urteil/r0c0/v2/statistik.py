"""Kennzahlen je Segment (nur lesen): Fläche, Rahmen, Farbe, Streuung, Teile, Nachbarn mit Grenzlänge.

Aufruf: PY statistik.py id1,id2,...   oder   PY statistik.py punkt x y
"""
import json
import sys
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image
from scipy import ndimage

DATEN = Path("C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500")
roh = np.array(Image.open(DATEN / "teilkacheln" / "r0c0.png").convert("RGB")).astype(float)
lab = tifffile.imread(str(DATEN / "vorstufe" / "r0c0" / "labels.tif")).astype(np.int64)
seg = {s["id"]: s for s in json.loads((DATEN / "vorstufe" / "r0c0" / "segmente.json").read_text(encoding="utf-8"))["segmente"]}

if sys.argv[1] == "punkt":
    pts = sys.argv[2:]
    for i in range(0, len(pts), 2):
        x, y = int(pts[i]), int(pts[i + 1])
        s = lab[y, x]
        print(f"{x}/{y}: {s} {seg.get(s, {}).get('klasse')}")
    sys.exit(0)

for sid in [int(v) for v in sys.argv[1].split(",")]:
    m = lab == sid
    if not m.any():
        print(sid, "nicht vorhanden")
        continue
    ys, xs = np.nonzero(m)
    farbe = roh[m].mean(0)
    streu = roh[m].std(0).mean()
    _, n = ndimage.label(m)
    rand = ndimage.binary_dilation(m) & ~m
    nb = {}
    for v in lab[rand]:
        nb[int(v)] = nb.get(int(v), 0) + 1
    nbs = ", ".join(f"{k % 100000}:{seg.get(k, {}).get('klasse')}({c})" for k, c in sorted(nb.items(), key=lambda t: -t[1])[:7])
    print(f"{sid % 100000} [{seg[sid].get('klasse')}] F={m.sum()} x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()} "
          f"RGB={farbe.round().astype(int).tolist()} s={streu:.1f} Teile={n} | {nbs}")
