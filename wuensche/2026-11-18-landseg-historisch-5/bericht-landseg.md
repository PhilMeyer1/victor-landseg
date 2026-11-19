# Bericht landseg
Status: bereit-zur-pruefung
Für den Nutzer: Das Gesamtprojekt victor-landseg (lokal, nicht hochgeladen) hat jetzt die Ergebnisse von H0 neben
  denen von T0: `ergebnisse/T0/`, `ergebnisse/H0/` und die Seite `ergebnisse/T0-H0.html` mit Bildwahl (dieselbe
  Seite, die Sie durchgesehen haben; nur die Quellpfade im Inneren sind andere). Achtung, neue Pfade: T0 liegt
  nicht mehr direkt in `ergebnisse/`, sondern in `ergebnisse/T0/`. ANLEITUNG, README und CLAUDE.md nennen H0 und
  lassen Claude Code zuerst `ergebnisse/T0-H0.html` öffnen. Nicht angesehen: die Seite im Browser (keine
  Browser-Erweiterung in diesem Lauf). Nach dem Einreihen muss das Gesamtprojekt noch einmal gebaut werden
  (programm/ zieht erst dann diesen Commit), danach kann es hochgeladen werden.
Commit: 869593b "feat(gesamt): results of the historical cut-out H0 next to T0 in the shared project"
  Dazu außerhalb des Repos: Übergabe-Grundlage `daten/landseg/uebergabe/landseg-t0` 172a019 "feat(H0): add the
  historical cut-out H0 next to T0 and a page with both images"; Gesamtprojekt 4635a5d, 7f02d4e (von `bauen`).
Abnahmekriterien:
AK6: erfüllt (Gesamtprojekt-Teil vorläufig, siehe Prüfungen) — Repo: `einstellungen/seite.json` (bilder T0/H0, schon aus Teil 1), README „Weiteres Bild" mit Befehlsfolge H0 aus dem Scan; Gesamtprojekt: `ergebnisse/H0/` (106 Dateien, 20,7 MB) neben `ergebnisse/T0/`, ANLEITUNG (Abschnitt „Historischer Ausschnitt H0", Prüfseite, Projektaufbau), README, CLAUDE.md nennen H0 und `ergebnisse/T0-H0.html`; `bauen` 0, `durchsicht` 0, `pruefen` siehe unten
AK7: nicht prüfbar (Ansicht) — keine Browser-Erweiterung. Ersatzbeleg: Daten der Seite `T0-H0.html` mit `seiten_vergleich.py` gegen die durchgesehene `daten/landseg/seiten/T0-H0.html` verglichen: gleich bis auf Quellpfade und Zeitstempel (T0 und H0 je A/B/C mit Daten, Nähte- und Einigungszahlen H0 A 163/33, B 151/16, C 133/12); im Gesamtprojekt Byte für Byte der Blob der Übergabe (`pruefen`: abweichend 0)
Prüfungen:
`"$PY" -B -m unittest tests.test_gesamt_projekt tests.test_seite` → Ran 20, OK
`"$PY" -I tools/pruefe_kategorien.py kategorien.json` → ok
`landseg seite --daten <Übergabe> --ziel <Übergabe>/T0-H0.html` (im Hauptordner, Code von main) → Exit 0, 13 620 221 Bytes
`gesamt_projekt.py bauen --basis <BASIS> --ziel <BASIS>/daten/gesamt/victor-landseg` → 0, 2 neue Commits (Ergebnisse 192 Dateien aus 172a019)
`gesamt_projekt.py pruefen … --luftbilder <BASIS>/daten/luftbilder` (vor dem Bericht) → 1: einziger Befund „Pfade in README.md: fehlt wuensche/2026-11-18-landseg-historisch-5" (dieser Berichtsordner existierte noch nicht); sonst fehlend/abweichend/fremd 0, Luftbilder 8/8, größte Datei 17,5 MB
`gesamt_projekt.py durchsicht … --bericht <Scratchpad>` → 0
Nicht geprüft: Ansicht der Seite (AK7) im Browser; volle Testreihe (Einreihen)
Einstieg: stimmte (Einstieg des Mutterwunschs; `seite.json` hatte die Bilder schon)
Technische Entscheidungen:
- Ablage im Gesamtprojekt: `ergebnisse/T0/`, `ergebnisse/H0/`, `ergebnisse/T0-H0.html` statt H0 in den T0-Ordner zu schachteln; dafür ist `umbau.aus` eine Liste von Einträgen der Übergabe (`T0`, `H0`, `T0-H0.html`), gespiegelt unter gleichem Namen. Alle T0-Pfade in ANLEITUNG (28) und CLAUDE.md auf `ergebnisse/T0/…` umgestellt.
- Übergabe-Grundlage: H0 mit derselben Auswahl wie T0 (Manifest unverändert, Ausschnitt, Teilkacheln, `ganz/`, je Fassung Karten, `segmente.json`, `kandidaten.json`, `zusammen/`, Liste, `urteil/<tk>/v<n>/urteil.json`, A `abgabe/<tk>/arbeitsweise.md` + `kategorien-teil.json`), ohne Agent-Bilder. Die Seite dort mit `seite --daten .` aus dem Hauptordner (main) gebaut, damit keine Arbeitskopie-Pfade eingebettet sind. Skript: Scratchpad `h0_uebergabe.py` (nicht im Repo).
- Die zwei nur-CRLF-Änderungen der Übergabe (`T0/a-alles-frei/kategorien-a.json`, `kategorien-b.json`, mit `core.autocrlf=false` ohne Diff) nicht angefasst.
Nacharbeit im Hauptordner: Nach dem Einreihen und dem Commit von `wuensche/`: `gesamt_projekt.py bauen|pruefen --luftbilder|durchsicht` mit dem Werkzeug aus `landseg` main erneut (programm/ und dieser Berichtsordner), dann Push durch die Hauptsession. Profil `BASIS/.claude/repos/landseg.md` (Routinen: Gesamtprojekt-Pfade `ergebnisse/T0/`, `ergebnisse/H0/`, `ergebnisse/T0-H0.html`, `umbau.aus` als Liste) und `landseg/betrieb.md` (Zeilen zu `ergebnisse/manifest.json` und `ergebnisse/T0.html`) nachziehen.
Abräumen: offen (Einreihen)
Lagebild: fehlt (landseg hat kein Lagebild; Profil ohne `lagebild:`)
Erkenntnisse fürs Profil:
- Im Gesamtprojekt liegt T0 jetzt unter `ergebnisse/T0/` (vorher direkt in `ergebnisse/`); Probeläufe von `seite` mit `daten/gesamt/victor-landseg/ergebnisse/T0/manifest.json`.
- `gesamt_projekt.py bauen` löscht entfernte Dateien mit `unlink`, leere Ordner bleiben im Arbeitsstand des Ziels stehen (Git sieht sie nicht).
- Bash-Heredocs verschlucken hier `\\` (auch in Python-Quelltext und sed-Mustern): Escapes über das Write-/Edit-Werkzeug.
- `pruefen` meldet einen in README.md genannten Berichtsordner als fehlend, solange er in `wuensche/` noch nicht existiert.
Abweichungen vom Zielbild: keine
