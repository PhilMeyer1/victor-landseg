# Teil 2 von landseg-historisch: Ausschnitt H0: kacheln, Vorstufe, Aufträge

Kurzname: landseg-historisch-2 | Datum: 2026-11-18 | Größe: mittel | Bereich: victor | Repos: landseg | Status: eingereiht (ohne Commit) | Mutterwunsch: landseg-historisch | Ergebnis: ohne Commit

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

Teil 2 des Mutterwunschs `landseg-historisch` (`wuensche/2026-11-18-landseg-historisch.md`), Zeile aus dessen Teile-Liste:

2. Ausschnitt H0: kacheln, Vorstufe, Aufträge — Umsetzer (ohne Commit) — Repo: landseg — Vorbedingungen: keine — Aufruf-Budget: 120 — nach: – — AK 2 — H0 aus dem Scan geschnitten, Vorstufe aller vier Teilkacheln gemessen, Kopien für B und C, Auftragsdateien und Bilder im Berichtsordner, Hash der Originale unverändert.

## Fragen

keine (siehe Mutterwunsch)

## Entscheidungen

siehe Mutterwunsch

## Arbeitsauftrag

### Abnahmekriterien

AK2: Der Ausschnitt H0 ist gekachelt (1000 × 1000, vier Teilkacheln), die Vorstufe liegt für alle vier vor, `pruefen` ist ok, die Zahl der Segmente je Teilkachel ist gemessen (liegt sie im Kern über etwa 80, steht die Entscheidung zur Kerngröße in der Messung); die Originale unter `daten/luftbilder/` sind byteweise unverändert — prüfbar: `PY -m landseg kacheln` und `PY -B -m landseg vorstufe --manifest <H0>/manifest.json`, `PY -m landseg pruefen` je Teilkachel, Vergleich der SHA-256 der zwei Scans vorher/nachher

Einstieg, Bausteine, Entscheidungen: siehe Mutterwunsch

Vorbedingungen: keine

Aufruf-Budget: 120

## Nachweis

- 2026-11-18: Datenlauf ohne Commit: Ausschnitt H0 aus dem Scan 1968 geschnitten, Vorstufe der vier Teilkacheln, Kopien für B und C, Aufträge unter wuensche/2026-11-18-landseg-historisch-2/auftraege.json; Daten unter Victor/daten/landseg/H0/ (136 MB), Originale unverändert.
