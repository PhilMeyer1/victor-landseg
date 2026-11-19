# Auf dem Bild von 1968 die als „unklar“ bewerteten Garten-Stellen als Garten mit Vermerk unsicher eintragen und die Prüfseite neu bauen

Kurzname: garten-h0-unsicher | Datum: 2026-11-19 | Größe: klein | Bereich: victor | Repos: landseg | Status: eingereiht (ohne Commit) | Ergebnis: ohne Commit

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

Antwort des Nutzers 2026-11-18 auf „Wie soll es auf dem Bild von 1968 sein?“: „Unklare als Garten, unsicher“.

Präzisierung: In landseg-garten-3 nannten die Bestätiger auf H0 65 Kandidaten „unklar“ (A 35, B 17, C 13; je Einheit `wuensche/2026-11-18-landseg-garten-3/einheiten/H0-*/entscheid.json`). Diese werden in `daten/landseg/H0/<fassung>/<tk>/segmente.json` zur Garten-Klasse der Fassung (C 3.6, A/B die eigene Garten-Klasse unter Dauergrünland) mit `sicher: false` und Grund „Garten wahrscheinlich, auf SW nicht sicher (Nutzer 2026-11-18)“, per `eingriff … stapel` (klasse_setzen), Sicherung vorher. Danach pruefen (A/B mit Liste der Fassung bzw. --frei), zusammentragen, einigung messen (offen 0, sonst nach vorlagen/einigung.md klären), Prüfseite `daten/landseg/seiten/T0-H0.html` und Gesamtprojekt lokal neu wie in landseg-garten-4; kein Hochladen. Datenlauf ohne Commit im Repo landseg (Ergebnis: ohne Commit).

## Fragen

<Prüfer: nur Fragen, die ohne Code-Wissen beantwortbar sind; jede mit Empfehlung>

## Entscheidungen

<Antworten des Nutzers mit Datum. Der Prüfer übernimmt beim Klären die Zeilen aus
`entscheidungen.md`, die für diesen Wunsch gelten, je mit „(aus entscheidungen.md, <Datum>)",
oder schreibt „entscheidungen.md: nichts für diesen Wunsch".>
- 2026-11-19 (Nutzer): AK3 nicht durch die Abnahme belegt (keine Browser-Erweiterung); der Nutzer sieht die Seite selbst durch („Ich sehe sie jetzt durch“) — seine Durchsicht ist der Beleg für AK3.

## Arbeitsauftrag

### Abnahmekriterien

AK1: Auf H0 tragen alle 65 als „unklar“ bewerteten Garten-Kandidaten die Garten-Klasse ihrer Fassung mit sicher: false; Zahl der Garten-Segmente je Fassung steht im Bericht — prüfbar: Verhalten (Zählung aus segmente.json gegen die entscheid.json der H0-Einheiten)
AK2: pruefen je Teilkachel ok, einigung messen offen 0 für H0 — prüfbar: Verhalten (Befehle und Logs)
AK3: Die Prüfseite T0-H0 zeigt auf H0 die neuen Gärten, als unsicher markiert — prüfbar: Ansicht (Seite über 127.0.0.1)

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

## Nachweis

- 2026-11-19: Datenlauf ohne Commit im Repo (Lauf 20261119a, abgenommen): 65 unklare Garten-Kandidaten auf H0 als Garten mit sicher: false eingetragen, pruefen und einigung messen ok, Prüfseite T0-H0 neu gebaut (11:38); AK3 per Durchsicht des Nutzers belegt („passt alles“, 2026-11-19).
