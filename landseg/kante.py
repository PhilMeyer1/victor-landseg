"""W4 ``kante``: Grenze zweier Nachbarsegmente im engen Band auf die Bildkante einrasten.

Ablauf (Einstellungen aus ``einstellungen/kante.json``):

1. Die bisherige Grenze zwischen ``a`` und ``b`` (optional nur innerhalb eines Polygons ``bereich``)
   bestimmt ein Band von ``band`` Bildpunkten zu beiden Seiten; nur Bildpunkte von ``a`` und ``b`` im
   Band dürfen die ID wechseln, alle anderen bleiben, die Karte bleibt also lückenlos.
2. Wasserscheide mit Marken (OpenCV) auf dem geglätteten Bild: Marken sind die Bildpunkte von ``a``
   und ``b`` direkt außerhalb des Bandes; das Band wird dazwischen an der stärksten Farbkante geteilt.
3. Entlang der neuen Grenze wird die Kantenstärke gemessen (Farbsprung je Bildpunkt in Lab). Wo sie
   unter ``kante_min`` liegt, gibt es im Bild keine Kante: dort bleibt die bisherige Grenze stehen,
   und die Strecke wird als „geschätzt" gemeldet, statt eine Kante zu raten.
4. Zerfällt ``a`` oder ``b`` dabei, gehen die abgetrennten Bandstücke an ihre alte ID zurück.

Koordinaten sind Bildpunkte der Label-Karte: ``x`` Spalte, ``y`` Zeile.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import cv2
import numpy as np
from scipy import ndimage

from .eingriff import EingriffFehler, polygon_maske
from .pruefen import VIERER

ACHTER = ndimage.generate_binary_structure(2, 2)


class KanteFehler(EingriffFehler):
    """Einrasten nicht möglich; nichts wurde geändert."""


@dataclass
class KantenErgebnis:
    karte: np.ndarray
    a: int
    b: int
    band: int
    kante_min: float
    nach_a: int = 0
    nach_b: int = 0
    grenze: int = 0
    geschaetzt: list[dict] = field(default_factory=list)

    @property
    def geschaetzt_laenge(self) -> int:
        return sum(s["laenge"] for s in self.geschaetzt)

    def als_dict(self, mit_punkten: bool = True) -> dict:
        strecken = self.geschaetzt if mit_punkten else [
            {k: v for k, v in s.items() if k != "punkte"} for s in self.geschaetzt]
        return {"a": self.a, "b": self.b, "band": self.band, "kante_min": self.kante_min,
                "umgeschrieben": {"nach_a": self.nach_a, "nach_b": self.nach_b},
                "grenze_laenge": self.grenze, "geschaetzt_laenge": self.geschaetzt_laenge,
                "eingerastet_laenge": self.grenze - self.geschaetzt_laenge,
                "geschaetzt": strecken}

    def als_text(self) -> str:
        zeilen = [
            f"kante {self.a}|{self.b}: Band ±{self.band} px, umgeschrieben {self.nach_a} px -> "
            f"{self.a}, {self.nach_b} px -> {self.b}",
            f"Grenze {self.grenze} px, an Bildkante eingerastet {self.grenze - self.geschaetzt_laenge}"
            f" px, geschätzt {self.geschaetzt_laenge} px in {len(self.geschaetzt)} Strecken",
        ]
        for nr, s in enumerate(self.geschaetzt, 1):
            zeilen.append(f"  geschätzt {nr}: von {tuple(s['von'])} bis {tuple(s['bis'])}, "
                          f"{s['laenge']} px, Kantenstärke {s['staerke']} (< {self.kante_min}): "
                          "keine Bildkante, Grenze unverändert")
        return "\n".join(zeilen)


def kantenstaerke(bild: np.ndarray, glaetten: float) -> np.ndarray:
    """Farbsprung je Bildpunkt in Lab-Einheiten (Sobel, auf eine Stufe normiert)."""
    weich = cv2.GaussianBlur(bild, (0, 0), glaetten) if glaetten > 0 else bild
    lab = cv2.cvtColor(weich, cv2.COLOR_RGB2LAB).astype(np.float32)
    summe = np.zeros(bild.shape[:2], np.float32)
    for k in range(3):
        gx = cv2.Sobel(lab[:, :, k], cv2.CV_32F, 1, 0, ksize=3)
        gy = cv2.Sobel(lab[:, :, k], cv2.CV_32F, 0, 1, ksize=3)
        summe += gx * gx + gy * gy
    return np.sqrt(summe) / 4.0


def _nachbarn(maske: np.ndarray) -> np.ndarray:
    """Bildpunkte mit einem 4er-Nachbarn in ``maske``."""
    return ndimage.binary_dilation(maske, structure=VIERER)


def grenze_zwischen(karte: np.ndarray, a: int, b: int) -> np.ndarray:
    """Bildpunkte von ``a`` mit 4er-Nachbar in ``b`` und umgekehrt."""
    ma, mb = karte == a, karte == b
    return (ma & _nachbarn(mb)) | (mb & _nachbarn(ma))


def _schwache_grenze(karte: np.ndarray, a: int, b: int, zone: np.ndarray, staerke: np.ndarray,
                     kante_min: float) -> np.ndarray:
    """Grenzpunkte auf der Seite von ``a``, an denen weder sie noch ihr Nachbar in ``b`` auf einer
    Bildkante liegen (Kantenstärke beider Seiten unter ``kante_min``)."""
    ma, mb = karte == a, karte == b
    stark_b = ndimage.binary_dilation(mb & (staerke >= kante_min), structure=VIERER)
    return ma & _nachbarn(mb) & zone & (staerke < kante_min) & ~stark_b


def _strecken(schwach: np.ndarray, staerke: np.ndarray, mindest: int) -> list[dict]:
    teile, anzahl = ndimage.label(schwach, structure=ACHTER)
    strecken = []
    for nr in range(1, anzahl + 1):
        ys, xs = np.nonzero(teile == nr)
        if len(xs) < mindest:
            continue
        # Endpunkte: die beiden am weitesten auseinanderliegenden entlang der Hauptrichtung.
        achse = xs if np.ptp(xs) >= np.ptp(ys) else ys
        i0, i1 = int(np.argmin(achse)), int(np.argmax(achse))
        strecken.append({
            "von": [int(xs[i0]), int(ys[i0])], "bis": [int(xs[i1]), int(ys[i1])],
            "laenge": int(len(xs)),
            "staerke": round(float(staerke[ys, xs].mean()), 1),
            "punkte": [[int(x), int(y)] for x, y in zip(xs, ys)],
        })
    return sorted(strecken, key=lambda s: (s["von"][1], s["von"][0]))


def _zusammenhalt_sichern(neu: np.ndarray, alt: np.ndarray, sid: int, band: int) -> None:
    """Hat das Umschreiben ``sid`` zerschnitten (abgetrennte Teile aus alten Bildpunkten), werden die
    Änderungen rund um die abgetrennten Teile zurückgenommen; hilft das nicht, KanteFehler."""
    if ndimage.label(alt == sid, structure=VIERER)[1] > 1:
        return  # war schon vorher zerfallen; pruefen meldet es
    for _ in range(3):
        teile, anzahl = ndimage.label(neu == sid, structure=VIERER)
        if anzahl < 2:
            return
        groessen = np.bincount(teile.ravel())[1:]
        klein = (teile > 0) & (teile != int(np.argmax(groessen)) + 1)
        umfeld = ndimage.distance_transform_edt(~klein) <= 2 * band + 2
        zurueck = umfeld & (neu != alt)
        neu[zurueck] = alt[zurueck]
    if ndimage.label(neu == sid, structure=VIERER)[1] > 1:
        raise KanteFehler(f"Segment {sid} zerfiele beim Einrasten; Bereich angeben oder Band "
                          "verkleinern")


def _grat_zuordnen(flut: np.ndarray, bild: np.ndarray) -> None:
    """Grat-Bildpunkte der Wasserscheide (-1) gehen an den 4er-Nachbarn aus a (1) oder b (2), dessen
    Farbe ihnen am nächsten ist; ohne solchen Nachbarn bleiben sie bei ihrer alten ID (0)."""
    grat = flut == -1
    if not grat.any():
        return
    farbe = np.pad(bild.astype(np.int32), ((1, 1), (1, 1), (0, 0)), mode="edge")
    marke = np.pad(flut, 1, constant_values=0)
    hoehe, breite = flut.shape
    mitte = farbe[1:-1, 1:-1]
    beste = np.zeros(flut.shape, np.int32)
    abstand = np.full(flut.shape, np.iinfo(np.int32).max)
    for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        nachbar = marke[1 + dy:1 + dy + hoehe, 1 + dx:1 + dx + breite]
        d = np.abs(mitte - farbe[1 + dy:1 + dy + hoehe, 1 + dx:1 + dx + breite]).sum(axis=2)
        besser = grat & ((nachbar == 1) | (nachbar == 2)) & (d < abstand)
        beste[besser] = nachbar[besser]
        abstand[besser] = d[besser]
    flut[grat] = beste[grat]


def _zerfall_heilen(neu: np.ndarray, alt: np.ndarray, sid: int) -> None:
    """Behält vom Segment ``sid`` nur das größte Stück; Bandstücke gehen an ihre alte ID zurück."""
    teile, anzahl = ndimage.label(neu == sid, structure=VIERER)
    if anzahl < 2:
        return
    groessen = np.bincount(teile.ravel())[1:]
    behalten = int(np.argmax(groessen)) + 1
    abgetrennt = (teile > 0) & (teile != behalten)
    neu[abgetrennt] = alt[abgetrennt]


def einrasten(bild: np.ndarray, karte: np.ndarray, a: int, b: int, vorgaben: dict, *,
              band: int | None = None, bereich=None) -> KantenErgebnis:
    """Rastet die Grenze zwischen ``a`` und ``b`` ein; ändert ``karte`` nicht (Ergebnis-Kopie)."""
    a, b = int(a), int(b)
    band = int(vorgaben["band"] if band is None else band)
    kante_min = float(vorgaben["kante_min"])
    if bild.shape[:2] != karte.shape:
        raise KanteFehler(f"Bild {bild.shape[:2]} passt nicht zur Label-Karte {karte.shape}")
    if a == b:
        raise KanteFehler("a und b sind dasselbe Segment")
    if band < 1:
        raise KanteFehler("band muss mindestens 1 sein")
    for sid in (a, b):
        if not (karte == sid).any():
            raise KanteFehler(f"Segment {sid} gibt es nicht")
    zone = polygon_maske(karte.shape, bereich) if bereich is not None else np.ones(karte.shape, bool)
    grenze0 = grenze_zwischen(karte, a, b) & zone
    if not grenze0.any():
        raise KanteFehler(f"Segmente {a} und {b} grenzen {'im Bereich ' if bereich else ''}nicht "
                          "aneinander")
    ab = (karte == a) | (karte == b)
    abstand = ndimage.distance_transform_edt(~grenze0)
    im_band = ab & zone & (abstand <= band)

    # Marken: Bildpunkte von a bzw. b direkt außerhalb des Bandes; fehlen sie (Segment schmaler als
    # das Band), bleibt der am weitesten von der Grenze entfernte Teil fest.
    ring = _nachbarn(im_band) & ~im_band
    marken = np.zeros(karte.shape, np.int32)
    for wert, sid in ((1, a), (2, b)):
        marke = ring & zone & (karte == sid)  # außerhalb des Bereichs: fest
        if not marke.any():
            seg = (karte == sid) & im_band
            weit = abstand[seg].max()
            marke = seg & (abstand >= weit)
            im_band &= ~marke
        marken[marke] = wert
    marken[~(im_band | (marken > 0))] = 3  # alles andere: fest, wird nicht geflutet

    staerke = kantenstaerke(bild, float(vorgaben["glaetten"]))
    weich = cv2.GaussianBlur(bild, (0, 0), float(vorgaben["glaetten"])) \
        if vorgaben["glaetten"] > 0 else bild
    ys, xs = np.nonzero(im_band | (marken == 1) | (marken == 2))
    y0, y1 = max(0, ys.min() - 1), min(karte.shape[0], ys.max() + 2)
    x0, x1 = max(0, xs.min() - 1), min(karte.shape[1], xs.max() + 2)
    # Ein Bildpunkt Rand ringsum, weil OpenCV den äußersten Rand des Ausschnitts als Grat markiert.
    ausschnitt = cv2.copyMakeBorder(cv2.cvtColor(weich[y0:y1, x0:x1], cv2.COLOR_RGB2BGR),
                                    1, 1, 1, 1, cv2.BORDER_REPLICATE)
    flut = np.pad(marken[y0:y1, x0:x1], 1)
    # Feste Bildpunkte (3) sollen nicht ins Band fluten: im Arbeitsbild weit weg von ihrer Farbe
    # setzen, damit ein Schritt von dort aus erst nach allen Schritten von a und b dran käme.
    fest = flut == 3
    ausschnitt[fest] = np.where(ausschnitt[fest] > 127, 0, 255).astype(np.uint8)
    cv2.watershed(ausschnitt, flut)
    flut = flut[1:-1, 1:-1]
    _grat_zuordnen(flut, bild[y0:y1, x0:x1])
    ergebnis = np.zeros(karte.shape, np.int32)
    ergebnis[y0:y1, x0:x1] = flut

    neu = karte.copy()
    neu[im_band & (ergebnis == 1)] = a
    neu[im_band & (ergebnis == 2)] = b
    for sid in (a, b):
        _zerfall_heilen(neu, karte, sid)

    # Wo die neue Grenze auf keiner Bildkante liegt: alte Grenze behalten (nicht raten).
    mindest = int(vorgaben["strecke_min"])
    schwach = _schwache_grenze(neu, a, b, zone, staerke, kante_min)
    if schwach.any():
        teile, anzahl = ndimage.label(schwach, structure=ACHTER)
        groessen = np.bincount(teile.ravel())
        lang = np.isin(teile, [i for i in range(1, anzahl + 1) if groessen[i] >= mindest])
        if lang.any():
            zurueck = im_band & (ndimage.distance_transform_edt(~lang) <= band + 1)
            neu[zurueck] = karte[zurueck]
            for sid in (a, b):
                _zerfall_heilen(neu, karte, sid)
    for sid in (a, b):
        if not (neu == sid).any():
            raise KanteFehler(f"Segment {sid} verschwände; Band verkleinern")
        _zusammenhalt_sichern(neu, karte, sid, band)
    for sid in (a, b):  # die Rücknahme für a kann b berühren und umgekehrt
        if (ndimage.label(neu == sid, structure=VIERER)[1] > 1
                and ndimage.label(karte == sid, structure=VIERER)[1] == 1):
            raise KanteFehler(f"Segment {sid} zerfiele beim Einrasten; Bereich angeben oder Band "
                              "verkleinern")

    # Längen in Bildpunkten der Grenze auf der Seite von a.
    seite_a = grenze_zwischen(neu, a, b) & zone & (neu == a)
    geschaetzt = _strecken(_schwache_grenze(neu, a, b, zone, staerke, kante_min), staerke, mindest)
    return KantenErgebnis(
        karte=neu, a=a, b=b, band=band, kante_min=kante_min,
        nach_a=int(((karte == b) & (neu == a)).sum()), nach_b=int(((karte == a) & (neu == b)).sum()),
        grenze=int(seite_a.sum()), geschaetzt=geschaetzt)
