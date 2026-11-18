import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi
from skimage.morphology import black_tophat, white_tophat, disk
b = np.array(Image.open(r"C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r1c0.png")).astype(float)
if b.ndim==3: b=b[...,0]
g = ndi.gaussian_filter(b, 1.2)
bt = black_tophat(g, disk(5)); wt = white_tophat(g, disk(6))
bt = np.clip(bt/np.percentile(bt,99.5)*255,0,255); wt=np.clip(wt/np.percentile(wt,99.5)*255,0,255)
rgb = np.stack([bt, wt, np.zeros_like(bt)],-1).astype(np.uint8)
s=3
im = Image.fromarray(rgb).resize((628*s,628*s), Image.BILINEAR)
d=ImageDraw.Draw(im); f=ImageFont.truetype("arial.ttf",14)
for v in range(25,628,25):
    c=(0,160,255) if v%50==0 else (0,70,110)
    d.line([(v*s,0),(v*s,im.height)],fill=c); d.line([(0,v*s),(im.width,v*s)],fill=c)
    d.text((v*s+2,2),str(v),fill=(255,255,255),font=f); d.text((2,v*s+2),str(v),fill=(255,255,255),font=f)
im.save("linien.jpg",quality=90)
