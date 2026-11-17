"""Teil 3 von landseg-test-t0: Kategorienlisten kategorien-b.json und kategorien-c.json im Format von
kategorien.json, dazu der Stand von Fassung C mit vereinheitlichten Codes und T0-weit eindeutigen IDs.

Aufruf: PY -I listen.py   (schreibt nur unter daten/landseg/T0/fassung-b/ und fassung-c/)
"""
import colorsys, importlib.util, json, math, shutil, sys
from collections import Counter
from pathlib import Path

import numpy as np
import tifffile

sys.stdout.reconfigure(encoding="utf-8")
BASIS = Path("C:/Users/Phil/Developement/Victor")
T0 = BASIS / "daten/landseg/T0"
REPO = BASIS / "landseg"
spec = importlib.util.spec_from_file_location("pk", REPO / "tools/pruefe_kategorien.py")
pk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pk)

MAPPINGS_LEER = {k: [] for k in pk.MAPPING_KEYS}
STATUS = {
    "bw": "nicht beurteilt: freie Liste einer Vergleichsfassung; die SW-Spalte steht überall auf 'eing.' als Platzhalter und ist ungeprüft.",
    "mappings": "keine Zuordnungen: freie Liste, gegen CORINE, CLC+, FLAIR, DKM und Bericht 48 nicht abgebildet (Listen leer); die Regel bericht48 ist eine Näherung des Umsetzers.",
    "colors": "B: Farben der Vereinheitlichung; C: vom Umsetzer je Ebene-1-Klasse eine Farbfamilie, Mindestabstand prüft tools/pruefe_kategorien.py",
}


def lies(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def schreib(p, daten):
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(daten, f, ensure_ascii=False, indent=1)
        f.write("\n")


def zaehlen(klassen, regeln):
    eltern = {k["parent"] for k in klassen}
    return {"level_1": sum(k["level"] == 1 for k in klassen), "level_2": sum(k["level"] == 2 for k in klassen),
            "leaves": sum(k["code"] not in eltern for k in klassen),
            "rules_g": sum(r["id"].startswith("G") for r in regeln), "rules_u": sum(r["id"].startswith("U") for r in regeln)}


def liste(titel, quelle, klassen, regeln):
    for k in klassen:
        k.setdefault("bw", "eing.")
        k.setdefault("mappings", dict(MAPPINGS_LEER))
    return {"schema": "landseg-kategorien/1", "title": titel, "date": "2026-11-17", "source": quelle,
            "counts": zaehlen(klassen, regeln), "status": STATUS, "bw_values": {"ja": "erkennbar", "eing.": "eingeschränkt", "nein": "nicht erkennbar"},
            "classes": klassen, "rules": regeln}


# ---------------------------------------------------------------- Fassung B
def baue_b():
    e = lies(T0 / "fassung-b/vereinheitlichung/kategorien-b-entwurf.json")
    klassen = [dict(k) for k in e["classes"]]
    regeln = [
        {"id": "G1", "kind": "grundsatz", "title": "Lückenlos",
         "text": "Jeder Bildpunkt gehört zu genau einem Segment mit genau einer Klasse dieser Liste. Für eine Auswertung nach Bericht 48 zählen Segmente der Klassen unter bericht48.im_siedlung_klassen mit im_siedlung: ja zur Klasse bericht48.im_siedlung_ziel (Näherung, ungeprüft).",
         "source": "wuensche/entscheidungen.md 2026-11-17 (Grundsätze F2, drei Fassungen)",
         "bericht48": {"im_siedlung_klassen": ["2.2", "3.3"], "im_siedlung_ziel": "4"}},
        {"id": "G2", "kind": "grundsatz", "title": "Freie Benennung, gleiche Arbeitsregeln",
         "text": "Die Klassen haben die Agents von Fassung B je Viertel selbst benannt und gestuft (grob/mittel/fein); ein Agent hat die 16 Listen über ganz T0 zu dieser Liste vereinheitlicht. Gearbeitet wurde nach den Regeln L1 bis L12 des Skills landseg-agent wie in Fassung A.",
         "source": "daten/landseg/T0/fassung-b/vereinheitlichung/vereinheitlichung.md"},
    ]
    d = liste(e.get("title") or "Fassung B", "daten/landseg/T0/fassung-b/vereinheitlichung/kategorien-b-entwurf.json (Vereinheitlichung der freien Viertel-Klassen)", klassen, regeln)
    schreib(T0 / "fassung-b/kategorien-b.json", d)
    print("B:", d["counts"])


# ---------------------------------------------------------------- Fassung C
C_KLASSEN = [  # code, name, Merkmal
    ("0", "Schatten / nicht bestimmbar", "dunkle Fläche ohne erkennbaren Untergrund"),
    ("0.1", "Schlagschatten", "dunkler Streifen neben Gebäude, Hecke oder Baum"),
    ("0.1.1", "Schlagschatten von Gebäude", "dunkler Streifen an der Schattenseite eines Hauses"),
    ("0.1.2", "Schlagschatten von Gehölz", "dunkler Streifen neben Baum oder Hecke"),
    ("1", "Gebäude und bauliche Anlagen", "Dächer und Bauwerke mit geraden Kanten"),
    ("1.1", "Gebäude", "Dachfläche mit geraden Kanten"),
    ("1.1.1", "Wohnhaus (Hauptgebäude)", "größeres Dach, Kamine, Gauben"),
    ("1.1.2", "Nebengebäude / Anbau / Schuppen", "kleines Dach neben dem Haus, Garage, Schuppen"),
    ("1.1.3", "Gartenhaus / Laube", "kleines Dach im Garten oder Kleingarten"),
    ("1.1.4", "Gewächshaus / Glas- oder Foliendach", "helles, spiegelndes Dach"),
    ("1.2", "Bauliche Anlagen und Objekte", "kleine Bauwerke und Gegenstände"),
    ("1.2.1", "Schwimmbecken", "türkise oder blaue Fläche mit Rand"),
    ("1.2.2", "Mauer / Stützmauer / Einfassung", "schmale gerade Linie, oft mit Schatten"),
    ("1.2.3", "Kleinobjekt", "Fahrzeug, Möbel, Plane, Schirm, Gartenausstattung"),
    ("1.2.4", "Holzhaufen / Schnittgut", "Haufen aus Holz oder Grünschnitt"),
    ("2", "Wege und befestigte Flächen", "glatte graue oder beige Flächen"),
    ("2.1", "Befestigt", "Asphalt, Beton, Pflaster, Schotter"),
    ("2.1.1", "Straße / Fahrweg", "breites graues Band"),
    ("2.1.2", "Hof / Zufahrt / Terrasse / Vorplatz", "befestigte Fläche am Haus"),
    ("2.1.3", "Gartenweg / Stufen / Platten", "schmaler befestigter Weg im Garten"),
    ("2.2", "Unbefestigt", "Erd- oder Graswege"),
    ("2.2.1", "Wiesenweg", "begrünter Weg, Fahrspuren im Gras"),
    ("2.2.2", "Trampelpfad / Erdweg", "schmale helle Spur"),
    ("3", "Garten / Siedlungsgrün", "Gartenflächen in der Siedlung"),
    ("3.1", "Gartenrasen", "gleichmäßig kurzes Grün im Garten"),
    ("3.2", "Gemischte Gartenfläche", "Mosaik aus Rasen, Beeten und Sträuchern"),
    ("3.3", "Gemüse- und Nutzbeete", "Reihen, offener Boden im Garten"),
    ("4", "Krautige Vegetation", "Wiese, Saum und Krautflur"),
    ("4.1", "Wiese / Grünland", "Grasfläche außerhalb der Gärten"),
    ("4.1.1", "Wiese ungemäht / langgrasig", "Halmstruktur, Altgras, Kräuter"),
    ("4.1.2", "Wiese niedrig", "gleichmäßig kurze Wiese"),
    ("4.2", "Saum / Feldrain / Böschung", "schmaler Grasstreifen am Rand"),
    ("4.3", "Verbuschte Wiese / Lichtung", "Krautflur mit Gebüsch oder im Gehölz"),
    ("5", "Feld und offener Boden", "Acker und vegetationsarme Flächen"),
    ("5.1", "Feld gemäht / abgeerntet", "beige Fläche mit Schwaden oder Stoppeln"),
    ("5.2", "Offener Boden / vegetationsarm", "Erde, Sand, Trockengras, lückiger Bewuchs"),
    ("6", "Gehölz", "Kronen mit Textur und Schatten"),
    ("6.1", "Wald / geschlossener Bestand", "geschlossenes Kronendach"),
    ("6.1.1", "Kronendach besonnt", "helles Kronendach"),
    ("6.1.2", "Kronendach beschattet", "dunkler Bestand"),
    ("6.2", "Baumgruppe / Feldgehölz", "mehrere zusammenhängende Kronen"),
    ("6.3", "Einzelbaum", "eine abgrenzbare Krone"),
    ("6.3.1", "Laubbaum", "runde Laubkrone"),
    ("6.3.2", "Laubbaum rotlaubig", "rotbraune Krone"),
    ("6.3.3", "Nadelbaum / Konifere", "spitze, dunkle Krone"),
    ("6.4", "Hecke / Gehölzstreifen", "lineares Gehölz, geschnitten oder frei"),
    ("6.5", "Strauch / Gebüsch", "kleine Kronen, Gartengehölz"),
]
# je Teilkachel: Code der eigenen Liste -> Code der vereinheitlichten Liste
C_ABB = {
    "r0c0": {"1": "1", "1.1": "1.1", "1.1.1": "1.1.1", "1.1.2": "1.1.2", "1.2": "2.1", "1.2.1": "2.1.1", "1.2.2": "2.1.2",
             "1.2.3": "2.1.3", "1.3": "1.2", "1.3.1": "1.2.1", "1.3.2": "1.2.2", "2": "3", "2.1": "3.1", "2.2": "3.2",
             "2.3": "6.4", "2.4": "6.5", "2.5": "1.2.3", "3": "4", "3.1": "4.1", "3.1.1": "4.1.1", "3.1.2": "4.1.2",
             "3.1.3": "4.2", "3.2": "5.1", "3.3": "4.3", "4": "6", "4.1": "6.3", "4.1.1": "6.3.1", "4.2": "6.2",
             "4.2.1": "6.2", "4.3": "6.5", "5": "0", "5.1": "1.2.4", "5.2": "0.1"},
    "r0c1": {"1": "1", "1.1": "1.1", "1.1.1": "1.1.1", "1.1.2": "1.1.2", "1.2": "2.1", "1.2.1": "2.1.1", "1.2.2": "2.1.2",
             "1.2.3": "2.1.3", "1.3": "1.2", "1.3.1": "1.2.1", "1.3.2": "1.2.3", "2": "5", "2.1": "5.1", "2.2": "4.2",
             "3": "4", "3.1": "3.1", "3.2": "4.1.1", "3.3": "5.2", "4": "6", "4.1": "6.3", "4.1.1": "6.3.1",
             "4.1.2": "6.3.2", "4.1.3": "6.3.3", "4.2": "6.2", "4.3": "6.5", "4.4": "3.2", "5": "0", "5.1": "0.1.1",
             "5.2": "0.1.2"},
    "r1c0": {"1": "6", "1.1": "6.1", "1.1.1": "6.1.1", "1.1.2": "6.1.2", "1.1.3": "6.1", "1.2": "6.3", "1.3": "6.2",
             "1.4": "6.5", "2": "4", "2.1": "4.1", "2.2": "4.3", "2.3": "4.2", "3": "5", "3.1": "5.2", "3.2": "5.1",
             "4": "2", "4.1": "2.2.2", "5": "3", "5.1": "1", "5.2": "3.2"},
    "r1c1": {"1": "1", "1.1": "1.1", "1.1.1": "1.1.3", "1.1.2": "1.1.2", "1.1.3": "1.1.4", "1.2": "1.2", "1.2.1": "1.2.1",
             "1.2.2": "1.2.2", "1.2.3": "1.2.3", "2": "2", "2.1": "2.1", "2.1.1": "2.1.1", "2.1.2": "2.1.3",
             "2.1.3": "2.1.2", "2.2": "2.2", "2.2.1": "2.2.1", "2.2.2": "2.2.2", "3": "5", "3.1": "5.1", "4": "4",
             "4.1": "4.1.1", "4.2": "3.1", "4.3": "4.2", "5": "3", "5.1": "3.3", "5.2": "3.2", "6": "6", "6.1": "6.1",
             "6.2": "6.2", "6.3": "6.3", "6.4": "6.4", "6.5": "6.5", "6.6": "1.2.4", "7": "0", "7.1": "0.1"},
}
FAMILIE = {"0": (0, 0.0), "1": (0, 0.75), "2": (28, 0.55), "3": (300, 0.55), "4": (95, 0.6), "5": (48, 0.75), "6": (135, 0.6)}


def farben(codes):
    gewaehlt = {}
    for code in codes:
        h0, s0 = FAMILIE[code.split(".")[0]]
        kand = []
        for dh in range(-30, 31, 5):
            for l in [x / 100 for x in range(22, 86, 4)]:
                for s in ([0.0] if s0 == 0 else [s0 - 0.2, s0, min(1, s0 + 0.2)]):
                    r, g, b = colorsys.hls_to_rgb(((h0 + dh) % 360) / 360, l, max(0, s))
                    kand.append("#%02x%02x%02x" % (round(r * 255), round(g * 255), round(b * 255)))
        best, best_d = None, -1
        for c in kand:
            lab = pk.to_lab(c)
            d = min((math.dist(lab, pk.to_lab(x)) for x in gewaehlt.values()), default=99)
            if d > best_d:
                best, best_d = c, d
        gewaehlt[code] = best
    return gewaehlt


def baue_c():
    codes = [k[0] for k in C_KLASSEN]
    col = farben(codes)
    klassen = []
    for code, name, merkmal in C_KLASSEN:
        teile = code.split(".")
        klassen.append({"code": code, "name": name, "parent": ".".join(teile[:-1]) or None, "level": len(teile),
                        "color": col[code], "image_cue": merkmal})
    regeln = [
        {"id": "G1", "kind": "grundsatz", "title": "Lückenlos",
         "text": "Jeder Bildpunkt gehört zu genau einem Segment mit genau einer Klasse dieser Liste. Für eine Auswertung nach Bericht 48 zählen Segmente unter bericht48.im_siedlung_klassen mit im_siedlung: ja zu bericht48.im_siedlung_ziel (Näherung, ungeprüft).",
         "source": "wuensche/entscheidungen.md 2026-11-17 (drei Fassungen, lückenlos in allen dreien)",
         "bericht48": {"im_siedlung_klassen": ["3"], "im_siedlung_ziel": "1"}},
        {"id": "G2", "kind": "grundsatz", "title": "Freie Arbeitsweise, Liste nachträglich vereinheitlicht",
         "text": "Jede Teilkachel hat ein Agent frei bearbeitet (eigene Kategorien, eigene Arbeitsweise, Beschreibung in abgabe/<teilkachel>/arbeitsweise.md). Die vier eigenen Listen hat der Umsetzer von Teil 3 nach Namen und Merkmalen zu dieser Liste zusammengelegt; der ursprüngliche Code steht je Segment unter klasse_teil.",
         "source": "daten/landseg/T0/fassung-c/abgabe/<teilkachel>/kategorien-teil.json"},
    ]
    d = liste("Gestufte Kategorienliste T0, Fassung C (aus den vier freien Listen der Teilkacheln zusammengelegt)",
              "daten/landseg/T0/fassung-c/abgabe/*/kategorien-teil.json", klassen, regeln)
    d["abbildung_teilkacheln"] = C_ABB
    schreib(T0 / "fassung-c/kategorien-c.json", d)
    print("C:", d["counts"])

    manifest = lies(T0 / "fassung-c/manifest.json")
    einheiten = []
    for nr, t in enumerate(manifest["teilkacheln"]):
        tk = t["id"]
        ab = T0 / "fassung-c/abgabe" / tk
        karte = tifffile.imread(ab / "labels.tif").astype(np.uint32)
        seg = lies(ab / "segmente.json")
        teil = {c["code"]: c["name"] for c in lies(ab / "kategorien-teil.json")["classes"]}
        versatz = 0 if karte.min() >= 100000 else (nr + 1) * 100000
        if karte.max() >= 100000 and versatz:
            raise SystemExit(f"{tk}: IDs teils über 100000, Versatz nicht eindeutig")
        neu, fehlt = [], Counter()
        for s in seg["segmente"]:
            e = dict(s)
            e["id_abgabe"] = s["id"]
            e["id"] = s["id"] + versatz
            e["klasse_teil"] = s["klasse"]
            e["klasse_teil_name"] = teil.get(s["klasse"])
            if s["klasse"] not in C_ABB[tk]:
                fehlt[s["klasse"]] += 1
            e["klasse"] = C_ABB[tk].get(s["klasse"], s["klasse"])
            e["grob"] = e["klasse"].split(".")[0]
            e["sicher"] = "ja" if s.get("sicher") in (True, "ja") else "nein"
            neu.append(e)
        if fehlt:
            raise SystemExit(f"{tk}: Codes ohne Abbildung {dict(fehlt)}")
        ziel = T0 / "fassung-c/stand" / tk
        ziel.mkdir(parents=True, exist_ok=True)
        tifffile.imwrite(ziel / "labels.tif", (karte + np.uint32(versatz)).astype(np.uint32), compression="zlib")
        schreib(ziel / "segmente.json", {**{k: v for k, v in seg.items() if k != "segmente"}, "fassung": "C",
                                         "stand": f"Abgabe C {tk}, Codes nach kategorien-c.json, ID + {versatz}",
                                         "segmente": neu})
        einheiten.append({"teilkachel": tk, "labels": f"stand/{tk}/labels.tif", "segmente": f"stand/{tk}/segmente.json",
                          "runde": 0, "name": f"c-{tk}"})
        print(f"C {tk}: {len(neu)} Segmente, Versatz {versatz}, im Kern {sum(1 for s in neu if s.get('im_kern'))}")
    schreib(T0 / "fassung-c/zusammentragen.json", {"schema": "landseg-zusammentragen/1", "manifest": "manifest.json",
                                                    "einheiten": einheiten, "ziel": "zusammen"})


if __name__ == "__main__":
    baue_b()
    baue_c()
