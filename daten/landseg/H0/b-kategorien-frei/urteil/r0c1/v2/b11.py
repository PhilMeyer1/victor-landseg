from werk import *
import pickle
r39, a39 = zerlegen_ws(200039, 120, 60, sigma=1.2, minfl=60); r39, a39 = gleichartige_vereinen(r39, a39)
print(len(a39), [(j, a39[j], int((r39==j).sum())) for j in a39])
regionen_bild("probe_39.jpg", r39, a39, 465, 145, 105, 115, 7, titel="Probe 39")
pickle.dump((r39, a39), open("probe39.pkl","wb"))
