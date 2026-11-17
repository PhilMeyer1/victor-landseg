"""Kennzahlen je Segment: stat.py id,id,...  (Fläche, Kern, Box, Farbe, Teile, Nachbarn)"""
import sys
import json
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

sys.stdout.reconfigure(encoding="utf-8")
B = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500"
lab = np.array(Image.open(B + "/vorstufe/r0c0/labels.tif")).astype(np.int64)
img = np.array(Image.open(B + "/teilkacheln/r0c0.png").convert("RGB")).astype(float)
seg = {s["id"]: s for s in json.load(open(B + "/vorstufe/r0c0/segmente.json", encoding="utf-8"))["segmente"]}
kern = np.zeros(lab.shape, bool)
kern[64:564, 64:564] = True
ids = [int(v) for v in sys.argv[1].split(",")]
for i in ids:
    m = lab == i
    s = seg.get(i, {})
    ys, xs = np.nonzero(m)
    mk = m & kern
    n_teile = ndi.label(mk)[1]
    rgb = img[m].mean(0)
    sd = img[m].std(0).mean()
    # Nachbarn: Grenzlänge
    dil = ndi.binary_dilation(m, structure=np.ones((3, 3), bool)) & ~m
    nb, cnt = np.unique(lab[dil], return_counts=True)
    order = np.argsort(-cnt)[:6]
    nbs = ", ".join(f"{nb[k] % 100000}:{seg.get(int(nb[k]), {}).get('klasse', '?')}({cnt[k]})" for k in order)
    inst = s.get("instanz", {}).get("text", "")
    print(f"{i % 100000} {s.get('klasse')} {s.get('herkunft')} '{inst}' w={s.get('sicherheit', {}).get('wert')} "
          f"sied={s.get('im_siedlung')} fl={m.sum()} kern={mk.sum()} teile={n_teile} "
          f"box x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()} rgb={rgb.round().astype(int).tolist()} sd={sd:.0f}")
    print(f"    Nachbarn: {nbs}")
