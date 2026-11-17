N, R = "uebersicht_nummern.jpg", "uebersicht_roh.jpg"
N1, R1, N2, R2, N3, R3, N4, R4 = ("nah%d_%s.jpg" % (k, t) for k in range(1, 5) for t in ("nummern", "roh"))
E1, E2 = "OUT:nah_1.jpg", "OUT:nah_2.jpg"
S, NS = "sauber", "nicht_sauber"
GEH, GEB, BAUM = "Gehölz", "Gebüsch", "Baum"
GE, BEF, GRAS, SCH = "Gebäude", "Befestigte Fläche", "Grasland", "Schatten"
FELD = ("Offener Boden", "Feld", "Feld gemäht")

UEB = [N, R]
NAH = [N1, R1, N2, R2, N3, N4, R4]
EIGEN = ["nah_1.jpg", "nah_2.jpg"]


def zu_feld(sid, kh, was, pt, fl, bilder, sicher=False):
    return (sid, kh, was, NS, FELD, sicher,
            [("verschmelzen", f"Gehört zur Feldfläche 170 (Randstück bei {pt}); mit 170 zusammenlegen.", fl)], bilder)


SEG = [
 (200145, "4.2.1", "Rötlich-violette Laubbaumkrone (vermutlich Blutbuche) am linken Kernrand.", S,
  (GEH, BAUM, "Einzelbaum"), True, [], [N, N1, R1]),
 (200139, "4.2.1", "Mehrere Laubbaumkronen am oberen linken Viertelrand, Teil des Gehölzgürtels oberhalb des Feldes, reicht nach v1.", S,
  (GEH, BAUM, "Baumgruppe"), True, [], [N, N1, R1]),
 (200156, "4.1", "Kleines Kronenstück zwischen den Bäumen 141 und 158.", NS,
  (GEH, BAUM, "Baumgruppe"), True,
  [("verschmelzen", "Kronenstück (174/347) ohne eigene Kante; mit 141 zusammenlegen.", 76)], [N, N1, R1]),
 (200141, "4.2.1", "Laubbaumkronen oben in der Mitte, reicht nach v1.", S,
  (GEH, BAUM, "Baumgruppe"), True, [], [N, N1, N2, R2]),
 (200157, "4.1", "Rasenstreifen nördlich des Pools.", NS,
  (GRAS, "Rasen", "Rasen"), True,
  [("klasse", "Glatte grüne Fläche ohne Kronen (244/348): Rasen, kein Wald.", 244)], [N, N2, R2]),
 (200149, "1.3.4", "Grasstreifen zwischen Gartengehölz 92 und Rasen 143, Fortsetzung des Gartenwegs 144.", NS,
  (GRAS, "Rasen", "Rasen"), False,
  [("klasse", "Grüner Streifen (258/318) ist Rasen bzw. Rasenweg, kein Sport- oder Spielplatz.", 156)], [N, N2, R2]),
 (200155, "4.1", "Dunkle Kronen im Schatten zwischen den Bäumen 145 und 139.", S,
  (GEH, BAUM, "Baumgruppe"), False, [], [N, N1, R1]),
 (200167, "4.2.4", "Gehölz aus Bäumen und Sträuchern am linken Viertelrand oberhalb des Feldes.", S,
  (GEH, BAUM, "Baumgruppe"), False, [], [N, N1, R1]),
 (200154, "0.2", "Dunkle Kronenlücke im Schatten zwischen den Kronen 139 und 158 innerhalb des Gehölzgürtels.", NS,
  (GEH, BAUM, "Baumgruppe"), False,
  [("klasse", "Schatten zwischen Kronen (120/362), umgeben von Gehölz: Gehölz statt Schatten ohne Grund.", 1262)], [N, N1, R1]),
 (200158, "4.2.1", "Große Laubbaumkrone(n) oberhalb des Feldes.", S,
  (GEH, BAUM, "Baumgruppe"), True, [], [N, N1, R1]),
 (200162, "4.1", "Kleines Kronenstück zwischen den Bäumen 141 und 160.", NS,
  (GEH, BAUM, "Einzelbaum"), True,
  [("verschmelzen", "Kronenstück (200/351) ohne eigene Kante; mit 160 zusammenlegen.", 93)], [N, N1, N2]),
 (200160, "4.2.1", "Dunkle Laubbaumkrone westlich des Pools, reicht bis an das Feld.", S,
  (GEH, BAUM, "Einzelbaum"), True, [], [N, N2, R2]),
 (200159, "1.1.1", "Helle Plattenfläche mit Stufen westlich des Pools, kein Gebäude.", NS,
  (BEF, "Terrasse", "Terrasse"), True,
  [("klasse", "Helle Platten am Pool (229/360): Terrasse, kein Hauptgebäude.", 359)], [N, N2, R2]),
 (200174, "1.1.1", "Dunkle Fläche mit Liegen und Möbeln südlich des Pools (Holzdeck oder Terrasse), ohne Dachform.", NS,
  (BEF, "Terrasse", "Terrasse"), False,
  [("klasse", "Fläche mit Möbeln (263/383): Terrasse am Pool; ein Dach ist nicht erkennbar.", 663)], [N, N2, R2, E2]),
 (200163, "1.3.3", "Rechteckiger Pool mit hellblauem Wasser.", S,
  ("Wasser", "Schwimmbecken", "Pool"), True, [], [N, N2, R2, E2]),
 (200172, "3.1", "Dunkler Strauch östlich des Pools, daneben ein weißer Gegenstand.", NS,
  (GEH, GEB, "Strauch"), False,
  [("klasse", "Dunkle Krone (284/369): Strauch statt Wiese.", 91)], [N, N2, R2, E2]),
 (200185, "4.1", "Grasiger Rand des Feldes am linken Kernrand.", NS,
  (GRAS, "Randstreifen", "Randstreifen"), False,
  [("klasse", "Grünbeiger Feldrand (69/421) ohne Kronen: Randstreifen, kein Wald.", 96)], [N, N1]),
 zu_feld(200184, "6.1", "Beiges Stück am oberen Feldrand, gleiche Farbe und Streifung wie das Feld, keine offene Sandstelle.", "(88/416)", 128, [N, N1, R1]),
 (200173, "4.1", "Hellere Lücke zwischen den Kronen 167 und 158 mit niedrigem Bewuchs (Krautsaum) zum Feld hin.", NS,
  (GRAS, "Randstreifen", "Randstreifen"), False,
  [("klasse", "Glattere graugrüne Fläche ohne Kronen (113/403): Krautsaum, kein Wald.", 648)], [N, N1, R1]),
 zu_feld(200183, "6.1", "Beiges Stück am oberen Feldrand unter den Kronen, wie das Feld gefärbt.", "(117/415)", 119, [N, N1, R1]),
 zu_feld(200181, "4.1", "Graubeiges Stück am Feldrand unter Krone 158.", "(187/409)", 88, [N, N1, R1]),
 zu_feld(200188, "2.1", "Beiges Randstück des Feldes unter Krone 160.", "(213/430)", 88, [N, N2, R2]),
 zu_feld(200187, "2.1", "Beiges Randstück des Feldes unter Krone 160.", "(230/429)", 109, [N, N2, R2]),
 (200180, "1.1.2", "Langes schmales graues Dach (rund 8 × 2,5 m) am unteren Gartenrand mit Schatten nach Norden: Schuppen oder Unterstand.", S,
  (GE, "Nebengebäude", "Gartenhütte"), False, [], [N, N2, R2, E2]),
 (200171, "4.1", "Gras- und Krautsaum mit Zaunlinie zwischen Poolgarten und Feld, darin ein kleines Glas- oder Frühbeet; reicht nach v4.", NS,
  (GRAS, "Randstreifen", "Randstreifen"), False,
  [("klasse", "Saum aus Gras, Kraut und Zaun am Feldrand (301/402), kein Wald.", None),
   ("trennen", "Helles kleines Rechteck (Frühbeet oder Glashaus, rund 3 × 1 m) bei x 233–249, y 397–402 (241/399) abtrennen.", 80)],
  [N, N2, R2, E2]),
 zu_feld(200191, "2.1", "Beiges Feldstück nördlich von Baum 193, gleiche Streifung wie das Feld.", "(225/497)", 205, [N, N4, R4, E1], True),
 (200189, "3.1", "Hohe, ungemähte Wiese südlich des Feldes.", S,
  (GRAS, "Wiese", "Wiese"), True, [], [N, N3, N4, R4, E1]),
 zu_feld(200196, "2.2", "Heller Streifen am Südrand des Feldes (trockenes Mähgut oder Fahrspur), Fortsetzung des hellen Randstreifens in 170.", "(183/518)", 195, [N, N3, N4, E1]),
 zu_feld(200199, "4.1", "Heller Streifen am Südrand des Feldes neben Baum 193, kein Wald.", "(201/523)", 128, [N, N4, R4, E1]),
 (200205, "4.1", "Dunkler Kronenrand an der Südseite von Baum 193.", NS,
  (GEH, BAUM, "Baumgruppe"), False,
  [("verschmelzen", "Kronenrand (221/542) mit 193 zusammenlegen.", 118)], [N, N4, R4]),
 (200193, "4.2.1", "Dunkle Baumgruppe am Südrand des Feldes.", S,
  (GEH, BAUM, "Baumgruppe"), True, [], [N, N4, R4, E1]),
 zu_feld(200200, "4.1", "Hellgraues Stück am Feldrand zwischen den Bäumen 193 und 197, kein Wald.", "(257/524)", 93, [N, N4, R4, E1]),
 zu_feld(200195, "2.4.1", "Beiges Feldstück am Rand von Baum 193, gleiche Streifung wie das Feld, kein Weingarten.", "(258/511)", 115, [N, N4, R4, E1]),
 (200204, "4.1", "Dunkelgrüner Kronenrand bzw. Gras an der Südseite von Baum 193.", NS,
  (GEH, BAUM, "Baumgruppe"), False,
  [("verschmelzen", "Kronenrand (260/541) mit 193 zusammenlegen; Gras am Rand nicht sicher abgrenzbar.", 248)], [N, N4, R4]),
 zu_feld(200202, "4.1", "Hellgraues Stück am Feldrand zwischen den Bäumen 193 und 197, kein Wald.", "(265/525)", 106, [N, N4, R4, E1]),
 (200197, "4.2.1", "Dunkle große Baumkrone am Südrand des Feldes, reicht nach v4.", S,
  (GEH, BAUM, "Einzelbaum"), True, [], [N, N4, R4]),
 (200207, "0.2", "Dunkle Baumkronen am unteren Kernrand, größtenteils im Kontextrand; kein Schatten ohne Grund.", NS,
  (GEH, BAUM, "Baumgruppe"), False,
  [("klasse", "Dunkle Kronen mit Sprenkeln (157/557): Baum statt Schatten.", 416)], [N, N3, N4]),
]

NAHT = [
 {"id": 200185, "seite": "links", "text": "185 reicht in r0c0; Randstreifen statt Wald muss dort gleich gelten."},
 {"id": 200207, "seite": "unten", "text": "207 reicht über die untere Kerngrenze nach r1c1; Baum statt Schatten muss dort gleich gelten."},
 {"id": 200170, "seite": "links", "text": "Feld 170 (in v4 geurteilt) läuft über die linke Kerngrenze; die hier vorgeschlagenen Randstücke gehören dazu."},
]
UNSICHER = [
 "200170 (Nachbar v4): großes Feld; Vorstufe führt es als 6.6 Feldweg, es ist eine gemähte bzw. abgeerntete Feldfläche.",
 "200143 (Nachbar v4): großer Rasen östlich des Pools; 157 und 149 sollten mit ihm zusammenpassen.",
 "200092 (Nachbar v1): Gartengehölz grenzt oben ohne klare Kante an 141 und 157.",
]
NICHT = []
OFFEN = [
 "Gehölzgürtel 139, 141, 145, 155, 158, 160, 167: ob als Baumgruppen oder zusammen als Feldgehölz/Gehölzbestand zu führen, ist eine Frage der Namensliste, nicht des Bildes.",
 "200174: ob über der Terrasse ein flaches Dach liegt, ist im Bild nicht erkennbar.",
 "200180: Schuppen oder Hochbeet bzw. Unterstand nicht sicher unterscheidbar.",
 "Heller Streifen am Südrand des Feldes (196, 199, Teile von 170): Fahrspur oder trockenes Mähgut nicht sicher.",
]
