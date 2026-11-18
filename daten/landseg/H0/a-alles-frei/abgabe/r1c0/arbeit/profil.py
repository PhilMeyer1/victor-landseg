import numpy as np
from PIL import Image
from scipy import ndimage as ndi
b = np.array(Image.open(r"C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r1c0.png")).astype(float)
if b.ndim==3: b=b[...,0]
b=ndi.gaussian_filter(b,1.5)
Y,X=np.mgrid[0:628,0:628]
d=np.array([0.81231158,-0.58322371]); n=np.array([0.58322371,0.81231158])
t=X*d[0]+Y*d[1]; u=X*n[0]+Y*n[1]
def L3t(uu): return -12.6+(uu-394)*(-54.4/312)
def L4t(uu): return 218+(uu-390)*(-83/480)
# F-mid: between L3 and L4
for name,m in [("Fmid_west", (t>L3t(u)+5)&(t<(L3t(u)+L4t(u))/2)), ("Fmid_ost",(t>=(L3t(u)+L4t(u))/2)&(t<L4t(u)-5)), ("Fsw",(t<L3t(u)-5)&(t>L3t(u)-200)), ("Fost",(t>L4t(u)+5))]:
    print(name)
    row=[]
    for u0 in range(396,880,6):
        mm=m&(u>=u0)&(u<u0+6)
        if mm.sum()>30: row.append(f"{u0}:{b[mm].mean():.0f}")
    print(" ".join(row))
