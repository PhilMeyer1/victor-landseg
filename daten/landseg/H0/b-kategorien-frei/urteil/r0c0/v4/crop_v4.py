import sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage
lab = np.array(Image.open("C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r0c0/labels.tif"))
img = np.array(Image.open("C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r0c0.png").convert("L"))
def crop(x0,y0,w,h,f,out,title,kontrast=False):
    a = img[y0:y0+h, x0:x0+w].astype(float)
    if kontrast:
        lo,hi=np.percentile(a,2),np.percentile(a,98); a=np.clip((a-lo)/(hi-lo)*255,0,255)
    l = lab[y0:y0+h, x0:x0+w]
    big = np.kron(a, np.ones((f,f))).astype(np.uint8)
    rgb = np.stack([big]*3,-1)
    lb = np.kron(l, np.ones((f,f),dtype=l.dtype))
    edge = np.zeros(lb.shape,bool)
    edge[:,1:] |= lb[:,1:]!=lb[:,:-1]; edge[1:,:] |= lb[1:,:]!=lb[:-1,:]
    rgb[edge]=[255,230,0]
    im=Image.fromarray(rgb); d=ImageDraw.Draw(im)
    try: font=ImageFont.truetype("arial.ttf",16)
    except: font=ImageFont.load_default()
    for i in np.unique(l):
        m=(l==i)
        if m.sum()<15: continue
        dist=ndimage.distance_transform_edt(np.pad(m,1))[1:-1,1:-1]
        yy,xx=np.unravel_index(dist.argmax(),m.shape)
        t=str(i%100000); d.text((xx*f-8,yy*f-8),t,fill=(255,255,255),font=font,stroke_width=2,stroke_fill=(0,0,0))
    # Kern-/Viertelgrenze
    for v in (314,564):
        if x0<=v<x0+w: d.line([((v-x0)*f,0),((v-x0)*f,h*f)],fill=(0,255,255),width=2)
        if y0<=v<y0+h: d.line([(0,(v-y0)*f),(w*f,(v-y0)*f)],fill=(0,255,255),width=2)
    d.rectangle([0,0,im.width,24],fill=(0,0,0)); d.text((4,3),title+f" (x {x0}–{x0+w-1}, y {y0}–{y0+h-1}, {f}fach)",fill=(255,255,0),font=font)
    im.save(out,quality=90)
crop(490,300,90,100,6,"nah_4.jpg","Nahansicht 4: Höfe östlich der Einmündung 143/178/186/189/165")
crop(350,500,80,80,7,"nah_5.jpg","Nahansicht 5: Feldecke unten links 216/220/224/225")
crop(330,380,180,130,5,"kontrast_2.jpg","Kontrast 2: Grenze Feld 154/195 und Baumreihe 183",kontrast=True)
