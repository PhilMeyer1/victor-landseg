"""Ergebnisbilder roh/umriss/maengel/vorschlag eines Viertels aus urteil.json und der aktuellen Karte.

Aufruf: PY -B bilder.py --viertel v1 --ordner <ergebnisordner>
"""
import argparse
import json
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
import werkzeug as wz  # noqa: E402

FENSTER = {"v1": (32, 32), "v2": (282, 32), "v3": (32, 282), "v4": (282, 282)}


def legende(canvas, zeilen, titel):
    fn = wz.font(14)
    h = 30 + 19 * len(zeilen)
    neu = Image.new("RGB", (canvas.size[0], canvas.size[1] + h), (255, 255, 255))
    neu.paste(canvas, (0, 0))
    d = ImageDraw.Draw(neu)
    d.text((10, canvas.size[1] + 6), titel, fill=(0, 0, 0), font=wz.font(15))
    for i, z in enumerate(zeilen):
        d.text((10, canvas.size[1] + 28 + 19 * i), z[:150], fill=(0, 0, 0), font=fn)
    return neu


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--viertel", required=True)
    p.add_argument("--ordner", required=True)
    a = p.parse_args()
    sys.stdout.reconfigure(encoding="utf-8")
    ordner = Path(a.ordner)
    urteil = json.loads((ordner / "urteil.json").read_text(encoding="utf-8"))
    karte, bild, seg = wz.lade()
    x0, y0 = FENSTER[a.viertel]
    w = h = 314
    v = wz.VIERTEL[a.viertel]
    f = 3
    c = wz.zeichne(karte, bild, x0, y0, w, h, f, viertel=v, nummern=False, rahmen=False,
                   titel=f"r0c1 {a.viertel}: Bild ohne Grenzen")
    wz.speichere(c, ordner / "roh.jpg")
    c = wz.zeichne(karte, bild, x0, y0, w, h, f, viertel=v, titel=f"r0c1 {a.viertel}: alle Grenzen mit ID (Stand nach Eingriffen)")
    wz.speichere(c, ordner / "umriss.jpg")
    punkte, zeilen = [], []
    n = 0
    for s in urteil["segmente"]:
        for pk in s.get("punkte", []):
            m = re.search(r"(\d+)\s*/\s*(\d+)", pk["text"])
            n += 1
            if m:
                punkte.append((int(m.group(1)), int(m.group(2)), n))
            zeilen.append(f"{n}: {s['id'] % 100000} {pk['art']}: {pk['text']}")
    c = wz.zeichne(karte, bild, x0, y0, w, h, f, viertel=v, punkte=punkte, titel=f"r0c1 {a.viertel}: Mängel")
    if not zeilen:
        zeilen = ["keine Mängel"]
    c = legende(c, zeilen, "Mängel (Nummer: Segment, Art, Stelle x/y im Teilkachelbild)")
    wz.speichere(c, ordner / "maengel.jpg")
    klassen = {}
    geaendert = False
    for s in urteil["segmente"]:
        kv = s.get("klasse_vorschlag")
        klassen[s["id"]] = (kv or s["klasse_heute"]) + ("" if s["sicher"] else "?")
        if kv and kv != s["klasse_heute"]:
            geaendert = True
    geaendert = geaendert or bool(urteil.get("eingriffe"))
    c = wz.zeichne(karte, bild, x0, y0, w, h, f, viertel=v, klassen=klassen,
                   titel=f"r0c1 {a.viertel}: Vorschlag, Grenzen nach Eingriffen, Klasse je Segment (? = unsicher)"
                   + ("" if geaendert else " - unverändert"))
    wz.speichere(c, ordner / "vorschlag.jpg")


if __name__ == "__main__":
    main()
