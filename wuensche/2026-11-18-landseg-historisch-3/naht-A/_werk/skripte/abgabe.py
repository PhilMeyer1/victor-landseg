"""Abgabe der Naht-Klärung Fassung A, H0: naht_abgabe.json, naht_<n>.jpg, Probe-Auftrag."""
import json
import os
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont

H0 = Path("C:/Users/Phil/Developement/Victor/daten/landseg/H0")
D = H0 / "a-alles-frei"
E = Path("C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/naht-A")
W = E / "_werk"
BEARBEITER = "agent:naht-A:20261118i"
tab = json.load(open(W / "tabelle.json", encoding="utf-8"))
bild = np.asarray(Image.open(H0 / "H0.png").convert("L"), dtype=np.float32)
karte = tifffile.imread(D / "zusammen/labels.tif")
try:
    font = ImageFont.truetype("arial.ttf", 15)
    fontk = ImageFont.truetype("arial.ttf", 13)
except OSError:
    font = fontk = ImageFont.load_default()

SENKRECHT = {"r0c0|r0c1", "r1c0|r1c1"}


def seiten(naht):
    return ("links", "rechts") if naht in SENKRECHT else ("oben", "unten")


def text(z):
    a, b = seiten(z["naht"])
    ka, kb = z["ka"], z["kb"]
    sa = f"{a} {z['ids'][0]} „{z['na']}“ ({ka})"
    sb = f"{b} {z['ids'][1]} „{z['nb']}“ ({kb})"
    if "1.2" in (ka, kb) and ka != kb:
        return (f"Keine Bildkante an der Kerngrenze: dieselbe Hoffläche läuft durch, eine Teilkachel fasst sie als "
                f"ungetrennten Block, die andere fein in Einzelflächen ({sa}; {sb}).")
    if ka == kb or ka.split(".")[0] == kb.split(".")[0]:
        return (f"Keine Bildkante an der Kerngrenze: dieselbe Fläche setzt sich über die Naht fort, nur die IDs der "
                f"beiden Teilkacheln sind verschieden ({sa}; {sb}).")
    return (f"Keine Bildkante an der Kerngrenze: die Fläche läuft durch, die beiden Teilkacheln haben ihre Grenze "
            f"versetzt bzw. verschieden fein gezogen ({sa}; {sb}).")


def kontrast(a):
    lo, hi = np.percentile(a, [1, 99])
    return np.clip((a - lo) / max(hi - lo, 1) * 255, 0, 255).astype(np.uint8)


def tafel(z, ueberschrift):
    senk = z["naht"] in SENKRECHT
    if senk:
        s0, s1 = z["von"][1], z["bis"][1] + 1
        lage = 500
    else:
        s0, s1 = z["von"][0], z["bis"][0] + 1
        lage = 500
    rand = max(15, (40 - (s1 - s0)) // 2)
    l0, l1 = max(0, s0 - rand), min(1000, s1 + rand)
    q0, q1 = lage - 20, lage + 20
    if senk:
        y0, y1, x0, x1 = l0, l1, q0, q1
    else:
        y0, y1, x0, x1 = q0, q1, l0, l1
    h, w = y1 - y0, x1 - x0
    S = max(3, min(10, 640 // max(h, w)))
    g = kontrast(bild[y0:y1, x0:x1])
    rgb = np.kron(np.stack([g] * 3, -1), np.ones((S, S, 1), np.uint8))
    p = Image.fromarray(rgb)
    dr = ImageDraw.Draw(p)
    k = karte[y0:y1, x0:x1]
    for yy in range(h):
        for xx in range(1, w):
            if k[yy, xx] != k[yy, xx - 1]:
                dr.line([(xx * S, yy * S), (xx * S, (yy + 1) * S)], fill=(255, 50, 50), width=1)
    for yy in range(1, h):
        for xx in range(w):
            if k[yy, xx] != k[yy - 1, xx]:
                dr.line([(xx * S, yy * S), ((xx + 1) * S, yy * S)], fill=(255, 50, 50), width=1)
    if senk:
        X = (lage - x0) * S
        for t in range(0, h * S, 10):
            dr.line([(X, t), (X, t + 5)], fill=(255, 225, 0), width=1)
        dr.rectangle([(X - 3, (s0 - y0) * S), (X + 3, (s1 - y0) * S - 1)], outline=(0, 200, 255), width=2)
    else:
        Y = (lage - y0) * S
        for t in range(0, w * S, 10):
            dr.line([(t, Y), (t + 5, Y)], fill=(255, 225, 0), width=1)
        dr.rectangle([((s0 - x0) * S, Y - 3), ((s1 - x0) * S - 1, Y + 3)], outline=(0, 200, 255), width=2)
    rahmen = Image.new("RGB", (max(p.width, 270), p.height + 24), (255, 255, 255))
    rahmen.paste(p, (0, 24))
    ImageDraw.Draw(rahmen).text((4, 4), ueberschrift, fill=(0, 0, 0), font=font)
    return rahmen


def zeilen_umbruch(t, breite, d):
    worte, zeilen, z = t.split(), [], ""
    for wort in worte:
        probe = (z + " " + wort).strip()
        if d.textlength(probe, font=fontk) > breite and z:
            zeilen.append(z)
            z = wort
        else:
            z = probe
    zeilen.append(z)
    return zeilen


verstoesse = []
for z in tab:
    t = text(z)
    verstoesse.append({"naht": z["naht"], "ids": z["ids"], "art": "ohne_kante", "entscheidung": "offen",
                       "teilkachel": None,
                       "text": f"Verstoß {z['n']} ({z['laenge']} Bildpunkte ab x {z['von'][0]}, y {z['von'][1]}): " + t})
    vor = tafel(z, "vorher")
    nach = tafel(z, "nachher (unverändert, offen)")
    breite = vor.width * 2 + 12
    tmp = Image.new("RGB", (max(breite, 640), 10))
    erste = (f"Verstoß {z['n']}: Naht {z['naht']}, Segmente {z['ids'][0]} | {z['ids'][1]}, "
              f"{z['laenge']} Bildpunkte ab x {z['von'][0]}, y {z['von'][1]}, Kantenstärke höchstens {z['kante']:.0f} (Schwelle 25)")
    zeilen = zeilen_umbruch(erste, max(breite, 640) - 10, ImageDraw.Draw(tmp))
    zeilen += zeilen_umbruch("Entscheidung: offen. " + t, max(breite, 640) - 10, ImageDraw.Draw(tmp))
    zeilen.append("Gelb gestrichelt: Kerngrenze; rot: Segmentgrenzen; blau: Strecke des Verstoßes.")
    unten = 8 + 17 * len(zeilen)
    ges = Image.new("RGB", (max(breite, 640), vor.height + unten), (255, 255, 255))
    ges.paste(vor, (0, 0))
    ges.paste(nach, (vor.width + 12, 0))
    d = ImageDraw.Draw(ges)
    for i, zl in enumerate(zeilen):
        d.text((5, vor.height + 4 + 17 * i), zl, fill=(0, 0, 0), font=fontk)
    if max(ges.size) > 2000:
        f = 2000 / max(ges.size)
        ges = ges.resize((int(ges.width * f), int(ges.height * f)))
    ges.save(E / f"naht_{z['n']}.jpg", quality=88)

# offen, gruppiert je Naht und ID-Paar
offen = [
    "Alle 187 Verstöße: An keiner der vier Kerngrenzen liegt eine echte Bildkante auf der Naht; die Flächen laufen durch. "
    "Fassung A hat jede Teilkachel frei mit eigenem ID-Bereich abgegeben (r0c0 ab 100000, r0c1 ab 200000, r1c0 ab 300000, "
    "r1c1 ab 400000), darum trägt kein Kontextrand eine ID der Gegenseite. `eingriff` schreibt nur IDs, die in der Karte "
    "schon vorkommen (verschmelzen, polygon, verschieben prüfen das), also lässt sich keine Seite an die andere angleichen. "
    "Klären würde es eine Operation, die einem Kernsegment die ID der Gegenseite gibt (Umnummern über die Naht, etwa als "
    "Feld im zusammentragen-Auftrag oder als eingriff-Op mit fremder Ziel-ID), oder ein gemeinsamer Ausgang mit globalen IDs.",
    "Nach dem Angleichen bleiben Klassenunterschiede an denselben Stellen (z. B. 1.2 Hofstelle-Block in r0c0 gegen 1.1/2.1/2.2/0.1 "
    "in r0c1; 5.1.3 heller Streifen in r1c0 gegen 3.2 Trift in r1c1; 4.2 gegen 5.1 an r0c0|r1c0); die entscheidet die Einigung (L13).",
    "Versetzte Grenzen (eine Seite zieht ein Haus, einen Weg oder einen Rain bis an die Naht, die andere nicht oder einige "
    "Bildpunkte versetzt, etwa Verstöße 2, 3, 77, 84, 87, 173–175, 185) brauchen nach dem Angleichen ein `verschieben` "
    "im Kern der falschen Seite; ohne gemeinsame ID bliebe jeder dieser Fälle ein Verstoß, darum hier nicht geändert.",
]
paare = {}
for v in verstoesse:
    paare.setdefault(v["naht"], []).append(f"{v['ids'][0]}|{v['ids'][1]}")
for naht, liste in paare.items():
    eindeutig = list(dict.fromkeys(liste))
    offen.append(f"Naht {naht}: {len(liste)} Verstöße, {len(eindeutig)} ID-Paare gleicher Fläche ohne Bildkante: "
                 + ", ".join(eindeutig))

abgabe = {"runde": 1, "bearbeiter": BEARBEITER, "verstoesse": verstoesse, "naht_bestaetigt": [],
          "einheiten": [], "offen": offen,
          "nicht_geprueft": [
              "Bildpunktgenaue Lage der versetzten Grenzen nicht nachgezogen (ohne gemeinsame ID ohne Wirkung auf die Nahtregel).",
              "Zerfallene Segmente der zusammengetragenen Karte (pruefen: nicht_zusammenhaengend, 16 IDs) gehören nicht zu diesem Auftrag."]}
with open(E / "naht_abgabe.json", "w", encoding="utf-8") as f:
    json.dump(abgabe, f, ensure_ascii=False, indent=1)

# Probe-Auftrag: Kopie des Auftrags, Pfade relativ zum Ergebnisordner
auftrag = json.load(open(D / "zusammentragen.json", encoding="utf-8"))
probe = dict(auftrag)
probe["manifest"] = os.path.relpath(H0 / "manifest.json", E).replace("\\", "/")
probe["einheiten"] = []
for e in auftrag["einheiten"]:
    e2 = dict(e)
    e2["labels"] = os.path.relpath(D / e["labels"], E).replace("\\", "/")
    e2["segmente"] = os.path.relpath(D / e["segmente"], E).replace("\\", "/")
    probe["einheiten"].append(e2)
probe["naht_bestaetigt"] = list(auftrag.get("naht_bestaetigt", []))
probe["ziel"] = "probe"
with open(E / "zusammentragen.json", "w", encoding="utf-8") as f:
    json.dump(probe, f, ensure_ascii=False, indent=1)
print(len(verstoesse), "Verstöße,", len(set((v["naht"], tuple(v["ids"])) for v in verstoesse)), "Paare")
