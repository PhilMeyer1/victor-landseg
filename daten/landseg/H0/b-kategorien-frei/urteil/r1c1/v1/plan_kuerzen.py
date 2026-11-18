import json, sys
p = sys.argv[1]; n = int(sys.argv[2])
d = json.load(open(p, encoding="utf-8")); d["schritte"] = d["schritte"][:n]
json.dump(d, open(p, "w", encoding="utf-8")); print(len(d["schritte"]))
