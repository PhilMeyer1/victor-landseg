# Teil 2 von landseg-werkzeuge: Vorstufe

Kurzname: landseg-werkzeuge-2 | Datum: 2026-11-17 | Größe: mittel | Bereich: victor | Repos: landseg | Status: eingereiht | Mutterwunsch: landseg-werkzeuge

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

Teil 2 des Mutterwunschs `landseg-werkzeuge` (`wuensche/2026-11-17-landseg-werkzeuge.md`), Zeile aus dessen Teile-Liste:

2. Vorstufe — Umsetzer — Repo: landseg — Vorbedingungen: keine — Aufruf-Budget: 100 — nach: 1 — AK 3 — Übersegmentierung, SAM 3 und Semantik-argmax liefern an einer echten T0-Teilkachel eine lückenlose Vorbelegung; Segmentzahl ist gemessen

## Fragen

keine (siehe Mutterwunsch)

## Entscheidungen

siehe Mutterwunsch

## Arbeitsauftrag

### Abnahmekriterien

AK3: Die Vorstufe (Übersegmentierung, SAM 3 mit Text je Kategorie, Semantik-argmax) läuft auf einer echten T0-Teilkachel und liefert `labels`, `segmente.json` (ID, Klasse fein/grob, Herkunft, Sicherheit) und Kandidatenliste; `pruefen` meldet H × W ohne 0; die Zahl der Segmente und der Anteil `sicher: nein` dieser Teilkachel stehen im Bericht — prüfbar: Befehl `vorstufe` und `pruefen` an der Teilkachel (ein Lauf, kurz), Lesen der Messzeile im Bericht

Einstieg, Bausteine, Entscheidungen: siehe Mutterwunsch

Vorbedingungen: keine

Aufruf-Budget: 100
