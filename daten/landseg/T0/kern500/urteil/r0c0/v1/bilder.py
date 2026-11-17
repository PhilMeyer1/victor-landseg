"""Ergebnisbilder eines Viertels aus seinem urteil.json: bilder.py v1|v2|v3|v4
Schreibt roh.jpg, umriss.jpg, maengel.jpg, vorschlag.jpg in den Ergebnisordner des Viertels.
Fenster = Übersichtsfenster des Viertels (32 px Umgebung), Faktor 3.
Stellen aus dem Punkttext „(x/y)“, Verschmelzungen aus „mit 1000nn“, fehlende Stücke mit
„Klasse <code>“ im Text; das Bild der Vorschläge färbt die Segmente des Viertels in der
vorgeschlagenen Klasse, lässt Grenzen zwischen zu verschmelzenden Segmenten weg und zeichnet
fehlende Stücke als gestrichelten Kreis mit Code."""
import json
import math
import re
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
B = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500"
v = sys.argv[1]
O = f"{B}/urteil/r0c0/{v}/"
vj = json.load(open(f"{B}/viertel/r0c0/{v}/viertel.json", encoding="utf-8"))
fe = vj["bilder"]["uebersicht_nummern.jpg"]["fenster"]
x0, y0, w, h, f = fe["x"], fe["y"], fe["breite"], fe["hoehe"], fe["faktor"]
vq = vj["viertel_im_bild"]
lab_full = np.array(Image.open(B + "/vorstufe/r0c0/labels.tif")).astype(np.int64)
img = Image.open(B + "/teilkacheln/r0c0.png").convert("RGB").crop((x0, y0, x0 + w, y0 + h))
seg = {s["id"]: s for s in json.load(open(B + "/vorstufe/r0c0/segmente.json", encoding="utf-8"))["segmente"]}
kat = {k["code"]: k for k in json.load(open("C:/Users/Phil/Developement/Victor/landseg/kategorien.json",
                                            encoding="utf-8"))["classes"]}
urt = json.load(open(O + "urteil.json", encoding="utf-8"))
L = lab_full[y0:y0 + h, x0:x0 + w]
W, H = w * f, h * f
up = np.repeat(np.repeat(L, f, 0), f, 1)
try:
    font = ImageFont.truetype("arial.ttf", 15)
    fontk = ImageFont.truetype("arial.ttf", 13)
    fontb = ImageFont.truetype("arialbd.ttf", 15)
except Exception:
    font = fontk = fontb = ImageFont.load_default()
eigen = {e["id"] for e in urt["segmente"]}


def kanten(arr):
    e = np.zeros(arr.shape, bool)
    e[:-1, :] |= arr[:-1, :] != arr[1:, :]
    e[:, :-1] |= arr[:, :-1] != arr[:, 1:]
    return e


def rahmen(d):
    qx0, qy0 = (vq["x"] - x0) * f, (vq["y"] - y0) * f
    d.rectangle([qx0, qy0, qx0 + vq["breite"] * f - 1, qy0 + vq["hoehe"] * f - 1], outline=(0, 255, 255), width=3)


def basis(dunkel=True):
    a = np.array(img.resize((W, H), Image.NEAREST)).astype(float)
    if dunkel:
        inq = np.zeros((H, W), bool)
        qx0, qy0 = (vq["x"] - x0) * f, (vq["y"] - y0) * f
        inq[qy0:qy0 + vq["hoehe"] * f, qx0:qx0 + vq["breite"] * f] = True
        a[~inq] *= 0.55
    return a


def mitte(mask):
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    k = np.argmin((xs - xs.mean()) ** 2 + (ys - ys.mean()) ** 2)
    return xs[k], ys[k]


def text(d, xy, s, fill=(255, 255, 255), fnt=None):
    d.text(xy, s, fill=fill, font=fnt or font, stroke_width=2, stroke_fill=(0, 0, 0))


def hexrgb(c):
    c = c.lstrip("#")
    return np.array([int(c[i:i + 2], 16) for i in (0, 2, 4)], float)


# roh
r = Image.fromarray(basis(False).astype(np.uint8))
d = ImageDraw.Draw(r)
rahmen(d)
r.save(O + "roh.jpg", quality=90)

# umriss
a = basis()
a[kanten(up)] = (255, 255, 0)
u = Image.fromarray(a.astype(np.uint8))
d = ImageDraw.Draw(u)
rahmen(d)
for i in np.unique(L):
    p = mitte(L == i)
    if p is None or (L == i).sum() < 8:
        continue
    col = (255, 255, 255) if i in eigen else (170, 170, 170)
    text(d, (p[0] * f - 12, p[1] * f - 8), str(int(i) % 100000), col)
text(d, (8, H - 24), f"Umrisse der Vorstufe, Nummer = ID − 100000; weiß: Segmente von {v}, grau: Nachbarn")
u.save(O + "umriss.jpg", quality=90)

# Punkte sammeln
punkte = []
merge = {}
fehlt = []
for e in urt["segmente"]:
    for p in e.get("punkte", []):
        m = re.search(r"\((\d+)/(\d+)\)", p["text"])
        if m:
            px, py = int(m.group(1)), int(m.group(2))
        else:
            c = mitte(L == e["id"])
            px, py = (c[0] + x0, c[1] + y0) if c else (vq["x"], vq["y"])
        art = p["art"]
        kurz = {"fremdes": "fremdes Stück", "fehlt": "fehlt", "trennen": "trennen", "verschmelzen": "verschmelzen",
                "grenze": "Grenze", "klasse": "Klasse", "zu_klein": "zu klein", "sonstiges": "sonstiges"}[art]
        mm = re.search(r"[Mm]it (1\d{5})", p["text"])
        mk = re.search(r"Klasse (\d(?:\.\d)*)", p["text"])
        if art == "verschmelzen" and mm:
            kurz += f" mit {int(mm.group(1)) % 100000}"
            merge[e["id"]] = int(mm.group(1))
        if art == "klasse" and e.get("klasse_vorschlag"):
            kurz += f" {e['klasse_heute']} → {e['klasse_vorschlag']}"
        if art == "fehlt" and mk:
            kurz += f": {mk.group(1)}"
            fehlt.append((px, py, p.get("flaeche_px") or 100, mk.group(1)))
        punkte.append((f"{e['id'] % 100000}.{p['nr']}", px, py, kurz))

# maengel
legende = [f"{n}  {k}" for n, _, _, k in punkte] or ["keine Mängel"]
spalten = 3
zeilen = math.ceil(len(legende) / spalten)
LH = 20 * zeilen + 34
a = basis()
a[kanten(up)] = (230, 230, 0)
mg = Image.new("RGB", (W, H + LH), (20, 20, 20))
mg.paste(Image.fromarray(a.astype(np.uint8)), (0, 0))
d = ImageDraw.Draw(mg)
rahmen(d)
for n, px, py, k in punkte:
    cx, cy = (px - x0) * f, (py - y0) * f
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 40, 40), outline=(255, 255, 255), width=2)
    text(d, (cx + 8, cy - 8), n, (255, 200, 200), fontb)
text(d, (8, H + 6), "Mängel (Nummer = Segment.Punkt, Stelle im Bild als roter Punkt):", (255, 255, 255))
for j, s in enumerate(legende):
    c, z = divmod(j, zeilen)
    d.text((8 + c * (W // spalten), H + 28 + z * 20), s[:52], fill=(255, 255, 255), font=fontk)
mg.save(O + "maengel.jpg", quality=90)

# vorschlag
klasse_neu = {}
for e in urt["segmente"]:
    klasse_neu[e["id"]] = e.get("klasse_vorschlag") or e["klasse_heute"]


def ziel(i):
    seen = set()
    while i in merge and i not in seen:
        seen.add(i)
        i = merge[i]
    return i


Lv = L.copy()
for i in np.unique(L):
    if int(i) in merge:
        Lv[L == i] = ziel(int(i))
upv = np.repeat(np.repeat(Lv, f, 0), f, 1)
a = basis()
for i in np.unique(L):
    i = int(i)
    code = klasse_neu.get(i) if i in eigen else None
    if code is None:
        continue
    col = hexrgb(kat[code]["color"]) if code in kat else np.array([255, 0, 255.])
    mk = up == i
    a[mk] = a[mk] * 0.55 + col * 0.45
a[kanten(upv)] = (255, 255, 0)
vs = Image.fromarray(a.astype(np.uint8))
d = ImageDraw.Draw(vs)
rahmen(d)
for i in np.unique(L):
    i = int(i)
    if i not in eigen:
        continue
    p = mitte(L == i)
    if p is None:
        continue
    alt = seg.get(i, {}).get("klasse")
    neu = klasse_neu[i]
    s = neu if neu == alt else f"{neu}*"
    text(d, (p[0] * f - 14, p[1] * f - 8), s, (255, 255, 255) if neu == alt else (255, 170, 60))
for px, py, fl, code in fehlt:
    cx, cy = (px - x0) * f, (py - y0) * f
    rr = max(10, math.sqrt(fl / math.pi) * f)
    for t in range(0, 360, 20):
        t0, t1 = math.radians(t), math.radians(t + 10)
        d.line([(cx + rr * math.cos(t0), cy + rr * math.sin(t0)), (cx + rr * math.cos(t1), cy + rr * math.sin(t1))],
               fill=(255, 60, 255), width=3)
    text(d, (cx - 14, cy - 8), code, (255, 140, 255))
gibt = any(klasse_neu[i] != seg.get(i, {}).get("klasse") for i in eigen) or merge or fehlt
text(d, (8, H - 44), "Vorschlag: Farbe = Klasse; orange* = geändert; gelbe Grenzen ohne Verschmelzungen;", (255, 255, 255))
text(d, (8, H - 24), "violett gestrichelt = fehlendes eigenes Segment (ungefähre Lage)" if gibt else "unverändert",
     (255, 255, 255))
vs.save(O + "vorschlag.jpg", quality=90)
print("Bilder:", O, len(punkte), "Punkte,", len(merge), "Verschmelzungen,", len(fehlt), "fehlend")
