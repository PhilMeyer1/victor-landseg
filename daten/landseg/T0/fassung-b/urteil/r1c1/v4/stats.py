"""Kennzahlen je Segment: stats.py <id,id,...> (IDs voll oder Nummer)."""
import json
import sys

import numpy as np
import tifffile
from PIL import Image

B = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b"
lab = tifffile.imread(B + "/vorstufe/r1c1/labels.tif").astype(np.int64)
img = np.array(Image.open(B + "/teilkacheln/r1c1.png").convert("RGB")).astype(float)
seg = {s["id"]: s for s in json.load(open(B + "/vorstufe/r1c1/segmente.json", encoding="utf-8"))["segmente"]}
ids = [int(x) for x in sys.argv[1].split(",")]
ids = [i if i > 100000 else 400000 + i for i in ids]
for i in ids:
    m = lab == i
    if not m.any():
        print(i, "leer")
        continue
    ys, xs = np.nonzero(m)
    s = seg[i]
    rgb = img[m].mean(0)
    sd = img[m].std(0).mean()
    nb = {}
    for dy, dx in ((0, 1), (1, 0)):
        a = lab[: lab.shape[0] - dy, : lab.shape[1] - dx]
        b = lab[dy:, dx:]
        e = (a != b) & ((a == i) | (b == i))
        o = np.where(a[e] == i, b[e], a[e])
        for v, c in zip(*np.unique(o, return_counts=True)):
            nb[int(v)] = nb.get(int(v), 0) + int(c)
    nbs = sorted(nb.items(), key=lambda t: -t[1])[:6]
    inst = (s.get("instanz") or {}).get("text", "")
    from scipy import ndimage
    ncomp = ndimage.label(m)[1]
    print(f"{i % 100000:4d} {s['klasse']:6s} {inst[:12]:12s} n={m.sum():5d} k={ncomp} x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()} "
          f"rgb={tuple(rgb.round().astype(int))} sd={sd:.0f} nb=" + " ".join(f"{k % 100000}({seg[k]['klasse']}):{c}" for k, c in nbs))
