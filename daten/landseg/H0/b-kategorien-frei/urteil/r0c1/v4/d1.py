from werk import *
import pickle
stat([200069,200071,200051,200079,200076,200077,200075,200082,200083,200080,200098,200095,200091,200063,200097,200116,200109,200114,200108,200105,200107,200122,200112,200111,200124,200123,200110,200125])
lab, img, seg = lade()
for sid in (200063, 200071, 200097):
    m = lab == sid; m[564:] = False; m[:, 564:] = False
    s = ndimage.gaussian_filter(img.astype(float),1.2)
    print(sid, np.percentile(s[m], [10,25,50,75,90]).round())
r, a = zerlegen_ws(200063, 120, 60, sigma=1.2, minfl=60); r, a = gleichartige_vereinen(r, a)
print("63:", len(a), {k: sum(1 for v in a.values() if v == k) for k in (1,2,3)})
regionen_bild("probe_63.jpg", r, a, 300, 300, 268, 268, 3, titel="Probe Zerlegung 63")
pickle.dump((r, a), open("probe63.pkl","wb"))
r2, a2 = zerlegen_ws(200071, 120, 60, sigma=1.2, minfl=60); r2, a2 = gleichartige_vereinen(r2, a2)
print("71:", [(j, a2[j], int((r2==j).sum())) for j in a2])
regionen_bild("probe_71.jpg", r2, a2, 290, 290, 110, 160, 5, titel="Probe 71")
pickle.dump((r2, a2), open("probe71.pkl","wb"))
ansicht("kontrast_1.jpg", 290, 290, 110, 160, 5, lab=False, kontrast=True, titel="kontrast_1: 71, 95, 97 links in v4")
