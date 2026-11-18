import json,sys
a=json.load(open(sys.argv[1],encoding='utf-8'))
print("klassen:")
for k in a['klassen']: print(" ",k['code'],k['name'])
for i,p in enumerate(a['paare'],1):
    print("=== paar",i,p.get('paar'),p.get('art'),p.get('bild'))
    print("  strecken",json.dumps(p.get('strecken'))[:200])
    for key in p:
        if key in ('paar','art','strecken','randpunkte','bild'): continue
        print("  ",key,json.dumps(p[key],ensure_ascii=False)[:900])
