"""Ergebnisbilder eines Viertels aus urteil.json: roh.jpg, umriss.jpg, maengel.jpg, vorschlag.jpg.
Aufruf: python render.py <viertel>   (liest und schreibt im Ergebnisordner urteil/r1c1/<viertel>)
Punkte werden aus dem Text "(x/y)" (Teilkachel-Bildpunkte) gelesen.
"""
import json
import re
import sys
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
K = Path("C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500")
LS = Path("C:/Users/Phil/Developement/Victor/landseg")
v = sys.argv[1]
VD = K / f"viertel/r1c1/{v}"
OUT = K / f"urteil/r1c1/{v}"
vj = json.loads((VD / "viertel.json").read_text(encoding="utf-8"))
fen = vj["bilder"]["uebersicht_roh.jpg"]["fenster"]
fx, fy, fw, fh, f = fen["x"], fen["y"], fen["breite"], fen["hoehe"], fen["faktor"]
vi = vj["viertel_im_bild"]
urteil = json.loads((OUT / "urteil.json").read_text(encoding="utf-8"))
kat = {k["code"]: k for k in json.loads((LS / "kategorien.json").read_text(encoding="utf-8"))["classes"]}
seg = {s["id"]: s for s in json.loads((K / "vorstufe/r1c1/segmente.json").read_text(encoding="utf-8"))["segmente"]}
lab = tifffile.imread(K / "vorstufe/r1c1/labels.tif").astype(np.int64)
L = lab[fy:fy + fh, fx:fx + fw]
Lb = np.kron(L, np.ones((f, f), dtype=np.int64))
edge = np.zeros(Lb.shape, bool)
edge[:, 1:] |= Lb[:, 1:] != Lb[:, :-1]
edge[1:, :] |= Lb[1:, :] != Lb[:-1, :]
roh = Image.open(VD / "uebersicht_roh.jpg").convert("RGB")
W, H = roh.size


def font(n):
    for name in ("arial.ttf", "segoeui.ttf"):
        try:
            return ImageFont.truetype(name, n)
        except OSError:
            pass
    return ImageFont.load_default()


F13, F15 = font(13), font(15)


def rahmen(d):
    x0, y0 = (vi["x"] - fx) * f, (vi["y"] - fy) * f
    d.rectangle([x0, y0, x0 + vi["breite"] * f, y0 + vi["hoehe"] * f], outline=(0, 255, 255), width=3)


def kopf(img, text, unten=None):
    lines = unten or []
    hh = 24 + 18 * len(lines) + (8 if lines else 0)
    c = Image.new("RGB", (W, H + hh), (0, 0, 0))
    c.paste(img, (0, 24))
    d = ImageDraw.Draw(c)
    d.text((6, 4), text, fill=(255, 255, 255), font=F15)
    for i, t in enumerate(lines):
        d.text((6, H + 30 + 18 * i), t, fill=(255, 255, 255), font=F13)
    if max(c.size) > 2000:
        r = 2000 / max(c.size)
        c = c.resize((int(c.size[0] * r), int(c.size[1] * r)), Image.LANCZOS)
    return c


def punkt_in(i):
    ys, xs = np.nonzero(L == i)
    cx, cy = xs.mean(), ys.mean()
    k = np.argmin((xs - cx) ** 2 + (ys - cy) ** 2)
    return xs[k] * f + f // 2, ys[k] * f + f // 2


eintraege = {e["id"]: e for e in urteil["segmente"]}
punkte_liste = {e["id"]: e.get("punkt") for e in vj["segmente"]}

# roh
r = roh.copy()
rahmen(ImageDraw.Draw(r))
kopf(r, f"r1c1 {v}: Luftbild unverändert, Viertel cyan umrandet (3fach, Fenster x {fx}–{fx + fw - 1}, y {fy}–{fy + fh - 1})").save(OUT / "roh.jpg", quality=92)

# umriss
u = Image.open(VD / "uebersicht_nummern.jpg").convert("RGB")
kopf(u, f"r1c1 {v}: alle Segmentgrenzen mit ID (Zahl im Bild + 400000 = volle ID), weiß = dieses Viertel").save(OUT / "umriss.jpg", quality=92)

# maengel
arr = np.asarray(roh).copy()
arr[edge] = (arr[edge] * 0.3 + np.array([255, 255, 0]) * 0.7).astype(np.uint8)
m = Image.fromarray(arr)
d = ImageDraw.Draw(m)
rahmen(d)
legende = []
n = 0
pat = re.compile(r"\((\d+)\s*/\s*(\d+)\)")
for e in urteil["segmente"]:
    for p in e.get("punkte", []):
        n += 1
        mm = pat.search(p["text"])
        if mm:
            x, y = int(mm.group(1)), int(mm.group(2))
            px, py = (x - fx) * f + f // 2, (y - fy) * f + f // 2
        else:
            px, py = punkt_in(e["id"])
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=(220, 30, 30), outline=(255, 255, 255))
        d.text((px - 6 if n < 10 else px - 8, py - 7), str(n), fill=(255, 255, 255), font=F13)
        t = f"{n}: {e['id']} {p['art']} – {p['text']}"
        legende.append(t if len(t) <= 150 else t[:147] + "…")
if not legende:
    legende = ["keine Mängel"]
kopf(m, f"r1c1 {v}: Mängel (rote Punkte, Nummer wie Legende)", legende).save(OUT / "maengel.jpg", quality=90)

# vorschlag
arr = np.asarray(roh).astype(np.float32).copy()
geaendert = set()
klasse_von = {}
for i in np.unique(L):
    e = eintraege.get(int(i))
    if e is not None:
        c = e.get("klasse_vorschlag") or e.get("klasse_heute")
        if e.get("klasse_vorschlag") and e["klasse_vorschlag"] != e["klasse_heute"]:
            geaendert.add(int(i))
    else:
        c = seg[int(i)]["klasse"]
    klasse_von[int(i)] = c
    col = np.array([int(kat[c]["color"][k:k + 2], 16) for k in (1, 3, 5)], np.float32)
    mk = np.kron(L == i, np.ones((f, f), bool))
    a = 0.5 if e is not None else 0.25
    arr[mk] = arr[mk] * (1 - a) + col * a
arr[edge] = (20, 20, 20)
for i in geaendert:
    mk = np.kron(L == i, np.ones((f, f), bool))
    b = mk & ~np.roll(mk, 1, 0) | mk & ~np.roll(mk, -1, 0) | mk & ~np.roll(mk, 1, 1) | mk & ~np.roll(mk, -1, 1)
    arr[b] = (255, 0, 255)
vimg = Image.fromarray(arr.clip(0, 255).astype(np.uint8))
d = ImageDraw.Draw(vimg)
rahmen(d)
for i, c in klasse_von.items():
    e = eintraege.get(i)
    if e is None:
        continue
    pk = punkte_liste.get(i)
    if pk:
        px, py = (pk[0] - fx) * f, (pk[1] - fy) * f
    else:
        px, py = punkt_in(i)
    t = c if i not in geaendert else f"{e['klasse_heute']}→{c}"
    d.text((px - 10, py - 7), t, fill=(255, 255, 255), font=F13, stroke_width=2, stroke_fill=(0, 0, 0))
n = 0
for e in urteil["segmente"]:
    for p in e.get("punkte", []):
        n += 1
        if p["art"] in ("trennen", "fremd", "fehlt", "grenze"):
            mm = pat.search(p["text"])
            if mm:
                x, y = int(mm.group(1)), int(mm.group(2))
                px, py = (x - fx) * f + f // 2, (y - fy) * f + f // 2
                d.line([px - 7, py - 7, px + 7, py + 7], fill=(255, 255, 255), width=3)
                d.line([px - 7, py + 7, px + 7, py - 7], fill=(255, 255, 255), width=3)
                d.text((px + 8, py - 8), str(n), fill=(255, 255, 255), font=F13, stroke_width=2, stroke_fill=(0, 0, 0))
unten = ["Farbe = Klasse, wie ich sie setzen würde (Farben aus kategorien.json); magenta umrandet = Klasse geändert (alt→neu);",
         "weißes Kreuz = Stelle, an der Grenze, Trennung oder Verschmelzung geändert gehört (Nummer wie im Mängelbild); blass = Nachbarviertel/Rand.",
         f"Geänderte Klassen: {len(geaendert)}" if geaendert else "Klassen unverändert"]
kopf(vimg, f"r1c1 {v}: Vorschlag", unten).save(OUT / "vorschlag.jpg", quality=90)
print("Punkte:", n, "geändert:", len(geaendert))
