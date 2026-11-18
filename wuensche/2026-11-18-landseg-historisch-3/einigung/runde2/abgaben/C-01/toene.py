"""Grauton beider Segmente nahe der Beruehrstelle (nur Kernanteile, Band von 8 px)."""
import json
from pathlib import Path

import numpy as np
from PIL import Image

D = Path("C:/Users/Phil/Developement/Victor/daten/landseg/H0")
C = D / "c-feste-liste"
MAN = json.loads((D / "manifest.json").read_text(encoding="utf-8"))
KONTEXT = {t["id"]: t["kontext"] for t in MAN["teilkacheln"]}
KERN = {t["id"]: t["kern"] for t in MAN["teilkacheln"]}
A = json.loads(Path("C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde2/auftraege-C/C-01/auftrag.json").read_text(encoding="utf-8"))
img = np.array(Image.open(D / "H0.png").convert("L")).astype(float)


def labels(tk):
    import tifffile
    return tifffile.imread(C / tk / "labels.tif").astype(np.int64)


def global_maske(tk, sid, lab):
    m = np.zeros(img.shape, bool)
    k, kern = KONTEXT[tk], KERN[tk]
    sub = lab[kern["y"] - k["y"]: kern["y"] - k["y"] + kern["hoehe"], kern["x"] - k["x"]: kern["x"] - k["x"] + kern["breite"]]
    m[kern["y"]: kern["y"] + kern["hoehe"], kern["x"]: kern["x"] + kern["breite"]] = sub == sid
    return m


cache = {}
for p in A["paare"]:
    pts = []
    for s in p["strecken"]:
        (x0, y0), (x1, y1) = s["von"], s["bis"]
        pts += [(x0, y0), (x1, y1)]
    xs, ys = [q[0] for q in pts], [q[1] for q in pts]
    bx0, bx1, by0, by1 = min(xs) - 8, max(xs) + 9, min(ys) - 8, max(ys) + 9
    out = []
    for s in p["segmente"]:
        tk, sid = s["segment"].split(":")
        if tk not in cache:
            cache[tk] = labels(tk)
        m = global_maske(tk, int(sid), cache[tk])
        box = np.zeros_like(m)
        box[max(0, by0):by1, max(0, bx0):bx1] = True
        nah = m & box
        ganz = m
        out.append(f"{s['segment']} nah n={nah.sum()} mittel={img[nah].mean():.0f} sd={img[nah].std():.0f} | ganz n={ganz.sum()} mittel={img[ganz].mean():.0f} sd={img[ganz].std():.0f}")
    print(p["nr"], "; ".join(out))
