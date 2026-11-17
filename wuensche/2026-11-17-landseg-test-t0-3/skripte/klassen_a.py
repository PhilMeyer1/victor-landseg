import json, sys
from collections import Counter, defaultdict
sys.stdout.reconfigure(encoding="utf-8")
T = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/"
kat = {c["code"]: c["name"] for c in json.load(open("C:/Users/Phil/Developement/Victor/landseg/kategorien.json", encoding="utf-8"))["classes"]}
z = defaultdict(lambda: [0, 0, 0, 0])
pk = Counter()
for tk in ("r0c0", "r0c1", "r1c0", "r1c1"):
    u = json.load(open(f"{T}kern500/urteil/{tk}/urteil.json", encoding="utf-8"))
    for s in u["segmente"]:
        r = z[s["klasse"]]; r[0] += 1; r[1] += (not s["sicher"]); r[2] += bool(s.get("klasse_vorschlag") and s["klasse_vorschlag"] != s["klasse_heute"]); r[3] += (s["urteil"] == "nicht_sauber")
        for p in s.get("punkte") or []: pk[p.get("art")] += 1
out = ["| Klasse | Name | Segmente | davon unsicher | Klasse geändert | nicht sauber |", "|---|---|---|---|---|---|"]
for c in sorted(z, key=lambda c: [int(x) for x in c.split(".")]):
    out.append(f"| {c} | {kat.get(c)} | {z[c][0]} | {z[c][1]} | {z[c][2]} | {z[c][3]} |")
out.append(""); out.append("Punkte nach Art: " + ", ".join(f"{k} {v}" for k, v in pk.most_common()))
open("C:/Users/Phil/Developement/Victor/wuensche/2026-11-17-landseg-test-t0-3/klassen-a.md", "w", encoding="utf-8").write("# Fassung A: Urteil je Klasse (Runde 0)\n\n" + "\n".join(out) + "\n")
print(len(z), "Klassen;", "\n".join(out[-1:]))
