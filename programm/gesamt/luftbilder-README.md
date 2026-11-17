# Original-Luftbilder (nicht im Projekt)

Die Original-Luftbilder sind zu groß für GitHub (einzelne Dateien über 100 MB) und liegen deshalb
nicht in diesem Projekt. Du bekommst sie getrennt (Download-Link). Lege sie genau so in diesen
Ordner `daten/luftbilder/`, mit unveränderten Dateinamen und den zwei Unterordnern:

```
daten/luftbilder/
  orthofoto-aktuell/   die sechs Dateien 0009626524_100_Orthophoto_aktuell_5236-55/-56 (.tif, .TFW, .PRJ)
  historisch/          die zwei Scans 1957004_004A_1557.tif und 1968105_0014_0228.tif
```

Die Lagedateien (`.TFW`, `.PRJ`) gehören über den gleichen Namen zu ihrem Bild; sie müssen neben
dem `.tif` liegen. Git nimmt die Bilder hier nicht auf (`.gitignore`), sie bleiben nur bei dir.

<!-- TABELLE -->

- `orthofoto-aktuell/`: zwei Kacheln eines aktuellen Orthofotos (Blätter 5236-55 und 5236-56),
  0,2 m je Bildpunkt, Lagebezug MGI / Austria GK Central, EPSG:31255. Der Test T0 ist ein
  Ausschnitt aus Blatt 5236-56.
- `historisch/`: zwei historische Luftbild-Scans ohne Lagedateien (nach den Dateinamen 1957 und 1968).

Prüfen, ob alles richtig liegt (im Projektordner, also eine Ebene über `daten/`):

```
python -B programm/tools/gesamt_projekt.py pruefen --ziel . --luftbilder daten/luftbilder
```

Erwartet ist die Zeile „Luftbilder: 8 von 8 passen“. Fehlt eine Datei oder ist sie anders, nennt
der Befehl sie mit Namen und endet mit Exit-Code 1.
