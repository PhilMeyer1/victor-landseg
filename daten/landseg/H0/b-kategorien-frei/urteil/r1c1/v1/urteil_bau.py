"""Gemeinsamer Baustein: urteil.json und Abgabebilder (roh, umriss, maengel, vorschlag) eines Viertels schreiben.

Aufruf aus einer Datendatei je Viertel: urteil_bau.schreiben(viertel, ordner, segmente, eingriffe, extra)
"""
import json
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

sys.path.insert(0, "C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c1/v1")
import werkzeug as wz  # noqa: E402

H0 = "C:/Users/Phil/Developement/Victor/daten/landseg/H0"
VB = H0 + "/viertel/r1c1"

K = {
    "STR_DORF": ("Verkehr", "Straße", "Dorfstraße"),
    "STR_LAND": ("Verkehr", "Straße", "Landstraße"),
    "STR_RAND": ("Verkehr", "Straße", "Straßenrand"),
    "PLATZ": ("Verkehr", "Platz", "Anger/Platz"),
    "WEG_BREIT": ("Verkehr", "Weg", "Weg breit"),
    "WEG_FELD": ("Verkehr", "Weg", "Feldweg"),
    "WEG_ZUF": ("Verkehr", "Weg", "Hofzufahrt"),
    "GEB_HELL": ("Siedlung", "Gebäude", "Gebäude mit hellem Dach"),
    "GEB_MITTEL": ("Siedlung", "Gebäude", "Gebäude mit mittelgrauem Dach"),
    "GEB_DUNKEL": ("Siedlung", "Gebäude", "Gebäude mit dunklem Dach"),
    "NEBEN": ("Siedlung", "Gebäude", "Nebengebäude"),
    "GEB": ("Siedlung", "Gebäude", "Gebäude"),
    "HOFST": ("Siedlung", "Hofstelle", "Streckhof-Streifen"),
    "HOF": ("Siedlung", "Hof/Freifläche", "Hof/Freifläche"),
    "VORPLATZ": ("Siedlung", "Hof/Freifläche", "Vorplatz"),
    "GARTEN": ("Siedlung", "Garten", "Garten"),
    "SIED": ("Siedlung", "Siedlung", "Siedlung"),
    "ACKER": ("Landwirtschaft", "Acker", "Acker"),
    "FELD": ("Landwirtschaft", "Feldflur", "Feldflur"),
    "RAIN": ("Landwirtschaft", "Feldrain", "Rain/Wegrand"),
    "BAUM": ("Gehölz", "Baum/Gebüsch", "Baum/Gebüsch"),
    "HECKE": ("Gehölz", "Baumreihe/Hecke", "Baumreihe/Hecke"),
    "BAUMGR": ("Gehölz", "Baumgruppe", "Baumgruppe"),
    "SCH_GEB": ("Schatten", "Schlagschatten", "Gebäudeschatten"),
    "SCH": ("Schatten", "Schlagschatten", "Schlagschatten"),
}

MERKMAL = {
    ("Siedlung", "grob"): "Bebaute Flächen und Hofflächen im Ort: Dächer, Höfe, Gärten in kleinteiligem Muster.",
    ("Verkehr", "grob"): "Helle, lange, gleichmäßige Bänder oder Flächen ohne Dachstruktur.",
    ("Landwirtschaft", "grob"): "Große, gleichmäßig mittelgraue Flächen außerhalb des Orts, teils mit Bearbeitungsstreifen.",
    ("Gehölz", "grob"): "Dunkle, körnig-wolkige Kronen, oft mit Schatten daneben.",
    ("Schatten", "grob"): "Sehr dunkle, glatte Flächen neben hohen Objekten; Untergrund nicht erkennbar.",
    ("Straße", "mittel"): "Breites helles Band, durchgehend, verbindet Ortsteile.",
    ("Platz", "mittel"): "Helle, breite, nicht bandförmige Verkehrsfläche an einer Straßengabel.",
    ("Weg", "mittel"): "Schmaleres oder kürzeres helles Band, zwischen Feldern oder zu Höfen.",
    ("Gebäude", "mittel"): "Rechteckige Fläche mit scharfen Kanten, oft mit Schlagschatten an einer Seite.",
    ("Hofstelle", "mittel"): "Langer Streifen eines Streckhofs zwischen zwei dunklen Schattenlinien: Dach und Hof bei 0,45 m nicht sicher trennbar.",
    ("Hof/Freifläche", "mittel"): "Unbebaute helle bis mittelgraue Fläche zwischen Gebäuden oder an der Straße.",
    ("Garten", "mittel"): "Kleinteilig gemusterte Fläche hinter den Häusern mit Flecken von Bewuchs.",
    ("Siedlung", "mittel"): "Fläche im Ort, Art nicht bestimmbar.",
    ("Acker", "mittel"): "Große Fläche mit parallelen Bearbeitungsstreifen; Acker oder Grünland ist im Schwarz-Weiß nur über die Streifen zu vermuten.",
    ("Feldflur", "mittel"): "Offene landwirtschaftliche Fläche, Acker oder Grünland nicht unterscheidbar.",
    ("Feldrain", "mittel"): "Schmaler Saum am Feld- oder Wegrand, anderer Grauton als das Feld.",
    ("Baum/Gebüsch", "mittel"): "Einzelne dunkle, runde Krone oder Gebüschfleck.",
    ("Baumreihe/Hecke", "mittel"): "Kette dunkler Kronen entlang eines Wegs oder Feldrands.",
    ("Baumgruppe", "mittel"): "Größere zusammenhängende dunkle Kronenfläche.",
    ("Schlagschatten", "mittel"): "Sehr dunkle Fläche an der Schattenseite von Gebäuden oder Bäumen.",
}
FEIN_MERKMAL = {
    "Dorfstraße": "Helle Straße im Ort zwischen den Häuserzeilen.",
    "Landstraße": "Breite, sehr helle, gerade Straße über Land.",
    "Straßenrand": "Schmaler Saum am Straßenrand, etwas dunkler als die Fahrbahn.",
    "Anger/Platz": "Erweiterte helle Fläche an der Straßengabel.",
    "Weg breit": "Breites helles Band zwischen Feldern, fleckig, Belag nicht erkennbar.",
    "Feldweg": "Schmales helles Band zwischen Feldern.",
    "Hofzufahrt": "Kurzes helles Band von der Straße in einen Hof.",
    "Gebäude mit hellem Dach": "Sehr helle Rechteckfläche mit scharfen Kanten.",
    "Gebäude mit mittelgrauem Dach": "Mittelgraue Rechteckfläche mit scharfen Kanten und Schatten.",
    "Gebäude mit dunklem Dach": "Dunkelgraue Rechteckfläche mit scharfen Kanten.",
    "Nebengebäude": "Kleines Rechteck (unter etwa 60 m²) im Hof.",
    "Gebäude": "Gebäude, Dachton gemischt.",
    "Streckhof-Streifen": "Langer schmaler Streifen quer zur Straße: Wohnhaus, Stall und Hof hintereinander.",
    "Hof/Freifläche": "Unbebaute Fläche im Hof.",
    "Vorplatz": "Helle Fläche zwischen Straße und Hauswand.",
    "Garten": "Fleckige Fläche hinter den Höfen.",
    "Siedlung": "Fläche im Ort, Art nicht bestimmbar.",
    "Acker": "Feld mit Bearbeitungsstreifen.",
    "Feldflur": "Feld ohne erkennbare Streifen.",
    "Rain/Wegrand": "Schmaler Saum zwischen Weg und Feld.",
    "Baum/Gebüsch": "Einzelne dunkle Krone.",
    "Baumreihe/Hecke": "Reihe dunkler Kronen.",
    "Baumgruppe": "Zusammenhängende Kronen.",
    "Gebäudeschatten": "Schatten an der Schattenseite einer Häuserzeile oder eines Gebäudes.",
    "Schlagschatten": "Schatten, Werfer nicht sicher bestimmbar.",
}
FARBE = {"Siedlung": (230, 80, 60), "Verkehr": (240, 240, 120), "Landwirtschaft": (120, 200, 80),
         "Gehölz": (30, 120, 40), "Schatten": (90, 60, 160)}


def klassen_frei(segmente):
    namen = {}
    for s in segmente:
        g, m, f = s["klasse_frei"]["grob"], s["klasse_frei"]["mittel"], s["klasse_frei"]["fein"]
        namen[(g, "grob")] = None
        namen[(m, "mittel")] = g
        if f != m:
            namen[(f, "fein")] = m
    aus = []
    for (n, e), el in namen.items():
        if e == "grob":
            mk = MERKMAL.get((n, "grob"), "")
        elif e == "mittel":
            mk = MERKMAL.get((n, "mittel"), "")
        else:
            mk = FEIN_MERKMAL.get(n, "")
        aus.append({"name": n, "ebene": e, "eltern": el, "merkmal": mk})
    ordnung = {"grob": 0, "mittel": 1, "fein": 2}
    return sorted(aus, key=lambda d: (ordnung[d["ebene"]], d["name"]))


def _grund(karte, x0, y0, w, h, f, roh=False, abdunkeln=None):
    img = np.asarray(Image.open(wz.BILD).convert("L")).astype(np.float32)
    crop = img[y0:y0 + h, x0:x0 + w]
    rgb = np.kron(np.stack([crop] * 3, -1), np.ones((f, f, 1))).astype(np.float32)
    if abdunkeln is not None:
        ax, ay, bx, by = abdunkeln
        m = np.ones((h, w), bool)
        m[max(ay - y0, 0):max(by - y0, 0), max(ax - x0, 0):max(bx - x0, 0)] = False
        mf = np.kron(m, np.ones((f, f))).astype(bool)
        rgb[mf] *= 0.55
    return rgb


def _rand(lab):
    r = np.zeros(lab.shape, bool)
    r[:, 1:] |= lab[:, 1:] != lab[:, :-1]
    r[1:, :] |= lab[1:, :] != lab[:-1, :]
    return r


def _rahmen(d, x0, y0, f, viertel_box):
    ax, ay, bx, by = 64, 64, 564, 564
    d.rectangle([(ax - x0) * f, (ay - y0) * f, (bx - x0) * f - 1, (by - y0) * f - 1], outline=(255, 255, 255), width=1)
    ax, ay, bx, by = viertel_box
    d.rectangle([(ax - x0) * f, (ay - y0) * f, (bx - x0) * f - 1, (by - y0) * f - 1], outline=(0, 255, 255), width=2)


def bilder(ordner, viertel_box, segmente, punkte_liste, titel):
    karte, seg = wz.laden(None, leise=True)
    ax, ay, bx, by = viertel_box
    x0, y0 = max(ax - 32, 0), max(ay - 32, 0)
    x1, y1 = min(bx + 32, karte.shape[1]), min(by + 32, karte.shape[0])
    w, h, f = x1 - x0, y1 - y0, 3
    lab = karte[y0:y1, x0:x1]
    labf = np.kron(lab, np.ones((f, f), np.uint32))
    rnd = _rand(labf)
    fn = wz.font(13)
    fk = wz.font(12)
    eigene = {s["id"]: s for s in segmente}
    # roh
    rgb = _grund(karte, x0, y0, w, h, f)
    im = Image.fromarray(rgb.clip(0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    _rahmen(d, x0, y0, f, viertel_box)
    d.text((6, 6), f"{titel}: unverändertes Bild", fill=(255, 255, 0), font=fn, stroke_width=2, stroke_fill=(0, 0, 0))
    im.save(Path(ordner) / "roh.jpg", quality=90)
    # umriss
    rgb = _grund(karte, x0, y0, w, h, f, abdunkeln=viertel_box)
    rgb[rnd] = (255, 230, 0)
    im = Image.fromarray(rgb.clip(0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    _rahmen(d, x0, y0, f, viertel_box)
    for sid in np.unique(lab):
        m = lab == sid
        dist = ndimage.distance_transform_edt(np.pad(m, 1))[1:-1, 1:-1]
        yy, xx = np.unravel_index(np.argmax(dist), dist.shape)
        col = (255, 255, 255) if int(sid) in eigene else (170, 170, 170)
        d.text((xx * f + 1, yy * f + 1), str(int(sid) % 100000), fill=col, font=fk, anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0))
    d.text((6, 6), f"{titel}: Grenzen nach dem Nachsegmentieren, Nummer = ID mod 100000 (weiß: dieses Viertel)",
           fill=(255, 255, 0), font=fn, stroke_width=2, stroke_fill=(0, 0, 0))
    im.save(Path(ordner) / "umriss.jpg", quality=90)
    # vorschlag
    rgb = _grund(karte, x0, y0, w, h, f)
    farbe = np.zeros(lab.shape + (3,), np.float32)
    hat = np.zeros(lab.shape, bool)
    for sid, s in eigene.items():
        m = lab == sid
        if m.any():
            farbe[m] = FARBE[s["klasse_frei"]["grob"]]
            hat |= m
    ff = np.kron(farbe, np.ones((f, f, 1)))
    hf = np.kron(hat, np.ones((f, f))).astype(bool)
    rgb[hf] = rgb[hf] * 0.55 + ff[hf] * 0.45
    rgb[rnd] = (255, 255, 255)
    im = Image.fromarray(rgb.clip(0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    _rahmen(d, x0, y0, f, viertel_box)
    for sid, s in eigene.items():
        m = lab == sid
        if not m.any():
            continue
        dist = ndimage.distance_transform_edt(np.pad(m, 1))[1:-1, 1:-1]
        yy, xx = np.unravel_index(np.argmax(dist), dist.shape)
        t = str(sid % 100000) + ("?" if not s["sicher"] else "")
        d.text((xx * f + 1, yy * f + 1), t, fill=(255, 255, 255), font=fk, anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0))
    # Legende
    leg = Image.new("RGB", (im.width, 26 + 18 * 3), (20, 20, 20))
    dl = ImageDraw.Draw(leg)
    dl.text((6, 4), f"{titel}: Grenzen nach Nachsegmentieren, Farbe = Oberklasse (frei), ? = sicher: false",
            fill=(255, 255, 255), font=fn)
    xx = 6
    for name, c in FARBE.items():
        dl.rectangle([xx, 26, xx + 14, 40], fill=c)
        dl.text((xx + 18, 26), name, fill=(255, 255, 255), font=fn)
        xx += 150
    ges = Image.new("RGB", (im.width, im.height + leg.height))
    ges.paste(im, (0, 0))
    ges.paste(leg, (0, im.height))
    ges.save(Path(ordner) / "vorschlag.jpg", quality=90)
    # maengel
    rgb = _grund(karte, x0, y0, w, h, f, abdunkeln=viertel_box)
    rgb[rnd] = rgb[rnd] * 0.4 + np.array([255, 230, 0]) * 0.6
    im = Image.fromarray(rgb.clip(0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    _rahmen(d, x0, y0, f, viertel_box)
    zeilen = []
    for nr, sid, text in punkte_liste:
        mt = re.search(r"\((\d+)/(\d+)\)", text)
        if mt:
            px, py = int(mt.group(1)), int(mt.group(2))
            cx, cy = (px - x0) * f + 1, (py - y0) * f + 1
            if 0 <= cx < im.width and 0 <= cy < im.height:
                d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(220, 0, 0), outline=(255, 255, 255))
                d.text((cx, cy), str(nr), fill=(255, 255, 255), font=wz.font(11), anchor="mm")
        zeilen.append(f"{nr}: {sid % 100000} – {text[:110]}")
    if not zeilen:
        zeilen = ["keine Mängel"]
    zh = 16
    leg = Image.new("RGB", (im.width, 8 + zh * len(zeilen)), (20, 20, 20))
    dl = ImageDraw.Draw(leg)
    for i, z in enumerate(zeilen):
        dl.text((6, 4 + i * zh), z, fill=(255, 255, 255), font=wz.font(11))
    ges = Image.new("RGB", (im.width, im.height + leg.height))
    ges.paste(im, (0, 0))
    ges.paste(leg, (0, im.height))
    if ges.height > 2000:
        fakt = 2000 / ges.height
        ges = ges.resize((int(ges.width * fakt), 2000))
    ges.save(Path(ordner) / "maengel.jpg", quality=90)


def schreiben(viertel, ordner, box, eintraege, eingriffe, uebersicht, nah, naht, unsicher, nicht_geprueft, offen):
    """eintraege: Liste (id, klasse_heute, key, sicher, urteil, was, punkte[(art, text, flaeche)], bilder[...])"""
    segmente = []
    punkte_liste = []
    nr = 0
    for (sid, kh, key, sicher, urteil, was, punkte, bilder_) in eintraege:
        g, m, f = K[key]
        pl = []
        for art, text, fl in punkte:
            nr += 1
            pl.append({"nr": nr, "art": art, "text": text, "flaeche_px": fl})
            punkte_liste.append((nr, sid, text))
        segmente.append({"id": sid, "klasse_heute": kh, "was_ist_es": was, "urteil": urteil,
                         "klasse_vorschlag": None, "klasse_frei": {"grob": g, "mittel": m, "fein": f},
                         "sicher": sicher, "punkte": pl, "bilder": bilder_})
    urteil = {"teilkachel": "r1c1", "viertel": viertel, "bearbeiter": f"urt-b-r1c1-{viertel}",
              "bilder_angesehen": {"uebersicht": uebersicht, "nah": nah},
              "segmente": segmente, "naht": naht, "unsicher": unsicher,
              "nicht_geprueft": nicht_geprueft, "offen": offen, "eingriffe": eingriffe,
              "klassen_frei": klassen_frei(segmente)}
    Path(ordner, "urteil.json").write_text(json.dumps(urteil, ensure_ascii=False, indent=1), encoding="utf-8")
    bilder(ordner, box, segmente, punkte_liste, f"r1c1 {viertel}")
    print("geschrieben", len(segmente), "Segmente,", nr, "Punkte,",
          sum(1 for s in segmente if not s["sicher"]), "unsicher,",
          sum(1 for s in segmente if s["urteil"] == "nicht_sauber"), "nicht sauber")


def eingriffe_aus_ergebnis(stapel_pfad, ergebnis_pfad, gruende):
    """Je Stapelschritt ein Eintrag {schritt, vorher, nachher, grund}; gruende: Funktion(schritt, erg) -> Text."""
    schritte = json.loads(Path(stapel_pfad).read_text(encoding="utf-8"))["schritte"]
    erg = []
    for z in Path(ergebnis_pfad).read_text(encoding="utf-8").splitlines():
        mt = re.match(r"(\d+)\. (\w+): (\{.*\})$", z)
        if mt:
            erg.append(json.loads(mt.group(3)))
    aus = []
    for s, e in zip(schritte, erg):
        if s["op"] == "teilen":
            vorher, nachher = [s["id"]], [s["id"]] + e["neu"]
        elif s["op"] == "verschmelzen":
            vorher, nachher = list(s["ids"]), [e["ziel"]]
        else:
            vorher = [i for i in [s.get("id")] if i] or []
            if not vorher:
                vorher = gruende("quelle", s, e)
            vorher = vorher + [i for i in e.get("entfernt", []) if i not in vorher]
            nachher = [e["ziel"]] + e.get("aufgeteilt_neu", [])
            if not vorher:
                vorher = gruende("quelle", s, e)
        aus.append({"schritt": s["op"], "vorher": vorher, "nachher": nachher, "grund": gruende("grund", s, e)})
    return aus
