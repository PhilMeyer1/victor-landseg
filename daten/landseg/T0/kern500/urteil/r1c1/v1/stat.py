"""Kennzahlen je Segment des Viertels: Fläche im Kern, Rahmen, Teile, Kernrand, Nachbarn."""
import json
import numpy as np
import tifffile
from scipy import ndimage

BASIS = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500"
lab = tifffile.imread(BASIS + "/vorstufe/r1c1/labels.tif").astype(np.int64)
seg = {s["id"]: s for s in json.load(open(BASIS + "/vorstufe/r1c1/segmente.json", encoding="utf-8"))["segmente"]}
ids = [400017,400018,400011,400001,400026,400033,400031,400040,400036,400037,400035,400045,400049,400059,400077,400055,400081,400046,400044,400060,400063,400047,400083,400061,400054,400052,400097,400098,400087,400094,400078,400090,400121,400103,400104,400116,400089,400109,400119,400102,400088,400125,400120,400127]
kern = lab[64:564, 64:564]
for i in ids:
    m = lab == i
    mk = kern == i
    ys, xs = np.nonzero(m)
    _, n = ndimage.label(m)
    _, nk = ndimage.label(mk)
    dil = ndimage.binary_dilation(m) & ~m
    nb, cnt = np.unique(lab[dil], return_counts=True)
    order = np.argsort(-cnt)[:6]
    nbs = ", ".join(f"{nb[k] % 100000}:{seg.get(nb[k], {}).get('klasse', '?')}({cnt[k]})" for k in order)
    rand = []
    if mk[0, :].any(): rand.append("oben")
    if mk[:, 0].any(): rand.append("links")
    s = seg[i]
    print(f"{i % 100000:>3} {s['klasse']:>6} sich={s['sicher']} herk={s['herkunft']} ges={m.sum()} kern={mk.sum()} teile={n}/{nk} "
          f"bbox=x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()} rand={rand} inst={s.get('instanz', {}).get('text')} | {nbs}")
