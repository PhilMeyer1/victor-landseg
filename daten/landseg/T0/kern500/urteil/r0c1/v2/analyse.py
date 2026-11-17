"""Kennzahlen je Segment des Viertels v2 (nur lesen)."""
import json
import sys
import numpy as np
import tifffile
from PIL import Image
from scipy import ndimage

BASIS = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500"
lab = tifffile.imread(f"{BASIS}/vorstufe/r0c1/labels.tif").astype(np.int64)
man = json.load(open(f"{BASIS}/manifest.json", encoding="utf-8"))
tk = man["teilkacheln"]["r0c1"] if isinstance(man["teilkacheln"], dict) else [t for t in man["teilkacheln"] if t.get("name") == "r0c1" or t.get("id") == "r0c1"][0]
img = np.asarray(Image.open(f"{BASIS}/{tk['bild']}").convert("RGB")).astype(float)
seg = json.load(open(f"{BASIS}/vorstufe/r0c1/segmente.json", encoding="utf-8"))
segl = seg["segmente"] if isinstance(seg, dict) else seg
info = {s["id"]: s for s in segl}
ids = [int(x) for x in sys.argv[1].split(",")]
kern = np.zeros(lab.shape, bool)
kern[64:564, 64:564] = True
for i in ids:
    m = lab == i
    ys, xs = np.nonzero(m)
    nk, _ = ndimage.label(m)
    ncomp = nk.max() if hasattr(nk, "max") else 0
    _, ncomp = ndimage.label(m)
    col = img[m].mean(0)
    sd = img[m].std(0).mean()
    dil = ndimage.binary_dilation(m) & ~m
    nb = {}
    for j in lab[dil]:
        nb[int(j)] = nb.get(int(j), 0) + 1
    nbs = sorted(nb.items(), key=lambda t: -t[1])[:6]
    nbtxt = ", ".join(f"{j % 100000}:{info.get(j, {}).get('klasse', '?')}({c})" for j, c in nbs)
    print(f"{i % 100000} {info[i]['klasse']} n={m.sum()} kern={(m & kern).sum()} bbox x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()} "
          f"rgb={col.round().astype(int).tolist()} sd={sd:.0f} komp={ncomp} | {nbtxt}")
