import json, numpy as np
from PIL import Image
import tifffile
D='C:/Users/Phil/Developement/Victor/daten/landseg/H0'
A='C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/einigung/runde1/auftraege-A/A-07/auftrag.json'
m=json.load(open(D+'/manifest.json',encoding='utf-8'))
img=np.array(Image.open(D+'/H0.png').convert('L')).astype(float)
tk={t['id']:t for t in m['teilkacheln']}
lab={}
def L(t):
    if t not in lab:
        l=tifffile.imread(f'{D}/a-alles-frei/{t}/labels.tif')
        c=tk[t]['kontext']
        lab[t]=(l,c)
    return lab[t]
a=json.load(open(A,encoding='utf-8'))
for p in a['paare']:
    print('Paar',p['nr'],p['paar'])
    s=p['strecken'][0]; cx,cy=s['von']
    for sg in p['segmente']:
        l,c=L(sg['teilkachel'])
        mask=(l==sg['id'])
        ys,xs=np.nonzero(mask)
        X=xs+c['x'];Y=ys+c['y']
        ok=(X>=0)&(Y>=0)&(X<1000)&(Y<1000)
        g=img[Y[ok],X[ok]]
        near=ok&(abs(X-cx)<=4)&(abs(Y-cy)<=4)
        gn=img[Y[near],X[near]]
        print('  ',sg['segment'],sg['klasse'],'mittel %.0f sd %.0f n=%d | nahe %.0f (n=%d) bbox x%d-%d y%d-%d'%(g.mean(),g.std(),len(g),gn.mean() if len(gn) else -1,len(gn),X.min(),X.max(),Y.min(),Y.max()))
