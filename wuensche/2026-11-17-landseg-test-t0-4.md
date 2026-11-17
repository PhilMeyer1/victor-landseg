# Teil 4 von landseg-test-t0: Umsetzen, Zusammentragen und Korrektur

Kurzname: landseg-test-t0-4 | Datum: 2026-11-17 | Größe: mittel | Bereich: victor | Repos: landseg | Status: bereit | Mutterwunsch: landseg-test-t0 | Ergebnis: ohne Commit

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

Teil 4 des Mutterwunschs `landseg-test-t0` (`wuensche/2026-11-17-landseg-test-t0.md`), Zeile aus dessen Teile-Liste:

4. Umsetzen, Zusammentragen und Korrektur — Workflow (ohne Commit) — Repo: landseg — Vorbedingungen: keine — Aufruf-Budget: 200 — nach: 3 — AK 4, 5, 6 — Skript der Hauptsession über `wunsch:workflow`, Modelle nach „Bausteine und Fallen": Karten von A und B umgesetzt, zusammengetragen, Naht geprüft, bei A die Kommentare des Nutzers umgesetzt.

## Fragen

keine (siehe Mutterwunsch)

## Entscheidungen

siehe Mutterwunsch

## Arbeitsauftrag

### Abnahmekriterien

AK4: (A) Je Teilkachel liegt eine umgesetzte Label-Karte vor, die nur im Kern geändert wurde und lückenlos ist (H × W, kein 0), und die zusammengetragene Karte von T0 hat 1000 × 1000 Bildpunkte ohne 0, jede ID genau eine Klasse und ein zusammenhängendes Gebiet, die Nahtprüfung meldet keinen offenen Verstoß — prüfbar: `PY -m landseg pruefen` je Teilkachel, Vergleich mit der Vorstufe im Kontextrand (bildpunktgleich), `PY -m landseg zusammentragen --datei zusammentragen.json` und `PY -m landseg naht`
AK5: (A) Die Korrekturrunde setzt genau die Kommentare des Nutzers um und lässt alles andere bildpunktgleich; Unklares steht unter `offen` — prüfbar: Vergleich der Karten Runde 0 und Runde 1 außerhalb der kommentierten Segmente, `pruefen` ok
AK6: (B) Fassung B liegt vor: je Teilkachel ein Urteil aus vier Viertel-Abgaben, das jedes Kernsegment einzeln mit selbst benannter und gestufter Klasse enthält und je Viertel die angesehenen Bilder belegt, eine zusammengetragene Karte von T0 (1000 × 1000 ohne 0, lückenlos, Naht ohne offenen Verstoß) und eine eigene, über alle Viertel vereinheitlichte Kategorienliste `kategorien-b.json` im Format von `kategorien.json` (Codes, Namen, Eltern, Ebenen, Farben), die die Prüfseite lädt — prüfbar: `PY -I tools/pruefe_kategorien.py <Pfad>/kategorien-b.json`, `PY -m landseg pruefen --kategorien <Pfad>/kategorien-b.json` je Teilkachel, Lesen `urteil.json` gegen `segmente.json`, `zusammentragen`, `naht`

Einstieg, Bausteine, Entscheidungen: siehe Mutterwunsch

Vorbedingungen: keine

Aufruf-Budget: 200
