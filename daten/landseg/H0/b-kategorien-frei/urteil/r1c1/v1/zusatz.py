import json, sys
p = sys.argv[1]
d = json.load(open(p, encoding="utf-8"))
for paar in sys.argv[2:]:
    ziel, frag = (int(v) for v in paar.split(":"))
    d["schritte"].append({"art": "roh", "schritt": {"op": "verschmelzen", "ids": [ziel, frag], "ziel": ziel}})
json.dump(d, open(p, "w", encoding="utf-8"))
print(len(d["schritte"]))
