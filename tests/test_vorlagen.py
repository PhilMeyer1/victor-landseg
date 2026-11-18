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

    def test_agent_prompts_der_urteile(self):
        erklaert = set(PLATZHALTER.findall((VORLAGEN / "README.md").read_text(encoding="utf-8")))
        for name in ("agent-urteil-viertel", "agent-urteil-teilkachel"):
            with self.subTest(vorlage=name):
                text = (VORLAGEN / f"{name}.md").read_text(encoding="utf-8")
                self.assertEqual(set(PLATZHALTER.findall(text)) - erklaert, set())
                self.assertIsNone(ABSOLUT.search(text))
                self.assertIn("landseg-agent", text)
                for alt in ("nacheinander", "bist das du selbst"):
                    self.assertNotIn(alt, text)

    def test_vorlagen_von_vorbereiten(self):
        erklaert = set(PLATZHALTER.findall((VORLAGEN / "README.md").read_text(encoding="utf-8")))
        for name in ("urteil-viertel", "frei", "vereinheitlichen-urteil", "vereinheitlichen-frei", "abschnitte"):
            with self.subTest(vorlage=name):
                text = (VORLAGEN / f"{name}.md").read_text(encoding="utf-8")
                self.assertEqual(set(PLATZHALTER.findall(text)) - erklaert, set())
                self.assertIsNone(ABSOLUT.search(text))
                self.assertNotIn("{{{", text)

    def test_skill_mit_kopf_und_regeln(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: landseg-agent\ndescription: "))
        self.assertIsNone(ABSOLUT.search(text))
        for regel in ("L1 Lückenlos", "L2 Nur im Kern", "L4 Kante aus dem Bild", "L6 Nahtregel", "L13 Einigung im Verbund"):
            self.assertIn(regel, text)


    def test_fertige_befehle_als_standardweg(self):
        urteil = (VORLAGEN / "urteil.md").read_text(encoding="utf-8")
        einigung = (VORLAGEN / "einigung.md").read_text(encoding="utf-8")
        for befehl in ("-m landseg urteil bauen", "-m landseg zoom", "liste.json"):
            self.assertIn(befehl, urteil)
        for befehl in ("-m landseg einigung abgabe", "-m landseg zoom", "liste.json"):
            self.assertIn(befehl, einigung)
        for text in (urteil, einigung):
            self.assertIn("eigenes Skript", text)
            self.assertNotIn("Eigene Skripte als Datei in", text)
        self.assertIn("ein eigenes Skript nur, wenn kein Befehl den Fall deckt", SKILL.read_text(encoding="utf-8"))

    def test_garten_in_regeln_und_auftraegen(self):
        """L14: wann „Garten“ zu wählen ist; freie Listen führen Garten unter Dauergrünland."""
        skill = SKILL.read_text(encoding="utf-8")
        self.assertIn("L14 Garten", skill)
        for pflicht in ("3.6 Garten", "Haus- oder", "Hofgarten", "Gehölz", "Park, Friedhof und Sportanlage",
                        "im_siedlung: ja", "„Dauergrünland“", "pruefen --frei"):
            self.assertIn(pflicht, skill)
        for name in ("urteil", "einigung", "naht", "korrektur", "umsetzen", "abschnitte"):
            with self.subTest(vorlage=name):
                text = (VORLAGEN / f"{name}.md").read_text(encoding="utf-8")
                self.assertIn("L14", text)
                self.assertIn("Garten", text)
        for name in ("frei", "vereinheitlichen-frei", "vereinheitlichen-urteil", "einigung", "abschnitte"):
            with self.subTest(freie_liste=name):
                text = (VORLAGEN / f"{name}.md").read_text(encoding="utf-8")
                self.assertIn("„Garten“", text)
                self.assertIn("„Dauergrünland“", text)
        self.assertIn("--frei", (VORLAGEN / "frei.md").read_text(encoding="utf-8"))
        einigung = (VORLAGEN / "einigung.md").read_text(encoding="utf-8")
        for liste in ("kategorien-a.json", "kategorien-b.json"):
            self.assertIn(liste, einigung)

    def test_einigung_vorlage(self):
        text = (VORLAGEN / "einigung.md").read_text(encoding="utf-8")
        for pflicht in ("einigung_abgabe.json", "kategorien-a.json", "beide Seiten", "L13", "Kontextrand"):
            self.assertIn(pflicht, text)
        self.assertIn("`einigung.md`", (VORLAGEN / "README.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
