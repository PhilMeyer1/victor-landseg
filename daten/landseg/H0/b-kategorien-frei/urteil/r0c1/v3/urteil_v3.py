from werk import *

KLASSEN.update({
    "Hof oder Dach, mittelgrau": ("fein", "Unklar", "mittelgraue Mischfläche aus Dächern und Höfen ohne trennbare Kante"),
    "Grünfläche": ("mittel", "Freifläche", "mittelgraue, weich gemusterte Fläche ohne Gebäude, von Wegen umgeben"),
    "Anger (Gras)": ("fein", "Grünfläche", "kleine Grasinsel in der Straßengabel mit einzelnen Bäumen"),
    "Schatten oder Baumreihe": ("fein", "Schlagschatten", "langes sehr dunkles Band mit unregelmäßiger Kante längs einer Straße"),
})
O = H0 + "/b-kategorien-frei/urteil/r0c1/v3"
V = VB + "/v3"
UN, UR, UK = V + "/uebersicht_nummern.jpg", V + "/uebersicht_roh.jpg", V + "/uebersicht_kontrast.jpg"
N1, N2, N3, N4 = [V + f"/nah{i}_nummern.jpg" for i in (1, 2, 3, 4)]
R1, R2, R3, R4 = [V + f"/nah{i}_roh.jpg" for i in (1, 2, 3, 4)]
o = lambda n: O + "/" + n
reg = {int(k): v for k, v in json.load(open(o("regionen_v3.json"))).items()}
nach = {(v["von"], v["region"]): k for k, v in reg.items()}
B47 = [UN, UK, N1, N3, o("probe_47.jpg"), o("nah_4.jpg"), o("kontrast_1.jpg")]
B74 = [UN, N2, o("nah_1.jpg"), o("probe_74.jpg"), o("nah_4.jpg")]
MISCH = ("Unklar", "Unklar", "Hof oder Dach, mittelgrau")
DACH = ("Bebaut", "Gebäude", "Wohnhaus, helles Dach")
E = []


def e(id, was, frei, sicher, urteil="sauber", punkte=(), bilder=B47):
    E.append(dict(id=id, was=was, frei=frei, sicher=sicher, urteil=urteil, punkte=list(punkte), bilder=bilder))


def lage(nid):
    x0, y0, x1, y1 = reg[nid]["bbox"]
    return f"x {x0}–{x1}, y {y0}–{y1}"


e(200054, "Sehr dunkles, unregelmäßig begrenztes Band längs der Westseite der Straße 49: Schatten einer Baumreihe oder hoher Häuser.",
  ("Schatten", "Schlagschatten", "Schatten oder Baumreihe"), False, bilder=[UN, UK, N1, R1, o("nah_4.jpg"), o("kontrast_1.jpg")])
e(200073, "Kleine mittelgraue Fläche, wo die Gasse auf die Straße trifft: Gassenende oder Hof.", HOF, False,
  bilder=[UN, N2, o("nah_1.jpg")])
e(200067, "Helle Fahrbahn der Einmündung zwischen Straße 49 und Straße 51.", STR, True, bilder=[UN, N2, R2, o("nah_1.jpg")])
e(200078, "Helle Fläche an der Ostseite der Straße 49 mit einem noch helleren schmalen Streifen: Straßenrand; der Streifen kann ein niedriger Bau sein.",
  RAND, False, "nicht_sauber",
  [("trennen", "Heller Streifen x 255–285, y 380–430 parallel zur Straße hebt sich vom mittelgrauen Rand ab: Gebäude oder Gehweg; ohne Farbbild nicht geteilt.", 270, 405, None)],
  [UN, N2, R2, o("nah_1.jpg")])
e(200074, "Nach dem Teilen der dunkle, scharf rechteckige Teil zwischen den Straßen (" + lage(200074) + "): Schattenseite eines Daches oder dunkles Dach.",
  SCH, False, bilder=B74)
for nid, (was, frei, s) in {
    nach[(200074, 2)]: ("Mittelgrauer Rest am Nordende des Blocks 74.", HALB, False),
    nach[(200074, 3)]: ("Heller langer Streifen an der Südwestseite des dunklen Teils 74: Sonnenseite desselben Daches oder Straßenrand.", GEB, False),
    nach[(200074, 4)]: ("Kleiner heller Dachstreifen östlich des dunklen Teils 74.", GEB, False),
}.items():
    e(nid, f"{was} ({lage(nid)})", frei, s, bilder=B74)

# Teile von 47
T47 = {
    1: ("Dunkle Fläche oben links an der Straße 81 und der linken Kerngrenze: Schatten.", SCH, False),
    2: ("Dunkles Band zwischen zwei Häusern an der linken Kerngrenze: Schatten.", SCH, False),
    3: ("Kleiner dunkler Fleck zwischen den Dächern 306 und 302: Schatten.", SCH, False),
    4: ("Dunkles Band nördlich des Dachs 302: Schatten.", SCH, False),
    5: ("Kleiner dunkler Streifen an der linken Kerngrenze: Schatten.", SCH, False),
    6: ("Dunkles Band zwischen den Dächern 302 und 304: Schatten.", SCH, False),
    7: ("Dunkle Fläche am Ostrand des Blocks neben dem Straßenschatten 54: Schatten oder Bäume.", SCH, False),
    8: ("Kleiner dunkler Fleck im Hof: Schatten oder Strauch.", SCH, False),
    9: ("Dunkles Band südlich des großen hellen Gebäudes: Schatten.", SCH, False),
    10: ("Breites dunkles, fleckiges Band quer durch den Block (y 440–524): Gärten mit Bäumen und Schatten.", ("Freifläche", "Garten", "Garten, dunkel (Bäume oder Schatten)"), False),
    11: ("Dunkle Fläche am Ostrand nahe der Straße 49: Schatten oder Baum.", SCH, False),
    12: ("Dunkle Fläche im Südosten am Straßenrand: Schatten oder Baum.", SCH, False),
    13: ("Kleine dunkle Fläche am unteren Kernrand: Schatten.", SCH, False),
    14: ("Mittelgraue Mischfläche oben links aus Dächern und Höfen.", MISCH, False),
    15: ("Kleine mittelgraue Fläche zwischen den Dächern oben.", MISCH, False),
    16: ("Mittelgraue Mischfläche an der linken Kerngrenze.", MISCH, False),
    17: ("Kleine mittelgraue Insel im Schatten.", MISCH, False),
    18: ("Große mittelgraue Mischfläche in der Blockmitte: Dächer mit Schattenseite und Höfe ohne trennbare Kante.", MISCH, False),
    19: ("Kleine mittelgraue Fläche am Ostrand.", MISCH, False),
    20: ("Mittelgraue Fläche am Ostrand des Blocks vor dem Straßenschatten: Hof.", HOF, False),
    21: ("Mittelgraue Fläche im großen Gebäude (dunkleres Innenfeld): Dachteil oder Innenhof.", MISCH, False),
    22: ("Mittelgraue Fläche am Ostrand: Hof.", HOF, False),
    23: ("Kleine mittelgraue Fläche nördlich der Gärten.", MISCH, False),
    24: ("Kleine mittelgraue Fläche nördlich der Gärten.", MISCH, False),
    25: ("Kleine mittelgraue Fläche im Garten an der linken Seite.", ("Freifläche", "Garten", "Garten"), False),
    26: ("Mittelgraue Fläche am Ostrand nahe der Straße: Hof.", HOF, False),
    27: ("Große mittelgraue Mischfläche im Südwesten des Blocks: Höfe und Dächer.", MISCH, False),
    28: ("Kleine mittelgraue Fläche am Ostrand.", MISCH, False),
    29: ("Mittelgraue Fläche zwischen den hellen Dächern 294 im Süden: Hof.", HOF, False),
    30: ("Mittelgraue Mischfläche im Südosten bis an die untere Kerngrenze.", MISCH, False),
    31: ("Mittelhelle Fläche oben links an der Straße 81: Dach oder Hof.", DACH, False),
    32: ("Heller rechteckiger Dachblock oben links.", DACH, True),
    33: ("Heller Dachblock oben links (Ost-West gestellt).", DACH, True),
    34: ("Heller langer Dachstreifen (Ost-West) an der linken Kerngrenze.", DACH, True),
    35: ("Kleiner heller Fleck: Dachteil.", DACH, False),
    36: ("Kleiner heller Fleck: Dachteil.", DACH, False),
    37: ("Kleiner heller Streifen: Dachteil.", DACH, False),
    38: None,
    39: ("Kleiner heller Fleck im Hof: Dachteil oder Hof.", DACH, False),
    40: ("Heller langer Dachstreifen (Ost-West) südlich der Gärten.", DACH, True),
    41: ("Heller langer Dachstreifen (Ost-West) im Süden, mit angrenzendem hellem Hof.", DACH, True),
    42: ("Heller Streifen am unteren Kernrand: Dach.", DACH, False),
}
e(200047, "Nach dem Teilen die große helle Fläche in der Blockmitte (" + lage(200047) + "): ein sehr helles Gebäude (etwa 35 × 8 m) zusammen mit hellen Hofflächen; Grenze dazwischen ohne klare Kante.",
  DACH, False, "nicht_sauber",
  [("trennen", "Helles Gebäude x 120–200, y 395–430 und helle Hofflächen links davon gleich hell; ohne Kante nicht getrennt.", 160, 412, 6753)], B47)
for j in sorted(T47):
    if T47[j] is None: continue
    nid = nach[(200047, j)]
    was, frei, s = T47[j]
    e(nid, f"{was} ({lage(nid)})", frei, s, bilder=B47)

e(200090, "Schmaler heller Streifen am Westrand der Straße 49 vor dem Straßenschatten.", RAND, False, bilder=[UN, N2, o("nah_2.jpg")])
e(200096, "Kleiner Fleck am Westrand der Straße 49, dunkel mit hellem Rand: Strauch oder Pfosten mit Schatten.",
  ("Gehölz", "Baum oder Strauch", "Strauch am Straßenrand"), False, bilder=[UN, N2, o("nah_2.jpg")])
e(200084, "Heller Weg um die Grasinsel (Anger) herum, Teil der Fahrbahnfläche.", STR, False, bilder=[UN, N2, R2, o("nah_2.jpg")])
e(200085, "Dunkle, kompakte Fläche auf der Insel in der Straßengabel: Baumkrone mit Schatten.", ("Gehölz", "Baum oder Strauch", "Baum"), False,
  bilder=[UN, N2, R2, o("nah_2.jpg")])
e(200094, "Mittelgraue Fläche mit dunklen Flecken auf der Insel: Gras mit Sträuchern (Anger).", ("Freifläche", "Grünfläche", "Anger (Gras)"), False,
  bilder=[UN, N2, R2, o("nah_2.jpg")])
e(200089, "Mittelhelle Fläche am Südende der Insel: Gras oder Weg (Anger).", ("Freifläche", "Grünfläche", "Anger (Gras)"), False,
  bilder=[UN, N2, R2, o("nah_2.jpg")])
e(200106, "Mittelgrauer Fleck am Ostrand der Straße 81 an der linken Kerngrenze: Straßenrand.", RAND, False, bilder=[UN, N3, o("nah_3.jpg")])
e(200099, "Heller Fleck am Westrand der Straße 49: Straßenrand.", RAND, False, bilder=[UN, N2, o("nah_2.jpg")])
e(200102, "Dunkle, rundliche Fläche am Westrand der Straße 49: Baumkrone mit Schatten.", ("Gehölz", "Baum oder Strauch", "Baum"), False,
  bilder=[UN, N2, o("nah_2.jpg")])
e(200103, "Heller Fleck am Westrand der Straße 49, gleicher Grauton wie die Fahrbahn.", STR, False, bilder=[UN, N2, o("nah_2.jpg")])
e(200049, "Fahrbahn der Straße 49 (Nordwest–Südost) mit der Gabelung um den Anger, hell und gleichmäßig.", STR, True,
  bilder=[UN, UR, N2, R2, N4, o("nah_2.jpg"), o("nah_4.jpg")])
e(200100, "Dunkle Fläche westlich der Straße 81, im Kern nur 53 Bildpunkte an der linken Kerngrenze: Schatten.", SCH, False,
  bilder=[UN, N3, o("nah_3.jpg")])
e(200115, "Mittelgraue Fläche an der linken unteren Ecke des Kerns (21 Bildpunkte): Hof oder Dach westlich der Straße 81.", MISCH, False,
  bilder=[UN, N3, o("nah_3.jpg")])
e(200081, "Helle Fahrbahn der Straße 81 am linken unteren Kernrand.", STR, True, bilder=[UN, N3, o("nah_3.jpg")])
e(200126, "Kleiner heller Rest am Ostrand der Straße 81 am unteren Kernrand.", RAND, False, bilder=[UN, N3, o("nah_3.jpg")])
e(200119, "Mittelgrauer Fleck östlich der Straße 81: Hof oder Vorgarten.", HOF, False, bilder=[UN, N3, o("nah_3.jpg")])
e(200121, "Heller, scharf begrenzter Rechteckblock am unteren Kernrand: Gebäude mit hellem Dach.", DACH, True, bilder=[UN, N3, o("nah_3.jpg")])
e(200113, "Sehr dunkle Fläche westlich der Straße 49 am unteren Kernrand: Schatten oder Baumkrone.", SCH, False,
  bilder=[UN, N4, o("nah_2.jpg")])
e(200120, "Heller Rest der Fahrbahn 49 am unteren Kernrand.", STR, False, bilder=[UN, N4, o("nah_2.jpg")])

uebersicht = [H0 + "/H0.png", H0 + "/ganz/H0_raster.jpg", H0 + "/ganz/r0c1/ganz_nummern.jpg", H0 + "/ganz/r0c1/ganz_roh.jpg",
              UN, UR, V + "/uebersicht_vorschlag.jpg", V + "/uebersicht_maengel.jpg", UK, V + "/uebersicht_gitter.jpg"]
nah = [N1, R1, N2, R2, N3, R3, N4, R4] + [o(n) for n in ("nah_1.jpg", "nah_2.jpg", "nah_3.jpg", "nah_4.jpg", "kontrast_1.jpg",
                                                         "probe_47.jpg", "probe_74.jpg")]
naht = []
for nid, r in sorted(reg.items()):
    if r["naht_links"]:
        naht.append({"id": nid, "seite": "links", "text": "Teilstück aus 47 an der Kerngrenze x 64; in r0c0 ist 47 noch ein Stück, dort sollte an denselben Hell-dunkel-Kanten geteilt werden."})
    if r["naht_unten"]:
        naht.append({"id": nid, "seite": "unten", "text": "Teilstück aus 47 an der Kerngrenze y 563; jenseits (r1c1) liegt der übrige Block 47 ungeteilt."})
naht += [{"id": 200081, "seite": "links", "text": "Straße 81 läuft über die linke untere Ecke; gleiche Klasse Straße beiderseits."},
         {"id": 200049, "seite": "unten", "text": "Fahrbahn 49 läuft über die untere Kerngrenze nach r1c1; gleiche Klasse Straße."},
         {"id": 200113, "seite": "unten", "text": "Dunkle Fläche reicht über die untere Kerngrenze; Klasse dort abgleichen (Schatten oder Baum)."}]
unsicher = ["200056 (Viertel v1): Randstreifen östlich der Straße 49, grenzt ohne scharfe Kante an 49.",
            "200097 (Viertel v4): dunkle Fläche östlich der Straße 49 gegenüber dem Anger.",
            "200071 (Viertel v4): Block östlich der Einmündung 67, Sammelsegment."]
nicht_geprueft = ["Kontextrand links (x < 64) und unten (y > 563) nur angesehen.",
                  "Werkzeug kante nicht benutzt; neue Grenzen aus der Wasserscheide auf dem Grauwert-Gradienten."]
offen = ["Block 47: die Häuser stehen hier Ost-West; helle Dächer und helle Höfe sind gleich hell, mittelgraue Dächer und Höfe ebenso. Die Mischflächen (Klasse Hof oder Dach, mittelgrau) und die große helle Fläche 47 brauchen das Farbbild zum Trennen.",
         "54: Schatten einer Baumreihe oder hoher Häuser längs der Straße 49; Farbbild entscheidet (Grün).",
         "Anger 94, 89, 85: Gras und Bäume angenommen; Farbbild bestätigt.",
         "78: heller Streifen neben der Straße, Gebäude oder Gehweg.",
         "Beim Teilen von 47 bekam der Kontextteil unterhalb der Kerngrenze (y > 563, 8482 Bildpunkte, außerhalb des Kerns) die neue ID 200291, weil er nur über den Kern mit dem Rest von 47 verbunden war; im Kern liegt davon nichts, darum wird er hier nicht geurteilt.",
         "Die neuen IDs tragen in segmente.json kein Feld im_kern und den Code des geteilten Segments; die Klasse steht nur hier."]
n47 = sorted([200047] + [nach[(200047, j)] for j in T47 if T47[j]])
n74 = sorted([200074] + [nach[(200074, j)] for j in (2, 3, 4)])
eingriffe = [
    {"schritt": "polygon_zuweisen", "vorher": [200047], "nachher": n47,
     "grund": "47 fasste den ganzen Block westlich der Straße 49 (Häuser, Höfe, Gärten, 42 075 Bildpunkte im Kern) zusammen; an den Hell-dunkel-Kanten in 42 Teile zerlegt; dabei entstand im Kontextrand zusätzlich 200291 (siehe offen)."},
    {"schritt": "polygon_zuweisen", "vorher": [200074], "nachher": n74,
     "grund": "74 umfasste einen dunklen rechteckigen Dachteil, helle Dachstreifen und einen mittelgrauen Rest; an den scharfen Kanten in 4 Teile zerlegt."}]
kf = klassen_frei_liste(E)
urteil_schreiben(O, "v3", E, uebersicht, nah, naht, unsicher, nicht_geprueft, offen, eingriffe, kf, 64, 314)
print(len(E), "Einträge", sum(1 for x in E if not x["sicher"]), "unsicher",
      sum(1 for x in E if x["urteil"] == "nicht_sauber"), "nicht sauber", sum(len(x["punkte"]) for x in E), "Punkte")
