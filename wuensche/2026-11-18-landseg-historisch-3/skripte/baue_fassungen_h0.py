"""H0: Stand der drei Fassungen wie in der T0-Übergabe aufbauen (Karten mit Klassen aus den Urteilen,
Kategorienlisten, zusammentragen.json).

Benennung wie heute: A = „Alles frei“ (a-alles-frei, freie Abgabe je Teilkachel unter abgabe/<tk>/),
B = „Kategorien frei“ (b-kategorien-frei), C = „Feste Kategorienliste“ (c-feste-liste).

- B und C: Karte = die Label-Karte in <ordner>/<tk>/labels.tif, auf der die Urteils-Agents schon
  nachsegmentiert haben (bleibt bildpunktgleich); segmente.json bekommt die Klasse aus dem Urteil
  (C: klasse_vorschlag, sonst klasse_heute; B: Code aus vereinheitlichung/codes.json), sicher aus dem
  Urteil. Kontextrand: Mehrheit der Klasse im Kern der Nachbarkachel, außerhalb H0 Vorstufe (C) bzw.
  „0 Nicht bestimmbar“ (B), immer sicher: nein. Die ursprüngliche segmente.json wird einmal unter
  <Berichtsordner>/sicherung/ abgelegt; jeder Lauf baut von dieser Sicherung aus (wiederholbar).
- A: Karte der freien Abgabe (abgabe/<tk>/), IDs + (Nummer der Teilkachel + 1) · 100000, Codes der
  eigenen Listen nach kategorien-a.json abgebildet (klasse_teil hält den Code der Abgabe).
- Die Gegenprobe (c-feste-liste/gegenprobe/, urteil-gegenprobe/, a-alles-frei/abgabe-gegenprobe/)
  geht in keine Karte ein.

Aufruf: PY -B baue_fassungen_h0.py
Schreibt nur unter daten/landseg/H0/<fassung>/ und im Berichtsordner.
"""
import colorsys
import importlib.util
import json
import math
import shutil
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import tifffile

sys.stdout.reconfigure(encoding="utf-8")
BASIS = Path("C:/Users/Phil/Developement/Victor")
H0 = BASIS / "daten/landseg/H0"
D = BASIS / "wuensche/2026-11-18-landseg-historisch-3"
REPO = BASIS / "landseg"
SICHERUNG = D / "sicherung"
BEARBEITER = "h0-fassungen"
ORDNER = {"A": H0 / "a-alles-frei", "B": H0 / "b-kategorien-frei", "C": H0 / "c-feste-liste"}
JETZT = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

spec = importlib.util.spec_from_file_location("pk", REPO / "tools/pruefe_kategorien.py")
pk = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pk)


def lies(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def schreib(p, daten):
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(daten, f, ensure_ascii=False, indent=1)
        f.write("\n")


def ja_nein(wert):
    if isinstance(wert, bool):
        return "ja" if wert else "nein"
    return "ja" if str(wert).lower() in ("ja", "true") else "nein"


def grob(code):
    return code.split(".")[0]


def kern(karte, t):
    k = t["kern_im_bild"]
    return karte[k["y"]:k["y"] + k["hoehe"], k["x"]:k["x"] + k["breite"]]


# ------------------------------------------------------------------ Kategorienlisten
MAPPINGS_LEER = {k: [] for k in pk.MAPPING_KEYS}
STATUS_A = {
    "bw": "nicht beurteilt: freie Liste einer Vergleichsfassung; die SW-Spalte steht überall auf 'eing.' als Platzhalter und ist ungeprüft.",
    "mappings": "keine Zuordnungen: freie Liste, gegen CORINE, CLC+, FLAIR, DKM und Bericht 48 nicht abgebildet (Listen leer); die Regel bericht48 ist eine Näherung des Umsetzers.",
    "colors": "vom Umsetzer je Ebene-1-Klasse eine Farbfamilie, Mindestabstand prüft tools/pruefe_kategorien.py",
}

A_KLASSEN = [  # code, name, Merkmal (Schwarz-Weiß-Scan 1968)
    ("0", "Nicht bestimmbar", "Fläche, deren Untergrund im Scan nicht zu sehen oder nicht zu deuten ist"),
    ("0.1", "Schatten (Untergrund nicht erkennbar)", "sehr dunkles Band oder Fleck neben Gebäude oder Gehölz"),
    ("0.2", "Sehr dunkle Fläche unklar", "dunkler Fleck: Baumkrone, dunkles Dach oder Schatten"),
    ("0.3", "Kleinobjekt unklar", "kleiner heller Fleck: Schuppen, Haufen, Fahrzeug"),
    ("1", "Gebäude und Hofstellen", "Dächer und Bauwerke mit geraden Kanten"),
    ("1.1", "Gebäude", "Dachfläche mit geraden Kanten"),
    ("1.1.1", "Hauptgebäude / Längsbau (Streckhof)", "langer heller Dachstreifen an der Straße"),
    ("1.1.2", "Nebengebäude / Schuppen / Querbau", "kleineres Dach am Grundstücksende oder quer"),
    ("1.1.3", "Großbau / Halle", "großes zusammenhängendes Dach"),
    ("1.1.4", "Dachfläche im Eigenschatten", "dunkle Dachseite mit geraden Kanten"),
    ("1.2", "Hofstelle ungetrennt (Dach oder Hof)", "Streifen aus Dach und Hof, im Scan nicht getrennt"),
    ("1.3", "Mauer / Einfriedung", "schmale gerade Linie, oft mit Schatten"),
    ("2", "Hof und Garten", "unbebaute Flächen im Grundstück"),
    ("2.1", "Hof- und Freifläche im Grundstück", "helle offene Fläche an den Gebäuden, auch Lagerfläche"),
    ("2.2", "Garten / Grün im Ort", "fleckige oder feinkörnige Fläche hinter den Höfen"),
    ("2.3", "Gartenland mit Reihen", "Beete oder Rebzeilen in Reihen"),
    ("3", "Verkehrsfläche", "glatte helle Bänder"),
    ("3.1", "Straße", "breites helles Band"),
    ("3.1.1", "Straße im Ort", "breite Fahrbahn zwischen den Höfen"),
    ("3.1.2", "Landstraße außerorts", "breite Fahrbahn zwischen den Feldern"),
    ("3.2", "Weg / Gasse", "schmaler Feld-, Hof-, Gras- oder Hintausweg"),
    ("3.3", "Straßenrand (Bankett, Gehweg, Vorplatz)", "schmaler Streifen an der Fahrbahn"),
    ("4", "Offene Fläche (nicht Acker)", "unbebaute Fläche ohne Bewirtschaftungsmuster"),
    ("4.1", "Anger / Dorfplatz", "offene Fläche im Ort, oft mit Fahrspuren"),
    ("4.2", "Brache / Ödland / Weide", "fleckige Fläche ohne Streifen am Ortsrand"),
    ("4.3", "Rain / Graben / Saum", "schmaler Streifen zwischen Feldern oder an Wegen"),
    ("5", "Landwirtschaftliche Fläche", "Acker oder Grünland, im Schwarz-Weiß nicht sicher getrennt"),
    ("5.1", "Feld / Acker (Streifenflur)", "gleichmäßiges Korn mit Längsstreifen"),
    ("5.1.1", "Feld, dunkler Bestand", "dunkle gleichmäßige Parzelle"),
    ("5.1.2", "Feld, mittelgrau", "mittelgraue gleichmäßige Parzelle"),
    ("5.1.3", "Feld, hell (offener Boden, Stoppel)", "helle gleichmäßige Parzelle"),
    ("6", "Gehölz", "Kronen mit Textur und Schatten"),
    ("6.1", "Einzelbaum / Busch / Baumgruppe", "runde dunkle Krone mit Schatten"),
    ("6.2", "Baumreihe / Hecke", "Kette von Kronen entlang Straße, Weg oder Ortsrand"),
]
# je Teilkachel: Code der eigenen Liste -> Code von kategorien-a.json (nach Namen und Merkmal)
A_ABB = {
    "r0c0": {"1": "1", "1.1": "1.1", "1.1.1": "1.1.1", "1.1.2": "1.1.2", "1.2": "2.1", "1.3": "1.2", "1.4": "2.2",
             "1.5": "1.3", "2": "3", "2.1": "3.1", "2.2": "3.2", "2.3": "3.3", "3": "5", "3.1": "5.1", "4": "6",
             "4.1": "6.1", "4.2": "6.2", "5": "4", "5.1": "4.1", "5.2": "4.2", "9": "0", "9.1": "0.1", "9.2": "0.2",
             "9.3": "0.3"},
    "r0c1": {"1": "1", "1.1": "1.1", "1.1.1": "1.1.1", "1.1.2": "1.1.2", "1.1.3": "1.1.3", "1.2": "3", "1.2.1": "3.1",
             "1.2.2": "3.2", "1.3": "2.1", "2": "2.2", "2.1": "2.2", "2.2": "6", "2.2.1": "6.1", "2.3": "4.1",
             "2.4": "2.3", "9": "0", "9.1": "0.1"},
    "r1c0": {"1": "3", "1.1": "3.1", "1.2": "3.2", "2": "1", "2.1": "1.1", "2.2": "2.1", "3": "5", "3.1": "5.1",
             "3.1.1": "5.1.1", "3.1.2": "5.1.2", "3.1.3": "5.1.3", "3.2": "4.2", "4": "6", "4.1": "6.1", "4.2": "4.3",
             "5": "0", "5.1": "0.2", "5.2": "0.3"},
    "r1c1": {"1": "1", "1.1": "1.1", "1.1.1": "1.1", "1.1.2": "1.1.4", "1.2": "2.1", "1.3": "2.2", "2": "3",
             "2.1": "3.1.1", "2.2": "3.1.2", "2.3": "3.2", "3": "5", "3.1": "5.1", "4": "6", "4.1": "6.2", "5": "0.1"},
}
FAMILIE = {"0": (0, 0.0), "1": (0, 0.75), "2": (300, 0.55), "3": (28, 0.55), "4": (75, 0.6), "5": (48, 0.75),
           "6": (135, 0.6)}


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


def zaehlen(klassen, regeln):
    eltern = {k["parent"] for k in klassen}
    return {"level_1": sum(k["level"] == 1 for k in klassen), "level_2": sum(k["level"] == 2 for k in klassen),
            "leaves": sum(k["code"] not in eltern for k in klassen),
            "rules_g": sum(r["id"].startswith("G") for r in regeln),
            "rules_u": sum(r["id"].startswith("U") for r in regeln)}


def baue_a_liste():
    col = farben([k[0] for k in A_KLASSEN])
    klassen = []
    for code, name, merkmal in A_KLASSEN:
        teile = code.split(".")
        klassen.append({"code": code, "name": name, "parent": ".".join(teile[:-1]) or None, "level": len(teile),
                        "color": col[code], "image_cue": merkmal, "bw": "eing.", "mappings": dict(MAPPINGS_LEER)})
    regeln = [
        {"id": "G1", "kind": "grundsatz", "title": "Lückenlos",
         "text": "Jeder Bildpunkt gehört zu genau einem Segment mit genau einer Klasse dieser Liste. Für eine Auswertung nach Bericht 48 zählen Segmente unter bericht48.im_siedlung_klassen mit im_siedlung: ja zu bericht48.im_siedlung_ziel (Näherung, ungeprüft).",
         "source": "wuensche/entscheidungen.md 2026-11-17 (drei Fassungen, lückenlos in allen dreien)",
         "bericht48": {"im_siedlung_klassen": ["2"], "im_siedlung_ziel": "1"}},
        {"id": "G2", "kind": "grundsatz", "title": "Freie Arbeitsweise, Liste nachträglich vereinheitlicht",
         "text": "Jede Teilkachel hat ein Agent frei bearbeitet (eigene Kategorien, eigene Arbeitsweise, Beschreibung in abgabe/<teilkachel>/arbeitsweise.md). Die vier eigenen Listen hat der Umsetzer nach Namen und Merkmalen zu dieser Liste zusammengelegt; der ursprüngliche Code steht je Segment unter klasse_teil, die Abbildung unter abbildung_teilkacheln.",
         "source": "a-alles-frei/abgabe/<teilkachel>/kategorien-teil.json"},
    ]
    d = {"schema": "landseg-kategorien/1",
         "title": "Gestufte Kategorienliste H0, Fassung A (aus den vier freien Listen der Teilkacheln zusammengelegt)",
         "date": JETZT[:10], "source": "a-alles-frei/abgabe/*/kategorien-teil.json",
         "counts": zaehlen(klassen, regeln), "status": STATUS_A,
         "bw_values": {"ja": "erkennbar", "eing.": "eingeschränkt", "nein": "nicht erkennbar"},
         "classes": klassen, "rules": regeln, "abbildung_teilkacheln": A_ABB}
    schreib(ORDNER["A"] / "kategorien-a.json", d)
    print("Liste A:", d["counts"])
    return {k["code"] for k in klassen}


def baue_b_liste():
    e = lies(ORDNER["B"] / "vereinheitlichung/kategorien-b-entwurf.json")
    d = dict(e)
    d["title"] = "Gestufte Kategorienliste H0, Fassung B (Vereinheitlichung der freien Viertel-Klassen)"
    d["source"] = list(e.get("source") or []) + [
        "b-kategorien-frei/vereinheitlichung/kategorien-b-entwurf.json (unverändert übernommen; nur Titel und Quelle ergänzt)"]
    for k in d["classes"]:
        k.setdefault("bw", "eing.")
        k.setdefault("mappings", dict(MAPPINGS_LEER))
    schreib(ORDNER["B"] / "kategorien-b.json", d)
    print("Liste B:", d.get("counts"))
    return {k["code"] for k in d["classes"]}


def baue_c_liste():
    shutil.copyfile(REPO / "kategorien.json", ORDNER["C"] / "kategorien-c.json")
    return {k["code"] for k in lies(REPO / "kategorien.json")["classes"]}


# ------------------------------------------------------------------ B und C
def sicherung(fa, tk):
    q = ORDNER[fa] / tk / "segmente.json"
    s = SICHERUNG / ORDNER[fa].name / tk / "segmente.json"
    if not s.exists():
        s.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(q, s)
    return lies(s)


def urteile(fa, tk):
    eintraege, eingriffe, info = {}, [], []
    for n in range(1, 5):
        v = f"v{n}"
        p = ORDNER[fa] / "urteil" / tk / v / "urteil.json"
        u = lies(p)
        for s in u["segmente"]:
            if s["id"] in eintraege:
                raise SystemExit(f"{fa} {tk}: Segment {s['id']} in zwei Vierteln")
            eintraege[s["id"]] = {**s, "viertel": v}
        eingriffe += [{**x, "viertel": v} for x in (u.get("eingriffe") or [])]
        info.append({"viertel": v, "bearbeiter": u.get("bearbeiter"), "segmente": len(u["segmente"]),
                     "eingriffe": len(u.get("eingriffe") or []),
                     "quelle": str(p.relative_to(ORDNER[fa])).replace("\\", "/")})
    return eintraege, eingriffe, info


def baue_bc(fa, codes_liste, manifest, befund):
    ordner = ORDNER[fa]
    codes_b = lies(ORDNER["B"] / "vereinheitlichung/codes.json")["segmente"] if fa == "B" else None
    stand, kernklasse = {}, {}
    bef = {}
    # 1. Kernsegmente: Klasse aus dem Urteil
    for t in manifest["teilkacheln"]:
        tk = t["id"]
        karte = tifffile.imread(ordner / tk / "labels.tif")
        seg = sicherung(fa, tk)
        kern_ids = {int(i) for i in np.unique(kern(karte, t))}
        alle_ids = {int(i) for i in np.unique(karte)}
        u, eingriffe, info = urteile(fa, tk)
        fehler = []
        fehlt = sorted(kern_ids - set(u))
        if fehlt:
            fehler.append(f"Kernsegmente ohne Urteil: {fehlt}")
        nicht_im_kern = sorted(set(u) - kern_ids)
        klassen = {}
        for i in kern_ids:
            e = u.get(i)
            if e is None:
                continue
            if fa == "C":
                k = e.get("klasse_vorschlag") or e.get("klasse_heute")
            else:
                c = codes_b.get(tk, {}).get(str(i))
                k = c["code"] if c else None
            if k not in codes_liste:
                fehler.append(f"Segment {i}: Klasse {k!r} nicht in der Liste")
            klassen[i] = k
        kernklasse[tk] = klassen
        stand[tk] = (karte, seg, t, u, kern_ids, alle_ids, eingriffe, info, fehler, nicht_im_kern)
    # 2. Klassenkarte von H0 aus den Kernurteilen (für den Kontextrand)
    h, w = manifest["ausschnitt"]["hoehe"], manifest["ausschnitt"]["breite"]
    sortiert = sorted(codes_liste)
    nummer = {c: n for n, c in enumerate(sortiert)}
    h0 = np.full((h, w), -1, np.int32)
    for t in manifest["teilkacheln"]:
        tk = t["id"]
        karte = stand[tk][0]
        kk = t["kern"]
        ks = kern(karte, t)
        lut = {i: nummer.get(c, -1) for i, c in kernklasse[tk].items()}
        werte = np.vectorize(lambda x: lut.get(int(x), -1), otypes=[np.int32])(ks)
        h0[kk["y"]:kk["y"] + kk["hoehe"], kk["x"]:kk["x"] + kk["breite"]] = werte
    # 3. segmente.json je Teilkachel
    for t in manifest["teilkacheln"]:
        tk = t["id"]
        karte, seg, t, u, kern_ids, alle_ids, eingriffe, info, fehler, nicht_im_kern = stand[tk]
        kx = t["kontext"]
        ys, xs = np.mgrid[0:karte.shape[0], 0:karte.shape[1]]
        ay, ax = ys + kx["y"], xs + kx["x"]
        innen = (ay >= 0) & (ay < h) & (ax >= 0) & (ax < w)
        klassen_h0 = np.full(karte.shape, -1, np.int32)
        klassen_h0[innen] = h0[ay[innen], ax[innen]]
        flaechen = Counter(karte.ravel().tolist())
        kflaechen = Counter(kern(karte, t).ravel().tolist())
        neu, n_kontext_nachbar, n_kontext_aussen, n_unsicher, n_sicher = [], 0, 0, 0, 0
        gesehen = set()
        for s in seg["segmente"]:
            i = s["id"]
            if i not in alle_ids:
                fehler.append(f"Segment {i} in segmente.json ohne Bildpunkte")
                continue
            gesehen.add(i)
            e2 = dict(s)
            e2["klasse_vorstufe"] = s.get("klasse")
            e2["sicher_vorstufe"] = s.get("sicher")
            e2["im_kern"] = i in kern_ids
            e2["flaeche"] = int(flaechen[i])
            e2["flaeche_kern"] = int(kflaechen.get(i, 0))
            for alt in ("herkunft_klasse", "urteil", "was_ist_es", "viertel", "punkte", "klasse_heute",
                        "klasse_vorschlag", "klasse_frei"):
                e2.pop(alt, None)
            if i in kern_ids and i in kernklasse[tk]:
                ur = u[i]
                e2["klasse"] = kernklasse[tk][i]
                e2["sicher"] = ja_nein(ur.get("sicher"))
                e2["urteil"] = ur.get("urteil")
                e2["was_ist_es"] = ur.get("was_ist_es")
                e2["viertel"] = ur["viertel"]
                if ur.get("punkte"):
                    e2["punkte"] = ur["punkte"]
                if fa == "C":
                    e2["klasse_heute"] = ur.get("klasse_heute")
                    e2["klasse_vorschlag"] = ur.get("klasse_vorschlag")
                else:
                    e2["klasse_frei"] = ur.get("klasse_frei")
                if e2["sicher"] == "ja":
                    n_sicher += 1
                else:
                    n_unsicher += 1
            else:
                werte = klassen_h0[karte == i]
                werte = werte[werte >= 0]
                if werte.size:
                    e2["klasse"] = sortiert[Counter(werte.tolist()).most_common(1)[0][0]]
                    e2["herkunft_klasse"] = "Kontextrand: Klasse aus dem Urteil der Nachbarkachel (Mehrheit der Bildpunkte)"
                    n_kontext_nachbar += 1
                else:
                    e2["klasse"] = s.get("klasse") if fa == "C" else "0"
                    e2["herkunft_klasse"] = ("Kontextrand außerhalb H0: Klasse der Vorstufe" if fa == "C"
                                             else "Kontextrand außerhalb H0: ohne Urteil, 0 Nicht bestimmbar")
                    n_kontext_aussen += 1
                e2["sicher"] = "nein"
                e2["urteil"] = "kontextrand"
            if e2["klasse"] not in codes_liste:
                fehler.append(f"Segment {i}: Klasse {e2['klasse']!r} nicht in der Liste")
            e2["grob"] = grob(e2["klasse"])
            neu.append(e2)
        ohne_eintrag = sorted(alle_ids - gesehen)
        if ohne_eintrag:
            fehler.append(f"Segmente ohne Eintrag: {ohne_eintrag[:10]}")
        n_verlauf = sum(1 for v in seg.get("verlauf") or [] if v.get("bearbeiter") != "vorstufe")
        verlauf = list(seg.get("verlauf") or []) + [{
            "nr": len(seg.get("verlauf") or []) + 1, "zeit": JETZT, "bearbeiter": BEARBEITER,
            "op": "klassen_aus_urteil",
            "parameter": {"quelle": f"urteil/{tk}/v1..v4/urteil.json",
                          "regel": ("klasse = klasse_vorschlag, sonst klasse_heute" if fa == "C" else
                                    "klasse = Code aus vereinheitlichung/codes.json")},
            "ergebnis": {"kern": len(kern_ids), "kontext_nachbar": n_kontext_nachbar,
                         "kontext_ausserhalb": n_kontext_aussen}}]
        ziel = {k: v for k, v in seg.items() if k not in ("segmente", "verlauf")}
        ziel["fassung"] = fa
        ziel["teilkachel"] = tk
        ziel["stand"] = (f"Fassung {fa}, Urteil Runde 0 (Karte nach den Eingriffen der Urteils-Agents, "
                         f"Klassen aus urteil/{tk}/v1..v4/urteil.json)")
        ziel["urteil"] = {"viertel": info, "eingriffe_urteil": len(eingriffe),
                          "eingriffe_verlauf": n_verlauf, "nicht_im_kern": nicht_im_kern}
        ziel["verlauf"] = verlauf
        ziel["segmente"] = neu
        schreib(ordner / tk / "segmente.json", ziel)
        bef[tk] = {"kern": len(kern_ids), "segmente": len(neu), "sicher_ja": n_sicher, "sicher_nein": n_unsicher,
                   "kontext_nachbar": n_kontext_nachbar, "kontext_ausserhalb": n_kontext_aussen,
                   "eingriffe_urteil": len(eingriffe), "eingriffe_verlauf": n_verlauf,
                   "urteil_nicht_im_kern": nicht_im_kern, "fehler": fehler}
        print(f"{fa} {tk}: Kern {len(kern_ids)}, sicher {n_sicher}, unsicher {n_unsicher}, "
              f"Kontext Nachbar {n_kontext_nachbar} / außen {n_kontext_aussen}, Eingriffe Urteil {len(eingriffe)} "
              f"/ Verlauf {n_verlauf}, Fehler {len(fehler)}")
        for x in fehler[:8]:
            print("   FEHLER", x)
    befund[fa] = bef


# ------------------------------------------------------------------ A
def baue_a(codes_liste, manifest, befund):
    ordner = ORDNER["A"]
    bef = {}
    for nr, t in enumerate(manifest["teilkacheln"]):
        tk = t["id"]
        ab = ordner / "abgabe" / tk
        karte = tifffile.imread(ab / "labels.tif").astype(np.uint32)
        seg = lies(ab / "segmente.json")
        teil = {c["code"]: c["name"] for c in lies(ab / "kategorien-teil.json")["classes"]}
        versatz = (nr + 1) * 100000
        if karte.max() >= 100000:
            raise SystemExit(f"A {tk}: IDs ab 100000, Versatz nicht eindeutig")
        kern_ids = {int(i) for i in np.unique(kern(karte, t))}
        flaechen = Counter(karte.ravel().tolist())
        kflaechen = Counter(kern(karte, t).ravel().tolist())
        fehler, neu = [], []
        fehlt = Counter()
        for s in seg["segmente"]:
            e = dict(s)
            e["id_abgabe"] = s["id"]
            e["id"] = s["id"] + versatz
            e["klasse_teil"] = s["klasse"]
            e["klasse_teil_name"] = teil.get(s["klasse"])
            if s["klasse"] not in A_ABB[tk]:
                fehlt[s["klasse"]] += 1
            e["klasse"] = A_ABB[tk].get(s["klasse"], s["klasse"])
            if e["klasse"] not in codes_liste:
                fehler.append(f"Segment {s['id']}: Klasse {e['klasse']!r} nicht in der Liste")
            e["grob"] = grob(e["klasse"])
            e["sicher"] = ja_nein(s.get("sicher"))
            e["im_kern"] = s["id"] in kern_ids
            e["flaeche"] = int(flaechen[s["id"]])
            e["flaeche_kern"] = int(kflaechen.get(s["id"], 0))
            neu.append(e)
        if fehlt:
            raise SystemExit(f"A {tk}: Codes ohne Abbildung {dict(fehlt)}")
        ids = {e["id_abgabe"] for e in neu}
        if ids != {int(i) for i in np.unique(karte)}:
            fehler.append("Segmente der Karte und der segmente.json stimmen nicht überein")
        ziel = ordner / tk
        ziel.mkdir(parents=True, exist_ok=True)
        tifffile.imwrite(ziel / "labels.tif", (karte + np.uint32(versatz)).astype(np.uint32), compression="zlib")
        verlauf = list(seg.get("verlauf") or []) + [{
            "zeit": JETZT, "bearbeiter": BEARBEITER, "op": "abgabe_uebernehmen",
            "parameter": {"quelle": f"abgabe/{tk}/", "id_versatz": versatz, "liste": "kategorien-a.json"}}]
        schreib(ziel / "segmente.json", {**{k: v for k, v in seg.items() if k not in ("segmente", "verlauf")},
                                         "schema": "landseg-segmente/1", "teilkachel": tk, "fassung": "A",
                                         "stand": f"Abgabe A {tk}, Codes nach kategorien-a.json, ID + {versatz}",
                                         "verlauf": verlauf, "segmente": neu})
        n_kern = [e for e in neu if e["im_kern"]]
        bef[tk] = {"kern": len(kern_ids), "segmente": len(neu), "versatz": versatz,
                   "sicher_ja": sum(e["sicher"] == "ja" for e in n_kern),
                   "sicher_nein": sum(e["sicher"] == "nein" for e in n_kern), "fehler": fehler}
        print(f"A {tk}: {len(neu)} Segmente, Kern {len(kern_ids)}, Versatz {versatz}, Fehler {len(fehler)}")
    befund["A"] = bef


def zusammentragen_json(fa, manifest):
    auftrag = {"schema": "landseg-zusammentragen/1", "manifest": "../manifest.json",
               "einheiten": [{"teilkachel": t["id"], "labels": f"{t['id']}/labels.tif",
                              "segmente": f"{t['id']}/segmente.json", "runde": 0,
                              "name": f"{fa.lower()}-{t['id']}"} for t in manifest["teilkacheln"]],
               "ziel": "zusammen"}
    schreib(ORDNER[fa] / "zusammentragen.json", auftrag)


def main():
    manifest = lies(H0 / "manifest.json")
    befund = {"schema": "landseg-h0-fassungen/1", "zeit": JETZT}
    listen = {"A": baue_a_liste(), "B": baue_b_liste(), "C": baue_c_liste()}
    baue_a(listen["A"], manifest, befund)
    baue_bc("B", listen["B"], manifest, befund)
    baue_bc("C", listen["C"], manifest, befund)
    for fa in "ABC":
        zusammentragen_json(fa, manifest)
    fehler = sum(len(x["fehler"]) for fa in "ABC" for x in befund[fa].values())
    befund["fehler"] = fehler
    schreib(D / "fassungen-h0.json", befund)
    print("Fehler gesamt:", fehler)
    return 1 if fehler else 0


if __name__ == "__main__":
    sys.exit(main())
