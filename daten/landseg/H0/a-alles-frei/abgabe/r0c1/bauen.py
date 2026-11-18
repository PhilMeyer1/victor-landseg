"""Fassung A, r0c1: eigene Segmentierung und Klassen.
Schritte: Straßen (Korridor + Helligkeit), Rest Wasserscheide + Verschmelzen nach Grauwert,
Kleinstücke an Nachbarn, Klassen nach Regeln, dann Korrekturen aus korrekturen.json.
Schreibt tmp/labels_roh.npy, tmp/seg_roh.json (vor Korrekturen) bzw. die Abgabe mit --abgabe."""
import json
import sys
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
from skimage import morphology, segmentation, filters, graph, measure

BILD = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r0c1.png"
a = np.array(Image.open(BILD)).astype(np.float32)
H, W = a.shape
g = ndi.gaussian_filter(a, 1.5)
STR = json.load(open("strassen.json", encoding="utf-8"))
KOR = json.load(open("korrekturen.json", encoding="utf-8"))


def poly_mask(pts, w=None, fill=False):
    im = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(im)
    pts = [tuple(p) for p in pts]
    if fill:
        d.polygon(pts, fill=1, outline=1)
    else:
        d.line(pts, fill=1, width=max(1, int(2 * w)), joint="curve")
        for p in pts:
            d.ellipse([p[0] - w, p[1] - w, p[0] + w, p[1] + w], fill=1)
    return np.array(im).astype(bool)


# ---------- 1 Straßen ----------
road = np.zeros((H, W), np.int32)
best = np.full((H, W), np.inf)
gr2 = ndi.gaussian_filter(a, 2.0)
for k, s in enumerate(STR["strassen"], start=1):
    kor = poly_mask(s["punkte"], s["breite"])
    m = kor & (gr2 > s.get("schwelle", 120))
    m = morphology.closing(m, morphology.disk(2))
    m = ndi.binary_fill_holes(m)
    m = morphology.opening(m, morphology.disk(s.get("oeffnen", 3)))
    ml = poly_mask(s["punkte"], 1)
    lab, n = ndi.label(m)
    keep = np.unique(lab[ml & (lab > 0)])
    m = np.isin(lab, keep[keep > 0])
    dist = ndi.distance_transform_edt(~ml)
    upd = m & (dist < best)
    road[upd] = k
    best[upd] = dist[upd]
# Flächen von Hand (Polygone), überschreiben alles
hand = np.zeros((H, W), np.int32)
for j, p in enumerate(KOR.get("polygone", []), start=1):
    hand[poly_mask(p["punkte"], fill=True)] = j

# ---------- 2 Rest: Wasserscheide ----------
grad = filters.sobel(g)
mk, _ = ndi.label(morphology.h_minima(grad, STR.get("h", 4)))
ws = segmentation.watershed(grad, mk)
rgb = np.stack([g] * 3, -1)
rag = graph.rag_mean_color(rgb, ws, connectivity=1)
ws = graph.cut_threshold(ws, rag, STR.get("rag", 20))
# feinere Zerlegung in Gebieten mit schwachem Kontrast
for j, fb in enumerate(KOR.get("fein", []), start=1):
    pm = poly_mask(fb["punkte"], fill=True)
    # Gebiet = grobe Segmente, die überwiegend im Polygon liegen (Grenzen bleiben Bildkanten)
    ids_c, cnt_c = np.unique(ws, return_counts=True)
    inn = ndi.sum(pm, ws, ids_c)
    fm = np.isin(ws, ids_c[inn > 0.5 * cnt_c])
    mk2, _ = ndi.label(morphology.h_minima(grad, fb.get("h", 2)) & fm)
    w2 = segmentation.watershed(grad, mk2, mask=fm)
    rag2 = graph.rag_mean_color(rgb, w2, connectivity=1)
    w2 = graph.cut_threshold(w2, rag2, fb.get("rag", 10))
    ws = np.where(fm, w2 + 10 ** 6 * j, ws)

lab = np.zeros((H, W), np.int64)
lab[:] = ws + 100000
lab[road > 0] = road[road > 0]
lab[hand > 0] = hand[hand > 0] + 50000


def relabel4(lab):
    out = np.zeros(lab.shape, np.int64)
    nxt = 1
    src = {}
    for v in np.unique(lab):
        cc, n = ndi.label(lab == v)
        for i in range(1, n + 1):
            out[cc == i] = nxt
            src[nxt] = int(v)
            nxt += 1
    return out, src


lab, src = relabel4(lab)


def merge_small(lab, src, minpx, protect):
    while True:
        ids, cnt = np.unique(lab, return_counts=True)
        small = [i for i, c in zip(ids, cnt) if c < minpx and src[i] not in protect]
        if not small:
            return lab
        means = ndi.mean(g, lab, ids)
        mean = dict(zip(ids, means))
        changed = False
        for i in small:
            m = lab == i
            if not m.any():
                continue
            ring = morphology.dilation(m, morphology.disk(1)) & ~m
            nb = lab[ring]
            nb = nb[nb != i]
            if len(nb) == 0:
                continue
            u, c = np.unique(nb, return_counts=True)
            # prefer non-road, similar mean, long border
            score = [c[k] - 0.5 * abs(mean.get(u[k], 0) - mean[i]) for k in range(len(u))]
            t = u[int(np.argmax(score))]
            lab[m] = t
            changed = True
        if not changed:
            return lab


lab = merge_small(lab, src, STR.get("min", 20), protect=set())
lab, src2 = relabel4(lab)
src = {k: src[v] for k, v in src2.items()}
lab = merge_small(lab, src, STR.get("min", 20), protect=set())
lab, src2 = relabel4(lab)
src = {k: src[v] for k, v in src2.items()}

# ---------- 3 Merkmale ----------
std = np.sqrt(np.maximum(ndi.gaussian_filter(a ** 2, 2) - ndi.gaussian_filter(a, 2) ** 2, 0))
props = measure.regionprops(lab.astype(np.int32), intensity_image=g)
seg = {}
for p in props:
    i = p.label
    sv = src[i]
    r = sv if sv < 50000 else 0
    hd = sv - 50000 if 50000 < sv < 100000 else 0
    mj, mn = p.axis_major_length, max(p.axis_minor_length, 1)
    cy, cx = p.centroid
    seg[i] = dict(id=i, flaeche=int(p.area), mittel=round(float(p.intensity_mean), 1),
                  streu=round(float(std[lab == i].mean()), 1),
                  lang=round(float(mj / mn), 2), breite=round(float(mn), 1),
                  cx=round(float(cx), 1), cy=round(float(cy), 1),
                  strasse=r, hand=hd, ori=float(p.orientation))


# ---------- 4 Klassen nach Regeln ----------
def regel(s):
    if s["hand"]:
        p = KOR["polygone"][s["hand"] - 1]
        return p["klasse"], p.get("sicher", True), p.get("grund", "von Hand gezogen")
    if s["strasse"]:
        st = STR["strassen"][s["strasse"] - 1]
        return st.get("klasse", "1.2.1"), True, "Straßenkorridor, hell und breit"
    m, sd, ln, A = s["mittel"], s["streu"], s["lang"], s["flaeche"]
    if m < 62 and ln < 2.5 and A > 800:
        return "9", False, "große dunkle Fläche ohne Streifenform: dichter Garten, Gehölz, dunkles Dach oder Schatten - nicht bestimmbar"
    if m < 62:
        return "9.1", False, "sehr dunkel: Schlagschatten oder Schattenseite eines Dachs, Untergrund nicht erkennbar"
    if m > 140:
        if ln >= 2.2:
            klar = ln >= 3.0 and m >= 150
            return "1.1.1", klar, ("hell, lang und schmal, parallel zu den Nachbarn: Dachstreifen eines Längsbaus" if klar else
                                   "hell und länglich, aber kurz oder nur mäßig hell: Dachstreifen oder heller Hofstreifen")
        return "1.1", False, "hell, kompakt: Dach (Kopf- oder Nebengebäude) oder offene helle Hoffläche"
    if m > 105:
        if ln >= 3.0:
            return "1.1", False, "mittelhell, lang: Dachfläche eines Längsbaus oder Hofstreifen"
        return "1.3", False, "mittelgrau ohne Dachform: Hof- oder Gartenfläche; Pflaster, Erde, Rasen auf SW nicht trennbar"
    if ln >= 3.0:
        return "1.1", False, "dunkelgrau, lang neben hellem Dachstreifen: beschattete Dachhälfte oder Schlagschatten auf Hof"
    return "2.1", False, "dunkelgrau, weich: Garten oder Hof im Halbschatten; Bewuchs auf SW nicht sicher, Farbbild würde entscheiden"

for i, s in seg.items():
    k, si, gr = regel(s)
    s.update(klasse=k, sicher=si, grund=gr, regel=k)

# helle Längsstreifen parallel zu einer angrenzenden Straße: Straßenrand statt Dach
road_of = {i: s["strasse"] for i, s in seg.items() if s["strasse"]}
hz = lab[:, 1:] != lab[:, :-1]
vz = lab[1:, :] != lab[:-1, :]
paare = np.concatenate([np.stack([lab[:, 1:][hz], lab[:, :-1][hz]], 1), np.stack([lab[1:, :][vz], lab[:-1, :][vz]], 1)])
from collections import Counter as _C
kont = _C(map(tuple, np.sort(paare, 1)))
nb_road = {}
for (u, v), c in kont.items():
    for x, y in ((u, v), (v, u)):
        if y in road_of and x not in road_of and c >= 8:
            nb_road.setdefault(int(x), []).append((c, road_of[y]))
parallel = 0
for i, lst in nb_road.items():
    s = seg[i]
    if s["hand"] or s["mittel"] <= 120 or s["lang"] < 2.2:
        continue
    c, rk = max(lst)
    pts = np.array(STR["strassen"][rk - 1]["punkte"], float)
    best_d, vec = 1e9, None
    for q in range(len(pts) - 1):
        m = (pts[q] + pts[q + 1]) / 2
        d = np.hypot(m[0] - s["cx"], m[1] - s["cy"])
        if d < best_d:
            best_d, vec = d, pts[q + 1] - pts[q]
    vec = vec / np.linalg.norm(vec)
    o = s["ori"]
    ax = np.array([np.sin(o), np.cos(o)])
    if abs(float(ax @ vec)) > np.cos(np.radians(20)):
        s.update(klasse="1.2.1", sicher=False, regel="1.2.1",
                 grund="heller Streifen längs der Straße, an sie grenzend: Straßenrand, Gehweg oder Bankett; Hausfront nicht ausgeschlossen")
        parallel += 1
print("parallel zur Straße", parallel)

np.save("tmp/labels_roh.npy", lab.astype(np.uint32))
json.dump({str(k): v for k, v in seg.items()}, open("tmp/seg_roh.json", "w", encoding="utf-8"), ensure_ascii=False)
print("segmente", len(seg), "im kern", sum(1 for s in seg.values() if 64 <= s["cx"] < 564 and 64 <= s["cy"] < 564))
from collections import Counter
print(Counter(s["klasse"] for s in seg.values()))
