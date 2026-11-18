import sys, numpy as np
from PIL import Image
import tifffile
D='C:/Users/Phil/Developement/Victor/daten/landseg/H0/'
img=np.array(Image.open(D+'H0.png').convert('L')).astype(int)
lab=tifffile.imread(D+'c-feste-liste/zusammen/labels.tif')
x0,x1,y0,y1=map(int,sys.argv[1:5])
ids=sorted(set(lab[y0:y1,x0:x1].ravel().tolist()))
code={s:chr(65+i) if i<26 else chr(97+i-26) for i,s in enumerate(ids)}
print({code[s]:s for s in ids})
print('     '+''.join(f'{x:>5}' for x in range(x0,x1)))
for y in range(y0,y1):
    print(f'{y:>4} '+''.join(f'{img[y,x]:>4}{code[lab[y,x]]}' for x in range(x0,x1)))
for s in ids:
    m=lab==s
    print(s, 'mean', round(img[m].mean(),1), 'n', int(m.sum()))
