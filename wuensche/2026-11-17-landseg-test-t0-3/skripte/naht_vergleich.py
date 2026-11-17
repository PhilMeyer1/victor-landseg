import sys, json
sys.path.insert(0, "C:/Users/Phil/Developement/Victor/landseg")
import numpy as np, tifffile
from PIL import Image
from landseg import naht, dateien
from landseg.seite import kern_ausschneiden
T = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/"
m = dateien.lese_json(T + "kern500/manifest.json")
bild = np.asarray(Image.open(T + "kern500/T0.png").convert("RGB"))
def gesamt(ordner):
    g = np.zeros((1000, 1000), np.uint32)
    for t in m["teilkacheln"]:
        k = t["kern"]; g[k["y"]:k["y"]+500, k["x"]:k["x"]+500] = kern_ausschneiden(tifffile.imread(f"{ordner}/{t['id']}/labels.tif"), t)
    return g
for name, g in [("A", gesamt(T + "kern500/urteil-stand")), ("C", gesamt(T + "fassung-c/stand")), ("C-zusammen", tifffile.imread(T + "fassung-c/zusammen/labels.tif"))]:
    for e in (None, {}):
        b = naht.pruefe_naehte(g, m, bild, e).als_dict()
        print(name, e, len(b["verstoesse"]), "ids", len(np.unique(g)))
for name, g in [("A", gesamt(T + "kern500/urteil-stand")), ("C", tifffile.imread(T + "fassung-c/zusammen/labels.tif"))]:
    b = naht.pruefe_naehte(g, m, bild, None)
    d = b.als_dict()
    print(name, [k for k in d], json.dumps(d["verstoesse"][:2], ensure_ascii=False)[:400])
    print("  ", {k: (len(v) if isinstance(v, list) else v) for k, v in d.items()})
