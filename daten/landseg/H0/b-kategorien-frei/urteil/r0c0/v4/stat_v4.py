import json, numpy as np
from PIL import Image
lab = np.array(Image.open("C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r0c0/labels.tif"))
img = np.array(Image.open("C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r0c0.png").convert("L")).astype(float)
man = json.load(open("C:/Users/Phil/Developement/Victor/daten/landseg/H0/manifest.json"))
print(man["teilkacheln"]["r0c0"] if isinstance(man["teilkacheln"], dict) else [t for t in man["teilkacheln"] if t.get("name")=="r0c0" or t.get("id")=="r0c0"])
ids=[100172,100180,100143,100276,100279,100178,100165,100185,100187,100183,100191,100189,100186,100194,100199,100193,100198,100196,100192,100176,100207,100201,100209,100216,100195,100210,100214,100211,100218,100215,100224,100220,100225,100219,100228,100229]
for i in ids:
    ys,xs=np.nonzero(lab==i)
    v=img[lab==i]
    print(i, len(xs), "x",xs.min(),xs.max(),"y",ys.min(),ys.max(),"mean %.0f sd %.0f"%(v.mean(),v.std()))
