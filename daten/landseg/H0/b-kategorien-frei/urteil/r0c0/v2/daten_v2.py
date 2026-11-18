VIERTEL = "v2"
U, R, K = "uebersicht_nummern.jpg", "uebersicht_roh.jpg", "uebersicht_kontrast.jpg"
N1, N2, N3, N4 = "nah1_nummern.jpg", "nah2_nummern.jpg", "nah3_nummern.jpg", "nah4_nummern.jpg"
R1, R2, R3, R4 = "nah1_roh.jpg", "nah2_roh.jpg", "nah3_roh.jpg", "nah4_roh.jpg"
UEBERSICHT_GESEHEN = [U, R]
NAH_GESEHEN = [N1, R1, N2, R2, N3, R3, N4, R4]
NAH_EIGENE = ["nah_1.jpg", "nah_2.jpg", "nah_3.jpg", "kontrast_1.jpg"]
A = "nah_2.jpg"
V = 100000
SEGMENTE = [
 (V+45, "HOF", False, "nicht_sauber", "Hof im Schlagschatten des Längsbaus 37/265; den hellen Längsbau 264 am linken Rand abgetrennt.", [
     ("trennen", "Heller Längsbau 312–332/75–105 abgetrennt als 264.", (322, 90), 272)], [U, N1, R1, A]),
 (V+264, "LAENGSBAU", True, "sauber", "Helles schmales Dach eines Längsbaus (neu aus 45), Schatten 48 an der Südwestseite.", [], [N1, A]),
 (V+41, "HOF", False, "sauber", "Hof im Schlagschatten des Längsbaus 265, Untergrund kaum sichtbar.", [], [U, N1, R1]),
 (V+37, "HOF", False, "nicht_sauber", "Hof im Schatten des Nachbarbaus 28; den hellen Längsbau 265 abgetrennt.", [
     ("trennen", "Heller Längsbau 395–428/78–114 abgetrennt als 265.", (410, 95), 282)], [U, N1, R1, A]),
 (V+265, "LAENGSBAU", True, "sauber", "Langes helles Dach eines Längsbaus (neu aus 37), Schatten 37 an der Südwestseite.", [], [N1, A]),
 (V+28, "HOF", False, "nicht_sauber", "Hof im Schatten zwischen zwei Längsbauten am oberen Kernrand; Dachstück 266 abgetrennt.", [
     ("trennen", "Helles Dachstück 418–432/65–80 im Kern abgetrennt als 266; der Rest des Dachs liegt im Kontextrand.", (425, 72), 166)], [U, N1, N2, A]),
 (V+266, "LAENGSBAU", False, "sauber", "Kernstück eines hellen Längsbaudachs am oberen Kernrand (neu aus 28).", [], [N2, A]),
 (V+50, "GARTEN", False, "sauber", "Kleine graue Fläche nördlich der Straße am oberen Kernrand, Garten oder Hof.", [], [U, N2, R2]),
 (V+12, "GARTEN", False, "sauber", "Kernstück einer großen Fläche im Kontextrand nördlich der Kreuzung; fleckig grau, Garten oder Feld.", [], [U, N2, R2]),
 (V+53, "GARTEN", False, "sauber", "Fleckige graue Fläche nördlich der Kreuzung, Garten oder Hof.", [], [U, N2, R2]),
 (V+54, "HOF", False, "sauber", "Gleichmäßig mittelgraue kleine Hoffläche nördlich der Kreuzung.", [], [U, N2, R2]),
 (V+60, "STRASSENRAND", False, "sauber", "Hellgrauer offener Platz an der Nordseite der Kreuzung, ohne Dach und Schatten.", [], [U, N2, R2]),
 (V+49, "HOF", False, "sauber", "Dunkle, beschattete kleine Fläche am oberen Kernrand.", [], [U, N2, R2]),
 (V+20, "HOF", False, "sauber", "Nur 7 Bildpunkte im Kern am oberen Kernrand.", [], [U, N2]),
 (V+46, "HOF", False, "sauber", "Mittelgrauer Hofstreifen zwischen den Längsbauten 42 und 56.", [], [U, N2, R2]),
 (V+56, "HOF", False, "nicht_sauber", "Hof im Schatten des Längsbaus 42; den hellen Längsbau 269 abgetrennt.", [
     ("trennen", "Heller Dachstreifen 525–546/80–95 abgetrennt als 269.", (535, 87), 101)], [U, N2, R2, A]),
 (V+269, "LAENGSBAU", False, "sauber", "Schmaler heller Dachstreifen (neu aus 56), kurz und unscharf.", [], [N2, A]),
 (V+42, "LAENGSBAU", True, "sauber", "Sehr helles, scharf begrenztes Dach am oberen rechten Kernrand mit Schatten an der Südwestseite.", [], [U, N2, R2]),
 (V+73, "FELDWEG", False, "sauber", "Heller Hinterweg vom Weg 64 zur Kreuzung bei 109, mit hellen Flecken.", [], [U, N1, R1]),
 (V+89, "NEBENGEB", False, "sauber", "Sehr heller kleiner Fleck 332–342/133–144 am Hinterweg: kleiner heller Bau oder heller Haufen.", [], [U, N1, R1]),
 (V+71, "HOF", False, "sauber", "Dunkle, beschattete Fläche am hinteren Ende des Hofs 45 am Hinterweg.", [], [U, N1, R1]),
 (V+82, "HOF", False, "sauber", "Kleine graue Fläche zwischen Hinterweg 73 und Garten 66.", [], [U, N1, R1]),
 (V+66, "GARTEN", False, "nicht_sauber", "Ummauertes Rechteck mit fleckigem Dunkelgrau, links beschattet; den hellen Bau 268 am unteren Ende abgetrennt.", [
     ("trennen", "Heller schmaler Bau 388–403/131–155 abgetrennt als 268.", (395, 143), 162)], [U, N1, R1, A]),
 (V+268, "NEBENGEB", False, "sauber", "Heller schmaler Bau am hinteren Ende des Gartens 66 (neu aus 66).", [], [N1, A]),
 (V+62, "GARTEN", False, "sauber", "Großes ummauertes Rechteck mit gleichmäßig mittelgrauem Korn zwischen 66, 37 und der Straße.", [], [U, N1, R1]),
 (V+84, "STRASSENRAND", False, "sauber", "Heller Streifen am Nordrand der Straße 30.", [], [U, N1, N2]),
 (V+86, "STRASSENRAND", False, "sauber", "Heller Streifen am Südrand der Straße 30.", [], [U, N2, R2]),
 (V+69, "STRASSENRAND", False, "sauber", "Mittelgrauer Streifen zwischen Straße 30 und Garten 62 mit dunklem Fleck (Busch) bei 477/113.", [], [U, N2, R2]),
 (V+87, "BAUM", False, "sauber", "Dunkler runder Fleck am Südrand der Straße: Baum oder Busch mit Schatten.", [], [U, N2, R2]),
 (V+30, "FAHRWEG", False, "sauber", "Helle Straßenkreuzung mit drei Ästen (nach Nordwest, Südost und zur Einmündung 109).", [], [U, N2, R2, "kontrast_1.jpg"]),
 (V+79, "STRASSENRAND", False, "sauber", "Schmaler mittelgrauer Streifen zwischen Straße und Hof 63.", [], [U, N2, R2]),
 (V+63, "HOF", False, "sauber", "Hof im Schatten zwischen Längsbau 56 und der Straße.", [], [U, N2, R2]),
 (V+32, "HOF", False, "sauber", "Kernstück eines beschatteten Hofs am rechten Kernrand, Hauptteil in r0c1.", [], [U, N2]),
 (V+81, "LAENGSBAU", False, "sauber", "Kernstück eines hellen Dachs am rechten Kernrand (547–563/122–145).", [], [U, N2, R2]),
 (V+70, "GEBAEUDE", False, "sauber", "Nur 45 Bildpunkte im Kern am rechten Kernrand; heller Teil eines Baus in r0c1.", [], [U, N2]),
 (V+94, "ANGER", False, "sauber", "Gleichmäßig graue offene Fläche zwischen Hinterweg 73 und 100, wie Anger 77.", [], [U, N1, N3]),
 (V+100, "SCHATTEN", False, "nicht_sauber", "Dunkle Fläche neben dem hellen Bau 271: Schatten oder dunkles Dach; den hellen Streifen 271 abgetrennt.", [
     ("trennen", "Heller Bau 333–347/161–186 abgetrennt als 271.", (340, 173), 175)], [U, N1, N3, A]),
 (V+271, "NEBENGEB", False, "sauber", "Heller schmaler Bau (neu aus 100).", [], [N1, A]),
 (V+110, "HOF", False, "sauber", "Kleine graue Fläche zwischen 100 und dem Hinterweg.", [], [U, N1, N3]),
 (V+109, "FAHRWEG", False, "sauber", "Helle Einmündung von Hinterweg 73 und Straße 30 in die Straße nach Süden.", [], [U, N1, N3]),
 (V+96, "WEGRAIN", False, "sauber", "Mittelgrauer Streifen am Südrand der Straße mit dunklen Flecken (Büsche).", [], [U, N2, R2]),
 (V+95, "GEBUESCH", False, "sauber", "Dunklerer Fleck am Straßenrand, Busch.", [], [U, N2, R2]),
 (V+125, "HOF", False, "sauber", "Kleine hellere Fläche zwischen 83 und dem Längsbau 127.", [], [U, N4, R4]),
 (V+83, "FELD", False, "sauber", "Große, gleichmäßig dunkelgraue Fläche zwischen den Straßen; schwache Tonstufe 480/130 bis 505/200 deutet zwei Parzellen an.", [
     ("sonstiges", "Schwache Tonstufe von etwa 480/130 nach 505/200 (rechts heller): vielleicht zwei Parzellen; keine klare Kante, nicht geteilt.", (492, 165), None)], [U, N2, R2, "kontrast_1.jpg"]),
 (V+111, "HOF", False, "nicht_sauber", "Beschatteter Hof am rechten Kernrand mit schmalem hellem Bau 534–547/183–210.", [
     ("trennen", "Schmaler heller Bau 534–547/183–210 steckt im Hof; nicht geteilt, weil der Schnitt das Segment über den Kernrand in zwei Teile zerlegt hätte.", (540, 196), 167)], [U, N2, N4, R4]),
 (V+107, "WEGRAIN", False, "sauber", "Mittelgraues Eckstück zwischen Straße 30, Feld 83 und Hof 111.", [], [U, N2, R2]),
 (V+92, "STRASSENRAND", False, "sauber", "Mittelgrauer Streifen an der Straße am rechten Kernrand.", [], [U, N2]),
 (V+112, "SCHATTEN", False, "sauber", "Fast schwarzer Fleck am rechten Kernrand.", [], [U, N2]),
 (V+104, "ANGER", False, "nicht_sauber", "Offene, fleckige Fläche zwischen Hinterweg, Straße und Feld 154; die helle Fahrspur 272 abgetrennt.", [
     ("trennen", "Helle Fahrspur 318–386/213–244 (Fortsetzung der Spur im Anger 114) abgetrennt als 272.", (350, 228), 792),
     ("sonstiges", "Dunkler kleiner Fleck 354–366/250–264 (Busch oder Schatten) und dunkle Fläche 361–396/185–224 bleiben im Segment.", (360, 257), None)], [U, N3, R3, A]),
 (V+272, "FELDWEG", False, "sauber", "Hellste, gerade Fahrspur über den Anger zur Einmündung 109 (neu aus 104); auch ein langer heller Bau wäre möglich.", [], [N3, R3, A]),
 (V+137, "BAUM", False, "sauber", "Dunkler Fleck am Westrand der Straße nach Süden.", [], [U, N3, R3]),
 (V+117, "FAHRWEG", False, "sauber", "Westliches helles Band der Straße nach Süden.", [], [U, N3, R3, "kontrast_1.jpg"]),
 (V+126, "WEGRAIN", False, "sauber", "Schmaler Streifen zwischen Straße 117 und Feld 83.", [], [U, N3]),
 (V+145, "BAUM", False, "sauber", "Fast schwarze, unregelmäßige Fläche östlich der Straße: Baumgruppe mit Schatten oder Schatten eines Baus.", [], [U, N3, N4, R4]),
 (V+141, "BAUM", False, "sauber", "Dunkle Fläche neben 145, gleiche Baumgruppe oder Schatten.", [], [U, N4, R4]),
 (V+139, "SCHATTEN", False, "sauber", "Dunkle kleine Fläche am Westende des Hofs 128.", [], [U, N4, R4]),
 (V+130, "HOF", False, "sauber", "Hellere fleckige Fläche vor dem Längsbau 127 mit zwei hellen Punkten.", [], [U, N4, R4]),
 (V+127, "LAENGSBAU", True, "sauber", "Langes helles Dach, scharf begrenzt, Schatten an der Südwestseite.", [], [U, N4, R4]),
 (V+128, "HOF", False, "nicht_sauber", "Hofstreifen zwischen den Längsbauten 127 und 142 und Hof rechts; das helle Dachstück dem Bau 142 zugeschlagen.", [
     ("trennen", "Helles Dachstück 472–518/226–254 abgetrennt und mit dem Dach 142 verschmolzen.", (495, 240), 421)], [U, N4, R4, "nah_1.jpg", A]),
 (V+148, "SCHATTEN", False, "sauber", "Fast schwarze, eckige Fläche 305–337/240–270: Schatten, dunkles Dach oder Gehölz.", [], [U, N3, R3]),
 (V+156, "NEBENGEB", False, "sauber", "Hellgraue rechteckige Fläche mit Schattenlinie 164 an der Südwestseite: Bau mit hellem Dach.", [], [U, N3, R3]),
 (V+164, "SCHATTEN", False, "sauber", "Dunkler Streifen an der Südwestseite von 156.", [], [U, N3, R3]),
 (V+151, "NEBENGEB", False, "sauber", "Heller Fleck zwischen 148 und 156, gleicher Grauton wie 156.", [
     ("verschmelzen", "Wahrscheinlich Teil des Baus 156, Grenze ohne klare Bildkante.", (341, 251), 128)], [U, N3, R3]),
 (V+155, "FELDRAIN", False, "sauber", "Schmaler Randstreifen zwischen Anger 104 und Feld 154.", [], [U, N3, R3]),
 (V+150, "WEGRAIN", False, "sauber", "Kleines Stück am Westrand der Straße nach Süden.", [], [U, N3, R3]),
 (V+161, "GEBUESCH", False, "sauber", "Dunklerer Fleck am Westrand der Straße, Busch.", [], [U, N3, R3]),
 (V+166, "BAUM", False, "sauber", "Dunkler Fleck am Westrand der Straße, Baum oder Busch.", [], [U, N3, R3]),
 (V+149, "FAHRWEG", False, "sauber", "Östliches helles Band der Straße nach Süden, reicht in v4.", [], [U, N3, R3]),
 (V+158, "BAUM", False, "sauber", "Kleine dunkle Fläche zwischen 145 und Straße.", [], [U, N3, N4]),
 (V+142, "LAENGSBAU", True, "nicht_sauber", "Großes helles Dach eines Längsbaus; um das abgetrennte Dachstück aus 128 ergänzt.", [
     ("verschmelzen", "Dachstück aus 128 (472–518/226–254) zugeschlagen, gleiche Dachfläche.", (495, 240), 421)], [U, N4, R4, "nah_1.jpg", A]),
 (V+167, "LAENGSBAU", False, "sauber", "Langes mittelgraues Dach mit hellerem Teil, Schatten an der Nordwestseite der Nachbarn.", [], [U, N4, R4]),
 (V+144, "LAENGSBAU", True, "sauber", "Langes helles Dach am rechten Kernrand.", [], [U, N4, R4]),
 (V+169, "BAUM", False, "sauber", "Fast schwarzer länglicher Fleck an der Straße: Baum mit Schatten.", [], [U, N3, R3]),
 (V+153, "HOF", False, "nicht_sauber", "Hof mit dunklem Fleck am rechten unteren Rand; das helle Dachstück 274 abgetrennt.", [
     ("trennen", "Helles Dachstück 532–555/289–313 abgetrennt als 274.", (543, 300), 255)], [U, N4, R4, A]),
 (V+274, "LAENGSBAU", False, "sauber", "Helles Dachstück (neu aus 153).", [], [N4, A]),
]

EINGRIFFE = [
 {"schritt": "teilen", "vorher": [V+45], "nachher": [V+45, V+264], "grund": "Heller Längsbau 312–332/75–105 steckte im Schattenhof 45; Splitter beim Schnitt wieder dem Bau zugeschlagen."},
 {"schritt": "teilen", "vorher": [V+37], "nachher": [V+37, V+265], "grund": "Heller Längsbau 395–428/78–114 steckte im Hof 37; Splitter wieder dem Bau zugeschlagen."},
 {"schritt": "teilen", "vorher": [V+28], "nachher": [V+28, V+266], "grund": "Helles Dachstück im Kern 418–432/65–80 steckte im Schattenhof 28."},
 {"schritt": "teilen", "vorher": [V+66], "nachher": [V+66, V+268], "grund": "Heller Bau 388–403/131–155 steckte im Garten 66; Splitter wieder dem Bau zugeschlagen."},
 {"schritt": "teilen", "vorher": [V+56], "nachher": [V+56, V+269], "grund": "Heller Dachstreifen 525–546/80–95 steckte im Schattenhof 56."},
 {"schritt": "teilen", "vorher": [V+100], "nachher": [V+100, V+271], "grund": "Heller Bau 333–347/161–186 steckte in der dunklen Fläche 100."},
 {"schritt": "teilen", "vorher": [V+104], "nachher": [V+104, V+272], "grund": "Helle Fahrspur 318–386/213–244 steckte im Anger 104."},
 {"schritt": "teilen", "vorher": [V+128], "nachher": [V+128, V+142], "grund": "Helles Dachstück 472–518/226–254 im Hof 128 abgetrennt und mit dem Dach 142 verschmolzen (gleiche Dachfläche)."},
 {"schritt": "teilen", "vorher": [V+153], "nachher": [V+153, V+274], "grund": "Helles Dachstück 532–555/289–313 steckte im Hof 153."},
]
NAHT = []
UNSICHER = [
 "100143 (v4): große Fläche südlich der Längsbauten 142/167; Hof oder Straße, in v4 zu urteilen.",
 "100154 (v3/v4): Feld; Randstreifen 155/164 grenzen ohne klare Bildkante.",
 "100077, 100115 (v1): Anger und heller Bau neben dem Anger 104.",
]
NICHT_GEPRUEFT = [
 "Naht zu r0c1 (rechter Kernrand x 563): Segmente auf der anderen Seite nicht angesehen; 32, 70, 81, 92, 111, 112, 128, 144, 153 reichen dorthin.",
]
OFFEN = [
 "Feld 83 und Gärten 12/50/53/62/66: Acker, Grünland oder Gemüsegarten im Schwarz-Weiß-Bild nicht zu trennen; im Farbbild Grün gegen Braun und Reihen.",
 "Straßen 30, 109, 117, 149 und Ränder 60/69/79/84/86/92: Belag nicht bestimmbar; im Farbbild Asphalt (dunkelgrau) gegen Schotter/Erde.",
 "272: helle gerade Spur in Verlängerung der Fahrspur des Angers 114, darum als Weg geurteilt; ein langer heller Bau wäre auch möglich (im Farbbild Dachfarbe).",
 "100, 148, 145, 141: dunkle Flächen, Schatten, dunkles Dach oder Gehölz; im Farbbild Grün (Gehölz) gegen Dachfarbe.",
 "111: schmaler heller Bau 534–547/183–210 im Hof nicht abgetrennt (Schnitt hätte das Segment über den Kernrand zerlegt).",
 "83: schwache Tonstufe deutet zwei Parzellen an; im Farbbild prüfen.",
 "Höfe im Schatten (41, 45, 28, 37, 56, 63, 71): Untergrund unter dem Schlagschatten nicht sichtbar.",
]
