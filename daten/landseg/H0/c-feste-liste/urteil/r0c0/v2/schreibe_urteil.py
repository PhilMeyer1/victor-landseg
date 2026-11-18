"""Writes urteil.json for r0c0/v2 (Fassung C) from the judgments below."""
import json
import numpy as np
import tifffile

B = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/"
E = B + "c-feste-liste/urteil/r0c0/v2/"
V = B + "viertel/r0c0/v2/"
L = tifffile.imread(B + "c-feste-liste/r0c0/labels.tif")
segs = {s["id"]: s for s in json.load(open(B + "c-feste-liste/r0c0/segmente.json", encoding="utf-8"))["segmente"]}
K = np.zeros_like(L, bool)
K[64:564, 64:564] = True

UE = [V + "uebersicht_nummern.jpg", V + "uebersicht_roh.jpg"]
NAH = {
    1: [V + "nah1_roh.jpg", V + "nah1_nummern.jpg", E + "nah_9.jpg"],
    2: [V + "nah2_roh.jpg", E + "nah_10.jpg"],
    3: [V + "nah3_roh.jpg", E + "nah_11.jpg", E + "nah_13.jpg", E + "kontrast_13.jpg"],
    4: [V + "nah4_roh.jpg", E + "nah_12.jpg"],
}


def punkt_in(i):
    m = L == i
    ys, xs = np.nonzero(m & K)
    cy, cx = np.median(ys), np.median(xs)
    k = np.argmin((ys - cy) ** 2 + (xs - cx) ** 2)
    return int(xs[k]), int(ys[k])


def kern(i):
    return int(((L == i) & K).sum())


# id: (vorschlag, sicher, was_ist_es, [(art, text, flaeche|"k"|None)], punkt_xy or None)
# "k" = Kernfläche des Segments
J = [
    (100045, "1.1", True, "Langes Streckhof-Haus am Nordwestrand des Viertels: helle Dachkante im Südwesten, dunkle Dachseite nach Nordosten.",
     [("klasse", "Gebäude klar (Dach mit Firstteilung), Wohn- oder Wirtschaftsteil auf SW nicht zu trennen: 1.1 statt 1.1.1 (339/87).", "k")], (339, 87)),
    (100041, "1", False, "Tiefschwarzes Band zwischen den Häusern 45 und 37: Schlagschatten bzw. schattige Dachseite.",
     [("klasse", "Schatten (U2): ob Dach oder Hof darunter liegt, ist nicht zu sehen; grobe Klasse 1 statt Hauptgebäude (355/71).", "k")], (355, 71)),
    (100037, "1.1", True, "Langes Streckhof-Haus mit hellem Dachstreifen an der Nordostseite und dunkler Dachseite daneben.",
     [("klasse", "Gebäude klar, Haupt- oder Nebengebäude offen: 1.1 (391/88).", "k")], (391, 88)),
    (100028, "1.1", True, "Langes Haus mit hellem Dachstreifen, reicht über die obere Kerngrenze in den Kontextrand.",
     [("klasse", "Gebäude klar, Haupt- oder Nebengebäude offen: 1.1 (437/76).", "k")], (437, 76)),
    (100050, "2", False, "Dunkler Fleck am Nordwestarm der Straße mit gleicher Textur wie die Fläche 12 nördlich davon.",
     [("verschmelzen", "Gehört zu 12 (469/67); nicht verschmolzen, weil 26 Bildpunkte im Kontextrand liegen (L2).", "k"),
      ("klasse", "Gepflügter Acker nicht belegt; wie 12 Acker/Garten auf Ebene 1.", None)], (469, 67)),
    (100012, "2", False, "Dunkel gefleckte Garten- oder Ackerfläche nördlich der Kreuzung, zu rund neun Zehnteln im Kontextrand.",
     [("klasse", "Acker mit Bewuchs (sicher: ja) zu stark: Beet, Acker oder Wiese mit Bäumen auf SW nicht zu trennen; 2 (483/73).", "k")], (483, 73)),
    (100060, "1.2", False, "Hellgraue Fläche nordöstlich der Kreuzung zwischen Straße und Haus 56: Vorplatz oder Einfahrt.",
     [("klasse", "Versiegelung auf SW nicht zu sehen; Verkehrsfläche 1.2 statt Straße (506/97).", "k")], (506, 97)),
    (100049, "2", False, "Dunkler Fleck am Südrand der Fläche 12.",
     [("verschmelzen", "Gehört zu 12 (507/68); nicht verschmolzen, weil 18 Bildpunkte im Kontextrand liegen (L2).", "k"),
      ("klasse", "Gepflügter Acker nicht belegt; wie 12 Ebene 1.", None)], (507, 68)),
    (100020, "1", False, "Nur 7 Bildpunkte im Kern an der oberen Kerngrenze (518/64), sonst dunkle Fläche zwischen Bauten im Kontextrand.",
     [("zu_klein", "Kernanteil 7 Bildpunkte; Baustelle nicht belegt, dunkle Fläche zwischen Bauten: grobe Klasse 1 (518/64).", "k")], (518, 64)),
    (100046, "1", False, "Schmaler mittelgrauer Streifen an der Nordwestseite von Haus 56: Dachrand, Anbau oder Hofstreifen.",
     [("klasse", "Dach oder Hof nicht zu trennen; grobe Klasse 1 statt Hauptgebäude (524/69).", "k")], (524, 69)),
    (100056, "1.1", True, "Langes, hell beleuchtetes Dach eines Hauses nordöstlich der Kreuzung.",
     [("klasse", "Gebäude klar, Haupt- oder Nebengebäude offen: 1.1 (544/90).", "k")], (544, 90)),
    (100042, "1.1", True, "Sehr helles großes Dach an der rechten oberen Kernecke, reicht in den Kontextrand.",
     [("klasse", "Gebäude klar; Nebengebäude der Vorstufe bei dieser Größe nicht belegt: 1.1 (548/72).", "k")], (548, 72)),
    (100073, "1.2", True, "Helle Gasse vom Hintausweg in v1 nach Südosten zur Kreuzung.",
     [("klasse", "Verkehrsfläche klar; versiegelt (1.2.1) oder unbefestigt (6.6) ist auf SW offen: 1.2 (331/121).", "k")], (331, 121)),
    (100089, "1.1", False, "Sehr heller, scharf begrenzter kleiner Körper (etwa 5 × 4 m) am Rand der Gasse 73.",
     [("klasse", "Keine Baustelle; kleiner Schuppen wahrscheinlich, heller Haufen möglich (337/139).", "k")], (337, 139)),
    (100071, "1", False, "Schwarzer Fleck südöstlich von Haus 45: Schlagschatten.",
     [("klasse", "Schatten (U2), darunter Hof 66 oder Dach; grobe Klasse 1 (345/114).", "k")], (345, 114)),
    (100066, "3", False, "Von Mauern und Häusern umfasster, dunkel gefleckter Hof bzw. Garten hinter den Häusern 45 und 37.",
     [("klasse", "Kein Dach (keine Firstteilung, ungleichmäßige Fleckung); Bewuchs vermutet: 3 statt Hauptgebäude (375/119).", "k")], (375, 119)),
    (100253, "1.1", False, "Neu aus 66: schmaler heller Bau (etwa 8 × 2 m, L-förmig) an der Nordostmauer des Hofes, vermutlich Schuppen.",
     [("klasse", "Klasse 1.1 aus dem Eingriff; Nebengebäude vermutet, heller Mauerkopf nicht ganz auszuschließen (393/140).", "k")], (393, 140)),
    (100062, "3", False, "Mittelgraue, fleckige Hof- bzw. Gartenfläche zwischen den Häusern 37/28 und der Straße, mit dunklem Schattenband im Nordosten.",
     [("klasse", "Kein Dach erkennbar; Bewuchs vermutet, Hofbelag möglich: 3 statt Hauptgebäude (424/132).", "k"),
      ("trennen", "Schattenband am Nordostrand (440–470/100–115) nicht abgetrennt, weil seine Kante eine Schattenkante ist.", None)], (424, 132)),
    (100069, "3", False, "Mittelgraue Fläche an der Kreuzung mit dunkler Zaun- oder Heckenlinie und rundem dunklem Fleck (Baum bei 473/112).",
     [("klasse", "Straße (sicher: ja) passt nicht: deutlich dunkler als die Fahrbahn, Zaunlinie; Gartenende oder Rain: 3 (477/113).", "k"),
      ("sonstiges", "Baumkrone bei 473/112 an der Erkennbarkeitsgrenze, nicht abgetrennt.", None)], (477, 113)),
    (100030, "1.2", True, "Helle Straßen der Kreuzung (Arme nach Nordwest, Südwest, Süd und Südost), reicht in den Kontextrand.",
     [("klasse", "Verkehrsfläche klar; befestigt oder Schotter auf SW nicht zu entscheiden: 1.2 statt Weg befestigt (497/119).", "k")], (497, 119)),
    (100079, "1.2", False, "Hellgrauer Streifen zwischen Südostarm der Straße und Haus 63: Vorplatz oder Straßenrand.",
     [("klasse", "Versiegelung nicht belegt; Verkehrsfläche 1.2, Grasrand möglich (530/126).", "k")], (530, 126)),
    (100063, "1", False, "Dunkles Band südwestlich von Haus 56 mit hellerem Teil: Schatten bzw. dunkle Dachseite und Hof.",
     [("klasse", "Mischfläche Schatten/Hof (U2); grobe Klasse 1 statt Hauptgebäude (532/107).", "k")], (532, 107)),
    (100032, "1", False, "Dunkle Fläche (Schatten oder schattige Dachseite) am rechten Kernrand, zu 86 % im Kontextrand.",
     [("klasse", "Schatten (U2), Untergrund nicht zu sehen; grobe Klasse 1 (553/119).", "k")], (553, 119)),
    (100081, "1.1", True, "Helles Dach am rechten Kernrand, überwiegend im Kontextrand.",
     [("klasse", "Gebäude klar, Haupt- oder Nebengebäude offen: 1.1 (556/132).", "k")], (556, 132)),
    (100070, "1.1", True, "Kleines Kernstück (45 Bildpunkte) eines hellen Daches im Kontextrand rechts.",
     [("klasse", "Gebäude klar, Haupt- oder Nebengebäude offen: 1.1 (561/115).", "k")], (561, 115)),
    (100094, "3", False, "Mittelgraue, gleichmäßige Randfläche zwischen Gasse 73 und Haus 100.",
     [("klasse", "Keine Baustelle; Grasrand oder unbefestigter Hof, Bewuchs vermutet: 3 (332/152).", "k")], (332, 152)),
    (100100, "1.1", True, "Haus mit heller Dachkante im Südwesten und schwarzer Schattenseite im Nordosten.",
     [("klasse", "Gebäude klar, Haupt- oder Nebengebäude offen: 1.1 (351/172).", "k")], (351, 172)),
    (100110, "1", False, "Dunkler Streifen östlich von Haus 100 an der Gasse: Schlagschatten.",
     [("klasse", "Schatten (U2); keine Baustelle; grobe Klasse 1 (377/178).", "k")], (377, 178)),
    (100096, "3.4", False, "Mittelgrauer Randstreifen zwischen Südwestarm der Straße und Parzelle 83, mit kleinen dunklen Punkten (Bäumchen oder Büsche).",
     [("klasse", "Keine Fahrbahn (Grau 86 gegen 145 der Straße); Wegrand-Krautsaum 3.4 (453/155).", "k"),
      ("sonstiges", "Dunkle Punkte am Straßenrand an der Erkennbarkeitsgrenze, nicht abgetrennt; Baumreihe 4.2.3 wäre im Farbbild zu prüfen.", None)], (453, 155)),
    (100083, "2", False, "Westliche, dunklere Parzelle der Garten- bzw. Ackerfläche im Straßendreieck.",
     [("klasse", "Acker mit oder ohne Bewuchs bzw. Garten auf SW nicht zu trennen: 2 statt 2.1 (450/200).", "k")], (450, 200)),
    (100251, "2", False, "Neu aus 83: östliche, hellere Parzelle derselben Fläche, mit deutlicher Tonkante zu 83.",
     [("klasse", "Klasse 2.1 aus der Teilung geerbt; Bewuchs auf SW nicht belegt: 2 (509/166).", "k")], (509, 166)),
    (100111, "1", False, "Mischfläche östlich der Parzelle 251: kleine helle Bauteile (bei 540/206 und 524/185) und dunkle Fläche östlich davon.",
     [("klasse", "Hauptgebäude nur für die kleinen hellen Teile belegt; Mischfläche Bau/Schatten/Garten: grobe Klasse 1 (538/198).", "k"),
      ("trennen", "Helle Bauteile und dunkle Fläche sind verschiedene Dinge; nicht geteilt, weil die dunkle Fläche großteils Schatten sein kann.", None)], (538, 198)),
    (100107, "3.4", False, "Mittelgrauer Randstreifen zwischen Südostarm der Straße und 111/251.",
     [("klasse", "Kein Acker; Wegrand-Krautsaum, Ton wie 96 (546/176).", "k")], (546, 176)),
    (100092, "1.2", False, "Hellgrauer Streifen nordöstlich des Südostarms vor den Häusern 81/32, Ton wie der Vorplatz 79.",
     [("klasse", "Keine Fahrbahn (Grau 96 gegen 145); Vorplatz oder befestigter Rand, Grasrand möglich: 1.2 (557/156).", "k")], (557, 156)),
    (100112, "1", False, "Schwarzer Fleck östlich von 111 am Straßenrand: Schlagschatten der Häuser im Osten.",
     [("klasse", "Wolke 0.2 falsch: Schatten mit erkennbarem Werfer (U2); Untergrund Straßenrand oder Hof, grobe Klasse 1 (561/191).", "k")], (561, 191)),
    (100104, "1", False, "Große Hoffläche westlich der Südstraße mit mehreren Bauten; reicht zu 29 % nach v1.",
     [("klasse", "Hof aus Erde/Gras mit Bauten gemischt; grobe Klasse 1 statt Hauptgebäude (360/200).", "k"),
      ("trennen", "Weiterer heller Bau im v1-Teil (290–310/245–270) und dunkler Nordwestteil nicht abgetrennt (anderes Viertel bzw. Schatten).", None)], (360, 200)),
    (100252, "1.1", False, "Neu aus 104: langer, schmaler, hell beleuchteter Bau (etwa 32 × 4 m) mit kurzem Flügel nach Süden am Westende.",
     [("klasse", "Klasse 1.1 aus dem Eingriff; Stadel vermutet, heller Weg nicht ganz auszuschließen (378/218).", "k")], (378, 218)),
    (100137, "1", False, "Schwarzer Streifen am Ostende des Baus 252 am Straßenrand: Schlagschatten.",
     [("klasse", "Schatten (U2); keine Baustelle; grobe Klasse 1 (397/230).", "k")], (397, 230)),
    (100117, "1.2", False, "Mittelgrauer Streifen der Südstraße unterhalb der Kreuzung zwischen hellem Fahrbahnteil 30 und hellem Ostrand von 149.",
     [("klasse", "Straße (versiegelt) nicht belegt; Fahrbahn mit dunklerem Belag oder Mittelstreifen, Grasrand möglich: 1.2 (411/239).", "k"),
      ("verschmelzen", "Liegt ohne klare Bildkante zwischen 30 und 149 (406–420/240–268); nicht verschmolzen, weil offen ist, ob es Fahrbahn oder Rand ist.", None)], (411, 239)),
    (100126, "3.4", False, "Dunkler schmaler Streifen zwischen Straßenrand 117 und Parzelle 83, im Ton wie die Parzelle.",
     [("klasse", "Straße 1.2.1 (sicher: ja) falsch: dunkel (Grau 68); Rain 3.4, Ackerrand von 83 oder Graben möglich (412/213).", "k")], (412, 213)),
    (100145, "4.2", False, "Tiefschwarze, gleichmäßige Fläche (etwa 20 × 20 m) östlich der Südstraße mit gelapptem Nordwestrand.",
     [("klasse", "Wolke 0.2 unpassend: kein Werfer im Südwesten (nur Straße), gelappter Rand spricht für Baumgruppe 4.2; dunkles Dach oder Schatten möglich (439/249).", "k")], (439, 249)),
    (100130, "1.1", False, "Kleiner heller Bau nördlich des Westendes von 127.",
     [("klasse", "Gebäude wahrscheinlich (gerade Kanten), Haupt- oder Nebengebäude offen: 1.1 (472/212).", "k")], (472, 212)),
    (100127, "1.1", True, "Langer hell gedeckter Bau mit Schattenband an der Südseite.",
     [("klasse", "Gebäude klar; Nebengebäude der Vorstufe nicht belegt: 1.1 (497/215).", "k")], (497, 215)),
    (100128, "1", False, "Mischfläche: Schattenband südlich von 127, schmaler Hofstreifen und dunkelgraue Fläche im Osten (530–560/205–245).",
     [("klasse", "Hauptgebäude nicht belegt; Schatten, Hof und dunkle Fläche gemischt: grobe Klasse 1 (538/225).", "k"),
      ("trennen", "Die drei Teile sind verschiedene Dinge; nicht geteilt, weil ihre Kanten Schattenkanten sind.", None)], (538, 225)),
    (100148, "1", False, "Schwarzes Rechteck östlich des hellen Baus bei 290–310/245–270 (Teil von 104 in v1): Schlagschatten oder dunkles Dach.",
     [("klasse", "Schatten (U2) wahrscheinlich, dunkles Dach (1.1) wegen der Rechteckform möglich; grobe Klasse 1 (324/254).", "k")], (324, 254)),
    (100156, "1.1", False, "Helles Rechteck (etwa 18 × 9 m) mit dünnem dunklem Saum an der Südostkante.",
     [("klasse", "Gebäude wahrscheinlich (gerade Kanten), heller Hof möglich; Nebengebäude nicht belegt: 1.1 (331/273).", "k")], (331, 273)),
    (100164, "1", False, "Dunkler Saum an der Südostkante von 156 zum Acker 154.",
     [("klasse", "Schatten oder dunkle Traufseite (U2); grobe Klasse 1, Ackerrand möglich (335/285).", "k")], (335, 285)),
    (100151, "1.1", False, "Kleiner heller Bau mit schwarzem Schatten östlich (in 104).",
     [("klasse", "Gebäude wahrscheinlich, Haupt- oder Nebengebäude offen: 1.1 (345/256).", "k")], (345, 256)),
    (100155, "3", False, "Kleiner mittelgrauer Fleck am Übergang vom Hof 104 zum Acker 154.",
     [("klasse", "Acker mit Bewuchs nicht belegt (heller als 154, ohne Furchen); Rain oder Grasfleck vermutet: 3 (375/259).", "k")], (375, 259)),
    (100150, "3.4", False, "Kleiner mittelgrauer Fleck zwischen Hof 104, Südstraße und Acker 154.",
     [("klasse", "Acker mit Bewuchs nicht belegt; Wegrand-Krautsaum vermutet: 3.4 (404/252).", "k")], (404, 252)),
    (100161, "4.2", False, "Dunkler Fleck westlich der Südstraße, nördliches Glied einer Reihe dunkler Kronen (161, 166, 169).",
     [("klasse", "Baum oder Strauch statt Acker: 4.2 (411/275).", "k")], (411, 275)),
    (100166, "4.2", False, "Dunkler Fleck westlich der Südstraße zwischen 161 und 169, Teil der Kronenreihe.",
     [("klasse", "Baum oder Strauch statt Baustelle: 4.2 (419/287).", "k")], (419, 287)),
    (100149, "1.2", True, "Südstraße von der Kreuzung nach Süden mit hellem Ostrand, zu 43 % in v4.",
     [("klasse", "Verkehrsfläche klar; Versiegelung auf SW offen: 1.2 statt 1.2.1 (428/278).", "k")], (428, 278)),
    (100158, "4.2", False, "Dunkelgrauer Fleck östlich der Südstraße zwischen 145 und 143.",
     [("klasse", "Keine Baustelle; Rand der Baumgruppe 145 oder Schatten: 4.2 (440/269).", "k")], (440, 269)),
    (100142, "1.1", True, "Hell gedeckter Baukomplex: quadratischer Hauptteil (490–530/235–265) und langer Flügel nach Südwesten.",
     [("klasse", "Gebäude klar, Haupt- oder Nebengebäude offen: 1.1 (476/266).", "k"),
      ("trennen", "Hauptteil und Flügel mit leichter Tonkante; nicht geteilt, weil sie ein zusammenhängender Bau sein können.", None)], (476, 266)),
    (100167, "1.1", True, "Langer heller Bau in der südlichen Reihe, reicht knapp nach v4.",
     [("klasse", "Gebäude klar; Nebengebäude der Vorstufe nicht belegt: 1.1 (501/296).", "k")], (501, 296)),
    (100144, "1.1", True, "Langer heller Bau östlich von 142, reicht über die rechte Kerngrenze.",
     [("klasse", "Gebäude klar, Haupt- oder Nebengebäude offen: 1.1 (529/274).", "k")], (529, 274)),
    (100169, "4.2", False, "Schwarzer ovaler Fleck (etwa 6 × 9 m) westlich der Südstraße: Baumkrone mit Schatten, südliches Glied der Kronenreihe.",
     [("klasse", "Gebüsch (4.2.4) gegen Einzelbaum auf SW nicht zu trennen: 4.2 (426/303).", "k")], (426, 303)),
    (100153, "1.1", False, "Heller Bau an der rechten unteren Ecke des Viertels mit dunklem Fleck, reicht nach v4 und in den Kontextrand.",
     [("klasse", "Gebäude wahrscheinlich, Haupt- oder Nebengebäude offen: 1.1 (549/304).", "k")], (549, 304)),
]


def nah_von(x, y):
    if x < 439:
        return 1 if y < 189 else 3
    return 2 if y < 189 else 4


segmente = []
nr = 0
punkte_bild = []
for i, vor, sicher, was, pk, pt in J:
    if pt is None:
        pt = punkt_in(i)
    heute = segs[i]["klasse"]
    pl = []
    for art, text, fl in pk:
        nr += 1
        f = kern(i) if fl == "k" else fl
        pl.append({"nr": nr, "art": art, "text": text, "flaeche_px": f})
        punkte_bild.append({"nr": nr, "id": i, "art": art, "x": pt[0], "y": pt[1]})
    urteil = "nicht_sauber" if pl else "sauber"
    segmente.append({
        "id": i, "klasse_heute": heute, "was_ist_es": was, "urteil": urteil,
        "klasse_vorschlag": vor if vor != heute else None, "sicher": sicher,
        "punkte": pl, "bilder": UE + NAH[nah_von(*pt)],
        "_punkt": list(pt),
    })

eingriffe = [
    {"schritt": "verschmelzen", "vorher": [100030, 100084, 100086, 100109], "nachher": [100030],
     "grund": "Fahrbahnränder 84, 86 und Kreuzungsmitte 109 waren Stücke derselben Straße ohne Bildkante."},
    {"schritt": "verschmelzen", "vorher": [100083, 100087, 100095], "nachher": [100083],
     "grund": "Randsplitter 87 und 95 der Parzelle ohne Bildkante."},
    {"schritt": "verschmelzen", "vorher": [100012, 100053, 100054], "nachher": [100012],
     "grund": "Stücke 53 und 54 derselben Garten- bzw. Ackerfläche ohne Bildkante."},
    {"schritt": "verschmelzen", "vorher": [100066, 100082], "nachher": [100066],
     "grund": "Splitter 82 an der Hofecke ohne Bildkante."},
    {"schritt": "verschmelzen", "vorher": [100145, 100141, 100139], "nachher": [100145],
     "grund": "Dunkle Stücke 141 und 139 derselben schwarzen Fläche ohne Bildkante."},
    {"schritt": "teilen", "vorher": [100083], "nachher": [100083, 100251],
     "grund": "Zwei Parzellen mit deutlicher Tonkante (470/126 bis 502/203), Grenze mit kante eingerastet."},
    {"schritt": "verschmelzen", "vorher": [100251, 100125], "nachher": [100251],
     "grund": "Streifen 125 setzt die hellere Ostparzelle ohne Kante fort."},
    {"schritt": "polygon_zuweisen", "vorher": [100104], "nachher": [100104, 100252],
     "grund": "Langer heller Bau im Hof 104 ist ein eigenes Objekt mit scharfer Kante."},
    {"schritt": "polygon_zuweisen", "vorher": [100066], "nachher": [100066, 100253],
     "grund": "Schmaler heller Bau an der Hofmauer von 66 ist ein eigenes Objekt."},
]

naht = [
    {"id": 100028, "seite": "oben", "text": "Haus 28 reicht über die obere Kerngrenze; Klasse 1.1 gilt auch im Kontextrand (r0c0 hat oben keinen Nachbarn im Ausschnitt)."},
    {"id": 100037, "seite": "oben", "text": "Haus 37 reicht über die obere Kerngrenze; Klasse 1.1 auch im Kontextrand."},
    {"id": 100012, "seite": "oben", "text": "Fläche 12 liegt zu neun Zehnteln oberhalb des Kerns; 50 und 49 gehören dazu, sind aber wegen ihres Kontextanteils nicht verschmolzen."},
    {"id": 100030, "seite": "oben", "text": "Straße 30 läuft mit dem Nordwestarm über die obere Kerngrenze und mit dem Nordostarm zum rechten Rand."},
    {"id": 100042, "seite": "oben", "text": "Helles Dach 42 reicht über die obere und rechte Kerngrenze."},
    {"id": 100032, "seite": "rechts", "text": "Dunkle Fläche 32 liegt zu 86 % rechts außerhalb des Kerns; Klasse 1 gilt für die ganze ID."},
    {"id": 100081, "seite": "rechts", "text": "Dach 81 liegt überwiegend rechts im Kontextrand (Teilkachel r0c1)."},
    {"id": 100111, "seite": "rechts", "text": "Mischfläche 111 reicht über die rechte Kerngrenze; dort mit r0c1 abzustimmen."},
    {"id": 100144, "seite": "rechts", "text": "Bau 144 reicht über die rechte Kerngrenze."},
    {"id": 100153, "seite": "rechts", "text": "Bau 153 reicht über die rechte Kerngrenze und nach v4."},
]

urteil = {
    "teilkachel": "r0c0", "viertel": "v2", "bearbeiter": "urt-c-r0c0-v2",
    "bilder_angesehen": {
        "uebersicht": [
            B + "H0.png",
            B + "ganz/r0c0/ganz_nummern.jpg",
            V + "uebersicht_nummern.jpg",
            V + "uebersicht_roh.jpg",
        ],
        "nah": [
            V + "nah1_roh.jpg", V + "nah1_nummern.jpg", V + "nah2_roh.jpg", V + "nah3_roh.jpg", V + "nah4_roh.jpg",
            E + "nah_9.jpg", E + "nah_10.jpg", E + "nah_11.jpg", E + "nah_12.jpg", E + "nah_13.jpg", E + "kontrast_13.jpg",
        ],
    },
    "segmente": [{k: v for k, v in s.items() if not k.startswith("_")} for s in segmente],
    "naht": naht,
    "unsicher": [
        "100143 (v4): dunkle Bänder und helle Bauteile zwischen 142, 167 und 144 reichen bis 510/284 in v2 hinein; Schattenteile sollten wie 128 die grobe Klasse 1 bekommen.",
        "100104 hat im v1-Teil einen weiteren hellen Bau (290–310/245–270), nicht abgetrennt (anderes Viertel).",
        "100154 (v3/v4): Acker; 155, 150 und 164 liegen an seinem Rand.",
        "100077 und 100114 (v1): Höfe westlich der Gasse 73 mit ähnlichem Ton wie 94; Klasse dort mit 94 abstimmen.",
    ],
    "nicht_geprueft": [
        "Vorbereitete Bilder uebersicht_vorschlag, uebersicht_maengel, uebersicht_kontrast, uebersicht_gitter sowie nah2_nummern, nah3_nummern und nah4_nummern nicht angesehen; statt der Nummernbilder eigene Nahansichten nah_9 bis nah_12 mit dem heutigen Kartenstand.",
        "Bilder nah_1 bis nah_8 und kontrast_1 bis kontrast_8 des ersten Laufs nicht angesehen; sie zeigen den Stand vor dessen Eingriffen.",
    ],
    "offen": [
        "Parzellen 83/251 und Fläche 12 mit 50/49: Beet bzw. Acker (2) oder Wiese (3.1) – Farbbild.",
        "Höfe 62, 66, 94 und Fleck 155: Bewuchs oder unversiegelter Hofbelag – Farbbild.",
        "Straßen 30, 149, 117, Gasse 73, Vorplätze 60, 79, 92: versiegelt (1.2.1) oder Schotter/Erde (6.6); 117 Fahrbahn oder Grasrand – Farbbild.",
        "145 und 158: Baumgruppe, dunkles Dach oder Schatten – Farbbild oder Höhenmodell.",
        "Schatten 41, 63, 71, 110, 112, 128, 137, 148, 164: Untergrund nicht sichtbar (U2); 148 könnte ein dunkles Dach sein.",
        "Bauten 45, 37, 28, 56, 42, 81, 70, 100, 127, 130, 142, 144, 151, 153, 156, 167, 252, 253, 89: Wohn- oder Wirtschaftsgebäude (1.1.1/1.1.2) – Kataster oder Farbbild.",
        "Kronenreihe 161, 166, 169: Einzelbäume, Hecke (4.2.3) oder Gebüsch (4.2.4) – Farbbild.",
    ],
    "eingriffe": eingriffe,
}
with open(E + "urteil.json", "w", encoding="utf-8") as fh:
    json.dump(urteil, fh, ensure_ascii=False, indent=1)
with open("C:/Users/Phil/AppData/Local/Temp/claude/27e54e3b8399faf6/a2bf01d3-627c-4b06-8b57-51f25ab5229e/scratchpad/punkte_bild.json", "w", encoding="utf-8") as fh:
    json.dump({"punkte": punkte_bild, "vorschlag": {s["id"]: (s["klasse_vorschlag"] or s["klasse_heute"]) for s in segmente},
               "punkt": {s["id"]: s["_punkt"] for s in segmente}}, fh, ensure_ascii=False)
ns = sum(1 for s in segmente if s["urteil"] == "nicht_sauber")
sf = sum(1 for s in segmente if not s["sicher"])
print("segmente", len(segmente), "nicht_sauber", ns, "punkte", nr, "sicher_false", sf)
