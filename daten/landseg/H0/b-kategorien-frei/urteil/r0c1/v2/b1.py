from werk import *
stat([200021,200017,200018,200026,200007,200034,200012,200030,200029,200016,200046,200050,200036,200045,200059,200055,200044,200039,200058,200064,200066,200070,200068])
lab, img, seg = lade()
m = lab == 200016
print("16 im Kern", int(m[64:564,64:564].sum()))
s = ndimage.gaussian_filter(img.astype(float),1.2)
print(np.percentile(s[m], [10,25,50,75,90]))
