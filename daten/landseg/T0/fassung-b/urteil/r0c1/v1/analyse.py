"""Kennzahlen je Kernsegment der Teilkachel r0c1 (nur lesen): Fläche, Rahmen, Schwerpunkt,
Zusammenhang, Farbmittel, Nachbarn mit Grenzlänge. Aufruf: PY analyse.py <ids,komma> """
import json
import sys
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image
from scipy import ndimage

B = Path("C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b")
lab = tifffile.imread(B / "vorstufe/r0c1/labels.tif").astype(np.int64)
img = np.asarray(Image.open(B / "teilkacheln/r0c1.png").convert("RGB")).astype(float)
seg = {s["id"]: s for s in json.loads((B / "vorstufe/r0c1/segmente.json").read_text(encoding="utf-8"))["segmente"]}
ids = [int(x) for x in sys.argv[1].split(",")]
kern = np.zeros(lab.shape, bool)
kern[64:564, 64:564] = True
# Nachbarschaft
h = np.stack([lab[:, :-1].ravel(), lab[:, 1:].ravel()], 1)
v = np.stack([lab[:-1, :].ravel(), lab[1:, :].ravel()], 1)
pairs = np.concatenate([h, v])
pairs = pairs[pairs[:, 0] != pairs[:, 1]]
from collections import Counter
cnt = Counter(map(tuple, np.sort(pairs, 1)))
for i in ids:
    m = lab == i
    mk = m & kern
    ys, xs = np.nonzero(m)
    n, ncomp = ndimage.label(m)[1], None
    comp = ndimage.label(m)[0]
    sizes = sorted(np.bincount(comp.ravel())[1:].tolist(), reverse=True)
    rgb = img[m].mean(0).round().astype(int).tolist()
    nb = sorted(((c, (a if b == i else b)) for (a, b), c in cnt.items() if i in (a, b)), reverse=True)
    nbs = ", ".join(f"{j % 100000}:{seg.get(j, {}).get('klasse', '?')}:{c}" for c, j in nb[:8])
    s = seg.get(i, {})
    print(f"{i % 100000} {s.get('klasse')} {s.get('instanz', {}).get('text') if s.get('instanz') else s.get('herkunft')} "
          f"A={m.sum()} kern={mk.sum()} bb=x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()} "
          f"c={int(xs.mean())}/{int(ys.mean())} teile={sizes[:4]} rgb={rgb} | {nbs}")
