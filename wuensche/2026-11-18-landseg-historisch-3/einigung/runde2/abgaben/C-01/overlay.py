"""Paar-Ansichten mit groesserem Umfeld fuer die Einigung C-01 (nur lesen)."""
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageOps

D = Path("C:/Users/Phil/Developement/Victor/daten/landseg/H0")
C = D / "c-feste-liste"
OUT = Path(__file__).resolve().parent
MAN = json.loads((D / "manifest.json").read_text(encoding="utf-8"))
KONTEXT = {t["id"]: t["kontext"] for t in MAN["teilkacheln"]}
KERN = {t["id"]: t["kern"] for t in MAN["teilkacheln"]}


def lade_labels(tk):
    try:
        import tifffile
        arr = tifffile.imread(C / tk / "labels.tif")
    except ImportError:
        arr = np.array(Image.open(C / tk / "labels.tif"))
    return arr.astype(np.int64)


def maske_global(tk, sid, x0, y0, x1, y1, labels):
    """Maske des Segments im Ausschnitt [x0,x1)x[y0,y1), nur im Kern der Teilkachel."""
    k = KONTEXT[tk]
    kern = KERN[tk]
    m = np.zeros((y1 - y0, x1 - x0), bool)
    for yy in range(y0, y1):
        for xx in range(x0, x1):
            if not (kern["x"] <= xx < kern["x"] + kern["breite"] and kern["y"] <= yy < kern["y"] + kern["hoehe"]):
                continue
            ix, iy = xx - k["x"], yy - k["y"]
            if 0 <= iy < labels.shape[0] and 0 <= ix < labels.shape[1] and labels[iy, ix] == sid:
                m[yy - y0, xx - x0] = True
    return m


def main():
    nrs = [int(a) for a in sys.argv[1:]]
    auftrag = json.loads((Path("C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde2/auftraege-C/C-01/auftrag.json")).read_text(encoding="utf-8"))
    img = Image.open(D / "H0.png").convert("L")
    cache = {}
    for p in auftrag["paare"]:
        if nrs and p["nr"] not in nrs:
            continue
        xs = [s["von"][0] for s in p["strecken"]] + [s["bis"][0] for s in p["strecken"]]
        ys = [s["von"][1] for s in p["strecken"]] + [s["bis"][1] for s in p["strecken"]]
        cx, cy = (min(xs) + max(xs)) // 2, (min(ys) + max(ys)) // 2
        r = 45
        x0, y0 = max(0, cx - r), max(0, cy - r)
        x1, y1 = min(1000, cx + r), min(1000, cy + r)
        f = 8
        crop = ImageOps.autocontrast(img.crop((x0, y0, x1, y1)), cutoff=1)
        roh = crop.resize(((x1 - x0) * f, (y1 - y0) * f), Image.NEAREST).convert("RGB")
        ov = roh.copy()
        d = ImageDraw.Draw(ov)
        farben = [(0, 230, 230), (255, 0, 255)]
        for s, col in zip(p["segmente"], farben):
            tk, sid = s["segment"].split(":")
            if tk not in cache:
                cache[tk] = lade_labels(tk)
            m = maske_global(tk, int(sid), x0, y0, x1, y1, cache[tk])
            # Umriss: Bildpunkte der Maske mit Nachbar ausserhalb
            for yy in range(m.shape[0]):
                for xx in range(m.shape[1]):
                    if not m[yy, xx]:
                        continue
                    rand = any(
                        not (0 <= yy + dy < m.shape[0] and 0 <= xx + dx < m.shape[1]) or not m[yy + dy, xx + dx]
                        for dy, dx in ((0, 1), (1, 0), (0, -1), (-1, 0))
                    )
                    if rand:
                        d.rectangle([xx * f + 2, yy * f + 2, xx * f + f - 3, yy * f + f - 3], outline=col)
        w = roh.width
        bild = Image.new("RGB", (w * 2 + 10, roh.height + 24), (20, 20, 20))
        bild.paste(roh, (0, 24))
        bild.paste(ov, (w + 10, 24))
        ImageDraw.Draw(bild).text((4, 4), f"Paar {p['nr']}  x {x0}-{x1}, y {y0}-{y1}, 8-fach; tuerkis {p['segmente'][0]['segment']}, magenta {p['segmente'][1]['segment']} (nur Kernanteile)", fill=(255, 255, 0))
        if bild.width > 2000:
            s = 2000 / bild.width
            bild = bild.resize((2000, int(bild.height * s)), Image.LANCZOS)
        name = OUT / f"einigung_{p['nr']:02d}.jpg"
        bild.save(name, quality=90)
        print(name.name, bild.size)


if __name__ == "__main__":
    main()
