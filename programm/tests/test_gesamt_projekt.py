import hashlib
import importlib.util
import io
import os
import re
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

REPO = Path(__file__).resolve().parent.parent
GIT_UMGEBUNG = {"GIT_AUTHOR_NAME": "Test", "GIT_AUTHOR_EMAIL": "test@beispiel.invalid",
                "GIT_COMMITTER_NAME": "Test", "GIT_COMMITTER_EMAIL": "test@beispiel.invalid"}


def werkzeug():
    spec = importlib.util.spec_from_file_location("gesamt_projekt", REPO / "tools" / "gesamt_projekt.py")
    modul = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modul)
    return modul


GP = werkzeug()


def git(ordner, *argumente):
    return subprocess.run(["git", "-C", str(ordner), "-c", "core.autocrlf=false", *argumente],
                          check=True, capture_output=True, text=True).stdout


def repo(ordner: Path, dateien: dict[str, bytes], nachricht="init") -> Path:
    ordner.mkdir(parents=True, exist_ok=True)
    git(ordner, "init", "-q", "-b", "main")
    for rel, daten in dateien.items():
        (ordner / rel).parent.mkdir(parents=True, exist_ok=True)
        (ordner / rel).write_bytes(daten)
    git(ordner, "add", "-A")
    git(ordner, "commit", "-q", "-m", nachricht)
    return ordner


def schreibe(pfad: Path, daten: bytes):
    pfad.parent.mkdir(parents=True, exist_ok=True)
    pfad.write_bytes(daten)


def ausfuehren(*argv) -> tuple[int, str]:
    puffer = io.StringIO()
    with redirect_stdout(puffer):
        code = GP.main(list(argv))
    return code, puffer.getvalue()


@mock.patch.dict(os.environ, GIT_UMGEBUNG)
class GesamtProjektTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.ort = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def basis(self) -> Path:
        basis = self.ort / "Victor"
        repo(basis / "landseg", {"README.md": b"landseg\n", "landseg/__init__.py": b""})
        repo(basis / "unterlagen", {"README.md": b"unterlagen\r\n", ".gitattributes": b"berichte/** -text\n"})
        schreibe(basis / "wuensche/2026-01-01-a.md", b"# Wunsch\r\nZeile mit CRLF\r\n")
        schreibe(basis / "wuensche/2026-01-01-a/bericht-landseg.md", b"Bericht\n")
        schreibe(basis / "wuensche/2026-01-01-a/roh/lauf.txt", b"roh\n")
        schreibe(basis / "wuensche/2026-01-01-a/einreihen-landseg.json", b"{}\n")
        schreibe(basis / "wuensche/.stand.json", b"{}\n")
        schreibe(basis / "daten/landseg/T0/kern500/a.bin", bytes(range(256)))
        schreibe(basis / "daten/README.md", ("# Daten\n\n## luftbilder/\n\n| Datei | Größe (Bytes) | SHA-256 |\n"
                 "|---|---:|---|\n| `x/bild.tif` | 3 | `" + hashlib.sha256(b"abc").hexdigest() + "` |\n\n"
                 "## anderes\n").encode("utf-8"))
        alt = repo(basis / "daten/landseg/uebergabe/landseg-t0",
                   {"T0/manifest.json": b"{}\n", "landseg/__init__.py": b"alt\n", "README.md": b"alt\n",
                    "ANLEITUNG.md": b"alt\n", ".gitignore": b"*.pyc\n", "kategorien.json": b"{}\n"})
        git(alt, "remote", "add", "origin", "https://beispiel.invalid/landseg-t0.git")
        return basis

    def klartext_in_neuen_commits(self, ziel: Path, bereich: str):
        shas = git(ziel, "rev-list", "--first-parent", bereich).split()
        self.assertTrue(shas, bereich)
        for sha in shas:
            text = git(ziel, "log", "-1", "--format=%B", sha)
            titel = re.findall(r"^Klartext-Titel: (.+)$", text, re.M)
            klartext = re.findall(r"^Klartext: (.+)$", text, re.M)
            self.assertEqual((len(titel), len(klartext)), (1, 1), text)
            self.assertLessEqual(len(titel[0]), 80, text)
            self.assertLessEqual(len(klartext[0]), 250, text)

    def test_bauen_ist_wiederholbar_und_bringt_neue_commits_mit_verlauf(self):
        basis, ziel = self.basis(), self.ort / "gesamt" / "victor-landseg"
        alt = git(basis / "daten/landseg/uebergabe/landseg-t0", "rev-parse", "HEAD").strip()
        code, text = ausfuehren("bauen", "--basis", str(basis), "--ziel", str(ziel))
        self.assertEqual(code, 0, text)
        self.assertEqual(git(ziel, "config", "core.autocrlf").strip(), "false")
        self.assertEqual(git(ziel, "remote", "get-url", "origin").strip(), "https://beispiel.invalid/landseg-t0.git")
        self.assertEqual(git(ziel, "cat-file", "-t", alt).strip(), "commit")
        for pfad in ("README.md", "ANLEITUNG.md", "programm/landseg/__init__.py", "unterlagen/README.md",
                     "ergebnisse/manifest.json", "daten/landseg/T0/kern500/a.bin", "daten/luftbilder/README.md"):
            self.assertTrue((ziel / pfad).is_file(), pfad)
        for pfad in ("landseg", "T0", "kategorien.json", "wuensche/.stand.json", "wuensche/2026-01-01-a/roh",
                     "wuensche/2026-01-01-a/einreihen-landseg.json", "daten/landseg/uebergabe"):
            self.assertFalse((ziel / pfad).exists(), pfad)
        self.assertEqual((ziel / "wuensche/2026-01-01-a.md").read_bytes(), b"# Wunsch\r\nZeile mit CRLF\r\n")
        self.assertIn(hashlib.sha256(b"abc").hexdigest(), (ziel / "daten/luftbilder/README.md").read_text(encoding="utf-8"))
        commits = git(ziel, "rev-list", "--count", "HEAD").strip()
        self.klartext_in_neuen_commits(ziel, f"{alt}..HEAD")
        self.assertIn("Add 'programm/' from landseg main", git(ziel, "log", "--oneline", "--", "programm"))

        code, text = ausfuehren("bauen", "--basis", str(basis), "--ziel", str(ziel))
        self.assertEqual(code, 0, text)
        self.assertIn("neue Commits: 0", text)
        self.assertEqual(git(ziel, "rev-list", "--count", "HEAD").strip(), commits)

        schreibe(basis / "landseg/neu.py", b"x = 1\n")
        git(basis / "landseg", "add", "-A")
        git(basis / "landseg", "commit", "-q", "-m", "feat: neu")
        neu = git(basis / "landseg", "rev-parse", "HEAD").strip()
        stand = git(ziel, "rev-parse", "HEAD").strip()
        code, text = ausfuehren("bauen", "--basis", str(basis), "--ziel", str(ziel))
        self.assertEqual(code, 0, text)
        self.assertEqual((ziel / "programm/neu.py").read_bytes(), b"x = 1\n")
        self.assertEqual(git(ziel, "merge-base", "--is-ancestor", neu, "HEAD"), "")
        self.assertIn(f"{neu[:7]} feat: neu", git(ziel, "log", "--oneline", "--abbrev=7"))
        self.assertIn("chore: update programm/ from landseg main", git(ziel, "log", "--oneline", "--", "programm"))
        self.klartext_in_neuen_commits(ziel, f"{stand}..HEAD")

        code, text = ausfuehren("pruefen", "--basis", str(basis), "--ziel", str(ziel))
        self.assertIn("fehlend 0, abweichend 0, fremd 0", text)
        self.assertIn("laut Durchsicht weggelassen 1", text)
        self.assertIn("Luftbilder nicht geprüft", text)

    def test_groessen_warnung_ab_50_und_fehler_ab_100_mb(self):
        ziel = repo(self.ort / "ziel", {"README.md": b"# Projekt\n", ".gitattributes": b"* -text\n"})
        for name, mb in (("mittel.bin", 60), ("riesig.bin", 101)):
            with (ziel / name).open("wb") as datei:
                datei.truncate(mb * GP.MB)
        warnungen, zu_gross, groesste = GP.groessen(ziel, 50, 100)
        self.assertEqual([rel for _, rel in warnungen], ["mittel.bin"])
        self.assertEqual([rel for _, rel in zu_gross], ["riesig.bin"])
        code, text = ausfuehren("pruefen", "--ziel", str(ziel))
        self.assertEqual(code, 1, text)
        self.assertIn("Warnungen: 1", text)
        self.assertIn("zu groß für GitHub (ab 100 MB): riesig.bin", text)
        (ziel / "riesig.bin").unlink()
        code, text = ausfuehren("pruefen", "--ziel", str(ziel))
        self.assertEqual(code, 0, text)
        self.assertIn("Warnung (ab 50 MB): mittel.bin 60.0 MB", text)

    def test_lfs_und_luftbilder(self):
        tabelle = ("| Datei | Größe (Bytes) | SHA-256 |\n|---|---:|---|\n"
                   f"| `a/eins.tif` | 3 | `{hashlib.sha256(b'abc').hexdigest()}` |\n"
                   f"| `a/zwei.tif` | 3 | `{hashlib.sha256(b'xyz').hexdigest()}` |\n")
        ziel = repo(self.ort / "ziel", {"README.md": b"Siehe `daten/luftbilder/README.md`.\n",
                                        ".gitattributes": b"* -text\n",
                                        "daten/luftbilder/README.md": tabelle.encode("utf-8")})
        code, text = ausfuehren("pruefen", "--ziel", str(ziel))
        self.assertEqual(code, 0, text)
        self.assertIn("Luftbilder nicht geprüft", text)
        self.assertIn("README-Pfade: alle vorhanden (1)", text)
        bilder = self.ort / "bilder"
        schreibe(bilder / "a/eins.tif", b"abc")
        code, text = ausfuehren("pruefen", "--ziel", str(ziel), "--luftbilder", str(bilder))
        self.assertEqual(code, 1, text)
        self.assertIn("1 von 2 passen", text)
        self.assertIn("fehlt: a/zwei.tif", text)
        schreibe(bilder / "a/zwei.tif", b"xyz")
        code, text = ausfuehren("pruefen", "--ziel", str(ziel), "--luftbilder", str(bilder))
        self.assertEqual(code, 0, text)
        self.assertIn("2 von 2 passen", text)
        schreibe(ziel / "unter/.gitattributes", b"*.tif filter=lfs diff=lfs merge=lfs -text\n")
        git(ziel, "add", "-A")
        git(ziel, "commit", "-q", "-m", "lfs")
        code, text = ausfuehren("pruefen", "--ziel", str(ziel))
        self.assertEqual(code, 1, text)
        self.assertIn("Git-Zusatzspeicher (lfs): unter/.gitattributes", text)

    def test_durchsicht_ordnet_funde_und_schwaerzt_zugaenge(self):
        geheim = "ghp_" + "A1b2C3d4" * 5
        ziel = repo(self.ort / "ziel", {
            "wuensche/a.md": "Bezug: kundenservice@bev.gv.at\nPython: C:/Users/Phil/x/python.exe\n".encode("utf-8"),
            "bild.png": b"\x89PNG\0nai@x.de",
        })
        bericht = self.ort / "durchsicht.md"
        code, text = ausfuehren("durchsicht", "--ziel", str(ziel), "--bericht", str(bericht))
        self.assertEqual(code, 0, text)
        inhalt = bericht.read_text(encoding="utf-8")
        self.assertIn("| `wuensche/a.md` | 1 | email | `kundenservice@bev.gv.at` | behalten |", inhalt)
        self.assertIn("| `wuensche/a.md` | 2 | kontopfad |", inhalt)
        self.assertNotIn("bild.png", inhalt)

        schreibe(ziel / "wuensche/b.md", f"Kontakt jemand@beispiel.de\ntoken = {geheim}\n".encode("utf-8"))
        git(ziel, "add", "-A")
        git(ziel, "commit", "-q", "-m", "b")
        code, text = ausfuehren("durchsicht", "--ziel", str(ziel), "--bericht", str(bericht))
        self.assertEqual(code, 1, text)
        self.assertIn("UNGEORDNET: wuensche/b.md:1 email jemand@beispiel.de", text)
        self.assertIn("FEHLER: wuensche/b.md:2 zugang (geschwärzt)", text)
        self.assertNotIn(geheim, text + bericht.read_text(encoding="utf-8"))

    def test_muster(self):
        self.assertTrue(GP.passt("a/roh/b/c.txt", ["**/roh/**"]))
        self.assertTrue(GP.passt("roh/c.txt", ["**/roh/**"]))
        self.assertFalse(GP.passt("a/rohling.txt", ["**/roh/**"]))
        self.assertTrue(GP.passt(".claude/x/y.md", [".claude/**"]))
        self.assertFalse(GP.passt("programm/.claude/x.md", [".claude/**"]))
        self.assertTrue(GP.passt("wuensche/x/einreihen-landseg.json", ["wuensche/**/einreihen-*.json"]))


if __name__ == "__main__":
    unittest.main()
