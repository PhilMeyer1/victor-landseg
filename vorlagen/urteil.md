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

Befehle im Ordner `{{REPO}}` mit `{{PY}} -B -m landseg <befehl>`; Aufruf und Schalter stehen in
`{{REPO}}/README.md`. Zuerst die fertigen Befehle, sie sind der Standardweg:

- Übersichtsbilder: `ansicht` (W3); fragliche Grenzen: `kante` (W4, hier nur zum Ansehen der Bildkante).
- Nahbilder einer Stelle mit Umriss und Nummern, links das rohe Luftbild:
  `{{PY}} -B -m landseg zoom --manifest {{DATEN}}/manifest.json --teilkachel {{TEILKACHEL}} --labels {{DATEN}}/{{LABELS}} --ids 17 --roh --ziel {{ERGEBNIS}}/nah_17_1.jpg`
  (statt `--ids` auch `--punkt x,y --radius r` oder `--rechteck x,y,b,h`).
- `urteil.json` nicht von Hand schreiben, sondern die kurze Liste `{{ERGEBNIS}}/liste.json` (Format unten)
  und daraus bauen:
  `{{PY}} -B -m landseg urteil bauen --manifest {{DATEN}}/manifest.json --teilkachel {{TEILKACHEL}} --labels {{DATEN}}/{{LABELS}} --segmente {{DATEN}}/{{SEGMENTE}} --bearbeiter {{BEARBEITER}} --liste {{ERGEBNIS}}/liste.json --ziel {{ERGEBNIS}}/urteil.json`
  Der Befehl prüft dabei alles (fehlende, doppelte oder fremde Segmente, Klassen, Punktarten, Bilder),
  nennt jeden Fehler und schreibt nur bei Exit 0; `urteil pruefen … --urteil {{ERGEBNIS}}/urteil.json`
  prüft eine fertige Datei.

Ein eigenes Skript (als Datei in `{{ERGEBNIS}}`) nur, wenn kein Befehl den Fall deckt, etwa eine fachliche
Hilfe beim Nachsegmentieren; nenne es in der Rückgabe.

## Ergebnis in `{{ERGEBNIS}}` (genau diese Namen)

- `roh.jpg`, `umriss.jpg` (alle Segmentgrenzen mit ID), `maengel.jpg` (nummerierte Punkte mit kurzer
  deutscher Beschriftung, sonst Vermerk „keine Mängel“), `vorschlag.jpg` (Grenzen und Klassen, wie
  du sie setzen würdest, sonst Vermerk „unverändert“): je die ganze Teilkachel, Kern umrandet.
- `nah_<id>_<n>.jpg`: Nahbilder der Stellen, die man in der Übersicht nicht beurteilen kann;
  `kontrast_<id>_<n>.jpg` bei blassen Stellen.
- `liste.json`, die kurze Liste für `urteil bauen`: was nur du weißt, je Segment `[id, urteil, vorschlag,
  punkte, bilder]` (hintere Felder dürfen fehlen) oder ein Objekt mit denselben Feldern und `was`
  (sonst Name der heutigen Klasse) und `sicher` (sonst `true`); ein Punkt `[art, text, flaeche_px]`.
  Segmente ohne Befund zählst du unter `sauber` auf, keines darf fehlen:

```
{"segmente": [[17, "nicht_sauber", "Code", [["trennen", "Satz mit Stelle (x/y im Teilkachelbild)", 340]], ["nah_17_1.jpg"]],
              {"id": 18, "urteil": "sauber", "was": "ein Satz", "sicher": false}],
 "sauber": [3, 4, 5],
 "naht": [], "unsicher": [], "nicht_geprueft": [], "offen": []}
```

- `urteil.json` (UTF-8), gebaut von `urteil bauen` (Teilkachel, Bearbeiter, `klasse_heute` und Schema
  füllt der Befehl):

```
{"teilkachel": "{{TEILKACHEL}}", "bearbeiter": "{{BEARBEITER}}",
 "segmente": [{"id": 17, "klasse_heute": "Code", "was_ist_es": "ein Satz",
               "urteil": "sauber" | "nicht_sauber", "klasse_vorschlag": "Code oder null",
               "sicher": true | false,
               "punkte": [{"nr": 1, "art": "fremdes|fehlt|trennen|verschmelzen|grenze|klasse|zu_klein|sonstiges",
                           "text": "ein Satz mit Stelle (x/y im Teilkachelbild)", "flaeche_px": Zahl oder null}],
               "bilder": ["nah_17_1.jpg"]}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "was an der Kerngrenze nicht passt"}],
 "unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."]}
```

Jedes Segment mit Bildpunkten im Kern steht genau einmal unter `segmente`, auch die sauberen.

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Punkte, Anteil `sicher: false`, wo du unsicher bist.
