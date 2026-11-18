"""Stand der Karte fuer die Nachhol-Gegenprobe v2: je ID Existenz, Kernflaeche, Anteil im Viertel, Klasse, Grauwert."""
import json
import numpy as np
import tifffile
from PIL import Image

B = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/"
lab = tifffile.imread(B + "c-feste-liste/gegenprobe/r0c0/labels.tif")
seg = json.load(open(B + "c-feste-liste/gegenprobe/r0c0/segmente.json", encoding="utf-8"))
img = np.asarray(Image.open(B + "teilkacheln/r0c0.png").convert("L")).astype(float)
segs = seg["segmente"] if isinstance(seg, dict) and "segmente" in seg else seg
byid = {s["id"]: s for s in segs}
liste = [100045,100041,100037,100028,100050,100012,100053,100054,100060,100049,100020,100046,100056,100042,100073,100089,100071,100082,100066,100062,100084,100086,100069,100087,100030,100079,100063,100032,100081,100070,100094,100100,100110,100109,100096,100095,100125,100083,100111,100107,100092,100112,100104,100137,100117,100126,100145,100141,100139,100130,100127,100128,100148,100156,100164,100151,100155,100150,100161,100166,100149,100158,100142,100167,100144,100169,100153]
neu = [100261,100262,100271,100275,100277,100279,100280,100281,100283,100285]
kern = np.zeros_like(lab, dtype=bool); kern[64:564, 64:564] = True
v = np.zeros_like(lab, dtype=bool); v[64:314, 314:564] = True
# alle IDs, deren groesster Kernanteil in v2 liegt
ids, cnt = np.unique(lab[kern], return_counts=True)
for i in liste + neu:
    m = lab == i
    s = byid.get(i)
    if not m.any():
        print(i, "WEG", s and s.get("klasse"))
        continue
    k = (m & kern).sum(); q = (m & v).sum()
    ys, xs = np.nonzero(m)
    print(i, s.get("klasse"), "sicher", s.get("sicher"), "kern", k, "v2", q, f"{q/max(k,1):.2f}",
          "bbox", xs.min(), ys.min(), xs.max(), ys.max(), "grau", round(img[m].mean()), "sd", round(img[m].std()),
          "herk", s.get("herkunft"))
print("--- weitere IDs mit Mehrheit in v2:")
quarters = [(64,64),(314,64),(64,314),(314,314)]
for i, c in zip(ids, cnt):
    if i in liste or i in neu:
        continue
    m = lab == i
    parts = [(m[y:y+250, x:x+250]).sum() for x, y in quarters]
    if int(np.argmax(parts)) == 1:
        print(i, byid[i].get("klasse"), parts, byid[i].get("herkunft"))
