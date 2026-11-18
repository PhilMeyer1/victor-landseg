import numpy as np
from PIL import Image
from scipy import ndimage
from skimage.morphology import closing, disk
from skimage.segmentation import felzenszwalb, find_boundaries
a=np.array(Image.open('C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r1c1.png')).astype(float)
s=ndimage.gaussian_filter(a,0.8)
bh=closing(s,disk(3))-s
x0,y0,x1,y1=185,60,315,190
for thr in (18,28):
    m=(bh>thr)&(s<120)
    rgb=np.stack([a]*3,-1)
    rgb[m]=[255,60,0]
    Image.fromarray(rgb[y0:y1,x0:x1].astype(np.uint8)).resize(((x1-x0)*4,(y1-y0)*4),Image.NEAREST).save(f't_lin{thr}.jpg')
seg=felzenszwalb(a/255.,scale=70,sigma=0.7,min_size=20)
b=find_boundaries(seg)
rgb=np.stack([a]*3,-1); rgb[b]=[255,220,0]
Image.fromarray(rgb[y0:y1,x0:x1].astype(np.uint8)).resize(((x1-x0)*4,(y1-y0)*4),Image.NEAREST).save('t_fz70.jpg')
print(seg.max())
