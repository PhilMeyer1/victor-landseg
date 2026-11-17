# Auftrag: Teilkachel {{TEILKACHEL}} ansehen und über alle Segmente urteilen

Lies zuerst den Skill `landseg-agent` (`{{REPO}}/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `{{TEILKACHEL}}` des Ausschnitts in `{{DATEN}}`. Du urteilst über jedes
Segment, das im Kern dieser Teilkachel liegt, ob Grenze und Klasse stimmen, und zeichnest ein, was
du ändern würdest. Die Label-Karte änderst du nicht.

## Daten (eingefrorener Stand, nur lesen)

- `{{DATEN}}/manifest.json`: Eintrag `{{TEILKACHEL}}` unter `teilkacheln` mit `bild` (Teilkachelbild,
  Kern + Kontextrand), `kern_im_bild` (Lage des Kerns im Teilkachelbild) und `kern` (Lage im Ausschnitt).
- `{{DATEN}}/{{LABELS}}`: Label-Karte (Segment-ID je Bildpunkt, Größe des Teilkachelbilds).
- `{{DATEN}}/{{SEGMENTE}}`: je Segment `id`, `klasse`, `grob`, `herkunft`, `sicher`; dazu die
  Kandidatenliste der Vorstufe, falls vorhanden.
- `{{REPO}}/kategorien.json` und `{{REPO}}/KATEGORIEN.md`: die gültigen Klassen und Regeln.

## Werkzeuge

Befehle im Ordner `{{REPO}}` mit `{{PY}} -m landseg <befehl>`; Aufruf und Schalter stehen in
`{{REPO}}/README.md`. Für die Bilder `ansicht` (W3), für fragliche Grenzen `kante` (W4, hier nur
zum Ansehen der Bildkante), zur Kontrolle `pruefen`. Eigene Skripte als Datei in `{{ERGEBNIS}}`.

## Ergebnis in `{{ERGEBNIS}}` (genau diese Namen)

- `roh.jpg`, `umriss.jpg` (alle Segmentgrenzen mit ID), `maengel.jpg` (nummerierte Punkte mit kurzer
  deutscher Beschriftung, sonst Vermerk „keine Mängel“), `vorschlag.jpg` (Grenzen und Klassen, wie
  du sie setzen würdest, sonst Vermerk „unverändert“): je die ganze Teilkachel, Kern umrandet.
- `nah_<id>_<n>.jpg`: Nahbilder der Stellen, die man in der Übersicht nicht beurteilen kann;
  `kontrast_<id>_<n>.jpg` bei blassen Stellen.
- `urteil.json` (UTF-8):

```
{"teilkachel": "{{TEILKACHEL}}", "bearbeiter": "{{BEARBEITER}}",
 "segmente": [{"id": 17, "klasse_heute": "Code", "was_ist_es": "ein Satz",
               "urteil": "sauber" | "nicht_sauber", "klasse_vorschlag": "Code oder null",
               "sicher": true | false,
               "punkte": [{"nr": 1, "art": "fremdes|fehlt|trennen|verschmelzen|grenze|klasse|zu_klein|sonstiges",
                           "text": "ein Satz mit Stelle (x/y im Teilkachelbild)", "flaeche_px": Zahl oder null}],
               "bilder": ["nah_17_1.jpg"]}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "was an der Kerngrenze nicht passt"}],
 "unsicher": ["..."], "nicht_geprueft": ["..."]}
```

Jedes Segment mit Bildpunkten im Kern steht genau einmal unter `segmente`, auch die sauberen.

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Punkte, Anteil `sicher: false`, wo du unsicher bist.
