import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import scipy.ndimage as ndi
from rect import img
def make(P0, T, N, u0, u1, v0, v1, s, out):
    P0 = np.array(P0, float); T = np.array(T, float); N = np.array(N, float)
    us = np.arange(u0, u1, 1/s); vs = np.arange(v0, v1, 1/s)
    U, V = np.meshgrid(us, vs)
    XY = P0 + np.multiply.outer(U, T) + np.multiply.outer(V, N)
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
if __name__ == '__main__':
    a = sys.argv[1:]
    make(eval(a[0]), eval(a[1]), eval(a[2]), *map(int, a[3:8]), a[8])
