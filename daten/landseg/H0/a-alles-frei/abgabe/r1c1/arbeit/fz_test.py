import sys
import numpy as np
from PIL import Image, ImageDraw
from skimage.segmentation import felzenszwalb, find_boundaries
from skimage.filters import gaussian

BILD = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r1c1.png"
img = np.array(Image.open(BILD).convert("L")).astype(np.float32) / 255.0
scale = float(sys.argv[1]); sigma = float(sys.argv[2]); mins = int(sys.argv[3])
seg = felzenszwalb(img, scale=scale, sigma=sigma, min_size=mins)
print("segmente", seg.max() + 1)
b = find_boundaries(seg, mode="inner")
rgb = np.stack([img * 255] * 3, -1).astype(np.uint8)
rgb[b] = (255, 220, 0)
big = Image.fromarray(rgb).resize((1256, 1256), Image.NEAREST)
big.save(sys.argv[4], quality=90)
np.save(sys.argv[4] + ".npy", seg)
