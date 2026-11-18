from werk import *
reg, arten = zerlegen_ws(200065, 150, 90, sigma=1.0, minfl=50, ero=(1,2,1))
reg, arten = gleichartige_vereinen(reg, arten)
for j,a in arten.items(): print(j, a, int((reg==j).sum()))
regionen_bild("probe_65.jpg", reg, arten, 255, 235, 80, 80, 8, titel="Probe 65")
