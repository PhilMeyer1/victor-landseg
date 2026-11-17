# Teil 1 von landseg-test-t0: Vorstufe, Gruppenbildung und Aufträge

Kurzname: landseg-test-t0-1 | Datum: 2026-11-17 | Größe: mittel | Bereich: victor | Repos: landseg | Status: eingereiht (ohne Commit) | Mutterwunsch: landseg-test-t0 | Ergebnis: ohne Commit

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

Teil 1 des Mutterwunschs `landseg-test-t0` (`wuensche/2026-11-17-landseg-test-t0.md`), Zeile aus dessen Teile-Liste:

1. Vorstufe, Gruppenbildung und Aufträge — Umsetzer (ohne Commit) — Repo: landseg — Vorbedingungen: keine — Aufruf-Budget: 150 — nach: – — AK 1 — Kacheln und Vorstufe von T0 für A, Kopien für B und C, `gruppen.json` und alle Auftragsdateien samt Bildern je Segment unter `$D/gruppen/`.

## Fragen

keine (siehe Mutterwunsch)

## Entscheidungen

siehe Mutterwunsch

## Arbeitsauftrag

### Abnahmekriterien

AK1: (A) Die Vorstufe liegt für alle vier Teilkacheln vor, mit gemessener Segmentzahl je Teilkachel; Originale wie Stitcher sind unverändert; liegt die Zahl im Kern über etwa 80 Segmenten, wird vor dem Urteil mit `--kern 250` neu gekachelt (das steht in der Messung; r0c0 liegt mit 154 schon darüber, die Entscheidung dazu steht in der Messung) — prüfbar: `PY -m landseg kacheln` und `PY -B -m landseg vorstufe --manifest ../daten/landseg/T0/kern500/manifest.json`, `PY -m landseg pruefen` je Teilkachel, `git -C` status in landseg und stitcher, Lesen der Messzeilen

Einstieg, Bausteine, Entscheidungen: siehe Mutterwunsch

Vorbedingungen: keine

Aufruf-Budget: 150

## Nachweis

- 2026-11-17: Datenlauf ohne Commit: Kacheln frisch nachgekachelt und bytegleich zu kern500 (kacheln-T0.log), Vorstufe aller 4 Teilkacheln bestätigt (vorstufe-T0.log), pruefen 12/12 ok für A, B, C (pruefen-T0.log), Kopien B/C bytegleich (kopien-messung.json), 32 Viertel-Aufträge A/B + 4 C + 4 Zweitagent + 1 Vereinheitlichung mit gruppen.json und Viertelbildern (viertel-bau.log); 641 Segmente je Fassung; alte Einzelbilder gelöscht.
