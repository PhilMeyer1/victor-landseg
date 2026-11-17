"""Fassung C, Teilkachel r0c0: eigene Label-Karte aus der Vorstufe plus Eingriffe bauen.

Ablauf: Vorstufen-IDs auf eigene Gruppen abbilden (verschmelzen), große Flächen per Polygon teilen,
Einzelheiten (Hecke, Schatten, Terrasse, Gartenhaus, Mauer) per Polygon einzeichnen, danach je Gruppe
zusammenhängende Teile bilden, Splitter an den Nachbarn mit der längsten Grenze geben.
"""
import json
import sys
from collections import Counter, defaultdict

import cv2
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

sys.path.insert(0, "C:/Users/Phil/Developement/Victor/landseg")
from landseg.dateien import lese_labels, schreibe_labels  # noqa: E402

BASIS = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c"
AUS = BASIS + "/abgabe/r0c0"
L0 = lese_labels(BASIS + "/vorstufe/r0c0/labels.tif").astype(np.int64) - 100000
IMG = np.asarray(Image.open(BASIS + "/teilkacheln/r0c0.png").convert("RGB")).astype(np.float32)
GRAU = cv2.blur(IMG.mean(2), (3, 3))
H, W = L0.shape
KERN = (64, 64, 564, 564)

# Gruppe: (klasse, name, sicher, notiz)
G = {
    "rasen_nw": ("2.1", "Gartenrasen NW (Rand)", False, "nur Rand"),
    "hecke_nw": ("2.3", "Hecke/Zaunlinie NW (Rand)", False, "Hecke oder Zaun mit Schatten"),
    "strauch3": ("2.4", "rotlaubiger Gartenstrauch (Rand)", False, ""),
    "poolrand": ("1.2.3", "Beckenumrandung / Terrasse am Pool (Rand)", False, ""),
    "pool": ("1.3.1", "Schwimmbecken offen (Rand)", True, ""),
    "garten_n1": ("2.2", "Ziergarten N (Rand)", False, ""),
    "schatten9": ("5.2", "Schatten zwischen Pool und Haus (Rand)", False, ""),
    "haus10": ("1.1.1", "Wohnhaus rotes Ziegeldach", True, ""),
    "garten11": ("2.2", "Garten am Hang mit Sträuchern", False, "Rasen und Gehölz gemischt, Grenze zur Böschung geschätzt"),
    "schatten12": ("5.2", "Schatten am Haus (Rand)", False, ""),
    "haus13": ("1.1.1", "Wohnhaus mit Solaranlage (Rand)", True, ""),
    "hof14": ("1.2.2", "Hof-/Platzfläche an der Einmündung", True, "enthält ein abgestelltes helles Fahrzeug"),
    "baum15": ("4.1", "Baum (Rand)", False, ""),
    "rasen16": ("2.1", "Gartenrasen NO (Rand)", False, ""),
    "haus17": ("1.1.1", "Wohnhaus rotes Dach (Rand)", True, ""),
    "garten24": ("2.2", "Garten (Rand)", False, ""),
    "strasse_w": ("1.2.1", "Straße West (Rand, unter Baumschatten)", False, ""),
    "baumgr48": ("4.2", "Baumgruppe an der Straße, dunkle Kronen", True, "Nadel/Laub nicht sicher"),
    "baum60": ("4.1", "Baum (Rand)", False, ""),
    "strauch30": ("2.4", "Gartenstrauch (Rand)", False, ""),
    "strauch32": ("2.4", "Gartenstrauch (Rand)", False, ""),
    "strauch42": ("2.4", "Gartenstrauch (Rand)", False, ""),
    "strauch43": ("2.4", "Gartenbaum dunkel (Rand)", False, ""),
    "haus33": ("1.1.1", "Wohnhaus Satteldach mit Gauben", True, ""),
    "pflaster34": ("1.2.3", "Pflaster am Haus (Rand)", False, ""),
    "garten36": ("2.2", "Gartenstreifen östlich Haus", False, ""),
    "boesch38": ("3.1.3", "Grasböschung zwischen Hecke und Straße", True, ""),
    "hecke41": ("2.3", "Hecke/Zaun an der Grundgrenze", False, "Hecke oder Zaun mit Schatten"),
    "gehoelz40": ("2.4", "Gartengehölz östlich Haus", False, ""),
    "strauch46": ("2.4", "Strauchreihe am Zaun", False, ""),
    "rasen47": ("2.1", "Gartenrasen hinter Rundhecke", True, ""),
    "hecke_rund": ("2.3", "Rundhecke um den Garten", True, ""),
    "weg52": ("1.2.3", "Gartenweg/Treppe, Pflaster rötlich", False, "Weg oder Mauerkrone"),
    "mauer63": ("1.3.2", "Mauerkante mit Schattenband", False, "niedrige Mauer vermutet"),
    "hecke55": ("2.3", "Hecke (Rand)", False, ""),
    "ausst57": ("2.5", "Paletten/Sandkasten im Garten", False, "Art des Gegenstands unsicher"),
    "strasse": ("1.2.1", "Straße (Asphalt)", True, ""),
    "garten61": ("2.2", "Garten mit befestigter Fläche", False, "überwiegend Rand"),
    "haus62": ("1.1.1", "Wohnhaus (Rand)", True, ""),
    "pflaster69": ("1.2.2", "befestigte Fläche (Rand)", False, ""),
    "garten70": ("2.2", "Ziergarten mit Spielgeräten", True, ""),
    "gehoelz73": ("2.4", "Gartengehölz am Haus", True, ""),
    "garten78": ("2.2", "Gartenstreifen südlich Haus mit Möbeln", False, ""),
    "gehoelz77": ("2.4", "Gartenbaum dunkel", False, "Baum oder Großstrauch"),
    "holz86": ("5.1", "Holzhaufen / Schnittgut", True, "Rand mit Kraut und Schatten einbezogen"),
    "anbau82": ("1.1.2", "Anbau/Pergola rotbraun am Haus", False, "Dach eines Anbaus oder Markise"),
    "gehoelz83": ("2.4", "Gartengehölz (Rand)", False, ""),
    "gehoelz88": ("2.4", "Gartengehölz (Rand)", False, ""),
    "gehoelz89": ("2.4", "Gartensträucher", True, ""),
    "pflaster90": ("1.2.2", "Zufahrt (Rand)", False, ""),
    "gehoelz91": ("2.4", "Gartenbaum hell", True, ""),
    "gruen_n": ("3.1.3", "Grünstreifen Nordrand der Straße", True, ""),
    "zufahrt": ("1.2.2", "Zufahrt/Vorplatz hell", True, ""),
    "gehsteig": ("1.2.2", "Randstreifen/Gehsteig Südrand der Straße", False, "mit kleinen Sträuchern"),
    "hecke106": ("2.3", "Hecke nördlich Flachdachhaus", False, "Hecke im Hausschatten"),
    "schatten_hecke": ("5.2", "Schlagschatten der hohen Hecke auf der Wiese", True, ""),
    "hecke_w": ("2.3", "hohe geschnittene Hecke an der Grundgrenze", True, "Breite geschätzt"),
    "gehoelz98": ("2.4", "Gartengehölz zwischen Hecke und Zufahrt", True, ""),
    "baum103": ("4.1", "Baum (Rand)", False, ""),
    "gehoelz108": ("2.4", "Gartenstrauch NO-Ecke Haus", False, ""),
    "gehoelz109": ("2.4", "Gartengehölz dunkel", False, ""),
    "baum112": ("4.1", "Baum in der Wiese", False, "Baum oder großer Strauch"),
    "haus113": ("1.1.1", "Flachdachhaus", True, "dunkle Dachfläche Westteil mitgezählt"),
    "gehoelz114": ("2.4", "Gartenbaum hell", True, ""),
    "gehoelz115": ("2.4", "Gartenbaum dunkel (Nadel?)", False, ""),
    "schatten117": ("5.2", "Hausschatten an der Westwand", False, ""),
    "haus118": ("1.1.1", "Wohnhaus (Rand)", True, ""),
    "garten119": ("2.4", "Sträucher SW-Ecke Garten", False, ""),
    "rasen120": ("2.1", "Gartenrasen Flachdachhaus", True, ""),
    "gehoelz121": ("2.4", "Gartenkonifere bläulich", False, ""),
    "gehoelz122": ("2.4", "Gartengehölz", False, ""),
    "busch123": ("4.3", "Gebüsch in der Wiese", False, ""),
    "busch125": ("4.3", "Gebüsch in der Wiese", False, ""),
    "baum126": ("4.1", "Baum (Rand)", False, ""),
    "baum127": ("4.1", "Baum dunkel am Gartenrand", False, ""),
    "gehoelz128": ("2.4", "Gartengehölz (Rand)", False, ""),
    "pool129": ("1.3.1", "Schwimmbecken abgedeckt", False, "Abdeckung grau; Becken vermutet"),
    "baum130": ("4.1", "Baum (Rand)", False, ""),
    "strauch131": ("2.4", "Strauch an der Gartengrenze", False, ""),
    "strauch134": ("2.4", "Strauch an der Gartengrenze", False, ""),
    "baum135": ("4.1", "Baum mit großer Krone", True, ""),
    "baum136": ("4.1.1", "Blutbuche (rotlaubiger Laubbaum)", True, ""),
    "rasen137": ("2.1", "Gartenrasen unterhalb Pool", True, ""),
    "busch138": ("4.3", "Gebüsch", False, ""),
    "baum140": ("4.1", "Baum dunkel", False, ""),
    "baum142": ("4.1", "Baum (Rand)", False, ""),
    "wiese143": ("3.1.1", "Wiese zwischen Garten und Feld", False, "Wiese oder ungepflegter Gartenteil"),
    "busch144": ("4.3", "Gebüsch (Rand)", False, ""),
    "baum145": ("4.1", "Baum dunkel", False, ""),
    "baumgr147": ("4.2", "Baumgruppe (Rand)", False, ""),
    "baumgr149": ("4.2", "Baumgruppe dunkel östlich der Blutbuche", True, ""),
    "busch151": ("4.3", "Gebüsch", False, ""),
    "baum157": ("4.1", "Baum dunkel", False, ""),
    "feld159": ("3.2", "gemähte Fläche mit Schwaden", True, "Heu oder Stroh, Acker oder Wiese offen"),
    "busch161": ("4.3", "Gebüsch", False, ""),
    "baum165": ("4.1", "Baum dunkel, große Krone", False, "Krone oder Krone mit Schlagschatten"),
    "wiese166": ("3.1.2", "Wiese gleichmäßig, niedrig", False, "gemäht oder nur kurzrasig, nicht sicher"),
    "baum171": ("4.1", "Baum dunkel", False, ""),
    "wiese175": ("3.1.1", "Wiese ungemäht südlich der Schwaden", True, ""),
    "dunkel177": ("4.2", "Gehölzrand, dunkle Kronen", False, "dunkle Kronen oder Schatten des Bestands"),
    "busch178": ("4.3", "Strauch hell", False, ""),
    "baum180": ("4.1", "Baum dunkel", False, ""),
    "baum181": ("4.1", "Baum dunkel", False, ""),
    "baum184": ("4.1", "Baum dunkel", False, "Baum oder Gebüsch"),
    "dunkel185": ("4.2", "Gehölzrand, dunkle Kronen", False, "dunkle Kronen oder Schatten des Bestands"),
    "busch186": ("4.3", "Gebüsch klein", False, ""),
    "kronen191": ("4.2.1", "Laubholz-Bestand, helle Kronen", True, ""),
    "dunkel194": ("4.2", "Gehölz dunkel SO", False, ""),
    "baum199": ("4.1", "Baum (Rand)", False, ""),
    "baum201": ("4.1", "Baum (Rand)", False, ""),
    "baum202": ("4.1", "Baum (Rand)", False, ""),
    "baum203": ("4.1", "Baum (Rand)", False, ""),
    "baum205": ("4.1", "Baum (Rand)", False, ""),
    "schatten45": ("5.2", "Schatten (Rand)", False, ""),
    # aus Polygonen
    "wiese_a": ("3.1.1", "Wiese ungemäht (Altgras, Kräuter)", True, ""),
    "busch_b": ("3.3", "verbuschte Wiese, Gebüsch-Hochstauden-Mosaik", True, "Grenze zur offenen Wiese geschätzt; Trampelpfad nicht ausgeschieden"),
    "schuppen": ("1.1.2", "Gartenhaus/Spielhaus", False, "kleines Dach, Art unsicher"),
    "rund124": ("2.5", "runder heller Gegenstand im Rasen", False, "Schachtdeckel, Tisch oder Becken"),
    "mauer_s": ("1.3.2", "Mauer/Randstein an der Gartengrenze Süd", False, "schmal, Lage geschätzt"),
    "terrasse": ("1.2.3", "Terrasse mit Rundelement", True, ""),
}

ZUORD = {}
def z(gruppe, *nums):
    for n in nums:
        ZUORD[n] = gruppe

z("rasen_nw", 1, 2, 23); z("hecke_nw", 26); z("strauch3", 3); z("poolrand", 4, 20); z("pool", 5, 37)
z("garten_n1", 6, 7, 8); z("schatten9", 9); z("haus10", 10); z("garten11", 11); z("schatten12", 12)
z("haus13", 13); z("hof14", 14, 19, 21, 22, 28, 39, 87); z("baum15", 15); z("rasen16", 16, 18, 29)
z("haus17", 17); z("garten24", 24); z("strasse_w", 25, 35); z("baumgr48", 27, 48, 49, 72)
z("baum60", 60, 64); z("strauch30", 30); z("strauch32", 32); z("strauch42", 42); z("strauch43", 43)
z("haus33", 31, 33); z("pflaster34", 34); z("garten36", 36, 53); z("boesch38", 38, 44)
z("hecke41", 41, 51); z("gehoelz40", 40); z("strauch46", 46); z("rasen47", 47)
z("hecke_rund", 50, 58, 65); z("weg52", 52); z("mauer63", 63, 66, 68); z("hecke55", 55)
z("ausst57", 57); z("strasse", 54, 59); z("garten61", 61); z("haus62", 62); z("pflaster69", 69, 75)
z("wiese_a", 56, 67, 79, 84, 92); z("garten70", 70, 76); z("gehoelz73", 71, 73); z("garten78", 74, 78)
z("gehoelz77", 77); z("holz86", 80, 81, 86); z("anbau82", 82); z("gehoelz83", 83, 85); z("gehoelz88", 88)
z("gehoelz89", 89); z("pflaster90", 90); z("gehoelz91", 91, 96); z("gruen_n", 93, 95, 99, 100)
z("zufahrt", 94, 101, 102); z("gehsteig", 104, 105, 107); z("hecke106", 106, 111)
z("schatten_hecke", 97, 116); z("gehoelz98", 98); z("baum103", 103); z("gehoelz108", 108)
z("gehoelz109", 109, 110); z("baum112", 112); z("haus113", 113); z("gehoelz114", 114)
z("gehoelz115", 115); z("schatten117", 117); z("haus118", 118); z("garten119", 119, 133)
z("rasen120", 120, 124); z("gehoelz121", 121); z("gehoelz122", 122); z("busch123", 123)
z("busch125", 125); z("baum126", 126); z("baum127", 127, 141); z("gehoelz128", 128)
z("pool129", 129, 139); z("baum130", 130); z("strauch131", 131); z("strauch134", 134)
z("baum135", 135, 146); z("baum136", 136); z("rasen137", 137); z("busch138", 138); z("baum140", 140)
z("baum142", 142); z("wiese143", 143, 148, 154, 158); z("busch144", 144); z("baum145", 145)
z("baumgr147", 147); z("baumgr149", 149, 150, 152); z("busch151", 151); z("baum157", 157)
z("feld159", 156, 159, 160, 162, 163, 164); z("busch161", 161); z("baum165", 165, 168)
z("wiese166", 166); z("baum171", 171); z("busch_b", 172, 176, 193, 195); z("wiese175", 173, 174, 175)
z("dunkel177", 177); z("busch178", 178); z("kronen191", 179, 183, 187, 189, 191)
z("baum180", 180, 192); z("baum181", 181); z("baum184", 184); z("dunkel185", 185, 190)
z("busch186", 186); z("dunkel194", 194); z("baum199", 199); z("baum201", 201); z("baum202", 202)
z("baum203", 203); z("baum205", 205); z("schatten45", 45)
AUTO = {132, 153, 155, 167, 169, 170, 182, 188, 196, 197, 198, 200, 204, 206}

def poly(pts):
    m = np.zeros((H, W), np.uint8)
    cv2.fillPoly(m, [np.array(pts, np.int32)], 1)
    return m.astype(bool)

def kreis(cx, cy, r):
    yy, xx = np.mgrid[0:H, 0:W]
    return (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r

alle = set(np.unique(L0).tolist())
fehlt = alle - set(ZUORD) - AUTO
assert not fehlt, f"ohne Zuordnung: {sorted(fehlt)}"

namen = list(G)
idx = {g: i + 1 for i, g in enumerate(namen)}
K = np.zeros((H, W), np.int64)  # Gruppenindex, 0 = noch offen (AUTO)
for n, g in ZUORD.items():
    K[L0 == n] = idx[g]

# --- Teilung der großen Wiesen (56, 166) ---
B = poly([(0, 140), (40, 150), (95, 185), (100, 240), (140, 255), (200, 262), (250, 285), (275, 320),
          (300, 380), (305, 430), (325, 470), (335, 520), (345, 560), (360, 627), (300, 627), (300, 600),
          (260, 585), (200, 575), (130, 560), (118, 545), (104, 532), (103, 482), (100, 474),
          (60, 468), (40, 405), (0, 400)])
gross = np.isin(L0, [56, 166])
K[gross & B] = idx["busch_b"]
# glatte Wiese im Südwesten, die die Vorstufe noch zu 56 zählte
K[(L0 == 56) & ~B & poly([(0, 400), (135, 400), (135, 627), (0, 627)])] = idx["wiese166"]
F = poly([(340, 500), (530, 500), (530, 627), (345, 627)])
K[(L0 == 56) & ~B & F] = idx["kronen191"]

# --- Hecke West und ihr Schlagschatten ---
S = poly([(320, 147), (316, 170), (312, 200), (308, 230), (304, 260), (301, 285), (302, 298),
          (309, 298), (310, 285), (313, 260), (317, 230), (321, 200), (324, 170), (329, 147)])
Hh = poly([(329, 147), (324, 170), (321, 200), (317, 230), (313, 260), (310, 285), (309, 298),
           (318, 298), (319, 285), (322, 260), (326, 230), (329, 200), (332, 170), (337, 147)])
basis_h = np.isin(L0, [56, 97, 98, 116, 119, 120])
# zeilenweise: dunkler Lauf um die erwartete Mitte = Schatten, rechts daneben die Hecke
K[np.isin(L0, [97, 116])] = idx["wiese_a"]  # alte Schattenstreifen erst freigeben
for y in range(147, 299):
    c = 326 - (y - 150) * 18 / 140
    xs = [x for x in range(int(c) - 8, int(c) + 9) if GRAU[y, x] < 62 and basis_h[y, x]]
    if not xs:
        continue
    a, b = min(xs), max(xs)
    for x in range(a, b + 1):
        if basis_h[y, x]:
            K[y, x] = idx["schatten_hecke"]
    breite = 8 if y < 215 else 11
    for x in range(b + 1, b + 1 + breite):
        if basis_h[y, x] and not (y > 262 and x > 328):
            K[y, x] = idx["hecke_w"]

# --- Einzelheiten ---
K[np.isin(L0, [70, 47]) & poly([(430, 104), (444, 103), (445, 117), (431, 117)])] = idx["schuppen"]
K[np.isin(L0, [124, 120]) & kreis(333.5, 271.5, 4.6)] = idx["rund124"]
K[np.isin(L0, [119, 120, 56, 131, 133]) & poly([(313, 290), (348, 298), (347, 302), (312, 294)])] = idx["mauer_s"]
ter = poly([(422, 239), (471, 239), (471, 270), (422, 270)]) | kreis(447, 267, 10)
K[(L0 == 113) & ter] = idx["terrasse"]
K[(L0 == 120) & kreis(447, 267, 10) & (GRAU > 130)] = idx["terrasse"]

# --- Segmente bilden: je Gruppe zusammenhängende Teile ---
STRUKT = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])

def nachbar_grenzen(M0, sid):
    ys, xs = np.nonzero(M0 == sid)
    if len(ys) == 0:
        return Counter()
    M = M0[max(ys.min() - 1, 0): ys.max() + 2, max(xs.min() - 1, 0): xs.max() + 2]
    h, w = M.shape
    c = Counter()
    for dy, dx in ((0, 1), (1, 0)):
        a = M[: h - dy, : w - dx]; b = M[dy:, dx:]
        sel = (a != b)
        aa = a[sel]; bb = b[sel]
        for p, q in zip(aa.tolist(), bb.tolist()):
            if p == sid and q > 0:
                c[q] += 1
            elif q == sid and p > 0:
                c[p] += 1
    return c

M = np.zeros((H, W), np.int64)
gruppe_von = {}
nid = 0
for g in namen:
    m = K == idx[g]
    if not m.any():
        continue
    lab, n = ndi.label(m, structure=STRUKT)
    for i in range(1, n + 1):
        nid += 1
        M[lab == i] = nid
        gruppe_von[nid] = g

# offene Pixel (AUTO) und Splitter verteilen
MIN = 75
SCHUTZ = {"rund124"}  # kleine, aber eindeutig eigene Gegenstände
def verteile():
    global M
    for _ in range(50):
        offen = M == 0
        if offen.any():
            lab, n = ndi.label(offen, structure=STRUKT)
            for i in range(1, n + 1):
                nid_t = -i
                M[lab == i] = nid_t
            for i in range(1, n + 1):
                c = nachbar_grenzen(M, -i)
                c = Counter({k: v for k, v in c.items() if k > 0})
                if c:
                    M[M == -i] = c.most_common(1)[0][0]
            M[M < 0] = 0
            continue
        flaechen = Counter(M.ravel().tolist())
        klein = [s for s, a in flaechen.items() if a < MIN and gruppe_von.get(s) not in SCHUTZ]
        if not klein:
            return
        for s in sorted(klein, key=lambda s: flaechen[s]):
            if (M == s).sum() == 0:
                continue
            c = nachbar_grenzen(M, s)
            if c:
                M[M == s] = c.most_common(1)[0][0]
        # Zusammenhang neu prüfen
        neu = np.zeros_like(M); k = 0; gv = {}
        for s in np.unique(M):
            lab, n = ndi.label(M == s, structure=STRUKT)
            for i in range(1, n + 1):
                k += 1; neu[lab == i] = k; gv[k] = gruppe_von[s]
        M = neu; gruppe_von.clear(); gruppe_von.update(gv)
    raise RuntimeError("verteile kam nicht zur Ruhe")

verteile()

# --- neu nummerieren: oben links nach unten rechts ---
ids = [s for s in np.unique(M) if s > 0]
schwer = {s: ndi.center_of_mass(M == s) for s in ids}
reihen = sorted(ids, key=lambda s: (int(schwer[s][0] // 40), schwer[s][1]))
END = np.zeros((H, W), np.uint32)
segmente = []
x0, y0, x1, y1 = KERN
for neu_id, s in enumerate(reihen, 1):
    m = M == s
    END[m] = neu_id
    g = gruppe_von[s]
    kl, name, sicher, notiz = G[g]
    vor = Counter(L0[m].tolist())
    eintrag = {
        "id": neu_id, "klasse": kl, "grob": kl.split(".")[0], "name": name,
        "im_kern": bool(m[y0:y1, x0:x1].any()), "sicher": sicher,
        "flaeche": int(m.sum()), "flaeche_kern": int(m[y0:y1, x0:x1].sum()),
        "gruppe": g, "vorstufe": [100000 + v for v, _ in vor.most_common(6)],
    }
    if notiz:
        eintrag["notiz"] = notiz
    segmente.append(eintrag)
assert END.min() > 0

schreibe_labels(AUS + "/labels.tif", END)
json.dump({"segmente": segmente}, open(AUS + "/arbeit/segmente_roh.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)
print("Segmente", len(segmente), "im Kern", sum(e["im_kern"] for e in segmente))
print(Counter(e["klasse"] for e in segmente if e["im_kern"]))
