# Teil 3 von landseg-historisch: Urteile A, B, C, Gegenprobe und Einigung

Kurzname: landseg-historisch-3 | Datum: 2026-11-18 | Größe: mittel | Bereich: victor | Repos: landseg | Status: eingereiht (ohne Commit) | Mutterwunsch: landseg-historisch | Ergebnis: ohne Commit

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

Teil 3 des Mutterwunschs `landseg-historisch` (`wuensche/2026-11-18-landseg-historisch.md`), Zeile aus dessen Teile-Liste:

3. Urteile A, B, C, Gegenprobe und Einigung — Workflow (ohne Commit) — Repo: landseg — Vorbedingungen: keine — Aufruf-Budget: 300 — nach: 2 — AK 3, 4 — Skript der Hauptsession über `wunsch:workflow`: 4 Agents je Fassung (B plus 1), Gegenprobe 1, Zusammentragen, Einigung und Naht je Fassung; Karten von H0 für A, B, C.

## Fragen

keine (siehe Mutterwunsch)

## Entscheidungen

siehe Mutterwunsch

## Arbeitsauftrag

### Abnahmekriterien

AK3: Jede der drei Fassungen A, B, C hat je Teilkachel ein Urteil, das jedes Kernsegment genau einmal enthält, jeden Agent mit angesehenen Bildern belegt (je Agent zuerst der ganze Ausschnitt, dann seine Teilkachel) und offen und nicht geprüft nennt; B und C haben eine eigene, prüfbare Kategorienliste — prüfbar: Lesen `urteil.json` gegen `segmente.json` je Teilkachel, `PY -I tools/pruefe_kategorien.py <Pfad>/kategorien-<b|c|a>.json`
AK4: Je Fassung liegt die zusammengetragene Karte von H0 vor (1000 × 1000, kein 0, jede ID genau eine Klasse und zusammenhängend), die Einigung an den Nähten ist gelaufen (Stellen, geeinigt, als unsicher markiert, `messen` je Fassung im Bericht), die Nahtprüfung meldet keinen offenen Verstoß — prüfbar: `PY -m landseg pruefen`, `zusammentragen`, `PY -B -m landseg einigung messen --manifest <H0>/manifest.json`, `PY -m landseg naht`

Einstieg, Bausteine, Entscheidungen: siehe Mutterwunsch

Vorbedingungen: keine

Aufruf-Budget: 300

## Nachweis

- 2026-11-18: Workflow wf_62f47ff3-c51 (Lauf 20261118i, Skript wuensche/2026-11-18-landseg-historisch-3/workflow.js): 71 Agents, 0 Fehler, 11,41 Mio. Tokens, 104 min. Grobe Vorstufe 465 Kernsegmente (Teil-2-Einstellungen Lauf 1, feine Fassung als *-fein gesichert, Hash der Scans gleich). Urteile 40/40 ok (8 Viertel unnötig nachgeholt: Segmentzahl durch Nachsegmentieren geändert), Eingriffe B 137, C 110. Vereinheitlichung B 41 Klassen. Zusammengeführt A 1823, B 708, C 457 Segmente. Einigung 3 Runden (41 Bündel, 465 Paare): offen 0 in A, B, C; unsicher A 34, B 17, C 13; geklärt A 179, B 136, C 86. Abweichung AK4: Nahtverstöße (ID-Teil) A 187, B 158, C 126 offen, weil jede Teilkachel eigene IDs hat und eingriff keine fremde ID übernimmt (wie bei T0); pruefen der zusammengetragenen Karte FEHLER wegen zerfallener Segmente (A 16, B 22, C 25) und ungültiger Klassen in A und B — Reparatur in Teil 4.
