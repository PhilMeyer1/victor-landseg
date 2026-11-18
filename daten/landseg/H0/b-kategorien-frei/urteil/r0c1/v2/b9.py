from werk import *
import pickle
for sid in (200007, 200039, 200029):
    lab, img, seg = lade()
    m = (lab == sid); m[:64]=False; m[:, 564:]=False
    s = ndimage.gaussian_filter(img.astype(float),1.2)
    print(sid, np.percentile(s[m],[10,50,90]).round())
r7, a7 = zerlegen_ws(200007, 120, 60, sigma=1.2, minfl=60); r7, a7 = gleichartige_vereinen(r7, a7)
print(len(a7), [(j, a7[j], int((r7==j).sum())) for j in a7])
regionen_bild("probe_7.jpg", r7, a7, 375, 60, 192, 80, 5, titel="Probe 7")
pickle.dump((r7, a7), open("probe7.pkl","wb"))
