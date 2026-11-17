"""punkt.py x,y x,y ... -> Segment-ID mod 100000 und Klasse je Punkt"""
import json, sys
import tifffile
B = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/"
lab = tifffile.imread(B + "vorstufe/r1c1/labels.tif")
seg = {s["id"]: s for s in json.load(open(B + "vorstufe/r1c1/segmente.json", encoding="utf-8"))["segmente"]}
for p in sys.argv[1:]:
    x, y = map(int, p.split(","))
    i = int(lab[y, x])
    print(p, i % 100000, seg.get(i, {}).get("klasse"))
