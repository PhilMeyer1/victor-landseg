import sys
from PIL import Image, ImageDraw
src = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png"
x0,y0,x1,y1,f,ziel = int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]),sys.argv[6]
im = Image.open(src).convert("RGB").crop((x0,y0,x1,y1))
im = im.resize(((x1-x0)*f,(y1-y0)*f), Image.NEAREST)
d = ImageDraw.Draw(im)
if y0 < 500 < y1:
    y=(500-y0)*f
    for xx in range(0, im.width, 12): d.line([(xx,y),(xx+5,y)], fill=(255,220,0), width=1)
for gx in range(((x0//20)+1)*20, x1, 20):
    d.text(((gx-x0)*f+2, 2), str(gx), fill=(255,255,0))
for gy in range(((y0//20)+1)*20, y1, 20):
    d.text((2,(gy-y0)*f+2), str(gy), fill=(255,255,0))
im.save(ziel, quality=92)
