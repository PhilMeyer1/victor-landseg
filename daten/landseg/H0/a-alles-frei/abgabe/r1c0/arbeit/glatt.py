import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi
b = np.array(Image.open(r"C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r1c0.png")).astype(float)
if b.ndim==3: b=b[...,0]
g = ndi.gaussian_filter(b, 4)
lo,hi = np.percentile(g,1),np.percentile(g,99)
g = np.clip((g-lo)/(hi-lo)*255,0,255).astype(np.uint8)
s=3
im = Image.fromarray(g).resize((628*s,628*s), Image.BICUBIC).convert("RGB")
d=ImageDraw.Draw(im); f=ImageFont.truetype("arial.ttf",14)
for v in range(25,628,25):
    c=(0,200,255) if v%50==0 else (0,90,120)
    d.line([(v*s,0),(v*s,im.height)],fill=c); d.line([(0,v*s),(im.width,v*s)],fill=c)
    d.text((v*s+2,2),str(v),fill=(255,255,0),font=f); d.text((2,v*s+2),str(v),fill=(255,255,0),font=f)
d.rectangle([64*s,64*s,564*s,564*s],outline=(255,0,0),width=2)
im.save("glatt.jpg",quality=90)
