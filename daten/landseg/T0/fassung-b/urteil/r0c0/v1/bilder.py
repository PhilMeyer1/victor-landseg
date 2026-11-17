"""Erzeugt roh.jpg, umriss.jpg, maengel.jpg, vorschlag.jpg fuer ein Viertel (Fassung B, r0c0).

Aufruf: <py> bilder.py --viertel v1 [--zeichnung zeichnung.json]
Liest nur: viertel/r0c0/<v>/ (Bilder, viertel.json), vorstufe/r0c0/labels.tif, urteil.json im Ergebnisordner.
zeichnung.json (optional, im Ergebnisordner): {"verschmelzen": [[von_id, nach_id], ...],
  "linien": [[[x,y],[x,y],...], ...]}  (Koordinaten im Teilkachelbild, neue Grenzen geschaetzt)
"""
import argparse
import json
import re
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

BASIS = Path("C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b")
FONT = "C:/Windows/Fonts/arial.ttf"
FONTB = "C:/Windows/Fonts/arialbd.ttf"


def grenzen(lab):
    g = np.zeros(lab.shape, bool)
    g[:, 1:] |= lab[:, 1:] != lab[:, :-1]
    g[1:, :] |= lab[1:, :] != lab[:-1, :]
    return g


def grenzbild(basis_img, lab_fen, faktor, farbe):
    lab_gross = np.kron(lab_fen, np.ones((faktor, faktor), dtype=lab_fen.dtype))
    g = grenzen(lab_gross)
    arr = np.array(basis_img.convert("RGB"))
    h, w = min(arr.shape[0], g.shape[0]), min(arr.shape[1], g.shape[1])
    arr[:h, :w][g[:h, :w]] = farbe
    return Image.fromarray(arr)


def rahmen(d, vb, fen, f):
    x0 = (vb["x"] - fen["x"]) * f
    y0 = (vb["y"] - fen["y"]) * f
    d.rectangle([x0, y0, x0 + vb["breite"] * f - 1, y0 + vb["hoehe"] * f - 1], outline=(0, 255, 255), width=3)


def text_kasten(d, xy, t, font, fg=(255, 255, 255), bg=(0, 0, 0)):
    x, y = xy
    bb = d.textbbox((x, y), t, font=font)
    d.rectangle([bb[0] - 2, bb[1] - 1, bb[2] + 2, bb[3] + 1], fill=bg)
    d.text((x, y), t, fill=fg, font=font)


def legende(img, zeilen, font, titel):
    breite = img.width
    zh = 18
    hoehe = 30 + zh * max(1, len(zeilen))
    neu = Image.new("RGB", (breite, img.height + hoehe), (255, 255, 255))
    neu.paste(img, (0, 0))
    d = ImageDraw.Draw(neu)
    d.text((8, img.height + 6), titel, fill=(0, 0, 0), font=font)
    for i, z in enumerate(zeilen):
        d.text((8, img.height + 26 + i * zh), z[:150], fill=(0, 0, 0), font=font)
    return neu


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--viertel", required=True)
    a = p.parse_args()
    v = a.viertel
    vdir = BASIS / "viertel/r0c0" / v
    odir = BASIS / "urteil/r0c0" / v
    vj = json.loads((vdir / "viertel.json").read_text(encoding="utf-8"))
    fen = vj["bilder"]["uebersicht_roh.jpg"]["fenster"]
    f = fen["faktor"]
    vb = vj["viertel_im_bild"]
    lab = np.array(Image.open(BASIS / "vorstufe/r0c0/labels.tif")).astype(np.int64)
    lab_fen = lab[fen["y"]:fen["y"] + fen["hoehe"], fen["x"]:fen["x"] + fen["breite"]]
    urteil = json.loads((odir / "urteil.json").read_text(encoding="utf-8"))
    zj = odir / "zeichnung.json"
    zeichnung = json.loads(zj.read_text(encoding="utf-8")) if zj.exists() else {}
    eigene = {s["id"] for s in vj["segmente"]}
    punkt = {s["id"]: s["punkt"] for s in vj["segmente"]}
    font = ImageFont.truetype(FONT, 13)
    fontb = ImageFont.truetype(FONTB, 15)
    fonts = ImageFont.truetype(FONT, 11)

    roh = Image.open(vdir / "uebersicht_roh.jpg").convert("RGB")

    # roh.jpg
    r = roh.copy()
    rahmen(ImageDraw.Draw(r), vb, fen, f)
    r.save(odir / "roh.jpg", quality=90)

    # umriss.jpg: alle Grenzen mit voller ID
    u = grenzbild(roh, lab_fen, f, (255, 255, 0))
    d = ImageDraw.Draw(u)
    rahmen(d, vb, fen, f)
    ids, zahl = np.unique(lab_fen, return_counts=True)
    for sid, n in zip(ids, zahl):
        sid = int(sid)
        if sid in punkt:
            px, py = punkt[sid]
        else:
            if n < 40:
                continue
            ys, xs = np.nonzero(lab_fen == sid)
            k = len(xs) // 2
            o = np.lexsort((xs, ys))
            px, py = xs[o[k]] + fen["x"], ys[o[k]] + fen["y"]
        bx, by = (px - fen["x"]) * f, (py - fen["y"]) * f
        if sid in eigene:
            text_kasten(d, (bx - 20, by - 7), str(sid), font)
        else:
            text_kasten(d, (bx - 18, by - 6), str(sid), fonts, fg=(200, 200, 200), bg=(40, 40, 40))
    u.save(odir / "umriss.jpg", quality=90)

    # maengel.jpg: nummerierte Punkte aus urteil.json
    m = grenzbild(roh, lab_fen, f, (255, 255, 0))
    d = ImageDraw.Draw(m)
    rahmen(d, vb, fen, f)
    zeilen = []
    nr = 0
    rx = re.compile(r"\((\d+)\s*/\s*(\d+)")
    for s in urteil["segmente"]:
        for pt in s.get("punkte", []):
            nr += 1
            t = pt["text"]
            mt = rx.search(t)
            if mt:
                x, y = int(mt.group(1)), int(mt.group(2))
            else:
                x, y = punkt.get(s["id"], (vb["x"], vb["y"]))
            bx, by = (x - fen["x"]) * f, (y - fen["y"]) * f
            d.ellipse([bx - 9, by - 9, bx + 9, by + 9], fill=(220, 0, 0), outline=(255, 255, 255), width=2)
            tw = d.textlength(str(nr), font=fonts)
            d.text((bx - tw / 2, by - 6), str(nr), fill=(255, 255, 255), font=fonts)
            zeilen.append(f"{nr}: {s['id']} [{pt['art']}] {t}")
    if not zeilen:
        text_kasten(d, (10, 10), "keine Mängel", fontb)
    m = legende(m, zeilen or ["keine Mängel"], fonts, f"Mängel {v} (Punkte im Teilkachelbild)")
    m.save(odir / "maengel.jpg", quality=90)

    # vorschlag.jpg: Grenzen nach Verschmelzen, neue Linien, Klassen frei (fein)
    lab2 = lab_fen.copy()
    ziel = {}
    for von, nach in zeichnung.get("verschmelzen", []):
        ziel[int(von)] = int(nach)

    def wurzel(i):
        seen = set()
        while i in ziel and i not in seen:
            seen.add(i)
            i = ziel[i]
        return i
    for von in list(ziel):
        lab2[lab2 == von] = wurzel(von)
    vs = grenzbild(roh, lab2, f, (255, 255, 0))
    d = ImageDraw.Draw(vs)
    rahmen(d, vb, fen, f)
    for linie in zeichnung.get("linien", []):
        pts = [((x - fen["x"]) * f, (y - fen["y"]) * f) for x, y in linie]
        d.line(pts, fill=(255, 0, 255), width=3)
    geaendert = bool(ziel) or bool(zeichnung.get("linien"))
    for s in urteil["segmente"]:
        sid = s["id"]
        if sid in ziel:
            continue
        x, y = punkt.get(sid, (None, None))
        if x is None:
            continue
        kf = s["klasse_frei"]
        t = kf["fein"]
        bx, by = (x - fen["x"]) * f, (y - fen["y"]) * f
        fg = (255, 255, 255) if s.get("sicher") else (255, 200, 120)
        text_kasten(d, (bx - 25, by - 7), f"{sid % 1000}: {t}", fonts, fg=fg)
    for von, nach in sorted(ziel.items()):
        if von in punkt:
            x, y = punkt[von]
            bx, by = (x - fen["x"]) * f, (y - fen["y"]) * f
            text_kasten(d, (bx - 15, by - 6), f"{von % 1000}→{wurzel(von) % 1000}", fonts, fg=(255, 120, 255))
    if not geaendert:
        text_kasten(d, (10, 10), "Grenzen unverändert", fontb)
    zl = ["gelb: Grenzen nach Vorschlag (Verschmelzungen angewandt); magenta: neue Grenze, von Hand geschätzt;",
          "Beschriftung: Nr (ID mod 1000): Klasse fein; orange = sicher: false; 'a→b' = a geht in b auf"]
    vs = legende(vs, zl, fonts, f"Vorschlag {v}")
    vs.save(odir / "vorschlag.jpg", quality=90)
    print("ok", v, "punkte", nr, "verschmolzen", len(ziel))


if __name__ == "__main__":
    main()
