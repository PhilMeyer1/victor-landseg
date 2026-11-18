"""W3 ``ansicht``: Standardbilder je Teilkachel und je Segment.

Bildarten (Auswahl und Größen in ``einstellungen/ansicht.json``):

- ``roh``: das Bild ohne Zutat (je Segment: Fenster um das Segment im Maßstab 1)
- ``umriss``: alle Segmentgrenzen; je Segment das Segment selbst breit hervorgehoben; Kern als Rahmen
- ``maengel``: Bild abgedunkelt, darüber Lücke (ID 0), nicht zusammenhängend, ohne Eintrag oder
  mit ungültiger Klasse, zu klein, ``sicher: nein``, Kandidaten und geschätzte Strecken aus
  ``kante``; Legende unten
- ``vorschlag``: Segmente in der Farbe ihrer Klasse aus ``kategorien.json``, mit Klassen-Code
- ``nah``: nur je Segment: das vergrößerte Fenster, nur mit dem Umriss des Segments
- ``kontrast``: Kontrast verstärkt (CLAHE auf der Helligkeit in Lab)
- ``gitter``: Koordinatengitter, beschriftet in Bildpunkten der Teilkachel

Je Segment werden alle Arten außer ``roh`` im vergrößerten Fenster gezeichnet, um einen ganzzahligen
Faktor, so dass jeder Bildpunkt als Quadrat erscheint und Grenzen auf Bildpunktkanten liegen.
``ansicht.json`` im Zielordner führt jedes Bild mit Fenster und Faktor:
``x_teilkachel = fenster.x + x_bild // faktor`` (im Gitterbild zuerst den Rand abziehen).
"""

from __future__ import annotations

import os
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from scipy import ndimage

from . import dateien
from . import einstellungen as einstellungen_mod
from .kategorien import Kategorien
from .pruefen import pruefen

SCHEMA = "landseg-ansicht/1"
#: Arten, die ohne Label-Karte gehen.
OHNE_KARTE = ("roh", "kontrast", "gitter")
#: Mängel-Arten in Zeichenreihenfolge (spätere überdecken frühere), mit Legendentext (ASCII, weil
#: die Bildschrift keine Umlaute kennt).
MAENGEL_ARTEN = {
    "unsicher": "sicher: nein",
    "zu_klein": "zu klein",
    "ohne_eintrag": "ohne Eintrag / Klasse ungueltig",
    "nicht_zusammenhaengend": "nicht zusammenhaengend",
    "luecke": "Luecke (ID 0)",
    "geschaetzt": "Grenze geschaetzt (kante)",
}
SCHRIFT = cv2.FONT_HERSHEY_SIMPLEX


class AnsichtFehler(ValueError):
    """Eingaben passen nicht zusammen."""


@dataclass(frozen=True)
class Fenster:
    """Ausschnitt der Teilkachel (Bildpunkte) und ganzzahliger Vergrößerungsfaktor."""

    x: int
    y: int
    breite: int
    hoehe: int
    faktor: int = 1

    def als_dict(self) -> dict:
        return {"x": self.x, "y": self.y, "breite": self.breite, "hoehe": self.hoehe,
                "faktor": self.faktor}

    def schnitt(self) -> tuple[slice, slice]:
        return slice(self.y, self.y + self.hoehe), slice(self.x, self.x + self.breite)


def _rgb(hexwert: str) -> tuple[int, int, int]:
    h = hexwert.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _gross(arr: np.ndarray, faktor: int) -> np.ndarray:
    if faktor == 1:
        return arr
    return np.repeat(np.repeat(arr, faktor, axis=0), faktor, axis=1)


def grenzen(karte: np.ndarray) -> np.ndarray:
    """Bildpunkte, deren rechter oder unterer Nachbar zu einem anderen Segment gehört (1 px breit)."""
    g = np.zeros(karte.shape, bool)
    g[:, :-1] |= karte[:, :-1] != karte[:, 1:]
    g[:-1, :] |= karte[:-1, :] != karte[1:, :]
    return g


def _ring(maske: np.ndarray, breite: int) -> np.ndarray:
    """Ring der Breite ``breite`` außen um eine Maske."""
    kern = np.ones((2 * breite + 1, 2 * breite + 1), np.uint8)
    return cv2.dilate(maske.astype(np.uint8), kern).astype(bool) & ~maske


def _text(bild: np.ndarray, text: str, x: int, y: int, farbe=(255, 255, 255), groesse=0.4) -> None:
    cv2.putText(bild, text, (x, y), SCHRIFT, groesse, (0, 0, 0), 3, cv2.LINE_AA)
    cv2.putText(bild, text, (x, y), SCHRIFT, groesse, farbe, 1, cv2.LINE_AA)


def kontrast(bild: np.ndarray, clip: float, kacheln: int) -> np.ndarray:
    lab = cv2.cvtColor(bild, cv2.COLOR_RGB2LAB)
    clahe = cv2.createCLAHE(clipLimit=float(clip), tileGridSize=(int(kacheln), int(kacheln)))
    lab[:, :, 0] = clahe.apply(lab[:, :, 0])
    return cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)


def _mischen(bild: np.ndarray, maske: np.ndarray, farbe, deckkraft: float) -> None:
    bild[maske] = (bild[maske] * (1 - deckkraft) + np.asarray(farbe) * deckkraft).astype(np.uint8)


def _kandidaten_lesen(daten) -> list[dict]:
    if daten is None:
        return []
    liste = daten.get("kandidaten", []) if isinstance(daten, dict) else daten
    return [k for k in liste if isinstance(k, dict) and isinstance(k.get("id"), int)]


def _geschaetzt_lesen(daten) -> list[list[list[int]]]:
    if not daten:
        return []
    return [s.get("punkte", []) for s in daten.get("geschaetzt", [])]


class Ansicht:
    """Vorberechnete Grundbilder einer Teilkachel; zeichnet Standardbilder für beliebige Fenster."""

    def __init__(self, bild: np.ndarray, karte: np.ndarray | None, segmente: dict | None,
                 kategorien: Kategorien | None, vorgaben: dict, *, kern: dict | None = None,
                 kandidaten=None, kante=None, mindestflaeche: int | None = None):
        if bild.ndim != 3 or bild.shape[2] != 3 or bild.dtype != np.uint8:
            raise AnsichtFehler(f"Bild muss RGB uint8 sein, hat Form {bild.shape} {bild.dtype}")
        if karte is not None and karte.shape != bild.shape[:2]:
            raise AnsichtFehler(f"Label-Karte {karte.shape} passt nicht zum Bild {bild.shape[:2]}")
        self.bild = bild
        self.karte = karte
        self.v = vorgaben
        self.farben = {k: _rgb(w) for k, w in vorgaben["farben"].items()}
        self.kern = kern
        self.kategorien = kategorien
        self.eintraege = dateien.segmente_nach_id(segmente) if segmente else {}
        self.kandidaten = _kandidaten_lesen(kandidaten)
        self.grund = {"roh": bild, "kontrast": kontrast(bild, **vorgaben["kontrast"])}
        self.maengel: dict = {}
        self.mangel_masken: dict[str, np.ndarray] = {}
        if karte is not None:
            self.ids = [int(i) for i in np.unique(karte) if i != 0]
            self._maengel_ermitteln(segmente, mindestflaeche, _geschaetzt_lesen(kante))
            self.grund["maengel"] = self._maengel_grund()
            self.grund["vorschlag"] = self._vorschlag_grund()
            lagen = ndimage.find_objects(karte)
            self.lage = {sid: lagen[sid - 1] for sid in self.ids}
        else:
            self.ids = []

    # -- Grundbilder ------------------------------------------------------------------------

    def _maengel_ermitteln(self, segmente, mindestflaeche, geschaetzt) -> None:
        karte = self.karte
        befund = pruefen(karte, None, None, mindestflaeche=None)
        ids, flaechen = np.unique(karte, return_counts=True)
        flaeche = dict(zip(ids.tolist(), flaechen.tolist()))
        ohne_eintrag = []
        if segmente is not None:
            for sid in self.ids:
                eintrag = self.eintraege.get(sid)
                if eintrag is None or (self.kategorien is not None
                                       and not self.kategorien.gueltig(eintrag.get("klasse"))):
                    ohne_eintrag.append(sid)
        unsicher = [sid for sid in self.ids
                    if self.eintraege.get(sid, {}).get("sicher") in ("nein", False)]
        zu_klein = ([sid for sid in self.ids if flaeche[sid] < mindestflaeche]
                    if mindestflaeche else [])
        geschaetzt_maske = np.zeros(karte.shape, bool)
        for punkte in geschaetzt:
            for x, y in punkte:
                if 0 <= y < karte.shape[0] and 0 <= x < karte.shape[1]:
                    geschaetzt_maske[y, x] = True
        self.mangel_masken = {
            "unsicher": np.isin(karte, unsicher),
            "zu_klein": np.isin(karte, zu_klein),
            "ohne_eintrag": np.isin(karte, ohne_eintrag),
            "nicht_zusammenhaengend": np.isin(karte, befund.nicht_zusammenhaengend),
            "luecke": karte == 0,
            "geschaetzt": geschaetzt_maske,
        }
        self.maengel = {
            "luecke_bildpunkte": int(befund.ohne_segment),
            "nicht_zusammenhaengend": befund.nicht_zusammenhaengend,
            "ohne_eintrag": ohne_eintrag,
            "zu_klein": zu_klein,
            "unsicher": unsicher,
            "kandidaten": self.kandidaten,
            "geschaetzt_strecken": len(geschaetzt),
            "geschaetzt_bildpunkte": int(geschaetzt_maske.sum()),
        }
        self.segment_maengel: dict[int, list[str]] = {}
        for art in ("unsicher", "zu_klein", "ohne_eintrag", "nicht_zusammenhaengend"):
            for sid in self.maengel[art]:
                self.segment_maengel.setdefault(sid, []).append(art)
        for k in self.kandidaten:
            self.segment_maengel.setdefault(k["id"], []).append(f"kandidat: {k.get('grund', '')}")

    def _maengel_grund(self) -> np.ndarray:
        bild = (self.bild * float(self.v["maengel_abdunkeln"])).astype(np.uint8)
        for art in MAENGEL_ARTEN:
            maske = self.mangel_masken[art]
            if maske.any():
                deck = 1.0 if art in ("luecke", "geschaetzt") else float(self.v["maengel_deckkraft"])
                _mischen(bild, maske, self.farben[art], deck)
        return bild

    def _vorschlag_grund(self) -> np.ndarray:
        palette: dict[int, tuple[int, int, int]] = {}
        for sid in self.ids:
            code = self.eintraege.get(sid, {}).get("klasse")
            farbe = self.farben["ohne_klasse"]
            if self.kategorien is not None and self.kategorien.gueltig(code):
                farbe = _rgb(self.kategorien.klassen[code].get("color", self.v["farben"]["ohne_klasse"]))
            palette[sid] = farbe
        if not palette:
            return self.bild.copy()
        ids = np.fromiter(palette, dtype=np.int64)
        farben = np.asarray([palette[i] for i in palette], np.float32)
        index = np.searchsorted(ids, self.karte)
        index = np.clip(index, 0, len(ids) - 1)
        treffer = ids[index] == self.karte
        flaeche = np.where(treffer[..., None], farben[index], self.bild.astype(np.float32))
        deck = float(self.v["vorschlag_deckkraft"])
        return (self.bild * (1 - deck) + flaeche * deck).astype(np.uint8)

    # -- Fenster ----------------------------------------------------------------------------

    def segment_fenster(self, sid: int) -> Fenster:
        ys, xs = self.lage[sid]
        rand, mindest = int(self.v["segment_rand"]), int(self.v["segment_mindestfenster"])
        hoehe_bild, breite_bild = self.karte.shape

        def spanne(a: int, b: int, laenge: int) -> tuple[int, int]:
            a, b = a - rand, b + rand
            if b - a < mindest:
                mitte = (a + b) // 2
                a, b = mitte - mindest // 2, mitte - mindest // 2 + mindest
            a, b = max(0, a), min(laenge, b)
            return a, b

        x0, x1 = spanne(xs.start, xs.stop, breite_bild)
        y0, y1 = spanne(ys.start, ys.stop, hoehe_bild)
        groesste = max(x1 - x0, y1 - y0)
        faktor = max(1, min(int(self.v["nah_hoechstfaktor"]),
                            int(self.v["nah_zielgroesse"]) // groesste))
        return Fenster(x0, y0, x1 - x0, y1 - y0, faktor)

    def ganz(self) -> Fenster:
        return Fenster(0, 0, self.bild.shape[1], self.bild.shape[0], 1)

    # -- Zeichnen ---------------------------------------------------------------------------

    def _karte_im(self, f: Fenster) -> np.ndarray:
        return _gross(self.karte[f.schnitt()], f.faktor)

    def _segment_umriss(self, bild: np.ndarray, karte: np.ndarray, sid: int, f: Fenster) -> None:
        breite = 1 if f.faktor < 3 else 2
        bild[_ring(karte == sid, breite)] = self.farben["segment"]

    def _kern_rahmen(self, bild: np.ndarray, f: Fenster, versatz=(0, 0)) -> None:
        if not self.kern:
            return
        k = self.kern
        x0 = (k["x"] - f.x) * f.faktor + versatz[0]
        y0 = (k["y"] - f.y) * f.faktor + versatz[1]
        x1 = x0 + k["breite"] * f.faktor - 1
        y1 = y0 + k["hoehe"] * f.faktor - 1
        cv2.rectangle(bild, (x0, y0), (x1, y1), self.farben["kern"], 1, cv2.LINE_4)

    def _beschriften(self, bild: np.ndarray, f: Fenster, text=None, ab: int | None = None,
                     groesse: float = 0.4) -> list[dict]:
        """Text je ausreichend großem Segment (Standard: Klassen-Code, ``text(id)`` sonst), an der Stelle
        größten Randabstands; gibt die Stellen in Bildpunkten der Teilkachel zurück."""
        ab = int(self.v["vorschlag_beschriftung_ab"]) if ab is None else ab
        karte = self.karte[f.schnitt()]
        orte = []
        for sid in np.unique(karte).tolist():
            maske = karte == sid
            if sid == 0 or maske.sum() * f.faktor ** 2 < ab:
                continue
            inhalt = str(self.eintraege.get(sid, {}).get("klasse", "?")) if text is None else text(sid)
            abstand = ndimage.distance_transform_edt(np.pad(maske, 1))[1:-1, 1:-1]
            y, x = np.unravel_index(int(np.argmax(abstand)), abstand.shape)
            px, py = int((x + 0.5) * f.faktor), int((y + 0.5) * f.faktor)
            halb, hoch = round(10 * groesse * len(inhalt)), round(10 * groesse)
            # ganz im Bild halten (Segmente am Rand des Fensters)
            tx = min(max(2, px - halb), max(2, bild.shape[1] - 2 * halb - 2))
            ty = min(max(2 * hoch + 2, py + hoch), bild.shape[0] - 3)
            _text(bild, inhalt, tx, ty, groesse=groesse)
            orte.append({"id": int(sid), "x": f.x + int(x), "y": f.y + int(y)})
        return orte

    def _legende(self, bild: np.ndarray) -> np.ndarray:
        eintraege = [(self.farben[a], t) for a, t in MAENGEL_ARTEN.items()
                     if self.mangel_masken.get(a) is not None and self.mangel_masken[a].any()]
        if self.kandidaten:
            eintraege.append((self.farben["kandidat"], "Kandidat (Umriss)"))
        if not eintraege:
            eintraege.append(((200, 200, 200), "keine Maengel"))
        zeile = 16
        streifen = np.zeros((zeile * len(eintraege) + 4, bild.shape[1], 3), np.uint8)
        for i, (farbe, text) in enumerate(eintraege):
            y = 2 + i * zeile
            cv2.rectangle(streifen, (4, y + 2), (14, y + 12), farbe, -1)
            _text(streifen, text, 20, y + 12)
        return np.vstack([bild, streifen])

    def _gitter(self, bild: np.ndarray, f: Fenster) -> np.ndarray:
        stufen = sorted(int(s) for s in self.v["gitter_stufen"])
        ziel = int(self.v["gitter_linien_ziel"])
        groesste = max(f.breite, f.hoehe)
        schritt = next((s for s in stufen if groesste / s <= ziel), stufen[-1])
        links, oben = 40, 16
        h, w = bild.shape[:2]
        aus = np.zeros((h + oben, w + links, 3), np.uint8)
        aus[oben:, links:] = bild
        farbe = self.farben["gitter"]
        for wert in range((f.x // schritt) * schritt, f.x + f.breite + 1, schritt):
            if wert < f.x:
                continue
            px = links + (wert - f.x) * f.faktor
            cv2.line(aus, (px, oben), (px, oben + h - 1), farbe, 1, cv2.LINE_4)
            _text(aus, str(wert), px - 4 * len(str(wert)), 12, farbe, 0.35)
        for wert in range((f.y // schritt) * schritt, f.y + f.hoehe + 1, schritt):
            if wert < f.y:
                continue
            py = oben + (wert - f.y) * f.faktor
            cv2.line(aus, (links, py), (links + w - 1, py), farbe, 1, cv2.LINE_4)
            _text(aus, str(wert), 2, py + 4, farbe, 0.35)
        return aus

    def zeichnen(self, art: str, f: Fenster, sid: int | None = None) -> np.ndarray:
        if art == "nah" and sid is None:
            raise AnsichtFehler("Bildart 'nah' gibt es nur je Segment")
        if self.karte is None and art not in OHNE_KARTE:
            raise AnsichtFehler(f"Bildart {art!r} braucht eine Label-Karte")
        grund = {"nah": "roh", "umriss": "roh", "gitter": "roh"}.get(art, art)
        if grund not in self.grund:
            raise AnsichtFehler(f"unbekannte Bildart {art!r}")
        bild = _gross(self.grund[grund][f.schnitt()], f.faktor).copy()
        karte = self._karte_im(f) if self.karte is not None else None
        if art in ("umriss", "maengel", "vorschlag"):
            farbe = self.farben["grenze"] if art == "umriss" else (40, 40, 40)
            bild[grenzen(karte)] = farbe
        if art == "maengel":
            for k in self.kandidaten:
                if (karte == k["id"]).any():
                    bild[_ring(karte == k["id"], 1)] = self.farben["kandidat"]
        if art == "vorschlag":
            self._beschriften(bild, f)
        if sid is not None and karte is not None and art != "roh":
            self._segment_umriss(bild, karte, sid, f)
        if art in ("umriss",):
            self._kern_rahmen(bild, f)
        if art == "maengel":
            bild = self._legende(bild)
        if art == "gitter":
            bild = self._gitter(bild, f)
        return bild


def _speichern(pfad: Path, bild: np.ndarray) -> None:
    pfad.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(bild).save(pfad, optimize=False)


def ansicht(bild: np.ndarray, karte: np.ndarray | None, ziel: str | Path, *,
            segmente: dict | None = None, kategorien: Kategorien | None = None,
            kern: dict | None = None, ids: list[int] | None = None, nur_teilkachel: bool = False,
            kandidaten=None, kante=None, mindestflaeche: int | None = None,
            vorgaben: dict | None = None, quelle: dict | None = None) -> dict:
    """Schreibt die Standardbilder nach ``ziel`` und gibt den Inhalt von ``ansicht.json`` zurück."""
    vorgaben = vorgaben or einstellungen_mod.laden("ansicht")
    ziel = Path(ziel)
    a = Ansicht(bild, karte, segmente, kategorien, vorgaben, kern=kern, kandidaten=kandidaten,
                kante=kante, mindestflaeche=mindestflaeche)
    auftraege: list[tuple[Path, str, Fenster, int | None]] = []
    teil_arten = [x for x in vorgaben["teilkachel_arten"] if karte is not None or x in OHNE_KARTE]
    index = {
        "schema": SCHEMA,
        "quelle": quelle or {},
        "koordinaten": "x_teilkachel = fenster.x + x_bild // faktor; im Gitterbild vorher 40 px "
                       "links und 16 px oben abziehen; im Mängelbild steht die Legende unten",
        "teilkachel": {"fenster": a.ganz().als_dict(), "bilder": {}},
        "maengel": a.maengel,
        "segmente": [],
    }
    for art in teil_arten:
        rel = f"teilkachel/{art}.png"
        index["teilkachel"]["bilder"][art] = rel
        auftraege.append((ziel / rel, art, a.ganz(), None))
    if karte is not None and not nur_teilkachel:
        gewaehlt = a.ids if ids is None else [i for i in ids if i in a.lage]
        fehlend = sorted(set(ids or []) - set(a.lage))
        if fehlend:
            raise AnsichtFehler(f"Segmente nicht in der Label-Karte: {fehlend}")
        for sid in gewaehlt:
            f = a.segment_fenster(sid)
            eintrag = {"id": sid, "klasse": a.eintraege.get(sid, {}).get("klasse"),
                       "flaeche": int((karte[f.schnitt()] == sid).sum()),
                       "maengel": a.segment_maengel.get(sid, []), "fenster": f.als_dict(),
                       "bilder": {}}
            for art in vorgaben["segment_arten"]:
                rel = f"segmente/{sid}/{art}.png"
                eintrag["bilder"][art] = rel
                fenster = Fenster(f.x, f.y, f.breite, f.hoehe, 1) if art == "roh" else f
                auftraege.append((ziel / rel, art, fenster, sid))
            index["segmente"].append(eintrag)

    def erledigen(auftrag) -> None:
        pfad, art, fenster, sid = auftrag
        _speichern(pfad, a.zeichnen(art, fenster, sid))

    with ThreadPoolExecutor(max_workers=min(8, os.cpu_count() or 1)) as pool:
        list(pool.map(erledigen, auftraege))
    index["bilderzahl"] = len(auftraege)
    dateien.schreibe_json(ziel / "ansicht.json", index)
    return index
