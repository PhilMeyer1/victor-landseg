"""Stapel planen: Schnitte aus spec (wie schnitte.py) im Speicher anwenden, Splitter (< 30 px)
automatisch mit dem angrenzenden Teil verschmelzen und den ganzen Stapel als eine Datei schreiben.
Die Karte auf der Platte bleibt unberührt.

Aufruf (im Ordner landseg): planer.py <spec.json> <eingriffe.json> <vorschau.jpg>
"""
import json
import subprocess
import sys

import numpy as np
from scipy import ndimage

sys.path.insert(0, "C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r0c0/v1")
sys.path.insert(0, "C:/Users/Phil/Developement/Victor/landseg")
import werkzeug as w
from landseg import dateien, kategorien
from landseg.eingriff import Bearbeitung

spec_pfad, ziel, vorschau = sys.argv[1:4]
entwurf = ziel + ".entwurf.json"
subprocess.run([sys.executable, "-B", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r0c0/v1/schnitte.py",
                spec_pfad, entwurf, vorschau], check=True)
schritte = json.load(open(entwurf, encoding="utf-8"))["schritte"]
spec = json.load(open(spec_pfad, encoding="utf-8"))["schnitte"]
neu_zu = {s["id"]: s["neu_zu"] for s in spec if "neu_zu" in s}
karte = dateien.lese_labels(w.LABELS) if hasattr(dateien, "lese_labels") else None
import tifffile
karte = tifffile.imread(w.LABELS).astype(np.uint32)
seg = dateien.lese_segmente(w.SEG)
arbeit = Bearbeitung(karte, seg, kategorien.laden(None), "planer")
alle = []
for s in schritte:
    vor = arbeit.karte.copy()
    e = arbeit.anwenden(s)
    alle.append(s)
    teile = [e["behalten"]] + e["neu"]
    groesse = {t: int((arbeit.karte == t).sum()) for t in teile}
    gross = [t for t in teile if groesse[t] >= 30]
    for t in teile:
        if groesse[t] >= 30:
            continue
        m = arbeit.karte == t
        rand = ndimage.binary_dilation(m, np.ones((3, 3), bool)) & ~m
        nb, cnt = np.unique(arbeit.karte[rand], return_counts=True)
        best = None
        for n, c in sorted(zip(nb.tolist(), cnt.tolist()), key=lambda z: -z[1]):
            if n in gross:
                best = n; break
        if best is None:
            best = max(gross, key=lambda g: groesse[g])
        v = {"op": "verschmelzen", "ids": [best, t]}
        try:
            arbeit.anwenden(v)
        except Exception as fehler:  # nicht benachbart: an den größten Nachbarn im Segment
            print("Splitter", t, "nicht verschmelzbar mit", best, fehler)
            continue
        alle.append(v)
    if s["id"] in neu_zu:
        rest = [t for t in e["neu"] if (arbeit.karte == t).any()]
        groesst = max(rest, key=lambda t: int((arbeit.karte == t).sum()))
        v = {"op": "verschmelzen", "ids": [neu_zu[s["id"]], groesst]}
        arbeit.anwenden(v)
        alle.append(v)
        print("  verschmolzen", v)
    print(s["id"], {t: int((arbeit.karte == t).sum()) for t in teile if (arbeit.karte == t).any()})
json.dump({"schritte": alle}, open(ziel, "w", encoding="utf-8"))
print("Schritte", len(alle))
