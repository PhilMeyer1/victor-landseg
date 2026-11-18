import sys, numpy as np, tifffile
L = tifffile.imread("C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r1c0/labels.tif")
x0,x1,y0,y1,s = map(int, sys.argv[1:6])
print("    " + "".join(f"{x:>3}"[-3:] if (x-x0)%(5*s)==0 else "" for x in range(x0,x1,s)))
for y in range(y0,y1,s):
    print(f"{y:>3} " + "".join(f"{L[y,x]%100:>2}"[-2:].replace(" ","0")[:2] if True else "" for x in range(x0,x1,s)))
