"""Neufassung der Abgabe Gegenprobe C, r0c0, v1: urteil.json und roh/umriss/maengel/vorschlag.jpg."""
import json

import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASIS = "C:/Users/Phil/Developement/Victor/daten/landseg/H0"
KARTE = BASIS + "/c-feste-liste/gegenprobe/r0c0/labels.tif"
SEG = BASIS + "/c-feste-liste/gegenprobe/r0c0/segmente.json"
BILD = BASIS + "/teilkacheln/r0c0.png"
ZIEL = BASIS + "/c-feste-liste/urteil-gegenprobe/r0c0/v1/"
VB = BASIS + "/viertel/r0c0/v1/"

U_N, U_R = VB + "uebersicht_nummern.jpg", VB + "uebersicht_roh.jpg"
N1N, N1R = VB + "nah1_nummern.jpg", VB + "nah1_roh.jpg"
O = {k: ZIEL + k for k in ["nah_1.jpg", "nah_2.jpg", "nah_3.jpg", "nah_4.jpg", "nah_1_roh.jpg",
                           "nah_2_roh.jpg", "nah_3_roh.jpg", "nah_4_roh.jpg", "kontrast_1.jpg"]}
K = O["kontrast_1.jpg"]


def nah(x, y):
    n = 1 + (1 if x >= 190 else 0) + (2 if y >= 190 else 0)
    return [O[f"nah_{n}.jpg"], O[f"nah_{n}_roh.jpg"]]


# (id, x, y, was_ist_es, klasse_vorschlag, sicher, [(art, text, flaeche)])
S = [
    (100001, 78, 78, "Großer dunkler, gleichmäßig gekörnter Schlag nordwestlich der Straße, wahrscheinlich Acker mit Bewuchs.",
     None, False, []),
    (100047, 97, 95, "Nach Verschmelzen: Randstreifen zwischen Acker 100001 und Straße 100004, etwas heller und fleckiger als der Acker.",
     "3.4", False, [("klasse", "Linearer Saum entlang der Straße (97/95 bis 135/62) statt Wiese/Weide: Krautsaum 3.4.", None),
                    ("grenze", "Grenze zum Acker 100001 nur schwach sichtbar (88/115 bis 125/62), geschätzt.", None)]),
    (100025, 139, 64, "Splitter der Fahrbahn 100004 am oberen Kernrand, 10 Bildpunkte im Kern.",
     "1.2", False, [("verschmelzen", "Ohne Bildkante zur Straße 100004 (139/64); gehört zu ihr.", 10),
                    ("klasse", "Teil der Straße, Klasse wie 100004 (1.2, Belag offen).", None)]),
    (100061, 151, 95, "Schmaler heller Streifen parallel zur Straße zwischen Saum 100033 und Hof 100065: Mauer, Pfad oder schmaler Bau.",
     "1", False, [("klasse", "Kein sicherer Bau: kein eigener Schlagschatten, Form eines Weg- oder Mauerstreifens (151/95); Ebene 1.", None)]),
    (100033, 153, 80, "Nach Verschmelzen mit 100072: grauer Streifen zwischen Straße 100004 und Hofreihe.",
     "3.4", False, [("klasse", "Fleckig mittelgrau wie ein Grasstreifen, nicht hell wie die Fahrbahn (153/80): Wegrand 3.4 statt Straße.", None)]),
    (100043, 202, 76, "Dunkler Schlagschatten nordöstlich des hellen schmalen Baus 100259.",
     "1", False, [("klasse", "Schatten, kein Gebäude (202/76); was darunter liegt, ist nicht erkennbar (U2), darum Ebene 1.", None)]),
    (100035, 251, 95, "Langes graues Rechteck mit dunklem Rand und hellem Südostende, Dach eines Streckhofs oder Hof.",
     "1", False, [("klasse", "Dach oder Hof auf dem Schwarz-Weiß-Bild nicht zu trennen (251/95); Ebene 1.", None),
                  ("trennen", "Helles Südostende (262/110) kann ein eigener Bau sein; Kante unscharf, nicht geteilt.", None)]),
    (100017, 270, 76, "Helles Dach mit Schlagschatten 100034 nach Nordosten, größtenteils im Kontextrand.",
     "1.1", True, [("klasse", "Gebäude sicher, Haupt- oder Nebengebäude nicht entscheidbar (270/76): 1.1.", None)]),
    (100034, 284, 69, "Dunkler Schlagschatten nordöstlich des Baus 100017.",
     "1", False, [("klasse", "Schatten, kein Gebäude (284/69); Untergrund nicht erkennbar, Ebene 1.", None)]),
    (100048, 287, 86, "Mischfläche aus Schattenkeil und grauem Streifen am Südostende von 100035, reicht nach v2.",
     "1", False, [("klasse", "Kein Gebäude erkennbar, Schatten und Gasse gemischt (287/86); Ebene 1.", None)]),
    (100007, 309, 64, "Ein Bildpunkt im Kern am oberen Rand, sonst dunkle Hof- oder Schattenfläche im Kontextrand.",
     "1", False, [("zu_klein", "Ein Bildpunkt im Kern (309/64), unter der Erkennbarkeit; fällt nach U4 dem Nachbarn zu.", 1)]),
    (100010, 310, 68, "Hellgrauer Gassenstreifen an der oberen rechten Viertelecke, Fortsetzung der Gasse 100064 nach Nordosten.",
     "1.2", False, [("klasse", "Keine Baustelle: gleichmäßiger heller Streifen zwischen Bauten (310/68), Gasse; Belag offen.", None)]),
    (100090, 68, 139, "Dunkler Ackerrand am linken Kernrand, gleicher Grauton wie der Acker 100001.",
     "2.1", False, [("klasse", "Kein Sportplatz: Grauton (56) und Körnung wie der Acker 100001 (68/139).", None),
                    ("verschmelzen", "Ohne Bildkante zum Acker 100001 (66/140); gehört zu ihm.", 129)]),
    (100097, 70, 149, "Kleiner dunkelgrauer Saum nordwestlich der Straße am linken Kernrand.",
     "3.4", False, [("klasse", "Fortsetzung des Straßensaums 100047 (70/149): 3.4 statt Wiese/Weide.", None)]),
    (100085, 74, 145, "Grauer Saum am Nordwestrand der Fahrbahn, heller als der Acker, dunkler als die Straße.",
     "3.4", False, [("klasse", "Keine Fahrbahn: deutlich dunkler als 100004 (74/145); Straßensaum 3.4.", None)]),
    (100088, 103, 145, "Nach Verschmelzen mit 100098 und 100108: gleichmäßig grauer Streifen zwischen Straße und Hofreihe.",
     "3.4", False, [("klasse", "Mittelgrau (95) statt hell wie die Fahrbahn (159), Grasstreifen oder Vorplatz (103/145); 3.4.", None)]),
    (100004, 112, 120, "Breite helle Fahrbahn quer durch das Viertel, Straße ins Dorf.",
     "1.2", False, [("klasse", "Breite und gleichmäßige Helligkeit sprechen für eine Straße, nicht für einen Feldweg (112/120); Belag nur im Farbbild, darum 1.2.", None)]),
    (100091, 113, 147, "Kleines dunkelgraues Stück zwischen Streifen 100088 und Schatten 100093.",
     "1", False, [("klasse", "Kein Bau erkennbar, Übergang zum Schatten 100093 (113/147); Ebene 1.", None),
                  ("verschmelzen", "Keine klare Kante zu 100093 (116/150).", 101)]),
    (100093, 125, 149, "Dunkler Schlagschatten nordöstlich des hellen Baus 100251.",
     "1", False, [("klasse", "Schatten über Hof, kein Gebäude (125/149); Ebene 1.", None)]),
    (100251, 120, 165, "Abgetrennt aus 100093: heller schmaler Bau mit Schatten nach Nordosten.",
     "1.1", True, [("klasse", "Gebäude sicher, Haupt- oder Nebengebäude nicht entscheidbar (120/165): 1.1.", None)]),
    (100078, 132, 130, "Graue, fleckige Hof- oder Gartenfläche hinter dem Straßenstreifen mit dunklem Fleck.",
     "1", False, [("klasse", "Kein Nebengebäude: kein Dachumriss, kein Schatten (132/130); Hof oder Garten, Ebene 1.", None)]),
    (100065, 166, 112, "Graue Hoffläche zwischen Streifen 100061 und Hofstreifen 100051.",
     "1", False, [("klasse", "Dach oder Hof nicht zu trennen (166/112); Ebene 1.", None)]),
    (100076, 205, 147, "Langes graues Dach mit hellem Südostende und Schlagschatten nach Nordosten.",
     "1.1", False, [("klasse", "Wahrscheinlich Dach eines Streckhofs (205/147), aber nicht sicher; Haupt oder Neben offen: 1.1.", None)]),
    (100051, 210, 107, "Grauer Hofstreifen mit dem Schatten des Baus 100076 an der Südwestseite.",
     "1", False, [("klasse", "Hof mit Schatten, kein ganzes Gebäude (210/107); Ebene 1.", None)]),
    (100259, 178, 77, "Abgetrennt aus 100051: schmaler heller Bau am Nordwestende der Parzelle, Schatten 100043 nordöstlich.",
     "1.1", True, [("klasse", "Gebäude sicher, Haupt oder Neben offen (178/77): 1.1.", None)]),
    (100064, 297, 104, "Hellgraue Gasse entlang der Südostenden der Höfe zwischen Höfen und Anger.",
     "1.2", False, [("klasse", "Keine Baustelle: gleichmäßiger Streifen, verbindet 100010 mit dem Anger (297/104); Gasse, Belag offen.", None)]),
    (100257, 310, 110, "Abgetrennt aus 100064: sehr heller kleiner Block an der Gasse, reicht nach v2.",
     "1", False, [("klasse", "Heller Bau oder Lagerhaufen (Sand, Kalk) nicht zu trennen (310/110); Ebene 1.", None)]),
    (100099, 103, 171, "Dunkler Schlagschatten nordöstlich des hellen Baus 100255.",
     "1", False, [("klasse", "Schatten über Hof, kein Gebäude (103/171); Ebene 1.", None)]),
    (100255, 95, 190, "Abgetrennt aus 100099: heller kleiner Bau mit Schatten nach Nordosten.",
     "1.1", False, [("klasse", "Wohl Bau, Umriss unscharf (95/190); 1.1 statt Hauptgebäude.", None)]),
    (100105, 149, 189, "Graue Parzellenfläche mit hellem Längsstreifen, Dach oder Hof.",
     "1", False, [("klasse", "Dach oder Hof nicht zu trennen (149/189); Ebene 1.", None)]),
    (100075, 175, 160, "Nach Abtrennen von 100249: Mischfläche aus Hof, Schatten und Dachteilen.",
     "1", False, [("klasse", "Kein ganzes Gebäude, Hof mit Schatten (175/160); Ebene 1.", None),
                  ("trennen", "Enthält noch dunkle Schattenteile (150/135) und helle Flecken; Kanten unscharf, nicht weiter geteilt.", None)]),
    (100249, 160, 150, "Abgetrennt aus 100075: heller schmaler Dachstreifen.",
     "1.1", False, [("klasse", "Heller Streifen, wohl Dach (160/150), Haupt oder Neben offen: 1.1.", None)]),
    (100106, 191, 180, "Hellgraue Hoffläche mit hellem Winkel am Südostende der Parzelle.",
     "1", False, [("klasse", "Hof oder Dach nicht zu trennen (191/180); Ebene 1.", None)]),
    (100113, 205, 191, "Kleiner sehr dunkler Fleck in einer Hofecke, Schatten.",
     "1", False, [("klasse", "Schatten, kein Gebäude (205/191); Ebene 1.", None)]),
    (100077, 276, 163, "Nach Verschmelzen mit 100080, 100103, 100122: fleckige offene Fläche hinter den Höfen, hell und dunkel gesprenkelt.",
     "3", False, [("klasse", "Kein gepflügter Acker: keine Furchen, unregelmäßig gefleckt (276/163); Grünland, Brache oder Garten, Ebene 3.", None)]),
    (100115, 304, 194, "Kleiner heller rechteckiger Bau mit Schatten nach Nordosten.",
     "1.1", True, [("klasse", "Gebäude sicher, Nebengebäude wegen der Größe (etwa 8 m) nur wahrscheinlich (304/194): 1.1.", None)]),
    (100124, 65, 202, "Splitter am linken Kernrand südöstlich der Fahrbahn, 18 Bildpunkte im Kern.",
     "3.4", False, [("klasse", "Keine Fahrbahn: grau wie der Straßensaum 100088 (65/202); 3.4.", None)]),
    (100136, 71, 232, "Großer dunkler, rundlicher Fleck am linken Kernrand, Schatten oder Baumkrone.",
     "1", False, [("klasse", "Kein Dach erkennbar (71/232); Schatten im Hof oder Baum nicht zu trennen, Ebene 1.", None)]),
    (100116, 79, 200, "Dunkle Fläche mit kleinem hellem Teil, Schatten im Hof.",
     "1", False, [("klasse", "Schatten, kein Gebäude (79/200); Ebene 1.", None)]),
    (100147, 79, 246, "Kleiner heller Hof- oder Wegfleck.",
     "1", False, [("klasse", "Keine Baustelle: kleiner gleichmäßiger heller Fleck zwischen Höfen (79/246); Ebene 1.", None)]),
    (100121, 139, 225, "Großes helles Rechteckdach mit Schatten 100132 nach Nordosten.",
     "1.1", True, [("klasse", "Gebäude sicher; Größe (etwa 22 × 11 m) spricht eher für Hauptgebäude, nicht für Nebengebäude (139/225): 1.1.", None)]),
    (100132, 164, 238, "Dunkles L an der Ost- und Südostseite des Baus 100121, Schlagschatten.",
     "1", False, [("klasse", "Schatten, kein Gebäude (164/238); Ebene 1.", None)]),
    (100120, 177, 204, "Dunkles Rechteck am Südostende der Parzelle 100105, dunkles Dach oder Schatten.",
     "1", False, [("klasse", "Dunkles Dach oder Schatten nicht zu trennen (177/204); Ebene 1.", None)]),
    (100134, 273, 233, "Dunkles, gekörntes Rechteck im offenen Gelände mit dunklem Rand an der Südwestseite, umfriedeter Garten.",
     "2", False, [("klasse", "Kein Nebengebäude: Körnung wie Bewuchs, kein Schatten nach Nordosten (273/233); Gartenbeet zählt nach G1 zu Acker (2), Rasen nicht ausgeschlossen.", None)]),
    (100129, 80, 270, "Helle, fleckige Hof- und Gartenfläche mit hellen Flecken.",
     "1", False, [("klasse", "Kein ganzes Gebäude (80/270); Hof mit Gartenstücken, Ebene 1.", None),
                  ("trennen", "Heller Bauteil (96/270) und dunklere Gartenstücke; Kanten unscharf, nicht geteilt.", None)]),
    (100138, 120, 252, "Gleichmäßig gekörnte dunkelgraue Fläche südwestlich von 100121, Garten.",
     "2", False, [("klasse", "Kein Nebengebäude: Körnung wie Bewuchs, kein eigener Schatten (120/252); Gartenbeet (2), Rasen nicht ausgeschlossen.", None)]),
    (100114, 202, 254, "Nach Verschmelzen mit 100171: offene, fleckige Fläche (Anger) mit hellem Fahrweg am Acker 100154, reicht nach v3.",
     "3", False, [("klasse", "Keine Baustelle: fleckiger Bewuchs mit Trittstellen (202/254); Grünland oder Ruderalflur, Ebene 3.", None),
                  ("trennen", "Heller Fahrweg von 100/300 bis 300/270 mit weicher Kante; nicht geteilt.", None)]),
    (100163, 306, 279, "Kleiner mittelgrauer Fleck an der Viertelecke zwischen Acker 100154 und Weg, Saum.",
     "3", False, [("klasse", "Kein Acker: heller und glatter als 100154 (306/279); Saum oder Wegrand, Ebene 3.", None)]),
    (100160, 74, 302, "Graue, etwas fleckige Parzelle unten links, reicht nach v3.",
     "3", False, [("klasse", "Kein Gebäude: gleichmäßige Fläche ohne Dach und Schatten (74/302); Wiese oder Garten, Ebene 3.", None)]),
    (100168, 190, 303, "Dunklerer Streifen zwischen Anger 100114 und Acker 100154, Feldrain.",
     "3.4", False, [("klasse", "Linearer Streifen am Ackerrand (190/303): Feldrain 3.4 statt Wiese/Weide.", None)]),
]

EINGRIFFE = [
    ("teilen", [100075], [100075, 100249], "Heller Dachstreifen (160/150) aus der Mischfläche aus Hof und Schatten gelöst."),
    ("teilen", [100093], [100093, 100251], "Heller schmaler Bau (120/165) aus dem Schattensegment gelöst; die Splitter 100250, 100252, 100253 des Schnitts sind in 100251 aufgegangen."),
    ("teilen", [100099], [100099, 100255], "Heller kleiner Bau (95/190) aus dem Schattensegment gelöst; die Splitter 100254, 100256 sind in 100255 aufgegangen."),
    ("teilen", [100064], [100064, 100257], "Sehr heller Block (310/110) aus der Gasse gelöst; die Splitter des Schnitts sind in 100257 aufgegangen."),
    ("verschmelzen", [100047, 100052, 100057, 100058, 100067, 100068, 100074], [100047], "Stücke des Straßensaums nordwestlich der Fahrbahn ohne Bildkante zueinander."),
    ("teilen", [100051], [100051, 100259], "Schmaler heller Bau (178/77) am Nordwestende aus dem Hofstreifen gelöst; die Splitter des Schnitts sind in 100259 aufgegangen."),
    ("verschmelzen", [100033, 100072], [100033], "Zwei Stücke desselben grauen Streifens zwischen Straße und Hofreihe ohne Bildkante."),
    ("verschmelzen", [100088, 100098, 100108], [100088], "Drei Stücke desselben grauen Streifens südöstlich der Fahrbahn ohne Bildkante."),
    ("verschmelzen", [100077, 100080, 100103, 100122], [100077], "Flecken derselben offenen Fläche hinter den Höfen ohne Bildkante."),
    ("verschmelzen", [100114, 100171], [100114], "Randstück des Angers ohne Bildkante zu 100114."),
]


def lade():
    try:
        import tifffile
        lab = tifffile.imread(KARTE)
    except ImportError:
        lab = np.array(Image.open(KARTE))
    return lab.astype(np.int64), np.array(Image.open(BILD).convert("RGB"))


def font(gr, fett=True):
    for f in (("C:/Windows/Fonts/arialbd.ttf",) if fett else ()) + ("C:/Windows/Fonts/arial.ttf",):
        try:
            return ImageFont.truetype(f, gr)
        except OSError:
            pass
    return ImageFont.load_default()


def urteil_schreiben(segs):
    eintraege = []
    for sid, x, y, was, kv, sicher, punkte in S:
        kh = segs[sid]["klasse"]
        pl = [{"nr": i, "art": a, "text": t, "flaeche_px": f} for i, (a, t, f) in enumerate(punkte, 1)]
        eintraege.append({
            "id": sid, "klasse_heute": kh, "was_ist_es": was,
            "urteil": "sauber" if not pl else "nicht_sauber",
            "klasse_vorschlag": kv, "sicher": sicher, "punkte": pl,
            "bilder": [U_N, U_R] + nah(x, y) + [K],
        })
    u = {
        "teilkachel": "r0c0", "viertel": "v1", "bearbeiter": "gegen-c-r0c0-v1",
        "bilder_angesehen": {
            "uebersicht": [BASIS + "/H0.png", BASIS + "/ganz/r0c0/ganz_nummern.jpg", U_N, U_R],
            "nah": [N1R, N1N] + [O[k] for k in ["nah_1.jpg", "nah_1_roh.jpg", "nah_2.jpg", "nah_2_roh.jpg",
                                               "nah_3.jpg", "nah_3_roh.jpg", "nah_4.jpg", "nah_4_roh.jpg",
                                               "kontrast_1.jpg"]],
        },
        "segmente": eintraege,
        "naht": [
            {"id": 100114, "seite": "unten", "text": "Reicht über die Viertelgrenze y 314 nach v3; die Klasse 3 gilt für das ganze Segment (Anger mit Fahrweg)."},
            {"id": 100160, "seite": "unten", "text": "Reicht zur Hälfte nach v3; Klasse 3 für das ganze Segment, im Viertel v3 gegenprüfen."},
            {"id": 100077, "seite": "rechts", "text": "Reicht über x 314 nach v2 (9 %); Klasse 3 für das ganze Segment."},
            {"id": 100257, "seite": "rechts", "text": "Heller Block reicht über x 314 nach v2 (26 %); Ebene 1 für das ganze Segment."},
        ],
        "unsicher": [
            "Schattenrichtung: Schlagschatten liegen nordöstlich der hellen Bauten (Sonne aus Südwest); dunkle Bänder darum als Schatten mit Ebene 1 und sicher: false.",
            "Die Eingriffe dieses Viertels standen schon auf der Kartenkopie (gleicher Bearbeiter-Name, erster Lauf dieses Auftrags); ich habe sie am Bild nachgesehen und behalten, keine neuen Eingriffe.",
            "100104 (v2): helle Fahrspur und Hof gemischt östlich von 100134; nur als Nachbar gesehen.",
            "100154 (v3/v4): großer Acker südlich des Angers, Grenze zum Rain 100168 plausibel; nur als Nachbar gesehen.",
            "100173 und 100181 (v3): grau gekörnte Flächen unten links wie 100160; nur als Nachbar gesehen.",
        ],
        "nicht_geprueft": [
            "Vorbereitete Nahansichten nah2–nah4 sowie uebersicht_kontrast, uebersicht_vorschlag, uebersicht_maengel und uebersicht_gitter nicht angesehen; statt dessen eigene Nahansichten des aktuellen Kartenstands (nah_1 bis nah_4, kontrast_1).",
            "H0_raster.jpg und ganz_roh.jpg nicht angesehen.",
            "Kontextrand-Anteile von 100001, 100007, 100010, 100017, 100034, 100097, 100124, 100136 nur als Umgebung gesehen.",
        ],
        "offen": [
            "Dach oder Hof bei 100035, 100051, 100065, 100075, 100105, 100106, 100120: im Farbbild (Ziegelrot gegen Grün/Grau) entscheidbar.",
            "Acker oder Grünland bei 100001, 100090, 100134, 100138, 100160: Farbbild oder Flurkarte (Gartenbeet, Rasen, Acker).",
            "Belag der Straße 100004 und der Gasse 100064/100010 (Asphalt, Pflaster oder Schotter): Farbbild oder Ortskenntnis.",
            "100136: Schatten oder Baumkrone; 100257: heller Bau oder Lagerhaufen; Farbbild entscheidet.",
            "Heller Fahrweg in 100114 (100/300 bis 300/270) wäre ein eigenes Segment (6.6), Kante zu weich zum Teilen.",
        ],
        "eingriffe": [{"schritt": s, "vorher": v, "nachher": n, "grund": g} for s, v, n, g in EINGRIFFE],
    }
    with open(ZIEL + "urteil.json", "w", encoding="utf-8") as f:
        json.dump(u, f, ensure_ascii=False, indent=1)
    return u


FARBE = {"1": (230, 60, 60), "2": (230, 200, 40), "3": (90, 200, 70), "4": (20, 120, 40),
         "5": (60, 120, 230), "6": (180, 130, 80), "0": (160, 160, 160)}


def basisbild(lab, img, x0, y0, w, h, f, grenzen=True):
    sub = img[y0:y0 + h, x0:x0 + w]
    big = np.kron(sub, np.ones((f, f, 1), dtype=np.uint8))
    if grenzen:
        Lb = np.kron(lab[y0:y0 + h, x0:x0 + w], np.ones((f, f), dtype=np.int64))
        r = np.zeros(Lb.shape, bool)
        r[:-1, :] |= Lb[:-1, :] != Lb[1:, :]
        r[:, :-1] |= Lb[:, :-1] != Lb[:, 1:]
        big[r] = (255, 230, 0)
    return big


def rahmen(d, x0, y0, f):
    d.rectangle([(64 - x0) * f, (64 - y0) * f, (314 - x0) * f, (314 - y0) * f], outline=(0, 230, 230), width=2)


def titel(im, text):
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, im.width, 20], fill=(0, 0, 0))
    d.text((6, 2), text, fill=(255, 255, 255), font=font(14))


def bilder(u, segs):
    lab, img = lade()
    x0, y0, w, h, f = 32, 32, 314, 314, 3
    eigene = {e["id"] for e in u["segmente"]}
    pos = {sid: (x, y) for sid, x, y, *_ in S}
    # roh
    im = Image.fromarray(basisbild(lab, img, x0, y0, w, h, f, grenzen=False))
    rahmen(ImageDraw.Draw(im), x0, y0, f)
    titel(im, "r0c0 v1: Teilkachelbild unverändert (3fach), Viertel cyan")
    im.save(ZIEL + "roh.jpg", quality=90)
    # umriss
    im = Image.fromarray(basisbild(lab, img, x0, y0, w, h, f))
    d = ImageDraw.Draw(im)
    rahmen(d, x0, y0, f)
    L = lab[y0:y0 + h, x0:x0 + w]
    fo = font(11)
    for i in np.unique(L):
        if i in pos:
            px, py = (pos[i][0] - x0) * f, (pos[i][1] - y0) * f
        else:
            ys, xs = np.nonzero(L == i)
            k = np.argmin((ys - ys.mean()) ** 2 + (xs - xs.mean()) ** 2)
            px, py = xs[k] * f, ys[k] * f
        col = (255, 255, 255) if i in eigene else (160, 160, 160)
        d.text((px, py), str(i), fill=col, font=fo, anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0))
    titel(im, "r0c0 v1: Segmentgrenzen (aktueller Stand), volle ID; weiß = dieses Viertel")
    im.save(ZIEL + "umriss.jpg", quality=90)
    # maengel
    base = Image.fromarray(basisbild(lab, img, x0, y0, w, h, f))
    mangel = [e for e in u["segmente"] if e["urteil"] == "nicht_sauber"]
    zeilen = (len(mangel) + 1) // 2
    im = Image.new("RGB", (base.width, base.height + 22 + zeilen * 16 + 8), (255, 255, 255))
    im.paste(base, (0, 22))
    d = ImageDraw.Draw(im)
    rahmen_off = lambda: d.rectangle([(64 - x0) * f, (64 - y0) * f + 22, (314 - x0) * f, (314 - y0) * f + 22], outline=(0, 230, 230), width=2)
    rahmen_off()
    fo, fl = font(12), font(11, fett=False)
    kurz = {"klasse": "Klasse", "trennen": "trennen", "verschmelzen": "verschmelzen", "grenze": "Grenze", "zu_klein": "zu klein"}
    for n, e in enumerate(mangel, 1):
        x, y = pos[e["id"]]
        px, py = (x - x0) * f, (y - y0) * f + 22
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=(220, 30, 30), outline=(255, 255, 255))
        d.text((px, py), str(n), fill=(255, 255, 255), font=font(10), anchor="mm")
        arten = ", ".join(dict.fromkeys(kurz.get(p["art"], p["art"]) for p in e["punkte"]))
        t = f"{n} {e['id']}: {arten}" + (f" → {e['klasse_vorschlag']}" if e["klasse_vorschlag"] else "")
        col, row = (n - 1) // zeilen, (n - 1) % zeilen
        d.text((8 + col * (im.width // 2), base.height + 26 + row * 16), t, fill=(0, 0, 0), font=fl)
    d.rectangle([0, 0, im.width, 20], fill=(0, 0, 0))
    d.text((6, 2), f"r0c0 v1: Mängel (rote Punkte, {len(mangel)} Segmente nicht sauber), Legende unten", fill=(255, 255, 255), font=font(14))
    im.save(ZIEL + "maengel.jpg", quality=90)
    # vorschlag
    big = basisbild(lab, img, x0, y0, w, h, f, grenzen=False).astype(float)
    Lb = np.kron(L, np.ones((f, f), dtype=np.int64))
    klasse = {e["id"]: (e["klasse_vorschlag"] or e["klasse_heute"]) for e in u["segmente"]}
    for i in np.unique(L):
        k = klasse.get(i, segs.get(int(i), {}).get("klasse", "0"))
        m = Lb == i
        a = 0.45 if i in eigene else 0.15
        big[m] = big[m] * (1 - a) + np.array(FARBE.get(k[0], (160, 160, 160))) * a
    big = big.astype(np.uint8)
    r = np.zeros(Lb.shape, bool)
    r[:-1, :] |= Lb[:-1, :] != Lb[1:, :]
    r[:, :-1] |= Lb[:, :-1] != Lb[:, 1:]
    big[r] = (255, 230, 0)
    base = Image.fromarray(big)
    im = Image.new("RGB", (base.width, base.height + 22 + 40), (255, 255, 255))
    im.paste(base, (0, 22))
    d = ImageDraw.Draw(im)
    d.rectangle([(64 - x0) * f, (64 - y0) * f + 22, (314 - x0) * f, (314 - y0) * f + 22], outline=(0, 230, 230), width=2)
    for e in u["segmente"]:
        x, y = pos[e["id"]]
        t = klasse[e["id"]] + ("" if e["sicher"] else "?")
        d.text(((x - x0) * f, (y - y0) * f + 22), t, fill=(255, 255, 255), font=font(12), anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0))
    leg = [("1", "1 bebaut/Verkehr"), ("2", "2 Acker/Garten"), ("3", "3 Grünland/Saum"), ("6", "6 offener Boden")]
    for n, (k, t) in enumerate(leg):
        xx = 8 + n * 230
        d.rectangle([xx, base.height + 30, xx + 16, base.height + 46], fill=FARBE[k])
        d.text((xx + 22, base.height + 30), t, fill=(0, 0, 0), font=font(13, fett=False))
    d.text((8, base.height + 48), "Code = vorgeschlagene Klasse, ? = sicher: false; Grenzen unverändert", fill=(0, 0, 0), font=font(11, fett=False))
    d.rectangle([0, 0, im.width, 20], fill=(0, 0, 0))
    d.text((6, 2), "r0c0 v1: Vorschlag (Grenzen unverändert, Klassen wie ich sie setzen würde)", fill=(255, 255, 255), font=font(14))
    im.save(ZIEL + "vorschlag.jpg", quality=90)


if __name__ == "__main__":
    segs = {s["id"]: s for s in json.load(open(SEG, encoding="utf-8"))["segmente"]}
    u = urteil_schreiben(segs)
    bilder(u, segs)
    ns = [e for e in u["segmente"] if e["urteil"] == "nicht_sauber"]
    print("segmente", len(u["segmente"]), "nicht_sauber", len(ns),
          "punkte", sum(len(e["punkte"]) for e in u["segmente"]),
          "unsicher", sum(1 for e in u["segmente"] if not e["sicher"]))
