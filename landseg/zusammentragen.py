"""W7 ``zusammentragen``: Abgaben der Teilkacheln zur Label-Karte des ganzen Ausschnitts fügen.

Alles Fallbezogene steht im Auftrag (``zusammentragen.json``), nichts im Code::

    {"schema": "landseg-zusammentragen/1",
     "manifest": "manifest.json",                 # von ``kacheln``
     "ausgang": "vorstufe/segmente.json",         # optional: IDs darin sind global
     "einheiten": [{"teilkachel": "r0c0", "labels": "r0c0/labels.tif",
                    "segmente": "r0c0/segmente.json", "runde": 0, "name": "umsetzen-r0c0"}, ...],
     "nutzerklassen": [{"id": 17, "klasse": "3.1.1", "kommentar": "..."}],
     "fragen": [{"id": "F1", "text": "...", "segmente": [17, 18]}],
     "naht": {"kante_schwelle": 25, "kante_band": 1, "mindestlaenge": 1},
     "naht_bestaetigt": [{"naht": "r0c0|r0c1", "ids": [3, 7], "grund": "..."}],
     "ziel": "zusammen"}

Pfade sind relativ zum Ordner des Auftrags. Je Teilkachel gilt die Einheit mit der höchsten
``runde`` (Korrekturrunden ersetzen frühere Stände). Aus jeder Abgabe zählt nur der Kern; die
Label-Karte einer Einheit hat die Größe des Teilkachelbilds (Kern + Kontext) oder nur des Kerns.

IDs: Mit ``ausgang`` sind dessen IDs global (aus der Vorstufe, in allen Teilkacheln gleich); eine
andere ID, die mehrere Teilkacheln neu angelegt haben, bekommt außer in der ersten eine neue Nummer
(``umbenannt``). Ohne ``ausgang`` gelten alle IDs als global.

Ergebnis im Ordner ``ziel``: ``labels.tif`` (ganzer Ausschnitt), ``segmente.json`` (je Segment ein
Eintrag mit ``teilkacheln``, dazu ``fragen`` und ``verlauf``) und ``naht.json`` (Nahtbefund,
Klassenkonflikte, Umbenennungen, Mängel, Befund von ``pruefen``).
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from . import dateien
from .kategorien import Kategorien
from .naht import NahtBefund, gegenueber, grenzen, lese_bild, pruefe_naehte, verstoss_text
from .pruefen import Befund, pruefen

SCHEMA = "landseg-zusammentragen/1"


class ZusammenFehler(Exception):
    pass


def _liste(auftrag: dict, schluessel: str, pfad: Path) -> list:
    wert = auftrag.get(schluessel, [])
    if not isinstance(wert, list):
        raise ZusammenFehler(f"{pfad}: Feld {schluessel!r} muss eine Liste sein")
    return wert


def _ganzzahl(wert: object) -> bool:
    return isinstance(wert, int) and not isinstance(wert, bool)


def lese_auftrag(pfad: str | Path) -> dict:
    """Liest und prüft den Auftrag; Fehler im Aufbau melden die Stelle."""
    pfad = Path(pfad)
    auftrag = dateien.lese_json(pfad)
    for pflicht in ("manifest", "einheiten", "ziel"):
        if not isinstance(auftrag.get(pflicht), (str, list)) or not auftrag.get(pflicht):
            raise ZusammenFehler(f"{pfad}: Feld {pflicht!r} fehlt oder ist leer")
    for nr, einheit in enumerate(_liste(auftrag, "einheiten", pfad), 1):
        for pflicht in ("teilkachel", "labels", "segmente"):
            if not isinstance(einheit.get(pflicht), str) or not einheit[pflicht]:
                raise ZusammenFehler(f"{pfad}: Einheit {nr} ohne {pflicht!r}")
        runde = einheit.get("runde", 0)
        if not _ganzzahl(runde) or runde < 0:
            raise ZusammenFehler(f"{pfad}: Einheit {nr} hat ungültige Runde {runde!r}")
    for nr, eintrag in enumerate(_liste(auftrag, "nutzerklassen", pfad), 1):
        if not _ganzzahl(eintrag.get("id")) or not isinstance(eintrag.get("klasse"), str):
            raise ZusammenFehler(f"{pfad}: Nutzerklasse {nr} braucht 'id' (Zahl) und 'klasse' (Code)")
    for nr, frage in enumerate(_liste(auftrag, "fragen", pfad), 1):
        if (not isinstance(frage.get("id"), str) or not isinstance(frage.get("text"), str)
                or not isinstance(frage.get("segmente"), list)
                or not all(_ganzzahl(s) for s in frage["segmente"])):
            raise ZusammenFehler(f"{pfad}: Frage {nr} braucht 'id', 'text' und 'segmente' (Liste von IDs)")
    for nr, eintrag in enumerate(_liste(auftrag, "naht_bestaetigt", pfad), 1):
        if not isinstance(eintrag.get("naht"), str) or not isinstance(eintrag.get("ids"), list):
            raise ZusammenFehler(f"{pfad}: naht_bestaetigt {nr} braucht 'naht' und 'ids'")
    if auftrag.get("schema", SCHEMA) != SCHEMA:
        raise ZusammenFehler(f"{pfad}: Schema {auftrag['schema']!r}, erwartet {SCHEMA!r}")
    return auftrag


def kern_ausschneiden(karte: np.ndarray, teilkachel: dict) -> np.ndarray:
    """Kern einer Abgabe: aus dem Teilkachelbild (Kern + Kontext) oder schon nur der Kern."""
    kern, im_bild, kontext = teilkachel["kern"], teilkachel["kern_im_bild"], teilkachel["kontext"]
    if karte.shape == (kontext["hoehe"], kontext["breite"]):
        return karte[im_bild["y"]:im_bild["y"] + kern["hoehe"], im_bild["x"]:im_bild["x"] + kern["breite"]]
    if karte.shape == (kern["hoehe"], kern["breite"]):
        return karte
    raise ZusammenFehler(
        f"Teilkachel {teilkachel['id']}: Label-Karte {karte.shape[1]} × {karte.shape[0]} passt weder "
        f"zum Teilkachelbild ({kontext['breite']} × {kontext['hoehe']}) noch zum Kern "
        f"({kern['breite']} × {kern['hoehe']})")


@dataclass
class Ergebnis:
    ziel: Path
    karte: np.ndarray
    segmente: dict
    naht: NahtBefund
    pruefung: Befund
    einheiten: dict[str, dict] = field(default_factory=dict)
    klassen_konflikte: list[dict] = field(default_factory=list)
    umbenannt: list[dict] = field(default_factory=list)
    maengel: list[str] = field(default_factory=list)

    @property
    def verstoesse(self) -> list[dict]:
        return self.klassen_konflikte + self.naht.verstoesse

    @property
    def ok(self) -> bool:
        return not self.maengel and not self.verstoesse and self.pruefung.ok

    def als_dict(self) -> dict:
        return {
            "ok": self.ok,
            "ziel": self.ziel.as_posix(),
            "einheiten": self.einheiten,
            "umbenannt": self.umbenannt,
            "maengel": self.maengel,
            "verstoesse": self.verstoesse,
            "naht": self.naht.als_dict(),
            "klassen_konflikte": self.klassen_konflikte,
            "pruefen": self.pruefung.als_dict(),
        }

    def als_text(self) -> str:
        runden = ", ".join(f"{k} Runde {e['runde']}" for k, e in self.einheiten.items())
        zeilen = [f"Zusammengetragen: {len(self.einheiten)} Teilkacheln ({runden}) -> {self.ziel.as_posix()}",
                  f"Umbenannt: {len(self.umbenannt)} neue IDs, Klassenkonflikte: {len(self.klassen_konflikte)}"]
        zeilen.extend(f"- {verstoss_text(k)}" for k in self.klassen_konflikte)
        zeilen.extend(self.naht.als_text())
        zeilen.extend(f"- Mangel: {m}" for m in self.maengel)
        zeilen.append(self.pruefung.als_text())
        zeilen.append("Zusammentragen ok" if self.ok else
                      f"Zusammentragen FEHLER: {len(self.verstoesse)} Nahtverstöße, "
                      f"{len(self.maengel)} Mängel, pruefen {'ok' if self.pruefung.ok else 'FEHLER'}")
        return "\n".join(zeilen)


def _einheiten_waehlen(auftrag: dict, teilkacheln: dict[str, dict]) -> dict[str, dict]:
    gewaehlt: dict[str, dict] = {}
    for einheit in auftrag["einheiten"]:
        tid = einheit["teilkachel"]
        if tid not in teilkacheln:
            raise ZusammenFehler(f"Einheit für unbekannte Teilkachel {tid!r} (Manifest kennt "
                                 f"{', '.join(teilkacheln)})")
        runde = einheit.get("runde", 0)
        bisher = gewaehlt.get(tid)
        if bisher is not None and bisher.get("runde", 0) == runde:
            raise ZusammenFehler(f"Teilkachel {tid}: zwei Einheiten in Runde {runde}")
        if bisher is None or bisher.get("runde", 0) < runde:
            gewaehlt[tid] = einheit
    return gewaehlt


def zusammentragen(auftrag_pfad: str | Path, kategorien: Kategorien,
                   ziel: str | Path | None = None, bearbeiter: str = "zusammentragen") -> Ergebnis:
    """Fügt die Abgaben zusammen, prüft Nähte und Karte und schreibt das Ergebnis nach ``ziel``."""
    auftrag_pfad = Path(auftrag_pfad).resolve()
    basis = auftrag_pfad.parent
    auftrag = lese_auftrag(auftrag_pfad)
    manifest_pfad = (basis / auftrag["manifest"]).resolve()
    manifest = dateien.lese_json(manifest_pfad)
    teilkacheln = {t["id"]: t for t in manifest["teilkacheln"]}
    hoehe, breite = manifest["ausschnitt"]["hoehe"], manifest["ausschnitt"]["breite"]
    ziel = Path(ziel).resolve() if ziel else (basis / auftrag["ziel"]).resolve()
    maengel: list[str] = []

    global_ids = None
    if auftrag.get("ausgang"):
        global_ids = set(dateien.segmente_nach_id(dateien.lese_segmente(basis / auftrag["ausgang"])))

    # 1. Kerne und Einträge je Teilkachel lesen
    gewaehlt = _einheiten_waehlen(auftrag, teilkacheln)
    gelesen = []
    hoechste = max(global_ids) if global_ids else 0
    for tid, tk in teilkacheln.items():
        einheit = gewaehlt.get(tid)
        if einheit is None:
            maengel.append(f"Teilkachel {tid}: keine Einheit im Auftrag, ihr Kern bleibt leer (ID 0)")
            continue
        kern = kern_ausschneiden(dateien.lese_labels(basis / einheit["labels"]), tk).copy()
        segmente = dateien.lese_segmente(basis / einheit["segmente"])
        eintraege = dateien.segmente_nach_id(segmente)
        if kern.size:
            hoechste = max(hoechste, int(kern.max()))
        gelesen.append((tid, tk, einheit, kern, eintraege, segmente.get("verlauf", [])))

    # 2. neue (nicht globale) IDs, die mehrere Teilkacheln vergeben haben, umnummern
    karte = np.zeros((hoehe, breite), np.uint32)
    vergeben: set[int] = set()
    naechste = hoechste + 1
    umbenannt: list[dict] = []
    vorkommen: dict[int, list[tuple[str, dict | None, int]]] = {}
    for tid, tk, einheit, kern, eintraege, _ in gelesen:
        ids, flaechen = np.unique(kern, return_counts=True)
        zuordnung = {}
        for alt in ids.tolist():
            if alt == 0 or global_ids is None or alt in global_ids or alt not in vergeben:
                zuordnung[alt] = alt
            else:
                zuordnung[alt] = naechste
                umbenannt.append({"teilkachel": tid, "alt": alt, "neu": naechste})
                naechste += 1
        for alt, neu in zuordnung.items():
            if alt != neu:
                kern[kern == alt] = neu
        k = tk["kern"]
        karte[k["y"]:k["y"] + k["hoehe"], k["x"]:k["x"] + k["breite"]] = kern
        for alt, flaeche in zip(ids.tolist(), flaechen.tolist()):
            if alt == 0:
                continue
            neu = zuordnung[alt]
            vergeben.add(neu)
            eintrag = copy.deepcopy(eintraege.get(alt))
            if eintrag is not None:
                eintrag["id"] = neu
            vorkommen.setdefault(neu, []).append((tid, eintrag, flaeche))

    # 3. Einträge zusammenführen; verschiedene Klassen derselben ID sind ein Konflikt
    naht_je_id = _naehte_je_id(karte, manifest)
    zusammen: dict[int, dict] = {}
    konflikte: dict[int, dict] = {}
    for sid, liste in sorted(vorkommen.items()):
        mit_eintrag = [(tid, e, f) for tid, e, f in liste if e is not None]
        if not mit_eintrag:
            continue  # fehlender Eintrag: meldet pruefen (Schema)
        tid_gross, eintrag, _ = max(mit_eintrag, key=lambda v: v[2])
        eintrag["teilkacheln"] = sorted(tid for tid, _, _ in liste)
        klassen = {tid: e.get("klasse") for tid, e, _ in mit_eintrag}
        if len(set(klassen.values())) > 1:
            konflikte[sid] = {"art": "klasse", "id": sid, "klassen": klassen,
                              "naehte": sorted(naht_je_id.get(sid, ()))}
            eintrag["klassen_je_teilkachel"] = klassen
        zusammen[sid] = eintrag

    # 4. Klassen des Nutzers (aus dem Auftrag) entscheiden
    verlauf = [dict(e, teilkachel=tid) for tid, _, _, _, _, v in gelesen for e in v]
    jetzt = datetime.now(timezone.utc).isoformat(timespec="seconds")
    for eintrag in auftrag.get("nutzerklassen", []):
        sid, klasse = eintrag["id"], eintrag["klasse"]
        if not kategorien.gueltig(klasse):
            raise ZusammenFehler(f"Nutzerklasse für Segment {sid}: Klasse {klasse!r} gibt es nicht")
        if sid not in zusammen:
            maengel.append(f"Nutzerklasse für Segment {sid}: Segment gibt es im Ergebnis nicht")
            continue
        segment = zusammen[sid]
        alt = segment.get("klasse")
        segment.update(klasse=klasse, grob=kategorien.grob(klasse), klasse_quelle="nutzer")
        if konflikte.pop(sid, None) is not None:
            segment["klasse_entschieden"] = "nutzerklasse"
        verlauf.append({"zeit": jetzt, "bearbeiter": "nutzer", "op": "nutzerklasse", "id": sid,
                        "alt": alt, "neu": klasse, "kommentar": eintrag.get("kommentar")})

    # 5. Nähte am Bild prüfen, Fragen verorten, ganze Karte prüfen
    bild = lese_bild(manifest_pfad.parent / manifest["ausschnitt"]["bild"])
    naht = pruefe_naehte(karte, manifest, bild, auftrag.get("naht"), auftrag.get("naht_bestaetigt"))
    fragen = []
    for frage in auftrag.get("fragen", []):
        fehlend = [s for s in frage["segmente"] if s not in zusammen]
        if fehlend:
            maengel.append(f"Frage {frage['id']}: Segment {', '.join(map(str, fehlend))} gibt es im Ergebnis nicht")
        vorhanden = [s for s in frage["segmente"] if s in zusammen]
        eintrag = dict(frage)
        if vorhanden:
            ys, xs = np.nonzero(np.isin(karte, vorhanden))
            eintrag["bbox"] = [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
        fragen.append(eintrag)

    verlauf.append({"zeit": jetzt, "bearbeiter": bearbeiter, "op": "zusammentragen",
                    "einheiten": {tid: e.get("name", e["labels"]) for tid, e in gewaehlt.items()},
                    "umbenannt": umbenannt})
    segmente = {"schema": dateien.SEGMENTE_SCHEMA, "segmente": [zusammen[s] for s in sorted(zusammen)],
                "fragen": fragen, "verlauf": verlauf}
    pruefung = pruefen(karte, segmente, kategorien, form=(hoehe, breite))
    ergebnis = Ergebnis(
        ziel=ziel, karte=karte, segmente=segmente, naht=naht, pruefung=pruefung,
        einheiten={tid: {"runde": e.get("runde", 0), "labels": e["labels"], "segmente": e["segmente"]}
                   for tid, e in sorted(gewaehlt.items())},
        klassen_konflikte=list(konflikte.values()), umbenannt=umbenannt, maengel=maengel)

    dateien.schreibe_labels(ziel / "labels.tif", karte)
    dateien.schreibe_json(ziel / "segmente.json", segmente)
    dateien.schreibe_json(ziel / "naht.json", ergebnis.als_dict())
    return ergebnis


def _naehte_je_id(karte: np.ndarray, manifest: dict) -> dict[int, set[str]]:
    """ID -> Nähte, an denen sie auf beiden Seiten liegt (reicht über die Kerngrenze)."""
    ergebnis: dict[int, set[str]] = {}
    for grenze in grenzen(manifest):
        a, b = gegenueber(karte, grenze)
        for sid in np.unique(a[a == b]).tolist():
            ergebnis.setdefault(sid, set()).add(grenze["naht"])
    return ergebnis
