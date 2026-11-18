import json, sys
import numpy as np
from PIL import Image
import tifffile

B = "C:/Users/Phil/Developement/Victor/daten/landseg/H0"
lab = tifffile.imread(B + "/c-feste-liste/r0c0/labels.tif").astype(np.int64)
img = np.array(Image.open(B + "/teilkacheln/r0c0.png").convert("L")).astype(float)
seg = json.load(open(B + "/c-feste-liste/r0c0/segmente.json", encoding="utf-8"))["segmente"]
by = {}
for s in seg:
    by.setdefault(s["id"], s)
liste = [100172,100180,100143,100178,100165,100185,100187,100183,100191,100189,100186,100194,100199,100193,100198,100196,100192,100176,100207,100201,100209,100216,100195,100210,100214,100211,100218,100215,100224,100220,100225,100219,100228,100229]
core = np.zeros_like(lab, bool); core[64:564, 64:564] = True
v4 = np.zeros_like(lab, bool); v4[314:564, 314:564] = True
ids_in_v4 = set(np.unique(lab[v4]).tolist())
for i in liste + sorted(ids_in_v4 - set(liste)):
    m = lab == i
    s = by.get(i)
    if not m.any():
        print(i, "NICHT AUF KARTE", "in json" if s else "")
        continue
    ys, xs = np.nonzero(m)
    mk = m & core
    print(i, "L" if i in liste else "x", s["klasse"] if s else "?", s.get("sicher") if s else "?",
          "kern", int(mk.sum()), "v4", int((m & v4).sum()), "ges", int(m.sum()),
          "bbox", xs.min(), ys.min(), xs.max(), ys.max(),
          "grau %.0f sd %.0f" % (img[m].mean(), img[m].std()))
