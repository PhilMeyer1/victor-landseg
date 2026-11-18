# Auftrag: {{AUSSCHNITT}}, Teilkachel {{TEILKACHEL}} frei segmentieren und klassifizieren ({{FASSUNG_NAME}})

Antworte auf Deutsch. Diese Abgabe gehört zu {{FASSUNG_NAME}}, einem Vergleichsmuster: Du wählst Kategorien und
Arbeitsweise selbst, ohne feste Kategorienliste und ohne die Arbeitsregeln des Skills `landseg-agent`
(`{{REPO}}/.claude/skills/landseg-agent/SKILL.md`; lesen darfst du ihn, er bindet dich hier nicht). Fest bleiben
nur: lückenlos (jeder Bildpunkt der Teilkachel gehört genau einem Segment, keine 0), eigener Ordner (du schreibst
nur in `{{ERGEBNIS}}`), Eingaben nur lesen.

Ziel: das Landschaftsbild so fein segmentieren, wie im Bild sicher erkennbar, und jedem Segment eine Klasse aus
deiner eigenen, gestuften Liste geben.

Zuerst siehst du den ganzen Ausschnitt an (`{{AUSSCHNITT_BILD}}`), dann deine Teilkachel (`{{TEILKACHEL_ROH}}`,
mit Grenzen der Vorstufe `{{TEILKACHEL_BILD}}`), und nennst beide in `arbeitsweise.md`.

## Hinweis des Laufs

{{HINWEIS}}
{{GEGENPROBE}}
## Daten (nur lesen)

- `{{DATEN}}/manifest.json`: Eintrag `{{TEILKACHEL}}` unter `teilkacheln` mit `bild`, `kern_im_bild` (Lage des
  Kerns im Teilkachelbild) und `kern`. Maßgeblich ist der Kern; der Kontextrand dient zum Ansehen, dort zählt
  beim Zusammentragen nichts.
- `{{DATEN}}/{{TEILKACHEL_DATEI}}`: das Bild der Teilkachel (Kern plus Rand).
- Vorbelegung der Vorstufe, wahlweise als Ausgang: `{{DATEN}}/{{LABELS}}`, `{{DATEN}}/{{SEGMENTE}}` (Klassen
  darin nach der festen Liste, für dich nur Hinweis).
- Bilder der ganzen Teilkachel: `{{BILDER}}` (`roh`, `kontrast`, `gitter`; `umriss`, `maengel`, `vorschlag` zeigen
  die Vorstufe), Verzeichnis `ansicht.json` dort.

## Werkzeuge

Alle Werkzeuge von landseg stehen dir frei (`{{REPO}}/README.md`; Befehle im Ordner `{{REPO}}` mit
`{{PY}} -B -m landseg …`, etwa `ansicht`, `zoom`, `eingriff`, `kante`, `pruefen`). Eigene Skripte als Datei in
`{{ERGEBNIS}}`, Python nur `{{PY}}`, nichts installieren, keine Fenster, keine Dauerprozesse.

## Ergebnis in `{{ERGEBNIS}}`

- `labels.tif`: einkanalig uint32 (zlib, wie `landseg.dateien.schreibe_labels`), Größe des Teilkachelbilds, kein
  Bildpunkt 0, jedes Segment zusammenhängend, IDs unter {{ID_GRENZE}}.
- `segmente.json`: `{"schema": "landseg-segmente/1", "segmente": [{"id": 1, "klasse": "Code", "grob": "Code der
  Ebene 1", "name": "kurz", "sicher": "ja|nein", "im_kern": true}], "verlauf": []}`, je ID der Karte genau ein
  Eintrag; Codes aus deiner Liste.
- `kategorien-teil.json`: deine Liste im Format von `{{REPO}}/kategorien.json` (`{"schema": "landseg-kategorien/1",
  "teilkachel": "{{TEILKACHEL}}", "classes": [{"code": "1", "name": "…", "parent": null, "level": 1, "color":
  "#rrggbb", "image_cue": "woran im Bild erkennbar"}, …]}`), gestufte Codes (`1`, `1.2`, `1.2.3`).
- `arbeitsweise.md`: wie du gearbeitet hast, warum diese Kategorien, was unsicher blieb.
- `ergebnis.jpg`: Grenzen und Klassenfarben über dem Bild, Kern umrandet, mit Legende.

Kontrolle (im Ordner `{{REPO}}`, muss mit `ok` enden):

```
{{PY}} -B -m landseg pruefen --labels {{ERGEBNIS}}/labels.tif --segmente {{ERGEBNIS}}/segmente.json --bild {{DATEN}}/{{TEILKACHEL_DATEI}} --kategorien {{ERGEBNIS}}/kategorien-teil.json
```

## Rückgabe

Zahl der Segmente (davon im Kern), Zahl der Klassen je Ebene, letzte Zeile von `pruefen`, die Arbeitsweise in
zwei Sätzen.
