N, R = "uebersicht_nummern.jpg", "uebersicht_roh.jpg"
N1, R1, N2, R2, N3, R3, N4 = "nah1_nummern.jpg", "nah1_roh.jpg", "nah2_nummern.jpg", "nah2_roh.jpg", "nah3_nummern.jpg", "nah3_roh.jpg", "nah4_nummern.jpg"
S, NS = "sauber", "nicht_sauber"
GEH, GEB, BAUM = "Gehölz", "Gebüsch", "Baum"
GE, BEF, GRAS, SCH = "Gebäude", "Befestigte Fläche", "Grasland", "Schatten"
FELD = ("Offener Boden", "Feld", "Feld gemäht")
RAND = (GRAS, "Randstreifen", "Randstreifen")

UEB = [N, R]
NAH = [N1, R1, N2, R2, N3, R3, N4]
EIGEN = []

SEG = [
 (200152, "4.1", "Kleiner Kronenrand an der Westseite von Baum 153 am Rasen 143.", NS,
  (GEH, BAUM, "Baumgruppe"), False,
  [("verschmelzen", "Kronenrand (355/328) ohne eigene Kante; mit 153 zusammenlegen.", 240)], [N, N1, R1]),
 (200153, "4.2.1", "Laubbaumkronen zwischen den Rasenflächen 143 und 140.", S,
  (GEH, BAUM, "Baumgruppe"), True, [], [N, N1, R1]),
 (200150, "4.1", "Helles Gras-Stück am oberen Viertelrand zwischen Baum 134 und Wiese 140.", NS,
  (GRAS, "Wiese", "Wiese"), False,
  [("verschmelzen", "Gras ohne Kronen (401/318) gehört zur Wiese 140; zusammenlegen.", 150)], [N, N1, R1]),
 (200140, "3.1", "Wiese im unteren Garten, darin eine helle rechteckige Bodenstelle mit Linien (alter Sandplatz oder Beet), reicht nach v2.", NS,
  (GRAS, "Wiese", "Wiese"), True,
  [("trennen", "Helle Bodenstelle mit Linien bei x 413–450, y 290–324 (430/310) als offenen Gartenboden abtrennen.", 700)],
  [N, N1, R1, N2, R2]),
 (200148, "4.2.1", "Laubbaumkrone(n) am oberen Viertelrand, reicht nach v2.", S,
  (GEH, BAUM, "Baumgruppe"), True, [], [N, N2, R2]),
 (200143, "3.1", "Großer gepflegter Rasen östlich des Pools mit einem weißen Gegenstand (Liege oder Abdeckung), reicht in alle Viertel.", S,
  (GRAS, "Rasen", "Rasen"), True, [], [N, N1, R1]),
 (200176, "4.1", "Schmaler Gehölz- und Grassaum zwischen Rasen 143 und Baum 165.", NS,
  (GEH, GEB, "Strauch"), False,
  [("klasse", "Schmaler Saum aus Sträuchern (376/378), kein Wald.", 303)], [N, N1, R1]),
 (200165, "4.2.1", "Dunkle Laubbaumgruppe am oberen Feldrand.", S,
  (GEH, BAUM, "Baumgruppe"), True, [], [N, N1, R1]),
 (200166, "4.2.1", "Dunkle runde Baumkrone am Rand der Wiese 140.", S,
  (GEH, BAUM, "Einzelbaum"), True, [], [N, N2, R2]),
 (200164, "0.2", "Dunkler schmaler Streifen nördlich der Strauchreihe am Feldrand: Schatten der Sträucher auf der Wiese oder dunkle Hecke.", S,
  (SCH, "Schlagschatten", "Schlagschatten"), False, [], [N, N2, R2]),
 (200175, "2.1", "Beiges Stück am Nordrand des Feldes, gleiche Farbe wie das Feld.", NS,
  FELD, False,
  [("verschmelzen", "Feldrand (486/377) mit 170 zusammenlegen.", 112)], [N, N2, R2]),
 (200169, "4.1", "Grüner Grasstreifen an der Nordostecke des Feldes.", NS,
  RAND, False,
  [("klasse", "Grasiger Feldrand (533/364) ohne Kronen: Randstreifen, kein Wald.", 214)], [N, N2, R2]),
 (200182, "6.1", "Graugrünes Stück zwischen dem Saum 171 und dem Feld, keine offene Sandstelle.", NS,
  RAND, False,
  [("verschmelzen", "Gras am Feldrand (362/413) gehört zum Randstreifen 171; zusammenlegen.", 154)], [N, N1, R1]),
 (200186, "4.1", "Graubeiges Stück am Feldrand unter Krone 165.", NS,
  FELD, False,
  [("verschmelzen", "Feldrand (407/421) mit 170 zusammenlegen.", 91)], [N, N1, R1]),
 (200179, "4.1", "Graugrünes Stück am Feldrand unter Krone 165.", NS,
  RAND, False,
  [("klasse", "Feldrand ohne Kronen (440/401): Randstreifen, kein Wald.", 72)], [N, N1, R1, N2]),
 (200170, "6.6", "Großes Feld mit parallelen dunkleren Schwaden entlang der Hanglinie: abgeerntetes Getreidefeld mit Strohschwaden oder gemähte Wiese mit Heuschwaden; kein Feldweg. Am Südrand ein heller Streifen.", NS,
  FELD, False,
  [("klasse", "Ganze Fläche (479/479) ist ein bearbeitetes Feld, kein unbefestigter Weg.", 63018),
   ("sonstiges", "Am Süd- und Nordrand liegen kleine Randstücke (v3: 184, 183, 181, 187, 188, 191, 195, 196, 199, 200, 202; v4: 175, 186) als eigene Segmente; sie gehören zum Feld (364/420).", None)],
  [N, N1, R1, N2, R2, N3, R3, N4]),
 (200203, "3.1", "Graugrüner Grasrand an der Südwestecke des Feldes neben Baum 197.", S,
  RAND, False, [], [N, N3, R3]),
 (200206, "4.2.1", "Baumkrone am unteren Kernrand, größtenteils im Kontextrand.", S,
  (GEH, BAUM, "Einzelbaum"), True, [], [N, N3, R3]),
 (200208, "4.1", "Dunkler Kronenrand von Baum 206.", NS,
  (GEH, BAUM, "Einzelbaum"), False,
  [("verschmelzen", "Kronenrand (337/556) mit 206 zusammenlegen.", 114)], [N, N3, R3]),
 (200211, "3.1", "Wiese südlich des Feldes, nur ein Zipfel im Kern.", S,
  (GRAS, "Wiese", "Wiese"), True, [], [N, N3]),
 (200209, "3.1", "Heller Grasrand am Südrand des Feldes.", S,
  RAND, False, [], [N, N3, R3]),
]

NAHT = [
 {"id": 200170, "seite": "links", "text": "Feld 170 läuft über die linke Kerngrenze nach r0c0; Klasse Feld statt Feldweg muss dort gleich gelten."},
 {"id": 200170, "seite": "unten", "text": "Feld 170 läuft über die untere Kerngrenze nach r1c1; gleiche Klasse dort."},
 {"id": 200206, "seite": "unten", "text": "206 liegt größtenteils in r1c1; Kronenrand 208 sollte dazu."},
]
UNSICHER = [
 "200103 (Nachbar v2): sein Südteil ist eine hellgrüne Strauchreihe am Nordostrand des Feldes, an die 164, 169 und 175 grenzen.",
 "200171 (Nachbar v3): Randstreifen am Feld; 182 gehört dazu.",
 "200134 (Nachbar v2): große Baumkrone grenzt oben an 150 und 153.",
]
NICHT = []
OFFEN = [
 "200170: ob abgeerntetes Getreidefeld (Stoppel mit Strohschwaden) oder gemähte Wiese mit Heuschwaden, lässt das Bild nicht sicher entscheiden; die graubeige Farbe ohne Grün spricht für Stoppelfeld.",
 "200164: Schatten der Strauchreihe oder dunkle Hecke nicht sicher.",
 "200140: helle Bodenstelle (alter Sandplatz, Boccia-Bahn oder Beet) nicht bestimmbar.",
]
