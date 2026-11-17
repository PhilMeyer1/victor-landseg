"""Test: sub-split large mixed vorstufe segments with masked SLIC, write probe label map.
probe_split.py <px_per_piece> <ids comma> [compactness]"""
import sys
import numpy as np
import tifffile
from PIL import Image
from skimage.segmentation import slic
from skimage.measure import label as cc

D = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c"
O = f"{D}/abgabe/r0c1"
img = np.asarray(Image.open(f"{D}/teilkacheln/r0c1.png").convert("RGB"))
lab = tifffile.imread(f"{D}/vorstufe/r0c1/labels.tif").astype(np.int64)
per = float(sys.argv[1])
targets = [int(t) + 200000 for t in sys.argv[2].split(",")]
comp_ = float(sys.argv[3]) if len(sys.argv) > 3 else 10
out = lab.copy()
nxt = 300000
for t in targets:
    m = lab == t
    n = max(2, int(m.sum() / per))
    s = slic(img, n_segments=n, compactness=comp_, sigma=1, mask=m, start_label=1, channel_axis=-1)
    comp = cc(np.where(m, s, 0), connectivity=1, background=0)
    for k in np.unique(comp[comp > 0]):
        out[comp == k] = nxt
        nxt += 1
tifffile.imwrite(f"{O}/probe.tif", out.astype(np.uint32), compression="zlib")
print("pieces", nxt - 300000)
