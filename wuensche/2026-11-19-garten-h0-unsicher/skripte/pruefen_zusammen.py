"""pruefen je Teilkachel (A/B mit --frei, eigene Liste) und zusammentragen je Fassung (eigene Liste), dann einigung messen.
Aufruf: python pruefen_zusammen.py <logname>"""
import re, subprocess, sys
from pathlib import Path
W = Path("C:/Users/Phil/Developement/Victor/wuensche/2026-11-19-garten-h0-unsicher")
D = Path("C:/Users/Phil/Developement/Victor/daten/landseg")
PY = "C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe"
REPO = "C:/Users/Phil/Developement/Victor/landseg"
BILD = {"H0": D / "H0"}
ORD = {"A": ("a-alles-frei", "kategorien-a.json"), "B": ("b-kategorien-frei", "kategorien-b.json"), "C": ("c-feste-liste", "kategorien-c.json")}
name = sys.argv[1]
log = open(W / "logs" / f"{name}.log", "w", encoding="utf-8")
def run(a):
    r = subprocess.run([PY, "-B", "-m", "landseg"] + a, cwd=REPO, capture_output=True, text=True, encoding="utf-8")
    log.write("$ " + " ".join(a) + "\n" + r.stdout + r.stderr + f"[exit {r.returncode}]\n\n"); log.flush()
    return r
for b, p in BILD.items():
    for f, (o, k) in ORD.items():
        ok = []
        for t in ("r0c0", "r0c1", "r1c0", "r1c1"):
            d = p / o / t
            a = ["pruefen", "--labels", str(d / "labels.tif"), "--segmente", str(d / "segmente.json"), "--kategorien", str(p / o / k), "--bild", str(p / "teilkacheln" / f"{t}.png")]
            if f in "AB": a.append("--frei")
            r = run(a); ok.append(r.stdout.strip().splitlines()[-1] if r.returncode == 0 else f"{t} FEHLER")
        r = run(["zusammentragen", "--datei", str(p / o / "zusammentragen.json"), "--kategorien", str(p / o / k)])
        out = r.stdout
        seg = re.search(r"Segmente: (\d+), nicht zusammenhängend: (\d+)", out)
        naht = re.search(r"Verstöße: (\d+), bestätigt: (\d+)", out)
        letzte = out.strip().splitlines()[-1] if out.strip() else r.stderr[-300:]
        g = [l for l in out.splitlines() if "Garten" in l][:0]
        print(f"{b} {f}: pruefen {'/'.join(ok)} | zusammen Exit {r.returncode}, Segmente {seg.group(1) if seg else '?'}, "
              f"nicht zusammenhängend {seg.group(2) if seg else '?'}, Naht {naht.groups() if naht else '?'} | {letzte}")
    r = run(["einigung", "messen", "--manifest", str(p / "manifest.json")])
    print(b, "einigung messen Exit", r.returncode); print("\n".join(l for l in r.stdout.splitlines() if l.strip())[-1200:])
