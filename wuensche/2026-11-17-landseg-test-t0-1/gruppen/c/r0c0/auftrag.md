# Auftrag: Teilkachel r0c0 frei segmentieren und klassifizieren (Fassung C: alles frei)

Antworte auf Deutsch. Diese Abgabe gehört zu Fassung C, einem Vergleichsmuster: Du wählst Kategorien
und Arbeitsweise selbst, ohne feste Kategorienliste und ohne die Arbeitsregeln des Skills
`landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`; lesen darfst du ihn, er bindet
dich hier nicht). Fest bleiben nur: lückenlos (jeder Bildpunkt der Teilkachel gehört genau einem
Segment, keine 0), eigener Ordner (du schreibst nur in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c/abgabe/r0c0`), Eingaben nur lesen.

Ziel: das Landschaftsbild so fein segmentieren, wie im Bild sicher erkennbar (Einzelbaum, schmaler
Weg, kleines Gebäude), und jedem Segment eine Klasse aus deiner eigenen, gestuften Liste geben.

## Daten (nur lesen)

- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c/manifest.json`: Eintrag `r0c0` unter `teilkacheln` mit `bild`, `kern_im_bild` (Lage des
  Kerns im Teilkachelbild) und `kern`. Maßgeblich ist der Kern; der Kontextrand dient zum Ansehen,
  dort zählt beim Zusammentragen nichts.
- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c/teilkacheln/r0c0.png`: das Bild der Teilkachel (Kern plus Rand, 628 × 628).
- Vorbelegung der Vorstufe, wahlweise als Ausgang: `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c/vorstufe/r0c0/labels.tif`,
  `segmente.json`, `kandidaten.json` (Klassen darin nach der festen Liste, für dich nur Hinweis).
- Bilder der ganzen Teilkachel: `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c/ansicht/r0c0/teilkachel/` (`roh`, `kontrast`, `gitter`; `umriss`,
  `maengel`, `vorschlag` zeigen die Vorstufe), Verzeichnis `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c/ansicht/r0c0/ansicht.json`.

## Werkzeuge

Alle Werkzeuge von landseg stehen dir frei (`C:/Users/Phil/Developement/Victor/landseg/README.md`; Befehle im Ordner `C:/Users/Phil/Developement/Victor/landseg` mit
`C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -m landseg …`, etwa `ansicht`, `eingriff`, `kante`, `pruefen`). Eigene Skripte als Datei in
`C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c/abgabe/r0c0`, Python nur `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe`, nichts installieren, keine Fenster, keine Dauerprozesse.

## Ergebnis in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c/abgabe/r0c0`

- `labels.tif`: einkanalig uint32 (über `tifffile`, zlib, wie `landseg.dateien.schreibe_labels`),
  Größe des Teilkachelbilds (628 × 628), kein Bildpunkt 0, jedes Segment zusammenhängend.
- `segmente.json`: `{"schema": "landseg-segmente/1", "segmente": [{"id": 1, "klasse": "Code", "grob": "Code der
  Ebene 1", "name": "kurz", "im_kern": true}], "verlauf": []}`, je ID der Karte genau ein Eintrag;
  Codes aus deiner Liste.
- `kategorien-teil.json`: deine Liste im Format von `C:/Users/Phil/Developement/Victor/landseg/kategorien.json`:
  `{"schema": "landseg-kategorien/1", "teilkachel": "r0c0", "classes": [{"code": "1", "name": "…",
  "parent": null, "level": 1, "color": "#rrggbb", "image_cue": "woran im Bild erkennbar"}, …]}`,
  gestufte Codes (`1`, `1.2`, `1.2.3`), so viele Ebenen und Klassen, wie du für richtig hältst.
- `arbeitsweise.md`: wie du gearbeitet hast (Schritte, Werkzeuge, Zahl der Läufe, ungefähre Zeit),
  warum diese Kategorien, was unsicher blieb.
- `ergebnis.jpg`: Grenzen und Klassenfarben über dem Bild, Kern umrandet, mit Legende.

Kontrolle (im Ordner `C:/Users/Phil/Developement/Victor/landseg`, muss mit `ok` enden):

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -m landseg pruefen --labels C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c/abgabe/r0c0/labels.tif --segmente C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c/abgabe/r0c0/segmente.json --bild C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c/teilkacheln/r0c0.png --kategorien C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-c/abgabe/r0c0/kategorien-teil.json
```

## Rückgabe

Zahl der Segmente (davon im Kern), Zahl der Klassen je Ebene, letzte Zeile von `pruefen`, die
Arbeitsweise in zwei Sätzen.
