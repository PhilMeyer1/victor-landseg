import sys, numpy as np
from PIL import Image, ImageDraw
import tifffile
D='C:/Users/Phil/Developement/Victor/daten/landseg/H0/'
img=np.array(Image.open(D+'H0.png').convert('L'))
lab=tifffile.imread(D+'c-feste-liste/zusammen/labels.tif')
print(img.shape, lab.shape, lab.dtype)
def crop(name,x0,y0,x1,y1,ids,f):
    g=img[y0:y1,x0:x1]; L=lab[y0:y1,x0:x1]
    rgb=np.stack([g]*3,-1).astype(np.uint8)
    big=np.kron(rgb,np.ones((f,f,1),dtype=np.uint8))
    out=big.copy()
    cols=[(0,220,220),(255,0,255),(255,255,0),(0,255,0),(255,128,0),(80,160,255)]
    for i,sid in enumerate(ids):
        m=(L==sid)
        if not m.any(): print('missing',sid); continue
        e=m&~(np.roll(m,1,0)&np.roll(m,-1,0)&np.roll(m,1,1)&np.roll(m,-1,1))
        eb=np.kron(e,np.ones((f,f),dtype=bool))
        out[eb]=cols[i%len(cols)]
    # naht lines at 500
    im=Image.fromarray(np.concatenate([big,np.zeros((big.shape[0],6,3),np.uint8),out],1))
    d=ImageDraw.Draw(im)
    W=big.shape[1]+6
    if x0<500<x1: d.line([(W+(500-x0)*f,0),(W+(500-x0)*f,im.height)],fill=(255,60,60),width=1)
    if y0<500<y1: d.line([(W,(500-y0)*f),(im.width,(500-y0)*f)],fill=(255,60,60),width=1)
    im.save(name,quality=92); print(name, im.size)
    print(sid, [ (s,int((L==s).sum())) for s in ids])
import json
args=json.loads(sys.argv[1])
for a in args: crop(*a)
