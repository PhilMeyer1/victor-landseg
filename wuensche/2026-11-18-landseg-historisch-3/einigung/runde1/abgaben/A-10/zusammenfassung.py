import json,sys
a=json.load(open(sys.argv[1],encoding='utf-8'))
print([ (k['code'],k['name']) for k in a['klassen']])
for i,p in enumerate(a['paare'],1):
    print('---',i,p['paar'],p['art'],'strecken',p.get('strecken'),'bild',p.get('bild'))
    for s in p['segmente']:
        print('  ',s['segment'],s['klasse'],s['name'],'teil',s.get('klasse_teil'),'sicher',s.get('sicher'),'fl',s.get('flaeche'),'kern',s.get('flaeche_kern'),'|',s.get('beschreibung') or '', '|',s.get('offen') or s.get('grund') or '', s.get('quelle') or '', s.get('grauwert') or '')
print([k for k in a['paare'][0].keys()])
