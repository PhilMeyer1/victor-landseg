"""Baut die Abgabe Fassung C fuer Teilkachel r1c1 aus der Vorstufe plus eigenen Entscheidungen.

Schritte: Vorstufe laden -> Verschmelzen -> Teilen an Engstellen (Rasen 67) -> Schneiden (177) ->
neue Flaechen aus Polygonen -> Zusammenhang erzwingen, Kleinstreste anhaengen -> Klassen setzen ->
labels.tif, segmente.json, kategorien-teil.json schreiben.
Nur die Vorstufe wird gelesen; geschrieben wird nur in diesen Ordner.
"""
import json
import sys
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image, ImageDraw
from scipy import ndimage

HIER = Path(__file__).resolve().parent
BASIS = HIER.parent.parent
VOR = BASIS / "vorstufe" / "r1c1"
B = 400000
KERN = (64, 64, 564, 564)  # x0, y0, x1, y1 (exklusiv)

sys.path.insert(0, str(HIER))
from entscheidungen import (KLASSEN, ENTSCHEIDUNG, VERSCHMELZEN, POLYGONE, SCHNITTE, ENGSTELLEN,  # noqa: E402
                            HELL, STANDARD)

V4 = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], bool)


def nachbar_mit_laengster_grenze(L, m):
    """ID des Nachbarn mit der laengsten gemeinsamen Kante zur Maske m."""
    zaehl = {}
    for dy, dx in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        a = np.roll(m, (dy, dx), (0, 1))
        if dy == 1:
            a[0, :] = False
        if dy == -1:
            a[-1, :] = False
        if dx == 1:
            a[:, 0] = False
        if dx == -1:
            a[:, -1] = False
        rand = a & ~m
        for v in L[rand]:
            zaehl[int(v)] = zaehl.get(int(v), 0) + 1
    if not zaehl:
        return None
    return max(zaehl.items(), key=lambda kv: kv[1])[0]


def polygon_maske(form, punkte):
    img = Image.new("L", (form[1], form[0]), 0)
    d = ImageDraw.Draw(img)
    if punkte[0] == "kreis":
        _, cx, cy, r = punkte
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=1)
    else:
        d.polygon([tuple(p) for p in punkte], fill=1)
    return np.asarray(img).astype(bool)


def main():
    L = tifffile.imread(VOR / "labels.tif").astype(np.uint32)
    vor = {s["id"]: s for s in json.load(open(VOR / "segmente.json", encoding="utf-8"))["segmente"]}
    klasse = {}  # id -> (code, name, sicher, notiz)
    for i, s in vor.items():
        kurz = i - B
        if kurz in ENTSCHEIDUNG:
            klasse[i] = ENTSCHEIDUNG[kurz]
        else:
            code = STANDARD(s)
            klasse[i] = (code, KLASSEN[code][0], False, "nur nach Regel aus der Vorstufe abgeleitet (ausserhalb des Kerns)")
    verlauf = []
    naechste = [B + 409]

    def neue_id():
        v = naechste[0]
        naechste[0] += 1
        return v

    # 1 Verschmelzen
    for ziel, quellen in VERSCHMELZEN:
        for q in quellen:
            L[L == B + q] = B + ziel
            klasse.pop(B + q, None)
        verlauf.append({"op": "verschmelzen", "ziel": ziel, "ids": quellen})

    # 2 Engstellen: Segment an Engstellen in Teile trennen (Erosion, Komponenten, Rueckverteilung)
    for kurz, radius, mindest in ENGSTELLEN:
        sid = B + kurz
        m = L == sid
        er = ndimage.binary_erosion(m, structure=V4, iterations=radius)
        lab, n = ndimage.label(er, structure=V4)
        groessen = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
        kerne = [k + 1 for k in range(n) if groessen[k] >= mindest]
        if len(kerne) < 2:
            continue
        saat = np.zeros(L.shape, np.int32)
        for j, k in enumerate(kerne):
            saat[lab == k] = j + 1
        # Rueckverteilung: jeder Bildpunkt von m an den naechsten Kern (euklidisch)
        _, (iy, ix) = ndimage.distance_transform_edt(saat == 0, return_indices=True)
        zu = saat[iy, ix]
        zu[~m] = 0
        groesste = max(range(1, len(kerne) + 1), key=lambda j: (zu == j).sum())
        neu_ids = []
        for j in range(1, len(kerne) + 1):
            if j == groesste:
                continue
            nid = neue_id()
            L[zu == j] = nid
            klasse[nid] = klasse[sid]
            neu_ids.append(nid)
        verlauf.append({"op": "teilen_engstellen", "id": sid, "radius": radius, "neu": neu_ids})

    # 3 Schnitte: Linie teilt Segment; Teil auf der Seite 'oben' bekommt neue ID und eigene Klasse
    for kurz, linie, neue_klasse in SCHNITTE:
        sid = B + kurz
        m = L == sid
        img = Image.new("L", (L.shape[1], L.shape[0]), 0)
        ImageDraw.Draw(img).line([tuple(p) for p in linie], fill=1, width=1)
        strich = np.asarray(img).astype(bool) & m
        rest = m & ~strich
        lab, n = ndimage.label(rest, structure=V4)
        if n < 2:
            raise SystemExit(f"Schnitt in {kurz} trennt nicht")
        groessen = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
        reihen = sorted(range(1, n + 1), key=lambda k: -groessen[k - 1])
        a, b = reihen[0], reihen[1]
        ya = np.nonzero(lab == a)[0].mean()
        yb = np.nonzero(lab == b)[0].mean()
        oben = a if ya < yb else b
        nid = neue_id()
        L[lab == oben] = nid
        klasse[nid] = neue_klasse
        verlauf.append({"op": "schneiden", "id": sid, "linie": linie, "neu": nid})

    # 3b Helle Teilflaeche abtrennen (Terrasse am Dach): Mittelwert RGB ueber Schwelle, gefuellt
    bild = np.asarray(Image.open(BASIS / "teilkacheln" / "r1c1.png").convert("RGB")).astype(float)
    for kurz, schwelle, eintrag in HELL:
        sid = B + kurz
        m = L == sid
        hell = m & (bild.mean(2) > schwelle)
        hell = ndimage.binary_opening(hell, structure=V4) & m
        lab, n = ndimage.label(hell, structure=V4)
        if n == 0:
            continue
        groessen = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
        k = int(np.argmax(groessen)) + 1
        nid = neue_id()
        L[lab == k] = nid
        klasse[nid] = eintrag
        verlauf.append({"op": "hell_abtrennen", "id": sid, "schwelle": schwelle, "neu": nid,
                        "flaeche": int((lab == k).sum())})

    # 4 Polygone: neue Segmente
    for name, punkte, eintrag in POLYGONE:
        pm = polygon_maske(L.shape, punkte)
        nid = neue_id()
        L[pm] = nid
        klasse[nid] = eintrag
        verlauf.append({"op": "polygon", "name": name, "neu": nid, "flaeche": int(pm.sum())})

    # 5 Zusammenhang erzwingen; Reste unter 12 Bildpunkten an den Nachbarn mit laengster Grenze
    for _runde in range(3):
        geaendert = False
        for sid in np.unique(L):
            m = L == sid
            lab, n = ndimage.label(m, structure=V4)
            if n <= 1:
                continue
            groessen = ndimage.sum(np.ones_like(lab), lab, range(1, n + 1))
            haupt = int(np.argmax(groessen)) + 1
            for k in range(1, n + 1):
                if k == haupt:
                    continue
                teil = lab == k
                if groessen[k - 1] < 12:
                    nb = nachbar_mit_laengster_grenze(L, teil)
                    L[teil] = nb
                else:
                    nid = neue_id()
                    L[teil] = nid
                    klasse[nid] = klasse[int(sid)]
                geaendert = True
        if not geaendert:
            break
    # Kleinstsegmente (< 6 Bildpunkte) an den Nachbarn anhaengen
    for sid in np.unique(L):
        m = L == sid
        if m.sum() < 6:
            nb = nachbar_mit_laengster_grenze(L, m)
            if nb is not None:
                L[m] = nb
                verlauf.append({"op": "anhaengen_klein", "id": int(sid), "an": nb})

    # 6 Ausgabe
    x0, y0, x1, y1 = KERN
    kern = np.zeros(L.shape, bool)
    kern[y0:y1, x0:x1] = True
    segmente, offen = [], []
    for sid in sorted(int(v) for v in np.unique(L)):
        code, name, sicher, notiz = klasse[sid]
        if code not in KLASSEN:
            raise SystemExit(f"Unbekannte Klasse {code} bei {sid}")
        m = L == sid
        im_kern = bool((m & kern).any())
        e = {"id": sid, "klasse": code, "grob": code.split(".")[0], "name": name, "im_kern": im_kern,
             "sicher": bool(sicher), "flaeche": int(m.sum())}
        if sid in vor:
            e["vorstufe_klasse"] = vor[sid]["klasse"]
        else:
            e["herkunft"] = "eigener Eingriff"
        if notiz:
            e["notiz"] = notiz
        segmente.append(e)
        if not sicher and im_kern:
            offen.append({"id": sid, "klasse": code, "notiz": notiz or "Klasse oder Grenze unsicher"})
    tmp = HIER / "labels.tif.tmp"
    tifffile.imwrite(tmp, L.astype(np.uint32), compression="zlib", photometric="minisblack")
    tmp.replace(HIER / "labels.tif")
    nicht = [
        "Grenzen der Vorstufe nur dort geaendert, wo in arbeitsweise.md genannt; die uebrigen Umrisse "
        "sind nicht Segment fuer Segment auf die Bildkante geprueft.",
        "Segmente ausserhalb des Kerns (Kontextrand) nur nach Regel aus der Vorstufe klassifiziert, nicht einzeln angesehen.",
    ]
    json.dump({"schema": "landseg-segmente/1", "teilkachel": "r1c1", "fassung": "C",
               "segmente": segmente, "offen": offen, "nicht_geprueft": nicht,
               "verlauf": [{"bearbeiter": "fassung-c-r1c1", **v} for v in verlauf]},
              open(HIER / "segmente.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    classes = []
    for code, (name, farbe, hinweis) in KLASSEN.items():
        teile = code.split(".")
        classes.append({"code": code, "name": name, "parent": ".".join(teile[:-1]) or None,
                        "level": len(teile), "color": farbe, "image_cue": hinweis})
    json.dump({"schema": "landseg-kategorien/1", "teilkachel": "r1c1", "classes": classes},
              open(HIER / "kategorien-teil.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    n_kern = sum(1 for s in segmente if s["im_kern"])
    print(f"Segmente {len(segmente)} (im Kern {n_kern}), offen im Kern {len(offen)}")


if __name__ == "__main__":
    main()
