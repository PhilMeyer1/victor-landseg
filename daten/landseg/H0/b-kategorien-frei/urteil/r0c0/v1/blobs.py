import sys
import numpy as np
from scipy import ndimage
sys.path.insert(0, ".")
import werkzeug as w
lab, img, seg = w.lade()
g = ndimage.gaussian_filter(img, 1.2)
for s in sys.argv[1].split(","):
    i = int(s) + 100000
    m = lab == i
    for name, mm in (("hell", m & (g > 135)), ("dunkel", m & (g < 55))):
        l, k = ndimage.label(mm)
        for j, sl in enumerate(ndimage.find_objects(l), 1):
            n = (l[sl] == j).sum()
            if n >= 60:
                print(s, name, n, f"x{sl[1].start}-{sl[1].stop-1} y{sl[0].start}-{sl[0].stop-1}")
