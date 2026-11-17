"""Hilfsauswertung je Segment eines Viertels (nur lesen): Fläche im Kern, Rahmen, Farbe, Nachbarn.
Aufruf: python stats.py <viertel> (v1..v4)
"""
import json
import sys
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image

K = Path("C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500")
sys.stdout.reconfigure(encoding="utf-8")
v = sys.argv[1]
lab = tifffile.imread(K / "vorstufe/r1c1/labels.tif").astype(np.int64)
img = np.asarray(Image.open(K / "teilkacheln/r1c1.png").convert("RGB")).astype(np.float32)
seg = {s["id"]: s for s in json.loads((K / "vorstufe/r1c1/segmente.json").read_text(encoding="utf-8"))["segmente"]}
vj = json.loads((K / f"viertel/r1c1/{v}/viertel.json").read_text(encoding="utf-8"))
liste = vj.get("segmente") or vj.get("liste")
kern = np.zeros(lab.shape, bool)
kern[64:564, 64:564] = True
# Nachbarschaft (4er) mit Kantenlänge
pairs = {}
for a, b in ((lab[:, :-1], lab[:, 1:]), (lab[:-1, :], lab[1:, :])):
    m = a != b
    for x, y in zip(a[m], b[m]):
        k = (min(x, y), max(x, y))
        pairs[k] = pairs.get(k, 0) + 1
nb = {}
for (x, y), n in pairs.items():
    nb.setdefault(x, []).append((y, n))
    nb.setdefault(y, []).append((x, n))
gray = img.mean(axis=2)
for e in liste:
    i = e["id"]
    m = lab == i
    mk = m & kern
    ys, xs = np.nonzero(mk)
    if len(xs) == 0:
        print(i, "leer im Kern")
        continue
    rgb = img[m].mean(axis=0)
    sd = gray[m].std()
    s = seg[i]
    nbs = sorted(nb.get(i, []), key=lambda t: -t[1])[:6]
    nbt = ", ".join(f"{j % 100000}:{seg[j]['klasse']}({n})" for j, n in nbs)
    print(f"{i % 100000:>3} {s['klasse']:<6} {s['sicher']:<4} {s.get('herkunft',''):<14} {s.get('instanz',{}).get('text','') if isinstance(s.get('instanz'),dict) else '':<12} "
          f"A={len(xs):>5} x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()} RGB={rgb[0]:.0f}/{rgb[1]:.0f}/{rgb[2]:.0f} sd={sd:.0f} | {nbt}")
