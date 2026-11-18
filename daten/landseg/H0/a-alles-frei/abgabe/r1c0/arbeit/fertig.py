"""Bereinigen, nummerieren, Abgabe schreiben (labels.tif, segmente.json, kategorien-teil.json, ergebnis.jpg)."""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi

sys.path.insert(0, r"C:/Users/Phil/Developement/Victor/landseg")
from landseg.dateien import schreibe_labels  # noqa: E402

ORD = Path(r"C:/Users/Phil/Developement/Victor/daten/landseg/H0/a-alles-frei/abgabe/r1c0")
A = ORD / "arbeit"
karte = np.load(A / "karte_roh.npy").astype(np.int64)
seg = json.load(open(A / "seg_roh.json", encoding="utf-8"))
nr2key = {v["nr"]: k for k, v in seg.items()}
VIER = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], bool)

# 1 Bereinigung: je ID nur die groesste Komponente, Splitter zum haeufigsten Nachbarn
for runde in range(10):
    geaendert = 0
    for i in np.unique(karte):
        m = karte == i
        lab, n = ndi.label(m, structure=VIER)
        if n <= 1:
            continue
        gr = ndi.sum(m, lab, range(1, n + 1))
        haupt = int(np.argmax(gr)) + 1
        for j in range(1, n + 1):
            if j == haupt:
                continue
            teil = lab == j
            rand = ndi.binary_dilation(teil, structure=VIER) & ~teil
            nb = karte[rand]
            nb = nb[nb != i]
            if nb.size == 0:
                continue
            ziel = np.bincount(nb).argmax()
            if teil.sum() >= 300:
                neu_nr = max(nr2key) + 1
                neu_key = f"{nr2key[i]}_t{neu_nr}"
                seg[neu_key] = dict(seg[nr2key[i]], nr=neu_nr, name=seg[nr2key[i]]["name"] + " (abgetrennter Teil)")
                nr2key[neu_nr] = neu_key
                print(f"Runde {runde}: Teil {teil.sum()} px von {nr2key[i]} -> eigenes Segment {neu_key}")
                karte[teil] = neu_nr
                geaendert += 1
                continue
            if teil.sum() > 40:
                print(f"Runde {runde}: Splitter {teil.sum()} px von {nr2key[i]} -> {nr2key[ziel]}")
            karte[teil] = ziel
            geaendert += 1
    if not geaendert:
        break

# 2 Nummerieren (nach Reihenfolge der Segmentliste)
ids = [i for i in sorted(nr2key) if (karte == i).any()]
neu = np.zeros_like(karte, dtype=np.uint32)
eintraege = []
KERN = (slice(64, 564), slice(64, 564))
for k, i in enumerate(ids, start=1):
    m = karte == i
    neu[m] = k
    s = seg[nr2key[i]]
    kern = bool(m[KERN].any())
    e = {"id": k, "klasse": s["klasse"], "grob": s["klasse"].split(".")[0], "name": s["name"],
         "im_kern": kern, "sicher": s["sicher"], "flaeche_px": int(m.sum()),
         "flaeche_kern_px": int(m[KERN].sum())}
    if s["grund"]:
        e["grund"] = s["grund"]
    e["schluessel"] = nr2key[i]
    eintraege.append(e)
assert (neu > 0).all()
schreibe_labels(ORD / "labels.tif", neu)

KLASSEN = [
    ("1", "Verkehrsfläche", None, "#5a5a5a", "helle, glatte, scharf begrenzte Bänder"),
    ("1.1", "Straße", "1", "#9a9a9a", "breites (~10 Bildpunkte), sehr helles, durchgehendes Band mit gleichmäßiger Krümmung"),
    ("1.2", "Feld-, Hof- oder Grasweg", "1", "#d8c8a0", "schmales helles Band (3–10 Bildpunkte), oft mit dunklen Rändern (Gräben)"),
    ("2", "Siedlung und Hof", None, "#b03030", "Gebäude, Schatten, Hofflächen am Ortsrand"),
    ("2.1", "Gebäude", "2", "#e04040", "kompaktes Rechteck mit scharfen Kanten und Schlagschatten"),
    ("2.2", "Hof- und Lagerfläche", "2", "#f0a070", "sehr helle, körnige oder glatte Fläche direkt am Gebäude"),
    ("3", "Offenland (Landwirtschaft)", None, "#3a7a2a", "großflächig, glatt bis fein gestreift, gerade Parzellengrenzen"),
    ("3.1", "Feldparzelle (Acker oder Grünland)", "3", "#5aa040", "Streifen- oder Blockparzelle; Acker und Grünland auf SW nicht trennbar"),
    ("3.1.1", "Feld, dunkler Bestand", "3.1", "#2f6f2f", "deutlich dunkler als die Nachbarparzellen, gleichmäßig"),
    ("3.1.2", "Feld, mittelgrau", "3.1", "#7fbf5f", "mittlerer Grauton, feine Streifung oder Fleckung"),
    ("3.1.3", "Feld, hell (offener Boden, Stoppel)", "3.1", "#d6e08a", "deutlich heller als die Nachbarparzellen"),
    ("3.2", "Brache, Ödland oder Hutweide", "3", "#c9b25a", "hell, unruhig, ohne Parzellenstreifung, mit dunklen Flecken"),
    ("4", "Gehölz und Kleinstrukturen", None, "#1f4f8f", "dunkle Punkte und Linien"),
    ("4.1", "Einzelgehölz oder dunkler Fleck", "4", "#2060c0", "kleiner, kompakter, sehr dunkler Fleck (Baum, Strauch oder Grube)"),
    ("4.2", "Rain, Graben oder Hecke", "4", "#40a0e0", "schmale dunkle Linie (2–7 Bildpunkte) zwischen Parzellen oder an Wegen"),
    ("5", "Unklar", None, "#a040a0", "auf SW nicht bestimmbar"),
    ("5.1", "Sehr dunkle Fläche (Schatten oder Baumkrone)", "5", "#600060", "fast schwarz, neben Gebäude"),
    ("5.2", "Kleines Objekt", "5", "#e070e0", "kleiner Fleck mit Form, Art nicht erkennbar"),
]
kat = {"schema": "landseg-kategorien/1", "teilkachel": "r1c0", "fassung": "A alles frei",
       "hinweis": "eigene Liste für den SW-Scan 1968; Ebene 3 unter 3.1 nur nach Grauton, nicht nach Nutzung",
       "classes": [{"code": c, "name": nm, "parent": p, "level": c.count(".") + 1, "color": col, "image_cue": cue}
                   for c, nm, p, col, cue in KLASSEN]}
json.dump(kat, open(ORD / "kategorien-teil.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

offen = [
    "Acker gegen Grünland: auf SW für alle Feldparzellen (3.1.x) nicht trennbar; im Farbbild entscheidbar (Grünton, Bearbeitungsspuren).",
    "Helle fleckige Fläche (3.2) mit dunklen Flecken: Brache, Hutweide oder alte Gruben; Farbbild oder Gelände würde entscheiden.",
    "Heller breiter Streifen östlich (3.1.3, ~12 m): Stoppel-/Brachstreifen oder breiter Erdweg; im Farbbild an Fahrspuren erkennbar.",
    "Schmale Linien zwischen den Parzellen (1.2/4.2): Grasweg, Rain, Graben oder Hecke nicht sicher trennbar.",
    "Gebäude am Hof (2.1) und die schwarze Fläche daneben (5.1): Dach/Schatten/Baumkrone; Grenze geschätzt.",
    "Weiche Grenzen ohne Bildkante (geschätzt): Feld Nord gegen Feld zwischen Rain und Hofweg, Streifengrenzen im Feld zwischen den Rainwegen, dunkler Feldteil West am Seitenweg.",
]
nicht = [
    "Kontextrand (außerhalb Kern) nur grob segmentiert; Ortsrand Nordost dort als ein Segment.",
    "Schmale Streifen der schrägen Streifenflur im Feld West (Breite 5–15 Bildpunkte) nicht einzeln getrennt.",
    "Straßenbankette und schmale Straßengräben (unter 3 Bildpunkte) der Straße bzw. dem Feld zugeschlagen.",
]
json.dump({"schema": "landseg-segmente/1", "teilkachel": "r1c0", "fassung": "A alles frei",
           "segmente": eintraege, "verlauf": [{"bearbeiter": "fassung-a-r1c0", "schritt": "Aufbau aus Linienzügen, Polygonen und Bildschwellen (arbeit/bauen.py, arbeit/fertig.py)"}],
           "offen": offen, "nicht_geprueft": nicht},
          open(ORD / "segmente.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# 3 ergebnis.jpg
b = np.array(Image.open(r"C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r1c0.png")).astype(float)
if b.ndim == 3:
    b = b[..., 0]
lo, hi = np.percentile(b, 1), np.percentile(b, 99.5)
grau = np.clip((b - lo) / (hi - lo) * 255, 0, 255)
farbe = {c: tuple(int(col[i:i + 2], 16) for i in (1, 3, 5)) for c, _, _, col, _ in KLASSEN}
fl = np.zeros((628, 628, 3))
for e in eintraege:
    fl[neu == e["id"]] = farbe[e["klasse"]]
mix = 0.55 * np.repeat(grau[..., None], 3, -1) + 0.45 * fl
S = 3
big = np.kron(mix, np.ones((S, S, 1)))
kb = np.kron(neu.astype(np.int64), np.ones((S, S), int))
gr = np.zeros(kb.shape, bool)
gr[:-1] |= kb[:-1] != kb[1:]
gr[:, :-1] |= kb[:, :-1] != kb[:, 1:]
big[gr] = [255, 255, 0]
LEG = 440
im = Image.new("RGB", (628 * S + LEG, 628 * S), (255, 255, 255))
im.paste(Image.fromarray(big.astype(np.uint8)), (0, 0))
d = ImageDraw.Draw(im)
d.rectangle([64 * S, 64 * S, 564 * S, 564 * S], outline=(0, 255, 255), width=3)
f = ImageFont.truetype("arial.ttf", 15)
fb = ImageFont.truetype("arialbd.ttf", 17)
for e in eintraege:
    m = neu == e["id"]
    dist = ndi.distance_transform_edt(np.pad(m, 1))[1:-1, 1:-1]
    yy, xx = np.unravel_index(np.argmax(dist), dist.shape)
    d.text((xx * S - 8, yy * S - 8), str(e["id"]), fill=(255, 255, 255), font=f, stroke_width=2,
           stroke_fill=(0, 0, 0))
x0 = 628 * S + 12
d.text((x0, 12), "r1c0 – Fassung A (alles frei)", fill=(0, 0, 0), font=fb)
d.text((x0, 36), "Türkis: Kern; Gelb: Segmentgrenzen", fill=(0, 0, 0), font=f)
y = 70
for c, nm, p, col, cue in KLASSEN:
    einr = "    " * (c.count("."))
    d.rectangle([x0, y + 2, x0 + 18, y + 18], fill=farbe[c], outline=(0, 0, 0))
    d.text((x0 + 26, y), f"{einr}{c} {nm}"[:58], fill=(0, 0, 0), font=f)
    y += 26
y += 10
d.text((x0, y), f"Segmente: {len(eintraege)}, im Kern: {sum(e['im_kern'] for e in eintraege)}",
       fill=(0, 0, 0), font=f)
y += 22
d.text((x0, y), f"unsicher: {sum(not e['sicher'] for e in eintraege)}", fill=(0, 0, 0), font=f)
im.thumbnail((2000, 2000))
im.save(ORD / "ergebnis.jpg", quality=90)
print("Segmente", len(eintraege), "im Kern", sum(e["im_kern"] for e in eintraege),
      "unsicher", sum(not e["sicher"] for e in eintraege),
      "unsicher im Kern", sum((not e["sicher"]) and e["im_kern"] for e in eintraege))
for e in eintraege:
    print(e["id"], e["klasse"], e["schluessel"], e["flaeche_px"], e["flaeche_kern_px"], e["sicher"])
