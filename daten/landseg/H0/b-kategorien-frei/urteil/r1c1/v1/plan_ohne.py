import json, sys
p = sys.argv[1]; weg = {int(i) for i in sys.argv[2].split(",")}
d = json.load(open(p, encoding="utf-8"))
d["schritte"] = [s for i, s in enumerate(d["schritte"], 1) if i not in weg]
json.dump(d, open(p, "w", encoding="utf-8")); print(len(d["schritte"]))
