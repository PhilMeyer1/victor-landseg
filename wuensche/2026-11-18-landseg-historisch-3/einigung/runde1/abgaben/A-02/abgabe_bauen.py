"""Baut einigung_abgabe.json fuer Buendel A-02 aus den Entscheidungen unten (nur im Ergebnisordner)."""
import json
from pathlib import Path

HIER = Path(__file__).parent
AUFTRAG = Path("C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde1/auftraege-A/A-02/auftrag.json")

E = {
    1: ("grenze", None, "Heller Fahrbahnstreifen der Straße C und matter, etwas dunklerer Randstreifen daneben; zwei verschiedene Flächen, nur ein Randpunkt an der Viertellinie."),
    2: ("grenze", None, "Helles Band der Straße C gegen die dunklere Hoffläche des Blocks; deutlicher Helligkeitsunterschied entlang der Straßenkante."),
    3: ("grenze", None, "Grauer Dachstreifen mit dunkler Mitte (Haus B4 4) gegen die hellere offene Hoffläche daneben; verschiedene Flächen."),
    4: ("grenze", None, "Mittelgraue Dreiecksfläche (Garten) gegen das helle Straßenband, das an der Naht nach Südosten weiterläuft; verschiedene Flächen."),
    5: ("grenze", None, "Helles Straßenband rechts gegen die Hofstelle links; die Spitze von r0c0:100032 reicht an der Naht etwa 6 Bildpunkte in Straßenrand und Schatten hinein (Grenzlage, nicht Klasse)."),
    6: ("grenze", None, "Hofstelle (Höfe zwischen den Häusern) und Schlagschattenband sind verschiedene Flächen; das dunkle Schattenband läuft aber bei y 110–170 etwa 20 Bildpunkte über die Naht in r0c0:100032 hinein (Grenzlage, nicht Klasse)."),
    7: ("unklar", None, "Beidseits der Naht dieselbe dunkle Fläche im Schattenband; ob darunter Garten (r0c1) oder Hof (r0c0) liegt, ist im Scan nicht zu sehen."),
    8: ("gleich", "1.2", "Das kleine Hofstück rechts setzt die mittelgraue Hoffläche der Hofstelle links ohne Kante fort; gemeinsame Klasse Hofstelle ungetrennt, die Hof einschließt."),
    9: ("unklar", None, "Ecke zwischen Dachstreifen und Hofstück, nur 4 Randpunkte im Übergang von dunkel zu hell; Dachrand oder Hof ist nicht zu trennen."),
    10: ("gleich", "1.1", "Der hellgraue Dachstreifen von Haus B4 3 läuft ohne Kante und mit gleichem Grauton über die Naht weiter; beide Seiten lesen ihn als Gebäude, Untertyp über den Schnitt nicht sicher, daher Elternklasse."),
    11: ("gleich", "1.1", "Kleines Dachstück am Unterrand desselben grauen Dachstreifens, gleicher Ton ohne Kante; gleiche Kette wie Haus B4 3."),
    12: ("gleich", "1.1", "Schmaler heller Dachstreifen, der an der Unterecke von Haus B4 3 ohne Kante anschließt; gleiche Kette, Klasse Gebäude."),
    13: ("grenze", None, "Heller schmaler Dachstreifen rechts gegen die dunklere Fuge der Hofstelle links; Helligkeitsumschlag an der Stelle."),
    14: ("unklar", None, "Derselbe mittelgraue, lange Streifen läuft ohne Kante über die Naht; links als Hausdach, rechts als Garten gelesen, und ob es Dach oder Garten ist, gibt der Scan nicht her."),
    15: ("unklar", None, "Dasselbe mittelgraue Streifenstück beidseits der Naht; Dach (r0c0) oder Hof (r0c1) ist am Grauton nicht zu entscheiden."),
    16: ("gleich", "1.1", "Unterer Rand desselben grauen Streifens beidseits gleich hell und ohne Kante; beide Seiten lesen ihn als Gebäude, daher Elternklasse Gebäude."),
    17: ("unklar", None, "Kleines mittelgraues Stück am Unterrand des Streifens, nur 2 Randpunkte; Dach oder Garten nicht zu trennen."),
    18: ("unklar", None, "Ein Randpunkt zwischen der dunklen Fuge (Hofstelle) und einem mittelgrauen Fleck (Garten); welche Fläche es ist, gibt das Bild nicht her."),
    19: ("gleich", "1.2", "Mittelgraue offene Fläche läuft ohne Kante von der Hofstelle links in das Hofstück rechts; gemeinsame Klasse Hofstelle ungetrennt, die Hof einschließt."),
    20: ("unklar", None, "Beidseits dieselbe mittelgraue Fläche ohne Kante; links Teil von Haus B4 5, rechts Hof, und Dach oder Hof ist nicht zu entscheiden."),
    21: ("unklar", None, "Mittelgraue Fläche oberhalb des dunklen Flecks setzt sich ohne Kante fort; links Haus B4 5, rechts Garten, nicht zu entscheiden."),
    22: ("grenze", None, "Dunklerer Kronenrand links gegen die gleichmäßig mittelgraue Gartenfläche rechts; Helligkeitsunterschied am Rand des Baums."),
    23: ("unklar", None, "Zwei Randpunkte an einer Ecke im dunklen Fleck; ob dort Baumkrone oder ihr Schatten liegt, ist nicht zu trennen."),
    24: ("grenze", None, "Haus B4 5 und Schatten sind verschiedene Flächen; der dunkle Fleck an der Naht liegt aber links in r0c0:100090 mit drin und setzt sich rechts als Schatten fort (Grenzlage, nicht Klasse)."),
    25: ("unklar", None, "Ein Randpunkt an der Ecke zwischen dunkler Fuge und Schatten; beides dunkel, nicht zu trennen."),
    26: ("unklar", None, "Zwei Randpunkte an einer Ecke zwischen Fuge und einem winzigen Gebäudestück im Übergang zum dunklen Fleck; Fläche nicht deutbar."),
    27: ("gleich", "1.1", "Zwei winzige Gebäudestücke mit gleichem Grauton stoßen ohne Kante zusammen; beide Seiten lesen Gebäude."),
    28: ("unklar", None, "Derselbe helle schmale Streifen läuft ohne Kante über die Naht; links Weg (schon dort als Weg oder Hof beschrieben), rechts Hof, nicht zu entscheiden."),
    29: ("grenze", None, "Mittelgraue Fläche von Haus B4 6 gegen den hellen Streifen; Helligkeitsumschlag am Berührpunkt."),
    30: ("gleich", "1.2", "Beidseits dieselbe mittelgraue Fläche ohne Kante, links als Haus (fast nur Kontext), rechts als Hof gelesen; gemeinsame Klasse Hofstelle ungetrennt (Dach oder Hof)."),
    31: ("unklar", None, "Mittelgraues Stück an zwei Randpunkten; Hausfläche oder Garten nicht zu entscheiden."),
    32: ("unklar", None, "Dieselbe mittelgraue Fläche ohne Kante; links Hofstelle, rechts Garten, und Hof oder Garten ist im Scan nicht zu trennen."),
    33: ("gleich", "1.2", "Mittelgraue Hoffläche läuft ohne Kante von der Hofstelle links in das Hofstück rechts; gemeinsame Klasse Hofstelle ungetrennt."),
    34: ("gleich", "1.2", "Ein Randpunkt, beidseits dieselbe mittelgraue Hoffläche; gleiche Kette wie die Hofstelle Block B4 Teil 2."),
    35: ("gleich", "1.2", "Das Kernstück von Haus B4 7 an der Naht ist mittelgrau wie das Hofstück rechts, ohne Kante; das helle Dach liegt erst rechts davon, daher Hofstelle ungetrennt (Dach oder Hof)."),
    36: ("gleich", "1.2", "Dieselbe mittelgraue Fläche links vom hellen Dach von Haus B4 7 auf beiden Seiten; gemeinsame Klasse Hofstelle ungetrennt."),
    37: ("gleich", "1.2", "Mittelgraue Hoffläche zwischen hellen Dächern läuft auf 27 Randpunkten ohne Kante über die Naht; gemeinsame Klasse Hofstelle ungetrennt."),
    38: ("grenze", None, "Heller Längsbau-Streifen rechts gegen die Hofstelle; der helle Streifen läuft aber links als Aufhellung in r0c0:100033 weiter (Grenzlage, nicht Klasse; Hofstelle schließt Dach ein)."),
    39: ("gleich", "1.1", "Kernsplitter von Haus B4 8 und das Gebäudestück rechts haben denselben mittelhellen Ton ohne Kante; beide Seiten lesen Gebäude."),
    40: ("unklar", None, "Beidseits mittelgrau ohne klare Kante; ob das Stück rechts Dach oder Hof ist, ist nicht zu entscheiden."),
    41: ("gleich", "1.2", "Mittelgraue Hoffläche läuft ohne Kante über die Naht; gemeinsame Klasse Hofstelle ungetrennt."),
    42: ("grenze", None, "Mittelgraue Hofstelle links gegen die dunkle, nicht bestimmbare Fläche rechts; die Kante des dunklen Bandes liegt nahe an der Naht."),
    43: ("grenze", None, "Mittelgraue Hofstelle gegen einen dunklen Schattenfleck; Helligkeitsumschlag an der Stelle."),
    44: ("grenze", None, "Helle Straße C gegen die dunkle, nicht bestimmbare Fläche; ein Randpunkt an der Ecke."),
    45: ("grenze", None, "Helle Straße C gegen ein winziges Hofstück; die Straßenkante liegt knapp rechts der Naht."),
    46: ("grenze", None, "Helle Straße C gegen mittelgraue Hoffläche; die Straßenkante liegt wenige Bildpunkte rechts der Naht."),
    47: ("grenze", None, "Straße C und Schlagschatten sind verschiedene Flächen; der Schatten reicht wenige Bildpunkte in die Spitze von r0c0:100059 hinein (Grenzlage, nicht Klasse)."),
    48: ("unklar", None, "Zwei Randpunkte im dunklen Fleck am Ende der Baumreihe; Krone oder Schatten ist nicht zu trennen."),
    49: ("grenze", None, "Dunkle Hecken-/Grabenlinie gegen die helle, fleckige Brache; verschiedene Flächen."),
    50: ("grenze", None, "Streifenacker gegen helle fleckige Brache, getrennt von der dunklen Rainlinie; verschiedene Flächen."),
    51: ("grenze", None, "Gleichmäßiger Acker gegen die dunkle schmale Rain-/Grabenlinie; verschiedene Flächen."),
    52: ("gleich", "5.1", "Derselbe gleichmäßig dunkelgraue Acker läuft auf 58 Randpunkten ohne Kante über die Naht; Kette der Feldsegmente, gemeinsame Elternklasse Feld/Acker."),
    53: ("gleich", "5.1", "Gleichmäßig dunkelgraue Ackerfläche ohne Kante auf 184 Randpunkten; gleiche Kette, Klasse Feld/Acker."),
    54: ("grenze", None, "Ackerfläche oben gegen das dunkle Dach am Hof unten; deutliche Kante an der Oberkante des Gebäudes."),
    55: ("grenze", None, "Ackerfläche gegen den fast schwarzen Fleck neben dem Gebäude; deutlicher Helligkeitssprung."),
    56: ("grenze", None, "Acker und heller Zufahrtsweg sind verschiedene Flächen; der Weg setzt sich nördlich der Naht als heller Streifen in r0c0:100043 fort (Grenzlage, nicht Klasse)."),
    57: ("gleich", "5.1", "Beidseits derselbe mittel- bis dunkelgraue Ackerboden östlich des Wegs ohne Kante; gleiche Kette, Klasse Feld/Acker."),
    58: ("gleich", "5.1", "Die umrandete Ackerparzelle läuft auf 73 Randpunkten ohne Kante über die Naht; gleiche Kette, Klasse Feld/Acker."),
    59: ("grenze", None, "Ackerparzelle gegen die schmale dunkle Graben-/Rainlinie; die Linie scheint schwach nördlich der Naht in r0c0:100044 weiterzulaufen (Grenzlage, nicht Klasse)."),
    60: ("gleich", "5.1", "Derselbe Ackerstreifen der Parzelle 5 läuft ohne Kante über die Naht; gleiche Kette, Klasse Feld/Acker."),
    61: ("grenze", None, "Dunkle Baumreihe gegen den mittelgrauen Acker; drei Randpunkte an der Ecke."),
    62: ("unklar", None, "Beidseits dunkle Fläche am Fuß der Baumreihe; ob Krone oder Schatten, ist nicht zu trennen."),
    63: ("gleich", "0.1", "Beidseits derselbe dunkle Rand des Schlagschattens an der Kreuzung; kein Dach zu sehen, daher gemeinsam Schatten."),
    64: ("grenze", None, "Helle Fahrbahn gegen den dunklen Schattenrand; ein Randpunkt."),
    65: ("gleich", "3.1.1", "Dieselbe helle Fahrbahn läuft ohne Kante über die Naht; Straße zwischen den Höfen, daher Straße im Ort."),
    66: ("gleich", "3.1.1", "Dieselbe helle Fahrbahn auf 16 Randpunkten ohne Kante; gleiche Kette, Straße im Ort."),
    67: ("grenze", None, "Helle Fahrbahn gegen mittelgraue Fläche neben der Kreuzung; ein Randpunkt mit Helligkeitsumschlag."),
    68: ("unklar", None, "Beidseits dieselbe mittelgraue Fläche, nicht fahrbahnhell; links Straße, rechts Gebäude (nur nach Grauton), keines ist sicher."),
    69: ("gleich", "2.1", "Dieselbe flache mittelgraue Fläche ohne Kante; rechts nur nach Grauton als Gebäude eingestuft, ohne Dachkanten, daher gemeinsam Hof-/Freifläche."),
    70: ("grenze", None, "Dunkler Acker gegen helle, körnige Lagerfläche; deutlicher Helligkeitsunterschied."),
    71: ("grenze", None, "Dunkler Feldstreifen gegen die helle Landstraße; deutliche Kante."),
    72: ("grenze", None, "Dunklerer und hellerer Feldstreifen mit schräger Tongrenze; zwei Streifen, nur 2 Randpunkte an der Viertellinie."),
    73: ("grenze", None, "Mittelgrauer Acker gegen den schmalen Weg/Rain mit hellen und dunklen Rändern."),
    74: ("grenze", None, "Mittelgrauer Acker gegen den schmalen Weg/Rain; verschiedene Flächen."),
    75: ("gleich", "0.1", "Der dunkle Kernrand der Ortsrandfläche ist derselbe Schlagschatten, den die Nachbarkachel als Schatten führt; kein Gebäude zu sehen."),
    76: ("gleich", "0.1", "Beidseits derselbe dunkle Schattenrand ohne Kante; gleiche Kette wie der Schatten an der Kreuzung."),
    77: ("grenze", None, "Dunkler Schattenrand gegen die helle Landstraße; deutlicher Helligkeitssprung."),
    78: ("gleich", "3.1.2", "Dieselbe helle Landstraße zwischen den Feldern läuft ohne Kante über die Naht; Landstraße außerorts."),
}

OFFEN = [
    "Grenzkorrektur r0c0:100032/r0c1:200345 (Paar 6): Schlagschattenband reicht bei x≈478–500, y≈110–170 in die Hofstelle; Grenze müsste auf die Schattenkante, nicht die Klasse.",
    "Grenzkorrektur r0c0:100032/r0c1:200226 (Paar 5): Spitze der Hofstelle bei x≈494–500, y≈108–116 liegt auf Straßenrand und Schatten.",
    "Grenzkorrektur r0c0:100090/r0c1:200583 (Paar 24): dunkler Fleck (Krone oder Schatten) bei x≈490–500, y≈265–285 steckt im Haus B4 5.",
    "Grenzkorrektur r0c0:100033/r0c1:200876 (Paar 38): heller Längsbau-Streifen läuft westlich der Naht in der Hofstelle weiter.",
    "Grenzkorrektur r0c0:100059/r0c1:201159 (Paar 47): Schatten reicht wenige Bildpunkte in die Spitze der Straße C.",
    "Grenzkorrektur r0c0:100043/r1c0:300038 (Paar 56): Zufahrtsweg setzt sich nördlich der Naht (x≈300–330) als heller Streifen im Acker fort, in r0c0 nicht abgetrennt.",
    "Prüfen r0c0:100044/r1c0:300036 (Paar 59): Graben-/Rainlinie scheint schwach nördlich der Naht in der Parzelle weiterzulaufen.",
    "Hinweis r0c0:100051/r1c0:300032 (Paare 49–51): Hecke (6.2) und Rain/Graben (4.3) sind wohl dieselbe dunkle Linie, an der Naht um etwa 8–10 Bildpunkte versetzt; sie berühren sich nicht und sind kein Paar dieses Bündels.",
    "Streifen r0c0:100089 / r0c1:200415 (Paare 14–17): langer mittelgrauer Streifen, links Haus, rechts Garten/Hof; Dach oder Garten am Scan nicht entscheidbar (Ansicht einigung_14.jpg).",
]

a = json.loads(AUFTRAG.read_text(encoding="utf-8"))
paare = []
for p in a["paare"]:
    ent, kl, gr = E[p["nr"]]
    paare.append({"paar": p["paar"], "entscheidung": ent, "klasse": kl if ent == "gleich" else None, "grund": gr})
assert len(paare) == len(a["paare"]) == len(E)
codes = {c["code"] if isinstance(c, dict) else c for c in a["klassen"]}
for x in paare:
    if x["klasse"] is not None:
        assert x["klasse"] in codes, x

# Ketten pruefen: jede gleich-Komponente hat genau eine Klasse
eltern = {}
def f(u):
    while eltern.setdefault(u, u) != u:
        u = eltern[u]
    return u
for x in paare:
    if x["entscheidung"] == "gleich":
        s, t = x["paar"].split("|")
        eltern[f(s)] = f(t)
komp = {}
for x in paare:
    if x["entscheidung"] == "gleich":
        komp.setdefault(f(x["paar"].split("|")[0]), set()).add(x["klasse"])
for k, v in komp.items():
    assert len(v) == 1, (k, v)

out = {"schema": "landseg-einigung-abgabe/1", "fassung": "A", "buendel": "A-02",
       "bearbeiter": "agent:einigung-A-02:20261118i-r1", "paare": paare,
       "offen": OFFEN, "nicht_geprueft": []}
(HIER / "einigung_abgabe.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
from collections import Counter
print(len(paare), Counter(x["entscheidung"] for x in paare), "Komponenten", len(komp))
