"""Schreibt urteil.json eines Viertels aus einer kompakten Datendatei (daten_<v>.py im Ergebnisordner).
Aufruf: python build.py <viertel>
Datendatei definiert: SEG = [(id, klasse_heute, was_ist_es, urteil, klasse_vorschlag, sicher, [(art, text, flaeche)], [bildkürzel])],
NAH_EIGEN = [n, ...], NAHT, UNSICHER, NICHT_GEPRUEFT, OFFEN.
Bildkürzel: UN UR UK UV UM UG (Übersicht), N1..N4 (nah nummern), R1..R4 (nah roh), E<n> (eigene nah_<n>.jpg), T0, TK.
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
K = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500"
v = sys.argv[1]
VD = f"{K}/viertel/r1c1/{v}"
OUT = Path(f"{K}/urteil/r1c1/{v}")
ns = {}
exec((OUT / f"daten_{v}.py").read_text(encoding="utf-8"), ns)
T0 = f"{K}/T0.png"
TKN = f"{K}/ganz/r1c1/ganz_nummern.jpg"
TKR = f"{K}/ganz/r1c1/ganz_roh.jpg"
KUERZEL = {"UN": "uebersicht_nummern.jpg", "UR": "uebersicht_roh.jpg", "UK": "uebersicht_kontrast.jpg",
           "UV": "uebersicht_vorschlag.jpg", "UM": "uebersicht_maengel.jpg", "UG": "uebersicht_gitter.jpg"}


def pfad(k):
    if k in KUERZEL:
        return f"{VD}/{KUERZEL[k]}"
    if k[0] == "N":
        return f"{VD}/nah{k[1]}_nummern.jpg"
    if k[0] == "R":
        return f"{VD}/nah{k[1]}_roh.jpg"
    if k[0] == "E":
        return f"{OUT.as_posix()}/nah_{k[1:]}.jpg"
    if k[0] == "C":
        return f"{OUT.as_posix()}/kontrast_{k[1:]}.jpg"
    if k == "T0":
        return T0
    if k == "TK":
        return TKN
    raise KeyError(k)


segs = []
for sid, kh, was, urt, kv, sicher, punkte, bilder in ns["SEG"]:
    segs.append({
        "id": sid, "klasse_heute": kh, "was_ist_es": was, "urteil": urt,
        "klasse_vorschlag": kv, "sicher": sicher,
        "punkte": [{"nr": i + 1, "art": a, "text": t, "flaeche_px": fl} for i, (a, t, fl) in enumerate(punkte)],
        "bilder": [pfad(b) for b in bilder],
    })
uebersicht = [T0, TKN, TKR] + [pfad(k) for k in ns.get("UEB", ["UN", "UR", "UV", "UM", "UK"])]
nah = [pfad(f"N{i}") for i in range(1, 5)] + [pfad(f"R{i}") for i in range(1, 5)]
nah += [pfad(f"E{n}") for n in ns.get("NAH_EIGEN", [])]
nah += [pfad(f"C{n}") for n in ns.get("KONTRAST_EIGEN", [])]
eigene = {"build.py", f"daten_{v}.py", "nah.py", "render.py", "stats.py", "urteil.json",
          "roh.jpg", "umriss.jpg", "maengel.jpg", "vorschlag.jpg"}
eigene |= {f"nah_{n}.jpg" for n in ns.get("NAH_EIGEN", [])}
fremd = sorted(p.name for p in OUT.iterdir() if p.is_file() and p.name not in eigene)
offen = list(ns.get("OFFEN", []))
if fremd:
    offen.append("Im Ergebnisordner liegen Dateien, die nicht von mir stammen (angelegt etwa 19:25–19:27 Uhr von einem "
                 "anderen Bearbeiter, vermutlich ein abgebrochener früherer Lauf): " + ", ".join(fremd) +
                 ". Ich habe sie weder angesehen noch verwendet noch gelöscht; gleichnamige eigene Nahansichten "
                 "(nah_<n>.jpg aus NAH_EIGEN) haben dessen Dateien überschrieben, falls es sie gab.")
ns["OFFEN"] = offen
u = {"teilkachel": "r1c1", "viertel": v, "bearbeiter": f"urt-a-r1c1-{v}",
     "bilder_angesehen": {"uebersicht": uebersicht, "nah": nah},
     "segmente": segs, "naht": ns.get("NAHT", []), "unsicher": ns.get("UNSICHER", []),
     "nicht_geprueft": ns.get("NICHT_GEPRUEFT", []), "offen": ns.get("OFFEN", [])}
(OUT / "urteil.json").write_text(json.dumps(u, ensure_ascii=False, indent=1), encoding="utf-8")
print("Segmente", len(segs), "nicht sauber", sum(s["urteil"] == "nicht_sauber" for s in segs),
      "Punkte", sum(len(s["punkte"]) for s in segs), "sicher false", sum(not s["sicher"] for s in segs))
