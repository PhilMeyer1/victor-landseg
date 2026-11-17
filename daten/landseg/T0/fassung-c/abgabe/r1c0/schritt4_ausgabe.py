"""Schritt 4: labels.tif, segmente.json, kategorien-teil.json, ergebnis.jpg und eine Segmenttabelle."""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi

HIER = Path(__file__).parent
A = HIER / "arbeit"
sys.path.insert(0, "C:/Users/Phil/Developement/Victor/landseg")
from landseg.dateien import schreibe_labels, schreibe_json  # noqa: E402

BILD = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c/teilkacheln/r1c0.png"
K0, K1 = 64, 564
CODES = json.load(open(A / "codes.json"))["codes"]
karte = np.load(A / "karte.npy").astype(np.uint32)
k = np.load(A / "klassen_final.npy")

KLASSEN = [
    # code, name, parent, color, image_cue
    ("1", "Gehölz", None, "#1b5e20", "Baum- und Strauchkronen: körnige, schattige Textur, dunkelgrün"),
    ("1.1", "Wald, geschlossenes Kronendach", "1", "#2e7d32",
     "zusammenhängende Kronen ohne Bodensicht über mehr als ca. 0,1 ha"),
    ("1.1.1", "Kronendach besonnt", "1.1", "#388e3c",
     "geschlossene, besonnte Laubkronen, rundliche Kronenballen mit hellen Rändern"),
    ("1.1.2", "Kronendach beschattet / dunkler Bestand", "1.1", "#0d3b1e",
     "großflächig sehr dunkle Stelle im Bestand mit schwacher Kronentextur: Schlagschatten höherer Bäume oder dunkle Baumart"),
    ("1.1.3", "auffällige Einzelkrone im Bestand", "1.1", "#8d6e63",
     "einzelne Krone mit abweichender Färbung (braun/rötlich) innerhalb des Bestands"),
    ("1.2", "Einzelbaum, freistehend", "1", "#66bb6a",
     "einzelne geschlossene Krone mit Schlagschatten, ringsum Offenland"),
    ("1.3", "Baumgruppe, freistehend", "1", "#43a047",
     "wenige verbundene Kronen, außerhalb des Waldes, ringsum Offenland"),
    ("1.4", "Gebüsch / Strauchgruppe", "1", "#9ccc65",
     "kleine, niedrige Gehölzflecken ohne klare Baumkrone, kurzer Schatten"),
    ("2", "Krautige Vegetation", None, "#c0ca33", "Gras- und Krautdecke ohne Gehölz, feine gleichmäßige Textur"),
    ("2.1", "Wiese / Grünland", "2", "#d4e157",
     "große, gleichmäßig grüne Grasfläche, teils mit hellen Tritt- oder Fahrspuren"),
    ("2.2", "Lichtung / Krautflur im Gehölz", "2", "#fff176",
     "helle Gras-/Krautfläche, vom Gehölz umschlossen, rauer als die Wiese"),
    ("2.3", "Saum / verbuschende Krautflur", "2", "#aed581",
     "raue Kraut- und Grasflur zwischen Wiese und Wald mit vielen kleinen Gebüschen und hellen Flecken"),
    ("3", "Vegetationsarme Flächen", None, "#bcaaa4", "Boden oder trockene Pflanzenreste sichtbar, beige bis braun"),
    ("3.1", "vegetationsarme Stelle (Boden / Trockengras / Streu)", "3", "#d7ccc8",
     "beige bis bräunliche Flecken und Streifen in der Wiese oder am Gehölzrand"),
    ("3.2", "Acker, abgeerntet (Stoppel)", "3", "#efebe9",
     "hellbeige Fläche mit parallelen Bearbeitungsspuren (nur Kontextrand oben rechts)"),
    ("4", "Wege", None, "#ff7043", "linienhafte helle Streifen"),
    ("4.1", "Trampelpfad, unbefestigt", "4", "#ff8a65",
     "schmale (1 bis 3 px) helle Linie durch Gras oder Gehölz"),
    ("5", "Siedlung / Gärten", None, "#ab47bc", "Dächer, Hartflächen, kleinteilige Gärten"),
    ("5.1", "Gebäude und befestigte Flächen (Kleingarten)", "5", "#e040fb",
     "graue, rote oder weiße Dächer, Wege, Becken, Pavillons"),
    ("5.2", "Gartenfläche (Rasen, Beete)", "5", "#ce93d8",
     "kleinteilige Grün- und Beetflächen zwischen Gartenhäusern"),
]
kat = {"schema": "landseg-kategorien/1", "teilkachel": "r1c0",
       "title": "Eigene gestufte Kategorien, Fassung C, Teilkachel r1c0",
       "classes": [{"code": c, "name": n, "parent": p, "level": c.count(".") + 1, "color": col,
                    "image_cue": cue} for c, n, p, col, cue in KLASSEN]}
schreibe_json(HIER / "kategorien-teil.json", kat)
NAME = {c: n for c, n, *_ in KLASSEN}
FARBE = {c: col for c, _, _, col, _ in KLASSEN}

# Unsicherheit je Klasse (Vorgabe) und Ausnahmen per Saatpunkt
OFFEN_KLASSE = {
    "1.1.2": "dunkle Fläche: Schlagschatten im Bestand oder dunkle Baumart (Nadelholz?) nicht unterscheidbar; Wald selbst sicher",
    "1.1.3": "Krone deutlich abweichend gefärbt; Ursache (Baumart, Laubverfärbung, Absterben) offen, Umriss von Hand",
    "1.2": "freistehende Krone; Baum oder hoher Strauch nicht sicher getrennt",
    "1.3": "Gehölzgruppe; Baumgruppe oder Gebüsch nicht sicher getrennt",
    "1.4": "kleiner dunkler Fleck; Strauch, Jungbaum oder dichter Krautbult nicht sicher getrennt",
    "2.2": "helle Fläche im Gehölz; Krautflur/Lichtung oder sehr helle, niedrige Gehölzkronen",
    "2.3": "Grenze Wiese/Saum von Hand gezogen (Übergang fließend)",
    "3.1": "offener Boden, Trockengras, Mähgut oder Trittstelle nicht unterscheidbar",
    "4.1": "Pfad von Hand nachgezeichnet, Verlauf nur stellenweise sichtbar",
    "5.2": "nur Kontextrand; Gartenflächen grob, Grenzen zu Gehölz und Bauten nicht geprüft",
}
SICHER_PUNKTE = {  # (x, y): Begründung, warum doch sicher
    (215, 150): "großer freistehender Baum mit klarem Schlagschatten",
    (150, 20): "deutliche Baumgruppe am Wiesenrand",
    (503, 184): "Hauptpfad durchgehend sichtbar; Breite von Hand (3 px)",
    (540, 170): "deutliche Gras-Lichtung mit Pfad, ringsum Gehölz",
}
sicher_ids = {int(karte[y, x]): grund for (x, y), grund in SICHER_PUNKTE.items()}

ids = np.unique(karte)
obj = ndi.find_objects(karte.astype(np.int64))
segs = []
zeilen = []
for sid in ids:
    sl = obj[sid - 1]
    m = karte[sl] == sid
    code = CODES[int(np.bincount(k[sl][m]).argmax())]
    ys, xs = np.nonzero(m)
    ys = ys + sl[0].start
    xs = xs + sl[1].start
    im_kern = bool(((xs >= K0) & (xs < K1) & (ys >= K0) & (ys < K1)).any())
    flaeche = int(m.sum())
    offen = OFFEN_KLASSE.get(code)
    sicher = offen is None
    if sid in sicher_ids:
        sicher, offen = True, None
    if code == "5.1" and flaeche < 100:
        sicher, offen = False, "kleiner heller Fleck im Garten, Bau oder Gerät unklar"
    e = {"id": int(sid), "klasse": code, "grob": code.split(".")[0], "name": NAME[code],
         "im_kern": im_kern, "sicher": sicher, "flaeche": flaeche,
         "bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]}
    if offen:
        e["offen"] = offen
    if sid in sicher_ids:
        e["begruendung"] = sicher_ids[sid]
    segs.append(e)
    zeilen.append(f"{sid:3d} {code:6s} {flaeche:7d} kern={int(im_kern)} sicher={int(sicher)} bbox={e['bbox']}")

schreibe_labels(HIER / "labels.tif", karte)
schreibe_json(HIER / "segmente.json", {"schema": "landseg-segmente/1", "teilkachel": "r1c0",
                                       "fassung": "C", "segmente": segs, "verlauf": [
    {"schritt": "eigene Pixel-Klassifikation + Regeln + Korrekturen", "skripte": [
        "schritt1_pixel.py", "schritt2_segmente.py", "schritt3_karte.py", "schritt4_ausgabe.py",
        "korrektur.json"]}]})
(A / "tabelle.txt").write_text("\n".join(zeilen), encoding="utf-8")

# ergebnis.jpg: Klassenfarben halbtransparent, Grenzen, Kern umrandet, Legende
img = np.array(Image.open(BILD).convert("RGB")).astype(float)
f = 2
farb = np.zeros_like(img)
code_je_id = {s["id"]: s["klasse"] for s in segs}
lut = np.zeros((int(karte.max()) + 1, 3))
for sid, c in code_je_id.items():
    h = FARBE[c].lstrip("#")
    lut[sid] = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
farb = lut[karte]
mix = (0.6 * img + 0.4 * farb).astype(np.uint8)
big = np.repeat(np.repeat(mix, f, 0), f, 1)
kb = np.repeat(np.repeat(karte, f, 0), f, 1)
rand = np.zeros(kb.shape, bool)
rand[:-1] |= kb[:-1] != kb[1:]
rand[:, :-1] |= kb[:, :-1] != kb[:, 1:]
big[rand] = (255, 255, 0)
legende_b = 430
canvas = Image.new("RGB", (big.shape[1] + legende_b, big.shape[0]), (255, 255, 255))
canvas.paste(Image.fromarray(big), (0, 0))
d = ImageDraw.Draw(canvas)
d.rectangle([K0 * f, K0 * f, K1 * f - 1, K1 * f - 1], outline=(0, 255, 255), width=3)
try:
    font = ImageFont.truetype("arial.ttf", 15)
    fontb = ImageFont.truetype("arialbd.ttf", 11)
except OSError:
    font = fontb = ImageFont.load_default()
for s in segs:
    m = karte == s["id"]
    dist = ndi.distance_transform_edt(m)
    cy, cx = np.unravel_index(dist.argmax(), m.shape)
    t = str(s["id"]) + ("" if s["sicher"] else "?")
    d.text((cx * f - 6 + 1, cy * f - 6 + 1), t, fill=(0, 0, 0), font=fontb)
    d.text((cx * f - 6, cy * f - 6), t, fill=(255, 255, 255), font=fontb)
x0 = big.shape[1] + 12
y = 12
d.text((x0, y), "Teilkachel r1c0, Fassung C", fill=(0, 0, 0), font=font)
y += 22
d.text((x0, y), "Kern cyan umrandet; Zahl = Segment, ? = unsicher", fill=(0, 0, 0), font=font)
y += 30
benutzt = set(code_je_id.values())
for c, n, p, col, _ in KLASSEN:
    lvl = c.count(".")
    if lvl > 0 and c not in benutzt:
        continue
    d.rectangle([x0 + lvl * 16, y, x0 + lvl * 16 + 18, y + 16], fill=col, outline=(0, 0, 0))
    d.text((x0 + lvl * 16 + 26, y), f"{c} {n}"[:52], fill=(0, 0, 0), font=font)
    y += 24
canvas.save(HIER / "ergebnis.jpg", quality=90)
print(len(segs), "Segmente,", sum(s["im_kern"] for s in segs), "im Kern,",
      sum(not s["sicher"] for s in segs), "unsicher")
