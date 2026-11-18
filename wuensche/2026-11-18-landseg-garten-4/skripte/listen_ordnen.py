"""Schritt 1 (landseg-garten-4): freie Listen A und B von T0 und H0 nach L14 ordnen, ohne Behelfsnamen.

- Die Ebene-1-Klasse des Grünlands heißt genau „Dauergrünland“ (statt „Dauergrünland (<alter Name>)“).
- Gartenklassen an anderer Stelle (L14: jeder Gartenname geht auf „Garten“ über) wandern unter die Klasse
  „Garten“ der Fassung: als deren Unterklasse mit altem Namen, Farbe und Merkmal (die Segmente behalten ihre
  feine Bedeutung) oder, wenn sie schon „Garten“ hießen (H0 B 2.2, T0 B 3.3 Gartenparzelle), direkt auf sie.
- Segmente werden nur über `landseg eingriff stapel` (klasse_setzen) umgestellt; leere Klassen fallen weg,
  Ebene-1-Namen ohne Gartenteil werden nur umbenannt, wenn kein Segment die Ebene-1-Klasse selbst trägt.
Aufruf: python listen_ordnen.py probe|echt
"""
import collections, json, shutil, subprocess, sys
from pathlib import Path

W = Path("C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-4")
D = Path("C:/Users/Phil/Developement/Victor/daten/landseg")
PY = "C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe"
REPO = "C:/Users/Phil/Developement/Victor/landseg"
BILD = {"T0": D / "uebergabe/landseg-t0/T0", "H0": D / "H0"}
ORD = {"A": ("a-alles-frei", "kategorien-a.json"), "B": ("b-kategorien-frei", "kategorien-b.json")}
PLAN = {
    ("T0", "A"): {"namen": {"4": "Dauergrünland"},
                  "wege": {"3.1": "4.4.1", "3.2": "4.4.2", "3.3": "4.4.3"}, "weg_wenn_leer": ["3"]},
    ("T0", "B"): {"namen": {"2": "Dauergrünland", "3": "Feld und offener Boden"},
                  "wege": {"3.3.1": "2.4.1", "3.3.2": "2.4.2", "3.3": "2.4"}, "weg_wenn_leer": []},
    ("H0", "A"): {"namen": {"4": "Dauergrünland"},
                  "wege": {"2.2": "4.4.1", "2.3": "4.4.2"}, "weg_wenn_leer": []},
    ("H0", "B"): {"namen": {"5": "Dauergrünland", "2": "Hof"},
                  "wege": {"2.2": "5.3"}, "weg_wenn_leer": []},
}
BEARBEITER = "umsetzer:landseg-garten-4"
sys.path.insert(0, REPO)
from landseg.kategorien import garten_maengel  # noqa: E402


def segmente(ordner):
    out = {}
    for p in sorted(ordner.glob("r?c?/segmente.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        out[p.parent.name] = d["segmente"]
    return out


def zaehlen(klassen):
    codes = [c["code"] for c in klassen]
    eltern = {c.get("parent") for c in klassen}
    return {"level_1": sum(1 for c in klassen if c.get("parent") is None),
            "level_2": sum(1 for c in klassen if c.get("level") == 2),
            "leaves": sum(1 for c in codes if c not in eltern)}


def main(art):
    log = []
    for (bild, fass), plan in PLAN.items():
        o, kn = ORD[fass]
        ordner = BILD[bild] / o
        pfad = ordner / kn
        daten = json.loads(pfad.read_text(encoding="utf-8"))
        klassen = daten["classes"]
        nach_code = {c["code"]: c for c in klassen}
        assert zaehlen(klassen) == {k: daten["counts"][k] for k in ("level_1", "level_2", "leaves")}, (bild, fass, zaehlen(klassen), daten["counts"])
        segs = segmente(ordner)
        benutzt = collections.Counter(s["klasse"] for ss in segs.values() for s in ss)
        # Kinder der wandernden Klassen müssen selbst im Plan stehen
        for alt in plan["wege"]:
            for c in klassen:
                if c.get("parent") == alt and c["code"] not in plan["wege"]:
                    raise SystemExit(f"{bild} {fass}: Kind {c['code']} von {alt} ohne Ziel")
        for code in plan["namen"]:
            if code != max(plan["namen"], key=lambda x: 0) and False:
                pass
        # neue Klassen anlegen
        neu = []
        for alt, ziel in plan["wege"].items():
            if ziel in nach_code:
                continue
            e = dict(nach_code[alt]); e["code"] = ziel; e["parent"] = ziel.rsplit(".", 1)[0]; e["level"] = ziel.count(".") + 1
            neu.append(e)
        # Ebene-1-Umbenennung nur, wenn kein Segment die Klasse selbst trägt (außer bei „Dauergrünland“: gleiche Bedeutung)
        for code, name in plan["namen"].items():
            if name != "Dauergrünland" and benutzt[code]:
                raise SystemExit(f"{bild} {fass}: {code} wird von {benutzt[code]} Segmenten getragen, nicht umbenennen")
        schritte = {tk: [{"op": "klasse_setzen", "id": s["id"], "klasse": plan["wege"][s["klasse"]]}
                         for s in ss if s["klasse"] in plan["wege"]] for tk, ss in segs.items()}
        log.append(f"{bild} {fass}: umbenennen {[(c, nach_code[c]['name'], n) for c, n in plan['namen'].items()]}")
        log.append(f"{bild} {fass}: neue Klassen {[(e['code'], e['name']) for e in neu]}")
        log.append(f"{bild} {fass}: Umstellung {dict((a, f'{z} ({benutzt[a]} Segmente)') for a, z in plan['wege'].items())}"
                   f" je Teilkachel {dict((t, len(s)) for t, s in schritte.items())}")
        if art != "echt":
            continue
        # 1. neue Klassen einfügen (hinter dem Ziel-Elternteil), alte bleiben vorerst
        for e in neu:
            pos = max(i for i, c in enumerate(klassen) if c["code"] == e["parent"] or c["code"].startswith(e["parent"] + ".")) + 1
            klassen.insert(pos, e)
        pfad.write_text(json.dumps(daten, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        # 2. Segmente umstellen
        for tk, st in schritte.items():
            if not st:
                continue
            sf = W / "logs" / f"schritte-{bild}-{fass}-{tk}.json"
            sf.write_text(json.dumps({"schritte": st}, ensure_ascii=False), encoding="utf-8")
            d = ordner / tk
            r = subprocess.run([PY, "-B", "-m", "landseg", "eingriff", "--labels", str(d / "labels.tif"), "--segmente",
                                str(d / "segmente.json"), "--kategorien", str(pfad), "--bearbeiter", BEARBEITER,
                                "stapel", "--datei", str(sf)], cwd=REPO, capture_output=True, text=True, encoding="utf-8")
            log.append(f"  eingriff {bild} {fass} {tk}: {len(st)} Schritte, Exit {r.returncode} {(r.stdout + r.stderr).strip()[-200:]}")
            if r.returncode:
                raise SystemExit("\n".join(log))
        # 3. alte Klassen entfernen, umbenennen, zählen
        benutzt = collections.Counter(s["klasse"] for ss in segmente(ordner).values() for s in ss)
        weg = [a for a in plan["wege"]] + plan["weg_wenn_leer"]
        for a in weg:
            assert benutzt[a] == 0, (bild, fass, a, benutzt[a])
            assert not any(c.get("parent") == a for c in klassen if c["code"] not in weg), (bild, fass, a)
        daten["classes"] = klassen = [c for c in klassen if c["code"] not in weg]
        for c in klassen:
            if c["code"] in plan["namen"]:
                c["name"] = plan["namen"][c["code"]]
        daten["counts"].update(zaehlen(klassen))
        pfad.write_text(json.dumps(daten, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        m = garten_maengel({c["code"]: c for c in klassen})
        log.append(f"  {bild} {fass}: counts {daten['counts']}, garten_maengel {m}")
    print("\n".join(log))
    (W / "logs" / f"listen-ordnen-{art}.log").write_text("\n".join(log) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv[1])
