import numpy as np, tifffile, json
from PIL import Image
D="C:/Users/Phil/Developement/Victor/daten/landseg/H0/"
H=np.array(Image.open(D+"H0.png").convert("L")).astype(float)
L0=tifffile.imread(D+"a-alles-frei/r0c1/labels.tif"); L1=tifffile.imread(D+"a-alles-frei/r1c1/labels.tif")
G=np.zeros(H.shape,dtype=np.int64)
G[0:500,500:1000]=L0[64:564,64:564]; G[500:1000,500:1000]=L1[64:564,64:564]
S1={s['id']:s for s in json.load(open(D+"a-alles-frei/r1c1/segmente.json",encoding='utf-8'))['segmente']}
S0={s['id']:s for s in json.load(open(D+"a-alles-frei/r0c1/segmente.json",encoding='utf-8'))['segmente']}
for s in [201233,400138,400141,201236,400144,201241,400146,201120,400149,400152,201128,400156]:
    m=G==s; ys,xs=np.nonzero(m)
    print(s, 'kern px',m.sum(),'mittel %.0f'%H[m].mean(),'std %.0f'%H[m].std(),'x',xs.min(),xs.max(),'y',ys.min(),ys.max())
# Zeilen 497..503 Segmente x 780..910
for y in range(496,505):
    row=G[y,780:910]; 
    out=[];prev=None
    for i,v in enumerate(row):
        if v!=prev: out.append((780+i,int(v))); prev=v
    print(y,out)
for sid in set(G[500:530,790:910].ravel()):
    s=S1.get(int(sid)) or S0.get(int(sid))
    print(sid, s and (s.get('klasse'),s.get('name'), s.get('quelle')))
