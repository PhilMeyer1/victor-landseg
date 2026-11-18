VIERTEL = "v1"
U, R, K = "uebersicht_nummern.jpg", "uebersicht_roh.jpg", "uebersicht_kontrast.jpg"
N1, N2, N3, N4 = "nah1_nummern.jpg", "nah2_nummern.jpg", "nah3_nummern.jpg", "nah4_nummern.jpg"
R1, R2, R3, R4 = "nah1_roh.jpg", "nah2_roh.jpg", "nah3_roh.jpg", "nah4_roh.jpg"
UEBERSICHT_GESEHEN = [U, R, K, "uebersicht_vorschlag.jpg"]
NAH_GESEHEN = [N1, R1, N2, R2, N3, R3, N4, R4]
NAH_EIGENE = ["nah_1.jpg", "nah_2.jpg", "nah_3.jpg", "nah_4.jpg", "nah_5.jpg", "kontrast_1.jpg", "kontrast_2.jpg", "kontrast_3.jpg"]

V = 100000
SW_FELD = "Acker oder Grünland im Schwarz-Weiß-Bild nicht zu trennen"
SEGMENTE = [
 (V+1, "FELD", False, "sauber", "Dunkle, gleichmäßig gekörnte Feldfläche links der Straße; im Kern nur die obere linke Ecke.", [], [U, R1, "kontrast_1.jpg"]),
 (V+58, "FELDRAIN", False, "sauber", "Fleckiger Streifen am Feldrand zwischen Feld 1 und dem Wegrain, Grauton fast wie das Feld.", [], [U, R1, "kontrast_1.jpg"]),
 (V+52, "FELDRAIN", False, "sauber", "Feldrand am Wegrain mit einem dunklen Fleck (Busch?) bei 108/90.", [], [U, R1, "kontrast_1.jpg"]),
 (V+57, "WEGRAIN", False, "sauber", "Heller Streifen direkt neben der Fahrbahn links der Straße.", [], [U, R1, "kontrast_1.jpg"]),
 (V+47, "WEGRAIN", False, "sauber", "Wegrain links der Straße am oberen Kernrand, mittelgrau.", [], [U, R1, "kontrast_1.jpg"]),
 (V+25, "WEGRAIN", False, "sauber", "Nur 10 Bildpunkte im Kern: Rand der Straße oben am Kernrand.", [], [U, R1]),
 (V+61, "NEBENGEB", False, "sauber", "Schmaler heller Streifen parallel zur Straße zwischen Straßenrand und Vorhof (143–160/85–108): kleiner Bau oder Mauerkrone.", [], [U, R1, "kontrast_2.jpg", "nah_1.jpg"]),
 (V+33, "STRASSENRAND", False, "sauber", "Mittelgrauer Streifen zwischen Fahrbahn und den Hofeinfahrten rechts der Straße.", [], [U, R1, "kontrast_1.jpg"]),
 (V+43, "HOF", False, "sauber", "Schlagschatten des Längsbaus 17 auf dem Hof des Grundstücks darunter; Untergrund kaum sichtbar.", [], [U, R2, "nah_1.jpg"]),
 (V+35, "GARTEN", False, "sauber", "Von dunklen Mauerlinien umrahmtes Rechteck mit fleckigem Grau (Garten); hinten ein heller Fleck 255–273/92–107.", [], [U, R2, "nah_3.jpg"]),
 (V+17, "LAENGSBAU", True, "sauber", "Helles Dach eines langen Streckhof-Längsbaus am oberen Kernrand, Schlagschatten 43 an seiner Südwestseite.", [], [U, R2, "nah_3.jpg"]),
 (V+34, "HOF", False, "sauber", "Dunkle Fläche neben dem Längsbau 17: Hof im Schatten des Nachbarbaus.", [], [U, R2, "nah_3.jpg"]),
 (V+48, "HOF", False, "nicht_sauber", "Dunkle Hoffläche im Schatten plus dunkle Mauerlinie am hinteren Gartenende von 35, reicht bis in v2.", [
     ("sonstiges", "Mischfläche aus beschattetem Hof (285–305/64–95) und der Schattenlinie der hinteren Gartenmauer (250–280/95–130); im Schwarz-Weiß-Bild nicht sicher zu trennen.", (290, 80), None)], [U, R2, "nah_3.jpg"]),
 (V+7, "HOF", False, "sauber", "Nur 1 Bildpunkt im Kern (309/64); Hauptteil im Kontextrand.", [], [U]),
 (V+10, "HOF", False, "sauber", "Hellgraue offene Fläche oben rechts am Kernrand (297–323/64–84), Übergang zum Hinterweg.", [], [U, R2, "nah_3.jpg"]),
 (V+90, "FELD", False, "sauber", "Dunkler Feldrand links unten am Wegrain, Grauton wie Feld 1.", [], [U, R1]),
 (V+97, "WEGRAIN", False, "sauber", "Kleines Stück Wegrain am linken Kernrand.", [], [U, R1]),
 (V+85, "WEGRAIN", False, "sauber", "Heller Streifen direkt links der Fahrbahn am linken Kernrand.", [], [U, R1, "kontrast_1.jpg"]),
 (V+68, "FELDRAIN", False, "sauber", "Feldrand mit dunklem Fleck (Busch?) bei 88/112, Grauton fast wie das Feld.", [], [U, R1, "kontrast_1.jpg"]),
 (V+74, "WEGRAIN", False, "sauber", "Mittelgrauer Wegrain links der Fahrbahn.", [], [U, R1, "kontrast_1.jpg"]),
 (V+67, "WEGRAIN", False, "sauber", "Mittelgrauer Wegrain links der Fahrbahn.", [], [U, R1, "kontrast_1.jpg"]),
 (V+88, "STRASSENRAND", False, "sauber", "Gleichmäßig mittelgrauer Streifen rechts der Fahrbahn vor den Höfen.", [], [U, R1, "kontrast_1.jpg"]),
 (V+4, "FAHRWEG", False, "sauber", "Helle, etwa 10 Bildpunkte breite Straße diagonal durch das Viertel; schließt rechts ein schmales Stück Straßenrand ein.", [], [U, R1, "kontrast_1.jpg"]),
 (V+91, "HOF", False, "sauber", "Kleine beschattete Fläche zwischen Straßenrand 88 und Hof 93.", [], [U, R1, "nah_4.jpg"]),
 (V+93, "HOF", False, "nicht_sauber", "Hof im Schlagschatten des Längsbaus 253; enthielt den hellen Längsbau 251, der abgetrennt wurde.", [
     ("trennen", "Heller Längsbau 113–131/152–182 steckte im Schattenhof; abgetrennt als 251 (Eingriff 2).", (122, 167), 192)], [U, N1, "nah_4.jpg", "nah_1.jpg"]),
 (V+251, "LAENGSBAU", True, "sauber", "Schmales helles Dach eines Längsbaus, quer zur Straße, Schlagschatten 99 an der Südwestseite (neu aus 93).", [], ["nah_1.jpg", "nah_4.jpg", N1]),
 (V+72, "STRASSENRAND", False, "sauber", "Kleines mittelgraues Stück Straßenrand rechts der Fahrbahn.", [], [U, R1, "kontrast_1.jpg"]),
 (V+78, "HOF", False, "sauber", "Mittelgrauer Vorhof hinter dem Straßenrand mit dunklem Fleck bei 122/125.", [], [U, R1, "kontrast_2.jpg"]),
 (V+65, "HOF", False, "sauber", "Mittelgrauer Vorhof des Grundstücks zwischen Straßenrand und Garten 51.", [], [U, R1, "kontrast_2.jpg"]),
 (V+76, "HOF", False, "nicht_sauber", "Hofstreifen mit einem schmalen hellen Längsbau entlang der Südwestseite; den hellen Endbau hinten (254) abgetrennt.", [
     ("trennen", "Weißer Bau am hinteren Ende 214–230/139–160 abgetrennt als 254 (Eingriff 4).", (222, 150), 211),
     ("trennen", "Schmaler heller Streifen 187/118 bis 215/148 an der Südwestseite ist vermutlich ein Längsbau; Kante zur Hoffläche nicht eindeutig, nicht geteilt.", (200, 132), None)], [U, R2, "nah_1.jpg", "kontrast_2.jpg"]),
 (V+254, "NEBENGEB", False, "sauber", "Weißer rechteckiger Bau am hinteren Ende des Hofs 76 (neu aus 76); auch heller Belag möglich.", [], ["nah_1.jpg", R2]),
 (V+51, "GARTEN", False, "nicht_sauber", "Langes Gartenrechteck mit Mauerlinien, vorn und am Nordostrand beschattet; den hellen Längsbau vorn (250) abgetrennt.", [
     ("trennen", "Heller Längsbau 166–189/67–87 am vorderen Ende abgetrennt als 250 (Eingriff 1).", (177, 77), 161),
     ("sonstiges", "Vorderer, beschatteter Teil 162–219/90–136 ist eher Hof als Garten; Grenze im Schatten nicht sichtbar.", (180, 105), None)], [U, R2, "nah_1.jpg", "nah_5.jpg"]),
 (V+250, "LAENGSBAU", True, "sauber", "Helles Dach eines Längsbaus an der Straßenseite des Grundstücks 51, Schatten im Vorhof daneben (neu aus 51).", [], ["nah_1.jpg", N1]),
 (V+80, "ANGER", False, "sauber", "Gleichmäßig graues Stück der offenen Fläche 77; gleiche Fläche, Grenze ohne Bildkante.", [
     ("verschmelzen", "Gehört zur Fläche 77, keine Bildkante dazwischen.", (277, 127), 182)], [U, R2, "nah_3.jpg"]),
 (V+64, "FELDWEG", False, "sauber", "Heller Hinterweg hinter den Gärten 35/51 mit sehr hellem Fleck 298–318/105–120 (Gegenstand oder heller Boden).", [], [U, R2, "nah_3.jpg"]),
 (V+108, "STRASSENRAND", False, "sauber", "Mittelgrauer Straßenrand rechts der Fahrbahn.", [], [U, N1, R3]),
 (V+98, "STRASSENRAND", False, "sauber", "Mittelgrauer Straßenrand rechts der Fahrbahn.", [], [U, N1]),
 (V+99, "HOF", False, "nicht_sauber", "Vorhof im Schlagschatten des Längsbaus 251; den hellen Längsbau 262 an der Straßenseite abgetrennt.", [
     ("trennen", "Heller Längsbau 88–101/179–200 abgetrennt als 262 (Eingriff 5).", (94, 190), 180)], [U, N1, N3, "nah_4.jpg"]),
 (V+262, "LAENGSBAU", False, "sauber", "Heller, länglicher, etwas unscharfer Bau an der Straßenseite (neu aus 99).", [], ["nah_1.jpg", "nah_4.jpg"]),
 (V+105, "HOF", False, "sauber", "Hof hinter dem Längsbau 251 mit hellen und beschatteten Flecken.", [], [U, N3, "nah_4.jpg"]),
 (V+75, "HOF", False, "nicht_sauber", "Langer Hof im Schlagschatten des Baus 76; den hellen Längsbau 253 abgetrennt.", [
     ("trennen", "Hellster Dachstreifen 152–170/142–164 abgetrennt als 253 (Eingriff 3).", (161, 152), 187),
     ("trennen", "Links daneben ein zweiter, mattheller Dachstreifen 136–151/144–160 (andere Dachseite?), Kante unscharf, nicht geteilt.", (143, 152), None)], [U, N1, "nah_4.jpg", "kontrast_2.jpg"]),
 (V+253, "LAENGSBAU", True, "sauber", "Helles Dach eines Längsbaus mit Schlagschatten 93 an der Südwestseite (neu aus 75).", [], ["nah_1.jpg", "nah_4.jpg"]),
 (V+106, "HOF", False, "sauber", "Heller Hof hinten im Grundstück, mit dünner heller Mauer- oder Zaunlinie.", [], [U, N2, "nah_4.jpg"]),
 (V+113, "SCHATTEN", False, "sauber", "Fast schwarze, scharf begrenzte Fläche 197–211/183–201 am Hofende, rundum von Hof 75 umgeben; Schatten oder dunkles Dach.", [], [U, N2, R4]),
 (V+77, "ANGER", False, "sauber", "Offene, fleckig mittelgraue Fläche hinter den Gärten mit hellen Fahrspuren.", [], [U, R2, R4, "kontrast_3.jpg"]),
 (V+122, "ANGER", False, "sauber", "Kleines Stück der offenen Fläche zwischen 77 und 104.", [], [U, N4, R4]),
 (V+103, "ANGER", False, "sauber", "Stück der offenen Fläche zwischen 77 und 104, gleicher Grauton.", [], [U, N2, R4]),
 (V+115, "NEBENGEB", False, "sauber", "Weißes, scharf begrenztes Quadrat 294–313/185–203 auf der offenen Fläche: kleiner Bau mit hellem Dach oder heller Haufen.", [], [U, N4, R4]),
 (V+124, "STRASSENRAND", False, "sauber", "Nur 18 Bildpunkte im Kern: Straßenrand am linken Kernrand.", [], [U, N3]),
 (V+136, "SCHATTEN", False, "sauber", "Dunkle unscharfe Fläche am linken Kernrand (64–81/216–246): Schatten eines Baus im Kontextrand oder Gehölz.", [], [U, N3, "nah_2.jpg"]),
 (V+116, "HOF", False, "nicht_sauber", "Vorhof im Schlagschatten des Längsbaus 262; unten links ein heller Dachrest 65–76/204–216 am Kernrand.", [
     ("trennen", "Heller Dachrest 65–76/204–216 (etwa 74 Bildpunkte) gehört vermutlich zu einem Längsbau im Kontextrand; zu klein und am Kernrand, nicht geteilt.", (70, 210), 74)], [U, N3, "nah_2.jpg"]),
 (V+147, "HOF", False, "sauber", "Heller Fleck im Hof 129 (offener Boden).", [], [U, N3, "nah_2.jpg"]),
 (V+121, "HINTERGEB", False, "sauber", "Helles, scharf begrenztes Rechteck quer im Grundstück, dunkler Saum an der Südwestseite; helles Dach oder heller befestigter Platz.", [], [U, N3, R3, "nah_4.jpg"]),
 (V+132, "SCHATTEN", False, "sauber", "Dunkle Fläche südwestlich des dunklen Baus 120 und hinter 121: Schlagschatten, Untergrund nicht erkennbar.", [], [U, N3, R3]),
 (V+120, "HINTERGEB", False, "sauber", "Dunkles, gerade begrenztes Rechteck am Hofende mit Schatten 132 an der Südwestseite: Bau mit dunklem Dach.", [], [U, N3, R3, "nah_4.jpg"]),
 (V+134, "HINTERGEB", False, "sauber", "Dunkelgraues Quadrat 247–298/211–259 mit dunklem Saum an der Südwestseite: Scheune mit dunklem Dach; auch dunkler Garten möglich.", [], [U, N4, R4, "kontrast_3.jpg"]),
 (V+129, "HOF", False, "sauber", "Offener, fleckig heller Hof- und Lagerplatz mit kleinem hellen Fleck 92–104/262–281 (Schuppen?).", [], [U, N3, R3, "nah_2.jpg"]),
 (V+138, "GARTEN", False, "sauber", "Gleichmäßig dunkelgraues Rechteck mit Schattenlinie von 121 an der Nordostseite: Garten oder dunkles Dach.", [], [U, N3, R3, "nah_2.jpg"]),
 (V+114, "ANGER", False, "sauber", "Breiter offener Streifen zwischen Hofenden und Feld 154 mit heller diffuser Fahrspur, zieht nach unten links in v3.", [], [U, N4, R4, "kontrast_3.jpg"]),
 (V+163, "FELDRAIN", False, "sauber", "Mittelgrauer Randstreifen zwischen Feld 154 und der offenen Fläche 104.", [], [U, N4, R4]),
 (V+160, "BRACHE", False, "sauber", "Fleckig mittelgraue Fläche links des Angers 114, ohne Struktur; Brache oder Garten.", [], [U, N3, "kontrast_3.jpg"]),
 (V+171, "ANGER", False, "sauber", "Hellerer Fleck am Rand des Angers 114; gleiche Fläche.", [
     ("verschmelzen", "Gehört zum Anger 114, keine klare Bildkante.", (101, 301), 170)], [U, N3, "kontrast_3.jpg"]),
 (V+168, "FELDRAIN", False, "sauber", "Dunkler Streifen zwischen Anger 114 und Feld 154.", [], [U, N4, R4, "kontrast_3.jpg"]),
]

EINGRIFFE = [
 {"schritt": "teilen", "vorher": [V+51], "nachher": [V+51, V+250], "grund": "Der helle Längsbau an der Straßenseite (166–189/67–87) steckte im Gartensegment 51; ein dabei entstandener Splitter (100249, 2 px) wurde wieder mit 250 verschmolzen."},
 {"schritt": "teilen", "vorher": [V+93], "nachher": [V+93, V+251], "grund": "Der helle Längsbau (113–131/152–182) steckte im Schattenhof 93; Splitter 100252 (2 px) wieder mit 251 verschmolzen."},
 {"schritt": "teilen", "vorher": [V+75], "nachher": [V+75, V+253], "grund": "Der hellste Dachstreifen eines Längsbaus (152–170/142–164) steckte im Hof 75."},
 {"schritt": "teilen", "vorher": [V+76], "nachher": [V+76, V+254], "grund": "Der weiße Bau am hinteren Hofende (214–230/139–160) steckte im Hof 76; sieben Splitter (100255–100261, je 2–10 px) wieder mit 254 verschmolzen."},
 {"schritt": "teilen", "vorher": [V+99], "nachher": [V+99, V+262], "grund": "Der helle Längsbau an der Straßenseite (88–101/179–200) steckte im Schattenhof 99; Splitter 100263/100264 wieder mit 262 verschmolzen."},
]

NAHT = []
UNSICHER = [
 "100104 (v2): gleiche offene Fläche wie 77/103/122 (Anger); Grenze 77|104 ohne Bildkante.",
 "100154 (v3/v4): Feld; der dunkle Streifen 168 an seinem Rand könnte auch Feld sein.",
 "100173, 100181 (v3/Kontext): Fortsetzung des Angers 114 nach unten links.",
]
NICHT_GEPRUEFT = []
OFFEN = [
 "Felder 1, 90 (und Ränder 52, 58, 68): " + SW_FELD + "; im Farbbild entscheidet Grün (Grünland) gegen Braun/Streifen (Acker).",
 "Straße 4, Straßenränder 33/72/88/98/108/124 und Hinterweg 64: Belag (Schotter, Erde, Asphalt) im Schwarz-Weiß-Bild nicht bestimmbar; im Farbbild Grauton/Farbe der Fahrbahn.",
 "Höfe im Schatten (43, 34, 48, 91, 93, 99, 116): Untergrund unter dem Schlagschatten nicht sichtbar; als Hof angenommen.",
 "121 und 134, 120: Dach oder befestigter Platz? 121 hat nur 1–2 Bildpunkte Schatten an der Südwestseite, 134 und 120 sind dunkel; im Farbbild Ziegel- oder Blechfarbe gegen Boden.",
 "35 und 51, 138: Garten oder Hof (Wiese, Gemüse, gestampfter Boden)? Im Farbbild Grün gegen Braun; heller Fleck 255–273/92–107 in 35 unklar (Schuppen oder heller Boden).",
 "76: schmaler Längsbau an der Südwestseite (187/118–228/152) vermutlich im Hofsegment, nicht geteilt, weil die Kante zur Hoffläche nicht eindeutig ist.",
 "113, 132, 136: Schlagschatten oder dunkles Dach/Gehölz; Untergrund nicht erkennbar.",
 "115, 254, 61: kleine helle Flächen, Bau oder heller Boden/Haufen.",
 "Nachsegmentieren in zwei Stapeln statt einem: Der erste Stapel (eingriffe.json, 5 Teilungen) ließ Splitter von 1–10 Bildpunkten entstehen, der zweite (eingriffe_2.json, 4 Verschmelzungen) hat sie wieder den neuen Bauten zugeschlagen; Karte danach lückenlos (pruefen ok).",
]
