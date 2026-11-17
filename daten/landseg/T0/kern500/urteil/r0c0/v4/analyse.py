"""Statistik je Segment des Viertels v4 (nur lesen)."""
import json
import sys
import numpy as np
from PIL import Image

B = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500"
try:
    import tifffile
    lab = tifffile.imread(B + "/vorstufe/r0c0/labels.tif")
except Exception:
    lab = np.array(Image.open(B + "/vorstufe/r0c0/labels.tif"))
img = np.array(Image.open(B + "/teilkacheln/r0c0.png").convert("RGB")).astype(float)
print("labels", lab.shape, lab.dtype, "bild", img.shape)
seg = {s["id"]: s for s in json.load(open(B + "/vorstufe/r0c0/segmente.json", encoding="utf-8"))["segmente"]}
ids = [int(x) for x in sys.argv[1].split(",")]
K0, K1 = 64, 564
for i in ids:
    m = lab == i
    ys, xs = np.nonzero(m)
    mk = m[K0:K1, K0:K1]
    col = img[m].mean(axis=0)
    # Nachbarn
    pad = np.zeros_like(m)
    pad[1:, :] |= m[:-1, :]; pad[:-1, :] |= m[1:, :]; pad[:, 1:] |= m[:, :-1]; pad[:, :-1] |= m[:, 1:]
    rand = pad & ~m
    nb, cnt = np.unique(lab[rand], return_counts=True)
    order = np.argsort(-cnt)
    nbs = ", ".join(f"{nb[k]%100000}:{seg.get(int(nb[k]),{}).get('klasse','?')}({cnt[k]})" for k in order[:6])
    s = seg.get(i, {})
    print(f"{i%100000:>4} {s.get('klasse'):>6} {s.get('herkunft','')[:12]:>12} {s.get('instanz',{}).get('text','')[:14]:>14} "
          f"A={m.sum():5d} kern={mk.sum():5d} bbox x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()} "
          f"rgb=({col[0]:.0f},{col[1]:.0f},{col[2]:.0f}) nb[{nbs}]")
