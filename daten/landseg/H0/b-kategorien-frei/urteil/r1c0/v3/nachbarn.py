import sys, numpy as np, tifffile
L = tifffile.imread("C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r1c0/labels.tif")
ids = [int(a) for a in sys.argv[1:]]
for i in ids:
    m = L == i
    nb = {}
    for a, b in ((L[:, 1:], L[:, :-1]), (L[1:, :], L[:-1, :])):
        for p, q in ((a, b), (b, a)):
            sel = (p == i) & (q != i)
            for v, c in zip(*np.unique(q[sel], return_counts=True)):
                nb[int(v)] = nb.get(int(v), 0) + int(c)
    ys, xs = np.nonzero(m)
    print(i, "px", m.sum(), "bbox x", xs.min(), xs.max(), "y", ys.min(), ys.max(), "nachbarn", nb)
for p in [(205,115),(128,118),(193,315),(196,128),(191,300)]:
    print(p, L[p[1], p[0]])
