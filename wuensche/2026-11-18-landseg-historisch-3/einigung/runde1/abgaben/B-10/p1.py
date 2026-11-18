import numpy as np
from PIL import Image
im=np.array(Image.open("C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png").convert("L")).astype(int)
for y in range(484,512):
    print(y," ".join("%3d"%im[y,x] for x in range(830,876,2)))
