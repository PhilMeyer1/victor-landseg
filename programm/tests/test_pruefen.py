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



class PruefenKategorienDesReposTest(unittest.TestCase):
    def test_alte_codes_und_falsches_merkmal_gemeldet(self):
        kat = kategorien.laden()
        karte, segmente = beispiel_karte()
        self.assertTrue(pruefen(karte, segmente, kat).ok)
        for alt in ("1.4", "1.4.1", "1.4.2", "1.4.3", "1.2.3"):
            daten = copy.deepcopy(segmente)
            daten["segmente"][1].update(klasse=alt, grob="1")
            befund = pruefen(karte, daten, kat)
            self.assertIn(f"Klasse: Segment 2 hat ungültige Klasse {alt!r}", befund.maengel)
        daten = copy.deepcopy(segmente)
        daten["segmente"][1]["im_siedlung"] = "ja"
        self.assertTrue(pruefen(karte, daten, kat).ok)
        daten["segmente"][1]["im_siedlung"] = "vielleicht"
        befund = pruefen(karte, daten, kat)
        self.assertFalse(befund.ok)
        self.assertTrue(any("im_siedlung" in m for m in befund.maengel), befund.maengel)


class PruefenGartenFreiTest(unittest.TestCase):
    """Garten in freien Fassungen (Skill landseg-agent, L14): ``pruefen --frei``."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ordner = Path(self.tmp.name)
        self.karte, _ = beispiel_karte()

    def tearDown(self):
        self.tmp.cleanup()

    def _freie_liste(self, klassen: list[dict]) -> kategorien.Kategorien:
        pfad = self.ordner / "kategorien-frei.json"
        dateien.schreibe_json(pfad, {"classes": klassen})
        return kategorien.laden(pfad)

    def _frei_segmente(self, code: str) -> dict:
        return {"segmente": [{"id": i, "klasse": code} for i in (1, 2, 3, 4)], "verlauf": []}

    def test_freie_fassung_mit_garten_unter_dauergruenland_ok(self):
        for name_dg, name_garten in (("Dauergrünland", "Garten"), ("dauergrünland (krautig)", "Garten (am Haus)")):
            kat = self._freie_liste([
                {"code": "1", "name": "Bebauung", "parent": None, "level": 1},
                {"code": "2", "name": name_dg, "parent": None, "level": 1},
                {"code": "2.1", "name": "Grünfläche", "parent": "2", "level": 2},
                {"code": "2.1.1", "name": name_garten, "parent": "2.1", "level": 3}])
            befund = pruefen(self.karte, self._frei_segmente("1"), kat, frei=True)
            self.assertTrue(befund.ok, befund.maengel)
        # die feste Liste erfüllt die Pflicht auch (3.6 unter 3)
        self.assertEqual(kategorien.laden().garten_maengel(), [])

    def test_freie_fassung_ohne_garten_fehler(self):
        kat = self._freie_liste([{"code": "1", "name": "Bebauung", "parent": None, "level": 1},
                                 {"code": "2", "name": "Dauergrünland", "parent": None, "level": 1},
                                 {"code": "2.1", "name": "Gartenland", "parent": "2", "level": 2}])
        befund = pruefen(self.karte, self._frei_segmente("1"), kat, frei=True)
        self.assertFalse(befund.ok)
        self.assertTrue(any(m.startswith("Garten: Liste ohne Klasse „Garten“") for m in befund.maengel),
                        befund.maengel)
        # ohne frei (feste Liste, Teil-Listen anderer Werkzeuge) keine Garten-Pflicht
        self.assertTrue(pruefen(self.karte, self._frei_segmente("1"), kat).ok)

    def test_freie_fassung_garten_nicht_unter_dauergruenland_fehler(self):
        kat = self._freie_liste([{"code": "1", "name": "Hof und Garten", "parent": None, "level": 1},
                                 {"code": "1.2", "name": "Garten", "parent": "1", "level": 2},
                                 {"code": "2", "name": "Dauergrünland", "parent": None, "level": 1},
                                 {"code": "3", "name": "Garten", "parent": None, "level": 1}])
        befund = pruefen(self.karte, self._frei_segmente("2"), kat, frei=True)
        self.assertIn("Garten: Klasse 1.2 „Garten“ steht unter 1 „Hof und Garten“, erwartet unter der "
                      "Ebene-1-Klasse „Dauergrünland“", befund.maengel)
        self.assertIn("Garten: Klasse 3 „Garten“ ist selbst Ebene 1, erwartet unter der Ebene-1-Klasse "
                      "„Dauergrünland“", befund.maengel)

    def test_befehl_frei(self):
        labels = self.ordner / "labels.tif"
        seg = self.ordner / "segmente.json"
        dateien.schreibe_labels(labels, self.karte)
        dateien.schreibe_json(seg, self._frei_segmente("1"))
        ohne = self._freie_liste([{"code": "1", "name": "Bebauung", "parent": None, "level": 1}])
        args = ["pruefen", "--labels", str(labels), "--segmente", str(seg), "--kategorien", str(ohne.pfad)]
        with redirect_stdout(io.StringIO()):
            self.assertEqual(main(args), 0)
        with redirect_stdout(io.StringIO()) as aus:
            self.assertEqual(main(args + ["--frei"]), 1)
        self.assertIn("Garten: Liste ohne Klasse", aus.getvalue())
        with redirect_stdout(io.StringIO()) as aus:   # auch ohne segmente.json: nur Karte und Liste
            self.assertEqual(main(["pruefen", "--labels", str(labels), "--kategorien", str(ohne.pfad), "--frei"]), 1)
        self.assertIn("Garten: Liste ohne Klasse", aus.getvalue())


if __name__ == "__main__":
    unittest.main()
