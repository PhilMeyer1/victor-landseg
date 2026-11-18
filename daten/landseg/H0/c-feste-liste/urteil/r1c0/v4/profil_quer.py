# Grauwertprofil quer zum hellen Streifen (Richtung senkrecht zu SW-NO), Mittel über Länge
import numpy as np, sys
from PIL import Image
from scipy import ndimage as ndi
img = np.array(Image.open("C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r1c0.png").convert("L")).astype(float)
img = ndi.uniform_filter(img, 3)
# Achse: Punkte entlang (cx,cy) mit Richtung d=(cos,-sin) slope
for cx in (380, 420, 460, 500):
    # Streifenrichtung etwa (1,-0.45) normiert
    dx, dy = 1, -0.45; n = (dx*dx+dy*dy)**.5; dx/=n; dy/=n
    nx, ny = -dy, dx  # senkrecht, nach unten-rechts
    cy = {380: 515, 420: 497, 460: 479, 500: 461}[cx]
    vals = []
    for t in range(-25, 26, 2):
        x, y = cx + nx*t, cy + ny*t
        vals.append("%d:%.0f" % (t, img[int(round(y)), int(round(x))]))
    print(cx, cy, " ".join(vals))
