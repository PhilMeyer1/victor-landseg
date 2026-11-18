import numpy as np
from PIL import Image

H0 = "C:/Users/Phil/Developement/Victor/daten/landseg/H0"
img = np.array(Image.open(H0 + "/H0.png").convert("L")).astype(float)
lab = np.array(Image.open(H0 + "/c-feste-liste/zusammen/labels.tif"))

# (Paar, Punkt x,y, ids): mittlerer Grauton jedes Segments im Fenster 15x15 um die Stelle
stellen = [
    (1, 121, 250, [100154, 100168]),
    (2, 359, 250, [100154, 100172]),
    (3, 367, 250, [100149, 100172]),
    (4, 389, 250, [100143, 100149, 100198]),
    (5, 394, 250, [100143, 100198]),
    (6, 414, 250, [100143, 100167]),
    (7, 295, 500, [100154, 300080, 300002]),
    (8, 298, 500, [100224, 300080]),
    (9, 305, 500, [100224, 300075]),
    (10, 322, 500, [100220, 300075]),
    (11, 336, 500, [100225, 300080]),
    (12, 339, 500, [100225, 300006]),
]
for nr, x, y, ids in stellen:
    r = 7
    I = img[y - r:y + r + 1, x - r:x + r + 1]
    L = lab[y - r:y + r + 1, x - r:x + r + 1]
    teile = []
    for s in ids:
        m = L == s
        teile.append(f"{s}: n={m.sum()} mittel={I[m].mean():.0f} sd={I[m].std():.0f}" if m.any() else f"{s}: -")
    print(nr, " | ".join(teile))

# ganze Segmente
for s in [100154, 100168, 100172, 100149, 100143, 100198, 100167, 100224, 100220, 100225, 300080, 300075, 300006]:
    m = lab == s
    print(s, m.sum(), f"{img[m].mean():.0f}", f"{img[m].std():.0f}")
# 300080 Teile: Zusammenhang
from scipy import ndimage
m = lab == 300080
z, n = ndimage.label(m)
print("300080 Teile im Ausschnitt:", n, [int((z == i).sum()) for i in range(1, n + 1)])
for i in range(1, n + 1):
    ys, xs = np.nonzero(z == i)
    print("  Teil", i, "x", xs.min(), xs.max(), "y", ys.min(), ys.max(), f"mittel={img[z == i].mean():.0f}")
m = lab == 100143
ys, xs = np.nonzero(m)
print("143 bbox", xs.min(), xs.max(), ys.min(), ys.max())
