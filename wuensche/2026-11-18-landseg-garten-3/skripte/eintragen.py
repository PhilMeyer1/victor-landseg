import json, shutil, subprocess, sys
from pathlib import Path
W = Path("C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3")
D = Path("C:/Users/Phil/Developement/Victor/daten/landseg")
PYX = "C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe"
REPO = "C:/Users/Phil/Developement/Victor/landseg"
BILD = {"T0": D / "uebergabe/landseg-t0/T0", "H0": D / "H0"}
ORD = {"A": "a-alles-frei", "B": "b-kategorien-frei", "C": "c-feste-liste"}
KAT = {"A": "kategorien-a.json", "B": "kategorien-b.json", "C": "kategorien-c.json"}
TK = ["r0c0", "r0c1", "r1c0", "r1c1"]
phase = sys.argv[1]
log = open(W / "anwenden" / f"{phase}.log", "a", encoding="utf-8")
def run(args):
    r = subprocess.run([PYX, "-B", "-m", "landseg"] + args, cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    log.write("$ " + " ".join(args) + "\n" + r.stdout + r.stderr + f"[exit {r.returncode}]\n\n"); log.flush()
    return r
if phase == "sicherung":
    for b, p in BILD.items():
        for f, o in ORD.items():
            for t in TK + ["zusammen"]:
                src = p / o / t
                dst = W / "sicherung-vor-garten" / b / o / t
                if dst.exists(): continue
                dst.mkdir(parents=True)
                for n in ("labels.tif", "segmente.json", "naht.json"):
                    if (src / n).exists(): shutil.copy2(src / n, dst / n)
    print("ok")
elif phase == "eintragen":
    plan = {}
    zaehl = {}
    for e in sorted((W / "einheiten").iterdir()):
        ent = json.loads((e / "entscheid.json").read_text(encoding="utf-8"))
        kd = json.loads((e / "kandidaten.json").read_text(encoding="utf-8"))
        key = (kd["bild"], kd["fassung"], kd["teilkachel"])
        z = zaehl.setdefault(key[:2], {"ja": 0, "nein": 0, "unklar": 0})
        for i, v in ent.items():
            g = v["garten"]; z[g] += 1
            if g == "ja":
                plan.setdefault(key, {"code": kd["garten_code"], "ids": set()})["ids"].add(int(i))
    (W / "anwenden" / "zaehlung.json").write_text(json.dumps({"|".join(k): v for k, v in zaehl.items()}, indent=1), encoding="utf-8")
    for (b, f, t), v in sorted(plan.items()):
        d = BILD[b] / ORD[f] / t
        sf = W / "anwenden" / f"schritte-{b}-{f}-{t}.json"
        sf.write_text(json.dumps({"schritte": [{"op": "klasse_setzen", "id": i, "klasse": v["code"]} for i in sorted(v["ids"])]}), encoding="utf-8")
        r = run(["eingriff", "--labels", str(d / "labels.tif"), "--segmente", str(d / "segmente.json"),
                 "--kategorien", str(BILD[b] / ORD[f] / KAT[f]), "--bearbeiter", "wf:garten:20261118n", "stapel", "--datei", str(sf)])
        print(b, f, t, len(v["ids"]), r.returncode)
elif phase == "pruefen":
    for b, p in BILD.items():
        for f, o in ORD.items():
            for t in TK:
                d = p / o / t
                a = ["pruefen", "--labels", str(d / "labels.tif"), "--segmente", str(d / "segmente.json"), "--kategorien", str(p / o / KAT[f]), "--bild", str(p / "teilkacheln" / f"{t}.png")]
                if f in "AB": a.append("--frei")
                r = run(a); print(b, f, t, r.returncode, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:])
elif phase == "zusammen":
    for b, p in BILD.items():
        for f, o in ORD.items():
            r = run(["zusammentragen", "--datei", str(p / o / "zusammentragen.json")]); print(b, f, r.returncode, r.stdout.strip().splitlines()[-1:])
        r = run(["einigung", "messen", "--manifest", str(p / "manifest.json")]); print(b, "messen", r.returncode); print(r.stdout[-1500:])
