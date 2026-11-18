import json
d=json.load(open(r"C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-B-r1c1-3/kandidaten.json",encoding="utf-8"))
unk={400215:"Winziger Splitter (1,4 m²) am Rand eines Weges zwischen den Gärten, Zugehörigkeit zum Garten am Bild nicht sicher.",
     400221:"Winziger Splitter (0,3 m²) zwischen Gehölz und Hofrand, am Bild nicht sicher einem Garten zuzuordnen.",
     400349:"Winziger Splitter (0,2 m²) am Rand des Weges unten, eher Wegsaum als Gartenfläche, nicht sicher."}
out={}
for k in d["kandidaten"]:
    i=k["id"]
    if i in unk: out[str(i)]={"garten":"unklar","grund":unk[i]}
    elif i==400067: out[str(i)]={"garten":"ja","grund":"Große krautige Grünfläche im Inneren des Wohnblocks, rundum von Wohnhäusern, Hecken und Gartenparzellen eingefasst, also Hausgärten."}
    elif k["klasse"]=="3.3.1": out[str(i)]={"garten":"ja","grund":"Beet direkt am Wohnhaus innerhalb der eingefassten Hausgartenparzelle."}
    else: out[str(i)]={"garten":"ja","grund":"Krautige Grünfläche zwischen Wohnhäusern innerhalb einer von Hecken und Gebäuden eingefassten Hausgartenparzelle."}
p=r"C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-B-r1c1-3/entscheid.json"
json.dump(out,open(p,"w",encoding="utf-8"),ensure_ascii=False,indent=1)
r=json.load(open(p,encoding="utf-8"))
ids={str(k["id"]) for k in d["kandidaten"]}
print(len(r),set(r)==ids,[sum(v["garten"]==g for v in r.values()) for g in("ja","nein","unklar")])
