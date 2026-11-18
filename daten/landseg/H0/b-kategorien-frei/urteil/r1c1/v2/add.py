import json
p = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c1/v2/plan_ws.json"
d = json.load(open(p, encoding="utf-8"))
d["schritte"].append({"art": "roh", "schritt": {"op": "polygon_zuweisen", "flaeche": [[503,145],[519,134],[536,147],[521,162]], "klasse": "1.1.1"}})
json.dump(d, open(p, "w", encoding="utf-8")); print(len(d["schritte"]))
