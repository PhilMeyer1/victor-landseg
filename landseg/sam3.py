"""SAM 3 für die Vorstufe (Schritte b und c): Instanzmasken und Semantikwerte je Text.

Übernommen und angepasst aus dem Stitcher (``scripts/sam3_pipeline/sam3_model.py``): transformers
``Sam3Model``/``Sam3Processor``, FP16 auf der GPU. Neu: Das Bild eines Fensters wird einmal kodiert
(``get_vision_features``), jeder Text läuft dann nur durch Dekoder und Köpfe. Je Text:

- Instanzen: ``post_process_instance_segmentation`` (Wert = Instanz mal Presence);
- Semantik: Sigmoid des Semantikkopfs mal Presence (Nachbau SegEarth-OV3);
- Textwert je Bildpunkt = Maximum aus Semantik und Wert × Maske jeder Instanz;
- Klassenwert = Maximum über die Texte der Klasse.

Bilder bis ``fenster_px`` laufen in einem Fenster, größere im Schiebefenster (Werte gemittelt,
doppelte Instanzen gleicher Klasse nach IoU entfernt). Die GPU ist Pflicht: ohne CUDA bricht das
Laden ab, statt still auf der CPU zu rechnen.
"""

from __future__ import annotations

import numpy as np
from PIL import Image

from .vorstufe import Instanz, Roh, VorstufeFehler


def fenster(hoehe: int, breite: int, groesse: int, ueberlapp: float) -> list[tuple[int, int, int, int]]:
    """(x0, y0, x1, y1) je Fenster; deckt das Bild ganz ab, ein Fenster, wenn es hineinpasst."""
    def achse(laenge: int) -> list[int]:
        if laenge <= groesse:
            return [0]
        schritt = max(1, int(groesse * (1 - ueberlapp)))
        starts = list(range(0, laenge - groesse, schritt)) + [laenge - groesse]
        return sorted(set(starts))
    return [(x, y, min(breite, x + groesse), min(hoehe, y + groesse))
            for y in achse(hoehe) for x in achse(breite)]


def _rahmen(maske: np.ndarray) -> tuple[int, int, int, int]:
    ys, xs = np.nonzero(maske)
    return int(ys.min()), int(ys.max()) + 1, int(xs.min()), int(xs.max()) + 1


def _iou(a: np.ndarray, b: np.ndarray, ra, rb) -> float:
    y0, y1 = min(ra[0], rb[0]), max(ra[1], rb[1])
    x0, x1 = min(ra[2], rb[2]), max(ra[3], rb[3])
    if max(ra[0], rb[0]) >= min(ra[1], rb[1]) or max(ra[2], rb[2]) >= min(ra[3], rb[3]):
        return 0.0  # Rahmen überlappen nicht
    a, b = a[y0:y1, x0:x1], b[y0:y1, x0:x1]
    vereinigt = np.logical_or(a, b).sum()
    return float(np.logical_and(a, b).sum() / vereinigt) if vereinigt else 0.0


class Sam3Vorschlag:
    def __init__(self, einst: dict, geraet: str = "cuda"):
        import torch
        from transformers import Sam3Model, Sam3Processor  # schwer: erst hier laden

        if geraet.startswith("cuda") and not torch.cuda.is_available():
            raise VorstufeFehler("SAM 3 braucht die GPU, CUDA ist nicht verfügbar "
                                 "(Befehl später wiederholen, nicht auf der CPU rechnen)")
        self.torch = torch
        self.einst = einst
        self.geraet = geraet
        self.dtype = torch.float16 if geraet.startswith("cuda") else torch.float32
        revision = einst.get("revision")
        self.processor = Sam3Processor.from_pretrained(einst["modell"], revision=revision)
        self.model = (Sam3Model.from_pretrained(einst["modell"], dtype=self.dtype, revision=revision)
                      .to(geraet).eval())
        self._texte: dict[str, dict] = {}

    def _text(self, text: str) -> dict:
        if text not in self._texte:
            self._texte[text] = self.processor(text=text, return_tensors="pt").to(self.geraet)
        return self._texte[text]

    def _fenster(self, bild: np.ndarray, n_klassen: int, texte: list[tuple[int, str]]):
        torch = self.torch
        h, w = bild.shape[:2]
        e = self.einst
        eingabe = self.processor(images=Image.fromarray(bild), return_tensors="pt").to(self.geraet)
        sicht = self.model.get_vision_features(pixel_values=eingabe["pixel_values"].to(self.dtype))
        werte = np.zeros((n_klassen, h, w), np.float32)
        instanzen: list[Instanz] = []
        for klasse, text in texte:
            t = self._text(text)
            aus = self.model(vision_embeds=sicht, input_ids=t["input_ids"],
                             attention_mask=t["attention_mask"])
            presence = torch.sigmoid(aus.presence_logits.float()).reshape(-1)[0]
            sem = torch.nn.functional.interpolate(aus.semantic_seg.float(), size=(h, w),
                                                  mode="bilinear", align_corners=False)
            textwert = (torch.sigmoid(sem)[0, 0] * presence).cpu().numpy()
            res = self.processor.post_process_instance_segmentation(
                aus, threshold=e["instanz_schwelle"], mask_threshold=e["maskenschwelle"],
                target_sizes=[(h, w)])[0]
            masken, punkte = res.get("masks"), res.get("scores")
            for i in range(0 if masken is None else len(masken)):
                maske = masken[i].detach().cpu().numpy().astype(bool)
                wert = float(punkte[i])
                if maske.any():
                    instanzen.append(Instanz(klasse, wert, maske, text))
                    np.maximum(textwert, maske * np.float32(wert), out=textwert)
            np.maximum(werte[klasse], textwert, out=werte[klasse])
        return werte, instanzen

    def berechne(self, bild: np.ndarray, klassen: list[str], texte: list[tuple[int, str]]) -> Roh:
        with self.torch.inference_mode():
            h, w = bild.shape[:2]
            e = self.einst
            summe = np.zeros((len(klassen), h, w), np.float32)
            zahl = np.zeros((h, w), np.float32)
            instanzen: list[Instanz] = []
            for x0, y0, x1, y1 in fenster(h, w, int(e["fenster_px"]), float(e["ueberlapp"])):
                werte, funde = self._fenster(np.ascontiguousarray(bild[y0:y1, x0:x1]),
                                             len(klassen), texte)
                summe[:, y0:y1, x0:x1] += werte
                zahl[y0:y1, x0:x1] += 1
                for f in funde:
                    voll = np.zeros((h, w), bool)
                    voll[y0:y1, x0:x1] = f.maske
                    instanzen.append(Instanz(f.klasse, f.wert, voll, f.text))
            if self.geraet.startswith("cuda"):
                self.torch.cuda.empty_cache()
        return Roh(list(klassen), summe / np.maximum(zahl, 1), entdoppeln(instanzen, e))


def entdoppeln(instanzen: list[Instanz], einst: dict) -> list[Instanz]:
    """Gleiche Klasse und IoU über der Schwelle: nur der stärkere Fund bleibt."""
    schwelle = float(einst.get("instanz_doppelt_iou", 0.5))
    behalten: list[tuple[Instanz, tuple]] = []
    for kandidat in sorted(instanzen, key=lambda i: -i.wert):
        rk = _rahmen(kandidat.maske)
        if not any(b.klasse == kandidat.klasse and _iou(b.maske, kandidat.maske, rb, rk) > schwelle
                   for b, rb in behalten):
            behalten.append((kandidat, rk))
    return [b for b, _ in behalten]
