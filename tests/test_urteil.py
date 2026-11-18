"""Tests für ``urteil`` (bauen, pruefen) an Wegwerf-Daten.

Teilkachelbild 48 × 48 aus Quadraten zu 12 px (Segmente 1–16, ``block_karte``), Kern 40 × 40 ab (4, 4); Segment 99
liegt nur in den obersten zwei Zeilen und damit nur im Kontextrand. Viertel v1 (oben links, Kern 0–19) enthält die
Segmente 1, 2, 5, 6.
"""

import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

from landseg import dateien
from landseg.__main__ import main
from landseg.urteil import SCHEMA, UrteilFehler, bauen, grundlage_laden, pruefen
from tests.hilfe import beispiel_kategorien, block_karte

TEIL = {"id": "r0c0", "bild": "teilkacheln/r0c0.png", "kern": {"x": 0, "y": 0, "breite": 40, "hoehe": 40},
        "kontext": {"x": -4, "y": -4, "breite": 48, "hoehe": 48},
        "kern_im_bild": {"x": 4, "y": 4, "breite": 40, "hoehe": 40}}


class UrteilTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ordner = Path(self.tmp.name)
        self.kat = beispiel_kategorien(self.ordner)
        karte, self.segmente = block_karte(48, 12)
        karte[0:2, :] = 99
        self.segmente["segmente"].append({"id": 99, "klasse": "3", "grob": "3"})
        self.karte = karte
        self.manifest = self.ordner / "manifest.json"
        dateien.schreibe_json(self.manifest, {"teilkacheln": [TEIL]})
        self.labels = self.ordner / "vorstufe" / "labels.tif"
        self.seg_pfad = self.ordner / "vorstufe" / "segmente.json"
        dateien.schreibe_labels(self.labels, karte)
        dateien.schreibe_json(self.seg_pfad, self.segmente)
        self.ergebnis = self.ordner / "ergebnis"
        self.ergebnis.mkdir()
        (self.ergebnis / "nah_6_1.jpg").write_bytes(b"jpg")

    def tearDown(self):
        self.tmp.cleanup()

    def grundlage(self, viertel=None, labels=None):
        return grundlage_laden(self.manifest, "r0c0", labels or self.labels, self.kat, self.seg_pfad, viertel)

    def liste(self, sauber=None) -> dict:
        return {"segmente": [[6, "nicht_sauber", "3.1", [["trennen", "Hecke bei x 20/y 22 abtrennen", 40],
                                                         {"art": "klasse", "text": "eher Laubwald"}],
                              ["nah_6_1.jpg"]],
                             {"id": 2, "urteil": "sauber", "was": "Laubwald am Weg", "sicher": False}],
                "sauber": [i for i in range(1, 17) if i not in (2, 6)] if sauber is None else sauber,
                "naht": [{"id": 4, "seite": "rechts", "text": "Wald endet an der Kerngrenze"}],
                "unsicher": ["Segment 2: Schatten"]}

    def test_bauen_feld_fuer_feld(self):
        urteil = bauen(self.grundlage(), self.liste(), "urt-r0c0")
        klasse = {s["id"]: s["klasse"] for s in self.segmente["segmente"]}
        self.assertEqual(list(urteil), ["schema", "teilkachel", "bearbeiter", "segmente", "naht", "unsicher",
                                        "nicht_geprueft", "offen"])
        self.assertEqual((urteil["schema"], urteil["teilkachel"], urteil["bearbeiter"]), (SCHEMA, "r0c0", "urt-r0c0"))
        self.assertEqual([s["id"] for s in urteil["segmente"]], list(range(1, 17)))
        nach_id = {s["id"]: s for s in urteil["segmente"]}
        self.assertEqual(nach_id[6], {
            "id": 6, "klasse_heute": klasse[6], "was_ist_es": self.kat.name(klasse[6]), "urteil": "nicht_sauber",
            "klasse_vorschlag": "3.1", "sicher": True,
            "punkte": [{"nr": 1, "art": "trennen", "text": "Hecke bei x 20/y 22 abtrennen", "flaeche_px": 40},
                       {"nr": 2, "art": "klasse", "text": "eher Laubwald", "flaeche_px": None}],
            "bilder": ["nah_6_1.jpg"]})
        self.assertEqual(nach_id[2], {"id": 2, "klasse_heute": klasse[2], "was_ist_es": "Laubwald am Weg",
                                      "urteil": "sauber", "klasse_vorschlag": None, "sicher": False, "punkte": [],
                                      "bilder": []})
        self.assertEqual(nach_id[1]["urteil"], "sauber")
        self.assertEqual(urteil["naht"], [{"id": 4, "seite": "rechts", "text": "Wald endet an der Kerngrenze"}])
        self.assertEqual((urteil["unsicher"], urteil["nicht_geprueft"], urteil["offen"]), (["Segment 2: Schatten"], [], []))
        self.assertEqual(pruefen(self.grundlage(), urteil, self.ergebnis), [])

    def test_ausgelassenes_segment_wird_gemeldet_nicht_ergaenzt(self):
        urteil = bauen(self.grundlage(), self.liste(sauber=[1, 3]), "urt-r0c0")
        self.assertEqual([s["id"] for s in urteil["segmente"]], [1, 2, 3, 6])
        fehler = pruefen(self.grundlage(), urteil, self.ergebnis)
        self.assertEqual(len(fehler), 1)
        self.assertIn("ohne Eintrag (12 im Kern): 4, 5, 7", fehler[0])

    def test_pruefen_je_fehlerart(self):
        gut = bauen(self.grundlage(), self.liste(), "urt-r0c0")
        self.assertEqual(pruefen(self.grundlage(), gut, self.ergebnis), [])

        def mit(aendern):
            u = json.loads(json.dumps(gut))
            aendern(u)
            return pruefen(self.grundlage(), u, self.ergebnis)

        def segment(u, sid):
            return next(s for s in u["segmente"] if s["id"] == sid)

        faelle = {
            "ohne Eintrag": (lambda u: u["segmente"].pop(0), "ohne Eintrag (1 im Kern): 1"),
            "doppelt": (lambda u: u["segmente"].append(dict(u["segmente"][0])), "mehr als ein Eintrag: Segment 1"),
            "unbekannte Klasse": (lambda u: segment(u, 6).update(klasse_vorschlag="9.9"),
                                  "Segment 6: unbekannte Klasse '9.9'"),
            "unbekannte Punktart": (lambda u: segment(u, 6)["punkte"][0].update(art="loch"),
                                    "Segment 6: unbekannte Punktart 'loch'"),
            "fehlende Bilddatei": (lambda u: segment(u, 6)["bilder"].append("nah_6_2.jpg"),
                                   "Segment 6: Bilddatei nah_6_2.jpg fehlt"),
            "außerhalb des Kerns": (lambda u: u["segmente"].append({**segment(u, 3), "id": 99}),
                                    "Segment 99: liegt nicht im Kern von r0c0"),
            "Urteil unbekannt": (lambda u: segment(u, 4).update(urteil="gut"), "Segment 4: Urteil 'gut'"),
        }
        for name, (aendern, erwartet) in faelle.items():
            with self.subTest(fall=name):
                fehler = mit(aendern)
                self.assertEqual(len(fehler), 1, fehler)
                self.assertIn(erwartet, fehler[0])
        alle = mit(lambda u: [f[0](u) for f in faelle.values()])
        self.assertGreaterEqual(len(alle), len(faelle), "alle Fehler auf einmal, nicht nur der erste")

    def test_viertel(self):
        g = self.grundlage("v1")
        self.assertEqual(g.soll, [1, 2, 5, 6])
        liste = {"segmente": [[6, "sauber"], [2, "sauber"]], "sauber": [1, 5]}
        urteil = bauen(g, liste, "urt-r0c0-v1")
        self.assertEqual((urteil["viertel"], [s["id"] for s in urteil["segmente"]]), ("v1", [1, 2, 5, 6]))
        self.assertEqual(pruefen(g, urteil, self.ergebnis), [])
        urteil["segmente"].append({**urteil["segmente"][0], "id": 3})
        self.assertEqual(pruefen(g, urteil, self.ergebnis), ["Segment 3: gehört zum Viertel v2, nicht zu v1"])
        self.assertEqual(sorted(len(self.grundlage(v).soll) for v in ("v1", "v2", "v3", "v4")), [4, 4, 4, 4])

    def test_nachsegmentiert_zaehlt_die_aktuelle_karte(self):
        karte = self.karte.copy()
        karte[14:20, 14:20] = 50  # aus Segment 6 nachträglich herausgeteilt
        neu = self.ordner / "nach" / "labels.tif"
        dateien.schreibe_labels(neu, karte)
        urteil = bauen(self.grundlage(), self.liste(), "urt-r0c0")
        self.assertEqual(pruefen(self.grundlage(labels=neu), urteil, self.ergebnis),
                         ["ohne Eintrag (1 im Kern): 50"])

    def test_formfehler_der_liste(self):
        with self.assertRaises(UrteilFehler):
            bauen(self.grundlage(), {"segmente": ["sechs"]}, "urt")
        with self.assertRaises(UrteilFehler):
            bauen(self.grundlage(), self.liste(), " ")

    def test_befehl(self):
        for schritt in ("bauen", "pruefen"):
            with redirect_stdout(StringIO()), self.assertRaises(SystemExit) as ende:
                main(["urteil", schritt, "--help"])
            self.assertEqual(ende.exception.code, 0)
        liste = self.ordner / "liste.json"
        liste.write_text(json.dumps(self.liste(), ensure_ascii=False), encoding="utf-8")
        ziel = self.ergebnis / "urteil.json"
        basis = ["--manifest", str(self.manifest), "--labels", str(self.labels), "--kategorien", str(self.kat.pfad)]
        aus = StringIO()
        with redirect_stdout(aus):
            code = main(["urteil", "bauen", *basis, "--teilkachel", "r0c0", "--segmente", str(self.seg_pfad),
                         "--bearbeiter", "urt-r0c0", "--liste", str(liste), "--ziel", str(ziel)])
        self.assertEqual(code, 0, aus.getvalue())
        self.assertIn("ok: r0c0, 16 Segmente", aus.getvalue())
        with redirect_stdout(StringIO()):
            self.assertEqual(main(["urteil", "pruefen", *basis, "--urteil", str(ziel)]), 0)
        kaputt = dateien.lese_json(ziel)
        kaputt["segmente"][0]["punkte"] = [{"nr": 1, "art": "loch", "text": "x"}]
        dateien.schreibe_json(ziel, kaputt)
        aus = StringIO()
        with redirect_stdout(aus):
            self.assertEqual(main(["urteil", "pruefen", *basis, "--urteil", str(ziel)]), 1)
        self.assertIn("unbekannte Punktart 'loch'", aus.getvalue())
        liste.write_text(json.dumps(self.liste(sauber=[])), encoding="utf-8")
        ziel2 = self.ergebnis / "zwei.json"
        with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
            self.assertEqual(main(["urteil", "bauen", *basis, "--teilkachel", "r0c0", "--segmente", str(self.seg_pfad),
                                   "--bearbeiter", "urt", "--liste", str(liste), "--ziel", str(ziel2)]), 1)
        self.assertFalse(ziel2.exists(), "mit Fehlern wird nichts geschrieben")


if __name__ == "__main__":
    unittest.main()
