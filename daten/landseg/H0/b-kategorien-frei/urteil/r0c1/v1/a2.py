from werk import *
lab, img, seg = lade()
m = (lab == 200004); m[:64] = False; m[:, :64] = False
print(np.percentile(ndimage.gaussian_filter(img.astype(float),1.2)[m], [10,25,50,75,90]))
