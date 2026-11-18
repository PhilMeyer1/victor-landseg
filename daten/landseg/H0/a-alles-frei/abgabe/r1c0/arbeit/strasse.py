import numpy as np
from PIL import Image
from scipy import ndimage as ndi
b = np.array(Image.open(r"C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r1c0.png")).astype(float)
if b.ndim==3: b=b[...,0]
g=ndi.gaussian_filter(b,1.5)
guess=np.interp(np.arange(628),[0,100,200,250,300,350,400,450,500,550,575,627],[488,412,322,276,247,216,185,153,123,92,80,60])
for x in range(0,628,20):
    y0=int(guess[x]); col=g[max(0,y0-20):y0+21,x]
    ys=np.arange(max(0,y0-20),y0+21)
    hi=col>col.max()-0.5*(col.max()-np.median(col))
    print(x, y0, int(col.max()), int(np.median(col)), ys[hi].min(), ys[hi].max(), round((ys[hi].min()+ys[hi].max())/2,1))
