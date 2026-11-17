# Bericht landseg
Status: eingereiht
Für den Nutzer: Die Prüfseite zeigt die Fassungen jetzt in der neuen Reihenfolge: A „Alles frei“,
  B „Kategorien frei“, C „Feste Kategorienliste“. Sie öffnet mit A. Das Übergabe-Projekt für Victor
  liegt fertig als lokales Git-Repo unter
  `C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/` (25 MB, ein Commit `main`).
  Darin sind die Werkzeuge, je Fassung Karte, Kategorienliste und Urteile, die Prüfseite `T0/T0.html`,
  Gesamtbilder je Fassung und die `ANLEITUNG.md` für Victor. Die Prüfseite habe ich nicht im Browser
  angesehen, weil die Browser-Erweiterung in dieser Sitzung fehlte. Geprüft habe ich die Daten, die
  in der Seite stecken. Hochgeladen ist noch nichts: Push und Einladung macht die Hauptsession nach
  dem Einreihen. Achtung bei Kommentaren aus der alten Seite `kern500/seite/T0-urteil.html`: Dort
  heißt die feste Liste noch „A“. In der neuen Benennung ist sie „C“.
Commit: bb7dd84 "feat(seite): reorder versions to A all free, B free categories, C fixed list"
Abnahmekriterien:
AK1: erfüllt — `einstellungen/seite.json` hat die Fassungen A „Alles frei“ (`a-alles-frei`), B „Kategorien frei“ (`b-kategorien-frei`) und C „Feste Kategorienliste“ (`c-feste-liste`) in dieser Reihenfolge. Die Seite öffnet mit der ersten Fassung mit Daten (`seite.js:44`, `ERSTE`). `PY -B -m unittest discover -s tests -t .` → 99 Tests OK; `test_einstellungen_und_befehl` prüft Reihenfolge, Namen und Ordner. README, Abschnitt „Erster Durchgang“, Tabelle der Fassungen.
AK2: teilweise belegt, kein Foto — Daten aus `T0/T0.html` gelesen: Reihenfolge A Alles frei, B Kategorien frei, C Feste Kategorienliste. Alle drei haben Daten, je Teilkachel `pruefen ok` und 0 Bildpunkte ohne Segment. Kategorienlisten: A `kategorien-a.json` (47 Klassen), B `kategorien-b.json` (49), C `kategorien-c.json` (58). Eine Ansicht im Browser fehlt (Erweiterung nicht erreichbar).
AK3: erfüllt — `git ls-files` → 123 Dateien. Je Fassung ein Ordner mit `<tk>/labels.tif` und `segmente.json` sowie Kategorienliste. Urteile (`urteil/<tk>/urteil.json`) gibt es für B und C. A hat kein Urteil je Segment, nur die Abgabe je Agent (`abgabe/<tk>/arbeitsweise.md`, `kategorien-teil.json`) und `zusammen/` (Karte von ganz T0, `naht.json`). Dazu `T0.html`, `gesamtbilder/` (6 PNG) und `ganz/` (Übersichtsbilder der Agents). Keine Viertelbilder, keine Vorstufe, kein `sam3_roh.npz`, keine Probeläufe. `du -sh` 25 MB ohne `.git`, 45 MB mit; `git count-objects -vH` → 19,19 MiB.
AK4: erfüllt — `grep -rn "fassung-c\|kern500\|Fassung C\b"` im Projekt findet keine alten Ordnernamen. Es bleiben nur Treffer „Fassung C“ in neuer Bedeutung (feste Liste): `c-feste-liste/<tk>/segmente.json` (`stand`), `kategorien-b.json:828` und `tests/test_seite.py`. Alte Namen stehen nur in der Übersetzungstabelle der Anleitung. Umbenannt wurden das Feld `fassung` (A↔C), Pfade, Bearbeiter und Titel. Wie oft je Datei: `umbenennung-landseg.json`.
AK5: erfüllt — `ANLEITUNG.md` deckt alle Punkte ab. Stichprobe gegen die Dateien (`zahlen-landseg.json`): C „nicht sauber“ 432 = 114+89+48+181, `sicher: nein` 481 (75 %); B 405 und 397 (62 %); A 607 Segmente in T0, 881 je Teilkachel; Nahtverstöße A 309 (`naht.json`, nachgerechnet); zerfallen 20 (`pruefen --form 1000x1000`); Klassenwechsel C 383; Punkte Klasse 328, Verschmelzen 156; Tokens 3,30 Mio. (Nachweis Teil 2). Alles stimmt mit den Berichten `-1` und `-3` überein. Zu `-4` gibt es keinen Bericht, Teil 4 ruht.
AK6: erfüllt — Abschnitte „Bekannte Schwächen“ und „Was fehlt“ der Anleitung, in der neuen Benennung.
AK7: erfüllt — `git -C <Projekt> status --short` leer, Branch `main`, Commit 73319af. Im Projekt: `PY -B -m unittest discover -s tests -t .` → OK, `PY -B -m landseg --help` → Exit 0. `README.md` beginnt mit dem Verweis auf `ANLEITUNG.md`.
AK8: teilweise belegt — Ich habe die Befehle der Anleitung am Probeausschnitt im Scratchpad laufen lassen (`skripte/probe.sh`), alle ohne Absturz. `kacheln` ergibt Teilkacheln und `T0.png` bytegleich zum Projekt. Die Vorstufe (GPU) ist übersprungen. Danach liefen `pruefen` → ok, `eingriff klasse` → ok, `zusammentragen` (Befund Nähte, Exit 1), `naht` und `seite` → Seite geschrieben. Die Karte von A nachgerechnet: `labels.tif` ist bytegleich, 309 Nahtverstöße. Die Ansicht von `T0.html` auf dem Desktop fehlt (kein Foto).
Prüfungen:
PY -B -m unittest discover -s tests -t . (Arbeitskopie) → Ran 99 tests, OK
PY -I tools/pruefe_kategorien.py kategorien.json → ok
PY -B -m landseg seite --manifest T0/manifest.json --ziel T0/T0.html --kategorien T0/c-feste-liste/kategorien-c.json (Projekt) → 3 Fassungen je 4 × pruefen ok, Seite 8104 KiB
PY -I tools/pruefe_kategorien.py T0/{a,b,c}-…/kategorien-{a,b,c}.json (Projekt) → 3 × ok
PY -B -m landseg naht … a-alles-frei/zusammen/labels.tif → FEHLER (309 Verstöße, erwartet)
PY -B -m landseg pruefen … a-alles-frei/zusammen --form 1000x1000 → 607 Segmente, 20 nicht zusammenhängend (erwartet)
skripte/probe.sh → siehe AK8
Fotos: keine (Browser-Erweiterung in dieser Sitzung nicht verfügbar)
Aufrufe: rund 50 von 120
Nicht geprüft:
- Ansicht von `T0/T0.html` im Browser (AK2, AK8): Die Claude-in-Chrome-Erweiterung war in dieser Sitzung nicht verfügbar.
- Das Übergabe-Projekt ist aus dem Commit bb7dd84 des Zweigs gebaut, nicht aus `main` nach dem Einreihen. `main` steht noch auf 0cd61ea, der Baum ist nach dem Einreihen derselbe. Zieht `main` vorher weiter, muss der Code-Schnappschuss erneuert werden: `git archive`, dann `skripte/baue_uebergabe.py` und `seite` wie in AK3.
- Push, Anlegen des Remotes und Einladung von Victor: nicht Teil dieses Laufs.
Einstieg: stimmte. Abweichung: Die Reihenfolge und die Startfassung kommen allein aus `seite.json` (`seite.js:39-46`), am Code war nichts zu ändern. Die Karten von C (bisher A) und B liegen unter `kern500/urteil-stand/` und `fassung-b/urteil-stand/`, nicht unter `vorstufe/` (Bericht `-3`).
Technische Entscheidungen:
- `seite.json` nimmt die Ordner des Übergabe-Projekts als Standard: `a-alles-frei/` mit `kategorien-a.json`, `b-kategorien-frei/` mit `kategorien-b.json`, `c-feste-liste/` mit der Liste des Aufrufs. So baut sich die Seite im Projekt ohne eigene Fassungsliste. Folge: Die reine Vorstufe zeigt die Seite nicht mehr von selbst. Das README erklärt, wie man sie als Ausgang nach `c-feste-liste/` kopiert oder per `--einstellungen` zeigt.
- In den Beispielen des README und in `vorlagen/README.md` steht jetzt der Platzhalter `<ausschnitt>` statt `../daten/landseg/T0/kern500`. Sonst hätte der Code-Schnappschuss AK4 verletzt, und der Ordner `kern500` sagt Victor nichts.
- Die Karte je Fassung ist der Stand, den die Seite bisher zeigte: `urteil-stand` für B und C, `stand` für A. Die Wunsch-Datei zählt `urteil-stand` zu den Zwischenständen. Es ist aber genau die „Karte“, die AK3 verlangt: Grenzen der Vorstufe mit Klassen aus dem Urteil.
- Pfade in den Dateien sind jetzt relativ zu `T0/`, ohne `C:/Users/…`. Bildpfade in `urteil.json` zeigen weiter auf nicht mitgelieferte Zwischenbilder. Die Anleitung sagt das.
- Das Manifest nennt bei `quelle.bild` nur den Dateinamen des Originals, mit dem Hinweis „nicht mitgeliefert“.
- Gesamtbilder habe ich selbst gezeichnet (Kerne zusammengesetzt, Farbe der feinsten Klasse, je allein und zu 55 % über dem Luftbild). Für A habe ich geprüft, dass das Bild gleich `zusammen/labels.tif` ist.
- Das README des Projekts hat oben einen Übergabe-Kopf bekommen, nur in der Kopie. Das Code-Repo verweist nicht auf die Anleitung.
- Das Übergabe-Projekt liegt außerhalb von Arbeitskopie und Berichtsordner, wie der Arbeitsauftrag es verlangt (`daten/landseg/uebergabe/landseg-t0/`, im Basis-Repo durch `/daten/*` ausgenommen). Die Quellen unter `daten/landseg/T0/` sind nur gelesen.
- Die Bau-, Zähl- und Probeskripte liegen in `skripte/`, damit das Projekt nach einer Nachbesserung neu gebaut werden kann.
Nacharbeit im Hauptordner:
- `C:/Users/Phil/Developement/.claude/hoheit.md`, Abschnitt „Victor“: In der Zeile zu den abgeleiteten Landseg-Daten `daten/landseg/` ergänzen, außerdem das Übergabe-Projekt `daten/landseg/uebergabe/landseg-t0`, den Namensraum `landseg:` und die Hoheit Bereich victor.
- `daten/README.md`: Abschnitt zu `landseg/uebergabe/landseg-t0/` (eigenes Git-Repo, Ziel `PhilMeyer1/landseg-t0` privat).
- Profil `BASIS/.claude/repos/landseg.md`: Die Fassungen heißen jetzt A Alles frei, B Kategorien frei, C Feste Liste, mit Ordnern `a-alles-frei/`, `b-kategorien-frei/` und `c-feste-liste/` als Standard von `seite.json`.
- Nach dem Einreihen: `gh repo create PhilMeyer1/landseg-t0 --private`, Remote setzen, `git -C <Projekt> push -u origin main`; Victor einladen, sobald sein Kontoname bekannt ist.
- Kommentare des Nutzers aus der alten Seite `T0-urteil.html` tragen „fassung A“ für die feste Liste. Wer sie mit neuen Seiten verwendet, muss A in C übersetzen.
Abräumen: Arbeitskopie bleibt bis zum Einreihen; keine Dauerprozesse; Probeordner nur im Scratchpad
Lagebild: fehlt (landseg hat kein `LAGEBILD.md`)
Erkenntnisse fürs Profil:
- `einstellungen/seite.json` erwartet die Fassungsordner `a-alles-frei/`, `b-kategorien-frei/` und `c-feste-liste/` neben dem Manifest. `vorstufe/` allein zeigt die Seite nicht mehr, sie bricht dann mit „keine Fassung mit Daten“ ab.
- Der Geheimnisschutz-Hook blockt Bash-Befehle, deren Muster `daten/landseg` enthält (er meldet `daten/zugaenge/`). Für solche Suchen das Grep-Werkzeug nehmen.
- `zusammentragen` und `naht` enden bei Nahtverstößen mit Exit 1. Das ist ein Befund, kein Absturz.
- Das Übergabe-Projekt `daten/landseg/uebergabe/landseg-t0/` ist ein eigenes Git-Repo ohne Profil. Es wird aus dem Code-Repo (`git archive`) und `daten/landseg/T0/` gebaut (`wuensche/2026-11-17-landseg-uebergabe/skripte/baue_uebergabe.py`).
Abweichungen vom Zielbild:
- landseg/seite.py:60 — vorgefunden, schon in landseg-test-t0-3 gemeldet: Die Seite liest das Luftbild mit `_lese_bild` statt `naht.lese_bild`. Ihr Nähte-Schalter zeigt deshalb für A 124 statt 309 Verstöße. Die Anleitung nennt das, im Code ist nichts geändert. Sauber wäre ein gemeinsamer Leser.
Einreihen (Skript): eingereiht bb7dd84 feat(seite): reorder versions to A all free, B free categories, C fixed list in C:/Users/Phil/Developement/Victor/landseg (main); Prüfung nach Risiko (ohne Prüfschleuse, keine Zeile schnell: im Profil); voll grün (2 s); volle Prüfung offen (vermerkt in C:/Users/Phil/Developement/Victor/landseg/.git/wunsch-einreihen/pruefung-offen.jsonl); Abräumen WEG
