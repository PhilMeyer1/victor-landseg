"""Baut urteil.json und die Ergebnisbilder (Nachholer urt-c-r0c0-v1), Stand der Karte nach den Eingriffen 2-6."""
import json
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont

H0 = Path("C:/Users/Phil/Developement/Victor/daten/landseg/H0")
ERG = H0 / "c-feste-liste/urteil/r0c0/v1"
VB = H0 / "viertel/r0c0/v1"
LAB = H0 / "c-feste-liste/r0c0/labels.tif"
SEG = H0 / "c-feste-liste/r0c0/segmente.json"
BILD = H0 / "teilkacheln/r0c0.png"
FX, FY, FW, FF = 32, 32, 314, 3

lab = tifffile.imread(str(LAB)).astype(np.int64)
img = np.array(Image.open(BILD).convert("L"))
seg = {s["id"]: s for s in json.loads(SEG.read_text(encoding="utf-8"))["segmente"]}

U = lambda n: str(VB / n).replace("\\", "/")
E = lambda n: str(ERG / n).replace("\\", "/")

# (id, vorschlag, sicher, was_ist_es, [(art, text, x, y, flaeche)])
D = [
 (100001, "2", False, "Großer dunkler, gleichmäßig feinkörniger Acker westlich der Straße mit schwachen Längsstreifen (Streifenflur); nach dem Verschmelzen mit den Splittern 58 und 68 eine Fläche.",
  [("klasse", "Acker sicher, aber mit Bewuchs (2.1) oder gepflügt (2.2) ist auf dem Schwarz-Weiß-Scan nicht zu trennen (78/78): Elternklasse 2.", 78, 78, None),
   ("grenze", "Grenze zum Randstreifen 47 liegt bei 97-105/70-110 ohne deutliche Bildkante, teils 5-8 Bildpunkte zu weit im Acker.", 100, 95, None)]),
 (100047, "3.4", False, "Hellerer Gras- bzw. Krautstreifen zwischen Straße 4 und Acker 1 (Wegrand), nach dem Verschmelzen mit 52, 57, 67 und 74 ein Streifen.",
  [("klasse", "Linearer Wegrand, keine Wiese: 3.4 statt 3.1 (118/73).", 118, 73, None),
   ("grenze", "Oben (97-130/64-100) greift der Streifen keilförmig in den Acker ein, wo das Bild keine Kante zeigt.", 108, 80, None)]),
 (100025, "3.4", False, "Nur 10 Bildpunkte im Kern an der oberen Kerngrenze (139/64): Fortsetzung des Wegrands westlich der Straße.",
  [("klasse", "Wegrand statt Straße (139/64).", 139, 64, 10)]),
 (100061, "1.1", False, "Schmaler, heller Streifen (etwa 17 × 3 m) zwischen Vorplatz 33 und Hof 65: schmaler Bau oder Mauerkrone mit Schatten in den Hof.",
  [("klasse", "Gebäude wahrscheinlich, Haupt- oder Nebengebäude nicht entscheidbar: 1.1 (151/95).", 151, 95, None)]),
 (100033, "3.4", False, "Mittelgrauer Streifen zwischen Straße 4 und den Hausfronten 43/61: Grünstreifen bzw. Vorplatz vor den Höfen, keine Fahrbahn.",
  [("klasse", "Kein Straßenbelag erkennbar, Grauton wie Wegrand: 3.4 statt 1.2.1 (153/80).", 153, 80, None)]),
 (100043, "1.1", False, "Langes schmales Haus an der Straße mit heller Dachhälfte (160-190/64-92) und dunkler Schattenseite nordöstlich, typisches Streckhof-Haus.",
  [("klasse", "Wohn- oder Wirtschaftsteil nicht trennbar: Elternklasse 1.1 (202/76).", 202, 76, None)]),
 (100035, "3", False, "Langer, von niedrigen Mauern (dünne Schattenlinien) umfasster, fleckig mittelgrauer Hof bzw. Garten; kein Dach (kein First, keine Schattenseite).",
  [("klasse", "Hof oder Garten statt Hauptgebäude (251/95); Bewuchs gegen Erdboden erst im Farbbild sicher.", 240, 90, None)]),
 (100249, "1.1", False, "Aus 35 abgetrennt: heller, scharf begrenzter Bau (etwa 8 × 7 m) am Südostende des Hofes 35, wohl Stadel oder Schuppen.", []),
 (100017, "1.1", False, "Helle lange Dachfläche eines Streckhof-Hauses nördlich von 35, nur 598 von 2519 Bildpunkten im Kern.",
  [("klasse", "Gebäude, Haupt- oder Nebengebäude offen: 1.1 (270/76).", 270, 76, None)]),
 (100034, "1.1", False, "Tiefschwarze Fläche nordöstlich des Dachs 17: Schattenseite des Daches bzw. Schlagschatten, überwiegend im Kontextrand.",
  [("klasse", "Schatten am Haus 17 (U2): Fortsetzung des Gebäudes, 1.1 statt 1.1.1 (284/69).", 284, 69, None)]),
 (100048, "1", False, "Mischfläche nordöstlich des Hofes 35: oben Schlagschatten von 17/34, unten heller Hintausweg; 76 % im Viertel.",
  [("trennen", "Schatten (oben, 280-300/72-85) und Weg (unten, 285-310/88-100) liegen in einem Segment; Kante im Schatten nicht sicher, darum nicht geteilt.", 290, 86, None)]),
 (100007, "1.1", False, "Nur 1 Bildpunkt im Kern (309/64); dunkle Fläche (Schatten bzw. Dach) nördlich im Kontextrand.",
  [("zu_klein", "1 Bildpunkt im Kern (309/64), gehört zum Bau im Kontextrand.", 309, 64, 1)]),
 (100010, "6.6", False, "Heller Boden an der oberen Kerngrenze (300-315/64-75), Fortsetzung des Hintauswegs nach Norden.",
  [("klasse", "Weg statt Baustelle (310/68), befestigt oder nicht erst im Farbbild.", 310, 68, None)]),
 (100090, "2", False, "Dunkles Stück des Ackers 1 am linken Kernrand (68/139), ohne Bildkante von 1 getrennt.",
  [("verschmelzen", "Gehört zu Acker 1, keine Kante (68/139).", 68, 139, 129),
   ("klasse", "Acker statt Sportplatz (68/139).", 68, 139, None)]),
 (100097, "3.4", False, "Kleines Kernstück (60 Bildpunkte) des hellen Randstreifens westlich der Straße am linken Kernrand.",
  [("klasse", "Wegrand (70/149).", 70, 149, None)]),
 (100085, "3.4", False, "Heller Gras- bzw. Krautstreifen westlich der Straße bei 74/145, Fortsetzung von 47.",
  [("klasse", "Wegrand statt Straße (74/145).", 74, 145, None)]),
 (100088, "3.4", False, "Mittelgrauer Streifen zwischen Straße 4 und den Häusern 99/93 (Grünstreifen bzw. Vorplatz), nach dem Verschmelzen mit 98 und 108 ein Streifen.",
  [("klasse", "Kein Fahrbahnbelag erkennbar: 3.4 statt 1.2.1 (103/145).", 103, 145, None)]),
 (100004, "1.2", False, "Helle, etwa 7 m breite gerade Straße von Südwest nach Nordost am Ortsrand mit scharfen Rändern.",
  [("klasse", "Verkehrsfläche sicher, versiegelt (1.2.1) oder Schotter (6.6) nicht entscheidbar: 1.2 (112/120).", 112, 120, None)]),
 (100091, "1.1", False, "Kleiner dunkler Splitter (101 Bildpunkte) am Nordwestende von Haus 93.",
  [("verschmelzen", "Gehört zur Schattenseite von Haus 93, keine Kante (113/147).", 113, 147, 101)]),
 (100093, "1.1", False, "Langes Haus senkrecht zur Straße: schmale helle Dachhälfte südwestlich und tiefschwarze Schattenseite nordöstlich.",
  [("klasse", "Gebäude, Art offen: 1.1 (125/149).", 125, 149, None)]),
 (100072, "1.2", False, "Hellerer Fleck zwischen Straße 4 und Vorgarten 78, wohl Einfahrt.",
  [("klasse", "Einfahrt, Belag offen: 1.2 (128/112).", 128, 112, None)]),
 (100078, "3", False, "Mittelgraue fleckige Fläche am Straßenende des Grundstücks mit dunklem rundem Fleck (Baum oder Strauch bei 125/127): Vorgarten bzw. Hof.",
  [("klasse", "Garten bzw. Hof statt Nebengebäude (132/130).", 132, 130, None),
   ("fehlt", "Dunkler runder Fleck (etwa 4 m) bei 125/127, wohl Gehölz (4.2), nicht abgetrennt; an der Erkennbarkeitsgrenze.", 125, 127, None)]),
 (100065, "3", False, "Mittelgraue Fläche zwischen dem Haus in 75 und dem schmalen Bau 61: Hof bzw. Garten des Grundstücks.",
  [("klasse", "Hof bzw. Garten statt Hauptgebäude (166/112).", 166, 112, None)]),
 (100076, "3", False, "Langer, fleckig mittelgrauer, ummauerter Hof bzw. Garten zwischen 51 und dem Schattenband in 75; der helle Bau am Südostende ist jetzt 250.",
  [("klasse", "Hof bzw. Garten statt Hauptgebäude (190/130).", 190, 130, None)]),
 (100250, "1.1", False, "Aus 76 abgetrennt: heller Bau (etwa 7 × 8 m) am Südostende des Hofes 76, Stadel oder Schuppen.", []),
 (100051, "3", False, "Langer, von niedrigen Mauern umfasster Hof bzw. Garten (etwa 40 × 12 m) neben Haus 43, fleckig mittelgrau.",
  [("klasse", "Hof bzw. Garten statt Hauptgebäude (210/107).", 210, 107, None)]),
 (100080, "3", False, "Etwas hellerer Fleck in der offenen Fläche 77 (279/127).",
  [("verschmelzen", "Teil der Fläche 77, nur schwache Helligkeitsänderung (279/127).", 279, 127, 182)]),
 (100064, "6.6", False, "Heller Hintausweg entlang der Gartenmauern von Südwest nach Nordost mit unruhigen Rändern.",
  [("klasse", "Weg statt Baustelle (297/104); unbefestigt wahrscheinlich, im Farbbild prüfen.", 297, 104, None)]),
 (100099, "1.1", False, "Streckhof-Haus: helle Dachhälfte bei 85-105/165-200 und dunkle Schattenseite nordöstlich.",
  [("klasse", "Gebäude, Art offen: 1.1 (103/171).", 103, 171, None)]),
 (100105, "6", False, "Helle, fleckige Fläche zwischen Haus 93 und dem großen Bau 121 mit kleinem dunklem Fleck: offene Hoffläche.",
  [("klasse", "Hoffläche statt Hauptgebäude (149/189); Erdboden oder Pflaster nur im Farbbild.", 149, 189, None)]),
 (100075, "1", False, "Großes Mischsegment: heller Dachstreifen eines Hauses (150-170/140-158), tiefschwarzes Schattenband (140-200/115-165) und Hoffläche (165-195/160-185).",
  [("trennen", "Dach (150-170/140-158) ist hell und scharf begrenzt, Schatten und Hof gehen ohne klare Kante ineinander über; als unklare Mischfläche nicht geteilt.", 160, 150, None),
   ("klasse", "Nur die Elternklasse 1 passt auf die Mischung (165/153).", 165, 153, None)]),
 (100106, "1.1", False, "Hellgraue rechteckige Fläche mit dünner heller Linie (First) und schwarzem Schatten südöstlich (113): eher ein Bau.",
  [("klasse", "Gebäude wahrscheinlich, aber auch Hoffläche möglich (191/180).", 191, 180, None)]),
 (100113, "1", False, "Tiefschwarzer rundlicher Fleck (etwa 6 m) am Südostende von 106: Schlagschatten des Baus 106 oder Baumkrone.",
  [("klasse", "Schatten oder Baum (205/191), Elternklasse der Umgebung (U2).", 205, 191, None)]),
 (100077, "3", False, "Große, fleckig mittelgraue offene Fläche hinter den Gärten mit hellen Trittflecken zwischen Hintausweg 64 und Bau 134.",
  [("klasse", "Krautige offene Fläche statt gepflügter Acker (276/163); Wiese, Ruderalflur oder Brache erst im Farbbild.", 276, 163, None)]),
 (100122, "3", False, "Kleiner Fleck (114 Bildpunkte) am Rand der offenen Fläche 77.",
  [("verschmelzen", "Teil von 77, keine Kante (282/199).", 282, 199, 114)]),
 (100103, "3", False, "Hellere Teilfläche der offenen Fläche 77 an der Viertelgrenze (292-312/156-184).",
  [("verschmelzen", "Schwach heller, aber ohne Kante zu 77 (304/163).", 304, 163, 369)]),
 (100115, "1.1", False, "Heller, scharf begrenzter Quader (etwa 9 × 8 m) mit schwarzem Schatten: kleines Gebäude.",
  [("klasse", "Gebäude, Art offen: 1.1 (304/194).", 304, 194, None)]),
 (100124, "3.4", False, "Nur 18 Bildpunkte im Kern (65/202): Wegrand an der Straße, Rest im Kontextrand.",
  [("klasse", "Wegrand statt Straße (65/202).", 65, 202, 18)]),
 (100136, "1.1", False, "Tiefschwarze Fläche am linken Kernrand: Schattenseite bzw. Schlagschatten eines Hauses, großteils im Kontextrand.",
  [("klasse", "Schatten am Haus (U2): 1.1 (71/232).", 71, 232, None)]),
 (100116, "1.1", False, "Kleines Streckhof-Haus: helle Dachkante südwestlich, schwarze Schattenseite nordöstlich.",
  [("klasse", "Gebäude, Art offen: 1.1 (79/200).", 79, 200, None)]),
 (100147, "6", False, "Heller Fleck (160 Bildpunkte) in der Hoffläche 129 bei 79/246.",
  [("verschmelzen", "Gehört zur Hoffläche 129, keine Kante (79/246).", 79, 246, 160)]),
 (100121, "1.1", False, "Großes, hell gedecktes Gebäude (etwa 27 × 11 m) mit breitem Schlagschatten nordöstlich (120) und südöstlich (132).",
  [("klasse", "Gebäude sicher, Stadel oder Wohnhaus offen: 1.1 (139/225).", 139, 225, None)]),
 (100132, "1", False, "Dunkler Streifen südöstlich des Baus 121: Schlagschatten, darunter Hof oder Boden.",
  [("klasse", "Schatten statt Hauptgebäude (U2), Elternklasse der Umgebung (164/238).", 164, 238, None)]),
 (100120, "1", False, "Tiefschwarzes Parallelogramm nordöstlich von 121 mit gerader Kante: Schlagschatten von 121 oder dunkles Dach.",
  [("klasse", "Schatten oder Dach (177/204), Elternklasse 1.", 177, 204, None)]),
 (100134, "2", False, "Dunkle, fein gesprenkelte quadratische Fläche (etwa 20 × 18 m) mit dunkler Mauer-Schattenlinie innen an der Südwestseite: umfriedetes Beet bzw. Gartenacker.",
  [("klasse", "Gartenacker statt Nebengebäude (273/233); dunkles Dach nicht ganz ausgeschlossen.", 273, 233, None)]),
 (100129, "6", False, "Helle, fleckige Hof- bzw. Bodenfläche südwestlich von 138 mit kleinem hellem Bau (90-100/258-272) und dessen Schatten.",
  [("klasse", "Offene Hoffläche statt Hauptgebäude (80/270).", 80, 270, None),
   ("trennen", "Kleiner heller Bau bei 90-100/258-272 steckt im Segment; Kante nur teilweise scharf, nicht geteilt.", 95, 265, None)]),
 (100138, "2", False, "Dunkle, fein gesprenkelte rechteckige Fläche (etwa 27 × 12 m) südwestlich von 121 mit dünner Mauer-Schattenlinie: umfriedetes Beet bzw. Gartenacker.",
  [("klasse", "Gartenacker statt Nebengebäude (120/252); dunkles Dach nicht ganz ausgeschlossen.", 120, 252, None)]),
 (100114, "3", False, "Große, unruhig fleckige offene Fläche hinter den Höfen bis zum Acker 154 (Anger bzw. Trittrasen) mit hellem Trampelpfad parallel zum Ackerrand.",
  [("klasse", "Offene krautige Fläche statt Baustelle (202/254).", 202, 254, None),
   ("trennen", "Heller Trampelpfad (etwa 60/300 bis 200/255) ohne scharfe Ränder in der Fläche; nicht geteilt.", 150, 275, None)]),
 (100163, "2", False, "Kleiner mittelgrauer Splitter (165 Bildpunkte) am Rand von Acker 154 neben 104.",
  [("verschmelzen", "Grauton und Textur wie Acker 154, keine Kante (306/279).", 306, 279, 165)]),
 (100160, "3", False, "Mittelgraue, fleckige offene Fläche am linken unteren Rand des Viertels (Fortsetzung von 114), zu 49 % in v3.",
  [("klasse", "Offene Fläche statt Hauptgebäude (74/302).", 74, 302, None)]),
 (100171, "3", False, "Kleiner hellerer Fleck (170 Bildpunkte) zwischen 114 und 160.",
  [("verschmelzen", "Teil der offenen Fläche, keine Kante (103/302).", 103, 302, 170)]),
 (100168, "3.4", False, "Dunklerer schmaler Streifen zwischen offener Fläche 114 und Acker 154: Rain mit Bewuchs.",
  [("klasse", "Linearer Rain: 3.4 (190/303).", 190, 303, None)]),
]

ids_d = [d[0] for d in D]
assert len(ids_d) == len(set(ids_d)) == 52, len(ids_d)

kern = np.zeros(lab.shape, bool)
kern[64:564, 64:564] = True


def bilder_fuer(x, y):
    links, oben = x < 189, y < 189
    n = {(True, True): 1, (False, True): 2, (True, False): 3, (False, False): 4}[(links, oben)]
    b = [U("uebersicht_nummern.jpg"), U("uebersicht_roh.jpg")]
    if n == 1:
        b.append(U("nah1_nummern.jpg"))
    b += [U(f"nah{n}_roh.jpg"), E(f"nah_{n}.jpg")]
    if 125 <= x <= 225 and 110 <= y <= 210:
        b += [E("nah_5.jpg"), E("kontrast_1.jpg")]
    return b


segmente, naht = [], []
for sid, vor, sicher, was, punkte in D:
    m = lab == sid
    ys, xs = np.nonzero(m & kern)
    cy, cx = ys.mean(), xs.mean()
    k = np.argmin((ys - cy) ** 2 + (xs - cx) ** 2)
    px, py = int(xs[k]), int(ys[k])
    heute = seg[sid]["klasse"]
    nicht_sauber = bool(punkte) or vor != heute
    segmente.append({
        "id": sid, "klasse_heute": heute, "was_ist_es": was,
        "urteil": "nicht_sauber" if nicht_sauber else "sauber",
        "klasse_vorschlag": vor if vor != heute else None,
        "sicher": sicher,
        "punkte": [{"nr": i + 1, "art": a, "text": t, "flaeche_px": f} for i, (a, t, _x, _y, f) in enumerate(punkte)],
        "bilder": bilder_fuer(px, py),
    })
    aus_o = int((m[:64, :]).sum())
    aus_l = int((m[:, :64]).sum())
    for seite, n in (("oben", aus_o), ("links", aus_l)):
        if n > 0 and int((m & kern).sum()) > 0:
            naht.append({"id": sid, "seite": seite,
                         "text": f"Segment reicht über die Kerngrenze ({n} Bildpunkte im Kontextrand {seite}); Klasse {vor} gilt für das ganze Segment, auch in der Nachbarteilkachel."})

bilder_ang = {
    "uebersicht": [
        "C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png",
        "C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r0c0/ganz_nummern.jpg",
        U("uebersicht_nummern.jpg"), U("uebersicht_roh.jpg"), U("uebersicht_kontrast.jpg"),
    ],
    "nah": [U("nah1_nummern.jpg"), U("nah1_roh.jpg"), U("nah2_roh.jpg"), U("nah3_roh.jpg"), U("nah4_roh.jpg"),
            E("nah_1.jpg"), E("nah_2.jpg"), E("nah_3.jpg"), E("nah_4.jpg"), E("nah_5.jpg"), E("kontrast_1.jpg")],
}

urteil = {
    "teilkachel": "r0c0", "viertel": "v1", "bearbeiter": "urt-c-r0c0-v1",
    "bilder_angesehen": bilder_ang,
    "segmente": segmente,
    "naht": naht,
    "unsicher": [
        "100104 (v2): große Mischfläche mit Bauten, offener Fläche und Schatten östlich von 134/77, vermutlich mehrere Objekte.",
        "100154 (v3/v4): großer Acker; Bewuchs auf Schwarz-Weiß nicht entscheidbar.",
        "100148 (v2): schwarze Fläche an der Viertelgrenze bei 315/250, Schatten oder dunkles Dach.",
    ],
    "nicht_geprueft": [
        "Kontextrand oberhalb y 64 und links von x 64 nur als Umgebung angesehen, nicht geurteilt.",
        "nah2_nummern.jpg, nah3_nummern.jpg, nah4_nummern.jpg, uebersicht_vorschlag.jpg, uebersicht_maengel.jpg und uebersicht_gitter.jpg nicht einzeln angesehen; Grenzen und Nummern stattdessen in eigenen Nahansichten der aktuellen Karte (nah_1 bis nah_5).",
        "Grenzen nicht mit dem Werkzeug kante nachgemessen; Kanten nur nach Augenmaß in den Nahansichten.",
    ],
    "offen": [
        "Höfe und Gärten der Streckhöfe (35, 51, 65, 76, 78): Bewuchs (3) oder Hofboden (6 bzw. 1.2.4); im Farbbild an Grün oder Erdfarbe entscheidbar.",
        "Dunkle umfriedete Flächen 134 und 138: Beet bzw. Gartenacker (2), Wiese (3.1) oder dunkles Dach (1.1); Farbbild oder Schattenlänge entscheidet.",
        "Straße 4: versiegelt (1.2.1) oder Schotter (6.6); Wege 64 und 10 unbefestigt (6.6) oder befestigt (1.2.2); Einfahrt 72; Höfe 105, 129, 147 Erdboden (6) oder Pflaster (1.2.4); Farbbild: Asphaltgrau gegen Erde.",
        "Acker 1 und 90: mit Bewuchs (2.1) oder gepflügt (2.2); Farbbild (grün oder braun).",
        "Gebäude 17, 43, 61, 93, 99, 115, 116, 121, 249, 250: Wohn- (1.1.1) oder Wirtschaftsgebäude (1.1.2); Kataster oder Farbbild (Dachfarbe, Kamine).",
        "Schatten 34, 113, 120, 132, 136: Untergrund nicht sichtbar (U2); 120 und 113 könnten auch dunkles Dach bzw. Baumkrone sein.",
        "75 ist eine Mischfläche aus Dach (150-170/140-158), Schatten und Hof; Teilung erst mit klarer Kante (Farbbild oder anderer Sonnenstand).",
        "48 mischt Schatten und Weg; 129 enthält einen kleinen hellen Bau bei 90-100/258-272; 114 enthält einen Trampelpfad. Nicht geteilt, weil die Kanten unscharf sind.",
        "Offene Flächen 77, 114, 160: Wiese, Ruderalflur oder Brache (alle unter 3); Farbbild bzw. Jahreszeit.",
        "Splitter ohne Kante (80, 90, 91, 103, 122, 147, 163, 171) sind als verschmelzen gemeldet, aber nicht verschmolzen; das Verschmelzen ist ein eigener Schritt.",
    ],
    "eingriffe": [
        {"schritt": "verschmelzen", "vorher": [100047, 100057, 100067, 100074, 100052], "nachher": [100047],
         "grund": "Stücke desselben Krautstreifens zwischen Straße und Acker ohne Bildkante."},
        {"schritt": "verschmelzen", "vorher": [100001, 100058, 100068], "nachher": [100001],
         "grund": "Splitter im Acker mit gleichem Grauton und ohne Bildkante."},
        {"schritt": "verschmelzen", "vorher": [100088, 100098, 100108], "nachher": [100088],
         "grund": "Stücke desselben Grünstreifens östlich der Straße ohne Bildkante."},
        {"schritt": "polygon_zuweisen", "vorher": [100035], "nachher": [100035, 100249],
         "grund": "Heller Bau am Südostende des ummauerten Hofes 35 ist ein eigenes Objekt mit scharfer Kante."},
        {"schritt": "polygon_zuweisen", "vorher": [100076], "nachher": [100076, 100250],
         "grund": "Heller Bau am Südostende des Hofes 76 ist ein eigenes Objekt mit scharfer Kante."},
    ],
}
(ERG / "urteil.json").write_text(json.dumps(urteil, ensure_ascii=False, indent=1), encoding="utf-8")

# ---- Bilder ----
try:
    font = ImageFont.truetype("arial.ttf", 13)
    fontk = ImageFont.truetype("arial.ttf", 11)
except OSError:
    font = fontk = ImageFont.load_default()
sub = img[FY:FY + FW, FX:FX + FW]
base = np.array(Image.fromarray(np.stack([sub] * 3, -1)).resize((FW * FF, FW * FF), Image.BICUBIC))
L = lab[FY:FY + FW, FX:FX + FW]
Lb = np.kron(L, np.ones((FF, FF), dtype=L.dtype))
edge = np.zeros(Lb.shape, bool)
edge[:, 1:] |= Lb[:, 1:] != Lb[:, :-1]
edge[1:, :] |= Lb[1:, :] != Lb[:-1, :]


def rahmen(d):
    a = (64 - FX) * FF
    b = (314 - FX) * FF
    d.rectangle([a, a, b, b], outline=(0, 255, 255), width=2)


def fuss(im, text):
    w, h = im.size
    neu = Image.new("RGB", (w, h + 8 + 17 * len(text)), (255, 255, 255))
    neu.paste(im, (0, 0))
    d = ImageDraw.Draw(neu)
    y = h + 4
    for zeile in text:
        d.text((6, y), zeile, fill=(0, 0, 0), font=font)
        y += 17
    return neu


def mitte(sid):
    m = (L == sid)
    ys, xs = np.nonzero(m)
    if len(xs) == 0:
        return None
    cy, cx = ys.mean(), xs.mean()
    k = np.argmin((ys - cy) ** 2 + (xs - cx) ** 2)
    return xs[k] * FF, ys[k] * FF


# roh
im = Image.fromarray(base.copy()); d = ImageDraw.Draw(im); rahmen(d)
fuss(im, ["H0 r0c0, Viertel v1: Ausschnitt 32-346 (3fach), Viertel cyan umrandet."]).save(ERG / "roh.jpg", quality=90)

# umriss
arr = base.copy(); arr[edge] = (255, 230, 0)
im = Image.fromarray(arr); d = ImageDraw.Draw(im); rahmen(d)
eigene = set(ids_d)
for sid in np.unique(L):
    p = mitte(int(sid))
    if p is None or (L == sid).sum() < 8:
        continue
    farbe = (255, 255, 255) if int(sid) in eigene else (170, 170, 170)
    d.text((p[0] - 8, p[1] - 7), str(int(sid) % 100000), fill=farbe, font=font, stroke_width=2, stroke_fill=(0, 0, 0))
fuss(im, ["Grenzen gelb (Stand nach den Eingriffen), Nummern = ID mod 100000;",
          "weiß = Segment dieses Viertels, grau = Nachbarn/Kontextrand."]).save(ERG / "umriss.jpg", quality=90)

# maengel
arr = base.copy(); arr[edge] = (200, 180, 0)
im = Image.fromarray(arr); d = ImageDraw.Draw(im); rahmen(d)
nr = 0
legende = []
kurz = {"klasse": "Klasse", "grenze": "Grenze", "trennen": "trennen", "verschmelzen": "verschmelzen",
        "fehlt": "fehlt", "zu_klein": "zu klein", "fremdes": "fremdes", "sonstiges": "sonstiges"}
farben = {"klasse": (255, 80, 80), "grenze": (255, 160, 0), "trennen": (255, 0, 255), "verschmelzen": (0, 200, 255),
          "fehlt": (0, 255, 0), "zu_klein": (200, 200, 200)}
for sid, vor, sicher, was, punkte in D:
    for (a, t, x, y, f) in punkte:
        if a == "klasse":
            continue
        nr += 1
        px, py = (x - FX) * FF, (y - FY) * FF
        c = farben.get(a, (255, 255, 255))
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=c, outline=(0, 0, 0))
        d.text((px - 6, py - 7), str(nr), fill=(0, 0, 0), font=fontk)
        legende.append(f"{nr} {sid % 100000} {kurz[a]}")
# Klassenwechsel als kleine rote Punkte
for sid, vor, sicher, was, punkte in D:
    heute = seg[sid]["klasse"]
    if vor != heute:
        p = mitte(sid)
        if p:
            d.rectangle([p[0] - 3, p[1] - 3, p[0] + 3, p[1] + 3], fill=(255, 60, 60))
zeilen = ["Rote Quadrate: Klasse ändern (alle Segmente sicher: nein). Kreise (Nr Segment Art):"]
rest = legende[:]
while rest:
    zeilen.append(", ".join(rest[:6])); rest = rest[6:]
fuss(im, zeilen).save(ERG / "maengel.jpg", quality=90)

# vorschlag
farbe_klasse = {"1": (230, 60, 60), "2": (230, 200, 60), "3": (110, 210, 90), "4": (20, 140, 40),
                "5": (60, 120, 230), "6": (180, 130, 80), "0": (128, 128, 128)}
vk = {}
for s in seg.values():
    vk[s["id"]] = s["klasse"]
for sid, vor, *_ in D:
    vk[sid] = vor
arr = base.copy().astype(np.float32)
for sid in np.unique(L):
    c = farbe_klasse.get(str(vk.get(int(sid), "0"))[0], (128, 128, 128))
    m = np.kron(L == sid, np.ones((FF, FF), bool))
    arr[m] = arr[m] * 0.6 + np.array(c) * 0.4
arr = arr.astype(np.uint8); arr[edge] = (255, 255, 255)
im = Image.fromarray(arr); d = ImageDraw.Draw(im); rahmen(d)
for sid in eigene:
    p = mitte(sid)
    if p:
        d.text((p[0] - 10, p[1] - 7), vk[sid], fill=(255, 255, 255), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
fuss(im, ["Vorschlag: Klasse je Segment dieses Viertels (Code), Farbe nach grober Klasse:",
          "1 rot, 2 gelb, 3 hellgrün, 6 braun; Grenzen weiß = Stand nach den Eingriffen, sonst unverändert."]).save(ERG / "vorschlag.jpg", quality=90)

print("segmente", len(segmente), "nicht_sauber", sum(s["urteil"] == "nicht_sauber" for s in segmente),
      "punkte", sum(len(s["punkte"]) for s in segmente), "sicher_false", sum(not s["sicher"] for s in segmente),
      "naht", len(naht))
