"""Grauwerte der Segmente nahe der Stelle (nur lesen)."""
import numpy as np
import tifffile
from PIL import Image

H0 = "C:/Users/Phil/Developement/Victor/daten/landseg/H0"
img = np.array(Image.open(H0 + "/H0.png").convert("L")).astype(np.float32)
lab = tifffile.imread(H0 + "/b-kategorien-frei/zusammen/labels.tif")

PAARE = [
    (100202, 300001, 0, 28, 500), (100221, 300001, 29, 37, 500), (100223, 300001, 31, 42, 500),
    (100223, 300002, 43, 43, 500), (100224, 300002, 296, 297, 500), (100224, 300073, 298, 310, 500),
    (100220, 300073, 311, 332, 500), (100225, 300073, 333, 333, 500), (100225, 300070, 334, 339, 500),
    (100195, 300070, 340, 345, 500),
]
for a, b, x0, x1, y in PAARE:
    for i in (a, b):
        m = lab == i
        print(i, "gesamt mittel %.0f sd %.0f" % (img[m].mean(), img[m].std()), end="  ")
    # Band 6 px ober- und unterhalb der Naht an der Stelle
    o = img[y - 6:y, x0:x1 + 1]
    u = img[y:y + 6, x0:x1 + 1]
    print("| oben je Zeile", [int(v) for v in o.mean(1)], "unten je Zeile", [int(v) for v in u.mean(1)])

# Viertel r0c1 (Kern x 500-999): senkrechte Viertellinie bei x 750
for a, b, y0, y1 in [(200025, 200219, 50, 50), (200192, 200211, 119, 122)]:
    for i in (a, b):
        m = lab == i
        print(i, "gesamt mittel %.0f sd %.0f" % (img[m].mean(), img[m].std()), end="  ")
    l = img[y0:y1 + 1, 744:750]
    r = img[y0:y1 + 1, 750:756]
    print("| links je Spalte", [int(v) for v in l.mean(0)], "rechts je Spalte", [int(v) for v in r.mean(0)])
    print("   Labels links", lab[y0, 744:750].tolist(), "rechts", lab[y0, 750:756].tolist())
