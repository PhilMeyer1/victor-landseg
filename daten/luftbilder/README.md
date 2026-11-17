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

| Datei | Größe (Bytes) | SHA-256 |
|---|---:|---|
| `orthofoto-aktuell/0009626524_100_Orthophoto_aktuell_5236-55.tif` | 93790448 | `493cdd0d833511c06fc0b74cf3ba3dee750123a76f1e7eaffbfc66c3266661b7` |
| `orthofoto-aktuell/0009626524_100_Orthophoto_aktuell_5236-55.TFW` | 156 | `9f1703b91906063c039fccc6ca3c8c5449d8b8357b33b8dbdbb2952265d56a40` |
| `orthofoto-aktuell/0009626524_100_Orthophoto_aktuell_5236-55.PRJ` | 654 | `d646af221dd5175c9c30875409d948d8e0e70f520c3825ef266d634123958cbe` |
| `orthofoto-aktuell/0009626524_100_Orthophoto_aktuell_5236-56.tif` | 93790448 | `28b3c1e66ad22ef3bd3f3ebd587257256de441829775acc8e50352523ccfb4e8` |
| `orthofoto-aktuell/0009626524_100_Orthophoto_aktuell_5236-56.TFW` | 156 | `a45ce3d89e029f0ea7a51fc647471b2567eb6baeaf3fec0f5fb5dce031912690` |
| `orthofoto-aktuell/0009626524_100_Orthophoto_aktuell_5236-56.PRJ` | 654 | `d646af221dd5175c9c30875409d948d8e0e70f520c3825ef266d634123958cbe` |
| `historisch/1957004_004A_1557.tif` | 165742246 | `0e09cfd447f4dc14c8f55d5178bf1e217fe40393fcaf78b980a6b00fa3af96f8` |
| `historisch/1968105_0014_0228.tif` | 256583547 | `79f3e033067a33b77213200c4e85d34ea97fc57ecfbf4231f7e8446c1b04d5d9` |

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
