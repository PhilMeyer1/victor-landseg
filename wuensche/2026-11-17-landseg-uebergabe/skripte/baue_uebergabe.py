"""Stellt die Ergebnisse von T0 im Übergabe-Projekt zusammen (kopiert, benennt um, zeichnet Gesamtbilder).

Aufruf: PY -I baue_uebergabe.py <projekt> <protokoll.json>
Liest nur aus daten/landseg/T0 (Quellen bleiben unverändert), schreibt nur unter <projekt>/T0.
"""
import json
import re
import shutil
import sys
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image

Q = Path("C:/Users/Phil/Developement/Victor/daten/landseg/T0")
KAT_REPO = "C:/Users/Phil/Developement/Victor/landseg/kategorien.json"
P = Path(sys.argv[1])
ZIEL = P / "T0"
PROTOKOLL = Path(sys.argv[2])
TK = ["r0c0", "r0c1", "r1c0", "r1c1"]
NEU = {"A": "a-alles-frei", "B": "b-kategorien-frei", "C": "c-feste-liste"}
zaehler: dict[str, dict[str, int]] = {}

# Reihenfolge zählt: erst die längeren, genaueren Muster, Platzhalter verhindern doppelten Tausch A <-> C
ERSETZE = [
    (KAT_REPO, "@CKAT@"),
    ("C:/Users/Phil/Developement/Victor/daten/landseg/T0/", ""),
    ("daten/landseg/T0/", ""),
    ("kern500/urteil-stand/", "@C@/"), ("fassung-b/urteil-stand/", "@B@/"), ("fassung-c/stand/", "@A@/"),
    ("kern500/urteil-stand", "@C@"), ("fassung-b/urteil-stand", "@B@"), ("fassung-c/stand", "@A@"),
    *[(f"{x}/{d}", d) for x in ("kern500", "fassung-b", "fassung-c") for d in ("T0.png", "teilkacheln/", "manifest.json")],
    ("kern500/ganz/", "ganz/"),
    ("fassung-c/kategorien-c.json", "@A@/kategorien-a.json"),
    ("fassung-b/kategorien-b.json", "@B@/kategorien-b.json"),
    ("kern500/", "@C@/"), ("fassung-b/", "@B@/"), ("fassung-c/", "@A@/"), ("fassung-c-", "@A@-"),
    ("kern500", "@C@"), ("fassung-b", "@B@"), ("fassung-c", "@A@"),
    ("kategorien-c.json", "kategorien-a.json"),
    ("Fassung A", "Fassung @c@"), ("Fassung C", "Fassung @a@"), ("urt-a-", "urt-c-"),
    ("@CKAT@", "c-feste-liste/kategorien-c.json"),
    ("@A@", NEU["A"]), ("@B@", NEU["B"]), ("@C@", NEU["C"]), ("@a@", "A"), ("@c@", "C"),
]
TAUSCH = {"A": "C", "C": "A", "B": "B"}


def text_umbenennen(s: str, datei: str) -> str:
    alt = s
    if "C:\\Users" in s:
        s = s.replace("\\", "/")
    for a, b in ERSETZE:
        if a in s:
            s = s.replace(a, b)
    if s != alt:
        zaehler.setdefault(datei, {}).setdefault("texte", 0)
        zaehler[datei]["texte"] += 1
    return s


def json_umbenennen(x, datei: str):
    if isinstance(x, dict):
        neu = {}
        for k, v in x.items():
            if k == "fassung" and isinstance(v, str) and v in TAUSCH:
                if TAUSCH[v] != v:
                    zaehler.setdefault(datei, {}).setdefault("fassung", 0)
                    zaehler[datei]["fassung"] += 1
                neu[k] = TAUSCH[v]
            else:
                neu[k] = json_umbenennen(v, datei)
        return neu
    if isinstance(x, list):
        return [json_umbenennen(v, datei) for v in x]
    if isinstance(x, str):
        return text_umbenennen(x, datei)
    return x


def kopiere(quelle: Path, ziel: Path, umbenennen: bool = True):
    ziel.parent.mkdir(parents=True, exist_ok=True)
    name = str(ziel.relative_to(P)).replace("\\", "/")
    if quelle.suffix == ".json" and umbenennen:
        daten = json_umbenennen(json.loads(quelle.read_text(encoding="utf-8")), name)
        ziel.write_text(json.dumps(daten, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    elif quelle.suffix == ".md" and umbenennen:
        zeilen = [text_umbenennen(z, name) for z in quelle.read_text(encoding="utf-8").splitlines()]
        ziel.write_text("\n".join(zeilen) + "\n", encoding="utf-8", newline="\n")
    else:
        shutil.copyfile(quelle, ziel)


def main():
    if ZIEL.exists():
        shutil.rmtree(ZIEL)
    k = Q / "kern500"
    # Ausschnitt, Teilkacheln, Manifest (Original des Orthofotos wird nicht mitgeliefert)
    for d in ("T0.png", "T0.pgw"):
        kopiere(k / d, ZIEL / d)
    for t in TK:
        for e in (".png", ".pgw"):
            kopiere(k / "teilkacheln" / f"{t}{e}", ZIEL / "teilkacheln" / f"{t}{e}")
        for d in ("ganz_roh.jpg", "ganz_nummern.jpg", "ganz.json"):
            kopiere(k / "ganz" / t / d, ZIEL / "ganz" / t / d)
    m = json.loads((k / "manifest.json").read_text(encoding="utf-8"))
    m["quelle"]["bild"] = Path(m["quelle"]["bild"]).name
    m["quelle"]["hinweis"] = "Originalbild der Lieferung nicht mitgeliefert (nur der Ausschnitt T0.png und die Teilkacheln)"
    (ZIEL / "manifest.json").write_text(json.dumps(m, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")

    # A Alles frei (bisher C): Karte je Teilkachel, zusammengetragene Karte, Liste, Arbeitsweise je Agent
    a = ZIEL / NEU["A"]
    for t in TK:
        for d in ("labels.tif", "segmente.json"):
            kopiere(Q / "fassung-c" / "stand" / t / d, a / t / d)
        for d in ("arbeitsweise.md", "kategorien-teil.json"):
            kopiere(Q / "fassung-c" / "abgabe" / t / d, a / "abgabe" / t / d)
    for d in ("labels.tif", "segmente.json", "naht.json"):
        kopiere(Q / "fassung-c" / "zusammen" / d, a / "zusammen" / d)
    kopiere(Q / "fassung-c" / "kategorien-c.json", a / "kategorien-a.json")
    auftrag = {"schema": "landseg-zusammentragen/1", "manifest": "../manifest.json",
               "einheiten": [{"teilkachel": t, "labels": f"{t}/labels.tif", "segmente": f"{t}/segmente.json",
                              "runde": 0, "name": f"a-{t}"} for t in TK],
               "ziel": "zusammen"}
    (a / "zusammentragen.json").write_text(json.dumps(auftrag, ensure_ascii=False, indent=1) + "\n",
                                           encoding="utf-8", newline="\n")

    # B Kategorien frei: Karte (Grenzen der Vorstufe, Klassen aus dem Urteil), Liste, Urteile
    b = ZIEL / NEU["B"]
    for t in TK:
        for d in ("labels.tif", "segmente.json"):
            kopiere(Q / "fassung-b" / "urteil-stand" / t / d, b / t / d)
        kopiere(Q / "fassung-b" / "urteil" / t / "urteil.json", b / "urteil" / t / "urteil.json")
    kopiere(Q / "fassung-b" / "kategorien-b.json", b / "kategorien-b.json")

    # C Feste Kategorienliste (bisher A): Karte, Urteile, Liste = kategorien.json des Repos
    c = ZIEL / NEU["C"]
    for t in TK:
        for d in ("labels.tif", "segmente.json"):
            kopiere(Q / "kern500" / "urteil-stand" / t / d, c / t / d)
        kopiere(Q / "kern500" / "urteil" / t / "urteil.json", c / "urteil" / t / "urteil.json")
    kopiere(P / "kategorien.json", c / "kategorien-c.json", umbenennen=False)

    gesamtbilder(m)
    PROTOKOLL.write_text(json.dumps({"umbenannt": zaehler}, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Dateien mit Umbenennungen:", len(zaehler))


def gesamtbilder(m: dict):
    """Je Fassung ein Bild von ganz T0 in den Farben der feinsten Klasse, allein und über dem Luftbild."""
    foto = np.asarray(Image.open(ZIEL / "T0.png").convert("RGB")).astype(np.float32)
    h, w = m["ausschnitt"]["hoehe"], m["ausschnitt"]["breite"]
    listen = {"A": ZIEL / NEU["A"] / "kategorien-a.json", "B": ZIEL / NEU["B"] / "kategorien-b.json",
              "C": ZIEL / NEU["C"] / "kategorien-c.json"}
    aus = ZIEL / "gesamtbilder"
    aus.mkdir(parents=True, exist_ok=True)
    for f, ordner in NEU.items():
        farben = {k["code"]: k["color"] for k in json.loads(listen[f].read_text(encoding="utf-8"))["classes"]}
        karte = np.zeros((h, w), np.uint32)
        klasse = {}
        for t in m["teilkacheln"]:
            lab = tifffile.imread(ZIEL / ordner / t["id"] / "labels.tif")
            ki, kk = t["kern_im_bild"], t["kern"]
            karte[kk["y"]:kk["y"] + kk["hoehe"], kk["x"]:kk["x"] + kk["breite"]] = \
                lab[ki["y"]:ki["y"] + ki["hoehe"], ki["x"]:ki["x"] + ki["breite"]]
            for s in json.loads((ZIEL / ordner / t["id"] / "segmente.json").read_text(encoding="utf-8"))["segmente"]:
                klasse.setdefault(s["id"], s.get("klasse"))
        if f == "A":  # die zusammengetragene Karte ist dieselbe Karte, mit eindeutigen IDs
            assert (tifffile.imread(ZIEL / ordner / "zusammen" / "labels.tif") == karte).all()
        ids, inv = np.unique(karte, return_inverse=True)
        tabelle = np.zeros((len(ids), 3), np.float32)
        for i, sid in enumerate(ids):
            hexw = farben.get(klasse.get(int(sid)), "#ff00ff").lstrip("#")[:6]
            tabelle[i] = [int(hexw[j:j + 2], 16) for j in (0, 2, 4)]
        rgb = tabelle[inv.reshape(h, w)]
        rand = np.zeros((h, w), bool)
        rand[:, 1:] |= karte[:, 1:] != karte[:, :-1]
        rand[1:, :] |= karte[1:, :] != karte[:-1, :]
        Image.fromarray(rgb.astype(np.uint8)).save(aus / f"{ordner}-klassen.png", optimize=True)
        ueber = 0.55 * rgb + 0.45 * foto
        ueber[rand] = 255
        Image.fromarray(ueber.clip(0, 255).astype(np.uint8)).save(aus / f"{ordner}-ueber-luftbild.png",
                                                                  optimize=True)
        print(f, ordner, "Segmente im Kern:", len(ids), "ohne Farbe:",
              sum(1 for s in ids if klasse.get(int(s)) not in farben))


if __name__ == "__main__":
    main()
