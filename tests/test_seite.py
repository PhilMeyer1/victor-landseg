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

from landseg import dateien, einigung, einstellungen, naht
from landseg.__main__ import main
from landseg.kacheln import kacheln
from landseg.seite import SeiteFehler, bilder_aus_einstellungen, labels_als_rgb, lage_in_worten, seite, seite_daten
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
        d = daten_aus_html(html)["bilder"][0]
        self.assertEqual((d["kennung"], d["titel"], d["vorhanden"]), ("TX", "Ausschnitt TX", True))
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
        self.assertEqual([(f["kennung"], f["vorhanden"], f.get("naht")) for f in erg["bilder"][0]["fassungen"]],
                         [("A", False, None), ("B", True, 0), ("C", True, 1)])

    def test_kachel_wahl(self):
        """Kachel-Wahl: Nummer und Lage je Teilkachel in den Daten; Wahl, Hinweis im Bild und Pfeiltasten in der Seite."""
        self.feste_liste()
        ziel = self.t / "seite" / "TX.html"
        seite(self.t / "manifest.json", ziel, self.kat)
        html = ziel.read_text(encoding="utf-8")
        d = daten_aus_html(html)["bilder"][0]
        self.assertEqual([(t["id"], t["nummer"], t["lage"]) for t in d["teilkacheln"]],
                         [("r0c0", 1, "links"), ("r0c1", 2, "rechts")])
        self.assertEqual([lage_in_worten(z, s, 2, 2) for z in (0, 1) for s in (0, 1)],
                         ["oben links", "oben rechts", "unten links", "unten rechts"])
        self.assertEqual(lage_in_worten(1, 1, 3, 3), "Mitte")
        self.assertEqual(lage_in_worten(0, 3, 2, 4), "Zeile 1, Spalte 4")
        for teil in ("c-kachelwahl", "Ganzer Ausschnitt", "'vorige'", "'nächste'", "' von ' + ANZAHL", "c-fortschritt",
                     "weiter: Teilkachel ", "ArrowLeft", "ArrowRight", "t === 'TEXTAREA' || t === 'INPUT'",
                     "--wahl-hoehe", "@media (max-width: 760px)"):
            self.assertIn(teil, html)
        # Miniaturen entstehen im Browser aus denselben Bildern: keine zweite Kopie in der Datei
        self.assertEqual(html.count(d["teilkacheln"][0]["bild"]), 1)

    def historisch(self, name: str = "HX") -> Path:
        """Zweites Bild wie ein Scan: Graustufen, ohne Weltdatei und GeoTIFF-Tags, mit Fassung C."""
        tif = self.ordner / "quelle" / "scan.tif"
        grau = np.tile(np.linspace(20, 230, 100).astype(np.uint8), (60, 1))
        tifffile.imwrite(tif, grau, photometric="minisblack")
        h = self.ordner / "H"
        manifest = kacheln(tif, 10, 10, 80, 40, h, kern=40, rand=8, name=name)
        for t in manifest["teilkacheln"]:
            k = t["kontext"]
            ziel = h / "c-feste-liste" / t["id"]
            ziel.mkdir(parents=True)
            dateien.schreibe_labels(ziel / "labels.tif", np.full((k["hoehe"], k["breite"]), 5, np.uint32))
            dateien.schreibe_json(ziel / "segmente.json", {"schema": "landseg-segmente/1", "segmente": [
                {"id": 5, "klasse": "1.1", "grob": "1", "sicher": "ja"}]})
        return h

    def test_mehrere_bilder_in_einer_seite(self):
        """Zwei Bilder mit Daten und eines ohne Manifest in einer Datei; jedes mit eigenen Fassungen und Zahlen."""
        self.feste_liste()
        self.fassung_b()
        h = self.historisch()
        werte = {**einstellungen.laden("seite"), "bilder": [
            {"kennung": "T", "name": "Orthofoto", "beschreibung": "Farbe", "manifest": "T/manifest.json"},
            {"kennung": "H", "name": "Scan", "manifest": "H/manifest.json"},
            {"kennung": "X", "name": "fehlt", "manifest": "X/manifest.json"}]}
        bilder = bilder_aus_einstellungen(self.ordner, werte)
        ziel = self.ordner / "seite.html"
        erg = seite(bilder, ziel, self.kat, werte=werte)
        html = ziel.read_text(encoding="utf-8")
        self.assertIn("<title>Übersicht TX, HX</title>", html)
        d = daten_aus_html(html)
        self.assertEqual(d["schema"], "landseg-seite/3")
        self.assertNotIn("bilder", d["einstellungen"])
        t, hb, x = d["bilder"]
        self.assertEqual([(b["kennung"], b["titel"], b["vorhanden"]) for b in d["bilder"]],
                         [("T", "Orthofoto", True), ("H", "Scan", True), ("X", "fehlt", False)])
        self.assertIn("X/manifest.json fehlt", x["grund"])
        self.assertEqual(t["beschreibung"], "Farbe")
        self.assertEqual([f["vorhanden"] for f in t["fassungen"]], [False, True, True])
        self.assertEqual([f["vorhanden"] for f in hb["fassungen"]], [False, False, True])
        # ohne Lage: kein transform, keine Weltdatei; Graustufen bleiben Graustufen
        m = dateien.lese_json(h / "manifest.json")
        self.assertIsNone(m["georeferenz"])
        self.assertEqual(m["quelle"]["kanaele"], 1)
        self.assertEqual(list(h.rglob("*.pgw")), [])
        for uri in [hb["ausschnitt"]["bild"]] + [tk["bild"] for tk in hb["teilkacheln"]]:
            self.assertEqual(Image.open(io.BytesIO(base64.b64decode(uri.split(",", 1)[1]))).mode, "L")
        # Nähte-Zahlen und Einigung je Bild aus dessen eigenen Daten: ein Segment je Teilkachel, gleiche Klasse
        c = hb["fassungen"][2]
        self.assertIsNotNone(c["naht"])
        self.assertEqual(c["einigung"]["stellen"], 0)
        self.assertEqual(t["fassungen"][2]["einigung"]["stellen"], 1)
        self.assertTrue((ids_aus_png(c["gesamt"]) == 5).all())
        self.assertEqual([(b["kennung"], b["vorhanden"], [f["vorhanden"] for f in b["fassungen"]])
                          for b in erg["bilder"]], [("T", True, [False, True, True]), ("H", True, [False, False, True]),
                                                    ("X", False, [])])
        for teil in ("data-bild", "c-bilder", "bildWahl(D.kennung)", "'#/' + ERSTES", "AKTUELL.taste(ev)"):
            self.assertIn(teil, html)

    def test_t0_unveraendert_neben_zweitem_bild(self):
        """Die Daten eines Bildes sind dieselben, ob es allein oder neben einem zweiten Bild auf der Seite steht."""
        self.feste_liste()
        self.historisch()
        allein = seite_daten(self.t / "manifest.json", self.kat)["bilder"][0]
        beide = seite_daten([{"kennung": "TX", "name": "Ausschnitt TX", "manifest": self.t / "manifest.json"},
                             {"kennung": "H", "manifest": self.ordner / "H" / "manifest.json"}], self.kat)
        self.assertEqual(json.dumps(beide["bilder"][0], sort_keys=True), json.dumps(allein, sort_keys=True))
        self.assertEqual(beide["bilder"][1]["titel"], "H")

    def test_bild_ohne_daten_und_eigene_ordner(self):
        h = self.historisch()
        (h / "c-feste-liste").rename(h / "c-scan")
        bilder = [{"kennung": "T", "manifest": self.t / "manifest.json"},
                  {"kennung": "H", "manifest": h / "manifest.json", "ordner": {"C": "c-scan"}}]
        d = seite_daten(bilder, self.kat)
        self.assertEqual([b["vorhanden"] for b in d["bilder"]], [False, True])
        self.assertIn("keine Fassung mit Daten", d["bilder"][0]["grund"])
        self.assertTrue(d["bilder"][1]["fassungen"][2]["vorhanden"])
        self.assertTrue(d["bilder"][1]["fassungen"][2]["quelle"].endswith("H/c-scan"))
        bilder[1]["ordner"] = {}
        with self.assertRaises(SeiteFehler):  # kein Bild mit Daten
            seite_daten(bilder, self.kat)
        with self.assertRaises(SeiteFehler):
            seite_daten([bilder[0], {**bilder[1], "kennung": "T"}], self.kat)
        with self.assertRaises(SeiteFehler):
            bilder_aus_einstellungen(self.ordner, {"bilder": [{"kennung": "H"}]})

    def test_kommentare_je_bild(self):
        self.feste_liste()
        self.historisch()
        k_h = self.ordner / "k-h.json"
        k_h.write_text(json.dumps({"bild": "H", "ausschnitt": "HX", "kommentare": [
            {"nr": 1, "fassung": "C", "teilkachel": "r0c0", "segment": 5, "text": "Scan"}]}), encoding="utf-8")
        k_t = self.ordner / "k-t.json"
        k_t.write_text(json.dumps({"ausschnitt": "TX", "kommentare": [
            {"nr": 1, "fassung": "C", "teilkachel": "r0c0", "segment": 1001, "text": "Ortho"}]}), encoding="utf-8")
        bilder = [{"kennung": "T", "manifest": self.t / "manifest.json"},
                  {"kennung": "H", "manifest": self.ordner / "H" / "manifest.json"}]
        d = seite_daten(bilder, self.kat, kommentare=[k_h, k_t])
        self.assertEqual([[k["text"] for k in b["kommentare"]] for b in d["bilder"]], [["Ortho"], ["Scan"]])
        ohne = self.ordner / "k.json"
        ohne.write_text(json.dumps({"kommentare": []}), encoding="utf-8")
        with self.assertRaises(SeiteFehler):  # mehrere Bilder: Zuordnung aus dem Export nötig
            seite_daten(bilder, self.kat, kommentare=ohne)
        self.assertEqual(seite_daten(self.t / "manifest.json", self.kat, kommentare=ohne)["bilder"][0]["kommentare"], [])

    def test_befehl_mit_daten(self):
        self.feste_liste()
        self.historisch()
        werte = self.ordner / "werte.json"
        werte.write_text(json.dumps({"bilder": [{"kennung": "T", "name": "Orthofoto", "manifest": "T/manifest.json"},
                                                {"kennung": "H", "name": "Scan", "manifest": "H/manifest.json"}]}),
                         encoding="utf-8")
        ziel = self.ordner / "aus" / "beide.html"
        puffer = io.StringIO()
        with redirect_stdout(puffer):
            code = main(["seite", "--daten", str(self.ordner), "--einstellungen", str(werte), "--ziel", str(ziel)])
        self.assertEqual(code, 0)
        self.assertIn("Bild H (Scan):", puffer.getvalue())
        self.assertEqual([b["kennung"] for b in daten_aus_html(ziel.read_text(encoding="utf-8"))["bilder"]], ["T", "H"])
        self.assertEqual([b["kennung"] for b in einstellungen.laden("seite")["bilder"]], ["T0", "H0"])

    def test_luecke(self):
        self.feste_liste(luecke=True)
        d = seite_daten(self.t / "manifest.json", self.kat)
        befund = d["bilder"][0]["fassungen"][2]["teilkacheln"]["r0c0"]["pruefen"]
        self.assertFalse(befund["ok"])
        self.assertEqual(befund["ohne_segment"], 4)

    def test_zwei_zahlen_und_gemeinsamer_bildleser(self):
        """Schnittlinien ohne Bildkante wie ``naht``, gleiche Fläche mit verschiedener Klasse wie ``einigung messen``
        (davon unsicher belegt); das Luftbild liest die Seite mit ``naht.lese_bild`` (Altlast A2)."""
        # schwacher Farbsprung genau auf der Kerngrenze (10 je Kanal, Abstand 17 < Schwelle 25): keine echte Bildkante;
        # als uint8 gelesen liefe die Differenz 110 - 120 über und gälte als Kante
        quelle = self.ordner / "quelle" / "blatt.tif"
        feld = np.full((60, 100, 3), 120, np.uint8)
        feld[:, 40:] = 110
        tifffile.imwrite(quelle, feld, photometric="rgb")
        self.t = self.ordner / "T2"
        self.manifest = kacheln(quelle, 0, 0, 80, 40, self.t, kern=40, rand=8, name="TX")
        self.assertEqual(self.manifest["teilkacheln"][1]["kern"]["x"], 40)
        self.feste_liste()
        rechts = self.t / "c-feste-liste" / "r0c1" / "segmente.json"
        daten = dateien.lese_segmente(rechts)
        daten["segmente"][0]["einigung"] = [{"paar": "r0c0:1001|r0c1:2001", "mit": "r0c0:1001",
                                             "entscheidung": "unklar", "grund": "Schatten, Klasse nicht erkennbar"}]
        dateien.schreibe_json(rechts, daten)
        manifest_pfad = self.t / "manifest.json"
        d = seite_daten(manifest_pfad, self.kat)
        c = d["bilder"][0]["fassungen"][2]
        bild = naht.lese_bild(self.t / self.manifest["ausschnitt"]["bild"])
        karte = np.where(np.arange(80)[None, :] < 40, 1001, 2001).astype(np.uint32).repeat(40, axis=0)
        self.assertEqual(len(c["naht"]["verstoesse"]), len(naht.pruefe_naehte(karte, self.manifest, bild).verstoesse))
        self.assertEqual(len(c["naht"]["verstoesse"]), 1)
        uint8 = np.asarray(Image.open(self.t / self.manifest["ausschnitt"]["bild"]).convert("RGB"))
        self.assertEqual(naht.pruefe_naehte(karte, self.manifest, uint8).verstoesse, [])  # der alte Leser übersah sie
        # neue Zahl: dieselben Zahlen wie ``einigung messen``
        f = einigung.fassung_aus_einstellungen(manifest_pfad, "C", self.kat, einstellungen.laden("seite")["fassungen"])
        gemessen = einigung.messen(f, bild, einstellungen.laden("einigung"))
        for status in ("offen", "unsicher", "geklaert"):
            self.assertEqual(c["einigung"][status], gemessen[status])
        self.assertEqual((c["einigung"]["stellen"], c["einigung"]["unsicher"]["paare"]), (1, 1))
        for tk in ("r0c0", "r0c1"):
            self.assertEqual(c["teilkacheln"][tk]["einigung"]["stellen"], 1)
        self.assertIsNone(c["einigung_fehler"])
        # B: ein Segment über die Naht, also keine Stelle
        self.fassung_b()
        ziel = self.t / "seite" / "TX.html"
        erg = seite(manifest_pfad, ziel, self.kat)
        self.assertEqual([(f["kennung"], f.get("naht"), f.get("einigung")) for f in erg["bilder"][0]["fassungen"]],
                         [("A", None, None), ("B", 0, {"stellen": 0, "unsicher": 0}),
                          ("C", 1, {"stellen": 1, "unsicher": 1})])
        html = ziel.read_text(encoding="utf-8")
        for teil in ("Stellen, an denen gleiche Flächen verschiedene Klassen haben", "unsicher belegt",
                     "an Nähten ohne Bildkante", "einigungText(FA.f.einigung, FA.f.einigung_fehler)",
                     "einigungText(st.roh.einigung"):
            self.assertIn(teil, html)
        self.assertNotIn("Stellen an Nähten passen nicht", html)
        # Graustufenbild: ein Kanal aus naht.lese_bild, eingebettet als PNG
        grau = self.ordner / "grau.tif"
        tifffile.imwrite(grau, np.full((60, 100), 90, np.uint8))
        self.t = self.ordner / "T3"
        self.manifest = kacheln(grau, 0, 0, 80, 40, self.t, kern=40, rand=8, name="TX")
        self.feste_liste()
        g = seite_daten(self.t / "manifest.json", self.kat)["bilder"][0]
        self.assertEqual(g["fassungen"][2]["einigung"]["stellen"], 1)
        png = Image.open(io.BytesIO(base64.b64decode(g["ausschnitt"]["bild"].split(",", 1)[1])))
        self.assertEqual((png.size, int(np.asarray(png.convert("L")).max())), ((80, 40), 90))

    def test_fehlende_teilkachel_naht_nicht_geprueft(self):
        self.feste_liste()
        (self.t / "c-feste-liste" / "r0c1" / "labels.tif").unlink()
        a = seite_daten(self.t / "manifest.json", self.kat)["bilder"][0]["fassungen"][2]
        self.assertIsNone(a["teilkacheln"]["r0c1"])
        self.assertIsNone(a["naht"])
        self.assertIsNone(a["einigung"])
        self.assertIsNone(a["gesamt"])

    def test_nur_freie_fassung_und_eigene_fassungsliste(self):
        b = self.fassung_b()
        werte = {**einstellungen.laden("seite"), "fassungen": [
            {"kennung": "A", "name": "fest", "ordner": "vorstufe"},
            {"kennung": "P", "name": "Probe", "beschreibung": "nur Probe", "ordner": str(b), "kategorien": "kategorien-b.json"}]}
        d = seite_daten(self.t / "manifest.json", self.kat, werte=werte)
        self.assertEqual([(f["kennung"], f["vorhanden"]) for f in d["bilder"][0]["fassungen"]], [("A", False), ("P", True)])
        self.assertEqual(d["bilder"][0]["fassungen"][1]["beschreibung"], "nur Probe")

    def test_einbettung_sicher(self):
        self.feste_liste()
        kommentare = self.ordner / "k.json"
        kommentare.write_text(json.dumps({"kommentare": [{"nr": 1, "fassung": "C", "teilkachel": "r0c0", "segment": 1001,
                                                          "text": "</script><b>x</b>"}]}), encoding="utf-8")
        ziel = self.ordner / "s.html"
        seite(self.t / "manifest.json", ziel, self.kat, kommentare=kommentare)
        html = ziel.read_text(encoding="utf-8")
        self.assertEqual(html.count("</script>"), 2)
        self.assertEqual(daten_aus_html(html)["bilder"][0]["kommentare"][0]["text"], "</script><b>x</b>")

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
                      "Schnittlinien ohne Bildkante 1; gleiche Fläche, verschiedene Klasse 1 "
                      "(davon 0 unsicher belegt)", text)
        self.assertIn("Fassung A (Alles frei): keine Daten", text)
        self.assertIn("Fassung B (Kategorien frei): keine Daten", text)
        self.assertEqual(main(["seite", "--manifest", str(self.t / "manifest.json"), "--ziel", str(self.ordner / "x.txt")]), 2)


if __name__ == "__main__":
    unittest.main()
