"""Teil 3 von landseg-test-t0: Viertel-Urteile A und B je Teilkachel zusammenführen und prüfen,
Stand für die Prüfseite schreiben (Label-Karte der Vorstufe unverändert, Klasse aus dem Urteil).

Aufruf: PY -I zusammenfuehren.py   (schreibt nur unter daten/landseg/T0/<kern500|fassung-b>/ und in den Berichtsordner)
"""
import json, re, shutil, sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import tifffile

sys.stdout.reconfigure(encoding="utf-8")
BASIS = Path("C:/Users/Phil/Developement/Victor")
T0 = BASIS / "daten/landseg/T0"
D = BASIS / "wuensche/2026-11-17-landseg-test-t0-3"
GRUPPEN = BASIS / "wuensche/2026-11-17-landseg-test-t0-1/gruppen.json"
REPO = BASIS / "landseg"

FASSUNGEN = {"a": T0 / "kern500", "b": T0 / "fassung-b"}
EINZELBILD = re.compile(r"(?:^|[_/\\-])(?:nah|segment|seg|kontrast)_(\d{5,})(?:[_.])")


def lies(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def schreib(p, daten):
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        json.dump(daten, f, ensure_ascii=False, indent=1)
        f.write("\n")


def codes_der_liste(p):
    return {c["code"]: c for c in lies(p)["classes"]}


def grob(code):
    return code.split(".")[0]


def ja_nein(wert):
    if isinstance(wert, bool):
        return "ja" if wert else "nein"
    return "ja" if str(wert).lower() in ("ja", "true") else "nein"


def main():
    manifest = lies(T0 / "kern500/manifest.json")
    gruppen = lies(GRUPPEN)["gruppen"]
    kat_a = codes_der_liste(REPO / "kategorien.json")
    kat_b = codes_der_liste(T0 / "fassung-b/kategorien-b.json")
    codes_b = lies(T0 / "fassung-b/vereinheitlichung/codes.json")["segmente"]
    befund = {"schema": "landseg-test-t0-teil3-pruefung/1", "fassungen": {}}
    fehler_gesamt = 0

    for fa, ordner in FASSUNGEN.items():
        kat = kat_a if fa == "a" else kat_b
        urteil_klasse = {}        # tk -> id -> code
        staende = {}
        bef_fa = {}
        for t in manifest["teilkacheln"]:
            tk = t["id"]
            fehler, hinweise = [], []
            karte = tifffile.imread(ordner / "vorstufe" / tk / "labels.tif")
            seg = lies(ordner / "vorstufe" / tk / "segmente.json")
            k = t["kern_im_bild"]
            kern = karte[k["y"]:k["y"] + k["hoehe"], k["x"]:k["x"] + k["breite"]]
            kern_ids = {int(i) for i in np.unique(kern)}
            alle_ids = {s["id"] for s in seg["segmente"]}
            soll_viertel = {}
            for g in gruppen:
                if g["fassung"] == fa and g["teilkachel"] == tk:
                    for i in g["segmente"]:
                        soll_viertel[i] = f"v{g['viertel']}"
            eintraege, viertel_info, gesehen = {}, [], Counter()
            naht, unsicher, nicht_geprueft, offen = [], [], [], []
            for n in range(1, 5):
                v = f"v{n}"
                vdir = ordner / "urteil" / tk / v
                u = lies(vdir / "urteil.json")
                ba = u.get("bilder_angesehen") or {}
                ueb, nah = list(ba.get("uebersicht") or []), list(ba.get("nah") or [])
                if not ueb:
                    fehler.append(f"{v}: keine Übersicht unter bilder_angesehen")
                fehlend, einzel = [], []
                bilder_alle = ueb + nah + [b for s in u["segmente"] for b in (s.get("bilder") or [])]
                for b in bilder_alle:
                    pb = Path(b)
                    pb = pb if pb.is_absolute() else vdir / pb
                    if not pb.exists():
                        fehlend.append(b)
                    m = EINZELBILD.search(pb.name)
                    if m and int(m.group(1)) in alle_ids:
                        einzel.append(b)
                if fehlend:
                    fehler.append(f"{v}: {len(set(fehlend))} genannte Bilddateien fehlen: {sorted(set(fehlend))[:5]}")
                if einzel:
                    fehler.append(f"{v}: Bilder mit Segment-ID im Namen (Einzelbild?): {sorted(set(einzel))[:5]}")
                for s in u["segmente"]:
                    i = s["id"]
                    gesehen[i] += 1
                    if i in eintraege:
                        fehler.append(f"Segment {i} in {eintraege[i]['viertel']} und {v}")
                        continue
                    if i not in kern_ids:
                        fehler.append(f"{v}: Segment {i} liegt nicht im Kern (Kontextrand oder unbekannt)")
                    if soll_viertel.get(i) != v:
                        hinweise.append(f"Segment {i}: in {v} geurteilt, laut gruppen.json {soll_viertel.get(i)}")
                    e = dict(s)
                    e["viertel"] = v
                    if fa == "a":
                        e["klasse"] = s.get("klasse_vorschlag") or s.get("klasse_heute")
                    else:
                        c = codes_b.get(tk, {}).get(str(i))
                        e["klasse"] = c["code"] if c else None
                    if e["klasse"] not in kat:
                        fehler.append(f"{v}: Segment {i}: Klasse {e['klasse']!r} nicht in der Liste")
                    eintraege[i] = e
                viertel_info.append({"viertel": v, "bearbeiter": u.get("bearbeiter"), "quelle": str(vdir / "urteil.json").replace("\\", "/"),
                                     "segmente": len(u["segmente"]), "bilder_angesehen": ba,
                                     **({"klassen_frei": u["klassen_frei"]} if "klassen_frei" in u else {})})
                naht += [{**x, "viertel": v} for x in (u.get("naht") or [])]
                unsicher += [f"{v}: {x}" for x in (u.get("unsicher") or [])]
                nicht_geprueft += [f"{v}: {x}" for x in (u.get("nicht_geprueft") or [])]
                offen += [f"{v}: {x}" for x in (u.get("offen") or [])]
            fehlt = sorted(kern_ids - set(eintraege))
            if fehlt:
                fehler.append(f"{len(fehlt)} Kernsegmente ohne Urteil: {fehlt[:10]}")
                nicht_geprueft.append(f"Kernsegmente ohne Urteil: {fehlt}")
            reihen = sorted(eintraege.values(), key=lambda e: (e["viertel"], e["id"]))
            n_nein = sum(1 for e in reihen if not e.get("sicher"))
            n_ns = sum(1 for e in reihen if e.get("urteil") == "nicht_sauber")
            n_wechsel = sum(1 for e in reihen if fa == "a" and e.get("klasse_vorschlag") and e["klasse_vorschlag"] != e["klasse_heute"])
            urteil = {
                "schema": "landseg-urteil-teilkachel/1", "fassung": fa.upper(), "teilkachel": tk,
                "zusammengefuehrt": "mechanisch aus den vier Viertel-Abgaben (Teil 3 landseg-test-t0)",
                "kategorien": str((REPO / "kategorien.json") if fa == "a" else (T0 / "fassung-b/kategorien-b.json")).replace("\\", "/"),
                "klasse_regel": ("klasse = klasse_vorschlag, sonst klasse_heute" if fa == "a"
                                 else "klasse = Code aus fassung-b/vereinheitlichung/codes.json (vereinheitlichte freie Klasse); klasse_frei = Benennung des Viertels"),
                "kernsegmente": len(kern_ids), "eintraege": len(reihen),
                "zahlen": {"nicht_sauber": n_ns, "sicher_nein": n_nein, "klassenwechsel": n_wechsel,
                           "je_viertel": dict(Counter(e["viertel"] for e in reihen))},
                "viertel": viertel_info, "segmente": reihen, "naht": naht, "unsicher": unsicher,
                "nicht_geprueft": nicht_geprueft, "offen": offen,
            }
            schreib(ordner / "urteil" / tk / "urteil.json", urteil)
            urteil_klasse[tk] = {e["id"]: e for e in reihen}
            staende[tk] = (karte, seg, t)
            fehler_gesamt += len(fehler)
            bef_fa[tk] = {"kernsegmente": len(kern_ids), "eintraege": len(reihen), "fehler": fehler,
                          "hinweise": hinweise, "nicht_sauber": n_ns, "sicher_nein": n_nein,
                          "anteil_sicher_nein": round(n_nein / max(1, len(reihen)), 3), "klassenwechsel": n_wechsel,
                          "klassen": len({e["klasse"] for e in reihen}),
                          "je_viertel": urteil["zahlen"]["je_viertel"]}
            print(f"{fa.upper()} {tk}: Kern {len(kern_ids)}, Einträge {len(reihen)}, nicht sauber {n_ns}, "
                  f"sicher nein {n_nein}, Fehler {len(fehler)}, Hinweise {len(hinweise)}")
            for x in fehler[:8]:
                print("   FEHLER", x)

        # Klassenkarte von T0 aus den Kernurteilen, für die Kontextrand-Segmente jeder Teilkachel
        codes = sorted(kat)
        t0 = np.full((1000, 1000), -1, dtype=np.int32)
        for tk, (karte, seg, t) in staende.items():
            k, kk = t["kern_im_bild"], t["kern"]
            kern = karte[k["y"]:k["y"] + k["hoehe"], k["x"]:k["x"] + k["breite"]]
            lut = {i: codes.index(e["klasse"]) for i, e in urteil_klasse[tk].items() if e["klasse"] in kat}
            blk = np.vectorize(lambda i: lut.get(int(i), -1), otypes=[np.int32])(kern)
            t0[kk["y"]:kk["y"] + kk["hoehe"], kk["x"]:kk["x"] + kk["breite"]] = blk
        for tk, (karte, seg, t) in staende.items():
            kx = t["kontext"]
            ys, xs = np.mgrid[0:karte.shape[0], 0:karte.shape[1]]
            ay, ax = ys + kx["y"], xs + kx["x"]
            innen = (ay >= 0) & (ay < 1000) & (ax >= 0) & (ax < 1000)
            klassen_t0 = np.full(karte.shape, -1, dtype=np.int32)
            klassen_t0[innen] = t0[ay[innen], ax[innen]]
            neu = []
            n_kontext_ohne = 0
            for s in seg["segmente"]:
                e2 = dict(s)
                e2["klasse_vorstufe"] = s.get("klasse")
                e2["sicher_vorstufe"] = s.get("sicher")
                u = urteil_klasse[tk].get(s["id"])
                if u:
                    e2["klasse"] = u["klasse"]
                    e2["sicher"] = ja_nein(u.get("sicher"))
                    e2["urteil"] = u.get("urteil")
                    e2["was_ist_es"] = u.get("was_ist_es")
                    e2["viertel"] = u["viertel"]
                    if u.get("punkte"):
                        e2["punkte"] = u["punkte"]
                    if fa == "a":
                        e2["klasse_heute"] = u.get("klasse_heute")
                        e2["klasse_vorschlag"] = u.get("klasse_vorschlag")
                    else:
                        e2["klasse_frei"] = u.get("klasse_frei")
                else:
                    werte = klassen_t0[karte == s["id"]]
                    werte = werte[werte >= 0]
                    if werte.size:
                        e2["klasse"] = codes[Counter(werte.tolist()).most_common(1)[0][0]]
                        e2["herkunft_klasse"] = "Kontextrand: Klasse aus dem Urteil der Nachbarkachel (Mehrheit der Bildpunkte)"
                    else:
                        n_kontext_ohne += 1
                        e2["klasse"] = s.get("klasse") if fa == "a" else "0"
                        e2["herkunft_klasse"] = ("Kontextrand außerhalb T0: Klasse der Vorstufe" if fa == "a"
                                                 else "Kontextrand außerhalb T0: ohne Urteil, 0 Nicht bestimmbar")
                    e2["sicher"] = "nein"
                    e2["urteil"] = "kontextrand"
                e2["grob"] = grob(e2["klasse"])
                neu.append(e2)
            ziel = ordner / "urteil-stand" / tk
            ziel.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ordner / "vorstufe" / tk / "labels.tif", ziel / "labels.tif")
            schreib(ziel / "segmente.json", {**{k2: v2 for k2, v2 in seg.items() if k2 != "segmente"},
                                             "stand": f"Fassung {fa.upper()}, Urteil Runde 0 (Karte der Vorstufe, Klassen aus urteil/{tk}/urteil.json)",
                                             "segmente": neu})
            bef_fa[tk]["kontext_ohne_urteil_ausserhalb_t0"] = n_kontext_ohne
        befund["fassungen"][fa.upper()] = bef_fa
    schreib(D / "pruefung-urteile.json", befund)
    print("Fehler gesamt:", fehler_gesamt)
    return 1 if fehler_gesamt else 0


if __name__ == "__main__":
    sys.exit(main())
