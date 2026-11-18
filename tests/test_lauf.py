"""Tests für ``vorbereiten`` und ``zusammenfuehren`` auf einem Mini-Ausschnitt (80 × 80, vier Teilkacheln)."""

import copy
import hashlib
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

import numpy as np

from landseg import dateien, lauf, vorbereiten, zusammenfuehren
from landseg.__main__ import main
from landseg.lauf import LaufFehler
from tests.hilfe import mini_lauf, mini_urteile

PY = sys.executable


def _stand(ordner: Path) -> dict:
    """Inhalt aller Dateien unter ``ordner`` (Pfad -> Hash), um „nichts geändert“ zu prüfen."""
    return {p.relative_to(ordner).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(ordner.rglob("*")) if p.is_file()}


class LaufTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ordner = Path(self.tmp.name)
        self.manifest = mini_lauf(self.ordner)
        self.daten = self.manifest.parent
        self.ziel = self.ordner / "bericht"

    def tearDown(self):
        self.tmp.cleanup()

    def ruf(self, *argv) -> tuple[int, str, str]:
        aus, err = StringIO(), StringIO()
        with redirect_stdout(aus), redirect_stderr(err):
            rc = main(list(argv))
        return rc, aus.getvalue(), err.getvalue()

    def vorbereiten(self, *extra) -> dict:
        rc, aus, err = self.ruf("vorbereiten", "--manifest", str(self.manifest), "--ziel", str(self.ziel), *extra)
        self.assertEqual(rc, 0, err)
        self.assertTrue(aus.rstrip().endswith("ok"), aus)
        return dateien.lese_json(self.ziel / "auftraege.json")

    # -- AK1 -----------------------------------------------------------------------------------

    def test_vorbereiten_baut_alles(self):
        plan = self.vorbereiten("--py", PY, "--lauf", "probe")
        arten = {}
        for e in plan["einheiten"]:
            arten[e["art"]] = arten.get(e["art"], 0) + 1
            self.assertTrue(Path(e["ergebnis"]).is_dir())
            text = Path(e["auftrag"]).read_text(encoding="utf-8")
            self.assertNotIn("{{", text)
        self.assertEqual(arten, {"a": 4, "b": 16, "c": 16, "z": 4})
        self.assertEqual(plan["kernsegmente"], {"r0c0": 4, "r0c1": 4, "r1c0": 4, "r1c1": 4})
        c = Path(next(e["auftrag"] for e in plan["einheiten"] if e["art"] == "c" and e["tk"] == "r0c1" and e["v"] == 2))
        text = c.read_text(encoding="utf-8")
        self.assertIn("Fassung C „Feste Kategorienliste“", text)
        self.assertIn("agent:c:r0c1-v2:probe", text)
        self.assertIn("c-feste-liste/r0c1/labels.tif", text)
        self.assertNotIn("Klassen frei", text)
        b = next(e["auftrag"] for e in plan["einheiten"] if e["art"] == "b")
        self.assertIn("## Klassen frei", Path(b).read_text(encoding="utf-8"))
        z = next(e["auftrag"] for e in plan["einheiten"] if e["art"] == "z")
        self.assertIn("c-feste-liste/gegenprobe/r0c0/labels.tif", Path(z).read_text(encoding="utf-8"))
        self.assertEqual({v["fassung"] for v in plan["vereinheitlichen"]}, {"A", "B"})
        for tk in ("r0c0", "r1c1"):
            for name in ("ganz_roh.jpg", "ganz_nummern.jpg", "ganz.json"):
                self.assertTrue((self.daten / "ganz" / tk / name).is_file(), name)
            for name in ("uebersicht_nummern.jpg", "uebersicht_gitter.jpg", "nah4.jpg", "viertel.json"):
                self.assertTrue((self.daten / "viertel" / tk / "v3" / name).is_file(), name)
            self.assertTrue((self.daten / "a-alles-frei" / "ansicht" / tk / "ansicht.json").is_file())
        marke = dateien.lese_json(self.daten / "b-kategorien-frei" / lauf.MARKE)
        self.assertEqual((marke["kennung"], marke["art"], marke["klassen"]), ("B", "urteil", "frei"))
        # der Plan ist Eingabe von landseg plan
        rc, _, err = self.ruf("plan", "--auftraege", str(self.ziel / "auftraege.json"),
                              "--ziel", str(self.ziel / "urteil-plan.json"))
        self.assertEqual(rc, 0, err)
        self.assertEqual(len(dateien.lese_json(self.ziel / "urteil-plan.json")["gruppen"]), 40)
        # kein Überschreiben ohne --ersetzen
        rc, _, err = self.ruf("vorbereiten", "--manifest", str(self.manifest), "--ziel", str(self.ziel))
        self.assertEqual(rc, 2)
        self.assertIn("--ersetzen", err)

    # -- AK2 -----------------------------------------------------------------------------------

    def test_selbstpruefung_je_verletzung(self):
        self.vorbereiten()
        plan_pfad = self.ziel / "auftraege.json"
        ursprung = plan_pfad.read_text(encoding="utf-8")

        def nur_pruefen(erwartet: str):
            rc, _, err = self.ruf("vorbereiten", "--manifest", str(self.manifest), "--ziel", str(self.ziel),
                                  "--nur-pruefen")
            self.assertEqual(rc, 1, err)
            self.assertIn(erwartet, err)

        self.assertEqual(self.ruf("vorbereiten", "--manifest", str(self.manifest), "--ziel", str(self.ziel),
                                  "--nur-pruefen")[0], 0)
        # 1. Kernsegment in keinem Viertel-Auftrag
        plan = json.loads(ursprung)
        weg = plan["viertel"][0]["segmente"].pop()
        dateien.schreibe_json(plan_pfad, plan)
        nur_pruefen(f"in keinem Viertel-Auftrag: [{weg}]")
        # ... und in zwei
        plan = json.loads(ursprung)
        plan["viertel"][1]["segmente"].append(plan["viertel"][0]["segmente"][0])
        dateien.schreibe_json(plan_pfad, plan)
        nur_pruefen("in mehreren Viertel-Aufträgen")
        plan_pfad.write_text(ursprung, encoding="utf-8")
        # 2. Platzhalter übrig
        auftrag = Path(json.loads(ursprung)["einheiten"][0]["auftrag"])
        text = auftrag.read_text(encoding="utf-8")
        auftrag.write_text(text + "\n{{ERGEBNIS}}\n", encoding="utf-8")
        nur_pruefen("Platzhalter übrig")
        auftrag.write_text(text, encoding="utf-8")
        # 3. Bild fehlt
        bild = self.daten / "viertel" / "r1c0" / "v2" / "nah3.jpg"
        inhalt = bild.read_bytes()
        bild.unlink()
        nur_pruefen("Bild fehlt")
        bild.write_bytes(inhalt)
        # 4. Kartenkopie nicht bildpunktgleich
        kopie = self.daten / "c-feste-liste" / "r0c1" / "labels.tif"
        karte = dateien.lese_labels(kopie)
        karte[10, 10] += 1
        dateien.schreibe_labels(kopie, karte)
        nur_pruefen("nicht bildpunktgleich")

    # -- AK3 -----------------------------------------------------------------------------------

    def test_zusammenfuehren_drei_fassungen(self):
        plan = self.vorbereiten()
        mini_urteile(plan)
        rc, aus, err = self.ruf("zusammenfuehren", "--manifest", str(self.manifest), "--ziel", str(self.ziel), "--json")
        self.assertEqual(rc, 0, err)
        erg = json.loads(aus)["fassungen"]
        self.assertEqual(set(erg), {"A", "B", "C"})
        for k in "ABC":
            self.assertEqual(erg[k]["segmente_kern"], 16, k)
            self.assertEqual(set(erg[k]["pruefen"].values()), {"ok"}, k)
        self.assertEqual(erg["C"]["eingriffe_urteil"], 4)   # je Teilkachel einer (v1)
        self.assertEqual(erg["C"]["unsicher"], 11)   # sicher: IDs 3, 6, 9, 12, 18
        c = dateien.lese_json(self.daten / "c-feste-liste" / "r0c0" / "segmente.json")
        kern = {s["id"]: s for s in c["segmente"] if s["im_kern"]}
        for sid, s in kern.items():
            self.assertEqual(s["klasse"], "2.1" if sid % 2 else "3")
            self.assertEqual(s["klasse_vorstufe"], ("1.1", "2.1")[sid % 2])
        rand = [s for s in c["segmente"] if not s["im_kern"]]
        self.assertTrue(rand and all(s["urteil"] == "kontextrand" and s["sicher"] == "nein" for s in rand))
        self.assertTrue((self.daten / "c-feste-liste" / "r0c0" / zusammenfuehren.SICHERUNG).is_file())
        a = dateien.lese_json(self.daten / "a-alles-frei" / "r1c0" / "segmente.json")
        self.assertTrue(all(s["id"] > 300000 and s["klasse"] in ("1.1", "2") for s in a["segmente"]))
        self.assertTrue(np.all(dateien.lese_labels(self.daten / "a-alles-frei" / "r1c0" / "labels.tif") > 300000))
        b = dateien.lese_json(self.daten / "b-kategorien-frei" / "r1c1" / "segmente.json")
        self.assertTrue(all(s["klasse"] == ("2" if s["id"] % 2 else "1.1") for s in b["segmente"] if s["im_kern"]))
        for k, ordner in (("A", "a-alles-frei"), ("B", "b-kategorien-frei"), ("C", "c-feste-liste")):
            f = self.daten / ordner
            self.assertTrue((f / "zusammen" / "labels.tif").is_file())
            self.assertTrue((f / f"kategorien-{k.lower()}.json").is_file())
            self.assertTrue((self.ziel / "einigung" / f"auftraege-{k}" / "einigung.json").is_file())
            self.assertEqual(len(erg[k]["buendel"]), len(dateien.lese_json(
                self.ziel / "einigung" / f"auftraege-{k}" / "einigung.json")["buendel"]))
        # zweiter Lauf nur mit --ersetzen, gleiches Ergebnis aus der Sicherung
        self.assertEqual(self.ruf("zusammenfuehren", "--manifest", str(self.manifest), "--ziel", str(self.ziel))[0], 2)
        rc, aus, err = self.ruf("zusammenfuehren", "--manifest", str(self.manifest), "--ziel", str(self.ziel),
                                "--ersetzen", "--json")
        self.assertEqual(rc, 0, err)
        nochmal = dateien.lese_json(self.daten / "c-feste-liste" / "r0c0" / "segmente.json")
        self.assertEqual([s["klasse"] for s in nochmal["segmente"]], [s["klasse"] for s in c["segmente"]])
        self.assertEqual(len(nochmal["verlauf"]), len(c["verlauf"]))

    def test_zusammenfuehren_zwei_fassungen(self):
        werte, seite = lauf.einstellungen_laden()
        werte = copy.deepcopy(werte)
        seite = copy.deepcopy(seite)
        werte["fassungen"] = [f for f in werte["fassungen"] if f["kennung"] in "BC"]
        werte["gegenprobe"] = None
        seite["fassungen"] = [f for f in seite["fassungen"] if f["kennung"] in "BC"]
        plan = vorbereiten.bauen(self.manifest, self.ziel, werte=werte, seite=seite, py=PY)
        self.assertEqual({e["art"] for e in plan["einheiten"]}, {"b", "c"})
        mini_urteile(plan)
        erg = zusammenfuehren.bauen(self.manifest, self.ziel, werte=werte, seite=seite)
        self.assertEqual(set(erg["fassungen"]), {"B", "C"})
        self.assertEqual(erg["fassungen"]["B"]["segmente_kern"], 16)
        self.assertFalse((self.daten / "a-alles-frei").exists())

    # -- AK4 -----------------------------------------------------------------------------------

    def test_vertauschte_zuordnung_und_fehlende_abgabe(self):
        plan = self.vorbereiten()
        mini_urteile(plan)
        vorher = _stand(self.daten)
        # B und C tauschen die Ordner: die Marken fassung.json passen nicht mehr
        seite = copy.deepcopy(lauf.einstellungen_laden()[1])
        ordner = {f["kennung"]: f["ordner"] for f in seite["fassungen"]}
        for f in seite["fassungen"]:
            f["ordner"] = {"B": ordner["C"], "C": ordner["B"]}.get(f["kennung"], f["ordner"])
        seite_pfad = self.ordner / "seite-vertauscht.json"
        dateien.schreibe_json(seite_pfad, {"fassungen": seite["fassungen"]})
        rc, _, err = self.ruf("zusammenfuehren", "--manifest", str(self.manifest), "--ziel", str(self.ziel),
                              "--seite", str(seite_pfad))
        self.assertEqual(rc, 1, err)
        self.assertIn("vertauscht", err)
        self.assertEqual(_stand(self.daten), vorher)
        self.assertFalse((self.ziel / "zusammenfuehren.json").exists())
        # eine Fassung fehlt in lauf.json
        werte = copy.deepcopy(lauf.einstellungen_laden()[0])
        werte["fassungen"] = [f for f in werte["fassungen"] if f["kennung"] != "B"]
        with self.assertRaises(LaufFehler) as fehler:
            zusammenfuehren.bauen(self.manifest, self.ziel, werte=werte)
        self.assertIn("Fassung B aus seite.json fehlt in lauf.json", str(fehler.exception))
        # eine Abgabe fehlt
        urteil = Path(next(e["ergebnis"] for e in plan["einheiten"] if e["art"] == "c")) / "urteil.json"
        urteil.unlink()
        vorher = _stand(self.daten)
        rc, _, err = self.ruf("zusammenfuehren", "--manifest", str(self.manifest), "--ziel", str(self.ziel))
        self.assertEqual(rc, 1, err)
        self.assertIn("Urteil fehlt", err)
        self.assertEqual(_stand(self.daten), vorher)
        # eine Abgabe passt nicht zur Liste
        mini_urteile(plan)
        frei = Path(next(v["ergebnis"] for v in plan["vereinheitlichen"] if v["fassung"] == "A"))
        liste = dateien.lese_json(frei / "kategorien-entwurf.json")
        del liste["abbildung_teilkacheln"]["r0c1"]["9"]
        dateien.schreibe_json(frei / "kategorien-entwurf.json", liste)
        vorher = _stand(self.daten)
        rc, _, err = self.ruf("zusammenfuehren", "--manifest", str(self.manifest), "--ziel", str(self.ziel))
        self.assertEqual(rc, 1, err)
        self.assertIn("ohne Abbildung", err)
        self.assertEqual(_stand(self.daten), vorher)


if __name__ == "__main__":
    unittest.main()
