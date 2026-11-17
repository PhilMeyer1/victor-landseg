import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import numpy as np
from PIL import Image

from landseg import dateien, einstellungen
from landseg.__main__ import main
from landseg.ansicht import AnsichtFehler, ansicht
from tests.hilfe import beispiel_karte, beispiel_kategorien

TEIL_ARTEN = ["roh", "umriss", "maengel", "vorschlag", "kontrast", "gitter"]
SEGMENT_ARTEN = ["roh", "umriss", "maengel", "vorschlag", "nah", "kontrast", "gitter"]


def bild_40() -> np.ndarray:
    rng = np.random.default_rng(3)
    bild = rng.integers(80, 120, (40, 40, 3), dtype=np.uint8)
    bild[:, 20:] += 60
    return bild


class AnsichtTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ordner = Path(self.tmp.name)
        self.kat = beispiel_kategorien(self.ordner)
        self.karte, self.segmente = beispiel_karte()

    def tearDown(self):
        self.tmp.cleanup()

    def lesen(self, rel: str) -> np.ndarray:
        with Image.open(self.ordner / "aus" / rel) as bild:
            return np.asarray(bild.convert("RGB"))

    def test_alle_standardbilder_je_teilkachel_und_segment(self):
        index = ansicht(bild_40(), self.karte, self.ordner / "aus", segmente=self.segmente,
                        kategorien=self.kat, kern={"x": 4, "y": 4, "breite": 32, "hoehe": 32})
        self.assertEqual(list(index["teilkachel"]["bilder"]), TEIL_ARTEN)
        self.assertEqual([s["id"] for s in index["segmente"]], [1, 2, 3, 4])
        for s in index["segmente"]:
            self.assertEqual(list(s["bilder"]), SEGMENT_ARTEN)
        self.assertEqual(index["bilderzahl"], 6 + 4 * 7)
        for rel in index["teilkachel"]["bilder"].values():
            self.assertTrue((self.ordner / "aus" / rel).exists(), rel)
        self.assertEqual(self.lesen("teilkachel/roh.png").shape, (40, 40, 3))
        self.assertTrue((self.lesen("teilkachel/roh.png") == bild_40()).all())
        gitter = self.lesen("teilkachel/gitter.png")
        self.assertEqual(gitter.shape, (40 + 16, 40 + 40, 3))
        self.assertFalse((self.lesen("teilkachel/kontrast.png") == bild_40()).all())
        umriss = self.lesen("teilkachel/umriss.png")
        self.assertEqual(tuple(umriss[10, 19]), (255, 255, 0))  # Grenze 1|2 bei x = 19/20
        gespeichert = json.loads((self.ordner / "aus" / "ansicht.json").read_text("utf-8"))
        self.assertEqual(gespeichert["schema"], "landseg-ansicht/1")

    def test_nah_ist_vergroessert_und_koordinaten_stimmen(self):
        index = ansicht(bild_40(), self.karte, self.ordner / "aus", segmente=self.segmente,
                        kategorien=self.kat, ids=[4])
        s = index["segmente"][0]
        f = s["fenster"]
        self.assertGreater(f["faktor"], 1)
        nah = self.lesen(s["bilder"]["nah"])
        self.assertEqual(nah.shape[:2], (f["hoehe"] * f["faktor"], f["breite"] * f["faktor"]))
        roh = self.lesen(s["bilder"]["roh"])
        self.assertEqual(roh.shape[:2], (f["hoehe"], f["breite"]))
        # Bildpunkt (3, 3) der Teilkachel liegt in Segment 4, im nah-Bild unverändert
        x = (3 - f["x"]) * f["faktor"] + f["faktor"] // 2
        y = (3 - f["y"]) * f["faktor"] + f["faktor"] // 2
        self.assertTrue((nah[y, x] == bild_40()[3, 3]).all())

    def test_maengel_zeigt_luecke_unsicher_und_geschaetzt(self):
        karte = self.karte.copy()
        karte[30:33, 5:8] = 0
        self.segmente["segmente"][1]["sicher"] = "nein"
        index = ansicht(bild_40(), karte, self.ordner / "aus", segmente=self.segmente,
                        kategorien=self.kat, nur_teilkachel=True,
                        kandidaten={"kandidaten": [{"id": 3, "grund": "Klasse unsicher"}]},
                        kante={"geschaetzt": [{"punkte": [[25, 35], [26, 35], [27, 35]]}]})
        m = index["maengel"]
        self.assertEqual(m["luecke_bildpunkte"], 9)
        self.assertEqual(m["unsicher"], [2])
        self.assertEqual(m["geschaetzt_bildpunkte"], 3)
        bild = self.lesen("teilkachel/maengel.png")
        self.assertGreater(bild.shape[0], 40)  # Legende unten
        self.assertEqual(tuple(bild[31, 6]), (255, 0, 0))
        self.assertEqual(tuple(bild[35, 26]), (255, 0, 0))
        self.assertEqual(index["segmente"], [])

    def test_ohne_label_karte_nur_bildarten_ohne_segmente(self):
        index = ansicht(bild_40(), None, self.ordner / "aus")
        self.assertEqual(list(index["teilkachel"]["bilder"]), ["roh", "kontrast", "gitter"])

    def test_falsche_form_und_unbekannte_ids(self):
        with self.assertRaises(AnsichtFehler):
            ansicht(bild_40()[:30], self.karte, self.ordner / "aus")
        with self.assertRaises(AnsichtFehler):
            ansicht(bild_40(), self.karte, self.ordner / "aus", ids=[99])

    def test_einstellungen_ueberschreiben(self):
        eigene = self.ordner / "eigen.json"
        eigene.write_text(json.dumps({"segment_arten": ["nah"], "kontrast": {"clip": 1.0}}), "utf-8")
        vorgaben = einstellungen.laden("ansicht", eigene)
        self.assertEqual(vorgaben["kontrast"], {"clip": 1.0, "kacheln": 8})
        index = ansicht(bild_40(), self.karte, self.ordner / "aus", vorgaben=vorgaben)
        self.assertEqual(index["bilderzahl"], 6 + 4)

    def test_befehl_mit_manifest(self):
        Image.fromarray(bild_40()).save(self.ordner / "r0c0.png")
        dateien.schreibe_json(self.ordner / "manifest.json", {"teilkacheln": [
            {"id": "r0c0", "bild": "r0c0.png",
             "kern_im_bild": {"x": 0, "y": 0, "breite": 36, "hoehe": 36}}]})
        dateien.schreibe_labels(self.ordner / "labels.tif", self.karte)
        dateien.schreibe_json(self.ordner / "segmente.json", self.segmente)
        aus = io.StringIO()
        with redirect_stdout(aus):
            code = main(["ansicht", "--manifest", str(self.ordner / "manifest.json"),
                         "--teilkachel", "r0c0", "--labels", str(self.ordner / "labels.tif"),
                         "--segmente", str(self.ordner / "segmente.json"),
                         "--kategorien", str(self.kat.pfad), "--ziel", str(self.ordner / "aus")])
        self.assertEqual(code, 0)
        self.assertIn("34 Bilder", aus.getvalue())
        self.assertTrue((self.ordner / "aus" / "segmente" / "4" / "nah.png").exists())


if __name__ == "__main__":
    unittest.main()
