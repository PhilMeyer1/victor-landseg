import sys, numpy as np, cv2
from PIL import Image
out, x0, y0, w, h, sc = sys.argv[1], *map(int, sys.argv[2:7])
step = int(sys.argv[7]) if len(sys.argv) > 7 else 10
img = np.asarray(Image.open('C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c/teilkacheln/r0c0.png').convert('RGB'))
big = cv2.resize(img[y0:y0+h, x0:x0+w], (w*sc, h*sc), interpolation=cv2.INTER_CUBIC)
for x in range((x0//step+1)*step, x0+w, step):
    X = (x-x0)*sc; cv2.line(big, (X, 0), (X, h*sc-1), (255,255,0), 1); cv2.putText(big, str(x), (X+2, 12), 0, 0.4, (255,255,0), 1)
for y in range((y0//step+1)*step, y0+h, step):
    Y = (y-y0)*sc; cv2.line(big, (0, Y), (w*sc-1, Y), (255,255,0), 1); cv2.putText(big, str(y), (2, Y-2), 0, 0.4, (255,255,0), 1)
Image.fromarray(big).save(out, quality=92)
