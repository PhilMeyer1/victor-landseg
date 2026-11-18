"""Prüft ein urteil.json (Viertel oder Teilkachel) gegen segmente.json der Vorstufe.

Aufruf (Python des Stitcher-venv oder jedes Python 3, nur Standardbibliothek):
  PY -I pruefe_urteil.py --urteil <urteil.json> --segmente <segmente.json> --fassung c|b (c = feste Liste, b = Kategorien frei; H0-Namen)
                         [--viertel v1 --ids 1,2,3] [--kategorien <kategorien.json>]

Ohne --ids müssen genau die Segmente des Kerns (im_kern) vorkommen, mit --ids genau diese.
Geprüft: jedes Segment genau einmal, kein Segment des Kontextrands, je Eintrag mindestens ein Bild,
jede genannte Bilddatei existiert (absolut oder relativ zum Ordner von urteil.json), Feld `sicher`
ist true/false; Fassung a: klasse_vorschlag ist null oder ein Code der Kategorienliste; Fassung b:
klasse_frei hat grob, mittel, fein als nicht leere Texte; Listen nicht_geprueft und offen vorhanden.
Mit --viertel: Feld `viertel` gleich dem Wert, `bilder_angesehen` mit nicht leerer Liste `uebersicht`
(darunter eine Datei `uebersicht_nummern.jpg`) und Liste `nah`, alle Dateien vorhanden.
Ohne --viertel, aber mit Liste `viertel` (zusammengeführtes Urteil): je Eintrag dasselbe für dessen
`bilder_angesehen`, und jedes Segment trägt ein Feld `viertel`.
Teil 3 (grobe Vorstufe, Nachsegmentieren): --segmente ist die bearbeitete Kartenkopie. Liste `eingriffe`
(je Eintrag `vorher`, `nachher` als ID-Listen, `grund` als Text) ist Pflicht, wenn --viertel gesetzt ist oder
neben urteil.json eine eingriffe.json liegt (dann nicht leer). Verlangt sind die IDs aus --ids, die noch auf
der Karte stehen, plus jede neue ID (in `nachher`, nicht in `vorher`) im Kern; eine ID aus --ids, die nicht
mehr auf der Karte steht, muss unter `vorher` stehen. IDs aus `nachher` dürfen geurteilt werden.
Ausgabe: Befund, letzte Zeile `ok` oder `FEHLER`; Exit 0 / 1, Aufruf- oder Lesefehler 2.
"""
import argparse
import json
import sys
from pathlib import Path


def bilder_pruefen(ba, wo: str, basis: Path, maengel: list) -> int:
    if not isinstance(ba, dict):
        maengel.append(f"{wo}: `bilder_angesehen` fehlt oder ist kein Objekt")
        return 0
    uebersicht, nah = ba.get("uebersicht"), ba.get("nah")
    if not isinstance(uebersicht, list) or not uebersicht:
        maengel.append(f"{wo}: `bilder_angesehen.uebersicht` fehlt oder ist leer")
        uebersicht = []
    elif not any(Path(str(b)).name == "uebersicht_nummern.jpg" for b in uebersicht):
        maengel.append(f"{wo}: Übersicht mit Grenzen und Nummern (uebersicht_nummern.jpg) nicht angesehen")
    if not isinstance(nah, list):
        maengel.append(f"{wo}: Liste `bilder_angesehen.nah` fehlt")
        nah = []
    for b in list(uebersicht) + list(nah):
        bp = Path(str(b))
        if not bp.is_absolute():
            bp = basis / bp
        if not bp.is_file():
            maengel.append(f"{wo}: angesehenes Bild fehlt: {b}")
    return len(uebersicht) + len(nah)


def main(argv):
    sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser()
    p.add_argument("--urteil", required=True)
    p.add_argument("--segmente", required=True)
    p.add_argument("--fassung", choices=["c", "b"], required=True)
    p.add_argument("--viertel")
    p.add_argument("--ids")
    p.add_argument("--kategorien")
    a = p.parse_args(argv)
    try:
        urteil_pfad = Path(a.urteil)
        urteil = json.loads(urteil_pfad.read_text(encoding="utf-8"))
        seg = json.loads(Path(a.segmente).read_text(encoding="utf-8"))
        codes = None
        if a.fassung == "c":
            kat_pfad = Path(a.kategorien) if a.kategorien else None
            if kat_pfad is not None:
                codes = {k["code"] for k in json.loads(kat_pfad.read_text(encoding="utf-8"))["classes"]}
    except (OSError, ValueError, KeyError) as e:
        print(f"Lesefehler: {e}")
        return 2

    kern = {s["id"] for s in seg["segmente"] if s.get("im_kern")}
    rand = {s["id"] for s in seg["segmente"] if not s.get("im_kern")}
    soll = {int(x) for x in a.ids.split(",")} if a.ids else kern
    maengel = []
    vorhanden = kern | rand
    eingriffe = urteil.get("eingriffe")
    stapel = Path(a.urteil).parent / "eingriffe.json"
    vorher_alle, nachher_alle, neu_alle = set(), set(), set()
    if eingriffe is None:
        if a.viertel is not None or stapel.is_file():
            maengel.append("Liste `eingriffe` fehlt (ohne Eingriff: leere Liste)")
        eingriffe = []
    if not isinstance(eingriffe, list):
        maengel.append("`eingriffe` ist keine Liste")
        eingriffe = []
    for i, g in enumerate(eingriffe, 1):
        vorher = g.get("vorher") if isinstance(g, dict) else None
        nachher = g.get("nachher") if isinstance(g, dict) else None
        if not (isinstance(vorher, list) and vorher and all(isinstance(x, int) for x in vorher)):
            maengel.append(f"Eingriff {i}: `vorher` keine nicht leere ID-Liste")
            vorher = []
        if not (isinstance(nachher, list) and all(isinstance(x, int) for x in nachher)):
            maengel.append(f"Eingriff {i}: `nachher` keine ID-Liste")
            nachher = []
        if not (isinstance(g, dict) and isinstance(g.get("grund"), str) and g["grund"].strip()):
            maengel.append(f"Eingriff {i}: `grund` fehlt")
        vorher_alle |= set(vorher)
        nachher_alle |= set(nachher)
        neu_alle |= set(nachher) - set(vorher)
    try:
        schritte = json.loads(stapel.read_text(encoding="utf-8")).get("schritte") if stapel.is_file() else None
    except (OSError, ValueError, AttributeError):
        schritte = None
        maengel.append("eingriffe.json nicht lesbar")
    if schritte and not eingriffe:
        maengel.append(f"eingriffe.json hat {len(schritte)} Schritte, `eingriffe` im Urteil ist leer")
    weg = sorted(i for i in soll if i not in vorhanden)
    ohne_eingriff = [i for i in weg if i not in vorher_alle]
    if ohne_eingriff:
        maengel.append(f"nicht mehr auf der Karte, aber in keinem Eingriff unter `vorher`: {ohne_eingriff}")
    soll = (soll & vorhanden) | (neu_alle & kern)
    erlaubt = soll | (nachher_alle & vorhanden)
    eintraege = urteil.get("segmente")
    if not isinstance(eintraege, list):
        print("FEHLER: `segmente` fehlt oder ist keine Liste")
        return 1
    basis = urteil_pfad.parent
    angesehen = 0
    zusammengefuehrt = a.viertel is None and isinstance(urteil.get("viertel"), list)
    if a.viertel is not None:
        if urteil.get("viertel") != a.viertel:
            maengel.append(f"`viertel` ist {urteil.get('viertel')!r}, verlangt {a.viertel!r}")
        angesehen = bilder_pruefen(urteil.get("bilder_angesehen"), a.viertel, basis, maengel)
    elif zusammengefuehrt:
        for v in urteil["viertel"]:
            wo = str(v.get("viertel")) if isinstance(v, dict) else "?"
            angesehen += bilder_pruefen(v.get("bilder_angesehen") if isinstance(v, dict) else None,
                                        wo, basis, maengel)
    gesehen = {}
    bilder_zahl = 0
    for e in eintraege:
        sid = e.get("id")
        gesehen[sid] = gesehen.get(sid, 0) + 1
        bilder = e.get("bilder") or []
        if not bilder:
            maengel.append(f"{sid}: keine Bilder")
        for b in bilder:
            bp = Path(b)
            if not bp.is_absolute():
                bp = basis / bp
            if not bp.is_file():
                maengel.append(f"{sid}: Bild fehlt: {b}")
            bilder_zahl += 1
        if not isinstance(e.get("sicher"), bool):
            maengel.append(f"{sid}: `sicher` ist nicht true/false")
        if zusammengefuehrt and not e.get("viertel"):
            maengel.append(f"{sid}: Feld `viertel` fehlt")
        if a.fassung == "c":
            kv = e.get("klasse_vorschlag")
            if kv is not None and codes is not None and kv not in codes:
                maengel.append(f"{sid}: klasse_vorschlag {kv!r} nicht in der Kategorienliste")
        else:
            kf = e.get("klasse_frei")
            if not isinstance(kf, dict) or not all(isinstance(kf.get(k), str) and kf.get(k).strip()
                                                   for k in ("grob", "mittel", "fein")):
                maengel.append(f"{sid}: klasse_frei ohne grob/mittel/fein")
    doppelt = sorted(i for i, n in gesehen.items() if n > 1)
    fehlt = sorted(soll - set(gesehen))
    fremd_rand = sorted(i for i in gesehen if i in rand and i not in erlaubt)
    fremd = sorted(i for i in gesehen if i not in erlaubt and i not in rand)
    for name in ("nicht_geprueft", "offen"):
        if not isinstance(urteil.get(name), list):
            maengel.append(f"Liste `{name}` fehlt")
    if doppelt:
        maengel.append(f"doppelt: {doppelt}")
    if fehlt:
        maengel.append(f"fehlt ({len(fehlt)}): {fehlt}")
    if fremd_rand:
        maengel.append(f"Kontextrand geurteilt: {fremd_rand}")
    if fremd:
        maengel.append(f"nicht verlangt: {fremd}")
    print(f"Einträge: {len(eintraege)}, verlangt: {len(soll)}, Bilder je Segment genannt: {bilder_zahl}, "
          f"angesehen (Viertel): {angesehen}, "
          f"nicht sauber: {sum(1 for e in eintraege if e.get('urteil') == 'nicht_sauber')}, "
          f"sicher false: {sum(1 for e in eintraege if e.get('sicher') is False)}, "
          f"Eingriffe: {len(eingriffe)}, neue IDs im Kern: {len(neu_alle & kern)}")
    for m in maengel[:60]:
        print("- " + m)
    if len(maengel) > 60:
        print(f"- … {len(maengel) - 60} weitere")
    print("ok" if not maengel else "FEHLER")
    return 0 if not maengel else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
