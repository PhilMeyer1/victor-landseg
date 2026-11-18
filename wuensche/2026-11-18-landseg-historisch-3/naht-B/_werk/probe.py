import json
E = "C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/naht-B"
H = "../../../daten/landseg/H0"
a = json.load(open("C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/zusammentragen.json", encoding="utf-8"))
ab = json.load(open(E + "/naht_abgabe.json", encoding="utf-8"))
a["manifest"] = H + "/manifest.json"
for e in a["einheiten"]:
    e["labels"] = H + "/b-kategorien-frei/" + e["labels"]; e["segmente"] = H + "/b-kategorien-frei/" + e["segmente"]
a["naht_bestaetigt"] = ab["naht_bestaetigt"]
a["ziel"] = "probe"
json.dump(a, open(E + "/zusammentragen.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
