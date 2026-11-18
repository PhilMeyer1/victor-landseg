import numpy as np, tifffile
from PIL import Image, ImageDraw
B="C:/Users/Phil/Developement/Victor/daten/landseg/H0/"
f=8
out=[]
for tk,ox,oy,ids in [("r0c1",436,-64,[200110,200125,200123,200124]),("r1c1",436,436,[400057,400029,400055])]:
    im=np.array(Image.open(B+f"teilkacheln/{tk}.png").convert("L")).astype(float)
    L=tifffile.imread(B+f"b-kategorien-frei/{tk}/labels.tif")
    x0,x1,y0,y1=950,1064,450,560
    c=im[y0-oy:y1-oy, x0-ox:x1-ox]; l=L[y0-oy:y1-oy, x0-ox:x1-ox]
    rgb=np.stack([c]*3,-1)
    pal=[(0,255,255),(255,0,255),(255,128,0),(0,255,0)]
    for i,s in enumerate(ids):
        m=l==s; rgb[m]=rgb[m]*0.65+np.array(pal[i])*0.35
        print(tk,s,m.sum())
    rgb=np.repeat(np.repeat(rgb,f,0),f,1); lb=np.repeat(np.repeat(l,f,0),f,1)
    e=np.zeros(lb.shape,bool); e[:,1:]|=lb[:,1:]!=lb[:,:-1]; e[1:,:]|=lb[1:,:]!=lb[:-1,:]
    rgb[e]=255
    img=Image.fromarray(rgb.clip(0,255).astype(np.uint8)); d=ImageDraw.Draw(img)
    d.line([(0,(500-y0)*f),(img.width,(500-y0)*f)],fill=(255,220,0)); d.line([((1000-x0)*f,0),((1000-x0)*f,img.height)],fill=(255,220,0))
    d.text((4,4),tk+" (gelb: Naht y500, Ausschnittrand x1000); cyan/magenta/orange/gruen = "+",".join(str(s)[-3:] for s in ids),fill=(255,255,0))
    out.append(img)
W=out[0].width; H=out[0].height
g=Image.new("RGB",(W,H*2+10)); g.paste(out[0],(0,0)); g.paste(out[1],(0,H+10))
if g.height>2000: g=g.resize((int(g.width*2000/g.height),2000))
g.save("einigung_10.jpg",quality=92); print(g.size)
