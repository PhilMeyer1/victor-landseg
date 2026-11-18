"""Urteile je Segment-ID (aktueller Lauf) als Punkt-Korrekturen in korrekturen.json eintragen.

Zeilen in einer Datei: "ids = klasse : s|u : Name [: Grund]"  (s = sicher, u = unsicher)
Aufruf: urteil.py datei.txt
"""
import json
import sys
from pathlib import Path

HIER = Path(__file__).resolve().parent
punkte = json.loads((HIER / "punkte.json").read_text(encoding="utf-8"))
kor_p = HIER / "korrekturen.json"
kor = json.loads(kor_p.read_text(encoding="utf-8"))
n = 0
for zeile in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines():
    zeile = zeile.strip()
    if not zeile or zeile.startswith("#"):
        continue
    ids, rest = zeile.split("=", 1)
    teile = [t.strip() for t in rest.split(":")]
    klasse, s, name = teile[0], teile[1], teile[2]
    grund = teile[3] if len(teile) > 3 else ""
    pts = []
    for i in ids.split(","):
        i = i.strip()
        if i not in punkte:
            raise SystemExit(f"ID {i} ohne Punkt (Prüfbild für den Ausschnitt erzeugen)")
        pts.append(punkte[i])
    kor["klassen"].append({"punkte": pts, "klasse": klasse, "sicher": s == "s", "name": name, "grund": grund,
                           "ids_lauf": ids.strip()})
    n += len(pts)
kor_p.write_text(json.dumps(kor, ensure_ascii=False, indent=1), encoding="utf-8")
print("eingetragen:", n)
