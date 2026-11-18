# Selbstprüfung workflow.js (landseg-einigung-t0), 2026-11-18

Hard-Stops: meta erstes Statement, reines Literal — ja. args normalisiert, Pflicht-Guard, Pfad-Whitelist — ja.
Jeder agent() mit model/effort (opus/high, begründet) — ja. Kein Date.now/Math.random/new Date/import/FILL — 0 Treffer.
Ausfall-Buchhaltung: .filter(Boolean), ohne_rueckmeldung, probe_rot, rest im return — ja. Deckel MAX_AGENTS 16 bei 12 Bündeln — ja.
Keine Schleife (eine Stufe), also kein Abbruchkriterium nötig. Nutzdaten nicht im Orchestrator: nur Pfade und Zahlen.
Schreibrechte: Prompt begrenzt auf den Ergebnisordner je Bündel, anwenden nur --probe; Umsetzen macht die Hauptsession.
Phase-1-Gate: Zuschnitt (je Bündel ein Agent, ~10–12 Agents, ~1 Mio. Tokens) stand in der Frage F1, die der Nutzer am 2026-11-18 mit der Empfehlung beantwortet hat.

Qualität: pipeline ohne Barriere (Bündel unabhängig); kein Verify-Agent, weil anwenden --probe die Form prüft und messen danach zählt; unklar als Ausweg erlaubt.
