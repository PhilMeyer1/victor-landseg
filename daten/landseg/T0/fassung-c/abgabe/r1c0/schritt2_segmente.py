"""Schritt 2: aus der Pixel-Klassifikation, Zonen von Hand und Regeln eine lückenlose Klassen- und Label-Karte.

Ergebnis: arbeit/klassen.npy (Klassencode-Index), arbeit/labels_roh.npy, arbeit/seg_roh.json und
ein Kontrollbild mit Nummern. Korrekturen je Segment folgen in schritt3_korrektur.py.
"""
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
from skimage.draw import polygon as poly_fill, line as draw_line
from skimage.morphology import disk, opening, closing

HIER = Path(__file__).parent
A = HIER / "arbeit"
H = W = 628
VIER = ndi.generate_binary_structure(2, 1)

pix = np.load(A / "pixel.npy")
proba = np.load(A / "proba.npy")
L = np.load(A / "L.npy")


def zone(pts):
    m = np.zeros((H, W), bool)
    rr, cc = poly_fill([p[1] for p in pts], [p[0] for p in pts], (H, W))
    m[rr, cc] = True
    return m


def modus(k, groesse=5, runden=2):
    for _ in range(runden):
        stapel = np.stack([ndi.uniform_filter((k == c).astype(float), groesse) for c in range(4)], -1)
        k = stapel.argmax(-1)
    return k


pix = modus(pix)

# Zonen (Koordinaten im Teilkachelbild, von Hand aus den Zoom-Bildern)
G = zone([(628, 385), (600, 393), (585, 412), (573, 430), (571, 520), (577, 560), (585, 600),
          (598, 628), (628, 628)])  # Kleingartenanlage (nur Kontextrand)
ACKER = zone([(560, 0), (628, 0), (628, 22), (600, 14), (585, 8), (560, 4)])  # Stoppelacker oben rechts

# Codes
CODES = ["1.1.1", "1.1.2", "1.1.3", "1.2", "1.3", "1.4", "2.1", "2.2", "2.3", "3.1", "3.2", "4.1",
         "5.1", "5.2"]
C = {c: i for i, c in enumerate(CODES)}
k = np.full((H, W), -1, int)

# Grundbelegung
holz = pix == 2
gras = pix == 0
beige = pix == 1
bau = pix == 3

# Bau-Pixel außerhalb der Gärten auf zweitbeste Klasse
if (bau & ~G).any():
    zweit = proba[..., :3].argmax(-1)
    holz |= bau & ~G & (zweit == 2)
    gras |= bau & ~G & (zweit == 0)
    beige |= bau & ~G & (zweit == 1)

# Garten
k[G & ~holz] = C["5.2"]  # Gehölz in den Gärten bleibt Gehölz
bg = bau & G
bg = opening(bg, disk(1))
lab_b, nb = ndi.label(bg, VIER)
for i in range(1, nb + 1):
    m = lab_b == i
    if m.sum() >= 25:
        k[m] = C["5.1"]
# Acker
k[ACKER & ~G & (beige | bau)] = C["3.2"]

frei = (k == -1)

# Schatten im Wald (außerhalb N): geglättete Helligkeit
Ls = ndi.gaussian_filter(L, 6)
D = holz & (Ls < 16.5) & frei
D = closing(opening(D, disk(3)), disk(4))
lab_d, nd = ndi.label(D, VIER)
groesse = ndi.sum(np.ones_like(lab_d), lab_d, range(1, nd + 1))
D = np.isin(lab_d, 1 + np.nonzero(groesse >= 1500)[0])

# Gehölz: Komponenten
lab_h, nh = ndi.label(holz & frei, VIER)
gh = ndi.sum(np.ones_like(lab_h), lab_h, range(1, nh + 1))
gross = 1 + int(np.argmax(gh))
wald = lab_h == gross
k[wald] = C["1.1.1"]
k[wald & D] = C["1.1.2"]
for i in range(1, nh + 1):
    if i == gross:
        continue
    m = lab_h == i
    a = int(m.sum())
    if a < 40:
        continue  # später den Nachbarn zuschlagen
    sl = ndi.find_objects(m.astype(int))[0]
    fuell = ndi.binary_fill_holes(m[sl])
    hh, ww = fuell.shape
    if a < 150:
        k[m] = C["1.4"]
    elif a <= 2600 and fuell.sum() / (hh * ww) > 0.45:
        k[m] = C["1.2"]
    else:
        k[m] = C["1.3"]

# Gras: Hauptwiese = größte Komponente mit Bildpunkten oben links
lab_g, ng = ndi.label(gras & frei & (k == -1), VIER)
for i in range(1, ng + 1):
    m = lab_g == i
    a = int(m.sum())
    if a < 60:
        continue
    k[m] = C["2.1"] if a > 3000 else C["2.2"]

# Beige: braun (dunkler) = offener Boden, hell = Trockengras/Streu
lab_y, ny = ndi.label(beige & frei & (k == -1), VIER)
for i in range(1, ny + 1):
    m = lab_y == i
    if m.sum() < 20:
        continue
    k[m] = C["3.1"]

# Pfade (von Hand nachgezeichnet, 3 px breit)
PFADE = {
    "pfad_haupt": [(492, 126), (489, 146), (490, 160), (498, 172), (503, 184), (507, 200), (509, 210)],
    "pfad_sued": [(526, 201), (550, 193), (568, 188), (580, 191), (588, 186)],
    "pfad_ost": [(553, 63), (560, 69), (572, 73)],
}
pfadmaske = {}
for name, pts in PFADE.items():
    m = np.zeros((H, W), bool)
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        rr, cc = draw_line(y0, x0, y1, x1)
        m[rr, cc] = True
    m = ndi.binary_dilation(m, disk(1))
    pfadmaske[name] = m
    k[m] = C["4.1"]

# Rest (-1) dem häufigsten Nachbarn zuschlagen
def fuellen(k):
    while (k == -1).any():
        offen = k == -1
        best = np.full((H, W), -1)
        bestz = np.zeros((H, W))
        for c in range(len(CODES)):
            z = ndi.uniform_filter((k == c).astype(float), 3)
            bess = (z > bestz) & offen
            best[bess] = c
            bestz[bess] = z[bess]
        k = np.where(offen & (best >= 0), best, k)
    return k

k = fuellen(k)
np.save(A / "klassen.npy", k)
json.dump({"codes": CODES}, open(A / "codes.json", "w"))
print({c: int((k == i).sum()) for c, i in C.items()})
