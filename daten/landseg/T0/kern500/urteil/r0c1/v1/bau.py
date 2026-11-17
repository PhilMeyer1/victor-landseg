"""Baut urteil.json des Viertels aus der Tabelle in eintraege_<v>.py (gleicher Ordner)."""
import sys, json, importlib.util
v = sys.argv[1]
B = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500"
OUT = B + "/urteil/r0c1/" + v + "/"
VB = B + "/viertel/r0c1/" + v + "/"
spec = importlib.util.spec_from_file_location("e", OUT + "eintraege.py")
e = importlib.util.module_from_spec(spec); spec.loader.exec_module(e)
VJ = json.load(open(VB + "viertel.json", encoding="utf-8"))
klasse = {s["id"]: s["klasse"] for s in VJ["segmente"]}
reihen = [s["id"] for s in VJ["segmente"]]


def bild(k):
    if k.startswith("eigen:"):
        return OUT + k[6:]
    return VB + k


segs = []
seen = set()
for t in e.E:
    sid, was, urt, vor, sicher, punkte, bilder = t
    sid = 200000 + sid if sid < 100000 else sid
    seen.add(sid)
    segs.append({"id": sid, "klasse_heute": klasse[sid], "was_ist_es": was,
                 "urteil": urt, "klasse_vorschlag": vor, "sicher": sicher,
                 "punkte": [{"nr": i + 1, "art": p[0], "text": p[1], "flaeche_px": p[2] if len(p) > 2 else None}
                            for i, p in enumerate(punkte)],
                 "bilder": [bild(b) for b in (["uebersicht_nummern.jpg"] + bilder)]})
order = {sid: i for i, sid in enumerate(reihen)}
segs.sort(key=lambda s: order[s["id"]])
fehlt = [s for s in reihen if s not in seen]
U = {"teilkachel": "r0c1", "viertel": v, "bearbeiter": "urt-a-r0c1-" + v,
     "bilder_angesehen": {"uebersicht": e.UEBERSICHT + [VB + b for b in e.UEB_V],
                          "nah": [bild(b) for b in e.NAH]},
     "segmente": segs, "naht": e.NAHT, "unsicher": e.UNSICHER,
     "nicht_geprueft": e.NICHT_GEPRUEFT, "offen": e.OFFEN}
json.dump(U, open(OUT + "urteil.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("geschrieben", len(segs), "fehlt", fehlt)
