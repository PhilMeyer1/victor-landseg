"""Schreibt urteil.json der Nachhol-Gegenprobe v2 (r0c0, Fassung C) neu aus der Tabelle unten."""
import json
import numpy as np
import tifffile

B = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/"
O = B + "c-feste-liste/urteil-gegenprobe/r0c0/v2/"
VB = B + "viertel/r0c0/v2/"
lab = tifffile.imread(B + "c-feste-liste/gegenprobe/r0c0/labels.tif")
seg = {s["id"]: s for s in json.load(open(B + "c-feste-liste/gegenprobe/r0c0/segmente.json", encoding="utf-8"))["segmente"]}

# id: (Punkt x, y, Vorschlag oder None, sicher, was_ist_es, [(art, text, flaeche)])
T = [
 (100045, 339, 87, "1.1", False, "Dunkles Band neben dem hellen Dachstreifen 100261: Schattenseite des Satteldachs eines Streckhofs oder Schlagschatten im Hof.", [("klasse", "Dunkles Band (339/87) ist kein sicher erkennbares Hauptgebäude; Dachhälfte im Schatten oder Hofschatten, darum Elternklasse 1.1.", None)]),
 (100041, 355, 71, "1.1", False, "Dunkles Band zwischen den Dachstreifen 100045 und 100037, vermutlich beschattete Dachhälfte.", [("klasse", "Dunkles Band (355/71): Dach im Schatten oder Hofschatten, Feinklasse nicht erkennbar.", None)]),
 (100037, 391, 88, "1.1", False, "Rest nach der Teilung: dunkles bis mittleres Band westlich des hellen Dachstreifens 100262.", [("klasse", "Mittelgraues bis dunkles Band (391/88), Dach im Schatten oder Hof; nur 1.1 vertretbar.", None)]),
 (100028, 437, 76, "1.1", False, "Heller Dachstreifen samt dunklem Schattenband einer Häuserzeile am Nordrand des Viertels.", [("trennen", "Heller Dachstreifen (um 440/70) und dunkles Band nordöstlich davon (um 455/80) stecken in einem Segment; Teilung wäre wie bei 100037 möglich.", None), ("klasse", "Hauptgebäude oder Stadel nicht unterscheidbar (437/76), darum 1.1.", None)]),
 (100050, 469, 67, "2.1", False, "Kleines mittelgraues Stück Garten zwischen dem Straßenarm nach Nordwesten und dem Garten 100012.", [("verschmelzen", "Kein Bildumschlag zum Garten 100012 (469/67); gehört zu dieser Fläche.", 119), ("klasse", "Kein gepflügter Acker, sondern Garten wie 100012.", None)]),
 (100012, 483, 73, None, False, "Gartenfläche mit fleckiger mittelgrauer Textur nördlich der Kreuzung, Großteil im Kontextrand.", []),
 (100060, 506, 97, "1.2", False, "Hellere Fläche nordöstlich der Kreuzung (506/97): Vorplatz, Hof oder kurzer Straßenarm.", [("klasse", "Straße, Platz oder Hof an der Kreuzung (506/97) auf Schwarz-Weiß nicht sicher getrennt; Elternklasse 1.2.", None)]),
 (100049, 507, 68, "2.1", False, "Dunkler gleichmäßiger Fleck am Garten 100012: Schlagschatten der Häuser im Norden auf dem Garten.", [("klasse", "Schatten auf dem Garten (507/68) bekommt nach U2 die Klasse der Fortsetzung 100012, nicht gepflügter Acker.", None), ("verschmelzen", "Schattengrenze ist keine Objektgrenze; mit 100012 zusammenlegen.", 141)]),
 (100020, 518, 64, "1", False, "Winziger Rest (7 Bildpunkte im Kern) eines Schattens neben dem hellen Dach 100042, sonst im Kontextrand.", [("zu_klein", "Nur 7 Bildpunkte im Kern an der Oberkante (518/64); keine Baustelle, Schatten an Gebäuden.", 7)]),
 (100046, 524, 69, "1.1", False, "Mittelgrauer Streifen parallel zum hellen Dach 100275, vermutlich andere Dachhälfte oder Anbau.", [("klasse", "Streifen (524/69) wirkt wie Dachfläche, Feinklasse nicht entscheidbar.", None)]),
 (100056, 555, 96, "1.1", False, "Dunkles Band nordöstlich des hellen Dachstreifens 100275: beschattete Dachhälfte oder Schatten im Hof.", [("klasse", "Dunkles Band (555/96), Dach im Schatten oder Hof; Elternklasse 1.1.", None)]),
 (100042, 548, 72, "1.1", False, "Sehr helles großes Dach in der Nordostecke, zum Teil im Kontextrand.", [("klasse", "Großes helles Dach (548/72): Nebengebäude oder Hauptgebäude nicht entscheidbar, darum 1.1.", None)]),
 (100073, 331, 121, "1.2", False, "Helle Dorfstraße am Rand des Angers von Nordwesten zur Kreuzung (331/121).", [("klasse", "Linienförmige helle Fahrbahn (331/121); ob befestigt oder Erdweg (6.6), zeigt der Scan nicht sicher.", None)]),
 (100089, 337, 139, "1.1", False, "Sehr heller ovaler Fleck am Straßenrand (337/139): kleines Gebäude, Fahrzeug oder heller Haufen.", [("klasse", "Heller Fleck (337/139) ist keine Baustelle; am ehesten kleiner Bau.", None)]),
 (100071, 345, 114, "1.1", False, "Dunkler Rest am Südostende des Bandes 100045 an der Straße: Schatten am Gebäudeende.", [("klasse", "Dunkle Stelle (345/114) als Schatten am Haus, Fortsetzung des Dachbandes.", None)]),
 (100082, 356, 136, "1", False, "Kleiner dunkler Fleck zwischen Straße 100073 und Innenhof 100066: Schatten am Straßenrand.", [("klasse", "Dunkler Fleck (356/136), Schatten auf Straße oder Hof; keine Baustelle.", None)]),
 (100066, 375, 119, "3.1", False, "Dunkler fleckiger Innenhof bzw. Garten zwischen den Häuserzeilen, nach Abtrennen des hellen Baus 100277.", [("klasse", "Fläche (375/119) ist kein Dach, sondern Garten mit Rasen, Beeten oder Sträuchern; 3.1 als wahrscheinlichste Bedeckung.", None)]),
 (100062, 424, 132, "3.1", False, "Mittelgraue Garten- oder Hoffläche hinter den Häusern an der Straße nach Südwesten.", [("klasse", "Gleichmäßige mittelgraue Fläche (424/132) ohne Dachkanten; Garten oder unbefestigter Hof, nicht Hauptgebäude.", None), ("grenze", "Schmaler dunkler Streifen entlang der Straße (um 450/130) steckt mit drin; Gehölz oder Schatten, Grenze ungenau.", None)]),
 (100069, 477, 113, "3.4", False, "Graues Zwickelstück zwischen den Straßenarmen nach Nordwesten und Südwesten (477/113).", [("klasse", "Dunkler als die Fahrbahn (477/113), eher Rasenstreifen am Straßenrand als Straße.", None)]),
 (100030, 497, 119, "1.2", False, "Straßenkreuzung mit den Armen nach Nordwesten, Südwesten und Südosten, nach dem Zusammenlegen der Straßenstücke.", [("klasse", "Fahrbahn (497/119); befestigt oder Schotter und Straße oder Weg auf dem Scan nicht sicher, darum 1.2.", None)]),
 (100079, 530, 126, "3.4", False, "Schmaler grauer Streifen am Nordostrand des Straßenarms nach Südosten.", [("klasse", "Streifen (530/126) dunkler als die Fahrbahn: Rasenstreifen oder Gehsteig.", None)]),
 (100063, 532, 107, "1", False, "Fleckige mittelgraue Hoffläche zwischen Platz 100060 und dem Schattenband 100056.", [("klasse", "Hof oder Garten zwischen Gebäuden (532/107), kein Dach erkennbar; Elternklasse 1 vorbehaltlich Farbbild.", None)]),
 (100032, 553, 119, "1.1", False, "Dach- und Schattenstreifen am Ostrand, großteils im Kontextrand.", [("klasse", "Dachstreifen (553/119), Feinklasse nicht entscheidbar.", None)]),
 (100081, 556, 132, "1.1", False, "Heller Dachstreifen mit Schatten am Ostrand des Kerns.", [("klasse", "Dach (556/132), Hauptgebäude oder Stadel nicht entscheidbar.", None)]),
 (100070, 561, 115, "1.1", False, "Kleiner Rest eines Dachstreifens am Ostrand (45 Bildpunkte im Kern).", [("klasse", "Dachrest (561/115), Feinklasse nicht entscheidbar.", None)]),
 (100094, 332, 152, "3.1", False, "Gleichmäßig mittelgraue Rasenfläche, Fortsetzung des Angers 100077 aus v1.", [("klasse", "Rasen am Anger (332/152), keine Baustelle.", None)]),
 (100100, 351, 172, "1.1", False, "Dunkle rechteckige Fläche neben dem hellen Bau 100279: Dach im Schatten oder dunkles Dach.", [("klasse", "Dunkle Fläche mit geraden Kanten (351/172), Dach oder Schatten am Haus; 1.1.", None)]),
 (100110, 377, 178, "1", False, "Kleiner dunkler Streifen zwischen 100100 und der Straße: Schatten.", [("klasse", "Schatten (377/178) zwischen Haus und Straße; keine Baustelle.", None)]),
 (100096, 453, 155, "3.4", False, "Grüner Randstreifen mit dunklen Flecken (Sträucher) zwischen Straße und Feld 100083.", [("klasse", "Linienförmiger Streifen (453/155) dunkler als die Fahrbahn, mit Sträuchern; Wegrand, nicht Straße.", None)]),
 (100125, 505, 199, "3.4", False, "Hellerer Streifen zwischen Feld 100083 und Dach 100127.", [("klasse", "Schmaler Rand (505/199) zwischen Feld und Gebäude, kein Acker.", None)]),
 (100083, 509, 166, None, False, "Große gleichmäßige Feld- oder Gartenfläche im Häuserblock südöstlich der Kreuzung.", []),
 (100111, 538, 198, "1", False, "Hof mit kleinen hellen Objekten östlich des Dachs 100127.", [("klasse", "Mischfläche aus Hof und kleinen hellen Bauten (538/198), kein einzelnes Hauptgebäude.", None), ("trennen", "Heller kleiner Bau bei 540/183 wäre als eigenes Segment abtrennbar.", None)]),
 (100107, 546, 176, "3.4", False, "Grauer Streifen zwischen Feld 100083 und dem Straßenarm nach Südosten.", [("klasse", "Randstreifen (546/176), kein Acker.", None)]),
 (100092, 557, 156, "3.4", False, "Grauer Streifen am Ostrand des Straßenarms nach Südosten, reicht in den Kontextrand.", [("klasse", "Dunkler als die Fahrbahn (557/156), eher Rand oder Gehsteig.", None)]),
 (100112, 561, 191, "4.2", False, "Kleiner sehr dunkler kompakter Fleck am Ostrand: Baumkrone oder Schatten.", [("klasse", "Nach U2 nicht 0.2, solange eine Krone denkbar ist (561/191).", None)]),
 (100104, 333, 213, "1", False, "Großer Hof mit Bauten, Schatten und Freiflächen westlich der Straße nach Süden, nach Abtrennen von 100280 und 100281.", [("klasse", "Mischfläche Hof (333/213), kein einzelnes Hauptgebäude; Elternklasse 1.", None), ("trennen", "Weiterer heller Bau nördlich parallel zu 100280 (um 330/210) und dunkler Schatten bei 385/195 stecken noch drin.", None)]),
 (100137, 397, 230, "4.2", False, "Dunkler schmaler Streifen am Westrand der Straße: Gehölz oder Schatten.", [("klasse", "Dunkles Band (397/230) am Straßenrand, keine Baustelle.", None)]),
 (100126, 412, 213, "3.4", False, "Schmaler grauer Rand zwischen Straße und Feld 100083.", [("klasse", "Dunkler als die Fahrbahn (412/213), Rand statt Straße.", None)]),
 (100145, 439, 249, "4.2", False, "Große sehr dunkle Fläche zwischen Straße und Häuserblock: Baumgruppe oder tiefer Schatten, nach Zusammenlegen mit 100141 und 100139.", [("klasse", "Kein gerichteter Schlagschatten der Nachbarbauten; am ehesten Gehölz (439/249), daher 4.2 statt 0.2.", None)]),
 (100130, 472, 212, "1.1", False, "Kleiner hellgrauer Bau nordwestlich des Dachs 100127.", [("klasse", "Kleines Dach (472/212), wohl Nebengebäude; Feinklasse unsicher.", None)]),
 (100127, 497, 215, "1.1", True, "Helles rechteckiges Dach.", [("klasse", "Dach sicher (497/215), Neben- oder Hauptgebäude auf dem Scan nicht entscheidbar.", None)]),
 (100128, 483, 240, "1.1", True, "Zwei Dächer unterschiedlicher Helligkeit im Block nach Abtrennen des dunklen Hofteils 100283.", [("klasse", "Dach sicher (483/240), Feinklasse nicht entscheidbar.", None), ("trennen", "Grauer Dachteil im Westen (um 470/245) und helles Dach im Osten (um 515/245) mit sichtbarer Kante, gleiche Klasse.", None)]),
 (100148, 324, 254, "1.1", False, "Dunkle rechteckige Fläche mit scharfen Kanten: dunkles Dach oder Gebäudeschatten.", [("klasse", "Scharfkantig rechteckig (324/254), darum Gebäude; Feinklasse und Schatten nicht entscheidbar.", None)]),
 (100156, 331, 273, "1.1", False, "Hellgraue rechteckige Fläche südlich von 100148: Dach.", [("klasse", "Dach (331/273), Größe spricht nicht klar für Schuppen; 1.1.", None)]),
 (100164, 335, 285, "2.1", False, "Dunkler Streifen südlich von 100156: Schlagschatten des Baus auf dem Feld 100154.", [("klasse", "Schatten (335/285) bekommt nach U2 die Klasse der Fortsetzung, das Feld 100154.", None)]),
 (100151, 345, 256, "1", False, "Kleines helles Stück Hof zwischen 100148 und dem Bau 100280.", [("klasse", "Hofstück (345/256), kein eigenes Gebäude erkennbar.", None)]),
 (100155, 375, 259, "3.4", False, "Grauer Randstreifen zwischen Hof 100104 und Feld 100154.", [("klasse", "Linienförmiger Rand (375/259), kein Acker.", None)]),
 (100150, 404, 252, "3.4", False, "Grauer Rand am Westrand der Straße nach Süden.", [("klasse", "Rand (404/252) zwischen Straße und Feld.", None)]),
 (100161, 411, 275, "4.2", False, "Dunkleres Stück am Westrand der Straße neben dem Gehölz 100169.", [("klasse", "Dunkel wie Gehölz (411/275), eher Strauch als Acker.", None)]),
 (100149, 428, 278, "1.2", False, "Straße nach Süden, läuft nach v4 weiter.", [("klasse", "Fahrbahn (428/278), Belag nicht erkennbar; 1.2.", None)]),
 (100158, 440, 269, "4.2", False, "Kleines dunkelgraues Stück zwischen dem Gehölz 100145, der Straße und dem Bau 100142.", [("klasse", "Wohl Rand des Gehölzes 100145 (440/269), keine Baustelle.", None)]),
 (100142, 476, 266, "1.1", True, "Großer Dachkomplex aus hellen Dächern.", [("klasse", "Dächer sicher (476/266), Feinklasse nicht entscheidbar.", None)]),
 (100167, 501, 296, "1.1", True, "Langes helles Dach am Südrand des Viertels.", [("klasse", "Langes Dach (501/296) ist eher Teil eines Hofs als Schuppen; Feinklasse offen.", None)]),
 (100144, 529, 274, "1.1", True, "Helles Dach am Ostrand.", [("klasse", "Dach (529/274), Feinklasse nicht entscheidbar.", None)]),
 (100169, 426, 303, "4.2", False, "Dunkles längliches Gehölz am Westrand der Straße nach Süden, nach Zusammenlegen mit 100166.", [("klasse", "Gehölz sicher, ob Gebüsch, Baum oder Baumreihe nicht entscheidbar (426/303).", None)]),
 (100153, 549, 304, "1.1", False, "Dachstreifen mit Schatten in der Südostecke, reicht in v4 und den Kontextrand.", [("klasse", "Dach (549/304), Feinklasse nicht entscheidbar.", None)]),
 (100261, 325, 95, "1.1", True, "Abgetrennt aus 100045: helle Dachhälfte eines Streckhofs.", [("klasse", "Dach sicher (325/95), Feinklasse nicht entscheidbar.", None)]),
 (100262, 405, 95, "1.1", True, "Abgetrennt aus 100037: langer heller Dachstreifen.", [("klasse", "Dach sicher (405/95), Feinklasse nicht entscheidbar.", None)]),
 (100271, 420, 92, "1.1", False, "Abgetrennt aus 100037: dunkles Band nordöstlich des Dachstreifens 100262.", [("klasse", "Dachhälfte im Schatten oder Hofschatten (420/92).", None)]),
 (100275, 532, 85, "1.1", True, "Abgetrennt aus 100056: heller Dachstreifen.", [("klasse", "Dach sicher (532/85), Feinklasse nicht entscheidbar.", None)]),
 (100277, 395, 140, "1.1", False, "Abgetrennt aus 100066: heller schmaler Bau im Innenhof.", [("klasse", "Schmal und hell (395/140): Bau, Mauer oder Weg nicht sicher.", None)]),
 (100279, 340, 175, "1.1", True, "Abgetrennt aus 100100: heller L-förmiger Bau.", [("klasse", "Dach sicher (340/175), Feinklasse nicht entscheidbar.", None)]),
 (100280, 355, 228, "1.1", True, "Abgetrennt aus 100104: langer heller Bau.", [("klasse", "Dach sicher (355/228), Feinklasse nicht entscheidbar.", None)]),
 (100281, 360, 257, "4.2", False, "Abgetrennt aus 100104: dunkler kompakter Fleck, Baumkrone oder Schatten.", [("klasse", "Kompakte dunkle Form (360/257), am ehesten Baumkrone.", None)]),
 (100283, 545, 225, "1", False, "Abgetrennt aus 100128: dunkler Hofteil bzw. Schatten zwischen den Dächern.", [("klasse", "Hof oder Dach im Schatten (545/225), nur Ebene 1.", None)]),
 (100285, 560, 225, "1", False, "Abgetrennt aus 100128: kleines Randstück am Ostrand des Kerns.", [("klasse", "Randstück (560/225), Hof oder Dach nicht entscheidbar.", None)]),
]


def bilder(x, y):
    links, oben = x < 439, y < 189
    nah = {(True, True): 1, (False, True): 2, (True, False): 3, (False, False): 4}[(links, oben)]
    b = [VB + "uebersicht_nummern.jpg", VB + "uebersicht_roh.jpg", VB + f"nah{nah}_roh.jpg", VB + f"nah{nah}_nummern.jpg",
         O + f"nah_{nah}.jpg"]
    if 380 <= x <= 480 and 85 <= y <= 175:
        b.append(O + "nah_5.jpg")
    return b


segmente = []
naht = []
for sid, x, y, vor, sicher, was, punkte in T:
    if lab[y, x] != sid:
        yy, xx = np.nonzero(lab == sid); k = np.argmin((yy - y) ** 2 + (xx - x) ** 2); print("FEHLT", sid, x, y, "->", xx[k], yy[k], lab[y, x])
    heute = seg[sid]["klasse"]
    if vor == heute:
        vor = None
    pk = [{"nr": i + 1, "art": a, "text": t, "flaeche_px": f} for i, (a, t, f) in enumerate(punkte)]
    segmente.append({"id": sid, "klasse_heute": heute, "was_ist_es": was,
                     "urteil": "sauber" if not pk and vor is None else "nicht_sauber",
                     "klasse_vorschlag": vor, "sicher": sicher, "punkte": pk, "bilder": bilder(x, y)})
    m = lab == sid
    ys, xs = np.nonzero(m)
    if ys.min() < 64:
        naht.append({"id": sid, "seite": "oben", "text": f"Reicht über die obere Kerngrenze in den Kontextrand; Klasse dort gleich halten ({vor or heute})."})
    if xs.max() >= 564:
        naht.append({"id": sid, "seite": "rechts", "text": f"Reicht über die rechte Kerngrenze in den Kontextrand; Klasse dort gleich halten ({vor or heute})."})

N = lambda n: O + n
u = {
 "teilkachel": "r0c0", "viertel": "v2", "bearbeiter": "gegen-c-r0c0-v2",
 "bilder_angesehen": {
  "uebersicht": [B + "H0.png", B + "ganz/r0c0/ganz_nummern.jpg", VB + "uebersicht_nummern.jpg", VB + "uebersicht_roh.jpg",
                 N("umriss.jpg")],
  "nah": [VB + f"nah{i}_{k}.jpg" for i in range(1, 5) for k in ("roh", "nummern")]
         + [N(f"nah_{i}.jpg") for i in range(1, 6)] + [N("nah_5_roh.jpg")]},
 "segmente": segmente,
 "naht": naht,
 "unsicher": [
  "100143 (v4, nach der Teilung durch v4 heute mit 3072 Bildpunkten in v2): heller Streifen östlich der Straße 100149, Gehsteig, Mauer oder Dach; hier nicht geurteilt.",
  "100288 (v4, aus 100143 geteilt) liegt größtenteils in v2 neben der Straße 100149; hier nicht geurteilt.",
  "100077 (v1, Anger): setzt sich ohne Bildkante in 100094 fort; gemeinsame Klasse 3.1 an der Viertelgrenze prüfen.",
  "100154 (v3/v4, Feld): Schatten 100164 gehört nach U2 zu diesem Feld.",
  "100257 (v1): heller Fleck westlich von 100261 an der Viertelgrenze, gleiche Häuserzeile."],
 "nicht_geprueft": ["Kontextrand-Anteile von 100028, 100037, 100041, 100042, 100012, 100020, 100030, 100032, 100070, 100081, 100092, 100111, 100144, 100153 nur als Umgebung angesehen.",
                    "Anteile von 100104, 100148 (v1) sowie 100149, 100167, 100153 (v4) außerhalb von v2 nur als Umgebung."],
 "offen": [
  "Dächer: Hauptgebäude oder Nebengebäude/Stadel ist auf dem Scan nirgends sicher; Farbbild oder Kataster würde es entscheiden.",
  "Dunkle Bänder 100045, 100041, 100056, 100271, 100071: beschattete Dachhälfte oder Schatten im Hof; Farbbild entscheidet.",
  "Höfe und Gärten 100062, 100063, 100066, 100104, 100111, 100283: befestigter Hof, Rasen oder Beet; im Farbbild entscheidbar.",
  "Felder 100083 und 100012: Acker oder Grünland (Garten); im Farbbild prüfen.",
  "Straßen 100030, 100073, 100149: befestigt oder Erdweg (6.6); Belag im Farbbild bzw. aus Altkarten.",
  "Dunkle Flächen 100145, 100112, 100281: Gehölz oder Schatten; Farbbild (Grün) entscheidet."],
 "eingriffe": [
  {"schritt": "teilen", "vorher": [100045], "nachher": [100045, 100261], "grund": "Die helle Dachhälfte 100261 wurde vom dunklen Band 100045 getrennt; Splitter des Schnitts (IDs 100260 bis 100265) wurden sofort wieder angefügt."},
  {"schritt": "teilen", "vorher": [100037], "nachher": [100037, 100262, 100271], "grund": "Heller Dachstreifen 100262 und dunkles Band 100271 wurden aus dem gemischten Segment gelöst; Splitter (IDs 100263 bis 100273) wieder an 100262 angefügt."},
  {"schritt": "teilen", "vorher": [100056], "nachher": [100056, 100275], "grund": "Heller Dachstreifen 100275 vom Schattenband 100056 getrennt; Splitter (IDs 100274 bis 100280) sofort wieder angefügt."},
  {"schritt": "teilen", "vorher": [100066], "nachher": [100066, 100277], "grund": "Schmaler heller Bau 100277 aus dem dunklen Innenhof 100066 gelöst; Splitter (IDs 100276 bis 100281) sofort wieder angefügt."},
  {"schritt": "teilen", "vorher": [100100], "nachher": [100100, 100279], "grund": "Heller L-förmiger Bau 100279 von der dunklen Fläche 100100 getrennt; Splitter (IDs 100278 bis 100281) sofort wieder angefügt."},
  {"schritt": "teilen", "vorher": [100104], "nachher": [100104, 100280], "grund": "Langer heller Bau 100280 aus der Hofmischfläche 100104 gelöst; ein Splitter wurde sofort wieder angefügt."},
  {"schritt": "teilen", "vorher": [100104], "nachher": [100104, 100281], "grund": "Dunkler kompakter Fleck 100281 (Baumkrone oder Schatten) aus der Hofmischfläche gelöst."},
  {"schritt": "teilen", "vorher": [100128], "nachher": [100128, 100283, 100285], "grund": "Dunkler Hofteil 100283 und Randstück 100285 von den hellen Dächern 100128 getrennt; Splitter (IDs 100282 bis 100292) wieder angefügt."},
  {"schritt": "verschmelzen", "vorher": [100030, 100109, 100117, 100084, 100086], "nachher": [100030], "grund": "Stücke derselben Fahrbahn und Kreuzung ohne Bildkante zu einem Segment zusammengelegt."},
  {"schritt": "verschmelzen", "vorher": [100083, 100095, 100087], "nachher": [100083], "grund": "Dunkle Flecken am Rand derselben Feldfläche ohne klare Kante angefügt."},
  {"schritt": "verschmelzen", "vorher": [100012, 100053, 100054], "nachher": [100012], "grund": "Stücke derselben Gartenfläche nördlich der Kreuzung ohne Kante zusammengelegt."},
  {"schritt": "verschmelzen", "vorher": [100145, 100141, 100139], "nachher": [100145], "grund": "Teile derselben dunklen Fläche ohne Bildkante zusammengelegt."},
  {"schritt": "verschmelzen", "vorher": [100169, 100166], "nachher": [100169], "grund": "Zwei Teile desselben dunklen Gehölzes am Straßenrand zusammengelegt."}],
}
open(O + "urteil.json", "w", encoding="utf-8").write(json.dumps(u, ensure_ascii=False, indent=1))
ns = sum(s["urteil"] == "nicht_sauber" for s in segmente)
np_ = sum(len(s["punkte"]) for s in segmente)
nu = sum(not s["sicher"] for s in segmente)
print("segmente", len(segmente), "nicht_sauber", ns, "punkte", np_, "unsicher", nu, "naht", len(naht))
