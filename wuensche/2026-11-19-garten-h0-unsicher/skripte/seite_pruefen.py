"""Beleg AK3 aus den Daten der Seite: je Fassung von H0 die Segmente mit Garten (samt Unterklassen),
davon unsicher, und ob alle 65 unklaren Kandidaten aus garten-3 dort als Garten und unsicher stehen.
Aufruf: python seite_pruefen.py <seite.html>"""
import json, sys
from pathlib import Path

G3 = Path("C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten")
CODE = {"A": "4.4", "B": "5.3", "C": "3.6"}

t = Path(sys.argv[1]).read_text(encoding="utf-8")
a = t.index("window.DATEN = ") + len("window.DATEN = ")
e = t.index("</script>", a)
daten = json.loads(t[a:e].rstrip().rstrip(";"))

unklar = {}
for ein in G3.glob("H0-*"):
    kd = json.loads((ein / "kandidaten.json").read_text(encoding="utf-8"))
    for i, v in json.loads((ein / "entscheid.json").read_text(encoding="utf-8")).items():
        if v["garten"] == "unklar":
            unklar.setdefault(kd["fassung"], set()).add((kd["teilkachel"], int(i)))


def segmente(fassung):
    """Segmente je Teilkachel, in beliebiger Tiefe der Fassung gesucht: {(tk, id): eintrag}."""
    gefunden = {}
    def suche(o, tk=None):
        if isinstance(o, dict):
            tk = o.get("id") if isinstance(o.get("id"), str) and o.get("id", "").startswith("r") else tk
            for k, v in o.items():
                if k == "segmente" and isinstance(v, list):
                    for s in v:
                        if isinstance(s, dict) and "klasse" in s:
                            gefunden[(tk, int(s["id"]))] = s
                else:
                    suche(v, k if len(k) == 4 and k[0] == "r" and k[2] == "c" else tk)
        elif isinstance(o, list):
            for v in o:
                suche(v, tk)
    suche(fassung)
    return gefunden


for bild in daten["bilder"]:
    if bild.get("kennung") != "H0":
        continue
    for f in bild["fassungen"]:
        k = f.get("kennung")
        s = segmente(f)
        garten = {key: x for key, x in s.items() if str(x.get("klasse")) == CODE[k] or str(x.get("klasse")).startswith(CODE[k] + ".")}
        uns = [x for x in garten.values() if x.get("sicher") in ("nein", False)]
        fehlt = [key for key in unklar.get(k, ()) if key not in garten or garten[key].get("sicher") not in ("nein", False)]
        beispiel = next((x for key, x in garten.items() if key in unklar.get(k, ())), {})
        print(f"H0 {k}: Segmente in der Seite {len(s)}, Garten {len(garten)}, davon unsicher {len(uns)}; "
              f"unklare Kandidaten {len(unklar.get(k, ()))}, nicht als unsicherer Garten in der Seite {len(fehlt)} {fehlt[:5]}; "
              f"Beispiel {json.dumps({x: beispiel.get(x) for x in ('id', 'klasse', 'sicher', 'grund')}, ensure_ascii=False)}")
