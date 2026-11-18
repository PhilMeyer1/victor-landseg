"""Baut urteil.json und die vier Ergebnisbilder eines Viertels aus einer Urteilsdatei (spec.json).

Aufruf: python -B bau.py <ergebnisordner>   (dort liegt spec.json)
spec.json: {"viertel": "v1", "bilder_angesehen": {...}, "segmente": [[id, was, vorschlag|null, sicher,
            [[art, text, flaeche|null], ...], [bildkuerzel...]], ...], "naht": [...], "unsicher": [...],
            "nicht_geprueft": [...], "offen": [...], "eingriffe": [...]}
Bildkürzel: U=uebersicht_nummern, R=uebersicht_roh, K=uebersicht_kontrast, N1..N4 = nah<n>_nummern (vorbereitet),
            n<k> = eigenes nah_<k>.jpg, k<k> = eigenes kontrast_<k>.jpg.
Punkte im Text als "(x/y)" in Teilkachel-Bildpunkten.
"""
import json
import re
import sys
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont

H0 = Path("C:/Users/Phil/Developement/Victor/daten/landseg/H0")
BILD = H0 / "teilkacheln/r1c1.png"
LABELS = H0 / "c-feste-liste/r1c1/labels.tif"
SEGMENTE = H0 / "c-feste-liste/r1c1/segmente.json"
KAT = Path("C:/Users/Phil/Developement/Victor/landseg/kategorien.json")
VIERTEL = {"v1": (64, 64), "v2": (314, 64), "v3": (64, 314), "v4": (314, 314)}


def font(n, fett=False):
    try:
        return ImageFont.truetype("arialbd.ttf" if fett else "arial.ttf", n)
    except OSError:
        return ImageFont.load_default()


def bildpfad(v, k, ordner):
    vb = H0 / "viertel/r1c1" / v
    if k == "U":
        return str(vb / "uebersicht_nummern.jpg").replace("\\", "/")
    if k == "R":
        return str(vb / "uebersicht_roh.jpg").replace("\\", "/")
    if k == "K":
        return str(vb / "uebersicht_kontrast.jpg").replace("\\", "/")
    if k.startswith("N"):
        return str(vb / f"nah{k[1:]}_nummern.jpg").replace("\\", "/")
    if k.startswith("n"):
        return str(ordner / f"nah_{k[1:]}.jpg").replace("\\", "/")
    if k.startswith("k"):
        return str(ordner / f"kontrast_{k[1:]}.jpg").replace("\\", "/")
    raise ValueError(k)


def grundbild(v, f=3):
    vx, vy = VIERTEL[v]
    x0, y0, w, h = vx - 32, vy - 32, 314, 314
    img = np.array(Image.open(BILD).convert("L"))
    L = tifffile.imread(LABELS)
    sub = img[y0:y0 + h, x0:x0 + w]
    lab = L[y0:y0 + h, x0:x0 + w]
    rgb = np.kron(np.stack([sub] * 3, -1), np.ones((f, f, 1), np.uint8))
    labb = np.kron(lab, np.ones((f, f), lab.dtype))
    return rgb, labb, lab, (x0, y0, f)


def grenzen(rgb, labb, farbe=(255, 230, 0)):
    g = np.zeros(labb.shape, bool)
    g[:, 1:] |= labb[:, 1:] != labb[:, :-1]
    g[1:, :] |= labb[1:, :] != labb[:-1, :]
    rgb[g] = farbe


def viertel_rahmen(d, v, fen, breite=3):
    vx, vy = VIERTEL[v]
    x0, y0, f = fen
    d.rectangle([(vx - x0) * f, (vy - y0) * f, (vx - x0 + 250) * f - 1, (vy - y0 + 250) * f - 1],
                outline=(0, 255, 255), width=breite)


def ankerpunkte(lab):
    ids, inv = np.unique(lab, return_inverse=True)
    inv = inv.reshape(lab.shape)
    out = {}
    for k, sid in enumerate(ids):
        ys, xs = np.nonzero(inv == k)
        if len(xs) < 6:
            continue
        cx, cy = xs.mean(), ys.mean()
        j = np.argmin((xs - cx) ** 2 + (ys - cy) ** 2)
        out[int(sid)] = (int(xs[j]), int(ys[j]))
    return out


def unterschrift(im, zeilen, titel):
    f = font(15)
    hoehe = 26 + 19 * len(zeilen)
    neu = Image.new("RGB", (im.width, im.height + hoehe), (25, 25, 25))
    neu.paste(im, (0, 0))
    d = ImageDraw.Draw(neu)
    d.text((8, im.height + 4), titel, fill=(255, 255, 255), font=font(15, True))
    for i, z in enumerate(zeilen):
        d.text((8, im.height + 24 + 19 * i), z, fill=(235, 235, 235), font=f)
    if max(neu.size) > 2000:
        s = 2000 / max(neu.size)
        neu = neu.resize((int(neu.width * s), int(neu.height * s)), Image.LANCZOS)
    return neu


def main(ordner):
    ordner = Path(ordner)
    spec = json.loads((ordner / "spec.json").read_text(encoding="utf-8"))
    v = spec["viertel"]
    seg = {s["id"]: s for s in json.loads(SEGMENTE.read_text(encoding="utf-8"))["segmente"]}
    kat = {c["code"]: c for c in json.loads(KAT.read_text(encoding="utf-8"))["classes"]}
    eintraege = []
    for sid, was, vorschlag, sicher, punkte, bilder in spec["segmente"]:
        pk = [{"nr": i + 1, "art": a, "text": t, "flaeche_px": fl} for i, (a, t, fl) in enumerate(punkte)]
        eintraege.append({
            "id": sid, "klasse_heute": seg[sid]["klasse"], "was_ist_es": was,
            "urteil": "sauber" if (vorschlag is None and not pk) else "nicht_sauber",
            "klasse_vorschlag": vorschlag, "sicher": bool(sicher), "punkte": pk,
            "bilder": [bildpfad(v, k, ordner) for k in bilder]})
    ba = spec["bilder_angesehen"]
    urteil = {"teilkachel": "r1c1", "viertel": v, "bearbeiter": f"urt-c-r1c1-{v}",
              "bilder_angesehen": {"uebersicht": ba["uebersicht"],
                                   "nah": [bildpfad(v, k, ordner) if len(k) <= 3 else k for k in ba["nah"]]},
              "segmente": eintraege, "naht": spec["naht"], "unsicher": spec["unsicher"],
              "nicht_geprueft": spec["nicht_geprueft"], "offen": spec["offen"], "eingriffe": spec["eingriffe"]}
    (ordner / "urteil.json").write_text(json.dumps(urteil, ensure_ascii=False, indent=1), encoding="utf-8")

    # roh.jpg
    rgb, labb, lab, fen = grundbild(v)
    im = Image.fromarray(rgb.copy())
    viertel_rahmen(ImageDraw.Draw(im), v, fen)
    unterschrift(im, [f"Viertel {v} cyan umrandet; 32 Bildpunkte Umgebung; 3fach."],
                 f"r1c1 {v}: Bild unverändert").save(ordner / "roh.jpg", quality=90)

    # umriss.jpg
    anker = ankerpunkte(lab)
    eigene = {e["id"] for e in eintraege}
    r = rgb.copy()
    grenzen(r, labb)
    im = Image.fromarray(r)
    d = ImageDraw.Draw(im)
    viertel_rahmen(d, v, fen)
    fk = font(13, True)
    for sid, (ax, ay) in anker.items():
        t = str(sid % 100000)
        farbe = (255, 255, 255) if sid in eigene else (170, 170, 170)
        px, py = ax * fen[2], ay * fen[2]
        d.text((px - 7, py - 6), t, fill=(0, 0, 0), font=fk)
        d.text((px - 8, py - 7), t, fill=farbe, font=fk)
    unterschrift(im, ["Grenzen gelb nach den Eingriffen; Nummer = ID − 400000 (weiß: dieses Viertel, grau: Nachbarn/Rand)."],
                 f"r1c1 {v}: Segmentgrenzen mit ID").save(ordner / "umriss.jpg", quality=90)

    # maengel.jpg
    r = rgb.copy()
    grenzen(r, labb, (150, 140, 60))
    im = Image.fromarray(r)
    d = ImageDraw.Draw(im)
    viertel_rahmen(d, v, fen)
    zeilen, n = [], 0
    for e in eintraege:
        for p in e["punkte"]:
            m = re.search(r"\((\d+)/(\d+)\)", p["text"])
            if not m:
                continue
            n += 1
            x, y = int(m.group(1)), int(m.group(2))
            px, py = (x - fen[0]) * fen[2], (y - fen[1]) * fen[2]
            d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=(220, 30, 30), outline=(255, 255, 255))
            d.text((px - 6 if n < 10 else px - 8, py - 7), str(n), fill=(255, 255, 255), font=font(12, True))
            kurz = p["text"]
            if len(kurz) > 105:
                kurz = kurz[:102] + "…"
            zeilen.append(f"{n}. [{e['id'] % 100000}, {p['art']}] {kurz}")
    if not zeilen:
        zeilen = ["keine Mängel"]
    unterschrift(im, zeilen, f"r1c1 {v}: Mängel (Nummer = Punkt; [Segment, Art])").save(ordner / "maengel.jpg", quality=90)

    # vorschlag.jpg
    r = rgb.copy().astype(np.float32)
    code_von = {}
    for sid in np.unique(lab):
        sid = int(sid)
        e = next((x for x in eintraege if x["id"] == sid), None)
        code = (e["klasse_vorschlag"] or e["klasse_heute"]) if e else seg.get(sid, {}).get("klasse", "0")
        code_von[sid] = (code, e is not None)
        if e is None:
            continue
        hexf = kat.get(code, {}).get("color", "#808080").lstrip("#")
        farbe = np.array([int(hexf[i:i + 2], 16) for i in (0, 2, 4)], np.float32)
        m = labb == sid
        r[m] = r[m] * 0.55 + farbe * 0.45
    r = r.astype(np.uint8)
    grenzen(r, labb, (255, 255, 255))
    im = Image.fromarray(r)
    d = ImageDraw.Draw(im)
    viertel_rahmen(d, v, fen)
    for sid, (ax, ay) in anker.items():
        code, eigen = code_von[sid]
        if not eigen:
            continue
        px, py = ax * fen[2], ay * fen[2]
        d.text((px - 9, py - 6), code, fill=(0, 0, 0), font=fk)
        d.text((px - 10, py - 7), code, fill=(255, 255, 0), font=fk)
    unterschrift(im, ["Klassen, wie ich sie setzen würde (Code und Farbe), nur Segmente dieses Viertels eingefärbt;",
                      "Grenzen weiß = Stand nach meinen Eingriffen; weitere Teilungen stehen als Punkte in maengel.jpg."],
                 f"r1c1 {v}: Vorschlag").save(ordner / "vorschlag.jpg", quality=90)
    print("geschrieben:", len(eintraege), "Segmente,", n, "Punkte")


if __name__ == "__main__":
    main(sys.argv[1])
