"""Befehlszeile: ``python -m landseg <befehl> ...`` (im Repo-Ordner).

Befehle: ``kacheln`` (W1), ``vorstufe`` (W2), ``ansicht`` (W3), ``kante`` (W4), ``eingriff`` (W5),
``pruefen`` (W6), ``zusammentragen`` (W7), ``seite`` (W8, Übersichtsseite), ``naht`` (Nahtregel allein),
``einigung`` (Klassen an den Übergängen der Teilkacheln: ``finden``, ``anwenden``, ``abgabe``, ``messen``),
``urteil`` (``urteil.json`` aus kurzer Liste bauen, prüfen), ``zoom`` (Ausschnitt einer Stelle mit Umriss und
Nummern), ``messung`` (Kosten eines Agent-Laufs aus den Transkripten), ``plan`` (Urteils-Agents eines Laufs:
ein Agent je Viertel, Fassung A je Teilkachel, mit Prompt). Exit-Code 0 = ok, 1 = Befund,
Nahtverstoß, offene Stellen oder Eingriff/Abgabe/Urteil abgelehnt, 2 = Aufruf- oder Lesefehler.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image

from . import dateien, einstellungen, kategorien, naht
from . import urteil as urteil_modul
from . import zoom as zoom_modul
from .ansicht import Ansicht, AnsichtFehler, ansicht
from . import einigung as einigung_modul
from .eingriff import Bearbeitung, EingriffFehler
from .einigung import EinigungFehler
from .kacheln import KachelFehler, kacheln
from .kante import einrasten
from .messung import messung_befehl, tabelle
from . import lauf as lauf_modul
from . import plan as plan_modul
from . import vorbereiten as vorbereiten_modul
from . import zusammenfuehren as zusammenfuehren_modul
from .lauf import LaufFehler
from .pruefen import pruefen
from .seite import SeiteFehler, bilder_aus_einstellungen, seite
from .vorstufe import Auftrag, VorstufeFehler, auftraege_aus_manifest, konfig_laden, vorstufe
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


def befehl_vorstufe(a) -> int:
    kat = kategorien.laden(a.kategorien)
    konfig = konfig_laden(a.konfig, kat)
    if a.manifest:
        if a.ziel:
            raise VorstufeFehler("--ziel nur mit --bild (mit --manifest: Ordner vorstufe/ daneben)")
        auftraege = auftraege_aus_manifest(a.manifest, konfig, a.teilkachel)
    else:
        if not a.ziel or a.teilkachel:
            raise VorstufeFehler("--bild braucht --ziel und kennt keine --teilkachel")
        auftraege = [Auftrag(name=Path(a.bild).stem, bild=Path(a.bild), ziel=Path(a.ziel))]

    def modell_laden():
        from .sam3 import Sam3Vorschlag
        return Sam3Vorschlag(konfig["sam3"], geraet=a.geraet)

    ergebnisse = vorstufe(auftraege, konfig, kat, modell_laden=modell_laden, neu=a.neu)
    return 0 if all(e["ok"] for e in ergebnisse) else 1


def befehl_pruefen(a) -> int:
    karte = dateien.lese_labels(a.labels)
    segmente = dateien.lese_segmente(a.segmente) if a.segmente else None
    kat = kategorien.laden(a.kategorien) if segmente is not None or a.frei else None
    form = a.form
    if a.bild:
        with Image.open(a.bild) as bild:
            form = (bild.height, bild.width)
    befund = pruefen(karte, segmente, kat, form=form, mindestflaeche=a.mindestflaeche, frei=a.frei)
    return _befund_ausgeben(befund, a.json)


def befehl_eingriff(a) -> int:
    with dateien.karte_sperren(a.labels):   # mehrere Agents je Karte (ein Agent je Viertel)
        return _eingriff(a)


def _eingriff(a) -> int:
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


def _einigung_fassungen(a) -> list:
    """Fassungen des Aufrufs: ``--ordner`` (eine), ``--fassung`` oder (nur ``messen``) alle aus den Einstellungen der Seite."""
    kat = kategorien.laden(a.kategorien)
    if a.ordner:
        return [einigung_modul.fassung_laden(a.manifest, a.ordner, kat, a.fassung or "")]
    liste = einstellungen.laden("seite")["fassungen"]
    kennungen = [a.fassung] if a.fassung else [str(e["kennung"]) for e in liste]
    fassungen = []
    for kennung in kennungen:
        try:
            fassungen.append(einigung_modul.fassung_aus_einstellungen(a.manifest, kennung, kat, liste))
        except EinigungFehler:
            if a.fassung:
                raise
    return fassungen


def befehl_einigung(a) -> int:
    einst = einstellungen.laden("einigung", a.einstellungen)
    if a.schritt == "abgabe" and not a.fassung:
        a.fassung = einigung_modul.auftrag_lesen(a.auftraege, a.buendel)["fassung"]
    if a.schritt in ("finden", "anwenden") and not (a.fassung or a.ordner):
        raise EinigungFehler(f"einigung {a.schritt}: --fassung oder --ordner angeben")
    manifest = dateien.lese_json(a.manifest)
    bild_pfad = Path(a.manifest).parent / manifest["ausschnitt"]["bild"]
    try:
        fassungen = _einigung_fassungen(a)
        if not fassungen:
            raise EinigungFehler("keine Fassung mit Daten gefunden")
        if a.schritt == "abgabe":
            abgabe, erg = einigung_modul.abgabe_bauen(fassungen[0], a.auftraege, a.buendel, a.bearbeiter,
                                                      dateien.lese_json(a.liste))
            dateien.schreibe_json(a.ziel, abgabe)
            print(json.dumps({"ziel": str(a.ziel), "probe": erg}, ensure_ascii=False) if a.json else
                  f"Abgabe {abgabe['buendel']} ({len(abgabe['paare'])} Paare: gleich {erg['gleich']}, grenze "
                  f"{erg['grenze']}, unklar {erg['unklar']}) -> {a.ziel}; Probe wie anwenden --probe: ok")
            return 0
        if a.schritt == "anwenden":
            erg = einigung_modul.anwenden(fassungen[0], [dateien.lese_json(d) for d in a.abgabe], a.auftraege,
                                          ziel=a.ziel, schreiben=not a.probe)
            print(json.dumps(erg, ensure_ascii=False) if a.json else
                  f"Fassung {erg['fassung']}: {erg['abgaben']} Abgaben, gleich {erg['gleich']}, grenze {erg['grenze']}, "
                  f"unklar {erg['unklar']}, Klassen gesetzt {erg['klassen_gesetzt']}, Teilkacheln "
                  f"{', '.join(erg['teilkacheln']) or '-'} -> {erg['ziel']}"
                  + ("" if erg["geschrieben"] else " (Probe, nichts geschrieben)"))
            return 0
        bild = naht.lese_bild(bild_pfad)
        if a.schritt == "finden":
            erg = einigung_modul.finden(fassungen[0], bild, einst, a.ziel)
            z = erg["zahlen"]
            print(json.dumps(erg, ensure_ascii=False) if a.json else
                  f"Fassung {erg['fassung']}: {z['offen']['paare']} offene Stellen ({z['offen']['randpunkte']} "
                  f"Randpunkte) in {len(erg['buendel'])} Bündeln -> {Path(a.ziel) / 'einigung.json'}")
            return 0
        ergebnisse = [einigung_modul.messen(f, bild, einst) for f in fassungen]
    except EingriffFehler as fehler:
        raise EinigungFehler(str(fehler)) from None
    if a.json:
        print(json.dumps(ergebnisse, ensure_ascii=False))
    else:
        for e in ergebnisse:
            print(f"Fassung {e['fassung']}: gleiche Fläche, verschiedene Klasse: offen {e['offen']['paare']} Paare "
                  f"({e['offen']['randpunkte']} Randpunkte), unsicher belegt {e['unsicher']['paare']} "
                  f"({e['unsicher']['randpunkte']}), geklärt {e['geklaert']['paare']} ({e['geklaert']['randpunkte']}); "
                  f"Schnittlinien ohne Bildkante: {e['ohne_kante']['paare']} Paare")
    return 0 if all(e["offen"]["paare"] == 0 for e in ergebnisse) else 1


def _teilkachel_quelle(a) -> tuple[Path, dict | None]:
    """Bildpfad und ``kern_im_bild`` aus ``--manifest``/``--teilkachel`` oder ``--bild`` (ohne Kern)."""
    if not a.manifest:
        return Path(a.bild), None
    manifest = dateien.lese_json(a.manifest)
    teil = next((t for t in manifest["teilkacheln"] if t["id"] == a.teilkachel), None)
    if teil is None:
        raise ValueError(f"Teilkachel {a.teilkachel!r} steht nicht im Manifest")
    return Path(a.manifest).parent / teil["bild"], teil["kern_im_bild"]


def befehl_urteil(a) -> int:
    kat = kategorien.laden(a.kategorien)
    if a.schritt == "pruefen":
        urteil = dateien.lese_json(a.urteil)
        teilkachel = a.teilkachel or urteil.get("teilkachel")
        viertel = a.viertel or urteil.get("viertel")
        ordner = Path(a.urteil).parent
    else:
        teilkachel, viertel, ordner = a.teilkachel, a.viertel, Path(a.ziel).parent
    g = urteil_modul.grundlage_laden(a.manifest, teilkachel, a.labels, kat, a.segmente, viertel)
    try:
        if a.schritt == "bauen":
            urteil = urteil_modul.bauen(g, dateien.lese_json(a.liste), a.bearbeiter)
        fehler = urteil_modul.pruefen(g, urteil, ordner)
    except urteil_modul.UrteilFehler as f:
        fehler = [str(f)]
    geschrieben = a.schritt == "bauen" and not fehler
    if geschrieben:
        dateien.schreibe_json(a.ziel, urteil)
    if a.json:
        print(json.dumps({"ok": not fehler, "fehler": fehler, "segmente_soll": len(g.soll),
                          "ziel": str(a.ziel) if geschrieben else None}, ensure_ascii=False))
        return 1 if fehler else 0
    for f in fehler:
        print(f"- {f}")
    wo = teilkachel + (f" Viertel {viertel}" if viertel else "")
    if fehler:
        print(f"FEHLER: {len(fehler)} Befunde in {wo}" + (", nichts geschrieben" if a.schritt == "bauen" else ""))
        return 1
    print(f"ok: {wo}, {len(g.soll)} Segmente mit Urteil" + (f" -> {a.ziel}" if geschrieben else ""))
    return 0


def befehl_zoom(a) -> int:
    if (a.punkt is None) != (a.radius is None):
        raise AnsichtFehler("--punkt und --radius gehören zusammen")
    bild_pfad, kern = _teilkachel_quelle(a)
    segmente = dateien.lese_segmente(a.segmente) if a.segmente else None
    ans = Ansicht(zoom_modul.bild_rgb(naht.lese_bild(bild_pfad)), dateien.lese_labels(a.labels), segmente,
                  kategorien.laden(a.kategorien) if segmente is not None else None,
                  einstellungen.laden("ansicht"), kern=kern)
    erg = zoom_modul.zoom(ans, einstellungen.laden("zoom", a.einstellungen), a.ziel, punkt=a.punkt,
                          radius=a.radius, rechteck=a.rechteck, ids=a.ids, roh=a.roh,
                          titel=a.teilkachel or bild_pfad.stem)
    f = erg["fenster"]
    print(json.dumps(erg, ensure_ascii=False) if a.json else
          f"{erg['ziel']}: {erg['groesse'][0]} × {erg['groesse'][1]} px, Ausschnitt x {f['x']}, y {f['y']}, "
          f"{f['breite']} × {f['hoehe']}, {f['faktor']}-fach, {len(erg['nummern'])} Nummern"
          + (", neben dem Luftbild" if erg["roh"] else ""))
    return 0


def _rgb_bild(pfad) -> np.ndarray:
    with Image.open(pfad) as bild:
        return np.asarray(bild.convert("RGB"))


def _rechteck(text: str) -> dict:
    x, y, b, h = (int(v) for v in text.split(","))
    return {"x": x, "y": y, "breite": b, "hoehe": h}


def befehl_seite(a) -> int:
    kat = kategorien.laden(a.kategorien)
    werte = einstellungen.laden("seite", a.einstellungen)
    bilder = a.manifest if a.manifest else bilder_aus_einstellungen(a.daten, werte)
    erg = seite(bilder, a.ziel, kat, kommentare=a.kommentare, werte=werte)
    if a.json:
        print(json.dumps(erg, ensure_ascii=False))
    else:
        for b in erg["bilder"]:
            if not b["vorhanden"]:
                print(f"Bild {b['kennung']} ({b['titel']}): keine Daten ({b['grund']})")
                continue
            if len(erg["bilder"]) > 1:
                print(f"Bild {b['kennung']} ({b['titel']}):")
            for f in b["fassungen"]:
                print(_fassung_zeile(f))
        print(f"Seite: {erg['ziel']} ({erg['groesse'] // 1024} KiB)")
    if a.oeffnen:
        import webbrowser
        webbrowser.open(Path(erg["ziel"]).resolve().as_uri())
    return 0


def _fassung_zeile(f: dict) -> str:
    if not f["vorhanden"]:
        return f"Fassung {f['kennung']} ({f['name']}): keine Daten in {f['quelle']}"
    teile = [f"{t['id']} –" if "segmente" not in t else
             f"{t['id']} {t['segmente']} Segmente, pruefen {'ok' if t['pruefen_ok'] else 'FEHLER'}"
             for t in f["teilkacheln"]]
    naht_text = "nicht geprüft" if f["naht"] is None else f["naht"]
    e = f["einigung"]
    einigung_text = "nicht gezählt" if e is None else f"{e['stellen']} (davon {e['unsicher']} unsicher belegt)"
    return (f"Fassung {f['kennung']} ({f['name']}): " + "; ".join(teile) + f"; Schnittlinien ohne Bildkante "
            f"{naht_text}; gleiche Fläche, verschiedene Klasse {einigung_text}")


def befehl_ansicht(a) -> int:
    kern = a.kern
    quelle = {}
    if a.manifest:
        manifest_pfad = Path(a.manifest)
        manifest = dateien.lese_json(manifest_pfad)
        teil = next((t for t in manifest["teilkacheln"] if t["id"] == a.teilkachel), None)
        if teil is None:
            raise ValueError(f"Teilkachel {a.teilkachel!r} steht nicht im Manifest")
        bild_pfad = manifest_pfad.parent / teil["bild"]
        kern = kern or teil["kern_im_bild"]
        quelle = {"manifest": str(manifest_pfad), "teilkachel": a.teilkachel}
    else:
        bild_pfad = Path(a.bild)
    quelle.update({"bild": str(bild_pfad), "labels": a.labels, "segmente": a.segmente})
    karte = dateien.lese_labels(a.labels) if a.labels else None
    segmente = dateien.lese_segmente(a.segmente) if a.segmente else None
    kat = kategorien.laden(a.kategorien) if segmente is not None else None
    index = ansicht(_rgb_bild(bild_pfad), karte, a.ziel, segmente=segmente, kategorien=kat,
                    kern=kern, ids=a.ids, nur_teilkachel=a.nur_teilkachel,
                    kandidaten=dateien.lese_json(a.kandidaten) if a.kandidaten else None,
                    kante=dateien.lese_json(a.kante) if a.kante else None,
                    mindestflaeche=a.mindestflaeche,
                    vorgaben=einstellungen.laden("ansicht", a.einstellungen), quelle=quelle)
    teil_arten = ", ".join(index["teilkachel"]["bilder"])
    print(f"{index['bilderzahl']} Bilder: Teilkachel ({teil_arten}), "
          f"{len(index['segmente'])} Segmente -> {Path(a.ziel) / 'ansicht.json'}")
    m = index["maengel"]
    if m:
        print(f"Mängel: Lücke {m['luecke_bildpunkte']} px, nicht zusammenhängend "
              f"{len(m['nicht_zusammenhaengend'])}, ohne Eintrag {len(m['ohne_eintrag'])}, "
              f"zu klein {len(m['zu_klein'])}, sicher: nein {len(m['unsicher'])}, Kandidaten "
              f"{len(m['kandidaten'])}, geschätzte Strecken {m['geschaetzt_strecken']}")
    return 0


def befehl_kante(a) -> int:
    if a.trocken:
        return _kante(a)
    with dateien.karte_sperren(a.labels):   # mehrere Agents je Karte (ein Agent je Viertel)
        return _kante(a)


def _kante(a) -> int:
    karte = dateien.lese_labels(a.labels)
    bild = _rgb_bild(a.bild)
    vorgaben = einstellungen.laden("kante", a.einstellungen)
    try:
        if a.trocken:
            ergebnis = einrasten(bild, karte, a.a, a.b, vorgaben, band=a.band, bereich=a.bereich)
        else:
            if not a.segmente or not a.bearbeiter:
                raise EingriffFehler("ohne --trocken sind --segmente und --bearbeiter nötig")
            kat = kategorien.laden(a.kategorien)
            arbeit = Bearbeitung(karte, dateien.lese_segmente(a.segmente), kat, a.bearbeiter)
            ergebnis = arbeit.kante_einrasten(bild, a.a, a.b, vorgaben, band=a.band,
                                              bereich=a.bereich)
    except EingriffFehler as fehler:
        print(f"abgelehnt, nichts geändert: {fehler}", file=sys.stderr)
        return 1
    print(json.dumps(ergebnis.als_dict(mit_punkten=False), ensure_ascii=False) if a.json
          else ergebnis.als_text())
    if a.bericht:
        dateien.schreibe_json(a.bericht, ergebnis.als_dict())
    if a.trocken:
        print("trocken: nichts geschrieben")
        return 0
    dateien.schreibe_labels(a.labels, arbeit.karte)
    dateien.schreibe_json(a.segmente, arbeit.segmente)
    return _befund_ausgeben(pruefen(arbeit.karte, arbeit.segmente, kat), False)


def befehl_plan(a) -> int:
    p = plan_modul.plan(a.auftraege, a.repo or Path(__file__).resolve().parent.parent, a.py or sys.executable,
                        hinweis=a.hinweis or "", teilkacheln=a.teilkachel, viertel=a.viertel)
    zeilen = plan_modul.log_zeilen(p)
    if a.ziel:
        dateien.schreibe_json(a.ziel, p)
        zeilen.append(f"Plan geschrieben: {a.ziel}")
    else:
        zeilen.append("trocken: nichts geschrieben (ohne --ziel)")
    print(json.dumps(p, ensure_ascii=False) if a.json else "\n".join(zeilen))
    return 0


def befehl_messung(a) -> int:
    m = messung_befehl(a.transkripte, lauf=a.lauf, ziel=a.ziel)
    print(json.dumps(m, ensure_ascii=False) if a.json else tabelle(m))
    return 0


def _lauf_einstellungen(a) -> tuple[dict, dict]:
    return lauf_modul.einstellungen_laden(a.einstellungen, a.seite)


def befehl_vorbereiten(a) -> int:
    werte, seite_werte = _lauf_einstellungen(a)
    try:
        if a.nur_pruefen:
            fehler = vorbereiten_modul.pruefen(a.manifest, a.ziel, werte=werte, seite=seite_werte)
            if fehler:
                raise LaufFehler(fehler)
            print("Vorbereitung geprüft: ok")
            return 0
        hinweis = Path(a.hinweis).read_text(encoding="utf-8") if a.hinweis else ""
        plan = vorbereiten_modul.bauen(a.manifest, a.ziel, werte=werte, seite=seite_werte, py=a.py or sys.executable,
                                       hinweis=hinweis, name=a.lauf or "", ersetzen=a.ersetzen)
    except LaufFehler as fehler:
        print("Abgelehnt:\n" + "\n".join(f"- {x}" for x in fehler.fehler), file=sys.stderr)
        return 1
    if a.json:
        print(json.dumps(plan, ensure_ascii=False))
    else:
        zahl = {}
        for e in plan["einheiten"]:
            zahl[e["art"]] = zahl.get(e["art"], 0) + 1
        print(f"Einheiten: {', '.join(f'{k} {v}' for k, v in zahl.items())}; Kernsegmente "
              f"{', '.join(f'{tk} {n}' for tk, n in plan['kernsegmente'].items())}; "
              f"Vereinheitlichen {len(plan['vereinheitlichen'])}; {plan['sekunden']} s")
        print(f"Plan: {Path(a.ziel) / 'auftraege.json'} (weiter mit landseg plan --auftraege …)")
        print("ok")
    return 0


def befehl_zusammenfuehren(a) -> int:
    werte, seite_werte = _lauf_einstellungen(a)
    try:
        erg = zusammenfuehren_modul.bauen(a.manifest, a.ziel, werte=werte, seite=seite_werte, ersetzen=a.ersetzen)
    except LaufFehler as fehler:
        print("Abgelehnt, nichts geschrieben:\n" + "\n".join(f"- {x}" for x in fehler.fehler), file=sys.stderr)
        return 1
    if a.json:
        print(json.dumps(erg, ensure_ascii=False))
    else:
        for k, e in erg["fassungen"].items():
            fehl = [tk for tk, x in e["pruefen"].items() if x != "ok"]
            print(f"Fassung {k} ({e['name']}): {e['segmente_kern']} Kernsegmente, unsicher {e['unsicher']}, "
                  f"Eingriffe {e['eingriffe_urteil']} (Verlauf {e['eingriffe_verlauf']}), Nahtverstöße "
                  f"{e['nahtverstoesse']}, offen an Übergängen {e['einigung_offen']} Paare in {len(e['buendel'])} "
                  f"Bündeln -> {e['auftraege']}" + (f"; pruefen FEHLER {', '.join(fehl)}" if fehl else ""))
        print(f"Befund: {Path(a.ziel) / 'zusammenfuehren.json'} ({erg['sekunden']} s)")
        print("ok" if erg["ok"] else "FEHLER")
    return 0 if erg["ok"] else 1


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

    v = befehle.add_parser("vorstufe", help="W2: lückenlose Vorbelegung (Superpixel, SAM 3, GPU)")
    quelle = v.add_mutually_exclusive_group(required=True)
    quelle.add_argument("--manifest", help="manifest.json von kacheln; Ausgabe in vorstufe/<id>/")
    quelle.add_argument("--bild", help="einzelnes Bild statt Teilkacheln (dann --ziel)")
    v.add_argument("--teilkachel", action="append", help="ID aus dem Manifest, mehrfach; Standard alle")
    v.add_argument("--ziel", help="Ausgabeordner (nur mit --bild)")
    v.add_argument("--konfig", help="Einstellungen (Standard: vorstufe.json des Repos)")
    v.add_argument("--kategorien", help="kategorien.json (Standard: die des Repos)")
    v.add_argument("--geraet", default="cuda", help="Torch-Gerät für SAM 3 (Standard cuda)")
    v.add_argument("--neu", action="store_true", help="auch fertige Teilkacheln neu rechnen")
    v.set_defaults(fn=befehl_vorstufe)

    pr = befehle.add_parser("pruefen", help="W6: Label-Karte prüfen")
    pr.add_argument("--labels", required=True, help="Label-Karte (.tif uint32 oder .npy)")
    pr.add_argument("--segmente", help="segmente.json (dann auch Klassen prüfen)")
    pr.add_argument("--kategorien", help="kategorien.json (Standard: die des Repos)")
    form = pr.add_mutually_exclusive_group()
    form.add_argument("--form", type=_form, help="erwartete Form HxW, z. B. 628x628")
    form.add_argument("--bild", help="Bild, dessen Größe die Karte haben muss")
    pr.add_argument("--mindestflaeche", type=int, help="kleinste erlaubte Segmentfläche")
    pr.add_argument("--frei", action="store_true",
                    help="Liste einer freien Fassung (A, B): Klasse „Garten“ muss unter „Dauergrünland“ stehen")
    pr.add_argument("--json", action="store_true", help="Befund als JSON")
    pr.set_defaults(fn=befehl_pruefen)

    an = befehle.add_parser("ansicht", help="W3: Standardbilder je Teilkachel und Segment")
    quelle = an.add_mutually_exclusive_group(required=True)
    quelle.add_argument("--bild", help="Bild der Teilkachel (PNG)")
    quelle.add_argument("--manifest", help="manifest.json von kacheln (mit --teilkachel)")
    an.add_argument("--teilkachel", help="ID der Teilkachel im Manifest, z. B. r0c0")
    an.add_argument("--kern", type=_rechteck, help="Kern im Bild x,y,breite,hoehe (Rahmen)")
    an.add_argument("--labels", help="Label-Karte; ohne nur roh, kontrast, gitter")
    an.add_argument("--segmente", help="segmente.json (Klassen, sicher)")
    an.add_argument("--kategorien", help="kategorien.json (Standard: die des Repos)")
    an.add_argument("--kandidaten", help='JSON {"kandidaten": [{"id": .., "grund": ..}]}')
    an.add_argument("--kante", help="Bericht von kante --bericht (geschätzte Strecken)")
    an.add_argument("--ids", type=_ids, help="nur diese Segmente, z. B. 3,5,8")
    an.add_argument("--nur-teilkachel", action="store_true", help="keine Bilder je Segment")
    an.add_argument("--mindestflaeche", type=int, help="kleinere Segmente als Mangel zeigen")
    an.add_argument("--einstellungen", help="JSON, überschreibt einstellungen/ansicht.json")
    an.add_argument("--ziel", required=True, help="Ausgabeordner (unter daten/landseg/)")
    an.set_defaults(fn=befehl_ansicht)

    kn = befehle.add_parser("kante", help="W4: Grenze a|b auf die Bildkante einrasten "
                                          "(schreibt zurück, außer --trocken)")
    kn.add_argument("--labels", required=True)
    kn.add_argument("--bild", required=True, help="Bild der Teilkachel (gleiche Größe)")
    kn.add_argument("--segmente", help="segmente.json (nötig ohne --trocken)")
    kn.add_argument("--kategorien", help="kategorien.json (Standard: die des Repos)")
    kn.add_argument("--bearbeiter", help="wer eingreift (Verlauf; nötig ohne --trocken)")
    kn.add_argument("--a", type=int, required=True, help="Segment auf der einen Seite")
    kn.add_argument("--b", type=int, required=True, help="Segment auf der anderen Seite")
    kn.add_argument("--band", type=int, help="halbe Bandbreite in px (Standard aus Einstellungen)")
    kn.add_argument("--bereich", type=_punkte, help="nur hier einrasten: Polygon x,y;x,y;...")
    kn.add_argument("--einstellungen", help="JSON, überschreibt einstellungen/kante.json")
    kn.add_argument("--bericht", help="Ergebnis mit allen Punkten der Strecken als JSON")
    kn.add_argument("--trocken", action="store_true", help="nur melden, nichts schreiben")
    kn.add_argument("--json", action="store_true", help="Meldung als JSON")
    kn.set_defaults(fn=befehl_kante)

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

    se = befehle.add_parser("seite", help="W8: Übersichtsseite als eine HTML-Datei (Bilder, Fassungen, Ebenen, "
                                          "Lücken, Nähte, Kommentare)")
    quelle = se.add_mutually_exclusive_group(required=True)
    quelle.add_argument("--manifest",
                        help="manifest.json von kacheln: Seite mit diesem einen Bild (Ordner der Fassungen relativ "
                             "dazu, siehe einstellungen/seite.json)")
    quelle.add_argument("--daten",
                        help="Ordner, zu dem die Manifeste unter 'bilder' in einstellungen/seite.json relativ sind: "
                             "Seite mit allen Bildern und Bildwahl")
    se.add_argument("--kommentare", action="append",
                    help="schon exportierte Kommentare (JSON) zum Anzeigen; mehrfach möglich, je Datei dem Bild aus "
                         "ihrem Export zugeordnet")
    se.add_argument("--kategorien", help="kategorien.json für Fassungen ohne eigene Liste (Standard: die des Repos)")
    se.add_argument("--einstellungen", help="JSON, überschreibt einstellungen/seite.json (etwa 'fassungen')")
    se.add_argument("--ziel", required=True, help="HTML-Datei (unter daten/landseg/)")
    se.add_argument("--oeffnen", action="store_true", help="danach im Standardbrowser öffnen")
    se.add_argument("--json", action="store_true", help="Zusammenfassung als JSON")
    se.set_defaults(fn=befehl_seite)

    n = befehle.add_parser("naht", help="Nahtregel auf einer zusammengetragenen Label-Karte prüfen")
    n.add_argument("--manifest", required=True, help="manifest.json von kacheln")
    n.add_argument("--labels", required=True, help="Label-Karte des ganzen Ausschnitts")
    n.add_argument("--datei", help="Auftrag zusammentragen.json (Einstellungen 'naht', 'naht_bestaetigt')")
    n.add_argument("--json", action="store_true", help="Befund als JSON")
    n.set_defaults(fn=befehl_naht)

    ei = befehle.add_parser("einigung", help="Klassen an den Übergängen der Teilkacheln abgleichen "
                                             "(finden, anwenden, abgabe, messen)")
    schritte = ei.add_subparsers(dest="schritt", required=True)
    for name, hilfe in (("finden", "offene Stellen bündeln, je Bündel Auftrag mit Bildern beider Seiten"),
                        ("anwenden", "Abgaben der Agents (einigung_abgabe.json) umsetzen, nur Klassen und Vermerke"),
                        ("abgabe", "einigung_abgabe.json aus einer kurzen Liste bauen (Paar oder Nummer, "
                                   "Entscheidung, Klasse, Grund) und wie anwenden --probe prüfen"),
                        ("messen", "Stellen gleicher Fläche mit verschiedener Klasse zählen: offen, unsicher, geklärt")):
        s = schritte.add_parser(name, help=hilfe, description=hilfe)
        s.add_argument("--manifest", required=True, help="manifest.json von kacheln")
        s.add_argument("--fassung", help="Kennung der Fassung aus einstellungen/seite.json (A, B, C); "
                                         "messen ohne --fassung und --ordner: alle")
        s.add_argument("--ordner", help="Ordner der Fassung mit <teilkachel>/labels.tif und segmente.json "
                                        "(statt der Einstellungen der Seite)")
        s.add_argument("--kategorien", help="Kategorienliste für --ordner bzw. Fassungen ohne eigene "
                                            "(Standard: die des Repos)")
        s.add_argument("--einstellungen", help="JSON, überschreibt einstellungen/einigung.json")
        s.add_argument("--json", action="store_true", help="Ergebnis als JSON")
        if name == "finden":
            s.add_argument("--ziel", required=True, help="neuer Ordner für einigung.json und die Bündel-Aufträge")
        if name == "anwenden":
            s.add_argument("--auftraege", required=True, help="Ordner von einigung finden (<bündel>/auftrag.json)")
            s.add_argument("--abgabe", action="append", required=True, help="einigung_abgabe.json (mehrfach)")
            s.add_argument("--ziel", help="neuer Ordner: Kopie der Fassung, in der geändert wird "
                                          "(sonst an Ort und Stelle)")
            s.add_argument("--probe", action="store_true", help="nur prüfen, nichts schreiben")
        if name == "abgabe":
            s.add_argument("--auftraege", required=True, help="Ordner von einigung finden (<bündel>/auftrag.json)")
            s.add_argument("--buendel", required=True, help="Name des Bündels, z. B. A-02 (die Fassung kommt aus dem "
                                                            "Auftrag, wenn --fassung fehlt)")
            s.add_argument("--bearbeiter", required=True, help="Name des Agents")
            s.add_argument("--liste", required=True,
                           help='JSON {"paare": [[Nummer oder "a|b", "gleich|grenze|unklar", "Klasse oder null", '
                                '"Grund"], ...], "offen": [], "nicht_geprueft": []}')
            s.add_argument("--ziel", required=True, help="einigung_abgabe.json im eigenen Ergebnisordner")
    ei.set_defaults(fn=befehl_einigung)

    me = befehle.add_parser("messung", help="Kosten eines Agent-Laufs je Phase aus den Transkripten "
                                            "(Tokens, USD, Minuten, Bilder, .py)")
    me.add_argument("--transkripte", required=True, help="Protokollordner des Laufs mit agent-*.jsonl und "
                                                         "agent-*.meta.json (wird nur gelesen)")
    me.add_argument("--lauf", help="Name des Laufs in Tabelle und messung.json (Standard: Name des Ordners)")
    me.add_argument("--ziel", help="Ordner für messung.json und messung.md (sonst nur Ausgabe)")
    me.add_argument("--json", action="store_true", help="Ergebnis als JSON statt Tabelle")
    me.set_defaults(fn=befehl_messung)

    pl = befehle.add_parser("plan", help="Urteils-Agents eines Laufs bilden: ein Agent je Viertel (B, C, "
                                          "Gegenprobe), Fassung A je Teilkachel; je Agent ein Auftrag und Prompt")
    pl.add_argument("--auftraege", required=True, help="auftraege.json der Vorbereitung (einheiten, Übersichtsbilder)")
    pl.add_argument("--repo", help="Ordner des Repos im Prompt (Standard: dieses Repo)")
    pl.add_argument("--py", help="Python für die Agents im Prompt (Standard: dieses Python)")
    pl.add_argument("--hinweis", help="Satz zum Bild für alle Agents, z. B. Schwarz-Weiß-Scan (Standard: keiner)")
    pl.add_argument("--teilkachel", nargs="+", help="nur diese Teilkacheln (Trockenlauf auf wenig Daten)")
    pl.add_argument("--viertel", nargs="+", type=int, choices=[1, 2, 3, 4],
                    help="nur diese Viertel (Fassung A fällt dann weg)")
    pl.add_argument("--ziel", help="Plan als JSON (landseg-urteil-plan/1); ohne: nur Ausgabe, nichts geschrieben")
    pl.add_argument("--json", action="store_true", help="ganzen Plan als JSON ausgeben (mit Prompts)")
    pl.set_defaults(fn=befehl_plan)

    for name, hilfe in (("vorbereiten", "Urteile eines Laufs vorbereiten: Kartenkopien, Bilder, Aufträge aus den Vorlagen, "
                                        "Plan (auftraege.json), leere Ergebnisordner; prüft sich selbst"),
                        ("zusammenfuehren", "Urteile und freie Abgabe je Fassung zu Karten und Listen, dann pruefen, "
                                            "zusammentragen, naht, einigung finden")):
        lv = befehle.add_parser(name, help=hilfe, description=hilfe + ". Fassungen: einstellungen/seite.json + lauf.json.")
        lv.add_argument("--manifest", required=True, help="manifest.json des Ausschnitts (Ordner = Daten des Laufs)")
        lv.add_argument("--ziel", required=True, help="Berichtsordner des Laufs (Aufträge, Plan, Einigung, Befund)")
        lv.add_argument("--einstellungen", help="eigene lauf.json (überschreibt die genannten Schlüssel)")
        lv.add_argument("--seite", help="eigene seite.json (Fassungen: Kennung, Name, Ordner, Liste)")
        lv.add_argument("--ersetzen", action="store_true", help="Ziele mit Inhalt ausdrücklich neu bauen")
        lv.add_argument("--json", action="store_true", help="Ergebnis als JSON")
        if name == "vorbereiten":
            lv.add_argument("--hinweis", help="Markdown-Datei mit dem Hinweis des Laufs (etwa Schwarz-Weiß-Scan)")
            lv.add_argument("--lauf", help="Name des Laufs in den Bearbeiter-Namen (Standard: Name des Ausschnitts)")
            lv.add_argument("--py", help="Python der Agents in den Aufträgen (Standard: dieser Interpreter)")
            lv.add_argument("--nur-pruefen", action="store_true", help="fertige Vorbereitung nur prüfen, nichts schreiben")
            lv.set_defaults(fn=befehl_vorbereiten)
        else:
            lv.set_defaults(fn=befehl_zusammenfuehren)

    ur = befehle.add_parser("urteil", help="urteil.json aus einer kurzen Liste bauen und prüfen (bauen, pruefen)")
    schritte = ur.add_subparsers(dest="schritt", required=True)
    for name, hilfe in (("bauen", "urteil.json aus der kurzen Liste des Agents bauen; schreibt nur, wenn die "
                                  "Prüfung ok ist"),
                        ("pruefen", "urteil.json prüfen: jeder Fehler in Klartext (Exit 0 ok, 1 Fehler)")):
        s = schritte.add_parser(name, help=hilfe, description=hilfe + ". Format der Liste: README, Abschnitt urteil.")
        s.add_argument("--manifest", required=True, help="manifest.json von kacheln")
        s.add_argument("--teilkachel", required=name == "bauen",
                       help="ID der Teilkachel, z. B. r0c0 (pruefen: Standard aus urteil.json)")
        s.add_argument("--viertel", choices=list(urteil_modul.VIERTEL),
                       help="nur dieses Viertel des Kerns (v1 oben links, v2 oben rechts, v3 unten links, "
                            "v4 unten rechts)")
        s.add_argument("--labels", required=True, help="aktuelle Label-Karte der Teilkachel")
        s.add_argument("--segmente", required=name == "bauen", help="segmente.json dazu (heutige Klasse)")
        s.add_argument("--kategorien", help="Kategorienliste der Fassung (Standard: die des Repos)")
        s.add_argument("--json", action="store_true", help="Ergebnis als JSON")
        if name == "bauen":
            s.add_argument("--bearbeiter", required=True, help="Name des Agents")
            s.add_argument("--liste", required=True,
                           help='JSON {"segmente": [[id, urteil, vorschlag, punkte, bilder], ...], "sauber": [ids], '
                                '"naht": [], "unsicher": [], "nicht_geprueft": [], "offen": []}')
            s.add_argument("--ziel", required=True, help="urteil.json im eigenen Ergebnisordner (Bilder relativ dazu)")
        else:
            s.add_argument("--urteil", required=True, help="urteil.json (Bilder relativ zu ihrem Ordner)")
    ur.set_defaults(fn=befehl_urteil)

    zo = befehle.add_parser("zoom", help="Ausschnitt einer Stelle vergrößert, mit Umriss und Segmentnummern (JPEG)")
    quelle = zo.add_mutually_exclusive_group(required=True)
    quelle.add_argument("--manifest", help="manifest.json von kacheln (mit --teilkachel; Kern als Rahmen)")
    quelle.add_argument("--bild", help="Bild der Teilkachel")
    zo.add_argument("--teilkachel", help="ID der Teilkachel im Manifest, z. B. r0c0")
    zo.add_argument("--labels", required=True, help="Label-Karte (gleiche Größe wie das Bild)")
    zo.add_argument("--segmente", help="segmente.json (nicht nötig für Umriss und Nummern)")
    zo.add_argument("--kategorien", help="kategorien.json (Standard: die des Repos)")
    stelle = zo.add_mutually_exclusive_group(required=True)
    stelle.add_argument("--punkt", type=lambda text: _punkte(text)[0], help="Mitte x,y (mit --radius)")
    stelle.add_argument("--rechteck", type=_rechteck, help="x,y,breite,hoehe")
    stelle.add_argument("--ids", type=_ids, help="Segmente, z. B. 3,5,8 (Rahmen um alle, farbig umrandet)")
    zo.add_argument("--radius", type=int, help="Radius um --punkt in Bildpunkten")
    zo.add_argument("--roh", action="store_true", help="links das rohe Luftbild daneben")
    zo.add_argument("--einstellungen", help="JSON, überschreibt einstellungen/zoom.json")
    zo.add_argument("--ziel", required=True, help="JPEG im eigenen Ergebnisordner, z. B. nah_17_1.jpg")
    zo.add_argument("--json", action="store_true", help="Ergebnis als JSON (Fenster, Lage der Nummern)")
    zo.set_defaults(fn=befehl_zoom)
    return p


def main(argv: list[str] | None = None) -> int:
    for strom in (sys.stdout, sys.stderr):
        if hasattr(strom, "reconfigure"):
            strom.reconfigure(encoding="utf-8")
    a = parser().parse_args(argv)
    try:
        return a.fn(a)
    except EinigungFehler as fehler:
        print(f"Abgelehnt: {fehler}", file=sys.stderr)
        return 1
    except (KachelFehler, VorstufeFehler, AnsichtFehler, ZusammenFehler, SeiteFehler, ValueError, OSError,
            KeyError) as fehler:
        print(f"Fehler: {fehler}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
