from werk import *
O = H0 + "/b-kategorien-frei/urteil/r0c1/v1"
V = VB + "/v1"
UN, UR, UK = V + "/uebersicht_nummern.jpg", V + "/uebersicht_roh.jpg", V + "/uebersicht_kontrast.jpg"
N1, N2, N3, N4 = [V + f"/nah{i}_nummern.jpg" for i in (1, 2, 3, 4)]
R1, R2, R3, R4 = [V + f"/nah{i}_roh.jpg" for i in (1, 2, 3, 4)]
o = lambda n: O + "/" + n
GEB = ("Bebaut", "Gebäude", "Langhaus, Dach Sonnenseite")
SCH = ("Schatten", "Schlagschatten", "Schatten zwischen Häusern")
HALB = ("Unklar", "Halbschatten", "Dachseite oder Hof")
HOF = ("Freifläche", "Hof oder Vorgarten", "Hof oder Vorgarten")
STR = ("Verkehrsfläche", "Straße", "Dorfstraße")
RAND = ("Verkehrsfläche", "Straßenrand", "Randstreifen (Bankett oder Gehweg)")
S4 = [UN, UR, N1, R1, o("nah_1.jpg"), o("kontrast_1.jpg"), o("nah_6.jpg")]
E = []


def e(id, was, frei, sicher, urteil="sauber", punkte=(), bilder=S4):
    E.append(dict(id=id, was=was, frei=frei, sicher=sicher, urteil=urteil, punkte=list(punkte), bilder=bilder))


e(200019, "Helles Wohnhaus links der Kerngrenze (in r0c0); im Kern von r0c1 liegt nur sein dunkler Schlagschatten (x 64–77, y 64–88).",
  ("Bebaut", "Gebäude", "Wohnhaus, helles Dach"), False, "nicht_sauber",
  [("trennen", "Der Kernteil in r0c1 (x 64–77, y 64–88) ist Schatten, kein Dach; die Trennung liegt an der Traufkante bei x 57–62 im Kern von r0c0 und gehört dorthin.", 70, 76, 146)],
  [UN, N1, R1, o("nah_5.jpg")])
e(200025, "Mittelgraue Ausbuchtung am Südrand der Straße an der Kreuzung, mit dünnem Ausläufer auf die Dachkante eines Langhauses.",
  RAND, False, "nicht_sauber",
  [("grenze", "Ausläufer x 300–325, y 100–125 liegt auf der hellen Dachkante des Nachbarhauses (16), nicht auf der Straße.", 312, 112, 60)],
  [UN, N2, R2, o("nah_2.jpg")])
e(200004, "Nach dem Teilen nur noch der dunkle Schatten zwischen den Langhäusern oben links (x 64–166, y 64–161); der übrige Häuserblock steht in eigenen Segmenten.",
  SCH, False, "sauber", [], S4)
e(200027, "Mittelgrauer Fleck mit dunklem Kern am Nordrand der Straße vor einem Hausgiebel: Einfahrt, Vorgarten oder Baum, auf dem Scan nicht zu trennen.",
  HOF, False, "sauber", [], [UN, N2, R2, o("nah_2.jpg")])
e(200043, "Zwei Bildpunkte der hellen Fahrbahn an der linken Kerngrenze (x 64, y 177–178); Rest in r0c0.",
  STR, True, "sauber", [], [UN, N3, o("nah_4.jpg")])
e(200042, "Heller Fahrbahnstreifen der nach Nordwesten laufenden Straße an der linken Kerngrenze.",
  STR, True, "sauber", [], [UN, N3, o("nah_4.jpg")])
e(200031, "Heller Streifen der nach Nordwesten laufenden Straße zwischen Häuserblock und Fahrbahn 49; ohne Kante zu 42 und 49.",
  STR, True, "sauber", [], [UN, N3, R3, o("nah_4.jpg")])
e(200052, "Schmaler heller Rand der Fahrbahn an der Einmündung, gleicher Grauton wie Straße 5 und 49.",
  STR, True, "sauber", [], [UN, N3, o("nah_4.jpg")])
e(200040, "Mittelgrauer Fleck am Nordrand der Straße vor dem Häuserblock, gleiche Fläche wie der Vorbereich 165.",
  HOF, False, "sauber", [], [UN, N1, N3, o("nah_4.jpg"), o("nah_6.jpg")])
e(200005, "Fahrbahn der Ortsstraße (Südwest–Nordost), hell und gleichmäßig; Belag nicht bestimmbar.",
  STR, True, "sauber", [], [UN, UR, N1, N2, N3, o("nah_2.jpg"), o("nah_6.jpg")])
e(200038, "Heller Fleck am Südrand der Straße vor einem Langhaus, mit Ausläufer auf dessen hellen Dachstreifen.",
  RAND, False, "nicht_sauber",
  [("grenze", "Ausläufer x 215–230, y 168–182 liegt auf dem hellen Dachstreifen des Langhauses in 16.", 224, 176, 50)],
  [UN, N2, R2, o("nah_2.jpg")])
e(200053, "Kleiner dunkelgrauer Fleck zwischen Fahrbahnrand und Häuserzeile: Bewuchs oder Schatten am Straßenrand.",
  ("Freifläche", "Randstreifen", "Randstreifen, dunkel (Bewuchs?)"), False, "sauber", [], [UN, N3, R3, o("nah_4.jpg")])
e(200048, "Helle, ebene, rechteckige Fläche an der Straßeneinmündung ohne eigenen Schatten: Vorplatz; ein flaches Gebäude ist nicht ausgeschlossen.",
  ("Verkehrsfläche", "Platz", "Vorplatz"), False, "sauber", [], [UN, N3, R3, N4, o("nah_4.jpg")])
e(200062, "Dunkler fleckiger Fleck am Südwestrand der Fahrbahn 49: Strauch oder kleiner Baum mit Schatten.",
  ("Gehölz", "Baum oder Strauch", "Strauch am Straßenrand"), False, "sauber", [], [UN, N3, R3, o("nah_4.jpg")])
e(200056, "Heller Randstreifen längs der Nordostseite der Fahrbahn 49, oben mit dunklerem Band (Graben oder Bewuchs).",
  RAND, False, "nicht_sauber",
  [("sonstiges", "Oberer Teil x 115–150, y 215–250 enthält ein dunkleres Band zwischen Fahrbahn und Häusern; ohne klare Kante nicht geteilt.", 130, 232, None)],
  [UN, N3, R3, N4, o("nah_4.jpg")])
e(200065, "Nach dem Teilen der dunkle Schlagschatten nordöstlich des hellen Nebengebäudes 191.",
  SCH, False, "sauber", [], [UN, N4, R4, o("nah_3.jpg"), o("nah_7.jpg")])
e(200191, "Sehr helles, scharf begrenztes Rechteck (etwa 11 × 5 m) mit Schatten auf der Nordostseite: Nebengebäude mit hellem Dach.",
  ("Bebaut", "Gebäude", "Nebengebäude, helles Dach"), True, "sauber", [], [UN, N4, R4, o("nah_3.jpg"), o("nah_7.jpg")])

neu4 = {
    200160: ("Großer dunkler Schatten zwischen den Langhäusern oben rechts im Block (x 142–261, y 64–128).", SCH, False),
    200162: ("Langer heller Dachstreifen eines Langhauses mit hellem Querbau am Straßenende (x 91–211, y 64–146).", GEB, True),
    200164: ("Heller Dachstreifen eines Langhauses in der Blockmitte (x 87–169, y 88–157).", GEB, True),
    200165: ("Mittelgraue, leicht fleckige Fläche zwischen den Hausgiebeln und der Straße: Hof oder Vorgarten.", HOF, False),
    200166: ("Dunkles Schattenband zwischen zwei hellen Dachstreifen oben (x 116–190, y 64–127).", SCH, False),
    200167: ("Dunkles Schattenband zwischen Dachstreifen 164 und 162 (x 116–176, y 85–145).", SCH, False),
    200169: ("Dunkles Schattenband zwischen Dachstreifen 170 und 171 links (x 64–118, y 120–166).", SCH, False),
    200170: ("Heller Dachstreifen eines Langhauses links (x 70–128, y 105–156).", GEB, True),
    200171: ("Heller Dachstreifen eines Langhauses an der linken Kerngrenze (x 64–105, y 127–173).", GEB, True),
    200172: ("Mittelgraue unruhige Fläche oben links zwischen Schatten und Dachstreifen: Hof oder Dachseite.", HALB, False),
    200173: ("Mittelgrauer Streifen neben dem hellen Dachblock 174: wohl dessen Schattenseite.", HALB, False),
    200174: ("Kurzer heller Dachblock (x 196–222, y 91–115), Teil eines Langhauses nahe der Straße.", GEB, True),
    200175: ("Dunkler Schatten unten links am Blockrand (x 76–96, y 153–189).", SCH, False),
    200177: ("Mittelgrauer Streifen am oberen Kernrand rechts: Dachseite oder Hof.", HALB, False),
    200178: ("Heller Dachstreifen am oberen Kernrand (x 160–196, y 64–91).", GEB, True),
    200179: ("Mittelgrauer Streifen neben einem hellen Dachstreifen oben rechts: Dachseite oder Hof.", HALB, False),
    200180: ("Mittelgraue Fläche an der linken Kerngrenze (x 64–79, y 141–163): Dachseite oder Hof.", HALB, False),
    200181: ("Mittelgrauer Fleck am Straßenrand vor dem Querbau (x 168–188, y 143–156): Hof oder Vorgarten.", HOF, False),
    200182: ("Mittelheller Streifen am oberen Kernrand rechts (Grauwert 116): Dachseite, schwächer beleuchtet.", GEB, False),
    200183: ("Mittelgraue Insel zwischen zwei Dachstreifen (x 100–117, y 100–116): Dachseite oder Hof.", HALB, False),
    200184: ("Mittelgrauer Streifen am oberen Kernrand (x 99–122, y 64–74): Dachseite oder Hof.", HALB, False),
    200185: ("Mittelgrauer Fleck vor den Hausgiebeln an der Straße (x 199–215, y 122–136): Hof oder Vorgarten.", HOF, False),
    200186: ("Mittelgrauer Fleck an der linken Kerngrenze (x 64–80, y 111–124): Dachseite oder Hof.", HALB, False),
    200187: ("Kleiner dunkler Schatten am oberen Kernrand (x 248–265, y 64–74).", SCH, False),
    200188: ("Kleiner mittelgrauer Rest am oberen Kernrand (x 188–202, y 64–72).", HALB, False),
    200189: ("Kleiner mittelgrauer Fleck unten links im Schatten (x 83–92, y 165–174).", HALB, False),
    200190: ("Kleine mittelgraue Insel im Schattenband 169 (x 103–111, y 147–155): Gegenstand oder Lücke im Schatten.", HALB, False),
}
reg = json.load(open(O + "/regionen_v1.json"))
for nid, (was, frei, sicher) in neu4.items():
    e(nid, was, frei, sicher, "sauber", [], S4)

uebersicht = [H0 + "/H0.png", H0 + "/ganz/H0_raster.jpg", H0 + "/ganz/r0c1/ganz_nummern.jpg", H0 + "/ganz/r0c1/ganz_roh.jpg",
              UN, UR, V + "/uebersicht_vorschlag.jpg", V + "/uebersicht_maengel.jpg", UK, V + "/uebersicht_gitter.jpg"]
nah = [N1, R1, N2, R2, N3, R3, N4, R4] + [o(n) for n in ("nah_1.jpg", "kontrast_1.jpg", "nah_2.jpg", "nah_3.jpg", "nah_4.jpg",
                                                         "nah_5.jpg", "nah_6.jpg", "nah_7.jpg", "probe_4.jpg", "probe_65.jpg")]
naht_links = [int(k) for k, v in reg.items() if v["naht_links"]]
naht = [{"id": 200019, "seite": "links", "text": "Segment reicht über die Kerngrenze: Dach in r0c0, Schatten in r0c1; die Trennung an der Traufkante (x 57–62) liegt im Kern von r0c0. Klasse einmal: Gebäude (unsicher)."}]
naht += [{"id": i, "seite": "links", "text": "Neues Teilstück aus 4 grenzt an der Kerngrenze x 64 an den Teil von 4 in r0c0, wo 4 noch der ganze Häuserblock ist; gleiche Fläche (Schatten bzw. Dach) beiderseits ohne Bildkante: r0c0 sollte 4 entlang derselben Hell-dunkel-Kanten teilen."}
         for i in sorted(naht_links) if i != 200004]
naht.append({"id": 200004, "seite": "links", "text": "4 behält die ID für den Schatten oben links; der Teil in r0c0 ist der ganze Häuserblock. Klasse hier Schatten, in r0c0 vermutlich Gebäude: an der Naht zu einigen, nachdem r0c0 geteilt hat."})
naht.append({"id": 200031, "seite": "links", "text": "Straßenstreifen 31, 42, 43 und Fahrbahn 49 sind eine Fläche ohne Kante; gleiche Klasse Straße für alle, auch in r0c0."})
unsicher = ["200016 (Viertel v2): der Häuserblock südöstlich der Straße ist wie 4 ein Sammelsegment vieler Langhäuser und Schatten.",
            "200049 (Viertel v3): Fahrbahn; 31, 42, 52 grenzen ohne Bildkante an, gleiche Klasse Straße nötig.",
            "200047 (Viertel v3): großes Sammelsegment westlich der Straße 49 (Häuser, Höfe, Gärten)."]
nicht_geprueft = ["Kontextrand (y < 64 und x < 64) nur angesehen, nicht geurteilt; dort trägt 4 noch den ganzen Häuserblock.",
                  "Das Werkzeug kante wurde nicht benutzt: die neuen Grenzen kommen aus einer Wasserscheide auf dem Grauwert-Gradienten und liegen schon auf den Hell-dunkel-Kanten."]
offen = ["Schattenbänder (Klasse Schatten zwischen Häusern) alle unsicher: bei Satteldächern mit Sonne aus Südwest ist die Nordostseite des Daches selbst dunkel; die dunklen Bänder sind breiter als die hellen Dachseiten und enthalten wohl Schattenseite des Daches plus Schlagschatten im Hof. Die Grenze zwischen beiden gibt der Scan nicht her; Farbbild oder Stereo entscheidet.",
         "Halbschatten-Streifen (Klasse Dachseite oder Hof, 11 Teile aus 4): ob Schattenseite des Daches oder Hof, entscheidet das Farbbild oder ein Stereo-Paar.",
         "Die hellen Dachstreifen zeigen nur die Sonnenseite der Langhäuser; der Gebäudeumriss ist breiter und reicht in den angrenzenden Schatten- oder Halbschattenstreifen. Eine Trennung Dach-Schattenseite gegen Schlagschatten gibt der Scan nicht her.",
         "Vorbereich 165, 181, 185, 40, 27 zwischen Giebeln und Straße: Hof, Vorgarten oder Einfahrt; das Farbbild entscheidet (Grün gegen Pflaster).",
         "48: Vorplatz oder flaches helles Gebäude; im Farbbild Dachfarbe gegen Pflaster prüfen.",
         "56: Bankett, Gehweg oder Grünstreifen; der Belag ist auf dem Scan nicht bestimmbar.",
         "62: Strauch oder dunkler Fleck am Fahrbahnrand; das Farbbild entscheidet.",
         "182: mittelhell am oberen Kernrand, Dachseite angenommen; Farbbild oder Kontextteil entscheidet.",
         "Die neuen IDs aus polygon_zuweisen tragen in segmente.json kein Feld im_kern (Werkzeugverhalten); sie liegen alle im Kern. Ihr technischer Code dort ist 1.1.1 (Code des geteilten Segments), die Klasse steht nur hier im Urteil."]
neue = sorted(neu4)
eingriffe = [{"schritt": "polygon_zuweisen", "vorher": [200004], "nachher": [200004] + neue,
              "grund": "Segment 4 fasste eine ganze Reihe Langhäuser mit Schatten und Vorbereich zusammen; nach den klaren Hell-dunkel-Kanten (Wasserscheide auf dem Gradienten) in Dachstreifen, Schatten- und Halbschattenbänder sowie Vorbereich geteilt (27 Polygone, Kontextteil unverändert)."},
             {"schritt": "polygon_zuweisen", "vorher": [200065], "nachher": [200065, 200191],
              "grund": "Segment 65 umfasste ein sehr helles Nebengebäude und seinen dunklen Schlagschatten; an der scharfen Kante getrennt."}]
kf = klassen_frei_liste(E)
urteil_schreiben(O, "v1", E, uebersicht, nah, naht, unsicher, nicht_geprueft, offen, eingriffe, kf, 64, 64)
print(len(E), "Einträge", sum(1 for x in E if not x["sicher"]), "unsicher",
      sum(1 for x in E if x["urteil"] == "nicht_sauber"), "nicht sauber", sum(len(x["punkte"]) for x in E), "Punkte")
