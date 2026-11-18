from werk import *
lab, img, seg = lade()
reg, arten = zerlegen_ws(200004, 120, 60, sigma=1.2, minfl=50)
reg, arten = gleichartige_vereinen(reg, arten)
m = lab == 200004
kern = np.zeros(lab.shape, bool); kern[64:564, 64:564] = True
ctx = m & ~kern
l, k = ndimage.label(ctx, structure=[[0,1,0],[1,1,1],[0,1,0]])
st=[[0,1,0],[1,1,1],[0,1,0]]
for i in range(1, k+1):
    mm = l == i
    dil = ndimage.binary_dilation(mm, structure=st)
    nb = np.unique(reg[dil & (reg > 0)])
    print("ctx", i, int(mm.sum()), "grenzt an Regionen", nb.tolist())
