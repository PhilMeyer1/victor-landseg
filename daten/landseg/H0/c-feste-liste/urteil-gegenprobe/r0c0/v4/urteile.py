from pathlib import Path
import importlib.util as _iu

VIERTEL = "v4"
H0 = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/"
UEBERSICHT = [H0 + "H0.png", H0 + "ganz/H0_raster.jpg", H0 + "ganz/r0c0/ganz_nummern.jpg", H0 + "ganz/r0c0/ganz_roh.jpg",
              "uebersicht_nummern.jpg", "uebersicht_roh.jpg"]
NAH = ["nah2_nummern.jpg", "nah2_roh.jpg", "nah4_nummern.jpg", "nah4_roh.jpg", "nah_1.jpg", "nah_2.jpg", "nah_2_roh.jpg",
       "kontrast_1.jpg"]
UN = "uebersicht_nummern.jpg"
SH = "Schatten bzw. dunkle Zone neben Bauten; nach U2 Ebene 1"
RA = "Linearer Rain/Grünstreifen zwischen Acker und Straße."
SEGMENTE = [
 (100172, "Dunkler Fleck am Westrand der Straße (432/318), Fortsetzung des Gehölzes 100169.", "n", "4.2", False,
  [("klasse", "Keine Baustelle: dunkle Krone/Gebüsch wie 100169; Schatten möglich.", None),
   ("verschmelzen", "Gehört zum Gehölz 100169 (v2); nicht verschmolzen, um das bereits geurteilte Segment nicht zu ändern.", None)],
  [UN, "nah2_roh.jpg", "nah_1.jpg"]),
 (100180, "Dunklerer Grasstreifen zwischen Acker 100154 und Straße 100149 (439/339).", "n", "3.4", False,
  [("klasse", RA, None)], [UN, "nah2_roh.jpg", "nah_1.jpg"]),
 (100143, "Nach Teilen: dunkle Schattenzone östlich der Straße und schmale Schattenlinien zwischen den Dächern in v2 (489/349).", "n", "1", False,
  [("trennen", "Heller Streifen parallel östlich der Straße in zwei Stücken abgetrennt (100287, 100288).", 973),
   ("klasse", "Kein Hauptgebäude: " + SH + ".", None)],
  [UN, "nah2_roh.jpg", "nah_1.jpg"]),
 (100178, "Graue, gleichmäßige Fläche nordöstlich der Einmündung (530/348): Hof oder Platz.", "n", "1", False,
  [("klasse", "Kein Dach erkennbar (keine Schattenkante); Hof/Platz, Dach nicht ausgeschlossen; Ebene 1.", None)],
  [UN, "nah2_roh.jpg", "nah_1.jpg"]),
 (100165, "Dachteil an der oberen rechten Ecke (557/318), großteils im Kontextrand.", "n", "1.1", False,
  [("klasse", "Helles Dach wahrscheinlich; Hauptgebäude nicht belegbar.", None)], [UN, "nah_1.jpg"]),
 (100185, "Grasstreifen am Ackerrand mit kleinem hellem Gegenstand (434/364).", "n", "3.4", False,
  [("klasse", "Kein Sportplatz: Rain mit kleinem hellem Objekt (Schuppen/Trog, 440/366), zu klein zum Teilen.", None)],
  [UN, "nah2_roh.jpg", "nah_1.jpg"]),
 (100187, "Grasstreifen am Ackerrand (442/379).", "n", "3.4", False, [("klasse", RA, None)], [UN, "nah2_roh.jpg", "nah_1.jpg"]),
 (100183, "Gras mit dunklen Büschen/Bäumen und kleinen hellen Bauteilen westlich der Einmündung (476/395).", "n", "3.5", False,
  [("klasse", "Keine Baustelle: Gras mit verstreuten Gehölzen; kleine helle Bauteile (465/385) zu klein zum Teilen.", None),
   ("trennen", "Dunkle Gehölzflecken (470/400, 485/410) unscharf begrenzt, nicht geteilt.", None)],
  [UN, "nah2_roh.jpg", "nah_1.jpg", "nah_2.jpg"]),
 (100189, "Graue gleichmäßige Fläche südöstlich der Einmündung (521/397): Hof oder flaches Dach.", "n", "1", False,
  [("klasse", "Nebengebäude nicht belegbar; Hof oder Dach; Ebene 1.", None)], [UN, "nah2_roh.jpg", "nah_1.jpg"]),
 (100186, "Heller Weg von der Einmündung nach Nordosten (528/368).", "n", "1.2", False,
  [("klasse", "Keine Baustelle: schmaler heller Weg; befestigt oder nicht unklar (U1).", None)], [UN, "nah2_roh.jpg", "nah_1.jpg"]),
 (100194, "Grasstreifen am Ackerrand (458/407).", "n", "3.4", False, [("klasse", RA, None)], [UN, "nah2_roh.jpg", "nah_2.jpg"]),
 (100199, "Grasstreifen am Ackerrand (462/425).", "n", "3.4", False, [("klasse", RA, None)], [UN, "nah2_roh.jpg", "nah_2.jpg"]),
 (100198, "Nach Verschmelzen: Straße nach Süden ab der Einmündung (513/445).", "n", "1.2", False,
  [("verschmelzen", "100191 und 100193 (Straßenstücke an der Einmündung) ohne Kante angefügt.", 245),
   ("klasse", "Straße, befestigt oder Schotter nicht entscheidbar (U1: 1.2).", None)], [UN, "nah4_roh.jpg", "nah_2.jpg"]),
 (100196, "Kleines dunkleres Stück neben Hof 100189 (519/414).", "n", "1", False,
  [("klasse", SH + ".", None)], [UN, "nah2_roh.jpg"]),
 (100192, "Kleines graues Stück östlich von 100189 (536/406).", "n", "1", False,
  [("klasse", "Hof/Schatten, kein Hauptgebäude.", None)], [UN, "nah2_roh.jpg"]),
 (100176, "Höfe, Dächer und Schatten östlich der Straße (543/434), großteils im Kontextrand.", "n", "1", False,
  [("trennen", "Enthält helle Dachstreifen (545/440), Höfe und die dunkle Linie am Straßenrand; großteils im Kontextrand, im Kern nicht geteilt.", None)],
  [UN, "nah2_roh.jpg", "nah4_roh.jpg"]),
 (100210, "Nach Verschmelzen: dunkle Gehölzreihe am Westrand der Straße entlang des Ackers 100195 (534/510).", "n", "4.2.3", False,
  [("verschmelzen", "100201 und 100207 (Teile derselben Reihe) ohne Kante angefügt.", 752),
   ("klasse", "Kein Acker: dunkle, gereihte Kronen; Hecke wahrscheinlich, Graben möglich.", None)], [UN, "nah4_roh.jpg", "nah_2.jpg"]),
 (100209, "4 Bildpunkte am rechten Kernrand (562/492), Segment liegt im Kontextrand.", "n", "1", False,
  [("zu_klein", "Nur 4 Bildpunkte; Schatten neben Bauten, nicht 0.2.", 4)], [UN, "nah4_nummern.jpg"]),
 (100216, "Dunkler Fleck an der Südwestecke des Ackers 100195 (379/529): Baumkrone.", "n", "4.2", False,
  [("klasse", "Kein Acker: dunkle runde Krone; Gebüsch oder Baum.", None)], [UN, "nah_2.jpg"]),
 (100195, "Acker südöstlich des Ackers 100154 (457/508).", "n", "2", False,
  [("klasse", "Acker sicher (Form, Streifen); bewachsen oder gepflügt nicht zu entscheiden, daher Elternklasse.", None),
   ("grenze", "Grenze zu 100154 gezackt und ohne Bildkante; die Parzellengrenze liegt vermutlich auf dem feinen hellen Streifen von 370/503 nach 447/410. Nicht verschoben, weil beide Segmente in den Kontextrand reichen.", None)],
  [UN, "kontrast_1.jpg", "nah_2.jpg"]),
 (100214, "Grauer Streifen zwischen Gehölzreihe 100210 und Straße (552/526).", "n", "3.4", False,
  [("klasse", "Keine Straße: Rain am Straßenrand.", None)], [UN, "nah4_roh.jpg"]),
 (100211, "Dunkle Zone am Ostrand der Straße (557/500).", "n", "1", False,
  [("klasse", "Keine Straße: dunkle Linie/Schatten am Straßenrand vor den Höfen; Gehölz möglich.", None)], [UN, "nah4_roh.jpg"]),
 (100218, "Dunkle Kronen östlich der Ackerecke an der Straße (557/542).", "n", "4.2", False,
  [("klasse", "Keine Baustelle: dunkle rundliche Kronen.", None)], [UN, "nah4_roh.jpg"]),
 (100215, "22 Bildpunkte am rechten Kernrand (562/520), Segment liegt im Kontextrand.", "n", "1", False,
  [("zu_klein", "Nur 22 Bildpunkte; Teil der Höfe östlich der Straße.", 22)], [UN, "nah4_nummern.jpg"]),
 (100224, "Randstück an der Südwestecke (369/559).", "n", "3.4", False,
  [("klasse", "Rain zwischen den Äckern, kein eigener Acker.", None)], [UN, "nah_2.jpg"]),
 (100220, "Heller Streifen an der Südwestecke des Ackers (382/557): Feldweg.", "n", "6.6", False,
  [("klasse", "Keine Baustelle: heller schmaler Streifen zwischen Äckern, unbefestigter Weg wahrscheinlich.", None)], [UN, "nah_2.jpg"]),
 (100225, "Dunkles kleines Stück am unteren Kernrand (398/558).", "n", "4.2", False,
  [("klasse", "Kein Acker: dunkle Krone/Gebüsch.", None)], [UN, "nah_2.jpg"]),
 (100219, "Hellerer Acker südlich der klaren Feldgrenze (537/551), großteils im Kontextrand.", "n", "2", False,
  [("klasse", "Kein Hauptgebäude: gleichmäßige Ackerfläche, heller als 100195, gerade Feldgrenze.", None)], [UN, "nah4_roh.jpg", "nah_2.jpg"]),
 (100228, "21 Bildpunkte am unteren Kernrand (542/562).", "n", "2", False,
  [("zu_klein", "Nur 21 Bildpunkte; Teil des Ackers 100219.", 21)], [UN, "nah4_nummern.jpg"]),
 (100229, "19 Bildpunkte am unteren Kernrand (545/562), Straßenrand.", "n", "1.2", False,
  [("zu_klein", "Nur 19 Bildpunkte; Rand der Straße 100198.", 19)], [UN, "nah4_nummern.jpg"]),
 (100287, "Abgetrennt aus 100143: heller Streifen östlich der Straße, unterer Teil (475/360).", "n", "1", False,
  [("klasse", "Langes schmales Dach (Schatten östlich) oder Gehweg; beides Ebene 1.", None)], ["nah_1.jpg", "nah2_roh.jpg"]),
 (100288, "Abgetrennt aus 100143: heller Streifen östlich der Straße, oberer Teil (450/295).", "n", "1", False,
  [("klasse", "Langes schmales Dach oder Gehweg; Ebene 1.", None)], ["nah_1.jpg"]),
]
NAHT = [
 {"id": 100195, "seite": "unten", "text": "Acker reicht über die Teilkachelgrenze nach r1c1; Klasse 2 halten."},
 {"id": 100198, "seite": "unten", "text": "Straße reicht nach r1c1; Klasse 1.2 halten."},
 {"id": 100176, "seite": "rechts", "text": "Höfe östlich der Straße größtenteils im Kontextrand; Kernanteil schmal."},
]
UNSICHER = [
 "100149 (v2): Straße; der parallele helle Streifen 100287/100288 ist durch einen Teil von 100149 unterbrochen (Grenze ohne Bildkante bei 470/335).",
 "100154 (v3): Grenze zu 100195 ohne Bildkante.",
]
NICHT_GEPRUEFT = ["Kontextrand-Anteile von 100165, 100176, 100209, 100215, 100219, 100228, 100229 nur als Umgebung gesehen."]
OFFEN = [
 "Heller Streifen 100287/100288: Dach oder Gehweg im Farbbild bzw. an Schatten im besseren Scan prüfen.",
 "Höfe 100178, 100189: Hof oder flaches Dach im Farbbild entscheidbar.",
 "Äcker 100195, 100219: bewachsen oder gepflügt im Farbbild entscheidbar.",
 "Gehölzreihe 100210: Hecke oder Graben im Farbbild entscheidbar.",
]
_s = _iu.spec_from_file_location("en", Path(__file__).resolve().parent / "eingriffe_netto.py")
_m = _iu.module_from_spec(_s)
_s.loader.exec_module(_m)
EINGRIFFE = _m.netto(Path(__file__).resolve().parent / "protokoll.json")
