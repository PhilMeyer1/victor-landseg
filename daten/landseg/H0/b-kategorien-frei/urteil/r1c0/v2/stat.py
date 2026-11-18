import sys, numpy as np, tifffile, json
L = tifffile.imread("C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r1c0/labels.tif")
img = np.array(__import__("PIL.Image", fromlist=["Image"]).open("C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r1c0.png").convert("L")).astype(float)
K = L[64:564, 64:564]; I = img[64:564, 64:564]
V = {"v1": (0,0), "v2": (250,0), "v3": (0,250), "v4": (250,250)}
for i in map(int, sys.argv[1:]):
    m = K == i
    parts = {v: int(m[y:y+250, x:x+250].sum()) for v, (x, y) in V.items()}
    ys, xs = np.nonzero(m)
    print(i, "kern", int(m.sum()), parts, "grau mittel %.0f sd %.0f" % (I[m].mean(), I[m].std()) if m.sum() else "", "bbox", (xs.min()+64, xs.max()+64, ys.min()+64, ys.max()+64) if m.sum() else "")
