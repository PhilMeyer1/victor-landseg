import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
bild = np.array(Image.open(r"C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r1c0.png"))
if bild.ndim == 3: bild = bild[..., 0]
x0, y0, x1, y1, s = map(int, sys.argv[1:6]); out = sys.argv[6]
kontrast = len(sys.argv) > 7
crop = bild[y0:y1, x0:x1].astype(float)
if kontrast:
    lo, hi = np.percentile(crop, 1), np.percentile(crop, 99)
    crop = np.clip((crop - lo) / (hi - lo) * 255, 0, 255)
im = Image.fromarray(crop.astype(np.uint8)).resize(((x1-x0)*s, (y1-y0)*s), Image.NEAREST if s >= 4 else Image.BICUBIC).convert("RGB")
d = ImageDraw.Draw(im)
try: f = ImageFont.truetype("arial.ttf", 14)
except Exception: f = None
step = 25 if (x1-x0) > 120 else 10
for gx in range((x0//step+1)*step, x1, step):
    X = (gx-x0)*s; d.line([(X,0),(X,im.height)], fill=(0,200,255) if gx%50==0 else (0,110,140), width=1); d.text((X+2,2), str(gx), fill=(255,255,0), font=f)
for gy in range((y0//step+1)*step, y1, step):
    Y = (gy-y0)*s; d.line([(0,Y),(im.width,Y)], fill=(0,200,255) if gy%50==0 else (0,110,140), width=1); d.text((2,Y+2), str(gy), fill=(255,255,0), font=f)
im.save(out, quality=90)
