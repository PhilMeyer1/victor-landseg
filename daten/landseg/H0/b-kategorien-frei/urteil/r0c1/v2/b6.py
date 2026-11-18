from werk import *
import pickle
reg, arten, kp = pickle.load(open("probe16.pkl","rb"))
regionen_bild("probe_16c.jpg", reg, arten, 118, 120, 220, 250, 4, titel="Probe 16 Südwest (v1/v3/v4)")
ansicht("kontrast_3.jpg", 118, 120, 220, 250, 4, lab=False, kontrast=True, titel="kontrast_3: Südwest-Teil von 16")
