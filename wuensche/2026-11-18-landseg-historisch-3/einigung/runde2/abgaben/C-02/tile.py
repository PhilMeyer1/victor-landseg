import sys, numpy as np
from PIL import Image
import tifffile
D='C:/Users/Phil/Developement/Victor/daten/landseg/H0/'
img=np.array(Image.open(D+'H0.png').convert('L')).astype(int)
t=sys.argv[1]; ox,oy=int(sys.argv[2]),int(sys.argv[3])
lab=tifffile.imread(D+f'c-feste-liste/{t}/labels.tif')
for s in map(int,sys.argv[4].split(',')):
    ys,xs=np.nonzero(lab==s)
    gx=xs+ox; gy=ys+oy
    ok=(gx>=0)&(gx<1000)&(gy>=0)&(gy<1000)
    v=img[gy[ok],gx[ok]]
    core=(gx>=int(sys.argv[5]))&(gx<int(sys.argv[6]))&(gy>=int(sys.argv[7]))&(gy<int(sys.argv[8]))
    print(t,s,'n',len(xs),'x',gx.min(),gx.max(),'y',gy.min(),gy.max(),'mean',round(v.mean(),1),'core n',int(core.sum()),'core mean',round(img[gy[core],gx[core]].mean(),1) if core.any() else None,'ctx mean', round(img[gy[ok&~core],gx[ok&~core]].mean(),1) if (ok&~core).any() else None)
