from werk import *
import pickle
lab, img, seg = lade()
r63, a63 = pickle.load(open("probe63.pkl","rb"))
for j in a63:
    m = r63 == j
    ps = maske_zu_polygonen(m)
    if len(ps) != 1 or len(ps[0]) < 3:
        ys, xs = np.nonzero(m); print(j, a63[j], int(m.sum()), [len(p) for p in ps], xs.min(), ys.min(), xs.max(), ys.max())
