"""Eigene Kontextbilder fuer Buendel B-05 (nur lesen, Ausgabe im eigenen Ordner)."""
import sys
import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont

H0 = "C:/Users/Phil/Developement/Victor/daten/landseg/H0"
OUT = "C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde1/abgaben/B-05"

img = np.array(Image.open(H0 + "/H0.png").convert("L")).astype(np.float32)
lab = tifffile.imread(H0 + "/b-kategorien-frei/zusammen/labels.tif")

FARBEN = [(0, 220, 220), (230, 0, 230), (255, 140, 0), (60, 220, 60), (80, 120, 255), (255, 60, 60)]


def bild(name, x0, y0, x1, y1, ids, scale, kontrast=False):
    g = img[y0:y1, x0:x1].copy()
    if kontrast:
        lo, hi = np.percentile(g, 1), np.percentile(g, 99)
        g = np.clip((g - lo) / max(hi - lo, 1) * 255, 0, 255)
    g = g.astype(np.uint8)
    L = lab[y0:y1, x0:x1]
    rgb = np.stack([g] * 3, -1).astype(np.float32)
    ov = rgb.copy()
    # Segmentgrenzen aller Segmente (duenn, weiss)
    rand = np.zeros(L.shape, bool)
    rand[:, 1:] |= L[:, 1:] != L[:, :-1]
    rand[1:, :] |= L[1:, :] != L[:-1, :]
    for k, i in enumerate(ids):
        m = L == i
        c = np.array(FARBEN[k % len(FARBEN)], np.float32)
        ov[m] = ov[m] * 0.55 + c * 0.45
    ov[rand] = (255, 255, 255)
    # Naht- und Viertellinien gelb
    for v in (250, 500, 750):
        if x0 <= v < x1:
            ov[:, v - x0] = (255, 230, 0)
        if y0 <= v < y1:
            ov[v - y0, :] = (255, 230, 0)
    a = Image.fromarray(rgb.astype(np.uint8)).resize(((x1 - x0) * scale, (y1 - y0) * scale), Image.NEAREST)
    b = Image.fromarray(ov.astype(np.uint8)).resize(((x1 - x0) * scale, (y1 - y0) * scale), Image.NEAREST)
    W = a.width * 2 + 10
    out = Image.new("RGB", (W, a.height + 40), (20, 20, 25))
    out.paste(a, (0, 40))
    out.paste(b, (a.width + 10, 40))
    d = ImageDraw.Draw(out)
    try:
        f = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 16)
    except Exception:
        f = ImageFont.load_default()
    txt = f"{name}: Ausschnitt x {x0}–{x1}, y {y0}–{y1}, {scale}-fach; " + ", ".join(
        f"{i}" for i in ids) + " (Farben türkis, magenta, orange, grün, blau, rot); gelb: Naht/Viertel"
    d.text((6, 10), txt, fill=(255, 230, 0), font=f)
    if out.width > 2000:
        r = 2000 / out.width
        out = out.resize((2000, int(out.height * r)), Image.LANCZOS)
    out.save(f"{OUT}/{name}.jpg", quality=90)
    print(name, out.size)


if __name__ == "__main__":
    name = sys.argv[1]
    x0, y0, x1, y1, scale = map(int, sys.argv[2:7])
    ids = [int(s) for s in sys.argv[7].split(",")] if len(sys.argv) > 7 and sys.argv[7] else []
    k = len(sys.argv) > 8 and sys.argv[8] == "k"
    bild(name, x0, y0, x1, y1, ids, scale, k)
