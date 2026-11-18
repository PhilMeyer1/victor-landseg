from werk import *

KLASSEN.update({
    "Grünfläche": ("mittel", "Freifläche", "mittelgraue, weich gemusterte Fläche ohne Gebäude, von Wegen umgeben"),
    "Anger (Gras)": ("fein", "Grünfläche", "kleine Grasinsel in der Straßengabel mit einzelnen Bäumen"),
})
O = H0 + "/b-kategorien-frei/urteil/r0c1/v4"
V = VB + "/v4"
UN, UR, UK = V + "/uebersicht_nummern.jpg", V + "/uebersicht_roh.jpg", V + "/uebersicht_kontrast.jpg"
N1, N2, N3, N4 = [V + f"/nah{i}_nummern.jpg" for i in (1, 2, 3, 4)]
R1, R2, R3, R4 = [V + f"/nah{i}_roh.jpg" for i in (1, 2, 3, 4)]
o = lambda n: O + "/" + n
reg = {int(k): v for k, v in json.load(open(o("regionen_v4.json"))).items()}
nach = {(v["von"], v["region"]): k for k, v in reg.items()}
B63 = [UN, UK, N2, N4, o("probe_63.jpg"), o("nah_4.jpg"), o("kontrast_2.jpg")]
BU = [UN, N4, R4, o("nah_2.jpg"), o("probe_105.jpg"), o("nah_4.jpg")]
DACH = ("Bebaut", "Gebäude", "Wohnhaus, helles Dach")
E = []


def e(id, was, frei, sicher, urteil="sauber", punkte=(), bilder=B63):
    E.append(dict(id=id, was=was, frei=frei, sicher=sicher, urteil=urteil, punkte=list(punkte), bilder=bilder))


def lage(nid):
    x0, y0, x1, y1 = reg[nid]["bbox"]
    return f"x {x0}–{x1}, y {y0}–{y1}"


e(200069, "Helle Fläche am Nordrand der Straße 51 am oberen Rand von v4: Teil der Fahrbahn.", STR, False,
  bilder=[UN, N2, R2, o("nah_4.jpg")])
e(200071, "Dunkle, gleichmäßig fleckige Fläche mit feinen Linien zwischen Gasse, Einmündung 67 und Straße 51: Garten (Beete oder Obstbäume); kein klarer Hell-dunkel-Rand, darum nicht geteilt.",
  ("Freifläche", "Garten", "Garten, fein gemustert"), False, bilder=[UN, N1, R1, o("kontrast_1.jpg"), o("probe_71.jpg")])
e(200051, "Fahrbahn der Straße 51 (Südwest–Nordost), hell und gleichmäßig.", STR, True, bilder=[UN, UR, N1, N2, o("nah_3.jpg"), o("nah_4.jpg")])
e(200079, "Mittelgrauer Streifen am Südostrand der Straße 51 vor den Hausgiebeln: Randstreifen oder Vorgarten.", RAND, False,
  bilder=[UN, N2, o("nah_3.jpg")])
e(200076, "Heller Fleck am Südostrand der Straße 51 vor einem Hausgiebel.", RAND, False, bilder=[UN, N2, o("nah_3.jpg")])
e(200077, "Heller Fleck am Nordende eines Dachstreifens an der Straße: Giebel oder Straßenrand.", RAND, False,
  bilder=[UN, N2, o("nah_3.jpg")])
e(200075, "Kleiner mittelgrauer Fleck zwischen zwei Giebeln an der Straße 51: Hofeinfahrt.", HOF, False, bilder=[UN, N2, o("nah_3.jpg")])
e(200082, "Mittelgraue bis helle Fläche an der Gabelung der Straßen 49 und 51: Straßenrand.", RAND, False,
  bilder=[UN, N1, o("nah_4.jpg")])
e(200083, "Kleiner mittelgrauer Fleck am Südrand der Straße 51: Randstreifen.", RAND, False, bilder=[UN, N1, o("nah_3.jpg")])
e(200080, "Kleiner dunkler Fleck am Südrand der Straße 51: Schatten oder Strauch.", SCH, False, bilder=[UN, N1, o("nah_3.jpg")])
e(200098, "Schmaler mittelgrauer Streifen zwischen Straße 49 und dem Anger 97: Straßenrand.", RAND, False,
  bilder=[UN, N3, o("nah_1.jpg")])
e(200095, "Helle Fahrbahn der Straße, die vom Anger nach Süden führt.", STR, True, bilder=[UN, N3, R3, o("nah_1.jpg")])
e(200091, "Kleiner mittelgrauer Fleck an der Gabelung: Straßenrand.", RAND, False, bilder=[UN, N1, o("nah_1.jpg")])

T63 = {
    1: ("Dunkles Schattenband rechts oben.", SCH, False),
    2: ("Dunkles Schattenband rechts oben.", SCH, False),
    3: ("Großes dunkles Schattenband zwischen den östlichen Dachstreifen.", SCH, False),
    4: ("Dunkles Schattenband zwischen den Dachstreifen 373 und 364.", SCH, False),
    5: ("Großes dunkles Schattenband zwischen den Dachstreifen der Blockmitte.", SCH, False),
    6: ("Dunkle Insel im hellgrauen Rahmen 361: Schatten in einem Hof oder dunkles Dach.", SCH, False),
    7: ("Dunkle Fläche in der Südwestecke des Blocks: Schatten oder Garten.", SCH, False),
    8: ("Dunkles Schattenband zwischen den Dachstreifen 366 und 368 bis an die untere Kerngrenze.", SCH, False),
    9: ("Kleiner dunkler Fleck im Hof 377: Schatten oder Strauch.", SCH, False),
    10: ("Dunkle Fläche im Süden zwischen den Dachstreifen: Schatten.", SCH, False),
    11: ("Kleine mittelgraue Fläche an der Straße 51 neben dem Querbau 379: Hofeinfahrt.", HOF, False),
    12: ("Mittelgrauer Rahmen um die dunkle Insel 378: Dachkanten eines Gebäudes oder Hof.", HALB, False),
    13: ("Kleiner mittelgrauer Streifen am rechten Kernrand.", HALB, False),
    14: ("Kleine mittelgraue Fläche an der Straße 51: Hofeinfahrt.", HOF, False),
    15: ("Kleiner mittelgrauer Streifen rechts.", HALB, False),
    16: ("Mittelgrauer Streifen zwischen den Dachstreifen rechts: Dachseite oder Hof.", HALB, False),
    17: ("Kleiner mittelgrauer Fleck rechts.", HALB, False),
    18: ("Kleiner mittelgrauer Fleck im Schatten links.", HALB, False),
    19: ("Mittelgraue Fläche hinter den Häusern im Südosten: Hof.", HOF, False),
    20: ("Mittelgrauer Streifen zwischen den Dachstreifen der Blockmitte: Dachseite oder Hof.", HALB, False),
    21: ("Mittelgrauer Streifen zwischen den Dachstreifen der Blockmitte: Dachseite oder Hof.", HALB, False),
    22: ("Mittelgraue Fläche im Südwesten: Hof.", HOF, False),
    23: ("Kurzer heller Streifen am rechten Kernrand: Dach.", GEB, False),
    24: ("Kurzer heller Dachstreifen oben.", GEB, True),
    25: ("Heller Dachstreifen eines Langhauses rechts oben.", GEB, True),
    26: ("Heller rechteckiger Block an der Straße 51 am Kopf der Häuserzeile: Querbau.", ("Bebaut", "Gebäude", "Querbau an der Straße"), True),
    27: ("Heller Dachstreifen eines Langhauses rechts.", GEB, True),
    28: ("Langer heller Dachstreifen eines Langhauses rechts.", GEB, True),
    29: ("Langer heller Dachstreifen eines Langhauses.", GEB, True),
    30: ("Sehr heller langer Dachstreifen eines Langhauses.", GEB, True),
    31: ("Langer heller Dachstreifen von der Straße 51 nach Südosten.", GEB, True),
    32: ("Sehr heller langer Dachstreifen eines Langhauses.", GEB, True),
    33: ("Heller langer Dachstreifen eines Langhauses.", GEB, True),
    34: ("Helle Fläche in der Südwestecke des Blocks mit Binnenstruktur: Dächer und heller Hof.", DACH, False),
    35: ("Kleiner heller Fleck im Hof 360.", DACH, False),
    36: ("Helle Fläche unten rechts am Südende der Dachstreifen: Dach oder Hof.", DACH, False),
    37: ("Mittelhelle Fläche am unteren Kernrand: Hof.", HOF, False),
}
for j in sorted(T63):
    nid = nach[(200063, j)]
    was, frei, s = T63[j]
    e(nid, f"{was} ({lage(nid)})", frei, s, bilder=B63)
e(200343, "Kontextteil von 63 rechts und unten außerhalb des Kerns; im Kern nur der Bildpunkt x 563, y 550 am Ende eines hellen Dachstreifens.",
  GEB, False, bilder=[UN, o("nah_4.jpg"), o("probe_63.jpg")])

e(200097, "Mittelgraue Dreiecksfläche zwischen Straße 49 und der Straße nach Süden mit hellem Innenrand: Grasfläche des Angers.",
  ("Freifläche", "Grünfläche", "Anger (Gras)"), False, bilder=[UN, N3, R3, o("nah_1.jpg")])
e(200116, "Kleiner heller Fleck an der Südspitze des Angers: Weg oder Straßenrand.", RAND, False, bilder=[UN, N3, o("nah_1.jpg")])
e(200109, "Kleiner heller Fleck der Fahrbahn an der Südspitze des Angers.", STR, False, bilder=[UN, N3, o("nah_1.jpg")])
e(200114, "Sehr dunkle, eckige Fläche am Südende der Dachstreifen: Schlagschatten eines Gebäudes.", SCH, False, bilder=BU)
e(200108, "Heller Block mit dunkler Binnenlinie am Südrand: Gebäude mit hellem Dach, eventuell zwei Dächer.", DACH, False, bilder=BU)
e(200105, "Nach dem Teilen der dunkle Teil (" + lage(200105) + "): Schatten zwischen zwei Dachenden.", SCH, False, bilder=BU)
e(nach[(200105, 2)], "Heller Dachstreifen am Südende eines Langhauses (" + lage(nach[(200105, 2)]) + ").", GEB, False, bilder=BU)
e(200107, "Nach dem Teilen der dunkle Rest am rechten Kernrand (" + lage(200107) + "): Schatten.", SCH, False, bilder=BU)
e(nach[(200107, 2)], "Sehr heller Dachstreifen am Südende eines Langhauses (" + lage(nach[(200107, 2)]) + ").", GEB, True, bilder=BU)
e(200122, "Kleiner mittelgrauer Fleck an der unteren linken Ecke von v4: Straßenrand.", RAND, False, bilder=[UN, N3, o("nah_1.jpg")])
e(200112, "Mittelhelle Fläche am unteren Kernrand südlich der Dachstreifen: Hof.", HOF, False, bilder=BU)
e(200111, "Helle, rundlich begrenzte Fläche am unteren Kernrand: heller Hof oder flaches Gebäude.", HOF, False, bilder=BU)
e(200124, "Dunkelgraue Fläche am unteren Kernrand: Schatten.", SCH, False, bilder=BU)
e(200123, "Kleine dunkelgraue Fläche am unteren Kernrand: Schatten.", SCH, False, bilder=BU)
e(200110, "Helle Fahrbahn der Straße am unteren Rand (Ost–West), überwiegend jenseits der Kerngrenze.", STR, True, bilder=BU)
e(200125, "Zwei Bildpunkte in der rechten unteren Kernecke, dunkelgrau: Schatten.", SCH, False, bilder=BU)

uebersicht = [H0 + "/H0.png", H0 + "/ganz/H0_raster.jpg", H0 + "/ganz/r0c1/ganz_nummern.jpg", H0 + "/ganz/r0c1/ganz_roh.jpg",
              UN, UR, V + "/uebersicht_vorschlag.jpg", V + "/uebersicht_maengel.jpg", UK, V + "/uebersicht_gitter.jpg"]
nah = [N1, R1, N2, R2, N3, R3, N4, R4] + [o(n) for n in ("nah_1.jpg", "nah_2.jpg", "nah_3.jpg", "nah_4.jpg", "kontrast_1.jpg",
                                                         "kontrast_2.jpg", "probe_63.jpg", "probe_71.jpg", "probe_105.jpg")]
naht = []
for nid, r in sorted(reg.items()):
    if r["naht_unten"]:
        naht.append({"id": nid, "seite": "unten", "text": "Teilstück reicht an die untere Kerngrenze y 563; jenseits (r1c1) ist 63 ungeteilt."})
naht += [{"id": 200110, "seite": "unten", "text": "Straße am unteren Rand läuft über die Kerngrenze; gleiche Klasse Straße."},
         {"id": 200095, "seite": "unten", "text": "Straße nach Süden läuft über die Kerngrenze; gleiche Klasse Straße."},
         {"id": 200097, "seite": "unten", "text": "Anger-Dreieck reicht über die Kerngrenze; gleiche Klasse beiderseits nötig."}]
unsicher = ["200067 (Viertel v3): Einmündung, an 69 und 51 ohne Kante; gleiche Klasse Straße.",
            "200049 (Viertel v3): Fahrbahn neben dem Anger 97 und 98."]
nicht_geprueft = ["Kontextrand rechts (x > 563, außerhalb von H0) und unten (y > 563) nur angesehen.",
                  "Werkzeug kante nicht benutzt; neue Grenzen aus der Wasserscheide auf dem Grauwert-Gradienten."]
offen = ["Schattenbänder in 63 (Klasse Schatten zwischen Häusern) enthalten wohl Schattenseite des Daches und Schlagschatten; Farbbild oder Stereo entscheidet.",
         "Halbschatten-Teile (Dachseite oder Hof): Farbbild entscheidet.",
         "71: Garten oder dunkle Dachfläche; im Farbbild Grün gegen Dach prüfen.",
         "97: Anger als Grasfläche angenommen, die helle Binnenlinie kann ein Weg oder Zaun sein.",
         "111, 108, 112: heller Hof oder flaches Gebäude; Farbbild entscheidet.",
         "63 steht nach dem Teilen nicht mehr auf der Karte (das Werkzeug gab beim Zerfall dem jeweils größten Stück die alte ID, das später überschrieben wurde); der Kontextteil rechts und unten trägt jetzt 200343 (im Kern 1 Bildpunkt), der Kontextteil unter dem Teil 37 die ID " + str(nach[(200063, 37)]) + ".",
         "Die neuen IDs tragen in segmente.json kein Feld im_kern und den Code des geteilten Segments; die Klasse steht nur hier."]
n63 = sorted([nach[(200063, j)] for j in T63] + [200343])
eingriffe = [
    {"schritt": "polygon_zuweisen", "vorher": [200063], "nachher": n63,
     "grund": "63 fasste die ganze Häuserzeile südlich der Straße 51 (36 113 Bildpunkte im Kern) zusammen; an den Hell-dunkel-Kanten in 37 Teile zerlegt (Dachstreifen, Querbau, Schatten, Halbschatten, Höfe)."},
    {"schritt": "polygon_zuweisen", "vorher": [200105], "nachher": [200105, nach[(200105, 2)]],
     "grund": "105 umfasste ein helles Dachende und einen dunklen Schatten; an der scharfen Kante getrennt."},
    {"schritt": "polygon_zuweisen", "vorher": [200107], "nachher": [200107, nach[(200107, 2)]],
     "grund": "107 umfasste einen sehr hellen Dachstreifen und einen dunklen Schatten; an der scharfen Kante getrennt."}]
kf = klassen_frei_liste(E)
urteil_schreiben(O, "v4", E, uebersicht, nah, naht, unsicher, nicht_geprueft, offen, eingriffe, kf, 314, 314)
print(len(E), "Einträge", sum(1 for x in E if not x["sicher"]), "unsicher",
      sum(1 for x in E if x["urteil"] == "nicht_sauber"), "nicht sauber", sum(len(x["punkte"]) for x in E), "Punkte")
