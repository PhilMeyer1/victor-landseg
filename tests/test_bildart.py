import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import numpy as np
import tifffile

from landseg import bildart, dateien, kategorien
from landseg.eingriff import Bearbeitung
from landseg.kacheln import kacheln
from landseg.pruefen import pruefen
from landseg.vorbereiten import bauen  # noqa: F401  (Vorlagen-Import prüfen)
from landseg.vorstufe import Roh, auftraege_aus_manifest, vorstufe
from tests.test_vorstufe import KAT, FalschesModell, test_bild, test_konfig


class FleckModell(FalschesModell):
    """Wie FalschesModell, dazu Korn: viele kleine Flecken (6 × 6) der Klasse Haus über das ganze Bild."""

    def berechne(self, bild, klassen, texte):
        roh = super().berechne(bild, klassen, texte)
        h, w = bild.shape[:2]
        for y in range(4, h - 8, 12):
            for x in range(4, w - 8, 12):
                roh.werte[klassen.index("1.1.1"), y:y + 6, x:x + 6] = 0.99
        return Roh(roh.klassen, roh.werte, roh.instanzen)


def _manifest(tmp: Path, grau: bool) -> Path:
    quelle = test_bild(120, 160)
    if grau:
        quelle = quelle.mean(axis=2).astype(np.uint8)
    tifffile.imwrite(tmp / "quelle.tif", quelle)
    kacheln(tmp / "quelle.tif", 0, 0, 160, 120, tmp / "aus", kern=80, rand=8)
    return tmp / "aus" / "manifest.json"


class BildartTest(unittest.TestCase):
    def test_bildart_aus_manifest(self):
        self.assertEqual(bildart.bildart_von({"quelle": {"kanaele": 1}}), "sw")
        self.assertEqual(bildart.bildart_von({"quelle": {"kanaele": 3}}), "farbe")
        self.assertEqual(bildart.bildart_von({"quelle": {"kanaele": 1}, "bildart": "farbe"}), "farbe")

    def test_feinheit_je_bildart(self):
        sw = bildart.feinheit("sw", 500 * 500)
        self.assertEqual(sw["richtwert"], 150)
        self.assertEqual(sw["mindest_px"], 494)  # 100 m² bei 0,45 m
        farbe = bildart.feinheit("farbe", 500 * 500, 0.2)
        self.assertIsNone(farbe["richtwert"])
        self.assertIsNone(farbe["mindest_px"])
        konfig = test_konfig()
        self.assertIs(bildart.vorstufe_konfig(konfig, "farbe"), konfig)
        self.assertNotEqual(bildart.vorstufe_konfig(konfig, "sw")["uebersegmentierung"],
                            konfig["uebersegmentierung"])
        self.assertEqual(bildart.auftrag_block(farbe), "")
        self.assertIn("150", bildart.auftrag_block(sw))

    def test_farbe_unveraendert_sw_weniger_segmente(self):
        """AK1: Farb-Teilkachel wie ohne Bildart (Byte für Byte), SW-Teilkachel weniger Segmente."""
        konfig = test_konfig()
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            farbe = _manifest(tmp, grau=False)
            auftraege = auftraege_aus_manifest(farbe, konfig, ["r1c1"])
            self.assertEqual(auftraege[0].bildart, "farbe")
            with redirect_stdout(io.StringIO()):
                vorstufe(auftraege, konfig, KAT, modell_laden=FleckModell)
            ziel = auftraege[0].ziel
            karte_neu = (ziel / "labels.tif").read_bytes()
            # dieselbe Teilkachel ohne Bildart-Abschnitt (alter Weg: Konfig unverändert, keine Feinheit)
            from landseg import vorstufe as vs
            alt = vs.bildart_modul.vorstufe_konfig
            try:
                vs.bildart_modul.vorstufe_konfig = lambda k, art, werte=None: k
                with redirect_stdout(io.StringIO()):
                    vorstufe(auftraege, konfig, KAT, modell_laden=FleckModell, neu=True)
            finally:
                vs.bildart_modul.vorstufe_konfig = alt
            self.assertEqual((ziel / "labels.tif").read_bytes(), karte_neu)

            sw_tmp = tmp / "sw"
            sw_tmp.mkdir()
            sw = _manifest(sw_tmp, grau=True)
            a_sw = auftraege_aus_manifest(sw, konfig, ["r1c1"])
            self.assertEqual(a_sw[0].bildart, "sw")
            fein = {**bildart.feinheit("sw", 80 * 80), "mindest_px": 50}
            alt_fein = bildart.feinheit
            try:
                bildart.feinheit = lambda *a, **k: fein
                with redirect_stdout(io.StringIO()):
                    vorstufe(a_sw, konfig, KAT, modell_laden=FleckModell)
            finally:
                bildart.feinheit = alt_fein
            seg_farbe = dateien.lese_segmente(ziel / "segmente.json")
            seg_sw = dateien.lese_segmente(a_sw[0].ziel / "segmente.json")
            karte_sw = dateien.lese_labels(a_sw[0].ziel / "labels.tif")
            self.assertLess(len(seg_sw["segmente"]), len(seg_farbe["segmente"]))
            self.assertTrue(pruefen(karte_sw, seg_sw, KAT, form=karte_sw.shape).ok)
            self.assertEqual(seg_sw["vorstufe"]["bildart"], "sw")

    def test_kleine_zusammenlegen_schutz_und_naht(self):
        kat = kategorien.laden()
        karte = np.full((40, 40), 1, np.uint32)
        karte[:, 20:] = 2
        karte[5:7, 5:7] = 3      # klein, unsicher: geht in 1
        karte[10:12, 5:7] = 4    # klein, sicher und Haus: bleibt
        karte[30:32, 25:27] = 5  # klein, aber an der Kerngrenze (y 30): bleibt
        seg = {"segmente": [
            {"id": 1, "klasse": "3.1", "sicher": "ja", "flaeche": 0},
            {"id": 2, "klasse": "2.1", "sicher": "nein", "flaeche": 0},
            {"id": 3, "klasse": "2.1", "sicher": "nein", "flaeche": 0},
            {"id": 4, "klasse": "1.1.1", "sicher": "ja", "flaeche": 0},
            {"id": 5, "klasse": "3.1", "sicher": "nein", "flaeche": 0}], "verlauf": []}
        arbeit = Bearbeitung(karte, seg, kat, "test")
        kern = {"x": 0, "y": 0, "breite": 40, "hoehe": 30}
        schutz = bildart.feinheit("sw")["schutz"]
        erg = bildart.kleine_zusammenlegen(arbeit, 10, schutz, kern, kat)
        ids = set(np.unique(arbeit.karte).tolist())
        self.assertEqual(ids, {1, 2, 4, 5})
        self.assertEqual(erg["zusammengelegt"], 1)
        self.assertEqual(erg["bleiben_unter_mindest"]["schutz"], 1)
        e1 = next(e for e in arbeit.segmente["segmente"] if e["id"] == 1)
        self.assertEqual((e1["klasse"], e1["flaeche"]), ("3.1", int((arbeit.karte == 1).sum())))
        self.assertEqual(arbeit.segmente["verlauf"][-1]["op"], "verschmelzen")
        self.assertTrue(pruefen(arbeit.karte, arbeit.segmente, kat).ok)

    def test_naht_nur_gleiche_klasse_und_einigung_zieht_um(self):
        """An Kern- und Viertelgrenzen nur mit gleicher Klasse zusammenlegen; Beschlüsse gelten danach weiter,
        auch auf der Seite des Partners in der Nachbar-Teilkachel."""
        kat = kategorien.laden()
        karte = np.full((40, 40), 1, np.uint32)
        karte[:, 30:] = 2
        karte[0:4, 26:30] = 3     # klein, an der Kerngrenze (y 0), Klasse wie 1: geht in 1, Beschluss zieht um
        karte[10:14, 26:30] = 4   # klein, an der Kerngrenze (x 29), andere Klasse als 1 und 2: bleibt
        seg = {"segmente": [
            {"id": 1, "klasse": "3.1", "sicher": "nein"},
            {"id": 2, "klasse": "2.1", "sicher": "nein"},
            {"id": 3, "klasse": "3.1", "sicher": "nein",
             "einigung": [{"paar": "r0c0:3|r1c0:7", "mit": "r1c0:7", "entscheidung": "grenze"}]},
            {"id": 4, "klasse": "4.1", "sicher": "nein"}], "verlauf": []}
        nachbar = {"segmente": [{"id": 7, "klasse": "2.1", "sicher": "nein", "einigung": [
            {"paar": "r0c0:3|r1c0:7", "mit": "r0c0:3", "entscheidung": "grenze"}]}], "verlauf": []}
        arbeit = Bearbeitung(karte, seg, kat, "test")
        partner = Bearbeitung(np.full((4, 4), 7, np.uint32), nachbar, kat, "test")
        erg = bildart.kleine_zusammenlegen(arbeit, 20, {}, {"x": 0, "y": 0, "breite": 30, "hoehe": 40}, kat)
        self.assertEqual(set(np.unique(arbeit.karte).tolist()), {1, 2, 4})
        self.assertEqual((erg["an_der_naht"], erg["ersetzt"], erg["bleiben_unter_mindest"]["naht"]), (1, {3: 1}, 1))
        geaendert = bildart.einigung_umbenennen({"r0c0": arbeit, "r1c0": partner}, {"r0c0": erg["ersetzt"]})
        self.assertEqual(geaendert, {"r0c0": 1, "r1c0": 1})
        e1 = next(e for e in arbeit.segmente["segmente"] if e["id"] == 1)
        self.assertEqual([(b["paar"], b["mit"]) for b in e1["einigung"]], [("r0c0:1|r1c0:7", "r1c0:7")])
        self.assertEqual([(b["paar"], b["mit"]) for b in partner.segmente["segmente"][0]["einigung"]],
                         [("r0c0:1|r1c0:7", "r0c0:1")])
        self.assertTrue(pruefen(arbeit.karte, arbeit.segmente, kat).ok)

    def test_naht_nur_mit_beruehrung_im_kern(self):
        """Zwei Segmente gleicher Klasse, die sich nur im Kontextrand berühren, bleiben getrennt (zusammentragen
        schneidet den Rand ab, das Segment wäre im Kern zerteilt)."""
        kat = kategorien.laden()
        karte = np.full((20, 20), 6, np.uint32)
        karte[0:5, 0:12] = 2      # Kern und Kontextrand (x >= 10)
        karte[5:7, 10:20] = 4     # berührt 2 nur im Kontextrand
        karte[7:9, 0:20] = 4      # Teil im Kern, durch 6 von 2 getrennt
        seg = {"segmente": [{"id": 2, "klasse": "3.1", "sicher": "nein"}, {"id": 4, "klasse": "3.1", "sicher": "nein"},
                            {"id": 6, "klasse": "2.1", "sicher": "nein"}], "verlauf": []}
        arbeit = Bearbeitung(karte, seg, kat, "test")
        erg = bildart.kleine_zusammenlegen(arbeit, 100, {}, {"x": 0, "y": 0, "breite": 10, "hoehe": 20}, kat)
        self.assertEqual(set(np.unique(arbeit.karte).tolist()), {2, 4, 6})
        self.assertEqual(erg["bleiben_unter_mindest"]["naht"], 2)

    def test_schutz_nur_im_kopf_des_namens(self):
        schutz = bildart.feinheit("sw")["schutz"]
        for name, erwartet in (("Gebäude (Dachfläche)", True), ("langes Haus auf dem Anger", True),
                               ("Baumreihe an der Dorfstraße", True), ("Gasse oder Hofweg", True),
                               ("Garten / Grasland im Grundstück", True), ("Schattenfuge zwischen Gebäuden", False),
                               ("Schatten zwischen Gebäuden", False), ("Acker", False)):
            self.assertIs(bildart.geschuetzt({"sicher": "ja", "name": name}, schutz), erwartet, name)
        self.assertFalse(bildart.geschuetzt({"sicher": "nein", "name": "Haus"}, schutz))

    def test_pruefen_richtwert_ist_hinweis(self):
        karte = np.arange(1, 17, dtype=np.uint32).reshape(4, 4)
        befund = pruefen(karte, richtwert=10)
        self.assertTrue(befund.ok)
        self.assertEqual(len(befund.hinweise), 1)
        self.assertIn("16 Segmente", befund.hinweise[0])
        self.assertEqual(pruefen(karte, richtwert=10, kern={"x": 0, "y": 0, "breite": 2, "hoehe": 2}).hinweise, [])


if __name__ == "__main__":
    unittest.main()
