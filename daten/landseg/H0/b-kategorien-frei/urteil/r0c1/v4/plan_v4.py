from werk import *
import pickle
lab, img, seg = lade()
r63, a63 = pickle.load(open("probe63.pkl","rb"))
r63[r63 == 38] = 0; del a63[38]  # 1 Bildpunkt am Kernrand ohne Nachbarregion: bleibt beim Kontextteil
print("kleinste Regionen 63:", sorted(int((r63==j).sum()) for j in a63)[:4])
r105, a105 = zerlegen_ws(200105, 130, 75, sigma=1.0, minfl=40, ero=(1,1,1)); r105, a105 = gleichartige_vereinen(r105, a105)
r107, a107 = zerlegen_ws(200107, 130, 75, sigma=1.0, minfl=40, ero=(1,1,1)); r107, a107 = gleichartige_vereinen(r107, a107)
print("105:", [(j, a105[j], int((r105==j).sum())) for j in a105]); print("107:", [(j, a107[j], int((r107==j).sum())) for j in a107])
rr = r105.copy(); aa = dict(a105)
for j, a in a107.items(): rr[r107 == j] = 100 + j; aa[100 + j] = a
regionen_bild("probe_105.jpg", rr, aa, 495, 500, 75, 64, 9, titel="Probe 105 und 107")
plan = [(200063, r63, a63), (200105, r105, a105), (200107, r107, a107)]
schritte = []
for sid, r, a in plan:
    if len(a) < 2: print(sid, "nicht geteilt"); continue
    b, rest = behalten_waehlen(sid, r, a, lab)
    print(sid, "behalten", b, a[b], "Kontext ohne Anschluss", rest)
    schritte += plan_schritte2(sid, r, b, seg[sid]["klasse"], lab)
plan = [p for p in plan if len(p[2]) >= 2]
karte, zu, fertig = simulieren2(schritte, [(sid, r) for sid, r, a in plan])
info = {}
for sid, r, a in plan: info.update(regionen_info(sid, r, a, zu, img))
for sid, r, a in plan: print(sid, "bleibt auf Karte:", int((karte == sid).sum()))
alt = set(np.unique(lab).tolist()); neu_ctx = sorted(set(np.unique(karte).tolist()) - alt - set(zu.values()))
print("neue IDs nur im Kontext:", neu_ctx)
json.dump({"schritte": fertig}, open("eingriffe.json", "w", encoding="utf-8"))
json.dump(info, open("regionen_v4.json", "w"), indent=0)
pickle.dump({"plan": plan, "zu": zu}, open("plan_v4.pkl", "wb"))
print(len(fertig), "Schritte")
