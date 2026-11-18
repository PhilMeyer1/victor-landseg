"""Bilder der Nachhol-Gegenprobe v2 aus dem heutigen Kartenstand.

Aufruf: bilder2.py nah            -> nah_1..nah_4.jpg (Fenster wie vorbereitete Nahansichten, 6fach)
        bilder2.py abgabe         -> roh, umriss, maengel, vorschlag aus urteil.json
"""
import json
import sys
import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont

B = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/"
O = B + "c-feste-liste/urteil-gegenprobe/r0c0/v2/"
lab = tifffile.imread(B + "c-feste-liste/gegenprobe/r0c0/labels.tif").astype(np.int64)
img = Image.open(B + "teilkacheln/r0c0.png").convert("RGB")
V = (314, 64, 564, 314)
KERN = (64, 64, 564, 564)


def font(n):
    for f in ("C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"):
        try:
            return ImageFont.truetype(f, n)
        except OSError:
            pass
    return ImageFont.load_default()


def grenzen(l):
    g = np.zeros(l.shape, bool)
    g[:, 1:] |= l[:, 1:] != l[:, :-1]
    g[1:, :] |= l[1:, :] != l[:-1, :]
    return g


def fenster(x, y, w, h, f, mit_grenzen=True, nummern=None, farbe=None):
    crop = img.crop((x, y, x + w, y + h)).resize((w * f, h * f), Image.NEAREST)
    a = np.asarray(crop).copy()
    l = lab[y:y + h, x:x + w]
    lb = np.kron(l, np.ones((f, f), dtype=np.int64))
    if farbe is not None:
        for i, c in farbe.items():
            m = lb == i
            a[m] = (0.55 * a[m] + 0.45 * np.array(c)).astype(np.uint8)
    if mit_grenzen:
        a[grenzen(lb)] = (255, 230, 0)
    im = Image.fromarray(a)
    d = ImageDraw.Draw(im)
    # Viertel und Kern
    for (x0, y0, x1, y1), c in ((KERN, (255, 255, 255)), (V, (0, 230, 230))):
        d.rectangle(((x0 - x) * f, (y0 - y) * f, (x1 - x) * f - 1, (y1 - y) * f - 1), outline=c, width=2)
    if nummern:
        fn = font(max(11, 4 * f // 2))
        for i in np.unique(l):
            m = l == i
            if m.sum() < 6:
                continue
            ys, xs = np.nonzero(m)
            # Punkt im Segment nahe dem Schwerpunkt
            cy, cx = ys.mean(), xs.mean()
            k = np.argmin((ys - cy) ** 2 + (xs - cx) ** 2)
            px, py = xs[k] * f, ys[k] * f
            t = str(i if nummern == "voll" else i % 100000)
            col = (255, 255, 255) if i in MEIN else (170, 170, 170)
            d.text((px, py), t, fill=col, font=fn, anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0))
    return im, d


def mein():
    u = json.load(open(O + "urteil.json", encoding="utf-8")) if len(sys.argv) > 1 and sys.argv[1] == "abgabe" else None
    if u:
        return {s["id"] for s in u["segmente"]}, u
    ids = [int(t) for t in open(O + "meine_ids.txt").read().split()]
    return set(ids), None


MEIN, U = mein()

if sys.argv[1] == "zoom":
    n, x, y, w, h, f = (int(t) for t in sys.argv[2:8])
    for roh in (False, True):
        im, d = fenster(x, y, w, h, f, mit_grenzen=not roh, nummern=None if roh else "voll")
        d.text((6, 4), f"r0c0 v2 eigene Nahansicht {n}{' (roh)' if roh else ''}, x {x}–{x+w}, y {y}–{y+h}",
               fill=(255, 255, 0), font=font(16), stroke_width=2, stroke_fill=(0, 0, 0))
        im.save(O + (f"nah_{n}_roh.jpg" if roh else f"nah_{n}.jpg"), quality=90)
    sys.exit(0)

if sys.argv[1] == "nah":
    for n, (x, y) in enumerate(((302, 52), (427, 52), (302, 177), (427, 177)), 1):
        im, d = fenster(x, y, 149, 149, 6, nummern="voll")
        d.text((6, 4), f"r0c0 v2 Nahansicht {n} (heutiger Kartenstand), x {x}–{x+149}, y {y}–{y+149}",
               fill=(255, 255, 0), font=font(16), stroke_width=2, stroke_fill=(0, 0, 0))
        im.save(O + f"nah_{n}.jpg", quality=90)
    sys.exit(0)

# Abgabebilder: Fenster wie Uebersicht, 3fach
X, Y, W, H, F = 282, 32, 314, 314, 3
seg = {s["id"]: s for s in U["segmente"]}

im, d = fenster(X, Y, W, H, F, mit_grenzen=False)
d.text((6, 4), "r0c0 v2: Bild unverändert (Viertel cyan, Kern weiß)", fill=(255, 255, 0), font=font(16),
       stroke_width=2, stroke_fill=(0, 0, 0))
im.save(O + "roh.jpg", quality=90)

im, d = fenster(X, Y, W, H, F, nummern="voll")
d.text((6, 4), "r0c0 v2: Segmentgrenzen heute, volle ID (weiß = dieses Viertel)", fill=(255, 255, 0),
       font=font(16), stroke_width=2, stroke_fill=(0, 0, 0))
im.save(O + "umriss.jpg", quality=90)

# Maengel: nummerierte Punkte je Segment mit Punkten
im, d = fenster(X, Y, W, H, F)
leg = []
nr = 0
fn = font(15)
for s in U["segmente"]:
    for j, p in enumerate(s["punkte"]):
        nr += 1
        m = lab == s["id"]
        ys, xs = np.nonzero(m & (np.arange(lab.shape[1])[None, :] >= V[0]) & (np.arange(lab.shape[0])[:, None] >= V[1])
                            & (np.arange(lab.shape[1])[None, :] < V[2]) & (np.arange(lab.shape[0])[:, None] < V[3]))
        if len(xs) == 0:
            ys, xs = np.nonzero(m)
        cy, cx = ys.mean(), xs.mean()
        k = np.argmin((ys - cy) ** 2 + (xs - cx) ** 2)
        px, py = (xs[k] - X) * F + 20 * j, (ys[k] - Y) * F + 12 * j
        d.ellipse((px - 9, py - 9, px + 9, py + 9), fill=(220, 30, 30), outline=(255, 255, 255))
        d.text((px, py), str(nr), fill=(255, 255, 255), font=font(12), anchor="mm")
        leg.append(f"{nr} ({s['id']}): {p['art']}")
d.text((6, 4), "r0c0 v2: Mängel (rote Punkte, Legende unten)", fill=(255, 255, 0), font=font(16),
       stroke_width=2, stroke_fill=(0, 0, 0))
zeilen = (len(leg) + 3) // 4
unten = Image.new("RGB", (im.width, 20 + 17 * zeilen), (20, 20, 20))
du = ImageDraw.Draw(unten)
for i, t in enumerate(leg):
    du.text((6 + (i // zeilen) * (im.width // 4), 6 + (i % zeilen) * 17), t, fill=(255, 255, 255), font=font(13))
if not leg:
    du.text((6, 6), "keine Mängel", fill=(255, 255, 255), font=font(13))
ges = Image.new("RGB", (im.width, im.height + unten.height))
ges.paste(im, (0, 0)); ges.paste(unten, (0, im.height))
ges.save(O + "maengel.jpg", quality=90)

# Vorschlag: Klassen nach Urteil (Ebene 1 farbig), Code an jedem Segment
FARBE = {"0": (128, 128, 128), "1": (189, 40, 53), "2": (238, 199, 43), "3": (157, 209, 97), "4": (29, 114, 57),
         "5": (29, 100, 201), "6": (216, 184, 151)}
farbe = {}
for s in U["segmente"]:
    k = s["klasse_vorschlag"] or s["klasse_heute"]
    farbe[s["id"]] = FARBE[k.split(".")[0]]
im, d = fenster(X, Y, W, H, F, farbe=farbe)
fn = font(13)
for s in U["segmente"]:
    m = lab == s["id"]
    m2 = m.copy(); m2[:, :V[0]] = False; m2[:, V[2]:] = False; m2[:V[1], :] = False; m2[V[3]:, :] = False
    if m2.sum() < 6:
        continue
    ys, xs = np.nonzero(m2)
    cy, cx = ys.mean(), xs.mean()
    k = np.argmin((ys - cy) ** 2 + (xs - cx) ** 2)
    kl = s["klasse_vorschlag"] or s["klasse_heute"]
    t = kl + ("" if s["sicher"] else "?")
    d.text(((xs[k] - X) * F, (ys[k] - Y) * F), t, fill=(255, 255, 255), font=fn, anchor="mm", stroke_width=2,
           stroke_fill=(0, 0, 0))
d.text((6, 4), "r0c0 v2: Vorschlag, Klassen nach Urteil (? = unsicher), Grenzen heute; Farbe = Ebene 1",
       fill=(255, 255, 0), font=font(15), stroke_width=2, stroke_fill=(0, 0, 0))
im.save(O + "vorschlag.jpg", quality=90)
print("ok", len(leg), "Punkte")
