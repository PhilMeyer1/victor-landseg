"""Tests für ``einigung`` (finden, anwenden, messen) auf einer synthetischen 2 × 2-Karte.

Ausschnitt 80 × 80, Kern 40: r0c0 hat links der Viertelgrenze (x 20) Segment 1 (Laubwald), rechts Segment 2
(Wald); r0c1 ist ganz Segment 20 (Laubwald), r1c0 ganz Segment 10 (Wald, dazu 11 nur im Kontextrand), r1c1
Segment 30 (Gebäude) und im Luftbild heller (echte Bildkante an beiden Nähten zu r1c1). Ohne Bildkante und mit
verschiedener Klasse sind also: r0c0:1|r0c0:2 (Viertelgrenze), r0c0:1|r1c0:10 und r0c0:2|r0c1:20 (Nähte an der
Ecke); r0c0:2|r1c0:10 grenzt ohne Bildkante, hat aber dieselbe Klasse.
"""

import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

import numpy as np
import tifffile
from PIL import Image

from landseg import dateien, einstellungen, naht
from landseg.__main__ import main
from landseg.einigung import EinigungFehler, _im_kern, anwenden, fassung_laden, finden, messen, schluessel_karte, stellen
from landseg.kacheln import kacheln
from landseg.pruefen import pruefen
from tests.hilfe import beispiel_kategorien
from tests.test_kacheln import PRJ

OFFEN = {"r0c0:1|r0c0:2", "r0c0:1|r1c0:10", "r0c0:2|r0c1:20"}
KLASSEN = {1: "3.1", 2: "3", 20: "3.1", 10: "3", 11: "3", 30: "1.1"}


def _id(tk: str, gx: int, gy: int) -> int:
    if tk == "r0c0":
        return 1 if gx < 20 else 2
    if tk == "r1c0":
        return 11 if gy < 40 else 10
    return {"r0c1": 20, "r1c1": 30}[tk]


class EinigungTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ordner = Path(self.tmp.name)
        quelle = self.ordner / "quelle"
        quelle.mkdir()
        bild = np.full((100, 100, 3), 120, np.uint8)
        bild[40:, 40:] = 200  # r1c1 hell: echte Bildkante an beiden Nähten zu r1c1
        tifffile.imwrite(quelle / "blatt.tif", bild, photometric="rgb")
        (quelle / "blatt.TFW").write_text("0.2\n0\n0\n-0.2\n1000.1\n5000.9\n", encoding="ascii")
        (quelle / "blatt.PRJ").write_text(PRJ, encoding="ascii")
        self.t = self.ordner / "T"
        self.manifest = kacheln(quelle / "blatt.tif", 0, 0, 80, 80, self.t, kern=40, rand=8, name="TX")
        self.kat = beispiel_kategorien(self.ordner)
        self.fassung = self.t / "fassung"
        for t in self.manifest["teilkacheln"]:
            k = t["kontext"]
            gy, gx = np.mgrid[k["y"]:k["y"] + k["hoehe"], k["x"]:k["x"] + k["breite"]]
            karte = np.vectorize(lambda x, y: _id(t["id"], x, y), otypes=[np.uint32])(gx, gy)
            eintraege = []
            for sid in np.unique(karte).tolist():
                eintraege.append({"id": sid, "klasse": KLASSEN[sid], "grob": KLASSEN[sid].split(".")[0],
                                  "sicher": "ja", "im_kern": sid != 11,
                                  **({"urteil": "kontextrand"} if sid == 11 else {})})
            dateien.schreibe_labels(self.fassung / t["id"] / "labels.tif", karte)
            dateien.schreibe_json(self.fassung / t["id"] / "segmente.json",
                                  {"schema": "landseg-segmente/1", "segmente": eintraege, "verlauf": []})
        self.einst = einstellungen.laden("einigung")
        self.bild = naht.lese_bild(self.t / self.manifest["ausschnitt"]["bild"])

    def tearDown(self):
        self.tmp.cleanup()

    def laden(self, ordner=None):
        return fassung_laden(self.t / "manifest.json", ordner or self.fassung, self.kat, "X")

    def abgabe(self, urteile: dict, buendel="X-01", bearbeiter="einigung-X-01") -> dict:
        return {"schema": "landseg-einigung-abgabe/1", "fassung": "X", "buendel": buendel, "bearbeiter": bearbeiter,
                "paare": [{"paar": p, **u} for p, u in urteile.items()], "offen": [], "nicht_geprueft": []}

    def test_finden_naht_ecke_viertel_und_kante(self):
        f = self.laden()
        liste = {p["paar"]: p for p in stellen(f, self.bild, self.einst)}
        self.assertEqual({p for p, s in liste.items() if s["status"] == "offen"}, OFFEN)
        self.assertEqual(liste["r0c0:1|r0c0:2"]["art"], "viertel")
        self.assertEqual(liste["r0c0:1|r1c0:10"]["art"], "naht")
        self.assertIsNone(liste["r0c0:2|r1c0:10"]["status"])  # ohne Bildkante, gleiche Klasse
        self.assertFalse([p for p in liste if "r1c1" in p], "echte Bildkante zu r1c1 zählt nicht")
        self.assertEqual(liste["r0c0:1|r1c0:10"]["randpunkte"], 20)
        self.assertEqual(liste["r0c0:1|r0c0:2"]["randpunkte"], 40)

        erg = finden(f, self.bild, self.einst, self.ordner / "einigung")
        self.assertEqual(erg["zahlen"]["offen"]["paare"], 3)
        self.assertEqual(len(erg["buendel"]), 1)  # über gemeinsame Segmente verbunden: Ecke in einem Bündel
        auftrag = dateien.lese_json(self.ordner / "einigung" / "X-01" / "auftrag.json")
        self.assertEqual({p["paar"] for p in auftrag["paare"]}, OFFEN)
        self.assertEqual(len(auftrag["abgabe_muster"]["paare"]), 3)
        for p in auftrag["paare"]:
            with Image.open(self.ordner / "einigung" / "X-01" / p["bild"]) as jpg:
                self.assertLessEqual(max(jpg.size), 2000)
            self.assertEqual({s["teilkachel"] for s in p["segmente"]}, {s.split(":")[0] for s in p["paar"].split("|")})
        with self.assertRaises(EinigungFehler):
            finden(f, self.bild, self.einst, self.ordner / "einigung")  # Ordner schon belegt

    def test_zusammenhaengendes_bleibt_ganz(self):
        erg = finden(self.laden(), self.bild, {**self.einst, "buendel_paare": 1}, self.ordner / "e1")
        self.assertEqual([(b["paare"], b["uebergross"]) for b in erg["buendel"]], [(3, True)])

    def test_gleiche_bildkanten_regel_wie_naht(self):
        f = self.laden()
        karte, _ = schluessel_karte(f)
        befund = naht.pruefe_naehte((karte & 0xFFFFFFFF).astype(np.uint32), self.manifest, self.bild)
        von_naht = {tuple(sorted(v["ids"])) for v in befund.verstoesse}
        eigene = {tuple(sorted(int(s.split(":")[1]) for s in p["segmente"]))
                  for p in stellen(f, self.bild, self.einst) if p["art"] == "naht"}
        self.assertEqual(eigene, von_naht)

    def test_anwenden_gleich_unklar_und_messen(self):
        f = self.laden()
        finden(f, self.bild, self.einst, self.ordner / "einigung")
        vorher = messen(f, self.bild, self.einst)
        self.assertEqual((vorher["offen"]["paare"], vorher["unsicher"]["paare"], vorher["geklaert"]["paare"]), (3, 0, 0))
        abgabe = self.abgabe({
            "r0c0:1|r0c0:2": {"entscheidung": "gleich", "klasse": "3", "grund": "derselbe Wald"},
            "r0c0:1|r1c0:10": {"entscheidung": "gleich", "klasse": "3", "grund": "Wald läuft über die Naht"},
            "r0c0:2|r0c1:20": {"entscheidung": "unklar", "grund": "Schatten, Art nicht erkennbar"}})
        ziel = self.ordner / "geeinigt"
        erg = anwenden(f, [abgabe], self.ordner / "einigung", ziel=ziel)
        self.assertEqual((erg["gleich"], erg["unklar"], erg["klassen_gesetzt"]), (2, 1, 1))
        for t in self.manifest["teilkacheln"]:
            self.assertEqual((ziel / t["id"] / "labels.tif").read_bytes(),
                             (self.fassung / t["id"] / "labels.tif").read_bytes(), "Karte bildpunktgleich")
        self.assertEqual(dateien.lese_json(self.fassung / "r0c0" / "segmente.json")["verlauf"], [], "Quelle unberührt")
        neu = self.laden(ziel)
        r0c0 = dateien.segmente_nach_id(neu.segmente["r0c0"])
        self.assertEqual((r0c0[1]["klasse"], r0c0[1]["grob"]), ("3", "3"))
        self.assertEqual({e["entscheidung"] for e in r0c0[1]["einigung"]}, {"gleich"})
        self.assertEqual(r0c0[2]["sicher"], "nein")
        self.assertEqual(r0c0[2]["einigung"][-1]["grund"], "Schatten, Art nicht erkennbar")
        r0c1 = dateien.segmente_nach_id(neu.segmente["r0c1"])
        self.assertEqual((r0c1[20]["klasse"], r0c1[20]["sicher"]), ("3.1", "nein"))
        verlauf = neu.segmente["r0c0"]["verlauf"]
        self.assertIn(("klasse_setzen", "einigung-X-01"), {(e["op"], e["bearbeiter"]) for e in verlauf})
        self.assertTrue(all(e["bearbeiter"] == "einigung-X-01" for e in verlauf))
        self.assertEqual(dateien.segmente_nach_id(neu.segmente["r1c0"])[10]["klasse"], "3")
        for tk in neu.karten:
            self.assertTrue(pruefen(neu.karten[tk], neu.segmente[tk], self.kat).ok, tk)
        nachher = messen(neu, self.bild, self.einst)
        self.assertEqual((nachher["offen"]["paare"], nachher["unsicher"]["paare"], nachher["geklaert"]["paare"]), (0, 1, 2))

    def test_grenze_haelt_klassen_und_zaehlt_als_geklaert(self):
        f = self.laden()
        finden(f, self.bild, self.einst, self.ordner / "einigung")
        abgabe = self.abgabe({p: {"entscheidung": "grenze", "grund": "Waldrand ohne Farbsprung"} for p in OFFEN})
        erg = anwenden(f, [abgabe], self.ordner / "einigung")  # an Ort und Stelle
        self.assertEqual((erg["grenze"], erg["klassen_gesetzt"]), (3, 0))
        neu = self.laden()
        self.assertEqual(dateien.segmente_nach_id(neu.segmente["r0c0"])[1]["klasse"], "3.1")
        z = messen(neu, self.bild, self.einst)
        self.assertEqual((z["offen"]["paare"], z["geklaert"]["paare"]), (0, 3))

    def test_abgelehnte_abgaben_aendern_nichts(self):
        f = self.laden()
        finden(f, self.bild, self.einst, self.ordner / "einigung")
        gut = {"entscheidung": "grenze", "grund": "x"}
        faelle = {
            "Kette mit zwei Klassen": {"r0c0:1|r0c0:2": {"entscheidung": "gleich", "klasse": "3", "grund": "x"},
                                       "r0c0:1|r1c0:10": {"entscheidung": "gleich", "klasse": "3.1", "grund": "x"},
                                       "r0c0:2|r0c1:20": gut},
            "Paar fehlt": {"r0c0:1|r0c0:2": gut, "r0c0:1|r1c0:10": gut},
            "Klasse ungültig": {"r0c0:1|r0c0:2": {"entscheidung": "gleich", "klasse": "9.9", "grund": "x"},
                                "r0c0:1|r1c0:10": gut, "r0c0:2|r0c1:20": gut},
            "fremdes Paar": {**{p: gut for p in OFFEN}, "r0c0:2|r1c0:10": gut},
            "ohne Grund": {**{p: gut for p in OFFEN}, "r0c0:1|r0c0:2": {"entscheidung": "grenze", "grund": " "}},
            "Entscheidung unbekannt": {**{p: gut for p in OFFEN}, "r0c0:1|r0c0:2": {"entscheidung": "egal", "grund": "x"}},
        }
        vorher = (self.fassung / "r0c0" / "segmente.json").read_bytes()
        for name, urteile in faelle.items():
            with self.subTest(fall=name), self.assertRaises(EinigungFehler):
                anwenden(f, [self.abgabe(urteile)], self.ordner / "einigung")
        with self.assertRaises(EinigungFehler):
            anwenden(f, [self.abgabe({p: gut for p in OFFEN}, buendel="X-99")], self.ordner / "einigung")
        with self.assertRaises(EinigungFehler):
            anwenden(f, [self.abgabe({p: gut for p in OFFEN}, bearbeiter="")], self.ordner / "einigung")
        probe = anwenden(f, [self.abgabe({p: gut for p in OFFEN})], self.ordner / "einigung", schreiben=False)
        self.assertFalse(probe["geschrieben"])
        self.assertEqual((self.fassung / "r0c0" / "segmente.json").read_bytes(), vorher)

    def test_nur_kern(self):
        f = self.laden()
        self.assertFalse(_im_kern(f, "r1c0:11"))
        self.assertTrue(_im_kern(f, "r1c0:10"))

    def test_befehl(self):
        manifest = str(self.t / "manifest.json")
        with redirect_stdout(StringIO()), self.assertRaises(SystemExit) as ende:
            main(["einigung", "finden", "--help"])
        self.assertEqual(ende.exception.code, 0)
        aus = StringIO()
        with redirect_stdout(aus):
            code = main(["einigung", "finden", "--manifest", manifest, "--ordner", str(self.fassung), "--fassung", "X",
                         "--kategorien", str(self.kat.pfad), "--ziel", str(self.ordner / "einigung")])
        self.assertEqual(code, 0)
        self.assertIn("3 offene Stellen", aus.getvalue())
        abgabe = self.ordner / "einigung_abgabe.json"
        abgabe.write_text(json.dumps(self.abgabe({p: {"entscheidung": "unklar", "grund": "x"} for p in OFFEN})),
                          encoding="utf-8")
        basis = ["--manifest", manifest, "--ordner", str(self.fassung), "--fassung", "X", "--kategorien", str(self.kat.pfad)]
        with redirect_stdout(StringIO()):
            self.assertEqual(main(["einigung", "messen", *basis]), 1)  # offen
            self.assertEqual(main(["einigung", "anwenden", *basis, "--auftraege", str(self.ordner / "einigung"),
                                   "--abgabe", str(abgabe)]), 0)
            aus = StringIO()
            with redirect_stdout(aus):
                self.assertEqual(main(["einigung", "messen", *basis, "--json"]), 0)
        self.assertEqual(json.loads(aus.getvalue())[0]["unsicher"]["paare"], 3)
        abgabe.write_text(json.dumps(self.abgabe({})), encoding="utf-8")
        with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
            self.assertEqual(main(["einigung", "anwenden", *basis, "--auftraege", str(self.ordner / "einigung"),
                                   "--abgabe", str(abgabe)]), 1)
            self.assertEqual(main(["einigung", "finden", "--manifest", manifest, "--ziel", "x"]), 1)


if __name__ == "__main__":
    unittest.main()
