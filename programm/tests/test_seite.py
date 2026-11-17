"""Tests für W8 seite (Übersichtsseite): Fassungen, Daten, Einbettung, Nähte, Lücken, Fehlerfälle, Befehl."""

import base64
import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image

from landseg import dateien, einstellungen
from landseg.__main__ import main
from landseg.kacheln import kacheln
from landseg.seite import SeiteFehler, labels_als_rgb, seite, seite_daten
from tests.hilfe import beispiel_kategorien
from tests.test_kacheln import PRJ


def daten_aus_html(html: str) -> dict:
    anfang = html.index("window.DATEN = ") + len("window.DATEN = ")
    ende = html.index(";\n</script>", anfang)
    return json.loads(html[anfang:ende])


def ids_aus_png(uri: str) -> np.ndarray:
    rgb = np.asarray(Image.open(io.BytesIO(base64.b64decode(uri.split(",", 1)[1]))).convert("RGB")).astype(np.uint32)
    return rgb[..., 0] + (rgb[..., 1] << 8) + (rgb[..., 2] << 16)


class SeiteTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ordner = Path(self.tmp.name)
        quelle = self.ordner / "quelle"
        quelle.mkdir()
        tif = quelle / "blatt.tif"
        tifffile.imwrite(tif, np.full((60, 100, 3), 120, np.uint8), photometric="rgb")  # ohne Bildkanten
        (quelle / "blatt.TFW").write_text("0.2\n0\n0\n-0.2\n1000.1\n5000.9\n", encoding="ascii")
        (quelle / "blatt.PRJ").write_text(PRJ, encoding="ascii")
        self.t = self.ordner / "T"
        self.manifest = kacheln(tif, 0, 0, 80, 40, self.t, kern=40, rand=8, name="TX")
        self.kat = beispiel_kategorien(self.ordner)

    def tearDown(self):
        self.tmp.cleanup()

    def stand(self, ordner: Path, ids: dict[str, int], klasse: dict[str, str], luecke: bool = False):
        for t in self.manifest["teilkacheln"]:
            k = t["kontext"]
            karte = np.full((k["hoehe"], k["breite"]), ids[t["id"]], np.uint32)
            if luecke and t["id"] == "r0c0":
                karte[0:2, 0:2] = 0
            ziel = ordner / t["id"]
            ziel.mkdir(parents=True, exist_ok=True)
            dateien.schreibe_labels(ziel / "labels.tif", karte)
            dateien.schreibe_json(ziel / "segmente.json", {"schema": "landseg-segmente/1", "segmente": [
                {"id": ids[t["id"]], "klasse": klasse[t["id"]], "grob": klasse[t["id"]].split(".")[0], "sicher": "nein"}],
                "verlauf": [{"nr": 1, "op": "klasse", "bearbeiter": "test", "parameter": {"id": ids[t["id"]]}}]})

    def feste_liste(self, **kw):
        """Fassung C (feste Kategorienliste): Klassen aus der Liste des Aufrufs, eine Naht ohne Bildkante."""
        self.stand(self.t / "c-feste-liste", {"r0c0": 1001, "r0c1": 2001}, {"r0c0": "1.1", "r0c1": "3.1.1"}, **kw)

    def fassung_b(self, mit_liste: bool = True):
        """Freie Fassung B mit eigener, zweistufiger Kategorienliste und einem Segment über beide Teilkacheln."""
        ordner = self.t / "b-kategorien-frei"
        self.stand(ordner, {"r0c0": 7, "r0c1": 7}, {"r0c0": "w.1", "r0c1": "w.1"})
        if mit_liste:
            dateien.schreibe_json(ordner / "kategorien-b.json", {"classes": [
                {"code": "w", "name": "Wasser frei", "parent": None, "level": 1, "color": "#2060ff"},
                {"code": "w.1", "name": "Teich frei", "parent": "w", "level": 2, "color": "#40a0ff"}]})
        return ordner

    def test_fassungen_mit_eigener_liste(self):
        self.feste_liste()
        self.fassung_b()
        ziel = self.t / "seite" / "TX.html"
        erg = seite(self.t / "manifest.json", ziel, self.kat)
        html = ziel.read_text(encoding="utf-8")
        for platz in ("/*CSS*/", "/*JS*/", "/*DATEN*/", "<!--TITEL-->"):
            self.assertNotIn(platz, html)
        self.assertIn("<title>Übersicht TX</title>", html)
        d = daten_aus_html(html)
        self.assertEqual([t["id"] for t in d["teilkacheln"]], ["r0c0", "r0c1"])
        self.assertNotIn("nachher", json.dumps(d))
        a, b, c = d["fassungen"]
        self.assertEqual([(f["kennung"], f["name"]) for f in (a, b, c)],
                         [("A", "Alles frei"), ("B", "Kategorien frei"), ("C", "Feste Kategorienliste")])
        self.assertEqual([a["vorhanden"], b["vorhanden"], c["vorhanden"]], [False, True, True])
        self.assertTrue(a["beschreibung"])
        self.assertNotIn("kategorien", a)
        # C: Klassen aus der Liste des Aufrufs; verschiedene IDs an der Kerngrenze ohne Bildkante -> Nahtverstoß
        self.assertEqual({k["code"] for k in c["kategorien"]}, set(self.kat.klassen))
        self.assertEqual([e["klassen"] for e in c["ebenen"]], [3, 3, 3])  # Blätter zählen auf feineren Ebenen mit
        self.assertEqual(c["ebenen"][0]["name"], "grob")
        links = c["teilkacheln"]["r0c0"]
        self.assertEqual(len(links["naht"]), 1)
        kx = d["teilkacheln"][0]["kontext"]["x"]
        self.assertEqual(links["naht"][0]["von"][0], self.manifest["teilkacheln"][1]["kern"]["x"] - kx)
        ids = ids_aus_png(links["labels"])
        self.assertEqual(ids.shape, (d["teilkacheln"][0]["kontext"]["hoehe"], d["teilkacheln"][0]["kontext"]["breite"]))
        self.assertTrue((ids == 1001).all())
        self.assertEqual(links["segmente"][0]["eingriffe"], ["1: klasse (test)"])
        self.assertTrue(links["pruefen"]["ok"])
        # B: eigene Liste mit eigenen Codes, Namen, Farben und Ebenen; ein Segment über die Naht -> keine Verstöße
        self.assertEqual([(k["code"], k["name"], k["color"]) for k in b["kategorien"]],
                         [("w", "Wasser frei", "#2060ff"), ("w.1", "Teich frei", "#40a0ff")])
        self.assertEqual([(e["name"], e["klassen"]) for e in b["ebenen"]], [("grob", 1), ("mittel", 1)])
        self.assertTrue(b["kategorien_quelle"].endswith("b-kategorien-frei/kategorien-b.json"))
        self.assertTrue(b["teilkacheln"]["r0c0"]["pruefen"]["ok"])
        self.assertTrue((ids_aus_png(b["gesamt"]) == 7).all())
        self.assertEqual([(f["kennung"], f["vorhanden"], f.get("naht")) for f in erg["fassungen"]],
                         [("A", False, None), ("B", True, 0), ("C", True, 1)])

    def test_luecke(self):
        self.feste_liste(luecke=True)
        d = seite_daten(self.t / "manifest.json", self.kat)
        befund = d["fassungen"][2]["teilkacheln"]["r0c0"]["pruefen"]
        self.assertFalse(befund["ok"])
        self.assertEqual(befund["ohne_segment"], 4)

    def test_fehlende_teilkachel_naht_nicht_geprueft(self):
        self.feste_liste()
        (self.t / "c-feste-liste" / "r0c1" / "labels.tif").unlink()
        a = seite_daten(self.t / "manifest.json", self.kat)["fassungen"][2]
        self.assertIsNone(a["teilkacheln"]["r0c1"])
        self.assertIsNone(a["naht"])
        self.assertIsNone(a["gesamt"])

    def test_nur_freie_fassung_und_eigene_fassungsliste(self):
        b = self.fassung_b()
        werte = {**einstellungen.laden("seite"), "fassungen": [
            {"kennung": "A", "name": "fest", "ordner": "vorstufe"},
            {"kennung": "P", "name": "Probe", "beschreibung": "nur Probe", "ordner": str(b), "kategorien": "kategorien-b.json"}]}
        d = seite_daten(self.t / "manifest.json", self.kat, werte=werte)
        self.assertEqual([(f["kennung"], f["vorhanden"]) for f in d["fassungen"]], [("A", False), ("P", True)])
        self.assertEqual(d["fassungen"][1]["beschreibung"], "nur Probe")

    def test_einbettung_sicher(self):
        self.feste_liste()
        kommentare = self.ordner / "k.json"
        kommentare.write_text(json.dumps({"kommentare": [{"nr": 1, "fassung": "C", "teilkachel": "r0c0", "segment": 1001,
                                                          "text": "</script><b>x</b>"}]}), encoding="utf-8")
        ziel = self.ordner / "s.html"
        seite(self.t / "manifest.json", ziel, self.kat, kommentare=kommentare)
        html = ziel.read_text(encoding="utf-8")
        self.assertEqual(html.count("</script>"), 2)
        self.assertEqual(daten_aus_html(html)["kommentare"][0]["text"], "</script><b>x</b>")

    def test_fehler(self):
        with self.assertRaises(SeiteFehler):
            seite_daten(self.t / "manifest.json", self.kat)  # keine Fassung mit Daten
        self.feste_liste()
        with self.assertRaises(SeiteFehler):
            seite(self.t / "manifest.json", self.ordner / "s.txt", self.kat)
        self.fassung_b(mit_liste=False)
        with self.assertRaises(SeiteFehler):  # freie Fassung ohne eigene Kategorienliste
            seite_daten(self.t / "manifest.json", self.kat)
        doppelt = {**einstellungen.laden("seite"), "fassungen": [{"kennung": "A", "ordner": "vorstufe"},
                                                                  {"kennung": "A", "ordner": "x"}]}
        with self.assertRaises(SeiteFehler):
            seite_daten(self.t / "manifest.json", self.kat, werte=doppelt)
        with self.assertRaises(SeiteFehler):
            seite_daten(self.t / "manifest.json", self.kat, werte={**doppelt, "fassungen": []})
        with self.assertRaises(SeiteFehler):
            labels_als_rgb(np.array([[2 ** 24]], np.uint32))

    def test_einstellungen_und_befehl(self):
        # Reihenfolge der Umschalter = Reihenfolge der Liste; die Seite öffnet mit der ersten (A Alles frei)
        self.assertEqual([(f["kennung"], f["name"], f["ordner"]) for f in einstellungen.laden("seite")["fassungen"]],
                         [("A", "Alles frei", "a-alles-frei"), ("B", "Kategorien frei", "b-kategorien-frei"),
                          ("C", "Feste Kategorienliste", "c-feste-liste")])
        self.feste_liste()
        ziel = self.ordner / "aus" / "s.html"
        puffer = io.StringIO()
        with redirect_stdout(puffer):
            code = main(["seite", "--manifest", str(self.t / "manifest.json"), "--kategorien", str(self.kat.pfad),
                         "--ziel", str(ziel)])
        self.assertEqual(code, 0)
        self.assertTrue(ziel.exists())
        text = puffer.getvalue()
        self.assertIn("Fassung C (Feste Kategorienliste): r0c0 1 Segmente, pruefen ok; r0c1 1 Segmente, pruefen ok; "
                      "Nahtverstöße 1", text)
        self.assertIn("Fassung A (Alles frei): keine Daten", text)
        self.assertIn("Fassung B (Kategorien frei): keine Daten", text)
        self.assertEqual(main(["seite", "--manifest", str(self.t / "manifest.json"), "--ziel", str(self.ordner / "x.txt")]), 2)


if __name__ == "__main__":
    unittest.main()
