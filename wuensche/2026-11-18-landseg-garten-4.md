# Teil 4 von landseg-garten: Seite und Gesamtprojekt neu bauen

Kurzname: landseg-garten-4 | Datum: 2026-11-18 | Größe: mittel | Bereich: victor | Repos: landseg | Status: eingereiht (ohne Commit) | Mutterwunsch: landseg-garten | Ergebnis: ohne Commit

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

Teil 4 des Mutterwunschs `landseg-garten` (`wuensche/2026-11-18-landseg-garten.md`), Zeile aus dessen Teile-Liste:

4. Seite und Gesamtprojekt neu bauen — Umsetzer — Repo: landseg — Vorbedingungen: keine — nach: 3 — AK 7, 8 — Seite und Gesamtprojekt zeigen Garten (ohne Hochladen)

## Fragen

keine (siehe Mutterwunsch)

## Entscheidungen

siehe Mutterwunsch

- Hauptsession 2026-11-18, Nacharbeit aus Teil 3 (Workflow wf_230c0b9f-a95, Bericht `wuensche/2026-11-18-landseg-garten-3/ergebnis.md`), vor dem Bau der Seite zu erledigen und im Bericht zu belegen:
  1. Freie Listen A und B von T0 und H0: `pruefen --frei` meldet den Garten-Listenfehler (Garten fehlt unter Dauergrünland bzw. steht unter „2 Hof und Garten“); Teil 3 hat Klassen umbenannt („Dauergrünland (alter Name)“). Listen so ordnen, dass Garten nach L14 sauber unter der Dauergrünland-Klasse der Fassung steht, ohne Behelfsnamen; die Segmente behalten ihre Bedeutung; `pruefen --frei` je Liste ok. Listen vorher: `garten-3/listen-vorher/`.
  2. `zusammentragen` meldet nach dem Vergröbern von H0 und bei T0 FEHLER (Nahtverstöße T0 309/312/312, H0 A 163, B 141, C 105, dazu „nicht zusammenhängende Segmente über Kerne“). Zerfallene Segmente beheben wie in Teil 4 von landseg-historisch (`wuensche/2026-11-18-landseg-historisch-4/skripte/zerfall_beheben.py`), bis 0 zerfallen; Nahtverstöße des ID-Teils bleiben bekannt offen (eigener Wunsch „Grenzlinien an den Nähten“), nur zählen.
  3. Zwei offene Einigungspaare (T0 B 1, T0 C 1) nach `vorlagen/einigung.md` klären (Garten auf nur einer Nahtseite), danach `einigung messen` offen 0.
  4. T0 B und C haben neu angelegte `zusammentragen.json` (nach Muster T0 A): prüfen, dass sie richtig sind.
  Danach Seite T0+H0 (`daten/landseg/seiten/T0-H0.html`, wie Teil 4 von landseg-historisch) und Gesamtprojekt lokal neu; kein Hochladen.
## Arbeitsauftrag

### Abnahmekriterien

AK7: Die Seite `T0-H0.html` zeigt „Garten“ in Legende, Ebenenauswahl und bei den Segmenten mit eigener Farbe, in allen Fassungen und beiden Bildern; das Gesamtprojekt victor-landseg ist neu gebaut, nicht hochgeladen — prüfbar: Ansicht Seite T0-H0, Segmentliste mit Garten, Desktop; `tests/test_seite.py`, `tests/test_gesamt_projekt.py`
AK8: Weg des Nutzers: Auf der Seite in T0 ein Haus mit Garten wählen und sehen, dass der Hausgarten als „Garten“ (Dauergrünland) gelistet ist, in jeder Fassung — prüfbar: Ansicht Seite am laufenden Stand, Desktop

Einstieg, Bausteine, Entscheidungen: siehe Mutterwunsch

Vorbedingungen: keine

## Nachweis

- 2026-11-19: Datenlauf ohne Commit im Repo (Lauf 20261118o): freie Listen A/B mit Garten unter Dauergrünland (pruefen --frei ok), zerfallene Segmente behoben (0), Einigung offen 0, Seite daten/landseg/seiten/T0-H0.html und Gesamtprojekt lokal neu gebaut und geprüft, nicht hochgeladen; T0-Ergebnisse in der Übergabe als 297ae4a committet. Bericht wuensche/2026-11-18-landseg-garten-4/bericht-landseg.md.
