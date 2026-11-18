"""Fasst Teilen + sofortiges Anfügen der Splitter zu einem Netto-Eingriff zusammen.

Das Werkzeug vergibt freigewordene IDs neu; Splitter-IDs, die sofort wieder verschwanden, würden sonst
später als „neu“ gelten, wenn ein anderes Viertel dieselbe Nummer bekommt.
"""
import json
from pathlib import Path


def netto(pfad):
    prot = json.loads(Path(pfad).read_text(encoding="utf-8"))
    teil = [e for e in prot if e["schritt"] == "teilen"]
    rest = [e for e in prot if e["schritt"] != "teilen"]
    splitter_merges = []
    for t in teil:
        neu = set(t["nachher"]) - set(t["vorher"])
        weg = set()
        for m in rest:
            if m["grund"].startswith("Splitter") and set(m["vorher"]) <= (neu | set(t["vorher"])) and set(m["vorher"]) & neu:
                weg |= set(m["vorher"]) - set(m["nachher"])
                splitter_merges.append(id(m))
        bleib = [i for i in t["nachher"] if i not in weg]
        if weg:
            t["grund"] += f" Splitter des Schnitts ({len(weg)} Stücke, IDs {min(weg)}–{max(weg)}) sofort wieder angefügt."
        t["nachher"] = bleib
    out = []
    for e in prot:
        if e["schritt"] == "teilen" or id(e) not in splitter_merges:
            out.append(e)
    return out
