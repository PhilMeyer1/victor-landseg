from werk import *
import pickle
lab, img, seg = lade()
p = pickle.load(open("plan_v4.pkl","rb"))
for sid, r, a in p["plan"]:
    for j in a:
        ids = np.unique(lab[r == j]); assert list(ids) == [p["zu"][(sid, int(j))]], (sid, j, ids)
kern = np.zeros(lab.shape, bool); kern[64:564,64:564] = True
m = lab == 200343; print("Zuordnung stimmt; 200343:", int(m.sum()), "im Kern", int((m & kern).sum()))
ansicht("nah_4.jpg", 300, 300, 268, 268, 3, titel="nah_4: 63, 105, 107 nach dem Teilen (Nummer = ID mod 100000)")
ansicht("kontrast_2.jpg", 300, 300, 268, 268, 3, lab=False, kontrast=True, titel="kontrast_2: v4, Kontrast gestreckt")
