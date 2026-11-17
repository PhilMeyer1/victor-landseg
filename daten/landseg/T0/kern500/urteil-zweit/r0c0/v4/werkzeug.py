"""Hilfswerkzeug des Zweitagents (Fassung A) fuer r0c0: Segment-Info und Ergebnisbilder.

  info   --viertel v1 [--ids 1,2]   : Kennzahlen je Segment (Klasse, Flaeche, Teile, Farbe, Nachbarn)
  bilder --viertel v1               : roh.jpg, umriss.jpg, maengel.jpg, vorschlag.jpg aus urteil.json
  nah    --viertel v1 --n 1 --x0 .. --y0 .. --w .. --h .. [--f 6] [--kontrast]
"""
import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont, ImageOps
from scipy import ndimage

BASIS = Path("C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500")
KAT = Path("C:/Users/Phil/Developement/Victor/landseg/kategorien.json")
TK = "r0c0"


def lade():
    lab = tifffile.imread(BASIS / "vorstufe" / TK / "labels.tif")
    img = np.asarray(Image.open(BASIS / "teilkacheln" / f"{TK}.png").convert("RGB"))
    seg = json.loads((BASIS / "vorstufe" / TK / "segmente.json").read_text(encoding="utf-8"))
    segd = {s["id"]: s for s in seg["segmente"]}
    kat = json.loads(KAT.read_text(encoding="utf-8"))
    farben = {k["code"]: k.get("color") or k.get("farbe") for k in kat["classes"]}
    return lab, img, segd, farben


def font(n):
    for f in ("C:/Windows/Fonts/arial.ttf", "C:/Windows/Fonts/segoeui.ttf"):
        try:
            return ImageFont.truetype(f, n)
        except OSError:
            pass
    return ImageFont.load_default()


def vinfo(v):
    d = json.loads((BASIS / "viertel" / TK / v / "viertel.json").read_text(encoding="utf-8"))
    return d


def info(a):
    lab, img, segd, _ = lade()
    vi = vinfo(a.viertel)
    ids = [int(x) for x in a.ids.split(",")] if a.ids else [s["id"] for s in vi["segmente"]]
    kern = np.zeros(lab.shape, bool)
    kern[64:564, 64:564] = True
    for i in ids:
        m = lab == i
        mk = m & kern
        s = segd.get(i, {})
        lb, n = ndimage.label(mk)
        ys, xs = np.nonzero(mk)
        col = img[mk].mean(0).astype(int) if mk.any() else None
        sd = img[mk].std(0).mean() if mk.any() else 0
        dil = ndimage.binary_dilation(m, structure=[[0, 1, 0], [1, 1, 1], [0, 1, 0]]) & ~m
        nb, cnt = np.unique(lab[dil], return_counts=True)
        nbs = sorted(zip(cnt, nb), reverse=True)[:6]
        teile = sorted(np.bincount(lb.ravel())[1:].tolist(), reverse=True)[:5] if n else []
        print(f"{i} {s.get('klasse')} sicher={s.get('sicher')} text={s.get('instanz', {}).get('text')} "
              f"kern={mk.sum()} teile={n}{teile} bbox=x{xs.min() if len(xs) else '-'}-{xs.max() if len(xs) else '-'} "
              f"y{ys.min() if len(ys) else '-'}-{ys.max() if len(ys) else '-'} rgb={None if col is None else col.tolist()} sd={sd:.1f} "
              f"nb={[(int(b) % 100000, segd.get(int(b), {}).get('klasse'), int(c)) for c, b in nbs]}")


def grenzen(lab):
    g = np.zeros(lab.shape, bool)
    g[:, 1:] |= lab[:, 1:] != lab[:, :-1]
    g[1:, :] |= lab[1:, :] != lab[:-1, :]
    return g


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def bilder(a):
    lab, img, segd, farben = lade()
    vi = vinfo(a.viertel)
    fe = vi["bilder"]["uebersicht_roh.jpg"]["fenster"]
    x0, y0, w, h, f = fe["x"], fe["y"], fe["breite"], fe["hoehe"], fe["faktor"]
    vx, vy = vi["viertel_im_bild"]["x"], vi["viertel_im_bild"]["y"]
    vw, vh = vi["viertel_im_bild"]["breite"], vi["viertel_im_bild"]["hoehe"]
    ziel = Path(a.ziel) if a.ziel else BASIS / "urteil-zweit" / TK / a.viertel
    urteil = json.loads((ziel / "urteil.json").read_text(encoding="utf-8"))
    eigene = {s["id"] for s in vi["segmente"]}
    sub = img[y0:y0 + h, x0:x0 + w]
    sl = lab[y0:y0 + h, x0:x0 + w]

    def gross(arr):
        return Image.fromarray(arr).resize((w * f, h * f), Image.NEAREST)

    def rahmen(im):
        d = ImageDraw.Draw(im)
        d.rectangle([(vx - x0) * f, (vy - y0) * f, (vx - x0 + vw) * f - 1, (vy - y0 + vh) * f - 1],
                    outline=(0, 255, 255), width=3)
        return d

    roh = gross(sub)
    rahmen(roh)
    roh.save(ziel / "roh.jpg", quality=90)

    g = grenzen(sl)
    gb = np.asarray(Image.fromarray(g).resize((w * f, h * f), Image.NEAREST))
    um = np.asarray(gross(sub)).copy()
    um[gb] = (255, 255, 0)
    um = Image.fromarray(um)
    d = rahmen(um)
    fn = font(13)
    for i in np.unique(sl):
        m = sl == i
        if m.sum() < 15:
            continue
        cy, cx = ndimage.center_of_mass(m)
        if not m[int(cy), int(cx)]:
            ys, xs = np.nonzero(m)
            k = len(ys) // 2
            cy, cx = ys[k], xs[k]
        col = (255, 255, 255) if int(i) in eigene else (170, 170, 170)
        t = str(int(i))
        d.text((cx * f, cy * f), t, fill=col, font=fn, anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0))
    um.save(ziel / "umriss.jpg", quality=90)

    # maengel
    ma = gross(sub)
    d = rahmen(ma)
    eintraege = []
    nr = 0
    for s in urteil["segmente"]:
        for p in s.get("punkte", []):
            mt = re.search(r"\((\d+)/(\d+)", p["text"])
            if not mt:
                continue
            nr += 1
            px, py = int(mt.group(1)), int(mt.group(2))
            eintraege.append((nr, s["id"], p, px, py))
    fn2 = font(16)
    for nr, sid, p, px, py in eintraege:
        cx, cy = (px - x0) * f + f // 2, (py - y0) * f + f // 2
        d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(230, 30, 30), outline=(255, 255, 255), width=2)
        d.text((cx, cy), str(nr), fill=(255, 255, 255), font=fn2, anchor="mm")
    import textwrap
    zeilen = []
    for nr, sid, p, _, _ in eintraege:
        zeilen += textwrap.wrap(f"{nr}: {sid % 100000} {p['art']} – {p['text']}", 118,
                                subsequent_indent="      ")
    zeilen = zeilen or ["keine Mängel"]
    lh = 18
    leg = Image.new("RGB", (ma.width, lh * len(zeilen) + 10), (20, 20, 20))
    dl = ImageDraw.Draw(leg)
    for k, z in enumerate(zeilen):
        dl.text((6, 5 + k * lh), z, fill=(255, 255, 255), font=font(12))
    out = Image.new("RGB", (ma.width, ma.height + leg.height))
    out.paste(ma, (0, 0))
    out.paste(leg, (0, ma.height))
    if out.height > 2000:
        out = out.resize((int(out.width * 2000 / out.height), 2000))
    out.save(ziel / "maengel.jpg", quality=90)

    # vorschlag
    vor = {s["id"]: s.get("klasse_vorschlag") for s in urteil["segmente"]}
    ov = np.asarray(gross(sub)).astype(float)
    farbe = np.zeros(sl.shape + (3,), float)
    code_of = {}
    for i in np.unique(sl):
        i = int(i)
        c = vor.get(i) or segd.get(i, {}).get("klasse")
        code_of[i] = c
        farbe[sl == i] = hexrgb(farben.get(c, "#808080"))
    fb = np.asarray(Image.fromarray(farbe.astype(np.uint8)).resize((w * f, h * f), Image.NEAREST)).astype(float)
    mix = (0.45 * ov + 0.55 * fb).astype(np.uint8)
    mix[gb] = (255, 255, 255)
    vo = Image.fromarray(mix)
    d = rahmen(vo)
    geaendert = [s for s in urteil["segmente"] if s.get("klasse_vorschlag") or s.get("urteil") == "nicht_sauber"]
    for i in np.unique(sl):
        m = sl == i
        if m.sum() < 15:
            continue
        ys, xs = np.nonzero(m)
        cy, cx = ndimage.center_of_mass(m)
        if not m[int(cy), int(cx)]:
            k = len(ys) // 2
            cy, cx = ys[k], xs[k]
        i = int(i)
        neu = i in vor and vor.get(i)
        t = f"{code_of[i]}" + ("*" if neu else "")
        d.text((cx * f, cy * f), t, fill=(255, 255, 0) if neu else (255, 255, 255), font=fn, anchor="mm",
               stroke_width=2, stroke_fill=(0, 0, 0))
    # vorgeschlagene Grenzen als Punkte aus Arten trennen/verschmelzen/grenze/fremdes
    for nr, sid, p, px, py in eintraege:
        if p["art"] in ("trennen", "verschmelzen", "grenze", "fremdes", "fehlt"):
            cx, cy = (px - x0) * f + f // 2, (py - y0) * f + f // 2
            d.rectangle([cx - 8, cy - 8, cx + 8, cy + 8], outline=(255, 0, 255), width=3)
            d.text((cx + 12, cy), f"{nr} {p['art']}", fill=(255, 0, 255), font=fn, anchor="lm",
                   stroke_width=2, stroke_fill=(0, 0, 0))
    hinweis = ("Klassen: * = geändert (gelb); magenta Kästchen = Grenzänderung laut Mängelliste"
               if geaendert else "unverändert")
    leg = Image.new("RGB", (vo.width, 30), (20, 20, 20))
    ImageDraw.Draw(leg).text((6, 7), hinweis, fill=(255, 255, 255), font=font(14))
    out = Image.new("RGB", (vo.width, vo.height + 30))
    out.paste(vo, (0, 0))
    out.paste(leg, (0, vo.height))
    out.save(ziel / "vorschlag.jpg", quality=90)
    print("bilder ok", ziel, len(eintraege), "Punkte")


def nah(a):
    lab, img, segd, _ = lade()
    ziel = Path(a.ziel) if a.ziel else BASIS / "urteil-zweit" / TK / a.viertel
    sub = img[a.y0:a.y0 + a.h, a.x0:a.x0 + a.w]
    sl = lab[a.y0:a.y0 + a.h, a.x0:a.x0 + a.w]
    if a.kontrast:
        im = ImageOps.autocontrast(Image.fromarray(sub), cutoff=2)
        sub = np.asarray(ImageOps.equalize(im))
    f = a.f
    big = np.asarray(Image.fromarray(sub).resize((a.w * f, a.h * f), Image.NEAREST)).copy()
    gb = np.asarray(Image.fromarray(grenzen(sl)).resize((a.w * f, a.h * f), Image.NEAREST))
    big[gb] = (255, 255, 0)
    im = Image.fromarray(big)
    d = ImageDraw.Draw(im)
    fn = font(14)
    for i in np.unique(sl):
        m = sl == i
        if m.sum() < 6:
            continue
        ys, xs = np.nonzero(m)
        cy, cx = ndimage.center_of_mass(m)
        if not m[int(cy), int(cx)]:
            k = len(ys) // 2
            cy, cx = ys[k], xs[k]
        d.text((cx * f, cy * f), str(int(i) % 100000), fill=(255, 255, 255), font=fn, anchor="mm",
               stroke_width=2, stroke_fill=(0, 0, 0))
    # Gitter alle 10 px beschriften
    for gx in range(((a.x0 + 9) // 10) * 10, a.x0 + a.w, 10):
        d.text(((gx - a.x0) * f, 2), str(gx), fill=(0, 255, 255), font=font(11))
    for gy in range(((a.y0 + 9) // 10) * 10, a.y0 + a.h, 10):
        d.text((2, (gy - a.y0) * f), str(gy), fill=(0, 255, 255), font=font(11))
    name = f"{'kontrast' if a.kontrast else 'nah'}_{a.n}.jpg"
    im.save(ziel / name, quality=90)
    print(ziel / name)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser()
    p.add_argument("was", choices=["info", "bilder", "nah"])
    p.add_argument("--viertel", required=True)
    p.add_argument("--ids")
    p.add_argument("--ziel")
    p.add_argument("--n", type=int, default=1)
    p.add_argument("--x0", type=int)
    p.add_argument("--y0", type=int)
    p.add_argument("--w", type=int, default=80)
    p.add_argument("--h", type=int, default=80)
    p.add_argument("--f", type=int, default=6)
    p.add_argument("--kontrast", action="store_true")
    a = p.parse_args()
    {"info": info, "bilder": bilder, "nah": nah}[a.was](a)


if __name__ == "__main__":
    main()
