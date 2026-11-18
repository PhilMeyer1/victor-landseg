"""Renders roh.jpg, umriss.jpg, maengel.jpg, vorschlag.jpg for r0c0/v2 from the current map and urteil."""
import json
import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont

B = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/"
E = B + "c-feste-liste/urteil/r0c0/v2/"
S = "C:/Users/Phil/AppData/Local/Temp/claude/27e54e3b8399faf6/a2bf01d3-627c-4b06-8b57-51f25ab5229e/scratchpad/punkte_bild.json"
L = tifffile.imread(B + "c-feste-liste/r0c0/labels.tif")
img = np.array(Image.open(B + "teilkacheln/r0c0.png").convert("RGB"))
segs = {s["id"]: s for s in json.load(open(B + "c-feste-liste/r0c0/segmente.json", encoding="utf-8"))["segmente"]}
kat = {c["code"]: c for c in json.load(open("C:/Users/Phil/Developement/Victor/landseg/kategorien.json", encoding="utf-8"))["classes"]}
P = json.load(open(S, encoding="utf-8"))
vorschlag = {int(k): v for k, v in P["vorschlag"].items()}
punkt = {int(k): v for k, v in P["punkt"].items()}

x0, y0, w, h, f = 282, 32, 314, 314, 3
sub = L[y0:y0 + h, x0:x0 + w]
base = np.kron(img[y0:y0 + h, x0:x0 + w].astype(float), np.ones((f, f, 1)))
lab = np.kron(sub, np.ones((f, f), dtype=sub.dtype))
edge = np.zeros(lab.shape, bool)
edge[:, 1:] |= lab[:, 1:] != lab[:, :-1]
edge[1:, :] |= lab[1:, :] != lab[:-1, :]
font = ImageFont.truetype("arial.ttf", 13)
fontb = ImageFont.truetype("arialbd.ttf", 15)


def frame(d):
    d.rectangle([(314 - x0) * f, (64 - y0) * f, (564 - x0) * f, (314 - y0) * f], outline=(0, 255, 255), width=2)


def kern_mask():
    yy, xx = np.mgrid[0:h * f, 0:w * f]
    tx, ty = x0 + xx // f, y0 + yy // f
    return (tx >= 314) & (tx <= 563) & (ty >= 64) & (ty <= 313)


def dim(arr):
    q = kern_mask()
    a = arr.copy()
    a[~q] = a[~q] * 0.55
    return a


def centre(i):
    if i in punkt:
        return punkt[i]
    ys, xs = np.nonzero(sub == i)
    cy, cx = np.median(ys), np.median(xs)
    k = np.argmin((ys - cy) ** 2 + (xs - cx) ** 2)
    return [int(xs[k]) + x0, int(ys[k]) + y0]


def legend(pil, text):
    W, H = pil.size
    out = Image.new("RGB", (W, H + 30), (20, 20, 20))
    out.paste(pil, (0, 0))
    ImageDraw.Draw(out).text((8, H + 7), text, fill=(255, 255, 255), font=font)
    return out


# roh
pil = Image.fromarray(base.astype(np.uint8))
frame(ImageDraw.Draw(pil))
legend(pil, "Roh: Teilkachel r0c0, Viertel v2 (cyan), 3fach; Schwarz-Weiß-Scan 1968").save(E + "roh.jpg", quality=90)

# umriss
a = dim(base)
a[edge] = [255, 230, 0]
pil = Image.fromarray(a.astype(np.uint8))
d = ImageDraw.Draw(pil)
frame(d)
for i in np.unique(sub):
    ys, xs = np.nonzero(sub == i)
    if len(xs) < 12:
        continue
    cx, cy = centre(int(i)) if int(i) in punkt else (int(np.median(xs)) + x0, int(np.median(ys)) + y0)
    if not (x0 <= cx < x0 + w and y0 <= cy < y0 + h) or sub[cy - y0, cx - x0] != i:
        cy, cx = centre(int(i))[1], centre(int(i))[0]
    col = (255, 255, 255) if int(i) in vorschlag else (170, 170, 170)
    d.text(((cx - x0) * f - 9, (cy - y0) * f - 7), str(int(i) % 100000), fill=col, font=font, stroke_width=2, stroke_fill=(0, 0, 0))
legend(pil, "Umriss: Grenzen gelb (Stand nach den Eingriffen), Nummer = ID mod 100000; weiß = Viertel v2, grau = Umgebung").save(E + "umriss.jpg", quality=90)

# maengel
a = dim(base)
a[edge] = [200, 180, 0]
pil = Image.fromarray(a.astype(np.uint8))
d = ImageDraw.Draw(pil)
frame(d)
kurz = {"klasse": "Kl", "trennen": "Tr", "verschmelzen": "Vs", "zu_klein": "kl", "sonstiges": "So", "grenze": "Gr", "fremdes": "Fr", "fehlt": "Fe"}
seen = {}
for p in P["punkte"]:
    x, y = p["x"], p["y"]
    k = seen.get((x, y), 0)
    seen[(x, y)] = k + 1
    px, py = (x - x0) * f, (y - y0) * f + k * 15
    d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=(255, 60, 60), outline=(0, 0, 0))
    d.text((px + 6, py - 8), f"{p['nr']} {kurz.get(p['art'], p['art'])}", fill=(255, 255, 255), font=font, stroke_width=2, stroke_fill=(0, 0, 0))
legend(pil, "Mängel: Punkt-Nr. wie in urteil.json; Kl = Klasse, Tr = trennen, Vs = verschmelzen, kl = zu klein, So = sonstiges").save(E + "maengel.jpg", quality=90)

# vorschlag
a = base.copy()
col = np.zeros_like(a)
has = np.zeros(lab.shape, bool)
for i, c in vorschlag.items():
    hexc = kat[c]["color"].lstrip("#")
    rgb = [int(hexc[j:j + 2], 16) for j in (0, 2, 4)]
    m = lab == i
    col[m] = rgb
    has |= m
a[has] = a[has] * 0.55 + col[has] * 0.45
a = dim(a)
a[edge] = [255, 255, 255]
pil = Image.fromarray(a.astype(np.uint8))
d = ImageDraw.Draw(pil)
frame(d)
for i, c in vorschlag.items():
    cx, cy = centre(i)
    if not (x0 <= cx < x0 + w and y0 <= cy < y0 + h):
        continue
    d.text(((cx - x0) * f - 10, (cy - y0) * f - 8), c, fill=(255, 255, 255), font=fontb, stroke_width=2, stroke_fill=(0, 0, 0))
legend(pil, "Vorschlag: Klassen, wie ich sie setzen würde (Code und Farbe aus kategorien.json); Grenzen = Stand nach den Eingriffen").save(E + "vorschlag.jpg", quality=90)
print("ok")
