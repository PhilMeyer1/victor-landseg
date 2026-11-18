import json,sys
k=json.load(open('korrekturen.json',encoding='utf-8'))
k.setdefault('schnitte',[])
for a in sys.argv[1:]:
    pts=[[int(v) for v in p.split(',')] for p in a.split(';')]
    k['schnitte'].append({'linie':pts,'breite':2})
json.dump(k,open('korrekturen.json','w',encoding='utf-8'),ensure_ascii=False,indent=1)
print(len(k['schnitte']))
