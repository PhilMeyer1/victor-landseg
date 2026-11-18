from werk import *
import pickle
stat([200054,200073,200067,200078,200074,200047,200090,200096,200084,200085,200094,200089,200106,200099,200102,200103,200049,200100,200115,200081,200126,200119,200121,200113,200120])
lab, img, seg = lade()
m = lab == 200047; m[:, :64] = False; m[564:] = False
s = ndimage.gaussian_filter(img.astype(float),1.2)
print(np.percentile(s[m], [10,25,50,75,90]).round())
r, a = zerlegen_ws(200047, 135, 75, sigma=1.2, minfl=60); r, a = gleichartige_vereinen(r, a)
print(len(a), {k: sum(1 for v in a.values() if v == k) for k in (1,2,3)})
regionen_bild("probe_47.jpg", r, a, 60, 120, 240, 450, 3, titel="Probe Zerlegung 47")
pickle.dump((r, a), open("probe47.pkl","wb"))
