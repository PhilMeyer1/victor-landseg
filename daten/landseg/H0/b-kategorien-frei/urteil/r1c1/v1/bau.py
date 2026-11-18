"""Stapel bauen: Linien über Wegpunkte folgen dem dunkelsten Weg im Bild (Kante), Ziel-ID je Linie
aus der Familie des Ausgangssegments; simuliert alles im Speicher und schreibt die Stapeldatei.

PY -B bau.py --plan plan.json --aus eingriffe_entwurf.json [--basis-stapel vorher.json]
plan.json: {"schritte": [ {"art": "linie", "familie": 400006, "punkte": [[x,y],...], "dunkel": true},
                          {"art": "roh", "schritt": {...Stapelschritt...}} ]}
"dunkel": true -> Weg über dunkle Pixel (Schattenlinie); "hell": Weg über helle Pixel; "gerade": Wegpunkte direkt.
"""
import argparse
import json
import sys

import numpy as np
from PIL import Image
from skimage import filters, graph

sys.path.insert(0, "C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c1/v1")
sys.path.insert(0, "C:/Users/Phil/Developement/Victor/landseg")
import werkzeug as wz  # noqa: E402
from landseg import dateien, kategorien  # noqa: E402
from landseg.eingriff import Bearbeitung, EingriffFehler  # noqa: E402


def weg(g, p, q, modus, rand=4):
    if modus == "gerade":
        return [list(p), list(q)]
    x0, x1 = max(min(p[0], q[0]) - rand, 0), min(max(p[0], q[0]) + rand + 1, g.shape[1])
    y0, y1 = max(min(p[1], q[1]) - rand, 0), min(max(p[1], q[1]) + rand + 1, g.shape[0])
    sub = g[y0:y1, x0:x1] / 255.0
    kosten = (sub ** 2 if modus == "dunkel" else (1 - sub) ** 2) + 0.12
    pfad, _ = graph.route_through_array(kosten, (p[1] - y0, p[0] - x0), (q[1] - y0, q[0] - x0),
                                        fully_connected=True, geometric=True)
    return [[int(c + x0), int(r + y0)] for r, c in pfad]


def verlaengern(pts, karte, fam, maxl):
    """Beide Enden in Linienrichtung verlängern, bis die Familie verlassen ist (im Kern)."""
    pts = [list(p) for p in pts]
    for ende in (0, -1):
        a = np.array(pts[ende], float)
        b = np.array(pts[1 if ende == 0 else -2], float)
        r = a - b
        r /= max(np.linalg.norm(r), 1e-6)
        q = a.copy()
        aussen = 0
        for _ in range(maxl):
            q = q + r
            x, y = int(round(q[0])), int(round(q[1]))
            if not (64 <= x < 564 and 64 <= y < 564):
                break
            if karte[y, x] in fam:
                aussen = 0
            else:
                aussen += 1
                if aussen >= 2:
                    break
        neu = [int(round(q[0])), int(round(q[1]))]
        neu = [min(max(neu[0], 64), 563), min(max(neu[1], 64), 563)]
        if ende == 0:
            pts.insert(0, neu)
        else:
            pts.append(neu)
    return pts


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--plan", required=True)
    ap.add_argument("--aus", required=True)
    ap.add_argument("--basis-stapel")
    a = ap.parse_args()
    img = np.asarray(Image.open(wz.BILD).convert("L")).astype(np.float32)
    g = filters.gaussian(img, 1.0, preserve_range=True)
    karte = dateien.lese_labels(wz.LABELS)
    seg = dateien.lese_segmente(wz.SEGM)
    start = karte.copy()
    arb = Bearbeitung(karte, seg, kategorien.laden(None), "sim")
    schritte_aus = []
    if a.basis_stapel:
        for s in json.load(open(a.basis_stapel, encoding="utf-8"))["schritte"]:
            arb.anwenden(s)
            schritte_aus.append(s)
    familie = {}
    plan = json.load(open(a.plan, encoding="utf-8"))["schritte"]
    linien_bild = []
    for nr, s in enumerate(plan, 1):
        if s["art"] == "roh":
            try:
                erg = arb.anwenden(s["schritt"])
            except EingriffFehler as e:
                print(f"P{nr} roh FEHLER: {e}")
                continue
            schritte_aus.append(s["schritt"])
            print(f"P{nr} roh {s['schritt']['op']}: {erg}")
            continue
        fam = familie.setdefault(s["familie"], {s["familie"]})
        pts = s["punkte"]
        pts = verlaengern(pts, arb.karte, fam, s.get("verl", 25))
        lz = []
        for p, q in zip(pts[:-1], pts[1:]):
            teil = weg(g, p, q, s.get("modus", "dunkel"))
            lz.extend(teil if not lz else teil[1:])
        # verdichteten Weg ausdünnen (jeder 2. Punkt, Enden behalten)
        lz2 = lz[::2] + ([lz[-1]] if (len(lz) - 1) % 2 else [])
        linien_bild.append(lz2)
        auf = np.zeros(arb.karte.shape, bool)
        for x, y in lz2:
            auf[y, x] = True
        ids = [i for i in np.unique(arb.karte[auf]).tolist() if i in fam]
        getan = False
        for sid in ids:
            schritt = {"op": "teilen", "id": int(sid), "linie": lz2}
            try:
                erg = arb.anwenden(schritt)
            except EingriffFehler as e:
                continue
            fam.update(erg["neu"])
            schritte_aus.append(schritt)
            getan = True
            print(f"P{nr} teilen {sid}: neu {erg['neu']}")
        if not getan:
            print(f"P{nr} Linie trennt nichts (IDs {ids})")
        # Splitter unter der Mindestgröße an den Familien-Nachbarn mit der längsten Grenze
        for kl in sorted(fam):
            m = arb.karte == kl
            n = int(m.sum())
            if n == 0 or n >= s.get("min", 80):
                continue
            d = np.zeros_like(m)
            d[1:] |= m[:-1]; d[:-1] |= m[1:]; d[:, 1:] |= m[:, :-1]; d[:, :-1] |= m[:, 1:]
            nb = arb.karte[d & ~m]
            nb = nb[np.isin(nb, list(fam))]
            if not len(nb):
                print(f"P{nr} Splitter {kl} ({n}) ohne Familien-Nachbar")
                continue
            ziel = int(np.bincount(nb.astype(np.int64)).argmax())
            schritt = {"op": "verschmelzen", "ids": [ziel, int(kl)], "ziel": ziel}
            arb.anwenden(schritt)
            schritte_aus.append(schritt)
            print(f"P{nr} Splitter {kl} ({n} px) -> {ziel}")
    rand = np.ones(start.shape, bool)
    rand[64:564, 64:564] = False
    geaendert = int(((arb.karte != start) & rand).sum())
    print("Kontextrand geändert:", geaendert)
    for f, fam in familie.items():
        print("Familie", f, sorted(fam))
        for i in sorted(fam):
            m = arb.karte == i
            print("  ", i, int(m.sum()), "kern" if m[64:564, 64:564].any() else "-")
    json.dump({"schritte": schritte_aus}, open(a.aus, "w", encoding="utf-8"))
    json.dump(linien_bild, open(a.aus.replace(".json", "_linien.json"), "w", encoding="utf-8"))
    print("geschrieben", a.aus, len(schritte_aus), "Schritte")


if __name__ == "__main__":
    main()
