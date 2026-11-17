"""Statistik je Kernsegment von r1c0: Fläche, Rahmen, Farbe, Helligkeit, Textur, Nachbarn, Komponenten."""
import json
import sys
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image
from scipy import ndimage

B = Path("C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b")
lab = tifffile.imread(B / "vorstufe/r1c0/labels.tif").astype(np.int64)
img = np.asarray(Image.open(B / "teilkacheln/r1c0.png").convert("RGB")).astype(np.float64)
seg = {s["id"]: s for s in json.loads((B / "vorstufe/r1c0/segmente.json").read_text(encoding="utf-8"))["segmente"]}
ids = [int(x) for x in sys.argv[1].split(",")]
gray = img.mean(axis=2)
# local texture: std in 5x5
m = ndimage.uniform_filter(gray, 5)
m2 = ndimage.uniform_filter(gray ** 2, 5)
tex = np.sqrt(np.maximum(m2 - m * m, 0))
kern = np.zeros(lab.shape, bool)
kern[64:564, 64:564] = True
for i in ids:
    msk = lab == i
    km = msk & kern
    ys, xs = np.nonzero(msk)
    comp, n = ndimage.label(msk)
    sizes = sorted(np.bincount(comp.ravel())[1:].tolist(), reverse=True)
    dil = ndimage.binary_dilation(msk, iterations=1) & ~msk
    nb = np.bincount(lab[dil].ravel())
    nbs = sorted([(int(c), int(k)) for k, c in enumerate(nb) if c > 0], reverse=True)[:6]
    rgb = img[msk].mean(axis=0)
    exg = (2 * img[msk][:, 1] - img[msk][:, 0] - img[msk][:, 2]).mean()
    s = seg[i]
    print(f"{i} {s['klasse']} {s.get('instanz', {}).get('text', s['herkunft'])} w={s['sicherheit'].get('wert')} "
          f"A={msk.sum()} kern={km.sum()} bbox=x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()} "
          f"rgb={rgb.round().astype(int).tolist()} exg={exg:.0f} hell={gray[msk].mean():.0f} tex={tex[msk].mean():.1f} "
          f"komp={n} {sizes[:4]} nb={[(k % 100000, c) for c, k in nbs]}")
