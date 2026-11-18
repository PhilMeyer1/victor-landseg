from werk import *
import pickle
reg, arten, kp = pickle.load(open("probe16.pkl","rb"))
lab, img, seg = lade()
for j in sorted(arten):
    m = reg == j; ys, xs = np.nonzero(m)
    dt = ndimage.distance_transform_edt(np.pad(m,1))[1:-1,1:-1]; yy, xx = np.unravel_index(np.argmax(dt), dt.shape)
    q = "v1" if xx<314 and yy<314 else "v2" if yy<314 else "v3" if xx<314 else "v4"
    print(j, "hmdG"[ [3,2,1,4].index(arten[j]) ], int(m.sum()), (int(xx),int(yy)), q, "bbox", xs.min(), ys.min(), xs.max(), ys.max(), "g", int(img[m].mean()))
