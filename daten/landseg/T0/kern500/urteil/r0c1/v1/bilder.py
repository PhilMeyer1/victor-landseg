"""Ergebnisbilder eines Viertels aus urteil.json: roh.jpg, umriss.jpg, maengel.jpg, vorschlag.jpg.
Aufruf: bilder.py <viertel>"""
import sys, json, re, textwrap
import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

B = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500"
v = sys.argv[1]
OUT = B + "/urteil/r0c1/" + v + "/"
VJ = json.load(open(B + "/viertel/r0c1/" + v + "/viertel.json", encoding="utf-8"))
U = json.load(open(OUT + "urteil.json", encoding="utf-8"))
KAT = {k["code"]: k for k in json.load(open("C:/Users/Phil/Developement/Victor/landseg/kategorien.json", encoding="utf-8"))["classes"]}
SEG = {s["id"]: s for s in json.load(open(B + "/vorstufe/r0c1/segmente.json", encoding="utf-8"))["segmente"]}
fe = VJ["bilder"]["uebersicht_roh.jpg"]["fenster"]
fx, fy, fw, fh, f = fe["x"], fe["y"], fe["breite"], fe["hoehe"], fe["faktor"]
vb = VJ["viertel_im_bild"]
mine = {s["id"]: s for s in VJ["segmente"]}
lab = tifffile.imread(B + "/vorstufe/r0c1/labels.tif").astype(np.int64)
L = lab[fy:fy + fh, fx:fx + fw]
Lb = np.kron(L, np.ones((f, f), dtype=np.int64))
edge = np.zeros(Lb.shape, bool)
edge[:, 1:] |= Lb[:, 1:] != Lb[:, :-1]
edge[1:, :] |= Lb[1:, :] != Lb[:-1, :]
roh = Image.open(B + "/viertel/r0c1/" + v + "/uebersicht_roh.jpg").convert("RGB")
font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 13)
fontb = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 15)


def rahmen(im):
    d = ImageDraw.Draw(im)
    x0, y0 = (vb["x"] - fx) * f, (vb["y"] - fy) * f
    d.rectangle([x0, y0, x0 + vb["breite"] * f, y0 + vb["hoehe"] * f], outline=(0, 255, 255), width=3)
    return d


def mitte(i):
    m = L == i
    dt = ndimage.distance_transform_edt(np.pad(m, 1))[1:-1, 1:-1]
    yy, xx = np.unravel_index(dt.argmax(), dt.shape)
    return xx * f + f // 2, yy * f + f // 2


def fuss(im, zeilen, titel):
    breite = im.width
    wrapped = []
    for z in zeilen:
        wrapped += textwrap.wrap(z, 150) or [""]
    hoehe = 24 + 16 * len(wrapped)
    neu = Image.new("RGB", (breite, im.height + hoehe), (255, 255, 255))
    neu.paste(im, (0, 0))
    d = ImageDraw.Draw(neu)
    d.text((6, im.height + 4), titel, fill=(0, 0, 0), font=fontb)
    for k, z in enumerate(wrapped):
        d.text((6, im.height + 22 + 16 * k), z, fill=(0, 0, 0), font=font)
    return neu


# roh
r = roh.copy(); rahmen(r)
fuss(r, [f"Teilkachel r0c1, Viertel {v}, Fenster x {fx}–{fx+fw-1}, y {fy}–{fy+fh-1}, 3fach"], "Luftbild unverändert").save(OUT + "roh.jpg", quality=90)

# umriss
a = np.asarray(roh).copy(); a[edge] = (255, 230, 0)
um = Image.fromarray(a); d = rahmen(um)
for i in np.unique(L):
    if (L == i).sum() < 8:
        continue
    px, py = mitte(i)
    col = (255, 255, 255) if i in mine else (170, 170, 170)
    d.text((px - 10, py - 7), str(i), fill=col, font=font, stroke_width=2, stroke_fill=(0, 0, 0))
fuss(um, ["Gelb: Segmentgrenzen der Vorstufe. Weiß: volle ID der Segmente dieses Viertels, grau: Nachbarn."], "Umriss mit ID").save(OUT + "umriss.jpg", quality=90)

# maengel
mg = Image.fromarray(a.copy()); d = rahmen(mg)
legende = []
n = 0
for s in U["segmente"]:
    for p in s.get("punkte", []):
        n += 1
        mm = re.search(r"(\d{2,3})/(\d{2,3})", p["text"])
        if mm:
            x, y = int(mm.group(1)), int(mm.group(2))
        else:
            x, y = mine[s["id"]]["punkt"]
        px, py = (x - fx) * f, (y - fy) * f
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=(220, 30, 30), outline=(255, 255, 255), width=2)
        d.text((px - 6 if n < 10 else px - 8, py - 7), str(n), fill=(255, 255, 255), font=font)
        legende.append(f"{n}: {s['id']} ({p['art']}) {p['text']}")
if not legende:
    legende = ["keine Mängel"]
fuss(mg, legende, "Mängel (rote Punkte, Nummer = Legende)").save(OUT + "maengel.jpg", quality=90)

# vorschlag
ziel = {}
for s in U["segmente"]:
    ziel[s["id"]] = s.get("klasse_vorschlag") or s["klasse_heute"]
geaendert = {s["id"] for s in U["segmente"] if s.get("klasse_vorschlag")}
over = np.asarray(roh).astype(float).copy()
for i in np.unique(L):
    k = ziel.get(int(i)) or SEG.get(int(i), {}).get("klasse")
    if not k or k not in KAT:
        continue
    c = KAT[k]["color"].lstrip("#")
    rgb = np.array([int(c[j:j + 2], 16) for j in (0, 2, 4)], float)
    m = Lb == i
    alpha = 0.45 if int(i) in mine else 0.2
    over[m] = over[m] * (1 - alpha) + rgb * alpha
o = over.astype(np.uint8); o[edge] = (40, 40, 40)
for i in geaendert:
    m = Lb == i
    if m.any():
        e = m & ~ndimage.binary_erosion(m, iterations=2)
        o[e] = (255, 40, 40)
vs = Image.fromarray(o); d = rahmen(vs)
for i in np.unique(L):
    if int(i) not in mine or (L == i).sum() < 8:
        continue
    px, py = mitte(i)
    d.text((px - 12, py - 7), ziel[int(i)], fill=(255, 255, 255), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
fuss(vs, ["Farbe und Code = Klasse, wie ich sie setzen würde (rot umrandet: geändert). Grenzen wie Vorstufe;",
          "Trennungen, Verschmelzungen und Grenzfehler stehen als Punkte in maengel.jpg." if geaendert else "unverändert"],
     "Vorschlag").save(OUT + "vorschlag.jpg", quality=90)
print("ok", n, "Punkte,", len(geaendert), "Klassen geändert")
