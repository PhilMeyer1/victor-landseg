import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image

from landseg.__main__ import main
from landseg.kacheln import KachelFehler, kacheln

PRJ = ('PROJCS["MGI / Austria GK Central",GEOGCS["MGI",DATUM["D_MGI"]],'
       'UNIT["metre",1],AUTHORITY["EPSG","31255"]]')


class KachelnTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ordner = Path(self.tmp.name)
        quelle = self.ordner / "quelle"
        quelle.mkdir()
        rnd = np.random.default_rng(3)
        self.bild = rnd.integers(0, 256, size=(300, 400, 3), dtype=np.uint8)
        self.tif = quelle / "blatt.tif"
        tifffile.imwrite(self.tif, self.bild, photometric="rgb")
        # Mitte des Bildpunkts oben links bei (1000.1, 5000.9), 0,2 m
        (quelle / "blatt.TFW").write_text("0.2\n0\n0\n-0.2\n1000.1\n5000.9\n", encoding="ascii")
        (quelle / "blatt.PRJ").write_text(PRJ, encoding="ascii")

    def tearDown(self):
        self.tmp.cleanup()

    def schneiden(self, kern, x=50, y=40, breite=200, hoehe=200, rand=16, name="t"):
        ziel = self.ordner / f"aus_{kern}_{x}_{y}"
        return ziel, kacheln(self.tif, x, y, breite, hoehe, ziel, kern=kern, rand=rand, name=name)

    def pruefe_kerne(self, ziel, manifest):
        a = manifest["ausschnitt"]
        abdeckung = np.zeros((a["hoehe"], a["breite"]), np.int32)
        for t in manifest["teilkacheln"]:
            k, kb = t["kern"], t["kern_im_bild"]
            abdeckung[k["y"]:k["y"] + k["hoehe"], k["x"]:k["x"] + k["breite"]] += 1
            self.assertFalse(Path(t["bild"]).is_absolute())
            teil = np.asarray(Image.open(ziel / t["bild"]))
            kx = manifest["ausschnitt"]["x"] + t["kontext"]["x"]
            ky = manifest["ausschnitt"]["y"] + t["kontext"]["y"]
            self.assertEqual(teil.shape[:2], (t["kontext"]["hoehe"], t["kontext"]["breite"]))
            np.testing.assert_array_equal(
                teil, self.bild[ky:ky + teil.shape[0], kx:kx + teil.shape[1]])
            self.assertEqual((kb["x"], kb["y"]), (k["x"] - t["kontext"]["x"],
                                                  k["y"] - t["kontext"]["y"]))
        self.assertTrue((abdeckung == 1).all(), "Kerne decken den Ausschnitt nicht genau einmal")

    def test_vier_teilkacheln(self):
        ziel, m = self.schneiden(100)
        self.assertEqual(len(m["teilkacheln"]), 4)
        self.assertEqual((m["raster"]["zeilen"], m["raster"]["spalten"]), (2, 2))
        for t in m["teilkacheln"]:
            self.assertEqual((t["kern"]["breite"], t["kern"]["hoehe"]), (100, 100))
            self.assertEqual((t["kontext"]["breite"], t["kontext"]["hoehe"]), (132, 132))
        self.pruefe_kerne(ziel, m)
        self.assertTrue((ziel / "manifest.json").exists())
        self.assertEqual(m["quelle"]["bild"], "../quelle/blatt.tif")

    def test_kerngroesse_ist_parameter(self):
        ziel, m = self.schneiden(50)
        self.assertEqual(len(m["teilkacheln"]), 16)
        self.pruefe_kerne(ziel, m)

    def test_kern_geht_nicht_auf(self):
        ziel, m = self.schneiden(70)
        self.assertEqual(len(m["teilkacheln"]), 9)
        self.assertEqual(m["teilkacheln"][-1]["kern"]["breite"], 60)
        self.pruefe_kerne(ziel, m)

    def test_kontext_endet_am_bildrand(self):
        ziel, m = self.schneiden(100, x=0, y=0)
        erste = m["teilkacheln"][0]
        self.assertEqual((erste["kontext"]["x"], erste["kontext"]["y"]), (0, 0))
        self.assertEqual((erste["kern_im_bild"]["x"], erste["kern_im_bild"]["y"]), (0, 0))
        self.assertEqual(erste["kontext"]["breite"], 116)
        self.pruefe_kerne(ziel, m)

    def test_georeferenz(self):
        _, m = self.schneiden(100)
        geo = m["georeferenz"]
        self.assertEqual(geo["epsg"], 31255)
        q = geo["transform_quelle"]
        self.assertAlmostEqual(q["c"], 1000.0)
        self.assertAlmostEqual(q["f"], 5001.0)
        a = m["ausschnitt"]["transform"]
        self.assertAlmostEqual(a["c"], 1000.0 + 50 * 0.2)
        self.assertAlmostEqual(a["f"], 5001.0 - 40 * 0.2)
        for t in m["teilkacheln"]:
            gx = 50 + t["kontext"]["x"]
            gy = 40 + t["kontext"]["y"]
            self.assertAlmostEqual(t["transform"]["c"], 1000.0 + gx * 0.2)
            self.assertAlmostEqual(t["transform"]["f"], 5001.0 - gy * 0.2)

    def test_ausschnitt_ausserhalb_und_vorhandenes_manifest(self):
        with self.assertRaises(KachelFehler):
            self.schneiden(100, x=300)
        self.schneiden(100)
        with self.assertRaises(KachelFehler):
            self.schneiden(100)

    def test_befehl(self):
        ziel = self.ordner / "cli"
        args = ["kacheln", "--bild", str(self.tif), "--x", "0", "--y", "0", "--breite", "200",
                "--hoehe", "100", "--kern", "100", "--ziel", str(ziel)]
        with redirect_stdout(io.StringIO()) as aus:
            self.assertEqual(main(args), 0)
        self.assertIn("2 Teilkacheln", aus.getvalue())
        with redirect_stdout(io.StringIO()):
            self.assertEqual(main(args + ["--kern", "50", "--ueberschreiben"]), 0)
        self.assertEqual(len(list((ziel / "teilkacheln").glob("*.png"))), 8)


if __name__ == "__main__":
    unittest.main()
