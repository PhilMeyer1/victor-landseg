import json, sys
sys.stdout.reconfigure(encoding="utf-8")
A = "C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde1/auftraege-B/B-04/auftrag.json"
d = json.load(open(A, encoding="utf-8"))
print(sorted(d["paare"][0]["segmente"][0].keys()))
for p in d["paare"]:
    print("=====", p["nr"], p["paar"], p["art"], p["strecken"])
    for s in p["segmente"]:
        kurz = {k: v for k, v in s.items() if k not in ("bbox", "kontur", "maske")}
        print("   ", json.dumps(kurz, ensure_ascii=False))
