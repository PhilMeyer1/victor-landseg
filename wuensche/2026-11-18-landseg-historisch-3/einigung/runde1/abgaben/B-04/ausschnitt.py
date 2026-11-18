from PIL import Image, ImageDraw
import sys
H0 = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png"
OUT = "C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde1/abgaben/B-04/"
im = Image.open(H0).convert("RGB")
def crop(name, x0, y0, x1, y1, f, linien=()):
    c = im.crop((x0, y0, x1, y1)).resize(((x1 - x0) * f, (y1 - y0) * f), Image.NEAREST)
    d = ImageDraw.Draw(c)
    for (ax, ay, bx, by) in linien:
        d.line(((ax - x0) * f, (ay - y0) * f, (bx - x0) * f, (by - y0) * f), fill=(255, 220, 0), width=1)
    c.save(OUT + name, quality=90)
    print(name, c.size)
crop("einigung_01.jpg", 380, 380, 640, 640, 5, [(500, 380, 500, 640), (380, 500, 640, 500)])
crop("einigung_07.jpg", 0, 640, 260, 860, 6, [(0, 750, 260, 750)])
crop("einigung_02.jpg", 440, 420, 560, 560, 10, [(500, 420, 500, 560), (440, 500, 560, 500)])
