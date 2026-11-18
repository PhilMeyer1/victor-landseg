import json
A = "C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde1/abgaben/A-04/einigung_abgabe.json"
P = [
    ("r0c0:100028|r0c1:200166", "unklar", None,
     "An der Naht läuft derselbe weiche mittel- bis dunkelgraue Verlauf ohne Kante durch; der kleine dunkle Fleck am Giebelende von Dach 200169 kann Schatten, Busch oder Hofboden sein, und 100028 berührt ihn nur mit einem Bildpunkt, daher weder Hofstelle noch Garten sicher."),
    ("r0c0:100028|r0c1:200167", "unklar", None,
     "Beidseits der Naht dieselbe mittelgraue Fläche (Grauwerte 75-105) zwischen dem hellen Dach 200169 und dem dunklen Schattenband 200234; ob Hof, Vorgarten oder Dachende, ist auf dem Schwarz-Weiß-Scan nicht zu trennen."),
    ("r0c0:100028|r0c1:200234", "grenze", None,
     "200234 ist das sehr dunkle Schattenband unter dem Dach 200169, 100028 im Kern vor allem das obere Ende des hellen Streifens darunter; die echte Kante hell/dunkel kreuzt die Naht bei y 60-63, die Berührung y 56-62 ist nur ein Versatz der Grenze um wenige Bildpunkte."),
    ("r0c0:100028|r0c1:200230", "gleich", "1.2",
     "Beidseits der Naht derselbe helle, körnige Streifen (Grauwerte 140-180) parallel zu den Häusern, mit Schatten auf der Straßenseite; Dach oder helle Hoffläche ist nicht zu trennen (so auch die Notiz zu 200230), daher gemeinsam Hofstelle ungetrennt."),
    ("r0c0:100054|r0c1:200230", "grenze", None,
     "200230 ist der helle Hofstellen-Streifen, 100054 das Straßensegment; die Oberkante von 100054 reicht an der Naht nur 3 Bildpunkte in den hellen Streifen, die echte Kante hell/dunkel liegt bei y 77-80, beide Flächen sind verschieden."),
    ("r0c0:100054|r0c1:200229", "grenze", None,
     "200229 ist der abfallende Unterrand des hellen Hofstellen-Streifens (Grauwerte 130 bis 85) zum Schattenstreifen hin, keine Fahrbahn; 100054 trägt die Straße, die helle Fahrbahn selbst liegt erst rund 15 Bildpunkte tiefer."),
    ("r0c0:100054|r0c1:200227", "unklar", None,
     "Beidseits der Naht derselbe sehr dunkle Streifen (Grauwerte 50-70) zwischen hellem Hofstreifen und Fahrbahn; ob Schatten auf der Straße oder auf Vorplatz und Hof, ist nicht zu sehen, und 100054 deckt dort statt der hellen Fahrbahn diesen Schattenstreifen."),
    ("r0c0:100054|r0c1:200283", "unklar", None,
     "Beidseits der Naht derselbe mittelgraue Streifen (Grauwerte 80-95) direkt oberhalb der hellen Fahrbahn; ob Straßenrand, Vorplatz oder Garten, ist auf dem Scan nicht zu entscheiden, 200283 reicht zudem in eine Gartenfläche weiter rechts."),
    ("r0c1:200192|r0c1:200249", "grenze", None,
     "200249 ist die breite helle Straße (Grauwerte 160-185), 200192 der mittelgraue Fleck (80-120) am Kopf des Hofstreifens darunter; an der Berührung liegt die weiche Straßenkante, verschiedene Flächen."),
]
d = {
    "schema": "landseg-einigung-abgabe/1", "fassung": "A", "buendel": "A-04",
    "bearbeiter": "agent:einigung-A-04:20261118i-r1",
    "paare": [{"paar": p, "entscheidung": e, "klasse": k, "grund": g} for p, e, k, g in P],
    "offen": [
        "Straße D an der Naht r0c0|r0c1 (Paare 5-8): Die helle Fahrbahn liegt an der Naht bei y 100-116 in r0c0:100009 (Klasse 2.2 Garten) und läuft drüben als r0c1:200226 (3.1) zur Kreuzung; r0c0:100054 (3.1, sicher) liegt dort rund 10-15 Bildpunkte zu hoch auf Hofstreifen-Unterrand und Schattenstreifen. Das ist eine Grenz- bzw. Klassenfrage außerhalb dieses Bündels (Paar 100009|200226 prüfen, Grenze von 100054 nachziehen).",
        "Paare 1, 2, 7, 8 unklar: Hof, Garten, Vorplatz oder Straßenrand im Schatten sind auf dem Schwarz-Weiß-Scan nicht zu trennen; ein Farbbild oder eine Ortskarte von 1968 würde entscheiden.",
    ],
    "nicht_geprueft": [],
}
with open(A, "w", encoding="utf-8") as f:
    json.dump(d, f, ensure_ascii=False, indent=1)
print("ok", len(P))
