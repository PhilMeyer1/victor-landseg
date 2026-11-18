"""Einstellungen der Werkzeuge aus JSON (``einstellungen/<werkzeug>.json`` im Repo).

Schwellen, Größen und Farben stehen nicht im Code, sondern in der JSON-Datei des Werkzeugs. Eine
eigene Datei (``--einstellungen``) überschreibt nur die Schlüssel, die sie nennt; verschachtelte
Abschnitte werden eine Ebene tief zusammengeführt.
"""

from __future__ import annotations

from pathlib import Path

from .dateien import lese_json

#: Standardordner: ``einstellungen/`` in der Wurzel des Repos (neben ``kategorien.json``).
STANDARD_ORDNER = Path(__file__).resolve().parent.parent / "einstellungen"


def laden(werkzeug: str, pfad: str | Path | None = None) -> dict:
    """Standard-Einstellungen des Werkzeugs, mit ``pfad`` überschrieben."""
    werte = lese_json(STANDARD_ORDNER / f"{werkzeug}.json")
    if pfad:
        werte = ueberschreiben(werte, lese_json(pfad))
    return werte


def ueberschreiben(werte: dict, ueber: dict) -> dict:
    """``werte`` mit den Schlüsseln aus ``ueber``; Abschnitte (dict) eine Ebene tief zusammengeführt."""
    werte = dict(werte)
    for schluessel, wert in ueber.items():
        if isinstance(wert, dict) and isinstance(werte.get(schluessel), dict):
            werte[schluessel] = {**werte[schluessel], **wert}
        else:
            werte[schluessel] = wert
    return werte
