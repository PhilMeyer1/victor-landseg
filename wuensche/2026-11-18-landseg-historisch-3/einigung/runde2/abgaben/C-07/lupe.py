import json, sys
import numpy as np
from PIL import Image, ImageDraw
sys.stdout.reconfigure(encoding="utf-8")
D = "C:/Users/Phil/Developement/Victor/daten/landseg/H0"
OUT = "C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde2/abgaben/C-07"
man = json.load(open(D + "/manifest.json", encoding="utf-8"))
img = np.array(Image.open(D + "/" + man["ausschnitt"]["bild"]).convert("L"))
tk = {t["id"]: t for t in man["teilkacheln"]}

def labels(tid):
    lab = np.array(Image.open(f"{D}/c-feste-liste/{tid}/labels.tif"))
    return lab, tk[tid]["kontext"]["x"], tk[tid]["kontext"]["y"]

x0, y0, x1, y1, f = [int(v) for v in sys.argv[1:6]]
name = sys.argv[6]
segs = sys.argv[7:]  # tid:id:farbe
crop = img[y0:y1, x0:x1]
# Kontrast strecken
lo, hi = np.percentile(crop, 1), np.percentile(crop, 99)
c = np.clip((crop.astype(float) - lo) / max(hi - lo, 1) * 255, 0, 255).astype(np.uint8)
H, W = c.shape
left = Image.fromarray(c).convert("RGB").resize((W * f, H * f), Image.NEAREST)
right = left.copy()
dr = ImageDraw.Draw(right)
colors = {"c": (0, 255, 255), "m": (255, 0, 255), "g": (0, 255, 0), "r": (255, 60, 60), "y": (255, 255, 0), "b": (80, 140, 255)}
for s in segs:
    tid, sid, col = s.split(":")
    lab, kx, ky = labels(tid)
    m = np.zeros((H, W), bool)
    for yy in range(H):
        for xx in range(W):
            ly, lx = y0 + yy - ky, x0 + xx - kx
            if 0 <= ly < lab.shape[0] and 0 <= lx < lab.shape[1] and lab[ly, lx] == int(sid):
                m[yy, xx] = True
    # Umriss zeichnen
    for yy in range(H):
        for xx in range(W):
            if not m[yy, xx]:
                continue
            for dy, dx in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                ny, nx = yy + dy, xx + dx
                if not (0 <= ny < H and 0 <= nx < W) or not m[ny, nx]:
                    X, Y = xx * f, yy * f
                    if dx == 1: dr.line([(X + f - 1, Y), (X + f - 1, Y + f - 1)], fill=colors[col])
                    if dx == -1: dr.line([(X, Y), (X, Y + f - 1)], fill=colors[col])
                    if dy == 1: dr.line([(X, Y + f - 1), (X + f - 1, Y + f - 1)], fill=colors[col])
                    if dy == -1: dr.line([(X, Y), (X + f - 1, Y)], fill=colors[col])
    print(s, "px im Ausschnitt:", int(m.sum()))
# Naht x=500 / y=500 markieren
for sx in (500,):
    if x0 <= sx < x1:
        X = (sx - x0) * f
        dr.line([(X, 0), (X, H * f)], fill=(255, 255, 255), width=1)
out = Image.new("RGB", (W * f * 2 + 8, H * f), (20, 20, 20))
out.paste(left, (0, 0)); out.paste(right, (W * f + 8, 0))
s = 2000 / max(out.size)
if s < 1:
    out = out.resize((int(out.size[0] * s), int(out.size[1] * s)))
out.save(f"{OUT}/{name}", quality=90)
print("gespeichert", name, out.size)
