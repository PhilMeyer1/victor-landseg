# bilder.py <config.json>: roh.jpg, umriss.jpg, maengel.jpg, vorschlag.jpg im Ordner der Konfiguration
import sys, json, os
import numpy as np, tifffile
from PIL import Image, ImageDraw, ImageFont
B = "C:/Users/Phil/Developement/Victor/daten/landseg/H0"
cfg = json.load(open(sys.argv[1], encoding="utf-8"))
out = os.path.dirname(os.path.abspath(sys.argv[1]))
img = np.array(Image.open(B + "/teilkacheln/r1c0.png").convert("L"))
L = tifffile.imread(B + "/b-kategorien-frei/r1c0/labels.tif")
x0, y0, w, h = cfg["fenster"]; f = cfg["faktor"]
vx, vy, vw, vh = cfg["viertel"]
eigene = set(cfg["eigene"])
font = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 13)
fontb = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 14)
crop = img[y0:y0+h, x0:x0+w]
base = np.kron(np.stack([crop]*3, -1), np.ones((f, f, 1), dtype=np.uint8))
Lc = L[y0:y0+h, x0:x0+w]; Lb = np.kron(Lc, np.ones((f, f), dtype=Lc.dtype))
edge = np.zeros(Lb.shape, bool)
edge[:, 1:] |= Lb[:, 1:] != Lb[:, :-1]; edge[1:, :] |= Lb[1:, :] != Lb[:-1, :]
def rahmen(d):
    d.rectangle([(vx-x0)*f, (vy-y0)*f, (vx+vw-x0)*f-1, (vy+vh-y0)*f-1], outline=(0, 255, 255), width=2)
    kx, ky = 64, 64
    d.rectangle([(kx-x0)*f, (ky-y0)*f, (kx+500-x0)*f-1, (ky+500-y0)*f-1], outline=(255, 255, 255), width=1)
def mitte(i):
    m = Lc == i
    ys, xs = np.nonzero(m)
    if not len(xs): return None
    # Punkt tief im Segment: Distanz zur Grenze maximal (grob ueber Erosion)
    mm = m.copy(); last = (ys, xs)
    for _ in range(40):
        e = mm.copy(); e[1:, :] &= mm[:-1, :]; e[:-1, :] &= mm[1:, :]; e[:, 1:] &= mm[:, :-1]; e[:, :-1] &= mm[:, 1:]
        e[0, :] = e[-1, :] = False; e[:, 0] = e[:, -1] = False
        if not e.any(): break
        mm = e; last = np.nonzero(mm)
    k = len(last[0]) // 2
    return last[1][k]*f + f//2, last[0][k]*f + f//2
def text(d, xy, s, fill, fnt=font):
    x, y = xy
    for dx, dy in ((-1,0),(1,0),(0,-1),(0,1)):
        d.text((x+dx, y+dy), s, font=fnt, fill=(0, 0, 0), anchor="mm")
    d.text((x, y), s, font=fnt, fill=fill, anchor="mm")
def legende(im, zeilen, titel):
    hh = 24 + 18 * max(1, len(zeilen))
    neu = Image.new("RGB", (im.width, im.height + hh), (20, 20, 20))
    neu.paste(im, (0, 0)); d = ImageDraw.Draw(neu)
    d.text((8, im.height + 4), titel, font=fontb, fill=(255, 255, 255))
    for k, z in enumerate(zeilen):
        d.text((8, im.height + 24 + 18*k), z, font=font, fill=(255, 255, 255))
    return neu
# roh
im = Image.fromarray(base.copy()); d = ImageDraw.Draw(im); rahmen(d)
im = legende(im, [], f"Teilkachel r1c0, Viertel {cfg['name']}: Bild unverändert (Fenster x {x0}–{x0+w-1}, y {y0}–{y0+h-1}, {f}fach), Viertel cyan")
im.save(out + "/roh.jpg", quality=90)
# umriss
a = base.copy(); a[edge] = [255, 255, 0]; im = Image.fromarray(a); d = ImageDraw.Draw(im); rahmen(d)
for i in np.unique(Lc):
    p = mitte(i)
    if p is None or (Lc == i).sum() < 15: continue
    text(d, p, str(int(i) % 100000), (255, 255, 255) if int(i) in eigene else (170, 170, 170))
im = legende(im, ["Nummer = ID mod 100000; weiß = Segment dieses Viertels nach dem Nachsegmentieren, grau = Nachbarn"], f"Viertel {cfg['name']}: Segmentgrenzen nach den Eingriffen")
im.save(out + "/umriss.jpg", quality=90)
# maengel
a = base.copy(); a[edge] = [200, 200, 0]; im = Image.fromarray(a); d = ImageDraw.Draw(im); rahmen(d)
zeilen = []
for nr, x, y, t in cfg["maengel"]:
    X, Y = (x - x0) * f, (y - y0) * f
    d.ellipse([X-11, Y-11, X+11, Y+11], fill=(220, 30, 30), outline=(255, 255, 255))
    d.text((X, Y), str(nr), font=fontb, fill=(255, 255, 255), anchor="mm")
    zeilen.append(f"{nr}: {t}")
if not zeilen: zeilen = ["keine Mängel"]
im = legende(im, zeilen, f"Viertel {cfg['name']}: Mängel und Eingriffe (Punkte im Teilkachelbild)")
im.save(out + "/maengel.jpg", quality=90)
# vorschlag
a = base.copy(); a[edge] = [255, 255, 0]; im = Image.fromarray(a); d = ImageDraw.Draw(im); rahmen(d)
zeilen = []
for i in np.unique(Lc):
    s = cfg["klassen"].get(str(int(i)))
    p = mitte(i)
    if p is None: continue
    if s:
        text(d, p, f"{int(i)%100000} {s}", (255, 255, 255))
    elif (Lc == i).sum() >= 15:
        text(d, p, str(int(i) % 100000), (150, 150, 150))
for k, v in cfg["klassen"].items():
    zeilen.append(f"{int(k)%100000}: {cfg['klassen_lang'].get(k, v)}")
im = legende(im, zeilen + [cfg.get("vermerk", "")], f"Viertel {cfg['name']}: Grenzen und Klassen (fein) wie vorgeschlagen; grau = andere Viertel")
im.save(out + "/vorschlag.jpg", quality=90)
print("ok")
