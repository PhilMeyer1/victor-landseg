# Selbstprüfung workflow.js (landseg-garten), 2026-11-18

Vorbild: `2026-11-18-landseg-historisch-3/workflow.js` (gelaufen, geprüft).

## Hard-Stops
- meta erstes Statement, reines Literal: ja. Kein Date/Math.random/import/FILL: 0 Treffer.
- Jeder agent()-Aufruf mit model + effort und Kommentar: 4/4 (Vergröbern, Anwenden sonnet/medium; Kandidaten, Bestätigen opus/medium).
- args normalisiert, Pfade gegen Whitelist `C:/Users/Phil/Developement/Victor/…`; Einheiten-Ordner der Agents erneut geprüft (nur unter `<bericht>/einheiten/`).
- Keine Schleife. Fan-out gedeckelt (MAX 48), Rest unter `rest`; Ausfall-Buchhaltung: `ohne_rueckmeldung`, `nicht_ok`; jede Barriere mit eigenem Return bei Ausfall (resume).
- Nutzdaten nie im Orchestrator: nur Zahlen, Namen, Pfade.
- Syntax: `node --check` auf einer Hülle: ok.

## Qualität
- Form: Kette mit Barrieren aus der Sache (erst gröber, dann Kandidaten, dann Bestätigen als pipeline, dann Anwenden).
- Verify: keiner; enge Ja/Nein-Frage, „unklar“ ändert nichts, `pruefen` prüft die Form.
- Schreibrechte disjunkt: Bestätiger schreiben nur ihr `entscheid.json`.
- Risiko: neue offene Einigungspaare durch Garten auf nur einer Nahtseite — werden gezählt und genannt, nicht geklärt.

## Schätzung
Agents: 1 + 1 + etwa 20–45 Einheiten + 1 ≈ 25–50. Tokens: Bestätigen je etwa 150–300 k gelesen (kurzer Kontext),
zusammen grob 25–45 USD Rechenwert. Dauer etwa 45–75 min.
