"""einigung: Klassen an den Übergängen der Teilkacheln abgleichen (finden, anwenden, messen).

Je Fassung urteilt ein Agent je Teilkachel; an den Kerngrenzen (Nähte samt Ecken) und an den
Viertelgrenzen (Mitte jedes Kerns) stoßen deshalb Segmente aneinander, die dieselbe Fläche zeigen,
aber verschiedene Klassen tragen. Eine **Stelle** ist ein Segment-Paar, das dort ohne Bildkante
aneinandergrenzt (Bildkanten-Regel und Strecken wie ``naht``: ``kantenstaerke``, ``gegenueber``,
``_strecken``, derselbe Bildleser ``naht.lese_bild``). Ein Segment ist ``<teilkachel>:<id>``, weil
die IDs je Teilkachel vergeben sind.

- ``finden``: die offenen Stellen (verschiedene Klasse, noch nicht geeinigt), gebündelt: Segment-Paare,
  die ein Segment teilen, bleiben zusammen (eine Ecke fällt so in ein Bündel); kleine Gruppen werden
  bis ``buendel_paare`` zusammengelegt. Je Bündel ein Auftrag (``auftrag.json``) mit Bildern beider
  Seiten je Paar für einen Agent (Vorlage ``vorlagen/einigung.md``).
- ``anwenden``: setzt die Abgaben der Agents (``einigung_abgabe.json``) um; je Paar ``gleich``
  (gemeinsame Klasse der Kategorienliste der Fassung, über ``eingriff.klasse_setzen``), ``grenze``
  (nichts ändert sich, Grund wird festgehalten) oder ``unklar`` (beide ``sicher: nein``). Jedes
  beteiligte Segment bekommt einen Eintrag unter ``einigung``; Label-Karten bleiben unberührt, nur
  Segmente im Kern werden geändert, alles oder nichts.
- ``messen``: Zahl der Stellen (Paare, Strecken, Randpunkte) getrennt nach offen, unsicher, geklärt.

Einstellungen in ``einstellungen/einigung.json``; die Fassungen (Ordner, Kategorienliste) kommen aus
``einstellungen/seite.json`` wie bei der Seite.
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from . import dateien, naht
from . import kategorien as kategorien_modul
from .ansicht import _gross, _rgb, grenzen as umrisse
from .eingriff import Bearbeitung, EingriffFehler
from .kategorien import Kategorien
from .pruefen import pruefen
from .zusammentragen import kern_ausschneiden

AUFTRAG_SCHEMA = "landseg-einigung-auftrag/1"
ABGABE_SCHEMA = "landseg-einigung-abgabe/1"
ENTSCHEIDUNGEN = ("gleich", "grenze", "unklar")
STATUS = ("offen", "unsicher", "geklaert")


class EinigungFehler(Exception):
    """Abgabe oder Daten passen nicht; nichts wurde geschrieben."""


@dataclass
class Fassung:
    kennung: str
    ordner: Path
    kat: Kategorien
    manifest: dict
    basis: Path                  # Ordner des Manifests
    karten: dict[str, np.ndarray]
    segmente: dict[str, dict]


def fassung_laden(manifest_pfad: str | Path, ordner: str | Path, kat: Kategorien, kennung: str = "") -> Fassung:
    """Label-Karten und ``segmente.json`` aller Teilkacheln einer Fassung (``<ordner>/<teilkachel>/``)."""
    manifest_pfad = Path(manifest_pfad)
    manifest = dateien.lese_json(manifest_pfad)
    ordner = Path(ordner)
    karten, segmente = {}, {}
    for t in manifest["teilkacheln"]:
        tk = ordner / t["id"]
        labels = tk / "labels.tif" if (tk / "labels.tif").exists() else tk / "labels.npy"
        if not labels.exists() or not (tk / "segmente.json").exists():
            raise EinigungFehler(f"{tk}: labels.tif und segmente.json fehlen (Einigung braucht alle Teilkacheln)")
        karten[t["id"]] = dateien.lese_labels(labels)
        kern_ausschneiden(karten[t["id"]], t)  # Form früh prüfen
        segmente[t["id"]] = dateien.lese_segmente(tk / "segmente.json")
    return Fassung(kennung or ordner.name, ordner, kat, manifest, manifest_pfad.parent, karten, segmente)


def fassung_aus_einstellungen(manifest_pfad: str | Path, kennung: str, kat_standard: Kategorien,
                              fassungen: list[dict]) -> Fassung:
    """Fassung nach Kennung aus der Liste ``fassungen`` von ``einstellungen/seite.json``."""
    for e in fassungen:
        if str(e.get("kennung")) == kennung:
            ordner = Path(e["ordner"])
            ordner = ordner if ordner.is_absolute() else Path(manifest_pfad).parent / ordner
            kat = kat_standard
            if e.get("kategorien"):
                liste = Path(e["kategorien"])
                kat = kategorien_modul.laden(liste if liste.is_absolute() else ordner / liste)
            return fassung_laden(manifest_pfad, ordner, kat, kennung)
    raise EinigungFehler(f"Fassung {kennung!r} steht nicht in den Einstellungen der Seite "
                         f"({', '.join(str(e.get('kennung')) for e in fassungen)})")


def linien(manifest: dict) -> list[dict]:
    """Kerngrenzen (``art`` naht, aus ``naht.grenzen``) und Viertelgrenzen (``art`` viertel, Mitte jedes Kerns)."""
    ergebnis = [{**g, "art": "naht"} for g in naht.grenzen(manifest)]
    for t in manifest["teilkacheln"]:
        k = t["kern"]
        if k["breite"] >= 2:
            ergebnis.append({"naht": f"{t['id']}:viertel-senkrecht", "art": "viertel", "a": t["id"], "b": t["id"],
                             "richtung": "senkrecht", "lage": k["x"] + k["breite"] // 2,
                             "von": k["y"], "bis": k["y"] + k["hoehe"]})
        if k["hoehe"] >= 2:
            ergebnis.append({"naht": f"{t['id']}:viertel-waagrecht", "art": "viertel", "a": t["id"], "b": t["id"],
                             "richtung": "waagrecht", "lage": k["y"] + k["hoehe"] // 2,
                             "von": k["x"], "bis": k["x"] + k["breite"]})
    return ergebnis


def schluessel_karte(f: Fassung) -> tuple[np.ndarray, list[str]]:
    """Karte des Ausschnitts aus den Kernen, je Bildpunkt ``Teilkachel-Nr << 32 | Segment-ID``."""
    aus = f.manifest["ausschnitt"]
    gesamt = np.zeros((aus["hoehe"], aus["breite"]), np.int64)
    tks = [t["id"] for t in f.manifest["teilkacheln"]]
    for nr, t in enumerate(f.manifest["teilkacheln"]):
        k = t["kern"]
        gesamt[k["y"]:k["y"] + k["hoehe"], k["x"]:k["x"] + k["breite"]] = (
            (nr << 32) | kern_ausschneiden(f.karten[t["id"]], t).astype(np.int64))
    return gesamt, tks


def _name(tks: list[str], wert: int) -> str:
    return f"{tks[int(wert) >> 32]}:{int(wert) & 0xFFFFFFFF}"


def _teile(segment: str) -> tuple[str, int]:
    tk, sid = segment.rsplit(":", 1)
    return tk, int(sid)


def paar_name(a: str, b: str) -> str:
    return "|".join(sorted((a, b), key=_teile))


def _eintrag(f: Fassung, segment: str) -> dict:
    tk, sid = _teile(segment)
    for e in f.segmente[tk]["segmente"]:
        if e.get("id") == sid:
            return e
    raise EinigungFehler(f"Segment {segment} fehlt in {tk}/segmente.json")


def _beschluss(eintrag: dict, paar: str) -> dict | None:
    """Letzter Einigungs-Eintrag des Segments zu diesem Paar."""
    treffer = [e for e in eintrag.get("einigung") or [] if e.get("paar") == paar]
    return treffer[-1] if treffer else None


def stellen(f: Fassung, bild: np.ndarray, einst: dict) -> list[dict]:
    """Alle Segment-Paare, die an einer Kern- oder Viertelgrenze ohne Bildkante aneinandergrenzen.

    ``status``: ``offen`` (verschiedene Klasse, ohne Einigung), ``unsicher`` (verschieden, als unklar belegt),
    ``geklaert`` (geeinigt: gleiche Klasse oder bestätigte Grenze), ``None`` (gleiche Klasse ohne Einigung)."""
    regel = naht.einstellungen(einst.get("naht"))
    karte, tks = schluessel_karte(f)
    if bild.shape[:2] != karte.shape:
        raise EinigungFehler(f"Bild {bild.shape[1]} × {bild.shape[0]} und Ausschnitt "
                             f"{karte.shape[1]} × {karte.shape[0]} sind nicht gleich groß")
    paare: dict[str, dict] = {}
    for linie in linien(f.manifest):
        a, b = naht.gegenueber(karte, linie)
        kante = naht.kantenstaerke(bild, linie, regel["kante_band"])
        ohne = (a != b) & (kante < regel["kante_schwelle"])
        for anfang, ende in naht._strecken(ohne, a, b):
            if ende - anfang < regel["mindestlaenge"]:
                continue
            s1, s2 = _name(tks, a[anfang]), _name(tks, b[anfang])
            name = paar_name(s1, s2)
            p = paare.setdefault(name, {"paar": name, "segmente": name.split("|"), "art": "viertel",
                                        "strecken": [], "randpunkte": 0})
            if linie["art"] == "naht":
                p["art"] = "naht"
            p["strecken"].append({"linie": linie["naht"], "richtung": linie["richtung"], "von": naht._ort(linie, anfang),
                                  "bis": naht._ort(linie, ende - 1), "laenge": ende - anfang,
                                  "kante_max": round(float(kante[anfang:ende].max()), 1)})
            p["randpunkte"] += ende - anfang
    for p in paare.values():
        eintraege = [_eintrag(f, s) for s in p["segmente"]]
        p["klassen"] = [e.get("klasse") for e in eintraege]
        verschieden = p["klassen"][0] != p["klassen"][1]
        beschluss = _beschluss(eintraege[0], p["paar"]) or _beschluss(eintraege[1], p["paar"])
        art = beschluss.get("entscheidung") if beschluss else None
        if verschieden:
            p["status"] = {"grenze": "geklaert", "unklar": "unsicher"}.get(art, "offen")
        else:
            p["status"] = "geklaert" if beschluss else None
    return sorted(paare.values(), key=lambda p: (p["strecken"][0]["linie"], p["strecken"][0]["von"][::-1]))


def zahlen(liste: list[dict]) -> dict:
    """Paare, Strecken und Randpunkte je Status, dazu je Art (naht, viertel) die Paare je Status."""
    ergebnis = {s: {"paare": 0, "strecken": 0, "randpunkte": 0} for s in STATUS}
    nach_art = {a: {s: 0 for s in STATUS} for a in ("naht", "viertel")}
    for p in liste:
        if p["status"] is None:
            continue
        ergebnis[p["status"]]["paare"] += 1
        ergebnis[p["status"]]["strecken"] += len(p["strecken"])
        ergebnis[p["status"]]["randpunkte"] += p["randpunkte"]
        nach_art[p["art"]][p["status"]] += 1
    ohne_kante = {"paare": len(liste), "randpunkte": sum(p["randpunkte"] for p in liste)}
    return {**ergebnis, "nach_art": nach_art, "ohne_kante": ohne_kante}


def messen(f: Fassung, bild: np.ndarray, einst: dict) -> dict:
    return {"fassung": f.kennung, "ordner": str(f.ordner).replace("\\", "/"), **zahlen(stellen(f, bild, einst))}


# -- finden ---------------------------------------------------------------------------------------

def buendeln(offene: list[dict], hoechstens: int) -> list[dict]:
    """Zusammenhängende Paare (über gemeinsame Segmente) bleiben in einem Bündel; jede kleine Gruppe kommt
    in das erste Bündel, das für sie noch Platz bis ``hoechstens`` Paare hat (first-fit in der Reihenfolge
    der Linien; so nie mehr Bündel als beim Auffüllen nur des letzten). Eine größere Gruppe bleibt ganz und
    allein (``uebergross``): Jedes Segment steht so in genau einem Bündel und bekommt genau ein Urteil."""
    eltern: dict[str, str] = {}

    def wurzel(s: str) -> str:
        while eltern.setdefault(s, s) != s:
            eltern[s] = eltern[eltern[s]]
            s = eltern[s]
        return s

    for p in offene:
        eltern[wurzel(p["segmente"][0])] = wurzel(p["segmente"][1])
    gruppen: dict[str, list[dict]] = {}
    for p in offene:  # Reihenfolge von ``stellen``: entlang der Linien
        gruppen.setdefault(wurzel(p["segmente"][0]), []).append(p)
    buendel: list[dict] = []
    for gruppe in gruppen.values():
        ziel = next((b for b in buendel
                     if not b["uebergross"] and len(b["paare"]) + len(gruppe) <= hoechstens), None)
        if ziel is not None:
            ziel["paare"].extend(gruppe)
        else:
            buendel.append({"paare": list(gruppe), "uebergross": len(gruppe) > hoechstens})
    return buendel


def _schrift(groesse: int):
    """Systemschrift mit Umlauten; die eingebaute Schrift von Pillow kennt keine."""
    for name in ("segoeui.ttf", "arial.ttf", "DejaVuSans.ttf"):
        try:
            return ImageFont.truetype(name, groesse)
        except OSError:
            continue
    return ImageFont.load_default()


def _paar_bild(bild: np.ndarray, karte: np.ndarray, tks: list[str], p: dict, nr: int, f: Fassung,
               einst: dict) -> Image.Image:
    """Links das Luftbild um die Stelle, rechts dasselbe mit beiden Segmenten (Farbe a/b) und der Grenzlinie."""
    punkte = np.array([q for s in p["strecken"] for q in (s["von"], s["bis"])])
    rand = int(einst["fenster"])
    h, w = karte.shape
    x0, y0 = max(0, punkte[:, 0].min() - rand), max(0, punkte[:, 1].min() - rand)
    x1, y1 = min(w, punkte[:, 0].max() + rand + 1), min(h, punkte[:, 1].max() + rand + 1)
    foto = np.clip(bild[y0:y1, x0:x1], 0, 255).astype(np.uint8)
    if foto.shape[2] == 1:
        foto = np.repeat(foto, 3, axis=2)
    teil = karte[y0:y1, x0:x1]
    lang = max(teil.shape)
    faktor = max(1, min(int(einst["vergroesserung_max"]), int(einst["bild_seite"]) // lang, 990 // lang))
    farben = einst["farben"]
    markiert = foto.astype(np.float32)
    masken = []
    for segment, farbe in zip(p["segmente"], (farben["a"], farben["b"])):
        tk, sid = _teile(segment)
        maske = teil == ((tks.index(tk) << 32) | sid)
        markiert[maske] = (1 - einst["deckkraft"]) * markiert[maske] + einst["deckkraft"] * np.array(_rgb(farbe))
        masken.append(maske)
    links, rechts = _gross(foto, faktor), _gross(markiert.astype(np.uint8), faktor)
    gross_karte = _gross(teil, faktor)
    rechts[umrisse(gross_karte) & _gross(masken[0] | masken[1], faktor)] = _rgb(farben["umriss"])
    for s in p["strecken"]:
        (ax, ay), (bx, by) = s["von"], s["bis"]
        if s["richtung"] == "senkrecht":
            rechts[(ay - y0) * faktor:(by - y0 + 1) * faktor, max(0, (ax - x0) * faktor - 1):(ax - x0) * faktor + 1] = _rgb(farben["linie"])
        else:
            rechts[max(0, (ay - y0) * faktor - 1):(ay - y0) * faktor + 1, (ax - x0) * faktor:(bx - x0 + 1) * faktor] = _rgb(farben["linie"])
    kopf = 44
    leinwand = Image.new("RGB", (links.shape[1] * 2 + 8, links.shape[0] + kopf), (20, 20, 24))
    leinwand.paste(Image.fromarray(links), (0, kopf))
    leinwand.paste(Image.fromarray(rechts), (links.shape[1] + 8, kopf))
    zeichnen = ImageDraw.Draw(leinwand)
    namen = [f"{s} „{f.kat.name(k) if f.kat.gueltig(k) else k}“" for s, k in zip(p["segmente"], p["klassen"])]
    zeichnen.text((6, 3), f"Paar {nr} ({p['art']}, {p['randpunkte']} Randpunkte ohne Bildkante), "
                          f"Ausschnitt x {x0}–{x1 - 1}, y {y0}–{y1 - 1}, {faktor}-fach", fill=(255, 255, 255), font=_schrift(14))
    zeichnen.text((6, 22), f"türkis: {namen[0]}   magenta: {namen[1]}   gelb: Grenze", fill=(255, 235, 60), font=_schrift(14))
    return leinwand


def finden(f: Fassung, bild: np.ndarray, einst: dict, ziel: str | Path) -> dict:
    """Schreibt je Bündel ``<ziel>/<bündel>/auftrag.json`` und ``paar_<n>.jpg``, dazu ``<ziel>/einigung.json``."""
    hoechstens = einst.get("buendel_paare")
    if isinstance(hoechstens, bool) or not isinstance(hoechstens, int) or hoechstens < 1:
        raise EinigungFehler(f"Einstellung 'buendel_paare' braucht eine ganze Zahl >= 1, hat {hoechstens!r}")
    ziel = Path(ziel)
    if (ziel / "einigung.json").exists():
        raise EinigungFehler(f"{ziel}: hier liegt schon eine Einigung (neuer, leerer Ordner)")
    liste = stellen(f, bild, einst)
    karte, tks = schluessel_karte(f)
    kat_liste = [{k: c.get(k) for k in ("code", "name", "parent", "level")} for c in f.kat.klassen.values()]
    uebersicht = {"schema": AUFTRAG_SCHEMA, "fassung": f.kennung, "ordner": str(f.ordner).replace("\\", "/"),
                  "kategorien": str(f.kat.pfad).replace("\\", "/"), "zahlen": zahlen(liste), "buendel": []}
    for nr, b in enumerate(buendeln([p for p in liste if p["status"] == "offen"], hoechstens), 1):
        name = f"{f.kennung}-{nr:02d}"
        ordner = ziel / name
        ordner.mkdir(parents=True, exist_ok=False)
        paare = []
        for i, p in enumerate(b["paare"], 1):
            datei = f"paar_{i:02d}.jpg"
            _paar_bild(bild, karte, tks, p, i, f, einst).save(ordner / datei, quality=90)
            paare.append({"nr": i, "paar": p["paar"], "art": p["art"], "bild": datei,
                          "randpunkte": p["randpunkte"], "strecken": p["strecken"],
                          "segmente": [{"segment": s, "teilkachel": _teile(s)[0], **_eintrag(f, s)}
                                       for s in p["segmente"]]})
        auftrag = {"schema": AUFTRAG_SCHEMA, "fassung": f.kennung, "buendel": name, "uebergross": b["uebergross"],
                   "kategorien": str(f.kat.pfad).replace("\\", "/"), "klassen": kat_liste, "paare": paare,
                   "abgabe_muster": {"schema": ABGABE_SCHEMA, "fassung": f.kennung, "buendel": name,
                                     "bearbeiter": "", "paare": [{"paar": p["paar"], "entscheidung": "",
                                                                  "klasse": None, "grund": ""} for p in b["paare"]],
                                     "offen": [], "nicht_geprueft": []}}
        dateien.schreibe_json(ordner / "auftrag.json", auftrag)
        uebersicht["buendel"].append({"buendel": name, "paare": len(paare), "uebergross": b["uebergross"],
                                      "segmente": sorted({s for p in b["paare"] for s in p["segmente"]}, key=_teile)})
    ziel.mkdir(parents=True, exist_ok=True)
    dateien.schreibe_json(ziel / "einigung.json", uebersicht)
    return uebersicht


# -- anwenden -------------------------------------------------------------------------------------

def _im_kern(f: Fassung, segment: str) -> bool:
    tk, sid = _teile(segment)
    eintrag = _eintrag(f, segment)
    if eintrag.get("im_kern") is False or eintrag.get("urteil") == "kontextrand":
        return False
    t = next(t for t in f.manifest["teilkacheln"] if t["id"] == tk)
    return bool((kern_ausschneiden(f.karten[tk], t) == sid).any())


def _abgabe_pruefen(f: Fassung, abgabe: dict, auftraege: Path) -> tuple[dict, list[dict]]:
    name = abgabe.get("buendel")
    if not isinstance(name, str) or not (auftraege / name / "auftrag.json").exists():
        raise EinigungFehler(f"Abgabe: Bündel {name!r} hat keinen Auftrag in {auftraege}")
    auftrag = dateien.lese_json(auftraege / name / "auftrag.json")
    if auftrag.get("fassung") != f.kennung or abgabe.get("fassung", f.kennung) != f.kennung:
        raise EinigungFehler(f"Abgabe {name}: Fassung {abgabe.get('fassung')!r}, erwartet {f.kennung!r}")
    if abgabe.get("schema", ABGABE_SCHEMA) != ABGABE_SCHEMA:
        raise EinigungFehler(f"Abgabe {name}: Schema {abgabe['schema']!r}, erwartet {ABGABE_SCHEMA!r}")
    if not isinstance(abgabe.get("bearbeiter"), str) or not abgabe["bearbeiter"].strip():
        raise EinigungFehler(f"Abgabe {name}: 'bearbeiter' fehlt")
    soll = {p["paar"]: p for p in auftrag["paare"]}
    urteile = abgabe.get("paare")
    if not isinstance(urteile, list):
        raise EinigungFehler(f"Abgabe {name}: Liste 'paare' fehlt")
    gesehen = set()
    for u in urteile:
        paar = u.get("paar") if isinstance(u, dict) else None
        if paar not in soll:
            raise EinigungFehler(f"Abgabe {name}: Paar {paar!r} gehört nicht zum Bündel")
        if paar in gesehen:
            raise EinigungFehler(f"Abgabe {name}: Paar {paar} hat mehr als ein Urteil")
        gesehen.add(paar)
        if u.get("entscheidung") not in ENTSCHEIDUNGEN:
            raise EinigungFehler(f"Abgabe {name}, Paar {paar}: Entscheidung {u.get('entscheidung')!r} "
                                 f"(erlaubt: {', '.join(ENTSCHEIDUNGEN)})")
        if not isinstance(u.get("grund"), str) or not u["grund"].strip():
            raise EinigungFehler(f"Abgabe {name}, Paar {paar}: 'grund' fehlt")
        if u["entscheidung"] == "gleich" and not f.kat.gueltig(u.get("klasse")):
            raise EinigungFehler(f"Abgabe {name}, Paar {paar}: Klasse {u.get('klasse')!r} steht nicht in "
                                 f"{f.kat.pfad.name}")
        for s in paar.split("|"):
            if not _im_kern(f, s):
                raise EinigungFehler(f"Abgabe {name}, Paar {paar}: Segment {s} liegt nicht im Kern")
    fehlen = sorted(set(soll) - gesehen)
    if fehlen:
        raise EinigungFehler(f"Abgabe {name}: ohne Urteil: {', '.join(fehlen)}")
    return auftrag, urteile


def anwenden(f: Fassung, abgaben: list[dict], auftraege: str | Path, ziel: str | Path | None = None,
             schreiben: bool = True) -> dict:
    """Setzt die Abgaben um. ``ziel``: Kopie des Fassungsordners, in der geändert wird (sonst an Ort und
    Stelle); ``schreiben=False`` prüft nur (Probe)."""
    auftraege = Path(auftraege)
    geprueft = [(a, *_abgabe_pruefen(f, a, auftraege)) for a in abgaben]
    # Kette a–b–c: Wer per ``gleich`` verbunden ist, bekommt dieselbe Klasse.
    eltern: dict[str, str] = {}

    def wurzel(s: str) -> str:
        while eltern.setdefault(s, s) != s:
            s = eltern[s]
        return s

    for _, _, urteile in geprueft:
        for u in urteile:
            if u["entscheidung"] == "gleich":
                a, b = u["paar"].split("|")
                eltern[wurzel(a)] = wurzel(b)
    klasse_je_kette: dict[str, tuple[str, str]] = {}
    for _, _, urteile in geprueft:
        for u in urteile:
            if u["entscheidung"] != "gleich":
                continue
            w = wurzel(u["paar"].split("|")[0])
            frueher = klasse_je_kette.setdefault(w, (u["klasse"], u["paar"]))
            if frueher[0] != u["klasse"]:
                raise EinigungFehler(f"Paare {frueher[1]} und {u['paar']} hängen zusammen, haben aber verschiedene "
                                     f"Klassen ({frueher[0]!r}, {u['klasse']!r}): eine Klasse für alle Glieder")
    vorher = {tk: set(pruefen(f.karten[tk], s, f.kat).maengel) for tk, s in f.segmente.items()}
    stand = {tk: s for tk, s in f.segmente.items()}
    zeit = datetime.now(timezone.utc).isoformat(timespec="seconds")
    zaehler = {"gleich": 0, "grenze": 0, "unklar": 0, "klassen_gesetzt": 0}
    geaendert: set[str] = set()
    try:
        for abgabe, auftrag, urteile in geprueft:
            arbeit: dict[str, Bearbeitung] = {}
            for u in urteile:
                zaehler[u["entscheidung"]] += 1
                segmente = u["paar"].split("|")
                for s, partner in ((segmente[0], segmente[1]), (segmente[1], segmente[0])):
                    tk, sid = _teile(s)
                    b = arbeit.get(tk) or arbeit.setdefault(
                        tk, Bearbeitung(f.karten[tk], stand[tk], f.kat, abgabe["bearbeiter"]))
                    eintrag = dateien.segmente_nach_id(b.segmente)[sid]
                    if u["entscheidung"] == "gleich" and eintrag.get("klasse") != u["klasse"]:
                        b.klasse_setzen(sid, u["klasse"])
                        zaehler["klassen_gesetzt"] += 1
                    beschluss = {"paar": u["paar"], "mit": partner, "entscheidung": u["entscheidung"],
                                 "grund": u["grund"].strip(), "bearbeiter": abgabe["bearbeiter"],
                                 "buendel": auftrag["buendel"], "zeit": zeit}
                    if u["entscheidung"] == "gleich":
                        beschluss["klasse"] = u["klasse"]
                    felder = {"einigung": list(eintrag.get("einigung") or []) + [beschluss]}
                    if u["entscheidung"] == "unklar":
                        felder["sicher"] = False if isinstance(eintrag.get("sicher"), bool) else "nein"
                    b.vermerken(sid, felder, op="einigung")
                    geaendert.add(tk)
            for tk, b in arbeit.items():
                stand[tk] = b.segmente
    except EingriffFehler as fehler:
        raise EinigungFehler(f"Einigung abgelehnt: {fehler}") from None
    befund = {}
    for tk in sorted(geaendert):
        neu = set(pruefen(f.karten[tk], stand[tk], f.kat).maengel) - vorher[tk]
        if neu:
            raise EinigungFehler(f"Teilkachel {tk}: pruefen meldet nach der Einigung neu: {'; '.join(sorted(neu))}")
        befund[tk] = not vorher[tk]
    ziel_ordner = Path(ziel) if ziel else f.ordner
    if schreiben:
        if ziel:
            if ziel_ordner.exists():
                raise EinigungFehler(f"{ziel_ordner}: Ziel gibt es schon (neuer Ordner für die Kopie)")
            shutil.copytree(f.ordner, ziel_ordner)
        for tk in sorted(geaendert):
            dateien.schreibe_json(ziel_ordner / tk / "segmente.json", stand[tk])
        f.segmente.update(stand)
    return {"fassung": f.kennung, "ziel": str(ziel_ordner).replace("\\", "/"), "geschrieben": schreiben,
            "abgaben": len(abgaben), **zaehler, "teilkacheln": sorted(geaendert), "pruefen_ok": befund}
