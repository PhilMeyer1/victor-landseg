import json
p = "urteil.json"
u = json.load(open(p, encoding="utf-8"))
n4 = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/viertel/r1c0/v3/nah4_nummern.jpg"
u["bilder_angesehen"]["nah"].append(n4)
for e in u["segmente"]:
    if e["id"] in (300060, 300073, 300061):
        e["bilder"].append(n4)
    if e["id"] == 300073:
        e["punkte"][1]["text"] = "Gerade senkrechte Westgrenze zu 300061 ohne Bildkante; mit 300061 bzw. 300008 verschmelzen (205/485)."
u["nicht_geprueft"] = ["nah3_roh, nah3_nummern und nah4_roh (Wald im Süden) sowie uebersicht_vorschlag/maengel/kontrast/gitter nicht eigens angesehen; der Waldteil wurde in uebersicht_roh und nah4_nummern beurteilt. Werkzeug kante nicht benutzt."]
json.dump(u, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
