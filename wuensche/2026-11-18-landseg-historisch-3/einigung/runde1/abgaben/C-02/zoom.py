import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

H0 = "C:/Users/Phil/Developement/Victor/daten/landseg/H0"
OUT = "C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde1/abgaben/C-02"

img = np.array(Image.open(H0 + "/H0.png").convert("L"))
lab = np.array(Image.open(H0 + "/c-feste-liste/zusammen/labels.tif"))


def zoom(name, x0, y0, x1, y1, ids, f):
    crop = img[y0:y1, x0:x1]
    L = lab[y0:y1, x0:x1]
    roh = Image.fromarray(crop).resize(((x1 - x0) * f, (y1 - y0) * f), Image.NEAREST).convert("RGB")
    ov = np.stack([crop] * 3, -1).astype(float)
    farben = [(0, 200, 220), (230, 0, 200), (255, 140, 0), (60, 220, 60), (80, 120, 255), (255, 60, 60)]
    for i, sid in enumerate(ids):
        m = L == sid
        c = np.array(farben[i % len(farben)])
        ov[m] = ov[m] * 0.5 + c * 0.5
    ov = Image.fromarray(ov.astype(np.uint8)).resize(roh.size, Image.NEAREST)
    # Grenzen aller Segmente
    Lb = np.kron(L, np.ones((f, f), dtype=L.dtype))
    rand = np.zeros(Lb.shape, bool)
    rand[:, 1:] |= Lb[:, 1:] != Lb[:, :-1]
    rand[1:, :] |= Lb[1:, :] != Lb[:-1, :]
    a = np.array(ov)
    a[rand] = (255, 255, 255)
    ov = Image.fromarray(a)
    W = roh.size[0] * 2 + 10
    out = Image.new("RGB", (W, roh.size[1] + 30), (20, 20, 25))
    out.paste(roh, (0, 30))
    out.paste(ov, (roh.size[0] + 10, 30))
    d = ImageDraw.Draw(out)
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 16)
    except Exception:
        font = None
    txt = f"{name}: x {x0}–{x1}, y {y0}–{y1}, {f}-fach; Farben: " + ", ".join(
        f"{n}={s}" for n, s in zip(["türkis", "magenta", "orange", "grün", "blau", "rot"], ids))
    d.text((5, 5), txt, fill=(255, 230, 80), font=font)
    out.save(OUT + "/" + name + ".jpg", quality=90)
    # IDs je Zeile y=499/500 drucken
    return out.size


if __name__ == "__main__":
    print(zoom("einigung_07", 270, 470, 380, 540, [100154, 300080, 100224, 300075, 100220, 100225], 9))
    print(zoom("einigung_04", 370, 225, 430, 275, [100143, 100149, 100198, 100172, 100167], 14))
    print(zoom("einigung_11", 315, 480, 365, 530, [100225, 300080, 300006, 300075, 100220], 16))
    # Zeilen um die Naht
    for y in (498, 499, 500, 501, 502):
        print(y, " ".join(str(v % 1000) for v in lab[y, 285:345]))
