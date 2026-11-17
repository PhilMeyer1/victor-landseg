import io
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

import numpy as np
from PIL import Image

from landseg import dateien, einstellungen
from landseg.__main__ import main
from landseg.eingriff import Bearbeitung
from landseg.kante import KanteFehler, einrasten
from landseg.pruefen import pruefen
from tests.hilfe import beispiel_kategorien


def zwei_flaechen(kante_x: int = 23, nur_oben: bool = False) -> tuple[np.ndarray, np.ndarray]:
    """60 × 40: links dunkel, rechts hell, Bildkante bei ``kante_x``; Label-Grenze bei x = 20.

    Mit ``nur_oben`` ist die untere Hälfte einfarbig (dort gibt es keine Bildkante).
    """
    bild = np.full((60, 40, 3), 60, np.uint8)
    bild[:, kante_x:] = 200
    if nur_oben:
        bild[30:, :] = 130
    karte = np.ones((60, 40), np.uint32)
    karte[:, 20:] = 2
    return bild, karte


class KanteTest(unittest.TestCase):
    def setUp(self):
        self.vorgaben = einstellungen.laden("kante")

    def test_rastet_auf_bildkante_ein(self):
        bild, karte = zwei_flaechen()
        erg = einrasten(bild, karte, 1, 2, self.vorgaben)
        self.assertTrue((erg.karte[:, :23] == 1).all())
        self.assertTrue((erg.karte[:, 23:] == 2).all())
        self.assertEqual(erg.nach_a, 60 * 3)
        self.assertEqual(erg.geschaetzt, [])
        self.assertEqual(erg.grenze, 60)
        self.assertTrue((karte[:, 20:] == 2).all(), "Eingabe bleibt unverändert")

    def test_ohne_bildkante_bleibt_grenze_und_wird_gemeldet(self):
        bild, karte = zwei_flaechen(nur_oben=True)
        erg = einrasten(bild, karte, 1, 2, self.vorgaben)
        # oben eingerastet, unten (ohne Kante) unverändert bei x = 20
        self.assertTrue((erg.karte[:20, :23] == 1).all() and (erg.karte[:20, 23:] == 2).all())
        self.assertTrue((erg.karte[40:, :20] == 1).all() and (erg.karte[40:, 20:] == 2).all())
        self.assertEqual(len(erg.geschaetzt), 1)
        strecke = erg.geschaetzt[0]
        self.assertGreaterEqual(strecke["laenge"], 20)
        self.assertTrue(all(y >= 28 for _, y in strecke["punkte"]))
        self.assertLess(strecke["staerke"], self.vorgaben["kante_min"])
        self.assertIn("geschätzt 1:", erg.als_text())

    def test_bleibt_lueckenlos_und_andere_unberuehrt(self):
        bild, karte = zwei_flaechen()
        karte[:10, :] = 3  # drittes Segment oben, berührt beide
        erg = einrasten(bild, karte, 1, 2, self.vorgaben, band=5)
        self.assertFalse((erg.karte == 0).any())
        self.assertTrue((erg.karte[:10] == 3).all())
        befund = pruefen(erg.karte, None, None, form=karte.shape)
        self.assertTrue(befund.ok, befund.als_text())

    def test_bereich_begrenzt_das_einrasten(self):
        bild, karte = zwei_flaechen()
        erg = einrasten(bild, karte, 1, 2, self.vorgaben, bereich=[[0, 0], [39, 0], [39, 29], [0, 29]])
        self.assertTrue((erg.karte[:25, 20:23] == 1).all())
        self.assertTrue((erg.karte[35:, 20:] == 2).all())

    def test_keine_nachbarn_abgelehnt(self):
        bild, karte = zwei_flaechen()
        karte[:, 30:] = 3
        with self.assertRaises(KanteFehler):
            einrasten(bild, karte, 1, 3, self.vorgaben)
        with self.assertRaises(KanteFehler):
            einrasten(bild, karte, 1, 9, self.vorgaben)

    def test_bearbeitung_schreibt_verlauf(self):
        with tempfile.TemporaryDirectory() as tmp:
            kat = beispiel_kategorien(Path(tmp))
            bild, karte = zwei_flaechen(nur_oben=True)
            segmente = {"segmente": [{"id": 1, "klasse": "1.1", "grob": "1"},
                                     {"id": 2, "klasse": "3", "grob": "3"}], "verlauf": []}
            arbeit = Bearbeitung(karte, segmente, kat, "test")
            erg = arbeit.kante_einrasten(bild, 1, 2, self.vorgaben)
            eintrag = arbeit.segmente["verlauf"][-1]
            self.assertEqual(eintrag["op"], "kante")
            self.assertEqual(len(eintrag["ergebnis"]["geschaetzt"]), 1)
            self.assertNotIn("punkte", eintrag["ergebnis"]["geschaetzt"][0])
            self.assertTrue((arbeit.karte == erg.karte).all())
            self.assertTrue(pruefen(arbeit.karte, arbeit.segmente, kat).ok)

    def test_befehl_schreibt_zurueck_und_bericht(self):
        with tempfile.TemporaryDirectory() as tmp:
            ordner = Path(tmp)
            kat = beispiel_kategorien(ordner)
            bild, karte = zwei_flaechen(nur_oben=True)
            Image.fromarray(bild).save(ordner / "bild.png")
            dateien.schreibe_labels(ordner / "labels.tif", karte)
            dateien.schreibe_json(ordner / "segmente.json", {"segmente": [
                {"id": 1, "klasse": "1.1", "grob": "1"}, {"id": 2, "klasse": "3", "grob": "3"}]})
            gemeinsam = ["kante", "--labels", str(ordner / "labels.tif"),
                         "--bild", str(ordner / "bild.png"), "--a", "1", "--b", "2"]
            aus = io.StringIO()
            with redirect_stdout(aus):
                self.assertEqual(main(gemeinsam + ["--trocken"]), 0)
            self.assertIn("geschätzt 1:", aus.getvalue())
            self.assertTrue((dateien.lese_labels(ordner / "labels.tif") == karte).all())
            with redirect_stdout(io.StringIO()):
                code = main(gemeinsam + ["--segmente", str(ordner / "segmente.json"),
                                         "--kategorien", str(kat.pfad), "--bearbeiter", "test",
                                         "--bericht", str(ordner / "kante.json")])
            self.assertEqual(code, 0)
            neu = dateien.lese_labels(ordner / "labels.tif")
            self.assertTrue((neu[:20, 20:23] == 1).all())
            bericht = dateien.lese_json(ordner / "kante.json")
            self.assertEqual(len(bericht["geschaetzt"]), 1)
            self.assertIn("punkte", bericht["geschaetzt"][0])
            with redirect_stderr(io.StringIO()):
                self.assertEqual(main(gemeinsam[:-4] + ["--a", "1", "--b", "7", "--trocken"]), 1)


if __name__ == "__main__":
    unittest.main()
