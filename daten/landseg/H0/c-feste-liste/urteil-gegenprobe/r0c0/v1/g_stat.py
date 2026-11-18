"""Kennzahlen je eigenem Segment (Kernfläche, Anteil im Viertel, Grauwert)."""
import json
import sys

import numpy as np
from PIL import Image

BASIS = "C:/Users/Phil/Developement/Victor/daten/landseg/H0"
KARTE = BASIS + "/c-feste-liste/gegenprobe/r0c0/labels.tif"
BILD = BASIS + "/teilkacheln/r0c0.png"
SEG = BASIS + "/c-feste-liste/gegenprobe/r0c0/segmente.json"

try:
    import tifffile
    lab = tifffile.imread(KARTE).astype(np.int64)
except ImportError:
    lab = np.array(Image.open(KARTE)).astype(np.int64)
g = np.array(Image.open(BILD).convert("L")).astype(float)
segs = {s["id"]: s for s in json.load(open(SEG, encoding="utf-8"))["segmente"]}
kern = np.zeros(lab.shape, bool)
kern[64:564, 64:564] = True
v1 = np.zeros(lab.shape, bool)
v1[64:314, 64:314] = True
ids = json.loads(sys.argv[1])
for i in ids:
    m = lab == i
    mk = m & kern
    a = int(mk.sum())
    av = int((m & v1).sum())
    ys, xs = np.nonzero(m)
    s = segs.get(i, {})
    print(i, s.get("klasse"), s.get("sicher"), "kern", a, "v1", av,
          "anteil %.0f%%" % (100 * av / max(a, 1)),
          "grau %.0f±%.0f" % (g[m].mean(), g[m].std()) if a else "",
          "bbox x%d-%d y%d-%d" % (xs.min(), xs.max(), ys.min(), ys.max()) if len(xs) else "WEG")
