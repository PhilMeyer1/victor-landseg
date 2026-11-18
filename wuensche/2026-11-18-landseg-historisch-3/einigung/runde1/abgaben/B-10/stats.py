import numpy as np, tifffile
from PIL import Image
B="C:/Users/Phil/Developement/Victor/daten/landseg/H0/"
im=np.array(Image.open(B+"H0.png").convert("L")).astype(float)
for tk,ox,oy,ids in [("r0c1",436,-64,[200363,200112,200350,200111,200124,200123,200110,200125]),("r1c1",436,436,[400011,400050,400042,400041,400055,400029,400057])]:
    L=tifffile.imread(B+f"b-kategorien-frei/{tk}/labels.tif")
    H,W=L.shape
    sub=im[max(oy,0):oy+H, ox:ox+W]
    Lc=L[max(oy,0)-oy:, :sub.shape[1]][:sub.shape[0]]
    for i in ids:
        m=Lc==i
        ys,xs=np.nonzero(m)
        v=sub[m]
        print(tk,i,m.sum(),"x",xs.min()+ox,xs.max()+ox,"y",ys.min()+max(oy,0),ys.max()+max(oy,0),"mean %.0f med %.0f p10 %.0f p90 %.0f"%(v.mean(),np.median(v),np.percentile(v,10),np.percentile(v,90)))
