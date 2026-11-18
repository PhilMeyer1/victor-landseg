"""Je Verstoß: Sieht jede Teilkachel in ihrer eigenen Karte (Kern + Kontextrand) an der Kerngrenze
eine Grenze oder dieselbe ID auf beiden Seiten? Ausgabe je ID-Paar."""
import collections
import json
from pathlib import Path

import tifffile

H0 = Path("C:/Users/Phil/Developement/Victor/daten/landseg/H0")
C = H0 / "c-feste-liste"
man = json.load(open(H0 / "manifest.json", encoding="utf-8"))
tk = {t["id"]: t for t in man["teilkacheln"]}
karten = {t: tifffile.imread(C / t / "labels.tif") for t in tk}
seg = {}
for t in tk:
    for e in json.load(open(C / t / "segmente.json", encoding="utf-8"))["segmente"]:
        seg[e["id"]] = e
verst = json.load(open(Path(__file__).parent / "streifen" / "verstoesse.json", encoding="utf-8"))


def lokal(t, x, y):
    k = tk[t]["kontext"]
    return karten[t][y - k["y"], x - k["x"]]


paare = collections.OrderedDict()
for v in verst:
    a_t, b_t = v["naht"].split("|")
    senk = v["von"][0] == v["bis"][0] and tk[a_t]["zeile"] == tk[b_t]["zeile"]
    pos = []
    if senk:
        x = v["von"][0]
        for y in range(v["von"][1], v["bis"][1] + 1):
            pos.append(((x - 1, y), (x, y)))
    else:
        y = v["von"][1]
        for x in range(v["von"][0], v["bis"][0] + 1):
            pos.append(((x, y - 1), (x, y)))
    a_gleich = sum(lokal(a_t, *p) == lokal(a_t, *q) for p, q in pos)
    b_gleich = sum(lokal(b_t, *p) == lokal(b_t, *q) for p, q in pos)
    v["a_sieht_gleich"] = int(a_gleich)
    v["b_sieht_gleich"] = int(b_gleich)
    key = (v["naht"], tuple(v["ids"]))
    paare.setdefault(key, []).append(v)

aus = []
for (naht, ids), vs in paare.items():
    L = sum(v["laenge"] for v in vs)
    ag = sum(v["a_sieht_gleich"] for v in vs)
    bg = sum(v["b_sieht_gleich"] for v in vs)
    a, b = ids
    aus.append({"naht": naht, "ids": list(ids), "n": [v["n"] for v in vs], "laenge": L,
                "a_gleich": ag, "b_gleich": bg,
                "klassen": [seg[a]["klasse"], seg[b]["klasse"]],
                "was": [seg[a].get("was_ist_es", ""), seg[b].get("was_ist_es", "")]})
    print(f"{naht} {a} ({seg[a]['klasse']}) | {b} ({seg[b]['klasse']}): n={[v['n'] for v in vs]} L={L} "
          f"a_sieht_gleich={ag} b_sieht_gleich={bg}")
json.dump(aus, open(Path(__file__).parent / "paare.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(verst, open(Path(__file__).parent / "streifen" / "verstoesse.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=0)
