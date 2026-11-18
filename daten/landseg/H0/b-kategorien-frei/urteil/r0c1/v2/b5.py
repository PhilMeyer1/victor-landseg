from werk import *
import pickle
reg, arten, kp = pickle.load(open("probe16.pkl","rb"))
regionen_bild("probe_16a.jpg", reg, arten, 300, 60, 260, 200, 4, titel="Probe 16 Nordost")
regionen_bild("probe_16b.jpg", reg, arten, 330, 190, 230, 190, 4, titel="Probe 16 Südost")
ansicht("kontrast_2.jpg", 330, 190, 230, 190, 4, lab=False, kontrast=True, titel="kontrast_2: Südost-Teil von 16")
