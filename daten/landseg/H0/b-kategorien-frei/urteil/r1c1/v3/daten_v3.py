"""Urteil v3 (r1c1, Fassung B) schreiben."""
import sys

sys.path.insert(0, "C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c1/v1")
import urteil_bau as ub  # noqa: E402

O = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c1/v3"
V = ub.VB + "/v3"
U, UR = V + "/uebersicht_nummern.jpg", V + "/uebersicht_roh.jpg"
N2, N2R, N4, N4R = V + "/nah2_nummern.jpg", V + "/nah2_roh.jpg", V + "/nah4_nummern.jpg", V + "/nah4_roh.jpg"
E1, K1 = O + "/nah_1.jpg", O + "/kontrast_1.jpg"

E = [
 (400145, "0.2", "HECKE", False, "nicht_sauber", "Langes dunkles, fleckiges Band am Westrand der Dorfstraße: Baum-/Gebüschreihe mit Schatten.", [("klasse", "Vorstufe Schatten; körnige Kronenreihe (198/321).", None)], [U, UR, N2, N2R]),
 (400154, "1.3.2", "SCH", False, "nicht_sauber", "Kleiner dunkler Fleck am Ostrand der Dorfstraße.", [("klasse", "Vorstufe Baustelle; dunkler Fleck (239/341).", None)], [U, N2, N2R]),
 (400153, "2.1", "RAIN", False, "sauber", "Dunkelgrauer Saum zwischen Feld 400118 und der Gehölzreihe: Feldrain.", [], [U, N2, N2R]),
 (400155, "1.2.1", "RAIN", False, "nicht_sauber", "Graues Stück zwischen Gehölzreihe und Fahrbahn: Bankett.", [("klasse", "Vorstufe Straße; dunkler als die Fahrbahn, Randstreifen (226/350).", None)], [U, N2, N2R]),
 (400162, "1.2.1", "BAUM", False, "nicht_sauber", "Dunkler Fleck am Westrand der Dorfstraße: Gebüsch.", [("klasse", "Vorstufe Straße; dunkler Gebüschfleck (234/372).", None)], [U, N2, N2R]),
 (400168, "1.3.2", "BAUM", False, "nicht_sauber", "Dunkler Fleck am Westrand der Dorfstraße: Gebüsch.", [("klasse", "Vorstufe Baustelle; Gebüsch (235/392).", None)], [U, N2, N2R]),
 (400164, "1.2.1", "RAIN", False, "nicht_sauber", "Graues Stück zwischen Gebüschen und Fahrbahn: Bankett.", [("klasse", "Vorstufe Straße; Randstreifen (241/378).", None)], [U, N2, N2R]),
 (400148, "6.6", "STR_DORF", True, "nicht_sauber", "Die helle Dorfstraße am Westrand des Orts.", [("klasse", "Vorstufe Feldweg; Dorfstraße (253/394).", None)], [U, UR, N2, N2R, N4]),
 (400163, "1.1.2", "SCH", False, "nicht_sauber", "Sehr dunkle kleine Fläche östlich der Straße neben 400257: Schatten oder Baumkrone.", [("klasse", "Vorstufe Nebengebäude; sehr dunkel, kein Dach (267/376).", None)], [U, N2, N2R, E1]),
 (400170, "1.3.2", "VORPLATZ", False, "nicht_sauber", "Graue Fläche zwischen Straße und Häusern: Vorplatz.", [("klasse", "Vorstufe Baustelle; Vorplatz (280/398).", None)], [U, N2, E1]),
 (400165, "1.3.2", "SCH", False, "nicht_sauber", "Kleiner dunkler Fleck östlich der Straße.", [("klasse", "Vorstufe Baustelle; dunkel (289/385).", None)], [U, N2, E1]),
 (400173, "3.1", "BAUM", False, "nicht_sauber", "Dunkelgrauer Fleck am Westrand der Dorfstraße: Gebüsch.", [("klasse", "Vorstufe Wiese; Gebüsch (238/401).", None)], [U, N2, N2R]),
 (400175, "2.1", "RAIN", False, "nicht_sauber", "Graues Stück zwischen Gebüschen und Fahrbahn: Bankett.", [("klasse", "Vorstufe Acker; Randstreifen (245/413).", None)], [U, N2, N2R]),
 (400180, "3.1", "BAUM", False, "nicht_sauber", "Dunkler Fleck am Westrand der Dorfstraße: Gebüsch.", [("klasse", "Vorstufe Wiese; Gebüsch (250/424).", None)], [U, N2, N2R]),
 (400178, "1.2.1", "STR_RAND", False, "sauber", "Hellgrauer Randstreifen der Dorfstraße.", [], [U, N2, N2R]),
 (400181, "1.3.2", "BAUM", False, "nicht_sauber", "Dunkle Flecken am Westrand der Dorfstraße: Gebüsch.", [("klasse", "Vorstufe Baustelle; Gebüsch (265/445).", None)], [U, N4, N4R]),
 (400177, "1.2.1", "VORPLATZ", False, "sauber", "Hellgraue Fläche am Ostrand der Straße vor den Häusern.", [], [U, N2, E1]),
 (400182, "1.2.1", "VORPLATZ", False, "sauber", "Sehr helle Fläche am Ostrand der Straße vor den Häusern: heller Vorplatz oder kleines helles Dach.", [], [U, N2, N4, E1]),
 (400171, "1.1.1", "GEB_MITTEL", False, "sauber", "Mittelgraue Dachfläche östlich der Straße mit hellem Westteil und Schatten an der Ostseite.", [], [U, N2, E1]),
 (400118, "2.2", "ACKER", False, "sauber", "Großes Feld westlich der Dorfstraße mit schrägen Bewirtschaftungsstreifen (Streifenflur) und einem schwachen dunklen Rechteckumriss.", [], [U, UR, N4, N4R, K1]),
 (400186, "2.1", "BAUM", False, "nicht_sauber", "Dunkelgrauer Fleck am Feldrand an der Straße: Gebüsch.", [("klasse", "Vorstufe Acker; Gebüsch (258/455).", None)], [U, N4, N4R]),
 (400189, "4.2.4", "BAUM", False, "sauber", "Dunkle Flecken am Westrand der Straße: Gebüsch.", [], [U, N4, N4R]),
 (400197, "2.1", "RAIN", False, "sauber", "Graues Stück am Feldrand an der Straße: Rain.", [], [U, N4, N4R]),
 (400200, "1.3.2", "BAUM", False, "nicht_sauber", "Dunkler runder Fleck am Straßenrand: Baum/Gebüsch.", [("klasse", "Vorstufe Baustelle; dunkle Krone (282/498).", None)], [U, N4, N4R]),
 (400187, "1.2.1", "STR_DORF", False, "sauber", "Helle Straßenfläche an der Einmündung der Quergasse 400192.", [], [U, N4, N4R]),
 (400190, "6.6", "STR_DORF", False, "sauber", "Kleines helles Stück der Straße an der Einmündung.", [], [U, N4]),
 (400202, "2.1", "RAIN", False, "sauber", "Stück der dunklen Feldgrenze am linken Rand (3 px im Kern).", [], [U, K1]),
 (400209, "1.3.4", "RAIN", False, "nicht_sauber", "Stück der dunklen Feldgrenze (Rain/Graben) am linken Kernrand.", [("klasse", "Vorstufe Sportplatz; Feldrain (66/524).", None)], [U, K1]),
 (400176, "2.1", "ACKER", False, "sauber", "Feld westlich der Feldgrenze, fast ganz im Kontextrand.", [], [U, K1]),
 (400211, "2.1", "RAIN", False, "sauber", "Stück der Feldgrenze am linken Kernrand.", [], [U, K1]),
 (400208, "6.1", "RAIN", False, "nicht_sauber", "Graues Stück am Feldrand an der Straße.", [("klasse", "Vorstufe Sandstelle; Feldrain (281/522).", None)], [U, N4, N4R]),
 (400203, "1.3.2", "STR_RAND", False, "nicht_sauber", "Hellgrauer Streifen am Straßenrand.", [("klasse", "Vorstufe Baustelle; Straßenrand (291/505).", None)], [U, N4, N4R]),
 (400214, "0.2", "BAUM", False, "nicht_sauber", "Sehr dunkler Fleck am Westrand der Straße: Baumkrone mit Schatten.", [("klasse", "Vorstufe Schatten; runde Krone (299/546).", None)], [U, N4, N4R]),
 (400207, "1.2.1", "STR_DORF", False, "sauber", "Helle Straße nach Süden mit Randanteil.", [], [U, N4, N4R]),
 (400215, "2.1", "RAIN", False, "sauber", "Stück der Feldgrenze am linken Kernrand.", [], [U, K1]),
 (400210, "2.1", "RAIN", False, "sauber", "Grauer, teils dunkler Saum am Feldrand an der Straße.", [], [U, N4, N4R]),
 (400216, "1.3.2", "SIED", False, "nicht_sauber", "Graue Fläche am Südrand östlich der Straße, meist im Kontextrand.", [("klasse", "Vorstufe Baustelle; Hof-/Hausfläche (310/560).", None)], [U, N4]),
]
uebersicht = [ub.H0 + "/H0.png", ub.H0 + "/ganz/H0_raster.jpg", ub.H0 + "/ganz/r1c1/ganz_nummern.jpg",
              ub.H0 + "/ganz/r1c1/ganz_roh.jpg", U, UR]
nah = [N2, N2R, N4, N4R, E1, K1]
naht = [
 {"id": 400118, "seite": "links", "text": "Feld reicht über die linke Kerngrenze nach r1c0 und nach oben in v1; dort dieselbe Klasse Acker."},
 {"id": 400176, "seite": "links", "text": "Feld westlich der Feldgrenze liegt fast ganz in r1c0; Klasse Acker dort bestätigen."},
 {"id": 400216, "seite": "unten", "text": "Reicht über die untere Kerngrenze (Rand des Ausschnitts); nur 88 px im Kern."},
]
unsicher = [
 "400196 (v4): enthält das kleine helle Dach an der Einmündung (305/487), das an 400187 grenzt.",
 "400257 (v1-Liste, aus 400006): dunkle Fläche neben 400163, gemeinsam Schatten oder Baumgruppe klären.",
 "400193, 400198 (Kontextrand links): weitere Stücke derselben Feldgrenze wie 400202/400209/400211/400215.",
]
nicht_geprueft = [
 "nah1 und nah3 (vorbereitet, Feldinneres) nicht eigens angesehen; das Feld ist in kontrast_1 ganz beurteilt.",
 "uebersicht_vorschlag, uebersicht_maengel, uebersicht_kontrast, uebersicht_gitter nicht angesehen.",
]
offen = [
 "400118: Streifenflur mit hellen und dunklen schrägen Streifen; ob es mehrere Felder (Besitzstreifen) sind, ist ohne klare Kante nicht zu entscheiden, daher nicht geteilt. Der schwache dunkle Rechteckumriss (etwa 135-175/400-440) und kurze dunkle Striche (etwa 200-225/530-550) sind nicht gedeutet.",
 "Acker gegen Grünland für 400118 und 400176 nur im Farbbild sicher.",
 "Gebüschflecken am Westrand der Dorfstraße (400162, 400168, 400173, 400180, 400181, 400186, 400189, 400200, 400214): einzelne Sträucher oder Bäume mit Schatten, Größe im Schwarz-Weiß nicht sicher.",
]
ub.schreiben("v3", O, (64, 314, 314, 564), E, [], uebersicht, nah, naht, unsicher, nicht_geprueft, offen)
