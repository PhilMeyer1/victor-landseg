import copy
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

import numpy as np
import tifffile

from landseg import dateien, kategorien
from landseg.__main__ import main
from landseg.kacheln import kacheln
from landseg.pruefen import pruefen
from landseg.sam3 import entdoppeln, fenster
from landseg.vorstufe import (Instanz, Roh, VorstufeFehler, auftraege_aus_manifest, grenzen,
                              bildpunkt_aus_transform, konfig_laden, siedlung_merkmal,
                              uebersegmentierung, verschmelzen, vorstufe)

KAT = kategorien.laden()


def test_konfig() -> dict:
    konfig = konfig_laden(None, KAT)
    konfig = copy.deepcopy(konfig)
    konfig["uebersegmentierung"]["flaeche_px"] = 36
    konfig["prompts"] = [{"klasse": "2.1", "texte": ["crop field"]},
                         {"klasse": "3.1", "texte": ["meadow"]},
                         {"klasse": "1.1.1", "texte": ["house"]}]
    konfig["arbeiter"] = 2
    return konfig


def test_bild(h: int = 60, w: int = 80) -> np.ndarray:
    """Links grün (Feld), rechts hellbraun (Wiese), ein graues Haus 10 × 10 oben rechts."""
    bild = np.zeros((h, w, 3), np.uint8)
    bild[:, : w // 2] = (60, 140, 50)
    bild[:, w // 2:] = (170, 150, 90)
    bild[10:20, 55:65] = (120, 120, 120)
    return bild


class FalschesModell:
    """Statt SAM 3: Feld links, Wiese rechts (rechts unsicher), Haus als Instanz."""

    def __init__(self, unsicher_rechts: bool = True):
        self.aufrufe = 0
        self.unsicher_rechts = unsicher_rechts

    def berechne(self, bild, klassen, texte):
        self.aufrufe += 1
        h, w = bild.shape[:2]
        werte = np.zeros((len(klassen), h, w), np.float32)
        werte[klassen.index("2.1"), :, : w // 2] = 0.9
        rechts = 0.45 if self.unsicher_rechts else 0.9
        werte[klassen.index("3.1"), :, w // 2:] = rechts
        werte[klassen.index("2.1"), :, w // 2:] = 0.4 if self.unsicher_rechts else 0.1
        haus = np.zeros((h, w), bool)
        haus[10:20, 55:65] = True
        werte[klassen.index("1.1.1")][haus] = 0.95
        return Roh(list(klassen), werte, [Instanz(klassen.index("1.1.1"), 0.95, haus, "house")])


class VorstufeTest(unittest.TestCase):
    def setUp(self):
        self.konfig = test_konfig()
        self.klassen = [e["klasse"] for e in self.konfig["prompts"]]

    def test_konfig_des_repos_passt_zur_kategorienliste(self):
        konfig = konfig_laden(None, KAT)
        self.assertGreater(len(konfig["prompts"]), 20)
        self.assertNotIn("_hinweis", konfig)

    def test_konfig_mit_unbekannter_klasse_scheitert(self):
        with tempfile.TemporaryDirectory() as tmp:
            daten = json.loads(Path(self.konfig["_pfad"]).read_text(encoding="utf-8"))
            daten["prompts"].append({"klasse": "9.9", "texte": ["x"]})
            pfad = Path(tmp) / "v.json"
            pfad.write_text(json.dumps(daten), encoding="utf-8")
            with self.assertRaises(VorstufeFehler):
                konfig_laden(pfad, KAT)

    def test_uebersegmentierung_lueckenlos_und_zusammenhaengend(self):
        sp = uebersegmentierung(test_bild(), self.konfig["uebersegmentierung"])
        self.assertEqual(sp.shape, (60, 80))
        self.assertEqual(int((sp == 0).sum()), 0)
        befund = pruefen(sp.astype(np.uint32))
        self.assertTrue(befund.ok, befund.maengel)
        self.assertGreater(befund.segmentzahl, 20)

    def test_verschmelzen_lueckenlos_mit_instanz_und_kandidaten(self):
        bild = test_bild()
        sp = uebersegmentierung(bild, self.konfig["uebersegmentierung"])
        roh = FalschesModell().berechne(bild, self.klassen, [])
        erg = verschmelzen(bild, sp, roh, self.konfig, KAT, id_start=300000,
                           kern={"x": 10, "y": 10, "breite": 40, "hoehe": 40})
        befund = pruefen(erg.labels, erg.segmente, KAT, form=(60, 80))
        self.assertTrue(befund.ok, befund.maengel)
        self.assertEqual(int(erg.labels.min()), 300001)
        nach_klasse = {e["klasse"]: e for e in erg.segmente["segmente"]}
        self.assertEqual(set(nach_klasse), {"2.1", "3.1", "1.1.1"})
        haus = nach_klasse["1.1.1"]
        self.assertEqual((haus["herkunft"], haus["sicher"], haus["grob"]), ("sam3-instanz", "ja", "1"))
        self.assertEqual(nach_klasse["2.1"]["sicher"], "ja")
        self.assertEqual(nach_klasse["3.1"]["sicher"], "nein")  # Wert 0.45, Abstand 0.05
        self.assertEqual(erg.messung["segmente"], 3)
        self.assertEqual(erg.messung["sicher_nein"], 1)
        self.assertFalse(nach_klasse["1.1.1"]["im_kern"])
        arten = {k["art"] for k in erg.kandidaten}
        self.assertIn("klasse_unsicher", arten)

    def test_instanz_in_zwei_teilen_wird_kandidat(self):
        bild = test_bild()
        sp = uebersegmentierung(bild, self.konfig["uebersegmentierung"])
        h, w = sp.shape
        werte = np.zeros((3, h, w), np.float32)
        werte[0] = 0.9
        maske = np.zeros((h, w), bool)
        maske[0:12, 0:12] = True
        maske[40:60, 60:80] = True
        roh = Roh(self.klassen, werte, [Instanz(2, 0.9, maske, "house")])
        erg = verschmelzen(bild, sp, roh, self.konfig, KAT)
        self.assertTrue(pruefen(erg.labels, erg.segmente, KAT).ok)
        zerfallen = [k for k in erg.kandidaten if k["art"] == "nicht_zusammenhaengend"]
        self.assertEqual(len(zerfallen), 1)
        self.assertEqual(len(zerfallen[0]["ids"]), 2)

    def test_kleine_instanz_vor_grosser_umschliessender(self):
        bild = test_bild()
        sp = uebersegmentierung(bild, self.konfig["uebersegmentierung"])
        h, w = sp.shape
        werte = np.zeros((3, h, w), np.float32)
        werte[1] = 0.9
        wiese = np.ones((h, w), bool)
        baum = np.zeros((h, w), bool)
        baum[20:44, 10:34] = True
        roh = Roh(self.klassen, werte, [Instanz(1, 0.95, wiese, "meadow"),
                                        Instanz(2, 0.6, baum, "house")])
        erg = verschmelzen(bild, sp, roh, self.konfig, KAT)
        self.assertTrue(pruefen(erg.labels, erg.segmente, KAT).ok)
        klein = [e for e in erg.segmente["segmente"] if e["klasse"] == "1.1.1"]
        self.assertEqual(len(klein), 1)
        self.assertGreater(klein[0]["flaeche"], 300)
        konfig = copy.deepcopy(self.konfig)
        konfig["verschmelzen"]["instanz_reihenfolge"] = "wert"  # stärkste zuerst: Wiese schluckt
        erg = verschmelzen(bild, sp, roh, konfig, KAT)
        self.assertEqual([e["klasse"] for e in erg.segmente["segmente"]], ["3.1"])

    def test_kleine_instanz_bildpunktgenau(self):
        bild = test_bild()
        sp = uebersegmentierung(bild, self.konfig["uebersegmentierung"])
        h, w = sp.shape
        werte = np.zeros((3, h, w), np.float32)
        werte[0] = 0.9
        maske = np.zeros((h, w), bool)
        maske[30:34, 5:10] = True  # 20 px, kleiner als die Hälfte jedes Superpixels
        roh = Roh(self.klassen, werte, [Instanz(2, 0.8, maske, "house")])
        konfig = copy.deepcopy(self.konfig)
        konfig["uebersegmentierung"]["flaeche_px"] = 400
        sp = uebersegmentierung(bild, konfig["uebersegmentierung"])
        erg = verschmelzen(bild, sp, roh, konfig, KAT)
        self.assertTrue(pruefen(erg.labels, erg.segmente, KAT).ok)
        haus = [e for e in erg.segmente["segmente"] if e["klasse"] == "1.1.1"]
        self.assertEqual(len(haus), 1)
        self.assertEqual(haus[0]["flaeche"], 20)
        self.assertFalse(haus[0]["instanz"]["eingerastet"])
        self.assertIn("zu_klein", {k["art"] for k in erg.kandidaten})

    def test_grenzen_ohne_kante(self):
        labels = np.ones((10, 10), np.int64)
        labels[:, 5:] = 2
        staerke = np.zeros((10, 10), np.float32)
        self.assertEqual(grenzen(labels, staerke), [(1, 2, 10, 0.0)])

    def test_fenster_decken_bild_ab(self):
        self.assertEqual(fenster(628, 628, 1008, 0.25), [(0, 0, 628, 628)])
        f = fenster(1500, 2100, 1008, 0.25)
        abdeckung = np.zeros((1500, 2100), int)
        for x0, y0, x1, y1 in f:
            self.assertEqual((x1 - x0, y1 - y0), (1008, 1008))
            abdeckung[y0:y1, x0:x1] += 1
        self.assertEqual(int((abdeckung == 0).sum()), 0)

    def test_entdoppeln_nur_gleiche_klasse(self):
        a = np.zeros((20, 20), bool)
        a[2:10, 2:10] = True
        b = a.copy()
        b[2:10, 10] = True
        funde = [Instanz(0, 0.7, a, "house"), Instanz(0, 0.9, b, "building"),
                 Instanz(1, 0.5, a, "tree")]
        rest = entdoppeln(funde, {"instanz_doppelt_iou": 0.5})
        self.assertEqual([(i.klasse, i.wert) for i in rest], [(0, 0.9), (1, 0.5)])

    def test_roh_speichern_und_laden(self):
        roh = FalschesModell().berechne(test_bild(), self.klassen, [])
        with tempfile.TemporaryDirectory() as tmp:
            pfad = Path(tmp) / "roh.npz"
            roh.speichern(pfad, "abc")
            self.assertIsNone(Roh.laden(pfad, "anders"))
            wieder = Roh.laden(pfad, "abc")
        self.assertEqual(wieder.klassen, self.klassen)
        self.assertTrue(np.array_equal(wieder.instanzen[0].maske, roh.instanzen[0].maske))
        self.assertTrue(np.allclose(wieder.werte, roh.werte, atol=1e-3))


class AblaufTest(unittest.TestCase):
    def test_manifest_bis_pruefen_mit_wiederaufnahme(self):
        konfig = test_konfig()
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            quelle = np.zeros((120, 160, 3), np.uint8)
            quelle[:, :] = test_bild(120, 160)
            tifffile.imwrite(tmp / "quelle.tif", quelle)
            kacheln(tmp / "quelle.tif", 0, 0, 160, 120, tmp / "aus", kern=80, rand=8)
            auftraege = auftraege_aus_manifest(tmp / "aus" / "manifest.json", konfig)
            self.assertEqual([a.id_start for a in auftraege], [100000, 200000, 300000, 400000])

            modell = FalschesModell()
            with redirect_stdout(io.StringIO()) as aus:
                ergebnisse = vorstufe(auftraege[:2], konfig, KAT, modell_laden=lambda: modell)
            self.assertEqual(modell.aufrufe, 2)
            self.assertTrue(all(e["ok"] for e in ergebnisse), aus.getvalue())
            self.assertIn("r0c0:", aus.getvalue())
            ordner = tmp / "aus" / "vorstufe" / "r0c1"
            karte = dateien.lese_labels(ordner / "labels.tif")
            segmente = dateien.lese_segmente(ordner / "segmente.json")
            self.assertTrue(pruefen(karte, segmente, KAT, form=karte.shape).ok)
            self.assertTrue((karte > 200000).all() and (karte < 300000).all())
            self.assertEqual(json.loads((ordner / "kandidaten.json").read_text(encoding="utf-8"))
                             ["schema"], "landseg-kandidaten/1")
            self.assertIn("messung", segmente["vorstufe"])

            # fertig mit gleichen Einstellungen: übersprungen; --neu: Rohwerte wiederverwendet
            with redirect_stdout(io.StringIO()) as aus:
                vorstufe(auftraege[:2], konfig, KAT, modell_laden=lambda: modell)
                vorstufe(auftraege[:2], konfig, KAT, modell_laden=lambda: modell, neu=True)
            self.assertIn("schon fertig", aus.getvalue())
            self.assertEqual(modell.aufrufe, 2)

    def test_befehl_vorstufe_unbekannte_teilkachel(self):
        with tempfile.TemporaryDirectory() as tmp:
            pfad = Path(tmp) / "manifest.json"
            pfad.write_text(json.dumps({"teilkacheln": [{"id": "r0c0", "bild": "x.png"}]}),
                            encoding="utf-8")
            with redirect_stdout(io.StringIO()), \
                    redirect_stdout(io.StringIO()):
                import contextlib
                with contextlib.redirect_stderr(io.StringIO()) as fehler:
                    code = main(["vorstufe", "--manifest", str(pfad), "--teilkachel", "r9c9"])
        self.assertEqual(code, 2)
        self.assertIn("r9c9", fehler.getvalue())



class SiedlungTest(unittest.TestCase):
    """Merkmal im_siedlung aus der fertigen Karte und Abbildung der Suchtexte auf Klassen."""

    def setUp(self):
        self.konfig = konfig_laden(None, KAT)

    @staticmethod
    def karte():
        """100 × 100: Haus oben links, Wiese und Baum daneben, Weg daneben, Wiese weit weg."""
        labels = np.full((100, 100), 4, np.uint32)  # 4: übrige Wiese
        labels[0:10, 0:10] = 1  # Haus
        labels[0:20, 10:25] = 2  # Wiese neben dem Haus
        labels[:, 60:] = 3  # Wiese fern (mindestens 50 Bildpunkte vom Haus)
        labels[10:20, 0:10] = 5  # unbefestigter Weg neben dem Haus
        labels[20:25, 0:10] = 6  # Gartenbaum neben dem Haus
        segmente = [{"id": 1, "klasse": "1.1.1"}, {"id": 2, "klasse": "3.1"}, {"id": 3, "klasse": "3.1"},
                    {"id": 4, "klasse": "3.1"}, {"id": 5, "klasse": "6.6"}, {"id": 6, "klasse": "4.2.1"}]
        return labels, segmente

    def test_wiese_neben_haus_ja_fern_nein_haus_nein(self):
        labels, segmente = self.karte()
        self.assertEqual(self.konfig["siedlung"]["puffer_m"], 20)
        ja = siedlung_merkmal(labels, segmente, self.konfig["siedlung"], KAT, bildpunkt_m=1.0)
        merkmal = {e["id"]: e["im_siedlung"] for e in segmente}
        self.assertEqual(merkmal, {1: "nein", 2: "ja", 3: "nein", 4: "nein", 5: "nein", 6: "ja"})
        self.assertEqual(ja, 2)

    def test_puffer_in_metern_ueber_bildpunktgroesse(self):
        labels, segmente = self.karte()
        einst = dict(self.konfig["siedlung"], bildpunkt_m=0.2)  # 20 m = 100 Bildpunkte
        siedlung_merkmal(labels, segmente, einst, KAT)
        self.assertEqual({e["id"]: e["im_siedlung"] for e in segmente}[3], "ja")
        self.assertAlmostEqual(bildpunkt_aus_transform({"a": 0.2, "b": 0.0, "c": 5.0, "d": 0.0,
                                                        "e": -0.2, "f": 9.0}), 0.2)
        self.assertIsNone(bildpunkt_aus_transform(None))

    def test_ohne_siedlungszone_alles_nein(self):
        labels, segmente = self.karte()
        segmente[0]["klasse"] = "3.1"
        self.assertEqual(siedlung_merkmal(labels, segmente, self.konfig["siedlung"], KAT, 1.0), 0)
        self.assertEqual({e["im_siedlung"] for e in segmente}, {"nein"})

    def test_verschmelzen_setzt_merkmal_je_segment(self):
        konfig = test_konfig()
        bild = test_bild()
        sp = uebersegmentierung(bild, konfig["uebersegmentierung"])
        roh = FalschesModell().berechne(bild, [e["klasse"] for e in konfig["prompts"]], [])
        erg = verschmelzen(bild, sp, roh, konfig, KAT, bildpunkt_m=0.2)
        nach_klasse = {e["klasse"]: e["im_siedlung"] for e in erg.segmente["segmente"]}
        self.assertEqual(nach_klasse, {"1.1.1": "nein", "2.1": "ja", "3.1": "ja"})
        self.assertEqual(erg.messung["im_siedlung_ja"], 2)
        befund = pruefen(erg.labels, erg.segmente, KAT, form=(60, 80))
        self.assertTrue(befund.ok, befund.maengel)

    def test_konfig_siedlung_ungueltig_scheitert(self):
        with tempfile.TemporaryDirectory() as tmp:
            daten = json.loads(Path(self.konfig["_pfad"]).read_text(encoding="utf-8"))
            daten["siedlung"]["anteil"] = 1.5
            pfad = Path(tmp) / "v.json"
            pfad.write_text(json.dumps(daten), encoding="utf-8")
            with self.assertRaises(VorstufeFehler):
                konfig_laden(pfad, KAT)

    def test_suchtexte_nach_bedeckung(self):
        klasse_je_text = {t: e["klasse"] for e in self.konfig["prompts"] for t in e["texte"]}
        erwartet = {"lawn": ("3.1", "3"), "meadow": ("3.1", "3"), "vegetable garden": ("2.1", "2"),
                    "dirt path": ("6.6", "6"), "dirt road": ("6.6", "6"), "tree": ("4.2.1", "4"),
                    "hedge": ("4.2.3", "4"), "bush": ("4.2.4", "4")}
        for text, (klasse, grob) in erwartet.items():
            self.assertEqual((klasse_je_text[text], KAT.grob(klasse_je_text[text])), (klasse, grob), text)
        for klasse in klasse_je_text.values():
            self.assertFalse(KAT.unter(klasse, ("1.4", "1.2.3")), klasse)

if __name__ == "__main__":
    unittest.main()
