"""Urteil v2 (r1c1, Fassung B) schreiben."""
import sys

sys.path.insert(0, "C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c1/v1")
import urteil_bau as ub  # noqa: E402

O = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c1/v2"
V = ub.VB + "/v2"
U, UR = V + "/uebersicht_nummern.jpg", V + "/uebersicht_roh.jpg"
N2, N2R = V + "/nah2_nummern.jpg", V + "/nah2_roh.jpg"
E1, E2, E3, K1 = O + "/nah_1.jpg", O + "/nah_2.jpg", O + "/nah_3.jpg", O + "/kontrast_1.jpg"
HS = "Streifen eines Streckhofs aus dem Nachsegmentieren von 400092: Dach und Hof zwischen dunklen Schattenlinien, bei 0,45 m nicht sicher trennbar"

E = [
 (400051, "1.2.1", "STR_DORF", False, "sauber", "Heller Streifen der östlichen Dorfstraße am Nordrand zwischen zwei Schattenbändern, mit Randanteilen.", [], [U, UR, E2]),
 (400053, "0.2", "SCH_GEB", True, "sauber", "Sehr dunkle Fläche neben einem hellen Dachstreifen: Schlagschatten.", [], [U, E2]),
 (400049, "1.1.1", "GEB_HELL", False, "sauber", "Heller schmaler Dachstreifen zwischen zwei Schatten am Nordrand (80 px im Kern).", [], [U, E2]),
 (400045, "0.2", "SCH_GEB", True, "sauber", "Langes dunkles Band an der Ostseite eines Dachstreifens: Schlagschatten.", [], [U, E2]),
 (400011, "1.2.1", "STR_DORF", True, "sauber", "Helle Straße am Nordrand, Fortsetzung der Dorfstraße zur Straßengabel.", [], [U, UR, E2]),
 (400050, "1.1.1", "SIED", False, "sauber", "Kleine graue Fläche am Nordrand (22 px im Kern), Dach oder Hof.", [], [U, E2]),
 (400042, "1.1.2", "SIED", False, "nicht_sauber", "Graue Fläche am Nordrand mit dunkler Schräglinie: Dach und Hof gemischt.", [("trennen", "Dachfläche und Hof stecken zusammen; Kante unscharf, nicht geteilt (439/73).", None)], [U, N2, N2R]),
 (400071, "1.2.1", "STR_DORF", False, "sauber", "Helle Aufweitung an der Einmündung in die Bogenstraße.", [], [U, N2, N2R]),
 (400041, "1.1.2", "GEB_HELL", False, "sauber", "Helles Dach am Nordrand, fast ganz im Kontextrand.", [], [U, N2]),
 (400055, "1.3.2", "BAUM", False, "nicht_sauber", "Dunkle fleckige Fläche am Nordrand der Bogenstraße: Gebüsch/Bäume mit Schatten.", [("klasse", "Vorstufe Baustelle; dunkle Kronen (494/73).", None)], [U, N2, N2R]),
 (400070, "1.2.2", "STR_DORF", True, "nicht_sauber", "Helle, im Bogen geführte Straße zwischen den Höfen.", [("klasse", "Vorstufe Weg befestigt; breite Dorfstraße im Bogen (529/95).", None)], [U, N2, N2R]),
 (400029, "1.2.1", "STR_DORF", False, "sauber", "Hellgraue Fläche am Nordostrand, Fortsetzung der Bogenstraße, meist im Kontextrand.", [], [U, N2]),
 (400076, "1.3.2", "SCH", False, "nicht_sauber", "Kleiner dunkler Fleck am Rand der Bogenstraße: Schatten oder Gebüsch.", [("klasse", "Vorstufe Baustelle; dunkler Fleck (551/99).", None)], [U, N2]),
 (400062, "0.2", "BAUM", False, "nicht_sauber", "Dunkle körnige Fläche am Straßenrand rechts: Baum/Gebüsch.", [("klasse", "Vorstufe Schatten; körnige Krone (557/86).", None)], [U, N2, N2R]),
 (400057, "1.3.2", "BAUM", False, "sauber", "Dunkle Fläche am Ostrand, fast ganz im Kontextrand (54 px im Kern): Gehölz.", [], [U, N2]),
 (400088, "1.2.1", "STR_DORF", False, "sauber", "Heller Westrand der östlichen Dorfstraße mit etwas Vorplatz.", [], [U, E2]),
 (400099, "1.2.1", "STR_DORF", True, "sauber", "Helles Stück der östlichen Dorfstraße.", [], [U, E2]),
 (400061, "1.1.1", "SCH_GEB", True, "nicht_sauber", "Langes sehr dunkles Band zwischen zwei Dachstreifen: Schlagschatten.", [("klasse", "Vorstufe Hauptgebäude; Schatten (349/104).", None)], [U, E2]),
 (400087, "0.2", "SCH_GEB", True, "sauber", "Dunkle Fläche östlich eines Dachstreifens: Schlagschatten.", [], [U, E2]),
 (400033, "1.3.2", "GEB_MITTEL", False, "nicht_sauber", "Nach dem Teilen der lange helle Dachstreifen zwischen den Schatten 400061 und 400045.", [("trennen", "Mehrere Dachstreifen und Hofteile waren ein Segment; in 4 Teile geteilt (379/109).", 2314)], [U, E2]),
 (400067, "1.1.1", "HOF", False, "nicht_sauber", "Fleckige Hoffläche mit Schattenanteil zwischen den Gebäuden.", [("klasse", "Vorstufe Hauptgebäude; Hof mit Schatten (396/125).", None)], [U, E2]),
 (400079, "1.1.2", "GEB_MITTEL", False, "sauber", "Hellgraues Rechteck mit klaren Kanten: Gebäude oder befestigter Hof.", [], [U, E2]),
 (400097, "1.2.1", "HOF", False, "nicht_sauber", "Kleine helle Fläche zwischen den Höfen: Durchgang/Hof.", [("klasse", "Vorstufe Straße; heller Hofdurchgang (410/136).", None)], [U, E2]),
 (400084, "1.1.1", "SCH", False, "nicht_sauber", "Dunkler Fleck an der Hofecke: Schatten.", [("klasse", "Vorstufe Hauptgebäude; dunkler Fleck (420/117).", None)], [U, E2]),
 (400077, "0.2", "SCH_GEB", True, "sauber", "Sehr dunkle Fläche an der Ostseite eines Gebäudes: Schlagschatten.", [], [U, N2, E2]),
 (400081, "1.3.2", "STR_RAND", False, "nicht_sauber", "Graue Fläche am Innenrand der Bogenstraße mit Schatten.", [("klasse", "Vorstufe Baustelle; Straßenrand (449/113).", None)], [U, N2, N2R]),
 (400083, "1.2.1", "GEB", False, "nicht_sauber", "Heller länglicher Streifen zwischen Bogenstraße und dunkler Fläche 400082: Dach eines schmalen Gebäudes oder Weg.", [("klasse", "Vorstufe Straße; eher schmales Gebäude (471/115).", None)], [U, N2, N2R]),
 (400091, "1.1.1", "GEB", False, "sauber", "Hellgraues Rechteck an 400083: Gebäude.", [], [U, N2, N2R]),
 (400082, "1.3.2", "SCH", False, "nicht_sauber", "Große dunkle Fläche östlich von 400083/400091 mit hellerem Einschluss: Schatten über Garten.", [("klasse", "Vorstufe Baustelle; Schatten und Garten (503/119).", None)], [U, N2, N2R, E1]),
 (400080, "1.2.1", "SCH", False, "nicht_sauber", "Dunkler Saum am Innenrand der Bogenstraße: Schatten.", [("klasse", "Vorstufe Straße; dunkler Saum (512/104).", None)], [U, N2, N2R]),
 (400086, "0.2", "SCH_GEB", True, "sauber", "Dunkles Band an der Nordostseite des Hofkomplexes 400093: Schlagschatten.", [], [U, N2, E1]),
 (400108, "1.2.1", "VORPLATZ", False, "sauber", "Kleine helle Fläche am Straßenrand.", [], [U, E2]),
 (400098, "1.1.2", "GEB_MITTEL", False, "sauber", "Mittelgraues Rechteck an der Dorfstraße mit Schatten an der Ostseite: Gebäude.", [], [U, E2]),
 (400093, "1.1.1", "GEB_HELL", False, "nicht_sauber", "Nach Abtrennen des Innenhofs 400288 der Ring heller Gebäudeflügel des Hofkomplexes mit Außensaum.", [("trennen", "Innenhof war mit den Flügeln ein Segment; Innenhof abgetrennt (518/148).", 493)], [U, N2, N2R, E1]),
 (400104, "1.1.1", "SIED", False, "sauber", "Große dunkelgraue gleichmäßige Fläche am Ostrand: großes Dach oder Garten, meist im Kontextrand.", [], [U, UR]),
 (400107, "1.3.2", "SCH_GEB", True, "nicht_sauber", "Kleine sehr dunkle Fläche südöstlich des Hofkomplexes: Schatten.", [("klasse", "Vorstufe Baustelle; Schatten (554/171).", None)], [U, N2, E1]),
 (400113, "1.2.1", "STR_RAND", False, "sauber", "Graues Stück am Ostrand der Dorfstraße.", [], [U, E3]),
 (400114, "0.2", "SCH", False, "sauber", "Dunkler Fleck am Ostrand der Dorfstraße: Schatten oder Baum.", [], [U, E3]),
 (400123, "1.2.1", "SCH", False, "nicht_sauber", "Dunkles kleines Stück am Straßenrand.", [("klasse", "Vorstufe Straße; dunkel (379/234).", None)], [U, E3]),
 (400092, "1.1.1", "SIED", False, "nicht_sauber", "Nach dem Teilen die große gleichmäßig hellgraue Fläche im Ostteil des Blocks: großes Dach oder Hof/Garten.", [("trennen", "Ganzer Häuserblock war ein Segment; in 11 Teile geteilt (452/229).", 13586)], [U, E3, K1]),
 (400090, "0.2", "SCH_GEB", True, "sauber", "Langes dunkles Band an der Nordostseite des Blocks: Schlagschatten.", [], [U, N2, E3]),
 (400106, "1.1.1", "SIED", False, "sauber", "Graue Fläche am Ostrand, fast ganz im Kontextrand (64 px).", [], [U]),
 (400141, "1.3.2", "SCH_GEB", True, "nicht_sauber", "Sehr dunkle Fläche am Westrand der Dorfstraße: Schatten.", [("klasse", "Vorstufe Baustelle; Schatten (373/292).", None)], [U, E3]),
 (400135, "1.2.1", "VORPLATZ", False, "sauber", "Helle Aufweitung am Ostrand der Dorfstraße vor dem Block.", [], [U, E3]),
 (400130, "1.1.1", "GEB_MITTEL", False, "sauber", "Langes gleichmäßig mittelgraues Band (etwa 55 × 9 m): langes Dach (Stall/Scheune oder Häuserzeile).", [], [U, UR, E3]),
 (400134, "1.1.1", "SIED", False, "sauber", "Kleine graue Fläche am Ostrand des Blocks.", [], [U, E3]),
 (400124, "1.3.2", "SIED", False, "nicht_sauber", "Fleckige graue Fläche am Ostrand, großteils im Kontextrand: Höfe und Dächer gemischt.", [("trennen", "Mischfläche aus Dächern und Höfen, Kanten im Kern unscharf; nicht geteilt (552/280).", None)], [U, UR, E3]),
]
NEU = {
 400274: "Streifen mit hellem Gebäude im Nordwesten des Blocks",
 400275: "Streifen im Norden des Blocks",
 400276: "Streifen an der Dorfstraße",
 400277: "Streifen mit hellem Dachteil",
 400278: "Dunkler Streifen mit Schatten an der Dorfstraße",
 400279: "Kleiner Streifen an der Dorfstraße",
 400280: "Streifen in der Blockmitte",
 400281: "Breiter Bereich im Süden des Blocks mit dunklem Gartenteil und mehreren Dachreihen (nicht weiter trennbar)",
 400283: "Streifen an der Südwestecke des Blocks",
 400289: "Streifen mit langem grauem Dach in der Blockmitte",
}
for sid, txt in NEU.items():
    E.append((sid, "1.1.1", "HOFST", False, "sauber", f"{txt}. {HS}.", [], [U, E3, K1]))
E.append((400284, "1.3.2", "HOFST", False, "sauber", "Aus 400033: langer heller Dachstreifen westlich des Schattens 400061 an der Dorfstraße mit Hofrest.", [], [U, E2]))
E.append((400285, "1.3.2", "HOF", False, "sauber", "Aus 400033: Hoffläche zwischen Schatten 400087 und den Gebäuden 400067/400097.", [], [U, E2]))
E.append((400287, "1.3.2", "HOF", False, "sauber", "Aus 400033: schmaler Hof-/Durchgangsstreifen südlich von Gebäude 400098.", [], [U, E2]))
E.append((400288, "1.1.1", "HOF", False, "sauber", "Aus 400093: dunkelgrauer quadratischer Innenhof des Hofkomplexes, im Nordwesten beschattet.", [], [U, N2R, E1]))

QUELLE = {i: 400092 for i in range(1, 10)}
QUELLE.update({10: 400033, 11: 400033, 12: 400033, 13: 400093, 14: 400092})
zaehler = {"n": 0}


def gruende(art, s, e):
    if art == "quelle":
        return [QUELLE[zaehler["n"] + 1]]
    zaehler["n"] += 1
    nr = zaehler["n"]
    if nr == 13:
        return "Innenhof des Hofkomplexes 400093 (dunkleres Quadrat zwischen den hellen Flügeln) als eigene Fläche abgetrennt."
    if nr in (10, 11, 12):
        return "Mischfläche 400033 per Wasserscheide auf den dunklen Schattenlinien in Dachstreifen und Hofteile zerlegt."
    return "Häuserblock 400092 per Wasserscheide auf den dunklen Schattenlinien in Streckhof-Streifen zerlegt (Polygon = genau die Teilfläche)."


ein = ub.eingriffe_aus_ergebnis(O + "/eingriffe.json", O + "/eingriffe_ergebnis.txt", gruende)
uebersicht = [ub.H0 + "/H0.png", ub.H0 + "/ganz/H0_raster.jpg", ub.H0 + "/ganz/r1c1/ganz_nummern.jpg",
              ub.H0 + "/ganz/r1c1/ganz_roh.jpg", U, UR]
nah = [N2, N2R, E1, E2, E3, K1]
naht = [
 {"id": 400124, "seite": "rechts", "text": "Mischfläche reicht weit in den Kontextrand (r1c2 gibt es nicht: Rand des Ausschnitts); Teilung nur mit Blick auf den Kontext sinnvoll."},
 {"id": 400011, "seite": "oben", "text": "Straße läuft über die Kerngrenze nach r0c1; dort dieselbe Klasse Dorfstraße erwarten."},
 {"id": 400029, "seite": "oben", "text": "Großteils im Kontextrand (r0c1); Straße oder Straßenrand dort gemeinsam festlegen."},
]
unsicher = [
 "400103 (v4): Fahrbahn der östlichen Dorfstraße; die Randstücke 400088, 400099, 400113, 400051 hier als Dorfstraße bzw. Straßenrand beurteilt, im Verbund gleich halten.",
 "400138 (v4): grenzt an 400130; ob 400130 ein langes Dach oder eine Häuserzeile ist, im Verbund mit 400138 prüfen.",
 "400060 (v1): Schattenband westlich der Dorfstraße, wie 400090/400061 als Schatten beurteilt.",
]
nicht_geprueft = [
 "nah1, nah3, nah4 (vorbereitete Nahansichten) nicht eigens angesehen; die Stellen sind in den eigenen Nahansichten nah_1 bis nah_3 und kontrast_1 mit Grenzen und Gitter beurteilt.",
 "uebersicht_vorschlag, uebersicht_maengel, uebersicht_kontrast, uebersicht_gitter nicht angesehen.",
]
offen = [
 "Streckhof-Streifen aus 400092 und 400033: Dach gegen Hof im Schwarz-Weiß bei 0,45 m nicht trennbar; im Farbbild über Dachfarbe trennbar.",
 "400092 (Rest): große gleichmäßige hellgraue Fläche, großes Dach (Scheune/Stall, langer Schatten 400090 an der Ostseite) oder Hof/Garten; Farbbild oder Höhendaten würden entscheiden.",
 "400281: dunkler Gartenteil und Dachreihen nicht an klaren Kanten trennbar; Farbbild würde Garten (grün) von Dach trennen.",
 "400083/400091: schmales Gebäude oder Weg neben der Bogenstraße; 400082 Schatten oder Garten mit Bäumen.",
 "400093: Hofkomplex mit Innenhof (Vierseithof, eventuell öffentliches Gebäude); Flügel und Außensaum nicht weiter getrennt.",
]
ub.schreiben("v2", O, (314, 64, 564, 314), E, ein, uebersicht, nah, naht, unsicher, nicht_geprueft, offen)
