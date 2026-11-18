"""Ergänzt segmente.json um offen / nicht_geprueft, zeichnet ergebnis.jpg mit Legende, druckt Zahlen."""
import json
from collections import Counter
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont

AB = Path(__file__).resolve().parent.parent
BILD = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r1c1.png"
img = np.array(Image.open(BILD).convert("L")).astype(np.float32)
L = tifffile.imread(AB / "labels.tif")
sp = AB / "segmente.json"
daten = json.loads(sp.read_text(encoding="utf-8"))
segs = daten["segmente"]
kat = json.loads((AB / "kategorien-teil.json").read_text(encoding="utf-8"))["classes"]
kd = {c["code"]: c for c in kat}

kern = [s for s in segs if s["im_kern"]]
quellen = Counter(s["quelle"] for s in kern)
daten["offen"] = [
    "Dach gegen Hof: helle, glatte Flächen ohne deutliche Traufkante sind als Dach (1.1/1.1.1) oder Hof (1.2) "
    "nur nach Grauton und Form zugeordnet; im Farbbild entscheiden Dachfarbe (Ziegelrot) gegen Pflaster/Erde.",
    "Dachhälften: 1.1.1/1.1.2 und 1.1 der Grauregel (Quelle 'grauregel', %d Segmente im Kern) sind nur nach "
    "Grauton vorklassifiziert und nicht einzeln bestätigt; eine Dachfläche kann ebenso Hof oder Garten sein." % quellen.get("grauregel", 0),
    "Garten gegen Wiese/Acker im Blockinneren (1.3): im Farbbild trennen Beete, Obstbäume und Wiesengrün.",
    "Feld nordwestlich der Trift und Nordwestecke: Acker oder Grünland (Klasse 3), im Farbbild nach Bewuchs zu trennen.",
    "Trift (2.3): Weg, Viehtrift oder Brachstreifen; im Farbbild Fahrspuren gegen Grasnarbe.",
    "Gehölzsaum (4.1) an der Dorfstraße West: Baumreihe oder Hecke; Einzelkronen fließen auf 0,45 m ineinander, "
    "darum keine Einzelbäume.",
    "Heller Rechteckfleck am Straßenrand (Klasse 1, um x 210, y 282): Flachdach, Lagerplatz oder Belag.",
    "Schattenflächen (5) verdecken den Untergrund; was darunter liegt (Straße, Hof, Dach), ist offen.",
    "Grenzen der Atome folgen Felzenszwalb-Kanten, Straßen dem Helligkeitsumschlag; von Hand gesetzt sind nur "
    "der Rechteckfleck, das schmale Straßenstück Mitte (x 302-320, y 56-116) und eine verlängerte Fuge (233,114)-(252,126).",
]
daten["nicht_geprueft"] = [
    "Kontextrand (außerhalb x/y 64-564): nur nach Grauregel und Objektvorgaben, nicht einzeln angesehen.",
    "Im Kern sind alle Ortsbereiche in 12 Prüfbildern (130 bzw. 175 Bildpunkte, vier- bis fünffach) angesehen, der Acker im Südwesten (x 64-225, y 395-564) nur in der Gesamtansicht zweifach; einzeln bestätigt oder "
    "umklassifiziert wurden nur die Segmente mit Quelle 'korrektur'. Die übrigen Ortssegmente stehen mit sicher: false.",
    "Einzelne Parzellen der Streifenflur im Acker Südwest sind nicht getrennt (Grenzen zu schwach).",
    "Kein Abgleich mit den Nachbar-Teilkacheln (Nahtregel) in dieser Fassung.",
]
sp.write_text(json.dumps(daten, ensure_ascii=False, indent=1), encoding="utf-8")

# Ergebnisbild
f = 2
farbe = np.zeros((L.max() + 1, 3), np.float32)
for s in segs:
    h = kd[s["klasse"]]["color"]
    farbe[s["id"]] = [int(h[i:i + 2], 16) for i in (1, 3, 5)]
rgb = np.stack([img] * 3, -1) * 0.55 + farbe[L] * 0.45
big = np.repeat(np.repeat(rgb, f, 0), f, 1)
lb = np.repeat(np.repeat(L, f, 0), f, 1)
rand = np.zeros(lb.shape, bool)
rand[:, 1:] |= lb[:, 1:] != lb[:, :-1]
rand[1:, :] |= lb[1:, :] != lb[:-1, :]
big[rand] = (255, 235, 0)
H, W = L.shape
breite_leg = 600
out = Image.new("RGB", (W * f + breite_leg, H * f), (255, 255, 255))
out.paste(Image.fromarray(big.clip(0, 255).astype(np.uint8)), (0, 0))
d = ImageDraw.Draw(out)
d.rectangle([64 * f, 64 * f, 564 * f, 564 * f], outline=(255, 0, 255), width=3)
ft = ImageFont.truetype("arialbd.ttf", 20)
fn = ImageFont.truetype("arial.ttf", 15)
x0 = W * f + 16
y = 14
d.text((x0, y), "H0 r1c1 – Fassung A „Alles frei“", fill=(0, 0, 0), font=ft)
y += 30
d.text((x0, y), "SW-Scan 1968, ca. 0,45 m je Bildpunkt", fill=(60, 60, 60), font=fn)
y += 22
d.text((x0, y), f"{len(segs)} Segmente, davon {len(kern)} im Kern (magenta)", fill=(60, 60, 60), font=fn)
y += 22
d.text((x0, y), "gelb: Segmentgrenzen", fill=(60, 60, 60), font=fn)
y += 32
anz = Counter(s["klasse"] for s in kern)
for c in kat:
    einr = 22 * (c["level"] - 1)
    d.rectangle([x0 + einr, y + 2, x0 + einr + 22, y + 20], fill=c["color"], outline=(0, 0, 0))
    txt = f'{c["code"]}  {c["name"]}'
    if len(txt) > 52 - 3 * c["level"]:
        txt = txt[:50 - 3 * c["level"]] + "…"
    d.text((x0 + einr + 30, y + 2), f"{txt} ({anz.get(c['code'], 0)})", fill=(0, 0, 0), font=fn)
    y += 28
y += 10
d.text((x0, y), "(Zahl) = Segmente der Klasse im Kern", fill=(90, 90, 90), font=fn)
out.save(AB / "ergebnis.jpg", quality=90)

print("Segmente", len(segs), "im Kern", len(kern))
print("unsicher im Kern", sum(1 for s in kern if not s["sicher"]), "unsicher gesamt", sum(1 for s in segs if not s["sicher"]))
print("Quellen im Kern", dict(quellen))
print("Klassen im Kern", dict(anz))
print("Ebenen", Counter(c["level"] for c in kat))
