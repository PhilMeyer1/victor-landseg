"""Mischsegmente finden: Anteile hell/dunkel (geglättet) und größte zusammenhängende Teile."""
import sys
import numpy as np
from scipy import ndimage
sys.path.insert(0, "C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r0c0/v1")
import werkzeug as w

lab, img, seg = w.lade()
g = ndimage.gaussian_filter(img, 1.2)
ids = [int(s) if int(s) > 99999 else 100000 + int(s) for s in sys.argv[1].split(",")]
for i in ids:
    m = lab == i
    m[:64, :] = False; m[564:, :] = False; m[:, :64] = False; m[:, 564:] = False
    n = m.sum()
    if n == 0:
        print(i % 100000, "nicht im Kern"); continue
    out = []
    for name, mm in (("hell", m & (g > 135)), ("dunkel", m & (g < 55)), ("mitte", m & (g >= 55) & (g <= 135))):
        l, k = ndimage.label(mm)
        big = sorted(np.bincount(l.ravel())[1:], reverse=True)[:2] if k else []
        out.append(f"{name}={mm.sum()/n:.0%}{list(map(int,big))}")
    print(f"{i%100000:>4} n={n:>5} " + " ".join(out))
