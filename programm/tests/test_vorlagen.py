"""W10: Auftragsvorlagen und Agent-Skill liegen vor, mit Platzhaltern und ohne Pfade dieses Rechners."""

import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
VORLAGEN = REPO / "vorlagen"
SKILL = REPO / ".claude" / "skills" / "landseg-agent" / "SKILL.md"
PLATZHALTER = re.compile(r"\{\{([A-Z_]+)\}\}")
ABSOLUT = re.compile(r"(?<![A-Za-z])[A-Za-z]:[\\/]|/Users/|/home/|\\Users\\")


class VorlagenTest(unittest.TestCase):
    def test_vorlagen_mit_platzhaltern_ohne_absolute_pfade(self):
        erklaert = set(PLATZHALTER.findall((VORLAGEN / "README.md").read_text(encoding="utf-8")))
        for name in ("urteil", "umsetzen", "korrektur", "naht", "einigung"):
            with self.subTest(vorlage=name):
                text = (VORLAGEN / f"{name}.md").read_text(encoding="utf-8")
                benutzt = set(PLATZHALTER.findall(text))
                self.assertIn("ERGEBNIS", benutzt)
                self.assertIn("landseg-agent", text)
                self.assertEqual(benutzt - erklaert, set(), "Platzhalter ohne Erklärung in vorlagen/README.md")
                self.assertIsNone(ABSOLUT.search(text), "absoluter Pfad in der Vorlage")
                self.assertNotIn("{{{", text)

    def test_skill_mit_kopf_und_regeln(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: landseg-agent\ndescription: "))
        self.assertIsNone(ABSOLUT.search(text))
        for regel in ("L1 Lückenlos", "L2 Nur im Kern", "L4 Kante aus dem Bild", "L6 Nahtregel", "L13 Einigung im Verbund"):
            self.assertIn(regel, text)


    def test_einigung_vorlage(self):
        text = (VORLAGEN / "einigung.md").read_text(encoding="utf-8")
        for pflicht in ("einigung_abgabe.json", "kategorien-a.json", "beide Seiten", "L13", "Kontextrand"):
            self.assertIn(pflicht, text)
        self.assertIn("`einigung.md`", (VORLAGEN / "README.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
