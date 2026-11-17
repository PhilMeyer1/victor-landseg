# Teil 3 von landseg-test-t0: Zusammenführen, Prüfen, Karten für B und C, Bestätigung

Kurzname: landseg-test-t0-3 | Datum: 2026-11-17 | Größe: mittel | Bereich: victor | Repos: landseg | Status: blockiert (ruht auf Wunsch des Nutzers [2026-11-17]: Stand jetzt an Victor übergeben [landseg-uebergabe]; Durchsicht der festen Liste und Teil 4/5 folgen erst, wenn der Nutzer sie anstößt) | Mutterwunsch: landseg-test-t0 | Ergebnis: ohne Commit

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

Teil 3 des Mutterwunschs `landseg-test-t0` (`wuensche/2026-11-17-landseg-test-t0.md`), Zeile aus dessen Teile-Liste:

3. Zusammenführen, Prüfen, Karten für B und C, Bestätigung — Umsetzer (ohne Commit) — Repo: landseg — Vorbedingungen: keine — Halt: Durchsicht — nach: 2 — AK 2, 3, 6, 7 — Viertel-Urteile je Teilkachel zu `urteil.json` zusammengeführt und gegen `segmente.json` geprüft, `kategorien-b.json` und `kategorien-c.json` gebaut und mit dem Prüfskript bestanden, C zusammengetragen; der Nutzer bestätigt A auf der Prüfseite, seine Abweichungen und das Urteil je Klasse stehen im Bericht.

## Fragen

keine (siehe Mutterwunsch)

## Entscheidungen

siehe Mutterwunsch

## Arbeitsauftrag

### Abnahmekriterien

AK2: (A) Zu jeder Teilkachel gibt es genau ein `urteil.json` (aus den vier Viertel-Abgaben zusammengeführt), das jedes Segment des Kerns genau einmal mit Klasse (Code aus `kategorien.json`), Sicherheit und Viertel enthält, je Viertel `bilder_angesehen` (Übersicht des Viertels mit Grenzen und Nummern, Nahansichten), kein Kontextrand-Segment urteilt, und unter `nicht_geprueft` und `offen` nennt, was fehlt — prüfbar: Lesen `urteil/<teilkachel>/v<1-4>/urteil.json` und `urteil/<teilkachel>/urteil.json` gegen `segmente.json` (Zahl der Einträge gleich Zahl der Kernsegmente, jedes Segment in genau einem Viertel, je Viertel mindestens eine Übersicht, die genannten Bilddateien existieren, kein Bild zeigt nur ein einzelnes Segment als Urteilsgrundlage)
AK3: (A) Der Nutzer hat alle vier Urteile auf der Prüfseite angesehen und bestätigt oder wörtlich korrigiert; seine Abweichungen und sein Urteil je Klasse (passt / passt nicht) stehen im Bericht — prüfbar: Ansicht Prüfseite an T0 Fassung A, Desktop, Lesen `bericht-landseg.md` (Halt)
AK6: (B) Fassung B liegt vor: je Teilkachel ein Urteil aus vier Viertel-Abgaben, das jedes Kernsegment einzeln mit selbst benannter und gestufter Klasse enthält und je Viertel die angesehenen Bilder belegt, eine zusammengetragene Karte von T0 (1000 × 1000 ohne 0, lückenlos, Naht ohne offenen Verstoß) und eine eigene, über alle Viertel vereinheitlichte Kategorienliste `kategorien-b.json` im Format von `kategorien.json` (Codes, Namen, Eltern, Ebenen, Farben), die die Prüfseite lädt — prüfbar: `PY -I tools/pruefe_kategorien.py <Pfad>/kategorien-b.json`, `PY -m landseg pruefen --kategorien <Pfad>/kategorien-b.json` je Teilkachel, Lesen `urteil.json` gegen `segmente.json`, `zusammentragen`, `naht`
AK7: (C) Fassung C liegt vor: je Teilkachel eine freie Abgabe (eigene Kategorien, eigene Arbeitsweise, im Bericht beschrieben), eine zusammengetragene Karte von T0 (1000 × 1000 ohne 0, lückenlos: jeder Bildpunkt genau ein Segment) und eine eigene Kategorienliste `kategorien-c.json` im Format von `kategorien.json` — prüfbar: `PY -I tools/pruefe_kategorien.py <Pfad>/kategorien-c.json`, `PY -m landseg pruefen --kategorien <Pfad>/kategorien-c.json`

Einstieg, Bausteine, Entscheidungen: siehe Mutterwunsch

Vorbedingungen: keine

Halt: Durchsicht
