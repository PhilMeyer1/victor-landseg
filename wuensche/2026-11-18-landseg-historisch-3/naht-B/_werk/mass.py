import json
import numpy as np, tifffile
from PIL import Image
H0 = "C:/Users/Phil/Developement/Victor/daten/landseg/H0"
B = H0 + "/b-kategorien-frei"
W = "C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/naht-B/_werk"
bild = np.asarray(Image.open(H0 + "/H0.png").convert("L")).astype(np.float32)
karte = tifffile.imread(B + "/zusammen/labels.tif")
nd = json.load(open(B + "/zusammen/naht.json", encoding="utf-8"))
seg = json.load(open(B + "/zusammen/segmente.json", encoding="utf-8"))
kl = {e["id"]: e.get("klasse") for e in seg["segmente"]}
R = 12
out = []
for n, v in enumerate(nd["verstoesse"], 1):
    a, b = v["ids"]
    senk = v["naht"] in ("r0c0|r0c1", "r1c0|r1c1")
    if senk:
        x = v["von"][0]; y0, y1 = v["von"][1], v["bis"][1] + 1
        gl = bild[y0:y1, x - 1]; gr = bild[y0:y1, x]
        win = (slice(max(y0 - R, 0), y1 + R), slice(x - R, x + R))
    else:
        y = v["von"][1]; x0, x1 = v["von"][0], v["bis"][0] + 1
        gl = bild[y - 1, x0:x1]; gr = bild[y, x0:x1]
        win = (slice(y - R, y + R), slice(max(x0 - R, 0), x1 + R))
    kw = karte[win]; bw = bild[win]
    ma = float(bw[kw == a].mean()); mb = float(bw[kw == b].mean())
    sa = float(bw[kw == a].std()); sb = float(bw[kw == b].std())
    gL, gR = float(gl.mean()), float(gr.mean())
    # Seite links passt zu a? rechts zu b?
    passt = (abs(gL - ma) < abs(gL - mb)) and (abs(gR - mb) < abs(gR - ma))
    out.append(dict(n=n, naht=v["naht"], ids=[a, b], kl=[kl.get(a), kl.get(b)], L=v["laenge"],
                    ma=round(ma), mb=round(mb), gL=round(gL), gR=round(gR), d=round(abs(ma - mb)),
                    passt=passt, k=v["kante_max"], von=v["von"], bis=v["bis"]))
json.dump(out, open(W + "/mass.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
for o in out:
    print(f"{o['n']:3d} {o['naht']} {o['ids']} {o['kl'][0]:>6}|{o['kl'][1]:<6} L{o['L']:<3} ma{o['ma']:4d} mb{o['mb']:4d} gL{o['gL']:4d} gR{o['gR']:4d} d{o['d']:4d} {'P' if o['passt'] else '-'} k{o['k']}")
