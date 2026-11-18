"""W1 ``kacheln``: Arbeitsausschnitt aus einem Bild schneiden und in Teilkacheln zerlegen.

Jede Teilkachel hat einen Kern (``kern`` × ``kern`` Bildpunkte, am rechten und unteren Rand des
Ausschnitts kleiner, wenn der Ausschnitt nicht aufgeht) und rundum einen Kontextrand von ``rand``
Bildpunkten. Der Kontext kommt aus dem Quellbild, auch über den Ausschnitt hinaus, und endet nur am
Rand des Quellbilds. Die Kerne zerlegen den Ausschnitt lückenlos und ohne Überlappung.

Das Manifest (``manifest.json``) nennt alle Pfade relativ zu seinem Ordner und die Georeferenz
(Weltdatei ``.tfw`` bzw. GeoTIFF-Tags, Lagebezug aus ``.prj``) für Quelle, Ausschnitt und jede
Teilkachel; ohne Weltdatei und GeoTIFF-Tags (etwa ein gescanntes Luftbild) ist ``georeferenz`` ``null`` und
es entstehen keine ``.pgw``. Graustufenbilder bleiben einkanalig (``kanaele: 1``); ein Palettenbild wird über
seine Farbtafel in Farben bzw., wenn die Tafel nur Grautöne hat, in Graustufen übersetzt, nicht als Indizes
geschrieben.
"""

from __future__ import annotations

import os
import re
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image

from .dateien import MANIFEST_SCHEMA, schreibe_json


class KachelFehler(Exception):
    pass


def _begleitdatei(bild: Path, endungen: tuple[str, ...]) -> Path | None:
    for kandidat in bild.parent.iterdir():
        if kandidat.stem == bild.stem and kandidat.suffix.lower() in endungen:
            return kandidat
    return None


def _transform_aus_weltdatei(pfad: Path) -> dict:
    werte = [float(z) for z in pfad.read_text(encoding="ascii").split()]
    if len(werte) != 6:
        raise KachelFehler(f"{pfad}: Weltdatei braucht 6 Zahlen, hat {len(werte)}")
    a, d, b, e, c, f = werte  # Mitte des Bildpunkts oben links
    return {"a": a, "b": b, "c": c - 0.5 * a - 0.5 * b, "d": d, "e": e, "f": f - 0.5 * d - 0.5 * e}


def _transform_aus_geotiff(seite) -> dict | None:
    tags = seite.tags
    if "ModelPixelScaleTag" not in tags or "ModelTiepointTag" not in tags:
        return None
    sx, sy = tags["ModelPixelScaleTag"].value[:2]
    i, j, _, x, y, _ = tags["ModelTiepointTag"].value[:6]
    return {"a": sx, "b": 0.0, "c": x - i * sx, "d": 0.0, "e": -sy, "f": y + j * sy}


def georeferenz(bild: Path, seite=None) -> dict | None:
    """Affine Abbildung Bildpunkt-Ecke -> Lage: ``X = a·x + b·y + c``, ``Y = d·x + e·y + f``."""
    transform = None
    quelle = None
    welt = _begleitdatei(bild, (".tfw", ".tifw", ".wld"))
    if welt is not None:
        transform, quelle = _transform_aus_weltdatei(welt), welt.name
    elif seite is not None:
        transform = _transform_aus_geotiff(seite)
        quelle = "GeoTIFF-Tags" if transform else None
    if transform is None:
        return None
    geo = {"transform": transform, "quelle": quelle, "crs_wkt": None, "epsg": None}
    prj = _begleitdatei(bild, (".prj",))
    if prj is not None:
        wkt = prj.read_text(encoding="utf-8", errors="replace").strip()
        geo["crs_wkt"] = wkt
        treffer = re.search(r'AUTHORITY\["EPSG","(\d+)"\]\]\s*$', wkt)
        geo["epsg"] = int(treffer.group(1)) if treffer else None
    return geo


def verschoben(transform: dict, x: int, y: int) -> dict:
    """Transform eines Bildes, dessen Bildpunkt (0, 0) im Ausgangsbild bei (x, y) liegt."""
    t = dict(transform)
    t["c"] = transform["a"] * x + transform["b"] * y + transform["c"]
    t["f"] = transform["d"] * x + transform["e"] * y + transform["f"]
    return t


def _schreibe_weltdatei(pfad: Path, t: dict) -> None:
    mitte_x = t["c"] + 0.5 * t["a"] + 0.5 * t["b"]
    mitte_y = t["f"] + 0.5 * t["d"] + 0.5 * t["e"]
    zeilen = [t["a"], t["d"], t["b"], t["e"], mitte_x, mitte_y]
    pfad.write_text("".join(f"{z:.10f}\n" for z in zeilen), encoding="ascii", newline="\n")


def _relativ(pfad: Path, basis: Path) -> str:
    try:
        return Path(os.path.relpath(pfad, basis)).as_posix()
    except ValueError as fehler:  # anderes Laufwerk: kein relativer Pfad möglich
        raise KachelFehler(f"Quelle {pfad} und Ziel {basis} liegen auf verschiedenen Laufwerken") from fehler


def _lese_quelle(bild: Path):
    with tifffile.TiffFile(bild) as tif:
        seite = tif.pages[0]
        try:
            daten = tifffile.memmap(bild, page=0, mode="r")
        except ValueError:  # komprimiert oder gekachelt: ganz lesen
            daten = seite.asarray()
        return daten, seite, farbtafel(seite)  # Farbtafel lesen, solange die Datei offen ist


def farbtafel(seite) -> np.ndarray | None:
    """Farbtafel eines Palettenbilds als uint8, Index -> Grauwert (Tafel nur aus Grautönen) bzw. Index -> RGB;
    ``None`` bei anderen Bildern."""
    if seite.photometric != tifffile.PHOTOMETRIC.PALETTE or seite.colormap is None:
        return None
    tafel = np.asarray(seite.colormap).T  # (Einträge, 3)
    if tafel.max() > 255:  # TIFF speichert 16 Bit je Kanal
        tafel = tafel >> 8
    tafel = tafel.astype(np.uint8)
    return tafel[:, 0].copy() if (tafel == tafel[:, :1]).all() else tafel


def raster(breite: int, hoehe: int, kern: int) -> list[tuple[int, int, int, int, int, int]]:
    """(zeile, spalte, x, y, kernbreite, kernhöhe) je Teilkachel, Kerne lückenlos über den Ausschnitt."""
    if kern <= 0:
        raise KachelFehler("Kerngröße muss > 0 sein")
    felder = []
    for zeile, y in enumerate(range(0, hoehe, kern)):
        for spalte, x in enumerate(range(0, breite, kern)):
            felder.append((zeile, spalte, x, y, min(kern, breite - x), min(kern, hoehe - y)))
    return felder


def kacheln(bild: str | Path, x: int, y: int, breite: int, hoehe: int, ziel: str | Path,
            kern: int = 500, rand: int = 64, name: str = "ausschnitt",
            ueberschreiben: bool = False) -> dict:
    """Schneidet den Ausschnitt, schreibt Bilder und ``manifest.json`` nach ``ziel``."""
    bild, ziel = Path(bild).resolve(), Path(ziel).resolve()
    if rand < 0:
        raise KachelFehler("Kontextrand muss >= 0 sein")
    manifest_pfad = ziel / "manifest.json"
    if manifest_pfad.exists() and not ueberschreiben:
        raise KachelFehler(f"{manifest_pfad} gibt es schon (--ueberschreiben, um es zu ersetzen)")

    daten, seite, tafel = _lese_quelle(bild)
    q_hoehe, q_breite = daten.shape[:2]
    if x < 0 or y < 0 or breite <= 0 or hoehe <= 0 or x + breite > q_breite or y + hoehe > q_hoehe:
        raise KachelFehler(
            f"Ausschnitt x {x}, y {y}, {breite} × {hoehe} liegt nicht im Bild ({q_breite} × {q_hoehe})")
    geo = georeferenz(bild, seite)

    ordner = ziel / "teilkacheln"
    ordner.mkdir(parents=True, exist_ok=True)
    for alt in ordner.iterdir():  # Reste eines früheren Rasters (nur eigene Dateinamen)
        if re.fullmatch(r"r\d+c\d+\.(png|pgw)", alt.name):
            alt.unlink()

    def speichern(pfad: Path, x0: int, y0: int, b: int, h: int) -> None:
        stueck = np.ascontiguousarray(daten[y0:y0 + h, x0:x0 + b])
        Image.fromarray(stueck if tafel is None else tafel[stueck]).save(pfad)
        if geo:
            _schreibe_weltdatei(pfad.with_suffix(".pgw"), verschoben(geo["transform"], x0, y0))

    speichern(ziel / f"{name}.png", x, y, breite, hoehe)
    teilkacheln = []
    for zeile, spalte, kx, ky, kb, kh in raster(breite, hoehe, kern):
        qx0, qy0 = max(0, x + kx - rand), max(0, y + ky - rand)
        qx1, qy1 = min(q_breite, x + kx + kb + rand), min(q_hoehe, y + ky + kh + rand)
        kid = f"r{zeile}c{spalte}"
        pfad = ordner / f"{kid}.png"
        speichern(pfad, qx0, qy0, qx1 - qx0, qy1 - qy0)
        eintrag = {
            "id": kid,
            "zeile": zeile,
            "spalte": spalte,
            "bild": _relativ(pfad, ziel),
            "kern": {"x": kx, "y": ky, "breite": kb, "hoehe": kh},
            "kontext": {"x": qx0 - x, "y": qy0 - y, "breite": qx1 - qx0, "hoehe": qy1 - qy0},
            "kern_im_bild": {"x": x + kx - qx0, "y": y + ky - qy0, "breite": kb, "hoehe": kh},
        }
        if geo:
            eintrag["transform"] = verschoben(geo["transform"], qx0, qy0)
        teilkacheln.append(eintrag)

    manifest = {
        "schema": MANIFEST_SCHEMA,
        "erstellt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "quelle": {"bild": _relativ(bild, ziel), "breite": q_breite, "hoehe": q_hoehe,
                   "kanaele": (1 if daten.ndim == 2 else int(daten.shape[2])) if tafel is None
                   else (1 if tafel.ndim == 1 else 3)},
        "ausschnitt": {"name": name, "x": x, "y": y, "breite": breite, "hoehe": hoehe,
                       "bild": f"{name}.png"},
        "raster": {"kern": kern, "rand": rand,
                   "zeilen": max(t["zeile"] for t in teilkacheln) + 1,
                   "spalten": max(t["spalte"] for t in teilkacheln) + 1},
        "koordinaten": "Bildpunkte; kern und kontext relativ zum Ausschnitt, kern_im_bild relativ "
                       "zum Bild der Teilkachel; transform: X = a·x + b·y + c, Y = d·x + e·y + f "
                       "für die Ecke oben links des Bildpunkts (x, y)",
        "georeferenz": None,
        "teilkacheln": teilkacheln,
    }
    if geo:
        manifest["georeferenz"] = {k: v for k, v in geo.items() if k != "transform"}
        manifest["georeferenz"]["transform_quelle"] = geo["transform"]
        manifest["ausschnitt"]["transform"] = verschoben(geo["transform"], x, y)
    schreibe_json(manifest_pfad, manifest)
    return manifest
