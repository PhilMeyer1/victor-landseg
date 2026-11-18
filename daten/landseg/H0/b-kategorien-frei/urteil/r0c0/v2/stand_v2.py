import json, numpy as np, tifffile
B='C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r0c0/'
L=tifffile.imread(B+'labels.tif')
s=json.load(open(B+'segmente.json',encoding='utf-8'))
for v in s['verlauf']:
    if 'v2' in json.dumps(v,ensure_ascii=False): print(json.dumps(v,ensure_ascii=False)[:400])
ids=[100045,100041,100037,100028,100050,100012,100053,100054,100060,100049,100020,100046,100056,100042,100073,100089,100071,100082,100066,100062,100084,100086,100069,100087,100030,100079,100063,100032,100081,100070,100094,100100,100110,100109,100096,100095,100125,100083,100111,100107,100092,100112,100104,100137,100117,100126,100145,100141,100139,100130,100127,100128,100148,100156,100164,100151,100155,100150,100161,100166,100149,100158,100142,100167,100144,100169,100153,100264,100265,100266,100268,100269,100271,100272,100274]
K=L[64:564,64:564]; V=L[64:314,314:564]
for i in ids:
    k=int((K==i).sum()); v=int((V==i).sum()); t=int((L==i).sum())
    ys,xs=np.nonzero(L==i)
    bb=(int(xs.min()),int(ys.min()),int(xs.max()),int(ys.max())) if t else None
    print(i,'kern',k,'viertel',v,'gesamt',t,'bbox',bb)
