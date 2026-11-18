"""Schnittlinien aus dem Bild entwerfen: Umriss einer hellen/dunklen Fläche in einem Segment.

Aufruf: schnitte.py <spec.json> <eingriffe.json> <vorschau.jpg>
spec: {"schnitte": [{"id": 100075, "box": [x0, y0, x1, y1], "schwelle": 170, "art": "hell",
                    "glatt": 1.2, "name": "..."}], "fenster": [x, y, w, h], "f": 5}
Erzeugt je Schnitt einen geschlossenen Linienzug (op teilen) entlang des Umrisses der Fläche.
"""
import json
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

sys.path.insert(0, "C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r0c0/v1")
import werkzeug as w

spec = json.load(open(sys.argv[1], encoding="utf-8"))
lab, img, seg = w.lade()
schritte = []
linien = []
for s in spec["schnitte"]:
    if "linie" in s:
        schritte.append({"op": "teilen", "id": s["id"], "linie": s["linie"]})
        linien.append(s["linie"])
        continue
    g = ndimage.gaussian_filter(img, s.get("glatt", 1.2))
    x0, y0, x1, y1 = s["box"]
    box = np.zeros(lab.shape, bool)
    box[y0:y1 + 1, x0:x1 + 1] = True
    m = (lab == s["id"]) & box
    m &= (g > s["schwelle"]) if s.get("art", "hell") == "hell" else (g < s["schwelle"])
    m = ndimage.binary_opening(m, np.ones((2, 2), bool))
    l, k = ndimage.label(m)
    if k == 0:
        print("leer", s); continue
    groesse = np.bincount(l.ravel())[1:]
    m = l == (int(np.argmax(groesse)) + 1)
    m = ndimage.binary_fill_holes(ndimage.binary_closing(m, np.ones((3, 3), bool)))
    cs, _ = cv2.findContours(m.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    c = max(cs, key=cv2.contourArea)
    c = cv2.approxPolyDP(c, 0.8, True).reshape(-1, 2).tolist()
    c.append(c[0])
    schritte.append({"op": "teilen", "id": s["id"], "linie": c})
    linien.append(c)
    print(s.get("name", s["id"]), "Fläche", int(m.sum()), "Punkte", len(c))

json.dump({"schritte": schritte}, open(sys.argv[2], "w", encoding="utf-8"))
x, y, ww, hh = spec["fenster"]
f = spec.get("f", 5)
sub = img[y:y + hh, x:x + ww]
rgb = np.kron(np.stack([sub] * 3, -1).astype(np.uint8), np.ones((f, f, 1), np.uint8))
L = np.kron(lab[y:y + hh, x:x + ww], np.ones((f, f), np.int64))
r = np.zeros(L.shape, bool)
r[:, 1:] |= L[:, 1:] != L[:, :-1]
r[1:, :] |= L[1:, :] != L[:-1, :]
rgb[r] = (255, 230, 0)
im = Image.fromarray(rgb)
d = ImageDraw.Draw(im)
for c in linien:
    d.line([((px - x) * f + f // 2, (py - y) * f + f // 2) for px, py in c], fill=(255, 0, 255), width=2)
im.save(sys.argv[3], quality=90)
