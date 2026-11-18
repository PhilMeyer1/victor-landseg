import hashlib
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from landseg.__main__ import main
from landseg.messung import agents_lesen, messung, messung_befehl, preis, tabelle


def _zeile(typ: str, zeit: str, **message) -> str:
    return json.dumps({"type": typ, "timestamp": f"2026-11-18T{zeit}Z", "uuid": f"u-{zeit}-{typ}",
                       "message": message})


def _usage(eingabe=0, schreiben=0, schreiben_1h=0, lesen=0, ausgabe=0) -> dict:
    return {"input_tokens": eingabe, "cache_creation_input_tokens": schreiben,
            "cache_read_input_tokens": lesen, "output_tokens": ausgabe,
            "cache_creation": {"ephemeral_1h_input_tokens": schreiben_1h,
                               "ephemeral_5m_input_tokens": schreiben - schreiben_1h}}


def beispiel_lauf(ordner: Path) -> Path:
    """Drei Agents, von Hand nachgerechnet (Preise je Mio.: Opus 4/5/8/0,20/20, Sonnet die Hälfte).

    a1 (Urteile, opus): Antwort m1 steht zweimal im Transkript (Text + Read eines Bildes) und zählt
    einmal: 10 000 Eingabe, 1 000 000 Cache-Schreiben (400 000 davon 1 h), 2 000 000 Cache-Lesen,
    50 000 Ausgabe; Antwort m2 (Write einer .py): 3 000 000 Cache-Lesen, 100 000 Ausgabe; eine kaputte
    Zeile. USD = (10 000·4 + 600 000·5 + 400 000·8 + 5 000 000·0,20 + 150 000·20) / 1e6 = 10,24.
    a2 (Einigung, sonnet): 200 000 Cache-Schreiben 5 min, 1 000 000 Cache-Lesen, 10 000 Ausgabe;
    USD = (200 000·2,5 + 1 000 000·0,10 + 10 000·10) / 1e6 = 0,70.
    a3 (ohne meta.json, Modell aus der Antwort): 100 000 Cache-Lesen bei Opus = 0,02 USD.
    """
    ordner.mkdir(parents=True, exist_ok=True)
    u1 = _usage(eingabe=10_000, schreiben=1_000_000, schreiben_1h=400_000, lesen=2_000_000, ausgabe=50_000)
    a1 = [
        _zeile("user", "10:00:00", role="user", content="Auftrag"),
        _zeile("assistant", "10:00:30", id="m1", model="claude-opus-5-5", usage=u1,
               content=[{"type": "text", "text": "ich sehe nach"}]),
        _zeile("assistant", "10:00:31", id="m1", model="claude-opus-5-5", usage=u1,
               content=[{"type": "tool_use", "id": "t1", "name": "Read", "input": {"file_path": "C:/x/Bild.PNG"}}]),
        "{kaputt",
        _zeile("user", "10:01:00", role="user", content=[{"type": "tool_result", "tool_use_id": "t1"}]),
        _zeile("assistant", "10:03:00", id="m2", model="claude-opus-5-5", usage=_usage(lesen=3_000_000, ausgabe=100_000),
               content=[{"type": "tool_use", "id": "t2", "name": "Write",
                         "input": {"file_path": "C:/x/abgabe_bauen.py", "content": "print(1)"}}]),
    ]
    a2 = [_zeile("assistant", "10:01:00", id="n1", model="claude-sonnet-5-5",
                 usage=_usage(schreiben=200_000, lesen=1_000_000, ausgabe=10_000), content=[]),
          _zeile("user", "10:05:00", role="user", content="ende")]
    a3 = [_zeile("assistant", "10:02:00", id="k1", model="claude-opus-5-5", usage=_usage(lesen=100_000), content=[])]
    for name, zeilen in (("a1", a1), ("a2", a2), ("a3", a3)):
        (ordner / f"agent-{name}.jsonl").write_text("\n".join(zeilen) + "\n", encoding="utf-8")
    (ordner / "agent-a1.meta.json").write_text(json.dumps({"workflowPhase": "Urteile", "model": "opus",
                                                           "description": "urteil:a:r0c0"}), encoding="utf-8")
    (ordner / "agent-a2.meta.json").write_text(json.dumps({"workflowPhase": "Einigung", "model": "sonnet"}),
                                               encoding="utf-8")
    (ordner / "journal.jsonl").write_text("{}\n", encoding="utf-8")
    return ordner


def _hashes(ordner: Path) -> dict:
    return {p.name: (hashlib.sha256(p.read_bytes()).hexdigest(), p.stat().st_mtime_ns) for p in ordner.iterdir()}


class MessungTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.lauf = beispiel_lauf(self.tmp / "wf_test")

    def tearDown(self):
        self._tmp.cleanup()

    def test_zahlen_von_hand(self):
        m = messung_befehl(self.lauf)
        self.assertEqual(list(m["phasen"]), ["Urteile", "Einigung", "?"])     # nach erstem Start
        u = m["phasen"]["Urteile"]
        self.assertEqual((u["agents"], u["runden"], u["gelesen"], u["neu"], u["ausgabe"]),
                         (1, 2, 5_000_000, 1_010_000, 150_000))
        self.assertAlmostEqual(u["usd"], 10.24, places=2)
        self.assertEqual((u["bilder"], u["py_geschrieben"], u["wand_min"], u["agent_min"]), (1, 1, 3.0, 3.0))
        self.assertEqual(u["modell"], "opus")
        e = m["phasen"]["Einigung"]
        self.assertEqual((e["runden"], e["gelesen"], e["neu"], e["ausgabe"]), (1, 1_000_000, 200_000, 10_000))
        self.assertAlmostEqual(e["usd"], 0.70, places=2)
        z = m["zusammen"]
        self.assertEqual((z["agents"], z["runden"], z["gelesen"], z["neu"], z["ausgabe"]),
                         (3, 4, 6_100_000, 1_210_000, 160_000))
        self.assertAlmostEqual(z["usd"], 10.96, places=2)
        self.assertEqual((z["wand_min"], z["agent_min"], z["bilder"], z["py_geschrieben"]), (5.0, 7.0, 1, 1))
        self.assertEqual(m["lauf"], "wf_test")

    def test_ohne_meta_und_kaputte_zeilen(self):
        m = messung_befehl(self.lauf)
        ohne = m["phasen"]["?"]
        self.assertEqual((ohne["agents"], ohne["runden"], ohne["gelesen"]), (1, 1, 100_000))
        self.assertAlmostEqual(ohne["usd"], 0.02, places=2)
        (self.lauf / "agent-leer.jsonl").write_text("nicht json\n\n[1, 2]\n", encoding="utf-8")
        m = messung_befehl(self.lauf)
        self.assertEqual(m["phasen"]["?"]["agents"], 2)
        self.assertEqual(m["zusammen"]["runden"], 4)

    def test_preise(self):
        self.assertEqual(preis("claude-opus-5-5", 0), (4.0, 5.0, 8.0, 0.20, 20.0))
        self.assertEqual(preis("sonnet", 0), (2.0, 2.5, 4.0, 0.10, 10.0))
        self.assertEqual(preis("claude-haiku-4-5", 200_000)[0], 0.50)
        self.assertIsNone(preis("<synthetic>", 0))

    def test_dateien_und_transkripte_unberuehrt(self):
        vorher = _hashes(self.lauf)
        ziel = self.tmp / "bericht"
        m = messung_befehl(self.lauf, lauf="H0 test", ziel=ziel)
        self.assertEqual(_hashes(self.lauf), vorher)
        daten = json.loads((ziel / "messung.json").read_text(encoding="utf-8"))
        self.assertEqual(daten["form"], "landseg-messung/1")
        self.assertEqual(daten["lauf"], "H0_test")
        self.assertEqual(daten["zusammen"]["agents"], 3)
        self.assertEqual(len(daten["agents"]), 3)
        md = (ziel / "messung.md").read_text(encoding="utf-8")
        self.assertEqual(md, tabelle(m))
        self.assertIn("keine Abo-Kosten", md)
        self.assertIn("| zusammen |  | 3 | 5,0 | 7,0 | 4 | 6,10 | 1,21 | 0,160 | 10,96 | 1 | 1 |", md)
        with self.assertRaises(ValueError):
            messung_befehl(self.lauf, ziel=self.lauf)

    def test_urteile_je_fassung(self):
        m = messung(agents_lesen(self.lauf), "probe")
        a1 = next(a for a in m["agents"] if a["agent"] == "a1")
        self.assertEqual(list(m["urteile_je_fassung"]), ["A"])
        fa = m["urteile_je_fassung"]["A"]
        self.assertEqual((fa["agents"], fa["gelesen"], fa["gelesen_je_agent"]), (1, a1["gelesen"], a1["gelesen"]))
        self.assertIn("Urteils-Agents je Fassung", tabelle(m))

    def test_befehlszeile(self):
        aus = io.StringIO()
        with redirect_stdout(aus):
            code = main(["messung", "--transkripte", str(self.lauf), "--lauf", "probe", "--ziel", str(self.tmp / "z")])
        self.assertEqual(code, 0)
        self.assertIn("# Messung probe", aus.getvalue())
        self.assertTrue((self.tmp / "z" / "messung.md").is_file())
        fehler = io.StringIO()
        with redirect_stderr(fehler), redirect_stdout(io.StringIO()):
            code = main(["messung", "--transkripte", str(self.tmp / "fehlt")])
        self.assertEqual(code, 2)
        self.assertIn("Protokollordner fehlt", fehler.getvalue())


if __name__ == "__main__":
    unittest.main()
