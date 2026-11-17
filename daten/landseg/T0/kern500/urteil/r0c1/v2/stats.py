import json, sys
import numpy as np
import tifffile
from PIL import Image
from scipy import ndimage

B = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500"
lab = tifffile.imread(B + "/vorstufe/r0c1/labels.tif").astype(np.int64)
img = np.asarray(Image.open(B + "/teilkacheln/r0c1.png").convert("RGB")).astype(float)
seg = json.load(open(B + "/vorstufe/r0c1/segmente.json", encoding="utf-8"))
segs = seg["segmente"] if isinstance(seg, dict) and "segmente" in seg else seg
info = {s["id"]: s for s in segs}
ids = [int(x) for x in sys.argv[1].split(",")]
kern = np.zeros(lab.shape, bool); kern[64:564, 64:564] = True
st = ndimage.generate_binary_structure(2, 1)
for i in ids:
    m = lab == i
    mk = m & kern
    ys, xs = np.nonzero(m)
    n, k = ndimage.label(mk, st)
    sizes = sorted(np.bincount(n.ravel())[1:].tolist(), reverse=True)
    col = img[m].mean(0)
    sd = img[m].std(0).mean()
    dil = ndimage.binary_dilation(m, st)
    nb = np.bincount(lab[dil & ~m].ravel())
    nbs = [(int(j), int(c)) for j, c in enumerate(nb) if c > 0]
    nbs.sort(key=lambda t: -t[1])
    nbtxt = " ".join(f"{j%100000}:{c}:{info.get(j,{}).get('klasse','?')}" for j, c in nbs[:8])
    print(f"{i%100000} {info[i]['klasse']} total={m.sum()} kern={mk.sum()} bbox x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()} teile={sizes[:4]} rgb={col.round().astype(int).tolist()} sd={sd:.0f} | nb {nbtxt}")
