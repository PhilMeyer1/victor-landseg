import json,os,numpy as np,tifffile
from PIL import Image,ImageDraw,ImageFont
from scipy import ndimage as ndi
B='C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/'
m=json.load(open(B+'manifest.json'))
F=2
font=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',16)
big=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf',40)
for t in m['teilkacheln']:
    tk=t['id'];o=B+'ganz/'+tk+'/';os.makedirs(o,exist_ok=True)
    im=Image.open(B+t['bild']).convert('RGB');W,H=im.size
    im.resize((W*F,H*F),Image.NEAREST).save(o+'ganz_roh.jpg',quality=90)
    k=t['kern_im_bild'];x0,y0=k['x'],k['y'];x1,y1=x0+k['breite'],y0+k['hoehe']
    L=tifffile.imread(B+'vorstufe/%s/labels.tif'%tk)
    a=np.array(im).astype(float)
    msk=np.zeros((H,W),bool);msk[y0:y1,x0:x1]=True
    a[~msk]*=0.6
    bd=np.zeros((H,W),bool)
    bd[:,1:]|=L[:,1:]!=L[:,:-1];bd[1:,:]|=L[1:,:]!=L[:-1,:]
    a[bd]=[255,255,0]
    big_im=Image.fromarray(a.astype(np.uint8)).resize((W*F,H*F),Image.NEAREST)
    d=ImageDraw.Draw(big_im)
    d.rectangle([x0*F,y0*F,x1*F-1,y1*F-1],outline='white',width=3)
    mx,my=(x0+x1)//2,(y0+y1)//2
    v={'v1':[x0,y0,mx,my],'v2':[mx,y0,x1,my],'v3':[x0,my,mx,y1],'v4':[mx,my,x1,y1]}
    for n,r in v.items():
        d.rectangle([r[0]*F,r[1]*F,r[2]*F-1,r[3]*F-1],outline='cyan',width=2)
        d.text((r[0]*F+8,r[1]*F+4),n,font=big,fill='cyan',stroke_width=3,stroke_fill='black')
    for sid in np.unique(L[y0:y1,x0:x1]):
        if sid==0:continue
        mk=L==sid
        if mk.sum()<40:continue
        dt=ndi.distance_transform_edt(np.pad(mk,1))[1:-1,1:-1]
        dt[~msk]=0
        if dt.max()<=0:continue
        y,x=np.unravel_index(dt.argmax(),dt.shape)
        d.text(((x+.5)*F,(y+.5)*F),str(int(sid)%100000),font=font,fill='white',stroke_width=2,stroke_fill='black',anchor='mm')
    big_im.save(o+'ganz_nummern.jpg',quality=90)
    json.dump({'tk':tk,'faktor':F,'kern_im_bild':[x0,y0,x1,y1],'viertel':v},open(o+'ganz.json','w'))
