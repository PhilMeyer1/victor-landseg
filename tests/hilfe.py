"""Gemeinsame Testdaten: kleine Beispiel-Kategorienliste und synthetische Label-Karten."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from landseg import kategorien

BEISPIEL_KLASSEN = [
    {"code": "0", "name": "Nicht bestimmbar", "parent": None, "level": 1},
    {"code": "1", "name": "Siedlung", "parent": None, "level": 1},
    {"code": "1.1", "name": "Gebäude", "parent": "1", "level": 2},
    {"code": "3", "name": "Wald", "parent": None, "level": 1},
    {"code": "3.1", "name": "Laubwald", "parent": "3", "level": 2},
    {"code": "3.1.1", "name": "Einzelbaum", "parent": "3.1", "level": 3},
]


def beispiel_kategorien(ordner: Path) -> kategorien.Kategorien:
    pfad = Path(ordner) / "kategorien_beispiel.json"
    pfad.write_text(json.dumps({"classes": BEISPIEL_KLASSEN}), encoding="utf-8")
    return kategorien.laden(pfad)


def beispiel_karte() -> tuple[np.ndarray, dict]:
    """40 × 40: links Segment 1 (mit Insel 4 oben links), rechts oben 2, rechts unten 3."""
    karte = np.zeros((40, 40), np.uint32)
    karte[:, :20] = 1
    karte[:20, 20:] = 2
    karte[20:, 20:] = 3
    karte[2:6, 2:6] = 4
    segmente = {
        "schema": "landseg-segmente/1",
        "segmente": [
            {"id": 1, "klasse": "1.1", "grob": "1"},
            {"id": 2, "klasse": "3.1", "grob": "3"},
            {"id": 3, "klasse": "3", "grob": "3"},
            {"id": 4, "klasse": "3.1.1", "grob": "3"},
        ],
        "verlauf": [],
    }
    return karte, segmente


def block_karte(groesse: int = 64, block: int = 8) -> tuple[np.ndarray, dict]:
    """Raster aus Quadraten, je Quadrat ein Segment; Klassen abwechselnd."""
    zeilen = np.arange(groesse) // block
    karte = (zeilen[:, None] * (groesse // block) + zeilen[None, :] + 1).astype(np.uint32)
    klassen = ["1.1", "3.1", "3", "3.1.1"]
    segmente = {"segmente": [], "verlauf": []}
    for sid in np.unique(karte).tolist():
        k = klassen[sid % len(klassen)]
        segmente["segmente"].append({"id": sid, "klasse": k, "grob": k.split(".")[0]})
    return karte, segmente


# -- Mini-Lauf für vorbereiten und zusammenfuehren -------------------------------------------------

#: Klassen der Vorstufe (aus kategorien.json des Repos) je Block, abwechselnd.
LAUF_KLASSEN = ("1.1", "2.1")
#: kleine freie Liste (Fassungen mit eigenen Klassen) und ihre Codes; Garten unter Dauergrünland ist Pflicht
FREIE_LISTE = [{"code": "0", "name": "Nicht bestimmbar", "parent": None, "level": 1, "color": "#808080"},
               {"code": "1", "name": "Bebaut", "parent": None, "level": 1, "color": "#c03030"},
               {"code": "1.1", "name": "Dach", "parent": "1", "level": 2, "color": "#ff6060"},
               {"code": "2", "name": "Offen", "parent": None, "level": 1, "color": "#30a030"},
               {"code": "3", "name": "Dauergrünland", "parent": None, "level": 1, "color": "#60c060"},
               {"code": "3.1", "name": "Garten", "parent": "3", "level": 2, "color": "#a6ffaf"}]


def _block_id(gx, gy):
    """Segment je 20-px-Block des Ausschnitts: jedes Viertel eines 40-px-Kerns ist genau ein Block."""
    return (gy // 20) * 5 + (gx // 20) + 1


def mini_lauf(ordner: Path) -> Path:
    """Ausschnitt 80 × 80 (Kern 40, Rand 8, vier Teilkacheln) mit Vorstufe ``vorstufe/<tk>/``; gibt das Manifest."""
    import tifffile

    from landseg import dateien
    from landseg.kacheln import kacheln
    from tests.test_kacheln import PRJ

    quelle = Path(ordner) / "quelle"
    quelle.mkdir(parents=True)
    ys, xs = np.mgrid[0:100, 0:100]
    bild = np.stack([(ys * 2) % 256, (xs * 2) % 256, ((xs // 20 + ys // 20) % 2) * 120 + 60], -1).astype(np.uint8)
    tifffile.imwrite(quelle / "blatt.tif", bild, photometric="rgb")
    (quelle / "blatt.TFW").write_text("0.2\n0\n0\n-0.2\n1000.1\n5000.9\n", encoding="ascii")
    (quelle / "blatt.PRJ").write_text(PRJ, encoding="ascii")
    daten = Path(ordner) / "M"
    manifest = kacheln(quelle / "blatt.tif", 0, 0, 80, 80, daten, kern=40, rand=8, name="M")
    for t in manifest["teilkacheln"]:
        k, ki = t["kontext"], t["kern_im_bild"]
        gy, gx = np.mgrid[k["y"]:k["y"] + k["hoehe"], k["x"]:k["x"] + k["breite"]]
        karte = _block_id(gx, gy).astype(np.uint32)
        kern = set(np.unique(karte[ki["y"]:ki["y"] + ki["hoehe"], ki["x"]:ki["x"] + ki["breite"]]).tolist())
        eintraege = [{"id": sid, "klasse": LAUF_KLASSEN[sid % 2], "grob": LAUF_KLASSEN[sid % 2].split(".")[0],
                      "sicher": "nein", "im_kern": sid in kern} for sid in np.unique(karte).tolist()]
        dateien.schreibe_labels(daten / "vorstufe" / t["id"] / "labels.tif", karte)
        dateien.schreibe_json(daten / "vorstufe" / t["id"] / "segmente.json",
                              {"schema": "landseg-segmente/1", "segmente": eintraege,
                               "verlauf": [{"nr": 1, "bearbeiter": "vorstufe", "op": "vorstufe"}]})
    return daten / "manifest.json"


def mini_urteile(plan: dict) -> None:
    """Schreibt zu einem Plan von ``vorbereiten`` die Abgaben der Agents: Urteile (B, C, Gegenprobe), freie
    Abgabe (A), Vereinheitlichungen; Klasse C = Vorschlag 3 für gerade IDs, sonst die heutige."""
    from landseg import dateien

    fassungen = {f["kennung"].lower(): f for f in plan["fassungen"]}
    for e in plan["einheiten"]:
        ziel = Path(e["ergebnis"])
        if e["art"] == "a":
            vorstufe = Path(plan["manifest"]).parent / "vorstufe" / e["tk"]
            karte = dateien.lese_labels(vorstufe / "labels.tif")
            ids = np.unique(karte).tolist()
            dateien.schreibe_labels(ziel / "labels.tif", karte)
            dateien.schreibe_json(ziel / "segmente.json", {"schema": "landseg-segmente/1", "verlauf": [], "segmente": [
                {"id": i, "klasse": "9" if i % 2 else "8", "grob": "9" if i % 2 else "8", "sicher": True,
                 "im_kern": True} for i in ids]})
            dateien.schreibe_json(ziel / "kategorien-teil.json", {"classes": [
                {"code": "8", "name": "Haus", "parent": None, "level": 1},
                {"code": "9", "name": "Feld", "parent": None, "level": 1}]})
            continue
        liste = next(v["segmente"] for v in plan["viertel"] + plan["gegenprobe"] if v["auftrag"] == e["auftrag"])
        frei = fassungen.get(e["art"], {}).get("klassen") == "frei"
        dateien.schreibe_json(ziel / "urteil.json", {
            "schema": "landseg-urteil/1", "teilkachel": e["tk"], "viertel": f"v{e['v']}",
            "bearbeiter": f"test:{e['art']}", "eingriffe": [{"schritt": "teilen", "vorher": [1], "nachher": [1]}]
            if e["v"] == 1 else [],
            "segmente": [{"id": i, "klasse_heute": LAUF_KLASSEN[i % 2], "urteil": "sauber",
                          "klasse_vorschlag": None if frei or i % 2 else "3", "sicher": i % 3 == 0,
                          "was_ist_es": "Test", **({"klasse_frei": {"grob": "Offen"}} if frei else {})}
                         for i in liste]})
    for v in plan["vereinheitlichen"]:
        ziel = Path(v["ergebnis"])
        art = v["fassung"].lower()
        liste = {"schema": "landseg-kategorien/1", "title": "Test", "classes": FREIE_LISTE}
        if art == "a":
            liste["abbildung_teilkacheln"] = {tk: {"8": "1.1", "9": "2"} for tk in plan["ganz_teilkachel"]}
        else:
            codes = {}
            for e in plan["viertel"]:
                if e["art"] == art:
                    for i in e["segmente"]:
                        codes.setdefault(e["teilkachel"], {})[str(i)] = {"code": "2" if i % 2 else "1.1",
                                                                         "viertel": e["viertel"]}
            dateien.schreibe_json(ziel / "codes.json", {"schema": "landseg-codes/1", "segmente": codes})
        dateien.schreibe_json(ziel / "kategorien-entwurf.json", liste)
