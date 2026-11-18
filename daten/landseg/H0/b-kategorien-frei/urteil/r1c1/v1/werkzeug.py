"""Hilfswerkzeug urt-b-r1c1: Ansichten, Kennzahlen, Stapel-Simulation (schreibt nie auf die Karte).

Aufruf (im Ordner landseg):
  PY -B werkzeug.py bild --x 64 --y 64 --b 125 --h 125 --f 8 --ziel out.jpg [--stapel s.json] [--roh]
  PY -B werkzeug.py stat --ids 1,2,3 [--stapel s.json]
  PY -B werkzeug.py sim --stapel s.json
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

sys.path.insert(0, "C:/Users/Phil/Developement/Victor/landseg")
from landseg import dateien, kategorien  # noqa: E402
from landseg.eingriff import Bearbeitung  # noqa: E402

BASIS = Path("C:/Users/Phil/Developement/Victor/daten/landseg/H0")
LABELS = BASIS / "b-kategorien-frei/r1c1/labels.tif"
SEGM = BASIS / "b-kategorien-frei/r1c1/segmente.json"
BILD = BASIS / "teilkacheln/r1c1.png"
KERN = (64, 64, 564, 564)


def laden(stapel=None, leise=False):
    karte = dateien.lese_labels(LABELS)
    seg = dateien.lese_segmente(SEGM)
    if stapel:
        kat = kategorien.laden(None)
        arb = Bearbeitung(karte, seg, kat, "sim")
        for nr, s in enumerate(json.loads(Path(stapel).read_text(encoding="utf-8"))["schritte"], 1):
            erg = arb.anwenden(s)
            if not leise:
                print(f"{nr}. {s['op']} {s.get('id', '')}: {json.dumps(erg, ensure_ascii=False)}")
        karte, seg = arb.karte, arb.segmente
    return karte, seg


def font(gr):
    for p in ("C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"):
        try:
            return ImageFont.truetype(p, gr)
        except OSError:
            pass
    return ImageFont.load_default()


def bild(a):
    karte, seg = laden(a.stapel, leise=True)
    img = np.asarray(Image.open(BILD).convert("L")).astype(np.float32)
    x0, y0, w, h, f = a.x, a.y, a.b, a.h, a.f
    crop = img[y0:y0 + h, x0:x0 + w]
    if a.kontrast:
        lo, hi = np.percentile(crop, 1), np.percentile(crop, 99)
        crop = np.clip((crop - lo) / max(hi - lo, 1) * 255, 0, 255)
    rgb = np.stack([crop] * 3, -1).astype(np.uint8)
    rgb = np.kron(rgb, np.ones((f, f, 1), np.uint8))
    lab = karte[y0:y0 + h, x0:x0 + w]
    if not a.roh:
        labf = np.kron(lab, np.ones((f, f), np.uint32))
        rand = np.zeros(labf.shape, bool)
        rand[:, 1:] |= labf[:, 1:] != labf[:, :-1]
        rand[1:, :] |= labf[1:, :] != labf[:-1, :]
        rgb[rand] = (255, 230, 0)
    im = Image.fromarray(rgb)
    d = ImageDraw.Draw(im)
    # Kern und Viertel
    for (ax, ay, bx, by), col in ((KERN, (255, 255, 255)), ((64, 64, 314, 314), (0, 255, 255)),
                                  ((314, 64, 564, 314), (0, 255, 255)), ((64, 314, 314, 564), (0, 255, 255)),
                                  ((314, 314, 564, 564), (0, 255, 255))):
        d.rectangle([(ax - x0) * f, (ay - y0) * f, (bx - x0) * f - 1, (by - y0) * f - 1], outline=col, width=1)
    fn = font(max(10, min(18, f * 2)))
    fs = font(11)
    if not a.roh:
        ids = np.unique(lab)
        for sid in ids:
            m = lab == sid
            dist = ndimage.distance_transform_edt(np.pad(m, 1))[1:-1, 1:-1]
            yy, xx = np.unravel_index(np.argmax(dist), dist.shape)
            t = str(int(sid) % 100000)
            px, py = xx * f + f // 2, yy * f + f // 2
            d.text((px, py), t, fill=(255, 255, 255), font=fn, anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0))
    # Maßstab
    schritt = a.tick
    for xv in range((x0 // schritt + 1) * schritt, x0 + w, schritt):
        d.line([((xv - x0) * f, 0), ((xv - x0) * f, 6)], fill=(255, 0, 0), width=2)
        d.text(((xv - x0) * f + 2, 7), str(xv), fill=(255, 80, 80), font=fs, stroke_width=1, stroke_fill=(0, 0, 0))
    for yv in range((y0 // schritt + 1) * schritt, y0 + h, schritt):
        d.line([(0, (yv - y0) * f), (6, (yv - y0) * f)], fill=(255, 0, 0), width=2)
        d.text((8, (yv - y0) * f - 6), str(yv), fill=(255, 80, 80), font=fs, stroke_width=1, stroke_fill=(0, 0, 0))
    if a.punkte:
        for p in a.punkte.split(";"):
            px, py = (int(v) for v in p.split(","))
            cx, cy = (px - x0) * f + f // 2, (py - y0) * f + f // 2
            d.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], outline=(255, 0, 255), width=2)
    if a.linien:
        for lz in json.loads(a.linien):
            pts = [((px - x0) * f + f // 2, (py - y0) * f + f // 2) for px, py in lz]
            d.line(pts, fill=(255, 0, 255), width=2)
    im.save(a.ziel, quality=90)
    print(a.ziel, im.size)


def stat(a):
    karte, seg = laden(a.stapel, leise=True)
    img = np.asarray(Image.open(BILD).convert("L")).astype(np.float32)
    kern = np.zeros(karte.shape, bool)
    kern[64:564, 64:564] = True
    eint = {s["id"]: s for s in seg["segmente"]}
    ids = [int(i) for i in a.ids.split(",")] if a.ids else sorted(np.unique(karte[kern]).tolist())
    for sid in ids:
        m = karte == sid
        if not m.any():
            print(sid, "WEG")
            continue
        mk = m & kern
        ys, xs = np.nonzero(m)
        _, n = ndimage.label(m)
        e = eint.get(sid, {})
        print(f"{sid} kl={e.get('klasse')} fl={int(m.sum())} kern={int(mk.sum())} "
              f"bbox=x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()} grau={img[m].mean():.0f}±{img[m].std():.0f} teile={n}")


def sim(a):
    karte, seg = laden(a.stapel)
    print("ok, Segmente:", len(np.unique(karte)))


def main():
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(dest="cmd", required=True)
    b = sp.add_parser("bild")
    for k in ("x", "y", "b", "h", "f"):
        b.add_argument("--" + k, type=int, required=True)
    b.add_argument("--ziel", required=True)
    b.add_argument("--stapel")
    b.add_argument("--roh", action="store_true")
    b.add_argument("--kontrast", action="store_true")
    b.add_argument("--tick", type=int, default=10)
    b.add_argument("--punkte")
    b.add_argument("--linien")
    s = sp.add_parser("stat")
    s.add_argument("--ids")
    s.add_argument("--stapel")
    m = sp.add_parser("sim")
    m.add_argument("--stapel", required=True)
    a = p.parse_args()
    {"bild": bild, "stat": stat, "sim": sim}[a.cmd](a)


if __name__ == "__main__":
    main()
