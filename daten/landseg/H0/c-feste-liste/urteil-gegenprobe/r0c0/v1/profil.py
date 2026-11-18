import numpy as np, tifffile, sys
from PIL import Image
from scipy import ndimage
B="C:/Users/Phil/Developement/Victor/daten/landseg/H0/"
img=np.array(Image.open(B+"teilkacheln/r0c0.png").convert("L")).astype(float)
img=ndimage.gaussian_filter(img,1)
lab=tifffile.imread(B+"c-feste-liste/gegenprobe/r0c0/labels.tif")
x0,y0,x1,y1=[float(t) for t in sys.argv[1:5]]
n=int(np.hypot(x1-x0,y1-y0))
for i in range(0,n+1):
    x=x0+(x1-x0)*i/n; y=y0+(y1-y0)*i/n
    xi,yi=int(round(x)),int(round(y))
    print(f"{xi},{yi} g={img[yi,xi]:.0f} id={lab[yi,xi]%100000}")
