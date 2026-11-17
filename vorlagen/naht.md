# Auftrag: Nahtverstöße des Ausschnitts klären (Runde {{RUNDE}})

Lies zuerst den Skill `landseg-agent` (`{{REPO}}/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier, besonders die Nahtregel. Antworte auf Deutsch.

Gegenstand: der Ausschnitt in `{{DATEN}}`. `zusammentragen` hat die Teilkacheln zusammengefügt und
an den Kerngrenzen Verstöße gemeldet. Du klärst jeden einzelnen: Entweder gehören beide Seiten zu
einem Segment (dann gleiche ID und Klasse), oder dort liegt wirklich eine Grenze (dann bestätigst du
sie mit Grund).

## Daten (eingefrorener Stand, nur lesen)

- `{{DATEN}}/manifest.json`: Teilkacheln, Kerne, Ausschnittbild.
- `{{DATEN}}/{{AUFTRAG_ZUSAMMEN}}`: welche Abgabe (Einheit, Runde) je Teilkachel gilt.
- `{{DATEN}}/{{ZUSAMMEN}}/naht.json`: unter `verstoesse` je Verstoß `art` (`ohne_kante`: zwei IDs
  grenzen ohne Bildkante aneinander, mit `naht`, `ids`, `von`, `bis`, `laenge`; `klasse`: eine ID hat
  in zwei Teilkacheln verschiedene Klassen, mit `id`, `klassen`), dazu `labels.tif` und
  `segmente.json` des ganzen Ausschnitts.

## Was

- Je Verstoß das Bild an der Stelle ansehen (`ansicht`, stark vergrößert, kontrastverstärkt).
- Gleiches Objekt auf beiden Seiten: In der Teilkachel, deren Seite falsch ist, die ID an die
  andere angleichen (`eingriff verschmelzen` mit der ID der Gegenseite als Ziel; die Gegenseite ist
  im Kontextrand der Label-Karte sichtbar) bzw. die Klasse setzen (`eingriff klasse`). Nur im Kern
  dieser Teilkachel ändern. Steht die ID der Gegenseite nicht im Kontextrand (dort neu vergeben),
  gleiche die Gegenseite an oder melde den Fall unter `offen`.
- Echte Grenze, die nur schwach im Bild liegt: nichts ändern, unter `naht_bestaetigt` mit Grund.
- Klassenkonflikt: Klasse nach dem Bild und `KATEGORIEN.md` entscheiden und in der Teilkachel mit
  der falschen Klasse setzen.
- Nicht sicher entscheidbar: nichts ändern, unter `offen`.

## Wie

Für jede Teilkachel, die du änderst: letzten Stand (Einheit mit der höchsten Runde aus
`{{AUFTRAG_ZUSAMMEN}}`) nach `{{ERGEBNIS}}/<teilkachel>/labels.tif` und `segmente.json` kopieren und
dort mit `{{PY}} -m landseg eingriff … --bearbeiter {{BEARBEITER}}` arbeiten (Befehle im Ordner
`{{REPO}}`). Zur Probe: `{{ERGEBNIS}}/zusammentragen.json` als Kopie des Auftrags anlegen, alle Pfade
relativ zu `{{ERGEBNIS}}` umschreiben, deine Teilkacheln als Einheiten mit Runde {{RUNDE}} und deine
Bestätigungen unter `naht_bestaetigt` ergänzen, `"ziel": "probe"`, dann
`{{PY}} -m landseg zusammentragen --datei {{ERGEBNIS}}/zusammentragen.json`. Am Ende darf kein
Verstoß übrig sein außer denen unter `offen`.

## Ergebnis in `{{ERGEBNIS}}` (genau diese Namen)

- `<teilkachel>/labels.tif`, `<teilkachel>/segmente.json` je geänderter Teilkachel.
- `zusammentragen.json` (Probe-Auftrag) und `probe/` (Ergebnis der Probe).
- `naht_<n>.jpg` je Verstoß: Stelle vorher und nachher, Kerngrenze eingezeichnet.
- `naht_abgabe.json` (UTF-8):

```
{"runde": {{RUNDE}}, "bearbeiter": "{{BEARBEITER}}",
 "verstoesse": [{"naht": "a|b", "ids": [3, 7], "art": "ohne_kante|klasse",
                 "entscheidung": "angeglichen|klasse_gesetzt|bestaetigt|offen",
                 "teilkachel": "geänderte Teilkachel oder null", "text": "ein Satz, was das Bild zeigt"}],
 "naht_bestaetigt": [{"naht": "a|b", "ids": [3, 7], "grund": "ein Satz"}],
 "einheiten": [{"teilkachel": "...", "labels": "<teilkachel>/labels.tif",
                "segmente": "<teilkachel>/segmente.json", "runde": {{RUNDE}}}],
 "offen": ["..."], "nicht_geprueft": ["..."]}
```

## Rückgabe

Verstöße vorher → nachher, je Entscheidung die Zahl, letzte Zeile der Probe, was offen blieb.
