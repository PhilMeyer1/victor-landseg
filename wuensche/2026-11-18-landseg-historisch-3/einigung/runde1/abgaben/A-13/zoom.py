import json, sys
import numpy as np
from PIL import Image, ImageDraw
import tifffile

sys.stdout.reconfigure(encoding="utf-8")
D = "C:/Users/Phil/Developement/Victor/daten/landseg/H0"
A = "C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde1/auftraege-A/A-13"
OUT = "C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde1/abgaben/A-13"

img = np.array(Image.open(D + "/teilkacheln/r1c1.png").convert("L")).astype(float)
lab = tifffile.imread(D + "/a-alles-frei/r1c1/labels.tif")
print("img", img.shape, "lab", lab.shape)
off = 436
auftrag = json.load(open(A + "/auftrag.json", encoding="utf-8"))

nrs = [int(x) for x in sys.argv[1:]] or [p["nr"] for p in auftrag["paare"]]
for p in auftrag["paare"]:
    if p["nr"] not in nrs:
        continue
    ids = [s["id"] for s in p["segmente"]]
    s0 = p["strecken"][0]
    cx, cy = s0["von"][0] - off, s0["von"][1] - off
    half = 50
    x0, y0 = max(cx - half, 0), max(cy - half, 0)
    x1, y1 = min(cx + half, img.shape[1]), min(cy + half, img.shape[0])
    crop = img[y0:y1, x0:x1]
    lo, hi = np.percentile(crop, 1), np.percentile(crop, 99)
    c = np.clip((crop - lo) / (hi - lo) * 255, 0, 255).astype(np.uint8)
    L = lab[y0:y1, x0:x1]
    for i in ids:
        m = lab == i
        v = img[m]
        print(p["nr"], i, "n", m.sum(), "mean %.1f p10 %.1f p90 %.1f" % (v.mean(), np.percentile(v, 10), np.percentile(v, 90)))
    # print gray values near the contact point
    print("  Werte um Kontakt (Zeilen y, Spalten x %d..%d):" % (cx - 4, cx + 4))
    for yy in range(cy - 4, cy + 5):
        row = []
        for xx in range(cx - 4, cx + 5):
            l = lab[yy, xx]
            tag = "A" if l == ids[0] else ("B" if l == ids[1] else ".")
            row.append("%3d%s" % (img[yy, xx], tag))
        print("   ", yy + off, " ".join(row))
    k = 7
    big = Image.fromarray(c).resize((c.shape[1] * k, c.shape[0] * k), Image.NEAREST).convert("RGB")
    ov = np.array(big).copy()
    Lb = np.kron(L, np.ones((k, k), dtype=L.dtype))
    edge = np.zeros(Lb.shape, bool)
    edge[:, 1:] |= Lb[:, 1:] != Lb[:, :-1]
    edge[1:, :] |= Lb[1:, :] != Lb[:-1, :]
    ov2 = ov.copy()
    ov2[edge] = [255, 255, 255]
    for i, col in zip(ids, ([0, 220, 220], [230, 0, 230])):
        e = edge & (np.kron(L == i, np.ones((k, k), bool)))
        ov2[e] = col
    both = np.concatenate([ov, ov2], axis=1)
    im = Image.fromarray(both)
    d = ImageDraw.Draw(im)
    d.text((5, 5), "Paar %d, x %d-%d, y %d-%d, 7-fach, Kontrast gespreizt" % (p["nr"], x0 + off, x1 + off, y0 + off, y1 + off), fill=(255, 255, 0))
    im.save(OUT + "/einigung_%02d.jpg" % p["nr"], quality=90)
