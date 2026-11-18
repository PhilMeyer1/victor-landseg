import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import scipy.ndimage as ndi
img = np.array(Image.open('C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r0c0.png')).astype(float)
if img.ndim == 3: img = img[..., 0]
img = ndi.gaussian_filter(img, 0.7)
P0 = np.array([193.0, 0.0]); T = np.array([-0.622, 0.783]); N = np.array([0.783, 0.622])
def to_xy(u, v):
    return P0 + np.multiply.outer(u, T) + np.multiply.outer(v, N)
if __name__ == '__main__':
    u0, u1, v0, v1, s = map(int, sys.argv[1:6]); out = sys.argv[6]
    us = np.arange(u0, u1, 1/s); vs = np.arange(v0, v1, 1/s)
    U, V = np.meshgrid(us, vs)
    XY = to_xy(U, V)
    val = ndi.map_coordinates(img, [XY[..., 1], XY[..., 0]], order=1, cval=0)
    lo, hi = np.percentile(val, 0.5), np.percentile(val, 99.5)
    im = Image.fromarray(np.clip((val - lo) / (hi - lo) * 255, 0, 255).astype(np.uint8)).convert('RGB')
    d = ImageDraw.Draw(im); f = ImageFont.truetype('arial.ttf', 12)
    for u in range((u0 // 10 + 1) * 10, u1, 10):
        for v in range((v0 // 10 + 1) * 10, v1, 10):
            X, Y = (u - u0) * s, (v - v0) * s
            d.point([(X, Y), (X+1, Y), (X-1, Y), (X, Y+1), (X, Y-1)], fill=(0, 230, 230))
    for u in range((u0 // 20 + 1) * 20, u1, 20):
        d.text(((u - u0) * s - 8, 1), str(u), fill=(0, 255, 255), font=f)
    for v in range((v0 // 20 + 1) * 20, v1, 20):
        d.text((1, (v - v0) * s - 6), str(v), fill=(0, 255, 255), font=f)
    im.save(out, quality=90)
