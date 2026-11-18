"""W8 seite: Übersichtsseite eines Ausschnitts als eine HTML-Datei, die man direkt im Browser öffnet.

Je Bild ein Stand, das Ergebnis, in einem großen Bild: Ebene grob/mittel/fein umschaltbar, Klassifikation
jedes Segments unter der Maus und per Klick, Kategorienliste mit Segmentzahl und Flächenanteil, Lückenkarte,
Naht-Ebene (Nahtregel auf den zusammengesetzten Kernen) mit zwei Zahlen: Schnittlinien ohne Bildkante
(``naht``) und Stellen, an denen gleiche Flächen verschiedene Klassen haben (``einigung``, davon unsicher
belegt), Übersicht des ganzen Ausschnitts und Kommentare mit
Export als JSON. Ein Umschalter wechselt zwischen den Fassungen desselben Ausschnitts (Einstellung
``fassungen``: Kennung, Name, Beschreibung, Ordner mit ``<teilkachel>/labels.tif`` und ``segmente.json``,
eigene Kategorienliste); eine Fassung ohne Daten erscheint ausgegraut.

Alles steckt in der einen Datei (Bilder als PNG im Text); Klassen, Namen und Farben kommen je Fassung aus
deren Kategorienliste (Format von ``kategorien.json``), Farben und Voreinstellungen der Seite aus
``einstellungen/seite.json``.
"""

from __future__ import annotations

import base64
import io
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from PIL import Image

from . import dateien, einigung, einstellungen, naht
from . import kategorien as kategorien_modul
from .kategorien import Kategorien
from .pruefen import pruefen
from .zusammentragen import kern_ausschneiden

KOMMENTAR_SCHEMA = "landseg-kommentare/1"
VORLAGEN = Path(__file__).resolve().parent / "seite_vorlage"
#: Größte Segment-ID, die die Seite darstellen kann (drei Farbkanäle zu je 8 Bit).
ID_GRENZE = 2 ** 24
#: Lage im Raster in Worten, je Zahl der Zeilen bzw. Spalten (größere Raster: „Zeile n, Spalte m").
_LAGE_ZEILE = {1: ("",), 2: ("oben", "unten"), 3: ("oben", "Mitte", "unten")}
_LAGE_SPALTE = {1: ("",), 2: ("links", "rechts"), 3: ("links", "Mitte", "rechts")}


class SeiteFehler(Exception):
    """Aufruf- oder Datenfehler der Seite."""


def _png(feld: np.ndarray) -> str:
    puffer = io.BytesIO()
    Image.fromarray(feld).save(puffer, "PNG", optimize=False, compress_level=6)
    return "data:image/png;base64," + base64.b64encode(puffer.getvalue()).decode("ascii")


def _pfad_text(pfad: Path) -> str:
    return str(pfad).replace("\\", "/")


def labels_als_rgb(karte: np.ndarray) -> np.ndarray:
    """Label-Karte als RGB-Bild: ID = R + 256·G + 65536·B (die Seite rechnet es zurück)."""
    if karte.size and int(karte.max()) >= ID_GRENZE:
        raise SeiteFehler(f"Segment-ID {int(karte.max())} zu groß für die Seite (Grenze {ID_GRENZE - 1})")
    k = karte.astype(np.uint32)
    return np.stack([(k & 255), (k >> 8) & 255, (k >> 16) & 255], axis=-1).astype(np.uint8)


def _als_bild(bild: np.ndarray) -> np.ndarray:
    """Bild aus ``naht.lese_bild`` (float32, ein oder drei Kanäle) als uint8 zum Einbetten."""
    feld = np.clip(np.rint(bild), 0, 255).astype(np.uint8)
    return feld[:, :, 0] if feld.shape[2] == 1 else feld


def _stand_lesen(ordner: Path, teilkachel: dict, kat: Kategorien) -> dict | None:
    """Label-Karte und Segmente einer Teilkachel in einer Fassung, mit Befund von ``pruefen``."""
    labels, segmente = ordner / "labels.tif", ordner / "segmente.json"
    if not labels.exists() and (ordner / "labels.npy").exists():
        labels = ordner / "labels.npy"
    if not labels.exists() or not segmente.exists():
        return None
    karte = dateien.lese_labels(labels)
    daten = dateien.lese_segmente(segmente)
    form = (teilkachel["kontext"]["hoehe"], teilkachel["kontext"]["breite"])
    if karte.shape != form:
        raise SeiteFehler(f"{labels}: {karte.shape[1]} × {karte.shape[0]}, erwartet wie das Teilkachelbild "
                          f"{form[1]} × {form[0]}")
    befund = pruefen(karte, daten, kat, form=form)
    kandidaten = []
    if (ordner / "kandidaten.json").exists():
        kandidaten = dateien.lese_json(ordner / "kandidaten.json").get("kandidaten", [])
    return {"karte": karte, "segmente": daten, "befund": befund.als_dict(), "kandidaten": kandidaten,
            "quelle": _pfad_text(ordner)}


def _zusammensetzen(manifest: dict, staende: dict[str, dict | None]) -> np.ndarray | None:
    """Kerne aller Teilkacheln zur Label-Karte des Ausschnitts; ``None``, wenn eine fehlt."""
    aus = manifest["ausschnitt"]
    gesamt = np.zeros((aus["hoehe"], aus["breite"]), np.uint32)
    for t in manifest["teilkacheln"]:
        stand = staende.get(t["id"])
        if stand is None:
            return None
        k = t["kern"]
        gesamt[k["y"]:k["y"] + k["hoehe"], k["x"]:k["x"] + k["breite"]] = kern_ausschneiden(stand["karte"], t)
    return gesamt


def _naht(manifest: dict, gesamt: np.ndarray | None, ausschnitt_bild: np.ndarray, einst: dict) -> dict | None:
    if gesamt is None:
        return None
    befund = naht.pruefe_naehte(gesamt, manifest, ausschnitt_bild, einst.get("naht"))
    return befund.als_dict()


def _einigung(kennung: str, ordner: Path, kat: Kategorien, manifest: dict, basis: Path,
              staende: dict[str, dict | None], ausschnitt_bild: np.ndarray,
              einst: dict) -> tuple[list[dict] | None, str | None]:
    """Stellen der Einigung (``einigung.stellen``) auf den schon gelesenen Ständen, mit der Nahtregel der Seite.

    ``(None, None)``, wenn eine Teilkachel fehlt; ``(None, Grund)``, wenn die Daten nicht zählbar sind (etwa ein
    Segment der Karte fehlt in ``segmente.json``; das zeigt die Seite schon über ``pruefen``)."""
    if any(staende.get(t["id"]) is None for t in manifest["teilkacheln"]):
        return None, None
    f = einigung.Fassung(kennung, ordner, kat, manifest, basis,
                         {tk: s["karte"] for tk, s in staende.items()},
                         {tk: s["segmente"] for tk, s in staende.items()})
    try:
        return einigung.stellen(f, ausschnitt_bild, {"naht": einst.get("naht")}), None
    except einigung.EinigungFehler as fehler:
        return None, str(fehler)


def _einigung_zahl(liste: list[dict] | None, teilkachel: str | None = None) -> dict | None:
    """Zahlen wie ``einigung messen``, wahlweise nur für Paare mit einem Segment dieser Teilkachel; dazu
    ``stellen`` = gleiche Fläche, verschiedene Klasse (offen und unsicher belegt)."""
    if liste is None:
        return None
    if teilkachel is not None:
        liste = [p for p in liste if any(s.split(":", 1)[0] == teilkachel for s in p["segmente"])]
    z = einigung.zahlen(liste)
    return {**z, "stellen": z["offen"]["paare"] + z["unsicher"]["paare"]}


def _segment_liste(daten: dict) -> list[dict]:
    """Segmente für die Seite: alle Felder aus ``segmente.json``, dazu die Eingriffe aus dem Verlauf,
    die das Segment nennen."""
    eingriffe: dict[int, list[str]] = {}
    for e in daten.get("verlauf", []) or []:
        text = f"{e.get('nr')}: {e.get('op')} ({e.get('bearbeiter')})"
        beteiligt = set()
        for teil in (e.get("parameter") or {}, e.get("ergebnis") or {}):
            for wert in teil.values():
                if isinstance(wert, int):
                    beteiligt.add(wert)
                elif isinstance(wert, list):
                    beteiligt.update(v for v in wert if isinstance(v, int))
        for sid in beteiligt:
            eingriffe.setdefault(sid, []).append(text)
    liste = []
    for s in daten.get("segmente", []):
        eintrag = dict(s)
        if s["id"] in eingriffe:
            eintrag["eingriffe"] = eingriffe[s["id"]]
        liste.append(eintrag)
    return liste


def _stand_fuer_seite(stand: dict | None, naht_befund: dict | None, teilkachel: dict,
                      stellen: list[dict] | None) -> dict | None:
    if stand is None:
        return None
    verstoesse = []
    if naht_befund is not None:
        dx, dy = teilkachel["kontext"]["x"], teilkachel["kontext"]["y"]
        for v in naht_befund["verstoesse"]:
            if v["art"] != "ohne_kante" or teilkachel["id"] not in v["naht"].split("|"):
                continue
            verstoesse.append({**v, "von": [v["von"][0] - dx, v["von"][1] - dy],
                               "bis": [v["bis"][0] - dx, v["bis"][1] - dy]})
    return {"labels": _png(labels_als_rgb(stand["karte"])), "segmente": _segment_liste(stand["segmente"]),
            "pruefen": stand["befund"], "kandidaten": stand["kandidaten"], "naht": verstoesse,
            "einigung": _einigung_zahl(stellen, teilkachel["id"]), "quelle": stand["quelle"]}


def lage_in_worten(zeile: int, spalte: int, zeilen: int, spalten: int) -> str:
    """Lage einer Teilkachel im Raster in Worten für die Kachel-Wahl der Seite („oben links" … „unten rechts")."""
    wz, ws = _LAGE_ZEILE.get(zeilen), _LAGE_SPALTE.get(spalten)
    if wz is None or ws is None:
        return f"Zeile {zeile + 1}, Spalte {spalte + 1}"
    worte = [w for w in (wz[zeile], ws[spalte]) if w]
    if worte == ["Mitte", "Mitte"]:
        return "Mitte"
    return " ".join(worte) or "ganzer Ausschnitt"


def _kommentare_lesen(pfad: Path | None) -> list[dict]:
    if pfad is None:
        return []
    if not pfad.exists():
        raise SeiteFehler(f"{pfad}: Kommentar-Datei fehlt")
    daten = dateien.lese_json(pfad)
    liste = daten.get("kommentare") if isinstance(daten, dict) else daten
    if not isinstance(liste, list):
        raise SeiteFehler(f"{pfad}: Liste 'kommentare' erwartet")
    return liste


def _fassung_lesen(eintrag: dict, basis: Path, kat_standard: Kategorien, manifest: dict,
                   ausschnitt_bild: np.ndarray, einst: dict) -> dict:
    """Eine Fassung: eigene Kategorienliste, Stand je Teilkachel, zusammengesetzte Karte und Nähte.

    ``ordner`` ist relativ zum Ordner des Manifests, ``kategorien`` relativ zum Ordner der Fassung; ohne
    ``kategorien`` gilt die Liste des Aufrufs (Standard: ``kategorien.json`` des Repos)."""
    kennung = str(eintrag.get("kennung") or "").strip()
    if not kennung:
        raise SeiteFehler(f"Fassung ohne 'kennung' in den Einstellungen: {eintrag!r}")
    if not eintrag.get("ordner"):
        raise SeiteFehler(f"Fassung {kennung}: 'ordner' fehlt in den Einstellungen")
    ordner = Path(eintrag["ordner"])
    ordner = ordner if ordner.is_absolute() else basis / ordner
    kopf = {"kennung": kennung, "name": eintrag.get("name") or kennung,
            "beschreibung": eintrag.get("beschreibung") or "", "quelle": _pfad_text(ordner)}
    if not ordner.is_dir() or not any((ordner / t["id"]).is_dir() for t in manifest["teilkacheln"]):
        return {**kopf, "vorhanden": False}
    kat = kat_standard
    if eintrag.get("kategorien"):
        liste = Path(eintrag["kategorien"])
        liste = liste if liste.is_absolute() else ordner / liste
        if not liste.exists():
            raise SeiteFehler(f"Fassung {kennung}: Kategorienliste {liste} fehlt")
        try:
            kat = kategorien_modul.laden(liste)
        except (ValueError, OSError) as fehler:
            raise SeiteFehler(f"Fassung {kennung}: {fehler}") from fehler
    staende = {t["id"]: _stand_lesen(ordner / t["id"], t, kat) for t in manifest["teilkacheln"]}
    if not any(staende.values()):
        return {**kopf, "vorhanden": False}
    gesamt = _zusammensetzen(manifest, staende)
    naht_befund = _naht(manifest, gesamt, ausschnitt_bild, einst)
    stellen, einigung_fehler = _einigung(kennung, ordner, kat, manifest, basis, staende, ausschnitt_bild, einst)
    # Klassen je Ebene wie in der Kategorienliste gezählt: die Klassen dieser Ebene und die Blätter darüber
    eltern = {k.get("parent") for k in kat.klassen.values()}
    ebenen = {e: sum(1 for code, k in kat.klassen.items()
                     if k.get("level", 1) == e or (k.get("level", 1) < e and code not in eltern))
              for e in sorted({k.get("level", 1) for k in kat.klassen.values()})}
    return {
        **kopf, "vorhanden": True,
        "kategorien": [{k: c.get(k) for k in ("code", "name", "parent", "level", "color", "image_cue")}
                       for c in kat.klassen.values()],
        "kategorien_quelle": _pfad_text(kat.pfad),
        "ebenen": [{"ebene": e, "name": einst["ebenen_namen"].get(str(e), str(e)), "klassen": n}
                   for e, n in sorted(ebenen.items())],
        "gesamt": _png(labels_als_rgb(gesamt)) if gesamt is not None else None,
        "naht": naht_befund,
        "einigung": _einigung_zahl(stellen),
        "einigung_fehler": einigung_fehler,
        "teilkacheln": {t["id"]: _stand_fuer_seite(staende[t["id"]], naht_befund, t, stellen)
                        for t in manifest["teilkacheln"]},
    }


def seite_daten(manifest_pfad: str | Path, kat: Kategorien, kommentare: str | Path | None = None,
                werte: dict | None = None) -> dict:
    """Alles, was die Seite anzeigt, als ein JSON-fähiges Wörterbuch."""
    manifest_pfad = Path(manifest_pfad)
    manifest = dateien.lese_json(manifest_pfad)
    basis = manifest_pfad.parent
    einst = werte or einstellungen.laden("seite")
    liste = einst.get("fassungen")
    if not isinstance(liste, list) or not liste:
        raise SeiteFehler("Einstellung 'fassungen' fehlt oder ist leer")
    ausschnitt = manifest["ausschnitt"]
    ausschnitt_bild = naht.lese_bild(basis / ausschnitt["bild"])  # derselbe Leser wie naht und einigung
    fassungen = [_fassung_lesen(e, basis, kat, manifest, ausschnitt_bild, einst) for e in liste]
    kennungen = [f["kennung"] for f in fassungen]
    if len(set(kennungen)) != len(kennungen):
        raise SeiteFehler(f"Kennungen der Fassungen doppelt: {kennungen}")
    if not any(f["vorhanden"] for f in fassungen):
        raise SeiteFehler("keine Fassung mit Daten: " + "; ".join(
            f"{f['kennung']}: {f['quelle']}/<teilkachel>/ ohne labels.tif und segmente.json" for f in fassungen))

    # Nummer (1 … n, zeilenweise von oben links) und Lage in Worten für die Kachel-Wahl
    zeilen = 1 + max(t["zeile"] for t in manifest["teilkacheln"])
    spalten = 1 + max(t["spalte"] for t in manifest["teilkacheln"])
    reihe = sorted(manifest["teilkacheln"], key=lambda t: (t["zeile"], t["spalte"]))
    nummer = {t["id"]: i + 1 for i, t in enumerate(reihe)}
    teilkacheln = [{"id": t["id"], "zeile": t["zeile"], "spalte": t["spalte"], "nummer": nummer[t["id"]],
                    "lage": lage_in_worten(t["zeile"], t["spalte"], zeilen, spalten),
                    "kern": t["kern"], "kontext": t["kontext"], "kern_im_bild": t["kern_im_bild"],
                    "bild": _png(_als_bild(naht.lese_bild(basis / t["bild"])))} for t in manifest["teilkacheln"]]
    return {
        "schema": "landseg-seite/2",
        "erstellt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "name": ausschnitt.get("name", manifest_pfad.parent.name),
        "manifest": _pfad_text(manifest_pfad),
        "ausschnitt": {"breite": ausschnitt["breite"], "hoehe": ausschnitt["hoehe"],
                       "bild": _png(_als_bild(ausschnitt_bild))},
        "teilkacheln": teilkacheln,
        "fassungen": fassungen,
        "kommentare": _kommentare_lesen(Path(kommentare) if kommentare else None),
        "kommentar_schema": KOMMENTAR_SCHEMA,
        "einstellungen": {k: v for k, v in einst.items() if k not in ("beschreibung", "naht", "fassungen")},
    }


def _einbetten(daten: dict) -> str:
    """Daten als JavaScript-Literal, sicher innerhalb von ``<script>``."""
    text = json.dumps(daten, ensure_ascii=False, separators=(",", ":"))
    return text.replace("</", "<\\/").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")


def seite(manifest_pfad: str | Path, ziel: str | Path, kat: Kategorien, kommentare: str | Path | None = None,
          werte: dict | None = None) -> dict:
    """Schreibt die Seite nach ``ziel`` (eine HTML-Datei) und gibt eine Zusammenfassung zurück."""
    ziel = Path(ziel)
    if ziel.suffix.lower() not in (".html", ".htm"):
        raise SeiteFehler(f"{ziel}: Ziel ist eine HTML-Datei (Endung .html)")
    daten = seite_daten(manifest_pfad, kat, kommentare=kommentare, werte=werte)
    html = (VORLAGEN / "seite.html").read_text(encoding="utf-8")
    for platz, inhalt in (("/*CSS*/", (VORLAGEN / "seite.css").read_text(encoding="utf-8")),
                          ("/*JS*/", (VORLAGEN / "seite.js").read_text(encoding="utf-8")),
                          ("/*DATEN*/", "window.DATEN = " + _einbetten(daten) + ";")):
        if platz not in html:
            raise SeiteFehler(f"Vorlage seite.html: Platzhalter {platz} fehlt")
        html = html.replace(platz, inhalt, 1)
    html = html.replace("<!--TITEL-->", f"Übersicht {daten['name']}", 1)
    ziel.parent.mkdir(parents=True, exist_ok=True)
    ziel.write_text(html, encoding="utf-8")
    zusammenfassung = {"ziel": str(ziel), "groesse": ziel.stat().st_size, "fassungen": []}
    for f in daten["fassungen"]:
        zeile = {"kennung": f["kennung"], "name": f["name"], "vorhanden": f["vorhanden"], "quelle": f["quelle"]}
        if f["vorhanden"]:
            zeile["naht"] = None if f["naht"] is None else len(f["naht"]["verstoesse"])
            e = f["einigung"]
            zeile["einigung"] = None if e is None else {"stellen": e["stellen"], "unsicher": e["unsicher"]["paare"]}
            zeile["teilkacheln"] = [
                {"id": tk, "segmente": len(s["segmente"]), "pruefen_ok": s["pruefen"]["ok"], "naht": len(s["naht"])}
                if s else {"id": tk} for tk, s in f["teilkacheln"].items()]
        zusammenfassung["fassungen"].append(zeile)
    return zusammenfassung
