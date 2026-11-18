import json
import numpy as np
from PIL import Image
import tifffile

B = "C:/Users/Phil/Developement/Victor/daten/landseg/H0"
img = np.array(Image.open(f"{B}/H0.png").convert("L")).astype(float)
l0 = tifffile.imread(f"{B}/b-kategorien-frei/r0c0/labels.tif")
l1 = tifffile.imread(f"{B}/b-kategorien-frei/r0c1/labels.tif")
lab = np.zeros((1000, 1000), dtype=np.int64)
lab[0:500, 0:500] = l0[64:564, 64:564]
lab[0:500, 500:1000] = l1[64:564, 64:564]
for k in [100032, 100056, 100063, 100070, 100081, 100092, 100030, 200004, 200019, 200169, 200186, 200180, 200031, 200171, 200049]:
    v = img[lab == k]
    print(k, len(v), "<60", round((v < 60).mean(), 2), "60-110", round(((v >= 60) & (v < 110)).mean(), 2), ">=110", round((v >= 110).mean(), 2))
for tk in ("r0c0", "r0c1"):
    s = json.load(open(f"{B}/b-kategorien-frei/{tk}/segmente.json", encoding="utf-8"))
    segs = s["segmente"] if isinstance(s, dict) else s
    for e in segs:
        if e.get("id") in (100030, 100079, 100107, 200171, 200170, 200042, 200049, 200043):
            print(tk, e.get("id"), e.get("klasse"), e.get("sicher"))
