import json, sys
sys.stdout.reconfigure(encoding="utf-8")
A = r"C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde2/auftraege-C/C-05/auftrag.json"
U = r"C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/{}/urteil.json"
a = json.load(open(A, encoding="utf-8"))
print("uebergross", a.get("uebergross"))
urteile = {}
def urteil(tk):
    if tk not in urteile:
        try:
            urteile[tk] = json.load(open(U.format(tk), encoding="utf-8"))
        except Exception as e:
            urteile[tk] = {"_fehler": str(e)}
    return urteile[tk]
def find(u, sid):
    out = []
    def walk(o, path=""):
        if isinstance(o, dict):
            if o.get("id") == sid or o.get("segment") == sid:
                out.append((path, o))
            for k, v in o.items():
                walk(v, path + "/" + k)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, path + f"[{i}]")
    walk(u)
    return out
for i, p in enumerate(a["paare"], 1):
    print("=" * 10, i, p["paar"], p["art"], p.get("bild"))
    print("  strecken", [(s["linie"], s["von"], s["bis"], s["laenge"], s["kante_max"]) for s in p["strecken"]])
    print("  randpunkte", p.get("randpunkte"))
    keys = [k for k in p if k not in ("paar", "art", "strecken", "randpunkte", "bild")]
    for k in keys:
        v = p[k]
        segs = v if isinstance(v, list) else [v]
        for s in segs:
            if isinstance(s, dict):
                s2 = {kk: vv for kk, vv in s.items()}
                print("  ", k, json.dumps(s2, ensure_ascii=False))
                u = urteil(s["teilkachel"])
                for path, o in find(u, s["id"]):
                    print("     URTEIL", path, json.dumps(o, ensure_ascii=False)[:500])
