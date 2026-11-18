import json, sys
p = "C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde2/auftraege-C/C-07/auftrag.json"
a = json.load(open(p, encoding="utf-8"))
print("codes:", ", ".join(k["code"] + "=" + k["name"] for k in a["klassen"]))
print()
for k, v in a.items():
    if k not in ("klassen", "paare"):
        print(k, ":", json.dumps(v, ensure_ascii=False)[:600])
print()
for i, pa in enumerate(a["paare"], 1):
    print("=== paar", i)
    for k, v in pa.items():
        if k in ("a", "b") or isinstance(v, dict):
            print(" ", k, ":", json.dumps(v, ensure_ascii=False)[:900])
        else:
            print(" ", k, ":", json.dumps(v, ensure_ascii=False)[:300])
