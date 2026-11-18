"""Einstellungen der Vorstufe für H0: vorstufe.json des Repos, nur siedlung.bildpunkt_m auf den Scan gesetzt.

Aufruf: PY -I konfig_h0.py <REPO> <Ziel.json> <bildpunkt_m>
Der Scan hat keine Georeferenz; ohne transform nimmt die Vorstufe siedlung.bildpunkt_m (Standard 0,2 m,
gedacht für das Orthofoto). Der 1968er Scan hat etwa 0,45 m je Bildpunkt (Vorerkundung, Klärung F1).
"""
import json
import sys
from pathlib import Path

repo, ziel, meter = Path(sys.argv[1]), Path(sys.argv[2]), float(sys.argv[3])
konfig = json.loads((repo / "vorstufe.json").read_text(encoding="utf-8"))
alt = konfig["siedlung"]["bildpunkt_m"]
konfig["siedlung"]["bildpunkt_m"] = meter
konfig["_h0"] = (f"Kopie von {(repo / 'vorstufe.json').as_posix()} für den Ausschnitt H0 (Scan 1968 ohne Georeferenz); "
                 f"geändert nur siedlung.bildpunkt_m {alt} -> {meter}")
ziel.write_text(json.dumps(konfig, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
print(f"siedlung.bildpunkt_m {alt} -> {meter}; {ziel.as_posix()}")
