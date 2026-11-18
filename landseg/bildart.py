"""Feinheit je Bildart: Richtwert der Segmentzahl, Mindestfläche, Vorstufe und Zusammenlegen kleiner Flächen.

Die Bildart (``farbe``, ``sw`` …) kommt aus dem Manifest: Feld ``bildart``, sonst ``quelle.kanaele`` 1 = ``sw``,
sonst ``farbe``. Was sie bedeutet, steht in ``einstellungen/bildarten.json``: Richtwert der Segmente je Million
Bildpunkte Kern, Mindestfläche in m², geschützte Objekte und die Schlüssel, mit denen die Vorstufe ``vorstufe.json``
überschreibt. Eine Bildart ohne Richtwert und Mindestfläche (Farbe) ändert nichts.

``kleine_zusammenlegen`` legt Segmente unter der Mindestfläche mit einem Nachbarn zusammen, nur über
``Bearbeitung.verschmelzen`` (Regel L1): bevorzugt ein Nachbar derselben Klasse, sonst der mit der längsten
gemeinsamen Grenze; ID und Klasse behält die größere Fläche, bei Gleichstand die sichere. Klar erkennbare
Objekte (``schutz``) bleiben. Ein Segment an einer Kern- oder Viertelgrenze geht nur in einen Nachbarn derselben
Klasse auf und gibt seine Einigungs-Beschlüsse an ihn weiter (Nähte und Einigung bleiben gültig).
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np

from . import einstellungen
from .dateien import segmente_nach_id

STANDARD = "farbe"


class BildartFehler(Exception):
    pass


def laden(pfad: str | Path | None = None) -> dict:
    """Einstellungen aller Bildarten (``einstellungen/bildarten.json``, mit ``pfad`` überschrieben)."""
    return einstellungen.laden("bildarten", pfad)["bildarten"]


def bildart_von(manifest: dict) -> str:
    """Bildart aus dem Manifest: Feld ``bildart``, sonst ein Kanal = ``sw``, sonst ``farbe``."""
    if manifest.get("bildart"):
        return str(manifest["bildart"])
    return "sw" if (manifest.get("quelle") or {}).get("kanaele") == 1 else STANDARD


def bildart_von_bild(pfad: str | Path) -> str:
    """Bildart eines einzelnen Bildes (ohne Manifest): Graustufen = ``sw``."""
    from PIL import Image
    with Image.open(pfad) as bild:
        return "sw" if bild.mode in ("1", "L", "LA", "I", "I;16", "F") else STANDARD


def eintrag(art: str, werte: dict | None = None) -> dict:
    werte = laden() if werte is None else werte
    if art not in werte:
        raise BildartFehler(f"Bildart {art!r} fehlt in einstellungen/bildarten.json ({', '.join(sorted(werte))})")
    return werte[art]


def bildpunkt_m(art_eintrag: dict, transform_m: float | None) -> float | None:
    return transform_m or art_eintrag.get("bildpunkt_m")


def feinheit(art: str, kern_px: int | None = None, transform_m: float | None = None,
             werte: dict | None = None) -> dict:
    """Richtwert (Segmente im Kern) und Mindestfläche (m², Bildpunkte) einer Bildart; ``None`` = ohne."""
    e = eintrag(art, werte)
    je_mio = e.get("richtwert_je_mio_px")
    m2 = e.get("mindestflaeche_m2")
    bp = bildpunkt_m(e, transform_m)
    if m2 and not bp:
        raise BildartFehler(f"Bildart {art!r}: Mindestfläche ohne Bildpunktgröße (bildpunkt_m)")
    return {
        "bildart": art,
        "name": e.get("name", art),
        "richtwert_je_mio_px": je_mio,
        "richtwert": round(je_mio * kern_px / 1e6) if je_mio and kern_px else None,
        "mindestflaeche_m2": m2,
        "mindest_px": math.ceil(m2 / (bp * bp)) if m2 else None,
        "bildpunkt_m": bp,
        "schutz": e.get("schutz") or {},
    }


def feinheit_aus_manifest(manifest: dict, teilkachel: str | None = None, werte: dict | None = None) -> dict:
    """Feinheit für eine Teilkachel des Manifests (Richtwert für ihren Kern) oder den ganzen Ausschnitt."""
    from .vorstufe import bildpunkt_aus_transform
    art = bildart_von(manifest)
    if teilkachel is None:
        a = manifest.get("ausschnitt") or {}
        return feinheit(art, int(a.get("breite", 0)) * int(a.get("hoehe", 0)) or None, werte=werte)
    for t in manifest.get("teilkacheln") or []:
        if t["id"] == teilkachel:
            k = t.get("kern_im_bild") or t.get("kern") or {}
            return feinheit(art, int(k.get("breite", 0)) * int(k.get("hoehe", 0)) or None,
                            bildpunkt_aus_transform(t.get("transform")), werte)
    raise BildartFehler(f"Teilkachel {teilkachel!r} fehlt im Manifest")


def vorstufe_konfig(konfig: dict, art: str, werte: dict | None = None) -> dict:
    """``vorstufe.json`` mit den Schlüsseln der Bildart überschrieben (Farbe: unverändert dasselbe Objekt)."""
    ueber = {k: ({kk: vv for kk, vv in v.items() if not kk.startswith("_")} if isinstance(v, dict) else v)
             for k, v in (eintrag(art, werte).get("vorstufe") or {}).items() if not k.startswith("_")}
    if not ueber:
        return konfig
    if "sam3" in ueber or "prompts" in ueber:
        raise BildartFehler(f"Bildart {art!r}: sam3 und prompts gehören nicht in die Bildart (Rohdaten)")
    return einstellungen.ueberschreiben(konfig, ueber)


# --- Zusammenlegen kleiner Flächen ------------------------------------------------------------------

def _sicher(e: dict) -> bool:
    return e.get("sicher") in ("ja", True)


def geschuetzt(e: dict, schutz: dict, kat=None) -> bool:
    """Klar erkennbares Objekt: (sicher, wenn ``nur_sicher``) und der Kopf des Klassennamens enthält ein
    Schutzwort. Kopf: der Name bis zur ersten Klammer oder zum ersten Lagewort (``schutz.lagewoerter``, etwa
    „zwischen“, „an“): ``Gebäude (Dachfläche)``, ``langes Haus auf dem Anger``, ``Baumreihe an der Dorfstraße``
    sind geschützt, ``Schattenfuge zwischen Gebäuden`` nicht (der Zusatz nennt nur die Lage)."""
    if schutz.get("nur_sicher", True) and not _sicher(e):
        return False
    name = e.get("name")
    if not name and kat is not None:
        try:
            name = kat.name(e.get("klasse"))
        except Exception:  # Klasse nicht in der Liste: dann kein Schutz über den Namen
            name = None
    lage = {str(w).lower() for w in schutz.get("lagewoerter") or []}
    kopf = []
    for wort in str(name or "").lower().split("(")[0].split():
        if wort.strip(",;:") in lage:
            break
        kopf.append(wort)
    kopf = " ".join(kopf)
    return any(str(w).lower() in kopf for w in schutz.get("namen") or [])


def naht_ids(karte: np.ndarray, kern: dict | None) -> set[int]:
    """IDs auf Kerngrenze und Viertelgrenzen (je zwei Reihen; dort misst `einigung` Paare)."""
    if not kern:
        return set()
    h, w = karte.shape
    x0, y0 = int(kern["x"]), int(kern["y"])
    x1, y1 = x0 + int(kern["breite"]), y0 + int(kern["hoehe"])
    band = np.zeros_like(karte, dtype=bool)
    ym, xm = y0 + int(kern["hoehe"]) // 2, x0 + int(kern["breite"]) // 2  # Viertelgrenzen wie vorbereiten
    for y in (y0 - 1, y0, y1 - 1, y1, ym - 1, ym):
        if 0 <= y < h:
            band[y, max(0, x0 - 1):min(w, x1 + 1)] = True
    for x in (x0 - 1, x0, x1 - 1, x1, xm - 1, xm):
        if 0 <= x < w:
            band[max(0, y0 - 1):min(h, y1 + 1), x] = True
    return set(np.unique(karte[band]).tolist())


def grenzlaengen(karte: np.ndarray, sid: int) -> dict[int, int]:
    """Nachbar-ID -> Länge der gemeinsamen Grenze (Bildpunktkanten, 4er-Nachbarschaft)."""
    ys, xs = np.nonzero(karte == sid)
    if not len(ys):
        return {}
    y0, y1 = max(0, ys.min() - 1), min(karte.shape[0], ys.max() + 2)
    x0, x1 = max(0, xs.min() - 1), min(karte.shape[1], xs.max() + 2)
    sub = karte[y0:y1, x0:x1]
    m = sub == sid
    nachbarn = []
    for a, b in ((m[1:], sub[:-1]), (m[:-1], sub[1:]), (m[:, 1:], sub[:, :-1]), (m[:, :-1], sub[:, 1:])):
        n = b[a]
        nachbarn.append(n[n != sid])
    alle = np.concatenate(nachbarn)
    ids, zahl = np.unique(alle, return_counts=True)
    return dict(zip(ids.tolist(), zahl.tolist()))


def _einigung_mitnehmen(arbeit, eintraege: dict, ab: int, ziel: int) -> int:
    """Die Einigungs-Beschlüsse von ``ab`` gehen auf ``ziel`` über (``verschmelzen`` löscht den Eintrag von
    ``ab``); die Namen im ``paar`` stellt ``einigung_umbenennen`` um. Ergebnis: Zahl der Beschlüsse."""
    alte = list(eintraege[ab].get("einigung") or [])
    if alte:
        bisher = list(segmente_nach_id(arbeit.segmente)[ziel].get("einigung") or [])
        arbeit.vermerken(ziel, {"einigung": bisher + alte}, op="einigung")
    return len(alte)


def einigung_umbenennen(arbeiten: dict, ersetzt: dict) -> dict[str, int]:
    """Stellt die Einigungs-Beschlüsse aller Teilkacheln einer Fassung auf die zusammengelegten Segmente um.

    ``arbeiten``: Teilkachel -> ``eingriff.Bearbeitung``; ``ersetzt``: Teilkachel -> {weggefallene ID: ID, in
    der sie aufging}. ``paar`` und ``mit`` jedes Beschlusses nennen danach die neuen Segmente (auch auf der Seite
    des Partners, wo der Beschluss oft allein steht), damit ``einigung messen`` die geeinigten Paare wiederfindet;
    ein Beschluss, dessen beide Seiten in dasselbe Segment aufgingen, fällt weg. Ergebnis: Teilkachel -> Zahl
    der geänderten Beschlüsse."""
    from .einigung import paar_name

    def neu(name: str) -> str:
        tk, sid = name.rsplit(":", 1)
        return f"{tk}:{ersetzt.get(tk, {}).get(int(sid), int(sid))}" if sid.isdigit() else name

    geaendert: dict[str, int] = {}
    for tk, arbeit in arbeiten.items():
        geaendert[tk] = 0
        for e in list(arbeit.segmente["segmente"]):
            alte = e.get("einigung") or []
            neue, anders = [], False
            for b in alte:
                teile = str(b.get("paar", "")).split("|")
                if len(teile) != 2:
                    neue.append(b)
                    continue
                a, c = (neu(t) for t in teile)
                if a == c:
                    anders = True
                    geaendert[tk] += 1
                    continue
                n = {**b, "paar": paar_name(a, c)}
                if b.get("mit"):
                    n["mit"] = neu(str(b["mit"]))
                anders |= n != b
                geaendert[tk] += n != b
                neue.append(n)
            if anders:
                arbeit.vermerken(e["id"], {"einigung": neue}, op="einigung")
    return geaendert


def kleine_zusammenlegen(arbeit, mindest_px: int, schutz: dict | None = None, kern: dict | None = None,
                         kat=None) -> dict:
    """Legt Segmente unter ``mindest_px`` mit einem Nachbarn zusammen (über ``arbeit.verschmelzen``).

    ``arbeit``: ``eingriff.Bearbeitung``. Ein Segment auf einer Kern- oder Viertelgrenze oder im Kontextrand
    (``naht_ids``) geht nur in einen Nachbarn derselben Klasse auf, und seine Einigungs-Beschlüsse ziehen mit
    um (``ersetzt``; die Namen in den Beschlüssen der ganzen Fassung stellt danach ``einigung_umbenennen`` um):
    so bleibt die Klasse an jeder Linie gleich und die Einigung gültig. Klar erkennbare Objekte (``schutz``)
    bleiben. Aktualisiert danach ``flaeche`` (und, wo vorhanden, ``flaeche_px``, ``flaeche_kern``, ``kern_px``,
    ``im_kern``) der übrigen Segmente. Ergebnis: Zahlen vorher/nachher.
    """
    schutz = schutz or {}
    eintraege = segmente_nach_id(arbeit.segmente)
    ids, zahl = np.unique(arbeit.karte, return_counts=True)
    flaeche = dict(zip(ids.tolist(), zahl.tolist()))
    vorher = len(flaeche)
    an_naht = naht_ids(arbeit.karte, kern)
    im_kern: set[int] = set(flaeche)
    if kern:  # Segmente ganz im Kontextrand gehören der Nachbar-Teilkachel (Einigung): wie die Naht
        im_kern = set(np.unique(_kern(arbeit.karte, kern)).tolist())
        an_naht |= set(flaeche) - im_kern
    weg: set[int] = set()
    bleiben = {"schutz": 0, "naht": 0, "ohne_nachbar": 0}
    klein = sorted((sid for sid, f in flaeche.items() if f < mindest_px), key=lambda s: (flaeche[s], s))
    zusammengelegt = an_der_naht = umgezogen = 0
    ersetzt: dict[int, int] = {}  # weggefallene ID an der Naht -> ID, in der sie aufging
    for sid in klein:
        if sid in weg or flaeche[sid] >= mindest_px:
            continue
        e = eintraege[sid]
        if geschuetzt(e, schutz, kat):
            bleiben["schutz"] += 1
            continue
        nachbarn = grenzlaengen(arbeit.karte, sid)
        if not nachbarn:
            bleiben["ohne_nachbar"] += 1
            continue
        rang = (flaeche[sid], _sicher(e))
        # Berührung im Kern: nur sie hält das Zusammengelegte im Kern zusammenhängend (zusammentragen schneidet
        # den Kontextrand ab)
        im_kern_nachbarn = grenzlaengen(_kern(arbeit.karte, kern), sid) if kern and sid in an_naht else nachbarn

        def erlaubt(n: int) -> bool:
            """Das Segment, das wegfällt (das kleinere), ist nicht geschützt; liegt es an der Naht, haben beide
            dieselbe Klasse; liegen beide im Kern, berühren sie sich dort."""
            ab, bleibt = (sid, n) if (flaeche[n], _sicher(eintraege[n])) >= rang else (n, sid)
            if ab == n and geschuetzt(eintraege[n], schutz, kat):
                return False
            if sid in im_kern and n in im_kern and n not in im_kern_nachbarn:
                return False
            return ab not in an_naht or eintraege[ab].get("klasse") == eintraege[bleibt].get("klasse")

        moeglich = [n for n in nachbarn if erlaubt(n)]
        if not moeglich:
            bleiben["naht" if sid in an_naht else "ohne_nachbar"] += 1
            continue
        gleich = [n for n in moeglich if eintraege[n].get("klasse") == e.get("klasse")]
        wahl = max(gleich or moeglich, key=lambda n: (nachbarn[n], flaeche[n], -n))
        # ID und Klasse behält die größere Fläche, bei Gleichstand die sichere
        if (flaeche[wahl], _sicher(eintraege[wahl])) >= rang:
            ziel, ab = wahl, sid
        else:
            ziel, ab = sid, wahl
        naht_ab = ab in an_naht
        arbeit.verschmelzen([ziel, ab], ziel)
        if naht_ab:
            umgezogen += _einigung_mitnehmen(arbeit, eintraege, ab, ziel)
            for alt in [k for k, v in ersetzt.items() if v == ab]:
                ersetzt[alt] = ziel
            ersetzt[ab] = ziel
            an_naht.add(ziel)
            an_der_naht += 1
        if ab in im_kern:
            im_kern.add(ziel)
        eintraege = segmente_nach_id(arbeit.segmente)
        flaeche[ziel] += flaeche.pop(ab)
        weg.add(ab)
        zusammengelegt += 1
    _flaechen_nachziehen(arbeit, kern)
    return {"vorher": vorher, "nachher": len(flaeche), "zusammengelegt": zusammengelegt,
            "an_der_naht": an_der_naht, "einigung_umgezogen": umgezogen, "ersetzt": ersetzt,
            "mindest_px": mindest_px, "bleiben_unter_mindest": bleiben}



def _kern(karte: np.ndarray, kern: dict) -> np.ndarray:
    return karte[kern["y"]:kern["y"] + kern["hoehe"], kern["x"]:kern["x"] + kern["breite"]]


def _flaechen_nachziehen(arbeit, kern: dict | None) -> None:
    karte = arbeit.karte
    ids, zahl = np.unique(karte, return_counts=True)
    flaeche = dict(zip(ids.tolist(), zahl.tolist()))
    im_kern: dict[int, int] = {}
    if kern:
        aus = karte[kern["y"]:kern["y"] + kern["hoehe"], kern["x"]:kern["x"] + kern["breite"]]
        ki, kz = np.unique(aus, return_counts=True)
        im_kern = dict(zip(ki.tolist(), kz.tolist()))
    for e in arbeit.segmente["segmente"]:
        f = flaeche.get(e["id"], 0)
        for schluessel in ("flaeche", "flaeche_px"):
            if schluessel in e:
                e[schluessel] = int(f)
        if kern:
            k = im_kern.get(e["id"], 0)
            for schluessel in ("flaeche_kern", "kern_px"):
                if schluessel in e:
                    e[schluessel] = int(k)
            if "im_kern" in e:
                e["im_kern"] = bool(k)


def feinheit_text(fein: dict) -> str:
    """Eine Zeile für Messung und Ausgabe."""
    if not fein.get("richtwert") and not fein.get("mindest_px"):
        return f"Bildart {fein['bildart']} ({fein['name']}): ohne Richtwert und Mindestfläche"
    return (f"Bildart {fein['bildart']} ({fein['name']}): Richtwert {fein['richtwert']} Segmente im Kern, "
            f"Mindestfläche {fein['mindestflaeche_m2']} m² = {fein['mindest_px']} Bildpunkte")


def auftrag_block(fein: dict) -> str:
    """``{{FEINHEIT}}`` der Aufträge: Abschnitt ``feinheit-<bildart>`` aus ``vorlagen/abschnitte.md`` als Absatz
    (Leerzeile davor), für eine Bildart ohne Text leer."""
    from . import lauf
    werte = {"RICHTWERT": str(fein.get("richtwert") or "–"),
             "MINDESTFLAECHE_QM": str(fein.get("mindestflaeche_m2") or "–"),
             "MINDESTFLAECHE_PX": str(fein.get("mindest_px") or "–")}
    text = lauf.fuellen(lauf.abschnitt("feinheit-" + fein["bildart"]), werte).strip()
    return f"\n\n{text}" if text else ""
