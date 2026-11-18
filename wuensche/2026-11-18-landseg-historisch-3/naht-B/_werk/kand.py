import json, collections
m = json.load(open("mass.json", encoding="utf-8"))
p = collections.defaultdict(list)
for o in m: p[(o["naht"], tuple(o["ids"]))].append(o)
for k, lst in p.items():
    if max(o["L"] for o in lst) <= 3 and min(o["d"] for o in lst) >= 30:
        print(k, [(o["n"], o["L"], o["d"], o["ma"], o["mb"], o["gL"], o["gR"], o["kl"]) for o in lst])
