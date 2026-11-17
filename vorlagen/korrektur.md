# Auftrag: Kommentare des Nutzers an Teilkachel {{TEILKACHEL}} umsetzen (Runde {{RUNDE}})

Lies zuerst den Skill `landseg-agent` (`{{REPO}}/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `{{TEILKACHEL}}` des Ausschnitts in `{{DATEN}}`. Der Nutzer hat den
zusammengetragenen Stand auf der Prüfseite angesehen und kommentiert. Deine Kommentare, wörtlich:

{{KOMMENTARE}}

## Daten (eingefrorener Stand, nur lesen)

- `{{DATEN}}/manifest.json` (Eintrag `{{TEILKACHEL}}`: `bild`, `kern_im_bild`, `kern`).
- `{{DATEN}}/{{LABELS}}` und `{{DATEN}}/{{SEGMENTE}}`: letzter Stand dieser Teilkachel.
- `{{DATEN}}/{{ZUSAMMEN}}/segmente.json`: Segmente und offene Fragen des ganzen Ausschnitts
  (IDs dort sind dieselben wie in der Teilkachel).

## Was

- Setze genau die Kommentare um, nicht mehr. Alles, was sie nicht betreffen, bleibt bildpunktgleich:
  nichts glätten, nichts neu ziehen.
- Bildpunkte, die du einem Segment nimmst, gehen an das Segment, zu dem sie nach dem Bild gehören;
  entscheide das ausdrücklich. Lücken kann es nicht geben, weil `eingriff` nur umnummeriert.
- Kante aus dem Bild mit `kante` im engen Band; wo das Bild nichts hergibt, von Hand und als
  geschätzt melden. Keine Geraden, wo das Bild eine geschwungene Grenze zeigt.
- Ist ein Kommentar nicht eindeutig oder am Bild nicht sicher entscheidbar: nichts raten. Setze um,
  was eindeutig ist, lass den Rest, und schreib unter `offen`, was offen blieb und welche Angabe des
  Nutzers es klären würde.
- Reicht ein Kommentar über den Kern hinaus in eine Nachbarkachel, setzt du nur deinen Kern um und
  meldest den Rest unter `naht`.

## Wie

Kopiere den letzten Stand nach `{{ERGEBNIS}}/labels.tif` und `{{ERGEBNIS}}/segmente.json`; Befehle im
Ordner `{{REPO}}` mit `{{PY}} -m landseg <befehl>` (README): `eingriff … --bearbeiter {{BEARBEITER}}`,
`kante`, `ansicht`. Nach jedem Eingriff muss `pruefen` `ok` melden. Eigene Dateien nur in
`{{ERGEBNIS}}`.

## Ergebnis in `{{ERGEBNIS}}` (genau diese Namen)

- `labels.tif`, `segmente.json`: Stand nach deinen Eingriffen.
- `vorher.jpg`, `nachher.jpg` der geänderten Stellen (vorherige Grenze im Nachher-Bild dünn rot),
  dazu `nah_<kennung>_<n>.jpg`.
- `abgabe.json` (UTF-8), wie bei `umsetzen.md`, aber `punkte` je Kommentar:

```
{"teilkachel": "{{TEILKACHEL}}", "runde": {{RUNDE}}, "bearbeiter": "{{BEARBEITER}}",
 "punkte": [{"kennung": "Kennung des Kommentars", "stand": "umgesetzt|teilweise|nicht", "text": "ein Satz"}],
 "geschaetzte_kanten": [{"bereich": [x0, y0, x1, y1], "laenge_px": Zahl, "text": "warum"}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "..."}],
 "offen": ["..."], "nicht_geprueft": ["..."]}
```

## Rückgabe

Je Kommentar umgesetzt / teilweise / nicht, letzte Zeile von `pruefen`, was offen blieb.
