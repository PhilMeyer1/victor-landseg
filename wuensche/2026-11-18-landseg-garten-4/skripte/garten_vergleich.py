"""Beleg AK8 aus den Daten (ohne Browser): Hausgärten in T0 je Fassung. Für jedes Garten-Segment der Fassung C
(3.6) an einem Hauptgebäude (1.1.1) zählt, welche Klasse A und B an denselben Bildpunkten tragen; dazu je Fassung die
Garten-Segmente im zusammengetragenen Ausschnitt und ihr Flächenanteil. Aufruf: python garten_vergleich.py"""
import collections, json, sys
from pathlib import Path
import numpy as np
from scipy import ndimage
sys.path.insert(0, "C:/Users/Phil/Developement/Victor/landseg")
from landseg.dateien import lese_labels  # noqa: E402
G = Path("C:/Users/Phil/Developement/Victor/daten/gesamt/victor-landseg/ergebnisse")
H = Path("C:/Users/Phil/Developement/Victor/daten/landseg/H0")
FASS = {"A": ("a-alles-frei", "kategorien-a.json"), "B": ("b-kategorien-frei", "kategorien-b.json"), "C": ("c-feste-liste", "kategorien-c.json")}

def laden(basis, f):
    o, k = FASS[f]
    kl = {c["code"]: c for c in json.loads((basis / o / k).read_text(encoding="utf-8"))["classes"]}
    g = next(c for c, e in kl.items() if e["name"].startswith("Garten (") or e["name"] == "Garten")
    karte = lese_labels(basis / o / "zusammen/labels.tif")
    segs = {int(s["id"]): s for s in json.loads((basis / o / "zusammen/segmente.json").read_text(encoding="utf-8"))["segmente"]}
    klasse = np.vectorize(lambda i: segs.get(int(i), {}).get("klasse", ""), otypes=[object])
    ids = np.unique(karte)
    lut = {int(i): segs.get(int(i), {}).get("klasse", "") for i in ids}
    ist_garten = np.isin(karte, [i for i, c in lut.items() if c == g or c.startswith(g + ".")])
    return kl, g, karte, segs, lut, ist_garten

for name, basis in (("T0", G), ("H0", H)):
    daten = {f: laden(basis, f) for f in FASS}
    for f, (kl, g, karte, segs, lut, ist) in daten.items():
        n = sum(1 for i, c in lut.items() if c == g or c.startswith(g + "."))
        print(f"{name} {f}: Garten-Code {g}, Garten-Segmente im Ausschnitt {n}, Fläche {ist.mean() * 100:.2f} %")
    if name != "T0":
        continue
    kl, g, karte, segs, lut, istC = daten["C"]
    haus = np.isin(karte, [i for i, c in lut.items() if c == "1.1.1"])
    nahe = ndimage.binary_dilation(haus, iterations=3)
    am_haus = [i for i, c in lut.items() if c == "3.6" and (nahe & (karte == i)).any()]
    print(f"T0 C: Garten-Segmente an einem Hauptgebäude: {len(am_haus)}")
    for f in ("A", "B"):
        _, gf, _, _, _, istf = daten[f]
        m = np.isin(karte, am_haus)
        print(f"  dieselben Bildpunkte in {f}: Garten {istf[m].mean() * 100:.1f} %")
    groesste = sorted(am_haus, key=lambda i: -(karte == i).sum())[:3]
    for i in groesste:
        ys, xs = np.nonzero(karte == i)
        # Punkt im Segment nahe am Schwerpunkt
        k = np.argmin((ys - ys.mean()) ** 2 + (xs - xs.mean()) ** 2)
        y, x = int(ys[k]), int(xs[k])
        zeile = [f"T0 Beispiel x {x}, y {y}:"]
        for f, (klf, gf, kf, sf, lf, _) in daten.items():
            sid = int(kf[y, x]); c = lf[sid]
            zeile.append(f"{f} {c} „{klf[c]['name'][:20]}“ unter „{klf[klf[c]['parent']]['name'][:14] if klf[c].get('parent') else '-'}“")
        print("  " + " | ".join(zeile))
