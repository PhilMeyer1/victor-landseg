from werk import *
import pickle
lab, img, seg = lade()
p = pickle.load(open("plan_v3.pkl","rb"))
for sid, r, a in p["plan"]:
    for j in a:
        ids = np.unique(lab[r == j]); assert list(ids) == [p["zu"][(sid, int(j))]], (sid, j, ids)
alle = set(np.unique(lab).tolist())
neu = sorted(i for i in alle if i > 200288 and i not in p["zu"].values())
print("Zuordnung stimmt; neue IDs nur im Kontext:", neu)
kern = np.zeros(lab.shape, bool); kern[64:564,64:564] = True
for i in neu:
    m = lab == i; ys, xs = np.nonzero(m); print(i, int(m.sum()), "im Kern:", int((m & kern).sum()), xs.min(), ys.min(), xs.max(), ys.max())
