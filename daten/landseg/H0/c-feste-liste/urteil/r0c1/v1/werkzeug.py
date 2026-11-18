"""Hilfswerkzeug des Urteils r0c1 (Fassung C): Nahansichten, Dach-Kandidaten, Probelauf eines Stapels.

Nur lesen; die Karte aendert ausschliesslich `python -m landseg eingriff ... stapel`.
Aufruf im Ordner landseg:  PY -B <dieses Skript> <befehl> ...
"""
import argparse
import json
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

sys.path.insert(0, "C:/Users/Phil/Developement/Victor/landseg")
from landseg.dateien import lese_labels, lese_segmente  # noqa: E402
from landseg.eingriff import Bearbeitung, polygon_maske, EingriffFehler  # noqa: E402
from landseg import kategorien as katmod  # noqa: E402

H0 = Path("C:/Users/Phil/Developement/Victor/daten/landseg/H0")
LABELS = H0 / "c-feste-liste/r0c1/labels.tif"
SEGMENTE = H0 / "c-feste-liste/r0c1/segmente.json"
BILD = H0 / "teilkacheln/r0c1.png"
KERN = (64, 64, 564, 564)  # x0, y0, x1, y1 (exklusiv)
VIERTEL = {"v1": (64, 64, 314, 314), "v2": (314, 64, 564, 314),
           "v3": (64, 314, 314, 564), "v4": (314, 314, 564, 564)}


def font(gr):
    for f in ("C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/arial.ttf"):
        try:
            return ImageFont.truetype(f, gr)
        except OSError:
            pass
    return ImageFont.load_default()


def lade():
    karte = lese_labels(LABELS)
    bild = np.asarray(Image.open(BILD).convert("L"))
    seg = lese_segmente(SEGMENTE)
    return karte, bild, seg


def zeichne(karte, bild, x0, y0, w, h, f, polys=None, markiere=None, titel=None, kontrast=False,
            viertel=None, nummern=True, rahmen=True, punkte=None, klassen=None, flaechen=None):
    crop = bild[y0:y0 + h, x0:x0 + w].astype(np.float32)
    if kontrast:
        lo, hi = np.percentile(crop, 2), np.percentile(crop, 98)
        crop = np.clip((crop - lo) / max(hi - lo, 1) * 255, 0, 255)
    rand_l, rand_o = 40, 20
    img = Image.fromarray(crop.astype(np.uint8)).resize((w * f, h * f), Image.BICUBIC).convert("RGB")
    lab = karte[y0:y0 + h, x0:x0 + w]
    big = np.kron(lab, np.ones((f, f), dtype=lab.dtype))
    grenze = np.zeros(big.shape, bool)
    grenze[:, 1:] |= big[:, 1:] != big[:, :-1]
    grenze[1:, :] |= big[1:, :] != big[:-1, :]
    arr = np.asarray(img).copy()
    if rahmen:
        arr[grenze] = (255, 230, 0)
    if flaechen:
        farben = [(255, 60, 60), (60, 200, 255), (255, 200, 0), (120, 255, 80), (255, 80, 255), (255, 140, 0)]
        for j, fm in enumerate(flaechen):
            m = np.kron(fm[y0:y0 + h, x0:x0 + w].astype(np.uint8), np.ones((f, f), np.uint8)).astype(bool)
            arr[m] = (arr[m] * 0.55 + np.array(farben[j % len(farben)]) * 0.45).astype(np.uint8)
    if markiere is not None:
        m = np.kron(np.isin(lab, list(markiere)).astype(np.uint8), np.ones((f, f), np.uint8)).astype(bool)
        arr[m] = (arr[m] * 0.6 + np.array([0, 120, 255]) * 0.4).astype(np.uint8)
    canvas = Image.new("RGB", (w * f + rand_l, h * f + rand_o + (24 if titel else 0)), (255, 255, 255))
    canvas.paste(Image.fromarray(arr), (rand_l, rand_o))
    d = ImageDraw.Draw(canvas)
    fn = font(12)
    for xx in range(x0 - x0 % 10, x0 + w, 10):
        if xx < x0:
            continue
        px = rand_l + (xx - x0) * f
        d.line([(px, rand_o - 5), (px, rand_o)], fill=(0, 0, 0))
        if xx % 20 == 0:
            d.text((px - 8, 2), str(xx), fill=(0, 0, 0), font=fn)
    for yy in range(y0 - y0 % 10, y0 + h, 10):
        if yy < y0:
            continue
        py = rand_o + (yy - y0) * f
        d.line([(rand_l - 5, py), (rand_l, py)], fill=(0, 0, 0))
        if yy % 20 == 0:
            d.text((2, py - 7), str(yy), fill=(0, 0, 0), font=fn)
    if viertel:
        vx0, vy0, vx1, vy1 = viertel
        d.rectangle([rand_l + (vx0 - x0) * f, rand_o + (vy0 - y0) * f,
                     rand_l + (vx1 - x0) * f - 1, rand_o + (vy1 - y0) * f - 1], outline=(0, 230, 230), width=2)
    if polys:
        for i, (pts, farbe, text) in enumerate(polys):
            q = [(rand_l + (x - x0) * f + f // 2, rand_o + (y - y0) * f + f // 2) for x, y in pts]
            if len(q) >= 2:
                d.line(q + [q[0]] if len(q) > 2 else q, fill=farbe, width=2)
            if text:
                cx = sum(p[0] for p in q) / len(q)
                cy = sum(p[1] for p in q) / len(q)
                d.text((cx - 6, cy - 6), text, fill=farbe, font=font(13))
    if nummern:
        fz = font(13 if f >= 4 else 11)
        for sid in np.unique(lab):
            m = lab == sid
            if m.sum() < 6:
                continue
            dist = ndimage.distance_transform_edt(np.pad(m, 1))[1:-1, 1:-1]
            yy, xx = np.unravel_index(np.argmax(dist), dist.shape)
            t = str(int(sid) % 100000)
            if klassen and int(sid) in klassen:
                t += " " + klassen[int(sid)]
            px, py = rand_l + xx * f + f // 2, rand_o + yy * f + f // 2
            d.rectangle([px - 3, py - 7, px + 7 * len(t) + 2, py + 7], fill=(0, 0, 0))
            d.text((px - 1, py - 7), t, fill=(255, 255, 255), font=fz)
    if punkte:
        for (x, y, t) in punkte:
            px, py = rand_l + (x - x0) * f + f // 2, rand_o + (y - y0) * f + f // 2
            d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=(220, 0, 0), outline=(255, 255, 255))
            d.text((px - 5, py - 8), str(t), fill=(255, 255, 255), font=font(13))
    if titel:
        d.text((rand_l, canvas.size[1] - 22), titel, fill=(0, 0, 0), font=font(15))
    return canvas


def speichere(canvas, pfad):
    s = max(canvas.size)
    if s > 2000:
        k = 2000 / s
        canvas = canvas.resize((int(canvas.size[0] * k), int(canvas.size[1] * k)), Image.LANCZOS)
    canvas.save(pfad, quality=90)
    print("Bild:", pfad, canvas.size)


def cmd_zoom(a):
    karte, bild, seg = lade()
    polys = []
    if a.stapel:
        for i, s in enumerate(json.loads(Path(a.stapel).read_text(encoding="utf-8"))["schritte"], 1):
            pts = s.get("flaeche") or s.get("linie")
            polys.append((pts, (255, 40, 40) if s["op"] != "teilen" else (0, 255, 120), str(i) if a.stapel_nr else ""))
    mark = [int(x) for x in a.markiere.split(",")] if a.markiere else None
    klassen = None
    if a.klassen:
        klassen = {s["id"]: s["klasse"] for s in seg["segmente"]}
    v = VIERTEL.get(a.viertel) if a.viertel else None
    c = zeichne(karte, bild, a.x0, a.y0, a.w, a.h, a.f, polys=polys, markiere=mark, titel=a.titel,
                kontrast=a.kontrast, viertel=v, nummern=not a.ohne_nummern, rahmen=not a.ohne_rahmen,
                klassen=klassen)
    speichere(c, a.out)


def kandidaten(karte, bild, sid, box, schwelle, sigma, oeffnen, minfl, rel, loch=30, schnitte=(), weg=()):
    x0, y0, x1, y1 = box
    erlaubt = np.zeros(karte.shape, bool)
    erlaubt[y0:y1, x0:x1] = True
    erlaubt &= karte == sid
    g = ndimage.gaussian_filter(bild.astype(np.float32), sigma)
    if rel:
        lokal = ndimage.uniform_filter(g, rel)
        hell = (g - lokal > schwelle) & erlaubt
    else:
        hell = (g > schwelle) & erlaubt
    if oeffnen:
        st = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (oeffnen, oeffnen))
        hell = cv2.morphologyEx(hell.astype(np.uint8), cv2.MORPH_OPEN, st).astype(bool)
    for lin in schnitte:
        lm = np.zeros(karte.shape, np.uint8)
        cv2.polylines(lm, [np.asarray(lin, np.int32)], False, 1, thickness=2, lineType=cv2.LINE_8)
        hell &= ~lm.astype(bool)
    for pg in weg:
        hell &= ~polygon_maske(karte.shape, pg)
    # Kanten-Ring: Polygon darf nur Bildpunkte von sid im Kern abdecken -> 1 px Abstand zum Rand von erlaubt
    innen = ndimage.binary_erosion(erlaubt, structure=np.ones((3, 3)))
    hell &= innen
    tl, n = ndimage.label(hell, structure=[[0, 1, 0], [1, 1, 1], [0, 1, 0]])
    polys = []
    for i in range(1, n + 1):
        m = tl == i
        if m.sum() < minfl:
            continue
        gefuellt = ndimage.binary_fill_holes(m)
        loecher, nl = ndimage.label(gefuellt & ~m)
        gross = [j for j in range(1, nl + 1) if (loecher == j).sum() > loch]
        if gross:
            yy, xx = np.nonzero(np.isin(loecher, gross))
            print(f"  Kandidat {len(polys) + 1} (Mitte {int(np.nonzero(m)[1].mean())}/{int(np.nonzero(m)[0].mean())}): "
                  f"grosses Loch bei {int(xx.mean())}/{int(yy.mean())} ({len(xx)} px); Schnitt noetig, verworfen")
            continue
        m = gefuellt & innen
        cs, _ = cv2.findContours(m.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        c = max(cs, key=cv2.contourArea)
        ap = cv2.approxPolyDP(c, 0.8, True).reshape(-1, 2)
        pm = polygon_maske(karte.shape, ap.tolist())
        vier = [[0, 1, 0], [1, 1, 1], [0, 1, 0]]
        if not (pm <= erlaubt).all() or ndimage.label(pm, structure=vier)[1] != 1:
            cs2, _ = cv2.findContours(m.astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            c = max(cs2, key=len)
            ap = c.reshape(-1, 2)
            pm = polygon_maske(karte.shape, ap.tolist())
            if not (pm <= erlaubt).all():
                pm2 = pm & erlaubt
                print(f"  Kandidat {i}: Polygon ragt {int((pm & ~erlaubt).sum())} px ueber; verworfen")
                continue
        polys.append({"punkte": ap.tolist(), "flaeche": int(pm.sum())})
    return polys


def cmd_dach(a):
    karte, bild, seg = lade()
    box = [int(v) for v in a.box.split(",")]
    schn = [[[int(v) for v in pt.split(',')] for pt in l.split(';')] for l in (a.schnitt or [])]
    weg = [[[int(v) for v in pt.split(',')] for pt in l.split(';')] for l in (a.weg or [])]
    polys = kandidaten(karte, bild, a.id, box, a.schwelle, a.sigma, a.oeffnen, a.minfl, a.rel, a.loch, schn, weg)
    print(f"{len(polys)} Kandidaten:", [p["flaeche"] for p in polys])
    Path(a.json).write_text(json.dumps(polys), encoding="utf-8")
    x0, y0, x1, y1 = box
    fl = [polygon_maske(karte.shape, p["punkte"]) for p in polys]
    if a.ausschnitt:
        x0, y0, x1, y1 = [int(v) for v in a.ausschnitt.split(",")]
    c = zeichne(karte, bild, x0 - 8, y0 - 8, x1 - x0 + 16, y1 - y0 + 16, a.f, flaechen=fl,
                polys=[(p["punkte"], (255, 40, 40), str(i + 1)) for i, p in enumerate(polys)],
                titel=f"Kandidaten fuer {a.id}", nummern=False)
    speichere(c, a.out)


def cmd_probe(a):
    karte, bild, seg = lade()
    kat = katmod.laden(None) if hasattr(katmod, "laden") else None
    b = Bearbeitung(karte, seg, kat, "probe")
    schritte = json.loads(Path(a.stapel).read_text(encoding="utf-8"))["schritte"]
    for nr, s in enumerate(schritte, 1):
        try:
            r = b.anwenden(s)
        except EingriffFehler as e:
            print(f"{nr}. {s['op']} FEHLER: {e}")
            return 1
        print(f"{nr}. {s['op']}: {json.dumps(r, ensure_ascii=False)}")
    vorher = set(np.unique(karte).tolist())
    nachher = set(np.unique(b.karte).tolist())
    print("neue IDs:", sorted(nachher - vorher), "weg:", sorted(vorher - nachher))
    geaendert = b.karte != karte
    ys, xs = np.nonzero(geaendert)
    if len(xs):
        print("geaendert:", int(geaendert.sum()), "px, x", xs.min(), xs.max(), "y", ys.min(), ys.max())
        aussen = geaendert.copy()
        aussen[KERN[1]:KERN[3], KERN[0]:KERN[2]] = False
        print("ausserhalb Kern geaendert:", int(aussen.sum()))
    for i in sorted(nachher - vorher):
        m = b.karte == i
        yy, xx = np.nonzero(m)
        e = next(s for s in b.segmente["segmente"] if s["id"] == i)
        nb = sorted(int(n) for n in nachbarn(b.karte, i)) if m.sum() < 200 else ""
        print(f"  {i}: {int(m.sum())} px, Mitte {int(xx.mean())}/{int(yy.mean())}, Klasse {e['klasse']} {nb}")
    if a.out:
        box = [int(v) for v in a.box.split(",")]
        c = zeichne(b.karte, bild, box[0], box[1], box[2] - box[0], box[3] - box[1], a.f, titel="Probe nach Stapel",
                    klassen={s["id"]: s["klasse"] for s in b.segmente["segmente"]} if a.klassen else None)
        speichere(c, a.out)
    return 0


def cmd_info(a):
    karte, bild, seg = lade()
    e = {s["id"]: s for s in seg["segmente"]}
    for sid in [int(x) for x in a.ids.split(",")]:
        m = karte == sid
        if not m.any():
            print(sid, "nicht auf der Karte")
            continue
        yy, xx = np.nonzero(m)
        g = bild[m]
        print(f"{sid}: {int(m.sum())} px, x {xx.min()}-{xx.max()}, y {yy.min()}-{yy.max()}, Grau mittel {g.mean():.0f} "
              f"(p10 {np.percentile(g, 10):.0f}, p90 {np.percentile(g, 90):.0f}), Klasse {e[sid]['klasse']}, "
              f"Nachbarn {sorted(int(n) for n in nachbarn(karte, sid))}")


def nachbarn(karte, sid):
    m = karte == sid
    d = ndimage.binary_dilation(m, structure=[[0, 1, 0], [1, 1, 1], [0, 1, 0]]) & ~m
    return set(np.unique(karte[d]).tolist())


def main():
    p = argparse.ArgumentParser()
    sp = p.add_subparsers(dest="cmd", required=True)
    z = sp.add_parser("zoom")
    for k in ("x0", "y0", "w", "h"):
        z.add_argument("--" + k, type=int, required=True)
    z.add_argument("--f", type=int, default=6)
    z.add_argument("--out", required=True)
    z.add_argument("--stapel")
    z.add_argument("--stapel_nr", action="store_true")
    z.add_argument("--markiere")
    z.add_argument("--titel")
    z.add_argument("--kontrast", action="store_true")
    z.add_argument("--viertel")
    z.add_argument("--ohne_nummern", action="store_true")
    z.add_argument("--ohne_rahmen", action="store_true")
    z.add_argument("--klassen", action="store_true")
    z.set_defaults(fn=cmd_zoom)
    d = sp.add_parser("dach")
    d.add_argument("--id", type=int, required=True)
    d.add_argument("--box", required=True)
    d.add_argument("--schwelle", type=float, default=120)
    d.add_argument("--sigma", type=float, default=1.0)
    d.add_argument("--oeffnen", type=int, default=3)
    d.add_argument("--minfl", type=int, default=40)
    d.add_argument("--rel", type=int, default=0)
    d.add_argument("--loch", type=int, default=30)
    d.add_argument("--ausschnitt")
    d.add_argument("--schnitt", action="append")
    d.add_argument("--weg", action="append")
    d.add_argument("--f", type=int, default=3)
    d.add_argument("--json", required=True)
    d.add_argument("--out", required=True)
    d.set_defaults(fn=cmd_dach)
    pr = sp.add_parser("probe")
    pr.add_argument("--stapel", required=True)
    pr.add_argument("--box", default="64,64,564,564")
    pr.add_argument("--f", type=int, default=2)
    pr.add_argument("--out")
    pr.add_argument("--klassen", action="store_true")
    pr.set_defaults(fn=cmd_probe)
    i = sp.add_parser("info")
    i.add_argument("--ids", required=True)
    i.set_defaults(fn=cmd_info)
    a = p.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    return a.fn(a) or 0


if __name__ == "__main__":
    sys.exit(main())
