K = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/"
UEBERSICHT = [K + "T0.png", K + "ganz/r0c1/ganz_nummern.jpg", K + "ganz/r0c1/ganz_roh.jpg"]
UEB_V = ["uebersicht_nummern.jpg", "uebersicht_roh.jpg"]
NAH = ["nah1_nummern.jpg", "nah2_nummern.jpg", "nah3_nummern.jpg", "nah4_nummern.jpg", "eigen:nah_1.jpg"]
N1, N2, N3, N4 = "nah1_nummern.jpg", "nah2_nummern.jpg", "nah3_nummern.jpg", "nah4_nummern.jpg"
R = "uebersicht_roh.jpg"
E1 = "eigen:nah_1.jpg"
F, T = False, True
E = [
 (152, "Kleiner Strauch bzw. kleine Krone am Rand des Rasens 200143 neben dem Baum 200153", "nicht_sauber", "4.2.4", F,
  [("klasse", "Einzelner kleiner Gehölzfleck bei 355/328 im Garten, kein Wald")], [N1]),
 (153, "Baumkrone(n) zwischen den Rasenflächen 200143 und 200140", "sauber", None, F, [], [N1, R]),
 (150, "Kleines Randstück der Krone 200134 am oberen Viertelrand", "nicht_sauber", "4.2.1", F,
  [("verschmelzen", "Kronenrand bei 401/318 mit dem Baum 200134 verschmelzen, kein eigener Wald", 150)], [N1, E1]),
 (140, "Rasen bzw. Wiese südlich des Gartens mit hellen, abgenutzten Stellen", "sauber", None, T, [], [N1, N2, R, E1]),
 (148, "Runde dunkle Baumkrone am oberen Viertelrand", "sauber", None, T, [], [N2, E1]),
 (143, "Großer Gartenrasen westlich der Bäume, mit einem kleinen weißen Gegenstand", "sauber", None, T, [], [N1, R]),
 (176, "Strauchiger Saum zwischen Baum 200165, Rasen 200143 und Grasstreifen 200171", "nicht_sauber", "4.2", F,
  [("klasse", "Niedrigeres Gehölz bei 376/378, kein geschlossener Wald")], [N1]),
 (165, "Großes dunkles Kronendach an der Ecke des Feldes, eine große Krone oder mehrere Bäume", "sauber", None, F, [], [N1, R]),
 (166, "Runde dunkle Baumkrone am Feldrand", "sauber", None, T, [], [N2, E1]),
 (164, "Dunkles längliches Gehölzband (Hecke bzw. Strauchreihe) am Feldrand", "nicht_sauber", "4.2", F,
  [("klasse", "Längliche dunkle Gehölzform mit Textur bei 484/364 neben dem Baum 200166; Gehölz nach U2, nicht 0.2")], [N2, E1]),
 (175, "Kleiner Randzipfel des Feldes am Gehölzrand", "nicht_sauber", "3.1.1", F,
  [("verschmelzen", "Heller Feldrand bei 486/377 mit der Fläche 200170 verschmelzen, kein Acker mit Bewuchs", 112)], [N2, E1]),
 (169, "Grasiger Saum am Nordostrand des Feldes", "nicht_sauber", "3.4", F,
  [("klasse", "Grünlicher Randstreifen bei 533/364 zwischen Feld und Gehölz, kein Wald")], [N2]),
 (182, "Grünlich-graue Stelle am Nordrand des Feldes im Grasstreifen", "nicht_sauber", "3.4", F,
  [("verschmelzen", "Stelle bei 362/413 gehört zum Grasstreifen 200171 bzw. Feldrand; keine Abbruchkante, kein offener Boden", 154)], [N1]),
 (186, "Feldrand unter dem Baum 200165", "nicht_sauber", "3.1.1", F,
  [("verschmelzen", "Heller Feldrand bei 407/421 mit 200170 verschmelzen, kein Wald", 91)], [N1]),
 (179, "Grasiger Saum am Feldrand unter dem Baum 200165", "nicht_sauber", "3.4", F,
  [("klasse", "Grünlicher Randstreifen bei 440/401, kein Wald")], [N1]),
 (170, "Große gemähte Fläche mit gebogenen Heuschwaden (Mahdspuren), von Gärten, Gehölz und Wiese umgeben", "nicht_sauber", "3.1.1", F,
  [("klasse", "Helle Schwaden mit grünlichen Streifen dazwischen, die der Feldform folgen, bei 479/479: gemähte Wiese bzw. Feld, kein unbefestigter Weg; Getreidestoppel (2.2) nicht ganz ausgeschlossen"),
   ("sonstiges", "Am Südrand bei 150/505 liegt ein heller, weißlicher Randstreifen (Feldrain bzw. trockener Boden) im Segment; als 3.4 abtrennen möglich", 900),
   ("sonstiges", "Viele kleine Randstücke (v3: 200184, 200183, 200188, 200187, 200191, 200195, 200196, 200199, 200200, 200202; v4: 200175, 200186) gehören zu dieser Fläche (bei 230/429)", None)],
  [N1, N2, N3, N4, R]),
 (203, "Heller grasiger Saum am Südwestrand des Feldes neben dem Baum 200197", "nicht_sauber", "3.4", F,
  [("klasse", "Feldrain zwischen Feld und Gehölz bei 327/544; als Saum statt flächiger Wiese")], [N3]),
 (206, "Baumkrone am unteren Kernrand, größter Teil im Kontextrand", "sauber", None, T, [], [N3]),
 (208, "Kleines Randstück der Krone 200206", "nicht_sauber", "4.2.1", F,
  [("verschmelzen", "Dunkle Krone bei 337/556 mit 200206 verschmelzen, kein eigener Wald", 114)], [N3]),
 (211, "Wiese am unteren Kernrand, im Kern nur ein kleines Stück", "sauber", None, T, [], [N3]),
 (209, "Heller Saum am Südrand des Feldes", "nicht_sauber", "3.4", F,
  [("klasse", "Heller Feldrain bei 362/560 zwischen Feld und Wiese; Saum statt Wiese")], [N3]),
]
NAHT = [
 {"id": 200170, "seite": "rechts", "text": "Feld reicht über den rechten, unteren und linken Kernrand; Klassenvorschlag 3.1.1 gilt in allen Teilkacheln"},
 {"id": 200206, "seite": "unten", "text": "Baumkrone über dem unteren Kernrand; Klasse passt auf beiden Seiten"},
 {"id": 200211, "seite": "unten", "text": "Wiese über dem unteren Kernrand; Klasse passt"},
]
UNSICHER = [
 "200103 (v2): enthält am Nordrand des Feldes einen grasigen Randstreifen (bei 500/370), der zum Saum gehört",
 "200171 (v3): Grasstreifen mit Hecke, als Wald eingetragen",
 "200134 (v2): große Krone, 200150 gehört dazu",
]
NICHT_GEPRUEFT = ["Bildkanten nicht mit dem Werkzeug kante nachgemessen; Grenzurteile nur nach Augenschein",
                  "uebersicht_vorschlag, uebersicht_kontrast und die Roh-Nahansichten dieses Viertels nicht geöffnet; die Vorstufen-Klassen stehen in der Liste"]
OFFEN = [
 "200170: Wiese mit Heuschwaden (3.1.1) oder Getreidestoppel mit Strohschwaden (2.2); ohne Fremddaten nicht sicher, Elternklasse wäre je nach Fall 3.1 bzw. 2",
 "200140: helle, rechteckig begrenzte abgenutzte Stelle bei 432/306, ob kahles Beet oder abgetretener Rasen",
 "200153, 200165: eine große Krone oder mehrere Bäume nicht sicher",
 "200164: Hecke (4.2.3) oder Strauchreihe (4.2.4) nicht unterscheidbar",
]
