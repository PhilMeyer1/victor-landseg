"""Schreibt urteil.json fuer r0c1 v4 (Fassung C) aus den Einzelurteilen unten."""
import json
from pathlib import Path

O = "C:/Users/Phil/Developement/Victor/daten/landseg/H0"
V = f"{O}/viertel/r0c1/v4"
E = f"{O}/c-feste-liste/urteil/r0c1/v4"
UE = f"{V}/uebersicht_nummern.jpg"
R = f"{V}/uebersicht_roh.jpg"


def s(id_, heute, was, urteil, vorschlag, sicher, punkte, bilder):
    return {"id": id_, "klasse_heute": heute, "was_ist_es": was, "urteil": urteil,
            "klasse_vorschlag": vorschlag, "sicher": sicher,
            "punkte": [{"nr": i + 1, "art": p[0], "text": p[1], "flaeche_px": p[2]} for i, p in enumerate(punkte)],
            "bilder": [UE] + [b if b.startswith("C:") else f"{E}/{b}" for b in bilder]}


seg = [
    s(200069, "1.2.1", "Helle Fläche am Südostrand der Querstraße 200051 (x 476–531, y 301–339), Vorplatz vor dem hellen Bau 200210.",
      "sauber", "1.2", False, [], [R, "nah_2.jpg"]),
    s(200071, "1.1.1", "Dunkler Block nordwestlich der Querstraße (x 289–386, y 318–438): dunkle Dächer, Höfe und Gärten ohne klare Lichtkanten.",
      "nicht_sauber", "1", False,
      [("klasse", "Kein einzelnes Hauptgebäude erkennbar (339/379); Mischung aus dunklen Dächern und Höfen, nicht geteilt.", 5459)],
      [R, "nah_2.jpg"]),
    s(200051, "1.2.1", "Querstraße von Südwest (311/455) nach Nordost (627/186), 18–22 px breit, gleichmäßig hell.",
      "sauber", "1.2", False, [], [R, "nah_2.jpg"]),
    s(200079, "1.2.1", "Mittelgrauer Streifen am Südostrand der Querstraße vor den Häusern (x 401–447, y 376–414), Gehweg oder Vorplatz im Halbschatten.",
      "sauber", "1.2", False, [], ["nah_2.jpg"]),
    s(200076, "1.2.1", "Kleines helles Randstück der Querstraße (x 444–464, y 359–383).",
      "nicht_sauber", "1.2", False,
      [("verschmelzen", "Ohne Bildkante zu 200051 (452/366).", 221)], ["nah_2.jpg"]),
    s(200077, "1.3.2", "Helles Stück am Kopf des Dachs 200215 an der Straße (x 444–462, y 373–396): Dachende oder Vorplatz.",
      "nicht_sauber", "1", False,
      [("klasse", "Keine Baustelle (454/385); Dachkopf oder Vorplatz, nicht zu trennen.", 199)], ["nah_2.jpg"]),
    s(200075, "1.3.2", "Dunkleres Stück am Straßenrand (x 457–470, y 354–373), Schatten.",
      "nicht_sauber", "1", False,
      [("klasse", "Keine Baustelle (463/362); Schatten am Straßenrand.", 91)], ["nah_2.jpg"]),
    s(200082, "1.2.1", "Fahrbahn an der Einmündung der Querstraße in die Straße 200049 (x 298–349, y 417–450), teils im Schatten.",
      "sauber", "1.2", False, [], ["nah_2.jpg", f"{O}/c-feste-liste/urteil/r0c1/v3/nah_3.jpg"]),
    s(200083, "1.2.1", "Dunklerer Straßenrand vor dem Block 63 (x 363–385, y 419–439).",
      "sauber", "1.2", False, [], ["nah_2.jpg"]),
    s(200080, "1.3.2", "Dunkles Stück am Straßenrand (x 383–398, y 412–427), Schatten am Kopf eines Dachs.",
      "nicht_sauber", "1", False,
      [("klasse", "Keine Baustelle (390/419); Schatten.", 112)], ["nah_2.jpg"]),
    s(200098, "1.2.1", "Helles Stück zwischen Straße 200049 und der Angerfläche 200097 (x 309–324, y 483–508).",
      "sauber", "1.2", False, [], ["nah_4.jpg"]),
    s(200095, "1.2.1", "Straße, die vom Anger nach Südosten am Block 63 entlang läuft (x 311–436, y 463–591).",
      "sauber", "1.2", False, [], ["nah_4.jpg", R]),
    s(200091, "1.3.2", "Mittelgraues Zwickelstück zwischen den Straßen 49, 51 und 95 (x 332–348, y 448–476).",
      "nicht_sauber", "1.2", False,
      [("klasse", "Keine Baustelle (341/463); Straßenrand im Zwickel.", 127)], ["nah_2.jpg"]),
    s(200063, "1.1.1", "Rest des großen Blocks südöstlich der Querstraße nach dem Abtrennen von elf Dächern: Höfe und Gärten zwischen den Streckhöfen, meist im Schatten, dazu nicht abgegrenzte graue Dachstreifen und der Westteil am Straßenbogen 95.",
      "nicht_sauber", "1", False,
      [("trennen", "Häuserzeilen samt Höfen waren ein Segment; elf Dächer als 200207–200219 abgetrennt (500/420).", 9640),
       ("trennen", "Weitere graue Dachstreifen (z. B. 405/460, 470/440) und der Westteil 330–400/450–560 mit hellem Bau nicht sicher abgrenzbar, nicht geteilt.", 6000),
       ("klasse", "Rest ist Hof oder Garten im Schatten (471/462); nach U2 Elternklasse 1.", None)],
      [R, "nah_1.jpg", "nah_3.jpg", "nah_2.jpg"]),
    s(200097, "1.1.1", "Graue Dreiecksfläche zwischen Straße 200049 und Straße 200095 (Kernteil x 305–431, y 482–563), mit heller rechteckiger Umrandung: östlicher Teil des Angers, Rasen oder Platz mit kleinem Bau.",
      "nicht_sauber", "1", False,
      [("klasse", "Kein Hauptgebäude über die ganze Fläche (333/527); Rasen, Platz und vielleicht ein kleiner Bau, im Farbbild trennen.", 3049)],
      ["nah_4.jpg", R]),
    s(200116, "1.3.2", "Helles Stückchen zwischen 97 und 109 (x 344–355, y 540–550), Wegrand.",
      "nicht_sauber", "1.2", False,
      [("klasse", "Keine Baustelle (348/546); heller Wegrand.", 86)], ["nah_4.jpg"]),
    s(200109, "1.2.1", "Helles Randstück zwischen Straße 95 und Angerfläche 97 (x 351–369, y 523–542).",
      "sauber", "1.2", False, [], ["nah_4.jpg"]),
    s(200114, "1.3.2", "Tiefdunkler Fleck (x 455–477, y 533–554), Schlagschatten zwischen den Häusern.",
      "nicht_sauber", "1", False,
      [("klasse", "Keine Baustelle (465/542); Schatten, nach U2 Elternklasse 1.", 239)], ["nah_4.jpg"]),
    s(200108, "1.1.1", "Hellgraue Fläche an der Straße 110 (x 496–525, y 517–565) mit dunkler Kerbe, wohl Dach eines Vorderhauses.",
      "sauber", "1.1", False, [], ["nah_4.jpg"]),
    s(200105, "1.1.1", "Gemischtes Stück (x 513–553, y 513–544): Ende einer hellen Dachkante und dunkler Schatten daneben.",
      "nicht_sauber", "1", False,
      [("trennen", "Helle Dachkante (545/525) und Schatten (525/530) in einem Segment; klein, nicht geteilt.", 728)], ["nah_4.jpg"]),
    s(200107, "1.1.1", "Ende einer sehr hellen Dachkante am Ostrand (x 544–564, y 516–542) mit Schatten.",
      "sauber", "1.1", False, [], ["nah_4.jpg"]),
    s(200122, "1.3.2", "Graues Stück an der Südwestecke (x 312–329, y 552–574) zwischen Straßenspitze 120 und Angerfläche 97.",
      "nicht_sauber", "1", False,
      [("klasse", "Keine Baustelle (322/560); Straßenrand oder Rasen.", 95)], ["nah_4.jpg"]),
    s(200112, "1.1.1", "Mittelgraue Fläche am Unterrand (x 419–473, y 531–582) vor den Dachenden: Vorplatz oder flaches Vorderhaus.",
      "nicht_sauber", "1", False,
      [("klasse", "Keine klare Dachform (443/554); Vorplatz oder Bau, im Farbbild prüfen.", 647)], ["nah_4.jpg"]),
    s(200111, "1.1.1", "Helle Fläche an der Straße 110 (x 468–502, y 529–571), Dach eines Vorderhauses.",
      "sauber", "1.1", False, [], ["nah_4.jpg"]),
    s(200124, "1.3.2", "Dunkelgrauer Streifen am Unterrand vor 111/108 (x 467–522, y 557–584), Schatten oder Straßenrand.",
      "nicht_sauber", "1", False,
      [("klasse", "Keine Baustelle (518/560); Schatten der Vorderhäuser auf dem Straßenrand.", 74)], ["nah_4.jpg"]),
    s(200123, "1.3.2", "Dunkles Stückchen zwischen 108 und Straße 110 (x 529–542, y 552–566), Schatten.",
      "nicht_sauber", "1", False,
      [("klasse", "Keine Baustelle (535/556); Schatten.", 94)], ["nah_4.jpg"]),
    s(200110, "1.2.1", "Straße am Unterrand (Kernteil x 425–564, y 524–563), läuft in r1c1 weiter.",
      "sauber", "1.2", False, [], ["nah_4.jpg"]),
    s(200125, "1.3.2", "Zwei Bildpunkte in der Südostecke (562/563) eines dunklen Stücks im Nachbarn r1c1.",
      "nicht_sauber", "1", False,
      [("zu_klein", "2 px im Kern (562/563); Klasse des Hauptteils in r1c1 urteilen.", 2)], ["nah_4.jpg"]),
]
for i, was, sich in [
    (200207, "Dachstreifen am Ostrand, Mitte 553/326.", True),
    (200208, "Kurzer Dachstreifen, Mitte 507/336.", True),
    (200209, "Dachstreifen, Mitte 547/354.", True),
    (200210, "Heller rechteckiger Bau an der Querstraße, Mitte 483/345.", True),
    (200212, "Langes Dach, Mitte 540/382.", True),
    (200213, "Langes Streckhofdach, Mitte 533/424.", True),
    (200214, "Langes Streckhofdach, Mitte 519/448.", True),
    (200215, "Sehr helle lange Dachkante, Mitte 489/443.", True),
    (200217, "Streckhofdach, Mitte 455/436.", True),
    (200218, "Streckhofdach mit Anbau am Ende, Mitte 457/491.", False),
    (200219, "Lange, sehr helle Dachkante bis zur Straße, Mitte 415/486.", True),
]:
    seg.append(s(i, "1.1", was, "sauber", "1.1", sich, [], ["nah_1.jpg", "nah_2.jpg"]))

urteil = {
    "teilkachel": "r0c1", "viertel": "v4", "bearbeiter": "urt-c-r0c1-v4",
    "bilder_angesehen": {
        "uebersicht": [f"{O}/H0.png", f"{O}/ganz/H0_raster.jpg", f"{O}/ganz/r0c1/ganz_nummern.jpg",
                       f"{O}/ganz/r0c1/ganz_roh.jpg", UE, R],
        "nah": [f"{E}/nah_{i}.jpg" for i in range(1, 5)],
    },
    "segmente": seg,
    "naht": [
        {"id": 200063, "seite": "unten", "text": "Rest reicht bis y 566 in r1c1; Vorschlag 1 auf beiden Seiten."},
        {"id": 200097, "seite": "unten", "text": "Angerfläche reicht bis y 627 in r1c1; Vorschlag 1 auf beiden Seiten."},
        {"id": 200110, "seite": "unten", "text": "Straße läuft in r1c1 weiter; Klasse 1.2."},
        {"id": 200112, "seite": "unten", "text": "Reicht bis y 582; Vorschlag 1 auf beiden Seiten."},
        {"id": 200111, "seite": "unten", "text": "Reicht bis y 571; Klasse 1.1."},
        {"id": 200124, "seite": "unten", "text": "Reicht bis y 584; Vorschlag 1."},
        {"id": 200122, "seite": "unten", "text": "Reicht bis y 574; Vorschlag 1."},
        {"id": 200125, "seite": "unten", "text": "Nur 2 px im Kern; Klasse des Hauptteils in r1c1."},
        {"id": 200095, "seite": "unten", "text": "Straße reicht bis y 591; Klasse 1.2."},
    ],
    "unsicher": [
        "200049 (v3): Straße am Westrand, an die 82, 91 und 98 grenzen.",
        "200016 (v2): sein Teil nördlich der Querstraße (x 330–470, y 300–330) ist Hof; das Dach 200184 reicht in dieses Viertel.",
        "Neue Segmente aus dem Stapel tragen in segmente.json kein Feld im_kern; sie liegen alle im Kern.",
    ],
    "nicht_geprueft": [
        "Teile von 200063 im Kontextrand (x > 563) und im Viertel v2 (y < 300) nicht geteilt.",
        "Vorbereitete Bilder uebersicht_vorschlag, uebersicht_maengel, uebersicht_kontrast, uebersicht_gitter und nah1_* bis nah4_* nicht einzeln angesehen; stattdessen eigene Nahansichten mit Gitter.",
    ],
    "offen": [
        "Belag aller Verkehrsflächen (200051, 200069, 200076, 200079, 200082, 200083, 200091, 200095, 200098, 200109, 200110, 200116): im Farbbild prüfen; darum nur 1.2.",
        "200063 (Rest) und 200071: Höfe, Gärten und dunkle Dächer im Farbbild trennen.",
        "200097: Rasen, Platz oder kleiner Bau auf dem Anger? Im Farbbild prüfen.",
        "200112, 200077: Vorplatz oder Bau? Im Farbbild prüfen.",
        "200114, 200124, 200123, 200075, 200080: Schatten; was darunter liegt, zeigt erst das Farbbild.",
        "Neue Dächer: Haupt- oder Nebengebäude auf dem Scan nicht trennbar, darum 1.1.",
    ],
    "eingriffe": [],
}
schritte = [(200207, []), (200208, []), (200209, []), (200210, [200211]), (200212, []), (200213, []), (200214, []),
            (200215, [200216]), (200217, []), (200218, []), (200219, [200220])]
for i, frag in schritte:
    urteil["eingriffe"].append({"schritt": "polygon_zuweisen", "vorher": [200063], "nachher": [200063, i] + frag,
                                "grund": "Dach (helle Lichtseite über Schwelle) aus dem Häuserblock gelöst"
                                + ("; ein Splitter fiel ab." if frag else ".")})
for i, frag in schritte:
    if frag:
        urteil["eingriffe"].append({"schritt": "verschmelzen", "vorher": [i] + frag, "nachher": [i],
                                    "grund": "Splitter am Dachrand gehört zum Dach."})

Path(f"{E}/urteil.json").write_text(json.dumps(urteil, ensure_ascii=False, indent=1), encoding="utf-8")
print("geschrieben", len(seg))
