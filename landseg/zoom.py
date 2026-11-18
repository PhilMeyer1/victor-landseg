"""zoom: vergrößerter Ausschnitt einer Stelle mit Segmentumrissen und Segmentnummern, auf Wunsch neben dem rohen
Luftbild; ein JPEG, höchstens ``lange_seite`` Bildpunkte an der langen Seite (Regel L11).

Die Stelle ist ein Punkt mit Radius, ein Rechteck oder eine Liste von Segmenten (Rahmen um alle, mit Rand); alle
Angaben in Bildpunkten des Teilkachelbilds. Gezeichnet wird mit ``ansicht.Ansicht`` (Umriss, Kernrahmen, Nummern);
gewählte Segmente sind zusätzlich farbig umrandet. Größen, Schrift und Farben in ``einstellungen/zoom.json``.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

from .ansicht import Ansicht, AnsichtFehler, Fenster
from .einigung import _schrift


def bild_rgb(bild: np.ndarray) -> np.ndarray:
    """Ausgabe von ``naht.lese_bild`` (float32, ein oder drei Kanäle) als RGB uint8 für ``Ansicht``."""
    rgb = np.clip(bild, 0, 255).astype(np.uint8)
    return np.repeat(rgb, 3, axis=2) if rgb.shape[2] == 1 else rgb[:, :, :3]


def bereich(a: Ansicht, *, punkt=None, radius: int | None = None, rechteck: dict | None = None,
            ids: list[int] | None = None, rand: int = 0) -> tuple[int, int, int, int]:
    """(x0, y0, x1, y1) der Stelle, auf das Bild beschnitten; genau eine Angabe."""
    h, w = a.bild.shape[:2]
    if sum(x is not None for x in (punkt, rechteck, ids)) != 1:
        raise AnsichtFehler("genau eine Stelle angeben: Punkt mit Radius, Rechteck oder Segmente")
    if punkt is not None:
        if radius is None or radius < 1:
            raise AnsichtFehler("ein Punkt braucht einen Radius >= 1")
        x0, y0, x1, y1 = punkt[0] - radius, punkt[1] - radius, punkt[0] + radius + 1, punkt[1] + radius + 1
    elif rechteck is not None:
        x0, y0 = rechteck["x"], rechteck["y"]
        x1, y1 = x0 + rechteck["breite"], y0 + rechteck["hoehe"]
    else:
        if a.karte is None:
            raise AnsichtFehler("Segmente als Stelle brauchen eine Label-Karte")
        fehlend = [i for i in ids if i not in a.lage]
        if fehlend or not ids:
            raise AnsichtFehler(f"Segmente nicht in der Label-Karte: {fehlend or ids}")
        lagen = [a.lage[i] for i in ids]
        x0, x1 = min(l[1].start for l in lagen) - rand, max(l[1].stop for l in lagen) + rand
        y0, y1 = min(l[0].start for l in lagen) - rand, max(l[0].stop for l in lagen) + rand
    x0, y0, x1, y1 = max(0, x0), max(0, y0), min(w, x1), min(h, y1)
    if x1 <= x0 or y1 <= y0:
        raise AnsichtFehler(f"die Stelle liegt außerhalb des Bilds ({w} × {h})")
    return x0, y0, x1, y1


def zoom(a: Ansicht, vorgaben: dict, ziel: str | Path, *, punkt=None, radius: int | None = None,
         rechteck: dict | None = None, ids: list[int] | None = None, roh: bool = False, titel: str = "") -> dict:
    """Zeichnet die Stelle nach ``ziel`` (JPEG) und gibt Fenster, Größe und Lage der Nummern zurück."""
    ziel = Path(ziel)
    if ziel.suffix.lower() not in (".jpg", ".jpeg"):
        raise AnsichtFehler(f"{ziel.name}: Zoombilder sind JPEG (Endung .jpg)")
    if a.karte is None:
        raise AnsichtFehler("der Zoom braucht eine Label-Karte (Umriss und Nummern)")
    x0, y0, x1, y1 = bereich(a, punkt=punkt, radius=radius, rechteck=rechteck, ids=ids,
                             rand=int(vorgaben["segment_rand"]))
    b, h = x1 - x0, y1 - y0
    tafeln, luecke, kopf = (2 if roh else 1), int(vorgaben["luecke"]), int(vorgaben["kopf"])
    lang = int(vorgaben["lange_seite"])
    faktor = max(1, min(int(vorgaben["hoechstfaktor"]), int(vorgaben["zielseite"]) // max(b, h),
                        (lang - luecke * (tafeln - 1)) // (b * tafeln), (lang - kopf) // h))
    f = Fenster(x0, y0, b, h, faktor)
    umriss = a.zeichnen("umriss", f)
    karte = a.karte[f.schnitt()]
    gross = np.repeat(np.repeat(karte, faktor, axis=0), faktor, axis=1)
    for sid in ids or []:
        if (karte == sid).any():
            a._segment_umriss(umriss, gross, sid, f)
    nummern = a._beschriften(umriss, f, text=str, ab=int(vorgaben["nummer_ab"]),
                             groesse=float(vorgaben["nummer_groesse"]))
    bilder = ([a.zeichnen("roh", f)] if roh else []) + [umriss]
    breite = sum(t.shape[1] for t in bilder) + luecke * (len(bilder) - 1)
    leinwand = Image.new("RGB", (breite, kopf + umriss.shape[0]), (20, 20, 24))
    schrift, x = _schrift(int(vorgaben["schrift"])), 0
    zeichnen = ImageDraw.Draw(leinwand)
    ueberschriften = (["Luftbild"] if roh else []) + ["Segmente mit Nummer (gelb: Grenze" + (", magenta: gewählt)" if ids else ")")]
    for tafel, text in zip(bilder, ueberschriften):
        leinwand.paste(Image.fromarray(tafel), (x, kopf))
        zeichnen.text((x + 4, kopf // 2 + 1), text, fill=(255, 235, 60), font=schrift)
        x += tafel.shape[1] + luecke
    zeichnen.text((4, 1), (f"{titel}: " if titel else "") + f"x {x0}–{x1 - 1}, y {y0}–{y1 - 1} (Bildpunkte der "
                  f"Teilkachel), {faktor}-fach", fill=(255, 255, 255), font=schrift)
    verkleinert = max(leinwand.size) > lang
    if verkleinert:
        leinwand.thumbnail((lang, lang), Image.LANCZOS)
    ziel.parent.mkdir(parents=True, exist_ok=True)
    leinwand.save(ziel, quality=int(vorgaben["jpeg_qualitaet"]))
    return {"ziel": str(ziel).replace("\\", "/"), "fenster": f.als_dict(), "groesse": list(leinwand.size),
            "roh": roh, "verkleinert": verkleinert, "nummern": nummern,
            "koordinaten": f"x_teilkachel = {x0} + (x_bild - versatz) // {faktor}, y_teilkachel = {y0} + "
                           f"(y_bild - {kopf}) // {faktor}; versatz der rechten Tafel "
                           f"{bilder[0].shape[1] + luecke if roh else 0}"}
