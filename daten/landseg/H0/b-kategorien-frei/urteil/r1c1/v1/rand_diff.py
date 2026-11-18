import sys
import numpy as np
sys.path.insert(0, "C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c1/v1")
import werkzeug as wz
a, _ = wz.laden(None, leise=True)
b, _ = wz.laden(sys.argv[1], leise=True)
rand = np.ones(a.shape, bool); rand[64:564, 64:564] = False
d = (a != b) & rand
ys, xs = np.nonzero(d)
from collections import Counter
print(Counter(zip(a[d].tolist(), b[d].tolist())))
if len(xs): print("x", xs.min(), xs.max(), "y", ys.min(), ys.max())
for nid in sorted(set(b[d].tolist())):
    m = b == nid
    print(nid, "gesamt", int(m.sum()), "im Kern", int((m & ~rand).sum()))
