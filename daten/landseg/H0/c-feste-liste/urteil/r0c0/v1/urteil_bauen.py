"""Baut urteil.json und die Abgabebilder (roh, umriss, maengel, vorschlag) eines Viertels aus einer
Datendatei des Bearbeiters urt-c-r0c0. Schreibt nur in den Ergebnisordner des Viertels.
Aufruf: python -B urteil_bauen.py <viertel v1..v4> <daten.json>"""
import json
import sys
import textwrap
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont

sys.stdout.reconfigure(encoding="utf-8")
H0 = Path("C:/Users/Phil/Developement/Victor/daten/landseg/H0")
V = sys.argv[1]
DATEN = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
ERG = H0 / "c-feste-liste/urteil/r0c0" / V
VB = H0 / "viertel/r0c0" / V
lab = tifffile.imread(str(H0 / "c-feste-liste/r0c0/labels.tif")).astype(np.int64)
img = np.array(Image.open(H0 / "teilkacheln/r0c0.png").convert("L"))
segj = json.loads((H0 / "c-feste-liste/r0c0/segmente.json").read_text(encoding="utf-8"))
seg = {s["id"]: s for s in segj["segmente"]}
kat = json.loads(Path("C:/Users/Phil/Developement/Victor/landseg/kategorien.json").read_text(encoding="utf-8"))
farbe = {k["code"]: k["color"] for k in kat["classes"]}
vj = json.loads((VB / "viertel.json").read_text(encoding="utf-8"))
fe = vj["bilder"]["uebersicht_nummern.jpg"]["fenster"]
vi = vj["viertel_im_bild"]
fx, fy, fw, fh, f = fe["x"], fe["y"], fe["breite"], fe["hoehe"], fe["faktor"]
try:
    FONT = ImageFont.truetype("arial.ttf", 13)
    FONTK = ImageFont.truetype("arial.ttf", 12)
except OSError:
    FONT = FONTK = ImageFont.load_default()


def pfad(n):
    if n.startswith("eig:"):
        return str(ERG / n[4:]).replace("\\", "/")
    if n.startswith("/") or ":" in n:
        return n
    return str(VB / (n if n.endswith(".jpg") else n + ".jpg")).replace("\\", "/")


def klasse_alt(sid):
    s = seg.get(sid)
    return s["klasse"] if s else DATEN.get("klasse_alt", {}).get(str(sid))


# --- urteil.json -----------------------------------------------------------------------------
eintraege = []
for e in DATEN["segmente"]:
    sid = e["id"]
    eintraege.append({
        "id": sid,
        "klasse_heute": klasse_alt(sid),
        "was_ist_es": e["w"],
        "urteil": e["u"],
        "klasse_vorschlag": e["k"],
        "sicher": e["s"],
        "punkte": [{"nr": i + 1, "art": p[0], "text": p[1], "flaeche_px": p[2] if len(p) > 2 else None}
                   for i, p in enumerate(e.get("p", []))],
        "bilder": [pfad(b) for b in e["b"]],
    })
urteil = {
    "teilkachel": "r0c0", "viertel": V, "bearbeiter": f"urt-c-r0c0-{V}",
    "bilder_angesehen": {"uebersicht": [pfad(b) for b in DATEN["uebersicht"]],
                         "nah": [pfad(b) for b in DATEN["nah"]]},
    "segmente": eintraege,
    "naht": DATEN.get("naht", []),
    "unsicher": DATEN.get("unsicher", []),
    "nicht_geprueft": DATEN.get("nicht_geprueft", []),
    "offen": DATEN.get("offen", []),
    "eingriffe": DATEN.get("eingriffe", []),
}
(ERG / "urteil.json").write_text(json.dumps(urteil, ensure_ascii=False, indent=1), encoding="utf-8")

# --- Bilder ----------------------------------------------------------------------------------
L = lab[fy:fy + fh, fx:fx + fw]
G = img[fy:fy + fh, fx:fx + fw]
eigene = {e["id"] for e in DATEN["segmente"]}
vx0, vy0 = (vi["x"] - fx) * f, (vi["y"] - fy) * f
vx1, vy1 = (vi["x"] + vi["breite"] - fx) * f, (vi["y"] + vi["hoehe"] - fy) * f


def basis(dunkel_aussen=True):
    rgb = np.stack([G] * 3, -1).astype(np.float64)
    big = np.kron(rgb, np.ones((f, f, 1)))
    if dunkel_aussen:
        m = np.ones(big.shape[:2], bool)
        m[vy0:vy1, vx0:vx1] = False
        big[m] *= 0.55
    return big


def kanten(big, farbe_k=(255, 230, 0)):
    Lb = np.kron(L, np.ones((f, f), dtype=L.dtype))
    e = np.zeros(Lb.shape, bool)
    e[:, 1:] |= Lb[:, 1:] != Lb[:, :-1]
    e[1:, :] |= Lb[1:, :] != Lb[:-1, :]
    big[e] = farbe_k
    return big


def rahmen(d):
    d.rectangle([vx0, vy0, vx1 - 1, vy1 - 1], outline=(0, 255, 255), width=2)


def punkt(sid):
    ys, xs = np.nonzero(L == sid)
    if len(ys) == 0:
        return None
    k = np.argmin((ys - ys.mean()) ** 2 + (xs - xs.mean()) ** 2)
    return xs[k] * f + f // 2, ys[k] * f + f // 2


def text(d, xy, t, fill=(255, 255, 255), font=FONT):
    d.text(xy, t, fill=(0, 0, 0), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
    d.text(xy, t, fill=fill, font=font)


def speichern(im, name):
    im.save(ERG / name, quality=90)


# roh
im = Image.fromarray(basis(False).clip(0, 255).astype(np.uint8))
rahmen(ImageDraw.Draw(im))
speichern(im, "roh.jpg")

# umriss
im = Image.fromarray(kanten(basis()).clip(0, 255).astype(np.uint8))
d = ImageDraw.Draw(im)
rahmen(d)
for sid in np.unique(L):
    p = punkt(sid)
    if p is None:
        continue
    eig = int(sid) in eigene
    text(d, (p[0] - 8, p[1] - 7), str(int(sid) % 100000), fill=(255, 255, 255) if eig else (160, 160, 160),
         font=FONT if eig else FONTK)
speichern(im, "umriss.jpg")

# vorschlag
big = basis()
Lb = np.kron(L, np.ones((f, f), dtype=L.dtype))
vors = {e["id"]: e["k"] for e in DATEN["segmente"]}
for sid, k in vors.items():
    if k is None or k not in farbe:
        continue
    c = np.array([int(farbe[k][i:i + 2], 16) for i in (1, 3, 5)], float)
    m = Lb == sid
    big[m] = big[m] * 0.55 + c * 0.45
im = Image.fromarray(kanten(big).clip(0, 255).astype(np.uint8))
d = ImageDraw.Draw(im)
rahmen(d)
for e in DATEN["segmente"]:
    p = punkt(e["id"])
    if p is None:
        continue
    t = f"{e['id'] % 100000}:{e['k']}" + ("" if e["s"] else "?")
    text(d, (p[0] - 14, p[1] - 7), t, font=FONTK)
breite = im.width
leg = Image.new("RGB", (breite, 40), (20, 20, 20))
dl = ImageDraw.Draw(leg)
dl.text((6, 4), "Vorschlag urt-c-r0c0-" + V + ": Nummer:Klasse (Farbe der Klasse); '?' = sicher: false", fill=(255, 255, 255), font=FONT)
dl.text((6, 21), "Grenzen gelb = Karte nach Nachsegmentieren; außerhalb des Viertels abgedunkelt", fill=(200, 200, 200), font=FONTK)
ges = Image.new("RGB", (breite, im.height + 40))
ges.paste(im, (0, 0))
ges.paste(leg, (0, im.height))
speichern(ges, "vorschlag.jpg")

# maengel
im = Image.fromarray(kanten(basis()).clip(0, 255).astype(np.uint8))
d = ImageDraw.Draw(im)
rahmen(d)
zeilen = []
n = 0
for e in DATEN["segmente"]:
    if e["u"] == "sauber" and e["s"]:
        continue
    p = punkt(e["id"])
    n += 1
    kurz = e.get("m") or (e["p"][0][1] if e.get("p") else e["w"])
    zeilen.append(f"{n}: {e['id'] % 100000} – {kurz}")
    if p:
        d.ellipse([p[0] - 9, p[1] - 9, p[0] + 9, p[1] + 9], fill=(220, 30, 30), outline=(255, 255, 255))
        d.text((p[0] - (7 if n > 9 else 4), p[1] - 7), str(n), fill=(255, 255, 255), font=FONTK)
if not zeilen:
    zeilen = ["keine Mängel"]
wr = []
for z in zeilen:
    wr += textwrap.wrap(z, width=int(breite / 6.6)) or [""]
leg = Image.new("RGB", (breite, 16 * len(wr) + 30), (20, 20, 20))
dl = ImageDraw.Draw(leg)
dl.text((6, 4), "Mängel (rote Punkte; nicht sauber oder sicher: false)", fill=(255, 255, 255), font=FONT)
for i, z in enumerate(wr):
    dl.text((6, 24 + 16 * i), z, fill=(230, 230, 230), font=FONTK)
ges = Image.new("RGB", (breite, im.height + leg.height))
ges.paste(im, (0, 0))
ges.paste(leg, (0, im.height))
if ges.height > 2000:
    s = 2000 / ges.height
    ges = ges.resize((int(ges.width * s), 2000), Image.LANCZOS)
speichern(ges, "maengel.jpg")
print("geschrieben:", ERG, len(eintraege), "Segmente,", n, "Mängelpunkte")
