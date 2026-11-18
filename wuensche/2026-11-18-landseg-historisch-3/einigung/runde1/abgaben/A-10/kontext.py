import numpy as np, tifffile, sys
from PIL import Image, ImageDraw
D="C:/Users/Phil/Developement/Victor/daten/landseg/H0/"
H=np.array(Image.open(D+"H0.png").convert("L"))
x0,y0,x1,y1=[int(v) for v in sys.argv[1:5]]; f=int(sys.argv[5]); ziel=sys.argv[6]
L0=tifffile.imread(D+"a-alles-frei/r0c1/labels.tif"); L1=tifffile.imread(D+"a-alles-frei/r1c1/labels.tif")
# ausschnitt label map from kern
G=np.zeros(H.shape,dtype=np.int64)
G[0:500,500:1000]=L0[64:564,64:564]
G[500:1000,500:1000]=L1[64:564,64:564]
crop=H[y0:y1,x0:x1]; g=G[y0:y1,x0:x1]
rgb=np.stack([crop]*3,-1).repeat(f,0).repeat(f,1)
ids=[int(v) for v in sys.argv[7].split(",")] if len(sys.argv)>7 else []
farben=[(0,255,255),(255,0,255),(255,255,0),(0,255,0),(255,128,0),(255,0,0),(80,160,255)]
gg=g.repeat(f,0).repeat(f,1)
for i,s in enumerate(ids):
    m=gg==s
    rand=m & ~(np.roll(m,1,0)&np.roll(m,-1,0)&np.roll(m,1,1)&np.roll(m,-1,1))
    rgb[rand]=farben[i%len(farben)]
im=Image.fromarray(rgb.astype(np.uint8)); d=ImageDraw.Draw(im)
if y0<500<y1: d.line([(0,(500-y0)*f),(im.width,(500-y0)*f)],fill=(255,60,60),width=1)
for k in range(0,x1-x0,20): d.text((k*f+2,2),str(x0+k),fill=(255,80,80))
for k in range(0,y1-y0,20): d.text((2,k*f+2),str(y0+k),fill=(255,80,80))
im.save(ziel,quality=90); print(im.size)
