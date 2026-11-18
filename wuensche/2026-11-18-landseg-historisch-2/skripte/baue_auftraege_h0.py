"""Teil 2 von landseg-historisch: Viertel, Bilder und alle Agent-Aufträge für den Ausschnitt H0.

Aufruf: PY -I baue_auftraege_h0.py <BASIS> <Berichtsordner D>

Nach dem Muster von T0 (wuensche/2026-11-17-landseg-test-t0-1/skripte/baue_viertel.py), mit den
Fassungsnamen aus einstellungen/seite.json (A „Alles frei“, B „Kategorien frei“, C „Feste
Kategorienliste“) und den Entscheidungen 2026-11-17/18 (ein Agent je Teilkachel und Fassung, sieht
zuerst den ganzen Ausschnitt, dann seine Teilkachel, arbeitet ihre vier Viertel-Aufträge nacheinander ab).

Schreibt
- daten/landseg/H0/ganz/H0_raster.jpg (ganzer Ausschnitt mit Teilkachelgitter) und je Teilkachel
  ganz/<tk>/ganz_roh.jpg, ganz_nummern.jpg, ganz.json (Gesamtbild der Teilkachel, Viertel cyan),
- daten/landseg/H0/viertel/<tk>/v<n>/ (Übersicht und vier Nahansichten je Viertel, viertel.json);
  B und C lesen dieselben Bilder (bildpunktgleiche Vorstufe, eine Ablage),
- daten/landseg/H0/a-alles-frei/ansicht/<tk>/ (landseg ansicht --nur-teilkachel, für A),
- leere Ergebnisordner (c-feste-liste/urteil, b-kategorien-frei/urteil, …/vereinheitlichung,
  a-alles-frei/abgabe, c-feste-liste/urteil-gegenprobe, a-alles-frei/abgabe-gegenprobe),
- D/auftraege/<c|b>/<tk>/v<n>/auftrag.md, D/auftraege/a/<tk>/auftrag.md, D/auftraege/b/vereinheitlichen.md,
  D/auftraege/gegenprobe/<c|a>/…/auftrag.md und D/auftraege.json (Plan samt Workflow-Einheiten).
"""
import json
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

BASIS = Path(sys.argv[1])
D = Path(sys.argv[2])
REPO = BASIS / "landseg"
sys.path.insert(0, str(REPO))

import cv2  # noqa: E402
import numpy as np  # noqa: E402
from PIL import Image  # noqa: E402
from scipy import ndimage  # noqa: E402

from landseg import dateien, einstellungen, kategorien  # noqa: E402
from landseg.ansicht import Ansicht, Fenster, grenzen  # noqa: E402

PY = "C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe"
H0 = BASIS / "daten" / "landseg" / "H0"
DA = D / "auftraege"
PRUEFE = D / "skripte" / "pruefe_urteil.py"
ORDNER = {"a": "a-alles-frei", "b": "b-kategorien-frei", "c": "c-feste-liste"}
NAME = {"a": "Fassung A „Alles frei“", "b": "Fassung B „Kategorien frei“", "c": "Fassung C „Feste Kategorienliste“"}
RAND_V, FAKTOR_U = 32, 3       # Übersicht je Viertel: Umgebung, Vergrößerung
RAND_N, FAKTOR_N = 12, 6       # Nahansichten
FAKTOR_G = 2                   # Gesamtbild der Teilkachel
JPEG_Q = 92
GEGEN_TK = "r0c0"              # Gegenprobe: gemischte Teilkachel (Ortsrand und Flur), mittlere Dichte
LAGE = {1: "oben links", 2: "oben rechts", 3: "unten links", 4: "unten rechts"}
ID_BLOCK = int(dateien.lese_json(REPO / "vorstufe.json")["id_block"])
KAT = kategorien.laden(REPO / "kategorien.json")
VORGABEN = einstellungen.laden("ansicht")
CYAN, GELB, WEISS, GRAU = (0, 255, 255), (255, 255, 0), (255, 255, 255), (175, 175, 175)
SCHRIFT = cv2.FONT_HERSHEY_SIMPLEX
KONFIG = D / "vorstufe-h0.json"

SW = f"""## Schwarz-Weiß-Scan (gilt für H0)

H0 ist ein Ausschnitt von 1000 × 1000 Bildpunkten aus einem eingescannten Schwarz-Weiß-Luftbild von
1968 (`daten/luftbilder/historisch/1968105_0014_0228.tif`, x 1500, y 2000): Ortsrand mit Streckhöfen
(lange schmale Häuser in Reihen), Straßen, ein kleiner Anger, Äcker mit Streifenflur. Das Bild hat einen
Kanal; alle Bilder zeigen es als RGB mit drei gleichen Kanälen. Es hat keine Lagedaten (keine
Weltdatei, `georeferenz: null` im Manifest); ein Bildpunkt sind etwa 0,45 m (geschätzt; das farbige Orthofoto hat 0,2 m).

- Farbe gibt es nicht: Urteile nach Grauton, Textur, Form, Schatten und Lage zu den Nachbarn.
- Die SW-Spalte (`bw`) in `kategorien.json` ist eine ungeprüfte Vermutung, kein Beleg.
- Ist eine feine Klasse auf Schwarz-Weiß nicht sicher zu unterscheiden (etwa Acker gegen Grünland,
  Dach gegen Hof, Belag eines Weges), nimm die Klasse der Ebene darüber, setze `sicher: false` und
  schreibe unter `offen`, was im Farbbild entscheiden würde.
- Die Klassen der Vorstufe sind auf dem Scan schwach (SAM 3 ist für Farb-Orthofotos gebaut; über
  90 % `sicher: nein`, Äcker teils als Gebäude): nur Hinweis.
- Die Vorstufe lief mit kleinerem SAM-3-Fenster (420 Bildpunkte, Schiebefenster) und niedriger
  Instanzschwelle (`{KONFIG.as_posix()}`), damit die Streckhöfe einzeln erscheinen. Gerade Grenzen
  mitten in einer gleichförmigen Fläche (etwa bei x 208 oder 420 im Teilkachelbild) können vom
  Schiebefenster stammen: dann ist es keine Bildkante.
"""


def p(x: Path) -> str:
    return x.as_posix()


# -- Viertel ---------------------------------------------------------------------------------

def viertel_rechtecke(k: dict) -> dict:
    x, y, b, h = k["x"], k["y"], k["breite"], k["hoehe"]
    hb, hh = b // 2, h // 2
    return {1: (x, y, hb, hh), 2: (x + hb, y, b - hb, hh), 3: (x, y + hh, hb, h - hh), 4: (x + hb, y + hh, b - hb, h - hh)}


def mit_rand(r, rand: int, faktor: int, form) -> Fenster:
    x, y, b, h = r
    x0, y0 = max(0, x - rand), max(0, y - rand)
    x1, y1 = min(form[1], x + b + rand), min(form[0], y + h + rand)
    return Fenster(x0, y0, x1 - x0, y1 - y0, faktor)


def einteilen(tk: str, labels: np.ndarray, seg: dict, kern: dict, kand: dict) -> dict:
    vr = viertel_rechtecke(kern)
    kern_ids = [s["id"] for s in seg["segmente"] if s.get("im_kern")]
    eintraege = dateien.segmente_nach_id(seg)
    anteil = {sid: {n: 0 for n in vr} for sid in kern_ids}
    fremd = set()
    for n, (x, y, b, h) in vr.items():
        ids, zahl = np.unique(labels[y:y + h, x:x + b], return_counts=True)
        for sid, z in zip(ids.tolist(), zahl.tolist()):
            if sid in anteil:
                anteil[sid][n] = z
            else:
                fremd.add(sid)
    ohne = [sid for sid in kern_ids if not sum(anteil[sid].values())]
    if fremd or ohne:
        raise SystemExit(f"{tk}: Kern passt nicht zu im_kern: fremd {sorted(fremd)}, ohne Kernfläche {ohne}")
    liste = {n: [] for n in vr}
    for sid in kern_ids:
        n = max(vr, key=lambda v: (anteil[sid][v], -v))
        vx, vy, vb, vh = vr[n]
        maske = np.pad(labels[vy:vy + vh, vx:vx + vb] == sid, 1)
        abstand = ndimage.distance_transform_edt(maske)[1:-1, 1:-1]
        py, px = np.unravel_index(int(np.argmax(abstand)), abstand.shape)
        e = eintraege[sid]
        kf = sum(anteil[sid].values())
        liste[n].append({"id": sid, "nr": sid % ID_BLOCK, "klasse": e.get("klasse"),
                         "name": KAT.name(e["klasse"]) if KAT.gueltig(e.get("klasse")) else "?",
                         "sicher": e.get("sicher"), "im_siedlung": e.get("im_siedlung"), "kern_flaeche": kf,
                         "anteil": round(anteil[sid][n] / kf, 3),
                         "auch_in": [f"v{v}" for v in vr if v != n and anteil[sid][v]],
                         "punkt": [int(vx + px), int(vy + py)], "kandidaten": sorted(kand.get(sid, []))})
    for n in liste:
        liste[n].sort(key=lambda s: (s["punkt"][1] // 50, s["punkt"][0], s["id"]))
    return {"rechtecke": vr, "liste": liste, "kern_ids": kern_ids}


# -- Bilder ----------------------------------------------------------------------------------

def rahmen(bild, r, f: Fenster, farbe, dicke=2, versatz=(0, 0)):
    x, y, b, h = r
    x0 = (x - f.x) * f.faktor + versatz[0]
    y0 = (y - f.y) * f.faktor + versatz[1]
    cv2.rectangle(bild, (x0, y0), (x0 + b * f.faktor - 1, y0 + h * f.faktor - 1), farbe, dicke, cv2.LINE_4)


def gross(arr, faktor):
    return np.repeat(np.repeat(arr, faktor, axis=0), faktor, axis=1)


def beschriften(bild, text, px, py, g, farbe):
    cv2.putText(bild, text, (px, py), SCHRIFT, g, (0, 0, 0), 3, cv2.LINE_AA)
    cv2.putText(bild, text, (px, py), SCHRIFT, g, farbe, 1, cv2.LINE_AA)


def nummern(roh, labels, f: Fenster, r_hell, kern: dict, eigene: set, nachbarn: set, groesse: float,
            viertel_rahmen=None, min_px=0):
    teil = labels[f.schnitt()]
    bild = gross(roh[f.schnitt()], f.faktor).astype(np.float32)
    innen = np.zeros(teil.shape, bool)
    x, y, b, h = r_hell
    innen[max(0, y - f.y):y + h - f.y, max(0, x - f.x):x + b - f.x] = True
    bild[~gross(innen, f.faktor)] *= 0.6
    bild = bild.astype(np.uint8)
    bild[grenzen(gross(teil, f.faktor))] = GELB
    rahmen(bild, (kern["x"], kern["y"], kern["breite"], kern["hoehe"]), f, WEISS, 1)
    for r in (viertel_rahmen or [r_hell]):
        rahmen(bild, r, f, CYAN, 2)
    for sid in np.unique(teil).tolist():
        if sid not in eigene and sid not in nachbarn:
            continue
        maske = np.pad(teil == sid, 1)
        if min_px and maske.sum() < min_px:
            continue
        abstand = ndimage.distance_transform_edt(maske)[1:-1, 1:-1]
        yy, xx = np.unravel_index(int(np.argmax(abstand)), abstand.shape)
        text = str(sid % ID_BLOCK)
        g = groesse if sid in eigene else groesse * 0.85
        (tb, th), _ = cv2.getTextSize(text, SCHRIFT, g, 1)
        beschriften(bild, text, int((xx + 0.5) * f.faktor) - tb // 2, int((yy + 0.5) * f.faktor) + th // 2,
                    g, WEISS if sid in eigene else GRAU)
    return bild


def speichern(pfad: Path, bild):
    pfad.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(bild).save(pfad, quality=JPEG_Q)


def viertelbilder(tk, roh, labels, a: Ansicht, kern, ein, ziel_tk: Path) -> dict:
    form = labels.shape
    out = {}
    for n, r in ein["rechtecke"].items():
        ziel = ziel_tk / f"v{n}"
        eigene = {s["id"] for s in ein["liste"][n]}
        nachbarn = set(ein["kern_ids"]) - eigene
        fu = mit_rand(r, RAND_V, FAKTOR_U, form)
        bilder = {}
        speichern(ziel / "uebersicht_nummern.jpg", nummern(roh, labels, fu, r, kern, eigene, nachbarn, 0.5))
        bilder["uebersicht_nummern.jpg"] = fu.als_dict()
        for art in ("roh", "vorschlag", "maengel", "kontrast", "gitter"):
            bild = a.zeichnen(art, fu)
            if art != "roh":
                bild = np.ascontiguousarray(bild)
                rahmen(bild, r, fu, CYAN, 2, (40, 16) if art == "gitter" else (0, 0))
            speichern(ziel / f"uebersicht_{art}.jpg", bild)
            bilder[f"uebersicht_{art}.jpg"] = {**fu.als_dict(), **({"rand_links": 40, "rand_oben": 16} if art == "gitter" else {})}
        for k, rt in viertel_rechtecke(dict(zip(("x", "y", "breite", "hoehe"), r))).items():
            fn = mit_rand(rt, RAND_N, FAKTOR_N, form)
            speichern(ziel / f"nah{k}_roh.jpg", a.zeichnen("roh", fn))
            speichern(ziel / f"nah{k}_nummern.jpg", nummern(roh, labels, fn, r, kern, eigene, nachbarn, 0.6))
            bilder[f"nah{k}_roh.jpg"] = fn.als_dict()
            bilder[f"nah{k}_nummern.jpg"] = fn.als_dict()
        dateien.schreibe_json(ziel / "viertel.json", {
            "schema": "landseg-h0-viertelbilder/1", "teilkachel": tk, "viertel": f"v{n}", "lage": LAGE[n],
            "viertel_im_bild": dict(zip(("x", "y", "breite", "hoehe"), r)), "kern_im_bild": kern,
            "koordinaten": "x_teilkachel = fenster.x + x_bild // faktor (im Gitterbild vorher 40 px links "
                           "und 16 px oben abziehen; im Mängelbild steht die Legende unten)",
            "nummer": f"Nummer im Bild = ID mod {ID_BLOCK}; weiß = Segment dieses Viertels, grau = "
                      "Kernsegment eines Nachbarviertels, ohne Nummer = Kontextrand",
            "bilder": {name: {"fenster": fe} for name, fe in bilder.items()}, "segmente": ein["liste"][n]})
        out[n] = {"ordner": ziel, "bilder": sorted(bilder)}
    return out


def ganzbilder(tk, roh, labels, kern, ein, ziel: Path) -> dict:
    """Gesamtbild der Teilkachel (2fach): Grenzen, Nummern, Kern weiß, Viertel cyan mit v1–v4."""
    form = labels.shape
    f = Fenster(0, 0, form[1], form[0], FAKTOR_G)
    vr = ein["rechtecke"]
    bild = nummern(roh, labels, f, (kern["x"], kern["y"], kern["breite"], kern["hoehe"]), kern,
                   set(ein["kern_ids"]), set(), 0.42, viertel_rahmen=list(vr.values()), min_px=40 * FAKTOR_G ** 2)
    for n, (x, y, b, h) in vr.items():
        beschriften(bild, f"v{n}", x * FAKTOR_G + 10, y * FAKTOR_G + 40, 1.3, CYAN)
    speichern(ziel / "ganz_nummern.jpg", bild)
    speichern(ziel / "ganz_roh.jpg", gross(roh, FAKTOR_G))
    dateien.schreibe_json(ziel / "ganz.json", {"tk": tk, "faktor": FAKTOR_G, "kern_im_bild": kern,
                                              "viertel": {f"v{n}": [x, y, x + b, y + h] for n, (x, y, b, h) in vr.items()}})
    return {"nummern": p(ziel / "ganz_nummern.jpg"), "roh": p(ziel / "ganz_roh.jpg")}


def rasterbild(manifest: dict, ziel: Path) -> str:
    bild = np.asarray(Image.open(H0 / manifest["ausschnitt"]["bild"]).convert("RGB")).copy()
    for t in manifest["teilkacheln"]:
        k = t["kern"]
        cv2.rectangle(bild, (k["x"], k["y"]), (k["x"] + k["breite"] - 1, k["y"] + k["hoehe"] - 1), CYAN, 2)
        beschriften(bild, t["id"], k["x"] + 12, k["y"] + 40, 1.2, CYAN)
    speichern(ziel, bild)
    return p(ziel)


# -- Aufträge --------------------------------------------------------------------------------

VORLAGE = (REPO / "vorlagen" / "urteil.md").read_text(encoding="utf-8")


def ersetze(text: str, alt: str, neu: str) -> str:
    if alt not in text:
        raise SystemExit(f"Vorlage geändert, Stelle fehlt: {alt[:60]!r}")
    return text.replace(alt, neu)


def fuelle(text: str, werte: dict) -> str:
    for k, v in werte.items():
        text = text.replace("{{" + k + "}}", v)
    if "{{" in text:
        i = text.index("{{")
        raise SystemExit(f"Platzhalter übrig: {text[i:i + 30]!r}")
    return text


def tabelle(liste: list) -> str:
    kopf = ("| Nr | ID | Klasse Vorstufe | sicher | im Siedlungsgebiet | Kernfläche px | Anteil hier | auch in | "
            "Punkt x/y | Kandidaten |\n|---|---|---|---|---|---|---|---|---|---|\n")
    return kopf + "\n".join(
        f"| {s['nr']} | {s['id']} | {s['klasse']} {s['name']} | {s['sicher']} | {s['im_siedlung']} | {s['kern_flaeche']} | "
        f"{round(100 * s['anteil'])} % | {', '.join(s['auch_in']) or '–'} | {s['punkt'][0]}/{s['punkt'][1]} | "
        f"{', '.join(s['kandidaten']) or '–'} |" for s in liste)


def viertel_auftrag(fassung, tk, n, ein, bilder: Path, ergebnis: Path, daten: Path, bearbeiter, ganz: dict) -> str:
    """fassung c = feste Liste, b = Kategorien frei; daten = Ordner der Fassung (Vorstufen-Kopie je Teilkachel)."""
    liste = ein["liste"][n]
    ids = [s["id"] for s in liste]
    x, y, b, h = ein["rechtecke"][n]
    je_viertel = ", ".join(f"v{v} {len(ein['liste'][v])}" for v in sorted(ein["liste"]))
    t = VORLAGE
    t = ersetze(t, "# Auftrag: Teilkachel {{TEILKACHEL}} ansehen und über alle Segmente urteilen",
                f"# Auftrag: H0, Teilkachel {{{{TEILKACHEL}}}}, Viertel v{n}: {len(ids)} Segmente im Verbund ansehen "
                f"und einzeln urteilen ({NAME[fassung]})")
    t = ersetze(t, "Du urteilst über jedes\nSegment, das im Kern dieser Teilkachel liegt,",
                f"Du urteilst über jedes\nSegment deines Viertels v{n} (Liste unter „Dein Viertel“),")
    t = ersetze(t, "Jedes Segment mit Bildpunkten im Kern steht genau einmal unter `segmente`, auch die sauberen.",
                "Jedes Segment deiner Liste steht genau einmal unter `segmente`, auch die sauberen, in der "
                "Reihenfolge der Liste. Segmente der Nachbarviertel (graue Nummern) und des Kontextrands (ohne "
                "Nummer) urteilst du in diesem Auftrag nicht; Auffälliges an ihnen nennst du unter `unsicher` mit ID.")
    t = ersetze(t, "- `nah_<id>_<n>.jpg`: Nahbilder der Stellen, die man in der Übersicht nicht beurteilen kann;\n"
                   "  `kontrast_<id>_<n>.jpg` bei blassen Stellen.",
                "- `nah_<n>.jpg`: eigene Nahansichten von Stellen, die man in den vorbereiteten Bildern nicht "
                "beurteilen kann,\n  je ein Teil des Viertels samt Nachbarn (mindestens 64 × 64 Bildpunkte der "
                "Teilkachel, kein freigestelltes\n  Einzelsegment); `kontrast_<n>.jpg` bei blassen Stellen.")
    t = ersetze(t, "je die ganze Teilkachel, Kern umrandet.",
                "je dein Viertel mit Umgebung, Viertel\n  umrandet (Grundlage: die vorbereiteten Übersichtsbilder).")
    t = ersetze(t, '{"teilkachel": "{{TEILKACHEL}}", "bearbeiter": "{{BEARBEITER}}",',
                f'{{"teilkachel": "{{{{TEILKACHEL}}}}", "viertel": "v{n}", "bearbeiter": "{{{{BEARBEITER}}}}",\n'
                f' "bilder_angesehen": {{"uebersicht": ["{p(H0)}/H0.png", "{ganz["nummern"]}", "{p(bilder)}/uebersicht_nummern.jpg", "…"],\n'
                f'                      "nah": ["{p(bilder)}/nah1_nummern.jpg", "{p(ergebnis)}/nah_1.jpg", "…"]}},')
    t = ersetze(t, '"bilder": ["nah_17_1.jpg"]}],',
                f'"bilder": ["{p(bilder)}/uebersicht_nummern.jpg", "{p(bilder)}/nah2_roh.jpg"]}}],')
    t = ersetze(t, "Für die Bilder `ansicht` (W3), für fragliche Grenzen `kante` (W4, hier nur\n"
                   "zum Ansehen der Bildkante), zur Kontrolle `pruefen`.",
                "Die Bilder deines Viertels liegen fertig vor (Abschnitt „Dein Viertel“); `ansicht` (W3) erzeugt "
                "Bilder\nje Segment und ist hier keine Urteilsgrundlage. Für fragliche Grenzen `kante` (W4, hier nur "
                "zum Ansehen\nder Bildkante), zur Kontrolle `pruefen`.")
    if fassung == "b":
        t = ersetze(t, '"unsicher": ["..."], "nicht_geprueft": ["..."]}',
                    '"unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."],\n'
                    ' "klassen_frei": [{"name": "Name", "ebene": "grob|mittel|fein", "eltern": "Name oder null", '
                    '"merkmal": "woran im Bild erkennbar"}]}')
        t = ersetze(t, '"klasse_vorschlag": "Code oder null",',
                    '"klasse_vorschlag": null,\n               "klasse_frei": {"grob": "Name", "mittel": "Name", "fein": "Name"},')
        t = ersetze(t, "- `{{REPO}}/kategorien.json` und `{{REPO}}/KATEGORIEN.md`: die gültigen Klassen und Regeln.",
                    "- `{{REPO}}/kategorien.json` und `{{REPO}}/KATEGORIEN.md`: nur Anregung; in Fassung B benennst "
                    "du die Klassen selbst (Abschnitt „Fassung B“).")
    else:
        t = ersetze(t, '"unsicher": ["..."], "nicht_geprueft": ["..."]}',
                    '"unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."]}')
    kat = f" --kategorien {p(REPO / 'kategorien.json')}" if fassung == "c" else ""
    abschnitt = f"""## Zuerst der ganze Ausschnitt, dann die Teilkachel

Bevor du dein Viertel ansiehst: zuerst den ganzen Ausschnitt H0 (`{p(H0)}/H0.png`, mit Teilkachelgitter
`{p(H0)}/ganz/H0_raster.jpg`; r0c0 oben links, r0c1 oben rechts, r1c0 unten links, r1c1 unten rechts),
dann die ganze Teilkachel `{{{{TEILKACHEL}}}}` (`{ganz["nummern"]}`: Grenzen, Nummern, Viertel cyan v1–v4;
`{ganz["roh"]}` unverändert; beide 2fach). Beide stehen in `bilder_angesehen.uebersicht` vor den Viertelbildern.

{SW}
## Dein Viertel

Viertel v{n} ({LAGE[n]}) des Kerns von `{{{{TEILKACHEL}}}}`: x {x}–{x + b - 1}, y {y}–{y + h - 1} im
Teilkachelbild ({b} × {h} Bildpunkte). Dir gehören die {len(ids)} Segmente der Liste unten: Jedes hat den
größten Teil seiner Kernfläche in diesem Viertel. Die Teilkachel hat {len(ein['kern_ids'])} Kernsegmente
({je_viertel}); die anderen Viertel stehen in eigenen Aufträgen mit eigenem Ergebnisordner. Ein Segment
über einer Viertelgrenze urteilt nur das Viertel mit dem größten Anteil; in den Bildern der Nachbarn ist
es mit grauer Nummer als Umgebung zu sehen.

Urteil im Verbund: Du siehst das Viertel als zusammenhängendes Bild mit Umgebung, arbeitest die Liste der
Reihe nach ab und beurteilst jedes Segment im Zusammenhang mit seinen Nachbarn; eingetragen wird jedes
Segment einzeln (Klasse, `sicher`, `was_ist_es` als Notiz). Bilder freigestellter Einzelsegmente gibt es
nicht, und sie sind keine Urteilsgrundlage.

Bilder des Viertels (fertig, JPEG, in `{p(bilder)}`, Fenster und Vergrößerung je Bild in `viertel.json`):

- Übersicht, das Viertel mit {RAND_V} Bildpunkten Umgebung, {FAKTOR_U}fach: `uebersicht_nummern.jpg`
  (Grenzen gelb, Nummern deiner Segmente weiß, der Nachbarviertel grau, Kontextrand ohne Nummer, Viertel
  cyan, Kern weiß umrandet, außerhalb des Viertels abgedunkelt), `uebersicht_roh.jpg`,
  `uebersicht_vorschlag.jpg` (Klassen der Vorstufe als Code und Farbe), `uebersicht_maengel.jpg`
  (`sicher: nein` und andere Mängel, Legende unten), `uebersicht_kontrast.jpg`, `uebersicht_gitter.jpg`
  (beschriftet in Bildpunkten der Teilkachel).
- Nahansichten, das Viertel in vier Teilen mit {RAND_N} Bildpunkten Umgebung, {FAKTOR_N}fach: `nah1_…` oben
  links, `nah2_…` oben rechts, `nah3_…` unten links, `nah4_…` unten rechts, je `_roh.jpg` und `_nummern.jpg`.
- Koordinaten: `x_teilkachel = fenster.x + x_bild // faktor` (im Gitterbild vorher 40 px links und 16 px
  oben abziehen). Nummer im Bild = ID mod {ID_BLOCK} (die letzten Stellen der ID); in `urteil.json` steht
  immer die volle ID.

Sieh zuerst `uebersicht_nummern.jpg` und `uebersicht_roh.jpg` an, dann die Nahansichten, bei blassen
Stellen `uebersicht_kontrast.jpg`. Unter `bilder_angesehen` stehen alle Bilder, die du angesehen hast
(`uebersicht`: H0, Teilkachel, mindestens `uebersicht_nummern.jpg`; `nah`: vorbereitete und eigene
Nahansichten, absolute Pfade), je Segment unter `bilder` die Bilder, auf denen du es beurteilt hast.

Liste (Reihenfolge der Abarbeitung, zeilenweise von oben links; Punkt = Stelle sicher im Segment, im
Teilkachelbild; Kandidaten aus `{p(daten)}/{tk}/kandidaten.json`, dort mit Grund, in den
Bildern nicht eingezeichnet; Anteil hier = Anteil der Kernfläche in diesem Viertel):

{tabelle(liste)}

`nicht_geprueft` nennt, was du nicht angesehen hast, `offen`, was du nicht entscheiden konntest.

Kontrolle vor der Rückgabe (muss mit `ok` enden):

```
{PY} -I {p(PRUEFE)} --urteil {p(ergebnis)}/urteil.json --segmente {p(daten)}/{tk}/segmente.json --fassung {fassung} --viertel v{n} --ids {",".join(str(i) for i in ids)}{kat}
```
"""
    if fassung == "b":
        abschnitt += """
## Fassung B: Kategorien frei

Dieses Viertel gehört zu Fassung B, einem Vergleichsmuster ohne feste Kategorienliste. Abweichend von
Regel L3 des Skills wählst du die Klassen nicht aus `kategorien.json`, sondern benennst jede Fläche
selbst, gestuft in drei Ebenen unter `klasse_frei`: `grob` (wenige Oberklassen für die ganze
Landschaft), `mittel` und `fein` (so fein, wie im Bild sicher erkennbar: Einzelbaum, schmaler Weg,
kleines Gebäude; sonst wiederholt `fein` die mittlere Ebene). Kurze deutsche Namen, gleiche Dinge
gleich benannt, geordnet nach dem, was in der Draufsicht zu sehen ist. `klasse_heute` ist der Code
der Vorstufe und nur ein Hinweis (auch die Farben in `uebersicht_vorschlag.jpg` folgen der festen
Liste und binden dich nicht); `klasse_vorschlag` bleibt `null`. Unter `klassen_frei` stehen alle
Namen, die du benutzt hast, je mit Ebene, Eltern und einem Satz Bildmerkmal. Nach allen Teilkacheln
gleicht ein eigener Agent die Namen der 16 Viertel zu einer Liste an. Alle übrigen Regeln (L1, L2,
L4–L13) gelten wie in Fassung C; jeder Bildpunkt gehört genau einem Segment.
"""
    t = ersetze(t, "## Werkzeuge", abschnitt + "\n## Werkzeuge")
    return fuelle(t, {"PY": PY, "REPO": p(REPO), "DATEN": p(H0), "TEILKACHEL": tk,
                      "LABELS": f"{daten.name}/{tk}/labels.tif", "SEGMENTE": f"{daten.name}/{tk}/segmente.json",
                      "ERGEBNIS": p(ergebnis), "BEARBEITER": bearbeiter})


def vereinheitlichen_auftrag(viertel_b: list, ergebnis: Path) -> str:
    zeilen = "\n".join(f"| `{e['teilkachel']}` | `v{e['viertel']}` | {len(e['segmente'])} | `{e['ergebnis']}/urteil.json` |"
                       for e in viertel_b)
    return f"""# Auftrag: freie Klassen der 16 Viertel von Fassung B (H0) zu einer Liste vereinheitlichen

Lies zuerst den Skill `landseg-agent` (`{p(REPO)}/.claude/skills/landseg-agent/SKILL.md`); seine Regeln
gelten hier ohne L3. Antworte auf Deutsch.

Gegenstand: Fassung B „Kategorien frei“ des Ausschnitts H0 (Schwarz-Weiß-Scan 1968) in
`{p(H0 / ORDNER['b'])}`. Vier Agents (einer je Teilkachel) haben je vier Viertel beurteilt und die
Flächen dabei selbst benannt (`klasse_frei` je Segment mit `grob`, `mittel`, `fein`; `klassen_frei` je
Viertel mit Ebene, Eltern, Bildmerkmal). Du machst daraus eine einheitliche, gestufte Kategorienliste
für ganz H0 und ordnest jedem Segment ihren Code zu. Du urteilst nicht neu am Bild, änderst keine
Viertel-Abgabe und nicht die Label-Karte.

## Eingaben (nur lesen)

| Teilkachel | Viertel | Segmente | Abgabe |
|---|---|---|---|
{zeilen}

- `{p(REPO)}/kategorien.json`: Format der Liste (nur das Format, nicht die Klassen).
- Bei Zweifeln, ob zwei Namen dasselbe meinen: die Bilder des Viertels unter `{p(H0)}/viertel/<teilkachel>/v<n>/`.

## Ergebnis in `{p(ergebnis)}` (nur dort, genau diese Namen)

- `kategorien-b-entwurf.json` im Format von `kategorien.json`: `{{"schema": "landseg-kategorien/1",
  "title": "…", "date": "JJJJ-MM-TT", "classes": [{{"code": "1", "name": "…", "parent": null, "level": 1,
  "color": "#rrggbb", "image_cue": "woran im Bild erkennbar"}}, …]}}`. Codes gestuft (`1`, `1.2`, `1.2.3`),
  Ebenen 1 bis 3, Ebene 1 höchstens sieben Klassen mit den Codes `0` bis `6` (`0` nur für „nicht
  bestimmbar“, falls gebraucht), jede Klasse mit Eltern auf der Ebene darüber, Farben paarweise gut
  unterscheidbar (CIELAB-Abstand mindestens 10). Gleiche Dinge stehen unter einem Namen, auch wenn die
  Viertel sie verschieden nannten. `image_cue` beschreibt Grauton, Textur und Form (kein Farbbild).
- `codes.json`: `{{"schema": "landseg-h0-codes-b/1", "segmente": {{"<teilkachel>": {{"<id>": {{"code":
  "1.2.3", "viertel": "v1", "klasse_frei": {{"grob": "…", "mittel": "…", "fein": "…"}}}}}}}}, "namen":
  [{{"teilkachel": "r0c0", "viertel": "v1", "ebene": "fein", "name": "Name des Viertels", "code": "1.2.3"}}],
  "offen": [], "nicht_geprueft": []}}`: jedes Segment jeder Viertel-Abgabe genau einmal mit dem Code seiner
  feinsten Ebene, jeder Name jedes Viertels mit seinem Code.
- `vereinheitlichung.md`: welche Namen du zusammengelegt oder getrennt hast und warum, was offen blieb.

Kontrolle der Liste (muss mit `ok` enden): `{PY} -I {p(REPO)}/tools/pruefe_kategorien.py {p(ergebnis)}/kategorien-b-entwurf.json`

Fehlt eine Viertel-Abgabe oder darin ein Segment: nicht nachholen, sondern unter `nicht_geprueft` nennen.

## Rückgabe

Zahl der Klassen je Ebene, Zahl der Segmente mit Code, Zahl der zusammengelegten Namen, was offen blieb.
"""


def frei_auftrag(tk, bilder: Path, ergebnis: Path, schema_seg, ganz: dict, gegenprobe: bool = False) -> str:
    gp = (f"\n## Unabhängig urteilen\n\nDu bist die Gegenprobe: Ein anderer Agent bearbeitet dieselbe Teilkachel "
          f"in `{p(H0 / ORDNER['a'] / 'abgabe' / tk)}`. Sein Ergebnis siehst du nicht an, auch nicht, wenn es schon "
          "da ist. Aus beiden Abgaben wird die Übereinstimmung (PQ, Boundary-PQ) gemessen.\n") if gegenprobe else ""
    return f"""# Auftrag: H0, Teilkachel {tk} frei segmentieren und klassifizieren (Fassung A „Alles frei“)

Antworte auf Deutsch. Diese Abgabe gehört zu Fassung A „Alles frei“, einem Vergleichsmuster: Du wählst
Kategorien und Arbeitsweise selbst, ohne feste Kategorienliste und ohne die Arbeitsregeln des Skills
`landseg-agent` (`{p(REPO)}/.claude/skills/landseg-agent/SKILL.md`; lesen darfst du ihn, er bindet
dich hier nicht). Fest bleiben nur: lückenlos (jeder Bildpunkt der Teilkachel gehört genau einem
Segment, keine 0), eigener Ordner (du schreibst nur in `{p(ergebnis)}`), Eingaben nur lesen.

Ziel: das Landschaftsbild so fein segmentieren, wie im Bild sicher erkennbar (Einzelbaum, schmaler
Weg, einzelnes Haus eines Streckhofs), und jedem Segment eine Klasse aus deiner eigenen, gestuften Liste geben.

Zuerst siehst du den ganzen Ausschnitt H0 an (`{p(H0)}/H0.png`, Gitter `{p(H0)}/ganz/H0_raster.jpg`),
dann deine Teilkachel (`{ganz["roh"]}`, mit Grenzen der Vorstufe `{ganz["nummern"]}`), und nennst beide
in `arbeitsweise.md`.

{SW}{gp}
## Daten (nur lesen)

- `{p(H0)}/manifest.json`: Eintrag `{tk}` unter `teilkacheln` mit `bild`, `kern_im_bild` (Lage des
  Kerns im Teilkachelbild) und `kern`. Maßgeblich ist der Kern; der Kontextrand dient zum Ansehen,
  dort zählt beim Zusammentragen nichts.
- `{p(H0)}/teilkacheln/{tk}.png`: das Bild der Teilkachel (Kern plus Rand, 628 × 628, ein Kanal).
- Vorbelegung der Vorstufe, wahlweise als Ausgang: `{p(H0)}/vorstufe/{tk}/labels.tif`,
  `segmente.json`, `kandidaten.json` (Klassen darin nach der festen Liste, für dich nur Hinweis).
- Bilder der ganzen Teilkachel: `{p(bilder)}/teilkachel/` (`roh`, `kontrast`, `gitter`; `umriss`,
  `maengel`, `vorschlag` zeigen die Vorstufe), Verzeichnis `{p(bilder)}/ansicht.json`.

## Werkzeuge

Alle Werkzeuge von landseg stehen dir frei (`{p(REPO)}/README.md`; Befehle im Ordner `{p(REPO)}` mit
`{PY} -m landseg …`, etwa `ansicht`, `eingriff`, `kante`, `pruefen`). Eigene Skripte als Datei in
`{p(ergebnis)}`, Python nur `{PY}`, nichts installieren, keine Fenster, keine Dauerprozesse.

## Ergebnis in `{p(ergebnis)}`

- `labels.tif`: einkanalig uint32 (über `tifffile`, zlib, wie `landseg.dateien.schreibe_labels`),
  Größe des Teilkachelbilds (628 × 628), kein Bildpunkt 0, jedes Segment zusammenhängend.
- `segmente.json`: `{{"schema": "{schema_seg}", "segmente": [{{"id": 1, "klasse": "Code", "grob": "Code der
  Ebene 1", "name": "kurz", "im_kern": true}}], "verlauf": []}}`, je ID der Karte genau ein Eintrag;
  Codes aus deiner Liste.
- `kategorien-teil.json`: deine Liste im Format von `{p(REPO)}/kategorien.json`:
  `{{"schema": "landseg-kategorien/1", "teilkachel": "{tk}", "classes": [{{"code": "1", "name": "…",
  "parent": null, "level": 1, "color": "#rrggbb", "image_cue": "woran im Bild erkennbar"}}, …]}}`,
  gestufte Codes (`1`, `1.2`, `1.2.3`), so viele Ebenen und Klassen, wie du für richtig hältst.
- `arbeitsweise.md`: wie du gearbeitet hast (Schritte, Werkzeuge, Zahl der Läufe, ungefähre Zeit),
  warum diese Kategorien, was unsicher blieb, welche Klassen auf Schwarz-Weiß nicht zu trennen waren.
- `ergebnis.jpg`: Grenzen und Klassenfarben über dem Bild, Kern umrandet, mit Legende.

Kontrolle (im Ordner `{p(REPO)}`, muss mit `ok` enden):

```
{PY} -m landseg pruefen --labels {p(ergebnis)}/labels.tif --segmente {p(ergebnis)}/segmente.json --bild {p(H0)}/teilkacheln/{tk}.png --kategorien {p(ergebnis)}/kategorien-teil.json
```

## Rückgabe

Zahl der Segmente (davon im Kern), Zahl der Klassen je Ebene, letzte Zeile von `pruefen`, die
Arbeitsweise in zwei Sätzen.
"""


def ansicht_a(tk: str, ziel: Path) -> dict:
    befehl = [PY, "-B", "-m", "landseg", "ansicht", "--manifest", p(H0 / "manifest.json"), "--teilkachel", tk,
              "--labels", p(H0 / "vorstufe" / tk / "labels.tif"), "--segmente", p(H0 / "vorstufe" / tk / "segmente.json"),
              "--ziel", p(ziel), "--nur-teilkachel"]
    t = time.perf_counter()
    r = subprocess.run(befehl, cwd=REPO, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return {"ziel": p(ziel), "rc": r.returncode, "s": round(time.perf_counter() - t, 1),
            "aus": ((r.stdout or "") + (r.stderr or "")).strip()[-400:]}


# -- Ablauf ----------------------------------------------------------------------------------

def je_teilkachel(tk: str, teil: dict) -> dict:
    t = time.perf_counter()
    roh = np.asarray(Image.open(H0 / teil["bild"]).convert("RGB"))   # Graustufen -> RGB mit gleichen Kanälen
    labels = dateien.lese_labels(H0 / "vorstufe" / tk / "labels.tif")
    seg = dateien.lese_segmente(H0 / "vorstufe" / tk / "segmente.json")
    kand = {}
    for k in dateien.lese_json(H0 / "vorstufe" / tk / "kandidaten.json").get("kandidaten", []):
        for sid in k.get("ids", []):
            kand.setdefault(sid, set()).add(k["art"])
    kern = teil["kern_im_bild"]
    ein = einteilen(tk, labels, seg, kern, kand)
    ziel_v = H0 / "viertel" / tk
    if ziel_v.exists():
        shutil.rmtree(ziel_v)
    bilder = viertelbilder(tk, roh, labels, Ansicht(roh, labels, seg, KAT, VORGABEN, kern=kern), kern, ein, ziel_v)
    ganz = ganzbilder(tk, roh, labels, kern, ein, H0 / "ganz" / tk)
    return {"ein": ein, "bilder": bilder, "ganz": ganz, "s": round(time.perf_counter() - t, 1), "schema": seg["schema"]}


def schreibe(pfad: Path, text: str):
    pfad.parent.mkdir(parents=True, exist_ok=True)
    pfad.write_text(text, encoding="utf-8", newline="\n")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    t0 = time.perf_counter()
    manifest = dateien.lese_json(H0 / "manifest.json")
    teile_m = {t["id"]: t for t in manifest["teilkacheln"]}
    tks = list(teile_m)
    raster = rasterbild(manifest, H0 / "ganz" / "H0_raster.jpg")
    with ThreadPoolExecutor(max_workers=len(tks)) as pool:
        erg = dict(zip(tks, pool.map(lambda tk: je_teilkachel(tk, teile_m[tk]), tks)))
    t_bilder = round(time.perf_counter() - t0, 1)
    alle = {}
    for tk in tks:
        for sid in erg[tk]["ein"]["kern_ids"]:
            alle.setdefault(sid, []).append(tk)
    mehrfach = {sid: v for sid, v in alle.items() if len(v) > 1}

    plan = {"schema": "landseg-h0-auftraege/1", "erstellt": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
            "berichtsordner": p(D), "repo": p(REPO), "py": PY, "h0": p(H0), "manifest": p(H0 / "manifest.json"),
            "ganz_ausschnitt": p(H0 / "H0.png"), "ganz_raster": raster,
            "ganz_teilkachel": {tk: erg[tk]["ganz"] for tk in tks},
            "fassungen": {k: {"name": NAME[k], "ordner": p(H0 / v)} for k, v in ORDNER.items()},
            "regel": "Kern jeder Teilkachel in vier Viertel (v1 oben links, v2 oben rechts, v3 unten links, "
                     "v4 unten rechts); jedes Kernsegment gehört dem Viertel mit dem größten Anteil seiner "
                     "Kernfläche (Gleichstand: kleinere Nummer). Ein Agent je Fassung und Teilkachel arbeitet "
                     "die vier Viertel-Aufträge nacheinander ab (Entscheidung 2026-11-17).",
            "viertel": [], "frei_a": [], "vereinheitlichung_b": None, "gegenprobe": [], "gegenprobe_a_alternative": None,
            "einheiten": []}
    for fassung in ("c", "b"):
        daten = H0 / ORDNER[fassung]
        for tk in tks:
            ein = erg[tk]["ein"]
            for n in sorted(ein["liste"]):
                ordner = DA / fassung / tk / f"v{n}"
                bilder = H0 / "viertel" / tk / f"v{n}"
                ergebnis = daten / "urteil" / tk / f"v{n}"
                bearbeiter = f"urt-{fassung}-{tk}-v{n}"
                ergebnis.mkdir(parents=True, exist_ok=True)
                schreibe(ordner / "auftrag.md", viertel_auftrag(fassung, tk, n, ein, bilder, ergebnis, daten, bearbeiter, erg[tk]["ganz"]))
                ids = [s["id"] for s in ein["liste"][n]]
                plan["viertel"].append({"fassung": fassung, "teilkachel": tk, "viertel": n, "segmente": ids,
                                        "auftrag": p(ordner / "auftrag.md"), "ergebnis": p(ergebnis), "bilder": p(bilder),
                                        "bearbeiter": bearbeiter, "modell": "opus", "effort": "hoch"})
                plan["einheiten"].append({"art": fassung, "tk": tk, "v": n, "n": len(ids),
                                          "auftrag": p(ordner / "auftrag.md"), "ergebnis": p(ergebnis)})
    erg_v = H0 / ORDNER["b"] / "vereinheitlichung"
    erg_v.mkdir(parents=True, exist_ok=True)
    viertel_b = [g for g in plan["viertel"] if g["fassung"] == "b"]
    schreibe(DA / "b" / "vereinheitlichen.md", vereinheitlichen_auftrag(viertel_b, erg_v))
    plan["vereinheitlichung_b"] = {"fassung": "b", "auftrag": p(DA / "b" / "vereinheitlichen.md"), "ergebnis": p(erg_v),
                                   "bearbeiter": "verein-b", "nach": [f"{g['teilkachel']}/v{g['viertel']}" for g in viertel_b],
                                   "modell": "opus", "effort": "mittel"}
    jobs = []
    for tk in tks:
        bilder = H0 / ORDNER["a"] / "ansicht" / tk
        ergebnis = H0 / ORDNER["a"] / "abgabe" / tk
        ergebnis.mkdir(parents=True, exist_ok=True)
        schreibe(DA / "a" / tk / "auftrag.md", frei_auftrag(tk, bilder, ergebnis, erg[tk]["schema"], erg[tk]["ganz"]))
        plan["frei_a"].append({"fassung": "a", "teilkachel": tk, "auftrag": p(DA / "a" / tk / "auftrag.md"),
                               "ergebnis": p(ergebnis), "bilder": p(bilder), "bearbeiter": f"frei-a-{tk}",
                               "modell": "opus", "effort": "hoch"})
        plan["einheiten"].append({"art": "a", "tk": tk, "v": 0, "n": len(erg[tk]["ein"]["kern_ids"]),
                                  "auftrag": p(DA / "a" / tk / "auftrag.md"), "ergebnis": p(ergebnis)})
        jobs.append((tk, bilder))
    # Gegenprobe (Standard): Fassung C auf GEGEN_TK wie bei T0 (dort die feste Liste auf r0c0)
    daten_c = H0 / ORDNER["c"]
    ein = erg[GEGEN_TK]["ein"]
    for n in sorted(ein["liste"]):
        ordner = DA / "gegenprobe" / "c" / GEGEN_TK / f"v{n}"
        bilder = H0 / "viertel" / GEGEN_TK / f"v{n}"
        ergebnis = daten_c / "urteil-gegenprobe" / GEGEN_TK / f"v{n}"
        ergebnis.mkdir(parents=True, exist_ok=True)
        text = viertel_auftrag("c", GEGEN_TK, n, ein, bilder, ergebnis, daten_c, f"gegen-c-{GEGEN_TK}-v{n}", erg[GEGEN_TK]["ganz"])
        text = ersetze(text, "\n## Werkzeuge",
                       "\n## Unabhängig urteilen\n\nDu bist die Gegenprobe: Ein anderer Agent urteilt über dasselbe "
                       f"Viertel. Sein Ergebnis (`{p(daten_c)}/urteil/`) siehst du nicht an, auch nicht, wenn es "
                       "schon da ist. Aus beiden Urteilen wird die Übereinstimmung gemessen.\n\n## Werkzeuge")
        schreibe(ordner / "auftrag.md", text)
        ids = [s["id"] for s in ein["liste"][n]]
        plan["gegenprobe"].append({"fassung": "c", "teilkachel": GEGEN_TK, "viertel": n, "segmente": ids,
                                   "auftrag": p(ordner / "auftrag.md"), "ergebnis": p(ergebnis), "bilder": p(bilder),
                                   "bearbeiter": f"gegen-c-{GEGEN_TK}-v{n}", "modell": "opus", "effort": "hoch"})
        plan["einheiten"].append({"art": "z", "tk": GEGEN_TK, "v": n, "n": len(ids),
                                  "auftrag": p(ordner / "auftrag.md"), "ergebnis": p(ergebnis)})
    # Alternative: Gegenprobe auf Fassung A (freie Abgabe), falls „von A“ im Mutterwunsch so gemeint ist
    erg_ga = H0 / ORDNER["a"] / "abgabe-gegenprobe" / GEGEN_TK
    erg_ga.mkdir(parents=True, exist_ok=True)
    schreibe(DA / "gegenprobe" / "a" / GEGEN_TK / "auftrag.md",
             frei_auftrag(GEGEN_TK, H0 / ORDNER["a"] / "ansicht" / GEGEN_TK, erg_ga, erg[GEGEN_TK]["schema"],
                          erg[GEGEN_TK]["ganz"], gegenprobe=True))
    plan["gegenprobe_a_alternative"] = {"fassung": "a", "teilkachel": GEGEN_TK,
                                        "auftrag": p(DA / "gegenprobe" / "a" / GEGEN_TK / "auftrag.md"),
                                        "ergebnis": p(erg_ga), "bearbeiter": f"gegen-a-{GEGEN_TK}",
                                        "einheit": {"art": "z", "tk": GEGEN_TK, "v": 0, "n": len(ein["kern_ids"]),
                                                    "auftrag": p(DA / "gegenprobe" / "a" / GEGEN_TK / "auftrag.md"),
                                                    "ergebnis": p(erg_ga)}}
    t_a = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as pool:
        laeufe_a = list(pool.map(lambda j: ansicht_a(*j), jobs))
    t_a = round(time.perf_counter() - t_a, 1)
    plan["messung"] = {
        "teilkacheln": {tk: {"kernsegmente": len(erg[tk]["ein"]["kern_ids"]),
                             "je_viertel": {f"v{n}": len(v) for n, v in sorted(erg[tk]["ein"]["liste"].items())},
                             "ueber_viertelgrenze": sum(1 for v in erg[tk]["ein"]["liste"].values() for s in v if s["auch_in"]),
                             "bilder_je_viertel": len(next(iter(erg[tk]["bilder"].values()))["bilder"]),
                             "s": erg[tk]["s"]} for tk in tks},
        "kernsegmente_gesamt": len(alle), "kernsegment_in_mehreren_teilkacheln": mehrfach,
        "bilder_wandzeit_s": t_bilder, "ansicht_a_laeufe": len(laeufe_a),
        "ansicht_a_fehler": [x for x in laeufe_a if x["rc"] != 0], "ansicht_a_wandzeit_s": t_a,
        "gesamt_s": round(time.perf_counter() - t0, 1)}
    schreibe(D / "auftraege.json", json.dumps(plan, ensure_ascii=False, indent=1))
    print(json.dumps(plan["messung"], ensure_ascii=False, indent=1))
    zahl = {k: sum(1 for e in plan["einheiten"] if e["art"] == k) for k in "cbaz"}
    print(f"Einheiten: C {zahl['c']}, B {zahl['b']}, A {zahl['a']}, Gegenprobe {zahl['z']} ({GEGEN_TK}); "
          f"Vereinheitlichung B 1; Alternative Gegenprobe A 1")
    return 1 if (plan["messung"]["ansicht_a_fehler"] or mehrfach) else 0


if __name__ == "__main__":
    sys.exit(main())
