import json,sys
a=json.load(open(sys.argv[1],encoding='utf-8'))
for p in a['paare']:
    print('=====',p['nr'],p['paar'])
    for s in p['segmente']:
        d={k:s.get(k) for k in ('segment','klasse','herkunft','instanz','flaeche','flaeche_kern','urteil','was_ist_es','punkte','klasse_heute','klasse_vorschlag','klasse_vorstufe','sicher')}
        print(json.dumps(d,ensure_ascii=False))
