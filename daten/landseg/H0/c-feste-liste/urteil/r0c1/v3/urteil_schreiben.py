"""Schreibt urteil.json fuer r0c1 v3 (Fassung C) aus den Einzelurteilen unten."""
import json
from pathlib import Path

O = "C:/Users/Phil/Developement/Victor/daten/landseg/H0"
V = f"{O}/viertel/r0c1/v3"
E = f"{O}/c-feste-liste/urteil/r0c1/v3"
UE = f"{V}/uebersicht_nummern.jpg"
R = f"{V}/uebersicht_roh.jpg"


def s(id_, heute, was, urteil, vorschlag, sicher, punkte, bilder):
    return {"id": id_, "klasse_heute": heute, "was_ist_es": was, "urteil": urteil,
            "klasse_vorschlag": vorschlag, "sicher": sicher,
            "punkte": [{"nr": i + 1, "art": p[0], "text": p[1], "flaeche_px": p[2]} for i, p in enumerate(punkte)],
            "bilder": [UE] + [b if b.startswith("C:") else f"{E}/{b}" for b in bilder]}


seg = [
    s(200054, "0.2", "Tiefdunkles Band zwischen dem Block 200047 und der Straße 200049 (x 74–233, y 210–452): Schlagschatten der straßenseitigen Gebäude auf Vorplatz und Straßenrand.",
      "nicht_sauber", "1", False,
      [("klasse", "Schatten mit erkennbarer Umgebung (176/346): nach U2 nicht 0.2, sondern Elternklasse der Umgebung 1.", 3870)],
      [R, "nah_1.jpg"]),
    s(200073, "1.3.2", "Kleines mittelgraues Stück an der Einmündung der Straße 200067 (x 229–254, y 340–359), Randstreifen zwischen 56, 16 und 67.",
      "nicht_sauber", "1", False,
      [("klasse", "Keine Baustelle (246/348); Randstreifen oder Hofzugang.", 164)], ["nah_3.jpg", "nah_7.jpg"]),
    s(200067, "1.2.1", "Straße von der Straße 200049 nach Osten zur Gasse 200185 und weiter (x 230–361, y 278–374), gleichmäßig hell.",
      "sauber", "1.2", False, [], [R, "nah_3.jpg", "nah_7.jpg"]),
    s(200078, "1.2.1", "Helles, etwa 12–25 px breites Band zwischen Straße 200049 und dem Schatten 200074 (x 234–300, y 365–436), nach dem Eingriff samt dem hellen Streifen aus 74: Dach eines langen Baus oder Platz.",
      "nicht_sauber", "1", False,
      [("grenze", "Heller Streifen bis zur Schattenkante (270/394) lag in 200074; an 78 gegeben.", 772),
       ("klasse", "Dach (Schatten nordöstlich davon) oder heller Platz an der Straße (260/400); auf dem Scan nicht zu trennen.", None)],
      ["nah_3.jpg", "nah_5.jpg", "nah_7.jpg"]),
    s(200074, "1.1.1", "Nach dem Eingriff der tiefdunkle Schlagschatten nordöstlich von 78 (x 260–314, y 350–425) auf Hof oder Garten; das kleine helle Dach 200206 ist abgetrennt.",
      "nicht_sauber", "1", False,
      [("trennen", "Heller Streifen an 78 gegeben und kleines Dach als 200206 abgetrennt (306/385).", 892),
       ("klasse", "Rest ist Schatten (285/385); darunter Hof oder Garten, nach U2 Elternklasse 1.", None)],
      ["nah_5.jpg", "nah_7.jpg"]),
    s(200047, "1.1.1", "Rest des großen Blocks südwestlich der Straße 200049 (x 0–299, y 179–627): lange Parzellen in Ost-West-Richtung mit hellgrauen Dächern, Höfen, dunklen Gärten oder Baumreihen; fünf klar getrennte Dächer abgetrennt.",
      "nicht_sauber", "1", False,
      [("trennen", "Ganzer Block mit Häusern, Höfen und Gärten war ein Segment; fünf Dächer als 200186–200190 abgetrennt (117/315 bis 188/541).", 3667),
       ("trennen", "Heller Gebäudekomplex an der Straße (175/420) und das lange helle Band 70–190/440–460 hängen ohne klare Kante zusammen; nicht geteilt.", 4700),
       ("trennen", "Dunkles Band 60–240/455–505 (140/480): Baumreihe oder Schatten der südlichen Dachreihe; nicht geteilt.", 5000),
       ("klasse", "Rest ist eine Mischung aus Dächern, Höfen und Gärten (143/469); nur Elternklasse 1.", None)],
      [R, "nah_1.jpg", "nah_2.jpg", "nah_8.jpg", "nah_6.jpg"]),
    s(200090, "1.2.1", "Helles Randstück der Straße 200049 an ihrem Westrand (x 227–237, y 447–472).",
      "nicht_sauber", "1.2", False,
      [("verschmelzen", "Gleiche Fahrbahn wie 200049 ohne Kante (232/460).", 114)], ["nah_3.jpg"]),
    s(200096, "1.2.1", "Gemischtes Stück am Westrand der Straße (x 239–256, y 475–498): heller Rand und dunkler Schatten der Häuser.",
      "nicht_sauber", "1", False,
      [("klasse", "Halb Fahrbahn, halb Schatten (247/490); keine reine Straße.", 200)], ["nah_3.jpg"]),
    s(200084, "1.2.1", "Heller Weg am Westrand des Angers zwischen Straße und der dunklen Fläche 200085 (x 242–274, y 431–480).",
      "sauber", "1.2", False, [], ["nah_3.jpg"]),
    s(200085, "1.1.1", "Dunkle, rundliche Fläche auf dem Anger (x 250–277, y 435–466): Baumgruppe oder dunkles Dach.",
      "nicht_sauber", "4.2", False,
      [("klasse", "Keine Lichtseite eines Dachs, rundliche Ränder und grobe Textur (265/450), eher Bäume.", 484)], ["nah_3.jpg"]),
    s(200094, "1.3.2", "Mittelgraue Fläche mit dunklen Flecken auf dem Anger (x 259–295, y 460–489): Rasen mit Baum- oder Strauchschatten.",
      "nicht_sauber", "3", False,
      [("klasse", "Keine Baustelle (275/475); Grünfläche des Angers mit Gehölz, im Farbbild prüfen.", 513)], ["nah_3.jpg"]),
    s(200089, "1.2.1", "Heller Weg am Ostrand der Angerfläche (x 261–297, y 446–493).",
      "sauber", "1.2", False, [], ["nah_3.jpg"]),
    s(200106, "1.2.1", "Hellgraues Stück zwischen der Straße 200081 und dem Block 47 am Westrand (x 61–75, y 514–532), Straßenrand oder Vorplatz.",
      "sauber", "1.2", False, [], ["nah_4.jpg"]),
    s(200099, "1.3.2", "Hellgraues Randstück der Straße am Westrand (x 247–266, y 493–515).",
      "nicht_sauber", "1.2", False,
      [("klasse", "Keine Baustelle; Straßenrand (256/503).", 156)], ["nah_3.jpg"]),
    s(200102, "1.3.2", "Dunkles Stück am Westrand der Straße (x 249–292, y 508–543): Schatten der Häuser von 47.",
      "nicht_sauber", "1", False,
      [("klasse", "Keine Baustelle; Schatten über Straßenrand oder Vorplatz (265/525), nach U2 Elternklasse 1.", 338)], ["nah_3.jpg"]),
    s(200103, "1.2.1", "Helles Fahrbahnstück am Westrand (x 266–285, y 511–533).",
      "nicht_sauber", "1.2", False,
      [("verschmelzen", "Gleiche Fahrbahn wie 200049 ohne Kante (275/522).", 126)], ["nah_3.jpg"]),
    s(200049, "1.2.2", "Hauptstraße von der Einmündung im Norden (100/200) nach Süden mit der Gabelung um den kleinen Anger (Dreieck 240–310/430–560).",
      "sauber", "1.2", False, [], [R, "nah_3.jpg", f"{O}/c-feste-liste/urteil/r0c1/v1/nah_4.jpg"]),
    s(200100, "1.2.1", "Randstück der Straße 200081 am Westrand (Kernteil 53 px, x 64–69, y 501–575), dunkler Saum zum Nachbarn r0c0.",
      "sauber", "1.2", False, [], ["nah_4.jpg"]),
    s(200115, "1.1.1", "Dunkle Fläche im Nachbarn r0c0; ihr Kernteil (21 px bei 65/558) liegt auf der hellen Straße 200081.",
      "nicht_sauber", None, False,
      [("grenze", "Kernteil 21 px (65/558) gehört zur Straße 200081; Klasse des Hauptteils wird in r0c0 geurteilt.", 21)], ["nah_4.jpg"]),
    s(200081, "1.2.2", "Straße am Westrand des Blocks 47 (x 0–137, y 413–627), gleichmäßig hell.",
      "sauber", "1.2", False, [], ["nah_4.jpg", R]),
    s(200126, "1.2.1", "Straßenrand am Unterrand (Kernteil 22 px bei 88/562), südlich davon ein heller Fleck im Nachbarn.",
      "sauber", "1.2", False, [], ["nah_4.jpg"]),
    s(200119, "1.3.2", "Graues Stück zwischen Straße 200081 und Block 47 (x 78–100, y 544–560), Vorplatz oder Hofeinfahrt.",
      "nicht_sauber", "1", False,
      [("klasse", "Keine Baustelle (91/551); Vorplatz oder Hof.", 173)], ["nah_4.jpg"]),
    s(200121, "1.1.1", "Helles Rechteck am Unterrand (x 128–166, y 549–571), Dach.",
      "sauber", "1.1", True, [], ["nah_4.jpg", R]),
    s(200113, "0.2", "Tiefdunkle Fläche am Westrand der südlichen Straßenspitze (x 272–309, y 532–592): Schlagschatten der Häuser auf Hof oder Straßenrand.",
      "nicht_sauber", "1", False,
      [("klasse", "Schatten mit erkennbarer Umgebung (286/552); nach U2 Elternklasse 1 statt 0.2.", 596)], ["nah_3.jpg"]),
    s(200120, "1.2.1", "Südspitze der Straße 200049 am Unterrand (x 300–317, y 546–574).",
      "nicht_sauber", "1.2", False,
      [("verschmelzen", "Gleiche Fahrbahn wie 200049 ohne Kante (311/561).", 76)], ["nah_3.jpg"]),
]
for i, was, sich in [
    (200186, "Dach in der nördlichen Parzelle des Blocks 47, Mitte 117/315.", True),
    (200187, "Langes helles Dach, Mitte 95/357.", True),
    (200188, "Helles Dach mit Anbau, Mitte 167/500.", False),
    (200189, "Langes helles Dach, Mitte 192/517.", True),
    (200190, "Helles Dach, Mitte 188/541.", True),
    (200206, "Kleines helles Dach (Lichtseite) im Schatten 74, Mitte 306/385.", False),
]:
    seg.append(s(i, "1.1", was, "sauber", "1.1", sich, [], ["nah_2.jpg", "nah_6.jpg"] if i != 200206 else ["nah_5.jpg", "nah_7.jpg"]))

urteil = {
    "teilkachel": "r0c1", "viertel": "v3", "bearbeiter": "urt-c-r0c1-v3",
    "bilder_angesehen": {
        "uebersicht": [f"{O}/H0.png", f"{O}/ganz/H0_raster.jpg", f"{O}/ganz/r0c1/ganz_nummern.jpg",
                       f"{O}/ganz/r0c1/ganz_roh.jpg", UE, R],
        "nah": [f"{E}/nah_{i}.jpg" for i in range(1, 9)],
    },
    "segmente": seg,
    "naht": [
        {"id": 200047, "seite": "links", "text": "Block reicht nach r0c0 (bis x 0) und r1c1 (bis y 627); Vorschlag 1 gilt für alle Seiten."},
        {"id": 200047, "seite": "unten", "text": "Siehe links; abgetrennte Dächer liegen alle oberhalb y 563."},
        {"id": 200081, "seite": "links", "text": "Straße über beide Nähte; Klasse 1.2 auf allen Seiten."},
        {"id": 200100, "seite": "links", "text": "Nur 53 px im Kern; Klasse 1.2 wie 200081, in r0c0 gleich setzen."},
        {"id": 200106, "seite": "links", "text": "Reicht bis x 61 in r0c0; Klasse 1.2."},
        {"id": 200115, "seite": "links", "text": "Kernteil von 21 px liegt auf der Straße; die Grenze bei x 64 hat dort keine Bildkante."},
        {"id": 200121, "seite": "unten", "text": "Dach reicht bis y 571 in r1c1; Klasse 1.1 auf beiden Seiten."},
        {"id": 200126, "seite": "unten", "text": "Reicht bis y 578 in r1c1; Klasse 1.2."},
        {"id": 200113, "seite": "unten", "text": "Schatten reicht bis y 592 in r1c1; Vorschlag 1 statt 0.2 auf beiden Seiten."},
        {"id": 200120, "seite": "unten", "text": "Straßenspitze reicht bis y 574 in r1c1; Klasse 1.2."},
    ],
    "unsicher": [
        "200071 (v4): dunkler Block östlich von 74; Grenze 74/71 liegt im Schatten ohne klare Kante.",
        "200056 (v1) und 200054: beide Streifen an der Straße 49; 56 hell, 54 Schatten.",
        "Neue Segmente aus dem Stapel tragen in segmente.json kein Feld im_kern; sie liegen alle im Kern.",
    ],
    "nicht_geprueft": [
        "Teile von 200047, 200081, 200113 im Kontextrand (x < 64 bzw. y > 563) nicht geteilt und nicht geurteilt (L2).",
        "Vorbereitete Bilder uebersicht_vorschlag, uebersicht_maengel, uebersicht_kontrast, uebersicht_gitter und nah1_* bis nah4_* nicht einzeln angesehen; stattdessen eigene Nahansichten mit Gitter.",
    ],
    "offen": [
        "Belag aller Verkehrsflächen (200049, 200067, 200081, 200084, 200089, 200090, 200099, 200100, 200103, 200106, 200120, 200126): im Farbbild prüfen; darum nur 1.2.",
        "200047 (Rest): Dächer, Höfe, Gärten und das dunkle Band (Bäume oder Schatten) im Farbbild trennen.",
        "200078: Dach oder Platz? Im Farbbild Dachdeckung prüfen.",
        "200085 und 200094 auf dem Anger: Bäume und Rasen (Vorschläge 4.2 und 3) im Farbbild prüfen.",
        "200054, 200113, 200074, 200102: Schatten; was darunter liegt, zeigt erst ein Bild mit anderem Sonnenstand oder das Farbbild.",
        "Neue Dächer: Haupt- oder Nebengebäude auf dem Scan nicht trennbar, darum 1.1.",
    ],
    "eingriffe": [
        {"schritt": "polygon_zuweisen", "vorher": [200047], "nachher": [200047, i],
         "grund": "Klar abgegrenztes helles Dach aus dem Block gelöst."} for i in (200186, 200187, 200188, 200189, 200190)
    ] + [
        {"schritt": "polygon_zuweisen", "vorher": [200074], "nachher": [200074, 200191] + list(range(200192, 200206)),
         "grund": "Heller Dachstreifen an der Westseite von 74 abgetrennt; dabei fielen 14 Splitter zwischen ihm und 78 ab."},
        {"schritt": "polygon_zuweisen", "vorher": [200074], "nachher": [200074, 200206, 200207],
         "grund": "Kleines helles Dach im Schatten abgetrennt; dabei fiel ein Splitter von 1 px ab."},
        {"schritt": "verschmelzen", "vorher": [200078, 200191] + list(range(200192, 200206)), "nachher": [200078],
         "grund": "Der helle Streifen und die Splitter bilden mit 78 eine durchgehende helle Fläche bis zur Schattenkante."},
        {"schritt": "verschmelzen", "vorher": [200206, 200207], "nachher": [200206], "grund": "Splitter gehört zum Dach."},
    ],
}

Path(f"{E}/urteil.json").write_text(json.dumps(urteil, ensure_ascii=False, indent=1), encoding="utf-8")
print("geschrieben", len(seg))
