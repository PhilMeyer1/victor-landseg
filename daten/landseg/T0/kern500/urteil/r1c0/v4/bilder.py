"""Erzeugt roh.jpg, umriss.jpg, maengel.jpg, vorschlag.jpg für ein Viertel aus urteil.json.

Aufruf: PY bilder.py --viertel v1 --aus <ergebnisordner> [--weitere <urteil.json> ...]
Nur lesen: Teilkachelbild, labels.tif, segmente.json, kategorien.json. Schreibt nur in --aus.
"""
import argparse
import json
import re
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

BASIS = Path("C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500")
TK = "r1c0"
KAT = Path("C:/Users/Phil/Developement/Victor/landseg/kategorien.json")
VIERTEL = {"v1": (64, 64), "v2": (314, 64), "v3": (64, 314), "v4": (314, 314)}
RAND, F, GR = 32, 3, 314
FONT = "C:/Windows/Fonts/arial.ttf"
FONTB = "C:/Windows/Fonts/arialbd.ttf"


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def grenzen(lab):
    g = np.zeros(lab.shape, bool)
    g[:, 1:] |= lab[:, 1:] != lab[:, :-1]
    g[1:, :] |= lab[1:, :] != lab[:-1, :]
    return g


def hoch(arr):
    return np.repeat(np.repeat(arr, F, axis=0), F, axis=1)


def rahmen(d, vx, vy, x0, y0):
    a = ((vx - x0) * F, (vy - y0) * F)
    b = ((vx + 250 - x0) * F - 1, (vy + 250 - y0) * F - 1)
    d.rectangle([a, b], outline=(0, 255, 255), width=3)


def text_mit_rand(d, xy, t, font, fill=(255, 255, 255)):
    x, y = xy
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx or dy:
                d.text((x + dx, y + dy), t, font=font, fill=(0, 0, 0), anchor="mm")
    d.text((x, y), t, font=font, fill=fill, anchor="mm")


def legende(img, zeilen, font):
    if not zeilen:
        return img
    zh = 22
    neu = Image.new("RGB", (img.width, img.height + 10 + zh * len(zeilen)), (255, 255, 255))
    neu.paste(img, (0, 0))
    d = ImageDraw.Draw(neu)
    for i, z in enumerate(zeilen):
        d.text((8, img.height + 6 + i * zh), z, font=font, fill=(0, 0, 0))
    return neu


def kurz(t, n=118):
    return t if len(t) <= n else t[:n - 1] + "…"


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--viertel", required=True)
    p.add_argument("--aus", required=True)
    p.add_argument("--weitere", nargs="*", default=[])
    a = p.parse_args()
    aus = Path(a.aus)
    vx, vy = VIERTEL[a.viertel]
    x0, y0 = vx - RAND, vy - RAND
    bild = np.asarray(Image.open(BASIS / "teilkacheln" / f"{TK}.png").convert("RGB"))
    lab = tifffile.imread(BASIS / "vorstufe" / TK / "labels.tif")
    seg = {s["id"]: s for s in json.loads((BASIS / "vorstufe" / TK / "segmente.json").read_text(encoding="utf-8"))["segmente"]}
    kat = {k["code"]: k for k in json.loads(KAT.read_text(encoding="utf-8"))["classes"]}
    urteil = json.loads((aus / "urteil.json").read_text(encoding="utf-8"))
    vorschlag = {sid: s["klasse"] for sid, s in seg.items()}
    for w in a.weitere:
        wp = Path(w)
        if wp.is_file():
            for e in json.loads(wp.read_text(encoding="utf-8")).get("segmente", []):
                if e.get("klasse_vorschlag"):
                    vorschlag[e["id"]] = e["klasse_vorschlag"]
    eigene = [e["id"] for e in urteil["segmente"]]
    for e in urteil["segmente"]:
        if e.get("klasse_vorschlag"):
            vorschlag[e["id"]] = e["klasse_vorschlag"]

    sl = (slice(y0, y0 + GR), slice(x0, x0 + GR))
    b = bild[sl]
    l = lab[sl]
    font = ImageFont.truetype(FONT, 15)
    fontb = ImageFont.truetype(FONTB, 16)
    fontl = ImageFont.truetype(FONT, 15)

    # roh
    roh = Image.fromarray(hoch(b))
    rahmen(ImageDraw.Draw(roh), vx, vy, x0, y0)
    roh.save(aus / "roh.jpg", quality=90)

    # umriss
    g = hoch(grenzen(l))
    u = hoch(b).copy()
    u[g] = (255, 255, 0)
    um = Image.fromarray(u)
    d = ImageDraw.Draw(um)
    rahmen(d, vx, vy, x0, y0)
    for sid in np.unique(l):
        m = l == sid
        if m.sum() < 15:
            continue
        dist = ndimage.distance_transform_edt(np.pad(m, 1))[1:-1, 1:-1]
        yy, xx = np.unravel_index(np.argmax(dist), dist.shape)
        farbe = (255, 255, 255) if int(sid) in eigene else (190, 190, 190)
        text_mit_rand(d, (xx * F + 1, yy * F + 1), str(int(sid)), font, farbe)
    um = legende(um, ["Gelb: Segmentgrenzen der Vorstufe; Zahl = volle Segment-ID (weiß: dieses Viertel, grau: Nachbarn/Rand); cyan: Viertel."], fontl)
    um.save(aus / "umriss.jpg", quality=90)

    # maengel
    mg = Image.fromarray(u.copy())
    d = ImageDraw.Draw(mg)
    rahmen(d, vx, vy, x0, y0)
    zeilen = []
    k = 0
    for e in urteil["segmente"]:
        for pt in e.get("punkte", []):
            k += 1
            mm = re.findall(r"\((\d+)/(\d+)\)", pt["text"])
            if mm:
                px, py = int(mm[-1][0]), int(mm[-1][1])
                cx, cy = (px - x0) * F + 1, (py - y0) * F + 1
                d.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=(220, 30, 30), outline=(255, 255, 255), width=2)
                d.text((cx, cy), str(k), font=fontb, fill=(255, 255, 255), anchor="mm")
            zeilen.append(kurz(f"{k}: {e['id']} {pt['art']}: {pt['text']}"))
    if not zeilen:
        zeilen = ["keine Mängel"]
    mg = legende(mg, zeilen, fontl)
    mg.save(aus / "maengel.jpg", quality=90)

    # vorschlag: Klassenfarbe je Segment, Grenzen nur zwischen verschiedenen Vorschlagsklassen
    kl = np.vectorize(lambda s: vorschlag.get(int(s), "0"))(l)
    codes = sorted(set(kl.ravel()))
    idx = np.zeros(l.shape, np.int32)
    for i, c in enumerate(codes):
        idx[kl == c] = i
    farbe = np.array([hexrgb(kat[c]["color"]) for c in codes], np.float32)
    misch = (0.55 * b.astype(np.float32) + 0.45 * farbe[idx]).astype(np.uint8)
    v = hoch(misch)
    gv = hoch(grenzen(idx))
    v[gv] = (255, 255, 0)
    vo = Image.fromarray(v)
    d = ImageDraw.Draw(vo)
    rahmen(d, vx, vy, x0, y0)
    lab_c, n = ndimage.label(np.ones_like(idx), structure=None)
    for i, c in enumerate(codes):
        teile, nt = ndimage.label(idx == i)
        for t in range(1, nt + 1):
            m = teile == t
            if m.sum() < 60:
                continue
            dist = ndimage.distance_transform_edt(np.pad(m, 1))[1:-1, 1:-1]
            yy, xx = np.unravel_index(np.argmax(dist), dist.shape)
            text_mit_rand(d, (xx * F + 1, yy * F + 1), c, font)
    geaendert = [e for e in urteil["segmente"] if e.get("klasse_vorschlag") and e["klasse_vorschlag"] != e.get("klasse_heute")]
    zeilen = ["Farbe und Code: Klasse, wie ich sie setzen würde; gelb nur Grenzen zwischen verschiedenen Klassen",
              "(gleiche Klasse nebeneinander = verschmelzen). Grenzverschiebungen stehen im Mängelbild."]
    if not geaendert:
        zeilen.append("unverändert")
    else:
        zeilen.append(kurz("Geändert: " + ", ".join(f"{e['id']} {e['klasse_heute']}→{e['klasse_vorschlag']}" for e in geaendert), 140))
        if len(zeilen[-1]) >= 139:
            zeilen.pop()
            gruppe = []
            for e in geaendert:
                gruppe.append(f"{e['id']} {e['klasse_heute']}→{e['klasse_vorschlag']}")
                if len(gruppe) == 6:
                    zeilen.append(", ".join(gruppe))
                    gruppe = []
            if gruppe:
                zeilen.append(", ".join(gruppe))
    vo = legende(vo, zeilen, fontl)
    vo.save(aus / "vorschlag.jpg", quality=90)
    print("ok", aus)


if __name__ == "__main__":
    main()
