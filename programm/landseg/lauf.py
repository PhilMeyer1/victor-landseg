"""Gemeinsames der Befehle ``vorbereiten`` und ``zusammenfuehren``: Fassungstabelle, Vorlagen, Schutz vor Überschreiben.

Die Zuordnung Fassung ↔ Buchstabe ↔ Ordner ↔ Kategorienliste steht an genau einer Stelle:
``einstellungen/seite.json`` (``fassungen``: Kennung, Name, Ordner, Liste). ``einstellungen/lauf.json`` nennt je
Kennung nur, wie die Fassung im Lauf entsteht (``art``: ``frei`` = eigene Karte je Teilkachel, ``urteil`` = Urteile
auf der Karte der Vorstufe; ``klassen``: ``fest`` oder ``frei``; Unterordner der Ergebnisse). Fehlt eine Kennung in
einer der beiden Dateien, stehen Ordner doppelt oder passt eine Angabe nicht, bricht der Befehl ab, bevor er etwas
schreibt (Exit 1).

In jeden Fassungsordner schreibt ``vorbereiten`` die Marke ``fassung.json`` (Kennung, Name, Ordner, Art);
``zusammenfuehren`` vergleicht sie mit der Tabelle, damit eine vertauschte Zuordnung nicht still durchläuft.
"""

from __future__ import annotations

import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path

from . import dateien, einstellungen

REPO = Path(__file__).resolve().parent.parent
VORLAGEN = REPO / "vorlagen"
PLATZHALTER = re.compile(r"\{\{([A-Z_]+)\}\}")
ARTEN = ("frei", "urteil")
KLASSEN = ("fest", "frei")
MARKE = "fassung.json"
MARKE_SCHEMA = "landseg-fassung/1"


class LaufFehler(Exception):
    """Befund: Vorbereitung oder Zusammenführen passen nicht (Exit 1); ``fehler`` nennt jede Stelle."""

    def __init__(self, fehler: list[str] | str):
        self.fehler = [fehler] if isinstance(fehler, str) else list(fehler)
        super().__init__("; ".join(self.fehler))


@dataclass(frozen=True)
class Fassung:
    kennung: str
    name: str
    ordner: Path
    liste: str | None          # Kategorienliste relativ zum Fassungsordner (None: Liste des Repos)
    art: str                   # frei | urteil
    klassen: str               # fest | frei (nur art urteil)
    werte: dict = field(default_factory=dict, compare=False)

    @property
    def kurz(self) -> str:
        """Art der Einheiten im Plan (``a``, ``b``, ``c``)."""
        return self.kennung.lower()

    @property
    def titel(self) -> str:
        return f"Fassung {self.kennung} „{self.name}“"

    def unter(self, schluessel: str, standard: str) -> Path:
        return self.ordner / str(self.werte.get(schluessel) or standard)

    def marke(self) -> dict:
        return {"schema": MARKE_SCHEMA, "kennung": self.kennung, "name": self.name, "ordner": self.ordner.name,
                "art": self.art, "klassen": self.klassen, "liste": self.liste}


def p(pfad) -> str:
    return Path(pfad).as_posix()


def einstellungen_laden(pfad: str | Path | None = None, seite: str | Path | None = None) -> tuple[dict, dict]:
    return einstellungen.laden("lauf", pfad), einstellungen.laden("seite", seite)


def fassungen(daten: str | Path, lauf: dict, seite: dict) -> list[Fassung]:
    """Fassungstabelle aus ``seite.json`` (Name, Ordner, Liste) und ``lauf.json`` (Art); Ordner relativ zu ``daten``."""
    daten = Path(daten)
    aus_seite = {str(e.get("kennung")): e for e in seite.get("fassungen") or []}
    aus_lauf = [e for e in lauf.get("fassungen") or [] if isinstance(e, dict)]
    fehler: list[str] = []
    kennungen = [str(e.get("kennung")) for e in aus_lauf]
    for k in sorted({k for k in kennungen if kennungen.count(k) > 1}):
        fehler.append(f"Fassung {k} steht mehrfach in lauf.json")
    for k in kennungen:
        if k not in aus_seite:
            fehler.append(f"Fassung {k} aus lauf.json fehlt in seite.json (fassungen)")
    for k in aus_seite:
        if k not in kennungen:
            fehler.append(f"Fassung {k} aus seite.json fehlt in lauf.json (fassungen)")
    ordner = [str(e.get("ordner") or "") for e in aus_seite.values()]
    for o in sorted({o for o in ordner if ordner.count(o) > 1 or not o}):
        fehler.append(f"Fassungsordner {o!r} leer oder mehrfach in seite.json")
    ergebnis = []
    for e in aus_lauf:
        k = str(e.get("kennung"))
        s = aus_seite.get(k)
        art, klassen = e.get("art"), e.get("klassen", "fest")
        if art not in ARTEN:
            fehler.append(f"Fassung {k}: art {art!r} (erlaubt: {', '.join(ARTEN)})")
        if art == "urteil" and klassen not in KLASSEN:
            fehler.append(f"Fassung {k}: klassen {klassen!r} (erlaubt: {', '.join(KLASSEN)})")
        if s is None or fehler:
            continue
        o = Path(s["ordner"])
        ergebnis.append(Fassung(k, str(s.get("name") or k), o if o.is_absolute() else daten / o,
                                s.get("kategorien") or None, art, klassen if art == "urteil" else "frei", dict(e)))
    if fehler:
        raise LaufFehler(fehler)
    return ergebnis


def marke_pruefen(f: Fassung) -> list[str]:
    """Vergleicht ``<ordner>/fassung.json`` mit der Tabelle; ohne Marke kein Befund (ältere Läufe)."""
    pfad = f.ordner / MARKE
    if not pfad.exists():
        return []
    m = dateien.lese_json(pfad)
    soll = f.marke()
    return [f"{f.titel}: {pfad.as_posix()} nennt {k} {m.get(k)!r}, die Einstellungen {soll[k]!r} "
            "(Zuordnung Fassung ↔ Ordner vertauscht?)"
            for k in ("kennung", "art", "klassen") if m.get(k) != soll[k]]


# -- Vorlagen -------------------------------------------------------------------------------------

def vorlage(name: str) -> str:
    return (VORLAGEN / name).read_text(encoding="utf-8")


def abschnitt(name: str) -> str:
    """Abschnitt ``<!-- abschnitt: name -->`` aus ``vorlagen/abschnitte.md`` (bis zum nächsten Abschnitt)."""
    text = vorlage("abschnitte.md")
    teile = re.split(r"^<!-- abschnitt: ([a-z0-9-]+) -->\n", text, flags=re.M)
    gefunden = dict(zip(teile[1::2], teile[2::2]))
    if name not in gefunden:
        raise LaufFehler(f"vorlagen/abschnitte.md: Abschnitt {name!r} fehlt")
    return gefunden[name].strip() + "\n"


def fuellen(text: str, werte: dict[str, str]) -> str:
    """Setzt ``{{NAME}}`` in einem Durchgang ein; ein Platzhalter ohne Wert ist ein Befund."""
    fehlt = sorted(set(PLATZHALTER.findall(text)) - set(werte))
    if fehlt:
        raise LaufFehler("Platzhalter ohne Wert: " + ", ".join(fehlt))
    return PLATZHALTER.sub(lambda m: str(werte[m.group(1)]), text)


def schreibe_text(pfad: Path, text: str) -> None:
    pfad.parent.mkdir(parents=True, exist_ok=True)
    pfad.write_text(text, encoding="utf-8", newline="\n")


# -- Schutz vor Überschreiben -----------------------------------------------------------------------

def belegt(pfad: Path) -> bool:
    return pfad.is_file() or (pfad.is_dir() and any(pfad.iterdir()))


def frei_machen(ziele: list[Path], ersetzen: bool) -> list[Path]:
    """Abbruch (Exit 2), wenn ein Ziel schon Inhalt hat; mit ``ersetzen`` wird es vorher entfernt."""
    voll = [z for z in dict.fromkeys(ziele) if belegt(z)]
    if voll and not ersetzen:
        raise ValueError("Ziel hat schon Inhalt, nichts geschrieben (ausdrücklich neu bauen: --ersetzen): "
                         + ", ".join(p(z) for z in voll[:8]) + (" …" if len(voll) > 8 else ""))
    for z in voll:
        if z.is_dir():
            shutil.rmtree(z)
        else:
            z.unlink()
    return voll
