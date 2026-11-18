"""Kategorienliste laden (``kategorien.json``) und Klassen-Codes auflösen.

Die Klassen kommen ausschließlich aus der JSON-Datei; im Code ist keine Klasse fest verdrahtet.
Auch die Abbildung auf Bericht 48 (``bericht48_klasse``) liest ihre Klassen aus der Datei: Regel G1,
Feld ``bericht48`` (``im_siedlung_klassen``, ``im_siedlung_ziel``).
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

#: Standardort der Kategorienliste: Wurzel des Repos (neben dem Paket).
STANDARD_PFAD = Path(__file__).resolve().parent.parent / "kategorien.json"

#: Namen, die jede freie Liste (Fassungen A und B) führen muss: Klasse „Garten“ unter der Ebene-1-Klasse
#: „Dauergrünland“ (Skill landseg-agent, L14). Ein Zusatz in Klammern ist erlaubt, etwa „Garten (Haus- und
#: Hofgarten)“; Groß- und Kleinschreibung zählt nicht.
GARTEN = "Garten"
DAUERGRUENLAND = "Dauergrünland"


def _heisst(name: object, wort: str) -> bool:
    return isinstance(name, str) and re.fullmatch(rf"{re.escape(wort)}(\s*\(.*\))?", name.strip(),
                                                  re.IGNORECASE | re.DOTALL) is not None


def garten_maengel(klassen: dict[str, dict]) -> list[str]:
    """Mängel einer freien Liste (Code -> Klasse) gegen die Pflicht „Garten unter Dauergrünland“; leer = ok."""
    garten = [c for c, k in klassen.items() if _heisst(k.get("name"), GARTEN)]
    if not garten:
        return [f"Garten: Liste ohne Klasse „{GARTEN}“ (Pflicht in jeder freien Fassung, unter der "
                f"Ebene-1-Klasse „{DAUERGRUENLAND}“; Skill landseg-agent, L14)"]
    maengel = []
    for code in garten:
        kette, gesehen = [code], {code}
        while (eltern := klassen.get(kette[-1], {}).get("parent")) is not None and str(eltern) not in gesehen:
            kette.append(str(eltern))
            gesehen.add(str(eltern))
        oben = kette[-1]
        if len(kette) < 2 or not _heisst(klassen.get(oben, {}).get("name"), DAUERGRUENLAND):
            ort = ("ist selbst Ebene 1" if len(kette) < 2
                   else f"steht unter {oben} „{klassen.get(oben, {}).get('name', oben)}“")
            maengel.append(f"Garten: Klasse {code} „{klassen[code].get('name')}“ {ort}, "
                           f"erwartet unter der Ebene-1-Klasse „{DAUERGRUENLAND}“")
    return maengel


@dataclass
class Kategorien:
    """Gelesene Kategorienliste: Code -> Klasse, mit Eltern und Ebene."""

    pfad: Path
    klassen: dict[str, dict] = field(default_factory=dict)
    #: Klassen (samt Unterklassen), die im Siedlungsgebiet nach Bericht 48 zur Siedlung zählen
    siedlung_klassen: tuple[str, ...] = ()
    #: Ebene-1-Klasse, als die sie dann zählen (Bericht 48: Versiegelt / bebaut)
    siedlung_ziel: str | None = None

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

    def vorfahren(self, code: str) -> list[str]:
        """Der Code selbst und alle Elternklassen bis Ebene 1."""
        kette = [code]
        while self.klassen[kette[-1]].get("parent") is not None:
            kette.append(self.klassen[kette[-1]]["parent"])
        return kette

    def unter(self, code: str, auswahl) -> bool:
        """Ob der Code eine der Klassen in ``auswahl`` ist oder darunter liegt."""
        return any(c in auswahl for c in self.vorfahren(code))

    def siedlung_moeglich(self, code: str) -> bool:
        """Ob ein Segment dieser Klasse das Merkmal ``im_siedlung: ja`` tragen kann."""
        return self.unter(code, self.siedlung_klassen)

    def garten_maengel(self) -> list[str]:
        """Pflicht der freien Fassungen: Klasse „Garten“ unter „Dauergrünland“ (``garten_maengel``)."""
        return garten_maengel(self.klassen)

    def bericht48_klasse(self, code: str, im_siedlung: object = None) -> str:
        """Ebene-1-Klasse für Auswertungen nach Bericht 48.

        Wie ``grob``, nur zählt ein Segment der Klassen ``siedlung_klassen`` (Acker, Grünland,
        Gehölz außerhalb Wald) mit ``im_siedlung: ja`` als ``siedlung_ziel`` (Hausgärten „als
        Teil der Siedlung führen“). Fehlt das Merkmal, gilt es als ``nein``.
        """
        if (self.siedlung_ziel is not None and im_siedlung in ("ja", True)
                and self.siedlung_moeglich(code)):
            return self.siedlung_ziel
        return self.grob(code)


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
    regel = next((r["bericht48"] for r in daten.get("rules") or []
                  if isinstance(r, dict) and isinstance(r.get("bericht48"), dict)), None)
    if regel is not None:
        auswahl = regel.get("im_siedlung_klassen") or []
        ziel = regel.get("im_siedlung_ziel")
        for code in [*auswahl, ziel]:
            if code not in klassen:
                raise ValueError(f"{pfad}: Regel bericht48 nennt unbekannte Klasse {code!r}")
        kat.siedlung_klassen = tuple(auswahl)
        kat.siedlung_ziel = ziel
    return kat
