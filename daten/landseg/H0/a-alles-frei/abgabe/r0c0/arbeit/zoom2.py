import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import tifffile
import scipy.ndimage as ndi
B = 'C:/Users/Phil/Developement/Victor/daten/landseg/H0/'
img = np.array(Image.open(B + 'teilkacheln/r0c0.png'))
if img.ndim == 3: img = img[..., 0]
img = ndi.gaussian_filter(img.astype(float), 0.7)
def crop(x0, y0, w, h, s, out, labels=None, names=None):
    sub = img[y0:y0+h, x0:x0+w]
    lo, hi = np.percentile(sub, 0.5), np.percentile(sub, 99.5)
    sub = np.clip((sub - lo) / (hi - lo) * 255, 0, 255).astype(np.uint8)
    im = Image.fromarray(sub).resize((w*s, h*s), Image.BICUBIC).convert('RGB')
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype('arial.ttf', 12)
    if labels is not None:
        L = labels[y0:y0+h, x0:x0+w]
        big = np.kron(L, np.ones((s, s), L.dtype))
        e = np.zeros_like(big, bool)
        e[:, 1:] |= big[:, 1:] != big[:, :-1]
        e[1:, :] |= big[1:, :] != big[:-1, :]
        a = np.array(im); a[e] = (255, 220, 0); im = Image.fromarray(a); d = ImageDraw.Draw(im)
        if names:
            for i in np.unique(L):
                ys, xs = np.nonzero(L == i)
                if len(xs) < 15: continue
                k = len(xs) // 2
                order = np.lexsort((xs, ys)); cy, cx = ys[order[k]], xs[order[k]]
                d.text((cx*s, cy*s), str(names.get(int(i), i)), fill=(255, 60, 60), font=f)
    for gx in range((x0 // 10 + 1) * 10, x0 + w, 10):
        for gy in range((y0 // 10 + 1) * 10, y0 + h, 10):
            X, Y = (gx - x0) * s, (gy - y0) * s
            c = (255, 0, 255) if (gx % 50 == 0 and gy % 50 == 0) else (0, 230, 230)
            d.point([(X, Y), (X+1, Y), (X, Y+1), (X-1, Y), (X, Y-1)], fill=c)
    for gx in range((x0 // 20 + 1) * 20, x0 + w, 20):
        d.text(((gx - x0) * s - 8, 1), str(gx), fill=(0, 255, 255), font=f)
        d.text(((gx - x0) * s - 8, h*s - 14), str(gx), fill=(0, 255, 255), font=f)
    for gy in range((y0 // 20 + 1) * 20, y0 + h, 20):
        d.text((1, (gy - y0) * s - 6), str(gy), fill=(0, 255, 255), font=f)
        d.text((w*s - 24, (gy - y0) * s - 6), str(gy), fill=(0, 255, 255), font=f)
    im.save(out, quality=90)
if __name__ == '__main__':
    x0, y0, w, h, s = map(int, sys.argv[1:6])
    lab = tifffile.imread(sys.argv[7]) if len(sys.argv) > 7 else None
    crop(x0, y0, w, h, s, sys.argv[6], lab)
