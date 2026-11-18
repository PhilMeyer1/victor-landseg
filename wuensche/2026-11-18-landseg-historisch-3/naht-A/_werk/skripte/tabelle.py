import json, sys
from pathlib import Path

D = Path("C:/Users/Phil/Developement/Victor/daten/landseg/H0/a-alles-frei")
W = Path("C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/naht-A/_werk")
naht = json.load(open(D / "zusammen/naht.json", encoding="utf-8"))
seg = {}
for t in ["r0c0", "r0c1", "r1c0", "r1c1"]:
    for s in json.load(open(D / t / "segmente.json", encoding="utf-8"))["segmente"]:
        seg[s["id"]] = s
kat = json.load(open(D / "kategorien-a.json", encoding="utf-8"))
namen = {}
def walk(n):
    if isinstance(n, list):
        for x in n: walk(x)
    elif isinstance(n, dict):
        if "code" in n: namen[n["code"]] = n.get("name")
        for kk in ("children", "kinder"):
            if kk in n: walk(n[kk])
walk(kat["classes"])
zeilen = []
for i, v in enumerate(naht["verstoesse"], 1):
    a, b = v["ids"]
    sa, sb = seg[a], seg[b]
    z = dict(n=i, naht=v["naht"], ids=v["ids"], laenge=v["laenge"], von=v["von"], bis=v["bis"],
             kante=v["kante_max"], ka=sa["klasse"], kb=sb["klasse"],
             na=sa.get("name", ""), nb=sb.get("name", ""))
    zeilen.append(z)
json.dump(zeilen, open(W / "tabelle.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
with open(W / "tabelle.txt", "w", encoding="utf-8") as f:
    for z in zeilen:
        f.write(f"{z['n']:3d} {z['naht']} {z['ids'][0]}|{z['ids'][1]} L{z['laenge']:3d} {z['von']}-{z['bis']} k{z['kante']:.0f} "
                f"{z['ka']}({z['na'][:28]}) | {z['kb']}({z['nb'][:28]})\n")
