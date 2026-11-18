import json, sys
from pathlib import Path
import numpy as np
sys.path.insert(0, "C:/Users/Phil/Developement/Victor/landseg")
from landseg import dateien
W = Path("C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3")
D = Path("C:/Users/Phil/Developement/Victor/daten/landseg")
BILD = {"T0": D / "uebergabe/landseg-t0/T0", "H0": D / "H0"}
ORD = {"A": "a-alles-frei", "B": "b-kategorien-frei", "C": "c-feste-liste"}
CODE = {("T0","A"):"4.4",("T0","B"):"2.4",("T0","C"):"3.6",("H0","A"):"4.4",("H0","B"):"5.3",("H0","C"):"3.6"}
for b,p in BILD.items():
    for f,o in ORD.items():
        z = p/o/"zusammen"
        s = {x["id"]:x for x in json.load(open(z/"segmente.json",encoding="utf-8"))["segmente"]}
        lab = dateien.lese_labels(z/"labels.tif")
        ids = [i for i,x in s.items() if x.get("klasse")==CODE[(b,f)]]
        m = np.isin(lab, ids)
        n = json.load(open(z/"naht.json",encoding="utf-8"))
        print(b,f,CODE[(b,f)],"segmente",len(ids),"px",int(m.sum()),"pct",round(100*m.mean(),3),"maengel",len(n["pruefen"]["maengel"]),"verstoesse",len(n["verstoesse"]),"zus_ok",n["pruefen"]["ok"])
