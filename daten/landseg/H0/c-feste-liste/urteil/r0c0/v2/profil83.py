"""Grauwertprofil je Zeile in Segment 83 (geglättet), um die Parzellengrenze zu finden; nur lesen."""
import numpy as np
import tifffile
from PIL import Image
from scipy.ndimage import gaussian_filter

lab = tifffile.imread("C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r0c0/labels.tif").astype(int)
img = np.array(Image.open("C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r0c0.png").convert("L")).astype(float)
g = gaussian_filter(img, 3.0)
gx = gaussian_filter(img, 2.0)
for y in range(126, 244, 4):
    xs = np.nonzero(lab[y] == 100083)[0]
    if len(xs) < 10:
        continue
    row = g[y, xs]
    # stärkster Anstieg (dunkel -> hell nach rechts) im Inneren
    d = np.gradient(gaussian_filter(img, 2.5)[y, xs.min():xs.max() + 1])
    inner = slice(4, len(d) - 4)
    k = int(np.argmax(d[inner])) + 4 + xs.min()
    print(f"y{y}: x{xs.min()}-{xs.max()}  " + " ".join(f"{int(v)}" for v in row[::4]) + f"  | max Anstieg bei x{k} ({d[k - xs.min()]:.1f})")
