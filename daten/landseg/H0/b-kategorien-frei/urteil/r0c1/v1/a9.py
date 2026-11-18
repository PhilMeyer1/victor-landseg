from werk import *
import pickle
lab, img, seg = lade()
p = pickle.load(open("plan_v1.pkl", "rb"))
for (sid, j), nid in p["zu"].items():
    r = p["r4"] if sid == 200004 else p["r65"]
    ids = np.unique(lab[r == j]); assert list(ids) == [nid], (sid, j, ids)
a = {}
for (sid, j), nid in p["zu"].items():
    r = p["r4"] if sid == 200004 else p["r65"]
    art = (p["a4"] if sid == 200004 else p["a65"])[j]
    m = r == j; ys, xs = np.nonzero(m)
    dt = ndimage.distance_transform_edt(np.pad(m,1))[1:-1,1:-1]; yy, xx = np.unravel_index(np.argmax(dt), dt.shape)
    a[nid] = dict(von=sid, art=art, fl=int(m.sum()), bbox=[int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())],
                  punkt=[int(xx),int(yy)], grau=round(float(img[m].mean())), naht_links=bool(xs.min()<=64), oben=bool(ys.min()<=64))
json.dump(a, open("regionen_v1.json","w"), indent=0)
for k,v in sorted(a.items()): print(k, v)
ansicht("nah_6.jpg", 56, 56, 190, 160, 5, titel="nah_6: Segment 4 nach dem Teilen (Nummern = ID mod 100000)")
ansicht("nah_7.jpg", 245, 225, 90, 90, 8, titel="nah_7: 65 nach dem Teilen")
