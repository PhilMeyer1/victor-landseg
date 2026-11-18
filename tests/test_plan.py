"""Tests für ``plan`` (Urteils-Agents: ein Agent je Viertel, Fassung A je Teilkachel) und die Sperre der Karte.

Auftragsliste wie die der Vorbereitung eines Laufs: zwei Teilkacheln, Fassungen A (je Teilkachel), B und C (je
Viertel), Gegenprobe z (C auf r0c0, je Viertel); Segmente je Viertel 10 × Teilkachel + Viertel + 100 × k.
"""

import json
import tempfile
import threading
import time
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

import numpy as np

from landseg import dateien
from landseg.__main__ import main
from landseg.plan import ARTEN, PlanFehler, einheiten_lesen, gruppieren, plan
from tests.hilfe import block_karte

TEILKACHELN = ("r0c0", "r0c1")


def auftraege(ordner: Path) -> dict:
    manifest = ordner / "manifest.json"
    manifest.write_text(json.dumps({"teilkacheln": [{"id": tk} for tk in TEILKACHELN]}), encoding="utf-8")
    daten = {"manifest": str(manifest), "ganz_ausschnitt": f"{ordner}/X0.png", "ganz_raster": f"{ordner}/ganz/X0_raster.jpg",
             "ganz_teilkachel": {tk: {"nummern": f"{ordner}/ganz/{tk}/ganz_nummern.jpg",
                                      "roh": f"{ordner}/ganz/{tk}/ganz_roh.jpg"} for tk in TEILKACHELN},
             "einheiten": [], "viertel": [], "gegenprobe": []}
    for t, tk in enumerate(TEILKACHELN):
        daten["einheiten"].append({"art": "a", "tk": tk, "v": 0, "n": 0, "auftrag": f"{ordner}/a/{tk}/auftrag.md",
                                   "ergebnis": f"{ordner}/a/abgabe/{tk}"})
        for k, art in enumerate(("b", "c", "z")):
            if art == "z" and tk != "r0c0":
                continue
            for v in (1, 2, 3, 4):
                segmente = [10 * t + v + 100 * k, 1000 + 10 * t + v]
                auftrag = f"{ordner}/{art}/{tk}/v{v}/auftrag.md"
                daten["einheiten"].append({"art": art, "tk": tk, "v": v, "n": len(segmente), "auftrag": auftrag,
                                           "ergebnis": f"{ordner}/{art}/urteil/{tk}/v{v}"})
                daten["gegenprobe" if art == "z" else "viertel"].append({"auftrag": auftrag, "segmente": segmente})
    return daten


class PlanTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.ordner = Path(self._tmp.name).as_posix()
        self.daten = auftraege(Path(self.ordner))
        self.datei = Path(self.ordner) / "auftraege.json"
        self.datei.write_text(json.dumps(self.daten), encoding="utf-8")

    def tearDown(self):
        self._tmp.cleanup()

    def test_ein_agent_je_viertel_fassung_a_je_teilkachel(self):
        # AK1, AK3: B, C, Gegenprobe vier Agents je Teilkachel, A einer; jeder Agent genau ein Auftrag
        gruppen = gruppieren(einheiten_lesen(self.daten))
        je = {(art, tk): [g for g in gruppen if g["art"] == art and g["tk"] == tk] for art in ARTEN for tk in TEILKACHELN}
        for tk in TEILKACHELN:
            self.assertEqual(len(je["a", tk]), 1)
            self.assertEqual(je["a", tk][0]["v"], 0)
            self.assertEqual(je["a", tk][0]["label"], f"a:{tk}")
            for art in ("b", "c"):
                self.assertEqual(sorted(g["v"] for g in je[art, tk]), [1, 2, 3, 4])
        self.assertEqual(sorted(g["label"] for g in je["z", "r0c0"]), [f"z:r0c0-v{v}" for v in (1, 2, 3, 4)])
        self.assertEqual(je["z", "r0c1"], [])
        self.assertEqual(len(gruppen), len(self.daten["einheiten"]))
        self.assertTrue(all(len(g["teile"]) == 1 for g in gruppen))
        # jedes Segment in genau einem Auftrag je Art und Teilkachel
        gesehen = {}
        for e in einheiten_lesen(self.daten):
            for sid in e.segmente or ():
                self.assertNotIn((e.art, e.tk, sid), gesehen)
                gesehen[e.art, e.tk, sid] = e.label
        self.assertEqual(len(gesehen), sum(len(x["segmente"]) for x in self.daten["viertel"] + self.daten["gegenprobe"]))

    def test_segment_in_zwei_auftraegen_und_doppelter_auftrag_abgelehnt(self):
        self.daten["viertel"][1]["segmente"][0] = self.daten["viertel"][0]["segmente"][0]
        with self.assertRaisesRegex(PlanFehler, "steht in b:r0c0-v1 und in b:r0c0-v2"):
            gruppieren(einheiten_lesen(self.daten))
        daten = auftraege(Path(self.ordner))
        daten["einheiten"].append(dict(daten["einheiten"][1]))
        with self.assertRaisesRegex(PlanFehler, "doppelt"):
            gruppieren(einheiten_lesen(daten))
        daten = auftraege(Path(self.ordner))
        daten["einheiten"][0]["v"] = 1
        with self.assertRaisesRegex(PlanFehler, "Fassung A hat v 0"):
            einheiten_lesen(daten)

    def test_prompt_viertel_reihenfolge_ohne_nacheinander(self):
        # AK2: Ausschnitt, dann Teilkachel, dann nur das Viertel; keine Sätze des alten Ablaufs
        p = plan(self.datei, "C:/repo", "C:/py/python.exe", hinweis="Schwarz-Weiß-Scan.")
        g = next(g for g in p["gruppen"] if g["label"] == "c:r0c1-v3")
        text = g["prompt"]
        ausschnitt = text.index(f"{self.ordner}/ganz/X0_raster.jpg")
        teilkachel = text.index(f"{self.ordner}/ganz/r0c1/ganz_nummern.jpg")
        viertel = text.index("3. Dann nur dein Viertel v3")
        self.assertLess(ausschnitt, teilkachel)
        self.assertLess(teilkachel, viertel)
        self.assertIn(f"{self.ordner}/c/r0c1/v3/auftrag.md", text)
        self.assertIn("unten links, 2 Segmente", text)
        self.assertIn("Schwarz-Weiß-Scan.", text)
        self.assertIn("(v = 3)", text)
        self.assertNotIn("{{", text)
        for alt in ("nacheinander", "bist das du selbst", "Viertel-Aufträge"):
            self.assertNotIn(alt, text)
        self.assertEqual(text.count("X0_raster.jpg"), 1)
        self.assertEqual(text.count("ganz_nummern.jpg"), 1)
        for andere in (f"{self.ordner}/c/r0c1/v{v}/auftrag.md" for v in (1, 2, 4)):
            self.assertNotIn(andere, text)

    def test_prompt_fassung_a_je_teilkachel(self):
        p = plan(self.datei, "C:/repo", "C:/py/python.exe")
        text = next(g for g in p["gruppen"] if g["label"] == "a:r0c0")["prompt"]
        self.assertIn("ganze Teilkachel r0c0", text)
        self.assertIn("eigenen Vorgehen", text)
        self.assertIn("(v = 0)", text)
        self.assertIn("keiner", text)
        self.assertNotIn("{{", text)

    def test_trockenlauf_eine_teilkachel_zwei_viertel(self):
        # AK5: je Viertel ein Auftrag, Zahl der Agents im Log, nichts geschrieben
        aus = StringIO()
        with redirect_stdout(aus):
            code = main(["plan", "--auftraege", str(self.datei), "--teilkachel", "r0c0", "--viertel", "1", "2"])
        self.assertEqual(code, 0)
        log = aus.getvalue()
        self.assertIn("6 Aufträge in 6 Urteils-Agents (B 2, C 2, Gegenprobe 2;", log)
        for art in ("b", "c", "z"):
            for v in (1, 2):
                self.assertEqual(log.count(f"  {art}:r0c0-v{v}: 1 Auftrag"), 1)
        self.assertNotIn("a:r0c0", log)
        self.assertIn("trocken: nichts geschrieben", log)

    def test_plan_datei_und_manifest(self):
        ziel = Path(self.ordner) / "plan" / "urteil-plan.json"
        with redirect_stdout(StringIO()):
            self.assertEqual(main(["plan", "--auftraege", str(self.datei), "--ziel", str(ziel)]), 0)
        p = json.loads(ziel.read_text(encoding="utf-8"))
        self.assertEqual(p["schema"], "landseg-urteil-plan/1")
        self.assertEqual(p["je_art"], {"a": 2, "b": 8, "c": 8, "z": 4})
        self.assertEqual(p["agents"], 22)
        self.assertEqual(p["gruppen"][0]["teile"][0].keys(), {"art", "tk", "v", "n", "auftrag", "ergebnis"})
        self.daten["einheiten"][0]["tk"] = "r5c5"
        self.datei.write_text(json.dumps(self.daten), encoding="utf-8")
        with self.assertRaisesRegex(PlanFehler, "nicht im Manifest: r5c5"):
            plan(self.datei, "C:/repo", "py")


class SperreTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.ordner = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def test_sperre_exklusiv_und_veraltet(self):
        labels = self.ordner / "labels.tif"
        with dateien.karte_sperren(labels):
            self.assertTrue((self.ordner / "labels.tif.sperre").exists())
            with self.assertRaises(TimeoutError):
                with dateien.karte_sperren(labels, warten=0.3):
                    pass
        self.assertFalse((self.ordner / "labels.tif.sperre").exists())
        (self.ordner / "labels.tif.sperre").write_text("1\n")
        alt = time.time() - 1000
        import os
        os.utime(self.ordner / "labels.tif.sperre", (alt, alt))
        with dateien.karte_sperren(labels, warten=1):
            pass

    def test_gleichzeitige_eingriffe_gehen_nicht_verloren(self):
        # vier Viertel-Agents setzen gleichzeitig Klassen auf derselben Karte: alle vier Änderungen bleiben
        karte, segmente = block_karte(32, 16)
        labels, seg = self.ordner / "labels.tif", self.ordner / "segmente.json"
        dateien.schreibe_labels(labels, karte)
        dateien.schreibe_json(seg, segmente)
        codes = []

        def setzen(sid):
            codes.append(main(["eingriff", "--labels", str(labels), "--segmente", str(seg),
                               "--bearbeiter", f"v{sid}", "klasse", "--id", str(sid), "--klasse", "0"]))

        faeden = [threading.Thread(target=setzen, args=(sid,)) for sid in np.unique(karte).tolist()]
        with redirect_stdout(StringIO()):
            for f in faeden:
                f.start()
            for f in faeden:
                f.join()
        self.assertEqual(len(codes), 4)
        klassen = {s["id"]: s["klasse"] for s in dateien.lese_segmente(seg)["segmente"]}
        self.assertEqual(set(klassen.values()), {"0"})
        self.assertEqual(len(dateien.lese_segmente(seg)["verlauf"]), 4)


if __name__ == "__main__":
    unittest.main()
