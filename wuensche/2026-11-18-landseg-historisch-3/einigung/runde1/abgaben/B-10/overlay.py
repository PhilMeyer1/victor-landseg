import sys, json
import numpy as np
from PIL import Image, ImageDraw
import tifffile
B="C:/Users/Phil/Developement/Victor/daten/landseg/H0/"
x0,y0,x1,y1,f,ziel=[int(v) for v in sys.argv[1:6]]+[sys.argv[6]]
ids=[int(v) for v in sys.argv[7].split(",")]
im=np.array(Image.open(B+"H0.png").convert("L")).astype(np.float32)
lab=np.zeros((1000,1000),np.int64)
for tk,ox,oy in [("r0c1",436,-64),("r1c1",436,436),("r0c0",-64,-64),("r1c0",-64,436)]:
    L=tifffile.imread(B+f"b-kategorien-frei/{tk}/labels.tif")
    kx=500 if tk[3]=="1" else 0; ky=500 if tk[1]=="1" else 0
    # kern region
    lab[ky:ky+500,kx:kx+500]=L[ky-oy:ky-oy+500,kx-ox:kx-ox+500]
crop=im[y0:y1,x0:x1]; lc=lab[y0:y1,x0:x1]
rgb=np.stack([crop]*3,-1)
pal=[(0,255,255),(255,0,255),(255,128,0),(0,255,0),(80,120,255),(255,60,60),(255,255,0),(160,255,160)]
legend=[]
for i,s in enumerate(ids):
    m=lc==s
    if m.any():
        c=np.array(pal[i%len(pal)],np.float32)
        rgb[m]=rgb[m]*0.6+c*0.4
        legend.append((s,pal[i%len(pal)],np.argwhere(m).mean(0)))
rgb=np.repeat(np.repeat(rgb,f,0),f,1)
lcb=np.repeat(np.repeat(lc,f,0),f,1)
edge=np.zeros(lcb.shape,bool)
edge[:,1:]|=lcb[:,1:]!=lcb[:,:-1]; edge[1:,:]|=lcb[1:,:]!=lcb[:-1,:]
rgb[edge]=(255,255,255)
img=Image.fromarray(rgb.clip(0,255).astype(np.uint8))
d=ImageDraw.Draw(img)
for s,c,(cy,cx) in legend:
    d.text((cx*f,cy*f),str(s)[-3:],fill=(0,0,0))
for gx in range(((x0//20)+1)*20,x1,20): d.text(((gx-x0)*f+2,2),str(gx),fill=(255,255,0))
for gy in range(((y0//20)+1)*20,y1,20): d.text((2,(gy-y0)*f+2),str(gy),fill=(255,255,0))
img.save(ziel,quality=92)
