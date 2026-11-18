"""Exaktes Polygon für das Straßenband (nur Bildpunkte von 143/183) nach den ersten zwei Schritten
von eingriffe2.json, ohne Reststücke abzuschneiden; schreibt den fertigen Stapel eingriffe2.json neu.
Nur Lesen der Karte, Rechnen im Speicher."""
import json
import sys

sys.path.insert(0, "C:/Users/Phil/Developement/Victor/landseg")
import cv2  # noqa: E402
import numpy as np  # noqa: E402
from scipy import ndimage  # noqa: E402
from landseg import dateien, kategorien  # noqa: E402
from landseg.eingriff import Bearbeitung  # noqa: E402

H0 = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r0c0/"
schritte = json.load(open("eingriffe2.json", encoding="utf-8"))["schritte"][:2]
arbeit = Bearbeitung(dateien.lese_labels(H0 + "labels.tif"), dateien.lese_segmente(H0 + "segmente.json"),
                     kategorien.laden("C:/Users/Phil/Developement/Victor/landseg/kategorien.json"), "probe")
for s in schritte:
    arbeit.anwenden(s)
L = arbeit.karte.astype(np.int64)
road = [[470, 338], [470, 348], [472, 356], [477, 364], [477, 372], [474, 380], [475, 388], [478, 394], [489, 398],
        [493, 398], [492, 392], [489, 386], [488, 380], [489, 372], [488, 364], [485, 356], [479, 348], [476, 340], [474, 336]]
pm = np.zeros(L.shape, np.uint8)
cv2.fillPoly(pm, [np.array(road, np.int32)], 1)
quelle = np.isin(L, [100143, 100183])
m = pm.astype(bool) & quelle
for sid in (100143, 100183):
    rest = (L == sid) & ~m
    t, n = ndimage.label(rest, structure=[[0, 1, 0], [1, 1, 1], [0, 1, 0]])
    if n > 1:
        gr = np.bincount(t.ravel())[1:]
        g = int(np.argmax(gr)) + 1
        for i in range(1, n + 1):
            if i != g:
                print(f"{sid}: Reststück {int(gr[i - 1])} px zur Straße genommen")
                m |= t == i
cs, _ = cv2.findContours(m.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
print(len(cs), "Konturen", [int(cv2.contourArea(c)) for c in cs])
c = max(cs, key=cv2.contourArea)
poly = c[:, 0, :].tolist()
probe = np.zeros(L.shape, np.uint8)
cv2.fillPoly(probe, [np.array(poly, np.int32)], 1)
fremd = probe.astype(bool) & ~quelle & (L != 100198)
print("fremde Bildpunkte im Polygon:", int(fremd.sum()), sorted(set(np.unique(L[fremd]).tolist())))
alle = json.load(open("eingriffe2.json", encoding="utf-8"))["schritte"][:2]
alle.append({"op": "polygon_zuweisen", "flaeche": poly, "id": 100198})
json.dump({"schritte": alle}, open("eingriffe2.json", "w", encoding="utf-8"))
