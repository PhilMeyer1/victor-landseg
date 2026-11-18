import json,sys
a=json.load(open(sys.argv[1],encoding='utf-8'))
print('KLASSEN:')
for k in a['klassen']: print(' ',k['code'],k['name'])
print('MUSTER',json.dumps(a.get('abgabe_muster'),ensure_ascii=False))
for p in a['paare']:
    print('\n=== nr',p['nr'],p['paar'],p['art'],'randpunkte',p['randpunkte'])
    for s in p['strecken']: print('  strecke',s['linie'],s['von'],s['bis'],s['laenge'],s.get('kante_max'))
    for s in p['segmente']:
        print('  SEG',s['segment'],'kl',s['klasse'],'frei',s.get('klasse_frei'),'sicher',s.get('sicher'),'fl',s.get('flaeche'),s.get('flaeche_kern'),'herk',s.get('herkunft'))
        print('     ',s.get('was_ist_es'))
