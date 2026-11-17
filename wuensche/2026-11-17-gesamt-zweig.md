# Gesamtprojekt: Hinweis „eigener Zweig“ für Victor und Klartext-Zeilen in den Commits des Bauwerkzeugs

Kurzname: gesamt-zweig | Datum: 2026-11-17 | Größe: <klein|mittel|gross> | Bereich: victor | Repos: landseg | Status: eingereiht

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

Aus der Freigabe des Nutzers (2026-11-17, „Mit Vollzugriff einladen (Empfohlen)“, Option: „ich sage ihm in der Anleitung, dass er auf einem eigenen Zweig arbeiten soll“) und der globalen Commit-Regel (Klartext-Zeilen in jedem Commit mit echter Änderung).

1. Die Einstiegsseite des Gesamtprojekts (Vorlage im Repo landseg unter gesamt/, README) bittet Victor, auf einem eigenen Zweig zu arbeiten und Änderungen per Pull-Request zusammenzuführen statt direkt auf main hochzuladen; mit den zwei, drei Befehlen dafür.
2. `tools/gesamt_projekt.py bauen` schreibt seine Commits im Gesamtprojekt (Abgleich der Kopien, Übernahme von programm/ und unterlagen/) mit den Zeilen `Klartext-Titel:` und `Klartext:` (Deutsch, einfache Sprache, ohne Fachwörter), damit künftige Commits der Regel folgen; bestehende Commits bleiben unverändert.
Hochladen (bauen am Ziel, Push) macht die Hauptsession danach.

## Fragen

<Prüfer: nur Fragen, die ohne Code-Wissen beantwortbar sind; jede mit Empfehlung>

## Entscheidungen

<Antworten des Nutzers mit Datum. Der Prüfer übernimmt beim Klären die Zeilen aus
`entscheidungen.md`, die für diesen Wunsch gelten, je mit „(aus entscheidungen.md, <Datum>)",
oder schreibt „entscheidungen.md: nichts für diesen Wunsch".>

## Arbeitsauftrag

### Abnahmekriterien

AK1: Die Einstiegsseite des Gesamtprojekts sagt Victor, dass er auf einem eigenen Zweig arbeitet und per Pull-Request zusammenführt, mit den Befehlen dafür — prüfbar: Ansicht README.md im Gesamtprojekt nach `gesamt_projekt.py bauen`
AK2: Jeder neue Commit, den `gesamt_projekt.py bauen` im Gesamtprojekt anlegt, trägt je eine Zeile `Klartext-Titel:` (bis 80 Zeichen) und `Klartext:` (bis 250 Zeichen) — prüfbar: Verhalten: `bauen` an einer Probe-Kopie, `git log -1 --format=%B` zeigt beide Zeilen; Tests grün

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
