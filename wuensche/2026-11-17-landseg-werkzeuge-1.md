# Teil 1 von landseg-werkzeuge: Gerüst, kacheln, eingriff, pruefen

Kurzname: landseg-werkzeuge-1 | Datum: 2026-11-17 | Größe: mittel | Bereich: victor | Repos: landseg | Status: eingereiht | Mutterwunsch: landseg-werkzeuge

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

Teil 1 des Mutterwunschs `landseg-werkzeuge` (`wuensche/2026-11-17-landseg-werkzeuge.md`), Zeile aus dessen Teile-Liste:

1. Gerüst, kacheln, eingriff, pruefen — Umsetzer — Repo: landseg — Vorbedingungen: keine — nach: – — AK 1, 2 — Repo mit Paket, Tests und `README.md` steht; T0 lässt sich kacheln, Eingriffe und Prüfung arbeiten lückenlos

## Fragen

keine (siehe Mutterwunsch)

## Entscheidungen

siehe Mutterwunsch

## Arbeitsauftrag

### Abnahmekriterien

AK1: Aus dem Testfenster T0 (Kachel 5236-56, x 2000, y 2400, 1000 × 1000 px) entstehen vier Teilkacheln (Kern 500 × 500, Kontextrand 64 px) mit einem Manifest (relative Pfade, Georeferenz); die Kerngröße ist ein Parameter (250 funktioniert ebenso) — prüfbar: Befehl `kacheln` auf T0 mit 500 und mit 250, Manifest lesen, Kerne ergeben zusammen genau 1000 × 1000
AK2: Alle Eingriffe (verschmelzen, teilen entlang Linie, Grenze verschieben, Klasse setzen, Polygon zuweisen) arbeiten auf der Label-Karte und lassen sie lückenlos; `pruefen` meldet H × W ohne 0, Zusammenhang je ID, gültige Klassen aus `kategorien.json` und schlägt bei einer absichtlich eingefügten Lücke fehl — prüfbar: Tests mit synthetischer Label-Karte, auch Gegenprobe

Einstieg, Bausteine, Entscheidungen: siehe Mutterwunsch

Vorbedingungen: keine
