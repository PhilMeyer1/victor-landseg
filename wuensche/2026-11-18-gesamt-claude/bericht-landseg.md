# Bericht landseg
Status: eingereiht
Für den Nutzer: Das Gesamtprojekt bekommt beim nächsten Bauen eine `CLAUDE.md` im Hauptordner. Öffnet
  Victor den Ordner mit Claude Code, öffnet Claude bei seiner ersten Antwort (Victor muss also zuerst
  irgendetwas schreiben, etwa „hallo“) ohne Rückfrage `ergebnisse/T0.html` im Standard-Browser,
  prüft, dass das ging, und erklärt in wenigen Sätzen die Seite (Fassungen A/B/C, vier Teilkacheln,
  Segment anklicken, Kommentare und Export) und wo er weiterliest. Fehlt die Seite, sagt Claude das
  offen. Die alten Seiten unter `daten/landseg/T0/kern500/seite/` sind dort als „nicht öffnen, alte
  Benennung“ markiert. `pruefen` verlangt jetzt README, ANLEITUNG und CLAUDE.md und prüft jeden darin
  genannten Pfad. Nebenbei gefunden und behoben: Die Vertraulichkeits-Durchsicht schlug schon auf dem
  heutigen GitHub-Stand mit 2 ungeordneten Fundstellen an (zitierte Testwerte in einem alten
  Durchsicht-Bericht), nach dem Neubauen wären es 16 gewesen; Berichte früherer Durchsichten gelten
  jetzt als „behalten“.
  Zum 404 beim Einladungslink: Die Einladung auf GitHub besteht (für das Konto `vschrn`, Schreibrecht,
  vom 17.11. 21:08, nicht abgelaufen), das Projekt ist privat und auf GitHub vollständig (Stand
  7e34599, frischer Klon geht). GitHub zeigt bei privaten Projekten 404, solange man nicht mit genau
  dem eingeladenen Konto angemeldet ist: Victor muss sich zuerst als `vschrn` anmelden und dann den
  Link öffnen (oder die Einladung unter github.com/notifications annehmen); ist `vschrn` nicht sein
  Konto, braucht es eine neue Einladung an das richtige.
  Ungeprüft: die Seite im Browser per Foto (Browser-Erweiterung in diesem Lauf nicht verfügbar) und
  das tatsächliche Öffnen per Befehl (hätte ein Browserfenster auf dem Bildschirm geöffnet).
  Nach dem Einreihen: neu bauen und hochladen (Hauptsession).
Commit: e3c15df "feat(tools): add CLAUDE.md to the shared project that opens the results page first"
Abnahmekriterien:
AK1: erfüllt (Inhalt), Verhalten nicht prüfbar — `gesamt/CLAUDE.md` wird von `bauen` in den Wurzelordner geschrieben (Probebau in Prüfordner: Commit e7e71c4 enthält `CLAUDE.md`, 76 Zeilen); Test `test_bauen_ist_wiederholbar…` vergleicht sie Byte für Byte mit der Vorlage. Windows-Befehl `cmd //c start "" "ergebnisse\T0.html"`: Pfad im Prüfordner vorhanden (`cmd //c if exist ergebnisse\T0.html` → da); das Öffnen selbst nicht ausgeführt (Fenster-Regel), für die Abnahme offen
AK2: erfüllt bis auf Foto und Testlauf — frischer Klon von GitHub (Stand 7e34599) in Prüfordner: 1596 Dateien, `pruefen` → ok; Probebau mit neuem Werkzeug: `pruefen --basis` → „fehlend 0, abweichend 0, fremd 0“, Pfade in README 41, ANLEITUNG 38, CLAUDE.md 14 alle vorhanden, Ergebnis ok; `durchsicht --basis` → Exit 0. `ergebnisse/T0.html` statisch geprüft: beide Skriptblöcke `node --check` Exit 0, keine Verweise ins Netz, Fassungen A „Alles frei“, B „Kategorien frei“, C „Feste Kategorienliste“ je mit Daten und 4 Teilkacheln (r0c0, r0c1, r1c0, r1c1). Tests von `programm/`: gebündelt — Pflichtlauf des Einreihens (volle Reihe des Profils, derselbe Code wie `programm/` nach dem Neubauen)
Prüfungen:
PY -B -m unittest tests.test_gesamt_projekt (in W) → 6 Tests OK (neu: test_pfade_in_readme_anleitung_und_claude; CLAUDE.md im Bau, Fehlen → Befund; Durchsicht-Berichte behalten)
PY -I tools/pruefe_kategorien.py kategorien.json → ok
git clone https://github.com/PhilMeyer1/victor-landseg.git (Scratchpad) → 7e34599, 1596 Dateien, sauber
programm/tools/gesamt_projekt.py pruefen --ziel . (im Klon, altes Werkzeug) → Ergebnis: ok
gesamt_projekt.py durchsicht --ziel <Klon> (neues Werkzeug vor der Regel) → 2 UNGEORDNET (wuensche/2026-11-17-landseg-gesamt/durchsicht-final.md:243)
gesamt_projekt.py bauen --basis BASIS --ziel <Kopie des Klons> → 1 neuer Commit e7e71c4 (CLAUDE.md, README, ANLEITUNG, Wünsche)
gesamt_projekt.py pruefen --basis BASIS --ziel <Bau> → Ergebnis: ok
gesamt_projekt.py durchsicht --basis BASIS --ziel <Bau> → vor der neuen Regel 16 UNGEORDNET, danach Exit 0
seite_pruefen.py (Scratchpad, statisch) → 2 Skripte node --check 0, A/B/C vorhanden, 4 Teilkacheln
Volle Stufe: offen, läuft im Pflichtlauf des Einreihens
Prüfordner (Scratchpad, kein Teil des Projekts): C:/Users/Phil/AppData/Local/Temp/claude/27e54e3b8399faf6/a2bf01d3-627c-4b06-8b57-51f25ab5229e/scratchpad/klon und …/scratchpad/bau, Durchsicht-Bericht …/scratchpad/durchsicht-bau.md
Nicht geprüft: Foto der Seite über die Browser-Erweiterung (in diesem Lauf nicht verfügbar); tatsächliches Öffnen per `start` (Browserfenster); Claude-Code-Session im Gesamtprojekt (ob Claude der Anweisung folgt); Luftbilder (`--luftbilder`, Originale nicht im Prüfordner)
Technische Entscheidungen:
- CLAUDE.md als weitere „Seite“ in `einstellungen/gesamt_projekt.json` (`seiten`), damit `bauen` sie schreibt und `pruefen --basis` sie über die Vollständigkeit verlangt; `CLAUDE.md` aus `verboten` entfernt (schützte bisher nur davor, dass eine fremde CLAUDE.md hineinkommt; das deckt jetzt der Byte-Vergleich mit der Vorlage).
- Die Pfadprüfung gilt jetzt für alle Seiten in `pfad_seiten` (README, ANLEITUNG, CLAUDE.md) und verlangt jede davon auch ohne `--basis`; `../` am Anfang zählt vom Projektordner (Befehle der Anleitung laufen in `programm/`), `\` wird zu `/`; `pfade_ohne: daten/luftbilder/*/**` nimmt die getrennt gelieferten Luftbilder aus. Ausgabezeile heißt jetzt „Pfade in <Seite>: …“ statt „README-Pfade: …“.
- Windows-Befehl für Claude Code im Bash-Werkzeug `cmd //c start "" "ergebnisse\T0.html"` (Git Bash), dazu PowerShell `Start-Process`, Eingabeaufforderung `start`, macOS `open`, Linux `xdg-open`.
- Neue Durchsicht-Regel steht als letzte, damit genauere Gründe vorgehen; sie greift nur, wo sonst keine Regel passt.
- Neu bauen nur in einen Prüfordner im Scratchpad (Kopie des GitHub-Klons), nicht in `BASIS/daten/gesamt/victor-landseg` (macht die Hauptsession).
Nacharbeit im Hauptordner: nach dem Einreihen `gesamt_projekt.py bauen`, `pruefen --basis`, `durchsicht` und Hochladen des Gesamtprojekts (Hauptsession, laut Wunsch); Victor muss die Einladung mit dem Konto `vschrn` angemeldet annehmen
Abräumen: offen (Arbeitskopie bleibt bis zum Einreihen); Prüfordner im Scratchpad (klon, bau, seite) sind außerhalb des Projekts
Lagebild: fehlt (landseg hat kein LAGEBILD.md, das Profil keine Zeile `lagebild:`)
Erkenntnisse fürs Profil:
`gesamt_projekt.py pruefen` heißt die Pfadzeilen jetzt „Pfade in README.md/ANLEITUNG.md/CLAUDE.md“ und verlangt alle drei Seiten auch ohne `--basis`; ein Test-Ziel braucht daher alle drei Dateien.
Escapes in Bash-Heredocs (`\\n`) kommen im Bash-Werkzeug einfach an (`\n`): Python-Hilfsskripte mit Escapes über das Write-Werkzeug anlegen, nicht per Heredoc.
`durchsicht` auf dem GitHub-Stand vom 17.11. (7e34599) war schon rot (2 ungeordnete E-Mail-Funde in einem zitierten Durchsicht-Bericht): vor dem Hochladen `durchsicht` immer mitfahren, nicht nur `pruefen`.
Abweichungen vom Zielbild: keine
Einreihen (Skript): eingereiht e3c15df feat(tools): add CLAUDE.md to the shared project that opens the results page first in C:/Users/Phil/Developement/Victor/landseg (main); Prüfung nach Risiko (ohne Prüfschleuse, keine Zeile schnell: im Profil); voll grün (19 s); volle Prüfung offen (vermerkt in C:/Users/Phil/Developement/Victor/landseg/.git/wunsch-einreihen/pruefung-offen.jsonl); Abräumen WEG; Waisen 1 (sonstige 1), 101 MB anderswo (aufraeumer.py melden; beenden nur mit Freigabe des Nutzers)
