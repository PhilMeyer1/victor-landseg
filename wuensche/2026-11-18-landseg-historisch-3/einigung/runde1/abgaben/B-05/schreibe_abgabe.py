"""Schreibt einigung_abgabe.json fuer Buendel B-05 (Fassung B)."""
import json

OUT = "C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde1/abgaben/B-05/einigung_abgabe.json"

paare = [
    ("r0c0:100202|r1c0:300001", "unklar", None,
     "An der Naht läuft derselbe helle Streifen westlich des dunklen Grabenbandes ohne Kante weiter (oben mit dunklen Buschflecken, unten mit heller Stelle bei y 515–540); 300001 ist aber weiter südlich ein Streifenfeld, der Übergang Brache–Feld liegt etwa bei y 555 mitten in 300001, und ob die helle Ecke noch Brache oder ein hellerer Feldteil ist, lässt das Bild nicht sicher erkennen."),
    ("r0c0:100221|r1c0:300001", "grenze", None,
     "100221 ist ein Stück des dunklen Rain- bzw. Grabenbandes (Grauwert um 70) zwischen hellem Brachestreifen und großem Feld, 300001 ist der hellere Streifen bzw. das Streifenfeld westlich davon (um 91); das Band läuft unter der Naht in 300001 hinein weiter, die Grenze Band–Fläche liegt dort im Segment, nicht an der Naht."),
    ("r0c0:100223|r1c0:300001", "grenze", None,
     "100223 liegt wie 100221 auf dem dunklen Rainband am Westrand des großen Feldes, 300001 ist der hellere Streifen bzw. das Streifenfeld westlich davon; verschiedene Flächen, nur dass das Band unter der Naht ein paar Bildpunkte in 300001 hineinläuft."),
    ("r0c0:100223|r1c0:300002", "grenze", None,
     "Berührung an einem Bildpunkt (x 43): westlich das dunkle Rainband (100223), östlich beginnt das gleichmäßig dunkelgraue große Feld 300002; schwacher, aber vorhandener Übergang vom Band zur Feldfläche."),
    ("r0c0:100224|r1c0:300002", "gleich", "6.1",
     "Beide Seiten zeigen dieselbe gleichmäßig mittelgraue, feinkörnige Feldfläche (Grauwert 72 gegen 76, wie das Nachbarfeld 100154 mit 77); einen eigenen Randstreifen zwischen Feld und hellem Weg zeigt das Bild an dieser Stelle nicht, also Feld."),
    ("r0c0:100224|r1c0:300073", "grenze", None,
     "Oben die mittelgraue Feldecke links des Weges, zwei bis drei Bildpunkte unter der Naht beginnt die dunkle Oberkante der Feldscheune (Grauwerte fallen von etwa 70 auf 40); echte Grenze Feld–Gebäude knapp unter der Naht."),
    ("r0c0:100220|r1c0:300073", "grenze", None,
     "Das helle Band des Feldwegs (Grauwert um 110) endet an der Naht, direkt darunter liegt der fast schwarze Block der Feldscheune (unter 40); deutlicher Helligkeitssprung einen Bildpunkt unter der Naht, also Weg gegen Gebäude."),
    ("r0c0:100225|r1c0:300073", "grenze", None,
     "Berührung an einem Bildpunkt (x 333): oben der dunkle Fleck rechts des Weges, unten die rechte Oberecke der Scheune, wo der Weg mit helleren Bildpunkten (65–80) zwischen Fleck und dunklem Block vorbeiführt; zwei verschiedene Dinge."),
    ("r0c0:100225|r1c0:300070", "grenze", None,
     "Der dunkle Fleck (Grauwert um 43) setzt sich unter der Naht noch etwa 7 Bildpunkte als dunkle Spitze von 300070 fort, erst darunter beginnt das helle Band des Feldwegs; Gebüschfleck und Weg sind verschiedene Flächen, die Grenze liegt knapp unter der Naht in 300070."),
    ("r0c0:100195|r1c0:300070", "grenze", None,
     "Oben der dunklere Südrand des großen gleichmäßig grauen Feldes 100195, unten die dunkle Spitze von 300070, an die nach etwa 7 Bildpunkten das helle Band des Feldwegs anschließt; Feld und Weg sind verschiedene Flächen, die Grenze liegt knapp unter der Naht."),
    ("r0c1:200025|r0c1:200219", "grenze", None,
     "Berührung an einem Bildpunkt: links das dunkle Schattenband zwischen den Dachstreifen (Grauwert um 35), rechts der dünne Ausläufer von 200025 auf der hellen Dachkante (steigt auf 100–200); starker Helligkeitssprung, Schatten gegen hellen Rand."),
    ("r0c1:200192|r0c1:200211", "grenze", None,
     "Links das dunkle Schattenband im Block, rechts das helle Dach der Halle mit einem etwas dunkleren Fleck an seiner Westkante; der Übergang von dunkel (75–125) zu hell (145–180) ist die Dachkante, Schatten und Gebäude sind verschiedene Flächen."),
]

abgabe = {
    "schema": "landseg-einigung-abgabe/1",
    "fassung": "B",
    "buendel": "B-05",
    "bearbeiter": "agent:einigung-B-05:20261118i-r1",
    "paare": [{"paar": p, "entscheidung": e, "klasse": k, "grund": g} for p, e, k, g in paare],
    "offen": [
        "r1c0:300001: die helle Nordwestecke (etwa x 0–40, y 500–555) setzt den Brachestreifen von r0c0:100202 fort, der Rest ist Streifenfeld; nur eine Teilung von 300001 etwa bei y 555 löst Paar 1, eine Klasse allein nicht.",
        "r1c0:300001: das dunkle Rain-/Grabenband von r0c0:100221 und 100223 läuft unter der Naht am Ostrand von 300001 (etwa x 33–45, y 500–560) weiter und ist dort nicht eigenes Segment (Grenzfrage, keine Klassenfrage).",
        "r1c0:300070: die obersten etwa 7 Bildpunkte (x 334–346, y 500–507) sind dunkel und gehören nach dem Bild zum Fleck r0c0:100225 bzw. zum dunklen Rand, nicht zum hellen Feldweg (Grenzfrage, keine Klassenfrage).",
    ],
    "nicht_geprueft": [],
}

with open(OUT, "w", encoding="utf-8") as f:
    json.dump(abgabe, f, ensure_ascii=False, indent=1)
print("geschrieben", len(abgabe["paare"]))
