import json
A = r"C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde2/auftraege-C/C-05/auftrag.json"
OUT = r"C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde2/abgaben/C-05/einigung_abgabe.json"
a = json.load(open(A, encoding="utf-8"))
E = {
    "r0c1:200120|r0c1:200122": ("gleich", "1.2", "Spitze der hellen Dorfstraße und das mittelgraue Stück daneben bilden zusammen den Einmündungsbereich der Straße; an der senkrechten Viertelgrenze ist weder ein Grauton- noch ein Texturwechsel zu sehen (Kette mit 400051 und 400009, Belag auf Schwarz-Weiß nicht sicher, daher Verkehrsfläche)."),
    "r0c1:200120|r1c1:400009": ("gleich", "1.2", "Beide sind der helle Rand derselben Straßenspitze, die über die Naht ohne Kante weiterläuft; Belag auf dem Scan nicht bestimmbar, daher Verkehrsfläche."),
    "r0c1:200120|r1c1:400051": ("gleich", "1.2", "Die helle Dorfstraße läuft über die Naht ohne Kante als schmale Gasse nach Süden weiter; Belag auf Schwarz-Weiß nicht sicher, daher Verkehrsfläche."),
    "r0c1:200122|r1c1:400051": ("gleich", "1.2", "Das mittelgraue Stück oberhalb der Naht setzt sich unterhalb im gleichen Grauton als oberer Teil der Gasse fort, die Naht ist eine Gerade ohne Bildkante; gleiche Fläche wie die Straßenkette, Verkehrsfläche."),
    "r1c1:400051|r1c1:400060": ("grenze", None, "Helle Gasse gegen dunkles Schattenband neben den Häusern: deutlicher Helligkeitssprung, nur an zwei Punkten der Viertelgrenze schwach, verschiedene Flächen."),
    "r0c1:200049|r0c1:200056": ("grenze", None, "Helle Fahrbahn gegen den dunkleren Randstreifen (Gehweg oder Vorgarten), getrennt durch eine dünne dunkle Linie; nur ein Punkt ohne Kante, verschiedene Flächen."),
    "r0c1:200081|r1c1:400003": ("gleich", "1.2", "Dieselbe helle, gleich breite Dorfstraße läuft ohne Grauton- oder Breitenwechsel über die Naht; Belag auf Schwarz-Weiß nicht sicher, daher Verkehrsfläche."),
    "r0c1:200121|r1c1:400006": ("grenze", None, "Helles Rechteckdach gegen die graue Hof- und Gartenfläche des Häuserblocks; der Dachrand ist eine klare Helligkeitskante, nur zwei Eckpunkte an der Naht ohne Kante."),
    "r1c1:400006|r1c1:400171": ("grenze", None, "Graues Einzeldach mit dunkler Schattenlinie an der Ostseite gegen die übrige Mischfläche des Blocks; nur zwei Punkte an der Viertelgrenze mit schwacher Kante, Gebäude bleibt Gebäude."),
    "r1c1:400006|r1c1:400148": ("grenze", None, "Helle Dorfstraße gegen die graue, unruhige Fläche des Häuserblocks östlich davon; Helligkeitswechsel entlang der Straße, nur ein Punkt an der Viertelgrenze schwach."),
}
paare = []
for p in a["paare"]:
    e, k, g = E[p["paar"]]
    paare.append({"paar": p["paar"], "entscheidung": e, "klasse": k, "grund": g})
assert len(paare) == len(E)
codes = {c["code"] for c in a["klassen"]} if isinstance(a["klassen"], list) and a["klassen"] and isinstance(a["klassen"][0], dict) else None
print("codes ok", codes is None or all(x["klasse"] in codes for x in paare if x["klasse"]))
out = {"schema": "landseg-einigung-abgabe/1", "fassung": "C", "buendel": "C-05",
       "bearbeiter": "agent:einigung-C-05:20261118i-r2", "paare": paare,
       "offen": [], "nicht_geprueft": []}
json.dump(out, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(paare))
