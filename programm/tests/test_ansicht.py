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
from landseg.ansicht import Ansicht, AnsichtFehler, Fenster, ansicht
from landseg.zoom import zoom
from tests.hilfe import beispiel_karte, beispiel_kategorien

TEIL_ARTEN = ["roh", "umriss", "maengel", "vorschlag", "kontrast", "gitter"]
SEGMENT_ARTEN = ["roh", "umriss", "maengel", "vorschlag", "nah", "paar", "kontrast", "gitter"]


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
        self.assertEqual(index["bilderzahl"], 6 + 4 * 8)
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

    def test_paar_roh_neben_nummern_im_selben_massstab(self):
        index = ansicht(bild_40(), self.karte, self.ordner / "aus", segmente=self.segmente,
                        kategorien=self.kat, ids=[4])
        s = index["segmente"][0]
        f, versatz = s["paar"]["fenster"], s["paar"]["versatz"]
        streifen = einstellungen.laden("ansicht")["paar"]["streifen"]
        self.assertEqual(f, s["fenster"])  # klein genug: Faktor wie bei nah
        self.assertEqual(versatz, f["breite"] * f["faktor"] + streifen)
        paar = self.lesen(s["bilder"]["paar"])
        self.assertEqual(paar.shape[:2], (f["hoehe"] * f["faktor"], 2 * f["breite"] * f["faktor"] + streifen))
        fenster = bild_40()[f["y"]:f["y"] + f["hoehe"], f["x"]:f["x"] + f["breite"]]
        roh_gross = np.repeat(np.repeat(fenster, f["faktor"], axis=0), f["faktor"], axis=1)
        self.assertTrue((paar[:, :f["breite"] * f["faktor"]] == roh_gross).all())  # linke Hälfte = Rohbild
        self.assertTrue((paar[:, f["breite"] * f["faktor"]:versatz] == (20, 20, 24)).all())  # Streifen

        def teilkachel(x_bild: int, y_bild: int, rechts: bool) -> tuple[int, int]:
            return (f["x"] + (x_bild - (versatz if rechts else 0)) // f["faktor"],
                    f["y"] + y_bild // f["faktor"])

        # Grenze 1|2 (Teilkachel x = 19) liegt rechts gelb, links an derselben Stelle steht das Rohbild
        a = Ansicht(bild_40(), self.karte, self.segmente, self.kat, einstellungen.laden("ansicht"))
        pf = a.paar_fenster(Fenster(10, 0, 20, 30, 4))
        bild = a.zeichnen("paar", pf)
        x_links, y_bild = (19 - 10) * 4 + 3, 2 * 4 + 1  # Grenze: letzte Spalte vor dem Wechsel
        x_rechts = a.paar_versatz(pf) + x_links
        self.assertEqual(tuple(bild[y_bild, x_rechts]), (255, 255, 0))
        self.assertTrue((bild[y_bild, x_links] == bild_40()[2, 19]).all())
        f, versatz = pf.als_dict(), a.paar_versatz(pf)
        self.assertEqual(teilkachel(x_links, y_bild, False), (19, 2))
        self.assertEqual(teilkachel(x_rechts, y_bild, True), (19, 2))
        gespeichert = json.loads((self.ordner / "aus" / "ansicht.json").read_text("utf-8"))
        self.assertIn("versatz", gespeichert["koordinaten"])
        self.assertIn("ID mod 100000", gespeichert["nummern"])

    def test_paar_hoechstens_2000_bildpunkte(self):
        karte = np.ones((300, 400), np.uint32)
        karte[:, 200:] = 2
        karte[150:, :] += 100000  # IDs mit Teilkachel-Block: im Bild steht ID mod 100000
        a = Ansicht(np.full((300, 400, 3), 90, np.uint8), karte, None, None, einstellungen.laden("ansicht"))
        sechsfach = Fenster(0, 0, 200, 150, 6)  # als Paar 2 × 1200 + 8 breit
        with self.assertRaises(AnsichtFehler):
            a.zeichnen("paar", sechsfach)
        pf = a.paar_fenster(sechsfach)
        self.assertEqual((pf.faktor, pf.x, pf.y, pf.breite, pf.hoehe), (4, 0, 0, 200, 150))
        bild = a.zeichnen("paar", pf)
        self.assertLessEqual(max(bild.shape[:2]), 2000)
        self.assertEqual(bild.shape[:2], (600, 2 * 800 + 8))
        rechts = bild[:, a.paar_versatz(pf):]
        self.assertTrue((rechts > 230).all(axis=2).any())  # Nummern (weiß) gezeichnet
        self.assertFalse((bild[:, :800] > 230).all(axis=2).any())
        with self.assertRaises(AnsichtFehler):  # auch im Maßstab 1 zu breit
            Ansicht(np.zeros((10, 1200, 3), np.uint8), np.ones((10, 1200), np.uint32), None, None,
                    einstellungen.laden("ansicht")).paar_fenster(Fenster(0, 0, 1200, 10, 1))

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
        self.assertIn("38 Bilder", aus.getvalue())
        self.assertTrue((self.ordner / "aus" / "segmente" / "4" / "nah.png").exists())


class ZoomTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ordner = Path(self.tmp.name)
        self.kat = beispiel_kategorien(self.ordner)
        self.karte, self.segmente = beispiel_karte()
        self.ansicht = Ansicht(bild_40(), self.karte, self.segmente, self.kat, einstellungen.laden("ansicht"),
                               kern={"x": 4, "y": 4, "breite": 32, "hoehe": 32})
        self.vorgaben = einstellungen.laden("zoom")

    def tearDown(self):
        self.tmp.cleanup()

    def test_stellen_groesse_format_und_nummern(self):
        for name, stelle in {"punkt": {"punkt": (30, 30), "radius": 6},
                             "rechteck": {"rechteck": {"x": 10, "y": 0, "breite": 20, "hoehe": 40}},
                             "ids": {"ids": [2, 4]}}.items():
            with self.subTest(stelle=name):
                ziel = self.ordner / f"{name}.jpg"
                erg = zoom(self.ansicht, self.vorgaben, ziel, roh=True, titel="r0c0", **stelle)
                with Image.open(ziel) as jpg:
                    self.assertEqual(jpg.format, "JPEG")
                    self.assertLessEqual(max(jpg.size), 2000)
                    self.assertEqual(list(jpg.size), erg["groesse"])
                self.assertGreater(erg["fenster"]["faktor"], 1)
                for n in erg["nummern"]:  # jede Nummer steht in ihrem Segment
                    self.assertEqual(int(self.karte[n["y"], n["x"]]), n["id"])
        erg = zoom(self.ansicht, self.vorgaben, self.ordner / "p.jpg", punkt=(30, 30), radius=6)
        self.assertEqual(erg["fenster"], {"x": 24, "y": 24, "breite": 13, "hoehe": 13, "faktor": 8})
        self.assertEqual([n["id"] for n in erg["nummern"]], [3])
        erg = zoom(self.ansicht, self.vorgaben, self.ordner / "i.jpg", ids=[4])
        self.assertEqual({n["id"] for n in erg["nummern"]}, {1, 2, 3, 4})  # Rand 24 um Segment 4

    def test_lange_seite_hoechstens_2000(self):
        gross = np.zeros((300, 1400), np.uint32) + 1
        gross[:, 700:] = 2
        a = Ansicht(np.full((300, 1400, 3), 90, np.uint8), gross, None, None, einstellungen.laden("ansicht"))
        erg = zoom(a, self.vorgaben, self.ordner / "g.jpg", rechteck={"x": 0, "y": 0, "breite": 1400, "hoehe": 300},
                   roh=True)
        self.assertLessEqual(max(erg["groesse"]), 2000)
        self.assertTrue(erg["verkleinert"])

    def test_falsche_angaben(self):
        with self.assertRaises(AnsichtFehler):
            zoom(self.ansicht, self.vorgaben, self.ordner / "x.png", ids=[1])
        with self.assertRaises(AnsichtFehler):
            zoom(self.ansicht, self.vorgaben, self.ordner / "x.jpg", ids=[77])
        with self.assertRaises(AnsichtFehler):
            zoom(self.ansicht, self.vorgaben, self.ordner / "x.jpg", punkt=(1, 1))

    def test_befehl(self):
        Image.fromarray(bild_40()).save(self.ordner / "r0c0.png")
        dateien.schreibe_labels(self.ordner / "labels.tif", self.karte)
        with redirect_stdout(io.StringIO()), self.assertRaises(SystemExit) as ende:
            main(["zoom", "--help"])
        self.assertEqual(ende.exception.code, 0)
        aus = io.StringIO()
        with redirect_stdout(aus):
            code = main(["zoom", "--bild", str(self.ordner / "r0c0.png"), "--labels", str(self.ordner / "labels.tif"),
                         "--ids", "4", "--roh", "--ziel", str(self.ordner / "z" / "nah_4_1.jpg"), "--json"])
        self.assertEqual(code, 0)
        self.assertTrue(json.loads(aus.getvalue())["roh"])
        self.assertTrue((self.ordner / "z" / "nah_4_1.jpg").exists())


if __name__ == "__main__":
    unittest.main()
