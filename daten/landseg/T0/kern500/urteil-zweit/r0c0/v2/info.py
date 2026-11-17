import json, sys
k = json.load(open(r"C:/Users/Phil/Developement/Victor/landseg/kategorien.json", encoding="utf-8"))
items = k if isinstance(k, list) else (k.get("kategorien") or k.get("classes") or k)
if isinstance(items, dict):
    print(list(items.keys()))
    for key, v in items.items():
        if isinstance(v, list):
            items = v
            break
for c in items:
    print(c.get("code"), "|", c.get("name"), "|", c.get("image_cue"))
v = json.load(open(r"C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/viertel/r0c0/v2/viertel.json", encoding="utf-8"))
for key, val in v.items():
    if key in ("segmente",):
        continue
    s = json.dumps(val, ensure_ascii=False)
    print(key, ":", s[:600])
