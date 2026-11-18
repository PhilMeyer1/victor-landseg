"""Rand der Straße 4 je Zeile im Kern von v1 schätzen (Helligkeitsumschlag), nur lesen."""
import numpy as np
import tifffile
from PIL import Image
from scipy.ndimage import gaussian_filter

lab = tifffile.imread("C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r0c0/labels.tif").astype(int)
img = np.array(Image.open("C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r0c0.png").convert("L")).astype(float)
g = gaussian_filter(img, 1.0)
for y in range(64, 300, 4):
    row = g[y, 0:260]
    m4 = np.nonzero(lab[y, 0:260] == 100004)[0]
    if len(m4) == 0:
        continue
    c = int(np.argmax(row[max(m4.min() - 5, 0):m4.max() + 5])) + max(m4.min() - 5, 0)
    top = row[c]
    # rechter Rand: erste Stelle rechts, an der der Grauwert unter 125 fällt
    r = c
    while r < 259 and row[r] > 125:
        r += 1
    l = c
    while l > 0 and row[l] > 125:
        l -= 1
    print(f"y{y}: 4 von x{m4.min()} bis x{m4.max()}, Mitte x{c} ({top:.0f}), hell x{l + 1}-{r - 1}, "
          f"rechts von Rand in 4: {max(0, m4.max() - r + 1)} px, links: {max(0, l - m4.min() + 1)} px")
