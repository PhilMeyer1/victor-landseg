from werk import *
import pickle
lab, img, seg = lade()
r4, a4 = zerlegen_ws(200004, 120, 60, sigma=1.2, minfl=50); r4, a4 = gleichartige_vereinen(r4, a4)
r65, a65 = zerlegen_ws(200065, 150, 90, sigma=1.0, minfl=50, ero=(1,2,1)); r65, a65 = gleichartige_vereinen(r65, a65)
# Region, die die ID 4 behaelt: die mit Kontakt zu beiden Kontextteilen von 4 (oben links, dunkel)
st=[[0,1,0],[1,1,1],[0,1,0]]
kern = np.zeros(lab.shape, bool); kern[64:564, 64:564] = True
ctx = (lab == 200004) & ~kern
l, k = ndimage.label(ctx, structure=st)
kand = None
for j in a4:
    d = ndimage.binary_dilation(r4 == j, structure=st)
    if all((d & (l == i)).any() for i in range(1, k+1)): kand = j
print("behalten 4:", kand, a4[kand], int((r4==kand).sum()))
fl = np.bincount(r65.ravel()); b65 = int(np.argmax(fl[1:]))+1
s = plan_schritte(200004, r4, kand, "1.1.1", lab) + plan_schritte(200065, r65, b65, "1.1.1", lab)
karte, zu, b = simulieren(s, [(200004, r4), (200065, r65)])
print(zu)
json.dump({"schritte": [{k: v for k, v in x.items() if not k.startswith("_")} for x in s]},
          open("eingriffe.json", "w", encoding="utf-8"))
pickle.dump({"r4": r4, "a4": a4, "r65": r65, "a65": a65, "zu": zu}, open("plan_v1.pkl", "wb"))
print(len(s), "Schritte")
