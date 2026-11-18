import numpy as np, tifffile, sys
from PIL import Image
B="C:/Users/Phil/Developement/Victor/daten/landseg/H0/"
im=np.array(Image.open(B+"H0.png").convert("L")).astype(float)
L0=tifffile.imread(B+"b-kategorien-frei/r0c1/labels.tif"); L1=tifffile.imread(B+"b-kategorien-frei/r1c1/labels.tif")
lab=np.zeros((1000,1000),np.int64)
lab[0:500,500:1000]=L0[64:564,64:564]; lab[500:1000,500:1000]=L1[64:564,64:564]
for a,b in [(200363,400011),(200363,400050),(200112,400042),(200350,400042),(200111,400042),(200111,400041),(200124,400055),(200124,400029),(200123,400029),(200110,400057),(200125,400057)]:
    for s,yr in [(a,(492,500)),(b,(500,508))]:
        m=(lab==s); m[:yr[0]]=False; m[yr[1]:]=False
        v=im[m]
        print(s, m.sum(), "%.0f %.0f"%(v.mean() if v.size else -1, v.std() if v.size else -1), end=" | ")
    print()
# profile across seam rows 494..506 for x 840..1000 step
for y in range(492,510,2):
    print(y, " ".join("%3d"%im[y,x] for x in range(840,1000,6)))
