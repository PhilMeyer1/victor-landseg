import json,sys
import numpy as np
from PIL import Image, ImageDraw
import tifffile
D='C:/Users/Phil/Developement/Victor/daten/landseg/H0'
B='C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei'
OUT='C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde1/abgaben/B-12'
a=json.load(open('C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde1/auftraege-B/B-12/auftrag.json',encoding='utf-8'))
img=np.array(Image.open(D+'/H0.png').convert('L'))
off={'r0c0':(-64,-64),'r0c1':(436,-64),'r1c0':(-64,436),'r1c1':(436,436)}
labs={}
def lab(t):
    if t not in labs:
        L=tifffile.imread(B+'/'+t+'/labels.tif')
        full=np.zeros(img.shape,dtype=np.int64)
        ox,oy=off[t]
        x0,y0=max(ox,0),max(oy,0)
        x1,y1=min(ox+L.shape[1],1000),min(oy+L.shape[0],1000)
        full[y0:y1,x0:x1]=L[y0-oy:y1-oy,x0-ox:x1-ox]
        labs[t]=full
    return labs[t]
R=int(sys.argv[2]) if len(sys.argv)>2 else 60
S=int(sys.argv[3]) if len(sys.argv)>3 else 6
for p in a['paare']:
    if str(p['nr']) not in sys.argv[1].split(','): continue
    s=p['strecken'][0]; cx,cy=s['von']
    x0,y0=max(cx-R,0),max(cy-R,0); x1,y1=min(cx+R,1000),min(cy+R,1000)
    c=img[y0:y1,x0:x1]
    # contrast stretch
    lo,hi=np.percentile(c,1),np.percentile(c,99)
    c2=np.clip((c.astype(float)-lo)/(hi-lo+1e-6)*255,0,255).astype(np.uint8)
    raw=Image.fromarray(c2).resize(((x1-x0)*S,(y1-y0)*S),Image.NEAREST).convert('RGB')
    ov=raw.copy(); d=ImageDraw.Draw(ov)
    cols=[(0,230,230),(255,0,255)]
    for seg,col in zip(p['segmente'],cols):
        m=(lab(seg['teilkachel'])[y0:y1,x0:x1]==seg['id'])
        e=m & ~(np.roll(m,1,0)&np.roll(m,-1,0)&np.roll(m,1,1)&np.roll(m,-1,1))
        for yy,xx in zip(*np.nonzero(e)):
            d.rectangle([xx*S,yy*S,xx*S+S-1,yy*S+S-1],outline=col)
    for st in p['strecken']:
        (ax,ay),(bx,by)=st['von'],st['bis']
        d.rectangle([(ax-x0)*S-2,(ay-y0)*S-2,(bx-x0+1)*S+1,(by-y0+1)*S+1],outline=(255,255,0),width=2)
    W=raw.width
    out=Image.new('RGB',(2*W+10,raw.height+30),(20,20,20))
    out.paste(raw,(0,30)); out.paste(ov,(W+10,30))
    ImageDraw.Draw(out).text((5,5),f"Paar {p['nr']}: x {x0}-{x1}, y {y0}-{y1}, {S}-fach, Kontrast gestreckt; tuerkis {p['segmente'][0]['segment']}, magenta {p['segmente'][1]['segment']}",fill=(255,255,0))
    if out.width>2000:
        f=2000/out.width; out=out.resize((2000,int(out.height*f)))
    out.save(OUT+f"/einigung_{p['nr']:02d}.jpg",quality=90)
    print('ok',p['nr'])
