"""Befehlszeile: ``python -m landseg <befehl> ...`` (im Repo-Ordner).

Befehle: ``kacheln`` (W1), ``eingriff`` (W5), ``pruefen`` (W6), ``zusammentragen`` (W7), ``naht``
(Nahtregel allein). Exit-Code 0 = ok, 1 = Befund, Nahtverstoß oder Eingriff abgelehnt, 2 = Aufruf-
oder Lesefehler.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image

from . import dateien, kategorien, naht
from .eingriff import Bearbeitung, EingriffFehler
from .kacheln import KachelFehler, kacheln
from .pruefen import pruefen
from .zusammentragen import ZusammenFehler, lese_auftrag, zusammentragen


def _punkte(text: str) -> list[list[int]]:
    """``"x,y;x,y;..."`` -> [[x, y], ...]"""
    try:
        return [[int(v) for v in paar.split(",")] for paar in text.split(";") if paar.strip()]
    except ValueError:
        raise argparse.ArgumentTypeError(f"Punkte als 'x,y;x,y;...' erwartet: {text!r}") from None


def _ids(text: str) -> list[int]:
    return [int(v) for v in text.split(",") if v.strip()]


def _form(text: str) -> tuple[int, int]:
    h, w = text.lower().replace("×", "x").split("x")
    return int(h), int(w)


def _befund_ausgeben(befund, als_json: bool) -> int:
    print(json.dumps(befund.als_dict(), ensure_ascii=False) if als_json else befund.als_text())
    return 0 if befund.ok else 1


def befehl_kacheln(a) -> int:
    manifest = kacheln(a.bild, a.x, a.y, a.breite, a.hoehe, a.ziel, kern=a.kern, rand=a.rand,
                       name=a.name, ueberschreiben=a.ueberschreiben)
    r = manifest["raster"]
    print(f"{len(manifest['teilkacheln'])} Teilkacheln ({r['zeilen']} × {r['spalten']}, "
          f"Kern {r['kern']}, Rand {r['rand']}) -> {Path(a.ziel) / 'manifest.json'}")
    return 0


def befehl_pruefen(a) -> int:
    karte = dateien.lese_labels(a.labels)
    segmente = dateien.lese_segmente(a.segmente) if a.segmente else None
    kat = kategorien.laden(a.kategorien) if segmente is not None else None
    form = a.form
    if a.bild:
        with Image.open(a.bild) as bild:
            form = (bild.height, bild.width)
    befund = pruefen(karte, segmente, kat, form=form, mindestflaeche=a.mindestflaeche)
    return _befund_ausgeben(befund, a.json)


def befehl_eingriff(a) -> int:
    karte = dateien.lese_labels(a.labels)
    segmente = dateien.lese_segmente(a.segmente)
    kat = kategorien.laden(a.kategorien)
    try:
        arbeit = Bearbeitung(karte, segmente, kat, a.bearbeiter)
        if a.op == "verschmelzen":
            schritte = [{"op": "verschmelzen", "ids": a.ids, "ziel": a.ziel}]
        elif a.op == "teilen":
            schritte = [{"op": "teilen", "id": a.id, "linie": a.linie}]
        elif a.op == "verschieben":
            schritte = [{"op": "grenze_verschieben", "von": a.von, "nach": a.nach,
                         "flaeche": a.flaeche}]
        elif a.op == "klasse":
            schritte = [{"op": "klasse_setzen", "id": a.id, "klasse": a.klasse}]
        elif a.op == "polygon":
            schritte = [{"op": "polygon_zuweisen", "flaeche": a.flaeche, "id": a.id,
                         "klasse": a.klasse}]
        else:  # stapel: alle Schritte oder keiner
            schritte = dateien.lese_json(a.datei)["schritte"]
        for nr, schritt in enumerate(schritte, 1):
            ergebnis = arbeit.anwenden(schritt)
            print(f"{nr}. {schritt['op']}: {json.dumps(ergebnis, ensure_ascii=False)}")
    except EingriffFehler as fehler:
        print(f"abgelehnt, nichts geändert: {fehler}", file=sys.stderr)
        return 1
    dateien.schreibe_labels(a.labels, arbeit.karte)
    dateien.schreibe_json(a.segmente, arbeit.segmente)
    return _befund_ausgeben(pruefen(arbeit.karte, arbeit.segmente, kat), False)


def befehl_zusammentragen(a) -> int:
    ergebnis = zusammentragen(a.datei, kategorien.laden(a.kategorien), ziel=a.ziel)
    print(json.dumps(ergebnis.als_dict(), ensure_ascii=False) if a.json else ergebnis.als_text())
    return 0 if ergebnis.ok else 1


def befehl_naht(a) -> int:
    manifest_pfad = Path(a.manifest)
    manifest = dateien.lese_json(manifest_pfad)
    werte, bestaetigt = None, None
    if a.datei:
        auftrag = lese_auftrag(a.datei)
        werte, bestaetigt = auftrag.get("naht"), auftrag.get("naht_bestaetigt")
    bild = naht.lese_bild(manifest_pfad.parent / manifest["ausschnitt"]["bild"])
    befund = naht.pruefe_naehte(dateien.lese_labels(a.labels), manifest, bild, werte, bestaetigt)
    print(json.dumps(befund.als_dict(), ensure_ascii=False) if a.json else
          "\n".join(befund.als_text() + ["ok" if befund.ok else "FEHLER"]))
    return 0 if befund.ok else 1


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python -m landseg", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    befehle = p.add_subparsers(dest="befehl", required=True)

    k = befehle.add_parser("kacheln", help="W1: Ausschnitt + Teilkacheln + Manifest")
    k.add_argument("--bild", required=True, help="Quellbild (GeoTIFF/TIFF)")
    k.add_argument("--x", type=int, required=True)
    k.add_argument("--y", type=int, required=True)
    k.add_argument("--breite", type=int, required=True)
    k.add_argument("--hoehe", type=int, required=True)
    k.add_argument("--ziel", required=True, help="Ausgabeordner (unter daten/landseg/)")
    k.add_argument("--kern", type=int, default=500, help="Kerngröße in Bildpunkten (Standard 500)")
    k.add_argument("--rand", type=int, default=64, help="Kontextrand in Bildpunkten (Standard 64)")
    k.add_argument("--name", default="ausschnitt", help="Name des Ausschnitts (Dateiname)")
    k.add_argument("--ueberschreiben", action="store_true")
    k.set_defaults(fn=befehl_kacheln)

    pr = befehle.add_parser("pruefen", help="W6: Label-Karte prüfen")
    pr.add_argument("--labels", required=True, help="Label-Karte (.tif uint32 oder .npy)")
    pr.add_argument("--segmente", help="segmente.json (dann auch Klassen prüfen)")
    pr.add_argument("--kategorien", help="kategorien.json (Standard: die des Repos)")
    form = pr.add_mutually_exclusive_group()
    form.add_argument("--form", type=_form, help="erwartete Form HxW, z. B. 628x628")
    form.add_argument("--bild", help="Bild, dessen Größe die Karte haben muss")
    pr.add_argument("--mindestflaeche", type=int, help="kleinste erlaubte Segmentfläche")
    pr.add_argument("--json", action="store_true", help="Befund als JSON")
    pr.set_defaults(fn=befehl_pruefen)

    e = befehle.add_parser("eingriff", help="W5: Label-Karte bearbeiten (schreibt zurück)")
    e.add_argument("--labels", required=True)
    e.add_argument("--segmente", required=True)
    e.add_argument("--kategorien", help="kategorien.json (Standard: die des Repos)")
    e.add_argument("--bearbeiter", required=True, help="wer eingreift (Verlauf)")
    ops = e.add_subparsers(dest="op", required=True)
    o = ops.add_parser("verschmelzen")
    o.add_argument("--ids", type=_ids, required=True, help="z. B. 3,5,8")
    o.add_argument("--ziel", type=int, help="behält ID und Klasse (Standard: erste ID)")
    o = ops.add_parser("teilen")
    o.add_argument("--id", type=int, required=True)
    o.add_argument("--linie", type=_punkte, required=True, help="x,y;x,y;...")
    o = ops.add_parser("verschieben", help="Grenze verschieben: Fläche von --von an --nach")
    o.add_argument("--von", type=int, required=True)
    o.add_argument("--nach", type=int, required=True)
    o.add_argument("--flaeche", type=_punkte, required=True, help="Polygon x,y;x,y;...")
    o = ops.add_parser("klasse")
    o.add_argument("--id", type=int, required=True)
    o.add_argument("--klasse", required=True, help="Code aus kategorien.json")
    o = ops.add_parser("polygon", help="Polygon einem Segment oder einem neuen zuweisen")
    o.add_argument("--flaeche", type=_punkte, required=True)
    ziel = o.add_mutually_exclusive_group(required=True)
    ziel.add_argument("--id", type=int)
    ziel.add_argument("--klasse")
    o = ops.add_parser("stapel", help='JSON {"schritte": [{"op": ...}, ...]}, alles oder nichts')
    o.add_argument("--datei", required=True)
    e.set_defaults(fn=befehl_eingriff)

    z = befehle.add_parser("zusammentragen", help="W7: Teilkacheln zur Label-Karte des Ausschnitts, Nähte prüfen")
    z.add_argument("--datei", required=True, help="Auftrag zusammentragen.json (Einheiten, Nutzerklassen, Fragen)")
    z.add_argument("--kategorien", help="kategorien.json (Standard: die des Repos)")
    z.add_argument("--ziel", help="Ausgabeordner (Standard: Feld 'ziel' des Auftrags)")
    z.add_argument("--json", action="store_true", help="Ergebnis als JSON")
    z.set_defaults(fn=befehl_zusammentragen)

    n = befehle.add_parser("naht", help="Nahtregel auf einer zusammengetragenen Label-Karte prüfen")
    n.add_argument("--manifest", required=True, help="manifest.json von kacheln")
    n.add_argument("--labels", required=True, help="Label-Karte des ganzen Ausschnitts")
    n.add_argument("--datei", help="Auftrag zusammentragen.json (Einstellungen 'naht', 'naht_bestaetigt')")
    n.add_argument("--json", action="store_true", help="Befund als JSON")
    n.set_defaults(fn=befehl_naht)
    return p


def main(argv: list[str] | None = None) -> int:
    for strom in (sys.stdout, sys.stderr):
        if hasattr(strom, "reconfigure"):
            strom.reconfigure(encoding="utf-8")
    a = parser().parse_args(argv)
    try:
        return a.fn(a)
    except (KachelFehler, ZusammenFehler, ValueError, OSError, KeyError) as fehler:
        print(f"Fehler: {fehler}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
