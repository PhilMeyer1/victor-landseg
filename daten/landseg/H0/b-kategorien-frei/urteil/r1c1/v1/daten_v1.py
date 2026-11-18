"""Urteil v1 (r1c1, Fassung B) schreiben."""
import sys

sys.path.insert(0, "C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c1/v1")
import urteil_bau as ub  # noqa: E402

O = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c1/v1"
V = ub.VB + "/v1"
U, UR = V + "/uebersicht_nummern.jpg", V + "/uebersicht_roh.jpg"
N1, N1R, N2, N2R = V + "/nah1_nummern.jpg", V + "/nah1_roh.jpg", V + "/nah2_nummern.jpg", V + "/nah2_roh.jpg"
N3, N3R, N4, N4R = V + "/nah3_nummern.jpg", V + "/nah3_roh.jpg", V + "/nah4_nummern.jpg", V + "/nah4_roh.jpg"
E1, E2, E3, E4, E5, E6, K1 = (O + "/nah_1.jpg", O + "/nah_2.jpg", O + "/nah_3.jpg", O + "/nah_4.jpg",
                              O + "/nah_5.jpg", O + "/nah_6.jpg", O + "/kontrast_1.jpg")
HS = "Streifen eines Streckhofs aus dem Nachsegmentieren von 400006: Dach und Hof zwischen zwei dunklen Schattenlinien, bei 0,45 m nicht sicher trennbar"

E = [
 (400037, "0.2", "SCH", False, "sauber", "Dunkle Fläche an der Ecke Landstraße/Dorfstraße, fast ganz im Kontextrand; Schatten oder Baumkrone.", [], [U, E6]),
 (400064, "1.2.2", "STR_LAND", True, "nicht_sauber", "Die breite, sehr helle Landstraße nach Südwesten (nur 66 px im Kern).", [("klasse", "Vorstufe 1.2.2 Weg; es ist die breite Landstraße (66/77).", None)], [U, E6]),
 (400072, "2.1", "RAIN", False, "sauber", "Dunklerer Saum am oberen Rand des Feldes 400078 unter der Landstraße.", [], [U, N1R, E6]),
 (400075, "3.1", "BAUM", False, "nicht_sauber", "Kompakter dunkler Fleck am Feldrand: Baum- oder Gebüschkrone mit Schatten.", [("klasse", "Vorstufe Wiese; dunkle runde Krone, eher Gehölz (89/97).", None)], [U, N1R, E6]),
 (400039, "1.3.2", "SIED", False, "sauber", "Mittelgraue Fläche am Nordrand, fast ganz im Kontextrand (34 px Kern); Dach oder Hof nicht erkennbar.", [], [U, E6]),
 (400056, "1.1.1", "NEBEN", False, "sauber", "Kleine sehr helle ovale Fläche an der Straßengabel (etwa 4 × 6 m): kleines Gebäude oder helle Fläche.", [], [U, N1R, E6]),
 (400046, "1.2.1", "PLATZ", False, "sauber", "Etwas dunklere Fläche in der Straßengabel neben dem dunklen Bereich 400054; Teil der Verkehrsfläche oder Grasinsel.", [], [U, N1R, E6]),
 (400054, "0.2", "SCH", False, "sauber", "Große dunkle, kantige Fläche zwischen hellem Dach 400048 und Straße: Schatten oder dunkles Dach.", [], [U, N1R, E6]),
 (400047, "1.1.1", "SIED", False, "sauber", "Graue Fläche am Nordrand links vom hellen Dach 400048, fast ganz im Kontextrand.", [], [U, E6]),
 (400048, "1.1.2", "GEB_HELL", True, "sauber", "Helles rechteckiges Dach am Nordrand (nur 67 px im Kern).", [], [U, E6, E3]),
 (400073, "1.2.1", "WEG_ZUF", False, "sauber", "Heller Streifen, der von der Straßengabel nach Nordosten in die Höfe führt: Zufahrt oder Gasse.", [], [U, E6, E3]),
 (400066, "1.1.1", "GEB_DUNKEL", True, "sauber", "Dunkelgraues Rechteck mit scharfen Kanten und Schattenstreifen: Gebäude mit dunklem Dach.", [], [U, N2R, E3]),
 (400063, "1.3.2", "HOF", False, "nicht_sauber", "Nach dem Abtrennen des Schattens 400270 der helle Streifen (Durchgang/Hof) am Ostrand der Häuserzeile.", [("klasse", "Vorstufe Baustelle; heller Durchgang im Hof (285/88), Schatten abgetrennt.", None)], [U, E1]),
 (400035, "0.2", "SCH_GEB", True, "sauber", "Nördliche Fortsetzung des dunklen Schattenbands 400060 an der Häuserzeile.", [], [U, E1]),
 (400009, "6.6", "STR_DORF", False, "sauber", "Helle Straße am Nordrand (nur 11 px im Kern), Fortsetzung der östlichen Dorfstraße.", [], [U, E1]),
 (400085, "3.1", "BAUM", False, "nicht_sauber", "Dunkler Fleck am Rand von Feld 400078 zur Dorfstraße: Baum oder Gebüsch.", [("klasse", "Vorstufe Wiese; dunkle Krone (100/118).", None)], [U, N1R, E6]),
 (400089, "2.1", "BAUM", False, "nicht_sauber", "Fleckige dunkelgraue Fläche unter 400085 am Feldrand: Gebüsch mit Saum.", [("klasse", "Vorstufe Acker; dunkle Flecken am Rand, eher Gebüsch (114/127).", None)], [U, N1R, E6]),
 (400003, "6.6", "STR_DORF", True, "nicht_sauber", "Die helle Dorfstraße mit der Gabel zur Landstraße.", [("klasse", "Vorstufe Feldweg unbefestigt; breite Dorfstraße (125/110).", None)], [U, N1, N1R, E6]),
 (400069, "1.3.2", "GARTEN", False, "nicht_sauber", "Fleckige Fläche zwischen Dorfstraße und Gebäude 400094 mit dunklen Kronen: Hof oder Garten.", [("klasse", "Vorstufe Baustelle; fleckige Hof-/Gartenfläche mit Bäumen (145/105).", None)], [U, N1R, E6]),
 (400094, "1.1.2", "GEB_MITTEL", False, "sauber", "Mittelgraue rechteckige Fläche mit Schatten 400096 an der Ostseite: Gebäude.", [], [U, N1, N1R, E6]),
 (400060, "0.2", "SCH_GEB", True, "sauber", "Langes dunkles Band an der Ostseite der Häuserzeile zur östlichen Dorfstraße: Schlagschatten.", [], [U, N2R, E1, E4]),
 (400078, "2.2", "ACKER", False, "sauber", "Große mittelgraue Feldfläche mit schwachen Längsstreifen westlich der Dorfstraße.", [], [U, UR, N1R, N3R]),
 (400101, "3.1", "BAUM", False, "nicht_sauber", "Dunkle Flecken am Straßenrand der Dorfstraße zum Feld: Gebüsch.", [("klasse", "Vorstufe Wiese; dunkle Gebüschflecken (126/150).", None)], [U, N1R, E6]),
 (400112, "1.2.1", "STR_DORF", True, "sauber", "Kleines Stück Fahrbahn an der Einmündung des breiten Wegs 400110 in die Dorfstraße.", [], [U, N1, N3]),
 (400102, "1.1.2", "GEB_HELL", False, "sauber", "Helles Rechteck mit kleinen dunklen Flecken, Schatten 400096 an der Ostseite: Gebäude mit hellem Dach (heller gepflasterter Hof möglich).", [], [U, N1, N1R, E4]),
 (400109, "1.1.1", "GEB_MITTEL", False, "sauber", "Hellgraues Rechteck südlich von 400102, Schatten an der Ostseite: Gebäude.", [], [U, N1, N4R, E4]),
 (400096, "0.2", "SCH_GEB", True, "sauber", "Dunkles Band an der Ostseite der Gebäude 400094/400102/400109: Schlagschatten.", [], [U, N1, N4R, E4]),
 (400105, "1.3.2", "HOF", False, "nicht_sauber", "Unregelmäßige graue Fläche am Ostende der Häuserzeile vor dem Schattenband: Hof- oder Vorgartenfläche.", [("klasse", "Vorstufe Baustelle; Hof/Vorgarten (303/163).", None)], [U, N2R, E4]),
 (400111, "1.3.2", "SCH", False, "sauber", "Kleines dunkelgraues Stück am Rand des Schattenbands an der Viertelgrenze.", [], [U, N2, E4]),
 (400110, "1.2.2", "WEG_BREIT", False, "sauber", "Breites helles fleckiges Band nach Südwesten zwischen den Feldern: Weg, Belag nicht erkennbar.", [], [U, UR, N3, N3R]),
 (400116, "2.1", "RAIN", False, "nicht_sauber", "Graue Kante zwischen dem breiten Weg 400110 und dem Feld: Wegrand.", [("klasse", "Vorstufe Acker; Wegrand (132/211).", None)], [U, N3, N3R]),
 (400115, "1.3.2", "BAUM", False, "nicht_sauber", "Dunkle fleckige Fläche an der Einmündung des breiten Wegs: Gebüsch mit Schatten.", [("klasse", "Vorstufe Baustelle; Gebüsch (149/205).", None)], [U, N3, N3R]),
 (400119, "3.1", "ACKER", False, "nicht_sauber", "Mittelgraue Ecke des Feldes 400118 zwischen Gebüschen; kein eigenes Objekt.", [("verschmelzen", "Gehört zum Feld 400118 (Nachbarviertel v3), keine Bildkante dazwischen (149/219).", 139)], [U, N3, N3R]),
 (400125, "3.1", "RAIN", False, "sauber", "Graue Fläche am Feldrand zwischen Gebüschen an der Dorfstraße.", [], [U, N3, N3R]),
 (400120, "0.2", "BAUM", False, "nicht_sauber", "Dunkle runde Krone am Feldrand.", [("klasse", "Vorstufe Schatten; runde Krone mit Schatten (157/225).", None)], [U, N3, N3R]),
 (400117, "1.2.1", "STR_RAND", False, "sauber", "Hellgrauer Saum zwischen Gebüsch 400115 und der Dorfstraße.", [], [U, N3, N3R]),
 (400128, "1.2.1", "BAUM", False, "nicht_sauber", "Dunkler Fleck am Westrand der Dorfstraße: Gebüsch.", [("klasse", "Vorstufe Straße; dunkler Gebüschfleck (173/249).", None)], [U, N3, N3R]),
 (400122, "1.3.2", "VORPLATZ", False, "nicht_sauber", "Hellgraue Fläche zwischen Dorfstraße und Häuserzeile: Vorplatz.", [("klasse", "Vorstufe Baustelle; Vorplatz an der Straße (193/234).", None)], [U, N4, N4R]),
 (400127, "1.2.1", "VORPLATZ", False, "sauber", "Hellgraue Fläche vor der Häuserzeile, wie 400122.", [], [U, N4, N4R, E2]),
 (400129, "1.3.2", "VORPLATZ", False, "nicht_sauber", "Kleine graue Fläche vor der Häuserzeile neben dem Schatten 400131.", [("klasse", "Vorstufe Baustelle; Vorplatz (213/245).", None)], [U, N4, E2]),
 (400006, "1.1.1", "HOFST", False, "nicht_sauber", "Nach dem Nachsegmentieren nur noch 4 px im Kern; der Rest liegt im Kontextrand (Häuserzeile in r0c1).", [("trennen", "Der ganze Häuserblock zwischen den Dorfstraßen war ein Segment; in 30 Teile geteilt (265/219).", 50140)], [U, N2, E4, E5, K1]),
 (400136, "2.1", "RAIN", False, "sauber", "Graue Kante am Südrand des breiten Wegs 400110, fast ganz im Kontextrand.", [], [U, N3]),
 (400137, "6.6", "SCH", False, "nicht_sauber", "Kurzer dunkler Strich am Südrand des Wegs: Schatten, Graben oder Fahrzeug.", [("klasse", "Vorstufe Feldweg; dunkler Strich (66/269).", None)], [U, N3, N3R]),
 (400140, "3.1", "BAUM", False, "nicht_sauber", "Dunkelgrauer Fleck am Feldrand an der Dorfstraße: Gebüsch oder Rain.", [("klasse", "Vorstufe Wiese; Gebüsch oder Saum (173/291).", None)], [U, N3, N3R]),
 (400133, "4.2.4", "BAUM", False, "sauber", "Dunkler Fleck am Westrand der Dorfstraße: Gebüsch.", [], [U, N3, N3R]),
 (400126, "0.2", "HECKE", False, "nicht_sauber", "Reihe dunkler Flecken am Westrand der Dorfstraße: Gebüsch-/Baumreihe mit Schatten.", [("klasse", "Vorstufe Schatten; Gehölzreihe (179/276).", None)], [U, N3, N3R]),
 (400142, "4.2.4", "BAUM", False, "sauber", "Dunkler Fleck am Feldrand an der Dorfstraße: Gebüsch.", [], [U, N3, N3R]),
 (400121, "6.6", "STR_DORF", True, "nicht_sauber", "Die helle Dorfstraße südlich der Gabel.", [("klasse", "Vorstufe Feldweg; Dorfstraße (188/255).", None)], [U, N3, N4, N4R]),
 (400143, "1.2.1", "STR_RAND", False, "sauber", "Kleines graues Stück am Westrand der Dorfstraße.", [], [U, N4, E2]),
 (400132, "1.1.2", "VORPLATZ", False, "nicht_sauber", "Nach dem Abtrennen des hellen Dachs 400273 die graue Fläche um das Dach (Straßenrand und Hof).", [("klasse", "Vorstufe Nebengebäude; nach Abtrennen des Dachs Vorplatz/Hof (225/280).", None)], [U, N4, N4R, E2]),
 (400131, "1.3.2", "SCH_GEB", True, "nicht_sauber", "Kleine sehr dunkle Fläche neben dem Vorplatz: Schlagschatten.", [("klasse", "Vorstufe Baustelle; Schatten (219/253).", None)], [U, N4, E2]),
 (400146, "1.2.1", "STR_DORF", False, "sauber", "Stück der Dorfstraße südlich des hellen Dachs, mit hellem Rand.", [], [U, N4, E2]),
]

NEU = {
 400234: ("HOFST", "Südöstlichster Streifen des Blocks an der Quergasse"),
 400236: ("HOFST", "Streifen nördlich von 400234"),
 400239: ("HOFST", "Dunklerer Streifen mit Schattenlinie"),
 400242: ("HOFST", "Streifen zwischen zwei langen Schattenlinien"),
 400244: ("HOFST", "Streifen mit hellem Dachabschnitt"),
 400245: ("HOFST", "Streifen in der Blockmitte am Westrand"),
 400246: ("HOFST", "Ostende eines Streifens am Schattenband"),
 400247: ("HOFST", "Streifen in der Blockmitte"),
 400248: ("HOFST", "Streifen mit hellem Dach im Norden des Blocks"),
 400249: ("VORPLATZ", "Hellgraue Fläche südlich von Gebäude 400109 an der Dorfstraße: Vorplatz"),
 400250: ("HOFST", "Streifen im Nordteil des Blocks"),
 400251: ("HOFST", "Streifen unter dem sehr hellen Dach"),
 400252: ("HOFST", "Streifen mit dem sehr hellen Dach (240/150) und dunklerem Westteil"),
 400253: ("HOFST", "Nördlicher Streifen mit hellem Dach"),
 400254: ("HOFST", "Streifen mit hellem Dach südlich der Blockmitte"),
 400255: ("HOFST", "Streifen am Ostrand"),
 400256: ("HOFST", "Ostende eines Streifens"),
 400257: ("BAUMGR", "Große dunkle Fläche am Westrand des Blocks an der Dorfstraße: Baumgruppe/Obstgarten oder Schatten"),
 400258: ("HOFST", "Kleiner Streifen mit hellen und dunklen Teilen am Westrand"),
 400259: ("HOFST", "Ostteil eines Streifens am Schattenband"),
 400260: ("HOFST", "Ostende mit dunklen Teilen am Schattenband"),
 400261: ("HOFST", "Westteil eines Streifens"),
 400262: ("HOFST", "Ostteil eines Streifens, dunkel"),
 400263: ("HOFST", "Ostteil eines Streifens, dunkel"),
 400264: ("HOFST", "Westteil eines Streifens mit hellen Flecken"),
 400265: ("HOFST", "Streifen im Südostteil"),
 400266: ("HOFST", "Streifen an der Quergasse"),
 400267: ("HOFST", "Nordöstliche Ecke am Kernrand mit hellem Dach"),
 400268: ("HOFST", "Graue Fläche am Nordrand südlich des hellen Dachs 400048"),
 400269: ("HOFST", "Fläche um das dunkle Dach 400066 im Norden"),
}
for sid, (key, txt) in NEU.items():
    if key == "HOFST":
        E.append((sid, "1.1.1", key, False, "sauber", f"{txt}. {HS}.", [], [U, E4, E5, K1]))
    else:
        E.append((sid, "1.1.1", key, False, "sauber", txt + ".", [], [U, E4, E5]))
E.append((400270, "1.1.1", "SCH_GEB", True, "sauber", "Aus 400063 abgetrennter dunkler Teil: Schatten am Ostende der Häuserzeile.", [], [U, E1]))
E.append((400273, "1.1.1", "GEB_HELL", True, "sauber", "Aus 400132 abgetrenntes sehr helles Rechteck mit scharfen Kanten (etwa 4 × 13 m): Gebäude mit hellem Dach.", [], [U, N4R, E2]))

QUELLE = {}
for i in range(23, 28):
    QUELLE[i] = 400244
for i in range(28, 31):
    QUELLE[i] = 400247
for i in range(31, 34):
    QUELLE[i] = 400245
for i in range(34, 36):
    QUELLE[i] = 400242
for i in range(36, 38):
    QUELLE[i] = 400006
QUELLE[38], QUELLE[39] = 400063, 400132
zaehler = {"n": 0}


def gruende(art, s, e):
    zaehler["n"] += 1 if art == "grund" else 0
    nr = zaehler["n"]
    if art == "quelle":
        return [QUELLE[nr + 1]]
    if s["op"] == "teilen":
        return "Häuserblock 400006 entlang einer dunklen Schattenlinie zwischen zwei Streckhof-Zeilen geteilt (Weg über die dunkelsten Bildpunkte)."
    if s["op"] == "verschmelzen":
        return "Splitter unter 80 px aus dem vorigen Schnitt an das Nachbarstück derselben Herkunft gegeben (L1, nichts weglassen)."
    if nr == 38:
        return "Dunkler Schattenteil (Grauwert unter 85) von 400063 abgetrennt, der helle Durchgang bleibt."
    if nr == 39:
        return "Sehr helles Dach (Grauwert über 205) aus 400132 abgetrennt; die graue Fläche darum bleibt."
    return "Großes Stück des Häuserblocks per Wasserscheide auf den dunklen Linien weiter in Streifen zerlegt (Polygon = genau die Teilfläche)."


ein = ub.eingriffe_aus_ergebnis(O + "/eingriffe.json", O + "/eingriffe_ergebnis.txt", gruende)

uebersicht = [ub.H0 + "/H0.png", ub.H0 + "/ganz/H0_raster.jpg", ub.H0 + "/ganz/r1c1/ganz_nummern.jpg",
              ub.H0 + "/ganz/r1c1/ganz_roh.jpg", U, UR]
nah = [N1, N1R, N2, N2R, N3, N3R, N4, N4R, E1, E2, E3, E4, E5, E6, K1]
naht = [
 {"id": 400006, "seite": "oben", "text": "400006 trägt nach dem Teilen nur noch den Kontextteil (Häuserzeile in r0c1) und 4 px im Kern; die Kernstücke 400267, 400268 (und 400269) haben neue IDs. Ihre Grenze zum Kontextteil von 400006 bei y=64 ist eine Gerade ohne sichere Bildkante: beim Zusammentragen mit r0c1 prüfen, ob sie mit 400006 zusammengehören."},
 {"id": 400267, "seite": "oben", "text": "Grenze bei y=64 zu 400006 (Kontext) ist eine Gerade aus dem Nachsegmentieren, keine Bildkante."},
 {"id": 400268, "seite": "oben", "text": "Grenze bei y=64 zu 400006 (Kontext) ist eine Gerade aus dem Nachsegmentieren, keine Bildkante."},
]
unsicher = [
 "400118 (v3): die Feldecke 400119 gehört ohne Bildkante zu diesem Feld; im Verbund dieselbe Klasse Acker geben.",
 "400163 (v3): dunkle Fläche neben 400257 am Westrand des Blocks; Schatten oder Baumgruppe wie 400257, gemeinsam klären.",
 "400171 (v3) und 400192 (v4) grenzen an die Streifen 400266/400234: Quergasse und Hofteile dort im Verbund prüfen.",
]
nicht_geprueft = [
 "uebersicht_vorschlag.jpg, uebersicht_maengel.jpg, uebersicht_kontrast.jpg und uebersicht_gitter.jpg nicht eigens angesehen; dafür eigene Kontrast-, Grat- und Gitteransichten.",
 "Die Streifen aus 400006 südlich y=314 (v3/v4-Gebiet) nur in nah_5.jpg und den Arbeitsansichten beurteilt, nicht in den vorbereiteten Viertelbildern von v3/v4.",
]
offen = [
 "Alle Hofstellen-Streifen aus 400006 (28 Stücke): Dach gegen Hof ist im Schwarz-Weiß-Scan bei 0,45 m nicht sicher zu trennen; im Farbbild würden Dachfarbe (Ziegel rot) gegen Hof (grau/grün) die Teilung in Gebäude und Hof erlauben.",
 "Einzelne Streifengrenzen aus der Wasserscheide (Teilflächen von 400244, 400247, 400245, 400242, 400006) liegen auf schwachen dunklen Linien; wo die Linie fehlt, ist die Grenze geschätzt.",
 "400054: Schatten oder dunkles Dach; Schattenrichtung (nach Osten, siehe 400096) spricht gegen einen Schatten des Dachs 400048. Farbbild oder Stereo würde entscheiden.",
 "400257: dunkle Fläche am Westrand des Blocks; Baumgruppe (Obstgarten) oder Schatten. Farbbild (grün) würde entscheiden.",
 "400078 und andere Feldflächen: Acker nach den Längsstreifen vermutet; Acker gegen Grünland nur im Farbbild sicher.",
 "400102: helles Dach oder heller Hof; der Schatten 400096 an der Ostseite spricht für ein Gebäude.",
 "400110: Belag des breiten Wegs (Schotter, Erde, Asphalt) nicht erkennbar.",
]
ub.schreiben("v1", O, (64, 64, 314, 314), E, ein, uebersicht, nah, naht, unsicher, nicht_geprueft, offen)
