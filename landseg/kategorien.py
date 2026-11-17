"""Kategorienliste laden (``kategorien.json``) und Klassen-Codes auflösen.

Die Klassen kommen ausschließlich aus der JSON-Datei; im Code ist keine Klasse fest verdrahtet.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

#: Standardort der Kategorienliste: Wurzel des Repos (neben dem Paket).
STANDARD_PFAD = Path(__file__).resolve().parent.parent / "kategorien.json"


@dataclass
class Kategorien:
    """Gelesene Kategorienliste: Code -> Klasse, mit Eltern und Ebene."""

    pfad: Path
    klassen: dict[str, dict] = field(default_factory=dict)

    def gueltig(self, code: object) -> bool:
        return isinstance(code, str) and code in self.klassen

    def grob(self, code: str) -> str:
        """Ebene-1-Vorfahr eines Codes (die grobe Klasse)."""
        gesehen = set()
        while True:
            klasse = self.klassen[code]
            eltern = klasse.get("parent")
            if eltern is None:
                return code
            if code in gesehen:
                raise ValueError(f"Kategorienliste: Zyklus bei Code {code!r}")
            gesehen.add(code)
            code = eltern

    def name(self, code: str) -> str:
        return self.klassen[code].get("name", code)


def laden(pfad: str | Path | None = None) -> Kategorien:
    """Liest die Kategorienliste; ohne Pfad die ``kategorien.json`` des Repos."""
    pfad = Path(pfad) if pfad else STANDARD_PFAD
    with open(pfad, encoding="utf-8") as f:
        daten = json.load(f)
    klassen_liste = daten.get("classes")
    if not isinstance(klassen_liste, list) or not klassen_liste:
        raise ValueError(f"{pfad}: Feld 'classes' fehlt oder ist leer")
    klassen: dict[str, dict] = {}
    for eintrag in klassen_liste:
        code = eintrag.get("code")
        if not isinstance(code, str) or not code:
            raise ValueError(f"{pfad}: Klasse ohne gültigen 'code': {eintrag!r}")
        if code in klassen:
            raise ValueError(f"{pfad}: Code {code!r} doppelt")
        klassen[code] = eintrag
    for code, eintrag in klassen.items():
        eltern = eintrag.get("parent")
        if eltern is not None and eltern not in klassen:
            raise ValueError(f"{pfad}: Elternklasse {eltern!r} von {code!r} fehlt")
    kat = Kategorien(pfad=pfad, klassen=klassen)
    for code in klassen:
        kat.grob(code)  # Zyklen früh melden
    return kat
