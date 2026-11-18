import json, sys
import numpy as np
from PIL import Image
import tifffile

B = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/"
lab = tifffile.imread(B + "c-feste-liste/urteil/r1c0/v1/probe/labels.tif").astype(np.int64)
img = np.array(Image.open(B + "teilkacheln/r1c0.png").convert("L")).astype(float)
seg = {s["id"]: s for s in json.load(open(B + "c-feste-liste/urteil/r1c0/v1/probe/segmente.json", encoding="utf-8"))["segmente"]}
ids = [int(a) for a in sys.argv[1].split(",")] if len(sys.argv) > 1 else sorted(np.unique(lab[64:564, 64:564]))
K = np.zeros_like(lab, bool); K[64:564, 64:564] = True
Q = {"v1": (64, 64), "v2": (314, 64), "v3": (64, 314), "v4": (314, 314)}
for i in ids:
    m = lab == i
    ys, xs = np.nonzero(m)
    if len(ys) == 0:
        print(i, "fehlt"); continue
    k = (m & K).sum()
    q = {n: int(m[y:y+250, x:x+250].sum()) for n, (x, y) in Q.items()}
    # neighbours
    nb = set()
    for dy, dx in ((0, 1), (1, 0)):
        a = lab[:lab.shape[0]-dy, :lab.shape[1]-dx]; b = lab[dy:, dx:]
        d = (a != b) & ((a == i) | (b == i))
        nb |= set(a[d].tolist()) | set(b[d].tolist())
    nb.discard(i)
    s = seg.get(i, {})
    print(i, s.get("klasse"), "ges", m.sum(), "kern", k, q, "bbox x", xs.min(), xs.max(), "y", ys.min(), ys.max(),
          "grau %.0f+-%.0f" % (img[m].mean(), img[m].std()), "nb", sorted(nb))
