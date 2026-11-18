import json, numpy as np, tifffile, sys
lab = tifffile.imread(r"C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r0c0/labels.tif")
seg = json.load(open(r"C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r0c0/segmente.json", encoding="utf-8"))
print(type(seg), list(seg.keys()) if isinstance(seg, dict) else len(seg))
segs = seg["segmente"] if isinstance(seg, dict) else seg
by = {s["id"]: s for s in segs}
ids = [int(x) for x in sys.argv[1].split(",")]
core = lab[64:564,64:564]
q = lab[64:314,64:314]
u, c = np.unique(q, return_counts=True)
for i in ids:
    n = int((core==i).sum()); nq = int((q==i).sum())
    s = by.get(i)
    print(i, n, nq, s and s.get("klasse"), s and s.get("sicher"), s and s.get("herkunft"))
print("ids im viertel nicht in liste:")
for i,cc in zip(u,c):
    if int(i) not in ids:
        ncore = int((core==i).sum())
        print(int(i), int(cc), ncore, by.get(int(i),{}).get("klasse"), by.get(int(i),{}).get("herkunft"))
for k in seg:
    if k!="segmente": print(k, str(seg[k])[:1500])
