"""SHA-256, Größe und Dateizeit der Originale unter daten/luftbilder/historisch (nur lesen).

Aufruf: PY -I hash_scans.py <BASIS> <Ausgabe.json>
"""
import hashlib
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

BASIS = Path(sys.argv[1])
AUS = Path(sys.argv[2])
ORDNER = BASIS / "daten" / "luftbilder" / "historisch"


def sha(p: Path) -> dict:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for block in iter(lambda: f.read(1 << 22), b""):
            h.update(block)
    st = os.stat(p)
    return {"datei": p.name, "sha256": h.hexdigest(), "bytes": st.st_size, "mtime_ns": st.st_mtime_ns}


dateien = sorted(p for p in ORDNER.iterdir() if p.is_file())
with ThreadPoolExecutor(max_workers=len(dateien) or 1) as pool:
    erg = list(pool.map(sha, dateien))
AUS.write_text(json.dumps({"ordner": ORDNER.as_posix(), "dateien": erg}, indent=1), encoding="utf-8", newline="\n")
for e in erg:
    print(e["datei"], e["sha256"], e["bytes"])
