"""Baut urteil.json aus einer kompakten Tabelle (daten_<v>.py im selben Ordner).

Aufruf: PY -I bau_urteil.py <viertel>
Kurznamen der Bilder: U uebersicht_nummern, R uebersicht_roh, K uebersicht_kontrast, n1..n4 nahN_nummern,
r1..r4 nahN_roh, e1..e9 eigene nah_N.jpg, k1..k9 eigene kontrast_N.jpg, T0 (T0.png), G (ganz_nummern), GR (ganz_roh).
"""
import json
import runpy
import sys
from pathlib import Path

BASIS = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500"


def pfad(k, v):
    vb = f"{BASIS}/viertel/r0c0/{v}"
    ub = f"{BASIS}/urteil-zweit/r0c0/{v}"
    feste = {"U": f"{vb}/uebersicht_nummern.jpg", "R": f"{vb}/uebersicht_roh.jpg",
             "K": f"{vb}/uebersicht_kontrast.jpg", "V": f"{vb}/uebersicht_vorschlag.jpg",
             "T0": f"{BASIS}/T0.png", "G": f"{BASIS}/ganz/r0c0/ganz_nummern.jpg",
             "GR": f"{BASIS}/ganz/r0c0/ganz_roh.jpg"}
    if k in feste:
        return feste[k]
    if k[0] == "n":
        return f"{vb}/nah{k[1:]}_nummern.jpg"
    if k[0] == "r":
        return f"{vb}/nah{k[1:]}_roh.jpg"
    if k[0] == "e":
        return f"{ub}/nah_{k[1:]}.jpg"
    if k[0] == "k":
        return f"{ub}/kontrast_{k[1:]}.jpg"
    raise ValueError(k)


def main():
    v = sys.argv[1]
    hier = Path(__file__).parent
    d = runpy.run_path(str(hier / f"daten_{v}.py"))
    segs = []
    for row in d["SEG"]:
        sid, heute, was, urteil, vorschlag, sicher, punkte, bilder = row
        segs.append({"id": sid, "klasse_heute": heute, "was_ist_es": was, "urteil": urteil,
                     "klasse_vorschlag": vorschlag, "sicher": sicher,
                     "punkte": [{"nr": i + 1, "art": p[0], "text": p[1], "flaeche_px": p[2]}
                                for i, p in enumerate(punkte)],
                     "bilder": [pfad(b, v) for b in bilder]})
    out = {"teilkachel": "r0c0", "viertel": v, "bearbeiter": f"zweit-a-r0c0-{v}",
           "bilder_angesehen": {"uebersicht": [pfad(b, v) for b in d["UEBERSICHT"]],
                                "nah": [pfad(b, v) for b in d["NAH"]]},
           "segmente": segs, "naht": [{"id": a, "seite": b, "text": c} for a, b, c in d["NAHT"]],
           "unsicher": d["UNSICHER"], "nicht_geprueft": d["NICHT_GEPRUEFT"], "offen": d["OFFEN"]}
    (hier / "urteil.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("geschrieben", len(segs), "Segmente")


if __name__ == "__main__":
    main()
