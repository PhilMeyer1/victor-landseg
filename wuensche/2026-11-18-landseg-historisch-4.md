# Teil 4 von landseg-historisch: Prüfen, Seite mit H0 und Messbericht

Kurzname: landseg-historisch-4 | Datum: 2026-11-18 | Größe: mittel | Bereich: victor | Repos: landseg | Status: frage-offen | Mutterwunsch: landseg-historisch | Ergebnis: ohne Commit

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

Teil 4 des Mutterwunschs `landseg-historisch` (`wuensche/2026-11-18-landseg-historisch.md`), Zeile aus dessen Teile-Liste:

4. Prüfen, Seite mit H0 und Messbericht — Umsetzer (ohne Commit) — Repo: landseg — Vorbedingungen: keine — Halt: Durchsicht — nach: 1, 3 — AK 5, 7 — Karten geprüft, Prüfseite mit T0 und H0 gebaut, Messbericht mit PQ-Skript, Kosten und Vergleich zu T0; der Nutzer sieht die Seite durch und urteilt je Klasse (nach F3).

## Fragen

keine (siehe Mutterwunsch)

## Entscheidungen

siehe Mutterwunsch

- 2026-11-18 (Hauptsession nach Teil 3): Teil 3 hinterließ in allen drei Fassungen `pruefen` FEHLER auf der zusammengetragenen Karte: zerfallene Segmente (A 16, B 22, C 25; Segmente, die nur über den Kontextrand zusammenhingen) und in A und B ungültige Klassen. Beides vor dem Bau der Seite beheben (zerfallene Teile eigene IDs mit gleicher Klasse bzw. an den Nachbarn gleicher Klasse; ungültige Klassen auf gültige Codes der Liste, Liste und Grund im Bericht). Die Nahtverstöße des ID-Teils (A 187, B 158, C 126) bleiben wie bei T0 offen (jede Teilkachel eigene IDs, eingriff übernimmt keine fremde ID); der Bericht nennt sie, Lösung ist ein eigener Wunsch „Grenzlinien an den Nähten nachziehen“. Teil 3 kostete 71 Agents, 11,41 Mio. Tokens, 104 min (Workflow wf_62f47ff3-c51); das gehört in den Messbericht.
- 2026-11-18, Durchsicht (Nutzer): „Ich kommentiere auf der Seite“ — der Nutzer kommentiert Flächen auf `daten/landseg/seiten/T0-H0.html` und gibt `kommentare-*.json` (Export); die Datei ist sein Urteil je Klasse für den Messbericht, ohne Korrekturrunde (F3). Ansicht der Seite (Bildwahl T0/H0, Fassungen A/C, Ganzer Ausschnitt, keine Konsolenfehler) hat die Hauptsession über die Browser-Erweiterung geprüft.
- 2026-11-18, Durchsicht verschoben (Nutzer): „Erst nach dem Umbau“ — die Durchsicht samt Kommentaren je Klasse erfolgt erst am umgebauten Stand (H0 gröber nach landseg-sw-grob, Gärten nach landseg-garten-3, Seite neu); bis dahin bleibt dieser Teil frage-offen.

## Arbeitsauftrag

### Abnahmekriterien

AK5: Der Bericht nennt wie bei T0 je Fassung Zahl der Agents, Läufe, Wandzeit, Tokens/Kosten (soweit die Werkzeuge sie liefern), Segmente, Klassen, Anteil `sicher: nein`, die Übereinstimmung der Gegenprobe (PQ und Boundary-PQ) auf einer Teilkachel und das Nutzerurteil je Klasse (nach F3), und stellt H0 und T0 gegenüber (was auf Schwarz-Weiß trägt und was nicht) — prüfbar: Lesen `bericht-landseg.md`
AK7: Der Weg des Nutzers: Er öffnet die Seite im Gesamtprojekt, wählt das Bild H0, sieht das historische Bild mit dem Ergebnis, schaltet A, B, C um, klickt sich durch die Schrittleiste der Teilkacheln, sieht die Nähte-Zahlen und beim Klick auf eine Stelle den Einigungsgrund, und wechselt zurück auf T0 — prüfbar: Ansicht Prüfseite im Gesamtprojekt, H0 und T0, Fassungen A, B, C, Desktop (nach dem Bauen, vor dem Einreihen)

Einstieg, Bausteine, Entscheidungen: siehe Mutterwunsch

Vorbedingungen: keine

Halt: Durchsicht
