import json, sys, numpy as np
from PIL import Image, ImageDraw, ImageFont
F=ImageFont.truetype("C:/Windows/Fonts/arial.ttf",15)
import tifffile
D='C:/Users/Phil/Developement/Victor/daten/landseg/H0'
O='C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde1/abgaben/A-07'
A='C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde1/auftraege-A/A-07/auftrag.json'
m=json.load(open(D+'/manifest.json',encoding='utf-8'))
img=np.array(Image.open(D+'/H0.png').convert('L')).astype(float)
tk={t['id']:t for t in m['teilkacheln']}
a=json.load(open(A,encoding='utf-8'))
nr=int(sys.argv[1]); r=int(sys.argv[2]); z=int(sys.argv[3])
p=a['paare'][nr-1]; cx,cy=p['strecken'][0]['von']
x0,y0=max(cx-r,0),max(cy-r,0); x1,y1=min(cx+r,1000),min(cy+r,1000)
crop=img[y0:y1,x0:x1]
lo,hi=np.percentile(crop,1),np.percentile(crop,99)
c8=np.clip((crop-lo)/(hi-lo)*255,0,255).astype(np.uint8)
masks=[]
for sg in p['segmente']:
    l=tifffile.imread(f"{D}/a-alles-frei/{sg['teilkachel']}/labels.tif"); c=tk[sg['teilkachel']]['kontext']
    full=np.zeros((1000,1000),bool)
    sub=(l==sg['id']); ys,xs=np.nonzero(sub); X=xs+c['x'];Y=ys+c['y']; ok=(X>=0)&(Y>=0)&(X<1000)&(Y<1000)
    full[Y[ok],X[ok]]=True; masks.append(full[y0:y1,x0:x1])
h,w=c8.shape
left=Image.fromarray(c8).resize((w*z,h*z),Image.NEAREST).convert('RGB')
right=left.copy(); d=ImageDraw.Draw(right)
cols=[(0,255,255),(255,0,255)]
for mk,col in zip(masks,cols):
    e=mk & ~(np.roll(mk,1,0)&np.roll(mk,-1,0)&np.roll(mk,1,1)&np.roll(mk,-1,1))
    for yy,xx in zip(*np.nonzero(e)):
        d.rectangle([xx*z+z//3,yy*z+z//3,xx*z+2*z//3,yy*z+2*z//3],fill=col)
d.ellipse([(cx-x0)*z-6,(cy-y0)*z-6,(cx-x0)*z+6,(cy-y0)*z+6],outline=(255,255,0),width=2)
out=Image.new('RGB',(w*z*2+10,h*z+30),(20,20,20))
out.paste(left,(0,30)); out.paste(right,(w*z+10,30))
ImageDraw.Draw(out).text((5,8),f"Paar {nr}: Ausschnitt x {x0}-{x1}, y {y0}-{y1}, {z}-fach, Kontrast gespreizt; Rand türkis={p['segmente'][0]['segment']}, magenta={p['segmente'][1]['segment']}, gelb: Berührstelle",fill=(255,255,0),font=F)
out.save(f'{O}/einigung_{nr:02d}.jpg',quality=90)
print(out.size)
