"""Schreibt urteil.json fuer r0c1 v2 (Fassung C) aus den Einzelurteilen unten."""
import json
from pathlib import Path

O = "C:/Users/Phil/Developement/Victor/daten/landseg/H0"
V = f"{O}/viertel/r0c1/v2"
E = f"{O}/c-feste-liste/urteil/r0c1/v2"
UE = f"{V}/uebersicht_nummern.jpg"


def s(id_, heute, was, urteil, vorschlag, sicher, punkte, bilder):
    return {"id": id_, "klasse_heute": heute, "was_ist_es": was, "urteil": urteil,
            "klasse_vorschlag": vorschlag, "sicher": sicher,
            "punkte": [{"nr": i + 1, "art": p[0], "text": p[1], "flaeche_px": p[2]} for i, p in enumerate(punkte)],
            "bilder": [UE] + [b if b.startswith("C:") else f"{E}/{b}" for b in bilder]}


R = f"{V}/uebersicht_roh.jpg"
seg = [
    s(200021, "1.2.1", "Fahrbahnstück am Oberrand, wo Weg 5 auf die Straße 200012 trifft (328/65).",
      "nicht_sauber", "1.2", False,
      [("verschmelzen", "Gleiche Fahrbahn wie 200005 ohne Bildkante (328/65).", 27)], [R, "umriss.jpg"]),
    s(200017, "1.1.1", "Sehr helle Fläche an der Ecke am Oberrand (x 331–364, y 44–77), wohl Dach eines Eckhauses; Kernteil nur 198 px.",
      "sauber", "1.1", False, [], [R, "nah_9.jpg"]),
    s(200018, "1.2.1", "Fünf Bildpunkte der Straße 200012 am Oberrand (421/64).",
      "nicht_sauber", "1.2", False,
      [("zu_klein", "Splitter am Oberrand (421/64) ohne Bildkante zu 200012; zusammenlegen.", 5)], [R]),
    s(200026, "1.2.1", "Dunklere Ausbuchtung am Südwestrand der Straße 200012 (x 420–450, y 83–106): Straßenrand im Schatten der Häuser.",
      "sauber", "1.2", False, [], [R, "nah_9.jpg"]),
    s(200007, "1.1.1", "Höfe, Gärten und Bäume nordöstlich der Straße 200012 (Kernteil x 420–564, y 64–110), fleckig grau und dunkel; die Häuser dazu liegen meist außerhalb des Ausschnitts.",
      "nicht_sauber", "1", False,
      [("klasse", "Kein Hauptgebäude: im Kern fleckige Höfe und Gärten (480/85); Dachkandidaten unregelmäßig, nicht geteilt.", 5318),
       ("trennen", "Oben rechts (555/75) zwei helle Dachkanten, die meist im Kontextrand liegen; nicht geteilt.", 150)],
      [R, "nah_4.jpg"]),
    s(200034, "1.2.1", "Grauer Streifen am Südwestrand der Straße 200012 (x 469–504, y 127–167), Straßenrand im Schatten.",
      "sauber", "1.2", False, [], [R, "nah_3.jpg"]),
    s(200012, "1.2.2", "Hauptstraße von Nordwest (370/25) nach Südost (569/182), 20–25 px (9–11 m) breit, gleichmäßig hell.",
      "nicht_sauber", "1.2", False,
      [("verschmelzen", "Setzt sich ohne Bildkante in 200044 nach Südosten fort (530/185).", 777)], [R, "nah_3.jpg"]),
    s(200030, "1.2.1", "Hellgraue Fläche nordöstlich der Straße 200012 (x 478–552, y 105–136): Vorplatz oder Gehweg vor den Höfen.",
      "sauber", "1.2", False, [], [R, "nah_4.jpg"]),
    s(200029, "1.3.2", "Mittelgraue, fleckige Fläche hinter 200030 (x 492–564 im Kern, y 94–149): Hof oder Garten, keine Erdbewegung.",
      "nicht_sauber", "1", False,
      [("klasse", "Keine Baustelle zu sehen (531/121); Hof oder Garten, im Farbbild prüfen.", 722)], [R, "nah_4.jpg"]),
    s(200016, "1.1.1", "Rest des Riesensegments nach dem Abtrennen von 15 Dächern und der Gasse 200185: Höfe und Gärten zwischen den Streckhöfen, meist im Schlagschatten, dazu nicht abgegrenzte Dachstreifen und der gemischte Bereich östlich der Gasse.",
      "nicht_sauber", "1", False,
      [("trennen", "Zwei Häuserblöcke samt Höfen und Gasse waren ein Segment über vier Viertel; 15 Dächer (200168–200180, 200183, 200184) und die Gasse 200185 abgetrennt (380/150).", 21000),
       ("trennen", "Weitere schmale Dachstreifen (z. B. 405/130, 250/175) und der gemischte Bereich 420–500/200–260 nicht sicher abgrenzbar, nicht geteilt.", 3000),
       ("klasse", "Rest ist Hof oder Garten im Schatten (360/120); nach U2 Elternklasse 1.", None)],
      [R, "nah_5.jpg", "nah_1.jpg", "nah_2.jpg", "nah_9.jpg", f"{O}/c-feste-liste/urteil/r0c1/v1/nah_4.jpg"]),
    s(200046, "1.3.2", "Hellere, rundliche Fläche im Hof (x 465–481, y 178–193), vielleicht kleiner Schuppen oder heller Boden.",
      "nicht_sauber", "1", False,
      [("klasse", "Keine Baustelle (473/185); kleiner Bau oder heller Hofboden, im Farbbild prüfen.", 216)], ["nah_3.jpg"]),
    s(200050, "4.2.4", "Dunkle, unregelmäßige Fläche am Straßenrand (x 482–514, y 181–207), wohl Strauch- oder Baumgruppe mit Schatten.",
      "sauber", "4.2", False, [], ["nah_3.jpg"]),
    s(200036, "1.1.1", "Sehr dunkle, grob strukturierte Fläche östlich der Straße (Kernteil x 532–564, y 129–219), wohl Baumgruppe; reicht weit in den Kontextrand.",
      "nicht_sauber", "4.2", False,
      [("klasse", "Kein Dach zu sehen: tiefdunkel mit grober Textur (553/163), eher Gehölz als Gebäude.", 740)], [R, "nah_3.jpg"]),
    s(200045, "1.3.2", "Dunkler Saum zwischen Straße 200012/200044 und der Baumgruppe 200036 (x 548–563, y 174–200).",
      "nicht_sauber", "1.2", False,
      [("klasse", "Keine Baustelle; Straßenrand im Schatten der Bäume (556/187).", 163)], ["nah_3.jpg"]),
    s(200059, "1.1.1", "Helles rechteckiges Dach nordwestlich der Gasse (x 337–381, y 227–266).",
      "sauber", "1.1", True, [], ["nah_1.jpg", "nah_2.jpg"]),
    s(200055, "1.3.2", "Tiefdunkler rundlicher Fleck (x 511–527, y 210–230), wohl Baumkrone mit Schatten.",
      "nicht_sauber", "4.2", False,
      [("klasse", "Keine Baustelle; runde, sehr dunkle Form (520/220) wie eine Krone.", 241)], ["nah_3.jpg"]),
    s(200044, "1.2.1", "Fortsetzung der Straße 200012 nach Südosten bis zur Querstraße 200051 (x 516–562, y 172–218).",
      "nicht_sauber", "1.2", False,
      [("verschmelzen", "Gleiche Fahrbahn wie 200012 ohne Bildkante (540/195).", 777)], ["nah_3.jpg"]),
    s(200039, "1.3.2", "Gemischte Fläche an der Einmündung (x 486–582, y 159–243): heller Hofboden, Schatten und Randstreifen.",
      "nicht_sauber", "1", False,
      [("klasse", "Keine Baustelle (554/227); Hof und Vorplatz mit Schatten, im Farbbild trennen.", 1907)], ["nah_3.jpg"]),
    s(200058, "1.1.1", "Großes Rechteck mit gleichmäßig dunkelgrauer, fein gestreifter Fläche und gezähntem Rand zur Straße 200051 (x 460–545, y 226–304), wohl Garten- oder Ackerland mit Reihen.",
      "nicht_sauber", "2", False,
      [("klasse", "Kein Dach: keine Lichtseite, keine Schatten, feine Reihen (504/261); eher Gartenland, im Farbbild prüfen.", 2778)],
      ["nah_3.jpg", R]),
    s(200064, "1.2.1", "Dunkler Saum zwischen 200058 und der Straße 200051 (x 510–538, y 252–283), gezähnter Rand oder Graben.",
      "nicht_sauber", "1", False,
      [("klasse", "Zu dunkel für Fahrbahn (532/258); Rand von 200058 oder Graben, im Farbbild prüfen.", 201)], ["nah_3.jpg"]),
    s(200066, "1.2.1", "Hellerer Rand an der Querstraße 200051 am Ostrand (x 542–564, y 261–301).",
      "sauber", "1.2", False, [], ["nah_3.jpg"]),
    s(200070, "1.3.2", "Graues Randstück am Nordwestrand der Querstraße 200051 (x 440–456, y 304–322).",
      "nicht_sauber", "1.2", False,
      [("klasse", "Keine Baustelle; Straßenrand (449/311).", 109)], ["nah_3.jpg"]),
    s(200068, "1.3.2", "Dunkelgraues Stück südöstlich der Querstraße (x 519–544, y 299–317), Hausfront oder Schatten an der Straße.",
      "nicht_sauber", "1", False,
      [("klasse", "Keine Baustelle (538/308); Hausvorplatz oder Schatten, im Farbbild prüfen.", 193)], ["nah_3.jpg"]),
]

neu = [
    (200168, "Dachstreifen am Oberrand, Mitte 348/88.", True),
    (200169, "Kurzer Dachstreifen, Mitte 394/81.", True),
    (200170, "Dachstreifen, Mitte 352/116.", True),
    (200171, "Kurzer Dachstreifen, Mitte 389/103.", True),
    (200172, "Langes Dach mit Querbau am Ende, Mitte 378/173.", False),
    (200173, "Dachstreifen, Mitte 341/161.", True),
    (200174, "Großes, sehr helles Dach (Halle oder Scheune), Mitte 327/186.", True),
    (200175, "Dach eines Streckhofs, Mitte 269/160 (im Viertel v1).", True),
    (200176, "Langes Streckhofdach, Mitte 282/201 (im Viertel v1).", True),
    (200177, "Streckhofdach, Mitte 263/219 (im Viertel v1).", True),
    (200178, "Streckhofdach, Mitte 231/218 (im Viertel v1).", True),
    (200179, "Streckhofdach, Mitte 201/256 (im Viertel v1).", True),
    (200180, "Helle Dachkante der ersten Häuserreihe an der Straße 200049, Mitte 144/244 (im Viertel v1).", False),
    (200183, "Streckhofdach mit hellem Kopfbau an der Straße 200049, Mitte 245/300 (Viertel v1/v3).", False),
    (200184, "Dach südlich der Gasse mit hellem Kopfstück, Mitte 389/313 (Viertel v2/v4).", False),
]
for i, was, sich in neu:
    seg.append(s(i, "1.1", was, "sauber", "1.1", sich, [], ["nah_5.jpg", "nah_9.jpg"]))
seg.append(s(200185, "1.1.1", "Schmale Gasse (8–9 px, rund 4 m) von der Straße 200067 nach Nordosten (330/296 bis 430/216), aus 200016 abgetrennt.",
             "nicht_sauber", "1.2", False,
             [("klasse", "Keine Gebäudefläche: helles, gleich breites Band (387/255); Verkehrsfläche.", 1135),
              ("grenze", "Südostrand bei 360–380/265–280 von Hand gesetzt, das Band geht dort ohne Kante in das Dach 200184 über.", None)],
             ["nah_2.jpg", "nah_9.jpg", "nah_7.jpg"]))

urteil = {
    "teilkachel": "r0c1", "viertel": "v2", "bearbeiter": "urt-c-r0c1-v2",
    "bilder_angesehen": {
        "uebersicht": [f"{O}/H0.png", f"{O}/ganz/H0_raster.jpg", f"{O}/ganz/r0c1/ganz_nummern.jpg",
                       f"{O}/ganz/r0c1/ganz_roh.jpg", UE, R],
        "nah": [f"{E}/{n}" for n in ("nah_5.jpg", "nah_1.jpg", "nah_2.jpg", "nah_6.jpg", "nah_7.jpg", "nah_8.jpg",
                                     "nah_9.jpg", "nah_3.jpg", "nah_4.jpg", "nah_10.jpg")],
    },
    "segmente": seg,
    "naht": [],
    "unsicher": [
        "200056 (v1): nach dem Abtrennen von 200180 zeigt sich, dass 56 der graue Streifen zwischen Straße und Dachkante ist (Gehweg oder Vorgarten), kein Dach; das Urteil in v1 ist entsprechend berichtigt.",
        "200051 (v4): Querstraße, Klasse 1.2.1; gleiche Fahrbahn wie 200066 und 200070.",
        "200067 (v3/v4): Straße, an die die Gasse 200185 anschließt.",
        "Neue Segmente aus dem Stapel tragen in segmente.json kein Feld im_kern; sie liegen alle im Kern.",
    ],
    "nicht_geprueft": [
        "Teile von 200007 und 200036 im Kontextrand (x > 563 bzw. y < 64) nicht geteilt und nicht geurteilt (L2).",
        "Vorbereitete Bilder uebersicht_vorschlag, uebersicht_maengel, uebersicht_kontrast, uebersicht_gitter und nah1_* bis nah4_* nicht einzeln angesehen; stattdessen eigene Nahansichten mit Gitter.",
    ],
    "offen": [
        "Belag aller Verkehrsflächen (200012, 200044, 200021, 200018, 200026, 200030, 200034, 200045, 200066, 200070, Gasse 200185): im Farbbild prüfen; darum nur 1.2.",
        "200016 (Rest), 200007, 200029, 200039, 200046, 200064, 200068: Hof oder Garten, im Farbbild Belag oder Bewuchs prüfen.",
        "200058: Gartenland (Vorschlag 2) oder großes dunkles Dach? Im Farbbild Grün oder Dachdeckung prüfen.",
        "200036, 200050, 200055: Gehölz (Vorschlag 4.2) oder tiefer Schatten? Im Farbbild Kronen prüfen.",
        "Neue Dächer: Haupt- oder Nebengebäude auf dem Scan nicht trennbar, darum 1.1.",
        "Die Dächer 200175–200180, 200183 liegen im Viertel v1 und 200184 reicht nach v4; sie stammen aus 200016 und sind darum hier geurteilt.",
    ],
    "eingriffe": [],
}
ids_neu = [200168, 200169, 200170, 200171, 200172, 200173, 200174, 200175, 200176, 200177, 200178, 200179]
for i in ids_neu:
    urteil["eingriffe"].append({"schritt": "polygon_zuweisen", "vorher": [200016], "nachher": [200016, i],
                                "grund": "Dach (helle Lichtseite und graue Dachfläche über Schwelle) aus dem Riesensegment gelöst."})
urteil["eingriffe"] += [
    {"schritt": "polygon_zuweisen", "vorher": [200016], "nachher": [200016, 200180, 200181, 200182],
     "grund": "Dachkante an der Straße gelöst; dabei fielen zwei Splitter (64 px und 1 px) ab."},
    {"schritt": "polygon_zuweisen", "vorher": [200016], "nachher": [200016, 200183], "grund": "Streckhofdach mit Kopfbau gelöst."},
    {"schritt": "polygon_zuweisen", "vorher": [200016], "nachher": [200016, 200184], "grund": "Dach südlich der Gasse gelöst."},
    {"schritt": "teilen", "vorher": [200016],
     "nachher": [200016, 200185, 200186, 200187, 200188, 200189, 200190, 200191, 200192],
     "grund": "Gasse entlang ihrer beiden Ränder (U-förmiger Linienzug) abgetrennt; dabei fielen Splitter ab."},
    {"schritt": "verschmelzen", "vorher": [200180, 200181, 200182], "nachher": [200180], "grund": "Splitter am Dachrand gehören zur Dachkante."},
    {"schritt": "verschmelzen", "vorher": [200185, 200186, 200187, 200188, 200189, 200190, 200191], "nachher": [200185],
     "grund": "Splitter am Gassenrand gehören zur Gasse."},
    {"schritt": "verschmelzen", "vorher": [200016, 200192], "nachher": [200016], "grund": "Hofstück jenseits der Gasse gehört zum Hof."},
]

Path(f"{E}/urteil.json").write_text(json.dumps(urteil, ensure_ascii=False, indent=1), encoding="utf-8")
print("geschrieben", len(seg))
