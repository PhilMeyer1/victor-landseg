import numpy as np, cv2, tifffile, sys
D='C:/Users/Phil/Developement/Victor/daten/landseg/H0/'
img=cv2.imread(D+'H0.png',cv2.IMREAD_GRAYSCALE)
L=np.zeros((1000,1000),np.int64)
l0=tifffile.imread(D+'a-alles-frei/r0c0/labels.tif').astype(np.int64)
l1=tifffile.imread(D+'a-alles-frei/r0c1/labels.tif').astype(np.int64)
L[0:500,0:500]=l0[64:564,64:564]
L[0:500,500:1000]=l1[64:564,64:564]
x0,x1,y0,y1,s=[int(a) for a in sys.argv[1:6]]; out=sys.argv[6]; sys.argv.insert(7,"")
ids=[int(a) for a in sys.argv[8:] if a]
cr=img[y0:y1,x0:x1]; lc=L[y0:y1,x0:x1]
big=cv2.resize(cr,None,fx=s,fy=s,interpolation=cv2.INTER_NEAREST)
raw=cv2.cvtColor(big,cv2.COLOR_GRAY2BGR)
ov=raw.copy()
lb=cv2.resize(lc.astype(np.float32),None,fx=s,fy=s,interpolation=cv2.INTER_NEAREST).astype(np.int64)
cols=[(255,200,0),(255,0,255),(0,200,0),(0,128,255),(0,0,255),(255,255,0),(128,0,255),(0,255,255)]
for i,idv in enumerate(ids):
    m=lb==idv
    c=np.array(cols[i%len(cols)])
    ov[m]=(ov[m]*0.5+c*0.5).astype(np.uint8)
e=(np.diff(lb,axis=0,prepend=lb[:1])!=0)|(np.diff(lb,axis=1,prepend=lb[:,:1])!=0)
ov[e]=(255,255,255)
if x0<500<x1:
    xx=(500-x0)*s; ov[:,xx]=(0,255,255)
out_img=np.concatenate([raw,np.zeros((raw.shape[0],8,3),np.uint8),ov],1)
cv2.putText(out_img,f"x {x0}-{x1} y {y0}-{y1} {s}x",(5,20),cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,255,255),2)
cv2.imwrite(out,out_img,[cv2.IMWRITE_JPEG_QUALITY,90])
print(out_img.shape)
