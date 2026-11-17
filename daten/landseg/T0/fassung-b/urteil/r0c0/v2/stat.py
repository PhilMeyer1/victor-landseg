"""Kennzahlen je Segment der Liste (nur lesen)."""
import json
import sys
from pathlib import Path
import numpy as np
from PIL import Image

BASIS = Path("C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b")
bild = np.array(Image.open(BASIS / "teilkacheln/r0c0.png").convert("RGB")).astype(float)
lab = np.array(Image.open(BASIS / "vorstufe/r0c0/labels.tif")).astype(np.int64)
ids = [int(x) for x in sys.argv[1].split(",")]
for sid in ids:
    m = lab == sid
    ys, xs = np.nonzero(m)
    kern = m[64:564, 64:564].sum()
    rgb = bild[m].mean(0)
    sd = bild[m].std(0).mean()
    # Nachbarn
    nb = {}
    for dy, dx in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        sh = np.roll(np.roll(lab, dy, 0), dx, 1)
        b = m & (sh != sid)
        for v, c in zip(*np.unique(sh[b], return_counts=True)):
            nb[int(v)] = nb.get(int(v), 0) + int(c)
    nbs = sorted(nb.items(), key=lambda t: -t[1])[:6]
    print(f"{sid % 100000}: n={m.sum()} kern={kern} bbox=({xs.min()},{ys.min()})-({xs.max()},{ys.max()}) "
          f"rgb=({rgb[0]:.0f},{rgb[1]:.0f},{rgb[2]:.0f}) sd={sd:.0f} nb=" + ",".join(f"{k % 100000}:{v}" for k, v in nbs))
