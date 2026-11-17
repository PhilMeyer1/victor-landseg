"""W7 zusammentragen und Nahtregel: zwei Teilkacheln (Kern 20, Rand 4) aus einem synthetischen Bild.

Ausschnitt 40 × 20, Kerngrenze bei x = 20. Bild und Wahrheit:
- Zeilen 0–9: links (x < 20) Segment 1 grün, rechts Segment 2 grau; der Farbsprung liegt genau auf
  der Kerngrenze, also eine echte Bildkante.
- Zeilen 10–19: Segment 3 (braun) reicht über die Grenze bis x 29, rechts davon Segment 4 (blau).
"""

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import numpy as np
import tifffile

from landseg import dateien
from landseg.__main__ import main
from landseg.kacheln import kacheln
from landseg.zusammentragen import ZusammenFehler, zusammentragen
from tests.hilfe import beispiel_kategorien

KLASSEN = {1: "3.1", 2: "1.1", 3: "3", 4: "1"}


def wahrheit(hoehe: int = 24, breite: int = 44) -> tuple[np.ndarray, np.ndarray]:
    bild = np.zeros((hoehe, breite, 3), np.uint8)
    karte = np.zeros((hoehe, breite), np.uint32)
    bild[:10, :20], karte[:10, :20] = (40, 160, 40), 1
    bild[:10, 20:], karte[:10, 20:] = (150, 150, 150), 2
    bild[10:, :30], karte[10:, :30] = (120, 90, 50), 3
    bild[10:, 30:], karte[10:, 30:] = (40, 60, 200), 4
    return bild, karte


class ZusammentragenTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ordner = Path(self.tmp.name)
        self.kat = beispiel_kategorien(self.ordner)
        bild, self.karte = wahrheit()
        tifffile.imwrite(self.ordner / "quelle.tif", bild, photometric="rgb")
        self.manifest = kacheln(self.ordner / "quelle.tif", 0, 0, 40, 20, self.ordner / "aus",
                                kern=20, rand=4, name="aus")
        self.einheiten = []
        for tk in self.manifest["teilkacheln"]:
            self.abgabe(tk["id"], KLASSEN)

    def tearDown(self):
        self.tmp.cleanup()

    def teilkachel(self, tid: str) -> dict:
        return next(t for t in self.manifest["teilkacheln"] if t["id"] == tid)

    def abgabe(self, tid: str, klassen: dict, aendern=None, runde: int = 0) -> None:
        """Label-Karte (Kern + Kontext) und segmente.json einer Teilkachel aus der Wahrheit."""
        kx = self.teilkachel(tid)["kontext"]
        karte = self.karte[kx["y"]:kx["y"] + kx["hoehe"], kx["x"]:kx["x"] + kx["breite"]].copy()
        if aendern:
            aendern(karte)
        eintraege = [{"id": s, "klasse": klassen[s], "grob": klassen[s].split(".")[0], "herkunft": "test"}
                     for s in np.unique(karte).tolist()]
        ordner = self.ordner / "aus" / f"{tid}-runde{runde}"
        dateien.schreibe_labels(ordner / "labels.tif", karte)
        dateien.schreibe_json(ordner / "segmente.json", {"segmente": eintraege, "verlauf": []})
        self.einheiten = [e for e in self.einheiten if not (e["teilkachel"] == tid and e["runde"] == runde)]
        self.einheiten.append({"teilkachel": tid, "labels": f"{tid}-runde{runde}/labels.tif",
                               "segmente": f"{tid}-runde{runde}/segmente.json", "runde": runde})

    def auftrag(self, **mehr) -> Path:
        pfad = self.ordner / "aus" / "zusammentragen.json"
        dateien.schreibe_json(pfad, {"schema": "landseg-zusammentragen/1", "manifest": "manifest.json",
                                     "einheiten": self.einheiten, "ziel": "zusammen", **mehr})
        return pfad

    def test_sauber_fuegt_kerne_zur_bild_karte(self):
        ergebnis = zusammentragen(self.auftrag(), self.kat)
        self.assertTrue(ergebnis.ok, ergebnis.als_text())
        np.testing.assert_array_equal(ergebnis.karte, self.karte[:20, :40])
        geschrieben = dateien.lese_labels(self.ordner / "aus" / "zusammen" / "labels.tif")
        np.testing.assert_array_equal(geschrieben, self.karte[:20, :40])
        segmente = dateien.lese_json(self.ordner / "aus" / "zusammen" / "segmente.json")
        nach_id = {s["id"]: s for s in segmente["segmente"]}
        self.assertEqual(sorted(nach_id), [1, 2, 3, 4])
        self.assertEqual(nach_id[3]["teilkacheln"], ["r0c0", "r0c1"])
        naht = ergebnis.naht.naehte[0]
        self.assertEqual((naht["naht"], naht["positionen"], naht["gleiche_id"], naht["andere_id_mit_kante"]),
                         ("r0c0|r0c1", 20, 10, 10))
        self.assertTrue(dateien.lese_json(self.ordner / "aus" / "zusammen" / "naht.json")["ok"])

    def test_naht_verletzung_ohne_bildkante_wird_gemeldet(self):
        # rechte Teilkachel gibt dem Stück von Segment 3 in ihrem Kern eine andere ID
        def neue_id(karte):
            ix = self.teilkachel("r0c1")["kern_im_bild"]
            kern = karte[ix["y"]:ix["y"] + 20, ix["x"]:ix["x"] + 20]
            kern[kern == 3] = 7
        self.abgabe("r0c1", {**KLASSEN, 7: "3"}, neue_id)
        ergebnis = zusammentragen(self.auftrag(), self.kat)
        self.assertFalse(ergebnis.ok)
        self.assertTrue(ergebnis.pruefung.ok, ergebnis.pruefung.maengel)  # Karte selbst lückenlos
        [verstoss] = ergebnis.naht.verstoesse
        self.assertEqual((verstoss["art"], verstoss["naht"], verstoss["ids"], verstoss["laenge"]),
                         ("ohne_kante", "r0c0|r0c1", [3, 7], 10))
        self.assertEqual((verstoss["von"], verstoss["bis"]), ([20, 10], [20, 19]))
        self.assertIn("ohne Bildkante", ergebnis.als_text())
        # bestätigt der Auftrag die Grenze als echt, ist es kein Verstoß mehr
        bestaetigt = [{"naht": "r0c0|r0c1", "ids": [7, 3], "grund": "Feldgrenze, kaum Farbsprung"}]
        ergebnis = zusammentragen(self.auftrag(naht_bestaetigt=bestaetigt), self.kat)
        self.assertTrue(ergebnis.ok, ergebnis.als_text())
        self.assertEqual(len(ergebnis.naht.bestaetigt), 1)
        # eine hohe Schwelle aus dem Auftrag macht auch die echte Kante bei Zeile 0–9 zum Verstoß
        ergebnis = zusammentragen(self.auftrag(naht={"kante_schwelle": 1000}), self.kat)
        self.assertEqual(sorted(tuple(v["ids"]) for v in ergebnis.naht.verstoesse), [(1, 2), (3, 7)])

    def test_naht_verletzung_klasse_und_nutzerklasse(self):
        self.abgabe("r0c1", {**KLASSEN, 3: "3.1"})
        ergebnis = zusammentragen(self.auftrag(), self.kat)
        self.assertFalse(ergebnis.ok)
        [konflikt] = ergebnis.klassen_konflikte
        self.assertEqual((konflikt["id"], konflikt["klassen"], konflikt["naehte"]),
                         (3, {"r0c0": "3", "r0c1": "3.1"}, ["r0c0|r0c1"]))
        nutzer = [{"id": 3, "klasse": "3.1.1", "kommentar": "Baumgruppe"}]
        ergebnis = zusammentragen(self.auftrag(nutzerklassen=nutzer), self.kat)
        self.assertTrue(ergebnis.ok, ergebnis.als_text())
        segment = next(s for s in ergebnis.segmente["segmente"] if s["id"] == 3)
        self.assertEqual((segment["klasse"], segment["grob"], segment["klasse_quelle"]), ("3.1.1", "3", "nutzer"))
        with self.assertRaises(ZusammenFehler):
            zusammentragen(self.auftrag(nutzerklassen=[{"id": 3, "klasse": "9.9"}]), self.kat)

    def test_kontext_zaehlt_nicht_und_spaetere_runde_ersetzt(self):
        def kontext_kaputt(karte):
            karte[:, 20:] = 99  # Kontextrand rechts von r0c0
        self.abgabe("r0c0", {**KLASSEN, 99: "1"}, kontext_kaputt)
        self.assertTrue(zusammentragen(self.auftrag(), self.kat).ok)

        def korrigiert(karte):
            ix = self.teilkachel("r0c1")["kern_im_bild"]
            karte[ix["y"]:ix["y"] + 10, ix["x"] + 15:ix["x"] + 20] = 5  # neues Segment im Kern
        self.abgabe("r0c1", {**KLASSEN, 5: "1.1"}, korrigiert, runde=1)
        ergebnis = zusammentragen(self.auftrag(), self.kat)
        self.assertTrue(ergebnis.ok, ergebnis.als_text())
        self.assertEqual(ergebnis.einheiten["r0c1"]["runde"], 1)
        self.assertEqual(int(ergebnis.karte[0, 39]), 5)

    def test_neue_ids_mehrerer_teilkacheln_werden_umnummeriert(self):
        ausgang = {"segmente": [{"id": s, "klasse": k} for s, k in KLASSEN.items()]}
        dateien.schreibe_json(self.ordner / "aus" / "vorstufe.json", ausgang)

        def stueck(tid):
            def aendern(karte):
                ix = self.teilkachel(tid)["kern_im_bild"]
                karte[ix["y"]:ix["y"] + 4, ix["x"] + 5:ix["x"] + 9] = 5
            return aendern
        self.abgabe("r0c0", {**KLASSEN, 5: "3.1.1"}, stueck("r0c0"))
        self.abgabe("r0c1", {**KLASSEN, 5: "1.1"}, stueck("r0c1"))
        ergebnis = zusammentragen(self.auftrag(ausgang="vorstufe.json"), self.kat)
        self.assertTrue(ergebnis.ok, ergebnis.als_text())
        self.assertEqual(ergebnis.umbenannt, [{"teilkachel": "r0c1", "alt": 5, "neu": 6}])
        self.assertEqual((int(ergebnis.karte[0, 5]), int(ergebnis.karte[0, 25])), (5, 6))
        klassen = {s["id"]: s["klasse"] for s in ergebnis.segmente["segmente"]}
        self.assertEqual((klassen[5], klassen[6]), ("3.1.1", "1.1"))

    def test_fragen_aus_json_mit_lage(self):
        fragen = [{"id": "F1", "text": "Weg oder Rain?", "segmente": [4]},
                  {"id": "F2", "text": "gibt es nicht", "segmente": [42]}]
        ergebnis = zusammentragen(self.auftrag(fragen=fragen), self.kat)
        f1, f2 = ergebnis.segmente["fragen"]
        self.assertEqual(f1["bbox"], [30, 10, 40, 20])
        self.assertNotIn("bbox", f2)
        self.assertEqual(ergebnis.maengel, ["Frage F2: Segment 42 gibt es im Ergebnis nicht"])
        self.assertFalse(ergebnis.ok)

    def test_fehlende_teilkachel_ist_luecke(self):
        self.einheiten = [e for e in self.einheiten if e["teilkachel"] != "r0c1"]
        ergebnis = zusammentragen(self.auftrag(), self.kat)
        self.assertFalse(ergebnis.ok)
        self.assertEqual(ergebnis.pruefung.ohne_segment, 400)

    def test_befehle_zusammentragen_und_naht(self):
        auftrag = self.auftrag()
        kat = str(self.ordner / "kategorien_beispiel.json")
        with redirect_stdout(io.StringIO()) as aus:
            self.assertEqual(main(["zusammentragen", "--datei", str(auftrag), "--kategorien", kat]), 0)
        self.assertIn("Zusammentragen ok", aus.getvalue())
        labels = self.ordner / "aus" / "zusammen" / "labels.tif"
        manifest = self.ordner / "aus" / "manifest.json"
        with redirect_stdout(io.StringIO()):
            self.assertEqual(main(["naht", "--manifest", str(manifest), "--labels", str(labels)]), 0)
        karte = dateien.lese_labels(labels)
        karte[10:, 20:30] = 7  # Naht-Verletzung im Ergebnis
        dateien.schreibe_labels(labels, karte)
        with redirect_stdout(io.StringIO()) as aus:
            self.assertEqual(main(["naht", "--manifest", str(manifest), "--labels", str(labels), "--json"]), 1)
        self.assertEqual(json.loads(aus.getvalue())["verstoesse"][0]["ids"], [3, 7])

    def test_nutzerklasse_behaelt_im_siedlung(self):
        for einheit in self.einheiten:
            pfad = self.ordner / "aus" / einheit["segmente"]
            daten = dateien.lese_json(pfad)
            for s in daten["segmente"]:
                if s["id"] == 3:
                    s["im_siedlung"] = "ja"
            dateien.schreibe_json(pfad, daten)
        ergebnis = zusammentragen(self.auftrag(nutzerklassen=[{"id": 3, "klasse": "3.1"}]), self.kat)
        segment = next(s for s in ergebnis.segmente["segmente"] if s["id"] == 3)
        self.assertEqual((segment["klasse"], segment["im_siedlung"]), ("3.1", "ja"))

if __name__ == "__main__":
    unittest.main()
