"""Urteil v4 (r1c1, Fassung B) schreiben."""
import sys

sys.path.insert(0, "C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c1/v1")
import urteil_bau as ub  # noqa: E402

O = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c1/v4"
V = ub.VB + "/v4"
U, UR = V + "/uebersicht_nummern.jpg", V + "/uebersicht_roh.jpg"
E1, E2, E3, K1 = O + "/nah_1.jpg", O + "/nah_2.jpg", O + "/nah_3.jpg", O + "/kontrast_1.jpg"
HS = "Streifen eines Streckhofs aus dem Nachsegmentieren: Dach und Hof zwischen dunklen Schattenlinien, bei 0,45 m nicht sicher trennbar"

E = [
 (400147, "1.2.1", "STR_DORF", False, "sauber", "Stück der östlichen Dorfstraße an der Viertelgrenze mit dunklem Rand.", [], [U, UR, E3]),
 (400151, "0.2", "SCH_GEB", True, "sauber", "Dunkle Fläche am Westrand der Dorfstraße: Schlagschatten der Häuser.", [], [U, E3]),
 (400157, "1.2.1", "STR_RAND", False, "sauber", "Grauer Randstreifen am Westrand der Dorfstraße.", [], [U, E3]),
 (400152, "1.3.2", "SCH", False, "nicht_sauber", "Dunkle Fläche am Ostrand der Dorfstraße: Schatten oder Baumkrone.", [("klasse", "Vorstufe Baustelle; dunkel (425/346).", None)], [U, E3]),
 (400156, "1.3.2", "HOF", False, "nicht_sauber", "Kleine graue Fläche zwischen Streifen und hellem Dach 400149: Hof.", [("klasse", "Vorstufe Baustelle; Hoffläche (506/341).", None)], [U, E1]),
 (400149, "1.1.1", "GEB_HELL", False, "sauber", "Großes helles Rechteck am Nordostrand mit dunklem Saum: Gebäude mit hellem Dach.", [], [U, UR, E1]),
 (400144, "0.2", "SCH_GEB", True, "sauber", "Sehr dunkle Fläche östlich des hellen Dachs 400149: Schlagschatten.", [], [U, E1]),
 (400160, "0.2", "SCH_GEB", True, "sauber", "Dunkle Fläche am Westrand der Dorfstraße: Schlagschatten.", [], [U, E3]),
 (400159, "1.3.2", "SCH", True, "nicht_sauber", "Kleine sehr dunkle Fläche zwischen den Höfen: Schatten.", [("klasse", "Vorstufe Baustelle; Schatten (498/353).", None)], [U, E1]),
 (400161, "0.2", "SCH", True, "sauber", "Sehr dunkle Fläche im Hof: Schatten.", [], [U, E1]),
 (400167, "0.2", "SCH", False, "sauber", "Dunkle Fläche am rechten Kernrand (38 px im Kern).", [], [U, E1]),
 (400138, "1.1.1", "HOFST", False, "nicht_sauber", "Nach dem Teilen der Rest des Häuserblocks östlich der Dorfstraße: Streifen am Ost- und Südrand, die über den Kernrand in den Kontext reichen.", [("trennen", "Ganzer Block östlich der Dorfstraße war ein Segment; Innenteile abgetrennt, Randteile bleiben verbunden (494/413).", 15045)], [U, UR, E1, E3, K1]),
 (400184, "0.2", "SCH", False, "sauber", "Dunkle Fläche am Ostrand: Schatten oder Bäume.", [], [U, E1]),
 (400188, "1.2.1", "STR_RAND", False, "sauber", "Kleines graues Stück an der Einmündung der Quergasse.", [], [U, E2]),
 (400192, "1.2.2", "STR_DORF", True, "nicht_sauber", "Helle Quergasse zwischen den beiden Dorfstraßen.", [("klasse", "Vorstufe Weg befestigt; Gasse/Straße im Ort (325/472).", None)], [U, UR, E2]),
 (400195, "0.2", "SCH_GEB", True, "sauber", "Dunkle Fläche an der Südseite der Quergasse: Schatten.", [], [U, E2]),
 (400194, "1.2.1", "VORPLATZ", False, "sauber", "Kleine helle Fläche an der Quergasse vor den Häusern.", [], [U, E2]),
 (400172, "0.2", "SCH_GEB", False, "sauber", "Langes dunkles Band an der Westseite der östlichen Dorfstraße: Schlagschatten der Häuserzeile, teils Bäume.", [], [U, E2, E3]),
 (400212, "0.2", "SCH", True, "sauber", "Sehr dunkle Fläche im Hof südlich der Quergasse: Schatten.", [], [U, E2]),
 (400204, "1.1.1", "GEB_MITTEL", False, "sauber", "Mittelgraues Rechteck südlich der Quergasse: Gebäude.", [], [U, E2]),
 (400196, "1.1.1", "HOFST", False, "nicht_sauber", "Nach dem Teilen die Hofstreifen südlich der Quergasse, die über den unteren Kernrand reichen.", [("trennen", "Mehrere Höfe in einem Segment; zwei Innenteile abgetrennt, Rest am Kernrand nicht trennbar (362/543).", 1710)], [U, UR, E2]),
 (400201, "1.2.1", "VORPLATZ", False, "sauber", "Kleine graue Fläche zwischen Haus und Dorfstraße.", [], [U, E2]),
 (400205, "0.2", "SCH", False, "sauber", "Dunkles Band südlich der Quergasse: Schatten mit Hofanteil.", [], [U, E2]),
 (400103, "1.2.2", "STR_DORF", True, "nicht_sauber", "Die helle östliche Dorfstraße mit der breiten Gabel im Süden.", [("klasse", "Vorstufe Weg befestigt; breite Dorfstraße (441/522).", None)], [U, UR, E2, E3]),
 (400206, "1.3.2", "SCH", False, "nicht_sauber", "Kleiner dunkler Fleck am Ostrand der Dorfstraße.", [("klasse", "Vorstufe Baustelle; dunkel (481/527).", None)], [U, E2]),
 (400213, "1.2.1", "HOF", False, "nicht_sauber", "Graue Fläche südlich der Straßengabel: Hof oder Vorplatz.", [("klasse", "Vorstufe Straße; dunkler als die Fahrbahn, Hof/Vorplatz (431/552).", None)], [U, E2]),
]
for sid, txt in {400290: "Dunklerer Streifen am Nordrand des Blocks", 400291: "Kleiner Streifen im Norden",
                 400292: "Streifen an der Dorfstraße im Norden", 400293: "Streifen im Nordteil",
                 400294: "Streifen an der Dorfstraße", 400295: "Streifen in der Blockmitte",
                 400296: "Streifen in der Blockmitte", 400297: "Streifen mit hellem Dach (480/450)",
                 400299: "Schmaler Streifen an der Dorfstraße", 400300: "Streifen im Südteil",
                 400301: "Streifen im Südteil", 400302: "Streifen am Ostrand im Süden",
                 400305: "Innenfläche des Blocks mit mehreren Dachteilen"}.items():
    E.append((sid, "1.1.1", "HOFST", False, "sauber", f"Aus 400138: {txt}. {HS}.", [], [U, E1, E3, K1]))
E.append((400303, "1.1.1", "HOFST", False, "sauber", f"Aus 400196: Streifen an der Einmündung mit kleinem hellem Dach (305/487). {HS}.", [], [U, E2]))
E.append((400304, "1.1.1", "GARTEN", False, "sauber", "Aus 400196: dunkle fleckige Fläche zwischen Quergasse und Gebäude 400204: Garten mit Schatten.", [], [U, E2]))

QUELLE = {i: 400138 for i in range(1, 13)}
QUELLE.update({13: 400196, 14: 400196, 15: 400138})
zaehler = {"n": 0}


def gruende(art, s, e):
    if art == "quelle":
        return [QUELLE[zaehler["n"] + 1]]
    zaehler["n"] += 1
    if QUELLE[zaehler["n"]] == 400196:
        return "Innenteil des Mischsegments 400196 per Wasserscheide auf dunklen Linien abgetrennt; Teile am Kernrand bleiben bei 400196."
    return "Innenteil des Häuserblocks 400138 per Wasserscheide auf dunklen Schattenlinien abgetrennt; Teile am Kernrand bleiben bei 400138 (Kontext unverändert)."


ein = ub.eingriffe_aus_ergebnis(O + "/eingriffe.json", O + "/eingriffe_ergebnis.txt", gruende)
uebersicht = [ub.H0 + "/H0.png", ub.H0 + "/ganz/H0_raster.jpg", ub.H0 + "/ganz/r1c1/ganz_nummern.jpg",
              ub.H0 + "/ganz/r1c1/ganz_roh.jpg", U, UR]
nah = [E1, E2, E3, K1]
naht = [
 {"id": 400138, "seite": "rechts", "text": "Rest von 400138 reicht über den rechten und unteren Kernrand; die abgetrennten Innenteile berühren den Kernrand nicht, der Kontext blieb unverändert."},
 {"id": 400196, "seite": "unten", "text": "Rest von 400196 reicht über den unteren Kernrand (Rand des Ausschnitts)."},
 {"id": 400103, "seite": "unten", "text": "Straße läuft über den unteren Kernrand; dieselbe Klasse Dorfstraße erwarten."},
]
unsicher = [
 "400130 (v2): langes graues Dach nördlich von 400290; ob Häuserzeile oder ein Gebäude, im Verbund mit 400290 prüfen.",
 "400234, 400236 (v1-Liste, aus 400006): Streifen westlich der Dorfstraße gegenüber; gleiche Klasse Hofstelle.",
 "400187 (v3): Straßenfläche an der Einmündung der Quergasse 400192; gleiche Klasse Dorfstraße.",
]
nicht_geprueft = [
 "Vorbereitete Nahansichten nah1 bis nah4 von v4 nicht angesehen; das Viertel ist in den eigenen Nahansichten nah_1 bis nah_3 und kontrast_1 mit Grenzen und Gitter beurteilt.",
 "uebersicht_vorschlag, uebersicht_maengel, uebersicht_kontrast, uebersicht_gitter nicht angesehen.",
]
offen = [
 "Hofstellen-Streifen aus 400138 und 400196: Dach gegen Hof im Schwarz-Weiß nicht trennbar; Farbbild würde trennen.",
 "400138 und 400196 bleiben am Kernrand große Mischflächen, weil ein Teilen dort den Kontextrand verändert oder eine gerade Naht ohne Bildkante erzeugt hätte; beim Zusammentragen mit dem Kontext weiter teilen.",
 "400172, 400205, 400184: Schatten oder Baumreihe; Farbbild würde entscheiden.",
]
ub.schreiben("v4", O, (314, 314, 564, 564), E, ein, uebersicht, nah, naht, unsicher, nicht_geprueft, offen)
