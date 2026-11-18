"""Teilt Segmente mit Linien aus blob.py, fügt Splitter (< 20 Bildpunkte) wieder an und protokolliert.

teile.py <bearbeiter> <spec.json>   spec: [{"id":..,"art":"gt","t":..,"roi":"-"}, ...] oder {"op":"verschmelzen",...}
Hängt alle ausgeführten Schritte an eingriffe.json an und schreibt protokoll.json (vorher/nachher je Schritt).
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import tifffile
from scipy import ndimage

ORD = Path(__file__).resolve().parent
P = sys.executable
B = "C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/"
LAB, SEG = B + "labels.tif", B + "segmente.json"
bearb = sys.argv[1]
spec = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
stapel = ORD / "eingriffe.json"
alle = json.loads(stapel.read_text(encoding="utf-8"))["schritte"] if stapel.exists() else []
prot_p = ORD / "protokoll.json"
prot = json.loads(prot_p.read_text(encoding="utf-8")) if prot_p.exists() else []


def lauf(schritte):
    tmp = ORD / "tmp" / "stapel_tmp.json"
    tmp.write_text(json.dumps({"schritte": schritte}), encoding="utf-8")
    r = subprocess.run([P, "-B", "-m", "landseg", "eingriff", "--labels", LAB, "--segmente", SEG, "--bearbeiter", bearb,
                        "stapel", "--datei", str(tmp)], capture_output=True, text=True,
                       cwd="C:/Users/Phil/Developement/Victor/landseg")
    print(r.stdout.strip().splitlines()[0] if r.stdout.strip() else r.stderr[-500:])
    if r.returncode != 0 or not r.stdout.strip().endswith("ok"):
        print(r.stdout, r.stderr)
        raise SystemExit("Stapel fehlgeschlagen")
    alle.extend(schritte)
    stapel.write_text(json.dumps({"schritte": alle}), encoding="utf-8")
    return r.stdout


for s in spec:
    if s.get("op") == "verschmelzen":
        lauf([s])
        prot.append({"schritt": "verschmelzen", "vorher": s["ids"], "nachher": [s["ziel"]], "grund": s["grund"]})
        continue
    sid = s["id"]
    out = subprocess.run([P, "-B", str(ORD / "blob.py"), str(sid), s["art"], str(s["t"]), str(ORD / "tmp" / f"s{sid}.jpg"),
                          s.get("roi", "-"), "1", str(s.get("oeffnen", 1))], capture_output=True, text=True, cwd=str(ORD)).stdout
    linie = json.loads(out)["linie"]
    vor = set(np.unique(tifffile.imread(LAB)).tolist())
    lauf([{"op": "teilen", "id": sid, "linie": linie}])
    lab = tifffile.imread(LAB)
    neu = sorted(set(np.unique(lab).tolist()) - vor)
    prot.append({"schritt": "teilen", "vorher": [sid], "nachher": [sid] + neu, "grund": s["grund"]})
    groesse = {i: int((lab == i).sum()) for i in neu}
    if not neu:
        continue
    haupt = max(neu, key=lambda i: groesse[i])
    klein = [i for i in neu if i != haupt]
    if klein:
        # Splitter an das Hauptstück, sonst an das Ursprungssegment
        an_haupt, an_alt = [], []
        hm = ndimage.binary_dilation(lab == haupt)
        for i in klein:
            (an_haupt if (hm & (lab == i)).any() else an_alt).append(i)
        schritte = []
        if an_haupt:
            schritte.append({"op": "verschmelzen", "ids": [haupt] + an_haupt, "ziel": haupt})
        for i in an_alt:
            schritte.append({"op": "verschmelzen", "ids": [sid, i], "ziel": sid})
        try:
            lauf(schritte)
            if an_haupt:
                prot.append({"schritt": "verschmelzen", "vorher": [haupt] + an_haupt, "nachher": [haupt],
                             "grund": "Splitter des Teilens zurück an das abgetrennte Stück."})
            for i in an_alt:
                prot.append({"schritt": "verschmelzen", "vorher": [sid, i], "nachher": [sid],
                             "grund": "Splitter des Teilens zurück an das Ursprungssegment."})
        except SystemExit:
            print("Splitter nicht angefügt:", klein)
    print(sid, "->", haupt, groesse[haupt])
prot_p.write_text(json.dumps(prot, ensure_ascii=False, indent=1), encoding="utf-8")
