"""Trockenlauf eines Stapels im Speicher (schreibt nichts): meldet je Schritt das Ergebnis und ob
Bildpunkte außerhalb des eigenen Viertels oder des Kerns geändert würden.
Aufruf: python -B probe.py <eingriffe.json> <x0,y0,x1,y1 des Viertels, exklusiv>"""
import json
import sys

sys.path.insert(0, "C:/Users/Phil/Developement/Victor/landseg")
import numpy as np  # noqa: E402
from landseg import dateien, kategorien  # noqa: E402
from landseg.eingriff import Bearbeitung, EingriffFehler  # noqa: E402

H0 = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r0c0/"
sys.stdout.reconfigure(encoding="utf-8")
karte = dateien.lese_labels(H0 + "labels.tif")
seg = dateien.lese_segmente(H0 + "segmente.json")
kat = kategorien.laden(None) if False else kategorien.laden("C:/Users/Phil/Developement/Victor/landseg/kategorien.json")
arbeit = Bearbeitung(karte, seg, kat, "probe")
schritte = json.load(open(sys.argv[1], encoding="utf-8"))["schritte"]
x0, y0, x1, y1 = map(int, sys.argv[2].split(","))
ok = True
for nr, s in enumerate(schritte, 1):
    vor = arbeit.karte.copy()
    try:
        erg = arbeit.anwenden(s)
    except EingriffFehler as e:
        print(f"{nr}. {s['op']}: ABGELEHNT {e}")
        ok = False
        break
    diff = vor != arbeit.karte
    aussen = diff.copy()
    aussen[y0:y1, x0:x1] = False
    ids = sorted(set(np.unique(vor[diff]).tolist()))
    print(f"{nr}. {s['op']}: {json.dumps(erg, ensure_ascii=False)} | geändert {int(diff.sum())} px, "
          f"außerhalb Viertel {int(aussen.sum())} px, IDs vorher {ids}")
    if aussen.any():
        ok = False
        ys, xs = np.nonzero(aussen)
        print(f"   außerhalb: x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()}, IDs {sorted(set(np.unique(vor[aussen]).tolist()))}")
print("probe ok" if ok else "probe FEHLER")
