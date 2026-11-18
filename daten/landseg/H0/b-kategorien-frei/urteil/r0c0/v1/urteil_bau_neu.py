"""Baut urteil.json und die Ergebnisbilder (roh, umriss, maengel, vorschlag) eines Viertels von r0c0.

Aufruf: urteil_bau.py <daten.py>   (daten.py definiert VIERTEL, SEGMENTE, EINGRIFFE, UNSICHER, OFFEN,
NICHT_GEPRUEFT, NAHT, NAH_EIGENE, UEBERSICHT_EIGENE)
"""
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image, ImageDraw, ImageFont

BASIS = "C:/Users/Phil/Developement/Victor/daten/landseg/H0"
LABELS = BASIS + "/b-kategorien-frei/r0c0/labels.tif"
BILD = BASIS + "/teilkacheln/r0c0.png"
VB = BASIS + "/viertel/r0c0"

KLASSEN = {
    "FELD": ("Landwirtschaft", "Feld", "Feld"),
    "WEGRAIN": ("Grünfläche", "Saum", "Wegrain"),
    "FELDRAIN": ("Grünfläche", "Saum", "Feldrain"),
    "ANGER": ("Grünfläche", "Anger/Brache", "Anger"),
    "BRACHE": ("Grünfläche", "Anger/Brache", "Brache"),
    "FAHRWEG": ("Verkehrsfläche", "Straße/Weg", "Fahrweg"),
    "STRASSENRAND": ("Verkehrsfläche", "Straße/Weg", "Straßenrand"),
    "FELDWEG": ("Verkehrsfläche", "Straße/Weg", "Feldweg"),
    "HOF": ("Hof und Garten", "Hof", "Hof"),
    "GARTEN": ("Hof und Garten", "Garten", "Garten"),
    "LAENGSBAU": ("Gebäude", "Gebäude", "Längsbau (Streckhof)"),
    "HINTERGEB": ("Gebäude", "Gebäude", "Hintergebäude"),
    "NEBENGEB": ("Gebäude", "Gebäude", "Nebengebäude"),
    "GEBAEUDE": ("Gebäude", "Gebäude", "Gebäude"),
    "GEBUESCH": ("Gehölz", "Gebüsch/Baum", "Gebüsch"),
    "BAUM": ("Gehölz", "Gebüsch/Baum", "Baum"),
    "SCHATTEN": ("Unklar", "Schatten", "Schlagschatten"),
}
FARBEN = {
    "Feld": (150, 200, 60), "Wegrain": (120, 230, 160), "Feldrain": (90, 200, 200), "Anger": (200, 230, 120),
    "Brache": (210, 180, 100), "Fahrweg": (255, 255, 90), "Straßenrand": (190, 160, 220),
    "Feldweg": (230, 210, 170), "Hof": (230, 150, 60), "Garten": (60, 170, 60),
    "Längsbau (Streckhof)": (230, 40, 40), "Hintergebäude": (180, 30, 120), "Nebengebäude": (250, 100, 150),
    "Gebäude": (200, 60, 60), "Gebüsch": (20, 110, 30), "Baum": (10, 80, 20), "Schlagschatten": (60, 60, 160),
}
MERKMALE = [
    ("Landwirtschaft", "grob", None, "große gleichmäßige Flächen außerhalb der Höfe, feine Streifen oder gleichmäßiges Korn"),
    ("Feld", "mittel", "Landwirtschaft", "große, gleichmäßig dunkelgraue Fläche mit feinem Korn; Acker oder Grünland im Schwarz-Weiß-Bild nicht sicher zu trennen"),
    ("Grünfläche", "grob", None, "unbebaute, unversiegelte Flächen mit fleckiger, mittelgrauer Textur ohne Feldstruktur"),
    ("Saum", "mittel", "Grünfläche", "schmaler Streifen zwischen Weg oder Hof und Feld, fleckig, oft mit dunklen Büschen"),
    ("Wegrain", "fein", "Saum", "Streifen neben einer Fahrbahn, heller als das Feld, dunkler als der Weg"),
    ("Feldrain", "fein", "Saum", "dunkler, fleckiger Randstreifen am Feldrand"),
    ("Anger/Brache", "mittel", "Grünfläche", "offene, fleckig mittelgraue Fläche hinter den Höfen, mit hellen Fahrspuren"),
    ("Anger", "fein", "Anger/Brache", "breiter offener Streifen zwischen Hofenden und Feld mit hellen, diffusen Fahrspuren"),
    ("Brache", "fein", "Anger/Brache", "fleckige, ungeordnete Fläche ohne Spuren und ohne Feldstreifen"),
    ("Verkehrsfläche", "grob", None, "lange, gleichmäßig breite, helle Bänder"),
    ("Straße/Weg", "mittel", "Verkehrsfläche", "helles Band mit parallelen Rändern; Belag im Schwarz-Weiß-Bild nicht bestimmbar"),
    ("Fahrweg", "fein", "Straße/Weg", "durchgehend sehr helles Band von etwa 10 Bildpunkten Breite"),
    ("Straßenrand", "fein", "Straße/Weg", "mittelgrauer, gleichmäßiger Streifen zwischen Fahrbahn und Hofeinfahrten"),
    ("Feldweg", "fein", "Straße/Weg", "schmaler heller Weg hinter den Höfen oder am Feldrand"),
    ("Hof und Garten", "grob", None, "Flächen innerhalb der Grundstücke zwischen den Gebäuden"),
    ("Hof", "mittel", "Hof und Garten", "mittelgraue bis dunkle (beschattete) Fläche zwischen den Längsbauten, ohne Gartenkorn"),
    ("Garten", "mittel", "Hof und Garten", "von dunklen Mauer- oder Zaunlinien umrahmtes Rechteck mit gleichmäßig fleckigem Grau"),
    ("Gebäude", "grob", None, "scharf und gerade begrenzte Fläche, an einer Seite ein fast schwarzer Schlagschatten"),
    ("Gebäude", "mittel", "Gebäude", "Dachfläche: hell bis mittelgrau, gerade Kanten, Schlagschatten daneben"),
    ("Längsbau (Streckhof)", "fein", "Gebäude", "langes schmales helles Dach längs des Grundstücks, quer zur Straße"),
    ("Hintergebäude", "fein", "Gebäude", "breiterer Bau quer am hinteren Grundstücksende (Stadel, Scheune)"),
    ("Nebengebäude", "fein", "Gebäude", "kleiner, scharf begrenzter heller Bau im Hof oder am Hofende"),
    ("Gehölz", "grob", None, "dunkle, rundliche, unscharf begrenzte Flecken mit Schatten"),
    ("Gebüsch/Baum", "mittel", "Gehölz", "dunkle Flecken oder Ketten von Flecken"),
    ("Gebüsch", "fein", "Gebüsch/Baum", "kleine dunkle Flecken am Weg- oder Feldrand"),
    ("Baum", "fein", "Gebüsch/Baum", "einzelne runde dunkle Krone mit Schatten"),
    ("Unklar", "grob", None, "Fläche, deren Oberfläche im Bild nicht zu sehen ist"),
    ("Schatten", "mittel", "Unklar", "fast schwarze Fläche neben einem Gebäude, Untergrund nicht erkennbar"),
    ("Schlagschatten", "fein", "Schatten", "fast schwarze, scharf begrenzte Fläche direkt neben einem hellen Bau (im Bild meist rechts oder unten rechts davon)"),
]


def lade_daten(pfad):
    spec = importlib.util.spec_from_file_location("daten", pfad)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def font(n):
    try:
        return ImageFont.truetype("arial.ttf", n)
    except OSError:
        return ImageFont.load_default()


def basisbild(img, fx, fy, fw, fh, f):
    sub = img[fy:fy + fh, fx:fx + fw]
    return np.kron(np.stack([sub] * 3, -1), np.ones((f, f, 1), np.uint8))


def rahmen(d, vx, vy, fx, fy, f, w=250):
    d.rectangle([(vx - fx) * f, (vy - fy) * f, (vx + w - fx) * f, (vy + w - fy) * f], outline=(0, 255, 255), width=2)


def bilder_bauen(D, ziel, eintraege):
    lab = tifffile.imread(LABELS).astype(np.int64)
    img = np.asarray(Image.open(BILD).convert("L"))
    vj = json.load(open(f"{VB}/{D.VIERTEL}/viertel.json", encoding="utf-8"))
    vi = vj["viertel_im_bild"]
    fe = vj["bilder"]["uebersicht_nummern.jpg"]["fenster"]
    fx, fy, fw, fh, f = fe["x"], fe["y"], fe["breite"], fe["hoehe"], fe["faktor"]
    L = lab[fy:fy + fh, fx:fx + fw]
    Lb = np.kron(L, np.ones((f, f), np.int64))
    rand = np.zeros(Lb.shape, bool)
    rand[:, 1:] |= Lb[:, 1:] != Lb[:, :-1]
    rand[1:, :] |= Lb[1:, :] != Lb[:-1, :]
    ids = {e["id"] for e in eintraege}
    # roh
    im = Image.fromarray(basisbild(img, fx, fy, fw, fh, f))
    d = ImageDraw.Draw(im)
    rahmen(d, vi["x"], vi["y"], fx, fy, f)
    d.text((6, 6), f"r0c0 {D.VIERTEL}: Luftbild 1968 (unverändert)", fill=(255, 255, 0), font=font(16), stroke_width=2, stroke_fill=(0, 0, 0))
    im.save(f"{ziel}/roh.jpg", quality=90)
    # umriss
    arr = basisbild(img, fx, fy, fw, fh, f)
    arr[rand] = (255, 230, 0)
    im = Image.fromarray(arr)
    d = ImageDraw.Draw(im)
    rahmen(d, vi["x"], vi["y"], fx, fy, f)
    from scipy import ndimage
    for i in np.unique(L):
        m = L == i
        if m.sum() < 8:
            continue
        dt = ndimage.distance_transform_edt(np.pad(m, 1))[1:-1, 1:-1]
        yy, xx = np.unravel_index(np.argmax(dt), dt.shape)
        col = (255, 255, 255) if int(i) in ids else (150, 150, 150)
        d.text((xx * f + f // 2, yy * f + f // 2), str(int(i) % 100000), fill=col, font=font(13), anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0))
    d.text((6, 6), f"r0c0 {D.VIERTEL}: Grenzen nach dem Nachsegmentieren, weiß = dieses Viertel", fill=(255, 255, 0), font=font(15), stroke_width=2, stroke_fill=(0, 0, 0))
    im.save(f"{ziel}/umriss.jpg", quality=90)
    # maengel
    punkte = []
    for e in eintraege:
        for p in e.get("_punkte_xy", []):
            punkte.append(p)
    arr = basisbild(img, fx, fy, fw, fh, f)
    arr[rand] = (200, 200, 0)
    h_leg = 22 + 17 * max(1, len(punkte))
    im = Image.new("RGB", (arr.shape[1], arr.shape[0] + h_leg), (20, 20, 20))
    im.paste(Image.fromarray(arr), (0, 0))
    d = ImageDraw.Draw(im)
    rahmen(d, vi["x"], vi["y"], fx, fy, f)
    if not punkte:
        d.text((6, arr.shape[0] + 4), "keine Mängel", fill=(255, 255, 255), font=font(14))
    for k, (nr, x, y, text) in enumerate(punkte, 1):
        px, py = (x - fx) * f, (y - fy) * f
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=(230, 0, 0), outline=(255, 255, 255))
        d.text((px, py), str(k), fill=(255, 255, 255), font=font(12), anchor="mm")
        d.text((6, arr.shape[0] + 4 + 17 * (k - 1)), f"{k}: {text}", fill=(255, 255, 255), font=font(13))
    im.save(f"{ziel}/maengel.jpg", quality=90)
    # vorschlag
    arr = basisbild(img, fx, fy, fw, fh, f).astype(np.float64)
    fein = {e["id"]: e["klasse_frei"]["fein"] for e in eintraege}
    farbe = np.zeros(Lb.shape + (3,), np.float64)
    hat = np.zeros(Lb.shape, bool)
    for i, name in fein.items():
        m = Lb == i
        farbe[m] = FARBEN.get(name, (255, 0, 255))
        hat |= m
    arr[hat] = arr[hat] * 0.5 + farbe[hat] * 0.5
    arr = arr.astype(np.uint8)
    arr[rand] = (255, 255, 255)
    benutzt = sorted(set(fein.values()))
    h_leg = 24 + 18 * ((len(benutzt) + 2) // 3)
    im = Image.new("RGB", (arr.shape[1], arr.shape[0] + h_leg), (20, 20, 20))
    im.paste(Image.fromarray(arr), (0, 0))
    d = ImageDraw.Draw(im)
    rahmen(d, vi["x"], vi["y"], fx, fy, f)
    for k, name in enumerate(benutzt):
        cx, cy = 6 + (k % 3) * 310, arr.shape[0] + 6 + 18 * (k // 3)
        d.rectangle([cx, cy + 2, cx + 14, cy + 14], fill=FARBEN.get(name, (255, 0, 255)))
        d.text((cx + 20, cy), name, fill=(255, 255, 255), font=font(13))
    d.text((6, 6), f"r0c0 {D.VIERTEL}: Klassen (fein) wie vorgeschlagen; ungefärbt = Nachbarviertel", fill=(255, 255, 0), font=font(15), stroke_width=2, stroke_fill=(0, 0, 0))
    im.save(f"{ziel}/vorschlag.jpg", quality=90)


def main():
    D = lade_daten(sys.argv[1])
    ziel = f"{BASIS}/b-kategorien-frei/urteil/r0c0/{D.VIERTEL}"
    vb = f"{VB}/{D.VIERTEL}"
    KH = {s["id"]: s["klasse"] for s in json.load(open(BASIS + "/b-kategorien-frei/r0c0/segmente.json", encoding="utf-8"))["segmente"]}
    eintraege = []
    benutzt = set()
    for s in D.SEGMENTE:
        sid, key, sicher, urteil, was, punkte, bilder = s
        kf = KLASSEN[key]
        benutzt |= set(kf)
        pl, pxy = [], []
        for nr, p in enumerate(punkte, 1):
            art, text, xy, fl = p
            pl.append({"nr": nr, "art": art, "text": text, "flaeche_px": fl})
            if xy:
                pxy.append((nr, xy[0], xy[1], f"{sid % 100000}: {text if len(text) <= 92 else text[:91] + '…'}"))
        bl = []
        for b in bilder:
            bl.append(b if "/" in b else (f"{vb}/{b}" if b.startswith(("uebersicht", "nah1", "nah2", "nah3", "nah4")) and "_" in b and not b.startswith("nah_") else f"{ziel}/{b}"))
        eintraege.append({"id": sid, "klasse_heute": KH.get(sid), "was_ist_es": was, "urteil": urteil,
                          "klasse_vorschlag": None, "klasse_frei": {"grob": kf[0], "mittel": kf[1], "fein": kf[2]},
                          "sicher": sicher, "punkte": pl, "bilder": bl, "_punkte_xy": pxy})
    bilder_bauen(D, ziel, eintraege)
    for e in eintraege:
        e.pop("_punkte_xy")
    klassen = []
    gesehen = set()
    for name, ebene, eltern, merkmal in MERKMALE:
        if name in benutzt and (name, ebene) not in gesehen:
            if ebene == "mittel" and name == "Gebäude" and eltern == "Gebäude":
                pass
            gesehen.add((name, ebene))
            klassen.append({"name": name, "ebene": ebene, "eltern": eltern, "merkmal": merkmal})
    uebersicht = [BASIS + "/H0.png", BASIS + "/ganz/r0c0/ganz_nummern.jpg"] + [f"{vb}/{n}" for n in D.UEBERSICHT_GESEHEN]
    nah = [f"{vb}/{n}" for n in D.NAH_GESEHEN] + [f"{ziel}/{n}" for n in D.NAH_EIGENE]
    out = {"teilkachel": "r0c0", "viertel": D.VIERTEL, "bearbeiter": f"urt-b-r0c0-{D.VIERTEL}",
           "bilder_angesehen": {"uebersicht": uebersicht, "nah": nah},
           "segmente": eintraege, "naht": D.NAHT, "unsicher": D.UNSICHER, "nicht_geprueft": D.NICHT_GEPRUEFT,
           "offen": D.OFFEN, "eingriffe": D.EINGRIFFE, "klassen_frei": klassen}
    Path(f"{ziel}/urteil.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("geschrieben", len(eintraege), "Segmente,", sum(1 for e in eintraege if not e["sicher"]), "unsicher,",
          sum(1 for e in eintraege if e["urteil"] == "nicht_sauber"), "nicht sauber,",
          sum(len(e["punkte"]) for e in eintraege), "Punkte")


if __name__ == "__main__":
    main()
