from werk import *
reg, arten = zerlegen_ws(200004, 120, 60, sigma=1.2, minfl=40)
print(len(arten), {a: sum(1 for v in arten.values() if v == a) for a in (1,2,3)})
for j,a in arten.items(): print(j, a, int((reg==j).sum()), end="; ")
regionen_bild("probe_4.jpg", reg, arten, 56, 56, 190, 160, 5, titel="Probe Zerlegung 4: rot hell, grün mittel, blau dunkel")
