import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi
b = np.array(Image.open(r"C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r1c0.png")).astype(float)
if b.ndim==3: b=b[...,0]
dx,dy = map(float, sys.argv[1:3]); out=sys.argv[3]; sx=float(sys.argv[4]) if len(sys.argv)>4 else 10
L=np.hypot(dx,dy); d=np.array([dx,dy])/L; n=np.array([-d[1],d[0]])
if n[1]<0: n=-n
# ranges
cs=np.array([[0,0],[627,0],[0,627],[627,627]],float)
t=cs@d; u=cs@n
T=np.arange(np.floor(t.min()),np.ceil(t.max())); U=np.arange(np.floor(u.min()),np.ceil(u.max()))
TT,UU=np.meshgrid(T,U)
X=TT*d[0]+UU*n[0]; Y=TT*d[1]+UU*n[1]
r=ndi.map_coordinates(b,[Y,X],order=1,cval=np.nan)
valid=~np.isnan(r); r2=np.where(valid,r,np.nanmean(r))
sm=ndi.gaussian_filter(r2,(1.5,sx))
lo,hi=np.percentile(sm[valid],1),np.percentile(sm[valid],99)
img=np.clip((sm-lo)/(hi-lo)*255,0,255); img[~valid]=0
s=2
im=Image.fromarray(img.astype(np.uint8)).resize((img.shape[1]*s,img.shape[0]*s),Image.BILINEAR).convert("RGB")
dr=ImageDraw.Draw(im); f=ImageFont.truetype("arial.ttf",13)
for j,uu in enumerate(U):
    if uu%10==0:
        dr.line([(0,j*s),(im.width,j*s)],fill=(0,200,255) if uu%50==0 else (0,80,110)); dr.text((2,j*s),str(int(uu)),fill=(255,255,0),font=f)
for i,tt in enumerate(T):
    if tt%50==0:
        dr.line([(i*s,0),(i*s,im.height)],fill=(0,80,110)); dr.text((i*s+2,2),str(int(tt)),fill=(255,255,0),font=f)
# kern outline
kc=np.array([[64,64],[564,64],[564,564],[64,564],[64,64]],float)
pts=[(((p@d)-T[0])*s,((p@n)-U[0])*s) for p in kc]
dr.line(pts,fill=(255,0,0),width=2)
print("d",d,"n",n,"T",T[0],T[-1],"U",U[0],U[-1], im.size)
im.save(out,quality=90)
