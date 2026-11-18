VIERTEL = "v3"
U, R, K = "uebersicht_nummern.jpg", "uebersicht_roh.jpg", "uebersicht_kontrast.jpg"
N1, N2, N3, N4 = "nah1_nummern.jpg", "nah2_nummern.jpg", "nah3_nummern.jpg", "nah4_nummern.jpg"
R1, R2, R3, R4 = "nah1_roh.jpg", "nah2_roh.jpg", "nah3_roh.jpg", "nah4_roh.jpg"
UEBERSICHT_GESEHEN = [U, R]
NAH_GESEHEN = [N1, R1, N3, R3]
NAH_EIGENE = ["kontrast_1.jpg"]
KK = "kontrast_1.jpg"
V = 100000
SEGMENTE = [
 (V+173, "ANGER", False, "sauber", "Mittelgraue Fläche am linken Kernrand neben dem Anger 114, Hauptteil im Kontextrand.", [], [U, N1, KK]),
 (V+177, "FELDRAIN", False, "sauber", "Dunkler Randstreifen zwischen Anger 114 und Feld 154 mit kleinem dunklem Busch.", [], [U, N1, KK]),
 (V+174, "FELDRAIN", False, "sauber", "Dunkler Randstreifen zwischen Anger 114 und Feld 154.", [], [U, N1, KK]),
 (V+175, "FELDRAIN", False, "sauber", "Dunkler Randstreifen zwischen Anger 114 und Feld 154, Fortsetzung von 168.", [], [U, N1]),
 (V+184, "ANGER", False, "sauber", "Heller kleiner Fleck am Anger am linken Kernrand.", [], [U, N1, KK]),
 (V+181, "BRACHE", False, "sauber", "Fleckig mittelgraue, ungeordnete Fläche westlich des Feldes 154, mit kleinen dunklen Büschen und hellen Flecken; Brache oder Weide.", [], [U, N1, N3, KK]),
 (V+204, "BRACHE", False, "sauber", "Hellerer Fleck in der Brache 181; gleiche Fläche.", [
     ("verschmelzen", "Gehört zur Brache 181, keine klare Bildkante.", (114, 440), 160)], [U, N1, KK]),
 (V+154, "FELD", False, "sauber", "Großes, gleichmäßig dunkelgraues Feld mit schwachen Streifen nach Nordost; im oberen Teil ein hellerer Streifen entlang des Angers.", [
     ("sonstiges", "Hellerer Streifen im Nordwestteil des Feldes (etwa 130/390 bis 300/320) kann eine eigene Parzelle sein; Übergang ohne klare Kante, nicht geteilt.", (220, 360), None)], [U, R, N1, R1, N3, KK]),
 (V+208, "BRACHE", False, "sauber", "Hellerer Fleck an der Feldecke zwischen 181 und 154.", [], [U, N1, KK]),
 (V+188, "FELDRAIN", False, "sauber", "Schmaler Feldrand mit sehr dunkler Linie (Hecke oder Graben mit Schatten) entlang der Westkante des Feldes 154.", [], [U, N1, R1, KK]),
 (V+202, "BRACHE", False, "sauber", "Heller offener Boden mit dunklen runden Flecken (Büsche oder Bäume) unten links, Hauptteil im Kontextrand.", [], [U, N3, R3, KK]),
 (V+213, "FELDRAIN", False, "sauber", "Dunkler Randstreifen (Hecke oder Graben) an der Westkante des Feldes.", [], [U, N3, KK]),
 (V+221, "FELDRAIN", False, "sauber", "Randstreifen an der Westkante des Feldes, unten am Kernrand.", [], [U, N3, KK]),
 (V+223, "FELDRAIN", False, "sauber", "Randstreifen an der Westkante des Feldes, unten am Kernrand.", [], [U, N3, KK]),
]
EINGRIFFE = []
NAHT = [
 {"id": V+154, "seite": "unten", "text": "Feld 154 reicht über den unteren Kernrand (y 563) nach r1c0; ein Segment, keine Grenze im Kern, Klasse in r1c0 gleich halten (Feld)."},
]
UNSICHER = [
 "100114 (v1): Anger reicht als heller Streifen bis an den linken Kernrand und weiter.",
 "100195 (v4): Fortsetzung des Feldes 154 nach rechts unten; Grenze 154|195 ohne klare Bildkante.",
]
NICHT_GEPRUEFT = [
 "Naht zu r1c0 (unterer Kernrand y 563) nur auf dieser Seite angesehen.",
]
OFFEN = [
 "Feld 154: Acker oder Grünland im Schwarz-Weiß-Bild nicht sicher zu trennen (schwache Streifen sprechen für Acker); im Farbbild Bewuchs und Bearbeitungsspuren.",
 "Brache 181/204/208 und 202: Brache, Weide oder Garten; dunkle Flecken in 202 Büsche oder Bäume; im Farbbild Grün und Kronen.",
 "Feldrand 188/213/221/223/174/175/177: dunkle Linie Hecke, Graben oder Schatten einer Böschung.",
]
