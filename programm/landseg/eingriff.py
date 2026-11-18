"""W5 ``eingriff``: Operationen auf der Label-Karte, stets lückenlos, mit Verlauf.

Jede Operation schreibt nur Segment-IDs auf vorhandene Bildpunkte um; ID 0 entsteht nie. Ein
Eingriff wirkt ganz oder gar nicht: Scheitert eine Bedingung, bleiben Karte und ``segmente.json``
unverändert (``EingriffFehler``). Zusammenhang gilt in 4er-Nachbarschaft wie in ``pruefen``.

Koordinaten sind Bildpunkte der Label-Karte: ``x`` Spalte, ``y`` Zeile.
"""

from __future__ import annotations

import copy
from datetime import datetime, timezone

import cv2
import numpy as np
from scipy import ndimage

from .dateien import segmente_nach_id
from .kategorien import Kategorien
from .pruefen import VIERER

Punkte = list[tuple[int, int]] | list[list[int]]


class EingriffFehler(Exception):
    """Der Eingriff ist nicht ausführbar; nichts wurde geändert."""


def _punkte_array(punkte: Punkte, mindestens: int) -> np.ndarray:
    arr = np.asarray(punkte, dtype=np.int32).reshape(-1, 2)
    if len(arr) < mindestens:
        raise EingriffFehler(f"mindestens {mindestens} Punkte nötig, {len(arr)} gegeben")
    return arr


def linie_maske(form: tuple[int, int], punkte: Punkte) -> np.ndarray:
    """8-verbundener Linienzug, 1 Bildpunkt breit (trennt 4er-zusammenhängende Gebiete)."""
    maske = np.zeros(form, np.uint8)
    cv2.polylines(maske, [_punkte_array(punkte, 2)], False, 1, thickness=1, lineType=cv2.LINE_8)
    return maske.astype(bool)


def polygon_maske(form: tuple[int, int], punkte: Punkte) -> np.ndarray:
    """Gefülltes Polygon einschließlich seines Randes."""
    maske = np.zeros(form, np.uint8)
    arr = _punkte_array(punkte, 3)
    cv2.fillPoly(maske, [arr], 1, lineType=cv2.LINE_8)
    cv2.polylines(maske, [arr], True, 1, thickness=1, lineType=cv2.LINE_8)
    return maske.astype(bool)


def _zusammenhaengend(maske: np.ndarray) -> bool:
    _, anzahl = ndimage.label(maske, structure=VIERER)
    return anzahl == 1


def _anwachsen(teile: np.ndarray, offen: np.ndarray) -> None:
    """Weist offene Bildpunkte schrittweise einem 4er-Nachbarn aus ``teile`` (>0) zu.

    Jeder zugewiesene Bildpunkt grenzt an sein Teil, die Teile bleiben also zusammenhängend.
    """
    offen = offen.copy()
    while offen.any():
        kandidat = np.zeros_like(teile)
        for achse, schritt in ((0, 1), (0, -1), (1, 1), (1, -1)):
            nachbar = np.roll(teile, schritt, axis=achse)
            if achse == 0:
                rand = (slice(0, 1) if schritt == 1 else slice(-1, None), slice(None))
            else:
                rand = (slice(None), slice(0, 1) if schritt == 1 else slice(-1, None))
            nachbar[rand] = 0
            setzen = (kandidat == 0) & (nachbar > 0)
            kandidat[setzen] = nachbar[setzen]
        neu = offen & (kandidat > 0)
        if not neu.any():
            raise EingriffFehler("Bildpunkte auf der Linie ohne Nachbar im Segment")
        teile[neu] = kandidat[neu]
        offen &= ~neu


class Bearbeitung:
    """Eine Label-Karte mit ihrer ``segmente.json`` in Bearbeitung."""

    def __init__(self, karte: np.ndarray, segmente: dict, kategorien: Kategorien,
                 bearbeiter: str):
        if karte.ndim != 2 or karte.dtype != np.uint32:
            raise EingriffFehler("Label-Karte muss 2-D uint32 sein")
        if (karte == 0).any():
            raise EingriffFehler("Label-Karte hat Lücken (ID 0); erst mit pruefen klären")
        if not bearbeiter:
            raise EingriffFehler("Bearbeiter fehlt")
        self.karte = karte.copy()
        self.segmente = copy.deepcopy(segmente)
        self.segmente.setdefault("verlauf", [])
        self.kategorien = kategorien
        self.bearbeiter = bearbeiter
        segmente_nach_id(self.segmente)  # doppelte IDs früh melden

    # -- Hilfen -----------------------------------------------------------------------------

    def _eintraege(self) -> dict[int, dict]:
        return copy.deepcopy(segmente_nach_id(self.segmente))

    def _segment(self, eintraege: dict[int, dict], sid: int) -> dict:
        if sid not in eintraege or not (self.karte == sid).any():
            raise EingriffFehler(f"Segment {sid} gibt es nicht")
        return eintraege[sid]

    def _klasse(self, klasse: str) -> str:
        if not self.kategorien.gueltig(klasse):
            raise EingriffFehler(f"Klasse {klasse!r} steht nicht in {self.kategorien.pfad.name}")
        return klasse

    @staticmethod
    def _naechste_id(karte: np.ndarray, eintraege: dict[int, dict]) -> int:
        return int(max(int(karte.max()), max(eintraege, default=0))) + 1

    def _abgeleitet(self, vorlage: dict, sid: int, herkunft: str) -> dict:
        eintrag = copy.deepcopy(vorlage)
        eintrag["id"] = sid
        eintrag["herkunft"] = herkunft
        return eintrag

    def _zerfallene_aufteilen(self, karte: np.ndarray, eintraege: dict[int, dict],
                              ids: set[int], op: str) -> list[int]:
        """Zerfallene Segmente: größtes Teil behält die ID, jedes weitere bekommt eine neue."""
        neue: list[int] = []
        for sid in sorted(ids):
            maske = karte == sid
            if not maske.any():
                continue
            teile, anzahl = ndimage.label(maske, structure=VIERER)
            if anzahl < 2:
                continue
            groessen = np.bincount(teile.ravel())[1:]
            behalten = int(np.argmax(groessen)) + 1
            for teil in range(1, anzahl + 1):
                if teil == behalten:
                    continue
                nid = self._naechste_id(karte, eintraege)
                karte[teile == teil] = nid
                eintraege[nid] = self._abgeleitet(eintraege[sid], nid, f"eingriff:{op} aus {sid}")
                neue.append(nid)
        return neue

    def _uebernehmen(self, karte: np.ndarray, eintraege: dict[int, dict], op: str,
                     parameter: dict, ergebnis: dict) -> dict:
        if (karte == 0).any():  # darf per Konstruktion nie eintreten
            raise RuntimeError(f"eingriff {op}: Lücke entstanden, Eingriff verworfen")
        vorhanden = set(np.unique(karte).tolist())
        self.karte = karte
        self.segmente["segmente"] = [eintraege[i] for i in sorted(eintraege) if i in vorhanden]
        self.segmente["verlauf"].append({
            "nr": len(self.segmente["verlauf"]) + 1,
            "zeit": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "bearbeiter": self.bearbeiter,
            "op": op,
            "parameter": parameter,
            "ergebnis": ergebnis,
        })
        return ergebnis

    # -- Operationen ------------------------------------------------------------------------

    def verschmelzen(self, ids: list[int], ziel: int | None = None) -> dict:
        """Mehrere benachbarte Segmente zu einem; ``ziel`` (Standard: erste ID) behält ID und Klasse."""
        ids = [int(i) for i in ids]
        if len(set(ids)) < 2:
            raise EingriffFehler("verschmelzen braucht mindestens zwei verschiedene IDs")
        ziel = ids[0] if ziel is None else int(ziel)
        if ziel not in ids:
            raise EingriffFehler(f"Ziel {ziel} ist nicht unter den IDs {ids}")
        eintraege = self._eintraege()
        for sid in ids:
            self._segment(eintraege, sid)
        vereint = np.isin(self.karte, ids)
        if not _zusammenhaengend(vereint):
            raise EingriffFehler(f"Segmente {ids} sind nicht zusammenhängend benachbart")
        karte = self.karte.copy()
        karte[vereint] = ziel
        entfernt = sorted(set(ids) - {ziel})
        for sid in entfernt:
            del eintraege[sid]
        return self._uebernehmen(karte, eintraege, "verschmelzen",
                                 {"ids": ids, "ziel": ziel}, {"ziel": ziel, "entfernt": entfernt})

    def teilen(self, sid: int, linie: Punkte) -> dict:
        """Teilt ein Segment entlang eines Linienzugs; das größte Teil behält die ID."""
        sid = int(sid)
        eintraege = self._eintraege()
        vorlage = self._segment(eintraege, sid)
        maske = self.karte == sid
        auf_linie = maske & linie_maske(self.karte.shape, linie)
        rest = maske & ~auf_linie
        teile, anzahl = ndimage.label(rest, structure=VIERER)
        if anzahl < 2:
            raise EingriffFehler(f"Die Linie teilt Segment {sid} nicht (Teile: {anzahl})")
        _anwachsen(teile, auf_linie)
        groessen = np.bincount(teile[maske], minlength=anzahl + 1)[1:]
        behalten = int(np.argmax(groessen)) + 1
        karte = self.karte.copy()
        neue: list[int] = []
        for teil in range(1, anzahl + 1):
            if teil == behalten:
                continue
            nid = self._naechste_id(karte, eintraege)
            karte[teile == teil] = nid
            eintraege[nid] = self._abgeleitet(vorlage, nid, f"eingriff:teilen aus {sid}")
            neue.append(nid)
        return self._uebernehmen(karte, eintraege, "teilen",
                                 {"id": sid, "linie": np.asarray(linie).tolist()},
                                 {"behalten": sid, "neu": neue})

    def grenze_verschieben(self, von: int, nach: int, flaeche: Punkte) -> dict:
        """Bildpunkte von ``von`` innerhalb des Polygons gehen an den Nachbarn ``nach``."""
        von, nach = int(von), int(nach)
        if von == nach:
            raise EingriffFehler("von und nach sind dasselbe Segment")
        eintraege = self._eintraege()
        self._segment(eintraege, von)
        self._segment(eintraege, nach)
        wechsel = (self.karte == von) & polygon_maske(self.karte.shape, flaeche)
        if not wechsel.any():
            raise EingriffFehler(f"Das Polygon enthält keine Bildpunkte von Segment {von}")
        karte = self.karte.copy()
        karte[wechsel] = nach
        if not _zusammenhaengend(karte == nach):
            raise EingriffFehler(f"Die verschobene Fläche grenzt nicht an Segment {nach}")
        rest = karte == von
        if rest.any() and not _zusammenhaengend(rest):
            raise EingriffFehler(f"Segment {von} zerfiele; Polygon anpassen oder teilen")
        ergebnis = {"bildpunkte": int(wechsel.sum()), "entfernt": [] if rest.any() else [von]}
        if not rest.any():
            del eintraege[von]
        return self._uebernehmen(karte, eintraege, "grenze_verschieben",
                                 {"von": von, "nach": nach, "flaeche": np.asarray(flaeche).tolist()},
                                 ergebnis)

    def kante_einrasten(self, bild: np.ndarray, a: int, b: int, vorgaben: dict,
                        band: int | None = None, bereich: Punkte | None = None):
        """W4: Grenze zwischen ``a`` und ``b`` im engen Band auf die Bildkante einrasten.

        Gibt das ``KantenErgebnis`` zurück (mit den geschätzten Strecken); der Verlauf führt sie
        ohne Einzelpunkte.
        """
        from .kante import einrasten  # kante baut auf eingriff auf

        a, b = int(a), int(b)
        eintraege = self._eintraege()
        self._segment(eintraege, a)
        self._segment(eintraege, b)
        ergebnis = einrasten(bild, self.karte, a, b, vorgaben, band=band, bereich=bereich)
        parameter = {"a": a, "b": b, "band": ergebnis.band, "kante_min": ergebnis.kante_min,
                     "bereich": None if bereich is None else np.asarray(bereich).tolist()}
        self._uebernehmen(ergebnis.karte, eintraege, "kante", parameter,
                          ergebnis.als_dict(mit_punkten=False))
        return ergebnis

    def klasse_setzen(self, sid: int, klasse: str) -> dict:
        sid = int(sid)
        eintraege = self._eintraege()
        eintrag = self._segment(eintraege, sid)
        alt = eintrag.get("klasse")
        eintrag["klasse"] = self._klasse(klasse)
        eintrag["grob"] = self.kategorien.grob(klasse)
        return self._uebernehmen(self.karte.copy(), eintraege, "klasse_setzen",
                                 {"id": sid, "klasse": klasse}, {"alt": alt, "neu": klasse})

    def vermerken(self, sid: int, felder: dict, op: str = "vermerk") -> dict:
        """Setzt Felder eines Segments, die weder Karte noch Klasse betreffen (etwa ``sicher``), mit Verlauf.

        ``id``, ``klasse`` und ``grob`` ändert nur ``klasse_setzen``."""
        sid = int(sid)
        verboten = {"id", "klasse", "grob"} & set(felder)
        if verboten:
            raise EingriffFehler(f"vermerken ändert {', '.join(sorted(verboten))} nicht (dafür klasse_setzen)")
        eintraege = self._eintraege()
        eintrag = self._segment(eintraege, sid)
        alt = {k: copy.deepcopy(eintrag.get(k)) for k in felder}
        eintrag.update(copy.deepcopy(felder))
        return self._uebernehmen(self.karte.copy(), eintraege, op, {"id": sid, "felder": sorted(felder)},
                                 {"alt": alt})

    def polygon_zuweisen(self, flaeche: Punkte, sid: int | None = None,
                         klasse: str | None = None) -> dict:
        """Alle Bildpunkte im Polygon an ein vorhandenes Segment oder an ein neues mit Klasse.

        Segmente, die dadurch zerfallen, werden in eigene IDs (gleiche Klasse) aufgeteilt.
        """
        if (sid is None) == (klasse is None):
            raise EingriffFehler("polygon_zuweisen braucht genau eins: id oder klasse")
        eintraege = self._eintraege()
        maske = polygon_maske(self.karte.shape, flaeche)
        if not maske.any():
            raise EingriffFehler("Das Polygon liegt außerhalb der Label-Karte")
        betroffen = set(np.unique(self.karte[maske]).tolist())
        karte = self.karte.copy()
        if sid is not None:
            ziel = int(sid)
            self._segment(eintraege, ziel)
        else:
            ziel = self._naechste_id(karte, eintraege)
            eintraege[ziel] = {"id": ziel, "klasse": self._klasse(klasse),
                               "grob": self.kategorien.grob(klasse),
                               "herkunft": "eingriff:polygon_zuweisen"}
        karte[maske] = ziel
        if not _zusammenhaengend(karte == ziel):
            raise EingriffFehler(f"Segment {ziel} wäre nicht zusammenhängend; Polygon muss angrenzen")
        betroffen.discard(ziel)
        entfernt = sorted(i for i in betroffen if not (karte == i).any())
        for i in entfernt:
            del eintraege[i]
        neu = self._zerfallene_aufteilen(karte, eintraege, betroffen - set(entfernt),
                                         "polygon_zuweisen")
        return self._uebernehmen(
            karte, eintraege, "polygon_zuweisen",
            {"id": sid, "klasse": klasse, "flaeche": np.asarray(flaeche).tolist()},
            {"ziel": ziel, "bildpunkte": int(maske.sum()), "entfernt": entfernt,
             "aufgeteilt_neu": neu})

    def anwenden(self, schritt: dict) -> dict:
        """Ein Schritt als Dict, wie in einer Stapeldatei (``{"op": ..., ...}``)."""
        op = schritt.get("op")
        werte = {k: v for k, v in schritt.items() if k != "op"}
        try:
            if op == "verschmelzen":
                return self.verschmelzen(werte["ids"], werte.get("ziel"))
            if op == "teilen":
                return self.teilen(werte["id"], werte["linie"])
            if op == "grenze_verschieben":
                return self.grenze_verschieben(werte["von"], werte["nach"], werte["flaeche"])
            if op == "klasse_setzen":
                return self.klasse_setzen(werte["id"], werte["klasse"])
            if op == "polygon_zuweisen":
                return self.polygon_zuweisen(werte["flaeche"], werte.get("id"), werte.get("klasse"))
        except KeyError as fehlt:
            raise EingriffFehler(f"Schritt {op!r}: Feld {fehlt} fehlt") from None
        raise EingriffFehler(f"unbekannte Operation {op!r}")
