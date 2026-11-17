# Selbstprüfung — landseg-urteile-t0 — 20261117k

Skript: workflow.js · Form: Vorstufe (1 Agent) → pipeline über 13 Gruppen (je Fassung und Teilkachel, 40 Aufträge) → 1 Abschluss-Agent · Agents geplant: 15 (Nutzer 2026-11-17 „je Fassung 4, Gegenprobe 1“)

## Hard-Stops
| # | Status | Beleg / Fix |
|---|---|---|
| H1 | ok | `export const meta` Zeile 25, davor nur Kommentare; phases-Titel = phase()/opts.phase (Gesamtbilder, Urteile, Vereinheitlichen) |
| H2 | ok | `typeof args`, Pflicht-Guards mit throw; Pfade gegen Whitelist `C:/Users/Phil/Developement/Victor/…`, kein `..` |
| H3 | ok | grep → 0 |
| H4 | ok | alle drei agent()-Aufrufe tragen `phase:` |
| H5 | ok | `ergebnisse.filter(Boolean)`, `ohne_rueckmeldung`, `rest`, `kontrolle_fehlt` im return |
| H6 | ok | 3 agent() / 3 model+effort, je mit Kommentar |
| H7 | ok | keine Schleife außer withRetry (Cap BACKOFF_MS.length) |
| H8 | ok | budget.remaining nicht benutzt |
| H9 | ok | return nur Zahlen, Kennungen, Pfade |
| H10 | ok | Schemas additionalProperties:false, required gesetzt, enum bei tk |
| H11 | ok | kein disallowedTools/agentType/bashCommandClamp |
| H12 | ok | 15 Agents < 22 |
| H13 | ok | grep FILL/TODO → 0 |
| H14 | ok | kein parallel() |
| H15 | ok | Schreibmengen disjunkt: je Einheit eigener Ergebnisordner (aus gruppen.json), Gesamtbilder nur unter ganz_dir, Vereinheitlichung nur fassung-b/vereinheitlichung |

## Qualitätsmerkmale
| # | Status | Begründung bei „nein" |
|---|---|---|
| Q1 | ok | Warum-Block (Viertel-Vorgabe, Reihenfolge dichteste zuerst, Barriere Vereinheitlichung) |
| Q2 | ok | MAX_AGENTS + args.max mit rest |
| Q3 | ok | keine Verify-Stufe; Gegenprobe ist Teil des Auftrags |
| Q4 | n/a | |
| Q5 | ok | Plan-Log vor Dispatch, Fortschritt je Einheit |
| Q6 | ok | Soll/Ist Segmentzahl je Viertel (segmentzahl_abweichend), ohne_rueckmeldung |
| Q7 | ok | nur Pfade in Prompts, Agents schreiben selbst |
| Q8 | ok | Zweifelsregel „im Zweifel sicher:false" mit Grund |
| Q9 | ok | whenToUse mit args-Doku |
| Q10 | nein | Urteils-Agents brauchen Read (Bilder), Bash (Python-Kontrolle), Write — voller Satz nötig; kein passender Minimal-Typ |
| Q11 | ok | Reihenfolge Rolle → Auftrag → Schreibrecht → Vorgabe → Zweifel → Verbote → RÜCKGABE |
| Q12 | ok | Labels `urteil:a:r0c0-v1` |

## Ergebnis
Hard-Stops offen: 0 · Durchläufe: 2 (zweiter nach Richtigstellung; Attrappen-Lauf: 15 Agents, 40/40 Aufträge zugeordnet) · Start freigegeben: ja
