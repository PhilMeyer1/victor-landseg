import json, os, sys
import numpy as np, tifffile
from PIL import Image, ImageDraw, ImageFont
H0 = "C:/Users/Phil/Developement/Victor/daten/landseg/H0"
B = H0 + "/b-kategorien-frei"
E = "C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/naht-B"
ziel = sys.argv[1] if len(sys.argv) > 1 else E
nur = set(int(x) for x in sys.argv[2].split(",")) if len(sys.argv) > 2 and sys.argv[2] else None
ents = {}
if os.path.exists(E + "/naht_abgabe.json"):
    ab = json.load(open(E + "/naht_abgabe.json", encoding="utf-8"))
    for i, v in enumerate(ab["verstoesse"], 1): ents[i] = v["entscheidung"]
bild = np.asarray(Image.open(H0 + "/H0.png").convert("L")).astype(np.float32)
karte = tifffile.imread(B + "/zusammen/labels.tif")
nd = json.load(open(B + "/zusammen/naht.json", encoding="utf-8"))
seg = json.load(open(B + "/zusammen/segmente.json", encoding="utf-8"))
kl = {e["id"]: e.get("klasse") for e in seg["segmente"]}
f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 15)
R = 24; S = 7
for n, v in enumerate(nd["verstoesse"], 1):
    if nur and n not in nur: continue
    a, b = v["ids"]; senk = v["naht"] in ("r0c0|r0c1", "r1c0|r1c1")
    cx = (v["von"][0] + v["bis"][0]) // 2; cy = (v["von"][1] + v["bis"][1]) // 2
    x0 = min(max(cx - R, 0), 1000 - 2 * R); y0 = min(max(cy - R, 0), 1000 - 2 * R)
    g = bild[y0:y0 + 2 * R, x0:x0 + 2 * R]; k = karte[y0:y0 + 2 * R, x0:x0 + 2 * R]
    lo, hi = np.percentile(g, 1), np.percentile(g, 99)
    g8 = np.clip((g - lo) / max(hi - lo, 1) * 255, 0, 255).astype(np.uint8)
    roh = np.repeat(np.repeat(np.stack([g8] * 3, -1), S, 0), S, 1)
    mit = roh.copy()
    kk = np.repeat(np.repeat(k, S, 0), S, 1)
    rand = np.zeros(kk.shape, bool)
    rand[:, 1:] |= kk[:, 1:] != kk[:, :-1]; rand[1:, :] |= kk[1:, :] != kk[:-1, :]
    mit[rand] = (255, 220, 0)
    # IDs a und b leicht einfärben
    for sid, farbe in ((a, (255, 80, 80)), (b, (80, 160, 255))):
        m = kk == sid
        mit[m] = (0.65 * mit[m] + 0.35 * np.array(farbe)).astype(np.uint8)
    pan = []
    for arr in (roh, mit):
        im = Image.fromarray(arr); d = ImageDraw.Draw(im)
        if senk:
            x = (v["von"][0] - x0) * S
            for yy in range(0, im.height, 10): d.line([(x, yy), (x, yy + 5)], fill=(0, 220, 255), width=2)
            ya = (v["von"][1] - y0) * S; yb = (v["bis"][1] - y0 + 1) * S
            d.rectangle([x - 4, ya, x + 3, yb], outline=(255, 0, 0), width=2)
        else:
            y = (v["von"][1] - y0) * S
            for xx in range(0, im.width, 10): d.line([(xx, y), (xx + 5, y)], fill=(0, 220, 255), width=2)
            xa = (v["von"][0] - x0) * S; xb = (v["bis"][0] - x0 + 1) * S
            d.rectangle([xa, y - 4, xb, y + 3], outline=(255, 0, 0), width=2)
        pan.append(im)
    Wp = pan[0].width
    can = Image.new("RGB", (2 * Wp + 10, Wp + 70), (255, 255, 255))
    can.paste(pan[0], (0, 50)); can.paste(pan[1], (Wp + 10, 50))
    d = ImageDraw.Draw(can)
    ent = ents.get(n, "")
    d.text((4, 2), f"Verstoß {n}: Naht {v['naht']}, Segmente {a} ({kl.get(a)}) | {b} ({kl.get(b)}), {v['laenge']} Bildpunkte, Kante max. {v['kante_max']}", fill=(0, 0, 0), font=f)
    d.text((4, 22), f"links Bild (Kontrast verstärkt), rechts vorher = nachher: rot {a}, blau {b}; Entscheidung: {ent or '-'}", fill=(0, 0, 0), font=f)
    d.text((4, Wp + 52), f"gestrichelt: Kerngrenze; roter Rahmen: Verstoßstrecke; Ausschnitt x {x0}–{x0+2*R}, y {y0}–{y0+2*R}", fill=(60, 60, 60), font=f)
    can.save(f"{ziel}/naht_{n}.jpg", quality=88)
