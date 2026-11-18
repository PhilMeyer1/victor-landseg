import json
P = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/zusammentragen.json"
E = "C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/naht-B"
a = json.load(open(P, encoding="utf-8"))
ab = json.load(open(E + "/naht_abgabe.json", encoding="utf-8"))
vorhanden = a.get("naht_bestaetigt", [])
schl = {(e["naht"], tuple(sorted(e["ids"]))) for e in vorhanden}
for e in ab["naht_bestaetigt"]:
    if (e["naht"], tuple(sorted(e["ids"]))) not in schl:
        vorhanden.append(dict(e, quelle="naht-B Runde 1, agent:naht-B:20261118i"))
a["naht_bestaetigt"] = vorhanden
for t in ab["einheiten"]:
    a["einheiten"].append(t)
json.dump(a, open(P, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(vorhanden), len(a["einheiten"]))
