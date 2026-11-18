import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

D = "C:/Users/Phil/Developement/Victor/daten/landseg/H0"
VB = D + "/viertel/r0c0/v4/"
OUT = D + "/b-kategorien-frei/urteil/r0c0/v4/"
lab = np.array(Image.open(D + "/b-kategorien-frei/r0c0/labels.tif"))
img = np.array(Image.open(D + "/teilkacheln/r0c0.png").convert("L"))
seg = {s["id"]: s for s in json.load(open(D + "/b-kategorien-frei/r0c0/segmente.json", encoding="utf-8"))["segmente"]}

U, R, K = VB + "uebersicht_nummern.jpg", VB + "uebersicht_roh.jpg", VB + "uebersicht_kontrast.jpg"
N1, N2, N3, N4 = VB + "nah1_nummern.jpg", VB + "nah2_nummern.jpg", VB + "nah3_nummern.jpg", VB + "nah4_nummern.jpg"
R2, R4 = VB + "nah2_roh.jpg", VB + "nah4_roh.jpg"
E4, E5, K2 = OUT + "nah_4.jpg", OUT + "nah_5.jpg", OUT + "kontrast_2.jpg"

KL = {
    "EINZELBAUM": ("Gehölz", "Baum", "Einzelbaum"),
    "BAUMREIHE": ("Gehölz", "Baumreihe", "Baumreihe"),
    "GEBUESCH": ("Gehölz", "Gebüsch", "Gebüsch"),
    "HECKE": ("Gehölz", "Gebüsch", "Hecke"),
    "WEGRAIN": ("Grünfläche", "Saum", "Wegrain"),
    "FELDRAIN": ("Grünfläche", "Saum", "Feldrain"),
    "HOF": ("Bebauung", "Hof", "Hof"),
    "GEBAEUDE": ("Bebauung", "Gebäude", "Gebäude"),
    "STRASSE": ("Verkehrsfläche", "Straße", "Straße"),
    "GASSE": ("Verkehrsfläche", "Weg", "Gasse"),
    "FELDWEG": ("Verkehrsfläche", "Weg", "Feldweg"),
    "BANKETT": ("Verkehrsfläche", "Straßenrand", "Bankett"),
    "FELD": ("Landwirtschaft", "Feld", "Feld"),
}
KLASSEN_FREI = [
    ("Bebauung", "grob", None, "Gebäude und Höfe im Ort: helle Dachflächen mit scharfen Kanten und harten Schatten, dazwischen graue Höfe."),
    ("Verkehrsfläche", "grob", None, "Helle, glatte, linienförmige Bänder ohne Textur."),
    ("Gehölz", "grob", None, "Sehr dunkle, rundliche oder gereihte Flecken mit Schlagschatten."),
    ("Grünfläche", "grob", None, "Mittelgraue, leicht fleckige Streifen ohne Bewirtschaftungsmuster zwischen Feld, Weg und Gehölz."),
    ("Landwirtschaft", "grob", None, "Große, gleichmäßig graue Flächen mit feinem Korn und Streifen der Bewirtschaftung."),
    ("Gebäude", "mittel", "Bebauung", "Hell oder mittelgrau mit geraden Kanten und dunklem Schlagschatten an einer Seite."),
    ("Hof", "mittel", "Bebauung", "Gleichmäßig graue oder beschattete Fläche zwischen Gebäuden, ohne Dachkanten."),
    ("Straße", "mittel", "Verkehrsfläche", "Breites helles Band (über 8 Bildpunkte), durchgehend, mit glatten Rändern."),
    ("Weg", "mittel", "Verkehrsfläche", "Schmales helles Band (unter 8 Bildpunkte)."),
    ("Straßenrand", "mittel", "Verkehrsfläche", "Schmaler grauer Saum direkt an der Fahrbahn."),
    ("Baum", "mittel", "Gehölz", "Einzelne dunkle runde Krone mit Schatten."),
    ("Baumreihe", "mittel", "Gehölz", "Mehrere dunkle Kronen in einer Reihe, dazwischen heller Boden."),
    ("Gebüsch", "mittel", "Gehölz", "Dunkle, unregelmäßige, kleinere Flecken ohne klare Einzelkrone."),
    ("Saum", "mittel", "Grünfläche", "Grauer Streifen zwischen Feld und Weg oder Gehölz."),
    ("Feld", "mittel", "Landwirtschaft", "Große Fläche mit feinem Korn; Acker oder Grünland auf Schwarz-Weiß nicht zu trennen."),
    ("Gebäude", "fein", "Gebäude", "wie mittlere Ebene."),
    ("Hof", "fein", "Hof", "wie mittlere Ebene."),
    ("Straße", "fein", "Straße", "wie mittlere Ebene; Belag nicht erkennbar."),
    ("Gasse", "fein", "Weg", "Schmales helles Band zwischen Höfen, von der Straße abzweigend."),
    ("Feldweg", "fein", "Weg", "Schmales helles Band am Feldrand."),
    ("Bankett", "fein", "Straßenrand", "Grauer Rand unmittelbar neben der hellen Fahrbahn."),
    ("Einzelbaum", "fein", "Baum", "Einzelne dunkle runde Krone, oft mit hellem Fleck daneben."),
    ("Baumreihe", "fein", "Baumreihe", "wie mittlere Ebene."),
    ("Gebüsch", "fein", "Gebüsch", "wie mittlere Ebene."),
    ("Hecke", "fein", "Gebüsch", "Dunkles schmales Band entlang einer Straße oder Feldgrenze."),
    ("Wegrain", "fein", "Saum", "Grauer Streifen zwischen Feld und Straße oder Weg."),
    ("Feldrain", "fein", "Saum", "Grauer Streifen am Feldrand ohne Weg daneben."),
    ("Feld", "fein", "Feld", "wie mittlere Ebene."),
]

V = 100000
# id, Klasse, sicher, urteil, was_ist_es, punkte[(art, text, (x,y), flaeche)], bilder
S = [
 (V+172, "EINZELBAUM", False, "sauber", "Dunkle runde Krone am Westrand der Straße, Fortsetzung der Baumreihe 169.", [], [U, R, N1]),
 (V+180, "WEGRAIN", False, "sauber", "Mittelgrauer Streifen mit einzelnen dunklen Flecken zwischen Feld 154 und Straße 149.", [], [U, R, N1, N2]),
 (V+143, "HOF", False, "nicht_sauber", "Beschattete Hofflächen zwischen den Längsbauten in v2 und ein großer dunkler Keil östlich der Straße; das helle Straßenband ist als 276/279 abgetrennt.", [
     ("sonstiges", "Dunkler Keil 470–530/300–390 ist Schlagschatten der Bauten oder dunkler Boden; ohne Bildkante dazwischen nicht teilbar, darum im Hofsegment gelassen.", (500, 350), None)], [U, R, N2, E4]),
 (V+276, "STRASSE", False, "sauber", "Helles Band östlich von 149 (neu aus 143), durch eine dunkle Linie von 149 getrennt: zweite Fahrbahnhälfte oder Gehweg.", [], [U, R, N2]),
 (V+279, "STRASSE", False, "sauber", "Kurzes Stück desselben hellen Bands südlich von 276 (neu aus 143).", [], [U, N2]),
 (V+178, "HOF", False, "sauber", "Gleichmäßig mittelgraue Fläche mit leichter Körnung zwischen 143 und 176: Hof oder Garten.", [], [U, R, N2, E4]),
 (V+165, "GEBAEUDE", False, "sauber", "Kernstück (551–563/318–338) eines Baus, dessen Hauptteil in r0c1 liegt; im Kern vor allem Schattenseite.", [], [U, E4]),
 (V+185, "WEGRAIN", False, "sauber", "Grauer Fleck am Straßenrand mit einem kleinen hellen Längsobjekt 444–454/365–370 (Schuppen, Fahrzeug oder Haufen).", [], [U, R, N1, N2]),
 (V+187, "WEGRAIN", False, "sauber", "Mittelgrauer Streifen zwischen Feld 154 und Baumreihe 183.", [], [U, R, N1]),
 (V+183, "BAUMREIHE", False, "nicht_sauber", "Reihe dunkler Kronen mit Schatten westlich der Einmündung, dazwischen heller offener Boden.", [
     ("trennen", "Dunkle Kronen (447–502/364–443) und helle Bodenflecken (etwa 466–474/415–424) stecken in einem Segment; die Einzelkronen sind nicht scharf genug getrennt, darum nicht geteilt.", (480, 410), None)], [U, R, K, N2, K2]),
 (V+191, "STRASSE", False, "sauber", "Helle Mitte der Einmündung der Gasse 186 in die Straße.", [], [U, N2, E4]),
 (V+189, "HOF", False, "sauber", "Gleichmäßig hellgraue Fläche südlich der Gasse (499–534/379–421): Hof oder offener Platz.", [], [U, R, N2, E4]),
 (V+186, "GASSE", False, "sauber", "Schmale helle Gasse von der Einmündung nach Nordost samt grauem Rand.", [], [U, N2, E4]),
 (V+194, "GEBUESCH", False, "sauber", "Dunkler Buschfleck mit grauem Rand zwischen Baumreihe 183 und Feld.", [], [U, N2, K2]),
 (V+199, "FELDRAIN", False, "sauber", "Gleichmäßig grauer, etwas hellerer Rand des Feldes 195 vor der Baumreihe.", [], [U, N2, K2]),
 (V+193, "STRASSE", False, "sauber", "Hellgrauer Teil der Einmündung zwischen 191 und Straße 198.", [], [U, N2, K2]),
 (V+198, "STRASSE", True, "sauber", "Breite helle Straße nach Südost von der Einmündung bis über den unteren Kernrand.", [], [U, R, N2, N4, R4]),
 (V+196, "HOF", False, "sauber", "Kleine graue Fläche mit Schattenfleck zwischen Platz 189 und Hof 176.", [], [U, N2, R2]),
 (V+192, "HOF", False, "sauber", "Kleine graue Hoffläche am Rand von 176.", [], [U, N2, E4]),
 (V+176, "HOF", False, "nicht_sauber", "Höfe mit hellen Längsbauten (Streckhöfe) östlich der Straße, Hauptteil im Kontextrand (r0c1/r1c1).", [
     ("trennen", "Helle Längsbauten 535–563/387–424 und 544–563/442–486 stecken im Hofsegment; nicht geteilt, weil sie über den Kernrand reichen und ein Schnitt nur im Kern die Naht verletzen würde.", (552, 462), None)], [U, R, N2, N4, R4]),
 (V+207, "GEBUESCH", False, "sauber", "Dunkle Busch- oder Baumgruppe am Feldrand an der Straße.", [], [U, N4, K2]),
 (V+201, "WEGRAIN", False, "sauber", "Grauer Streifen mit dunklen Stellen zwischen Feld 195 und Straße 198.", [], [U, N4, R4]),
 (V+209, "GEBUESCH", False, "sauber", "Nur 4 Bildpunkte im Kern; Rand einer dunklen Gehölzgruppe in r0c1.", [], [U, N4]),
 (V+216, "EINZELBAUM", False, "nicht_sauber", "Dunkle runde Krone an der Feldecke unten links, links daneben heller Streifen.", [
     ("fremdes", "Heller Streifen 366–373/526–538 links der Krone gehört zum Feldweg 220.", (369, 532), 60)], [U, R, N3, E5]),
 (V+195, "FELD", False, "nicht_sauber", "Großes gleichmäßig graues Feld mit feinen hellen Linien südöstlich von Feld 154.", [
     ("grenze", "Grenze zu 154 läuft zackig ohne Bildkante (etwa 340/450 bis 440/400) durch eine einheitliche Fläche; ein dunklerer Bewirtschaftungsstreifen läuft ungebrochen von 195 nach 154.", (380, 445), None)], [U, R, K, N1, N3, N4, K2]),
 (V+210, "HECKE", False, "sauber", "Dunkles Band entlang des Straßenrands (509–547/473–536): Hecke oder Gehölzstreifen mit Schatten.", [], [U, N4, R4]),
 (V+214, "WEGRAIN", False, "sauber", "Mittelgrauer Streifen zwischen Hecke 210 und Straße 198.", [], [U, N4, R4]),
 (V+211, "GEBUESCH", False, "sauber", "Dunkler Streifen am rechten Kernrand östlich der Straße, Rand der Gehölzgruppe 209 oder Schatten.", [], [U, N4, R4]),
 (V+218, "GEBUESCH", False, "sauber", "Dunkle rundliche Flecken am unteren rechten Kernrand neben der Straße.", [], [U, N4, R4]),
 (V+215, "HOF", False, "sauber", "Nur 22 Bildpunkte im Kern; Rand einer grauen Fläche östlich der Straße in r0c1.", [], [U, N4]),
 (V+224, "FELDRAIN", False, "sauber", "Kleiner grauer Randstreifen links des Feldwegs 220 am unteren Kernrand.", [], [U, N3, E5]),
 (V+220, "FELDWEG", False, "sauber", "Heller schmaler Streifen nach Süden an der Feldecke unten links.", [], [U, R, N3, E5]),
 (V+225, "GEBUESCH", False, "sauber", "Kleiner dunkler Fleck am unteren Kernrand rechts des Feldwegs.", [], [U, N3, E5]),
 (V+219, "FELD", False, "sauber", "Hellere Parzelle unter Feld 195 mit klarer Kante: eigene Bewirtschaftung.", [], [U, R, N4, R4]),
 (V+228, "FELD", False, "sauber", "Nur 21 Bildpunkte im Kern; Teil der hellen Parzelle wie 219.", [], [U, N4]),
 (V+229, "BANKETT", False, "sauber", "Nur 19 Bildpunkte im Kern am unteren Kernrand neben der Straße.", [], [U, N4]),
]

EINGRIFFE = [
 {"schritt": "teilen", "vorher": [V+143], "nachher": [V+143, V+275, V+276, V+277, V+278, V+279],
  "grund": "Das helle Straßenband östlich von 149 (436–478/272–352) steckte im beschatteten Hofsegment 143 und wurde entlang seiner Ostkante abgeschnitten."},
 {"schritt": "verschmelzen", "vorher": [V+143, V+275, V+277, V+278], "nachher": [V+143],
  "grund": "Drei kleine Splitter des Schnitts ohne eigene Bildkante wieder dem Hofsegment 143 zugeschlagen."},
]
NAHT = [
 {"id": V+176, "seite": "rechts", "text": "Hofsegment 176 reicht weit nach r0c1/r1c1 und enthält helle Längsbauten über den Kernrand; dort einheitlich teilen, nicht nur im Kern."},
 {"id": V+198, "seite": "unten", "text": "Straße 198 läuft über den unteren rechten Kernrand weiter; Klasse Straße auf beiden Seiten."},
 {"id": V+195, "seite": "unten", "text": "Feld 195 reicht über den unteren Kernrand nach r1c0/r1c1; Klasse Feld auf beiden Seiten."},
 {"id": V+165, "seite": "rechts", "text": "Gebäude 165 liegt zum größten Teil in r0c1; die Klasse Gebäude gilt nur, wenn r0c1 den Bau ebenso sieht."},
]
UNSICHER = [
 "100154 (v3): Grenze zu 195 ohne Bildkante; dieselbe Feldfläche, gemeinsame Klasse Feld.",
 "100149 (v2): Straßenband westlich von 276; gleiche Klasse Straße wie 276/279.",
 "100169 (v2): dunkle Krone, mit 172 eine Baumreihe am Westrand der Straße.",
]
NICHT_GEPRUEFT = [
 "Naht zu r0c1, r1c0 und r1c1 nur von dieser Seite angesehen.",
 "Der Schnitt an 143 wurde vom ersten Bearbeiter dieses Viertels gesetzt; ich habe ihn am Bild nachgesehen (umriss.jpg, nah2), nicht neu gesetzt.",
]
OFFEN = [
 "Felder 195, 219, 228 und Saum 199: Acker oder Grünland auf Schwarz-Weiß nicht zu trennen; im Farbbild entscheidet Grün gegen Braun und Furchenmuster.",
 "Straßen 198, 276, 279, 191, 193 und Gasse 186: Belag nicht bestimmbar; 276 könnte Gehweg statt Fahrbahn sein.",
 "143: dunkler Keil 470–530/300–390 Schatten oder dunkler Boden; im Farbbild bzw. bei anderem Sonnenstand zu klären.",
 "183, 194, 207, 209, 210, 211, 216, 218, 225: Baum, Busch, Hecke oder Graben mit Schatten; im Farbbild Grün der Kronen.",
 "178, 189, 192, 196: Hof, Garten oder Platz nicht zu trennen; im Farbbild Pflaster gegen Rasen.",
 "185: kleines helles Längsobjekt 444–454/365–370 (Schuppen, Fahrzeug, Haufen) nicht bestimmbar und unter der Mindestfläche.",
 "Grenze 154|195 zackig ohne Bildkante: beide gleiche Klasse Feld; Grenze besser entlang eines Bewirtschaftungsstreifens oder Zusammenlegung (betrifft 154 in v3).",
]

# --- Bilder ---
FX, FY, FW, F = 282, 282, 314, 3
font = ImageFont.truetype("arial.ttf", 15)
fontk = ImageFont.truetype("arial.ttf", 13)

def basis(kontrast=False):
    a = img[FY:FY+FW, FX:FX+FW].astype(float)
    big = np.kron(a, np.ones((F, F))).astype(np.uint8)
    return np.stack([big]*3, -1)

def kanten(l):
    lb = np.kron(l, np.ones((F, F), dtype=l.dtype))
    e = np.zeros(lb.shape, bool)
    e[:, 1:] |= lb[:, 1:] != lb[:, :-1]
    e[1:, :] |= lb[1:, :] != lb[:-1, :]
    return e

def viertel(d):
    d.rectangle([(314-FX)*F, (314-FY)*F, (564-FX)*F, (564-FY)*F], outline=(0, 255, 255), width=2)

def kopf(im, text):
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, im.width, 22], fill=(0, 0, 0))
    d.text((4, 3), text, fill=(255, 255, 0), font=font)

l = lab[FY:FY+FW, FX:FX+FW]
ids = [s[0] for s in S]

im = Image.fromarray(basis()); viertel(ImageDraw.Draw(im)); kopf(im, "r0c0 v4: Rohbild, Viertel cyan (x 314–563, y 314–563)")
im.save(OUT + "roh.jpg", quality=90)

def labels_zeichnen(d, l, farbe=lambda i: (255, 255, 255), text=lambda i: str(i % 100000)):
    for i in np.unique(l):
        m = l == i
        if m.sum() < 10:
            continue
        dist = ndimage.distance_transform_edt(np.pad(m, 1))[1:-1, 1:-1]
        yy, xx = np.unravel_index(dist.argmax(), m.shape)
        t = text(i)
        if t:
            d.text((xx*F - 10, yy*F - 7), t, fill=farbe(i), font=fontk, stroke_width=2, stroke_fill=(0, 0, 0))

rgb = basis(); rgb[kanten(l)] = [255, 230, 0]
im = Image.fromarray(rgb); d = ImageDraw.Draw(im); viertel(d)
labels_zeichnen(d, l, farbe=lambda i: (255, 255, 255) if i in ids else (170, 170, 170))
kopf(im, "r0c0 v4: Segmentgrenzen nach dem Nachsegmentieren, weiß = dieses Viertel")
im.save(OUT + "umriss.jpg", quality=90)

# Mängel
rgb = basis(); rgb[kanten(l)] = [200, 200, 0]
im = Image.fromarray(rgb); d = ImageDraw.Draw(im); viertel(d)
leg = []
nr = 0
for sid, k, sic, urt, was, pk, b in S:
    for art, text, (x, y), fl in pk:
        nr += 1
        cx, cy = (x-FX)*F, (y-FY)*F
        d.ellipse([cx-11, cy-11, cx+11, cy+11], fill=(220, 30, 30), outline=(255, 255, 255))
        d.text((cx-5 if nr < 10 else cx-8, cy-8), str(nr), fill=(255, 255, 255), font=font)
        leg.append(f"{nr} ({sid % 100000}, {art}): {text}")
H = 22 + 18*len(leg)*2 + 10
out = Image.new("RGB", (im.width, im.height + H), (0, 0, 0)); out.paste(im, (0, 0))
d = ImageDraw.Draw(out); y = im.height + 6
for t in leg:
    # umbrechen
    zeilen, z = [], ""
    for w in t.split():
        if d.textlength(z + " " + w, font=fontk) > out.width - 12:
            zeilen.append(z); z = w
        else:
            z = (z + " " + w).strip()
    zeilen.append(z)
    for zz in zeilen:
        d.text((6, y), zz, fill=(255, 255, 255), font=fontk); y += 17
out = out.crop((0, 0, out.width, y + 6))
kopf(out, "r0c0 v4: Mängel (rote Punkte, Legende unten)")
if out.height > 2000:
    out = out.resize((int(out.width*2000/out.height), 2000))
out.save(OUT + "maengel.jpg", quality=90)

# Vorschlag: Klassen farbig (mittlere Ebene)
FARBE = {"Hof": (200, 140, 60), "Gebäude": (220, 60, 60), "Straße": (240, 240, 240), "Weg": (250, 220, 150),
         "Straßenrand": (170, 170, 170), "Baum": (20, 120, 20), "Baumreihe": (40, 160, 40), "Gebüsch": (90, 170, 60),
         "Saum": (170, 220, 120), "Feld": (230, 210, 80)}
rgb = basis().astype(float)
for sid, k, *_ in S:
    m = np.kron(l == sid, np.ones((F, F))).astype(bool)
    rgb[m] = rgb[m]*0.55 + np.array(FARBE[KL[k][1]])*0.45
rgb = rgb.astype(np.uint8); rgb[kanten(l)] = [255, 230, 0]
im = Image.fromarray(rgb); d = ImageDraw.Draw(im); viertel(d)
klmap = {s[0]: KL[s[1]][2] for s in S}
labels_zeichnen(d, l, text=lambda i: (f"{i % 100000} {klmap[i]}" if i in klmap else ""))
# vorgeschlagene Änderung: Grenze 154|195 entfällt (gestrichelt markieren)
b = (l == V+195) & ndimage.binary_dilation(l == V+154)
ys, xs = np.nonzero(b)
for x, y in zip(xs[::3], ys[::3]):
    d.ellipse([x*F, y*F, x*F+3, y*F+3], fill=(255, 0, 255))
leg = ["Farbe = mittlere Ebene: " + ", ".join(f"{n}" for n in FARBE), "Magenta: Grenze 154|195 ohne Bildkante, Vorschlag beide Feld (zusammenlegen)",
       "176: Längsbauten bei 535–563/387–424 und 544–563/442–486 abtrennen (mit r0c1/r1c1)"]
out = Image.new("RGB", (im.width, im.height + 20*len(leg) + 10), (0, 0, 0)); out.paste(im, (0, 0))
d = ImageDraw.Draw(out)
for j, t in enumerate(leg):
    d.text((6, im.height + 5 + 20*j), t, fill=(255, 255, 255), font=fontk)
kopf(out, "r0c0 v4: Vorschlag (freie Klassen, fein)")
out.save(OUT + "vorschlag.jpg", quality=90)

# --- urteil.json ---
segs = []
for sid, k, sic, urt, was, pk, b in S:
    g, m_, f = KL[k]
    segs.append({"id": sid, "klasse_heute": seg[sid]["klasse"], "was_ist_es": was, "urteil": urt,
                 "klasse_vorschlag": None, "klasse_frei": {"grob": g, "mittel": m_, "fein": f}, "sicher": sic,
                 "punkte": [{"nr": i+1, "art": a, "text": t, "flaeche_px": fl} for i, (a, t, _, fl) in enumerate(pk)],
                 "bilder": b})
alle_nah = [N1, R2, N2, N3, N4, R4, E4, E5, K2, OUT + "nah_2.jpg"]
u = {"teilkachel": "r0c0", "viertel": "v4", "bearbeiter": "urt-b-r0c0-v4",
     "bilder_angesehen": {"uebersicht": [D + "/H0.png", D + "/ganz/r0c0/ganz_nummern.jpg", U, R, K, OUT + "umriss.jpg"],
                          "nah": alle_nah},
     "segmente": segs, "naht": NAHT, "unsicher": UNSICHER, "nicht_geprueft": NICHT_GEPRUEFT, "offen": OFFEN,
     "eingriffe": EINGRIFFE,
     "klassen_frei": [{"name": n, "ebene": e, "eltern": p, "merkmal": mk} for n, e, p, mk in KLASSEN_FREI]}
json.dump(u, open(OUT + "urteil.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(segs), sum(s["urteil"] == "nicht_sauber" for s in segs), sum(len(s["punkte"]) for s in segs), sum(not s["sicher"] for s in segs))
