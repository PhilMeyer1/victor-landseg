import sys, numpy as np, tifffile
from PIL import Image
H0="C:/Users/Phil/Developement/Victor/daten/landseg/H0"
img=np.array(Image.open(f"{H0}/teilkacheln/r1c1.png").convert("L")).astype(int)
lab=tifffile.imread(f"{H0}/a-alles-frei/r1c1/labels.tif")
x0,y0,x1,y1=[int(v)-436 for v in sys.argv[1:5]]
ids=[int(v) for v in sys.argv[5:]]
for y in range(y0,y1):
    row=[]
    for x in range(x0,x1):
        v=lab[y,x]; m={i:c for i,c in zip(ids,'ABCDEFG')}.get(v,'.')
        row.append(f"{m}{img[y,x]:3d}")
    print(y+436, ' '.join(row))
