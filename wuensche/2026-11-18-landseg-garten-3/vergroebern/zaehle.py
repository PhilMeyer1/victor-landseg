import json,sys
for o in ["a-alles-frei","b-kategorien-frei","c-feste-liste"]:
    r=[]
    for base in [sys.argv[1]+"/"+o, sys.argv[2]+"/"+o]:
        d=json.load(open(base+"/zusammen/segmente.json",encoding="utf-8"))
        s=d.get("segmente",d)
        r.append(len(s))
    print(o,r)
