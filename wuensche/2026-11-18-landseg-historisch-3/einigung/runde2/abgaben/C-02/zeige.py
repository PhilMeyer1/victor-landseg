import json,sys
a=json.load(open(sys.argv[1],encoding='utf-8'))
print([k for k in a])
for k in a:
    if k not in ('paare','klassen'): print(k, json.dumps(a[k],ensure_ascii=False)[:600])
print('KLASSEN:', ', '.join(f"{c['code']}={c['name']}" for c in a['klassen']) if isinstance(a['klassen'],list) and isinstance(a['klassen'][0],dict) else json.dumps(a['klassen'],ensure_ascii=False)[:2000])
for i,p in enumerate(a['paare'],1):
    print('-----',i)
    for k,v in p.items():
        if k in ('segmente','a','b','seg_a','seg_b'):
            print(k, json.dumps(v,ensure_ascii=False)[:900])
        else:
            print(k, json.dumps(v,ensure_ascii=False)[:400])
