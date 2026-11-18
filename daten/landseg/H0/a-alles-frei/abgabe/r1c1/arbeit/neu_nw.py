import json
p='objekte.json'
o=json.load(open(p,encoding='utf-8'))
band=[[70,84],[90,100],[104,124],[116,150],[127,172],[137,192],[158,186],[146,160],[136,132],[124,108],[104,86],[84,70]]
neu=[
 {"art":"pixel","name":"Rain an der Dorfstraße (Nordwest)","klasse":"3","sicher":False,
  "grund":"Saum zwischen Feld und Straße: Gras oder Gebüsch auf SW nicht zu trennen","polygone":[band]},
 {"art":"pixel","name":"Bäume/Gebüsch an der Dorfstraße (Nordwest)","klasse":"4.1","sicher":False,
  "grund":"dunkle Flecken mit Schatten, Baum oder Strauch nicht zu trennen","polygone":[band],
  "grau_max":92,"oeffnen":1,"min_stueck":15,"loecher_fuellen":20}]
# vor den Straßen einfügen (Straßen überschreiben)
i=[k for k,ob in enumerate(o["objekte"]) if ob["name"].startswith("Landstraße")][0]
o["objekte"][i:i]=neu
json.dump(o,open(p,'w',encoding='utf-8'),ensure_ascii=False,indent=1)
k={"polygone":[{"flaeche":[[201,268],[209,265],[221,290],[212,300]],"klasse":"1","sicher":False,
  "name":"heller Rechteckfleck am Straßenrand","grund":"sehr hell, scharf rechteckig, ohne Schlagschatten: flaches Dach, Lagerplatz oder Belag; auf SW nicht zu entscheiden"}],
  "verschmelzen":[],"klassen":[]}
json.dump(k,open('korrekturen.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
