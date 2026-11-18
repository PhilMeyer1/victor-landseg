VIERTEL = "v1"
U, R = "uebersicht_nummern.jpg", "uebersicht_roh.jpg"
N1, N2, N3, N4 = "nah1_nummern.jpg", "nah2_nummern.jpg", "nah3_nummern.jpg", "nah4_nummern.jpg"
R1, R2, R3, R4 = "nah1_roh.jpg", "nah2_roh.jpg", "nah3_roh.jpg", "nah4_roh.jpg"
K5, K6 = "kontrast_5.jpg", "kontrast_6.jpg"
UEBERSICHT_GESEHEN = [U, R]
NAH_GESEHEN = [N1, R1, N2, R2, N3, R3, N4, R4]
NAH_EIGENE = [K5, K6]

V = 100000
SEGMENTE = [
 (V+1, "FELD", False, "sauber", "Dunkle, gleichmäßig gekörnte Feldfläche links der Straße (Grau 56); im Kern nur die Ecke oben links.", [], [U, N1, R1]),
 (V+58, "FELDRAIN", False, "sauber", "Etwas hellerer, fleckiger Feldrand zwischen Feld 1 und dem Straßenrand 67.", [], [U, N1, R1]),
 (V+52, "FELDRAIN", False, "sauber", "Feldrand mit einem dunklen Fleck (Busch?) um 108/90, zwischen Feld 1 und Wegrain 47.", [], [U, N1, R1]),
 (V+57, "STRASSENRAND", False, "sauber", "Hellerer Streifen direkt links der Fahrbahn 4 (Grau 100), Bankett oder Grünstreifen.", [], [U, N1, R1]),
 (V+47, "WEGRAIN", False, "sauber", "Fleckiger Rain links der Straße am oberen Kernrand mit dunklen Flecken (Gebüsch?).", [], [U, N1, R1]),
 (V+25, "STRASSENRAND", False, "sauber", "Nur 10 Bildpunkte im Kern (138–141/64–68): Rand der Straße am oberen Kernrand.", [], [U, N1]),
 (V+61, "NEBENGEB", False, "sauber", "Schmaler heller Streifen 143–180/85–107 zwischen Straßenrand und Vorhof 65: kleiner Bau oder Mauerkrone.", [], [U, N1, R1]),
 (V+33, "STRASSENRAND", False, "sauber", "Mittelgrauer Streifen rechts der Fahrbahn vor den Hofeinfahrten (Grau 97).", [], [U, N1, R1]),
 (V+43, "HOF", False, "sauber", "Fast schwarze Fläche 160–213/64–86 vor dem Garten 51 und dem Längsbau 250: beschatteter Vorhof.", [], [U, N2, R2, K5]),
 (V+35, "GARTEN", False, "sauber", "Rechteck 194–273/64–121, rundum von einer dünnen dunklen Linie (Mauer, Zaun) gefasst, fein gekörntes Grau; hinten ein heller Fleck 255–273/92–107.", [], [U, N2, R2, K5]),
 (V+17, "LAENGSBAU", True, "sauber", "Helles langes Dach eines Streckhof-Längsbaus am oberen Kernrand, fast schwarzer Schatten 34 daneben.", [], [U, N2, R2, K5]),
 (V+34, "HOF", False, "sauber", "Fast schwarze Fläche rechts des Längsbaus 17: Hof im Schlagschatten.", [], [U, N2, R2]),
 (V+48, "HOF", False, "nicht_sauber", "Beschatteter Hof oben rechts plus die dunkle Linie am hinteren Ende von Garten 35, reicht in v2.", [
     ("sonstiges", "Mischfläche aus beschattetem Hof (285–305/64–95) und der Schattenlinie hinter Garten 35 (250–280/95–130); im Schwarz-Weiß-Bild ohne sichere Kante, nicht geteilt.", (290, 82), None)], [U, N2, R2, K5]),
 (V+7, "HOF", False, "sauber", "Nur 1 Bildpunkt im Kern (309/64); Hauptteil im Kontextrand.", [], [U]),
 (V+10, "HOF", False, "sauber", "Hellgraue offene Fläche oben rechts am Kernrand (297–323/64–84), Übergang zum Hinterweg 64; Hauptteil im Kontextrand.", [], [U, N2, R2]),
 (V+90, "FELD", False, "nicht_sauber", "Dunkler Feldrand links unten (Grau 56 wie Feld 1); Vorstufe nennt Sportplatz, im Bild aber Feld.", [
     ("verschmelzen", "Gleicher Grauton und gleiches Korn wie Feld 1, keine Bildkante bei 70/135; gehört zu Feld 1.", (70, 140), 129)], [U, N1, R1]),
 (V+97, "WEGRAIN", False, "sauber", "Kleines Stück Rain am linken Kernrand zwischen Feld 90 und Straßenrand 85.", [], [U, N1]),
 (V+85, "STRASSENRAND", False, "sauber", "Hellerer Streifen direkt links der Fahrbahn am linken Kernrand.", [], [U, N1, R1]),
 (V+68, "FELDRAIN", False, "sauber", "Feldrand mit dunklem Fleck (Busch?) um 88/112, Grauton fast wie Feld 1.", [], [U, N1, R1]),
 (V+74, "STRASSENRAND", False, "sauber", "Mittelgrauer Streifen links der Fahrbahn, Bankett oder Grünstreifen.", [], [U, N1, R1]),
 (V+67, "STRASSENRAND", False, "sauber", "Mittelgrauer Streifen links der Fahrbahn, Bankett oder Grünstreifen.", [], [U, N1, R1]),
 (V+88, "STRASSENRAND", False, "sauber", "Gleichmäßig mittelgrauer Streifen rechts der Fahrbahn vor den Höfen.", [], [U, N1, R1]),
 (V+4, "FAHRWEG", False, "sauber", "Helle, etwa 10 Bildpunkte breite Straße diagonal durch das Viertel (Grau 159).", [], [U, R, N1, R1]),
 (V+91, "HOF", False, "sauber", "Kleine beschattete Fläche zwischen Straßenrand 88 und Hof 93.", [], [U, N1, R1]),
 (V+93, "HOF", False, "nicht_sauber", "Hof im Schatten neben dem Längsbau 251; der helle Längsbau wurde abgetrennt.", [
     ("trennen", "Heller Längsbau 113–131/156–182 steckte im Schattenhof; abgetrennt als 251.", (122, 168), 194)], [U, N1, R1]),
 (V+251, "LAENGSBAU", True, "sauber", "Schmales helles Dach eines Längsbaus quer zur Straße (neu aus 93).", [], [U, N1, R1]),
 (V+72, "STRASSENRAND", False, "sauber", "Kleines mittelgraues Stück Straßenrand rechts der Fahrbahn.", [], [U, N1, R1]),
 (V+78, "HOF", False, "sauber", "Mittelgrauer Vorhof hinter dem Straßenrand mit dunklem Fleck um 122/125.", [], [U, N1, R1]),
 (V+65, "HOF", False, "sauber", "Mittelgrauer Vorhof zwischen Straßenrand und Garten 51.", [], [U, N1, R1]),
 (V+76, "HOF", False, "nicht_sauber", "Hofstreifen mit schmalem hellem Streifen an der Südwestseite; der helle Bau hinten (254) wurde abgetrennt.", [
     ("trennen", "Weißer Bau am hinteren Ende 214–231/139–160 abgetrennt als 254.", (222, 150), 240),
     ("trennen", "Schmaler heller Streifen von 187/118 bis 215/148 ist vermutlich ein Längsbau oder die helle Dachseite; Kante zur Hoffläche unscharf, nicht geteilt.", (200, 132), None)], [U, N2, R2, K5]),
 (V+254, "NEBENGEB", False, "sauber", "Weißer rechteckiger Bau am hinteren Ende von Hof 76 (neu aus 76); auch heller Belag möglich.", [], [U, N2, R2, K5]),
 (V+51, "GARTEN", False, "nicht_sauber", "Langes Rechteck mit dünnen dunklen Rändern und fein gekörntem Grau; vorn der helle Längsbau 250 abgetrennt.", [
     ("trennen", "Heller Längsbau 166–189/67–87 am vorderen Ende abgetrennt als 250.", (177, 77), 161),
     ("sonstiges", "Vorderer beschatteter Teil 162–219/90–136 eher Hof als Garten; Grenze im Schatten nicht sichtbar, nicht geteilt.", (190, 110), None)], [U, N2, R2, K5]),
 (V+250, "LAENGSBAU", True, "sauber", "Helles Dach eines Längsbaus an der Straßenseite des Grundstücks 51 (neu aus 51).", [], [U, N1, N2, K5]),
 (V+80, "ANGER", False, "nicht_sauber", "Gleichmäßig graues Stück der offenen Fläche 77 (Grau 100 gegen 96).", [
     ("verschmelzen", "Keine Bildkante zu 77 bei 277/127; gleiche Fläche.", (277, 127), 182)], [U, N2, R2]),
 (V+64, "FELDWEG", False, "sauber", "Heller Hinterweg hinter den Gärten 35/51 mit sehr hellem Fleck 298–318/105–120 (Gegenstand oder heller Boden).", [], [U, N2, R2, K5]),
 (V+108, "STRASSENRAND", False, "sauber", "Mittelgrauer Straßenrand rechts der Fahrbahn.", [], [U, N1, N3]),
 (V+98, "STRASSENRAND", False, "sauber", "Mittelgrauer Straßenrand rechts der Fahrbahn.", [], [U, N1, R1]),
 (V+99, "HOF", False, "nicht_sauber", "Vorhof im Schatten; den hellen Längsbau an der Straßenseite (262) abgetrennt.", [
     ("trennen", "Heller Längsbau 86–101/179–200 abgetrennt als 262.", (93, 190), 180)], [U, N1, R1]),
 (V+262, "LAENGSBAU", False, "sauber", "Heller, länglicher, etwas unscharfer Bau an der Straßenseite (neu aus 99).", [], [U, N1, R1, N3]),
 (V+105, "HOF", False, "sauber", "Hof hinter dem Längsbau 251 mit hellen und beschatteten Flecken (Grau 101±35).", [], [U, N3, R3]),
 (V+75, "HOF", False, "nicht_sauber", "Langer Hof im Schatten neben 76; den hellsten Dachstreifen (253) abgetrennt; hinten bei 113 ein heller Fleck.", [
     ("trennen", "Hellster Dachstreifen 152–170/142–164 abgetrennt als 253.", (161, 153), 187),
     ("trennen", "Links daneben ein zweiter, matthellerer Dachstreifen 136–151/144–160; Kante unscharf, nicht geteilt.", (143, 152), None),
     ("sonstiges", "Hinteres Ende 198–215/185–200 hell (Boden oder Bau) im selben Segment wie der Schattenhof.", (206, 196), None)], [U, N1, N4, R4]),
 (V+253, "LAENGSBAU", True, "sauber", "Helles Dach eines Längsbaus (neu aus 75).", [], [U, N1, R1]),
 (V+106, "HOF", False, "sauber", "Heller Hof hinten im Grundstück, mit dünner heller Mauer- oder Zaunlinie.", [], [U, N4, R4]),
 (V+113, "SCHATTEN", False, "sauber", "Fast schwarze, scharf begrenzte Fläche 197–211/183–201, ringsum von Hof 75: Schatten, dunkles Dach oder Grube.", [], [U, N4, R4]),
 (V+77, "ANGER", False, "sauber", "Offene, fleckig mittelgraue Fläche hinter den Gärten mit hellen Fahrspuren (Grau 96).", [], [U, N2, R2, N4, R4]),
 (V+122, "ANGER", False, "nicht_sauber", "Kleines Stück der offenen Fläche zwischen 77 und 104.", [
     ("verschmelzen", "Keine Bildkante zu 77 bei 285/198; gleicher Grauton.", (285, 198), 114)], [U, N4, R4]),
 (V+103, "ANGER", False, "nicht_sauber", "Stück der offenen Fläche zwischen 77 und 104, gleicher Grauton.", [
     ("verschmelzen", "Keine Bildkante zu 77 bei 300/170; gleiche Fläche.", (300, 170), 369)], [U, N2, R2, N4]),
 (V+115, "NEBENGEB", False, "sauber", "Weißes, scharf begrenztes Viereck 294–313/185–203 auf der offenen Fläche: kleiner Bau mit hellem Dach oder heller Haufen.", [], [U, N4, R4]),
 (V+124, "STRASSENRAND", False, "sauber", "Nur 18 Bildpunkte im Kern: Straßenrand am linken Kernrand.", [], [U, N3]),
 (V+136, "SCHATTEN", False, "sauber", "Dunkle unscharfe Fläche am linken Kernrand (64–81/216–246): Schatten eines Baus im Kontextrand oder Gehölz.", [], [U, N3, R3, K6]),
 (V+116, "HOF", False, "nicht_sauber", "Vorhof im Schatten; am linken Kernrand ein heller Dachrest.", [
     ("trennen", "Heller Dachrest 65–76/204–216 (etwa 70 Bildpunkte) gehört vermutlich zu einem Längsbau im Kontextrand; am Kernrand, nicht geteilt.", (70, 210), 70)], [U, N3, R3]),
 (V+147, "HOF", False, "sauber", "Heller Fleck offenen Bodens im Hof 129.", [], [U, N3, R3, K6]),
 (V+121, "HINTERGEB", True, "sauber", "Helles, scharf begrenztes Rechteck quer im Grundstück, daneben der fast schwarze Schatten 132: Bau mit hellem Dach.", [], [U, N3, R3, K6]),
 (V+132, "SCHATTEN", False, "sauber", "Fast schwarze Fläche neben dem hellen Bau 121: Schlagschatten, Untergrund nicht erkennbar.", [], [U, N3, R3, K6]),
 (V+120, "HINTERGEB", False, "sauber", "Dunkles, gerade begrenztes Rechteck am Hofende: Bau mit dunklem Dach oder Schatten.", [], [U, N3, R3, K6]),
 (V+134, "GARTEN", False, "sauber", "Dunkelgraues, gerade begrenztes Viereck 247–298/211–259 mit dunklem Saum innen an der linken Seite (Mauerschatten): ummauerter Garten oder Bau mit dunklem Dach.", [], [U, N4, R4, K6]),
 (V+129, "HOF", False, "sauber", "Offener, fleckig heller Hof- und Lagerplatz mit kleinem hellem Fleck 92–104/262–281 (Schuppen?).", [], [U, N3, R3, K6]),
 (V+138, "GARTEN", False, "sauber", "Gleichmäßig dunkelgraues Rechteck mit gerader Kante, fein gekörnt: Garten oder Bau mit dunklem Dach.", [], [U, N3, R3, K6]),
 (V+114, "ANGER", False, "sauber", "Breiter offener Streifen zwischen Hofenden und Feld 154 mit heller, unscharfer Fahrspur; zieht nach unten links in v3.", [], [U, R, N3, R3, N4, R4, K6]),
 (V+163, "FELDRAIN", False, "sauber", "Mittelgrauer Randstreifen zwischen Feld 154 und der offenen Fläche 104.", [], [U, N4, R4, K6]),
 (V+160, "BRACHE", False, "sauber", "Fleckig mittelgraue Fläche links des Angers 114 ohne Struktur; Brache oder Garten, Hälfte in v3.", [], [U, N3, R3, K6]),
 (V+171, "ANGER", False, "nicht_sauber", "Etwas hellerer Fleck am Rand des Angers 114.", [
     ("verschmelzen", "Keine klare Bildkante zu 114 bei 101/301; gleiche Fläche.", (101, 301), 170)], [U, N3, R3, K6]),
 (V+168, "FELDRAIN", False, "sauber", "Dunkler Streifen zwischen Anger 114 und Feld 154 (Grau 64 gegen 77 im Feld).", [], [U, N3, N4, R4, K6]),
]

EINGRIFFE = [
 {"schritt": "teilen", "vorher": [V+51], "nachher": [V+51, V+250], "grund": "Der helle Längsbau an der Straßenseite (166–189/67–87) steckte im Gartensegment 51; ein Splitter (100249) wurde im zweiten Stapel wieder mit 250 verschmolzen."},
 {"schritt": "teilen", "vorher": [V+93], "nachher": [V+93, V+251], "grund": "Der helle Längsbau (113–131/156–182) steckte im Schattenhof 93; Splitter 100252 wieder mit 251 verschmolzen."},
 {"schritt": "teilen", "vorher": [V+75], "nachher": [V+75, V+253], "grund": "Der hellste Dachstreifen eines Längsbaus (152–170/142–164) steckte im Hof 75."},
 {"schritt": "teilen", "vorher": [V+76], "nachher": [V+76, V+254], "grund": "Der weiße Bau am hinteren Hofende (214–231/139–160) steckte im Hof 76; Splitter 100255–100261 wieder mit 254 verschmolzen."},
 {"schritt": "teilen", "vorher": [V+99], "nachher": [V+99, V+262], "grund": "Der helle Längsbau an der Straßenseite (86–101/179–200) steckte im Schattenhof 99; Splitter 100263/100264 wieder mit 262 verschmolzen."},
]

NAHT = []
UNSICHER = [
 "100104 (v2): gleiche offene Fläche wie 77/103/122; Grenze 77|104 ohne Bildkante.",
 "100154 (v3/v4): Feld; der dunkle Streifen 168 an seinem Rand könnte auch Feld sein.",
 "100173, 100181 (v3/Kontext): Fortsetzung des Angers 114 nach unten links.",
 "100264: diese ID entstand zuerst als Splitter im Stapel dieses Viertels und wurde verschmolzen; sie ist jetzt einem Segment aus 100045 (v2, 312–332/75–105) neu vergeben, kein Fehler dieses Viertels.",
]
NICHT_GEPRUEFT = [
 "uebersicht_kontrast.jpg, uebersicht_vorschlag.jpg, uebersicht_maengel.jpg, uebersicht_gitter.jpg nicht angesehen; statt dessen eigene Kontrastbilder kontrast_5.jpg und kontrast_6.jpg.",
]
OFFEN = [
 "Felder 1, 90 und Ränder 52, 58, 68: Acker oder Grünland im Schwarz-Weiß-Bild nicht zu trennen; im Farbbild entscheidet Grün (Grünland) gegen Braun/Streifen (Acker).",
 "Straße 4, Straßenränder 25/33/57/67/72/74/85/88/98/108/124 und Hinterweg 64: Belag und ob Bankett, Grünstreifen oder Gehweg, im Schwarz-Weiß-Bild nicht bestimmbar; im Farbbild Grün gegen Grau.",
 "Höfe im Schatten (34, 43, 48, 91, 93, 99, 116): Untergrund unter dem Schatten nicht sichtbar; als Hof angenommen.",
 "35, 51, 134, 138: Garten oder Dach? Gerade Kanten und gleichmäßiges Grau passen zu beidem; dünne dunkle Linien auf allen Seiten sprechen für Mauer/Zaun; im Farbbild Grün/Braun gegen Ziegelrot.",
 "120: Bau mit dunklem Dach oder tiefer Schatten; 113, 132, 136: Schatten, dunkles Dach oder Gehölz.",
 "115, 254, 61: kleine helle Flächen, Bau oder heller Boden/Haufen.",
 "76 und 75: helle Dachstreifen an der Seite nicht geteilt, weil die Kante zur Hoffläche unscharf ist.",
 "80, 103, 122 (zu 77), 90 (zu 1), 171 (zu 114): ohne Bildkante abgetrennte Stücke derselben Fläche; zum Verschmelzen vorgeschlagen, nicht ausgeführt.",
 "Das Nachsegmentieren lief in zwei Stapeln (eingriffe.json mit 5 Teilungen, eingriffe_2.json mit 4 Verschmelzungen von Splittern); die Karte ist danach lückenlos (pruefen ok). Dieser Nachholauf hat die Karte nicht weiter geändert.",
]
