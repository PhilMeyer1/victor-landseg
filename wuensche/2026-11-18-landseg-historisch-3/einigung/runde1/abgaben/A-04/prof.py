import numpy as np, cv2, tifffile, json
D='C:/Users/Phil/Developement/Victor/daten/landseg/H0/'
img=cv2.imread(D+'H0.png',cv2.IMREAD_GRAYSCALE).astype(float)
g=cv2.GaussianBlur(img,(0,0),1.2)
L=np.zeros((1000,1000),np.int64); kl={}
for t,ox in (('r0c0',0),('r0c1',500)):
    l=tifffile.imread(D+'a-alles-frei/'+t+'/labels.tif').astype(np.int64)
    L[0:500,ox:ox+500]=l[64:564,64:564]
    for s in json.load(open(D+'a-alles-frei/'+t+'/segmente.json',encoding='utf-8'))['segmente']: kl[s['id']]=s['klasse']
for y in range(44,104,1):
    row=[]
    for x in (496,498,499,500,501,503):
        i=L[y,x]; row.append(f"{int(g[y,x]):3d} {i%1000:3d}:{kl[i]:<5}")
    print(y," | ".join(row))
