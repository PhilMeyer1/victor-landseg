VIERTEL = "v4"
U, R, K = "uebersicht_nummern.jpg", "uebersicht_roh.jpg", "uebersicht_kontrast.jpg"
N1, N2, N3, N4 = "nah1_nummern.jpg", "nah2_nummern.jpg", "nah3_nummern.jpg", "nah4_nummern.jpg"
R1, R2, R3, R4 = "nah1_roh.jpg", "nah2_roh.jpg", "nah3_roh.jpg", "nah4_roh.jpg"
UEBERSICHT_GESEHEN = [U, R]
NAH_GESEHEN = [N2, N4]
NAH_EIGENE = ["kontrast_1.jpg", "nah_1.jpg", "nah_2.jpg", "nah_3.jpg"]
KK = "kontrast_1.jpg"
V = 100000
SEGMENTE = [
 (V+172, "BAUM", False, "sauber", "Dunkler Fleck am Westrand der Straße nach Süden, Fortsetzung der Baumreihe 169.", [], [U, KK]),
 (V+180, "WEGRAIN", False, "sauber", "Mittelgrauer Streifen mit Buschflecken zwischen Feld 154 und Straße 149.", [], [U, KK]),
 (V+143, "HOF", False, "nicht_sauber", "Beschattete Hofflächen zwischen den Längsbauten 142/167/144 und ein dunkler Keil östlich der Straße; das helle östliche Straßenband (276, 279) abgetrennt.", [
     ("trennen", "Helles östliches Band der Straße 436–469/272–332 abgetrennt als 276, Reststück 465–478/336–352 als 279.", (452, 300), 692),
     ("sonstiges", "Dunkler Keil 470–530/300–390 ist Schatten oder dunkler Boden; im Segment gelassen.", (500, 350), None)], [U, KK, "nah_1.jpg", "nah_3.jpg"]),
 (V+276, "FAHRWEG", False, "sauber", "Helles östliches Band der Straße nach Süden (neu aus 143), durch eine dunkle Linie von 149 getrennt.", [], ["nah_2.jpg", "nah_3.jpg"]),
 (V+279, "FAHRWEG", False, "sauber", "Kurzes Stück desselben hellen Straßenbands (neu aus 143), nicht mit 276 verbunden.", [], ["nah_3.jpg"]),
 (V+178, "HOF", False, "sauber", "Gleichmäßig mittelgraue Fläche zwischen 143 und 176 ohne Schatten: Hof oder Garten.", [], [U, KK, "nah_3.jpg"]),
 (V+165, "GEBAEUDE", False, "sauber", "Kernstück eines Baus am rechten Kernrand, Hauptteil in r0c1.", [], [U, "nah_3.jpg"]),
 (V+185, "WEGRAIN", False, "sauber", "Hellerer Fleck am Straßenrand zwischen Feld und Baumreihe.", [], [U, KK]),
 (V+187, "WEGRAIN", False, "sauber", "Mittelgrauer Streifen zwischen Feld 154 und Baumreihe 183.", [], [U, KK]),
 (V+183, "GEBUESCH", False, "sauber", "Baum- und Buschreihe mit Schatten westlich der Einmündung, dazwischen grauer Boden.", [
     ("sonstiges", "Mischung aus dunklen Kronen (447–502/364–443) und grauem Wegrain; einzelne Kronen nicht getrennt.", (480, 415), None)], [U, R, KK]),
 (V+191, "FAHRWEG", False, "sauber", "Helle Mitte der Einmündung der Gasse 186 in die Straße.", [], [U, KK]),
 (V+189, "STRASSENRAND", False, "sauber", "Gleichmäßig hellgraue Fläche an der Einmündung (499–534/379–421), offener Platz oder Hof.", [], [U, KK]),
 (V+186, "FELDWEG", False, "sauber", "Schmale helle Gasse von der Einmündung nach Nordost.", [], [U, KK, "nah_3.jpg"]),
 (V+194, "WEGRAIN", False, "sauber", "Streifen mit Buschfleck zwischen Baumreihe 183 und Feld.", [], [U, KK]),
 (V+199, "FELDRAIN", False, "sauber", "Mittelgrauer Rand des Feldes 195 an der Baumreihe.", [], [U, KK]),
 (V+193, "STRASSENRAND", False, "sauber", "Mittelgrauer Rand an der Einmündung zwischen Baumreihe und Straße.", [], [U, KK]),
 (V+198, "FAHRWEG", False, "sauber", "Helle Straße nach Südost von der Einmündung bis zum unteren Kernrand.", [], [U, R, KK]),
 (V+196, "HOF", False, "sauber", "Kleine graue Fläche zwischen Platz 189 und Hof 176.", [], [U, KK]),
 (V+192, "HOF", False, "sauber", "Kleine graue Hoffläche am Rand von 176.", [], [U, KK]),
 (V+176, "HOF", False, "nicht_sauber", "Höfe mit hellen Längsbauten östlich der Straße, Hauptteil im Kontextrand (r0c1/r1c1).", [
     ("trennen", "Helle Längsbauten 544–563/442–486 und 535–563/387–424 stecken im Hofsegment; nicht geteilt, weil sie über den Kernrand reichen und ein Schnitt nur im Kern die Naht verletzen würde.", (552, 462), None)], [U, R, KK]),
 (V+207, "GEBUESCH", False, "sauber", "Dunkle Busch- oder Baumgruppe am Feldrand an der Straße.", [], [U, KK]),
 (V+201, "WEGRAIN", False, "sauber", "Mittelgrauer Streifen südwestlich der Straße 198.", [], [U, KK]),
 (V+209, "SCHATTEN", False, "sauber", "Nur 4 Bildpunkte im Kern, dunkle Fläche in r0c1.", [], [U]),
 (V+216, "BAUM", False, "sauber", "Dunkler runder Fleck am Feldrand unten links: Baum oder Busch mit Schatten.", [], [U, R]),
 (V+195, "FELD", False, "nicht_sauber", "Großes dunkelgraues Feld mit feinen hellen Linien, südöstlich an Feld 154 anschließend.", [
     ("grenze", "Grenze zu 154 läuft zackig ohne Bildkante (etwa 340/450 bis 420/410); eine schwache helle Linie 359/495–482/462 könnte die wahre Parzellengrenze sein.", (380, 450), None)], [U, R, KK]),
 (V+210, "GEBUESCH", False, "sauber", "Dunkles Band entlang des Straßenrands (509–547/473–536): Hecke, Baumreihe oder Graben mit Schatten.", [], [U, KK]),
 (V+214, "WEGRAIN", False, "sauber", "Mittelgrauer Streifen zwischen dunklem Band 210 und Straße.", [], [U, KK]),
 (V+211, "SCHATTEN", False, "sauber", "Dunkle Fläche am rechten Kernrand neben der Straße.", [], [U, KK]),
 (V+218, "SCHATTEN", False, "sauber", "Dunkle Fläche am rechten unteren Kernrand neben der Straße, Schatten oder Gehölz.", [], [U, KK]),
 (V+215, "HOF", False, "sauber", "Nur 22 Bildpunkte im Kern am rechten Kernrand.", [], [U]),
 (V+224, "FELDRAIN", False, "sauber", "Kleiner Randstreifen am unteren Kernrand links.", [], [U, R]),
 (V+220, "HOF", False, "sauber", "Hellerer Fleck an der Feldecke unten links vor einem dunklen Bau im Kontextrand.", [], [U, R]),
 (V+225, "GEBUESCH", False, "sauber", "Kleiner dunkler Fleck am unteren Kernrand.", [], [U, R]),
 (V+219, "FELD", False, "sauber", "Hellerer Streifen unter dem Feld 195 am unteren Kernrand: eigene Parzelle oder Wiese.", [], [U, R, KK]),
 (V+228, "FELD", False, "sauber", "Nur 21 Bildpunkte im Kern am unteren Kernrand.", [], [U]),
 (V+229, "STRASSENRAND", False, "sauber", "Nur 19 Bildpunkte im Kern am unteren Kernrand neben der Straße.", [], [U]),
]
EINGRIFFE = [
 {"schritt": "teilen", "vorher": [V+143], "nachher": [V+143, V+276, V+279], "grund": "Das helle östliche Straßenband (436–478/272–352) steckte im beschatteten Hofsegment 143; Schnitt entlang seiner Ostkante, drei Splitter wieder 143 zugeschlagen."},
]
NAHT = [
 {"id": V+176, "seite": "rechts", "text": "Hofsegment 176 reicht weit nach r0c1/r1c1 und enthält helle Längsbauten über den Kernrand; dort einheitlich teilen, nicht nur im Kern."},
 {"id": V+198, "seite": "unten", "text": "Straße 198 läuft über den unteren rechten Kernrand weiter; Klasse Fahrweg auf beiden Seiten."},
 {"id": V+195, "seite": "unten", "text": "Feld 195 reicht über den unteren Kernrand nach r1c0/r1c1; Klasse Feld."},
]
UNSICHER = [
 "100154 (v3): Grenze zu 195 ohne Bildkante (siehe Punkt bei 195).",
 "100149 (v2): enthält im unteren Teil das östliche helle Straßenband (470–495/340–395) mit; beide Bänder gehören zur Straße.",
 "100167, 100153 (v2): Längsbauten nördlich des Schattenkeils 143.",
]
NICHT_GEPRUEFT = [
 "Vorbereitete Nahansichten nah1 und nah3 von v4 (Feldflächen 154/195 links) nicht einzeln angesehen; dafür Übersicht und eigene Nahansicht kontrast_1.",
 "Naht zu r0c1, r1c0 und r1c1 nur von dieser Seite angesehen.",
]
OFFEN = [
 "Felder 195, 219, 228: Acker oder Grünland im Schwarz-Weiß-Bild nicht zu trennen; 219 ist heller (andere Nutzung?).",
 "Straßen 198, 276, 279, 191 und Ränder 189/193/229: Belag nicht bestimmbar.",
 "143: dunkler Keil 470–530/300–390 Schatten oder dunkler Boden; 176: Längsbauten nicht abgetrennt (Naht).",
 "183, 207, 210, 216, 225: Bäume, Büsche, Hecke oder Graben mit Schatten; im Farbbild Grün der Kronen.",
 "Grenze 154|195: zackig ohne Bildkante; wahre Parzellengrenze vermutlich entlang der schwachen hellen Linie 359/495–482/462.",
]
