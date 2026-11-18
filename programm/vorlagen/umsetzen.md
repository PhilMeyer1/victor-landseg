# Auftrag: bestätigtes Urteil der Teilkachel {{TEILKACHEL}} auf der Label-Karte umsetzen

Lies zuerst den Skill `landseg-agent` (`{{REPO}}/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `{{TEILKACHEL}}` des Ausschnitts in `{{DATEN}}`. Der Nutzer hat die Vorlagen
des Urteils geprüft und bestätigt. Was er anders will: {{ABWEICHUNGEN}}{{FEINHEIT}}

## Daten (eingefrorener Stand, nur lesen)

- `{{DATEN}}/manifest.json` (Eintrag `{{TEILKACHEL}}`: `bild`, `kern_im_bild`, `kern`).
- `{{DATEN}}/{{LABELS}}` und `{{DATEN}}/{{SEGMENTE}}`: Ausgangsstand.
- `{{DATEN}}/{{URTEIL}}` mit den Bildern daneben: was zu tun ist.

## Was

- Kopiere den Ausgangsstand nach `{{ERGEBNIS}}/labels.tif` und `{{ERGEBNIS}}/segmente.json` und
  arbeite nur an diesen Kopien.
- Setze jeden Punkt des Urteils (mit den Abweichungen oben) um, Segment für Segment, nur im Kern.
  Was das Urteil nicht nennt, bleibt bildpunktgleich.
- Klassen nach dem Urteil und `KATEGORIEN.md`. Gärten nach Regel L14 des Skills: krautige Grünfläche und Beet im Haus- oder Hofgarten = 3.6 Garten;
  Wiese/Weide oder Acker mit `im_siedlung: ja` ist nur ein Kandidat, entschieden wird am Bild.
- Grenzen legst du mit `kante` auf die Kante im Bild; wo das Bild keine hergibt, setzt du sie von
  Hand und meldest die Strecke als geschätzt.
- Ändert ein Eingriff eine Grenze bis an den Kernrand, meldest du das Segment unter `naht`.

## Wie

Befehle im Ordner `{{REPO}}` mit `{{PY}} -m landseg <befehl>` (README): `eingriff --labels
{{ERGEBNIS}}/labels.tif --segmente {{ERGEBNIS}}/segmente.json --bearbeiter {{BEARBEITER}} …`
(mehrere Schritte als `stapel`), `kante`, `ansicht`. Nach jedem Eingriff meldet `pruefen` den
Befund; er muss `ok` sein. Eigene Dateien nur in `{{ERGEBNIS}}`.

## Ergebnis in `{{ERGEBNIS}}` (genau diese Namen)

- `labels.tif`, `segmente.json`: Stand nach deinen Eingriffen (Verlauf mit deinem Bearbeiter-Namen).
- `vorher.jpg`, `nachher.jpg` (ganze Teilkachel, Kern umrandet, Grenzen und IDs), dazu
  `nah_<id>_<n>.jpg` je geänderter Stelle.
- `abgabe.json` (UTF-8):

```
{"teilkachel": "{{TEILKACHEL}}", "runde": {{RUNDE}}, "bearbeiter": "{{BEARBEITER}}",
 "punkte": [{"id": 17, "nr": 1, "stand": "umgesetzt|teilweise|nicht", "text": "ein Satz"}],
 "geschaetzte_kanten": [{"bereich": [x0, y0, x1, y1], "laenge_px": Zahl, "text": "warum"}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "was sich am Kernrand geändert hat"}],
 "offen": ["was offen blieb und was es klären würde"], "nicht_geprueft": ["..."]}
```

## Rückgabe

Umgesetzt / teilweise / nicht je als Zahl, letzte Zeile von `pruefen`, Zahl der geschätzten
Strecken und der Naht-Meldungen.
