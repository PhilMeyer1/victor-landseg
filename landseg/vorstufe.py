"""W2 ``vorstufe``: lückenlose Vorbelegung einer Teilkachel als Vorschlag für das Urteil.

Ablauf (Bericht landseg-methode 3.2, Schritt 3):

a. Übersegmentierung: SLIC in Lab, jede Stelle des Bildes hat einen Superpixel.
b. SAM 3 mit je einem oder mehreren Texten je Kategorie (``vorstufe.json``): Instanzmasken.
c. SAM-3-Semantikkopf mal Presence je Text, Klassenwert = bester Text der Klasse, auch aus den
   Instanzen (Nachbau SegEarth-OV3); argmax über die Klassen.
d. Verschmelzen: Instanzen rasten auf Superpixel ein (Mehrheit der Superpixel-Fläche in der Maske),
   übrige Superpixel bekommen die argmax-Klasse ihres Mittels und verbinden sich mit gleichklassigen
   Nachbarn. Jedes zusammenhängende Gebiet gleicher Herkunft wird ein Segment, also ist die Karte
   lückenlos und jedes Segment zusammenhängend (per Konstruktion). Danach, rein aus der fertigen
   Karte, das Merkmal ``im_siedlung`` je Segment (Abschnitt ``siedlung`` in ``vorstufe.json``).
e. ``pruefen``: H × W, kein 0, Zusammenhang, Klassen gültig.

Ausgabe je Teilkachel: ``labels.tif`` (uint32), ``segmente.json`` (ID, Klasse fein/grob, Herkunft,
Sicherheit, im Siedlungsgebiet), ``kandidaten.json`` (Klasse unsicher, Grenze ohne Bildkante, nicht zusammenhängend, zu
klein) und ``sam3_roh.npz`` (Rohwerte von SAM 3; ein neuer Lauf mit gleichen SAM-3-Einstellungen
braucht keine GPU).

Die Bildpunkt-Schritte (a, d, e) laufen für mehrere Teilkacheln gleichzeitig, SAM 3 (b, c) läuft
Teilkachel nach Teilkachel auf der GPU. Ein Modell kommt von außen (``modell``) oder wird erst
geladen, wenn eine Teilkachel keine passenden Rohwerte hat.
"""

from __future__ import annotations

import hashlib
import json
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage
from skimage.measure import label as zusammenhang_label
from skimage.segmentation import slic

from . import dateien
from .kategorien import Kategorien
from .pruefen import VIERER, pruefen

KONFIG_SCHEMA = "landseg-vorstufe/1"
KANDIDATEN_SCHEMA = "landseg-kandidaten/1"
STANDARD_KONFIG = Path(__file__).resolve().parent.parent / "vorstufe.json"
HERKUNFT_INSTANZ = "sam3-instanz"
HERKUNFT_SEMANTIK = "semantik"


class VorstufeFehler(Exception):
    pass


# --- Einstellungen ----------------------------------------------------------------------------

def _ohne_hinweise(wert):
    if isinstance(wert, dict):
        return {k: _ohne_hinweise(v) for k, v in wert.items() if not k.startswith("_")}
    if isinstance(wert, list):
        return [_ohne_hinweise(v) for v in wert]
    return wert


def konfig_laden(pfad: str | Path | None, kat: Kategorien) -> dict:
    """Liest ``vorstufe.json`` (ohne Hinweis-Schlüssel) und prüft die Klassen der Texte."""
    pfad = Path(pfad) if pfad else STANDARD_KONFIG
    konfig = _ohne_hinweise(dateien.lese_json(pfad))
    if konfig.get("schema") != KONFIG_SCHEMA:
        raise VorstufeFehler(f"{pfad}: schema {konfig.get('schema')!r}, erwartet {KONFIG_SCHEMA!r}")
    for teil in ("uebersegmentierung", "sam3", "verschmelzen", "sicherheit", "kandidaten",
                 "siedlung", "prompts", "id_block"):
        if teil not in konfig:
            raise VorstufeFehler(f"{pfad}: Abschnitt {teil!r} fehlt")
    _siedlung_pruefen(konfig["siedlung"], pfad, kat)
    gesehen = set()
    for eintrag in konfig["prompts"]:
        klasse, texte = eintrag.get("klasse"), eintrag.get("texte")
        if not kat.gueltig(klasse):
            raise VorstufeFehler(f"{pfad}: Klasse {klasse!r} fehlt in {kat.pfad.name}")
        if klasse in gesehen:
            raise VorstufeFehler(f"{pfad}: Klasse {klasse!r} doppelt unter prompts")
        if not texte or not all(isinstance(t, str) and t.strip() for t in texte):
            raise VorstufeFehler(f"{pfad}: Klasse {klasse!r} ohne Text")
        gesehen.add(klasse)
    if not gesehen:
        raise VorstufeFehler(f"{pfad}: keine prompts")
    konfig["_pfad"] = str(pfad)
    return konfig


def _siedlung_pruefen(einst: dict, pfad: Path, kat: Kategorien) -> None:
    zone = einst.get("zone_klassen")
    if not isinstance(zone, list) or not zone:
        raise VorstufeFehler(f"{pfad}: siedlung.zone_klassen fehlt oder ist leer")
    for klasse in zone:
        if not kat.gueltig(klasse):
            raise VorstufeFehler(f"{pfad}: siedlung.zone_klassen: Klasse {klasse!r} fehlt in {kat.pfad.name}")
    for schluessel, unten, oben in (("puffer_m", 0.0, None), ("anteil", 0.0, 1.0), ("bildpunkt_m", 0.0, None)):
        wert = einst.get(schluessel)
        if (not isinstance(wert, (int, float)) or isinstance(wert, bool) or wert < unten
                or (oben is not None and wert > oben) or (schluessel != "puffer_m" and wert <= 0)):
            raise VorstufeFehler(f"{pfad}: siedlung.{schluessel} {wert!r} ungültig")


def fingerabdruck(daten) -> str:
    text = json.dumps(daten, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]


def sam3_teil(konfig: dict) -> dict:
    """Was die Rohwerte von SAM 3 bestimmt (Modell, Fenster, Schwellen, Texte)."""
    return {"sam3": konfig["sam3"], "prompts": konfig["prompts"]}


def klassen_und_texte(konfig: dict) -> tuple[list[str], list[tuple[int, str]]]:
    klassen = [e["klasse"] for e in konfig["prompts"]]
    texte = [(i, t) for i, e in enumerate(konfig["prompts"]) for t in e["texte"]]
    return klassen, texte


# --- Rohwerte von SAM 3 -----------------------------------------------------------------------

@dataclass
class Instanz:
    klasse: int  # Index in Roh.klassen
    wert: float
    maske: np.ndarray  # bool H × W
    text: str = ""


@dataclass
class Roh:
    """Ergebnis von SAM 3 an einem Bild: Klassenwerte je Bildpunkt und Instanzen."""

    klassen: list[str]
    werte: np.ndarray  # float32 C × H × W, 0..1
    instanzen: list[Instanz] = field(default_factory=list)

    def speichern(self, pfad: Path, abdruck: str) -> None:
        pfad.parent.mkdir(parents=True, exist_ok=True)
        h, w = self.werte.shape[1:]
        masken = (np.stack([np.packbits(i.maske.ravel()) for i in self.instanzen])
                  if self.instanzen else np.zeros((0, (h * w + 7) // 8), np.uint8))
        tmp = pfad.with_name(pfad.name + ".tmp.npz")
        np.savez_compressed(
            tmp, werte=self.werte.astype(np.float16), form=np.array([h, w]),
            klassen=np.array(self.klassen), abdruck=np.array(abdruck),
            inst_klasse=np.array([i.klasse for i in self.instanzen], np.int32),
            inst_wert=np.array([i.wert for i in self.instanzen], np.float32),
            inst_text=np.array([i.text for i in self.instanzen] or [""]),
            inst_masken=masken)
        tmp.replace(pfad)

    @classmethod
    def laden(cls, pfad: Path, abdruck: str) -> "Roh | None":
        """Gespeicherte Rohwerte, wenn sie mit denselben SAM-3-Einstellungen entstanden."""
        if not pfad.exists():
            return None
        with np.load(pfad) as d:
            if str(d["abdruck"]) != abdruck:
                return None
            h, w = (int(v) for v in d["form"])
            instanzen = [
                Instanz(int(k), float(v), np.unpackbits(m)[:h * w].reshape(h, w).astype(bool), str(t))
                for k, v, m, t in zip(d["inst_klasse"], d["inst_wert"], d["inst_masken"],
                                      d["inst_text"])]
            return cls([str(k) for k in d["klassen"]], d["werte"].astype(np.float32), instanzen)


# --- a: Übersegmentierung ---------------------------------------------------------------------

def uebersegmentierung(bild: np.ndarray, einst: dict) -> np.ndarray:
    """Superpixel 1..S (int32), jeder zusammenhängend (4er-Nachbarschaft)."""
    if einst.get("verfahren", "slic") != "slic":
        raise VorstufeFehler(f"Übersegmentierung {einst.get('verfahren')!r} unbekannt (nur slic)")
    h, w = bild.shape[:2]
    anzahl = max(1, round(h * w / float(einst["flaeche_px"])))
    sp = slic(bild, n_segments=anzahl, compactness=float(einst["kompaktheit"]),
              sigma=float(einst.get("sigma", 0)), start_label=1, convert2lab=True,
              enforce_connectivity=True, channel_axis=-1)
    # SLIC garantiert Zusammenhang nur in 8er-Nachbarschaft: nachzählen
    return zusammenhang_label(sp, background=0, connectivity=1).astype(np.int32)


# --- d: Verschmelzen --------------------------------------------------------------------------

def _mittel_je(labels: np.ndarray, werte: np.ndarray, n: int) -> np.ndarray:
    flaeche = np.bincount(labels.ravel(), minlength=n + 1).astype(np.float64)
    summe = np.bincount(labels.ravel(), weights=werte.ravel().astype(np.float64), minlength=n + 1)
    return summe / np.maximum(flaeche, 1)


def gradient(bild: np.ndarray) -> np.ndarray:
    """Gradientstärke des Grauwerts (0..1 skaliert, Sobel / 8), float32."""
    grau = (bild[..., :3].astype(np.float32).mean(axis=2) if bild.ndim == 3
            else bild.astype(np.float32)) / 255.0
    grau = ndimage.gaussian_filter(grau, 1.0)
    return (np.hypot(ndimage.sobel(grau, axis=0), ndimage.sobel(grau, axis=1)) / 8.0).astype(np.float32)


def grenzen(labels: np.ndarray, staerke: np.ndarray) -> list[tuple[int, int, int, float]]:
    """(id a, id b, Länge in Bildpunkt-Kanten, mittlere Gradientstärke) je Nachbarpaar."""
    a = np.concatenate([labels[:, :-1].ravel(), labels[:-1, :].ravel()]).astype(np.int64)
    b = np.concatenate([labels[:, 1:].ravel(), labels[1:, :].ravel()]).astype(np.int64)
    g = np.concatenate([np.maximum(staerke[:, :-1], staerke[:, 1:]).ravel(),
                        np.maximum(staerke[:-1, :], staerke[1:, :]).ravel()])
    verschieden = a != b
    if not verschieden.any():
        return []
    a, b, g = a[verschieden], b[verschieden], g[verschieden]
    klein, gross = np.minimum(a, b), np.maximum(a, b)
    basis = int(labels.max()) + 1
    paare, inv = np.unique(klein * basis + gross, return_inverse=True)
    laenge = np.bincount(inv)
    summe = np.bincount(inv, weights=g.astype(np.float64))
    return [(int(p // basis), int(p % basis), int(n), float(s / n))
            for p, n, s in zip(paare, laenge, summe)]


def bildpunkt_aus_transform(transform: dict | None) -> float | None:
    """Kantenlänge eines Bildpunkts in Metern aus ``X = a·x + b·y + c``, ``Y = d·x + e·y + f``."""
    if not transform:
        return None
    flaeche = abs(transform["a"] * transform["e"] - transform["b"] * transform["d"])
    return float(np.sqrt(flaeche)) if flaeche > 0 else None


def siedlung_merkmal(labels: np.ndarray, segmente: list[dict], einst: dict, kat: Kategorien,
                     bildpunkt_m: float | None = None) -> int:
    """Setzt ``im_siedlung: ja | nein`` je Segment aus der fertigen Karte; Rückgabe: Zahl ``ja``.

    Siedlungszone = Segmente der ``zone_klassen`` um ``puffer_m`` aufgeweitet (Abstandstransformation).
    ``ja`` bekommt ein Segment, dessen Klasse ``kat.siedlung_moeglich`` ist und von dessen Fläche
    mindestens ``anteil`` in der Zone liegt; alle anderen ``nein``.
    """
    if not segmente:
        return 0
    ids = np.array([int(e["id"]) for e in segmente], np.int64)
    ordnung = np.argsort(ids)
    nr = ordnung[np.searchsorted(ids[ordnung], labels.astype(np.int64))]  # Index je Bildpunkt
    zone_seg = np.array([kat.unter(e["klasse"], einst["zone_klassen"]) for e in segmente])
    zone = zone_seg[nr]
    if zone.any():
        meter = bildpunkt_m or float(einst["bildpunkt_m"])
        radius = float(einst["puffer_m"]) / meter
        zone = ndimage.distance_transform_edt(~zone) <= radius
    n = len(segmente)
    drin = np.bincount(nr[zone], minlength=n)
    flaeche = np.bincount(nr.ravel(), minlength=n)
    ja = 0
    for i, eintrag in enumerate(segmente):
        im = (kat.siedlung_moeglich(eintrag["klasse"]) and flaeche[i] > 0
              and drin[i] >= float(einst["anteil"]) * flaeche[i])
        eintrag["im_siedlung"] = "ja" if im else "nein"
        ja += bool(im)
    return ja


@dataclass
class Ergebnis:
    labels: np.ndarray
    segmente: dict
    kandidaten: list[dict]
    messung: dict


def verschmelzen(bild: np.ndarray, sp: np.ndarray, roh: Roh, konfig: dict, kat: Kategorien,
                 id_start: int = 0, kern: dict | None = None,
                 bildpunkt_m: float | None = None) -> Ergebnis:
    """Schritt d: Superpixel + Rohwerte -> lückenlose Label-Karte, Segmente, Kandidaten.

    ``bildpunkt_m``: Bildpunktgröße für den Puffer der Siedlungszone (sonst ``siedlung.bildpunkt_m``).
    """
    h, w = sp.shape
    if roh.werte.shape[1:] != (h, w):
        raise VorstufeFehler(f"Rohwerte {roh.werte.shape[1:]} passen nicht zum Bild {h} × {w}")
    v, s, kd = konfig["verschmelzen"], konfig["sicherheit"], konfig["kandidaten"]
    n_sp = int(sp.max())
    n_kl = len(roh.klassen)

    # Klassenwerte je Bildpunkt: bester und zweitbester (für Sicherheit), Mittel je Superpixel
    sortiert = np.sort(roh.werte, axis=0)
    bester = sortiert[-1]
    abstand = bester - sortiert[-2] if n_kl > 1 else bester
    mittel = np.stack([_mittel_je(sp, roh.werte[k], n_sp) for k in range(n_kl)])  # C × (S+1)
    sp_klasse = mittel.argmax(axis=0)

    # Instanzen einrasten (Reihenfolge nach Einstellung): Superpixel mit Mehrheit in der Maske
    sp_flaeche = np.bincount(sp.ravel(), minlength=n_sp + 1)
    besitzer = np.zeros(n_sp + 1, np.int64)  # 0 = keine Instanz, sonst Index + 1
    pixel_besitzer = np.zeros((h, w), np.int64)
    if v.get("instanz_reihenfolge", "flaeche") == "wert":  # stärkste zuerst
        reihenfolge = sorted(range(len(roh.instanzen)), key=lambda i: -roh.instanzen[i].wert)
    else:  # kleinste zuerst: Dinge (Baum, Haus) vor Flächen (Wiese), die sie umschließen
        reihenfolge = sorted(range(len(roh.instanzen)),
                             key=lambda i: (int(roh.instanzen[i].maske.sum()), -roh.instanzen[i].wert))
    ohne_superpixel = []
    for i in reihenfolge:
        maske = roh.instanzen[i].maske
        drin = np.bincount(sp[maske], minlength=n_sp + 1)
        treffer = (drin >= v["instanz_mehrheit"] * np.maximum(sp_flaeche, 1)) & (besitzer == 0)
        treffer[0] = False
        if treffer.any():
            besitzer[treffer] = i + 1
        else:
            ohne_superpixel.append(i)
    schluessel = np.where(besitzer[sp] > 0, besitzer[sp], len(roh.instanzen) + 1 + sp_klasse[sp])
    # Kleine Instanzen (bis instanz_klein_max_px), die keinen Superpixel einrasten: bildpunktgenau,
    # wo noch keine Instanz liegt, nur Teile ab instanz_min_px. Größere ohne Superpixel lagen unter
    # stärkeren Instanzen und entfallen (ihre Klasse wirkt über die Semantikwerte weiter).
    for i in ohne_superpixel:
        if roh.instanzen[i].maske.sum() > v["instanz_klein_max_px"]:
            continue
        maske = roh.instanzen[i].maske & (besitzer[sp] == 0) & (pixel_besitzer == 0)
        teile, anzahl = ndimage.label(maske, structure=VIERER)
        if not anzahl:
            continue
        groesse = np.bincount(teile.ravel(), minlength=anzahl + 1)
        gross = groesse >= v["instanz_min_px"]
        gross[0] = False
        maske = gross[teile]
        if maske.any():
            pixel_besitzer[maske] = i + 1
            schluessel[maske] = i + 1

    # Segmente: zusammenhängende Gebiete gleichen Schlüssels (4er-Nachbarschaft)
    lokal = zusammenhang_label(schluessel, background=0, connectivity=1).astype(np.int64)
    n = int(lokal.max())
    if id_start + n >= 2 ** 32:
        raise VorstufeFehler("Segment-IDs passen nicht in uint32")
    labels = (lokal + id_start).astype(np.uint32)

    flaeche = np.bincount(lokal.ravel(), minlength=n + 1)
    m_bester = _mittel_je(lokal, bester, n)
    m_abstand = _mittel_je(lokal, abstand, n)
    # Schlüssel je Segment (alle Bildpunkte eines Segments haben denselben)
    seg_schluessel = np.zeros(n + 1, np.int64)
    seg_schluessel[lokal.ravel()] = schluessel.ravel()
    im_kern = None
    if kern:
        ausschnitt = lokal[kern["y"]:kern["y"] + kern["hoehe"], kern["x"]:kern["x"] + kern["breite"]]
        im_kern = np.zeros(n + 1, bool)
        im_kern[np.unique(ausschnitt)] = True

    segmente, kandidaten = [], []
    teile_je_instanz: dict[int, list[int]] = {}
    for nr in range(1, n + 1):
        sid = nr + id_start
        sch = int(seg_schluessel[nr])
        eintrag = {"id": sid}
        if sch <= len(roh.instanzen):
            inst = roh.instanzen[sch - 1]
            klasse = roh.klassen[inst.klasse]
            sicher = inst.wert >= s["instanz_wert"]
            eintrag.update(klasse=klasse, grob=kat.grob(klasse), herkunft=HERKUNFT_INSTANZ,
                           sicher="ja" if sicher else "nein",
                           sicherheit={"wert": round(inst.wert, 3)},
                           instanz={"text": inst.text, "eingerastet": bool((besitzer == sch).any())})
            teile_je_instanz.setdefault(sch, []).append(sid)
            grund = f"Instanz „{inst.text}“ mit Wert {inst.wert:.2f} < {s['instanz_wert']}"
        else:
            klasse = roh.klassen[sch - len(roh.instanzen) - 1]
            wb, wa = float(m_bester[nr]), float(m_abstand[nr])
            sicher = wb >= s["semantik_wert"] and wa >= s["semantik_abstand"]
            eintrag.update(klasse=klasse, grob=kat.grob(klasse), herkunft=HERKUNFT_SEMANTIK,
                           sicher="ja" if sicher else "nein",
                           sicherheit={"wert": round(wb, 3), "abstand": round(wa, 3)})
            grund = (f"Semantik: Wert {wb:.3f} (mind. {s['semantik_wert']}), "
                     f"Abstand {wa:.3f} (mind. {s['semantik_abstand']})")
        eintrag["flaeche"] = int(flaeche[nr])
        if im_kern is not None:
            eintrag["im_kern"] = bool(im_kern[nr])
        segmente.append(eintrag)
        if not sicher:
            kandidaten.append({"art": "klasse_unsicher", "ids": [sid], "grund": grund})
        if flaeche[nr] < kd["zu_klein_px"]:
            kandidaten.append({"art": "zu_klein", "ids": [sid],
                               "grund": f"{int(flaeche[nr])} Bildpunkte < {kd['zu_klein_px']}"})

    for sch, ids in teile_je_instanz.items():
        if len(ids) > 1:
            inst = roh.instanzen[sch - 1]
            kandidaten.append({"art": "nicht_zusammenhaengend", "ids": ids,
                               "grund": f"Instanz „{inst.text}“ zerfällt in {len(ids)} Segmente"})

    for a, b, laenge, staerke in grenzen(lokal, gradient(bild)):
        if laenge >= kd["kante_min_laenge_px"] and staerke < kd["kante_min"]:
            kandidaten.append({"art": "grenze_ohne_bildkante", "ids": [a + id_start, b + id_start],
                               "laenge_px": laenge, "staerke": round(staerke, 4),
                               "grund": f"mittlere Kantenstärke {staerke:.3f} < {kd['kante_min']}"})

    im_siedlung_ja = siedlung_merkmal(labels, segmente, konfig["siedlung"], kat, bildpunkt_m)
    nein = [e for e in segmente if e["sicher"] == "nein"]
    arten: dict[str, int] = {}
    for k in kandidaten:
        arten[k["art"]] = arten.get(k["art"], 0) + 1
    messung = {
        "segmente": n,
        "segmente_im_kern": int(im_kern[1:].sum()) if im_kern is not None else None,
        "superpixel": n_sp,
        "instanzen": len(roh.instanzen),
        "segmente_instanz": sum(e["herkunft"] == HERKUNFT_INSTANZ for e in segmente),
        "sicher_nein": len(nein),
        "anteil_sicher_nein": round(len(nein) / n, 4) if n else 0.0,
        "flaeche_sicher_nein": round(sum(e["flaeche"] for e in nein) / (h * w), 4),
        "kandidaten": arten,
        "im_siedlung_ja": im_siedlung_ja,
    }
    daten = {"schema": dateien.SEGMENTE_SCHEMA, "segmente": segmente, "verlauf": []}
    return Ergebnis(labels=labels, segmente=daten, kandidaten=kandidaten, messung=messung)


# --- Ablauf über Teilkacheln ------------------------------------------------------------------

@dataclass
class Auftrag:
    """Eine Teilkachel (oder ein einzelnes Bild) für die Vorstufe."""

    name: str
    bild: Path
    ziel: Path  # Ordner der Ausgaben
    id_start: int = 0
    kern: dict | None = None
    bildpunkt_m: float | None = None  # aus dem transform der Teilkachel


def auftraege_aus_manifest(manifest_pfad: str | Path, konfig: dict,
                           auswahl: list[str] | None = None) -> list[Auftrag]:
    manifest_pfad = Path(manifest_pfad)
    manifest = dateien.lese_json(manifest_pfad)
    ordner = manifest_pfad.parent
    alle = manifest.get("teilkacheln") or []
    bekannt = {t["id"] for t in alle}
    for name in auswahl or []:
        if name not in bekannt:
            raise VorstufeFehler(f"Teilkachel {name!r} fehlt im Manifest ({', '.join(sorted(bekannt))})")
    auftraege = []
    for nr, t in enumerate(alle, 1):
        if auswahl and t["id"] not in auswahl:
            continue
        auftraege.append(Auftrag(name=t["id"], bild=ordner / t["bild"],
                                 ziel=ordner / "vorstufe" / t["id"],
                                 id_start=nr * int(konfig["id_block"]),
                                 kern=t.get("kern_im_bild"),
                                 bildpunkt_m=bildpunkt_aus_transform(t.get("transform"))))
    return auftraege


def lese_bild(pfad: Path) -> np.ndarray:
    with Image.open(pfad) as bild:
        return np.asarray(bild.convert("RGB"))


def messzeile(name: str, messung: dict, befund_ok: bool, sekunden: float) -> str:
    kern = messung.get("segmente_im_kern")
    kern_text = f" (im Kern {kern})" if kern is not None else ""
    arten = ", ".join(f"{k} {v}" for k, v in sorted(messung["kandidaten"].items())) or "keine"
    return (f"{name}: {messung['hoehe']} × {messung['breite']}, Segmente {messung['segmente']}{kern_text}, "
            f"sicher: nein {messung['sicher_nein']} ({100 * messung['anteil_sicher_nein']:.1f} %, "
            f"Fläche {100 * messung['flaeche_sicher_nein']:.1f} %), Kandidaten: {arten}; "
            f"pruefen {'ok' if befund_ok else 'FEHLER'}; {sekunden:.1f} s")


def vorstufe(auftraege: list[Auftrag], konfig: dict, kat: Kategorien, modell_laden=None,
             neu: bool = False, ausgabe=print) -> list[dict]:
    """Führt die Vorstufe für alle Aufträge aus; Ergebnis je Auftrag als dict (Messung, Befund).

    ``modell_laden``: Funktion ohne Argumente, die ein Objekt mit ``berechne(bild, klassen, texte)
    -> Roh`` liefert; sie wird höchstens einmal und nur bei Bedarf aufgerufen.
    """
    abdruck_sam3 = fingerabdruck(sam3_teil(konfig))
    abdruck = fingerabdruck({k: v for k, v in konfig.items() if not k.startswith("_")})
    klassen, texte = klassen_und_texte(konfig)
    modell = None
    ergebnisse: list[dict] = []

    def bildpunkt_schritte(auftrag: Auftrag, bild: np.ndarray, sp_zukunft, roh: Roh,
                           t_start: float, sam3_s: float) -> dict:
        sp = sp_zukunft.result()
        t0 = time.perf_counter()
        erg = verschmelzen(bild, sp, roh, konfig, kat, id_start=auftrag.id_start, kern=auftrag.kern,
                           bildpunkt_m=auftrag.bildpunkt_m)
        befund = pruefen(erg.labels, erg.segmente, kat, form=bild.shape[:2])
        erg.messung.update(hoehe=int(bild.shape[0]), breite=int(bild.shape[1]))
        sekunden = time.perf_counter() - t_start
        erg.messung["laufzeit_s"] = {"sam3": round(sam3_s, 2),
                                     "verschmelzen": round(time.perf_counter() - t0, 2),
                                     "gesamt": round(sekunden, 2)}
        erg.segmente["vorstufe"] = {
            "teilkachel": auftrag.name, "bild": auftrag.bild.name, "konfig": abdruck,
            "sam3": abdruck_sam3, "modell": konfig["sam3"]["modell"],
            "erstellt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "messung": erg.messung, "pruefen": befund.als_dict()}
        erg.segmente["verlauf"].append({"zeit": erg.segmente["vorstufe"]["erstellt"],
                                        "bearbeiter": "vorstufe", "op": "vorstufe",
                                        "konfig": abdruck})
        dateien.schreibe_labels(auftrag.ziel / "labels.tif", erg.labels)
        dateien.schreibe_json(auftrag.ziel / "kandidaten.json", {
            "schema": KANDIDATEN_SCHEMA, "teilkachel": auftrag.name, "kandidaten": erg.kandidaten})
        dateien.schreibe_json(auftrag.ziel / "segmente.json", erg.segmente)  # zuletzt: fertig
        zeile = messzeile(auftrag.name, erg.messung, befund.ok, sekunden)
        if not befund.ok:
            zeile += "\n" + befund.als_text()
        ausgabe(zeile)
        return {"teilkachel": auftrag.name, "ziel": str(auftrag.ziel), "ok": befund.ok,
                "messung": erg.messung}

    arbeiter = max(1, int(konfig.get("arbeiter", 4)))
    with ThreadPoolExecutor(max_workers=arbeiter) as pool:
        offen = []
        for auftrag in auftraege:
            fertig = auftrag.ziel / "segmente.json"
            if not neu and fertig.exists():
                alt = dateien.lese_json(fertig).get("vorstufe", {})
                if alt.get("konfig") == abdruck:
                    ausgabe(f"{auftrag.name}: schon fertig mit denselben Einstellungen "
                            f"(--neu rechnet neu)")
                    ergebnisse.append({"teilkachel": auftrag.name, "ziel": str(auftrag.ziel),
                                       "ok": alt.get("pruefen", {}).get("ok", False),
                                       "messung": alt.get("messung"), "uebersprungen": True})
                    continue
            t_start = time.perf_counter()
            bild = lese_bild(auftrag.bild)
            sp_zukunft = pool.submit(uebersegmentierung, bild, konfig["uebersegmentierung"])
            roh_pfad = auftrag.ziel / "sam3_roh.npz"
            t0 = time.perf_counter()
            roh = Roh.laden(roh_pfad, abdruck_sam3)
            if roh is None or roh.werte.shape[1:] != bild.shape[:2]:
                if modell is None:
                    if modell_laden is None:
                        raise VorstufeFehler("kein SAM-3-Modell angegeben")
                    modell = modell_laden()
                roh = modell.berechne(bild, klassen, texte)
                roh.speichern(roh_pfad, abdruck_sam3)
            sam3_s = time.perf_counter() - t0
            offen.append(pool.submit(bildpunkt_schritte, auftrag, bild, sp_zukunft, roh,
                                     t_start, sam3_s))
        ergebnisse.extend(z.result() for z in offen)
    return ergebnisse
