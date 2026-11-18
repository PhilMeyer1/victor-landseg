"""plan: Urteils-Agents eines Laufs aus den Aufträgen bilden (Gruppierung und Prompt je Agent).

Eingabe ist die Auftragsliste der Vorbereitung (``auftraege.json``)::

    {"manifest": "<manifest.json>", "ganz_ausschnitt": "<Bild>", "ganz_raster": "<Bild mit Gitter>",
     "ganz_teilkachel": {"r0c0": {"nummern": "<Bild>", "roh": "<Bild>"}, ...},
     "einheiten": [{"art": "c", "tk": "r0c0", "v": 1, "n": 58, "auftrag": "<auftrag.md>", "ergebnis": "<Ordner>"}, ...],
     "viertel": [{"auftrag": "<auftrag.md>", "segmente": [ids]}, ...], "gegenprobe": [...]}

``art``: ``a`` Fassung A „Alles frei“ (ohne Viertel, ``v`` 0), ``b`` Fassung B, ``c`` Fassung C, ``z`` Gegenprobe
(Zweitagent auf C). Gruppierung nach der Entscheidung des Nutzers vom 18.11.2026: B, C und Gegenprobe bekommen
**einen Agent je Viertel** (Schlüssel ``art:tk-vN``, vier je Teilkachel), Fassung A bleibt ein Agent je Teilkachel.
Jeder Agent sieht zuerst den ganzen Ausschnitt, dann seine ganze Teilkachel, dann nur seinen Auftrag. Die Segmente
eines Auftrags (``segmente`` aus ``viertel``/``gegenprobe``, Zuordnung über den Pfad des Auftrags) dürfen in keinem
zweiten Auftrag derselben Art und Teilkachel stehen.

Der Plan (``landseg-urteil-plan/1``) nennt je Agent Label, Art, Teilkachel, Viertel, Segmentzahl, seinen einen
Auftrag (``teile``, Form der Einheiten) und den fertigen Prompt aus ``vorlagen/agent-urteil-viertel.md`` bzw.
``vorlagen/agent-urteil-teilkachel.md``. Die Quittung je Agent bleibt die des Laufs (``teile`` mit einem Eintrag);
Nachholen, Vereinheitlichen, Nähte und Einigung arbeiten weiter mit dem Ergebnis je Viertel.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from . import dateien

SCHEMA = "landseg-urteil-plan/1"
VORLAGEN = Path(__file__).resolve().parent.parent / "vorlagen"
ARTEN = {
    "a": "Fassung A „Alles frei“",
    "b": "Fassung B „Kategorien frei“",
    "c": "Fassung C „Feste Kategorienliste“",
    "z": "Gegenprobe (Zweitagent, Fassung C „Feste Kategorienliste“)",
}
LAGE = {1: "oben links", 2: "oben rechts", 3: "unten links", 4: "unten rechts"}
TEILKACHEL_ID = re.compile(r"^r\d+c\d+$")
PLATZHALTER = re.compile(r"\{\{([A-Z_]+)\}\}")


class PlanFehler(ValueError):
    """Aufträge passen nicht zur Gruppierung (doppelt, fehlende Felder, Segment in zwei Aufträgen)."""


@dataclass(frozen=True)
class Einheit:
    art: str
    tk: str
    v: int
    n: int
    auftrag: str
    ergebnis: str
    segmente: tuple[int, ...] | None = None

    @property
    def label(self) -> str:
        return f"{self.art}:{self.tk}" + (f"-v{self.v}" if self.v else "")

    def als_dict(self) -> dict:
        return {"art": self.art, "tk": self.tk, "v": self.v, "n": self.n, "auftrag": self.auftrag,
                "ergebnis": self.ergebnis}


def _pfad(text) -> str:
    return str(text or "").replace("\\", "/")


def einheiten_lesen(daten: dict) -> list[Einheit]:
    """Einheiten aus ``auftraege.json`` prüfen und mit ihren Segmentlisten verbinden."""
    roh = daten.get("einheiten")
    if not isinstance(roh, list) or not roh:
        raise PlanFehler("Feld 'einheiten' fehlt oder ist leer")
    segmente: dict[str, tuple[int, ...]] = {}
    for liste in ("viertel", "gegenprobe"):
        for eintrag in daten.get(liste) or []:
            if isinstance(eintrag, dict) and isinstance(eintrag.get("segmente"), list):
                segmente[_pfad(eintrag.get("auftrag"))] = tuple(int(s) for s in eintrag["segmente"])
    einheiten = []
    for i, e in enumerate(roh):
        wo = f"einheiten[{i}]"
        if not isinstance(e, dict):
            raise PlanFehler(f"{wo}: kein Objekt")
        art, tk = str(e.get("art")), str(e.get("tk"))
        if art not in ARTEN:
            raise PlanFehler(f"{wo}: art {art!r} unbekannt (erlaubt: {', '.join(ARTEN)})")
        if not TEILKACHEL_ID.match(tk):
            raise PlanFehler(f"{wo}: tk {tk!r} ist keine Teilkachel-ID wie r0c0")
        v, n = e.get("v"), e.get("n", 0)
        if not isinstance(v, int) or isinstance(v, bool) or not 0 <= v <= 4:
            raise PlanFehler(f"{wo}: v {v!r} ist keine Viertelnummer 0–4")
        if (art == "a") != (v == 0):
            raise PlanFehler(f"{wo}: Fassung A hat v 0 (ein Agent je Teilkachel), B, C und Gegenprobe v 1–4")
        if not isinstance(n, int) or isinstance(n, bool) or n < 0:
            raise PlanFehler(f"{wo}: n {n!r} ist keine Segmentzahl")
        auftrag, ergebnis = _pfad(e.get("auftrag")), _pfad(e.get("ergebnis"))
        if not auftrag or not ergebnis:
            raise PlanFehler(f"{wo}: auftrag oder ergebnis fehlt")
        liste = segmente.get(auftrag)
        if liste is not None and n and n != len(liste):
            raise PlanFehler(f"{wo}: n {n}, aber {len(liste)} Segmente in der Liste des Auftrags")
        einheiten.append(Einheit(art, tk, v, n or (len(liste) if liste else 0), auftrag, ergebnis, liste))
    return einheiten


def gruppieren(einheiten: list[Einheit]) -> list[dict]:
    """Ein Agent je Viertel (B, C, Gegenprobe), je Teilkachel (A); jeder mit genau einem Auftrag.

    Doppelte Aufträge und Segmente, die in zwei Aufträgen derselben Art und Teilkachel stehen, sind Fehler.
    Reihenfolge: meiste Segmente zuerst (die längsten Agents starten früh), dann nach Label.
    """
    gruppen: dict[str, dict] = {}
    besitzer: dict[tuple[str, str, int], str] = {}
    for e in einheiten:
        if e.label in gruppen:
            raise PlanFehler(f"Auftrag {e.label} doppelt")
        for sid in e.segmente or ():
            frueher = besitzer.setdefault((e.art, e.tk, sid), e.label)
            if frueher != e.label:
                raise PlanFehler(f"Segment {sid} steht in {frueher} und in {e.label}")
        gruppen[e.label] = {"label": e.label, "art": e.art, "tk": e.tk, "v": e.v, "n": e.n,
                            "teile": [e.als_dict()]}
    return sorted(gruppen.values(), key=lambda g: (-g["n"], g["label"]))


def vorlage_fuellen(text: str, werte: dict[str, str]) -> str:
    """Setzt ``{{NAME}}`` ein; ein Platzhalter ohne Wert ist ein Fehler (es darf keiner übrig bleiben)."""
    fehlt = sorted(set(PLATZHALTER.findall(text)) - set(werte))
    if fehlt:
        raise PlanFehler("Platzhalter ohne Wert: " + ", ".join(fehlt))
    return PLATZHALTER.sub(lambda m: str(werte[m.group(1)]), text)


def _uebersicht(daten: dict, tk: str) -> tuple[str, str]:
    ausschnitt = _pfad(daten.get("ganz_raster") or daten.get("ganz_ausschnitt"))
    teil = (daten.get("ganz_teilkachel") or {}).get(tk) or {}
    teilkachel = _pfad(teil.get("nummern") or teil.get("roh"))
    if not ausschnitt or not teilkachel:
        raise PlanFehler(f"Übersichtsbilder fehlen (ganz_raster/ganz_ausschnitt, ganz_teilkachel.{tk}.nummern)")
    return ausschnitt, teilkachel


def prompt(gruppe: dict, daten: dict, repo: str, py: str, hinweis: str = "") -> str:
    """Prompt eines Urteils-Agents aus der Vorlage seiner Art (Viertel oder ganze Teilkachel)."""
    ausschnitt_bild, teilkachel_bild = _uebersicht(daten, gruppe["tk"])
    e = gruppe["teile"][0]
    werte = {
        "FASSUNG_NAME": ARTEN[gruppe["art"]],
        "AUSSCHNITT": Path(_pfad(daten.get("ganz_ausschnitt") or ausschnitt_bild)).stem,
        "AUSSCHNITT_BILD": ausschnitt_bild,
        "TEILKACHEL": gruppe["tk"],
        "TEILKACHEL_BILD": teilkachel_bild,
        "AUFTRAG": e["auftrag"],
        "ERGEBNIS": e["ergebnis"],
        "REPO": _pfad(repo),
        "PY": _pfad(py),
        "HINWEIS": hinweis.strip() or "keiner",
        "V": str(gruppe["v"]),
    }
    if gruppe["v"]:
        werte.update({"VIERTEL": f"v{gruppe['v']}", "VIERTEL_LAGE": LAGE[gruppe["v"]],
                      "SEGMENTZAHL": str(gruppe["n"])})
        name = "agent-urteil-viertel.md"
    else:
        name = "agent-urteil-teilkachel.md"
    return vorlage_fuellen((VORLAGEN / name).read_text(encoding="utf-8"), werte).strip() + "\n"


def plan(auftraege: str | Path, repo: str | Path, py: str, hinweis: str = "",
         teilkacheln: list[str] | None = None, viertel: list[int] | None = None) -> dict:
    """Plan aus ``auftraege.json``; ``teilkacheln``/``viertel`` grenzen ihn ein (Trockenlauf auf wenig Daten).

    Die Teilkacheln der Aufträge müssen im Manifest (Feld ``manifest``) stehen. Fassung A fällt bei einer
    Eingrenzung auf Viertel weg (sie hat keine).
    """
    daten = dateien.lese_json(auftraege)
    einheiten = einheiten_lesen(daten)
    if daten.get("manifest"):
        bekannt = {t["id"] for t in dateien.lese_json(daten["manifest"]).get("teilkacheln", [])}
        fremd = sorted({e.tk for e in einheiten} - bekannt)
        if fremd:
            raise PlanFehler("Teilkachel nicht im Manifest: " + ", ".join(fremd))
    if teilkacheln:
        einheiten = [e for e in einheiten if e.tk in teilkacheln]
    if viertel:
        einheiten = [e for e in einheiten if e.v in viertel]
    if not einheiten:
        raise PlanFehler("nach der Eingrenzung bleibt kein Auftrag")
    gruppen = gruppieren(einheiten)
    for g in gruppen:
        g["prompt"] = prompt(g, daten, str(repo), py, hinweis)
    je_art = {art: sum(1 for g in gruppen if g["art"] == art) for art in ARTEN}
    return {"schema": SCHEMA, "quelle": _pfad(auftraege), "manifest": _pfad(daten.get("manifest")),
            "agents": len(gruppen), "auftraege": len(einheiten), "segmente": sum(g["n"] for g in gruppen),
            "je_art": je_art, "gruppen": gruppen}


def log_zeilen(p: dict) -> list[str]:
    """Zeilen für Konsole und Lauf-Log: Zahl der Agents, dann je Agent sein Auftrag."""
    namen = {"a": "A", "b": "B", "c": "C", "z": "Gegenprobe"}
    zeilen = [f"{p['auftraege']} Aufträge in {p['agents']} Urteils-Agents ("
              + ", ".join(f"{namen[k]} {n}" for k, n in p["je_art"].items() if n)
              + f"; {p['segmente']} Segmente; ein Agent je Viertel, Fassung A je Teilkachel)"]
    for g in p["gruppen"]:
        e = g["teile"][0]
        zeilen.append(f"  {g['label']}: 1 Auftrag, {g['n']} Segmente: {e['auftrag']} -> {e['ergebnis']}")
    return zeilen
