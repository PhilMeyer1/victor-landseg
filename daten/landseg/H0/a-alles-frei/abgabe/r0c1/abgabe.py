"""Wendet korrekturen.json (verschmelzen, punkte) auf tmp/labels_roh.npy an und schreibt die Abgabe:
labels.tif, segmente.json, kategorien-teil.json, ergebnis.jpg."""
import json
import numpy as np
from scipy import ndimage as ndi
from PIL import Image, ImageDraw, ImageFont
import tifffile

BILD = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r0c1.png"
lab = np.load("tmp/labels_roh.npy").astype(np.int64)
seg = {int(k): v for k, v in json.load(open("tmp/seg_roh.json", encoding="utf-8")).items()}
KOR = json.load(open("korrekturen.json", encoding="utf-8"))
KAT = json.load(open("kategorien-teil.json", encoding="utf-8"))
codes = {c["code"]: c for c in KAT["classes"]}

# union-find für Verschmelzen
par = {i: i for i in seg}


def f(i):
    while par[i] != i:
        par[i] = par[par[i]]
        i = par[i]
    return i


for v in KOR.get("verschmelzen", []):
    pts = v["punkte"]
    ids = [int(lab[y, x]) for x, y in pts]
    r = f(ids[0])
    for j in ids[1:]:
        par[f(j)] = r
    if "klasse" in v:
        seg[r]["klasse"] = v["klasse"]
        seg[r]["sicher"] = v.get("sicher", False)
        seg[r]["grund"] = v.get("grund", "")
        seg[r]["name"] = v.get("name", "")
mp = np.zeros(lab.max() + 1, np.int64)
for i in seg:
    mp[i] = f(i)
lab = mp[lab]
for p in KOR.get("punkte", []):
    x, y = p["xy"]
    i = int(lab[y, x])
    s = seg[i]
    s["klasse"] = p["klasse"]
    s["sicher"] = p.get("sicher", False)
    s["grund"] = p.get("grund", s["grund"])
    if p.get("name"):
        s["name"] = p["name"]

# Zusammenhang prüfen (Verschmelzen nur Nachbarn)
ids = np.unique(lab)
for i in ids:
    n = ndi.label(lab == i)[1]
    if n != 1:
        raise SystemExit(f"Segment {i} nicht zusammenhängend ({n})")
# kompakt nummerieren, nach Lage (Zeilen dann Spalten des Schwerpunkts)
cent = ndi.center_of_mass(np.ones_like(lab), lab, ids)
order = sorted(range(len(ids)), key=lambda k: (int(cent[k][0] // 40), cent[k][1]))
neu = np.zeros(lab.max() + 1, np.uint32)
for n, k in enumerate(order, start=1):
    neu[ids[k]] = n
out = neu[lab].astype(np.uint32)
assert out.min() >= 1
tifffile.imwrite("labels.tif", out, compression="zlib", photometric="minisblack")

kern = np.zeros(out.shape, bool)
kern[64:564, 64:564] = True
NAMEN = {c: codes[c]["name"] for c in codes}
liste = []
for n, k in enumerate(order, start=1):
    s = seg[int(ids[k])]
    m = out == n
    kl = s["klasse"]
    if kl not in codes:
        raise SystemExit(f"Klasse {kl} fehlt in der Liste")
    grob = kl.split(".")[0]
    e = {"id": n, "klasse": kl, "grob": grob, "name": s.get("name") or NAMEN[kl],
         "im_kern": bool((m & kern).any()), "sicher": bool(s["sicher"]),
         "flaeche_px": int(m.sum()), "kern_px": int((m & kern).sum())}
    if not s["sicher"]:
        e["offen"] = s["grund"]
    else:
        e["grund"] = s["grund"]
    liste.append(e)
json.dump({"schema": "landseg-segmente/1", "teilkachel": "r0c1", "fassung": "A alles frei",
           "segmente": liste, "verlauf": [{"was": "eigene Segmentierung (bauen.py, abgabe.py)", "bearbeiter": "agent-a-r0c1"}]},
          open("segmente.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------- ergebnis.jpg ----------
a = np.array(Image.open(BILD)).astype(np.float32)
s = 2
rgb = np.stack([a] * 3, -1)
farbe = {c: np.array([int(codes[c]["color"][j:j + 2], 16) for j in (1, 3, 5)], np.float32) for c in codes}
klasse_von = {e["id"]: e["klasse"] for e in liste}
for e in liste:
    m = out == e["id"]
    rgb[m] = 0.55 * rgb[m] + 0.45 * farbe[e["klasse"]]
im = Image.fromarray(rgb.clip(0, 255).astype(np.uint8)).resize((628 * s, 628 * s), Image.NEAREST)
Lb = np.kron(out, np.ones((s, s), np.uint32))
edge = np.zeros(Lb.shape, bool)
edge[:, 1:] |= Lb[:, 1:] != Lb[:, :-1]
edge[1:, :] |= Lb[1:, :] != Lb[:-1, :]
arr = np.array(im)
arr[edge] = (255, 255, 255)
# unsichere Segmente: Rand gelb
uns = np.isin(Lb, [e["id"] for e in liste if not e["sicher"]])
arr[edge & uns] = (255, 230, 0)
im = Image.fromarray(arr)
d = ImageDraw.Draw(im)
d.rectangle([64 * s, 64 * s, 564 * s - 1, 564 * s - 1], outline=(0, 255, 255), width=3)
try:
    fo = ImageFont.truetype("arial.ttf", 17)
except Exception:
    fo = ImageFont.load_default()
used = sorted({e["klasse"] for e in liste}, key=lambda c: [int(x) for x in c.split(".")])
leg = Image.new("RGB", (640, 30 + 26 * (len(used) + 3)), (255, 255, 255))
dl = ImageDraw.Draw(leg)
dl.text((10, 6), "Legende r0c1 (Fassung A „Alles frei“)", fill=(0, 0, 0), font=fo)
for j, c in enumerate(used):
    y = 34 + 26 * j
    dl.rectangle([10, y, 34, y + 18], fill=tuple(int(v) for v in farbe[c]), outline=(0, 0, 0))
    dl.text((42, y), f"{c}  {codes[c]['name']}", fill=(0, 0, 0), font=fo)
y = 34 + 26 * len(used)
dl.text((10, y), "Türkis: Kern;  weiß: Grenze sicher;", fill=(0, 0, 0), font=fo)
dl.text((10, y + 24), "gelb: Grenze eines unsicheren Segments", fill=(0, 0, 0), font=fo)
W2 = 628 * s
full = Image.new("RGB", (W2 + leg.width, W2), (255, 255, 255))
full.paste(im, (0, 0))
full.paste(leg, (W2, 0))
# lange Seite <= 2000
if full.width > 2000:
    full = full.resize((2000, int(full.height * 2000 / full.width)), Image.LANCZOS)
full.save("ergebnis.jpg", quality=90)
from collections import Counter
print("segmente", len(liste), "im kern", sum(e["im_kern"] for e in liste), "unsicher", sum(not e["sicher"] for e in liste))
print("unsicher im kern", sum((not e["sicher"]) and e["im_kern"] for e in liste))
print(Counter(e["klasse"] for e in liste))
json.dump({"farben": {c: codes[c]["color"] for c in codes}, "seg": {str(e["id"]): e["klasse"] for e in liste}},
          open("tmp/f_final.json", "w"))
