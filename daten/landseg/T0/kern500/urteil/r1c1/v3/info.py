import json, sys
import numpy as np
from PIL import Image
import tifffile
from scipy import ndimage

B = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/"
lab = tifffile.imread(B + "vorstufe/r1c1/labels.tif")
seg = {s["id"]: s for s in json.load(open(B + "vorstufe/r1c1/segmente.json", encoding="utf-8"))["segmente"]}
ids = [int(x) for x in sys.argv[1].split(",")]
for i in ids:
    m = lab == i
    ys, xs = np.nonzero(m)
    s = seg.get(i, {})
    comp, n = ndimage.label(m)
    sizes = sorted(np.bincount(comp.ravel())[1:].tolist(), reverse=True)
    # neighbours
    d = ndimage.binary_dilation(m) & ~m
    nb = np.unique(lab[d])
    nbs = ",".join(f"{v%100000}:{seg.get(int(v),{}).get('klasse','?')}" for v in nb)
    print(i % 100000, s.get("klasse"), s.get("instanz", {}).get("text"), s.get("herkunft"),
          s.get("sicherheit", {}).get("wert"), "fl", m.sum(), "bbox", xs.min(), ys.min(), xs.max(), ys.max(),
          "komp", sizes[:4], "nb", nbs)
