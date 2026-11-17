"""Overview of the vorstufe segments of r0c1: id, class hint, area, centroid, bbox, mean colour."""
import json
import sys
import numpy as np
import tifffile
from PIL import Image

D = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c"
lab = tifffile.imread(f"{D}/vorstufe/r0c1/labels.tif")
img = np.asarray(Image.open(f"{D}/teilkacheln/r0c1.png").convert("RGB")).astype(float)
seg = {s["id"]: s for s in json.load(open(f"{D}/vorstufe/r0c1/segmente.json", encoding="utf-8"))["segmente"]}
print("shape", lab.shape, "n", len(np.unique(lab)), "zero", int((lab == 0).sum()))
ids = np.unique(lab)
kern = np.zeros(lab.shape, bool)
kern[64:564, 64:564] = True
for i in ids:
    m = lab == i
    ys, xs = np.nonzero(m)
    rgb = img[m].mean(0)
    s = seg.get(int(i), {})
    print(f"{int(i)-200000:4d} {s.get('klasse','?'):7s} {s.get('instanz',{}).get('text','') if s.get('instanz') else '':10s} "
          f"A={m.sum():6d} K={int((m&kern).sum()):6d} c=({xs.mean():.0f},{ys.mean():.0f}) "
          f"bb=({xs.min()},{ys.min()},{xs.max()},{ys.max()}) rgb=({rgb[0]:.0f},{rgb[1]:.0f},{rgb[2]:.0f}) sd={img[m].std(0).mean():.0f}")
