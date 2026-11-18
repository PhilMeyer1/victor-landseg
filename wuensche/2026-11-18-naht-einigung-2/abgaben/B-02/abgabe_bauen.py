"""Baut einigung_abgabe.json fuer Buendel B-02 aus den Entscheidungen unten."""
import json

A = "C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-naht-einigung-2/auftraege-B/B-02/auftrag.json"
OUT = "C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-naht-einigung-2/abgaben/B-02/einigung_abgabe.json"

E = {
    1: ("gleich", "1", "Dunkle Gehölzkronen (Sträucher und kleine Bäume) laufen am oberen Bildrand ohne Helligkeits- oder Farbsprung über die Naht; ob Gebüsch oder Baumgruppe, ist an der Stelle nicht sicher zu trennen, daher die Elternklasse Gehölz."),
    2: ("gleich", "3.3.2", "Der grüne Garten- und Rasenstreifen östlich des Hauses setzt sich ohne Kante in das Gartensammelsegment 200043 fort (Hecken, Sträucher, Terrassen, Flachdach gemischt), das als gemischte Gartenparzelle besser passt als Gebüsch."),
    3: ("gleich", "3.3.2", "Die hellen Gartengegenstände am Rasenrand reichen bei y 44–52 sichtbar über die Naht in dasselbe Gartensammelsegment; gleiche Klasse wie Paar 2 (Kette 100061–200043–100074)."),
    4: ("grenze", None, "Der graugrüne Grasstreifen am Nordrand der Straße stößt an die Unterkante einer dunklen Baumkrone; zwei verschiedene Flächen, die Klassen bleiben."),
    5: ("gleich", "2.3", "Der graugrüne Streifen zwischen Gehölz und Straße läuft ohne Kante über die Naht weiter; ein schmaler bewachsener Straßenrand, daher Saum und Randstreifen (Kette mit Paar 6)."),
    6: ("gleich", "2.3", "Derselbe graugrüne Randstreifen nördlich der Asphaltstraße setzt sich östlich der Naht im Segment 200100 fort (Farbe zwischen Gras und Asphalt, mit weißem Pfosten); eine Fläche mit Paar 5, Klasse Saum und Randstreifen."),
    7: ("grenze", None, "Die Asphaltstraße und der Randstreifen darüber berühren sich nur an einem Eckpunkt; die Straßenkante trennt beide Flächen auch westlich der Naht (dort Grasstreifen 100099), die Klassen bleiben."),
    8: ("grenze", None, "Die Asphaltstraße endet am hellen Randstein; das Segment 200116 liegt als dunkler Kronen- und Schattenstreifen darunter, zwei verschiedene Flächen."),
    9: ("gleich", "1", "Unter dem südlichen Randstein liegt beidseits der Naht derselbe dunkle Kronen- und Schattenbereich ohne Kante; gleiche Klasse wie die Kette mit Paar 10, daher Gehölz."),
    10: ("gleich", "1", "Die Sträucher zwischen Hauswand und Nadelbaum und der dunkle Gehölzstreifen östlich davon gehen ohne Kante ineinander über (helle Strauchteile bei y 214–232 und Schatten bei y 202–212 auf beiden Seiten); Kette 100109–200116–100122 mit Krone und Sträuchern, daher Elternklasse Gehölz."),
    11: ("grenze", None, "Die mittelgrünen Sträucher enden an der rötlich-violetten Blutbuchenkrone 200145, die auch westlich der Naht deutlich anders gefärbt ist; zwei verschiedene Gehölze."),
    12: ("grenze", None, "Die grob strukturierte olivgrüne Laubbaumkrone 100114 berührt die dunkelgrüne Kronengruppe 200107 nur an einem Eckpunkt; zwei verschiedene, im Bild getrennte Kronen."),
}

a = json.load(open(A, encoding="utf-8"))
paare = []
for p in a["paare"]:
    ent, kl, grund = E[p["nr"]]
    paare.append({"paar": p["paar"], "entscheidung": ent, "klasse": kl, "grund": grund})
assert len(paare) == len(E)
codes = {c["code"] for c in json.load(open(a["kategorien"], encoding="utf-8"))["classes"]}
assert all(x["klasse"] in codes for x in paare if x["entscheidung"] == "gleich")
out = {
    "schema": "landseg-einigung-abgabe/1", "fassung": "B", "buendel": "B-02",
    "bearbeiter": "agent:einigung-B-02:20261118e",
    "paare": paare,
    "offen": [
        "r0c1:200043 ist ein Sammelsegment (Hecken, Flachdach, Terrassen, Gartenboden); die Klasse 3.3.2 gilt bis zur Teilung, die das Urteil r0c1 vorschlägt.",
        "r0c1:200100 enthält neben dem graugrünen Streifen den weißen Pfosten an der Straßenkante; ob dort ein Randstein liegt (6.5), ist bei 0,2 m Bildpunkt nicht sicher."
    ],
    "nicht_geprueft": [],
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
from collections import Counter
print(Counter(x["entscheidung"] for x in paare))
