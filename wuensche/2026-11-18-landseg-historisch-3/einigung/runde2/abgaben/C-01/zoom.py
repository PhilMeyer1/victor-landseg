"""Eigene Vergroesserungen fuer die Einigung C-01 (nur lesen, Bilder nur in diesem Ordner)."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageOps

H0 = Path("C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png")
OUT = Path(__file__).resolve().parent

# name, x0, y0, x1, y1, faktor, Markierungen [(x, y)]
AUSSCHNITTE = [
    ("einigung_01", 440, 0, 600, 140, 6, []),
    ("einigung_07", 440, 150, 600, 300, 6, []),
    ("einigung_09", 440, 370, 600, 520, 6, []),
]


def main():
    img = Image.open(H0).convert("L")
    for name, x0, y0, x1, y1, f, marks in AUSSCHNITTE:
        crop = img.crop((x0, y0, x1, y1))
        crop = ImageOps.autocontrast(crop, cutoff=1)
        crop = crop.resize(((x1 - x0) * f, (y1 - y0) * f), Image.NEAREST).convert("RGB")
        d = ImageDraw.Draw(crop)
        # Naht x = 500 und Naht y = 500 als gestrichelte gelbe Linie
        if x0 < 500 < x1:
            sx = (500 - x0) * f
            for yy in range(0, crop.height, 12):
                d.line([(sx, yy), (sx, yy + 5)], fill=(255, 220, 0), width=1)
        if y0 < 500 < y1:
            sy = (500 - y0) * f
            for xx in range(0, crop.width, 12):
                d.line([(xx, sy), (xx + 5, sy)], fill=(255, 220, 0), width=1)
        # Gitter alle 20 px mit Beschriftung
        for gx in range((x0 // 20 + 1) * 20, x1, 20):
            d.text(((gx - x0) * f + 2, 2), str(gx), fill=(0, 255, 255))
        for gy in range((y0 // 20 + 1) * 20, y1, 20):
            d.text((2, (gy - y0) * f + 2), str(gy), fill=(0, 255, 255))
        for gx in range((x0 // 20 + 1) * 20, x1, 20):
            d.line([((gx - x0) * f, 0), ((gx - x0) * f, 8)], fill=(0, 255, 255))
        for gy in range((y0 // 20 + 1) * 20, y1, 20):
            d.line([(0, (gy - y0) * f), (8, (gy - y0) * f)], fill=(0, 255, 255))
        crop.save(OUT / f"{name}.jpg", quality=90)
        print(name, crop.size)


if __name__ == "__main__":
    sys.exit(main())
