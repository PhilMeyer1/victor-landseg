"""Messzahlen für den Messbericht H0 gegen T0 und PQ/Boundary-PQ der Gegenprobe.

Aufruf: python -B messen_h0.py <ausgabe.json>
Zählt im Kern (zusammengesetzt aus den Teilkachelkarten der Fassung): Segmente, benutzte Klassen,
Anteil sicher: nein (Segmente und Fläche), Rückfall auf Elternklassen (Code mit weniger als drei
Stufen), je Klasse Segmente/Fläche/sicher-nein; dazu PQ und Boundary-PQ (klassenunabhängig) der
Gegenprobe A r0c0 gegen die Erstabgabe im Kern.
"""
import json
import sys
from pathlib import Path

import numpy as np
from scipy import ndimage

sys.path.insert(0, "C:/Users/Phil/Developement/Victor/landseg")
from landseg.dateien import lese_labels, lese_json  # noqa: E402
from landseg.zusammentragen import kern_ausschneiden  # noqa: E402

BILDER = {
    "T0": Path("C:/Users/Phil/Developement/Victor/daten/gesamt/victor-landseg/ergebnisse"),
    "H0": Path("C:/Users/Phil/Developement/Victor/daten/landseg/H0"),
}
FASSUNGEN = {"A": "a-alles-frei", "B": "b-kategorien-frei", "C": "c-feste-liste"}
REPO_KAT = Path("C:/Users/Phil/Developement/Victor/landseg/kategorien.json")


def namen(kat_pfad):
    d = json.loads(Path(kat_pfad).read_text(encoding="utf-8"))
    ergebnis = {}

    def gehe(x):
        if isinstance(x, dict):
            if "code" in x and "name" in x:
                ergebnis[str(x["code"])] = x["name"]
            for v in x.values():
                gehe(v)
        elif isinstance(x, list):
            for v in x:
                gehe(v)
    gehe(d)
    return ergebnis


def unsicher(e):
    return e.get("sicher") in (False, "nein", "false", 0)


def fassung(basis, ordner):
    m = lese_json(basis / "manifest.json")
    segs, flaechen = {}, {}
    for t in m["teilkacheln"]:
        tk = basis / ordner / t["id"]
        if not (tk / "labels.tif").exists():
            return None
        kern = kern_ausschneiden(lese_labels(tk / "labels.tif"), t)
        ids, z = np.unique(kern, return_counts=True)
        d = lese_json(tk / "segmente.json")
        nach_id = {int(s["id"]): s for s in d["segmente"]}
        for i, n in zip(ids.tolist(), z.tolist()):
            segs[(t["id"], i)] = nach_id.get(i, {})
            flaechen[(t["id"], i)] = n
    gesamt = sum(flaechen.values())
    klassen = {}
    for k, e in segs.items():
        c = str(e.get("klasse"))
        kl = klassen.setdefault(c, {"segmente": 0, "flaeche": 0, "unsicher": 0, "flaeche_unsicher": 0})
        kl["segmente"] += 1
        kl["flaeche"] += flaechen[k]
        if unsicher(e):
            kl["unsicher"] += 1
            kl["flaeche_unsicher"] += flaechen[k]
    n = len(segs)
    nein = sum(1 for e in segs.values() if unsicher(e))
    f_nein = sum(flaechen[k] for k, e in segs.items() if unsicher(e))
    eltern = sum(1 for e in segs.values() if str(e.get("klasse")).count(".") < 2)
    f_eltern = sum(flaechen[k] for k, e in segs.items() if str(e.get("klasse")).count(".") < 2)
    je_tk = {}
    for (tk, _), e in segs.items():
        j = je_tk.setdefault(tk, {"segmente": 0, "unsicher": 0})
        j["segmente"] += 1
        j["unsicher"] += unsicher(e)
    return {"segmente": n, "klassen": len(klassen), "sicher_nein": nein,
            "anteil_sicher_nein": round(nein / n, 3), "anteil_flaeche_sicher_nein": round(f_nein / gesamt, 3),
            "elternklasse": eltern, "anteil_elternklasse": round(eltern / n, 3),
            "anteil_flaeche_elternklasse": round(f_eltern / gesamt, 3),
            "je_teilkachel": je_tk, "je_klasse": klassen}


def pq(a, b, rand_px):
    """Klassenunabhängiges PQ und Boundary-PQ (Qualität = min(Masken-IoU, Rand-IoU), Cheng et al. 2021)."""
    ids_a, ids_b = np.unique(a), np.unique(b)
    # Schnittmengen über ein gemeinsames Paarlabel
    paar, zahl = np.unique(a.astype(np.int64) * (1 << 32) + b.astype(np.int64), return_counts=True)
    fa = dict(zip(*np.unique(a, return_counts=True)))
    fb = dict(zip(*np.unique(b, return_counts=True)))
    treffer = []
    for p, z in zip(paar.tolist(), zahl.tolist()):
        i, j = p >> 32, p & 0xFFFFFFFF
        iou = z / (fa[i] + fb[j] - z)
        if iou > 0.5:
            treffer.append((i, j, iou))
    tp, fp, fn = len(treffer), len(ids_b) - len(treffer), len(ids_a) - len(treffer)
    pq_wert = sum(t[2] for t in treffer) / (tp + 0.5 * fp + 0.5 * fn)
    st = ndimage.generate_binary_structure(2, 1)

    def band(maske):
        return maske & ~ndimage.binary_erosion(maske, structure=st, iterations=rand_px, border_value=1)
    biou = []
    for i, j, iou in treffer:
        ma, mb = a == i, b == j
        ba, bb = band(ma) , band(mb)
        u = (ba | bb).sum()
        biou.append(min(iou, ((ba & bb).sum() / u) if u else 1.0))
    bpq = sum(biou) / (tp + 0.5 * fp + 0.5 * fn)
    return {"segmente_erst": len(ids_a), "segmente_gegen": len(ids_b), "tp": tp, "fp": fp, "fn": fn,
            "sq": round(sum(t[2] for t in treffer) / tp, 3) if tp else 0, "rq": round(tp / (tp + 0.5 * fp + 0.5 * fn), 3),
            "pq": round(pq_wert, 3), "boundary_pq": round(bpq, 3), "rand_px": rand_px}


def main():
    aus = {"bilder": {}, "namen_c": namen(REPO_KAT)}
    for b, basis in BILDER.items():
        aus["bilder"][b] = {k: fassung(basis, o) for k, o in FASSUNGEN.items()}
    h0 = BILDER["H0"]
    m = lese_json(h0 / "manifest.json")
    t = next(x for x in m["teilkacheln"] if x["id"] == "r0c0")
    if not (h0 / "a-alles-frei/abgabe-gegenprobe/r0c0/labels.tif").exists():
        aus["gegenprobe_H0_A_r0c0"] = "fehlt: keine labels.tif der Gegenprobe"
    else:
      erst = kern_ausschneiden(lese_labels(h0 / "a-alles-frei/abgabe/r0c0/labels.tif"), t)
      gegen = kern_ausschneiden(lese_labels(h0 / "a-alles-frei/abgabe-gegenprobe/r0c0/labels.tif"), t)
      aus["gegenprobe_H0_A_r0c0"] = {f"rand{r}": pq(erst, gegen, r) for r in (2, 5)}
    Path(sys.argv[1]).write_text(json.dumps(aus, ensure_ascii=False, indent=1), encoding="utf-8")
    for b in aus["bilder"]:
        for k, v in aus["bilder"][b].items():
            if v:
                print(b, k, {x: v[x] for x in v if x not in ("je_klasse", "je_teilkachel")},
                      {tk: f"{j['segmente']}/{j['unsicher']}" for tk, j in v["je_teilkachel"].items()})
    print("PQ", aus["gegenprobe_H0_A_r0c0"])


if __name__ == "__main__":
    main()
