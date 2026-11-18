from werk import *
import pickle
lab, img, seg = lade()
p = pickle.load(open("plan_v2.pkl","rb"))
print({k: v for k, v in p["zu"].items() if k[0] in (200039, 200007)})
for sid in (200016, 200007, 200039):
    print(sid, "auf Karte:", int((lab == sid).sum()))
lab0 = None
