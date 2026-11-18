from werk import *


O = H0 + "/b-kategorien-frei/urteil/r0c1/v2"
V = VB + "/v2"
UN, UR, UK = V + "/uebersicht_nummern.jpg", V + "/uebersicht_roh.jpg", V + "/uebersicht_kontrast.jpg"
N1, N2, N3, N4 = [V + f"/nah{i}_nummern.jpg" for i in (1, 2, 3, 4)]
R1, R2, R3, R4 = [V + f"/nah{i}_roh.jpg" for i in (1, 2, 3, 4)]
o = lambda n: O + "/" + n

# Ansichten nach dem Teilen
ansicht(o("nah_6.jpg"), 290, 60, 275, 200, 4, titel="nah_6: 16, 7, 39 nach dem Teilen, Nordost (Nummer = ID mod 100000)")
ansicht(o("nah_7.jpg"), 118, 100, 300, 290, 3, titel="nah_7: 16 nach dem Teilen, Südwest und Süd (Nummer = ID mod 100000)")

reg = {int(k): v for k, v in json.load(open(o("regionen_v2.json"))).items()}
nach = {(v["von"], v["region"]): k for k, v in reg.items()}
B16 = [UN, UR, o("probe_16.jpg"), o("nah_6.jpg"), o("nah_7.jpg"), o("kontrast_1.jpg"), o("kontrast_2.jpg"), o("kontrast_3.jpg")]
B7 = [UN, N2, R2, o("nah_2.jpg"), o("kontrast_4.jpg"), o("probe_7.jpg"), o("nah_6.jpg")]
B39 = [UN, N4, o("nah_3.jpg"), o("kontrast_5.jpg"), o("probe_39.jpg"), o("nah_6.jpg")]

E = []


def e(id, was, frei, sicher, urteil="sauber", punkte=(), bilder=B16):
    E.append(dict(id=id, was=was, frei=frei, sicher=sicher, urteil=urteil, punkte=list(punkte), bilder=bilder))


def lage(nid):
    r = reg[nid]; x0, y0, x1, y1 = r["bbox"]
    return f"x {x0}–{x1}, y {y0}–{y1}"


# --- Liste des Auftrags, in dieser Reihenfolge ---
e(200021, "Kleiner heller Rest der Fahrbahn an der Einmündung der Straße 5 neben dem hellen Block 17; nur 27 Bildpunkte im Kern.",
  STR, False, bilder=[UN, N1, o("nah_5.jpg")])
e(200017, "Heller, scharf begrenzter Block am oberen Kernrand am Kopf der Straße 5, mit dunklem Schatten südöstlich: wohl Gebäude mit hellem Dach, helles Pflaster nicht ausgeschlossen.",
  ("Bebaut", "Gebäude", "Wohnhaus, helles Dach"), False, bilder=[UN, N1, o("nah_5.jpg")])
e(200018, "Fünf Bildpunkte am Südwestrand der Straße 12 am oberen Kernrand.", STR, False, bilder=[UN, N1, o("nah_5.jpg")])
e(200026, "Mittelgrauer Fleck zwischen Straße 12 und den Häusern von 16 (x 420–450, y 83–106): Vorgarten oder Hofeinfahrt.",
  HOF, False, bilder=[UN, N1, o("nah_5.jpg"), o("nah_2.jpg")])
e(200007, "Nach dem Teilen der Kernteil des dunklen Schattens im Block nordöstlich der Straße 12 (" + lage(200007) + "); Kontextteil oben unverändert.",
  SCH, False, bilder=B7)
e(200034, "Schmaler mittelgrauer Streifen am Südwestrand der Straße 12 zwischen Fahrbahn und Hausgiebeln.", RAND, False,
  bilder=[UN, N2, R2, o("nah_2.jpg")])
e(200012, "Fahrbahn der Straße 12 (Nordwest–Südost) mit Abzweig nach Osten, hell und gleichmäßig.", STR, True,
  bilder=[UN, UR, N2, R2, o("nah_2.jpg"), o("kontrast_4.jpg")])
e(200030, "Helle, leicht fleckige Fläche nordöstlich der Straße 12 vor den Häusern: Vorplatz oder befestigter Hof.",
  ("Verkehrsfläche", "Platz", "Vorplatz"), False, bilder=[UN, N2, R2, o("nah_2.jpg"), o("kontrast_4.jpg")])
e(200029, "Mittelgraue, unruhige Fläche östlich des Vorplatzes 30 (Kernteil x 492–563): Hof oder Garten.", HOF, False,
  bilder=[UN, N2, R2, o("nah_2.jpg"), o("kontrast_4.jpg")])

# Teile von 16 (Reihenfolge nach Region)
T16 = {
    1: ("Dunkles Schattenband zwischen den Langhäusern oben (Nordteil des Blocks).", SCH, False),
    2: ("Großes dunkles Schattenband zwischen den östlichen Langhäusern bis an die Gasse.", SCH, False),
    3: ("Dunkles Schattenband zwischen den Dachstreifen 43 und 41.", SCH, False),
    4: ("Dunkler Streifen am Südwestrand der Straße 12 vor den Höfen: Schatten, ein Graben ist nicht ausgeschlossen.", SCH, False),
    5: ("Großes dunkles Schattenband zwischen den Langhäusern der Blockmitte (um das helle Nebengebäude 59).", SCH, False),
    6: ("Dunkles Schattenband zwischen den Dachstreifen 48 und 46.", SCH, False),
    7: ("Dunkles Schattenband zwischen den Dachstreifen 50 und 48.", SCH, False),
    8: ("Große dunkle, fleckige Fläche am Südende der Grundstücke vor der Gasse: Hausgärten mit Bäumen und Schatten.", ("Freifläche", "Garten", "Garten, dunkel (Bäume oder Schatten)"), False),
    9: ("Dunkles Schattenband zwischen den Dachstreifen 51 und 50.", SCH, False),
    10: ("Dunkle Fläche östlich am Hof (x 519–554): Schatten eines Gebäudes oder Baumkrone.", SCH, False),
    11: ("Große dunkle, fleckige Fläche am Südwestende der Grundstücke an der Straße 49: Gärten mit Schatten.", ("Freifläche", "Garten", "Garten, dunkel (Bäume oder Schatten)"), False),
    12: ("Dunkles Schattenband östlich des langen Dachstreifens 59 im Block südlich der Gasse.", SCH, False),
    13: ("Dunkles Schattenband links neben Dachstreifen 51.", SCH, False),
    14: ("Dunkle, fleckige Fläche westlich des Dachstreifens 59 südlich der Gasse: Schatten oder Garten.", SCH, False),
    15: ("Große mittelgraue Fläche zwischen den östlichen Häusern und der Straße 12; im Kontrastbild parallele Bänder mit dunklen Linien: Dächer im Halbschatten oder Höfe.", HALB, False),
    16: ("Mittelgraue Fläche zwischen Hausgiebeln und Straße 5 (Nordwestecke des Blocks): Hof oder Vorgarten.", HOF, False),
    17: ("Mittelgraue Bänder zwischen Schatten 2 und Fläche 15: Dachseiten oder Höfe.", HALB, False),
    18: ("Kleine mittelgraue Insel im Schatten 3.", HALB, False),
    19: ("Kleine mittelgraue Insel zwischen Schatten und Dachstreifen 49.", HALB, False),
    20: ("Kleine mittelgraue Insel im Schatten 5.", HALB, False),
    21: ("Mittelgrauer Streifen neben Dachstreifen 49: Dachseite oder Hof.", HALB, False),
    22: ("Mittelgraue Fläche östlich am Hof bei 44 (x 500–532): Hof.", HOF, False),
    23: ("Mittelgraue Fläche am Nordostende der Gasse: Hof.", HOF, False),
    24: ("Mittelgrauer Streifen zwischen den Dachstreifen 43 und 41: Dachseite oder Hof.", HALB, False),
    25: ("Mittelgraue, fleckige Fläche am Südwestende der Grundstücke: Garten.", ("Freifläche", "Garten", "Garten"), False),
    26: ("Kleine mittelgraue Fläche am Westrand des Blocks (x 123–141).", HALB, False),
    27: ("Mittelgrauer Streifen zwischen Schatten 5 und Dachstreifen 46: Dachseite oder Hof.", HALB, False),
    28: ("Mittelgraue Fläche südöstlich der Gasse: Hof.", HOF, False),
    29: ("Mittelgrauer Streifen neben dem hellen Nebengebäude 191: Dachseite oder Hof.", HALB, False),
    30: ("Große mittelgraue, fleckige Fläche südlich der Gasse vor dem Garten 58: Hof oder Garten.", ("Freifläche", "Garten", "Garten"), False),
    31: ("Mittelgraue, fleckige Fläche westlich des langen Dachstreifens 59: Garten oder Hof.", ("Freifläche", "Garten", "Garten"), False),
    32: ("Mittelgraue Fläche östlich des Schattens 12: Hof.", HOF, False),
    33: ("Kleine mittelgraue Fläche am Südwestende der Gasse.", HOF, False),
    34: ("Mittelgraue fleckige Fläche zwischen Schatten 11 und Querbau 50: Garten.", ("Freifläche", "Garten", "Garten"), False),
    35: ("Mittelgraue fleckige Fläche am Südrand der Gärten: Garten.", ("Freifläche", "Garten", "Garten"), False),
    36: ("Mittelgraue Fläche am Südende des Blocks südlich der Gasse (y 357–380): Garten oder Hof.", ("Freifläche", "Garten", "Garten"), False),
    37: ("Heller Dachstreifen eines Langhauses im Nordteil.", GEB, True),
    38: ("Kurzer heller Dachstreifen oben.", GEB, True),
    39: ("Heller Dachstreifen eines Langhauses oben links.", GEB, True),
    40: ("Kurzer heller Dachstreifen oben.", GEB, True),
    41: ("Langer heller Dachstreifen eines Langhauses bis zur Gasse.", GEB, True),
    42: ("Kleiner heller Fleck am Südwestrand der Straße 12: Straßenrand.", RAND, False),
    43: ("Heller Dachstreifen eines Langhauses (Mitte).", GEB, True),
    44: ("Sehr helles, großes Dach (etwa 40 × 9 m) mitten im Block: Halle oder Scheune mit hellem Dach.", ("Bebaut", "Gebäude", "Halle oder Scheune, helles Dach"), True),
    45: ("Heller Dachstreifen eines Langhauses an der Straße 5.", GEB, True),
    46: ("Langer heller Dachstreifen eines Langhauses.", GEB, True),
    47: ("Kleiner heller Fleck in der Fläche 15: Gegenstand oder Lichtfleck.", ("Unklar", "Unklar", "heller Fleck im Hof"), False),
    48: ("Langer heller Dachstreifen eines Langhauses.", GEB, True),
    49: ("Heller Dachstreifen eines Langhauses nahe der Gasse.", GEB, True),
    50: ("Langer heller Dachstreifen mit hellem Querbau am Südende (Scheune quer zum Langhaus).", GEB, True),
    51: ("Heller Dachstreifen eines Langhauses links.", GEB, True),
    52: ("Helle, ebene Fläche südöstlich der Gasse ohne Schattenwurf: befestigter Hof.", HOF, False),
    53: ("Heller Dachstreifen eines Langhauses am Westrand.", GEB, True),
    54: ("Kleiner heller Dachstreifen eines Nebengebäudes südlich der Gasse.", ("Bebaut", "Gebäude", "Nebengebäude, helles Dach"), False),
    55: ("Kleiner heller Fleck im Hof südlich der Gasse.", HOF, False),
    56: ("Schmale helle Gasse (etwa 3–4 m), die den Block von Südwest nach Nordost quert; Nordwestkante klar, Südostkante weich.", ("Verkehrsfläche", "Weg", "Gasse"), True),
    57: ("Kleiner heller Fleck an der Gasse: Hof oder Gassenrand.", HOF, False),
    58: ("Kleiner heller Fleck an der Gasse: Hof oder Gassenrand.", HOF, False),
    59: ("Langer heller Dachstreifen mit Querbau an der Gasse (L-förmig) südlich der Gasse; der Querbau ist weich begrenzt.", GEB, True),
    60: ("Dunkles Endstück der Gasse am Südwestrand, im Schatten.", ("Verkehrsfläche", "Weg", "Gasse"), False),
}
for j in sorted(T16):
    nid = nach[(200016, j)]
    was, frei, s = T16[j]
    e(nid, f"{was} ({lage(nid)})", frei, s, bilder=B16)

e(200046, "Heller, rundlicher Fleck (etwa 7 m) ohne erkennbaren Schatten im Hof westlich von 50: Baumkrone oder kleiner Schuppen.",
  ("Unklar", "Unklar", "heller runder Fleck"), False, bilder=[UN, N4, o("nah_3.jpg"), o("kontrast_5.jpg")])
e(200050, "Dunkle, fleckige Fläche im Hof: Gebüsch oder Baumgruppe.", ("Gehölz", "Baum oder Strauch", "Gebüsch"), False,
  bilder=[UN, N4, o("nah_3.jpg"), o("kontrast_5.jpg")])
e(200036, "Große, sehr dunkle Fläche östlich der Kreuzung (Kernteil x 532–563): Schatten hoher Gebäude oder dichte Baumgruppe.",
  ("Schatten", "Schlagschatten", "Schatten oder Baumgruppe"), False, bilder=[UN, N2, o("nah_2.jpg"), o("nah_3.jpg")])
e(200045, "Kleiner dunkler Streifen östlich des hellen Blocks 44: dessen Schatten.", SCH, False,
  bilder=[UN, N2, o("nah_3.jpg"), o("kontrast_5.jpg")])
e(200059, "Heller, scharf begrenzter Block (etwa 20 × 9 m) mit Schatten an der Nordostseite: Gebäude mit hellem Dach.",
  ("Bebaut", "Gebäude", "Wohnhaus, helles Dach"), True, bilder=[UN, N3, R3, o("nah_1.jpg")])
e(200055, "Sehr dunkler, rundlicher Fleck im Hof (etwa 7 m): Baumkrone oder Schatten.", ("Gehölz", "Baum oder Strauch", "Baum"), False,
  bilder=[UN, N4, o("nah_3.jpg"), o("kontrast_5.jpg")])
e(200044, "Heller, rechteckiger Block mit scharfen Kanten und Schatten 45 an der Ostseite: Gebäude mit hellem Dach (kein Weg).",
  ("Bebaut", "Gebäude", "Nebengebäude, helles Dach"), False, bilder=[UN, N4, o("nah_3.jpg"), o("kontrast_5.jpg")])
T39 = {
    1: ("Dunkles Band zwischen Gebüsch 50 und Block 44: Schatten.", SCH, False),
    2: ("Dunkle Fläche am Südostende an der Straße 51: Schatten.", SCH, False),
    3: ("Mittelgraue Fläche am Südwestrand der Straße 12: Hof.", HOF, False),
    4: ("Mittelgraue Fläche zwischen Weg und Block 44: Hof.", HOF, False),
    5: ("Heller Fleck am Südwestrand der Straße 12: Hof oder Straßenrand.", HOF, False),
    6: ("Heller schmaler Streifen von Südwest nach Nordost, parallel zur Gasse: Hofweg.", ("Verkehrsfläche", "Weg", "Hofweg"), False),
    7: ("Helle Fläche am rechten Kernrand an der Straße 51: Hof oder Straßenrand.", HOF, False),
}
for j in sorted(T39):
    nid = nach[(200039, j)]
    was, frei, s = T39[j]
    e(nid, f"{was} ({lage(nid)})", frei, s, bilder=B39)
e(200058, "Große, gleichmäßig fein gemusterte, mittel- bis dunkelgraue Fläche (etwa 36 × 18 m) mit gezackter Kante zur Straße 51: Garten (Beete oder Obstgarten); ein dunkles Dach ist nicht ausgeschlossen.",
  ("Freifläche", "Garten", "Garten, fein gemustert"), False, bilder=[UN, N4, R4, o("nah_1.jpg"), o("kontrast_2.jpg"), o("nah_4.jpg")])
e(200064, "Dunkler schmaler Streifen zwischen Garten 58 und Straße 51: Hecke oder Schatten des Zauns.",
  ("Gehölz", "Baum oder Strauch", "Hecke"), False, bilder=[UN, N4, o("nah_4.jpg")])
e(200066, "Helle Fläche am Nordrand der Straße 51 an der rechten Kernkante: Straßenrand oder Einfahrt.", RAND, False,
  bilder=[UN, N4, o("nah_4.jpg")])
e(200070, "Kurzer heller Streifen am unteren Rand von v2 (x 440–456, y 304–322): Stück eines Dachstreifens.", GEB, False,
  bilder=[UN, N3, o("nah_4.jpg")])
e(200068, "Heller Fleck am Südrand der Straße 51 vor einem Langhaus: Giebel oder Hofeinfahrt.", ("Bebaut", "Gebäude", "Langhaus, Dach Sonnenseite"), False,
  bilder=[UN, N4, o("nah_4.jpg")])
T7 = {
    1: None,
    2: ("Dunkle Fläche oben rechts im Block 7: Schatten.", SCH, False),
    3: ("Dunkles Band neben dem hellen Dachstreifen 9 im Block 7: Schatten.", SCH, False),
    4: ("Dunkle Fläche am Ostrand des Blocks 7: Schatten oder dunkles Dach.", SCH, False),
    5: ("Mittelgraue fleckige Fläche im Block 7 (Westteil): Hof oder Garten.", ("Freifläche", "Garten", "Garten"), False),
    6: ("Mittelgraue fleckige Fläche im Block 7 (Ostteil) bis an den Vorplatz 30: Hof oder Garten.", ("Freifläche", "Garten", "Garten"), False),
    7: ("Mittelgrauer Streifen im Block 7: Hof.", HOF, False),
    8: ("Heller kleiner Block am rechten oberen Kernrand: Dach.", GEB, False),
    9: ("Heller Dachstreifen eines Langhauses im Block 7.", GEB, True),
}
for j in sorted(T7):
    if T7[j] is None: continue
    nid = nach[(200007, j)]
    was, frei, s = T7[j]
    e(nid, f"{was} ({lage(nid)})", frei, s, bilder=B7)

uebersicht = [H0 + "/H0.png", H0 + "/ganz/H0_raster.jpg", H0 + "/ganz/r0c1/ganz_nummern.jpg", H0 + "/ganz/r0c1/ganz_roh.jpg",
              UN, UR, V + "/uebersicht_vorschlag.jpg", V + "/uebersicht_maengel.jpg", UK, V + "/uebersicht_gitter.jpg"]
nah = [N1, R1, N2, R2, N3, R3, N4, R4] + [o(n) for n in (
    "nah_1.jpg", "nah_2.jpg", "nah_3.jpg", "nah_4.jpg", "nah_5.jpg", "nah_6.jpg", "nah_7.jpg", "kontrast_1.jpg",
    "kontrast_2.jpg", "kontrast_3.jpg", "kontrast_4.jpg", "kontrast_5.jpg", "probe_16.jpg", "probe_16a.jpg",
    "probe_16b.jpg", "probe_16c.jpg", "probe_7.jpg", "probe_39.jpg")]
naht = []
for nid, r in sorted(reg.items()):
    if r["naht_unten"]:
        naht.append({"id": nid, "seite": "unten", "text": "Teilstück reicht an die untere Kerngrenze (Naht zu r1c1)."})
unsicher = ["200063 (Viertel v4): Häuserzeile südlich der Straße 51, Sammelsegment wie 16.",
            "200051 (Viertel v4): Straße 51, an ihrem Nordrand liegen 64 und 66 ohne scharfe Kante.",
            "200049 (Viertel v3): Fahrbahn; Gärten 11 und 25 aus 16 grenzen an."]
nicht_geprueft = ["Kontextrand oben (y < 64) und rechts (x > 563) nur angesehen; er liegt außerhalb von H0, dort gibt es keine Naht.",
                  "Werkzeug kante nicht benutzt: die neuen Grenzen kommen aus einer Wasserscheide auf dem Grauwert-Gradienten (Marken aus Grautonklassen, für die Gasse eine Marke von Hand) und liegen auf den Hell-dunkel-Kanten; die Südostkante der Gasse ist weich und dort geschätzt."]
offen = ["Schattenbänder (Klasse Schatten zwischen Häusern) alle unsicher: bei Satteldächern mit Sonne aus Südwest ist die Nordostseite des Daches selbst dunkel; die dunklen Bänder sind breiter als die hellen Dachseiten und enthalten wohl Schattenseite des Daches plus Schlagschatten im Hof. Die Grenze zwischen beiden gibt der Scan nicht her; Farbbild oder Stereo entscheidet.",
         "Halbschatten-Teile (Dachseite oder Hof) und die großen mittelgrauen Flächen 15 und 17: im Kontrastbild parallele Bänder mit dunklen Linien, also eher Dächer mit Schattenseite als Höfe; Farbbild oder Stereo entscheidet.",
         "Gärten (dunkel, fleckig) gegen Schatten: am Südende der Grundstücke (Teile 8, 11, 14) liegen Bäume und Schlagschatten ineinander; das Farbbild trennt Grün von Schatten.",
         "58: Garten (Beete) oder großes dunkles Dach; im Farbbild Dachfarbe gegen Grün prüfen.",
         "36, 55, 50, 46: Baumkronen oder Schatten bzw. Schuppen; das Farbbild entscheidet.",
         "17, 44: helles Dach oder helles Pflaster; Schattenwurf spricht für Dach.",
         "Die Teile von 16 liegen auch in den Vierteln v1, v3 und v4; sie werden nur hier geurteilt (Segment der Liste v2). 16 selbst und 39 stehen nach dem Teilen nicht mehr auf der Karte: das Werkzeug gab beim Zerfall jeweils dem größten Stück die alte ID, die zuletzt überschrieben wurde; der Kontextteil von 16 (oben, außerhalb von H0) trägt jetzt die ID " + str(nach[(200016, 1)]) + ", der von 39 (rechts, außerhalb von H0) die ID " + str(nach[(200039, 2)]) + ".",
         "Die neuen IDs tragen in segmente.json kein Feld im_kern und als technischen Code den Code des geteilten Segments; die Klasse steht nur hier."]
n16 = sorted(nach[(200016, j)] for j in T16)
n39 = sorted(nach[(200039, j)] for j in T39)
n7 = sorted([200007] + [nach[(200007, j)] for j in T7 if T7[j]])
eingriffe = [
    {"schritt": "polygon_zuweisen", "vorher": [200016], "nachher": n16,
     "grund": "Segment 16 fasste den ganzen Häuserblock zwischen Straße 5, Straße 12 und Straße 51 samt Gasse, Höfen und Gärten zusammen (71 529 Bildpunkte); entlang der Hell-dunkel-Kanten in 60 Teile zerlegt (Dachstreifen, Schatten, Halbschatten, Höfe, Gärten, Gasse)."},
    {"schritt": "polygon_zuweisen", "vorher": [200007], "nachher": n7,
     "grund": "Kernteil von 7 (Block nordöstlich der Straße 12) umfasste Dach, Schatten und Gärten; an den Grauton-Kanten in 9 Teile zerlegt."},
    {"schritt": "polygon_zuweisen", "vorher": [200039], "nachher": n39,
     "grund": "39 umfasste Hofflächen, einen hellen Hofweg und zwei Schatten an der Kreuzung; an den Kanten in 7 Teile zerlegt."}]
kf = klassen_frei_liste(E)
urteil_schreiben(O, "v2", E, uebersicht, nah, naht, unsicher, nicht_geprueft, offen, eingriffe, kf, 314, 64)
print(len(E), "Einträge", sum(1 for x in E if not x["sicher"]), "unsicher",
      sum(1 for x in E if x["urteil"] == "nicht_sauber"), "nicht sauber", sum(len(x["punkte"]) for x in E), "Punkte")
