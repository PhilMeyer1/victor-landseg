import numpy as np, cv2, tifffile, sys, json
D='C:/Users/Phil/Developement/Victor/daten/landseg/H0/'
img=cv2.imread(D+'H0.png',cv2.IMREAD_GRAYSCALE)
L=np.zeros((1000,1000),np.int64)
kl={}
for t,ox in (('r0c0',0),('r0c1',500)):
    l=tifffile.imread(D+'a-alles-frei/'+t+'/labels.tif').astype(np.int64)
    L[0:500,ox:ox+500]=l[64:564,64:564]
    for s in json.load(open(D+'a-alles-frei/'+t+'/segmente.json',encoding='utf-8'))['segmente']:
        kl[s['id']]=s['klasse']
x0,x1,y0,y1,s=[int(a) for a in sys.argv[1:6]]; out=sys.argv[6]
cr=img[y0:y1,x0:x1]; lc=L[y0:y1,x0:x1]
big=cv2.resize(cr,None,fx=s,fy=s,interpolation=cv2.INTER_CUBIC)
raw=cv2.cvtColor(big,cv2.COLOR_GRAY2BGR); ov=raw.copy()
lb=np.kron(lc,np.ones((s,s),np.int64))
e=(np.diff(lb,axis=0,prepend=lb[:1])!=0)|(np.diff(lb,axis=1,prepend=lb[:,:1])!=0)
ov[e]=(0,0,255)
if x0<500<x1: ov[:,(500-x0)*s]=(0,255,255)
for idv in np.unique(lc):
    ys,xs=np.nonzero(lc==idv)
    if len(ys)<6: continue
    # point closest to centroid within segment
    cy,cx=ys.mean(),xs.mean(); k=np.argmin((ys-cy)**2+(xs-cx)**2)
    txt=f"{idv%1000}:{kl.get(idv,'?')}"
    cv2.putText(ov,txt,(int(xs[k]*s)-20,int(ys[k]*s)+4),cv2.FONT_HERSHEY_SIMPLEX,0.4,(0,255,0),1)
o=np.concatenate([raw,np.zeros((raw.shape[0],8,3),np.uint8),ov],1)
cv2.putText(o,f"x {x0}-{x1} y {y0}-{y1} {s}x",(5,15),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,255),1)
cv2.imwrite(out,o,[cv2.IMWRITE_JPEG_QUALITY,90]); print(o.shape)
