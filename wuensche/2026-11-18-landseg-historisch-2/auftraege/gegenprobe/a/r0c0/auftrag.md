# Auftrag: H0, Teilkachel r0c0 frei segmentieren und klassifizieren (Fassung A „Alles frei“)

Antworte auf Deutsch. Diese Abgabe gehört zu Fassung A „Alles frei“, einem Vergleichsmuster: Du wählst
Kategorien und Arbeitsweise selbst, ohne feste Kategorienliste und ohne die Arbeitsregeln des Skills
`landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`; lesen darfst du ihn, er bindet
dich hier nicht). Fest bleiben nur: lückenlos (jeder Bildpunkt der Teilkachel gehört genau einem
Segment, keine 0), eigener Ordner (du schreibst nur in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/a-alles-frei/abgabe-gegenprobe/r0c0`), Eingaben nur lesen.

Ziel: das Landschaftsbild so fein segmentieren, wie im Bild sicher erkennbar (Einzelbaum, schmaler
Weg, einzelnes Haus eines Streckhofs), und jedem Segment eine Klasse aus deiner eigenen, gestuften Liste geben.

Zuerst siehst du den ganzen Ausschnitt H0 an (`C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png`, Gitter `C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/H0_raster.jpg`),
dann deine Teilkachel (`C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r0c0/ganz_roh.jpg`, mit Grenzen der Vorstufe `C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r0c0/ganz_nummern.jpg`), und nennst beide
in `arbeitsweise.md`.

## Schwarz-Weiß-Scan (gilt für H0)

H0 ist ein Ausschnitt von 1000 × 1000 Bildpunkten aus einem eingescannten Schwarz-Weiß-Luftbild von
1968 (`daten/luftbilder/historisch/1968105_0014_0228.tif`, x 1500, y 2000): Ortsrand mit Streckhöfen
(lange schmale Häuser in Reihen), Straßen, ein kleiner Anger, Äcker mit Streifenflur. Das Bild hat einen
Kanal; alle Bilder zeigen es als RGB mit drei gleichen Kanälen. Es hat keine Lagedaten (keine
Weltdatei, `georeferenz: null` im Manifest); ein Bildpunkt sind etwa 0,45 m (geschätzt; das farbige Orthofoto hat 0,2 m).

- Farbe gibt es nicht: Urteile nach Grauton, Textur, Form, Schatten und Lage zu den Nachbarn.
- Die SW-Spalte (`bw`) in `kategorien.json` ist eine ungeprüfte Vermutung, kein Beleg.
- Ist eine feine Klasse auf Schwarz-Weiß nicht sicher zu unterscheiden (etwa Acker gegen Grünland,
  Dach gegen Hof, Belag eines Weges), nimm die Klasse der Ebene darüber, setze `sicher: false` und
  schreibe unter `offen`, was im Farbbild entscheiden würde.
- Die Klassen der Vorstufe sind auf dem Scan schwach (SAM 3 ist für Farb-Orthofotos gebaut; über
  90 % `sicher: nein`, Äcker teils als Gebäude): nur Hinweis.
- Die Vorstufe lief mit kleinerem SAM-3-Fenster (420 Bildpunkte, Schiebefenster) und niedriger
  Instanzschwelle (`C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-2/vorstufe-h0.json`), damit die Streckhöfe einzeln erscheinen. Gerade Grenzen
  mitten in einer gleichförmigen Fläche (etwa bei x 208 oder 420 im Teilkachelbild) können vom
  Schiebefenster stammen: dann ist es keine Bildkante.

## Unabhängig urteilen

Du bist die Gegenprobe: Ein anderer Agent bearbeitet dieselbe Teilkachel in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/a-alles-frei/abgabe/r0c0`. Sein Ergebnis siehst du nicht an, auch nicht, wenn es schon da ist. Aus beiden Abgaben wird die Übereinstimmung (PQ, Boundary-PQ) gemessen.

## Daten (nur lesen)

- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/manifest.json`: Eintrag `r0c0` unter `teilkacheln` mit `bild`, `kern_im_bild` (Lage des
  Kerns im Teilkachelbild) und `kern`. Maßgeblich ist der Kern; der Kontextrand dient zum Ansehen,
  dort zählt beim Zusammentragen nichts.
- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r0c0.png`: das Bild der Teilkachel (Kern plus Rand, 628 × 628, ein Kanal).
- Vorbelegung der Vorstufe, wahlweise als Ausgang: `C:/Users/Phil/Developement/Victor/daten/landseg/H0/vorstufe/r0c0/labels.tif`,
  `segmente.json`, `kandidaten.json` (Klassen darin nach der festen Liste, für dich nur Hinweis).
- Bilder der ganzen Teilkachel: `C:/Users/Phil/Developement/Victor/daten/landseg/H0/a-alles-frei/ansicht/r0c0/teilkachel/` (`roh`, `kontrast`, `gitter`; `umriss`,
  `maengel`, `vorschlag` zeigen die Vorstufe), Verzeichnis `C:/Users/Phil/Developement/Victor/daten/landseg/H0/a-alles-frei/ansicht/r0c0/ansicht.json`.

## Werkzeuge

Alle Werkzeuge von landseg stehen dir frei (`C:/Users/Phil/Developement/Victor/landseg/README.md`; Befehle im Ordner `C:/Users/Phil/Developement/Victor/landseg` mit
`C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -m landseg …`, etwa `ansicht`, `eingriff`, `kante`, `pruefen`). Eigene Skripte als Datei in
`C:/Users/Phil/Developement/Victor/daten/landseg/H0/a-alles-frei/abgabe-gegenprobe/r0c0`, Python nur `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe`, nichts installieren, keine Fenster, keine Dauerprozesse.

## Ergebnis in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/a-alles-frei/abgabe-gegenprobe/r0c0`

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
  warum diese Kategorien, was unsicher blieb, welche Klassen auf Schwarz-Weiß nicht zu trennen waren.
- `ergebnis.jpg`: Grenzen und Klassenfarben über dem Bild, Kern umrandet, mit Legende.

Kontrolle (im Ordner `C:/Users/Phil/Developement/Victor/landseg`, muss mit `ok` enden):

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -m landseg pruefen --labels C:/Users/Phil/Developement/Victor/daten/landseg/H0/a-alles-frei/abgabe-gegenprobe/r0c0/labels.tif --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/a-alles-frei/abgabe-gegenprobe/r0c0/segmente.json --bild C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r0c0.png --kategorien C:/Users/Phil/Developement/Victor/daten/landseg/H0/a-alles-frei/abgabe-gegenprobe/r0c0/kategorien-teil.json
```

## Rückgabe

Zahl der Segmente (davon im Kern), Zahl der Klassen je Ebene, letzte Zeile von `pruefen`, die
Arbeitsweise in zwei Sätzen.
