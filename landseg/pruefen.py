"""W6 ``pruefen``: Wächter der Lückenlosigkeit einer Label-Karte.

Geprüft wird: Form H × W (wenn erwartet), kein Bildpunkt mit ID 0, jede ID ein zusammenhängendes
Gebiet (4er-Nachbarschaft), und mit ``segmente.json`` und Kategorienliste: jede ID der Karte hat
genau einen Eintrag mit gültiger Klasse, kein Eintrag ohne Bildpunkte, ``grob`` passt zur Klasse.
Optional: Mindestfläche je Segment.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
from scipy import ndimage

from .kategorien import Kategorien

#: 4er-Nachbarschaft: zwei Bildpunkte hängen nur über eine gemeinsame Kante zusammen.
VIERER = ndimage.generate_binary_structure(2, 1)


@dataclass
class Befund:
    hoehe: int
    breite: int
    ohne_segment: int = 0
    segmentzahl: int = 0
    nicht_zusammenhaengend: list[int] = field(default_factory=list)
    maengel: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.maengel

    @property
    def bildpunkte(self) -> int:
        return self.hoehe * self.breite

    def als_dict(self) -> dict:
        return {
            "ok": self.ok,
            "hoehe": self.hoehe,
            "breite": self.breite,
            "bildpunkte": self.bildpunkte,
            "ohne_segment": self.ohne_segment,
            "segmentzahl": self.segmentzahl,
            "nicht_zusammenhaengend": self.nicht_zusammenhaengend,
            "maengel": self.maengel,
        }

    def als_text(self) -> str:
        zeilen = [
            f"H × W: {self.hoehe} × {self.breite} = {self.bildpunkte} Bildpunkte, "
            f"ohne Segment (ID 0): {self.ohne_segment}",
            f"Segmente: {self.segmentzahl}, nicht zusammenhängend: {len(self.nicht_zusammenhaengend)}",
        ]
        if self.ok:
            zeilen.append("ok")
        else:
            zeilen.append(f"FEHLER: {len(self.maengel)} Mängel")
            zeilen.extend(f"- {m}" for m in self.maengel)
        return "\n".join(zeilen)


def zerfallene_ids(karte: np.ndarray, ids: list[int] | None = None) -> dict[int, int]:
    """ID -> Zahl der Teilgebiete, nur für IDs mit mehr als einem Teilgebiet."""
    werte, kompakt = np.unique(karte, return_inverse=True)
    kompakt = kompakt.reshape(karte.shape) + 1
    gefragt = None if ids is None else set(int(i) for i in ids)
    ergebnis: dict[int, int] = {}
    for idx, ausschnitt in enumerate(ndimage.find_objects(kompakt)):
        if ausschnitt is None:
            continue
        sid = int(werte[idx])
        if gefragt is not None and sid not in gefragt:
            continue
        _, anzahl = ndimage.label(kompakt[ausschnitt] == idx + 1, structure=VIERER)
        if anzahl > 1:
            ergebnis[sid] = anzahl
    return ergebnis


def pruefen(
    karte: np.ndarray,
    segmente: dict | None = None,
    kategorien: Kategorien | None = None,
    form: tuple[int, int] | None = None,
    mindestflaeche: int | None = None,
) -> Befund:
    hoehe, breite = karte.shape
    befund = Befund(hoehe=hoehe, breite=breite)
    if form is not None and tuple(form) != (hoehe, breite):
        befund.maengel.append(
            f"Form: Label-Karte {hoehe} × {breite}, erwartet {form[0]} × {form[1]}"
        )
    if karte.dtype != np.uint32:
        befund.maengel.append(f"Datentyp: {karte.dtype}, erwartet uint32")

    luecke = karte == 0
    befund.ohne_segment = int(luecke.sum())
    if befund.ohne_segment:
        ys, xs = np.nonzero(luecke)
        befund.maengel.append(
            f"Lücke: {befund.ohne_segment} Bildpunkte ohne Segment (ID 0), "
            f"Bereich x {xs.min()}–{xs.max()}, y {ys.min()}–{ys.max()}"
        )

    ids, flaechen = np.unique(karte[~luecke], return_counts=True)
    befund.segmentzahl = int(len(ids))

    zerfallen = zerfallene_ids(np.where(luecke, 0, karte))
    zerfallen.pop(0, None)
    befund.nicht_zusammenhaengend = sorted(zerfallen)
    for sid in befund.nicht_zusammenhaengend:
        befund.maengel.append(f"Zusammenhang: Segment {sid} besteht aus {zerfallen[sid]} Teilen")

    if mindestflaeche:
        for sid, fl in zip(ids.tolist(), flaechen.tolist()):
            if fl < mindestflaeche:
                befund.maengel.append(
                    f"Mindestfläche: Segment {sid} hat {fl} Bildpunkte (< {mindestflaeche})"
                )

    if segmente is not None:
        _pruefe_segmente(befund, set(ids.tolist()), segmente, kategorien)
    return befund


def _pruefe_segmente(befund: Befund, ids_karte: set[int], segmente: dict,
                     kategorien: Kategorien | None) -> None:
    eintraege: dict[int, dict] = {}
    for eintrag in segmente.get("segmente", []):
        sid = eintrag.get("id")
        if not isinstance(sid, int) or isinstance(sid, bool) or sid <= 0:
            befund.maengel.append(f"Schema: Segment-Eintrag ohne gültige ID: {eintrag!r}")
            continue
        if sid in eintraege:
            befund.maengel.append(f"Schema: Segment-ID {sid} doppelt in segmente.json")
            continue
        eintraege[sid] = eintrag

    for sid in sorted(ids_karte - eintraege.keys()):
        befund.maengel.append(f"Schema: Segment {sid} der Karte fehlt in segmente.json")
    for sid in sorted(eintraege.keys() - ids_karte):
        befund.maengel.append(f"Schema: Segment {sid} in segmente.json hat keine Bildpunkte")

    if kategorien is None:
        return
    for sid in sorted(eintraege):
        eintrag = eintraege[sid]
        klasse = eintrag.get("klasse")
        if not kategorien.gueltig(klasse):
            befund.maengel.append(f"Klasse: Segment {sid} hat ungültige Klasse {klasse!r}")
            continue
        grob = eintrag.get("grob")
        if grob is not None and grob != kategorien.grob(klasse):
            befund.maengel.append(
                f"Klasse: Segment {sid} grob {grob!r} passt nicht zu {klasse!r} "
                f"(erwartet {kategorien.grob(klasse)!r})"
            )
