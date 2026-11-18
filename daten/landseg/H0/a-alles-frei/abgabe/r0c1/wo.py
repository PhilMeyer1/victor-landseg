"""wo.py x,y x,y ... : Segment (roh) an Punkten"""
import sys, json
import numpy as np
lab = np.load("tmp/labels_roh.npy")
seg = json.load(open("tmp/seg_roh.json", encoding="utf-8"))
for a in sys.argv[1:]:
    x, y = map(int, a.split(","))
    i = int(lab[y, x])
    s = seg[str(i)]
    print(f"({x},{y}) roh {i}: {s['klasse']} A={s['flaeche']} m={s['mittel']} lang={s['lang']} c=({s['cx']:.0f},{s['cy']:.0f})")
