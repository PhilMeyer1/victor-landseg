from werk import *
import pickle
lab, img, seg = lade()
p = pickle.load(open("plan_v2.pkl","rb"))
for sid, r, a in p["plan"]:
    for j in a:
        ids = np.unique(lab[r == j]); assert list(ids) == [p["zu"][(sid, int(j))]], (sid, j, ids)
print("Zuordnung stimmt")
