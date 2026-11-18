import json, sys
import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont

H0 = "C:/Users/Phil/Developement/Victor/daten/landseg/H0"
AUF = "C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde1/auftraege-A/A-14/auftrag.json"
OUT = "C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde1/abgaben/A-14"
OFF = 436
img = np.array(Image.open(f"{H0}/teilkacheln/r1c1.png").convert("L")).astype(float)
lab = tifffile.imread(f"{H0}/a-alles-frei/r1c1/labels.tif")
seg = {s["id"]: s for s in json.load(open(f"{H0}/a-alles-frei/r1c1/segmente.json", encoding="utf-8"))["segmente"]}
auf = json.load(open(AUF, encoding="utf-8"))
nrs = [int(a) for a in sys.argv[1:]] or [p["nr"] for p in auf["paare"]]
R = int(26)
S = 18
try:
    font = ImageFont.truetype("arial.ttf", 15)
    fontb = ImageFont.truetype("arialbd.ttf", 17)
except Exception:
    font = fontb = ImageFont.load_default()

for p in auf["paare"]:
    if p["nr"] not in nrs:
        continue
    st = p["strecken"][0]
    cx, cy = st["von"][0] - OFF, st["von"][1] - OFF
    ids = [s["id"] for s in p["segmente"]]
    x0, y0 = cx - R, cy - R
    crop = img[y0:y0 + 2 * R + 1, x0:x0 + 2 * R + 1]
    lc = lab[y0:y0 + 2 * R + 1, x0:x0 + 2 * R + 1]
    lo, hi = np.percentile(crop, 1), np.percentile(crop, 99)
    c = np.clip((crop - lo) / max(hi - lo, 1) * 255, 0, 255).astype(np.uint8)
    big = np.kron(c, np.ones((S, S), dtype=np.uint8))
    h, w = big.shape
    left = Image.fromarray(big).convert("RGB")
    right = left.copy()
    d = ImageDraw.Draw(right)
    cols = {ids[0]: (0, 230, 230), ids[1]: (255, 0, 255)}
    for yy in range(lc.shape[0]):
        for xx in range(lc.shape[1]):
            v = lc[yy, xx]
            if xx + 1 < lc.shape[1] and lc[yy, xx + 1] != v:
                X = (xx + 1) * S
                col = (255, 255, 0) if {v, lc[yy, xx + 1]} == set(ids) else (cols.get(v) or cols.get(lc[yy, xx + 1]) or (255, 120, 0))
                wd = 3 if (v in cols or lc[yy, xx + 1] in cols) else 1
                d.line([(X, yy * S), (X, (yy + 1) * S)], fill=col, width=wd)
            if yy + 1 < lc.shape[0] and lc[yy + 1, xx] != v:
                Y = (yy + 1) * S
                col = (255, 255, 0) if {v, lc[yy + 1, xx]} == set(ids) else (cols.get(v) or cols.get(lc[yy + 1, xx]) or (255, 120, 0))
                wd = 3 if (v in cols or lc[yy + 1, xx] in cols) else 1
                d.line([(xx * S, Y), ((xx + 1) * S, Y)], fill=col, width=wd)
    # labels at segment centroids within crop
    for v in np.unique(lc):
        yy, xx = np.nonzero(lc == v)
        if len(yy) < 6 and v not in cols:
            continue
        k = int(np.argmin((yy - yy.mean()) ** 2 + (xx - xx.mean()) ** 2))
        s = seg.get(int(v), {})
        t = f"{s.get('klasse','?')} #{int(v)%1000}"
        X, Y = xx[k] * S, yy[k] * S
        d.text((X + 1, Y + 1), t, fill=(0, 0, 0), font=font)
        d.text((X, Y), t, fill=cols.get(v, (255, 255, 255)), font=font)
    # mark contact point
    d.ellipse([(R * S - 8, R * S - 8), (R * S + S + 8, R * S + S + 8)], outline=(255, 60, 60), width=2)
    canvas = Image.new("RGB", (2 * w + 20, h + 50), (20, 20, 25))
    canvas.paste(left, (0, 50))
    canvas.paste(right, (w + 20, 50))
    dd = ImageDraw.Draw(canvas)
    a, b = p["segmente"]
    dd.text((8, 4), f"Paar {p['nr']}: Ausschnitt x {x0+OFF}–{x0+OFF+2*R}, y {y0+OFF}–{y0+OFF+2*R}, {S}-fach; roter Kreis = Berührpunkt", fill=(255, 255, 255), font=fontb)
    dd.text((8, 26), f"türkis #{a['id']%1000} {a['klasse']} ({a['grauwert']})   magenta #{b['id']%1000} {b['klasse']} ({b['grauwert']})   gelb: gemeinsame Grenze, orange: andere Grenzen", fill=(255, 230, 120), font=font)
    if canvas.width > 2000:
        f = 2000 / canvas.width
        canvas = canvas.resize((2000, int(canvas.height * f)), Image.LANCZOS)
    canvas.save(f"{OUT}/einigung_{p['nr']:02d}.jpg", quality=90)
    # neighbours info
    print(p["nr"], "Nachbarn im Ausschnitt:", sorted({(int(v) % 1000, seg.get(int(v), {}).get('klasse')) for v in np.unique(lc)}))
