"""Zerfallene Kernsegmente der H0-Fassungen beheben (Teil 4 von landseg-historisch).

Ein Segment einer Teilkachel ist im Teilkachelbild zusammenhängend, im Kern aber in mehrere Teile
zerfallen (nur über den Kontextrand verbunden). Nach dem Zusammentragen ist es dann nicht
zusammenhängend. Der größte Kernteil behält die ID; jeder weitere Kernteil geht an einen
angrenzenden Nachbarn gleicher Klasse im Kern (längste gemeinsame Grenze) oder bekommt eine eigene
neue ID mit derselben Klasse. Bildpunkte des Segments im Kontextrand gehen an den nächstgelegenen
Kernteil (euklidisch), damit jede Teilkachelkarte zusammenhängend bleibt.

Aufruf: python -B zerfall_beheben.py <H0-Ordner> <Sicherungsordner> <Protokoll.json> [--probe]
"""
import copy
import json
import shutil
import sys
from pathlib import Path

import numpy as np
from scipy import ndimage

sys.path.insert(0, "C:/Users/Phil/Developement/Victor/landseg")
from landseg.dateien import lese_labels, schreibe_labels, lese_json, schreibe_json  # noqa: E402

VIERER = ndimage.generate_binary_structure(2, 1)
FASSUNGEN = ["a-alles-frei", "b-kategorien-frei", "c-feste-liste"]


def kernteile(karte, kern_sl):
    """{id: [Masken der Kernteile im Kernausschnitt, absteigend nach Größe]} für zerfallene IDs."""
    k = karte[kern_sl]
    ergebnis = {}
    for sid in np.unique(k):
        maske = k == sid
        lab, n = ndimage.label(maske, structure=VIERER)
        if n > 1:
            groessen = ndimage.sum(maske, lab, range(1, n + 1))
            reihenfolge = np.argsort(-groessen)
            ergebnis[int(sid)] = [lab == (i + 1) for i in reihenfolge]
    return ergebnis


def nachbar_gleicher_klasse(k, teil, klasse, segs, eigene_id):
    rand = ndimage.binary_dilation(teil, structure=VIERER) & ~teil
    ids, zahl = np.unique(k[rand], return_counts=True)
    beste = None
    for nid, z in sorted(zip(ids.tolist(), zahl.tolist()), key=lambda p: -p[1]):
        if nid == eigene_id:
            continue
        if segs.get(nid, {}).get("klasse") == klasse:
            beste = nid
            break
    return beste


def bearbeite(fassung_dir, tk, info, sicherung, probe):
    lab_p, seg_p = fassung_dir / tk / "labels.tif", fassung_dir / tk / "segmente.json"
    karte = lese_labels(lab_p).copy()
    daten = lese_json(seg_p)
    segs = {int(s["id"]): s for s in daten["segmente"]}
    kib, kern = info["kern_im_bild"], info["kern"]
    y0, x0, h, w = kib["y"], kib["x"], kern["hoehe"], kern["breite"]
    kern_sl = (slice(y0, y0 + h), slice(x0, x0 + w))
    zerfallen = kernteile(karte, kern_sl)
    protokoll = []
    if not zerfallen:
        return protokoll
    naechste_id = max(segs) + 1
    for sid, teile in zerfallen.items():
        eintrag = segs[sid]
        klasse = eintrag.get("klasse")
        voll = karte == sid
        # Kontextpixel des Segments dem nächsten Kernteil zuordnen
        teil_marker = np.zeros(karte.shape, dtype=np.int32)
        for i, t in enumerate(teile):
            teil_marker[kern_sl][t] = i + 1
        # geodätisch innerhalb des Segments wachsen lassen: jedes Stück bleibt zusammenhängend
        zuordnung = teil_marker.copy()
        while True:
            offen = voll & (zuordnung == 0)
            if not offen.any():
                break
            gewachsen = ndimage.grey_dilation(zuordnung, footprint=VIERER)
            neu = offen & (gewachsen > 0)
            if not neu.any():
                break
            zuordnung[neu] = gewachsen[neu]
        for i, t in enumerate(teile[1:], start=2):
            stueck = zuordnung == i
            nid = nachbar_gleicher_klasse(karte[kern_sl], t, klasse, segs, sid)
            n_kern = int(t.sum())
            n_ges = int(stueck.sum())
            if nid is not None:
                karte[stueck] = nid
                segs[nid]["flaeche"] = int(segs[nid].get("flaeche", 0)) + n_ges
                if "flaeche_kern" in segs[nid]:
                    segs[nid]["flaeche_kern"] = int(segs[nid]["flaeche_kern"]) + n_kern
                art = f"an Nachbar {nid} (gleiche Klasse {klasse})"
            else:
                nid = naechste_id
                naechste_id += 1
                neu = copy.deepcopy(eintrag)
                neu["id"] = nid
                neu["flaeche"] = n_ges
                if "flaeche_kern" in neu:
                    neu["flaeche_kern"] = n_kern
                neu["im_kern"] = True
                neu["zerfall_teil_von"] = sid
                daten["segmente"].append(neu)
                segs[nid] = neu
                karte[stueck] = nid
                art = f"neue ID {nid} (Klasse {klasse})"
            eintrag["flaeche"] = int(eintrag.get("flaeche", 0)) - n_ges
            if "flaeche_kern" in eintrag:
                eintrag["flaeche_kern"] = int(eintrag["flaeche_kern"]) - n_kern
            protokoll.append({"teilkachel": tk, "segment": sid, "teil": i, "kern_px": n_kern,
                              "gesamt_px": n_ges, "nach": art})
    # Prüfen: jede ID der Teilkachel zusammenhängend
    for sid in set(int(x) for x in np.unique(karte)):
        _, n = ndimage.label(karte == sid, structure=VIERER)
        if n != 1:
            protokoll.append({"teilkachel": tk, "segment": sid, "FEHLER": f"{n} Teile nach Behebung"})
    if not probe:
        ziel = sicherung / fassung_dir.name / tk
        ziel.mkdir(parents=True, exist_ok=True)
        if not (ziel / "labels.tif").exists():
            shutil.copy2(lab_p, ziel / "labels.tif")
            shutil.copy2(seg_p, ziel / "segmente.json")
        schreibe_labels(lab_p, karte)
        schreibe_json(seg_p, daten)
    return protokoll


def main():
    h0, sicherung, ausgabe = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    probe = "--probe" in sys.argv
    manifest = lese_json(h0 / "manifest.json")
    tks = {t["id"]: t for t in manifest["teilkacheln"]}
    alles = {}
    for f in FASSUNGEN:
        alles[f] = []
        for tk in sorted(tks):
            alles[f] += bearbeite(h0 / f, tk, tks[tk], sicherung, probe)
        fehler = [p for p in alles[f] if "FEHLER" in p]
        print(f"{f}: {len([p for p in alles[f] if 'FEHLER' not in p])} Teile umgehängt, "
              f"neu {sum(1 for p in alles[f] if str(p.get('nach','')).startswith('neue'))}, "
              f"an Nachbarn {sum(1 for p in alles[f] if str(p.get('nach','')).startswith('an '))}, Fehler {len(fehler)}")
        for p in fehler:
            print("  ", p)
    ausgabe.write_text(json.dumps(alles, ensure_ascii=False, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
