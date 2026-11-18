# Teil 2 von landseg-garten: Regeln und Aufträge der Agents, Prüfung der freien Fassungen

Kurzname: landseg-garten-2 | Datum: 2026-11-18 | Größe: mittel | Bereich: victor | Repos: landseg | Status: eingereiht | Mutterwunsch: landseg-garten

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

Teil 2 des Mutterwunschs `landseg-garten` (`wuensche/2026-11-18-landseg-garten.md`), Zeile aus dessen Teile-Liste:

2. Regeln und Aufträge der Agents, Prüfung der freien Fassungen — Umsetzer — Repo: landseg — Vorbedingungen: keine — nach: 1 — AK 4, 5 — Skill, Vorlagen und `pruefen` kennen Garten (erst nach den effiz-Wünschen einreihen)

## Fragen

keine (siehe Mutterwunsch)

## Entscheidungen

siehe Mutterwunsch

## Arbeitsauftrag

### Abnahmekriterien

AK4: Die Regeln für Agents (Skill `landseg-agent`, Vorlagen `urteil`, `einigung`, `naht`, `korrektur`, `umsetzen`) sagen, wann „Garten“ zu wählen ist; die freien Fassungen A und B führen Garten unter Dauergrünland in ihrer Liste bzw. erhalten es beim Zusammenlegen (`kategorien-a.json`, `kategorien-b.json`) — prüfbar: `"$PY" -B -m unittest tests.test_vorlagen tests.test_einigung`
AK5: `pruefen` meldet einen Fehler, wenn in einer freien Fassung die Klasse „Garten“ fehlt oder nicht unter Dauergrünland steht — prüfbar: `"$PY" -B -m unittest tests.test_pruefen`

Einstieg, Bausteine, Entscheidungen: siehe Mutterwunsch

Vorbedingungen: keine
