"""Baut urteil.json aus urteile.py (gleicher Ordner) und zeichnet roh/umriss/maengel/vorschlag.jpg.

Aufruf: python -B abgabe.py   (im Ergebnisordner des Viertels)
"""
import importlib.util
import json
from pathlib import Path

import cv2
import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont

ORD = Path(__file__).resolve().parent
B = Path("C:/Users/Phil/Developement/Victor/daten/landseg/H0")
LAB = B / "c-feste-liste/gegenprobe/r0c0/labels.tif"
SEGJ = B / "c-feste-liste/gegenprobe/r0c0/segmente.json"
BILD = B / "teilkacheln/r0c0.png"
KAT = Path("C:/Users/Phil/Developement/Victor/landseg/kategorien.json")

spec = importlib.util.spec_from_file_location("urteile", ORD / "urteile.py")
U = importlib.util.module_from_spec(spec)
spec.loader.exec_module(U)

V = U.VIERTEL
VB = B / "viertel/r0c0" / V
vj = json.loads((VB / "viertel.json").read_text(encoding="utf-8"))
vx, vy = vj["viertel_im_bild"]["x"], vj["viertel_im_bild"]["y"]
lab = tifffile.imread(LAB)
img = np.array(Image.open(BILD).convert("L"))
seg = {s["id"]: s for s in json.loads(SEGJ.read_text(encoding="utf-8"))["segmente"]}
kat = {k["code"]: k for k in json.loads(KAT.read_text(encoding="utf-8"))["classes"]}


def pfad(name):
    if name.startswith("C:"):
        return name
    if name.startswith("nah_") or name.startswith("kontrast_"):
        return str(ORD / name).replace("\\", "/")
    return str(VB / name).replace("\\", "/")


# ---- urteil.json
eintraege = []
for e in U.SEGMENTE:
    sid, was, urt, kv, sicher, punkte, bilder = e
    if sid not in seg:
        raise SystemExit(f"{sid} nicht auf der Karte")
    eintraege.append({
        "id": sid, "klasse_heute": seg[sid]["klasse"], "was_ist_es": was,
        "urteil": "sauber" if urt == "s" else "nicht_sauber",
        "klasse_vorschlag": kv, "sicher": sicher,
        "punkte": [{"nr": i + 1, "art": p[0], "text": p[1], "flaeche_px": p[2] if len(p) > 2 else None}
                   for i, p in enumerate(punkte)],
        "bilder": [pfad(b) for b in bilder],
    })
urteil = {
    "teilkachel": "r0c0", "viertel": V, "bearbeiter": f"gegen-c-r0c0-{V}",
    "bilder_angesehen": {"uebersicht": [pfad(b) for b in U.UEBERSICHT], "nah": [pfad(b) for b in U.NAH]},
    "segmente": eintraege, "naht": U.NAHT, "unsicher": U.UNSICHER,
    "nicht_geprueft": U.NICHT_GEPRUEFT, "offen": U.OFFEN, "eingriffe": U.EINGRIFFE,
}
(ORD / "urteil.json").write_text(json.dumps(urteil, ensure_ascii=False, indent=1), encoding="utf-8")

# ---- Bilder
F = 3
x0, y0 = max(0, vx - 32), max(0, vy - 32)
x1, y1 = min(lab.shape[1], vx + 250 + 32), min(lab.shape[0], vy + 250 + 32)
sub = lab[y0:y1, x0:x1].astype(np.int64)
im = img[y0:y1, x0:x1]
W, H = (x1 - x0) * F, (y1 - y0) * F
big = cv2.resize(im, (W, H), interpolation=cv2.INTER_CUBIC)
sb = cv2.resize(sub.astype(np.float64), (W, H), interpolation=cv2.INTER_NEAREST).astype(np.int64)
rand = np.zeros(sb.shape, bool)
rand[:, 1:] |= sb[:, 1:] != sb[:, :-1]
rand[1:, :] |= sb[1:, :] != sb[:-1, :]
font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 14)
fontk = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 12)
eigen = {e["id"] for e in eintraege}
by_id = {e["id"]: e for e in eintraege}


def punkt_in(i):
    m = (sub == i).astype(np.uint8)
    dt = cv2.distanceTransform(np.pad(m, 1), cv2.DIST_L2, 3)[1:-1, 1:-1]
    yy, xx = np.unravel_index(dt.argmax(), dt.shape)
    return xx * F + F // 2, yy * F + F // 2, dt.max()


def rahmen(d):
    d.rectangle([(vx - x0) * F, (vy - y0) * F, (vx - x0 + 250) * F, (vy - y0 + 250) * F], outline=(0, 255, 255), width=2)


def grund():
    return np.stack([big] * 3, -1).copy()


# roh
p = Image.fromarray(grund()); d = ImageDraw.Draw(p); rahmen(d)
d.text((6, 6), f"r0c0 {V}: Bild ohne Grenzen", fill=(255, 255, 0), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
p.save(ORD / "roh.jpg", quality=90)

# umriss
a = grund(); a[rand] = (255, 230, 0)
p = Image.fromarray(a); d = ImageDraw.Draw(p); rahmen(d)
for i in np.unique(sub):
    xx, yy, r = punkt_in(i)
    if r < 2:
        continue
    d.text((xx, yy), str(i), fill=(255, 255, 255) if i in eigen else (170, 170, 170), font=fontk, anchor="mm",
           stroke_width=2, stroke_fill=(0, 0, 0))
d.text((6, 6), f"r0c0 {V}: Segmentgrenzen nach Nachsegmentieren, volle ID (weiß = dieses Viertel)", fill=(255, 255, 0),
       font=font, stroke_width=2, stroke_fill=(0, 0, 0))
p.save(ORD / "umriss.jpg", quality=90)

# maengel
a = grund(); a[rand] = (200, 180, 0)
legende = []
p = Image.fromarray(a); d = ImageDraw.Draw(p); rahmen(d)
n = 0
for e in eintraege:
    if e["urteil"] != "nicht_sauber":
        continue
    n += 1
    xx, yy, _ = punkt_in(e["id"]) if (sub == e["id"]).any() else (0, 0, 0)
    d.ellipse([xx - 9, yy - 9, xx + 9, yy + 9], fill=(220, 30, 30), outline=(255, 255, 255))
    d.text((xx, yy), str(n), fill=(255, 255, 255), font=fontk, anchor="mm")
    kurz = e["punkte"][0]["art"] if e["punkte"] else "klasse"
    legende.append(f"{n}: {e['id']} {kurz}" + (f" -> {e['klasse_vorschlag']}" if e["klasse_vorschlag"] else ""))
if not legende:
    legende = ["keine Mängel"]
zeilen = (len(legende) + 3) // 4
leg = Image.new("RGB", (W, 18 * zeilen + 24), (20, 20, 20))
dl = ImageDraw.Draw(leg)
dl.text((6, 4), "Mängel (rote Punkte, Nummer = Zeile), Art des ersten Punkts:", fill=(255, 255, 0), font=font)
for k, t in enumerate(legende):
    dl.text((6 + (k % 4) * (W // 4), 22 + (k // 4) * 18), t, fill=(255, 255, 255), font=fontk)
out = Image.new("RGB", (W, H + leg.height)); out.paste(p, (0, 0)); out.paste(leg, (0, H))
out.save(ORD / "maengel.jpg", quality=90)

# vorschlag
a = grund().astype(float)
farbe = np.zeros_like(a)
maske = np.zeros(sb.shape, bool)
for i in np.unique(sub):
    if i not in by_id:
        continue
    e = by_id[i]
    code = e["klasse_vorschlag"] or e["klasse_heute"]
    h = kat[code]["color"].lstrip("#")
    c = tuple(int(h[k:k + 2], 16) for k in (0, 2, 4))
    m = sb == i
    farbe[m] = c
    maske |= m
a[maske] = a[maske] * 0.55 + farbe[maske] * 0.45
a = a.astype(np.uint8)
a[rand] = (255, 255, 255)
p = Image.fromarray(a); d = ImageDraw.Draw(p); rahmen(d)
for i in np.unique(sub):
    if i not in by_id:
        continue
    e = by_id[i]
    xx, yy, r = punkt_in(i)
    if r < 2:
        continue
    code = e["klasse_vorschlag"] or e["klasse_heute"]
    t = code + ("?" if not e["sicher"] else "")
    d.text((xx, yy), t, fill=(255, 255, 255), font=fontk, anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0))
d.text((6, 6), f"r0c0 {V}: Klassen, wie ich sie setzen würde (? = unsicher); Grenzen nach Nachsegmentieren",
       fill=(255, 255, 0), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
p.save(ORD / "vorschlag.jpg", quality=90)
print("geschrieben", len(eintraege), "Segmente")
