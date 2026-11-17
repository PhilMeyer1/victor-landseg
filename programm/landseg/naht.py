"""Nahtregel: Prüfung jeder Kerngrenze zwischen benachbarten Teilkacheln.

An einer Kerngrenze stehen sich je Position zwei Bildpunkte gegenüber (links/rechts an einer
senkrechten, oben/unten an einer waagrechten Grenze). Die Regel: Beide tragen dieselbe Segment-ID,
oder zwischen ihnen liegt eine echte Bildkante (Farbsprung über ``kante_schwelle``). Eine
ID-Grenze genau auf der Kerngrenze ohne Bildkante ist ein Verstoß: Dort haben zwei Bearbeiter
dieselbe Fläche verschieden zugeordnet, oder die Grenze ist eine Gerade, die nur die Kachelung
gezogen hat. Den zweiten Teil der Regel (eine ID, die über die Grenze reicht, hat in beiden
Teilkacheln dieselbe Klasse) prüft ``zusammentragen``, weil nur es beide Abgaben kennt.

Zusammenhängende Strecken mit demselben ID-Paar werden zu einem Verstoß gebündelt. Einstellungen
(Schwelle, Band, Mindestlänge) und bestätigte Grenzen kommen aus JSON, nicht aus dem Code.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
from PIL import Image

#: Standardwerte; jede Einstellung lässt sich im Auftrag (``naht``) überschreiben.
STANDARD = {
    "kante_schwelle": 25.0,  # kleinster Farbabstand (RGB, euklidisch) für eine echte Bildkante
    "kante_band": 1,         # die Kante darf so viele Bildpunkte neben der Kerngrenze liegen
    "mindestlaenge": 1,      # kürzere Verstoß-Strecken zählen nur in ``kurz``
}


def einstellungen(werte: dict | None) -> dict:
    """Standardwerte, überschrieben mit ``werte``; unbekannte Schlüssel sind ein Fehler."""
    ergebnis = dict(STANDARD)
    for schluessel, wert in (werte or {}).items():
        if schluessel not in STANDARD:
            raise ValueError(f"Naht-Einstellung {schluessel!r} unbekannt (erlaubt: {', '.join(STANDARD)})")
        if isinstance(wert, bool) or not isinstance(wert, (int, float)) or wert < 0:
            raise ValueError(f"Naht-Einstellung {schluessel!r} braucht eine Zahl >= 0, hat {wert!r}")
        ergebnis[schluessel] = wert
    for ganz in ("kante_band", "mindestlaenge"):
        if int(ergebnis[ganz]) != ergebnis[ganz]:
            raise ValueError(f"Naht-Einstellung {ganz!r} muss ganzzahlig sein")
        ergebnis[ganz] = int(ergebnis[ganz])
    ergebnis["mindestlaenge"] = max(1, ergebnis["mindestlaenge"])
    return ergebnis


def naht_name(a: str, b: str) -> str:
    return f"{a}|{b}"


def grenzen(manifest: dict) -> list[dict]:
    """Je Paar benachbarter Teilkacheln die gemeinsame Kerngrenze, in Ausschnitt-Koordinaten.

    ``lage`` ist die erste Spalte (senkrecht) bzw. Zeile (waagrecht) der zweiten Teilkachel,
    ``von``/``bis`` der Bereich entlang der Grenze (``bis`` ausschließlich).
    """
    nach_ort = {(t["zeile"], t["spalte"]): t for t in manifest["teilkacheln"]}
    ergebnis = []
    for t in manifest["teilkacheln"]:
        kern = t["kern"]
        rechts = nach_ort.get((t["zeile"], t["spalte"] + 1))
        if rechts is not None:
            ergebnis.append({"naht": naht_name(t["id"], rechts["id"]), "a": t["id"], "b": rechts["id"],
                             "richtung": "senkrecht", "lage": rechts["kern"]["x"],
                             "von": kern["y"], "bis": kern["y"] + kern["hoehe"]})
        unten = nach_ort.get((t["zeile"] + 1, t["spalte"]))
        if unten is not None:
            ergebnis.append({"naht": naht_name(t["id"], unten["id"]), "a": t["id"], "b": unten["id"],
                             "richtung": "waagrecht", "lage": unten["kern"]["y"],
                             "von": kern["x"], "bis": kern["x"] + kern["breite"]})
    return ergebnis


def lese_bild(pfad: str | Path) -> np.ndarray:
    """Bild als float32 H × W × Kanäle (Graustufen mit einem Kanal)."""
    with Image.open(pfad) as bild:
        if bild.mode not in ("L", "RGB"):
            bild = bild.convert("RGB")
        daten = np.asarray(bild, dtype=np.float32)
    return daten[:, :, None] if daten.ndim == 2 else daten


def kantenstaerke(bild: np.ndarray, grenze: dict, band: int) -> np.ndarray:
    """Größter Farbsprung quer zur Grenze je Position, im Band ``lage ± band``."""
    if grenze["richtung"] == "senkrecht":
        streifen = bild[grenze["von"]:grenze["bis"], :, :]          # Zeilen entlang, Spalten quer
    else:
        streifen = bild[:, grenze["von"]:grenze["bis"], :].transpose(1, 0, 2)
    quer = streifen.shape[1]
    staerke = np.zeros(streifen.shape[0], np.float32)
    for versatz in range(-band, band + 1):
        stelle = grenze["lage"] + versatz
        if 1 <= stelle < quer:
            sprung = np.linalg.norm(streifen[:, stelle] - streifen[:, stelle - 1], axis=-1)
            np.maximum(staerke, sprung, out=staerke)
    return staerke


def gegenueber(karte: np.ndarray, grenze: dict) -> tuple[np.ndarray, np.ndarray]:
    von, bis, lage = grenze["von"], grenze["bis"], grenze["lage"]
    if grenze["richtung"] == "senkrecht":
        return karte[von:bis, lage - 1], karte[von:bis, lage]
    return karte[lage - 1, von:bis], karte[lage, von:bis]


def _ort(grenze: dict, i: int) -> list[int]:
    """[x, y] der Position ``i`` auf der Seite der zweiten Teilkachel."""
    if grenze["richtung"] == "senkrecht":
        return [grenze["lage"], grenze["von"] + i]
    return [grenze["von"] + i, grenze["lage"]]


def _strecken(maske: np.ndarray, a: np.ndarray, b: np.ndarray) -> list[tuple[int, int]]:
    """(Anfang, Ende ausschließlich) je zusammenhängender Strecke mit gleichem ID-Paar."""
    strecken = []
    anfang = None
    for i in range(len(maske) + 1):
        weiter = (i < len(maske) and maske[i] and anfang is not None
                  and a[i] == a[anfang] and b[i] == b[anfang])
        if anfang is not None and not weiter:
            strecken.append((anfang, i))
            anfang = None
        if anfang is None and i < len(maske) and maske[i]:
            anfang = i
    return strecken


@dataclass
class NahtBefund:
    einstellungen: dict
    naehte: list[dict] = field(default_factory=list)
    verstoesse: list[dict] = field(default_factory=list)
    bestaetigt: list[dict] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.verstoesse

    def als_dict(self) -> dict:
        return {"ok": self.ok, "einstellungen": self.einstellungen, "naehte": self.naehte,
                "verstoesse": self.verstoesse, "bestaetigt": self.bestaetigt}

    def als_text(self) -> list[str]:
        positionen = sum(n["positionen"] for n in self.naehte)
        zeilen = [f"Nähte: {len(self.naehte)} Kerngrenzen, {positionen} Positionen, "
                  f"Verstöße: {len(self.verstoesse)}, bestätigt: {len(self.bestaetigt)}"]
        for v in self.verstoesse:
            zeilen.append("- " + verstoss_text(v))
        return zeilen


def verstoss_text(v: dict) -> str:
    if v["art"] == "klasse":
        klassen = ", ".join(f"{k} {c!r}" for k, c in v["klassen"].items())
        return f"Naht {'/'.join(v['naehte']) or '-'}: Segment {v['id']} hat verschiedene Klassen ({klassen})"
    return (f"Naht {v['naht']}: Segmente {v['ids'][0]} | {v['ids'][1]} grenzen ohne Bildkante aneinander, "
            f"{v['laenge']} Bildpunkte von x {v['von'][0]}, y {v['von'][1]} bis x {v['bis'][0]}, y {v['bis'][1]}")


def _ist_bestaetigt(verstoss: dict, bestaetigt: list[dict]) -> dict | None:
    for eintrag in bestaetigt:
        if eintrag.get("naht") == verstoss["naht"] and sorted(eintrag.get("ids", [])) == sorted(verstoss["ids"]):
            return eintrag
    return None


def pruefe_naehte(karte: np.ndarray, manifest: dict, bild: np.ndarray, werte: dict | None = None,
                  bestaetigt: list[dict] | None = None) -> NahtBefund:
    """Prüft die Nahtregel auf der Label-Karte des ganzen Ausschnitts.

    ``bestaetigt``: Einträge ``{"naht": "r0c0|r0c1", "ids": [a, b], "grund": "..."}`` für Grenzen,
    die ein Bearbeiter am Bild als echt bestätigt hat, obwohl der Farbsprung unter der Schwelle liegt.
    """
    einst = einstellungen(werte)
    if bild.shape[:2] != karte.shape:
        raise ValueError(f"Bild {bild.shape[1]} × {bild.shape[0]} und Label-Karte "
                         f"{karte.shape[1]} × {karte.shape[0]} sind nicht gleich groß")
    befund = NahtBefund(einstellungen=einst)
    for grenze in grenzen(manifest):
        a, b = gegenueber(karte, grenze)
        kante = kantenstaerke(bild, grenze, einst["kante_band"])
        verschieden = a != b
        ohne_kante = verschieden & (kante < einst["kante_schwelle"])
        kurz = 0
        verstoesse = 0
        for anfang, ende in _strecken(ohne_kante, a, b):
            if ende - anfang < einst["mindestlaenge"]:
                kurz += 1
                continue
            verstoss = {"art": "ohne_kante", "naht": grenze["naht"],
                        "ids": [int(a[anfang]), int(b[anfang])], "laenge": ende - anfang,
                        "von": _ort(grenze, anfang), "bis": _ort(grenze, ende - 1),
                        "kante_max": round(float(kante[anfang:ende].max()), 1)}
            beleg = _ist_bestaetigt(verstoss, bestaetigt or [])
            if beleg is not None:
                befund.bestaetigt.append({**verstoss, "grund": beleg.get("grund")})
            else:
                befund.verstoesse.append(verstoss)
                verstoesse += 1
        befund.naehte.append({
            "naht": grenze["naht"], "richtung": grenze["richtung"], "lage": grenze["lage"],
            "positionen": int(len(a)), "gleiche_id": int((~verschieden).sum()),
            "andere_id_mit_kante": int((verschieden & ~ohne_kante).sum()),
            "ohne_kante": int(ohne_kante.sum()), "verstoesse": verstoesse, "kurz": kurz,
        })
    return befund
