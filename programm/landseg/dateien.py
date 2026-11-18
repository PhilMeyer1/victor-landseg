"""Lesen und Schreiben von Label-Karte, ``segmente.json`` und Manifest.

Label-Karte: Segment-ID je Bildpunkt, ``uint32``, 0 heißt „kein Segment" und darf in einer
fertigen Karte nicht vorkommen. Gespeichert als einkanaliges 32-Bit-TIFF (zlib), weil PNG höchstens
16 Bit je Kanal kennt.

``segmente.json``::

    {"schema": "landseg-segmente/1",
     "segmente": [{"id": 1, "klasse": "3.1", "grob": "3", ...}, ...],
     "verlauf": [{"zeit": ..., "bearbeiter": ..., "op": ..., ...}, ...]}
"""

from __future__ import annotations

import json
import os
import time
from contextlib import contextmanager
from pathlib import Path

import numpy as np
import tifffile

SEGMENTE_SCHEMA = "landseg-segmente/1"
MANIFEST_SCHEMA = "landseg-manifest/1"


def lese_labels(pfad: str | Path) -> np.ndarray:
    pfad = Path(pfad)
    if pfad.suffix.lower() == ".npy":
        karte = np.load(pfad)
    else:
        karte = tifffile.imread(pfad)
    if karte.ndim != 2:
        raise ValueError(f"{pfad}: Label-Karte muss einkanalig sein, hat Form {karte.shape}")
    if karte.dtype != np.uint32:
        if not np.issubdtype(karte.dtype, np.integer) or karte.min() < 0:
            raise ValueError(f"{pfad}: Label-Karte braucht ganzzahlige IDs >= 0, hat {karte.dtype}")
        karte = karte.astype(np.uint32)
    return karte


def schreibe_labels(pfad: str | Path, karte: np.ndarray) -> None:
    pfad = Path(pfad)
    if karte.dtype != np.uint32 or karte.ndim != 2:
        raise ValueError("Label-Karte muss 2-D uint32 sein")
    pfad.parent.mkdir(parents=True, exist_ok=True)
    tmp = pfad.with_name(pfad.name + ".tmp")
    if pfad.suffix.lower() == ".npy":
        with open(tmp, "wb") as f:
            np.save(f, karte)
    else:
        tifffile.imwrite(tmp, karte, compression="zlib", photometric="minisblack")
    os.replace(tmp, pfad)


@contextmanager
def karte_sperren(labels: str | Path, warten: float = 600.0, veraltet: float = 300.0):
    """Exklusiv für Lesen-Ändern-Schreiben von Label-Karte und ``segmente.json``.

    Mehrere Agents (je Viertel einer) bearbeiten dieselbe Karte: Wer schreibt, hält die Sperrdatei
    ``<labels>.sperre`` vom Lesen bis zum Schreiben; die anderen warten (höchstens ``warten`` Sekunden,
    dann ``TimeoutError``). So geht kein Eingriff verloren, und jeder liest den Stand nach dem letzten.
    Eine Sperrdatei älter als ``veraltet`` Sekunden stammt von einem abgebrochenen Aufruf und wird entfernt.
    """
    sperre = Path(labels).with_name(Path(labels).name + ".sperre")
    sperre.parent.mkdir(parents=True, exist_ok=True)
    ende = time.monotonic() + warten
    while True:
        try:
            fd = os.open(sperre, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            break
        except FileExistsError:
            try:
                if time.time() - sperre.stat().st_mtime > veraltet:
                    sperre.unlink()
                    continue
            except FileNotFoundError:
                continue
            if time.monotonic() >= ende:
                raise TimeoutError(f"{sperre}: Karte nach {warten:.0f} s noch von einem anderen Aufruf gesperrt")
            time.sleep(0.1)
    try:
        os.write(fd, f"{os.getpid()}\n".encode())
        os.close(fd)
        yield
    finally:
        try:
            sperre.unlink()
        except FileNotFoundError:
            pass


def lese_json(pfad: str | Path) -> dict:
    with open(pfad, encoding="utf-8") as f:
        return json.load(f)


def schreibe_json(pfad: str | Path, daten: dict) -> None:
    pfad = Path(pfad)
    pfad.parent.mkdir(parents=True, exist_ok=True)
    tmp = pfad.with_name(pfad.name + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(daten, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(tmp, pfad)


def lese_segmente(pfad: str | Path) -> dict:
    daten = lese_json(pfad)
    if not isinstance(daten.get("segmente"), list):
        raise ValueError(f"{pfad}: Feld 'segmente' fehlt oder ist keine Liste")
    daten.setdefault("schema", SEGMENTE_SCHEMA)
    daten.setdefault("verlauf", [])
    return daten


def segmente_nach_id(daten: dict) -> dict[int, dict]:
    """ID -> Eintrag; doppelte IDs sind ein Fehler."""
    ergebnis: dict[int, dict] = {}
    for eintrag in daten["segmente"]:
        sid = eintrag.get("id")
        if not isinstance(sid, int) or isinstance(sid, bool):
            raise ValueError(f"Segment ohne ganzzahlige ID: {eintrag!r}")
        if sid in ergebnis:
            raise ValueError(f"Segment-ID {sid} doppelt in segmente.json")
        ergebnis[sid] = eintrag
    return ergebnis
