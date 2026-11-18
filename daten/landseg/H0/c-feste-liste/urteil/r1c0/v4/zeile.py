import sys, numpy as np, tifffile
lab = tifffile.imread("C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r1c0/labels.tif").astype(np.int64)
x0,x1,y0,y1,st = [int(a) for a in sys.argv[1:6]]
print("     " + " ".join("%3d" % (x % 1000) for x in range(x0, x1, st)))
for y in range(y0, y1, st):
    print("%4d " % y + " ".join("%3d" % (lab[y, x] % 100) for x in range(x0, x1, st)))
