"""Einigung für Paare nachziehen (Kopie aus landseg-historisch-4; Paare ohne Zerfall-Bezug bleiben offen), die durch das Beheben zerfallener Segmente neu entstanden sind.

Ein Kernteil, der eine neue ID bekam (``zerfall_teil_von``) oder an einen Nachbarn gleicher Klasse
ging (Protokoll zerfall.json), bildet an der Naht ein neues Paar. Gab es für das alte Paar
(Ursprungssegment, Gegenüber) einen Beschluss, wird er für das neue Paar übernommen (gleiche
Entscheidung, Grund mit Hinweis); sonst wird das Paar als ``unklar`` belegt.

Aufruf: python -B einigung_nachziehen.py <manifest.json> <zerfall.json> [--probe]
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, "C:/Users/Phil/Developement/Victor/landseg")
from landseg import dateien, einstellungen, kategorien, naht  # noqa: E402
from landseg import einigung as E  # noqa: E402

BEARBEITER = "umsetzer:landseg-garten-4"


def main():
    manifest_pfad, protokoll_pfad = Path(sys.argv[1]), Path(sys.argv[2])
    probe = "--probe" in sys.argv
    protokoll = json.loads(protokoll_pfad.read_text(encoding="utf-8"))
    einst = einstellungen.laden("einigung", None)
    manifest = dateien.lese_json(manifest_pfad)
    bild = naht.lese_bild(manifest_pfad.parent / manifest["ausschnitt"]["bild"])
    liste = einstellungen.laden("seite")["fassungen"]
    kat = kategorien.laden(None)
    ordner_zu_kennung = {e["ordner"]: str(e["kennung"]) for e in liste}
    jetzt = datetime.now(timezone.utc).isoformat(timespec="seconds")
    for ordner, eintraege in protokoll.items():
        f = E.fassung_aus_einstellungen(manifest_pfad, ordner_zu_kennung[ordner], kat, liste)
        # Ursprung je Segment: neue IDs und Nachbarn, die einen Kernteil bekamen
        ursprung: dict[str, set[str]] = {}
        for p in eintraege:
            nach = str(p.get("nach", ""))
            ziel = None
            if nach.startswith("neue ID "):
                ziel = nach.split()[2]
            elif nach.startswith("an Nachbar "):
                ziel = nach.split()[2]
            if ziel:
                ursprung.setdefault(f"{p['teilkachel']}:{ziel}", set()).add(f"{p['teilkachel']}:{p['segment']}")
        offene = [s for s in E.stellen(f, bild, einst) if s["status"] == "offen"]
        geaendert = set()
        for s in offene:
            a, b = s["segmente"]
            neu, gegen = (a, b) if a in ursprung else (b, a) if b in ursprung else (None, None)
            beschluss, alt = None, None
            if neu:
                for u in sorted(ursprung[neu]):
                    alt = E.paar_name(u, gegen)
                    beschluss = (E._beschluss(E._eintrag(f, u), alt)
                                 or E._beschluss(E._eintrag(f, gegen), alt))
                    if beschluss:
                        break
            if beschluss:
                eintrag = {**beschluss, "paar": s["paar"], "mit": gegen,
                           "grund": f"{beschluss.get('grund', '')} [übernommen aus Paar {alt}: Kernteil "
                                    f"nach Zerfall eigene Fläche bzw. an gleichklassigen Nachbarn]",
                           "bearbeiter": BEARBEITER, "zeit": jetzt}
            elif not neu:
                print(f"{ordner}: {s['paar']} {s['klassen']} -> bleibt offen (kein Kernteil eines zerfallenen Segments)")
                continue
            else:
                eintrag = {"paar": s["paar"], "mit": gegen, "entscheidung": "unklar",
                           "grund": "Kernteil eines zerfallenen Segments, ohne Beschluss für das alte Paar; "
                                    "nicht neu beurteilt (landseg-garten-4)",
                           "bearbeiter": BEARBEITER, "zeit": jetzt}
            ziel_eintrag = E._eintrag(f, neu)
            ziel_eintrag["einigung"] = list(ziel_eintrag.get("einigung") or []) + [eintrag]
            geaendert.add(neu.split(":")[0])
            print(f"{ordner}: {s['paar']} {s['klassen']} -> {eintrag['entscheidung']}"
                  f" ({'aus ' + alt if beschluss else 'ohne alten Beschluss'})")
        if not probe:
            for tk in sorted(geaendert):
                dateien.schreibe_json(f.ordner / tk / "segmente.json", f.segmente[tk])


if __name__ == "__main__":
    main()
