import json, sys, os
sys.stdout.reconfigure(encoding="utf-8")
p = "C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde2/auftraege-C/C-07/auftrag.json"
a = json.load(open(p, encoding="utf-8"))
seen = {}
for pa in a["paare"]:
    for s in pa["segmente"]:
        seen[s["segment"]] = s
for k, s in seen.items():
    d = {kk: vv for kk, vv in s.items() if kk not in ("segment", "teilkachel", "id")}
    print(k, json.dumps(d, ensure_ascii=False)[:1500])
    print()
# Urteile
base = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil"
for tk in sorted({s["teilkachel"] for s in seen.values()}):
    f = os.path.join(base, tk, "urteil.json")
    u = json.load(open(f, encoding="utf-8"))
    print("== urteil", tk, "keys:", list(u.keys()))
    segs = u.get("segmente") or u.get("urteile") or []
    if isinstance(segs, dict):
        segs = [dict(id=k, **v) for k, v in segs.items()]
    ids = {s2["id"] for s2 in seen.values() if s2["teilkachel"] == tk}
    for e in segs:
        if e.get("id") in ids or str(e.get("id")) in {str(i) for i in ids}:
            print("  ", json.dumps(e, ensure_ascii=False)[:800])
    for kk in ("naht", "offen", "hinweise", "notizen"):
        if kk in u:
            print("  ", kk, json.dumps(u[kk], ensure_ascii=False)[:1500])
