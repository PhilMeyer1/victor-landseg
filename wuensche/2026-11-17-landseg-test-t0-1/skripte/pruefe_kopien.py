"""Teil 1 von landseg-test-t0: Kopien B/C gegen A, frisches kacheln gegen A, Messzeilen der Vorstufe.

Aufruf: PY -I pruefe_kopien.py <T0-Ordner> <frisch-gekachelter Ordner> <Ausgabe.json>
"""
import hashlib
import json
import sys
from pathlib import Path

T0 = Path(sys.argv[1])
FRISCH = Path(sys.argv[2])
AUS = Path(sys.argv[3])
A = T0 / "kern500"
FASSUNGEN = ["fassung-b", "fassung-c"]


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def dateien(wurzel: Path) -> dict:
    """Eingaben der Fassungen: Ausschnitt, Manifest, Teilkacheln, Vorstufe (nicht probe-b/seite)."""
    out = {}
    for rel in ["T0.png", "T0.pgw", "manifest.json"]:
        out[rel] = sha(wurzel / rel)
    for unter in ["teilkacheln", "vorstufe"]:
        for p in sorted((wurzel / unter).rglob("*")):
            if p.is_file():
                out[p.relative_to(wurzel).as_posix()] = sha(p)
    return out


ergebnis = {"kopien": {}, "frisch": {}, "messung": {}}
a = dateien(A)
ergebnis["dateien_a"] = len(a)
for f in FASSUNGEN:
    b = dateien(T0 / f)
    ergebnis["kopien"][f] = {
        "gleich": sorted(k for k in a if b.get(k) == a[k]).__len__(),
        "anders": sorted(k for k in a if k in b and b[k] != a[k]),
        "fehlt": sorted(k for k in a if k not in b),
        "zusaetzlich": sorted(k for k in b if k not in a),
    }

# frisch gekachelt: Bilder und Weltdateien bildpunkt-/bytegleich, Manifest bis auf "erstellt"
fr = {}
for rel in ["T0.png", "T0.pgw"] + [p.relative_to(FRISCH).as_posix()
                                   for p in sorted((FRISCH / "teilkacheln").glob("*"))]:
    fr[rel] = (sha(FRISCH / rel) == a.get(rel))
ma = json.loads((A / "manifest.json").read_text(encoding="utf-8"))
mf = json.loads((FRISCH / "manifest.json").read_text(encoding="utf-8"))
ma.pop("erstellt", None)
mf.pop("erstellt", None)
fr["manifest.json (ohne erstellt)"] = (ma == mf)
ergebnis["frisch"] = fr

for tk in sorted(p.name for p in (A / "vorstufe").iterdir() if p.is_dir()):
    seg = json.loads((A / "vorstufe" / tk / "segmente.json").read_text(encoding="utf-8"))
    m = seg["vorstufe"]["messung"]
    kern = [s for s in seg["segmente"] if s.get("im_kern")]
    ergebnis["messung"][tk] = {
        "konfig": seg["vorstufe"]["konfig"], "sam3": seg["vorstufe"]["sam3"],
        "erstellt": seg["vorstufe"]["erstellt"],
        "segmente": m["segmente"], "segmente_im_kern": m["segmente_im_kern"],
        "kern_nachgezaehlt": len(kern),
        "kern_sicher_nein": sum(1 for s in kern if s.get("sicher") == "nein"),
        "anteil_sicher_nein": m["anteil_sicher_nein"], "flaeche_sicher_nein": m["flaeche_sicher_nein"],
        "kandidaten": m["kandidaten"], "im_siedlung_ja": m.get("im_siedlung_ja"),
        "laufzeit_s": m["laufzeit_s"], "pruefen_ok": seg["vorstufe"]["pruefen"]["ok"],
    }

AUS.write_text(json.dumps(ergebnis, ensure_ascii=False, indent=1), encoding="utf-8")
print(json.dumps(ergebnis, ensure_ascii=False, indent=1))
