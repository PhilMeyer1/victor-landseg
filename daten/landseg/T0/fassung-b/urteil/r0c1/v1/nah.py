import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

B = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b"
O = "C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/urteil/r0c1/v1/"
lab = np.array(Image.open(B + "/vorstufe/r0c1/labels.tif")).astype(np.int64)
img = np.array(Image.open(B + "/teilkacheln/r0c1.png").convert("RGB"))

def mach(name, x0, y0, x1, y1, f, tint=(), kontrast=False):
    L = lab[y0:y1, x0:x1]
    I = img[y0:y1, x0:x1].astype(np.float32)
    if kontrast:
        lo = np.percentile(I, 2, axis=(0, 1)); hi = np.percentile(I, 98, axis=(0, 1))
        I = np.clip((I - lo) / (hi - lo) * 255, 0, 255)
    I = np.repeat(np.repeat(I, f, 0), f, 1)
    Lb = np.repeat(np.repeat(L, f, 0), f, 1)
    for t in tint:
        m = Lb == t
        I[m] = I[m] * 0.6 + np.array([255, 0, 255]) * 0.4
    edge = np.zeros(Lb.shape, bool)
    edge[:, 1:] |= Lb[:, 1:] != Lb[:, :-1]
    edge[1:, :] |= Lb[1:, :] != Lb[:-1, :]
    I[edge] = [255, 255, 0]
    im = Image.fromarray(I.astype(np.uint8))
    d = ImageDraw.Draw(im)
    try:
        fo = ImageFont.truetype("arial.ttf", 16)
    except Exception:
        fo = ImageFont.load_default()
    # quarter outline
    qx0, qy0, qx1, qy1 = [(64 - x0) * f, (64 - y0) * f, (314 - x0) * f, (314 - y0) * f]
    d.rectangle([qx0, qy0, qx1, qy1], outline=(0, 255, 255), width=2)
    for i in np.unique(L):
        m = L == i
        if m.sum() < 15:
            continue
        dt = ndimage.distance_transform_edt(np.pad(m, 1))[1:-1, 1:-1]
        yy, xx = np.unravel_index(np.argmax(dt), dt.shape)
        t = str(i % 100000)
        d.text((xx * f + f // 2, yy * f + f // 2), t, fill=(255, 255, 255), font=fo, anchor="mm", stroke_width=2, stroke_fill=(0, 0, 0))
    # grid ticks every 10 px
    for gx in range((x0 // 10 + 1) * 10, x1, 10):
        d.text(((gx - x0) * f, 2), str(gx), fill=(0, 255, 255), font=fo, stroke_width=2, stroke_fill=(0, 0, 0))
    for gy in range((y0 // 10 + 1) * 10, y1, 10):
        d.text((2, (gy - y0) * f), str(gy), fill=(0, 255, 255), font=fo, stroke_width=2, stroke_fill=(0, 0, 0))
    im.save(O + name, quality=90)

if __name__ == "__main__":
    a = sys.argv
    tint = [int(t) for t in a[7].split(",")] if len(a) > 7 and a[7] else []
    mach(a[1], int(a[2]), int(a[3]), int(a[4]), int(a[5]), int(a[6]), tint, kontrast=(len(a) > 8 and a[8] == "k"))
