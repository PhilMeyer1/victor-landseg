import copy
import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import numpy as np

from landseg import dateien, kategorien
from landseg.__main__ import main
from landseg.pruefen import pruefen
from tests.hilfe import beispiel_karte, beispiel_kategorien


class PruefenTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ordner = Path(self.tmp.name)
        self.kat = beispiel_kategorien(self.ordner)
        self.karte, self.segmente = beispiel_karte()

    def tearDown(self):
        self.tmp.cleanup()

    def test_saubere_karte_ok_und_meldet_h_mal_w(self):
        befund = pruefen(self.karte, self.segmente, self.kat, form=(40, 40))
        self.assertTrue(befund.ok, befund.maengel)
        self.assertEqual((befund.hoehe, befund.breite, befund.bildpunkte), (40, 40, 1600))
        self.assertEqual(befund.ohne_segment, 0)
        self.assertEqual(befund.segmentzahl, 4)
        self.assertIn("H × W: 40 × 40 = 1600 Bildpunkte, ohne Segment (ID 0): 0", befund.als_text())

    def test_gegenprobe_luecke_schlaegt_fehl(self):
        self.karte[10, 30] = 0
        befund = pruefen(self.karte, self.segmente, self.kat)
        self.assertFalse(befund.ok)
        self.assertEqual(befund.ohne_segment, 1)
        self.assertTrue(any(m.startswith("Lücke: 1 Bildpunkte") for m in befund.maengel))

    def test_gegenprobe_luecke_die_segment_trennt(self):
        self.karte[:20, 25] = 0  # Spalte quer durch Segment 2
        befund = pruefen(self.karte, self.segmente, self.kat)
        self.assertFalse(befund.ok)
        self.assertIn(2, befund.nicht_zusammenhaengend)

    def test_gegenprobe_nicht_zusammenhaengend(self):
        self.karte[35, 5] = 2  # Insel von 2 mitten in 1
        befund = pruefen(self.karte, self.segmente, self.kat)
        self.assertEqual(befund.nicht_zusammenhaengend, [2])
        self.assertFalse(befund.ok)

    def test_nur_diagonal_verbunden_gilt_als_getrennt(self):
        karte = np.array([[1, 2], [2, 1]], np.uint32)
        befund = pruefen(karte)
        self.assertEqual(befund.nicht_zusammenhaengend, [1, 2])

    def test_gegenprobe_klassen(self):
        faelle = {
            "ungültige Klasse": lambda s: s["segmente"][0].update(klasse="9.9"),
            "grob passt nicht": lambda s: s["segmente"][1].update(grob="1"),
            "Eintrag fehlt": lambda s: s["segmente"].pop(3),
            "Eintrag ohne Bildpunkte": lambda s: s["segmente"].append({"id": 77, "klasse": "3"}),
            "ID doppelt": lambda s: s["segmente"].append({"id": 1, "klasse": "3"}),
        }
        for name, aendern in faelle.items():
            with self.subTest(name):
                segmente = copy.deepcopy(self.segmente)
                aendern(segmente)
                self.assertFalse(pruefen(self.karte, segmente, self.kat).ok)

    def test_gegenprobe_form(self):
        self.assertFalse(pruefen(self.karte, form=(40, 41)).ok)

    def test_mindestflaeche(self):
        self.assertTrue(pruefen(self.karte, mindestflaeche=16).ok)
        self.assertFalse(pruefen(self.karte, mindestflaeche=17).ok)

    def test_kategorien_des_repos_laden(self):
        kat = kategorien.laden()
        self.assertEqual(sum(1 for k in kat.klassen.values() if k.get("parent") is None), 7)
        for code in kat.klassen:
            self.assertIsNone(kat.klassen[kat.grob(code)].get("parent"))

    def test_befehl_exit_codes(self):
        labels = self.ordner / "labels.tif"
        seg = self.ordner / "segmente.json"
        dateien.schreibe_labels(labels, self.karte)
        dateien.schreibe_json(seg, self.segmente)
        args = ["pruefen", "--labels", str(labels), "--segmente", str(seg),
                "--kategorien", str(self.kat.pfad), "--form", "40x40"]
        with redirect_stdout(io.StringIO()) as aus:
            self.assertEqual(main(args), 0)
        self.assertIn("ok", aus.getvalue())
        self.karte[0, 0] = 0
        dateien.schreibe_labels(labels, self.karte)
        with redirect_stdout(io.StringIO()) as aus:
            self.assertEqual(main(args), 1)
        self.assertIn("Lücke", aus.getvalue())

    def test_labels_rundreise_uint32(self):
        karte = np.array([[1, 70000], [4_000_000_000, 2]], np.uint32)
        pfad = self.ordner / "gross.tif"
        dateien.schreibe_labels(pfad, karte)
        gelesen = dateien.lese_labels(pfad)
        self.assertEqual(gelesen.dtype, np.uint32)
        np.testing.assert_array_equal(gelesen, karte)


if __name__ == "__main__":
    unittest.main()
