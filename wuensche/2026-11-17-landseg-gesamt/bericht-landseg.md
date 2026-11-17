# Bericht landseg
Status: bereit-zur-pruefung
Für den Nutzer: Das Gesamtprojekt für Victor liegt fertig gebaut unter `BASIS/daten/gesamt/victor-landseg`
  (ein Git-Repo, nicht hochgeladen). Darin: Einstiegsseite `README.md` mit Lesereihenfolge und der
  Benennung A/B/C samt Übersetzung zu den alten Namen, `ANLEITUNG.md` (die Übergabe-Anleitung, Pfade
  angepasst, neu ein Abschnitt „Zuerst: einrichten und ausprobieren“), `programm/` (landseg mit allen
  9 Commits), `unterlagen/` (mit beiden Commits), `wuensche/` (alle Aufträge und Berichte), `ergebnisse/`
  (die Übergabe-Auswahl), `daten/landseg/` (alle Arbeitsdaten, rund 320 MB) und
  `daten/luftbilder/README.md` (die acht Originale mit Größe und Prüfsumme; die Bilder selbst fehlen
  bewusst). Größte Datei 17,8 MB, also nichts über 50 MB.
  Bei der Durchsicht auf Vertrauliches fand sich nichts an Zugangsdaten oder Schlüsseln. In der Kopie
  weggelassen habe ich 24 Dateien: 22 Verwaltungsdateien des Wunsch-Systems (Laufzähler,
  `profile-vorher.json`, `einreihen-*.json`) und die zwei Einzelberichte e05 der Methoden-Ermittlung,
  die eine Arbeitssitzung im Bereich nai (Repo stitcher) im Detail auswerten. Behalten sind die zwei
  Behörden-Adressen (BEV, DORIS), alle Pfade mit `C:/Users/Phil/…` und die kurzen Erwähnungen des
  Stitchers als Herkunft der Methode. Hinweis zu e05: Victors eigener Bericht 48 nennt NAI selbst, und
  `programm/landseg/sam3.py` sagt, dass es aus dem Stitcher übernommen ist; wenn du e05 doch mitgeben
  willst, reicht es, eine Regel in `einstellungen/gesamt_projekt.json` zu streichen und neu zu bauen.
  Eine Abweichung vom Auftrag: `git log -- programm` zeigt nur die Übernahme-Commits, nicht die
  einzelnen Commits des Programms. Die Commits sind trotzdem alle mit ihrer ursprünglichen Kennung da
  (`git log --oneline` zeigt sie); das README erklärt, wie man den Verlauf einer Programmdatei sieht.
  Wichtig vor dem Hochladen: Nach dem Einreihen muss `bauen` einmal neu laufen (Nacharbeit), erst dann
  enthält `programm/` das neue Prüfwerkzeug, das der erste Befehl der Anleitung braucht.
Commit: 2bbe64a "feat(tools): add gesamt_projekt to build, check and review the shared project for Victor"
Abnahmekriterien:
  AK1: nicht erfüllt (ein Teil) — `README.md`, `ANLEITUNG.md`, `programm/`, `unterlagen/`, `wuensche/`, `daten/landseg/`, `ergebnisse/`, `daten/luftbilder/README.md` liegen im Ziel; alle 9 Commits aus `git -C landseg log main` und beide aus unterlagen stehen mit gleicher Kennung im Ziel (Schleife `git cat-file -e <sha>` über `git -C landseg log --format=%H main`: keiner fehlt), `git -C <Ziel> log --oneline` zeigt sie, `git -C <Ziel> cat-file -t f0a0198` → `commit`. Nicht erfüllt: `git log --oneline -- programm` zeigt nur `Add 'programm/' from commit 'bb7dd84…'`, weil `git subtree` (wie verlangt, ohne `--squash`) die Commits mit ihren ursprünglichen Pfaden ohne Vorsatz übernimmt; Verlauf je Datei: `git log --oneline --full-history -- landseg/kacheln.py` zeigt die landseg-Commits (geprüft: `e805308 feat: add landseg package …`).
  AK2: erfüllt — `"$PY" -B tools/gesamt_projekt.py pruefen --basis C:/Users/Phil/Developement/Victor --ziel C:/Users/Phil/Developement/Victor/daten/gesamt/victor-landseg` → „Vollständigkeit: fehlend 0, abweichend 0, fremd 0 (geprüft 1585 Dateien; laut Durchsicht weggelassen 24)“, „Verbotene Pfade: 0“, Exit 0; am echten Ziel mit `--luftbilder C:/Users/Phil/Developement/Victor/daten/luftbilder` → „Luftbilder: 8 von 8 passen“, „Ergebnis: ok“. Verglichen wird die Git-Prüfsumme jeder Quelldatei mit dem Blob im Commit des Ziels (Byte für Byte). Weggelassen sind nur die 24 Dateien der Durchsicht (AK4) und 5 `__pycache__/*.pyc` aus `daten/landseg/T0/kern500/urteil/*/v*/` (Bytecode der Hilfsskripte, Git nimmt ihn nach `.gitignore` ohnehin nicht).
  AK3: erfüllt — `pruefen` → „größte Datei 16.9 MB (…/kern500/vorstufe/r1c1/sam3_roh.npz (Verlauf)); Warnungen: 0; ab 100 MB: 0“ (MiB; 17,8 Mio. Bytes), „Git-Zusatzspeicher (lfs): keiner“; Unittest `test_groessen_warnung_ab_50_und_fehler_ab_100_mb` (60 MB → Warnung, 101 MB → „zu groß für GitHub“, Exit 1). Geprüft werden Arbeitsstand und alle Blobs im Verlauf.
  AK4: erfüllt — `"$PY" -B tools/gesamt_projekt.py durchsicht --basis … --ziel … --bericht wuensche/2026-11-17-landseg-gesamt/durchsicht-landseg.md` → „ungeordnet oder Fehler: 0“, Exit 0; Zugangsdaten/Schlüssel: 0 Fundstellen. Fundstellen unten unter „Durchsicht“, vollständig mit Datei und Zeilen in `durchsicht-landseg.md`. Quellordner unverändert (das Werkzeug liest dort nur).
  AK5: erfüllt — `README.md` (Lesereihenfolge, Aufbau, Benennung A/B/C, Übersetzungstabelle aus der Anleitung übernommen, `ergebnisse/` gegen `daten/landseg/`); `pruefen` → „README-Pfade: alle vorhanden (41)“.
  AK6: erfüllt — `ANLEITUNG.md` Schritt 1 und `daten/luftbilder/README.md` (Tabelle aus `BASIS/daten/README.md`, Zielordner `daten/luftbilder/orthofoto-aktuell/` und `historisch/`); im frischen Klon mit hineinkopierten Originalen: `pruefen --ziel . --luftbilder daten/luftbilder` → „Luftbilder: 8 von 8 passen“, Exit 0; ohne Option „Luftbilder nicht geprüft (ohne --luftbilder)“, Exit 0; ein Bild entfernt → „7 von 8 passen / fehlt: historisch/1957004_004A_1557.tif“, Exit 1.
  AK7: erfüllt (an einem Probe-Bau aus dem Zweig `wunsch/landseg-gesamt`, weil `main` das Werkzeug noch nicht hat) — Ablauf in `nutzerweg-landseg.log`: `git clone` des Probe-Ziels, Originale hineinkopiert, Schritt 1 Exit 0, Tests in `programm/` „Ran 104 tests … OK“, Schritt 3 `landseg pruefen` auf `ergebnisse/c-feste-liste/r0c0` → „ok“, Exit 0, Schritt 4 `kacheln` aus dem Original → `T0.png` und vier Teilkacheln bytegleich mit `ergebnisse/`, `git status` im Klon leer.
  AK8: erfüllt — Unittest `test_bauen_ist_wiederholbar_und_bringt_neue_commits_mit_verlauf` (zweiter Lauf „neue Commits: 0“, neuer landseg-Commit kommt mit Kennung nach `programm/`); am echten Ziel dritter Lauf ohne Änderung → „neue Commits: 0“; `git -C <Ziel> config core.autocrlf` → `false`, dazu `* -text` in `.gitattributes`.
Prüfungen:
  schnell: `pruefe_kategorien.py kategorien.json` → ok; `git status --short` sauber nach Commit
  `"$PY" -B -m unittest discover -s tests -t .` (in W) → Ran 104 tests in 29 s, OK
  `"$PY" -B -m unittest tests.test_gesamt_projekt` → 5 Tests OK (rund 15 s, `git subtree` unter Windows)
  `gesamt_projekt.py bauen` am echten Ziel → 5 Commits auf `f0a0198` (Umbau, zwei Subtree-Übernahmen, Abgleich), danach je ein Abgleich-Commit, zuletzt „neue Commits: 0“
  `gesamt_projekt.py pruefen --basis … --ziel …` → Ergebnis: ok, Exit 0
  `gesamt_projekt.py durchsicht --basis … --ziel …` → 0 ungeordnet, Exit 0
  Nutzerweg im Klon: `nutzerweg-landseg.log` (alle Schritte Exit 0)
  volle Stufe: nicht selbst gefahren (Pflichtlauf des Einreihens)
Durchsicht (Zusammenfassung; jede Fundstelle mit Datei und Zeilen in `durchsicht-landseg.md`):
  Zugangsdaten/Schlüssel: keine.
  E-Mail-Adressen: nur `kundenservice@bev.gv.at` und `doris.geol.post@ooe.gv.at` — behalten (öffentliche Behörden-Adressen, Bezugsquelle der Luftbilder): `wuensche/2026-11-17-landseg-methode.md` Z. 198, `wuensche/2026-11-17-landseg-methode/einheiten/n02.md` Z. 43, 70, 75, `wuensche/2026-11-17-landseg-methode/gegenpruefung/n02.md` Z. 13, 23, `wuensche/2026-11-17-landseg-gesamt.md` Z. 65, dazu die Berichte dieses Wunschs.
  Anderer Bereich, in der Kopie entfernt: `wuensche/2026-11-17-landseg-methode/einheiten/e05.md`, `wuensche/2026-11-17-landseg-methode/gegenpruefung/e05.md` (ausführliche Auswertung der Stitcher-Sitzung im Bereich nai: Abläufe, Aufträge, Agent-Namen, Pfade in Sitzungsprotokolle).
  Anderer Bereich, behalten: Pfad zur Python-Umgebung bzw. zu Vorlagen unter `websites/nai/stitcher` (222 Fundstellen, v. a. die 40 `auftrag.md` unter `wuensche/2026-11-17-landseg-test-t0-1/`, `gruppen.json`, Berichte der Werkzeug-Teile); Erwähnung „Stitcher“ als Herkunft (372 + 104, u. a. `wuensche/2026-11-17-landseg-methode/bericht.md`, `plan.md`, `deutung.md`, `einheiten/e03.md`, `e06.md`, `programm/landseg/sam3.py` Z. 3, `programm/KATEGORIEN.md` Z. 156, `programm/kategorien.json` Z. 1587, `programm/.claude/skills/landseg-agent/SKILL.md` Z. 10, die `arbeitsweise.md` von r1c0/r1c1); „NAI“ in Victors eigenem `unterlagen/berichte/48_luftbild_segmentierung_klassen.md` Z. 56; „privat“ = privates GitHub-Projekt in `wuensche/2026-11-17-landseg-uebergabe/bericht-landseg.md`; die Bereichsliste im Auftrag dieses Wunschs. marlene, eventmanagement: nur in diesem Auftrag.
  Wunsch-System, in der Kopie entfernt: `wuensche/.laeufe.json`, 11 × `profile-vorher.json`, 10 × `einreihen-landseg.json`/`einreihen-unterlagen.json` (Buchführung ohne Wert zum Nachvollziehen); behalten: Erwähnungen als Herkunft (118 Fundstellen, z. B. `wunsch-system`, `.claude/repos`, `stand.py`), dazu die Entwurfs-Vorlagen unter `wuensche/2026-11-17-landseg-werkzeuge/entwurf/gemeinsam/` (nötig, um die Entwürfe der Prüfseite anzusehen).
  Pfad mit Kontoname (`C:/Users/Phil/…`): 10 455 Fundstellen in 285 Dateien, behalten (Ablageort auf dem Rechner, kein Geheimnis; das README sagt, dass `C:/Users/Phil/Developement/Victor/` dem Projektordner entspricht).
Nicht geprüft: Push nach GitHub, Umbenennen, Einladen (Sache der Hauptsession); der Nutzerweg (AK7) am echten Ziel erst nach dem Einreihen und neuem `bauen` möglich, weil `programm/` bis dahin `tools/gesamt_projekt.py` nicht enthält; Vorstufe (GPU) im Klon nicht gefahren.
Einstieg: stimmte; `tools/pruefe_kategorien.py` als Muster, `README.md`-Tabelle ergänzt; die Dateitabelle der Übergabe-Anleitung stand in Zeilen 25–40, die Benennung in 47–60.
Technische Entscheidungen:
  - Gesamt-Ordner `BASIS/daten/gesamt/victor-landseg` (wie im Arbeitsauftrag) außerhalb von W angelegt und dort committet; die Übergabe-Kopie `daten/landseg/uebergabe/landseg-t0` blieb unverändert. `origin` zeigt auf `https://github.com/PhilMeyer1/landseg-t0.git`.
  - `T0/` per `git mv` zu `ergebnisse/` (Verlauf der Ergebnisdateien bleibt verfolgbar), übrige Wurzeldateien der alten Kopie per `git rm` (im Verlauf bleiben sie).
  - Programm und Unterlagen kommen per `git subtree add/pull` vom Hauptbranch `main` (nicht vom Arbeitszweig), damit die Kennungen nach dem Einreihen stimmen.
  - README, Anleitung und Luftbild-Beschreibung sind Vorlagen im Repo (`gesamt/`), `bauen` schreibt sie mit LF; die Luftbild-Tabelle wird aus `BASIS/daten/README.md` übernommen, nicht abgeschrieben.
  - Durchsicht nach festen Mustern (Arten) und Regeln in `einstellungen/gesamt_projekt.json`; jede neue Fundstelle ohne Regel lässt `durchsicht` mit Exit 1 enden, Zugangsdaten immer, und ihr Wert wird nie ausgegeben. Entfernt wird nur dateiweise (keine geänderten Kopien), damit alle übrigen Dateien bytegleich bleiben.
  - `pruefen --luftbilder` endet mit Exit 1, wenn ein Original fehlt oder abweicht (nennt es mit Namen; kein Absturz); ohne Option Exit 0.
  - `.gitignore` des Ziels schließt nur `daten/luftbilder/*` (außer README) und `arbeit/` aus, keine Dateiendungen.
Nacharbeit im Hauptordner:
  - Nach dem Einreihen: in `R` `"$PY" -B tools/gesamt_projekt.py bauen --basis C:/Users/Phil/Developement/Victor --ziel C:/Users/Phil/Developement/Victor/daten/gesamt/victor-landseg`, danach `pruefen --basis …` und `durchsicht --basis … --bericht …` (bringt den neuen Commit nach `programm/` und den aktuellen Stand von `wuensche/`); erst dann pushen.
  - `.claude/hoheit.md` (Abschnitt „Victor“): Zeile „Gesamtprojekt victor-landseg (GitHub, Kopie)“ — Hoheit Bereich victor, abgeleitet aus `programm/`, `unterlagen/`, `wuensche/`, `daten/landseg/`; keine eigenen Daten.
  - `BASIS/daten/README.md`: Hinweis auf `BASIS/daten/gesamt/`.
  - Hauptsession: auf GitHub umbenennen, `origin` umstellen, pushen in Etappen ohne Force (Objekte rund 240 MB lose), Victor einladen.
  - Profil landseg: Routine `tools/gesamt_projekt.py` nennen; Laufzeit der Testsuite jetzt rund 30 s statt unter 2 s.
Abräumen: offen (Einreihen); Probe-Ordner `scratchpad/probe/` (Probe-Ziel, Klon, Kopie der Originale) gelöscht; das Probe-Skript hat einen dort schon liegenden Ordner `probe/` vor dem Lauf geleert, falls ein früherer Lauf ihn angelegt hatte (geprüft habe ich das vorher nicht); keine Dauerprozesse.
Lagebild: fehlt (landseg hat kein Lagebild)
Erkenntnisse fürs Profil:
  - Die Testsuite braucht jetzt rund 30 s (vorher unter 2 s): `tests/test_gesamt_projekt.py` baut Wegwerf-Repos mit `git subtree`, das unter Windows je Aufruf mehrere Sekunden braucht.
  - Global steht `core.autocrlf=true`: Dateien im Hauptordner können nach einem Checkout CRLF haben, auch wenn der Blob LF ist; Byte-Vergleiche gegen Git-Blobs, nicht gegen den Arbeitsstand.
  - Nach `git subtree add` zeigt `git log -- <prefix>` nur die Übernahme-Commits; den Verlauf einer übernommenen Datei zeigt `git log --full-history -- <pfad ohne prefix>`.
  - `git -C … -c core.autocrlf=false config core.autocrlf` liefert immer den `-c`-Wert, nicht die Einstellung des Repos.
Abweichungen vom Zielbild:
  - `tools/gesamt_projekt.py:51` — liest `einstellungen/gesamt_projekt.json` selbst und `--einstellungen` ersetzt die Datei ganz, statt über `landseg/einstellungen.py` einzelne Schlüssel zu überschreiben — nötig, weil das Skript in `tools/` ohne das Paket (Standardbibliothek, ohne numpy) laufen soll — sauber wäre ein paketfreier Lader, den Paket und `tools/` gemeinsam nutzen.
  - `gesamt/README.md` — die Vorlagen der Gesamtprojekt-Seiten liegen im Code-Repo und erscheinen im Gesamtprojekt doppelt (Wurzel und `programm/gesamt/`) — gewählt, damit sie versioniert und mit dem Werkzeug geprüft sind — sauber wäre ein eigenes kleines Repo für die Seiten des Gesamtprojekts.
