"""PQ/Boundary-PQ der H0-Gegenprobe (Fassung C, r0c0) gegen das Erst-Urteil, im Kern.

Erst-Urteil: Karte von C r0c0 vor dem Beheben der Zerfälle (Sicherung Teil 4; Einigung ändert nur
Klassen). Gegenprobe: c-feste-liste/gegenprobe/r0c0. Klassenunabhängig und klassengleich (Treffer
nur bei gleicher Klasse, PQ-Definition von Kirillov et al. je Bild über alle Klassen gemittelt
ohne Klassenmittel: gleiche Formel, Treffer auf gleiche Klasse beschränkt).
Aufruf: python -B pq_gegenprobe.py <ausgabe.json>
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, "C:/Users/Phil/Developement/Victor/landseg")
from messen_h0 import pq  # noqa: E402
from landseg.dateien import lese_labels, lese_json  # noqa: E402
from landseg.zusammentragen import kern_ausschneiden  # noqa: E402

H0 = Path("C:/Users/Phil/Developement/Victor/daten/landseg/H0")
SICH = Path("C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-4/sicherung")


def main():
    m = lese_json(H0 / "manifest.json")
    t = next(x for x in m["teilkacheln"] if x["id"] == "r0c0")
    erst_p = SICH / "c-feste-liste/r0c0"
    gegen_p = H0 / "c-feste-liste/gegenprobe/r0c0"
    erst = kern_ausschneiden(lese_labels(erst_p / "labels.tif"), t)
    gegen = kern_ausschneiden(lese_labels(gegen_p / "labels.tif"), t)
    ke = {int(s["id"]): str(s.get("klasse")) for s in lese_json(erst_p / "segmente.json")["segmente"]}
    kg = {int(s["id"]): str(s.get("klasse")) for s in lese_json(gegen_p / "segmente.json")["segmente"]}
    aus = {f"klassenunabhaengig_rand{r}": pq(erst, gegen, r) for r in (2, 5)}
    # klassengleich: Segmente verschiedener Klasse dürfen nicht treffen -> Klasse in die ID kodieren
    codes = {c: i + 1 for i, c in enumerate(sorted(set(ke.values()) | set(kg.values())))}
    e2 = np.vectorize(lambda i: i * 1000 + codes[ke.get(int(i), "?")] if ke.get(int(i)) in codes else i * 1000)(erst)
    g2 = np.vectorize(lambda i: i * 1000 + codes[kg.get(int(i), "?")] if kg.get(int(i)) in codes else i * 1000)(gegen)
    # Treffer nur bei gleicher Klasse: Schnitt verschiedener Klassen auf leer setzen, indem man die
    # Klassen als getrennte Ebenen vergleicht
    tp = fp = fn = 0
    summe = 0.0
    for c, ci in codes.items():
        ma, mb = (e2 % 1000) == ci, (g2 % 1000) == ci
        a = np.where(ma, e2, 0)
        b = np.where(mb, g2, 0)
        if not ma.any() and not mb.any():
            continue
        r = pq(a, b, 2)
        # Hintergrund 0 zählt mit, wenn vorhanden: herausrechnen
        tp_c = r["tp"] - (1 if (~ma).any() and (~mb).any() and (((~ma) & (~mb)).sum() / ((~ma) | (~mb)).sum() > 0.5) else 0)
        n_a = len(np.unique(a[ma])) if ma.any() else 0
        n_b = len(np.unique(b[mb])) if mb.any() else 0
        summe += r["sq"] * r["tp"] - (((~ma) & (~mb)).sum() / ((~ma) | (~mb)).sum() if tp_c < r["tp"] else 0)
        tp += tp_c
        fp += n_b - tp_c
        fn += n_a - tp_c
    aus["klassengleich_rand2"] = {"tp": tp, "fp": fp, "fn": fn,
                                  "pq": round(summe / (tp + 0.5 * fp + 0.5 * fn), 3) if tp else 0}
    Path(sys.argv[1]).write_text(json.dumps(aus, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(aus, ensure_ascii=False))


if __name__ == "__main__":
    main()
