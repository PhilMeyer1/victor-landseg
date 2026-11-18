"""Baut die Label-Karte für r1c1 (Fassung A) aus Atomen (Felzenszwalb) plus Objektvorgaben.

Schritte:
 1. Atome (Felzenszwalb) als Grundlage, jedes Atom ein Segment.
 2. Felder: Atome mit Mehrheit in einem groben Polygon werden zu einem Feld zusammengelegt.
 3. Bildpunkt-Objekte (in Reihenfolge, später überschreibt früher): Polygon oder Korridor um eine
    Leitlinie, wahlweise nur Bildpunkte im Grauwertbereich (geglättet), wahlweise nur die
    Zusammenhangsstücke, die die Leitlinie berühren; Grenze also am Helligkeitsumschlag.
 4. Korrekturen (korrekturen.json): Polygone, Verschmelzen je Punktliste, Klasse je Punkt.
 5. Zusammenhang erzwingen, Kleinstücke mit dem Nachbarn der längsten Grenze verschmelzen.
 6. Segmente aus Atomresten: Klasse nach Grauregel aus ihren tatsächlichen Bildpunkten.
"""
import json
from collections import Counter
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image, ImageDraw
from scipy import ndimage
from skimage.segmentation import felzenszwalb

HIER = Path(__file__).resolve().parent
AB = HIER.parent
BILD = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r1c1.png"
VIER = ndimage.generate_binary_structure(2, 1)
K0, K1 = 64, 564  # Kern im Bild

img = np.array(Image.open(BILD).convert("L"))
H, W = img.shape
glatt = ndimage.gaussian_filter(img.astype(float), 1.5)
atome = felzenszwalb(img.astype(np.float32) / 255.0, scale=150, sigma=0.8, min_size=25) + 1

obj = json.loads((HIER / "objekte.json").read_text(encoding="utf-8"))
kor = json.loads((HIER / "korrekturen.json").read_text(encoding="utf-8"))


def linie_maske(punkte, breite=1):
    m = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(m)
    pts = [tuple(p[:2]) for p in punkte]
    d.line(pts, fill=1, width=breite)
    r = breite / 2
    for x, y in pts:
        d.ellipse([x - r, y - r, x + r, y + r], fill=1)
    return np.array(m, bool)


def korridor(punkte, hw):
    """Leitlinie mit Halbbreite; Punkte [x,y] oder [x,y,hw]."""
    m = np.zeros((H, W), bool)
    for a, b in zip(punkte[:-1], punkte[1:]):
        h = a[2] if len(a) > 2 else hw
        m |= linie_maske([a, b], int(2 * h))
    return m


def poly_maske(punkte):
    m = Image.new("L", (W, H), 0)
    ImageDraw.Draw(m).polygon([tuple(p) for p in punkte], fill=1, outline=1)
    return np.array(m, bool)


karte = atome.astype(np.int64).copy()
info = {}  # id -> dict ; Atome ohne Eintrag bekommen die Grauregel
nxt = int(karte.max()) + 1


def neues(maske, o):
    global nxt
    sid = nxt
    nxt += 1
    karte[maske] = sid
    info[sid] = {"klasse": o["klasse"], "name": o["name"], "sicher": o.get("sicher", True),
                 "grund": o.get("grund", ""), "quelle": o.get("quelle", "objekt")}
    return sid


# 1b. Schattenfugen: schmale dunkle Linien (Black-Hat) schneiden die Atome; eigene Segmente
from skimage.morphology import closing, disk
s08 = ndimage.gaussian_filter(img.astype(float), 0.8)
bh = closing(s08, disk(3)) - s08
fuge = (bh > obj.get("fuge_schwelle", 18)) & (s08 < 120)
lab, nf = ndimage.label(fuge, structure=VIER)
gf = np.bincount(lab.ravel())
gf[0] = 0
for t in np.nonzero(gf >= obj.get("fuge_min", 15))[0]:
    m = lab == t
    g = float(img[m].mean())
    neues(m, {"klasse": "5", "name": "Schattenfuge zwischen Gebäuden", "sicher": g < 80,
              "grund": "" if g < 80 else "schmale dunkle Linie, aber nicht schwarz: Schatten, Traufkante oder schmaler Gang",
              "quelle": "fuge"})

# 2. Felder aus Atomen
n_at = atome.max() + 1
fl = np.bincount(atome.ravel(), minlength=n_at)
for o in obj["objekte"]:
    if o.get("art") != "feld":
        continue
    m = np.zeros((H, W), bool)
    for p in o["polygone"]:
        m |= poly_maske(p)
    anteil = np.bincount(atome[m].ravel(), minlength=n_at) / np.maximum(fl, 1)
    sel = np.nonzero(anteil > o.get("anteil", 0.5))[0]
    neues(np.isin(atome, sel), o)

# 3. Bildpunkt-Objekte
for o in obj["objekte"]:
    if o.get("art") != "pixel":
        continue
    m = np.zeros((H, W), bool)
    for p in o.get("polygone", []):
        m |= poly_maske(p)
    for li in o.get("korridore", []):
        m |= korridor(li["linie"], li["hw"])
    if "grau_min" in o:
        m &= glatt >= o["grau_min"]
    if "grau_max" in o:
        m &= glatt <= o["grau_max"]
    if o.get("oeffnen"):
        m = ndimage.binary_opening(m, structure=VIER, iterations=o["oeffnen"])
    if o.get("an_linie"):
        lin = np.zeros((H, W), bool)
        for li in o["korridore"]:
            lin |= linie_maske(li["linie"], 3)
        lab, n = ndimage.label(m, structure=VIER)
        keep = np.unique(lab[lin & m])
        keep = keep[keep > 0]
        m = np.isin(lab, keep)
    if o.get("min_stueck"):
        lab, n = ndimage.label(m, structure=VIER)
        g = np.bincount(lab.ravel())
        g[0] = 0
        m = np.isin(lab, np.nonzero(g >= o["min_stueck"])[0])
    if o.get("loecher_fuellen"):
        gef = ndimage.binary_fill_holes(m)
        loch = gef & ~m
        lab, n = ndimage.label(loch, structure=VIER)
        g = np.bincount(lab.ravel())
        g[0] = 0
        m |= np.isin(lab, np.nonzero((g > 0) & (g <= o["loecher_fuellen"]))[0])
    if o.get("nur_frei"):
        frei = ~np.isin(karte, list(info.keys()))
        m &= frei
    if m.any():
        neues(m, o)
    else:
        print("WARNUNG: leer:", o["name"])

# 4. Korrekturen
for p in kor.get("polygone", []):
    m = poly_maske(p["flaeche"])
    if "nur_ids_bei" in p:  # nur Bildpunkte der Segmente an diesen Punkten
        ids = [int(karte[y, x]) for x, y in p["nur_ids_bei"]]
        m &= np.isin(karte, ids)
    neues(m, dict(p, quelle="korrektur"))
for li in kor.get("schnitte", []):
    m = linie_maske(li["linie"], li.get("breite", 2))
    objekt_ids = [k for k, v in info.items() if v["quelle"] not in ("fuge",)]
    m &= ~np.isin(karte, objekt_ids)
    if m.any():
        neues(m, {"klasse": "5", "name": "Schattenfuge (von Hand verlängert)", "sicher": False,
                  "grund": "Fuge im Bild nur schwach sichtbar, von Hand nachgezogen", "quelle": "fuge"})


def zusammenhang():
    global karte, nxt
    for idx, sl in enumerate(ndimage.find_objects(karte)):
        if sl is None:
            continue
        sid = idx + 1
        m = karte[sl] == sid
        lab, n = ndimage.label(m, structure=VIER)
        if n <= 1:
            continue
        g = np.bincount(lab.ravel())[1:]
        gross = int(np.argmax(g)) + 1
        sub = karte[sl]
        for t in range(1, n + 1):
            if t == gross:
                continue
            sub[lab == t] = nxt
            if sid in info:
                info[nxt] = dict(info[sid])
            nxt += 1


def verschmelze_punkte(punkte, o=None):
    ziel = int(karte[punkte[0][1], punkte[0][0]])
    for x, y in punkte[1:]:
        s = int(karte[y, x])
        if s != ziel:
            karte[karte == s] = ziel
            info.pop(s, None)
    if o and "klasse" in o:
        info[ziel] = {"klasse": o["klasse"], "name": o.get("name", ""), "sicher": o.get("sicher", True),
                      "grund": o.get("grund", ""), "quelle": "korrektur"}


zusammenhang()
for v in kor.get("verschmelzen", []):
    verschmelze_punkte(v["punkte"], v)

# 5. Kleinstücke
MIN = obj.get("mindestflaeche", 12)
for runde in range(6):
    ids, cnt = np.unique(karte, return_counts=True)
    klein = [int(i) for i, c in zip(ids, cnt) if c < MIN]
    if not klein:
        break
    for s in klein:
        m = karte == s
        if not m.any():
            continue
        rand = ndimage.binary_dilation(m, structure=VIER) & ~m
        w, c = np.unique(karte[rand], return_counts=True)
        if w.size:
            karte[m] = int(w[np.argmax(c)])
            info.pop(s, None)
zusammenhang()

# 6. Grauregel für Atomreste, dann Klassen je Punkt
for sid in np.unique(karte):
    sid = int(sid)
    if sid in info:
        continue
    g = img[karte == sid].mean()
    for r in obj["grauregel"]:
        if g < r["bis"]:
            info[sid] = {"klasse": r["klasse"], "name": r["name"], "sicher": r.get("sicher", False),
                         "grund": r.get("grund", ""), "quelle": "grauregel"}
            break
for c in kor.get("klassen", []):
    pts = c["punkte"] if "punkte" in c else [c["punkt"]]
    for x, y in pts:
        sid = int(karte[y, x])
        info[sid] = {"klasse": c["klasse"], "name": c.get("name", ""), "sicher": c.get("sicher", True),
                     "grund": c.get("grund", ""), "quelle": "korrektur"}

# fortlaufend nummerieren, Atomnummern stabil halten über Ordnung nach Lage
ids = np.unique(karte)
# Ordnung: nach Schwerpunkt (Zeile, Spalte) grob, damit Nummern lesbar sind
schw = ndimage.center_of_mass(np.ones_like(karte), karte, ids)
ordnung = sorted(range(len(ids)), key=lambda i: (int(schw[i][0] // 40), schw[i][1]))
lut = np.zeros(int(ids.max()) + 1, np.uint32)
umb = {}
for neu_i, i in enumerate(ordnung, start=1):
    lut[ids[i]] = neu_i
    umb[int(ids[i])] = neu_i
karte_out = lut[karte]

kat = json.loads((AB / "kategorien-teil.json").read_text(encoding="utf-8"))
eltern = {c["code"]: c["parent"] for c in kat["classes"]}
grob = {}
for c in eltern:
    g = c
    while eltern[g] is not None:
        g = eltern[g]
    grob[c] = g
kern = np.zeros((H, W), bool)
kern[K0:K1, K0:K1] = True
segs = []
for alt, n in sorted(umb.items(), key=lambda t: t[1]):
    i = info[alt]
    m = karte_out == n
    segs.append({"id": n, "klasse": i["klasse"], "grob": grob[i["klasse"]], "name": i["name"],
                 "im_kern": bool((m & kern).any()), "sicher": bool(i["sicher"]), "grund": i["grund"],
                 "quelle": i["quelle"], "flaeche": int(m.sum()), "grauwert": round(float(img[m].mean()), 1)})
tifffile.imwrite(AB / "labels.tif", karte_out.astype(np.uint32), compression="zlib")
(AB / "segmente.json").write_text(json.dumps(
    {"schema": "landseg-segmente/1", "segmente": segs,
     "verlauf": [{"bearbeiter": "agent-a-r1c1", "schritt": "arbeit/bauen.py",
                  "beschreibung": "Atome (Felzenszwalb 150/0,8/25) + Felder aus Atomen + Bildpunkt-Objekte "
                                  "(Straßen, Baumreihe, Rain) am Helligkeitsumschlag + Grauregel + Korrekturen je Segment"}]},
    ensure_ascii=False, indent=1), encoding="utf-8")
print("Segmente:", len(segs), "im Kern:", sum(s["im_kern"] for s in segs))
print(Counter(s["klasse"] for s in segs if s["im_kern"]))
