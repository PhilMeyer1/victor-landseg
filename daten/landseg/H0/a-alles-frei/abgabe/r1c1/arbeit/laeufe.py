import sys
import numpy as np
from PIL import Image
from scipy import ndimage
a=np.array(Image.open('C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r1c1.png')).astype(float)
s=ndimage.gaussian_filter(a,1.5)
x0,x1,y0,y1,st=map(int,sys.argv[1:6]); thr=float(sys.argv[6]) if len(sys.argv)>6 else 140
for y in range(y0,y1,st):
    row=s[y,x0:x1]>thr
    runs=[];i=0
    while i<len(row):
        if row[i]:
            j=i
            while j<len(row) and row[j]: j+=1
            if j-i>=6: runs.append(f"{x0+i}-{x0+j-1}")
            i=j
        else: i+=1
    print(y, ' '.join(runs))
