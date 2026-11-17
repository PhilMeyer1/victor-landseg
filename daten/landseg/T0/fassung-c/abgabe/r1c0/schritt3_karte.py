"""Schritt 3: Klassenkarte -> Segmente (zusammenhängend), Kleinstücke verschmelzen, Korrekturen,
Ausgabe labels.tif, segmente.json, Kontrollbilder.

Korrekturen werden über Saatpunkte (x, y) angegeben, damit sie nicht an laufenden Nummern hängen.
"""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi

HIER = Path(__file__).parent
A = HIER / "arbeit"
sys.path.insert(0, "C:/Users/Phil/Developement/Victor/landseg")
from landseg.dateien import schreibe_labels  # noqa: E402

H = W = 628
K0, K1 = 64, 564
VIER = ndi.generate_binary_structure(2, 1)
CODES = json.load(open(A / "codes.json"))["codes"]
C = {c: i for i, c in enumerate(CODES)}
k = np.load(A / "klassen.npy")
MIN = 30

# --- Klassen-Korrekturen vor der Segmentbildung: (x, y) -> Code für die ganze Komponente
UMKLASSE = json.load(open(HIER / "korrektur.json", encoding="utf-8")) if (HIER / "korrektur.json").exists() else {}


def komponenten(k):
    lab = np.zeros((H, W), np.int64)
    n = 0
    for c in range(len(CODES)):
        l, m = ndi.label(k == c, VIER)
        lab[l > 0] = l[l > 0] + n
        n += m
    return lab, n


for eintrag in UMKLASSE.get("klasse", []):
    x, y, code = eintrag["x"], eintrag["y"], eintrag["code"]
    lab, _ = komponenten(k)
    k[lab == lab[y, x]] = C[code]

for eintrag in UMKLASSE.get("flaeche", []):  # Rechteck/Polygon einer Klasse zuweisen
    from skimage.draw import polygon as pf
    pts = eintrag["punkte"]
    rr, cc = pf([p[1] for p in pts], [p[0] for p in pts], (H, W))
    m = np.zeros((H, W), bool)
    m[rr, cc] = True
    if "nur" in eintrag:
        m &= np.isin(k, [C[c] for c in eintrag["nur"]])
    k[m] = C[eintrag["code"]]

for eintrag in UMKLASSE.get("klasse_nach", []):  # Saatpunkt-Korrekturen nach den Flächen
    x, y, code = eintrag["x"], eintrag["y"], eintrag["code"]
    lab, _ = komponenten(k)
    k[lab == lab[y, x]] = C[code]

# --- kleine Lichtungen (2.2), die ganz von Gehölz umschlossen sind, sind besonnte Kronen: Gehölz
HOLZ = [C[c] for c in ("1.1.1", "1.1.2", "1.1.3")]
behalten = [tuple(p) for p in UMKLASSE.get("lichtung_behalten", [])]
lab, n = komponenten(k)
for sid in np.unique(lab[k == C["2.2"]]):
    m = lab == sid
    if m.sum() >= 1500 or any(m[y, x] for x, y in behalten):
        continue
    ring = ndi.binary_dilation(m, VIER) & ~m
    if np.isin(k[ring], HOLZ).mean() > 0.9:
        k[m] = C["1.1.1"]

# --- Kleinstücke verschmelzen (mit dem Nachbarn längster gemeinsamer Grenze)
for _ in range(6):
    lab, n = komponenten(k)
    flaeche = np.bincount(lab.ravel(), minlength=n + 1)
    klein = np.nonzero((flaeche < MIN) & (flaeche > 0))[0]
    if len(klein) == 0:
        break
    for sid in klein:
        m = lab == sid
        if not m.any():
            continue
        ring = ndi.binary_dilation(m, VIER) & ~m
        nb = k[ring]
        nb = nb[nb != k[m][0]] if (nb != k[m][0]).any() else nb
        k[m] = np.bincount(nb).argmax()

lab, n = komponenten(k)
# fortlaufend nummerieren, nach Lage (oben links zuerst)
ids = np.unique(lab)
mitte = ndi.center_of_mass(np.ones_like(lab), lab, ids)
reihen = sorted(zip(ids, mitte), key=lambda t: (int(t[1][0] // 40), t[1][1]))
neu = np.zeros(int(lab.max()) + 1, np.uint32)
for i, (sid, _) in enumerate(reihen, 1):
    neu[sid] = i
karte = neu[lab]
np.save(A / "karte.npy", karte)
np.save(A / "klassen_final.npy", k)
print("Segmente:", int(karte.max()))
