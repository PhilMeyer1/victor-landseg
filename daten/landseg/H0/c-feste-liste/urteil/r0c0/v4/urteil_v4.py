"""Schreibt urteil.json, maengel.jpg und vorschlag.jpg für r0c0/v4 (urt-c-r0c0-v4, Nachholung)."""
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import tifffile
import bilder_v4 as bv

B = "C:/Users/Phil/Developement/Victor/daten/landseg/H0"
OUT = B + "/c-feste-liste/urteil/r0c0/v4/"
VQ = B + "/viertel/r0c0/v4/"
seg = {s["id"]: s for s in json.load(open(B + "/c-feste-liste/r0c0/segmente.json", encoding="utf-8"))["segmente"]}

UN, UR, UK = VQ + "uebersicht_nummern.jpg", VQ + "uebersicht_roh.jpg", VQ + "uebersicht_kontrast.jpg"
N1, N2, N3, N4, N5, N6, N7, N8, K1 = [OUT + n for n in
    ["nah_1.jpg", "nah_2.jpg", "nah_3.jpg", "nah_4.jpg", "nah_5.jpg", "nah_6.jpg", "nah_7.jpg", "nah_8.jpg", "kontrast_1.jpg"]]
OBEN = [UN, UR, N1, N2, N7]
OST = [UN, N1, N2, N8, K1]
UNTEN_R = [UN, UR, N3, N4]
UNTEN_L = [UN, UR, N5, N6]

# id: (vorschlag, sicher, was_ist_es, [(art, text, flaeche, (x, y))], bilder)
U = [
 (100172, "4.2", False, "Dunkler Fleck westlich der Straße am oberen Viertelrand, Fortsetzung der Kronenreihe 161/166/169 (Baum oder Strauch mit Schatten).",
  [("klasse", "Dunkle Krone statt Baustelle bei 432/318; Baum oder Strauch, auf SW nicht sicher von Schatten zu trennen.", None, (432, 318))], OBEN),
 (100180, "3.4", False, "Mitteldunkler Randstreifen zwischen Acker 154 und Straße 149.",
  [("klasse", "Schmaler Streifen am Straßenrand bei 439/339: Rain statt Acker mit Bewuchs; dunkler als der Acker, Schatten der Bäume möglich.", None, (439, 339))], OBEN),
 (100143, "1", False, "Große dunkle Fläche östlich der Straße: im v4-Teil eine fast schwarze Fläche zwischen Straße und Hof 178, im v2-Teil die Schattenbänder zwischen den Bauten 142/167; dazu noch ein Straßenstreifen nördlich von y 314.",
  [("fremdes", "Der östliche Fahrbahnstreifen 454–473/314–337 lag in 143; an die Straße 198 gegeben (Eingriff). Nördlich von y 314 (v2) liegt der Streifen weiter in 143.", 210, (462, 322)),
   ("trennen", "Schwarze Fläche bei 489/349 und Schattenbänder im v2-Teil sind verschiedene Dinge; nicht geteilt, weil die Trennung im v2-Teil läge.", None, (489, 349)),
   ("klasse", "Kein Dach zu sehen: Schatten, dichter Bewuchs oder dunkler Garten; Elternklasse 1 der Umgebung (U2).", None, (495, 360))], OBEN + [N8]),
 (100178, "3", False, "Mittelgraue, leicht fleckige Fläche östlich der schwarzen Fläche 143, von dunklen Linien umgrenzt, ohne First und ohne eigenen Schatten.",
  [("klasse", "Kein Dach bei 530/348 (keine Firstlinie, kein Schlagschatten); Garten oder Hof, Bewuchs vermutet.", None, (530, 348))], OST),
 (100165, "1", False, "Kleiner Kernteil an der rechten Kerngrenze, Rest im Kontextrand; mittelgrau zwischen den Dachreihen 153 und 170.",
  [("klasse", "Im Kernteil bei 557/318 kein Dach erkennbar; Hauptgebäude nicht belegt, Elternklasse 1.", None, (557, 318))], [UN, N7, N8, K1]),
 (100185, "1.1", False, "Kleiner heller länglicher Körper (etwa 9 × 3 m) mit Schlagschatten am Feldrand westlich der Straße.",
  [("klasse", "Sportplatz (Vorstufe sicher: ja) passt nicht bei 434/364: Körper mit Schatten, eher Schuppen, Wagen oder Haufen; Gebäude 1.1 vermutet.", None, (434, 364))], OBEN),
 (100187, "3.4", False, "Mittelgrauer Randstreifen zwischen Acker 154 und der Gehölzfläche 183.",
  [("klasse", "Rain statt Acker mit Bewuchs bei 442/379; die Kante zu 154 ist schwach, Teil des Ackers möglich.", None, (442, 379))], OBEN),
 (100183, "4.2", False, "Streifen westlich der Straßengabel mit mehreren dunklen Kronen und Schatten, dazwischen heller Boden.",
  [("klasse", "Keine Baustelle bei 476/395: Baumreihe an der Straße mit Boden dazwischen; Gehölz überwiegt.", None, (476, 400)),
   ("trennen", "Kronen und Boden nicht einzeln getrennt, weil die Kanten im Schatten unscharf sind.", None, (462, 385))], OBEN),
 (100189, "1.2", False, "Glatte hellgraue Fläche südlich des Weges 186 an der Straßengabel (Hof oder Vorplatz).",
  [("klasse", "Kein Dach bei 521/397 (kein Schatten, keine Kanten eines Baus); Hof- oder Verkehrsfläche, Belag offen.", None, (521, 397))], OST),
 (100186, "1.2", False, "Heller schmaler Weg, der an der Straßengabel nach Nordosten abzweigt, mit einer grauen Fläche nördlich davon und einem hellen runden Körper am Westende.",
  [("klasse", "Keine Baustelle bei 528/368: Weg, Belag offen.", None, (528, 368)),
   ("grenze", "Der Weg läuft östlich von 539/372 in 176 weiter; die graue Fläche 522–539/363–370 nördlich des Weges gehört eher zum Hof.", None, (540, 372))], OST),
 (100194, "4.2", False, "Dunklere Fläche mit Kronen zwischen Gehölz 183 und Acker 195.",
  [("klasse", "Dunkle Kronen bei 458/407 statt Acker mit Bewuchs; Gehölz vermutet.", None, (458, 407))], OBEN),
 (100198, "1.2", False, "Helle Hauptstraße von der Gabel nach Südosten über die Kerngrenze; nach den Eingriffen auch die östliche Fahrbahnhälfte zwischen y 314 und der Gabel.",
  [("verschmelzen", "Die Stücke 191 und 193 derselben Fahrbahn sind angehängt (erster Bearbeiter).", None, (494, 400)),
   ("fehlt", "Fahrbahn 454–493/314–398 lag in 143 und 183; an 198 gegeben.", None, (468, 345)),
   ("klasse", "Befestigt (1.2.2 der Vorstufe) und versiegelt sind auf SW nicht belegt; Verkehrsfläche 1.2.", None, (530, 480))], OBEN + UNTEN_R),
 (100196, "4.2", False, "Schwarzer Fleck östlich der Straße mit einem helleren Rand darüber (Baum, Strauch oder Schatten).",
  [("klasse", "Kein Hauptgebäude bei 519/422: schwarz ohne Dachfläche; Gehölz vermutet, Schatten möglich.", None, (518, 424))], OST),
 (100176, "1", False, "Sehr große Mischfläche östlich der Straße mit Höfen, Bauten, einem schwarzen Schattenfleck und dem dunklen Saum an der Straße; zu zwei Dritteln im Kontextrand.",
  [("trennen", "Enthält Höfe, Dächer und den schwarzen Fleck 530–555/382–402; nicht geteilt, weil die meisten Teile über die Kerngrenze reichen.", None, (542, 392)),
   ("verschmelzen", "Fleck 192 ohne Kante angehängt (erster Bearbeiter).", None, (536, 406)),
   ("klasse", "Hauptgebäude trifft nur Teile; Elternklasse 1 für die Mischfläche.", None, (545, 440))], OST + UNTEN_R),
 (100207, "4.2", False, "Dunkler Fleck westlich der Straße zwischen Acker 195 und Randstreifen 201.",
  [("klasse", "Baum oder Strauch bei 495/450 statt Acker.", None, (495, 450))], [UN, N1, N3, N4]),
 (100201, "3.4", False, "Mittelgrauer Randstreifen westlich der Straße mit einzelnen dunklen Flecken.",
  [("klasse", "Keine Fahrbahn bei 512/468 (Grau 80, die Straße ist um 150): Wegrand.", None, (512, 468))], [UN, N1, N3, N4]),
 (100209, "4.2", False, "Nur 4 Bildpunkte im Kern; im Kontextrand eine dunkle, fleckige Fläche östlich der Straße.",
  [("zu_klein", "Kernanteil 4 px bei 562/492; im Kontextrand Bäume oder Schatten, Wolke 0.2 nicht belegt.", 4, (562, 492))], UNTEN_R),
 (100216, "4.2.1", False, "Schwarze runde Krone (etwa 5 m) am Feldweg zwischen 154 und 195, dazu ein Stück des hellen Weges westlich davon.",
  [("klasse", "Einzelbaum statt Acker bei 379/529; Strauch möglich.", None, (379, 529)),
   ("grenze", "Der helle Wegstreifen 366–374/517–535 gehört zum Feldweg 220, nicht zur Krone.", 60, (370, 525))], UNTEN_L),
 (100195, "2", False, "Großer Acker mit Längsstreifen südöstlich von 154, reicht über die untere Kerngrenze.",
  [("grenze", "Grenze zu 154 läuft zackig quer zu den Ackerstreifen ohne Bildkante (etwa 340/510 bis 475/420); die Parzellengrenzen sind die hellen Streifen (etwa 315/482 bis 482/409).", None, (420, 455)),
   ("verschmelzen", "Randsplitter 199 ohne Kante angehängt (erster Bearbeiter).", None, (462, 425)),
   ("klasse", "Bewuchs auf SW nicht sicher; Acker 2.", None, (457, 508))], UNTEN_L + UNTEN_R + [UK]),
 (100210, "4.2.3", False, "Dunkler länglicher Streifen westlich der Straße (Hecke, Baumreihe oder Graben mit Schatten).",
  [("klasse", "Lineares Gehölz bei 534/510 statt Acker mit Bewuchs; ein Graben ist auf SW nicht auszuschließen.", None, (534, 510))], UNTEN_R),
 (100214, "3.4", False, "Mittelgrauer Randstreifen zwischen Hecke 210, Straße und Baum 218.",
  [("klasse", "Keine Fahrbahn bei 552/526 (Grau 82): Wegrand.", None, (550, 524))], UNTEN_R),
 (100211, "4.2", False, "Dunkler Fleck an der Ostseite der Straße an der rechten Kerngrenze.",
  [("klasse", "Baum oder Schatten bei 557/500 statt Straße; die Fahrbahn ist hell.", None, (557, 500))], UNTEN_R),
 (100218, "4.2", False, "Schwarzer Fleck westlich der Straße an der unteren Kerngrenze (Baum mit Schatten).",
  [("klasse", "Baum statt Baustelle bei 557/542.", None, (556, 545))], UNTEN_R),
 (100215, "1", False, "Nur 22 Bildpunkte im Kern; im Kontextrand eine helle Hof- oder Baufläche östlich der Straße.",
  [("zu_klein", "Kernanteil 22 px bei 562/520; Nebengebäude nicht belegt.", 22, (562, 520))], UNTEN_R),
 (100224, "2", False, "Kleines Stück Acker am Feldweg an der unteren Kerngrenze.",
  [("klasse", "Acker bei 369/559, Bewuchs offen.", None, (369, 559))], UNTEN_L),
 (100220, "6.6", False, "Heller Streifen des Feldwegs zwischen den Äckern 154 und 195 an der unteren Kerngrenze.",
  [("klasse", "Keine Baustelle bei 382/557: unbefestigter Feldweg vermutet.", None, (384, 552))], UNTEN_L),
 (100225, "4.2", False, "Dunkler Fleck am Feldweg an der unteren Kerngrenze.",
  [("klasse", "Gehölz oder Schatten bei 398/558 statt Acker.", None, (398, 558))], UNTEN_L),
 (100219, "2", False, "Hellerer Acker südlich von 195, großteils im Kontextrand.",
  [("klasse", "Hauptgebäude falsch bei 500/555: gleichmäßige Ackertextur mit Streifen; Acker, Bewuchs offen.", None, (500, 555))], UNTEN_R),
 (100228, "2", False, "Nur 21 Bildpunkte im Kern am Rand des Ackers 219.",
  [("zu_klein", "Kernanteil 21 px bei 542/562; gehört zum Acker 219.", 21, (538, 561))], UNTEN_R),
 (100229, "1.2", False, "Nur 19 Bildpunkte im Kern; Weg im Kontextrand unterhalb.",
  [("zu_klein", "Kernanteil 19 px bei 545/562; Weg, Belag offen.", 19, (548, 561))], UNTEN_R),
]

segmente, mpunkte = [], []
nr = 0
for sid, vor, sicher, was, punkte, bilder in U:
    pl = []
    for art, text, fl, xy in punkte:
        nr += 1
        pl.append({"nr": nr, "art": art, "text": text, "flaeche_px": fl})
        mpunkte.append((nr, xy, art))
    heute = seg[sid]["klasse"]
    segmente.append({"id": sid, "klasse_heute": heute, "was_ist_es": was,
                     "urteil": "nicht_sauber" if pl else "sauber",
                     "klasse_vorschlag": vor if vor != heute else None,
                     "sicher": sicher, "punkte": pl, "bilder": bilder})

nah = [VQ + "nah2_roh.jpg", VQ + "nah2_nummern.jpg", N1, N2, N3, N4, N5, N6, N7, N8, K1]
urteil = {
 "teilkachel": "r0c0", "viertel": "v4", "bearbeiter": "urt-c-r0c0-v4",
 "bilder_angesehen": {"uebersicht": [B + "/H0.png", B + "/ganz/r0c0/ganz_nummern.jpg", UN, UR, UK,
                                      OUT + "umriss.jpg", OUT + "maengel.jpg", OUT + "vorschlag.jpg"],
                      "nah": nah},
 "segmente": segmente,
 "naht": [
  {"id": 100198, "seite": "unten", "text": "Straße 198 läuft über die untere und die rechte Kerngrenze weiter; Klasse 1.2 für beide Seiten."},
  {"id": 100195, "seite": "unten", "text": "Acker 195 reicht über die untere Kerngrenze; Klasse 2."},
  {"id": 100219, "seite": "unten", "text": "Acker 219 liegt überwiegend unterhalb des Kerns; Hauptgebäude der Vorstufe passt nicht, Klasse 2."},
  {"id": 100176, "seite": "rechts", "text": "Mischfläche 176 liegt zu zwei Dritteln rechts außerhalb des Kerns; Klasse 1."},
  {"id": 100209, "seite": "rechts", "text": "209 hat nur 4 px im Kern; das Urteil 4.2 gilt für die dunkle Fläche jenseits der rechten Kerngrenze."},
  {"id": 100215, "seite": "rechts", "text": "215 hat nur 22 px im Kern; das Urteil 1 gilt für die helle Fläche jenseits der rechten Kerngrenze."},
 ],
 "unsicher": [
  "100154 (v3): Grenze zu 195 ohne Bildkante quer zu den Ackerstreifen; die Parzellengrenzen sind die hellen Streifen.",
  "100149 (v2) und 198: beide Fahrbahn derselben Straße, liegen bei 440–475/314–362 nebeneinander ohne Bildkante; gemeinsame Klasse 1.2.",
  "100143: nördlich von y 314 (v2) liegt die östliche Fahrbahnhälfte (etwa 452–470/229–314) noch in 143; gehört zur Straße 149/198.",
 ],
 "nicht_geprueft": [
  "Segmente der Nachbarviertel und des Kontextrands nur als Umgebung angesehen.",
  "Die Bilder kontrast_2.jpg und kontrast_3.jpg des ersten Bearbeiters nicht neu erzeugt und nicht als Grundlage genutzt.",
 ],
 "offen": [
  "143 (v4-Teil): Schatten, dichter Bewuchs oder dunkler Garten – Farbbild.",
  "178: Garten oder unbefestigter Hof – Farbbild.",
  "172, 183, 194, 196, 207, 210, 211, 216, 218, 225: Bäume, Hecke, Graben oder Schatten – Farbbild.",
  "Äcker 195, 219, 224, 228: Bewuchs ja oder nein – Farbbild.",
  "Straße 198, Weg 186, Hof 189, Weg 229: befestigt, versiegelt oder Schotter – Farbbild.",
  "185: Schuppen, Wagen oder Haufen – Farbbild oder Stereo.",
  "165, 215: Dach oder Hof im Kernteil – Farbbild.",
 ],
 "eingriffe": [
  {"schritt": "verschmelzen", "vorher": [100198, 100191, 100193], "nachher": [100198], "grund": "Erster Bearbeiter: Fahrbahnstücke derselben Straße ohne Bildkante."},
  {"schritt": "verschmelzen", "vorher": [100195, 100199], "nachher": [100195], "grund": "Erster Bearbeiter: Randsplitter des Ackers ohne Bildkante."},
  {"schritt": "verschmelzen", "vorher": [100176, 100192], "nachher": [100176], "grund": "Erster Bearbeiter: Fleck in der Hoffläche ohne Bildkante."},
  {"schritt": "grenze_verschieben", "vorher": [100183, 100143], "nachher": [100183, 100143], "grund": "Erster Bearbeiter: Splitter von 183 östlich der Straße an 143 und Splitter von 143 westlich der Straße an 183."},
  {"schritt": "polygon_zuweisen", "vorher": [100143, 100183, 100198], "nachher": [100143, 100183, 100198], "grund": "Erster Bearbeiter: das Straßenstück zwischen 149 und der Gabel lag in 143 und 183 und ist jetzt Teil der Straße 198."},
  {"schritt": "grenze_verschieben", "vorher": [100143, 100198], "nachher": [100143, 100198], "grund": "Nachholung: die östliche Fahrbahnhälfte 454–473/314–337 (210 px) ging von 143 an die Straße 198, entlang der hell-dunkel-Kante."},
 ],
}
with open(OUT + "urteil.json", "w", encoding="utf-8") as f:
    json.dump(urteil, f, ensure_ascii=False, indent=1)

# Bilder
x0, y0, x1, y1, fk = 282, 282, 596, 596, 3
FONT = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 15)
FONT_S = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 13)


def legende(im, zeilen):
    w = im.width
    h = 18 * len(zeilen) + 8
    neu = Image.new("RGB", (w, im.height + h), (0, 0, 0))
    neu.paste(im, (0, 0))
    d = ImageDraw.Draw(neu)
    for i, z in enumerate(zeilen):
        d.text((6, im.height + 4 + 18 * i), z, fill=(255, 255, 255), font=FONT_S)
    return neu

m = bv.umriss(x0, y0, x1, y1, fk, nummern=False)
d = ImageDraw.Draw(m)
farbe = {"klasse": (255, 80, 80), "fremdes": (255, 0, 255), "trennen": (255, 160, 0), "grenze": (0, 200, 255),
         "verschmelzen": (120, 255, 120), "fehlt": (255, 0, 255), "zu_klein": (200, 200, 200)}
for n, (x, y), art in mpunkte:
    px, py = (x - x0) * fk, (y - y0) * fk
    d.ellipse([px - 10, py - 10, px + 10, py + 10], fill=farbe.get(art, (255, 255, 255)), outline=(0, 0, 0))
    d.text((px, py), str(n), fill=(0, 0, 0), font=FONT_S, anchor="mm")
zeilen = ["Mängel (Nummer = Punkt in urteil.json): rot Klasse, violett fremdes/fehlt, orange trennen, blau Grenze, grün verschmolzen, grau zu klein"]
m = legende(m, zeilen)
m.save(OUT + "maengel.jpg", quality=90)

klassen = {}
for s in segmente:
    klassen[s["id"]] = (s["klasse_vorschlag"] or s["klasse_heute"]) + ("?" if not s["sicher"] else "")
v = bv.umriss(x0, y0, x1, y1, fk, nummern=True, klassen=klassen)
v = legende(v, ["Vorschlag: Nummer und Klasse, wie ich sie setzen würde (? = unsicher); Grenzen nach den Eingriffen, sonst unverändert"])
v.save(OUT + "vorschlag.jpg", quality=90)
print("segmente", len(segmente), "punkte", nr, "unsicher", sum(1 for s in segmente if not s["sicher"]))
