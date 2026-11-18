import numpy as np, tifffile, sys
from PIL import Image
from scipy import ndimage
B="C:/Users/Phil/Developement/Victor/daten/landseg/H0/"
img=ndimage.gaussian_filter(np.array(Image.open(B+"teilkacheln/r0c0.png").convert("L")).astype(float),1)
lab=tifffile.imread(B+"c-feste-liste/gegenprobe/r0c0/labels.tif")
for t in sys.argv[1].split(","):
    i=int(t); m=lab==i
    if i<100000: i+=100000; m=lab==i
    g=img[m]
    h=[(g<60).mean(),((g>=60)&(g<90)).mean(),((g>=90)&(g<130)).mean(),(g>=130).mean()]
    print(i%100000, m.sum(), "dunkel<60 %.2f mittel60-90 %.2f hell90-130 %.2f sehrhell>130 %.2f"%tuple(h))
