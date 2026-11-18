import numpy as np
from PIL import Image
from scipy import ndimage as ndi
img = np.array(Image.open("C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r1c0.png").convert("L")).astype(float)
s = ndi.uniform_filter(img, 5)
for x in range(345, 531, 10):
    col = s[430:560, x]
    thr = 97
    best = (0, 0, 0); start = None
    for i, v in enumerate(list(col) + [0]):
        if v > thr and start is None: start = i
        if v <= thr and start is not None:
            if i - start > best[0]: best = (i - start, start + 430, i - 1 + 430)
            start = None
    print(x, best, "max %.0f" % col.max())
