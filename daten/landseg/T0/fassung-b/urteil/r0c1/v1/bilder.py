"""Ergebnisbilder eines Viertels aus urteil.json (und optional formen.json) zeichnen.
Aufruf: PY bilder.py <ergebnisordner> <viertelbilder-ordner>
Schreibt roh.jpg, umriss.jpg, maengel.jpg, vorschlag.jpg in den Ergebnisordner (nur dort)."""
import json
import re
import sys
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

B = Path("C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b")
out = Path(sys.argv[1])
vb = Path(sys.argv[2])
vj = json.loads((vb / "viertel.json").read_text(encoding="utf-8"))
fen = vj["bilder"]["uebersicht_roh.jpg"]["fenster"]
X0, Y0, W, H, F = fen["x"], fen["y"], fen["breite"], fen["hoehe"], fen["faktor"]
q = vj["viertel_im_bild"]
lab = tifffile.imread(B / "vorstufe/r0c1/labels.tif").astype(np.int64)[Y0:Y0 + H, X0:X0 + W]
img = np.asarray(Image.open(B / "teilkacheln/r0c1.png").convert("RGB"))[Y0:Y0 + H, X0:X0 + W]
urteil = json.loads((out / "urteil.json").read_text(encoding="utf-8"))
formen = json.loads((out / "formen.json").read_text(encoding="utf-8")) if (out / "formen.json").is_file() else []
eigene = {e["id"]: e for e in urteil["segmente"]}

def font(n):
    try:
        return ImageFont.truetype("arial.ttf", n)
    except OSError:
        return ImageFont.load_default()

F14, F12 = font(15), font(13)
Lb = np.repeat(np.repeat(lab, F, 0), F, 1)
edge = np.zeros(Lb.shape, bool)
edge[:, 1:] |= Lb[:, 1:] != Lb[:, :-1]
edge[1:, :] |= Lb[1:, :] != Lb[:-1, :]
base = np.repeat(np.repeat(img, F, 0), F, 1).astype(np.float32)

def P(x, y):
    return ((x - X0) * F + F // 2, (y - Y0) * F + F // 2)

def rahmen(d):
    d.rectangle([(q["x"] - X0) * F, (q["y"] - Y0) * F, (q["x"] + q["breite"] - X0) * F - 1,
                 (q["y"] + q["hoehe"] - Y0) * F - 1], outline=(0, 255, 255), width=3)

def mitte(i):
    m = lab == i
    if m.sum() == 0:
        return None
    dt = ndimage.distance_transform_edt(np.pad(m, 1))[1:-1, 1:-1]
    yy, xx = np.unravel_index(np.argmax(dt), dt.shape)
    return xx * F + F // 2, yy * F + F // 2

def mit_legende(im, zeilen, titel):
    import textwrap
    zeilen = [w for z in zeilen for w in textwrap.wrap(z, 135, subsequent_indent="     ")]
    hoehe = 26 + 17 * len(zeilen)
    neu = Image.new("RGB", (im.width, im.height + hoehe), (255, 255, 255))
    neu.paste(im, (0, 0))
    d = ImageDraw.Draw(neu)
    d.text((8, im.height + 5), titel, fill=(0, 0, 0), font=F14)
    for k, z in enumerate(zeilen):
        d.text((8, im.height + 24 + 17 * k), z, fill=(0, 0, 0), font=F12)
    return neu

# roh
im = Image.fromarray(base.astype(np.uint8)); d = ImageDraw.Draw(im); rahmen(d)
mit_legende(im, [f"Teilkachel r0c1, Viertel {urteil['viertel']}, Fenster x {X0}–{X0 + W - 1}, y {Y0}–{Y0 + H - 1}, {F}fach"],
            "Rohbild").save(out / "roh.jpg", quality=90)

# umriss
I = base.copy(); I[edge] = [255, 255, 0]
im = Image.fromarray(I.astype(np.uint8)); d = ImageDraw.Draw(im); rahmen(d)
for i in np.unique(lab):
    c = mitte(i)
    if c and (lab == i).sum() >= 12:
        d.text(c, str(i % 100000), fill=(255, 255, 255) if i in eigene else (190, 190, 190), font=F12,
               anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0))
mit_legende(im, ["Gelb: Segmentgrenzen der Vorstufe; Nummer = ID − 200000 (weiß: dieses Viertel, grau: Nachbarn/Rand)"],
            "Umriss mit ID").save(out / "umriss.jpg", quality=90)

# maengel
I = base.copy() * 0.85; I[edge] = [230, 230, 120]
im = Image.fromarray(I.astype(np.uint8)); d = ImageDraw.Draw(im); rahmen(d)
zeilen, n = [], 0
for e in urteil["segmente"]:
    for p in e.get("punkte", []):
        n += 1
        m = re.search(r"\((\d+)/(\d+)\)", p["text"])
        if m:
            x, y = P(int(m.group(1)), int(m.group(2)))
        else:
            c = mitte(e["id"]); x, y = c if c else (10, 10)
        d.ellipse([x - 10, y - 10, x + 10, y + 10], fill=(220, 30, 30), outline=(255, 255, 255), width=2)
        d.text((x, y), str(n), fill=(255, 255, 255), font=F12, anchor="mm")
        zeilen.append(f"{n}: {e['id'] % 100000} {p['art']} – {p['text']}")
if not zeilen:
    zeilen = ["keine Mängel"]
mit_legende(im, zeilen, "Mängel (rote Punkte, Nummer = Zeile der Legende; Segmentnummer = ID − 200000)").save(
    out / "maengel.jpg", quality=90)

# vorschlag
FARBE = {"Gebäude": (200, 40, 50), "Befestigte Fläche": (150, 150, 150), "Gehölz": (20, 150, 60),
         "Grasland": (160, 220, 90), "Offener Boden": (200, 160, 90), "Wasser": (40, 120, 230),
         "Schatten": (60, 60, 60)}
I = base.copy()
for i, e in eigene.items():
    m = Lb == i
    c = np.array(FARBE.get(e["klasse_frei"]["grob"], (255, 0, 255)), np.float32)
    I[m] = I[m] * 0.55 + c * 0.45
I[edge] = [255, 255, 0]
im = Image.fromarray(I.astype(np.uint8)); d = ImageDraw.Draw(im); rahmen(d)
for f in formen:
    pts = [P(x, y) for x, y in f["poly"]]
    d.line(pts + [pts[0]], fill=(255, 0, 255), width=3)
for i, e in eigene.items():
    c = mitte(i)
    if c and (lab == i).sum() >= 40:
        d.text(c, f"{i % 100000} {e['klasse_frei']['fein']}", fill=(255, 255, 255), font=F12, anchor="mm",
               stroke_width=2, stroke_fill=(0, 0, 0))
for f in formen:
    x = sum(p[0] for p in f["poly"]) / len(f["poly"]); y = sum(p[1] for p in f["poly"]) / len(f["poly"])
    d.text(P(int(x), int(y)), f["name"], fill=(255, 210, 255), font=F12, anchor="mm", stroke_width=2,
           stroke_fill=(0, 0, 0))
leg = ["Füllung = grobe Klasse: " + ", ".join(f"{k}" for k in FARBE) + " (rot, grau, grün, hellgrün, braun, blau, dunkel)",
       "Magenta: vorgeschlagene neue Teilflächen (grob umrissen, Grenze auf Bildkante noch einzurasten)",
       "Beschriftung: Segmentnummer und feine Klasse (nur Segmente dieses Viertels ab 40 px)"]
if not formen and all(e["urteil"] == "sauber" for e in eigene.values()):
    leg.append("unverändert")
mit_legende(im, leg, "Vorschlag (Grenzen und Klassen, wie ich sie setzen würde)").save(out / "vorschlag.jpg", quality=90)
print("ok", n, "Punkte")
