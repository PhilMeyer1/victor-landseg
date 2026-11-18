from werk import *
import pickle
lab, img, seg = lade()
r16, a16, kp = pickle.load(open("probe16.pkl","rb"))
r7, a7 = pickle.load(open("probe7.pkl","rb"))
r39, a39 = pickle.load(open("probe39.pkl","rb"))
plan = [(200016, r16, a16), (200007, r7, a7), (200039, r39, a39)]
schritte = []; beh = {}
for sid, r, a in plan:
    b, rest = behalten_waehlen(sid, r, a, lab)
    beh[sid] = b
    print(sid, "behalten Region", b, "Art", a[b], "Kontextteile ohne Anschluss:", rest)
    schritte += plan_schritte2(sid, r, b, "1.1.1" if seg[sid]["klasse"] == "1.1.1" else seg[sid]["klasse"], lab)
karte, zu, fertig = simulieren2(schritte, [(sid, r) for sid, r, a in plan])
info = {}
for sid, r, a in plan:
    info.update(regionen_info(sid, r, a, zu, img))
json.dump({"schritte": fertig},
          open("eingriffe.json", "w", encoding="utf-8"))
json.dump(info, open("regionen_v2.json", "w"), indent=0)
pickle.dump({"plan": plan, "zu": zu}, open("plan_v2.pkl", "wb"))
print(len(schritte), "Schritte;", len(info), "Regionen")
