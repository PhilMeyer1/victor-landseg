import sys
import numpy as np
from PIL import Image
img=np.array(Image.open("C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c/teilkacheln/r1c0.png").convert("RGB")).astype(float)
x0,y0,x1,y1,f=map(int,sys.argv[1:6])
c=img[y0:y1,x0:x1]
lo=np.percentile(c,1);hi=np.percentile(c,99)
c=np.clip((c-lo)/(hi-lo),0,1)**0.6*255
Image.fromarray(c.astype(np.uint8)).resize(((x1-x0)*f,(y1-y0)*f),Image.LANCZOS).save(sys.argv[6],quality=92)
