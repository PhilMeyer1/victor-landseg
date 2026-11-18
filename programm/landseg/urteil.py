"""urteil: ``urteil.json`` eines Urteils-Agents aus einer kurzen Liste bauen (``bauen``) und prüfen (``pruefen``).

Der Agent schreibt nur, was nur er wissen kann: je Segment Nummer, Urteil, Vorschlag, Punkte und Bilder (dazu
auf Wunsch ``was`` und ``sicher``). Teilkachel, Viertel, Bearbeiter, heutige Klasse und Schema füllt ``bauen``
aus den Daten (Manifest, Label-Karte, ``segmente.json``). Was im Kern liegt, liest es aus der **aktuellen**
Label-Karte, auch nach Nachsegmentieren.

Liste (JSON)::

    {"segmente": [[17, "nicht_sauber", "3.1", [["trennen", "Hecke bei x 120/y 80 abtrennen", 340]], ["nah_17_1.jpg"]],
                  {"id": 18, "urteil": "sauber", "was": "Acker", "sicher": false}],
     "sauber": [3, 4, 5],
     "naht": [], "unsicher": [], "nicht_geprueft": [], "offen": []}

Ein Eintrag als Liste: ``[id, urteil, vorschlag, punkte, bilder]`` (hintere Felder dürfen fehlen); als Objekt mit
``id``, ``urteil``, ``vorschlag`` (oder ``klasse_vorschlag``), ``punkte``, ``bilder``, ``was`` (oder
``was_ist_es``), ``sicher``. Ein Punkt: ``[art, text, flaeche_px]`` oder ``{"art", "text", "flaeche_px"}``, die
Nummer zählt der Befehl. ``sauber`` nennt Segmente ohne Befund ausdrücklich. Ohne ``was`` steht dort der Name der
heutigen Klasse, ohne ``sicher`` gilt ``true``. Ein Segment, das in der Liste fehlt, ergänzt der Befehl nicht,
sondern meldet es (Regel L1).

Viertel: ``v1`` oben links, ``v2`` oben rechts, ``v3`` unten links, ``v4`` unten rechts (Teilung in der Mitte des
Kerns). Ein Segment gehört zu dem Viertel, in dem die meisten seiner Kern-Bildpunkte liegen (bei Gleichstand das
erste); so steht jedes Kernsegment in genau einem Viertel.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np

from . import dateien
from .kategorien import Kategorien
from .zusammentragen import kern_ausschneiden

SCHEMA = "landseg-urteil/1"
URTEILE = ("sauber", "nicht_sauber")
PUNKTARTEN = ("fremdes", "fehlt", "trennen", "verschmelzen", "grenze", "klasse", "zu_klein", "sonstiges")
SEITEN = ("links", "rechts", "oben", "unten")
#: Viertel des Kerns: (Spalte, Zeile) der Hälften.
VIERTEL = {"v1": (0, 0), "v2": (1, 0), "v3": (0, 1), "v4": (1, 1)}
LISTEN = ("naht", "unsicher", "nicht_geprueft", "offen")


class UrteilFehler(ValueError):
    """Eingaben passen nicht zusammen (Aufruf, Liste); Befunde der Prüfung sind keine Ausnahme."""


@dataclass
class Grundlage:
    """Was der Befehl aus den Daten kennt: Kernsegmente (aktuelle Label-Karte), Klassen, Kategorien."""

    teilkachel: str
    viertel: str | None
    zuordnung: dict[int, str]          # Kernsegment -> Viertel
    eintraege: dict[int, dict]          # segmente.json nach ID (leer, wenn nicht gelesen)
    kat: Kategorien

    @property
    def soll(self) -> list[int]:
        """Segmente, die genau einmal unter ``segmente`` stehen müssen (Kern bzw. Viertel)."""
        return sorted(s for s, v in self.zuordnung.items() if self.viertel is None or v == self.viertel)


def viertel_zuordnen(kern: np.ndarray) -> dict[int, str]:
    """Kernsegment -> Viertel mit den meisten seiner Bildpunkte."""
    h, w = kern.shape
    zaehler: dict[int, list[int]] = {}
    for i, (name, (sp, ze)) in enumerate(VIERTEL.items()):
        teil = kern[ze * (h // 2):(h if ze else h // 2), sp * (w // 2):(w if sp else w // 2)]
        ids, anzahl = np.unique(teil, return_counts=True)
        for sid, n in zip(ids.tolist(), anzahl.tolist()):
            if sid:
                zaehler.setdefault(sid, [0] * len(VIERTEL))[i] = n
    namen = list(VIERTEL)
    return {sid: namen[int(np.argmax(n))] for sid, n in zaehler.items()}


def grundlage_laden(manifest: str | Path, teilkachel: str, labels: str | Path, kat: Kategorien,
                    segmente: str | Path | None = None, viertel: str | None = None) -> Grundlage:
    if viertel is not None and viertel not in VIERTEL:
        raise UrteilFehler(f"Viertel {viertel!r} unbekannt (erlaubt: {', '.join(VIERTEL)})")
    m = dateien.lese_json(manifest)
    teil = next((t for t in m["teilkacheln"] if t["id"] == teilkachel), None)
    if teil is None:
        raise UrteilFehler(f"Teilkachel {teilkachel!r} steht nicht im Manifest")
    kern = kern_ausschneiden(dateien.lese_labels(labels), teil)
    eintraege = dateien.segmente_nach_id(dateien.lese_segmente(segmente)) if segmente else {}
    return Grundlage(teilkachel, viertel, viertel_zuordnen(kern), eintraege, kat)


def _liste_lesen(eintrag, i: int, fehler: list[str]) -> dict | None:
    felder = ("id", "urteil", "vorschlag", "punkte", "bilder")
    if isinstance(eintrag, (list, tuple)) and 1 <= len(eintrag) <= len(felder):
        return dict(zip(felder, eintrag))
    if isinstance(eintrag, dict):
        werte = dict(eintrag)
        for kurz, lang in (("vorschlag", "klasse_vorschlag"), ("was", "was_ist_es")):
            if lang in werte:
                werte.setdefault(kurz, werte.pop(lang))
        return werte
    fehler.append(f"Eintrag {i}: erwartet [id, urteil, vorschlag, punkte, bilder] oder ein Objekt, hat {eintrag!r}")
    return None


def _punkt(p, nr: int) -> dict:
    if isinstance(p, (list, tuple)):
        p = dict(zip(("art", "text", "flaeche_px"), p))
    if not isinstance(p, dict):
        return {"nr": nr, "art": None, "text": str(p), "flaeche_px": None}
    return {"nr": p.get("nr", nr), "art": p.get("art"), "text": p.get("text", ""), "flaeche_px": p.get("flaeche_px")}


def bauen(g: Grundlage, liste: dict, bearbeiter: str) -> dict:
    """``urteil.json`` im Format der Vorlage ``vorlagen/urteil.md``; Formfehler der Liste als ``UrteilFehler``."""
    if not isinstance(bearbeiter, str) or not bearbeiter.strip():
        raise UrteilFehler("--bearbeiter fehlt")
    if isinstance(liste, list):
        liste = {"segmente": liste}
    if not isinstance(liste, dict):
        raise UrteilFehler("Liste: erwartet ein Objekt mit 'segmente' (und 'sauber')")
    fehler: list[str] = []
    roh = [_liste_lesen(e, i, fehler) for i, e in enumerate(liste.get("segmente") or [], 1)]
    sauber = liste.get("sauber") or []
    if not isinstance(sauber, list):
        fehler.append("'sauber' muss eine Liste von Segmentnummern sein")
        sauber = []
    roh += [{"id": sid, "urteil": "sauber"} for sid in sauber]
    segmente = []
    for werte in roh:
        if werte is None:
            continue
        sid = werte.get("id")
        if isinstance(sid, bool) or not isinstance(sid, int):
            fehler.append(f"Segmentnummer {sid!r} ist keine ganze Zahl")
            continue
        heute = g.eintraege.get(sid, {}).get("klasse")
        was = werte.get("was") or (g.kat.name(heute) if g.kat.gueltig(heute) else "")
        segmente.append({"id": sid, "klasse_heute": heute, "was_ist_es": was, "urteil": werte.get("urteil"),
                         "klasse_vorschlag": werte.get("vorschlag"),
                         "sicher": werte.get("sicher", True),
                         "punkte": [_punkt(p, nr) for nr, p in enumerate(werte.get("punkte") or [], 1)],
                         "bilder": list(werte.get("bilder") or [])})
    if fehler:
        raise UrteilFehler("; ".join(fehler))
    urteil = {"schema": SCHEMA, "teilkachel": g.teilkachel}
    if g.viertel:
        urteil["viertel"] = g.viertel
    urteil.update({"bearbeiter": bearbeiter.strip(), "segmente": sorted(segmente, key=lambda s: s["id"])})
    for name in LISTEN:
        urteil[name] = list(liste.get(name) or [])
    return urteil


def _ids(ids: list[int]) -> str:
    return ", ".join(str(i) for i in ids)


def pruefen(g: Grundlage, urteil: dict, ordner: str | Path) -> list[str]:
    """Jeder Fehler als Satz; leer = ok. Bilder relativ zu ``ordner`` (Ordner der ``urteil.json``) oder absolut."""
    fehler: list[str] = []
    if urteil.get("teilkachel") != g.teilkachel:
        fehler.append(f"Teilkachel {urteil.get('teilkachel')!r}, erwartet {g.teilkachel!r}")
    if g.viertel and urteil.get("viertel", g.viertel) != g.viertel:
        fehler.append(f"Viertel {urteil.get('viertel')!r}, erwartet {g.viertel!r}")
    if not isinstance(urteil.get("bearbeiter"), str) or not urteil["bearbeiter"].strip():
        fehler.append("'bearbeiter' fehlt")
    liste = urteil.get("segmente")
    if not isinstance(liste, list):
        return fehler + ["Liste 'segmente' fehlt"]
    gesehen: dict[int, int] = {}
    ordner = Path(ordner)
    for s in liste:
        sid = s.get("id") if isinstance(s, dict) else None
        if isinstance(sid, bool) or not isinstance(sid, int):
            fehler.append(f"Eintrag ohne ganze Segmentnummer: {s!r}"[:200])
            continue
        gesehen[sid] = gesehen.get(sid, 0) + 1
        if sid not in g.zuordnung:
            fehler.append(f"Segment {sid}: liegt nicht im Kern von {g.teilkachel} (Kontextrand oder nicht in der "
                          f"Label-Karte)")
        elif g.viertel and g.zuordnung[sid] != g.viertel:
            fehler.append(f"Segment {sid}: gehört zum Viertel {g.zuordnung[sid]}, nicht zu {g.viertel}")
        if s.get("urteil") not in URTEILE:
            fehler.append(f"Segment {sid}: Urteil {s.get('urteil')!r} (erlaubt: {', '.join(URTEILE)})")
        vorschlag = s.get("klasse_vorschlag")
        if vorschlag is not None and not g.kat.gueltig(vorschlag):
            fehler.append(f"Segment {sid}: unbekannte Klasse {vorschlag!r} (nicht in {g.kat.pfad.name})")
        if not isinstance(s.get("sicher"), bool):
            fehler.append(f"Segment {sid}: 'sicher' muss true oder false sein, hat {s.get('sicher')!r}")
        for p in s.get("punkte") or []:
            art = p.get("art") if isinstance(p, dict) else None
            if art not in PUNKTARTEN:
                fehler.append(f"Segment {sid}: unbekannte Punktart {art!r} (erlaubt: {', '.join(PUNKTARTEN)})")
            elif not str(p.get("text") or "").strip():
                fehler.append(f"Segment {sid}, Punkt {p.get('nr')}: Text fehlt")
        for bild in s.get("bilder") or []:
            if not (ordner / str(bild)).is_file():
                fehler.append(f"Segment {sid}: Bilddatei {bild} fehlt")
    doppelt = sorted(i for i, n in gesehen.items() if n > 1)
    if doppelt:
        fehler.append(f"mehr als ein Eintrag: Segment {_ids(doppelt)}")
    fehlen = [i for i in g.soll if i not in gesehen]
    if fehlen:
        wo = f"im Viertel {g.viertel}" if g.viertel else "im Kern"
        fehler.append(f"ohne Eintrag ({len(fehlen)} {wo}): {_ids(fehlen)}")
    for n in urteil.get("naht") or []:
        if not isinstance(n, dict) or n.get("seite") not in SEITEN:
            fehler.append(f"naht: Seite {n.get('seite') if isinstance(n, dict) else n!r} (erlaubt: "
                          f"{', '.join(SEITEN)})")
    return fehler
