"""naht_<n>.jpg je Verstoß: roh (kontrastverstärkt), Grenzen vorher, Grenzen nachher; Kerngrenze
gestrichelt cyan, die Verstoß-Strecke gelb neben der Grenze. Optional Entscheidungen aus
entscheidungen.json (n -> Text). Aufruf: einzel.py <zusammen-ordner-vorher> <zusammen-ordner-nachher> <ziel>"""
import json
import sys
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont

H0 = Path("C:/Users/Phil/Developement/Victor/daten/landseg/H0")
WERK = Path(__file__).parent
vorher_dir, nachher_dir, ziel = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
ziel.mkdir(parents=True, exist_ok=True)
bild = np.asarray(Image.open(H0 / "H0.png").convert("L"), dtype=np.float32)
kv = tifffile.imread(vorher_dir / "labels.tif")
kn = tifffile.imread(nachher_dir / "labels.tif")
verst = json.load(open(WERK / "streifen" / "verstoesse.json", encoding="utf-8"))
ent = {}
if (WERK / "entscheidungen.json").exists():
    ent = {int(k): v for k, v in json.load(open(WERK / "entscheidungen.json", encoding="utf-8")).items()}
FONT = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 16)
S, R = 8, 22


def kontrast(a):
    lo, hi = np.percentile(a, 1), np.percentile(a, 99)
    return np.clip((a - lo) / max(hi - lo, 1) * 255, 0, 255).astype(np.uint8)


def raender(k):
    r = np.zeros(k.shape, bool)
    r[:, 1:] |= k[:, 1:] != k[:, :-1]
    r[1:, :] |= k[1:, :] != k[:-1, :]
    return r


nur = set(int(x) for x in sys.argv[4].split(",")) if len(sys.argv) > 4 else None
for v in verst:
    n = v["n"]
    if nur and n not in nur:
        continue
    senk = v["naht"] in ("r0c0|r0c1", "r1c0|r1c1")
    (ax, ay), (bx, by) = v["von"], v["bis"]
    cx, cy = (ax + bx) // 2, (ay + by) // 2
    halb_lang = max(R, (max(bx - ax, by - ay) // 2) + 6)
    if senk:
        x0, x1, y0, y1 = cx - R, cx + R, cy - halb_lang, cy + halb_lang
    else:
        x0, x1, y0, y1 = cx - halb_lang, cx + halb_lang, cy - R, cy + R
    x0, y0, x1, y1 = max(x0, 0), max(y0, 0), min(x1, 1000), min(y1, 1000)
    roh = kontrast(bild[y0:y1, x0:x1])
    h, w = roh.shape
    S = max(2, min(8, 1500 // max(h, w)))
    groß = Image.fromarray(np.kron(roh, np.ones((S, S), np.uint8))).convert("RGB")
    tafeln = [groß.copy()]
    for k in (kv, kn):
        rgb = np.asarray(groß).copy()
        kg = np.kron(k[y0:y1, x0:x1], np.ones((S, S), k.dtype))
        rgb[raender(kg)] = (255, 40, 40)
        tafeln.append(Image.fromarray(rgb))
    for t in tafeln:
        d = ImageDraw.Draw(t)
        if senk:
            gx = (500 - x0) * S
            for yy in range(0, h * S, 10):
                d.line([(gx, yy), (gx, yy + 5)], fill=(0, 220, 255), width=2)
            d.line([(gx - 2 * S, (ay - y0) * S), (gx - 2 * S, (by - y0 + 1) * S)], fill=(255, 220, 0), width=3)
        else:
            gy = (500 - y0) * S
            for xx in range(0, w * S, 10):
                d.line([(xx, gy), (xx + 5, gy)], fill=(0, 220, 255), width=2)
            d.line([((ax - x0) * S, gy - 2 * S), ((bx - x0 + 1) * S, gy - 2 * S)], fill=(255, 220, 0), width=3)
    pw, ph = w * S, h * S
    kopf = 70
    stapeln = pw > 600
    if stapeln:
        orte = [(0, kopf + i * (ph + 30)) for i in range(3)]
        ges = Image.new("RGB", (max(pw, 900), kopf + 3 * (ph + 30) + 10), "white")
    else:
        orte = [(i * (pw + 20), kopf) for i in range(3)]
        ges = Image.new("RGB", (max(3 * pw + 40, 900), ph + kopf + 50), "white")
    for t, (ox, oy) in zip(tafeln, orte):
        ges.paste(t, (ox, oy))
    d = ImageDraw.Draw(ges)
    d.text((5, 5), f"Verstoß {n}: Naht {v['naht']}, Segmente {v['ids'][0]} | {v['ids'][1]}, "
                   f"{v['laenge']} Bildpunkte ab x {ax}, y {ay}", fill="black", font=FONT)
    d.text((5, 27), f"Ausschnitt x {x0}..{x1 - 1}, y {y0}..{y1 - 1}, {S}-fach; cyan = Kerngrenze, gelb = Strecke",
           fill="black", font=FONT)
    for (ox, oy), z in zip(orte, ("Bild (Kontrast verstärkt)", "Grenzen vorher", "Grenzen nachher")):
        d.text((ox + 5, oy - 22), z, fill="black", font=FONT)
    ph = orte[-1][1] + ph - kopf
    if n in ent:
        import textwrap
        breite = max(40, int(ges.width / 8.5))
        zeilen = textwrap.wrap("Entscheidung: " + ent[n], breite)
        neu = Image.new("RGB", (ges.width, ph + kopf + 20 + 20 * len(zeilen)), "white")
        neu.paste(ges.crop((0, 0, ges.width, ph + kopf + 5)), (0, 0))
        ges = neu
        d = ImageDraw.Draw(ges)
        for i, z in enumerate(zeilen):
            d.text((5, ph + kopf + 8 + 20 * i), z, fill="black", font=FONT)
    if ges.width > 2000 or ges.height > 2000:
        f = 2000 / max(ges.size)
        ges = ges.resize((int(ges.width * f), int(ges.height * f)), Image.LANCZOS)
    ges.save(ziel / f"naht_{n}.jpg", quality=88)
print("fertig")
