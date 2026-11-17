import json
import numpy as np
from PIL import Image
import tifffile

B = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500"
man = json.load(open(B + "/manifest.json", encoding="utf-8"))
tk = man["teilkacheln"]["r0c0"] if isinstance(man["teilkacheln"], dict) else [t for t in man["teilkacheln"] if t.get("id") == "r0c0" or t.get("name") == "r0c0"][0]
print({k: v for k, v in tk.items() if k != "segmente"})
bild = tk["bild"]
import os
if not os.path.isabs(bild):
    bild = os.path.join(B, bild)
img = np.asarray(Image.open(bild).convert("RGB")).astype(float)
lab = tifffile.imread(B + "/vorstufe/r0c0/labels.tif")
print("img", img.shape, "lab", lab.shape)
seg = json.load(open(B + "/vorstufe/r0c0/segmente.json", encoding="utf-8"))
segs = seg["segmente"] if isinstance(seg, dict) else seg
info = {s["id"]: s for s in segs}
ids = [100063,100046,100014,100065,100058,100047,100050,100057,100031,100033,100036,100053,100040,100092,100059,100087,100070,100093,100076,100071,100073,100089,100082,100091,100078,100077,100074,100061,100097,100098,100094,100101,100102,100111,100104,100105,100095,100107,100106,100100,100108,100096,100099,100109,100116,100117,100113,100115,100114,100121,100110,100124,100119,100120,100133,100131,100134,100132,100129,100127,100122,100139]
# neighbors via 4-connectivity
a = lab
pairs = set()
for d in [(a[:, 1:], a[:, :-1]), (a[1:, :], a[:-1, :])]:
    m = d[0] != d[1]
    for x, y in zip(d[0][m].ravel(), d[1][m].ravel()):
        pairs.add((int(x), int(y)))
nb = {}
for x, y in pairs:
    nb.setdefault(x, set()).add(y)
    nb.setdefault(y, set()).add(x)
for i in ids:
    m = lab == i
    ys, xs = np.nonzero(m)
    col = img[m].mean(0)
    sd = img[m].std(0).mean()
    s = info.get(i, {})
    nbs = sorted(nb.get(i, []))
    nbt = ",".join(f"{n % 100000}:{info.get(n, {}).get('klasse', '?')}" for n in nbs)
    print(f"{i%100000:>4} {s.get('klasse'):>6} n={m.sum():5d} bbox x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()} rgb={col.astype(int).tolist()} sd={sd:.0f} | {nbt}")
print(json.dumps(segs[0], ensure_ascii=False))
