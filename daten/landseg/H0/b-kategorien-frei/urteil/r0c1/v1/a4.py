from werk import *
reg, arten = zerlegen_ws(200004, 120, 60, sigma=1.2, minfl=50)
reg, arten = gleichartige_vereinen(reg, arten)
print(len(arten), {a: sum(1 for v in arten.values() if v == a) for a in (1,2,3)})
regionen_bild("probe_4.jpg", reg, arten, 56, 56, 190, 160, 5, titel="Probe Zerlegung 4: rot hell, grün mittel, blau dunkel")
fl = np.bincount(reg.ravel()); beh = int(np.argmax(fl[1:]))+1
sch = plan_schritte(200004, reg, beh, "1.1.1")
karte, zu, b = simulieren(sch, [(200004, reg)])
print("ok", beh, zu)
