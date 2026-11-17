"""Fassung C, r0c0: kategorien-teil.json, segmente.json und ergebnis.jpg aus bauen.py-Ergebnis."""
import json
import sys
from collections import Counter
from datetime import datetime, timezone

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, "C:/Users/Phil/Developement/Victor/landseg")
from landseg.dateien import lese_labels  # noqa: E402

BASIS = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c"
AUS = BASIS + "/abgabe/r0c0"

KL = [
    ("1", "Bebaut / versiegelt", "#9e3a36", "graue, rote oder helle Flächen mit geraden Kanten"),
    ("1.1", "Gebäude", "#c62828", "Dachfläche mit Firsten, Gauben oder Flachdachrand"),
    ("1.1.1", "Wohngebäude (Hauptdach)", "#ef5350", "großes Dach, Ziegel rot, grau oder Flachdach mit Attika"),
    ("1.1.2", "Nebengebäude / Anbau / Gartenhaus", "#ff8a65", "kleines Dach, an Haus angebaut oder frei im Garten"),
    ("1.2", "Verkehrs- und Hofflächen", "#78909c", "befestigte, befahr- oder begehbare Flächen"),
    ("1.2.1", "Straße (Asphalt)", "#424242", "dunkelgraues Band mit gleichmäßiger Breite"),
    ("1.2.2", "Hof / Zufahrt / Platz / Randstreifen", "#bdbdbd", "hellgraue Beton- oder Pflasterfläche an Straße und Haus"),
    ("1.2.3", "Terrasse / Gartenweg / Beckenumrandung", "#e0c09a", "helle Platten oder Pflaster direkt am Haus oder Becken"),
    ("1.3", "Bauliche Kleinanlagen", "#5d6d7e", "kleine gebaute Elemente ohne Dach"),
    ("1.3.1", "Schwimmbecken", "#29b6f6", "Rechteck mit hellem Rand, Wasser türkis oder graue Abdeckung"),
    ("1.3.2", "Mauer / Einfassung (linear)", "#8d6e63", "schmale helle Linie, oft mit Schattenband"),
    ("2", "Garten / Siedlungsgrün", "#ab47bc", "Grün innerhalb eingefriedeter Grundstücke"),
    ("2.1", "Rasen (gepflegt)", "#d4e157", "gleichmäßig kurzes Grün, scharf begrenzt"),
    ("2.2", "Ziergarten gemischt", "#f06292", "kleinteiliges Nebeneinander von Rasen, Beet, Gehölz, Gegenständen"),
    ("2.3", "Gartenhecke (geschnitten, linear)", "#6a1b9a", "schmales gerades oder gebogenes Gehölzband an der Grundgrenze"),
    ("2.4", "Gartengehölz (Strauch, Kleinbaum)", "#ce93d8", "Kronen im Garten, oft Ziergehölz oder Konifere"),
    ("2.5", "Gartenausstattung", "#ffd54f", "Spielgerät, Paletten, runde Objekte im Rasen"),
    ("3", "Offenland (krautig)", "#9ccc65", "Gras- und Krautflächen ohne Gehölz"),
    ("3.1", "Wiese / Grünland", "#8bc34a", "geschlossene grüne Krautschicht"),
    ("3.1.1", "Wiese ungemäht (Altgras, Kräuter)", "#7cb342", "körnig-raue Textur, hellere Blüten- und Altgrasflecken"),
    ("3.1.2", "Wiese gleichmäßig niedrig", "#c0ca33", "glatte, hellere Textur ohne Struktur"),
    ("3.1.3", "Böschung / Straßenbegleitgrün", "#00e676", "schmaler Grasstreifen entlang Straße oder Hecke"),
    ("3.2", "Gemähte Fläche mit Schwaden", "#e6c27a", "strohgelb-braun mit parallelen gebogenen Streifen"),
    ("3.3", "Verbuschte Wiese (Gebüsch-Hochstauden-Mosaik)", "#827717", "Wiese mit vielen kleinen Sträuchern, fleckig dunkel-hell"),
    ("4", "Gehölz (freie Landschaft)", "#1b5e20", "Baumkronen und Sträucher außerhalb der Gärten"),
    ("4.1", "Baum (Einzelkrone)", "#2e7d32", "runde bis gelappte Krone, deutlich höher als Umgebung, wirft Schatten"),
    ("4.1.1", "Laubbaum", "#00897b", "gelappte Krone, hier eindeutig an rotem Laub (Blutbuche)"),
    ("4.2", "Baumgruppe / Gehölzbestand", "#004d40", "mehrere verwachsene Kronen, keine Einzelkrone abgrenzbar"),
    ("4.2.1", "Laubholz-Bestand", "#26a69a", "viele helle, gelappte Kronen dicht an dicht"),
    ("4.3", "Gebüsch / Strauch", "#66bb6a", "kleine dunkle Krone unter etwa 25 m², kaum Schatten"),
    ("5", "Sonstiges", "#795548", "nicht Bewuchs und nicht gebaut"),
    ("5.1", "Holzhaufen / Schnittgut", "#a1887f", "helle Stämme und Äste kreuz und quer"),
    ("5.2", "Schlagschatten", "#263238", "sehr dunkle Fläche neben Haus oder Hecke, Untergrund kaum erkennbar"),
]
FARBE = {c: f for c, _, f, _ in KL}
NAME = {c: n for c, n, _, _ in KL}

def eltern(code):
    return code.rsplit(".", 1)[0] if "." in code else None

kat = {"schema": "landseg-kategorien/1", "teilkachel": "r0c0",
       "title": "Eigene gestufte Liste, Fassung C, Teilkachel r0c0",
       "classes": [{"code": c, "name": n, "parent": eltern(c), "level": c.count(".") + 1,
                    "color": f, "image_cue": cue} for c, n, f, cue in KL]}
json.dump(kat, open(AUS + "/kategorien-teil.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

L = lese_labels(AUS + "/labels.tif")
roh = json.load(open(AUS + "/arbeit/segmente_roh.json", encoding="utf-8"))["segmente"]
offen, kern_unsicher = [], 0
for e in roh:
    assert e["klasse"] in FARBE, e
    if e["im_kern"] and not e["sicher"]:
        kern_unsicher += 1
        offen.append(f"Segment {e['id']} ({NAME[e['klasse']]}, {e['name']}): "
                     + (e.get("notiz") or "Klasse nach Bild nicht eindeutig"))
offen += [
    "Dunkle Kronen (viele 4.1/4.2): wahrscheinlich Nadelbäume oder beschattete Kronen; Nadel/Laub bewusst nicht vergeben, "
    "bei Segmenten im Gehölzrand südlich der Wiese auch Schlagschatten des Bestands möglich.",
    "Grenze zwischen offener Wiese (3.1.1) und verbuschter Wiese (3.3) von Hand als Linienzug gezogen; dort gibt es keine scharfe Bildkante.",
    "In der verbuschten Wiese ein schmaler heller Trampelpfad (etwa 2 Bildpunkte breit) sichtbar, nicht als eigenes Segment ausgeschieden.",
    "Schwaden-Fläche (3.2): ob Getreide-Stoppel mit Stroh oder gemähte Wiese mit Heu, ist im Bild nicht zu entscheiden.",
    "Kontextrand (außerhalb des Kerns) nur grob nachgesehen; Klassen dort zählen nicht.",
]
segmente = []
for e in roh:
    s = {k: e[k] for k in ("id", "klasse", "grob", "name", "im_kern", "sicher", "flaeche", "flaeche_kern", "vorstufe")}
    if e.get("notiz"):
        s["notiz"] = e["notiz"]
    segmente.append(s)
doc = {"schema": "landseg-segmente/1", "teilkachel": "r0c0", "fassung": "C",
       "segmente": segmente,
       "verlauf": [{"zeit": datetime.now(timezone.utc).isoformat(timespec="seconds"), "bearbeiter": "fassung-c-r0c0",
                    "op": "neu_aufgebaut",
                    "beschreibung": "Vorstufe als Ausgang, alle IDs neu zugeordnet und verschmolzen, große Wiese per Linienzug geteilt, "
                                    "Hecke/Schatten zeilenweise nach Helligkeit getrennt, Terrasse, Gartenhaus, Mauer, rundes Objekt per Polygon; "
                                    "Splitter unter 75 Bildpunkten an den Nachbarn mit der längsten Grenze (Skripte bauen.py, abschluss.py)"}],
       "offen": offen, "nicht_geprueft": []}
json.dump(doc, open(AUS + "/segmente.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# ergebnis.jpg
img = np.asarray(Image.open(BASIS + "/teilkacheln/r0c0.png").convert("RGB")).astype(np.float32)
S = 2
H, W = L.shape
farb = np.zeros((H, W, 3), np.float32)
klasse = {e["id"]: e["klasse"] for e in roh}
for sid, kl in klasse.items():
    h = FARBE[kl].lstrip("#")
    farb[L == sid] = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
mix = (img * 0.55 + farb * 0.45).clip(0, 255).astype(np.uint8)
big = cv2.resize(mix, (W * S, H * S), interpolation=cv2.INTER_NEAREST)
Lb = cv2.resize(L.astype(np.float32), (W * S, H * S), interpolation=cv2.INTER_NEAREST).astype(np.int64)
rand = np.zeros(Lb.shape, bool)
rand[:-1] |= Lb[:-1] != Lb[1:]; rand[:, :-1] |= Lb[:, :-1] != Lb[:, 1:]
big[rand] = (255, 255, 255)
cv2.rectangle(big, (64 * S, 64 * S), (564 * S - 1, 564 * S - 1), (0, 255, 255), 2)
for e in roh:
    m = L == e["id"]
    d = cv2.distanceTransform(np.pad(m, 1).astype(np.uint8), cv2.DIST_L2, 3)[1:-1, 1:-1]
    yy, xx = np.unravel_index(d.argmax(), d.shape)
    t = str(e["id"]) + ("" if e["sicher"] else "?")
    p = (int(xx * S) - 4 * len(t), int(yy * S) + 4)
    cv2.putText(big, t, p, cv2.FONT_HERSHEY_SIMPLEX, 0.38, (0, 0, 0), 3)
    cv2.putText(big, t, p, cv2.FONT_HERSHEY_SIMPLEX, 0.38, (255, 255, 255), 1)
legbreite = 460
leinw = Image.new("RGB", (W * S + legbreite, H * S), (250, 250, 250))
leinw.paste(Image.fromarray(big), (0, 0))
dr = ImageDraw.Draw(leinw)
try:
    f = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 15); fb = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 17)
except OSError:
    f = fb = ImageFont.load_default()
x0 = W * S + 14
dr.text((x0, 10), "r0c0, Fassung C: Klassen (Segmente im Kern)", fill=(0, 0, 0), font=fb)
zahl = Counter(e["klasse"] for e in roh if e["im_kern"])
y = 40
for c, n, fa, _ in KL:
    ein = "    " * c.count(".")
    unter = sum(v for k, v in zahl.items() if k == c or k.startswith(c + "."))
    dr.rectangle([x0, y + 2, x0 + 16, y + 16], fill=fa, outline=(0, 0, 0))
    gew = fb if "." not in c else f
    dr.text((x0 + 24, y), f"{ein}{c} {n} ({unter})", fill=(0, 0, 0), font=gew)
    y += 21 if "." in c else 24
y += 10
dr.text((x0, y), "Cyan: Kern 500 × 500. Weiß: Segmentgrenzen.", fill=(0, 0, 0), font=f); y += 20
dr.text((x0, y), "Zahl = Segment-ID, „?“ = sicher: false.", fill=(0, 0, 0), font=f)
leinw.save(AUS + "/ergebnis.jpg", quality=90)
print("Segmente", len(roh), "im Kern", sum(e["im_kern"] for e in roh), "unsicher im Kern", kern_unsicher,
      "unsicher gesamt", sum(not e["sicher"] for e in roh))
ebenen = Counter(c.count(".") + 1 for c, *_ in KL)
print("Klassen je Ebene", dict(ebenen))
