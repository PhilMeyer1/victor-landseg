# Selbstprüfung workflow.js (landseg-h0), 2026-11-18

Vorbilder: `2026-11-17-landseg-test-t0-2/workflow.js` (Urteile T0, 15 Agents, 3,30 Mio. Tokens, 25 min) und
`2026-11-18-naht-einigung-2/workflow.js` (Einigung T0, 15 Agents, 1,89 Mio. Tokens, 13,5 min).

## Hard-Stops
- meta erstes Statement, reines Literal: ja. Kein Date/Math.random/import: 0 Treffer. Kein FILL: 0.
- Jeder agent()-Aufruf mit model + effort und Kommentar: 7/7 (Urteil, Nachholen, Naht, Einigung opus/high; Zusammenführen opus/medium; Vereinheitlichen, Anwenden sonnet/medium).
- args normalisiert, Pfade gegen Whitelist `C:/Users/Phil/Developement/Victor/…`, art/v geprüft (A nur v 0).
- Schleife Einigung: Abbruch keine Bündel mehr oder MAX_RUNDEN 3; Deckel MAX_BUENDEL 30 je Runde, Rest unter `rest`.
- Nachholen gedeckelt (8), Rest unter `nachhol_rest`.
- Ausfall-Buchhaltung: fehlende Urteils-Agents als nicht ok gezählt; `ohne_rueckmeldung` im return; Zusammenführen ohne Rückmeldung beendet den Lauf mit eigenem return (resume).
- Nutzdaten nie im Orchestrator: nur Zahlen, Pfade, Bündelnamen.
- Syntax: `node --check` auf einer Hülle mit Attrappen: ok.

## Qualität
- Form: pipeline je Stufe; Barrieren aus der Sache (Vereinheitlichen und Zusammenführen brauchen alle Abgaben, anwenden alle Abgaben einer Fassung).
- Verify: keine eigene Stufe; Gegenprobe ist die Zweitmeinung, pruefen/naht/messen prüfen die Form.
- Risiko: H0 hat 1.366 Kernsegmente (T0 641), ein Agent bis 518 (r1c1); darum Stufe Nachholen je Viertel.
- Risiko: Zusammenführen überträgt T0-Skripte mit vertauschten Buchstaben A/C; Prompt warnt ausdrücklich, opus.
- Gegenprobe = C auf r0c0 (vergleichbar mit T0), Alternative A nicht genutzt.

## Schätzung
Agents: 13 Urteile + 0–8 Nachholen + 1 + 1 + 0–3 Nähte + Einigung (etwa 20–35 Bündel in Runde 1, wenige in 2–3) + bis 3 Anwenden ≈ 45–65.
Tokens: Urteile etwa 7 Mio. (T0 3,3 Mio. für halb so viele Segmente), Einigung 3–4 Mio., Rest etwa 1 Mio.: zusammen etwa 11–12 Mio.
Dauer: etwa 1,5 bis 2 Stunden (längster Urteils-Agent 518 Segmente gegen 301 bei T0).

## Umbau nach Neuklärung (2026-11-18, grobe Vorstufe, Nachsegmentieren)
- Neue erste Stufe Vorbereitung (opus/medium): feine Fassung umbenennen in `<name>-fein` (nichts gelöscht), Vorstufe grob (Repo-Einstellungen, nur bildpunkt_m 0,45), Kopien B/C und eigene Gegenprobe-Kopie, Aufträge und Bilder neu, Plan `auftraege.json` in diesem Ordner; liefert den Katalog. Abbruch vor den Urteilen bei ok=false, > 800 Kernsegmenten oder geändertem Hash.
- Viertel-Aufträge tragen den Abschnitt „Nachsegmentieren“ (ein `eingriff … stapel` je Viertel, kante, pruefen); nur der Agent der Teilkachel schreibt auf seine Karte, darum keine Schreibkonflikte.
- Zusammenführen zählt die Eingriffe je Fassung (AK5).
- Prüfung: `node --check` ok; 8/8 agent()-Aufrufe mit model+effort; kein Date/Math.random/import.
- Schätzung neu: 32–45 Agents, etwa 6–7 Mio. Tokens, etwa 1,5 Stunden. Feine Fassung des Skripts: `workflow-fein.js`.
