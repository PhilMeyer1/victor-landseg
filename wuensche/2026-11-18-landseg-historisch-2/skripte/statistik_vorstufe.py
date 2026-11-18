"""Kennzahlen einer Vorstufe je Teilkachel: Herkunft, Klassen, große Gebäudesegmente (nur lesen).

Aufruf: PY -I statistik_vorstufe.py <Ordner mit <tk>/segmente.json> [<Ausgabe.json>]
"""
import json
import sys
from collections import Counter
from pathlib import Path

ordner = Path(sys.argv[1])
erg = {}
for tk in ("r0c0", "r0c1", "r1c0", "r1c1"):
    seg = json.loads((ordner / tk / "segmente.json").read_text(encoding="utf-8"))
    alle = seg["segmente"]
    kern = [s for s in alle if s.get("im_kern")]
    herkunft = Counter(s.get("herkunft") for s in kern)
    klassen = Counter(s.get("klasse") for s in kern)
    gebaeude = sorted((s["flaeche"] for s in kern if str(s.get("klasse", "")).startswith("1.1")), reverse=True)
    erg[tk] = {"segmente": len(alle), "im_kern": len(kern), "herkunft_kern": dict(herkunft),
               "sicher_nein_kern": sum(1 for s in kern if s.get("sicher") in ("nein", False)),
               "klassen_kern": dict(klassen.most_common()),
               "gebaeude_kern": len(gebaeude), "gebaeude_groesste_px": gebaeude[:5],
               "gebaeude_ueber_3000px": sum(1 for f in gebaeude if f > 3000),
               "messung": seg.get("vorstufe", {}).get("abdruck") or seg.get("vorstufe", {}).get("einstellungen")}
text = json.dumps(erg, ensure_ascii=False, indent=1)
if len(sys.argv) > 2:
    Path(sys.argv[2]).write_text(text, encoding="utf-8", newline="\n")
for tk, e in erg.items():
    print(tk, "Kern", e["im_kern"], "Herkunft", e["herkunft_kern"], "Gebäude", e["gebaeude_kern"],
          "größte", e["gebaeude_groesste_px"], ">3000px", e["gebaeude_ueber_3000px"])
