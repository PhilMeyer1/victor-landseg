# Vorbild: Prüfseite der Stitcher-Session („Kachel mit korrigierten Masken")

Quelle (nur lesen, Zwischenordner, kann verschwinden):
`C:/Users/Phil/AppData/Local/Temp/claude/6bc45b42c5448cb2/6e02ebfe-8ebf-4cf1-90c0-685926031afe/scratchpad/aufbereitung/kachel_direkt/index.html`
(Bau-Skript daneben: `bau.py`; Kopf der Seite: `quelle/seite.html`). Nicht im Browser angesehen;
die Angaben stammen aus dem Stylesheet am Kopf der Datei und aus dem Nachvollzug der Session.
Der Nutzer kennt diese Seite und fand die Arbeit damit gut.

## Farben und Schrift (aus `:root` der Seite)

- Hintergrund `#0e0f11`, Flächen (Leiste, Dock) `#16181b`, Linien `#2a2d32`
- Text `#d6d8dc`, leiser Text `#8b9099`, Akzent `#ffeb3c` (Gelb)
- Detailbereich `#131518`, Markierung an: Hintergrund `#7a1f63`, Rand `#ff7ad9`
- Schrift 13px/1.45 "Segoe UI", system-ui; kleine Angaben 11–12px
- dunkle Oberfläche, ganze Fensterhöhe, kein Seitenscrollen (`overflow:hidden`)

## Aufbau

- Raster: links die große Bildfläche (Rest der Breite), rechts eine feste Leiste von 380px über
  die ganze Höhe; unter dem Bild schmale Zeilen (Legende mit Kategorien und Zählung, Hinweise).
- Rechte Leiste von oben: Kopfblock (Titel, Stand, Filterknöpfe, Trefferzahl), Details zum
  gewählten Segment (Vorschaubild 140 × 140, Name, Kategorie, Fläche), darunter scrollbare
  Segmentliste mit Vorschaubildern, unten ein Dock mit dem Kommentarfeld.
- Reiter „Kommentare" und „Hinweise".

## Bedienung

- Mausrad zoomt, Ziehen verschiebt, Klick wählt ein Segment und passt es ein, Hover hebt hervor.
- Tasten: V nächster Stand, Leertaste voriger Stand, M Fläche/Umriss, X Masken aus/an,
  G Ebene „Geändert", B Beschriftung, F nächste offene Frage, K Kommentar, 1–6 Kategorie.
- Stände umschaltbar (Ausgang, vor Korrektur, Runde 1, Runde 2); Kommentare als JSON exportierbar.
- Technik: eine HTML-Datei, läuft über file:// ohne Server; Masken als Lauflängen-Daten in der
  Seite; Bild als Teilbilder in Zoomstufen daneben.

## Was für die Landschaft dazukommt (aus dem Wunsch)

- Umschalten grobe/feine Kategorie-Ebene (3 Stufen: 7/25/46), Lückenkarte (unvergebene
  Bildpunkte, soll leer sein), Naht-Ebene (Grenzen der Teilkacheln und Verstöße), Vorher/Nachher.
- Viel mehr und flächige Segmente statt einzelner Objekte auf freiem Grund: Die Liste braucht
  Filter nach Kategorie und „unsicher"; Farben je Kategorie müssen auf einem Luftbild lesbar sein.
- Letzter Nutzerwunsch an die Stitcher-Seite (noch nicht umgesetzt): Seitenleiste aufräumen, so
  einfach, dass sie jeder ohne Erklärung versteht.
