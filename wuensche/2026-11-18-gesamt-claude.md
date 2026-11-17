# Gesamtprojekt victor-landseg: CLAUDE.md, die beim Öffnen mit Claude Code sofort die Ergebnis-Ansicht im Browser öffnet, und Prüfung, dass alles da ist und funktioniert

Kurzname: gesamt-claude | Datum: 2026-11-18 | Größe: <klein|mittel|gross> | Bereich: victor | Repos: landseg | Status: eingereiht

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

„stelle sicher, dass alles da ist und funktioniert und außerdem, dass wenn Victor das Repo mit Claude aufmachen lässt der ihm dann direkt im Browser die Ansicht öffnet mit der die Ergebnisse dann eingesehen werden können. Klare Anweisung an Claude Code"

Präzisierung:
- Das Gesamtprojekt (lokal C:/Users/Phil/Developement/Victor/daten/gesamt/victor-landseg, GitHub PhilMeyer1/victor-landseg, gebaut von `landseg/tools/gesamt_projekt.py bauen` aus den Vorlagen unter `landseg/gesamt/`) bekommt im Wurzelordner eine `CLAUDE.md` (Vorlage unter `landseg/gesamt/`, von `bauen` kopiert und von `pruefen` verlangt). Sie weist Claude Code klar an: Zu Beginn jeder Session in diesem Projekt (erste Antwort, ohne Rückfrage) die Ergebnis-Ansicht `ergebnisse/T0.html` im Standard-Browser öffnen, mit dem passenden Befehl je Betriebssystem (Windows `start "" "ergebnisse/T0.html"` bzw. PowerShell `Start-Process`, macOS `open`, Linux `xdg-open`), prüfen, dass der Befehl ohne Fehler lief, und Victor in wenigen Sätzen sagen, was er sieht (Fassungen A Alles frei, B Kategorien frei, C Feste Kategorienliste; Umschalter oben, Teilkacheln, Segment anklicken, Kommentare und Export) und wo er weiterliest (README, ANLEITUNG). Fehlt die Datei (z. B. unvollständiger Download), das sagen und nicht raten. Dazu kurz: Projekt-Aufbau, was nur gelesen werden soll (Originaldaten, Ergebnisse), Arbeiten auf eigenem Zweig, wie die Werkzeuge laufen (Python-Umgebung laut ANLEITUNG). Die älteren Seiten unter daten/…/seite/ (alte Benennung) als „Arbeitsstand, alte Benennung“ kennzeichnen, damit Claude nicht die falsche öffnet.
- Alles da und funktioniert: ein frischer Klon von GitHub (in einen eigenen Prüfordner, nicht der Arbeitsordner) enthält alle Dateien, die README, ANLEITUNG und CLAUDE.md nennen; `ergebnisse/T0.html` öffnet ohne Fehler und schaltet A, B, C um und zeigt die vier Teilkacheln; die Tests von `programm/` sind grün; `pruefen` ohne Befund. Gefundene Lücken werden behoben.
- Neu bauen und Hochladen macht die Hauptsession nach dem Einreihen.

## Fragen

<Prüfer: nur Fragen, die ohne Code-Wissen beantwortbar sind; jede mit Empfehlung>

## Entscheidungen

<Antworten des Nutzers mit Datum. Der Prüfer übernimmt beim Klären die Zeilen aus
`entscheidungen.md`, die für diesen Wunsch gelten, je mit „(aus entscheidungen.md, <Datum>)",
oder schreibt „entscheidungen.md: nichts für diesen Wunsch".>

## Arbeitsauftrag

### Abnahmekriterien

AK1: Im Gesamtprojekt liegt im Wurzelordner eine CLAUDE.md, die Claude Code anweist, zu Beginn jeder Session ohne Rückfrage `ergebnisse/T0.html` im Standard-Browser zu öffnen (Befehl je Betriebssystem), den Erfolg zu prüfen und Victor kurz zu sagen, was er sieht und wo er weiterliest; ohne Datei: offen sagen — prüfbar: Lesen CLAUDE.md im frisch gebauten Gesamtprojekt; Verhalten: der dort genannte Windows-Befehl öffnet die Seite
AK2: Ein frischer Klon von PhilMeyer1/victor-landseg bzw. der frisch gebaute Stand enthält alles, was README, ANLEITUNG und CLAUDE.md nennen, `ergebnisse/T0.html` öffnet ohne Fehler, zeigt die Fassungen A Alles frei, B Kategorien frei, C Feste Kategorienliste und die vier Teilkacheln, die Tests von programm/ sind grün und `gesamt_projekt.py pruefen` meldet ok — prüfbar: Ansicht ergebnisse/T0.html (über lokalen Webserver mit der Browser-Erweiterung), Verhalten: Tests und pruefen

## Teile

<Nur bei Größe gross, vom Prüfer: nummerierte Liste, je Teil
„Name — Umsetzer|Workflow [— Halt: Durchsicht|Wahl|Freigabe] — nach: –|<Nummern> — AK <Nummern> — ein
Satz, was dann fertig ist". `Halt:` nur, wenn der Nutzer vor dem Einreihen durchsieht, wählt oder freigibt.
„nach" nennt die Teile, die vorher eingereiht sein müssen; Teile ohne gemeinsame Stellen laufen
parallel. Die Hauptsession legt je Teil einen eigenen Wunsch <kurzname>-N an.>

## Varianten

<Nur bei Größe mittel mit sichtbarer Entwurfsfrage, vom Prüfer: „a: …" und „b: …", je ein bis
zwei Sätze, was der Nutzer sehen wird. Mit Entwurf zeigt er beide, der Nutzer wählt bei der
Freigabe; ohne Entwurf bauen zwei Umsetzer parallel. Die Wahl steht danach unter „Entscheidungen".>

## Entwurf

<Vom Prüfer beim Klären, nur bei sichtbaren Oberflächen: erste Zeile „Stufe: nein — <Grund>",
„Stufe: skizze", „Stufe: ausgearbeitet" oder „Stufe: nach F<n>"; darunter, was der Entwurf
zeigt: Ansichten, Zustände, Desktop/Handy, Nachbarn, Beispieldaten, Varianten. Der Workflow
`wunsch:entwurf` zeichnet daraus fünf Entwürfe nach `entwurf/` im Berichtsordner; die Freigabe des
Nutzers steht danach unter „Entscheidungen".>
