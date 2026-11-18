"""zusammenfuehren: aus den Urteilen und der freien Abgabe je Fassung die Karten, Listen und Einigungsbündel bauen.

Je Fassung (Tabelle aus ``einstellungen/seite.json`` + ``einstellungen/lauf.json``, siehe ``landseg.lauf``):

- ``art: urteil`` (B, C): Karte = ``<ordner>/<tk>/labels.tif``, auf der die Urteils-Agents schon nachsegmentiert
  haben (bleibt unverändert); ``segmente.json`` bekommt die Klasse aus dem Urteil (``klassen: fest``:
  ``klasse_vorschlag``, sonst ``klasse_heute``; ``klassen: frei``: Code aus ``<vereinheitlichung>/codes.json``),
  ``sicher`` aus dem Urteil, die Eingriffe werden gezählt (``eingriffe`` der Urteile, Verlauf der Karte).
  Kontextrand: Mehrheit der Klasse im Kern der Nachbarkachel, außerhalb des Ausschnitts ``kontext_aussen``; immer
  ``sicher: nein``. Die ``segmente.json`` der Urteils-Agents bleibt als ``segmente.vor-zusammenfuehren.json``
  daneben; jeder Lauf baut von ihr aus.
- ``art: frei`` (A): Karte der freien Abgabe ``<ergebnis>/<tk>/``, IDs + (Nummer der Teilkachel + 1) ·
  ``id_versatz``, Codes über ``abbildung_teilkacheln`` der vereinheitlichten Liste (``klasse_teil`` hält den
  Code der Abgabe).
- Kategorienliste ``<ordner>/<liste>`` (Name aus ``seite.json``, sonst ``kategorien-<kennung>.json``),
  ``zusammentragen.json``; danach ``pruefen`` je Teilkachel, ``zusammentragen`` nach ``<ordner>/zusammen/``,
  ``naht`` und ``einigung finden`` nach ``<ziel>/<einigung>/auftraege-<kennung>/``.

Alles wird zuerst im Speicher gebaut und geprüft; ein Befund (fehlende Abgabe, Klasse nicht in der Liste, Marke
``fassung.json`` passt nicht zur Tabelle) ist ein ``LaufFehler`` (Exit 1), dann wird nichts geschrieben. Die
Urteile selbst ändert der Befehl nie; die Gegenprobe geht in keine Karte ein.
"""

from __future__ import annotations

import copy
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from . import dateien, einigung, einstellungen, kategorien, lauf, naht
from .lauf import Fassung, LaufFehler, p
from .pruefen import pruefen
from .urteil import VIERTEL
from .vorbereiten import Lauf
from .zusammentragen import kern_ausschneiden, lese_auftrag, zusammentragen

SICHERUNG = "segmente.vor-zusammenfuehren.json"
ENTWURF = "kategorien-entwurf.json"
BEARBEITER = "zusammenfuehren"
MAPPINGS = ("corine", "clc_plus", "flair", "dkm", "bericht48")


def _ja_nein(wert) -> str:
    if isinstance(wert, bool):
        return "ja" if wert else "nein"
    return "ja" if str(wert).lower() in ("ja", "true") else "nein"


def _grob(code: str) -> str:
    return str(code).split(".")[0]


def _kern(karte: np.ndarray, t: dict) -> np.ndarray:
    return kern_ausschneiden(karte, t)


class Bau:
    """Was je Fassung geschrieben wird (alles im Speicher, bis die Prüfung durch ist)."""

    def __init__(self, f: Fassung):
        self.f = f
        self.liste_pfad = f.ordner / (f.liste or f"kategorien-{f.kurz}.json")
        self.liste: dict = {}
        self.json: dict[Path, dict] = {}
        self.karten: dict[Path, np.ndarray] = {}
        self.zahlen: dict[str, dict] = {}
        self.fehler: list[str] = []
        self.ziele: list[Path] = []


# -- Listen ---------------------------------------------------------------------------------------

def _liste(b: Bau, name: str) -> set[str]:
    f = b.f
    if f.art == "urteil" and f.klassen == "fest":
        b.liste = dateien.lese_json(kategorien.STANDARD_PFAD)
    else:
        quelle = f.unter("vereinheitlichung", "vereinheitlichung") / ENTWURF
        if not quelle.is_file():
            b.fehler.append(f"{f.titel}: vereinheitlichte Liste fehlt: {p(quelle)}")
            return set()
        b.liste = copy.deepcopy(dateien.lese_json(quelle))
        b.liste["title"] = b.liste.get("title") or f"Gestufte Kategorienliste {name}, {f.titel}"
        b.liste["source"] = list(b.liste.get("source") or []) if isinstance(b.liste.get("source"), list) else (
            [b.liste["source"]] if b.liste.get("source") else [])
        b.liste["source"].append(f"{p(quelle.relative_to(f.ordner))} (von zusammenfuehren übernommen)")
        for k in b.liste.get("classes") or []:
            k.setdefault("bw", "eing.")
            k.setdefault("mappings", {m: [] for m in MAPPINGS})
        if f.art == "frei" and not isinstance(b.liste.get("abbildung_teilkacheln"), dict):
            b.fehler.append(f"{f.titel}: {p(quelle)} ohne abbildung_teilkacheln")
    return {str(k["code"]) for k in b.liste.get("classes") or []}


# -- Fassungen mit Urteil -------------------------------------------------------------------------

def _urteile(b: Bau, tk: str) -> tuple[dict, list, list]:
    f = b.f
    eintraege, eingriffe, info = {}, [], []
    for v in VIERTEL:
        pfad = f.unter("ergebnis", "urteil") / tk / v / "urteil.json"
        if not pfad.is_file():
            b.fehler.append(f"{f.titel}: Urteil fehlt: {p(pfad)}")
            continue
        u = dateien.lese_json(pfad)
        if u.get("teilkachel") not in (None, tk):
            b.fehler.append(f"{f.titel}: {p(pfad)} nennt Teilkachel {u.get('teilkachel')!r}")
        for s in u.get("segmente") or []:
            if s["id"] in eintraege:
                b.fehler.append(f"{f.titel} {tk}: Segment {s['id']} in zwei Vierteln")
            eintraege[s["id"]] = {**s, "viertel": v}
        eingriffe += [{**x, "viertel": v} for x in (u.get("eingriffe") or [])]
        info.append({"viertel": v, "bearbeiter": u.get("bearbeiter"), "segmente": len(u.get("segmente") or []),
                     "eingriffe": len(u.get("eingriffe") or []), "quelle": p(pfad.relative_to(f.ordner))})
    return eintraege, eingriffe, info


def _bau_urteil(b: Bau, l: Lauf, codes: set[str], jetzt: str) -> None:
    f = b.f
    codes_frei = None
    if f.klassen == "frei":
        pfad = f.unter("vereinheitlichung", "vereinheitlichung") / "codes.json"
        if not pfad.is_file():
            b.fehler.append(f"{f.titel}: Codes der Vereinheitlichung fehlen: {p(pfad)}")
            return
        codes_frei = dateien.lese_json(pfad).get("segmente") or {}
    aussen = str(f.werte.get("kontext_aussen") or "vorstufe")
    stand, kernklasse = {}, {}
    for tk in l.tks:
        t = l.teil[tk]
        ordner = f.ordner / tk
        sicherung = ordner / SICHERUNG
        quelle = sicherung if sicherung.is_file() else ordner / "segmente.json"
        if not (ordner / "labels.tif").is_file() or not quelle.is_file():
            b.fehler.append(f"{f.titel}: Karte fehlt: {p(ordner)}/labels.tif und segmente.json")
            continue
        if sicherung.is_file():
            b.ziele.append(sicherung)
        karte = dateien.lese_labels(ordner / "labels.tif")
        seg = dateien.lese_segmente(quelle)
        kern_ids = set(np.unique(_kern(karte, t)).tolist()) - {0}
        u, eingriffe, info = _urteile(b, tk)
        fehlt = sorted(kern_ids - set(u))
        if fehlt and info:
            b.fehler.append(f"{f.titel} {tk}: Kernsegmente ohne Urteil: {fehlt[:10]}")
        klassen = {}
        for i in kern_ids & set(u):
            e = u[i]
            if codes_frei is None:
                k = e.get("klasse_vorschlag") or e.get("klasse_heute")
            else:
                c = (codes_frei.get(tk) or {}).get(str(i))
                k = c.get("code") if isinstance(c, dict) else None
            if k not in codes:
                b.fehler.append(f"{f.titel} {tk}: Segment {i}: Klasse {k!r} nicht in der Liste")
            klassen[i] = k
        kernklasse[tk] = klassen
        stand[tk] = (karte, seg, u, kern_ids, eingriffe, info, sorted(set(u) - kern_ids), quelle)
    if b.fehler:
        return
    # Klassenkarte des Ausschnitts aus den Kernurteilen (für den Kontextrand)
    h, w = l.manifest["ausschnitt"]["hoehe"], l.manifest["ausschnitt"]["breite"]
    sortiert = sorted(codes)
    nummer = {c: n for n, c in enumerate(sortiert)}
    gesamt = np.full((h, w), -1, np.int32)
    for tk in l.tks:
        t, kk = l.teil[tk], l.teil[tk]["kern"]
        ids, inv = np.unique(_kern(stand[tk][0], t), return_inverse=True)
        werte = np.array([nummer.get(kernklasse[tk].get(i), -1) for i in ids.tolist()], np.int32)
        gesamt[kk["y"]:kk["y"] + kk["hoehe"], kk["x"]:kk["x"] + kk["breite"]] = werte[inv].reshape(kk["hoehe"], kk["breite"])
    for tk in l.tks:
        t = l.teil[tk]
        karte, seg, u, kern_ids, eingriffe, info, nicht_im_kern, quelle = stand[tk]
        kx = t["kontext"]
        ys, xs = np.mgrid[0:karte.shape[0], 0:karte.shape[1]]
        ay, ax = ys + kx["y"], xs + kx["x"]
        innen = (ay >= 0) & (ay < h) & (ax >= 0) & (ax < w)
        klassen_gesamt = np.full(karte.shape, -1, np.int32)
        klassen_gesamt[innen] = gesamt[ay[innen], ax[innen]]
        flaechen = Counter(karte.ravel().tolist())
        kflaechen = Counter(_kern(karte, t).ravel().tolist())
        alle_ids = set(flaechen)
        neu, z = [], Counter()
        gesehen = set()
        for s in seg["segmente"]:
            i = s["id"]
            if i not in alle_ids:
                b.fehler.append(f"{f.titel} {tk}: Segment {i} in segmente.json ohne Bildpunkte")
                continue
            gesehen.add(i)
            e2 = dict(s)
            e2["klasse_vorstufe"], e2["sicher_vorstufe"] = s.get("klasse"), s.get("sicher")
            e2["im_kern"] = i in kern_ids
            e2["flaeche"], e2["flaeche_kern"] = int(flaechen[i]), int(kflaechen.get(i, 0))
            for alt in ("herkunft_klasse", "urteil", "was_ist_es", "viertel", "punkte", "klasse_heute",
                        "klasse_vorschlag", "klasse_frei"):
                e2.pop(alt, None)
            if i in kern_ids:
                ur = u[i]
                e2.update({"klasse": kernklasse[tk][i], "sicher": _ja_nein(ur.get("sicher")),
                           "urteil": ur.get("urteil"), "was_ist_es": ur.get("was_ist_es"), "viertel": ur["viertel"]})
                if ur.get("punkte"):
                    e2["punkte"] = ur["punkte"]
                if f.klassen == "fest":
                    e2["klasse_heute"], e2["klasse_vorschlag"] = ur.get("klasse_heute"), ur.get("klasse_vorschlag")
                else:
                    e2["klasse_frei"] = ur.get("klasse_frei")
                z["sicher_ja" if e2["sicher"] == "ja" else "sicher_nein"] += 1
            else:
                werte = klassen_gesamt[karte == i]
                werte = werte[werte >= 0]
                if werte.size:
                    e2["klasse"] = sortiert[Counter(werte.tolist()).most_common(1)[0][0]]
                    e2["herkunft_klasse"] = "Kontextrand: Klasse aus dem Urteil der Nachbarkachel (Mehrheit der Bildpunkte)"
                    z["kontext_nachbar"] += 1
                else:
                    e2["klasse"] = s.get("klasse") if aussen == "vorstufe" else aussen
                    e2["herkunft_klasse"] = ("Kontextrand außerhalb des Ausschnitts: Klasse der Vorstufe"
                                             if aussen == "vorstufe" else
                                             f"Kontextrand außerhalb des Ausschnitts: ohne Urteil, {aussen}")
                    z["kontext_ausserhalb"] += 1
                e2["sicher"], e2["urteil"] = "nein", "kontextrand"
            if e2["klasse"] not in codes:
                b.fehler.append(f"{f.titel} {tk}: Segment {i}: Klasse {e2['klasse']!r} nicht in der Liste")
            e2["grob"] = _grob(e2["klasse"])
            neu.append(e2)
        if alle_ids - gesehen - {0}:
            b.fehler.append(f"{f.titel} {tk}: Segmente ohne Eintrag: {sorted(alle_ids - gesehen)[:10]}")
        n_verlauf = sum(1 for v in seg.get("verlauf") or [] if v.get("bearbeiter") != "vorstufe")
        quelle_text = f"{p(f.unter('ergebnis', 'urteil').relative_to(f.ordner))}/{tk}/v1..v4/urteil.json"
        verlauf = list(seg.get("verlauf") or []) + [{
            "nr": len(seg.get("verlauf") or []) + 1, "zeit": jetzt, "bearbeiter": BEARBEITER,
            "op": "klassen_aus_urteil",
            "parameter": {"quelle": quelle_text,
                          "regel": ("klasse = klasse_vorschlag, sonst klasse_heute" if f.klassen == "fest" else
                                    "klasse = Code aus codes.json der Vereinheitlichung")},
            "ergebnis": {"kern": len(kern_ids), "kontext_nachbar": z["kontext_nachbar"],
                         "kontext_ausserhalb": z["kontext_ausserhalb"]}}]
        ziel = {k: v for k, v in seg.items() if k not in ("segmente", "verlauf")}
        ziel.update({"fassung": f.kennung, "teilkachel": tk,
                     "stand": f"{f.titel}, Karte nach den Eingriffen der Urteils-Agents, Klassen aus {quelle_text}",
                     "urteil": {"viertel": info, "eingriffe_urteil": len(eingriffe), "eingriffe_verlauf": n_verlauf,
                                "nicht_im_kern": nicht_im_kern},
                     "verlauf": verlauf, "segmente": neu})
        b.json[f.ordner / tk / "segmente.json"] = ziel
        b.json[f.ordner / tk / SICHERUNG] = seg
        b.zahlen[tk] = {"kern": len(kern_ids), "segmente": len(neu), "sicher_ja": z["sicher_ja"],
                        "sicher_nein": z["sicher_nein"], "kontext_nachbar": z["kontext_nachbar"],
                        "kontext_ausserhalb": z["kontext_ausserhalb"], "eingriffe_urteil": len(eingriffe),
                        "eingriffe_verlauf": n_verlauf, "urteil_nicht_im_kern": nicht_im_kern}


# -- freie Fassung --------------------------------------------------------------------------------

def _bau_frei(b: Bau, l: Lauf, codes: set[str], jetzt: str) -> None:
    f = b.f
    abb = b.liste.get("abbildung_teilkacheln") or {}
    schritt = int(f.werte.get("id_versatz") or 100000)
    for nr, tk in enumerate(l.tks):
        t = l.teil[tk]
        ab = f.unter("ergebnis", "abgabe") / tk
        if not (ab / "labels.tif").is_file() or not (ab / "segmente.json").is_file():
            b.fehler.append(f"{f.titel}: Abgabe fehlt: {p(ab)}/labels.tif und segmente.json")
            continue
        karte = dateien.lese_labels(ab / "labels.tif").astype(np.uint32)
        seg = dateien.lese_segmente(ab / "segmente.json")
        teil_liste = ab / "kategorien-teil.json"
        teil = ({c["code"]: c["name"] for c in dateien.lese_json(teil_liste).get("classes") or []}
                if teil_liste.is_file() else {})
        versatz = (nr + 1) * schritt
        if int(karte.max()) >= schritt:
            b.fehler.append(f"{f.titel} {tk}: IDs ab {schritt}, Versatz nicht eindeutig")
            continue
        abbildung = abb.get(tk)
        if not isinstance(abbildung, dict):
            b.fehler.append(f"{f.titel} {tk}: abbildung_teilkacheln.{tk} fehlt in der Liste")
            continue
        kern_ids = set(np.unique(_kern(karte, t)).tolist())
        flaechen = Counter(karte.ravel().tolist())
        kflaechen = Counter(_kern(karte, t).ravel().tolist())
        neu, ohne = [], Counter()
        for s in seg["segmente"]:
            e = dict(s)
            e["id_abgabe"], e["id"] = s["id"], s["id"] + versatz
            e["klasse_teil"], e["klasse_teil_name"] = s["klasse"], teil.get(s["klasse"])
            if s["klasse"] not in abbildung:
                ohne[s["klasse"]] += 1
            e["klasse"] = abbildung.get(s["klasse"], s["klasse"])
            if e["klasse"] not in codes:
                b.fehler.append(f"{f.titel} {tk}: Segment {s['id']}: Klasse {e['klasse']!r} nicht in der Liste")
            e["grob"] = _grob(e["klasse"])
            e["sicher"] = _ja_nein(s.get("sicher"))
            e["im_kern"] = s["id"] in kern_ids
            e["flaeche"], e["flaeche_kern"] = int(flaechen[s["id"]]), int(kflaechen.get(s["id"], 0))
            neu.append(e)
        if ohne:
            b.fehler.append(f"{f.titel} {tk}: Codes der Abgabe ohne Abbildung in der Liste: {dict(ohne)}")
        if {e["id_abgabe"] for e in neu} != set(flaechen):
            b.fehler.append(f"{f.titel} {tk}: Segmente der Karte und der segmente.json stimmen nicht überein")
        ziel = f.ordner / tk
        b.ziele.append(ziel)
        b.karten[ziel / "labels.tif"] = (karte + np.uint32(versatz)).astype(np.uint32)
        verlauf = list(seg.get("verlauf") or []) + [{
            "zeit": jetzt, "bearbeiter": BEARBEITER, "op": "abgabe_uebernehmen",
            "parameter": {"quelle": f"{p(ab.relative_to(f.ordner))}/", "id_versatz": versatz,
                          "liste": b.liste_pfad.name}}]
        b.json[ziel / "segmente.json"] = {**{k: v for k, v in seg.items() if k not in ("segmente", "verlauf")},
                                          "schema": "landseg-segmente/1", "teilkachel": tk, "fassung": f.kennung,
                                          "stand": f"Abgabe {f.kennung} {tk}, Codes nach {b.liste_pfad.name}, "
                                                   f"ID + {versatz}",
                                          "verlauf": verlauf, "segmente": neu}
        im_kern = [e for e in neu if e["im_kern"]]
        b.zahlen[tk] = {"kern": len(kern_ids), "segmente": len(neu), "versatz": versatz,
                        "sicher_ja": sum(e["sicher"] == "ja" for e in im_kern),
                        "sicher_nein": sum(e["sicher"] == "nein" for e in im_kern)}


# -- Ablauf ---------------------------------------------------------------------------------------

def bauen(manifest: str | Path, ziel: str | Path, *, werte: dict | None = None, seite: dict | None = None,
          ersetzen: bool = False) -> dict:
    """Prüft und baut alle Fassungen; gibt die Zahlen je Fassung zurück. Befund vor dem Schreiben: ``LaufFehler``."""
    t0 = time.perf_counter()
    lw, sw = lauf.einstellungen_laden()
    l = Lauf(manifest, ziel, werte or lw, seite or sw)
    jetzt = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    einigung_ordner = l.ziel / str(l.werte.get("einigung") or "einigung")
    baue, fehler = [], []
    for f in l.fassungen:
        b = Bau(f)
        b.fehler += lauf.marke_pruefen(f)
        if not f.ordner.is_dir():
            b.fehler.append(f"{f.titel}: Fassungsordner fehlt: {p(f.ordner)}")
        else:
            codes = _liste(b, l.name)
            if not b.fehler:
                (_bau_urteil if f.art == "urteil" else _bau_frei)(b, l, codes, jetzt)
        b.json[b.liste_pfad] = b.liste
        b.json[f.ordner / "zusammentragen.json"] = {
            "schema": "landseg-zusammentragen/1", "manifest": p(Path("..") / l.manifest_pfad.name)
            if f.ordner.parent == l.daten else p(l.manifest_pfad),
            "einheiten": [{"teilkachel": tk, "labels": f"{tk}/labels.tif", "segmente": f"{tk}/segmente.json",
                           "runde": 0, "name": f"{f.kurz}-{tk}"} for tk in l.tks],
            "ziel": "zusammen"}
        b.ziele += [b.liste_pfad, f.ordner / "zusammentragen.json", f.ordner / "zusammen",
                    einigung_ordner / f"auftraege-{f.kennung}"]
        fehler += b.fehler
        baue.append(b)
    if fehler:
        raise LaufFehler(fehler)
    befund_pfad = l.ziel / "zusammenfuehren.json"
    lauf.frei_machen([z for b in baue for z in b.ziele] + [befund_pfad], ersetzen)

    for b in baue:
        for pfad, karte in b.karten.items():
            dateien.schreibe_labels(pfad, karte)
        for pfad, daten in b.json.items():
            dateien.schreibe_json(pfad, daten)

    bild = naht.lese_bild(l.daten / l.manifest["ausschnitt"]["bild"])
    einst = einstellungen.laden("einigung")
    ergebnis = {"schema": "landseg-zusammenfuehren/1", "zeit": jetzt, "manifest": p(l.manifest_pfad),
                "fassungen": {}}
    for b in baue:
        f = b.f
        kat = kategorien.laden(b.liste_pfad)
        pruef = {}
        for tk in l.tks:
            befund = pruefen(dateien.lese_labels(f.ordner / tk / "labels.tif"),
                             dateien.lese_segmente(f.ordner / tk / "segmente.json"), kat)
            pruef[tk] = "ok" if befund.ok else " | ".join(befund.als_text().splitlines()[:3])
        auftrag = f.ordner / "zusammentragen.json"
        zt = zusammentragen(auftrag, kat, bearbeiter=BEARBEITER)
        a = lese_auftrag(auftrag)
        nb = naht.pruefe_naehte(dateien.lese_labels(zt.ziel / "labels.tif"), l.manifest, bild, a.get("naht"),
                                a.get("naht_bestaetigt"))
        fe = einigung.fassung_laden(l.manifest_pfad, f.ordner, kat, f.kennung)
        gefunden = einigung.finden(fe, bild, einst, einigung_ordner / f"auftraege-{f.kennung}")
        kern = [z for z in b.zahlen.values()]
        ergebnis["fassungen"][f.kennung] = {
            "name": f.name, "ordner": p(f.ordner), "liste": p(b.liste_pfad),
            "segmente_kern": sum(z["kern"] for z in kern), "segmente": sum(z["segmente"] for z in kern),
            "unsicher": sum(z["sicher_nein"] for z in kern),
            "eingriffe_urteil": sum(z.get("eingriffe_urteil", 0) for z in kern),
            "eingriffe_verlauf": sum(z.get("eingriffe_verlauf", 0) for z in kern),
            "pruefen": pruef, "zusammentragen_ok": zt.ok, "zusammentragen_maengel": zt.maengel,
            "nahtverstoesse": len(nb.verstoesse), "klassen_konflikte": len(zt.klassen_konflikte),
            "einigung_offen": gefunden["zahlen"]["offen"]["paare"],
            "buendel": [{"name": x["buendel"], "ordner": p(einigung_ordner / f"auftraege-{f.kennung}" / x["buendel"]),
                         "paare": x["paare"], "uebergross": x["uebergross"]} for x in gefunden["buendel"]],
            "auftraege": p(einigung_ordner / f"auftraege-{f.kennung}"), "teilkacheln": b.zahlen}
    ergebnis["sekunden"] = round(time.perf_counter() - t0, 1)
    ergebnis["ok"] = all(x == "ok" for e in ergebnis["fassungen"].values() for x in e["pruefen"].values())
    dateien.schreibe_json(befund_pfad, ergebnis)
    return ergebnis
