"""Build the fassung-C result for r0c1 from the vorstufe map plus own decisions.

Steps: (1) own class per vorstufe segment, (2) merges, (3) SLIC sub-split of mixed segments with
colour rules, (4) manual polygons, (5) connectivity and fragment clean-up, (6) write outputs."""
import json
import numpy as np
import tifffile
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
from skimage.segmentation import slic
from skimage.measure import label as cc
from skimage.draw import polygon as skpoly

D = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c"
O = f"{D}/abgabe/r0c1"
img = np.asarray(Image.open(f"{D}/teilkacheln/r0c1.png").convert("RGB"))
H, W = img.shape[:2]
vlab = tifffile.imread(f"{D}/vorstufe/r0c1/labels.tif").astype(np.int64)
vseg = {s["id"] - 200000: s for s in json.load(open(f"{D}/vorstufe/r0c1/segmente.json", encoding="utf-8"))["segmente"]}
lab = vlab - 200000  # short ids 1..234
KERN = np.zeros((H, W), bool)
KERN[64:564, 64:564] = True

# ---------------------------------------------------------------- (1) own classes (kern segments)
# id: (class, name, sicher, offen)
K = {}
def k(ids, cls, name, sicher=True, offen=""):
    for i in (ids if isinstance(ids, (list, tuple)) else [ids]):
        K[i] = (cls, name, sicher, offen)

k(29, "1.2.3", "Poolumfeld hell (Rand)", False, "Rand; Holzdeck oder Sand")
k(13, "3.1", "Rasen Vorgarten Nord", False, "fast ganz im Rand")
k(19, "1.2.1", "Straße hell (Beton)")
k(27, "4.1.1", "Laubbaum groß an der Straße", False, "evtl. zwei Kronen")
k(36, "4.1.1", "Laubbaum Nordgarten")
k(45, "4.2", "Baumgruppe östlich Pool", False, "Kronen nicht sicher trennbar")
k(47, "5.1", "Gebäudeschatten auf Straße")
k(52, "4.3", "Hecke/Strauch nördlich Haus (beschattet)", False, "dunkel, Hecke oder Schatten")
k(54, "1.1.1", "Wohnhaus Flachdach Ost")
k(58, "4.1.1", "Baum/Großstrauch Garten West", False, "Baum oder Großstrauch")
k(59, "1.2.3", "Poolumfeld hell (Holzdeck oder Sand)", False, "Holzdeck, Sand oder Pflaster nicht unterscheidbar")
k(60, "1.1.1", "Wohnhaus rotes Ziegeldach")
k(62, "5.1", "Gebäudeschatten an Zufahrt")
k(63, "1.2.2", "Zufahrt zwischen den Häusern")
k([64, 66], "4.3", "Zierstrauch")
k(65, "1.3.1", "Aufstellpool rund")
k(69, "5.1", "Schatten an Hauswand West", False, "Schatten oder dunkler Belag")
k(70, "5.1", "Gebäudeschatten Nordseite (Untergrund Grünstreifen?)")
k(72, "4.1.1", "Laubbaum zwischen den Häusern")
k(74, "1.1.1", "Wohnhaus Flachdach Mitte")
k(75, "4.4", "Gartenvegetation entlang Straße (Hecke, Sträucher)")
k(76, "4.1.1", "Laubbaum Vorgarten")
k(78, "1.2.3", "Weg/Zugang an Hausostseite", False, "Weg oder beschatteter Rasen")
k(79, "1.2.1", "Straßenrand/Gehsteig", False, "Mischfarbe Belag und Grün")
k(80, "4.1.1", "Laubbaum West")
k(81, "3.1", "Grünstreifen an der Straße")
k(82, "1.2.3", "Terrasse/Sitzplatz Südseite Haus", False, "klein, hell, Art unklar")
k(83, "3.1", "Rasen Garten Ost")
k(85, "1.2.2", "Hofeinfahrt/Stellplatz Asphalt")
k(86, "5.2", "Schatten Baum auf Grünstreifen", False, "Schatten oder Strauch")
k(87, "1.3.2", "Kleinobjekt an Terrasse", False, "Art unklar")
k([88, 90], "4.3", "Zierstrauch")
k(89, "1.2.1", "Gehsteig/Randstreifen mit Zaun", False, "schmal, Mischfarbe")
k(91, "1.2.3", "Terrasse/Pflaster vor Haus Ost", False, "Pflaster oder heller Strauch")
k(92, "4.4", "Gartenvegetation Hang")
k(93, "1.2.1", "Straße Asphalt dunkel")
k(94, "4.1.1", "Laubbaum an Straße", False, "dunkle Krone, evtl. mit Schatten")
k(96, "4.1.1", "Laubbaum hellgrün (Zierbaum)", False, "Baum oder Großstrauch")
k(98, "5.1", "Gebäudeschatten Nordecke")
k(102, "1.1.1", "Wohnhaus Walmdach grau")
k(103, "4.4", "Gartenvegetation Ost")
k(104, "3.1", "Rasen Garten Mitte")
k(105, "5.1", "Gebäudeschatten Garage")
k(107, "4.2", "Baumgruppe Garten West")
k(108, "4.3", "Strauch an Einfahrt")
k(109, "1.3.2", "Gartenmöbel (Tisch, Stühle)")
k(110, "1.1.2", "Garage")
k(111, "1.2.2", "Garagenvorplatz")
k(112, "5.1", "Gebäudeschatten Nordseite Haus")
k(115, "1.2.3", "Belag an Hausecke", False, "Belag oder Rasen")
k(116, "4.2", "Gehölz dicht West")
k(117, "5.1", "Schatten an Garage", False, "Schatten oder dunkler Belag")
k(118, "5.2", "Schlagschatten Konifere auf Rasen")
k(121, "1.2.3", "Gartenweg/Treppe zwischen Häusern", False, "schmal")
k(122, "4.1.1", "Laubbaum West")
k(123, "4.1.3", "Zierkonifere gelbgrün", False, "Nadelbaum vermutet (Säulenform, Farbe)")
k(125, "5.2", "Schlagschatten großer Baum auf Rasen")
k(126, "1.1.1", "Wohnhaus Flachdach West")
k(127, "1.2.3", "Belag an Hausecke Süd", False, "klein")
k(128, "3.1", "Rasenstreifen neben Haus")
k(130, "5.1", "Schatten an Hauswand", False, "Schatten oder Hecke")
k(131, "4.3", "Strauch")
k(132, "4.1.3", "Nadelbaum bläulich", False, "Blaufichte vermutet")
k(133, "5.1", "Schatten an Hauswand West", False)
k(134, "4.1.1", "Laubbaum groß", False, "evtl. zwei Kronen")
k(136, "3.3", "offener Boden (Beet/Kompost)", False, "Beet, Kompost oder Erde")
k(137, "4.4", "Gartenvegetation")
k(138, "1.1.2", "Anbau/Wintergarten", False, "Anbau oder Dach Terrasse")
k([139, 141, 148, 153, 158, 160, 165, 166, 197], "4.1.1", "Laubbaum")
k(140, "3.1", "Rasen/Wiese Garten Ost", False, "extensiv gemäht")
k(142, "5.2", "Schatten oder sehr dunkle Krone", False, "Schatten von Gehölz oder dunkle Baumkrone")
k(143, "3.1", "Rasen Garten Pool")
k(144, "1.2.3", "Gartenweg")
k(145, "4.1.2", "Blutbuche (rotlaubig)")
k(147, "3.1", "Rasenfleck")
k(154, "5.2", "Schatten unter Baumgruppe", False, "Untergrund nicht erkennbar")
k(155, "4.2", "Gehölz")
k(157, "4.4", "Gartenvegetation am Pool")
k(159, "1.2.3", "Terrasse Pool West")
k(163, "1.3.1", "Swimmingpool")
k(164, "5.2", "Schatten Baum auf Rasen")
k(167, "4.2", "Gehölz dicht Feldrand West")
k([169, 175, 179, 181, 182, 183, 184, 185, 186, 187, 188], "2.2", "Feldrain/Grasstreifen", False, "schmal, Übergang Feld–Gehölz")
k(170, "2.1", "Feld gemäht mit Schwaden")
k(171, "4.4", "Streifen Hecke/Saum Gartenende")
k(172, "4.3", "Strauch am Pool")
k(173, "4.3", "Strauch Feldrand")
k(174, "1.2.3", "Terrasse Pool Süd mit Möbeln")
k(176, "4.3", "Strauch")
k(180, "1.3.2", "Kleinbauwerk (Hochbeet/Mauer)", False, "Art nicht erkennbar")
k(189, "3.2", "Wiese langgrasig Süd")
k(193, "4.1.1", "Laubbaum am Feldrand", False, "Lücken in der Krone")
k([196, 200, 203, 209], "2.2", "Feldrain hell", False, "heller Saum, Erde oder trockenes Gras")
k(206, "4.1.1", "Laubbaum Süd", False)
k(207, "4.2", "Gehölz dunkel Süd", False, "Vorstufe: Schatten; wirkt wie Kronen")
k(211, "3.2", "Wiese Süd")
k(151, "3.2", "Wiese Ost", False, "Rand")
k([135, 106], "5.2", "Schatten oder dunkle Krone", False, "Rand")
k(124, "1.1.1", "Wohnhaus (Rand)", False, "Rand")
k(201, "4.2", "Gehölz (Rand)", False, "Rand")

# merges: source -> target (short ids)
MERGE = {57: 60, 67: 65, 61: 19, 73: 19, 77: 70, 68: 63, 71: 63, 55: 62, 100: 93, 101: 93,
         113: 83, 119: 83, 129: 104, 146: 134, 149: 143, 150: 153, 152: 153, 156: 141, 162: 160,
         97: 94, 191: 170, 195: 170, 199: 196, 202: 200, 204: 193, 205: 193, 208: 206}

# vorstufe class -> own class for remaining (context) segments
GEN = {"1.1.1": "1.1.1", "1.1.2": "1.1.2", "1.2.1": "1.2.1", "1.2.2": "1.2.1", "1.2.4": "1.2.2",
       "1.3.3": "1.3.1", "1.3.4": "3.1", "0.2": "5.2", "3.1": "3.1", "4.1": "4.2", "4.2.1": "4.1.1",
       "4.2.4": "4.3", "6.1": "2.2", "6.6": "2.2", "2.1": "3.2", "2.2": "3.3", "2.3": "3.2", "2.4.1": "2.2"}

# ---------------------------------------------------------------- (2) apply merges
for s, t in MERGE.items():
    lab[lab == s] = t

# ---------------------------------------------------------------- (3) SLIC sub-split with colour rules
def rule(px):
    r, g, b = px[:, 0].mean(), px[:, 1].mean(), px[:, 2].mean()
    v = (r + g + b) / 3
    sd = px.std(0).mean()
    exg = 2 * g - r - b
    if v < 52 and sd < 15:
        return "5.2"
    if max(r, g, b) - min(r, g, b) < 16 and v > 110:
        return "1.2.3"
    if r > g and v > 120:
        return "3.3"
    if exg >= 20 and g >= 100 and sd <= 20:
        return "3.1"
    if g < 86:
        return "4.2"
    return "4.4"

NAMES = {"5.2": "Schatten unter Gehölz", "1.2.3": "Belag/Weg", "3.3": "offener Boden/Sand",
         "3.1": "Rasen", "4.2": "Gehölz (Baumgruppe)", "4.4": "Gartenvegetation gemischt"}
SPLIT = {43: 400, 92: 500, 103: 500, 171: 250, 81: 250}
PARENT = {}
nxt = 1000
for sid, per in SPLIT.items():
    m = lab == sid
    n = max(2, int(m.sum() / per))
    s = slic(img, n_segments=n, compactness=8, sigma=1, mask=m, start_label=1, channel_axis=-1)
    s = cc(np.where(m, s, 0), connectivity=1, background=0)
    pieces = [p for p in np.unique(s) if p > 0]
    cls = {p: rule(img[s == p].astype(float)) for p in pieces}
    # merge same-class neighbouring pieces: label connected regions of the class map
    cmap = np.zeros((H, W), np.int32)
    codes = sorted(set(cls.values()))
    for p in pieces:
        cmap[s == p] = codes.index(cls[p]) + 1
    for ci, code in enumerate(codes):
        comp = cc(cmap == ci + 1, connectivity=1)
        for q in range(1, comp.max() + 1):
            mm = comp == q
            lab[mm] = nxt
            parent = K.get(sid, ("", "", True, ""))
            nm = NAMES[code]
            if sid == 171 and code == "4.2":
                code, nm = "4.3", "Hecke"
            K[nxt] = (code, nm + f" (aus {parent[1] or sid})", False,
                      "Teilung nach Farbe/Textur, Grenze und Klasse aus Regel")
            PARENT[nxt] = sid
            nxt += 1

# ---------------------------------------------------------------- (4) manual polygons
def band(points, half):
    """Polygon around a polyline with half width."""
    pts = np.array(points, float)
    left, right = [], []
    for i in range(len(pts)):
        a = pts[max(i - 1, 0)]
        b = pts[min(i + 1, len(pts) - 1)]
        d = b - a
        d = d / (np.hypot(*d) or 1)
        nrm = np.array([-d[1], d[0]])
        left.append(pts[i] + nrm * half)
        right.append(pts[i] - nrm * half)
    return left + right[::-1]

def poly_mask(pts):
    pts = np.array(pts, float)
    rr, cc_ = skpoly(pts[:, 1], pts[:, 0], (H, W))
    m = np.zeros((H, W), bool)
    m[rr, cc_] = True
    return m

# (target: existing id or None, class, name, sicher, offen, points, take-from ids or None=all except protected)
PROTECT = {60, 65, 54, 74, 102, 126, 110, 163}
POLYS = [
    (59, None, None, None, None,
     [(225, 58), (233, 50), (242, 47), (248, 50), (257, 58), (265, 67), (273, 70), (275, 80), (268, 88),
      (260, 92), (253, 95), (245, 92), (237, 88), (228, 83), (223, 75)], "split43"),
    (None, "1.1.2", "Gartenhaus/Schuppen dunkles Dach", True, "",
     [(77, 88), (106, 87), (107, 103), (78, 104)], "split43"),
    (None, "1.2.3", "Pflaster/Terrasse neben Schuppen", False, "hell, Art unklar",
     [(107, 96), (119, 96), (120, 110), (108, 110)], "split43"),
    (None, "1.3.2", "Gerätebox/kleines Objekt weiß", False, "Kiste, Box oder Möbel",
     [(212, 102), (220, 102), (221, 113), (213, 113)], "split43"),
    (None, "1.3.2", "Auto weiß am Straßenrand", False, "Fahrzeug vermutet",
     [(364, 77), (377, 76), (378, 88), (365, 88)], [51]),
    (None, "1.3.2", "Gartenobjekt grau-grün (Anhänger/Kasten)", False, "Art nicht erkennbar",
     [(371, 116), (386, 114), (387, 128), (372, 130)], [70, 76, 19]),
    (None, "1.3.2", "Gartenobjekt weiß (Liege)", False, "Art unklar",
     [(342, 374), (352, 374), (352, 380), (342, 380)], [143]),
    (None, "1.3.2", "Kleinobjekt hellgrün (Frühbeet?)", False, "Art nicht erkennbar",
     [(237, 396), (248, 396), (248, 402), (237, 402)], "split171"),
    (None, "1.3.2", "Gartenobjekt weiß (Schaukel/Bank)", False, "Art unklar",
     [(500, 247), (509, 247), (509, 256), (500, 256)], "split103"),
    (None, "1.2.3", "Gartenweg diagonal", False, "schmal, Breite geschätzt",
     band([(424, 245), (432, 260), (440, 274), (447, 284)], 2.2), "split103"),
    (None, "3.3", "heller Fleck im Rasen (lückig/Boden)", False, "lückiger Rasen oder ehemalige Fläche",
     [(413, 294), (446, 292), (448, 320), (414, 322)], [140]),
]
split_parents = {}
for i, sid in PARENT.items():
    split_parents.setdefault(f"split{sid}", []).append(i)

for tgt, cls, name, sicher, offen, pts, src in POLYS:
    pm = poly_mask(pts)
    if src is None:
        allowed = ~np.isin(lab, list(PROTECT))
    else:
        ids = split_parents.get(src, []) if isinstance(src, str) else src
        if isinstance(src, str):
            ids = ids + [int(src[5:])]
        allowed = np.isin(lab, ids)
    m = pm & allowed
    if tgt is None:
        lab[m] = nxt
        K[nxt] = (cls, name, sicher, offen)
        nxt += 1
    else:
        lab[m] = tgt

# light split pieces of 43 next to the pool deck belong to the deck
def _nb(m):
    dil = ndi.binary_dilation(m, structure=[[0, 1, 0], [1, 1, 1], [0, 1, 0]])
    return set(np.unique(lab[dil & ~m]).tolist())
for i in split_parents.get("split43", []):
    m = lab == i
    if m.any() and K[i][0] in ("1.2.3", "3.3") and 59 in _nb(m):
        lab[m] = 59

# field margin strip: less brown (R-B small) pixels of the field next to the meadow, west part
rb = ndi.uniform_filter(img[..., 0].astype(float) - img[..., 2].astype(float), 3)
dist = ndi.distance_transform_edt(~np.isin(lab, [189, 196, 193]))
X = np.arange(W)[None, :].repeat(H, 0)
bm = (lab == 170) & (dist <= 9) & (X < 215) & (rb < 29)
bm = ndi.binary_closing(bm, iterations=2) & (lab == 170) & (dist <= 9)
comp = cc(bm, connectivity=1)
for q in range(1, comp.max() + 1):
    mm = comp == q
    if mm.sum() < 25:
        continue
    lab[mm] = nxt
    K[nxt] = ("2.2", "Feldrain hell Südrand", False,
              "heller Saum aus trockenem Gras oder Erde; Grenze nach Farbton (weniger braun als Feld)")
    nxt += 1

# ---------------------------------------------------------------- (5) connectivity and fragments
def neighbours_border(lab, m):
    dil = ndi.binary_dilation(m, structure=[[0, 1, 0], [1, 1, 1], [0, 1, 0]])
    ring = dil & ~m
    vals, cnt = np.unique(lab[ring], return_counts=True)
    return dict(zip(vals.tolist(), cnt.tolist()))

def cls_of(i):
    if i in K:
        return K[i][0]
    return GEN.get(vseg.get(i, {}).get("klasse", ""), "4.4")

# split disconnected
for i in np.unique(lab):
    m = lab == i
    comp, n = ndi.label(m)
    if n > 1:
        sizes = np.bincount(comp.ravel())[1:]
        big = sizes.argmax() + 1
        for q in range(1, n + 1):
            if q == big:
                continue
            lab[comp == q] = nxt
            K[nxt] = (cls_of(i), (K[i][1] if i in K else "Teil") + " (Teil)",
                      K[i][2] if i in K else False, K[i][3] if i in K else "")
            nxt += 1

MIN = 30
changed = True
while changed:
    changed = False
    ids, cnts = np.unique(lab, return_counts=True)
    for i, c in sorted(zip(ids.tolist(), cnts.tolist()), key=lambda t: t[1]):
        if c >= MIN:
            break
        m = lab == i
        nb = neighbours_border(lab, m)
        if not nb:
            continue
        same = {j: n for j, n in nb.items() if cls_of(j) == cls_of(i)}
        tgt = max(same or nb, key=lambda j: (same or nb)[j])
        lab[m] = tgt
        changed = True
        break

# ---------------------------------------------------------------- (6) relabel and write
ids = np.unique(lab)
new = np.zeros(ids.max() + 1, np.uint32)
new[ids] = np.arange(1, len(ids) + 1)
out = new[lab].astype(np.uint32)
assert out.min() >= 1
tifffile.imwrite(f"{O}/labels.tif", out, compression="zlib", photometric="minisblack")

segs = []
herkunft = {}
for i in ids.tolist():
    m = out == new[i]
    entry = K.get(i)
    if entry is None:
        vs = vseg.get(i, {})
        c = GEN.get(vs.get("klasse", ""), "4.4")
        entry = (c, "Randsegment (Vorstufe übernommen)", False, "nur Kontextrand, grob nach Vorstufe")
    cls, name, sicher, offen = entry
    e = {"id": int(new[i]), "klasse": cls, "grob": cls.split(".")[0], "name": name,
         "im_kern": bool((m & KERN).any()), "sicher": bool(sicher), "flaeche": int(m.sum()),
         "flaeche_kern": int((m & KERN).sum()),
         "herkunft": (f"vorstufe:{i + 200000}" if i < 1000 else ("teilung/polygon" if i >= 1000 else ""))}
    if offen:
        e["offen"] = offen
    segs.append(e)
json.dump({"schema": "landseg-segmente/1", "segmente": segs,
           "verlauf": [{"bearbeiter": "fassung-c-r0c1", "schritt": "build.py: Vorstufe + eigene Klassen, Verschmelzen, Teilen, Polygone"}]},
          open(f"{O}/segmente.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("segmente", len(segs), "im_kern", sum(s["im_kern"] for s in segs),
      "unsicher_kern", sum((not s["sicher"]) and s["im_kern"] for s in segs))
