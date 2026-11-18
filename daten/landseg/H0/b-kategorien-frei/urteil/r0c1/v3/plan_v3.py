from werk import *
import pickle
lab, img, seg = lade()
r47, a47 = pickle.load(open("probe47.pkl","rb"))
r74, a74 = zerlegen_ws(200074, 140, 80, sigma=1.0, minfl=60, ero=(1,2,1)); r74, a74 = gleichartige_vereinen(r74, a74)
print("74:", [(j, a74[j], int((r74==j).sum())) for j in a74])
regionen_bild("probe_74.jpg", r74, a74, 225, 330, 110, 120, 5, titel="Probe 74")
plan = [(200047, r47, a47), (200074, r74, a74)]
schritte = []
for sid, r, a in plan:
    b, rest = behalten_waehlen(sid, r, a, lab)
    print(sid, "behalten", b, a[b], "Kontext ohne Anschluss", rest)
    schritte += plan_schritte2(sid, r, b, seg[sid]["klasse"], lab)
karte, zu, fertig = simulieren2(schritte, [(sid, r) for sid, r, a in plan])
info = {}
for sid, r, a in plan: info.update(regionen_info(sid, r, a, zu, img))
for sid in (200047, 200074): print(sid, "bleibt auf Karte:", int((karte == sid).sum()))
json.dump({"schritte": fertig}, open("eingriffe.json", "w", encoding="utf-8"))
json.dump(info, open("regionen_v3.json", "w"), indent=0)
pickle.dump({"plan": plan, "zu": zu}, open("plan_v3.pkl", "wb"))
print(len(fertig), "Schritte")
