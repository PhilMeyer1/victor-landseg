import json, sys
sys.stdout.reconfigure(encoding="utf-8")
A = "C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde2/auftraege-C/C-03/auftrag.json"
d = json.load(open(A, encoding="utf-8"))
seen = {}
for i, p in enumerate(d["paare"], 1):
    print(i, p["paar"], p["art"], json.dumps(p["strecken"]))
    for s in p["segmente"]:
        seen[s["segment"]] = s
print()
for k, s in seen.items():
    print("=" * 60)
    print(k)
    for kk, v in s.items():
        if kk in ("segment",):
            continue
        print("  ", kk, ":", json.dumps(v, ensure_ascii=False))
