import json, glob, collections, sys
import numpy as np, tifffile
T0 = "C:/Users/Phil/Developement/Victor/daten/landseg/T0"
for fa in ("kern500", "fassung-b"):
    keys = collections.Counter(); skeys = collections.Counter()
    for p in sorted(glob.glob(f"{T0}/{fa}/urteil/*/v*/urteil.json")):
        u = json.load(open(p, encoding="utf-8"))
        keys.update(u.keys())
        for s in u["segmente"]: skeys.update(s.keys())
    print(fa, dict(keys)); print("  seg", dict(skeys))
    u = json.load(open(f"{T0}/{fa}/urteil/r0c1/v2/urteil.json", encoding="utf-8"))
    print(json.dumps(u["segmente"][0], ensure_ascii=False)[:900])
    for k in u:
        if k not in ("segmente", "bilder_angesehen"): print("  ", k, json.dumps(u[k], ensure_ascii=False)[:300])
for t in ("r0c0", "r0c1", "r1c0", "r1c1"):
    k = json.load(open(f"{T0}/fassung-c/abgabe/{t}/kategorien-teil.json", encoding="utf-8"))
    lab = tifffile.imread(f"{T0}/fassung-c/abgabe/{t}/labels.tif")
    s = json.load(open(f"{T0}/fassung-c/abgabe/{t}/segmente.json", encoding="utf-8"))
    used = collections.Counter(x["klasse"] for x in s["segmente"] if x.get("im_kern", True))
    print(t, lab.shape, lab.dtype, "min", lab.min(), "n", len(s["segmente"]), "kern", sum(1 for x in s["segmente"] if x.get("im_kern")), "keys", sorted(k.keys()))
    for c in k["classes"]:
        print(f"   {c['code']:8} L{c.get('level')} {c['name'][:45]:45} n={used.get(c['code'],0)}")
    print("   unbekannt:", set(used) - {c['code'] for c in k['classes']})
