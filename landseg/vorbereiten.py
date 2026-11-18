"""vorbereiten: alles, was die Urteils-Agents eines Laufs brauchen, aus Manifest, Vorstufe und Einstellungen.

Eingaben: ``manifest.json`` von ``kacheln`` (Ordner = Daten des Ausschnitts), die fertige Vorstufe
(``<daten>/vorstufe/<tk>/labels.tif`` und ``segmente.json``; die GPU-Vorstufe ist ein eigener Befehl), die
Fassungstabelle (``einstellungen/seite.json`` + ``einstellungen/lauf.json``, siehe ``landseg.lauf``) und die
Vorlagen in ``vorlagen/``. Schreibt

- unter ``<daten>``: ``ganz/<name>_raster.jpg`` (Ausschnitt mit Teilkachelgitter), je Teilkachel ``ganz/<tk>/``
  (``ganz_roh.jpg``, ``ganz_nummern.jpg`` mit Vierteln, ``ganz.json``) und ``viertel/<tk>/v<n>/`` (Übersicht in
  sechs Bildarten, vier Nahansichten als Paar, ``viertel.json`` mit Fenstern und Segmentliste); je Fassung die
  Marke ``fassung.json``, für Fassungen mit Urteil die Kartenkopien der Vorstufe ``<ordner>/<tk>/`` (und für die
  Gegenprobe ``<ordner>/<karte>/<tk>/``), für die freie Fassung die Ansichten ``<ordner>/<ansicht>/<tk>/``, und
  leere Ergebnisordner;
- unter ``<ziel>``: ``auftraege/<art>/<tk>/[v<n>/]auftrag.md``, ``auftraege/<art>/vereinheitlichen.md`` und den
  Plan ``auftraege.json`` (Eingabe von ``landseg plan``).

Danach prüft der Befehl sich selbst (``pruefen``): jedes Kernsegment in genau einem Viertel-Auftrag je Fassung,
kein Platzhalter übrig, jedes genannte Bild da, Kartenkopien bildpunktgleich zur Vorstufe. Ein Befund ist ein
``LaufFehler`` (Exit 1).
"""

from __future__ import annotations

import shutil
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import cv2
import numpy as np
from PIL import Image
from scipy import ndimage

from . import dateien, einstellungen, kategorien, lauf, naht
from .ansicht import Ansicht, Fenster, _text, grenzen
from .ansicht import ansicht as ansicht_schreiben
from .lauf import Fassung, LaufFehler, p
from .plan import ARTEN as PLAN_ARTEN
from .urteil import VIERTEL, viertel_zuordnen
from .zoom import bild_rgb

SCHEMA = "landseg-auftraege/1"
LAGE = {"v1": "oben links", "v2": "oben rechts", "v3": "unten links", "v4": "unten rechts"}
KARTE = ("labels.tif", "segmente.json", "kandidaten.json")
WEISS, GRAU = (255, 255, 255), (175, 175, 175)


# -- Viertel ------------------------------------------------------------------------------------

def viertel_rechtecke(kern: dict) -> dict[str, tuple[int, int, int, int]]:
    """Viertel des Kerns (x, y, breite, hoehe im Teilkachelbild), Teilung wie ``urteil.viertel_zuordnen``."""
    x, y, b, h = kern["x"], kern["y"], kern["breite"], kern["hoehe"]
    hb, hh = b // 2, h // 2
    return {"v1": (x, y, hb, hh), "v2": (x + hb, y, b - hb, hh), "v3": (x, y + hh, hb, h - hh),
            "v4": (x + hb, y + hh, b - hb, h - hh)}


def einteilen(labels: np.ndarray, seg: dict, kern: dict, kat, kand: dict, modulo: int) -> dict:
    """Kernsegmente je Viertel (Liste in Lesereihenfolge) samt Anteil, Punkt und Kandidaten."""
    k = labels[kern["y"]:kern["y"] + kern["hoehe"], kern["x"]:kern["x"] + kern["breite"]]
    zuordnung = viertel_zuordnen(k)
    vr = viertel_rechtecke(kern)
    eintraege = dateien.segmente_nach_id(seg)
    ohne = sorted(set(zuordnung) - set(eintraege))
    if ohne:
        raise LaufFehler(f"Kernsegmente ohne Eintrag in segmente.json: {ohne[:10]}")
    anteil: dict[int, dict[str, int]] = {sid: dict.fromkeys(vr, 0) for sid in zuordnung}
    for v, (x, y, b, h) in vr.items():
        ids, zahl = np.unique(labels[y:y + h, x:x + b], return_counts=True)
        for sid, z in zip(ids.tolist(), zahl.tolist()):
            if sid in anteil:
                anteil[sid][v] = z
    liste: dict[str, list[dict]] = {v: [] for v in vr}
    for sid, v in zuordnung.items():
        vx, vy, vb, vh = vr[v]
        abstand = ndimage.distance_transform_edt(np.pad(labels[vy:vy + vh, vx:vx + vb] == sid, 1))[1:-1, 1:-1]
        py, px = np.unravel_index(int(np.argmax(abstand)), abstand.shape)
        e = eintraege[sid]
        kf = sum(anteil[sid].values())
        liste[v].append({"id": sid, "nr": sid % modulo, "klasse": e.get("klasse"),
                         "name": kat.name(e["klasse"]) if kat.gueltig(e.get("klasse")) else "?",
                         "sicher": e.get("sicher"), "im_siedlung": e.get("im_siedlung"), "kern_flaeche": kf,
                         "anteil": round(anteil[sid][v] / kf, 3),
                         "auch_in": [w for w in vr if w != v and anteil[sid][w]],
                         "punkt": [int(vx + px), int(vy + py)], "kandidaten": sorted(kand.get(sid, []))})
    for v in liste:
        liste[v].sort(key=lambda s: (s["punkt"][1] // 50, s["punkt"][0], s["id"]))
    return {"rechtecke": vr, "liste": liste, "kern_ids": sorted(zuordnung)}


def tabelle(liste: list[dict]) -> str:
    kopf = ("| Nr | ID | Klasse Vorstufe | sicher | im Siedlungsgebiet | Kernfläche px | Anteil hier | auch in | "
            "Punkt x/y | Kandidaten |\n|---|---|---|---|---|---|---|---|---|---|\n")
    return kopf + "\n".join(
        f"| {s['nr']} | {s['id']} | {s['klasse']} {s['name']} | {s['sicher']} | {s['im_siedlung']} | "
        f"{s['kern_flaeche']} | {round(100 * s['anteil'])} % | {', '.join(s['auch_in']) or '–'} | "
        f"{s['punkt'][0]}/{s['punkt'][1]} | {', '.join(s['kandidaten']) or '–'} |" for s in liste)


# -- Bilder -------------------------------------------------------------------------------------

def _rahmen(bild, r, f: Fenster, farbe, dicke=2, versatz=(0, 0)) -> None:
    x, y, b, h = r
    x0, y0 = (x - f.x) * f.faktor + versatz[0], (y - f.y) * f.faktor + versatz[1]
    cv2.rectangle(bild, (x0, y0), (x0 + b * f.faktor - 1, y0 + h * f.faktor - 1), farbe, dicke, cv2.LINE_4)


def _fenster(r, rand: int, faktor: int, form) -> Fenster:
    x, y, b, h = r
    x0, y0 = max(0, x - rand), max(0, y - rand)
    return Fenster(x0, y0, min(form[1], x + b + rand) - x0, min(form[0], y + h + rand) - y0, faktor)


def nummern(a: Ansicht, f: Fenster, hell, eigene: set, nachbarn: set, modulo: int, groesse: float,
            rahmen: list, farbe, min_px: int = 0) -> np.ndarray:
    """Umriss mit Nummern (ID mod ``modulo``): eigene weiß, Nachbarn grau; außerhalb ``hell`` abgedunkelt."""
    bild = a.zeichnen("roh", f).astype(np.float32)
    teil = a.karte[f.schnitt()]
    innen = np.zeros(teil.shape, bool)
    x, y, b, h = hell
    innen[max(0, y - f.y):max(0, y + h - f.y), max(0, x - f.x):max(0, x + b - f.x)] = True
    bild[~np.repeat(np.repeat(innen, f.faktor, 0), f.faktor, 1)] *= 0.6
    bild = bild.astype(np.uint8)
    bild[grenzen(np.repeat(np.repeat(teil, f.faktor, 0), f.faktor, 1))] = a.farben["grenze"]
    if a.kern:
        k = a.kern
        _rahmen(bild, (k["x"], k["y"], k["breite"], k["hoehe"]), f, WEISS, 1)
    for r in rahmen:
        _rahmen(bild, r, f, farbe, 2)
    for sid in np.unique(teil).tolist():
        if sid not in eigene and sid not in nachbarn:
            continue
        maske = np.pad(teil == sid, 1)
        if min_px and maske.sum() * f.faktor ** 2 < min_px:
            continue
        abstand = ndimage.distance_transform_edt(maske)[1:-1, 1:-1]
        yy, xx = np.unravel_index(int(np.argmax(abstand)), abstand.shape)
        text = str(sid % modulo)
        g = groesse if sid in eigene else groesse * 0.85
        (tb, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, g, 1)
        _text(bild, text, int((xx + 0.5) * f.faktor) - tb // 2, int((yy + 0.5) * f.faktor) + th // 2,
              WEISS if sid in eigene else GRAU, g)
    return bild


def _speichern(pfad: Path, bild: np.ndarray, qualitaet: int) -> None:
    pfad.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(bild).save(pfad, quality=qualitaet)


def teilkachel_bilder(tk: str, a: Ansicht, ein: dict, ganz: Path, viertel: Path, b: dict, modulo: int) -> dict:
    """Gesamtbild der Teilkachel und je Viertel Übersicht und vier Nahansichten (Paar)."""
    form = a.karte.shape
    q = int(b["jpeg_qualitaet"])
    farbe = a.farben["gitter"]
    fg = Fenster(0, 0, form[1], form[0], int(b["ganz_faktor"]))
    k = a.kern
    bild = nummern(a, fg, (k["x"], k["y"], k["breite"], k["hoehe"]), set(ein["kern_ids"]), set(), modulo, 0.42,
                   list(ein["rechtecke"].values()), farbe, min_px=40 * fg.faktor ** 2)
    for v, (x, y, _, _) in ein["rechtecke"].items():
        _text(bild, v, x * fg.faktor + 10, y * fg.faktor + 40, farbe, 1.3)
    _speichern(ganz / "ganz_nummern.jpg", bild, q)
    _speichern(ganz / "ganz_roh.jpg", a.zeichnen("roh", fg), q)
    dateien.schreibe_json(ganz / "ganz.json", {"teilkachel": tk, "faktor": fg.faktor, "kern_im_bild": k,
                                               "viertel": {v: list(r) for v, r in ein["rechtecke"].items()}})
    alle = set(ein["kern_ids"])
    for v, r in ein["rechtecke"].items():
        ziel = viertel / v
        eigene = {s["id"] for s in ein["liste"][v]}
        fu = _fenster(r, int(b["viertel_rand"]), int(b["viertel_faktor"]), form)
        fenster = {"uebersicht_nummern.jpg": fu.als_dict()}
        _speichern(ziel / "uebersicht_nummern.jpg",
                   nummern(a, fu, r, eigene, alle - eigene, modulo, 0.5, [r], farbe), q)
        for art in ("roh", "vorschlag", "maengel", "kontrast", "gitter"):
            bild = np.ascontiguousarray(a.zeichnen(art, fu))
            if art != "roh":
                _rahmen(bild, r, fu, farbe, 2, (40, 16) if art == "gitter" else (0, 0))
            _speichern(ziel / f"uebersicht_{art}.jpg", bild, q)
            fenster[f"uebersicht_{art}.jpg"] = {**fu.als_dict(),
                                                **({"rand_links": 40, "rand_oben": 16} if art == "gitter" else {})}
        for n, rt in enumerate(viertel_rechtecke(dict(zip(("x", "y", "breite", "hoehe"), r))).values(), 1):
            fn = a.paar_fenster(_fenster(rt, int(b["nah_rand"]), int(b["nah_faktor"]), form))
            _speichern(ziel / f"nah{n}.jpg", a.zeichnen("paar", fn), q)
            fenster[f"nah{n}.jpg"] = {**fn.als_dict(), "versatz": a.paar_versatz(fn)}
        dateien.schreibe_json(ziel / "viertel.json", {
            "schema": "landseg-viertelbilder/1", "teilkachel": tk, "viertel": v, "lage": LAGE[v],
            "viertel_im_bild": dict(zip(("x", "y", "breite", "hoehe"), r)), "kern_im_bild": k,
            "koordinaten": "x_teilkachel = fenster.x + x_bild // faktor (im Gitterbild vorher 40 px links und 16 px "
                           "oben abziehen; im Paar rechts vorher versatz abziehen)",
            "nummer": f"Nummer im Bild = ID mod {modulo}; weiß = Segment dieses Viertels, grau = Kernsegment eines "
                      "Nachbarviertels, ohne Nummer = Kontextrand",
            "bilder": {name: {"fenster": fe} for name, fe in fenster.items()}, "segmente": ein["liste"][v]})
    return {"nummern": p(ganz / "ganz_nummern.jpg"), "roh": p(ganz / "ganz_roh.jpg")}


def rasterbild(daten: Path, manifest: dict, ziel: Path, farbe, q: int) -> str:
    with Image.open(daten / manifest["ausschnitt"]["bild"]) as bild:
        rgb = np.asarray(bild.convert("RGB")).copy()
    for t in manifest["teilkacheln"]:
        k = t["kern"]
        cv2.rectangle(rgb, (k["x"], k["y"]), (k["x"] + k["breite"] - 1, k["y"] + k["hoehe"] - 1), farbe, 2)
        _text(rgb, t["id"], k["x"] + 12, k["y"] + 40, farbe, 1.2)
    _speichern(ziel, rgb, q)
    return p(ziel)


# -- Aufbau -------------------------------------------------------------------------------------

class Lauf:
    """Pfade und Einstellungen eines Laufs (Daten des Ausschnitts, Ziel für Aufträge)."""

    def __init__(self, manifest: str | Path, ziel: str | Path, werte: dict, seite: dict):
        self.manifest_pfad = Path(manifest).resolve()
        self.daten = self.manifest_pfad.parent
        self.manifest = dateien.lese_json(self.manifest_pfad)
        self.name = str(self.manifest["ausschnitt"].get("name") or self.daten.name)
        self.ziel = Path(ziel).resolve()
        self.werte = werte
        self.fassungen = lauf.fassungen(self.daten, werte, seite)
        ordner = werte.get("ordner") or {}
        self.vorstufe = self.daten / str(ordner.get("vorstufe") or "vorstufe")
        self.ganz = self.daten / str(ordner.get("ganz") or "ganz")
        self.viertel = self.daten / str(ordner.get("viertel") or "viertel")
        self.auftraege = self.ziel / "auftraege"
        self.plan = self.ziel / "auftraege.json"
        self.tks = [t["id"] for t in self.manifest["teilkacheln"]]
        self.teil = {t["id"]: t for t in self.manifest["teilkacheln"]}
        self.gegenprobe = self.gegenprobe_lesen()

    def gegenprobe_lesen(self) -> dict | None:
        g = self.werte.get("gegenprobe")
        if not g:
            return None
        f = next((f for f in self.fassungen if f.kennung == str(g.get("fassung"))), None)
        fehler = []
        if f is None or f.art != "urteil":
            fehler.append(f"Gegenprobe: Fassung {g.get('fassung')!r} ist keine Fassung mit Urteil")
        if g.get("teilkachel") not in self.teil:
            fehler.append(f"Gegenprobe: Teilkachel {g.get('teilkachel')!r} steht nicht im Manifest")
        if fehler:
            raise LaufFehler(fehler)
        return {"fassung": f, "tk": g["teilkachel"], "karte": f.ordner / str(g.get("karte") or "gegenprobe"),
                "ergebnis": f.ordner / str(g.get("ergebnis") or "urteil-gegenprobe")}

    def karten(self) -> list[tuple[str, Path]]:
        """(Teilkachel, Ordner der Kartenkopie) aller Kopien der Vorstufe."""
        aus = [(tk, f.ordner / tk) for f in self.fassungen if f.art == "urteil" for tk in self.tks]
        if self.gegenprobe:
            aus.append((self.gegenprobe["tk"], self.gegenprobe["karte"] / self.gegenprobe["tk"]))
        return aus


def _arten(l: Lauf) -> None:
    fehler = [f"{f.titel}: Kennung {f.kurz!r} kennt plan nicht (erlaubt: a, b, c)"
              for f in l.fassungen if f.kurz not in PLAN_ARTEN or f.kurz == "z"]
    if l.werte.get("einheit", "viertel") != "viertel":
        fehler.append(f"einheit {l.werte.get('einheit')!r}: plan bildet Fassungen mit Urteil nur je Viertel "
                      "(einheit viertel)")
    for f in l.fassungen:
        if f.art == "frei" and f.kurz != "a":
            fehler.append(f"{f.titel}: freie Abgabe je Teilkachel heißt im Plan a")
    if fehler:
        raise LaufFehler(fehler)


def _vorstufe_pruefen(l: Lauf) -> list[str]:
    fehler = []
    for tk in l.tks:
        for name in KARTE[:2]:
            if not (l.vorstufe / tk / name).is_file():
                fehler.append(f"Vorstufe fehlt: {p(l.vorstufe / tk / name)} (erst `vorstufe` fahren)")
    return fehler


def _werte_basis(l: Lauf, py: str, hinweis: str) -> dict:
    return {"PY": py, "REPO": p(lauf.REPO), "DATEN": p(l.daten), "AUSSCHNITT": l.name,
            "HINWEIS": hinweis.strip() or "keiner"}


def _abschnitt(name: str, werte: dict) -> str:
    return lauf.fuellen(lauf.abschnitt(name), werte).strip()


def _block(name: str, werte: dict) -> str:
    """Abschnitt als eigener Block (Leerzeile davor) oder leer."""
    text = _abschnitt(name, werte)
    return f"\n{text}\n" if text else ""


def bauen(manifest: str | Path, ziel: str | Path, *, werte: dict | None = None, seite: dict | None = None,
          py: str, hinweis: str = "", name: str = "", ersetzen: bool = False) -> dict:
    """Baut die Vorbereitung und prüft sie; gibt den Plan zurück. Befund: ``LaufFehler``."""
    t0 = time.perf_counter()
    lw, sw = lauf.einstellungen_laden()
    l = Lauf(manifest, ziel, werte or lw, seite or sw)
    _arten(l)
    fehler = _vorstufe_pruefen(l)
    if fehler:
        raise LaufFehler(fehler)
    lauf.frei_machen([l.ganz, l.viertel, l.auftraege, l.plan] + [f.ordner for f in l.fassungen], ersetzen)
    kat = kategorien.laden()
    vorgaben = einstellungen.laden("ansicht")
    modulo = int(vorgaben["paar"]["nummer_modulo"])
    b = l.werte["bilder"]
    q = int(b["jpeg_qualitaet"])
    farbe = tuple(int(str(vorgaben["farben"]["gitter"]).lstrip("#")[i:i + 2], 16) for i in (0, 2, 4))
    lauf_name = name or l.name

    # 1. Kartenkopien der Vorstufe und Marken
    for tk, ordner in l.karten():
        ordner.mkdir(parents=True, exist_ok=True)
        for datei in KARTE:
            if (l.vorstufe / tk / datei).is_file():
                shutil.copyfile(l.vorstufe / tk / datei, ordner / datei)
    for f in l.fassungen:
        dateien.schreibe_json(f.ordner / lauf.MARKE, f.marke())

    # 2. Bilder und Viertel je Teilkachel (nebenläufig)
    frei = [f for f in l.fassungen if f.art == "frei"]

    def je_teilkachel(tk: str) -> dict:
        t = l.teil[tk]
        bild = bild_rgb(naht.lese_bild(l.daten / t["bild"]))
        labels = dateien.lese_labels(l.vorstufe / tk / "labels.tif")
        seg = dateien.lese_segmente(l.vorstufe / tk / "segmente.json")
        kand: dict[int, set] = {}
        if (l.vorstufe / tk / "kandidaten.json").is_file():
            for k in dateien.lese_json(l.vorstufe / tk / "kandidaten.json").get("kandidaten", []):
                for sid in k.get("ids", []):
                    kand.setdefault(sid, set()).add(k["art"])
        kern = t["kern_im_bild"]
        try:
            ein = einteilen(labels, seg, kern, kat, kand, modulo)
        except LaufFehler as fehler:
            raise LaufFehler(f"{tk}: {fehler}") from None
        a = Ansicht(bild, labels, seg, kat, vorgaben, kern=kern)
        ganz = teilkachel_bilder(tk, a, ein, l.ganz / tk, l.viertel / tk, b, modulo)
        for f in frei:
            ansicht_schreiben(bild, labels, f.unter("ansicht", "ansicht") / tk, segmente=seg, kategorien=kat,
                              kern=kern, nur_teilkachel=True, vorgaben=vorgaben)
        return {"ein": ein, "ganz": ganz}

    raster = rasterbild(l.daten, l.manifest, l.ganz / f"{l.name}_raster.jpg", farbe, q)
    with ThreadPoolExecutor(max_workers=min(8, len(l.tks))) as pool:
        erg = dict(zip(l.tks, pool.map(je_teilkachel, l.tks)))

    # 3. Aufträge aus den Vorlagen
    basis = _werte_basis(l, py, hinweis)
    plan = {"schema": SCHEMA, "erstellt": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "lauf": lauf_name,
            "manifest": p(l.manifest_pfad), "ganz_ausschnitt": p(l.daten / l.manifest["ausschnitt"]["bild"]),
            "ganz_raster": raster, "ganz_teilkachel": {tk: erg[tk]["ganz"] for tk in l.tks},
            "fassungen": [{**f.marke(), "ordner": p(f.ordner)} for f in l.fassungen],
            "einheiten": [], "viertel": [], "gegenprobe": [], "vereinheitlichen": []}
    vorlage_viertel, vorlage_frei = lauf.vorlage("urteil-viertel.md"), lauf.vorlage("frei.md")

    def viertel_auftrag(f: Fassung, art: str, tk: str, v: str, karte: Path, ergebnis: Path, gp: bool) -> None:
        ein, t = erg[tk]["ein"], l.teil[tk]
        liste = ein["liste"][v]
        x, y, bb, hh = ein["rechtecke"][v]
        w = {**basis, "TEILKACHEL": tk, "VIERTEL": v, "VIERTEL_LAGE": LAGE[v], "SEGMENTZAHL": str(len(liste)),
             "FASSUNG_NAME": (f"Gegenprobe (Zweitagent, {f.titel})" if gp else f.titel),
             "LABELS": p((karte / "labels.tif").relative_to(l.daten)),
             "SEGMENTE": p((karte / "segmente.json").relative_to(l.daten)),
             "TEILKACHEL_DATEI": t["bild"], "AUSSCHNITT_BILD": raster, "TEILKACHEL_BILD": erg[tk]["ganz"]["nummern"],
             "TEILKACHEL_ROH": erg[tk]["ganz"]["roh"],
             "VIERTEL_RECHTECK": f"x {x}–{x + bb - 1}, y {y}–{y + hh - 1} im Teilkachelbild ({bb} × {hh} Bildpunkte)",
             "KERNZAHL": str(len(ein["kern_ids"])),
             "JE_VIERTEL": ", ".join(f"{w_} {len(ein['liste'][w_])}" for w_ in VIERTEL),
             "BILDER": p(l.viertel / tk / v), "NUMMER_MODULO": str(modulo), "LISTE": tabelle(liste),
             "ERGEBNIS": p(ergebnis), "BEARBEITER": f"agent:{art}:{tk}-{v}:{lauf_name}"}
        w["KATEGORIEN"] = _abschnitt("kategorien-" + f.klassen, w)
        w["FASSUNG_ABSCHNITT"] = _block("fassung-" + f.klassen, w) + (_block("gegenprobe", w) if gp else "")
        pfad = l.auftraege / art / tk / v / "auftrag.md"
        lauf.schreibe_text(pfad, lauf.fuellen(vorlage_viertel, w))
        ergebnis.mkdir(parents=True, exist_ok=True)
        ids = [s["id"] for s in liste]
        plan["einheiten"].append({"art": art, "tk": tk, "v": int(v[1]), "n": len(ids), "auftrag": p(pfad),
                                  "ergebnis": p(ergebnis)})
        plan["gegenprobe" if gp else "viertel"].append({"art": art, "teilkachel": tk, "viertel": v,
                                                       "auftrag": p(pfad), "segmente": ids})

    for f in l.fassungen:
        if f.art == "urteil":
            for tk in l.tks:
                for v in VIERTEL:
                    viertel_auftrag(f, f.kurz, tk, v, f.ordner / tk, f.unter("ergebnis", "urteil") / tk / v, False)
        else:
            for tk in l.tks:
                ergebnis = f.unter("ergebnis", "abgabe") / tk
                w = {**basis, "TEILKACHEL": tk, "FASSUNG_NAME": f.titel, "ERGEBNIS": p(ergebnis),
                     "AUSSCHNITT_BILD": raster, "TEILKACHEL_BILD": erg[tk]["ganz"]["nummern"],
                     "TEILKACHEL_ROH": erg[tk]["ganz"]["roh"], "TEILKACHEL_DATEI": l.teil[tk]["bild"],
                     "LABELS": p((l.vorstufe / tk / "labels.tif").relative_to(l.daten)),
                     "SEGMENTE": p((l.vorstufe / tk / "segmente.json").relative_to(l.daten)),
                     "BILDER": p(f.unter("ansicht", "ansicht") / tk / "teilkachel"),
                     "ID_GRENZE": str(int(f.werte.get("id_versatz") or 100000))}
                w["GEGENPROBE"] = _block("keine-gegenprobe", w)
                pfad = l.auftraege / f.kurz / tk / "auftrag.md"
                lauf.schreibe_text(pfad, lauf.fuellen(vorlage_frei, w))
                ergebnis.mkdir(parents=True, exist_ok=True)
                plan["einheiten"].append({"art": f.kurz, "tk": tk, "v": 0, "n": 0, "auftrag": p(pfad),
                                          "ergebnis": p(ergebnis)})
    if l.gegenprobe:
        g = l.gegenprobe
        for v in VIERTEL:
            viertel_auftrag(g["fassung"], "z", g["tk"], v, g["karte"] / g["tk"], g["ergebnis"] / g["tk"] / v, True)

    # 4. Vereinheitlichen (Fassungen mit freien Klassen)
    for f in l.fassungen:
        if f.klassen != "frei":
            continue
        ergebnis = f.unter("vereinheitlichung", "vereinheitlichung")
        if f.art == "urteil":
            zeilen = [e for e in plan["einheiten"] if e["art"] == f.kurz]
            abgaben = ("| Teilkachel | Viertel | Segmente | Abgabe |\n|---|---|---|---|\n" + "\n".join(
                f"| `{e['tk']}` | `v{e['v']}` | {e['n']} | `{e['ergebnis']}/urteil.json` |" for e in zeilen))
            vorlage = "vereinheitlichen-urteil.md"
        else:
            abgaben = ("| Teilkachel | Abgabe |\n|---|---|\n" + "\n".join(
                f"| `{tk}` | `{p(f.unter('ergebnis', 'abgabe') / tk)}/` (`segmente.json`, `kategorien-teil.json`) |"
                for tk in l.tks))
            vorlage = "vereinheitlichen-frei.md"
        w = {**basis, "FASSUNG_NAME": f.titel, "ABGABEN": abgaben, "BILDER": p(l.viertel), "ERGEBNIS": p(ergebnis)}
        pfad = l.auftraege / f.kurz / "vereinheitlichen.md"
        lauf.schreibe_text(pfad, lauf.fuellen(lauf.vorlage(vorlage), w))
        ergebnis.mkdir(parents=True, exist_ok=True)
        plan["vereinheitlichen"].append({"fassung": f.kennung, "auftrag": p(pfad), "ergebnis": p(ergebnis)})

    plan["kernsegmente"] = {tk: len(erg[tk]["ein"]["kern_ids"]) for tk in l.tks}
    plan["sekunden"] = round(time.perf_counter() - t0, 1)
    dateien.schreibe_json(l.plan, plan)
    fehler = pruefen(manifest, ziel, werte=l.werte, seite=seite or sw)
    if fehler:
        raise LaufFehler(fehler)
    return plan


# -- Selbstprüfung ------------------------------------------------------------------------------

def pruefen(manifest: str | Path, ziel: str | Path, *, werte: dict | None = None, seite: dict | None = None) -> list[str]:
    """Befunde einer fertigen Vorbereitung (leer = ok); schreibt nichts."""
    lw, sw = lauf.einstellungen_laden()
    l = Lauf(manifest, ziel, werte or lw, seite or sw)
    if not l.plan.is_file():
        return [f"Plan fehlt: {p(l.plan)}"]
    plan = dateien.lese_json(l.plan)
    fehler: list[str] = []
    # Kartenkopien bildpunktgleich zur Vorstufe
    for tk, ordner in l.karten():
        for datei in KARTE[:2]:
            if not (ordner / datei).is_file():
                fehler.append(f"Kartenkopie fehlt: {p(ordner / datei)}")
        if fehler:
            continue
        a, b = dateien.lese_labels(ordner / "labels.tif"), dateien.lese_labels(l.vorstufe / tk / "labels.tif")
        if a.shape != b.shape or not np.array_equal(a, b):
            fehler.append(f"Kartenkopie {p(ordner / 'labels.tif')} ist nicht bildpunktgleich zur Vorstufe "
                          f"({int((a != b).sum()) if a.shape == b.shape else 'Form'} Bildpunkte)")
        if dateien.lese_json(ordner / "segmente.json") != dateien.lese_json(l.vorstufe / tk / "segmente.json"):
            fehler.append(f"Kartenkopie {p(ordner / 'segmente.json')} weicht von der Vorstufe ab")
    # jedes Kernsegment in genau einem Viertel-Auftrag je Art
    for art, karte_von in [(f.kurz, lambda tk, f=f: f.ordner / tk) for f in l.fassungen if f.art == "urteil"] + (
            [("z", lambda tk: l.gegenprobe["karte"] / tk)] if l.gegenprobe else []):
        tks = [l.gegenprobe["tk"]] if art == "z" else l.tks
        for tk in tks:
            t = l.teil[tk]
            labels = karte_von(tk) / "labels.tif"
            if not labels.is_file():
                continue
            k = t["kern_im_bild"]
            kern_ids = set(np.unique(dateien.lese_labels(labels)[k["y"]:k["y"] + k["hoehe"],
                                                              k["x"]:k["x"] + k["breite"]]).tolist()) - {0}
            zaehler: dict[int, int] = {}
            for e in plan.get("gegenprobe" if art == "z" else "viertel") or []:
                if e.get("art") == art and e.get("teilkachel") == tk:
                    for sid in e.get("segmente") or []:
                        zaehler[sid] = zaehler.get(sid, 0) + 1
            ohne = sorted(kern_ids - set(zaehler))
            doppelt = sorted(s for s, n in zaehler.items() if n > 1)
            fremd = sorted(set(zaehler) - kern_ids)
            for text, ids in (("in keinem Viertel-Auftrag", ohne), ("in mehreren Viertel-Aufträgen", doppelt),
                              ("in einem Auftrag, aber nicht im Kern", fremd)):
                if ids:
                    fehler.append(f"Art {art}, {tk}: Kernsegmente {text}: {ids[:10]}")
    # Aufträge ohne Platzhalter
    auftraege = [e["auftrag"] for e in plan.get("einheiten") or []] + [
        e["auftrag"] for e in plan.get("vereinheitlichen") or []]
    for a in auftraege:
        pfad = Path(a)
        if not pfad.is_file():
            fehler.append(f"Auftrag fehlt: {a}")
            continue
        rest = sorted(set(lauf.PLATZHALTER.findall(pfad.read_text(encoding="utf-8"))))
        if rest:
            fehler.append(f"Platzhalter übrig in {a}: {', '.join('{{' + r + '}}' for r in rest)}")
        if not Path(next(e["ergebnis"] for e in (plan.get("einheiten") or []) + (plan.get("vereinheitlichen") or [])
                         if e["auftrag"] == a)).is_dir():
            fehler.append(f"Ergebnisordner zu {a} fehlt")
    # Bilder
    bilder = [plan.get("ganz_raster"), plan.get("ganz_ausschnitt")]
    for g in (plan.get("ganz_teilkachel") or {}).values():
        bilder += [g.get("nummern"), g.get("roh")]
    for tk in l.tks:
        for v in VIERTEL:
            vj = l.viertel / tk / v / "viertel.json"
            if not vj.is_file():
                fehler.append(f"Viertelbilder fehlen: {p(vj)}")
                continue
            bilder += [p(vj.parent / name) for name in dateien.lese_json(vj).get("bilder") or {}]
    for f in l.fassungen:
        if f.art == "frei":
            bilder += [p(f.unter("ansicht", "ansicht") / tk / "ansicht.json") for tk in l.tks]
    for bild in bilder:
        if not bild or not Path(bild).is_file():
            fehler.append(f"Bild fehlt: {bild}")
    return fehler
