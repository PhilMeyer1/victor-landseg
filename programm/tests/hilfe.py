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
