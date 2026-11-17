import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from landseg import kategorien
from tests.hilfe import beispiel_kategorien

REPO = Path(__file__).resolve().parent.parent
KAT = kategorien.laden()


def pruefskript():
    spec = importlib.util.spec_from_file_location("pruefe_kategorien", REPO / "tools" / "pruefe_kategorien.py")
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


class KategorienTest(unittest.TestCase):
    def test_kein_siedlungsgruen_und_weg_unter_offenem_boden(self):
        for alt in ("1.4", "1.4.1", "1.4.2", "1.4.3", "1.2.3"):
            self.assertFalse(KAT.gueltig(alt), alt)
        self.assertEqual((KAT.grob("6.6"), KAT.klassen["6.6"]["parent"]), ("6", "6"))
        self.assertEqual(KAT.name("6.6"), "Weg, unbefestigt (Feld-, Wald-, Schotterweg)")

    def test_pruefskript_zaehlt_7_25_43(self):
        doc = json.loads((REPO / "kategorien.json").read_text(encoding="utf-8"))
        fehler, zahlen = pruefskript().check(doc)
        self.assertEqual(fehler, [])
        self.assertEqual((zahlen["level_1"], zahlen["level_2"], zahlen["leaves"], zahlen["classes"]),
                         (7, 25, 43, 58))

    def test_pruefskript_meldet_kaputte_bericht48_regel(self):
        doc = json.loads((REPO / "kategorien.json").read_text(encoding="utf-8"))
        g1 = next(r for r in doc["rules"] if r["id"] == "G1")
        kaputt = copy.deepcopy(doc)
        next(r for r in kaputt["rules"] if r["id"] == "G1")["bericht48"]["im_siedlung_klassen"] = ["1.4"]
        fehler, _ = pruefskript().check(kaputt)
        self.assertTrue(any("bericht48" in f for f in fehler), fehler)
        ohne = copy.deepcopy(doc)
        del next(r for r in ohne["rules"] if r["id"] == "G1")["bericht48"]
        fehler, _ = pruefskript().check(ohne)
        self.assertTrue(any("bericht48" in f for f in fehler), fehler)
        self.assertEqual(g1["bericht48"], {"im_siedlung_klassen": ["2", "3", "4.2"], "im_siedlung_ziel": "1"})


class Bericht48Test(unittest.TestCase):
    def test_im_siedlung_macht_acker_gruenland_gehoelz_zu_siedlung(self):
        for code in ("2", "2.1", "2.2", "2.4.2", "3", "3.1", "3.1.1", "3.4", "4.2", "4.2.1", "4.2.3", "4.2.4"):
            self.assertEqual(KAT.bericht48_klasse(code, "ja"), "1", code)
            self.assertEqual(KAT.bericht48_klasse(code, "nein"), KAT.grob(code), code)
            self.assertEqual(KAT.bericht48_klasse(code), KAT.grob(code), code)

    def test_alles_andere_bleibt_bei_der_ebene_1(self):
        for code in ("0", "0.2", "1.1.1", "1.2.1", "1.3.1", "4", "4.1", "4.1.1", "5.2", "6.1", "6.6"):
            for merkmal in ("ja", "nein", None):
                self.assertEqual(KAT.bericht48_klasse(code, merkmal), KAT.grob(code), (code, merkmal))

    def test_rasen_ist_gruenland_grob_und_siedlung_nur_mit_merkmal(self):
        self.assertEqual(KAT.grob("3.1"), "3")
        self.assertEqual(KAT.bericht48_klasse("3.1", "ja"), "1")

    def test_liste_ohne_regel_bildet_wie_grob_ab(self):
        with tempfile.TemporaryDirectory() as tmp:
            kat = beispiel_kategorien(Path(tmp))
            self.assertEqual(kat.bericht48_klasse("3.1.1", "ja"), "3")

    def test_regel_mit_unbekannter_klasse_scheitert(self):
        with tempfile.TemporaryDirectory() as tmp:
            doc = json.loads((REPO / "kategorien.json").read_text(encoding="utf-8"))
            next(r for r in doc["rules"] if r["id"] == "G1")["bericht48"]["im_siedlung_ziel"] = "9"
            pfad = Path(tmp) / "k.json"
            pfad.write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
            with self.assertRaises(ValueError):
                kategorien.laden(pfad)


if __name__ == "__main__":
    unittest.main()
