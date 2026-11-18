"""Schritt 1: Klasse Garten in die Kategorienlisten der Fassungen A, B, C von T0 und H0 eintragen.

C (feste Liste): Klasse 3.6 aus landseg/kategorien.json ergänzen (nur sie).
A, B (freie Listen, Regel L14): die eigene Grünland-Klasse der Ebene 1 heißt „Dauergrünland (<alter Name>)“,
darunter eine neue Klasse „Garten“ (nächster freier Code der Ebene 2). Eine schon vorhandene Klasse mit dem
Namen „Garten“ an anderer Stelle wird umbenannt (Code bleibt), damit nur eine Garten-Klasse besteht.
Vorher-Kopien unter <wunsch>/listen-vorher/. Keine Karte, kein Segment wird geändert.
"""
import json
import shutil
import sys
from pathlib import Path

WUNSCH = Path("C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3")
DATEN = Path("C:/Users/Phil/Developement/Victor/daten/landseg")
MASTER = Path("C:/Users/Phil/Developement/Victor/landseg/kategorien.json")
BILDER = {"T0": DATEN / "uebergabe/landseg-t0/T0", "H0": DATEN / "H0"}
ORDNER = {"A": ("a-alles-frei", "a"), "B": ("b-kategorien-frei", "b"), "C": ("c-feste-liste", "c")}

# eigene Grünland-Klasse (Ebene 1) je freier Liste; umzubenennende alte Garten-Klasse
GRUENLAND = {("T0", "A"): "4", ("T0", "B"): "2", ("H0", "A"): "4", ("H0", "B"): "5"}
ALT_GARTEN = {("H0", "B"): ("2.2", "Gartenfläche am Hof (bisher „Garten“)")}

GARTEN_NAME = "Garten (Haus- und Hofgarten: Grünfläche, Beet)"
GARTEN_CUE = "krautige Grünfläche und Beete im Haus- oder Hofgarten, von Gebäude, Zaun oder Hecke eingefasst"


def to_lab(h):
    def lin(c):
        c /= 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(int(h[i:i + 2], 16)) for i in (1, 3, 5))
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    f = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def de(a, b):
    la, lb = to_lab(a), to_lab(b)
    return sum((p - q) ** 2 for p, q in zip(la, lb)) ** 0.5


def farbe_waehlen(vorhanden):
    kandidaten = ["#a6ffaf", "#7cfc9a", "#b8f5a0", "#5fe08a", "#c6ff8f", "#8ef0c8", "#3fbf7f", "#d0ffd8",
                  "#66cc99", "#99ff66", "#2e9e5b", "#b0e57c"]
    for r in range(0, 256, 17):
        for g in range(128, 256, 17):
            for b in range(0, 256, 17):
                kandidaten.append(f"#{r:02x}{g:02x}{b:02x}")
    best = max(kandidaten, key=lambda c: min(de(c, v) for v in vorhanden))
    for c in kandidaten:
        if min(de(c, v) for v in vorhanden) >= 15.0:
            return c
    return best


def naechster_code(klassen, eltern):
    nummern = [int(c["code"].split(".")[1]) for c in klassen
               if c.get("parent") == eltern and c["code"].count(".") == 1]
    return f"{eltern}.{max(nummern, default=0) + 1}"


def main():
    master = json.loads(MASTER.read_text(encoding="utf-8"))
    m36 = next(c for c in master["classes"] if c["code"] == "3.6")
    bericht = []
    for bild, basis in BILDER.items():
        for fass, (ordner, k) in ORDNER.items():
            pfad = basis / ordner / f"kategorien-{k}.json"
            daten = json.loads(pfad.read_text(encoding="utf-8"))
            klassen = daten["classes"]
            sicherung = WUNSCH / "listen-vorher" / bild / ordner / pfad.name
            if not sicherung.exists():
                sicherung.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(pfad, sicherung)
            if fass == "C":
                if any(c["code"] == "3.6" for c in klassen):
                    bericht.append(f"{bild} {fass}: 3.6 schon vorhanden")
                    continue
                pos = max(i for i, c in enumerate(klassen) if c["code"] == "3" or c["code"].startswith("3.")) + 1
                klassen.insert(pos, dict(m36))
                code = "3.6"
            else:
                if any(c.get("name", "").startswith("Garten") and c.get("parent") == GRUENLAND[(bild, fass)]
                       for c in klassen):
                    bericht.append(f"{bild} {fass}: Garten schon vorhanden")
                    continue
                gl = next(c for c in klassen if c["code"] == GRUENLAND[(bild, fass)])
                if not gl["name"].startswith("Dauergrünland"):
                    gl["name"] = f"Dauergrünland ({gl['name']})"
                if (bild, fass) in ALT_GARTEN:
                    ac, an = ALT_GARTEN[(bild, fass)]
                    alt = next(c for c in klassen if c["code"] == ac)
                    alt["name"] = an
                code = naechster_code(klassen, gl["code"])
                neu = {"code": code, "name": GARTEN_NAME, "parent": gl["code"], "level": 2,
                       "color": farbe_waehlen([c["color"] for c in klassen]), "image_cue": GARTEN_CUE,
                       "bw": "eing.", "mappings": {"corine": [], "clc_plus": [], "flair": [], "dkm": [],
                                                   "bericht48": []}}
                pos = max(i for i, c in enumerate(klassen)
                          if c["code"] == gl["code"] or c["code"].startswith(gl["code"] + ".")) + 1
                klassen.insert(pos, neu)
            daten["counts"]["level_2"] += 1
            daten["counts"]["leaves"] += 1
            pfad.write_text(json.dumps(daten, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            bericht.append(f"{bild} {fass}: {pfad} Garten = {code}")
    (WUNSCH / "listen-garten.json").write_text(json.dumps(bericht, ensure_ascii=False, indent=1), encoding="utf-8")
    print("\n".join(bericht))


if __name__ == "__main__":
    sys.exit(main())
