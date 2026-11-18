import json,sys
a=json.load(open(sys.argv[1],encoding='utf-8'))
print([k for k in a if k not in('klassen','paare')])
print({k:a[k] for k in a if k not in('klassen','paare')})
for k in a['klassen']: print(k['code'],k['name'],k.get('parent'))
for p in a['paare']:
    print('---',p['nr'],p['paar'],p['art'],'rand',p['randpunkte'],[ (s['linie'],s['von'],s['bis'],s['laenge'],s.get('kante_max')) for s in p['strecken']])
    for s in p['segmente']:
        print('   ',s['segment'],s['klasse'],s['name'],'teil:',s.get('klasse_teil'),s.get('klasse_teil_name'),'sicher',s['sicher'],'|',s.get('grund'),'|',s.get('quelle'),'fl',s['flaeche'],'kern',s.get('flaeche_kern'),'grau',s.get('grauwert'),'im_kern',s['im_kern'])
