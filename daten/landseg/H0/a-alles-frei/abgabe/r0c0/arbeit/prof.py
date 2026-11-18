import sys
import numpy as np
from PIL import Image
import scipy.ndimage as ndi
img = np.array(Image.open('C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r0c0.png')).astype(float)
if img.ndim == 3: img = img[..., 0]
img = ndi.gaussian_filter(img, 1.0)
args = sys.argv[1:]
for a in args:
    x0, y0, x1, y1 = map(float, a.split(','))
    n = int(max(abs(x1-x0), abs(y1-y0))) + 1
    xs = np.linspace(x0, x1, n); ys = np.linspace(y0, y1, n)
    v = ndi.map_coordinates(img, [ys, xs], order=1)
    print(a, ' '.join(f'{int(x)},{int(y)}:{int(t)}' for x, y, t in zip(xs[::2], ys[::2], v[::2])))
