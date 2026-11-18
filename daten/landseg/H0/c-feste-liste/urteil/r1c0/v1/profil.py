"""profil.py a b [x0,y0,x1,y1] : mittlerer Grauwert nach Abstand zur Grenze a|b (negativ = in a)."""
import sys
import numpy as np
from PIL import Image
import tifffile
from scipy import ndimage as ndi

B = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/"
lab = tifffile.imread(B + "c-feste-liste/r1c0/labels.tif").astype(np.int64)
img = np.array(Image.open(B + "teilkacheln/r1c0.png").convert("L")).astype(float)
img = ndi.uniform_filter(img, 3)
a, b = int(sys.argv[1]), int(sys.argv[2])
box = [int(v) for v in sys.argv[3].split(",")] if len(sys.argv) > 3 else [0, 0, 628, 628]
ma, mb = lab == a, lab == b
da = ndi.distance_transform_edt(~mb)  # distance to b for pixels in a
db = ndi.distance_transform_edt(~ma)
sel = np.zeros_like(ma); sel[box[1]:box[3], box[0]:box[2]] = True
out = []
for d in range(1, 16):
    ia = ma & sel & (np.abs(da - d) < 0.5)
    ib = mb & sel & (np.abs(db - d) < 0.5)
    out.append((d, img[ia].mean() if ia.any() else float("nan"), ia.sum(), img[ib].mean() if ib.any() else float("nan"), ib.sum()))
print("a=%d  b=%d" % (a, b))
print(" ".join("%.0f" % o[1] for o in reversed(out)), "|", " ".join("%.0f" % o[3] for o in out))
print("Anzahl", out[0][2], out[0][4])
