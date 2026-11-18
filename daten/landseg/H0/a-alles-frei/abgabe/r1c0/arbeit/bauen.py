"""Label-Karte r1c0 (Fassung A) aus Linienzuegen, Polygonen und Bildschwellen bauen.

Malreihenfolge: spaetere Flaechen ueberschreiben fruehere. Danach Bereinigung (jede ID
zusammenhaengend, Splitter zum haeufigsten Nachbarn).
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage as ndi
from skimage.draw import polygon as skpoly

ORDNER = Path(r"C:/Users/Phil/Developement/Victor/daten/landseg/H0/a-alles-frei/abgabe/r1c0")
BILD = Path(r"C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r1c0.png")
H = W = 628
K0, K1 = 64, 564  # Kern [K0, K1)

b = np.array(Image.open(BILD)).astype(float)
if b.ndim == 3:
    b = b[..., 0]
g1 = ndi.gaussian_filter(b, 1.2)
g4 = ndi.gaussian_filter(b, 4)
Y, X = np.mgrid[0:H, 0:W]
d_str = np.array([0.81231158, -0.58322371])
n_str = np.array([0.58322371, 0.81231158])
U = X * n_str[0] + Y * n_str[1]  # Lage quer zur Strasse (Streifenflur)


def poly(pts):
    m = np.zeros((H, W), bool)
    p = np.array(pts, float)
    rr, cc = skpoly(p[:, 1], p[:, 0], (H, W))
    m[rr, cc] = True
    return m


def linie(pts, hw):
    """Band der halben Breite hw um einen Linienzug (Abstand zum Polygonzug)."""
    m = np.zeros((H, W), bool)
    p = np.array(pts, float)
    for (x0, y0), (x1, y1) in zip(p[:-1], p[1:]):
        n = int(max(abs(x1 - x0), abs(y1 - y0)) * 3) + 2
        xs = np.linspace(x0, x1, n)
        ys = np.linspace(y0, y1, n)
        xi = np.clip(np.round(xs).astype(int), 0, W - 1)
        yi = np.clip(np.round(ys).astype(int), 0, H - 1)
        m[yi, xi] = True
    dist = ndi.distance_transform_edt(~m)
    return dist <= hw


def interp_x(pts, y):
    p = np.array(pts, float)
    return np.interp(y, p[:, 1], p[:, 0])


def interp_y(pts, x):
    p = np.array(pts, float)
    return np.interp(x, p[:, 0], p[:, 1])


def hell_im_band(pts, hw, rand=6, anteil=0.5):
    """Helle Linie (Weg) im Band: Schwelle zwischen Mitte und Umgebung."""
    band = linie(pts, hw)
    mitte = linie(pts, max(1.5, hw / 3))
    ring = linie(pts, hw + rand) & ~band
    innen = np.median(g1[mitte])
    aussen = np.median(g1[ring])
    thr = aussen + anteil * (innen - aussen)
    m = band & (g1 > thr)
    m = ndi.binary_closing(m, iterations=2) & band
    m = ndi.binary_opening(m, iterations=1)
    m = ndi.binary_fill_holes(m | mitte) & band
    return m, (round(innen), round(aussen), round(thr))


def groesste(m):
    lab, n = ndi.label(m)
    if n == 0:
        return m
    gr = ndi.sum(m, lab, range(1, n + 1))
    return lab == (1 + int(np.argmax(gr)))


def dunkler_fleck(x0, y0, x1, y1, delta=25, sigma=1.2):
    """Dunkler, kompakter Fleck im Kasten: deutlich unter dem Kastenmedian."""
    box = np.zeros((H, W), bool)
    box[y0:y1, x0:x1] = True
    gg = ndi.gaussian_filter(b, sigma)
    thr = np.median(gg[box]) - delta
    m = box & (gg < thr)
    m = groesste(m)
    m = ndi.binary_dilation(m, iterations=1) & box
    return ndi.binary_fill_holes(m)


# ---------------------------------------------------------------- Linien
STRASSE = [(0, 489.5), (20, 472.5), (40, 455.5), (60, 439), (80, 422.5), (100, 407.5), (120, 388.5),
           (140, 372.5), (160, 355), (180, 337.5), (200, 320.5), (220, 305), (240, 288.5), (260, 273.5),
           (280, 259), (300, 246), (320, 232.5), (340, 219.5), (360, 206), (380, 193), (400, 181),
           (420, 167.5), (440, 154), (460, 142), (480, 128.5), (500, 116), (520, 103), (540, 90.5),
           (560, 78.5), (577, 72), (595, 76), (612, 80), (628, 84)]
STRASSE_N = [(580, 0), (579, 30), (577, 72)]
SEITENWEG = [(0, 203), (12, 222), (30, 245), (50, 268), (62, 288), (75, 302), (100, 307),
             (150, 310), (185, 311), (198, 316)]
HOFWEG = [(360, 0), (367, 23), (380, 45), (390, 60), (398, 72), (404, 85), (410, 97), (418, 110),
          (428, 125), (437, 138), (447, 151)]
L1 = [(183, 118), (192, 150), (203, 173), (213, 193), (227, 220), (237, 240), (250, 266)]
L2 = [(97, 0), (102, 40), (110, 83), (118, 120), (124, 145)]
L3 = [(216, 322), (230, 350), (257, 400), (277, 443), (290, 467), (300, 493), (312, 510), (330, 550),
      (347, 587), (357, 613), (364, 628)]
L4 = [(401, 182), (410, 213), (430, 253), (450, 290), (463, 317), (477, 343), (490, 367), (503, 393),
      (517, 423), (530, 450), (547, 487), (563, 513), (577, 540), (590, 567), (605, 600), (617, 628)]
GRABEN = [(447, 128), (475, 113), (500, 99), (525, 86), (550, 73)]
GRABEN2 = [(415, 95), (440, 88), (476, 71), (490, 64), (515, 52), (540, 42)]
SPUR_SW = [(107, 467), (140, 440), (173, 413)]

road_y = interp_y(STRASSE, X)
nw_strasse = Y < road_y
se_strasse = ~nw_strasse
l1_x = interp_x(L1, Y)
l3_x = interp_x(L3, Y)
l4_x = interp_x(L4, Y)

# ---------------------------------------------------------------- Segmentliste
# (schluessel, klasse, name, sicher, grund)
SEG = {}
karte = np.zeros((H, W), np.int32)
reihen = []


def malen(schl, maske, klasse, name, sicher=True, grund=""):
    if schl not in SEG:
        SEG[schl] = dict(nr=len(SEG) + 1, klasse=klasse, name=name, sicher=sicher, grund=grund)
    karte[maske] = SEG[schl]["nr"]


# 1 Grundflaechen SE der Strasse (Streifenflur)
fsw = se_strasse & (X < l3_x)
fmid = se_strasse & (X >= l3_x) & (X < l4_x)
fost = se_strasse & (X >= l4_x)
malen("fsw", fsw, "3.1.2", "Feld SW der Straße, mittelgrau",
      False, "Acker oder Grünland auf SW nicht trennbar")
malen("fmid_d", fmid & (U < 456), "3.1.1", "Feldstreifen dunkel an der Straße",
      False, "dunkler Streifen: dichter Bestand oder feuchter Boden; Acker/Grünland offen")
BAND = [(200, 609), (340, 545), (380, 526), (450, 495), (505, 470), (525, 460), (640, 407)]
band_y = interp_y(BAND, X)
band = fmid & linie(BAND, 8)
malen("fmid_m1", fmid & (U >= 456) & (Y < band_y), "3.1.2", "Feldstreifen mittelgrau",
      False, "Acker oder Grünland auf SW nicht trennbar; schwacher dunkler Streifen u≈606–630 nicht abgetrennt")
malen("fmid_m2", fmid & (U >= 456) & (Y >= band_y), "3.1.2", "Feldstreifen mittelgrau, fleckig",
      False, "Acker oder Grünland auf SW nicht trennbar")
malen("fmid_h", band, "3.1.3", "schmaler heller Feldstreifen",
      False, "heller Streifen ~7 m: offener Boden, Stoppel oder Rain; Grenzen weich, geschätzt")
malen("fost_n", fost & (U < 538), "3.1.2", "Feld östlich Rain, nördlich hellem Streifen",
      False, "Acker oder Grünland auf SW nicht trennbar")
malen("fost_s", fost & (U >= 538), "3.1.2", "Feld östlich Rain, südlich hellem Streifen",
      False, "Acker oder Grünland auf SW nicht trennbar")

# 2 Grundflaechen NW der Strasse
malen("a5", nw_strasse, "3.1.2", "Feld West (Streifen schräg), mittelgrau",
      False, "Acker oder Grünland auf SW nicht trennbar; schräge Streifung")
a6 = poly(SEITENWEG + [(200, 330), (150, 372), (100, 415), (50, 455), (0, 495)]) & nw_strasse
malen("a6", a6, "3.1.2", "Feld zwischen Seitenweg und Straße",
      False, "Acker oder Grünland auf SW nicht trennbar")
a6d = a6 & poly([(0, 326), (30, 318), (80, 314), (96, 322), (108, 345), (112, 370), (105, 398),
                  (86, 423), (62, 442), (30, 452), (0, 455)])
malen("a6d", a6d, "3.1.1", "Feld dunkel zwischen Seitenweg und Straße",
      False, "sehr dunkel und gestreift: dichter Bestand (Getreide, Mais, Klee?) oder junge Gehölzpflanzung")
a4 = poly([(0, 0), (97, 0), (102, 40), (110, 83), (118, 120), (124, 145), (90, 150), (40, 150), (0, 145)])
malen("a4", a4, "3.2", "helle Fläche West (Brache/Ödland)",
      False, "heller, fleckiger Grund mit dunklen Flecken im Kontext: Brache, Weide oder Abbau; im Kern nur Rand")
a3 = poly([(97, 0), (362, 0), (400, 70), (330, 95), (300, 104), (288, 100), (250, 106), (210, 110),
           (183, 118), (184, 130), (128, 135), (124, 145), (118, 120), (110, 83), (102, 40)])
malen("a3", a3, "3.1.1", "Feld Nord, dunkel",
      False, "dunkler, gleichmäßiger Bestand; Acker oder Grünland offen")
f15 = poly([(183, 118), (210, 110), (250, 106), (288, 100), (300, 104), (330, 95), (400, 70),
            (447, 151)] + [(x, interp_y(STRASSE, x)) for x in range(447, 249, -10)] + [(250, 266)]
           + L1[::-1]) & nw_strasse & (X > l1_x - 1)
malen("f15", f15, "3.1.2", "Feld zwischen Rain und Hofweg, mittelgrau",
      False, "Acker oder Grünland auf SW nicht trennbar")
fne_a = poly([(412, 96), (440, 88), (476, 71), (490, 64), (515, 52), (540, 42), (548, 45), (560, 72),
              (577, 72)] + [(x, interp_y(STRASSE, x)) for x in range(570, 446, -8)] + [(447, 151)]
             + HOFWEG[::-1][:5]) & nw_strasse
malen("fne_a", fne_a, "3.1.2", "Feldstreifen nördlich der Straße, Ost",
      False, "Acker oder Grünland auf SW nicht trennbar")
fne_b = poly([(362, 0), (538, 0), (540, 42), (515, 52), (490, 64), (476, 71), (440, 88), (412, 96),
              (400, 70)])
malen("fne_b", fne_b, "3.1.1", "Feld Nordost, dunkel (fast nur Kontext)",
      False, "Acker oder Grünland auf SW nicht trennbar")
ecke = poly([(538, 0), (628, 0), (628, 64), (600, 66), (585, 74), (566, 77), (552, 76), (548, 45), (540, 42)])
malen("ecke", ecke, "2", "Ortsrand Nordost: Gebäude, Schatten, Gärten (Kontext)",
      False, "im Kern nur der dunkle Rand (Gebäude oder Schatten); Rest Kontext, nicht einzeln geteilt")

# 3 A1/A2: helle Flaeche mit Gehoelz west von L1 (Bildschwelle auf g4)
w_l1 = nw_strasse & (X < l1_x - 3.5)
a1_zone = w_l1 & poly([(122, 128), (190, 120), (215, 200), (240, 255), (238, 300), (190, 304), (175, 250),
                       (140, 225), (118, 170)])
ref = np.median(g4[w_l1 & ~a1_zone & (Y > 140) & (Y < 300)])
print("A5 Median g4", round(ref))
hell = a1_zone & (g4 > ref + 14)
hell = ndi.binary_opening(ndi.binary_closing(hell, iterations=3), iterations=2)
lab, n = ndi.label(hell)
gr = ndi.sum(hell, lab, range(1, n + 1))
ordn = np.argsort(gr)[::-1]
print("A1/A2 Komponenten", [int(gr[i]) for i in ordn[:5]])
a1 = ndi.binary_fill_holes(lab == ordn[0] + 1)
a2 = ndi.binary_fill_holes(lab == ordn[1] + 1) if n > 1 else np.zeros_like(a1)
if a2.sum() < 150:
    a2[:] = False
# A1 oben, A2 unten (nach Schwerpunkt)
if a2.any() and ndi.center_of_mass(a2)[0] < ndi.center_of_mass(a1)[0]:
    a1, a2 = a2, a1
malen("a1", a1, "3.2", "helle fleckige Fläche mit Gehölz (Brache/Ödland)",
      False, "hell, unruhig, mit dunklen Flecken: Brache, Hutweide oder alte Gruben; im Farbbild/Gelände zu klären")
if a2.any():
    malen("a2", a2, "3.2", "helle Fläche am Rain (Brache/Ödland)",
          False, "hell, unruhig: Brache oder offener Boden")
a5d = w_l1 & ~a1 & ~a2 & poly([(140, 240), (168, 236), (192, 245), (196, 280), (196, 306), (170, 308),
                                (150, 302), (135, 275)])
malen("a5d", a5d, "3.1.1", "dunkler Feldteil West am Seitenweg",
      False, "dunkler als die Umgebung; Grenze weich, geschätzt")

# 4 helle Flecken in Feldern (Bildschwelle)
def helle_flecken(zone, delta, min_px, schl, name, grund):
    ref = np.median(g4[zone])
    m = zone & (g4 > ref + delta)
    m = ndi.binary_opening(ndi.binary_closing(m, iterations=2), iterations=2)
    lab, n = ndi.label(m)
    k = 0
    for i in range(1, n + 1):
        mm = ndi.binary_fill_holes(lab == i)
        if mm.sum() >= min_px:
            k += 1
            malen(f"{schl}{k}", mm, "3.1.3", name, False, grund)
    print(schl, "ref", round(ref), "Flecken", k)


fsw_rest = fsw & (karte == SEG["fsw"]["nr"])
helle_flecken(fsw_rest & (U > 470), 12, 250, "fsw_h", "heller Fleck im Feld SW",
              "heller, unregelmäßiger Fleck: offener Boden, Stoppel oder lückiger Bestand")
helle_flecken(fost & (U >= 575) & (U < 650), 14, 120, "fost_h", "heller Fleck im Feld Ost",
              "heller Fleck: offener Boden oder Kalk-/Sandstelle")

# 5 Hof
bright = poly([(285, 122), (295, 108), (308, 101), (320, 92), (330, 88), (337, 100), (345, 106), (355, 104),
               (362, 112), (363, 123), (357, 128), (348, 134), (337, 139), (320, 148), (308, 152),
               (298, 147), (288, 138)])
malen("hof_hell", bright, "2.2", "helle Hof-/Lagerfläche mit Haufen",
      False, "sehr hell, körnig, streifig: Schutt, Sand, Mist oder Stroh; offener Boden möglich")
yard = poly([(350, 106), (362, 100), (372, 97), (388, 96), (398, 92), (404, 100), (406, 112), (395, 118),
             (380, 120), (365, 124), (360, 114)])
malen("hof_grau", yard, "2.2", "Hoffläche grau zwischen Gebäude und Weg",
      False, "heller als das Feld, glatt: Hof oder Vorplatz; Belag offen")
geb = poly([(334, 82), (342, 70), (352, 64), (366, 62), (373, 64), (373, 82), (371, 96), (360, 100),
            (346, 105), (337, 100), (333, 92)])
malen("geb", geb, "2.1", "Gebäude am Hof (dunkles Dach)",
      False, "dunkles Rechteck mit hellem Fleck; Dach oder Gehölz nicht sicher trennbar")
schatten = poly([(370, 56), (386, 52), (398, 60), (401, 74), (398, 90), (390, 97), (376, 98), (372, 82)])
malen("schatten", schatten, "5.1", "sehr dunkle Fläche östlich Gebäude",
      False, "fast schwarz: Schlagschatten des Gebäudes oder dichte Baumkrone")

# 6 Wege und Strassen (Bildschwelle im Band)
s_band = linie(STRASSE, 11) | linie(STRASSE_N, 11)
ref_s = np.median(g1[linie(STRASSE, 2)])
thr_s = 0.5 * (ref_s + np.median(g1[linie(STRASSE, 18) & ~linie(STRASSE, 11)]))
strasse = s_band & (g1 > thr_s)
strasse = ndi.binary_opening(ndi.binary_closing(strasse, iterations=2), iterations=1)
strasse = groesste(ndi.binary_fill_holes(strasse | linie(STRASSE, 2)))
print("Strasse thr", round(thr_s))

weg, info = hell_im_band(SEITENWEG, 7)
print("Seitenweg", info)
hofweg, info = hell_im_band(HOFWEG, 9)
print("Hofweg", info)
s_zone = fost & (U > 505) & (U < 572) & (X > l4_x + 3)
ref_sz = np.median(g4[fost & (U > 470) & (U < 505)])
streifen = s_zone & (g1 > ref_sz + 0.45 * (np.percentile(g1[s_zone], 90) - ref_sz))
streifen = ndi.binary_opening(ndi.binary_closing(streifen, iterations=3), iterations=2)
streifen = groesste(ndi.binary_fill_holes(streifen))
malen("streifen", streifen, "3.1.3", "heller breiter Streifen parallel zur Straße",
      False, "sehr hell, ~12 m breit: Stoppel-/Brachstreifen oder breiter Erdweg; im Farbbild/Höhe klären")
malen("l1", linie(L1, 5.5) & nw_strasse, "1.2", "schmaler Feldweg mit Gräben (Doppellinie)",
      False, "zwei dunkle Linien mit heller Mitte: Grasweg zwischen Gräben oder Rain mit Hecke")
malen("l2", linie(L2, 2.5), "4.2", "Rain/Graben West (dunkle Linie)",
      False, "dunkle Linie: Graben oder Rain")
malen("l3", linie(L3, 4) & se_strasse, "1.2", "schmaler Feldweg/Rain West",
      False, "helle Mitte, dunkle Ränder: Grasweg oder Rain mit Gräben")
malen("l4", linie(L4, 4) & se_strasse, "1.2", "schmaler Feldweg/Rain Ost",
      False, "helle Mitte, dunkle Ränder: Grasweg oder Rain mit Gräben")
malen("graben", linie(GRABEN, 2.5) & nw_strasse, "4.2", "Graben/Hecke nördlich der Straße",
      False, "dunkle Linie parallel zur Straße: Straßengraben oder Hecke")
malen("graben2", linie(GRABEN2, 3), "4.2", "Graben/Hecke Feldgrenze Nordost",
      False, "dunkle Linie: Graben oder Hecke")
malen("spur", linie(SPUR_SW, 3) & fsw, "1.2", "helle Spur im Feld SW",
      False, "schwache helle Linie: Fahrspur, Rain oder Bewirtschaftungsgrenze")
malen("hofweg", hofweg, "1.2", "Zufahrtsweg zum Hof", True, "")
malen("seitenweg", weg, "1.2", "Feldweg West (unbefestigt)", True, "")
malen("strasse", strasse, "1.1", "Landstraße", True, "Belag (Schotter/Asphalt) auf SW offen")

# 7 dunkle Einzelobjekte
for schl, box, name, kl, grund in [
    ("geh0", (88, 114, 104, 132), "dunkler Fleck in heller Fläche West", "4.1", "dunkler Fleck: Strauch, Baum oder Grube"),
    ("geh1", (160, 158, 178, 182), "Gehölz/Grube 1 in heller Fläche", "4.1", "dunkler Fleck: Strauch, Baum oder Grube mit Schatten"),
    ("geh2", (174, 174, 192, 190), "Gehölz/Grube 2 in heller Fläche", "4.1", "dunkler Fleck: Strauch, Baum oder Grube mit Schatten"),
    ("geh3", (188, 208, 212, 230), "Gehölzgruppe in heller Fläche", "4.1", "dunkle Flecken: Sträucher oder Gruben"),
    ("obj_s", (548, 262, 574, 286), "dunkles Objekt im hellen Streifen", "5.2", "klein, länglich: Heuhaufen, Fuhrwerk oder Gerät"),
    ("obj_r", (98, 380, 122, 400), "dunkles Objekt am Straßenrand", "5.2", "klein, dunkel: Baum, Strauch oder Fahrzeug"),
]:
    m = dunkler_fleck(*box, delta=22)
    print(schl, int(m.sum()))
    malen(schl, m, kl, name, False, grund)

np.save(ORDNER / "arbeit" / "karte_roh.npy", karte)
json.dump(SEG, open(ORDNER / "arbeit" / "seg_roh.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("Segmente roh", len(SEG), "Luecken", int((karte == 0).sum()))
