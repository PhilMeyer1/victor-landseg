# Teil 1 von naht-einigung: Einigungs-Werkzeug mit Vorlage

Kurzname: naht-einigung-1 | Datum: 2026-11-18 | Größe: mittel | Bereich: victor | Repos: landseg | Status: eingereiht | Mutterwunsch: naht-einigung

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

Teil 1 des Mutterwunschs `naht-einigung` (`wuensche/2026-11-18-naht-einigung.md`), Zeile aus dessen Teile-Liste:

1. Einigungs-Werkzeug mit Vorlage — Umsetzer — Repo: landseg — Vorbedingungen: keine — nach: – — AK 1, 2, 3, 4 — `landseg einigung` (finden, anwenden, messen), `vorlagen/einigung.md`, Regel L13, `einstellungen/einigung.json`, Tests auf synthetischen Karten; Karten bleiben unverändert, Klassen und Verlauf stimmen.

## Fragen

keine (siehe Mutterwunsch)

## Entscheidungen

siehe Mutterwunsch

## Arbeitsauftrag

### Abnahmekriterien

AK1: Ein neues Werkzeug `einigung finden` sucht an allen Kerngrenzen (Nähte und Ecken) und an den Viertelgrenzen im Kern (Mitte jeder Teilkachel) die Stellen, an denen zwei benachbarte Segmente ohne Bildkante verschiedene Klassen tragen, bündelt zusammenhängende Segment-Paare (eine Ecke bleibt in einem Bündel) und legt je Bündel einen Auftrag mit Bildern beider Seiten ab — prüfbar: `PY -B -m unittest tests.test_einigung` (synthetische Karte mit Naht, Ecke, Viertelgrenze, echter Kante) und `PY -B -m landseg einigung finden --help`
AK2: `einigung anwenden` setzt aus der Abgabe der Agents je Paar eine von drei Entscheidungen um: gleiche Fläche (beide Segmente bekommen eine gemeinsame, in der Kategorienliste der Fassung gültige Klasse), echte Grenze (nichts ändert sich, Begründung wird festgehalten), unklar (beide Segmente `sicher: nein` mit Grund); Label-Karten bleiben bildpunktgleich, `pruefen` bleibt `ok`, jede Änderung steht im Verlauf der `segmente.json` mit Bearbeiter, nur Kern-Segmente werden geändert — prüfbar: `PY -B -m unittest tests.test_einigung`
AK3: `einigung messen` nennt je Fassung die Zahl der Stellen (Segment-Paare und Randpunkte) mit gleicher Fläche und verschiedener Klasse, getrennt: offen, als unsicher belegt, geklärt; nach dem Anwenden einer Abgabe sinkt „offen“ entsprechend; die Zählung benutzt dieselbe Bildkanten-Regel wie `naht` (gleicher Bildleser) — prüfbar: `PY -B -m unittest tests.test_einigung`
AK4: Für die Agents gibt es die Vorlage `vorlagen/einigung.md` (Urteil im Verbund: Bilder beider Seiten, ein Urteil je Stelle für alle Beteiligten, nur Klassen im Kern, Abgabe `einigung_abgabe.json`) samt Regel L13 im Skill `landseg-agent` und Eintrag in der Vorlagen-Tabelle; sie sagt für Fassung A ausdrücklich, dass die Einigung auf der zusammengelegten Liste `kategorien-a.json` läuft — prüfbar: Lesen `vorlagen/einigung.md`, `vorlagen/README.md`, `.claude/skills/landseg-agent/SKILL.md`; `PY -B -m unittest tests.test_vorlagen`

Einstieg, Bausteine, Entscheidungen: siehe Mutterwunsch

Vorbedingungen: keine
