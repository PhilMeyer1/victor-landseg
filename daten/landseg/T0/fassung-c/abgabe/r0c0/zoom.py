import sys, json
import numpy as np, cv2
sys.path.insert(0, 'C:/Users/Phil/Developement/Victor/landseg')
from landseg.dateien import lese_labels
from PIL import Image
# usage: zoom.py labels.tif out_prefix x0 y0 w h scale [offset]
lab, out, x0, y0, w, h, sc = sys.argv[1], sys.argv[2], *map(int, sys.argv[3:8])
off = int(sys.argv[8]) if len(sys.argv) > 8 else 0
L = lese_labels(lab)
img = np.asarray(Image.open('C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c/teilkacheln/r0c0.png').convert('RGB'))
crop = img[y0:y0+h, x0:x0+w]
big = cv2.resize(crop, (w*sc, h*sc), interpolation=cv2.INTER_CUBIC)
Image.fromarray(big).save(out + '_roh.jpg', quality=92)
Lc = L[y0:y0+h, x0:x0+w]
Lb = cv2.resize(Lc.astype(np.float32), (w*sc, h*sc), interpolation=cv2.INTER_NEAREST).astype(np.int64)
edge = np.zeros(Lb.shape, bool)
edge[:-1] |= Lb[:-1] != Lb[1:]; edge[:, :-1] |= Lb[:, :-1] != Lb[:, 1:]
ov = big.copy(); ov[edge] = (255, 255, 0)
# kern rectangle 64..564
kx0, ky0 = (64-x0)*sc, (64-y0)*sc; kx1, ky1 = (564-x0)*sc, (564-y0)*sc
cv2.rectangle(ov, (kx0, ky0), (kx1, ky1), (0, 255, 255), 1)
for i in np.unique(Lc):
    m = Lc == i
    # place label at point farthest from boundary
    d = cv2.distanceTransform(np.pad(m, 1).astype(np.uint8), cv2.DIST_L2, 3)[1:-1, 1:-1]
    yy, xx = np.unravel_index(d.argmax(), d.shape)
    t = str(int(i) - off)
    p = (int(xx*sc+sc/2) - 6*len(t), int(yy*sc+sc/2) + 5)
    cv2.putText(ov, t, p, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 3)
    cv2.putText(ov, t, p, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
Image.fromarray(ov).save(out + '_nr.jpg', quality=92)
