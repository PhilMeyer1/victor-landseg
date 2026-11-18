"""Einmalige Anpassung der Kopie pruefe_h0.py für Teil 3 (grobe Vorstufe, Nachsegmentieren, Gegenprobe-Kopie)."""
from pathlib import Path

p = Path("C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/skripte/pruefe_h0.py")
t = p.read_text(encoding="utf-8")


def r(alt, neu):
    global t
    assert t.count(alt) == 1, alt[:80]
    t = t.replace(alt, neu)


r('"""Unabhängige Prüfung von Teil 2 (H0)',
  '"""Teil 3 (Kopie aus Teil 2, erweitert: Abschnitt Nachsegmentieren wörtlich, Zeile Karte, Gegenprobe-Kopie,\n'
  'Kopien bildpunktgleich, höchstens 800 Kernsegmente, Probe pruefe_urteil mit echtem Eingriff auf einer Kopie).\n\n'
  'Unabhängige Prüfung von Teil 2 (H0)')
r('''import numpy as np
import tifffile
''', '''import numpy as np
import tifffile

sys.path.insert(0, str(Path(sys.argv[2]) / "skripte"))
REPO = Path(sys.argv[1]) / "landseg"
''')
r('''def auftrag_ok(pfad: str, ids=None):
    t = Path(pfad).read_text(encoding="utf-8")
''', '''def nachseg_erwartet() -> str:
    quelle = (D / "skripte" / "baue_auftraege_h0.py").read_text(encoding="utf-8")
    a = quelle.index('NACHSEG = """') + len('NACHSEG = """')
    return quelle[a:quelle.index('"""', a)].replace("{{PY}}", plan["py"])


NACHSEG = nachseg_erwartet()
kern_gesamt = 0


def auftrag_ok(pfad: str, ids=None, karte=None):
    t = Path(pfad).read_text(encoding="utf-8")
    if karte is not None:
        if t.count(NACHSEG) != 1:
            maengel.append(f"Abschnitt Nachsegmentieren nicht genau einmal wörtlich in {pfad}")
        zeile = f"Karte zum Nachsegmentieren: `{karte}/labels.tif` und `{karte}/segmente.json`"
        if t.count(zeile) != 1:
            maengel.append(f"Zeile Karte fehlt oder falsch in {pfad}")
        if t.count("Karte zum Nachsegmentieren:") != 1:
            maengel.append(f"mehr als eine Karte genannt in {pfad}")
        if f"--segmente {karte}/segmente.json --fassung" not in t:
            maengel.append(f"Kontrollbefehl nicht auf der Karte in {pfad}")
    elif "Nachsegmentieren" in t:
        maengel.append(f"A-Auftrag mit Nachsegmentieren: {pfad}")
''')
r('''    im_kern = {s["id"] for s in seg["segmente"] if s.get("im_kern")}
''', '''    im_kern = {s["id"] for s in seg["segmente"] if s.get("im_kern")}
    kern_gesamt += len(im_kern)
''')
r('''    for f in ("b-kategorien-frei", "c-feste-liste"):
        for name in ("labels.tif", "segmente.json", "kandidaten.json"):
            if sha(H0 / f / tk / name) != sha(H0 / "vorstufe" / tk / name):
                maengel.append(f"{f}/{tk}/{name} nicht bytegleich zur Vorstufe")
''', '''    kopien = [H0 / f / tk for f in ("b-kategorien-frei", "c-feste-liste")]
    if tk == "r0c0":
        kopien.append(H0 / "c-feste-liste" / "gegenprobe" / "r0c0")
    for ordner in kopien:
        for name in ("labels.tif", "segmente.json", "kandidaten.json"):
            if sha(ordner / name) != sha(H0 / "vorstufe" / tk / name):
                maengel.append(f"{ordner}/{name} nicht bytegleich zur Vorstufe")
        if not np.array_equal(tifffile.imread(ordner / "labels.tif"), labels):
            maengel.append(f"{ordner}/labels.tif nicht bildpunktgleich")
''')
r('''            auftrag_ok(e["auftrag"], e["segmente"])
            bilder = Path(e["bilder"])''', '''            auftrag_ok(e["auftrag"], e["segmente"], (H0 / ("c-feste-liste" if fassung == "c" else "b-kategorien-frei") / tk).as_posix())
            bilder = Path(e["bilder"])''')
r('''for e in plan["gegenprobe"]:
    auftrag_ok(e["auftrag"], e["segmente"])''', '''for e in plan["gegenprobe"]:
    auftrag_ok(e["auftrag"], e["segmente"], (H0 / "c-feste-liste" / "gegenprobe" / "r0c0").as_posix())
    if any(Path(e["ergebnis"]).iterdir()):
        maengel.append(f"Ergebnisordner nicht leer: {e['ergebnis']}")''')
r('''if arten != {"c": 16, "b": 16, "a": 4, "z": 4}:
    maengel.append(f"Einheiten {arten}")
''', '''if arten != {"c": 16, "b": 16, "a": 4, "z": 4}:
    maengel.append(f"Einheiten {arten}")
if kern_gesamt > 800:
    maengel.append(f"Kernsegmente {kern_gesamt} > 800")
for name in ("vorstufe-fein", "viertel-fein", "ganz-fein", "a-alles-frei-fein", "b-kategorien-frei-fein", "c-feste-liste-fein"):
    if not (H0 / name).is_dir():
        maengel.append(f"feine Fassung fehlt: {name}")
''')
# Probe mit echtem Eingriff auf einer Kopie (Teilen eines Segments aus der Liste)
r('''if proben != {"gueltig": 0, "fehlt": 1, "ohne_uebersicht": 1}:''', '''    import shutil
    kopie = Path(tmp) / "karte"
    kopie.mkdir()
    for name in ("labels.tif", "segmente.json"):
        shutil.copy2(H0 / "c-feste-liste" / "r1c0" / name, kopie / name)
    lab = tifffile.imread(kopie / "labels.tif")
    ziel_id = max(e["segmente"], key=lambda s: int((lab == s).sum()))
    ys, xs = np.nonzero(lab == ziel_id)
    xm = int(np.median(xs))
    (Path(tmp) / "erg").mkdir()
    (Path(tmp) / "erg" / "eingriffe.json").write_text(json.dumps(
        {"schritte": [{"op": "teilen", "id": ziel_id, "linie": [[xm, int(ys.min()) - 1], [xm, int(ys.max()) + 1]]}]}), encoding="utf-8")
    r = subprocess.run([plan["py"], "-B", "-m", "landseg", "eingriff", "--labels", str(kopie / "labels.tif"),
                        "--segmente", str(kopie / "segmente.json"), "--bearbeiter", "probe", "stapel",
                        "--datei", str(Path(tmp) / "erg" / "eingriffe.json")], cwd=REPO, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    proben["eingriff_rc"] = r.returncode
    seg_neu = json.loads((kopie / "segmente.json").read_text(encoding="utf-8"))
    neu = sorted({s["id"] for s in seg_neu["segmente"]} - {s["id"] for s in json.loads(seg_pfad.read_text(encoding="utf-8"))["segmente"]})
    proben["neue_ids"] = len(neu)
    eintrag = urteil["segmente"][0]
    u2 = {**urteil, "segmente": urteil["segmente"] + [{**eintrag, "id": i} for i in neu],
          "eingriffe": [{"schritt": "teilen", "vorher": [ziel_id], "nachher": [ziel_id] + neu, "grund": "Probe"}]}
    for name, u in (("eingriff_gueltig", u2), ("eingriff_neu_fehlt", {**u2, "segmente": urteil["segmente"]}),
                    ("eingriff_ohne_liste", {k: v for k, v in u2.items() if k != "eingriffe"})):
        pf = Path(tmp) / "erg" / "urteil.json"
        pf.write_text(json.dumps(u), encoding="utf-8")
        r = subprocess.run([PY, "-I", str(D / "skripte" / "pruefe_urteil.py"), "--urteil", str(pf), "--segmente",
                            str(kopie / "segmente.json"), "--fassung", "c", "--viertel", "v4", "--ids",
                            ",".join(map(str, e["segmente"])), "--kategorien", str(BASIS / "landseg" / "kategorien.json")],
                           capture_output=True, text=True)
        proben[name] = r.returncode
        if name == "eingriff_gueltig" and r.returncode:
            print(r.stdout[-800:], r.stderr[-400:])
if proben != {"gueltig": 0, "fehlt": 1, "ohne_uebersicht": 1, "eingriff_rc": 0, "neue_ids": proben.get("neue_ids") or -1,
              "eingriff_gueltig": 0, "eingriff_neu_fehlt": 1, "eingriff_ohne_liste": 1}:''')
r('''print("Zahlen (Kern, je Viertel):", json.dumps(zahlen))''',
  '''print("Kernsegmente gesamt:", kern_gesamt)
print("Zahlen (Kern, je Viertel):", json.dumps(zahlen))''')
p.write_text(t, encoding="utf-8", newline="\n")
print("ok")
