# Teil 2 von landseg-test-t0: Urteile A und B je Viertel, freie Abgabe C

Kurzname: landseg-test-t0-2 | Datum: 2026-11-17 | Größe: mittel | Bereich: victor | Repos: landseg | Status: eingereiht (ohne Commit) | Mutterwunsch: landseg-test-t0 | Ergebnis: ohne Commit

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

Teil 2 des Mutterwunschs `landseg-test-t0` (`wuensche/2026-11-17-landseg-test-t0.md`), Zeile aus dessen Teile-Liste:

2. Urteile A und B je Viertel, freie Abgabe C — Workflow (ohne Commit) — Repo: landseg — Vorbedingungen: keine — Aufruf-Budget: 400 — nach: 1 — AK 2, 6, 7 — Skript der Hauptsession über `wunsch:workflow`, Modelle nach „Bausteine und Fallen“: 16 Viertel-Urteile je Fassung A und B, Vereinheitlichung der Liste von B, freie Abgabe von C, Zweitagent auf den vier Vierteln einer Teilkachel.

## Fragen

keine (siehe Mutterwunsch)

## Entscheidungen

siehe Mutterwunsch

## Arbeitsauftrag

### Abnahmekriterien

AK2: (A) Zu jeder Teilkachel gibt es genau ein `urteil.json` (aus den vier Viertel-Abgaben zusammengeführt), das jedes Segment des Kerns genau einmal mit Klasse (Code aus `kategorien.json`), Sicherheit und Viertel enthält, je Viertel `bilder_angesehen` (Übersicht des Viertels mit Grenzen und Nummern, Nahansichten), kein Kontextrand-Segment urteilt, und unter `nicht_geprueft` und `offen` nennt, was fehlt — prüfbar: Lesen `urteil/<teilkachel>/v<1-4>/urteil.json` und `urteil/<teilkachel>/urteil.json` gegen `segmente.json` (Zahl der Einträge gleich Zahl der Kernsegmente, jedes Segment in genau einem Viertel, je Viertel mindestens eine Übersicht, die genannten Bilddateien existieren, kein Bild zeigt nur ein einzelnes Segment als Urteilsgrundlage)
AK6: (B) Fassung B liegt vor: je Teilkachel ein Urteil aus vier Viertel-Abgaben, das jedes Kernsegment einzeln mit selbst benannter und gestufter Klasse enthält und je Viertel die angesehenen Bilder belegt, eine zusammengetragene Karte von T0 (1000 × 1000 ohne 0, lückenlos, Naht ohne offenen Verstoß) und eine eigene, über alle Viertel vereinheitlichte Kategorienliste `kategorien-b.json` im Format von `kategorien.json` (Codes, Namen, Eltern, Ebenen, Farben), die die Prüfseite lädt — prüfbar: `PY -I tools/pruefe_kategorien.py <Pfad>/kategorien-b.json`, `PY -m landseg pruefen --kategorien <Pfad>/kategorien-b.json` je Teilkachel, Lesen `urteil.json` gegen `segmente.json`, `zusammentragen`, `naht`
AK7: (C) Fassung C liegt vor: je Teilkachel eine freie Abgabe (eigene Kategorien, eigene Arbeitsweise, im Bericht beschrieben), eine zusammengetragene Karte von T0 (1000 × 1000 ohne 0, lückenlos: jeder Bildpunkt genau ein Segment) und eine eigene Kategorienliste `kategorien-c.json` im Format von `kategorien.json` — prüfbar: `PY -I tools/pruefe_kategorien.py <Pfad>/kategorien-c.json`, `PY -m landseg pruefen --kategorien <Pfad>/kategorien-c.json`

Einstieg, Bausteine, Entscheidungen: siehe Mutterwunsch

Vorbedingungen: keine

Aufruf-Budget: 400

## Nachweis

- 2026-11-17: Workflow wf_e81273d7-c88 (Lauf 20261117k, Skript wuensche/2026-11-17-landseg-test-t0-2/workflow.js): 15 Agents, 0 Fehler, 3,30 Mio. Tokens, 25 min. 40/40 Aufträge mit bestandener Kontrolle: urteil.json A 16, B 16, Gegenprobe r0c0 4; Abgabe C 4 Teilkacheln (labels.tif); Vereinheitlichung B ok (fassung-b/vereinheitlichung, 7/21/21 Klassen). Segmente A 641/641, B 641/641, Gegenprobe 141, C 881. Nicht sauber: A 432, B 405, Gegenprobe 121.
