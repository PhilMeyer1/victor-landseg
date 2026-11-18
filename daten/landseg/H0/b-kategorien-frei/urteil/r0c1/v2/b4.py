from werk import *
lab, img, seg = lade()
s = ndimage.gaussian_filter(img.astype(float), 1.0)
a = np.array([340, 285.]); b = np.array([500, 168.])
d = (b-a)/np.linalg.norm(b-a); n = np.array([d[1]*-1, d[0]])  # n zeigt nach ...
n = np.array([-d[1], d[0]])
print("d", d, "n", n)
for t in np.linspace(0, 1, 12):
    p = a + t*(b-a)
    vals = []
    for k in range(-16, 17, 2):
        q = p + k*n
        vals.append(int(s[int(round(q[1])), int(round(q[0]))]))
    print(np.round(p).astype(int), vals)
