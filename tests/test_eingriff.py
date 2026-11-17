import io
import json
import random
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

import numpy as np

from landseg import dateien
from landseg.__main__ import main
from landseg.eingriff import Bearbeitung, EingriffFehler
from landseg.pruefen import pruefen
from tests.hilfe import beispiel_karte, beispiel_kategorien, block_karte


class EingriffTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ordner = Path(self.tmp.name)
        self.kat = beispiel_kategorien(self.ordner)
        karte, segmente = beispiel_karte()
        self.arbeit = Bearbeitung(karte, segmente, self.kat, "test")

    def tearDown(self):
        self.tmp.cleanup()

    def assertLueckenlos(self):
        befund = pruefen(self.arbeit.karte, self.arbeit.segmente, self.kat, form=(40, 40))
        self.assertTrue(befund.ok, befund.maengel)
        self.assertEqual(befund.ohne_segment, 0)

    def assertAbgelehnt(self, aufruf, *args, **kwargs):
        vorher_karte = self.arbeit.karte.copy()
        vorher_seg = json.dumps(self.arbeit.segmente, sort_keys=True)
        with self.assertRaises(EingriffFehler):
            aufruf(*args, **kwargs)
        np.testing.assert_array_equal(self.arbeit.karte, vorher_karte)
        self.assertEqual(json.dumps(self.arbeit.segmente, sort_keys=True), vorher_seg)

    def ids(self):
        return sorted(np.unique(self.arbeit.karte).tolist())

    # verschmelzen
    def test_verschmelzen(self):
        ergebnis = self.arbeit.verschmelzen([2, 3])
        self.assertEqual(ergebnis["entfernt"], [3])
        self.assertEqual(self.ids(), [1, 2, 4])
        self.assertEqual(int((self.arbeit.karte == 2).sum()), 800)
        self.assertLueckenlos()

    def test_verschmelzen_ziel_behaelt_klasse(self):
        self.arbeit.verschmelzen([1, 4], ziel=4)
        eintrag = {s["id"]: s for s in self.arbeit.segmente["segmente"]}[4]
        self.assertEqual(eintrag["klasse"], "3.1.1")
        self.assertLueckenlos()

    def test_verschmelzen_nicht_benachbart_abgelehnt(self):
        self.assertAbgelehnt(self.arbeit.verschmelzen, [4, 3])
        self.assertAbgelehnt(self.arbeit.verschmelzen, [1, 99])

    # teilen
    def test_teilen_senkrecht(self):
        ergebnis = self.arbeit.teilen(2, [[30, 0], [30, 19]])
        self.assertEqual(len(ergebnis["neu"]), 1)
        self.assertEqual(len(self.ids()), 5)
        self.assertLueckenlos()

    def test_teilen_schraeg_bleibt_zusammenhaengend(self):
        self.arbeit.teilen(1, [[0, 39], [19, 8]])
        self.assertLueckenlos()

    def test_teilen_in_drei(self):
        ergebnis = self.arbeit.teilen(3, [[20, 25], [39, 25], [39, 30], [20, 30]])
        self.assertEqual(len(ergebnis["neu"]), 2)
        self.assertLueckenlos()

    def test_teilen_linie_trennt_nicht_abgelehnt(self):
        self.assertAbgelehnt(self.arbeit.teilen, 2, [[25, 0], [25, 10]])

    # Grenze verschieben
    def test_grenze_verschieben(self):
        ergebnis = self.arbeit.grenze_verschieben(3, 2, [[20, 20], [39, 20], [39, 24], [20, 24]])
        self.assertEqual(ergebnis["bildpunkte"], 100)
        self.assertEqual(int((self.arbeit.karte == 2).sum()), 500)
        self.assertLueckenlos()

    def test_grenze_verschieben_ganz(self):
        ergebnis = self.arbeit.grenze_verschieben(4, 1, [[0, 0], [10, 0], [10, 10], [0, 10]])
        self.assertEqual(ergebnis["entfernt"], [4])
        self.assertLueckenlos()

    def test_grenze_verschieben_abgelehnt(self):
        # nicht angrenzend
        self.assertAbgelehnt(self.arbeit.grenze_verschieben, 3, 4, [[30, 30], [35, 30], [35, 35]])
        # 3 zerfiele (Streifen quer durch)
        self.assertAbgelehnt(self.arbeit.grenze_verschieben, 3, 2,
                             [[29, 20], [31, 20], [31, 39], [29, 39]])

    # Klasse setzen
    def test_klasse_setzen(self):
        self.arbeit.klasse_setzen(3, "1.1")
        eintrag = {s["id"]: s for s in self.arbeit.segmente["segmente"]}[3]
        self.assertEqual((eintrag["klasse"], eintrag["grob"]), ("1.1", "1"))
        self.assertLueckenlos()

    def test_klasse_ungueltig_abgelehnt(self):
        self.assertAbgelehnt(self.arbeit.klasse_setzen, 3, "7.7")

    # Polygon zuweisen
    def test_polygon_neues_segment(self):
        ergebnis = self.arbeit.polygon_zuweisen([[24, 24], [30, 24], [30, 30], [24, 30]], klasse="1.1")
        self.assertEqual(ergebnis["bildpunkte"], 49)
        self.assertLueckenlos()

    def test_polygon_teilt_nachbarn_auf(self):
        # Querstreifen durch Segment 1: Rest von 1 zerfällt in oben und unten
        ergebnis = self.arbeit.polygon_zuweisen([[0, 15], [19, 15], [19, 17], [0, 17]], sid=2)
        self.assertEqual(len(ergebnis["aufgeteilt_neu"]), 1)
        self.assertLueckenlos()

    def test_polygon_frisst_segment(self):
        ergebnis = self.arbeit.polygon_zuweisen([[0, 0], [8, 0], [8, 8], [0, 8]], sid=1)
        self.assertEqual(ergebnis["entfernt"], [4])
        self.assertLueckenlos()

    def test_polygon_abgelehnt(self):
        self.assertAbgelehnt(self.arbeit.polygon_zuweisen, [[30, 30], [35, 30], [35, 35]], sid=4)
        self.assertAbgelehnt(self.arbeit.polygon_zuweisen, [[1, 1], [2, 1], [2, 2]])
        self.assertAbgelehnt(self.arbeit.polygon_zuweisen, [[1, 1], [2, 1], [2, 2]], klasse="x")

    # allgemein
    def test_verlauf_mit_bearbeiter(self):
        self.arbeit.verschmelzen([2, 3])
        self.arbeit.klasse_setzen(2, "3")
        verlauf = self.arbeit.segmente["verlauf"]
        self.assertEqual([v["op"] for v in verlauf], ["verschmelzen", "klasse_setzen"])
        self.assertEqual({v["bearbeiter"] for v in verlauf}, {"test"})

    def test_karte_mit_luecke_wird_nicht_bearbeitet(self):
        karte, segmente = beispiel_karte()
        karte[0, 0] = 0
        with self.assertRaises(EingriffFehler):
            Bearbeitung(karte, segmente, self.kat, "test")

    def test_zufallsfolge_bleibt_lueckenlos(self):
        rnd = random.Random(17)
        karte, segmente = block_karte()
        arbeit = Bearbeitung(karte, segmente, self.kat, "zufall")
        erfolgreich = 0
        for _ in range(150):
            ids = np.unique(arbeit.karte).tolist()
            punkt = lambda: [rnd.randrange(64), rnd.randrange(64)]
            op = rnd.choice(["verschmelzen", "teilen", "verschieben", "klasse", "polygon"])
            try:
                if op == "verschmelzen":
                    a = rnd.choice(ids)
                    nachbar = int(arbeit.karte[min(63, np.argwhere(arbeit.karte == a)[-1][0] + 1),
                                               np.argwhere(arbeit.karte == a)[-1][1]])
                    arbeit.verschmelzen([a, nachbar])
                elif op == "teilen":
                    arbeit.teilen(rnd.choice(ids), [punkt() for _ in range(rnd.randint(2, 4))])
                elif op == "verschieben":
                    arbeit.grenze_verschieben(rnd.choice(ids), rnd.choice(ids),
                                              [punkt() for _ in range(rnd.randint(3, 5))])
                elif op == "klasse":
                    arbeit.klasse_setzen(rnd.choice(ids), rnd.choice(["0", "1", "3.1.1"]))
                else:
                    arbeit.polygon_zuweisen([punkt() for _ in range(rnd.randint(3, 5))],
                                            klasse=rnd.choice(["1.1", "3"]))
                erfolgreich += 1
            except EingriffFehler:
                pass
            befund = pruefen(arbeit.karte, arbeit.segmente, self.kat, form=(64, 64))
            self.assertTrue(befund.ok, (op, befund.maengel))
        self.assertGreater(erfolgreich, 50)

    def test_befehl_stapel_alles_oder_nichts(self):
        karte, segmente = beispiel_karte()
        labels, seg = self.ordner / "labels.tif", self.ordner / "segmente.json"
        dateien.schreibe_labels(labels, karte)
        dateien.schreibe_json(seg, segmente)
        stapel = self.ordner / "stapel.json"
        basis = ["eingriff", "--labels", str(labels), "--segmente", str(seg),
                 "--kategorien", str(self.kat.pfad), "--bearbeiter", "cli"]
        stapel.write_text(json.dumps({"schritte": [
            {"op": "verschmelzen", "ids": [2, 3]},
            {"op": "klasse_setzen", "id": 2, "klasse": "unbekannt"},
        ]}), encoding="utf-8")
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            self.assertEqual(main(basis + ["stapel", "--datei", str(stapel)]), 1)
        np.testing.assert_array_equal(dateien.lese_labels(labels), karte)
        stapel.write_text(json.dumps({"schritte": [
            {"op": "verschmelzen", "ids": [2, 3]},
            {"op": "teilen", "id": 1, "linie": [[0, 30], [19, 30]]},
        ]}), encoding="utf-8")
        with redirect_stdout(io.StringIO()) as aus:
            self.assertEqual(main(basis + ["stapel", "--datei", str(stapel)]), 0)
        self.assertIn("ok", aus.getvalue())
        self.assertEqual(len(np.unique(dateien.lese_labels(labels))), 4)
        self.assertEqual(len(dateien.lese_segmente(seg)["verlauf"]), 2)
        with redirect_stdout(io.StringIO()):
            self.assertEqual(main(basis + ["klasse", "--id", "4", "--klasse", "1"]), 0)



class MerkmalTest(unittest.TestCase):
    def test_klasse_setzen_behaelt_im_siedlung(self):
        with tempfile.TemporaryDirectory() as tmp:
            kat = beispiel_kategorien(Path(tmp))
            karte, segmente = beispiel_karte()
            segmente["segmente"][2]["im_siedlung"] = "ja"
            arbeit = Bearbeitung(karte, segmente, kat, "test")
            arbeit.klasse_setzen(3, "3.1")
            eintrag = {s["id"]: s for s in arbeit.segmente["segmente"]}[3]
            self.assertEqual((eintrag["klasse"], eintrag["im_siedlung"]), ("3.1", "ja"))

if __name__ == "__main__":
    unittest.main()
