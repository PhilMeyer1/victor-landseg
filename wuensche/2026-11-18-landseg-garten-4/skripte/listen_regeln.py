"""Schritt 1b (landseg-garten-4): Verweise der freien Listen auf die umgezogenen Codes nachziehen.
- Regel G1 `bericht48.im_siedlung_klassen`: Garten im Siedlungsgebiet zählt zur Siedlung (wie AK3 der festen Liste),
  weggefallene Codes durch die Garten-Klasse ersetzt.
- `abbildung_teilkacheln` (Fassung A): Zielcodes über dieselben Wege wie in listen_ordnen.py.
"""
import json, sys
from pathlib import Path
D = Path("C:/Users/Phil/Developement/Victor/daten/landseg")
LISTEN = {
    ("T0", "A"): (D / "uebergabe/landseg-t0/T0/a-alles-frei/kategorien-a.json",
                  {"3.1": "4.4.1", "3.2": "4.4.2", "3.3": "4.4.3", "3": "4.4"}, ["4.4"]),
    ("T0", "B"): (D / "uebergabe/landseg-t0/T0/b-kategorien-frei/kategorien-b.json",
                  {"3.3.1": "2.4.1", "3.3.2": "2.4.2", "3.3": "2.4"}, ["2.2", "2.4"]),
    ("H0", "A"): (D / "H0/a-alles-frei/kategorien-a.json", {"2.2": "4.4.1", "2.3": "4.4.2"}, ["2", "4.4"]),
    ("H0", "B"): (D / "H0/b-kategorien-frei/kategorien-b.json", {"2.2": "5.3"}, ["2", "5.3"]),
}
for (bild, fass), (pfad, wege, siedlung) in LISTEN.items():
    d = json.loads(pfad.read_text(encoding="utf-8"))
    codes = {c["code"] for c in d["classes"]}
    for r in d.get("rules", []):
        if isinstance(r.get("bericht48"), dict):
            alt = r["bericht48"]["im_siedlung_klassen"]
            r["bericht48"]["im_siedlung_klassen"] = siedlung
            if bild == "H0" and fass == "B":
                r["text"] = r["text"].replace("Höfe und Gärten (Klasse 2) zählen", "Höfe (Klasse 2) und Gärten (Klasse 5.3) zählen")
            print(bild, fass, "bericht48", alt, "->", siedlung)
    abb = d.get("abbildung_teilkacheln")
    if isinstance(abb, dict):
        n = 0
        for tk, m in abb.items():
            for k, v in m.items():
                if v in wege:
                    m[k] = wege[v]; n += 1
        print(bild, fass, "abbildung_teilkacheln umgestellt:", n)
        fremd = sorted({v for m in abb.values() for v in m.values() if v not in codes})
        assert not fremd, fremd
    for c in siedlung:
        assert c in codes, c
    pfad.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
