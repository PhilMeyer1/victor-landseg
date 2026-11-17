# landseg

Werkzeuge für die Landschafts-Segmentierung von Luftbildern: Jedes Luftbild wird lückenlos in
Segmente zerlegt, und jedes Segment bekommt eine Kategorie aus einer festen, gestuften Liste.
Grundlage ist die Ermittlung `landseg-methode` im Wunsch-System (Basisordner, `wuensche/`).

## Inhalt

| Pfad | Was |
|---|---|
| `kategorien.json` | Kategorienliste, maschinenlesbar: 7 grobe Klassen (Codes 0 bis 6), 25 auf Ebene 2, 46 feinste Klassen; je Klasse Code, Name, Elternklasse, Ebene, Farbe, SW-Kennzeichen und Abbildungen auf CORINE, CLC+, FLAIR, DKM und Bericht 48; dazu die Regeln G1–G5 und U1–U5 und die Abweichungen A1–A4 |
| `KATEGORIEN.md` | Erklärung der Kategorienliste in Alltagssprache: Aufbau, Klassentabelle, Regeln, Abweichungen von Bericht 48, was noch ungesichert ist |
| `tools/pruefe_kategorien.py` | Prüfskript für `kategorien.json` (nur Python-Standardbibliothek) |

Die Werkzeuge selbst (Kacheln, Vorstufe, Bearbeiten, Prüfen, Zusammentragen) folgen.

## Kategorienliste prüfen

Im Repo-Ordner, mit dem Python des Stitcher-venv (dort nichts installieren) oder jedem Python 3:

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I tools/pruefe_kategorien.py kategorien.json
```

Ausgabe: die Zahlen je Ebene (`7/25/46`), die Zahl der Regeln (`5 G, 5 U`), der kleinste
Farbabstand und am Ende `ok`. Bei einem Fehler nennt das Skript die Stelle und endet mit Code 1.

## Daten

Originalbilder und abgeleitete Daten (Kacheln, Label-Karten) liegen nie im Repo: Originale unter
`daten/luftbilder/` des Basisordners (nur lesen), Abgeleitetes unter `daten/landseg/`.
