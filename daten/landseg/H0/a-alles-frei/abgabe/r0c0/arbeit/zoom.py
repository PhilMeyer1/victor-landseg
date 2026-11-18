import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import tifffile
B = 'C:/Users/Phil/Developement/Victor/daten/landseg/H0/'
img = np.array(Image.open(B + 'teilkacheln/r0c0.png'))
if img.ndim == 3: img = img[..., 0]
import scipy.ndimage as ndi
img = ndi.gaussian_filter(img.astype(float), 0.8)
def crop(x0, y0, w, h, s, out, labels=None, grid=10):
    sub = img[y0:y0+h, x0:x0+w]
    # contrast stretch
    lo, hi = np.percentile(sub, 1), np.percentile(sub, 99)
    sub = np.clip((sub.astype(float) - lo) / (hi - lo) * 255, 0, 255).astype(np.uint8)
    im = Image.fromarray(sub).resize((w*s, h*s), Image.NEAREST if s >= 4 else Image.BICUBIC).convert('RGB')
    d = ImageDraw.Draw(im)
    if labels is not None:
        L = labels[y0:y0+h, x0:x0+w]
        e = np.zeros_like(L, bool)
        e[:, 1:] |= L[:, 1:] != L[:, :-1]
        e[1:, :] |= L[1:, :] != L[:-1, :]
        ys, xs = np.nonzero(e)
        for yy, xx in zip(ys, xs):
            d.rectangle([xx*s, yy*s, xx*s+s-1, yy*s+s-1], outline=None, fill=(255, 230, 0))
    try:
        f = ImageFont.truetype('arial.ttf', 13)
    except Exception:
        f = None
    for gx in range((x0 // grid + 1) * grid, x0 + w, grid):
        X = (gx - x0) * s
        d.line([X, 0, X, h*s], fill=(0, 200, 200) if gx % 50 else (255, 0, 255), width=1)
        (gx % 20 == 0) and d.text((X + 2, 2), str(gx), fill=(0, 255, 255), font=f)
    for gy in range((y0 // grid + 1) * grid, y0 + h, grid):
        Y = (gy - y0) * s
        d.line([0, Y, w*s, Y], fill=(0, 200, 200) if gy % 50 else (255, 0, 255), width=1)
        (gy % 20 == 0) and d.text((2, Y + 2), str(gy), fill=(0, 255, 255), font=f)
    im.save(out, quality=90)
if __name__ == '__main__':
    x0, y0, w, h, s = map(int, sys.argv[1:6])
    out = sys.argv[6]
    lab = tifffile.imread(sys.argv[7]) if len(sys.argv) > 7 else None
    crop(x0, y0, w, h, s, out, lab)
