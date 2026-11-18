from werk import *
import pickle
a = np.array([325, 296.]); b = np.array([505, 165.])
d = (b-a)/np.linalg.norm(b-a); n = np.array([-d[1], d[0]])
kern_poly = [a-2*n, b-2*n, b+3*n, a+3*n]
kern_poly = [[int(round(p[0])), int(round(p[1]))] for p in kern_poly]
reg, arten = zerlegen_ws(200016, 120, 60, sigma=1.2, minfl=60, extra_marken=[(kern_poly, 4)])
reg, arten = gleichartige_vereinen(reg, arten)
print(len(arten), {a: sum(1 for v in arten.values() if v == a) for a in (1,2,3,4)})
regionen_bild("probe_16.jpg", reg, arten, 118, 60, 450, 330, 3, titel="Probe Zerlegung 16: rot hell, grün mittel, blau dunkel, ohne Farbe = Gasse")
pickle.dump((reg, arten, kern_poly), open("probe16.pkl","wb"))
