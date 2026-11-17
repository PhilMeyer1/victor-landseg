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
| `landseg/` | Python-Paket mit den Werkzeugen, ein Modul je Werkzeug; Befehlszeile `python -m landseg <befehl>` |
| `landseg/kacheln.py` | W1 `kacheln`: Arbeitsausschnitt aus einem Luftbild, Teilkacheln (Kern + Kontextrand), Manifest mit Georeferenz |
| `landseg/eingriff.py` | W5 `eingriff`: Bearbeiten der Label-Karte (verschmelzen, teilen, Grenze verschieben, Klasse setzen, Polygon zuweisen), immer lückenlos, mit Verlauf |
| `landseg/pruefen.py` | W6 `pruefen`: Wächter der Lückenlosigkeit (H × W ohne 0, Zusammenhang je Segment, gültige Klassen) |
| `landseg/zusammentragen.py` | W7 `zusammentragen`: Abgaben der Teilkacheln (je Teilkachel die letzte Runde, nur der Kern) zur Label-Karte des Ausschnitts; Einheiten, Klassen des Nutzers und offene Fragen aus einem JSON-Auftrag |
| `landseg/naht.py` | Nahtregel: an jeder Kerngrenze gleiche ID oder echte Bildkante, gleiche Klasse |
| `vorlagen/` | Auftragsvorlagen für Agents (Urteil, Umsetzen, Korrektur, Naht) mit Platzhaltern, erklärt in `vorlagen/README.md` |
| `.claude/skills/landseg-agent/SKILL.md` | Agent-Skill mit den Arbeitsregeln für diese Aufträge |
| `landseg/kategorien.py`, `landseg/dateien.py` | Kategorienliste laden; Lesen und Schreiben von Label-Karte, `segmente.json`, Manifest |
| `tests/` | Tests (Python-Standardmodul `unittest`, synthetische Bilder und Label-Karten) |

Die übrigen Werkzeuge (Vorstufe, Ansicht, Kante, Prüfseite) folgen.

## Umgebung

Das Repo hat noch keine eigene Python-Umgebung. Alle Befehle laufen mit dem Python des Stitcher-venv
(dort nichts installieren): `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe`,
unten kurz `PY`. Aufruf immer im Repo-Ordner, damit Python das Paket `landseg` findet.

## Begriffe und Dateien

- **Label-Karte** (`labels.tif`): für jeden Bildpunkt die Nummer (ID) seines Segments, 32 Bit ohne
  Vorzeichen; 0 heißt „kein Segment“ und darf in einer fertigen Karte nicht vorkommen. Gespeichert als
  einkanaliges TIFF, weil PNG nur bis 16 Bit reicht.
- **`segmente.json`**: je Segment `id`, `klasse` (Code aus `kategorien.json`, feinste sichere Ebene),
  `grob` (Ebene-1-Klasse), dazu Felder wie `herkunft`; unter `verlauf` jeder Eingriff mit Zeit und
  Bearbeiter.
- **Manifest** (`manifest.json`, von `kacheln`): Quelle, Ausschnitt, Raster und je Teilkachel Bild,
  Kern, Kontext und Lage. Alle Pfade relativ zum Ordner des Manifests. Koordinaten in Bildpunkten:
  `kern` und `kontext` relativ zum Ausschnitt, `kern_im_bild` relativ zum Bild der Teilkachel;
  `transform` rechnet die Ecke oben links eines Bildpunkts in Landeskoordinaten um (EPSG aus der
  `.prj`). Neben jedem PNG liegt eine Weltdatei `.pgw` für GIS-Programme.
- **Zusammenhang** heißt: Bildpunkte eines Segments hängen über gemeinsame Kanten zusammen (nur über
  eine Ecke reicht nicht).

## Befehle

Abgeleitete Daten gehören nach `daten/landseg/` im Basisordner, nie ins Repo und nie zu den
Originalen. Exit-Code 0 = in Ordnung, 1 = Befund bzw. Eingriff abgelehnt, 2 = Aufruf- oder Lesefehler.

### kacheln

Testfenster T0 (Blatt 5236-56, x 2000, y 2400, 1000 × 1000 Bildpunkte) in vier Teilkacheln mit
Kern 500 und Kontextrand 64:

```
PY -m landseg kacheln --bild ../daten/luftbilder/orthofoto-aktuell/0009626524_100_Orthophoto_aktuell_5236-56.tif \
   --x 2000 --y 2400 --breite 1000 --hoehe 1000 --kern 500 --rand 64 --name T0 --ziel ../daten/landseg/T0/kern500
```

Ergebnis: `T0.png` (ganzer Ausschnitt), `teilkacheln/r<zeile>c<spalte>.png` (Kern plus Rand, Rand
aus dem Originalbild, nur am Bildrand abgeschnitten) und `manifest.json`. Die Kerngröße ist frei
(`--kern 250` ergibt 16 Teilkacheln); geht sie nicht auf, sind die letzten Kerne kleiner. Ein
vorhandenes Manifest wird nur mit `--ueberschreiben` ersetzt.

### pruefen

```
PY -m landseg pruefen --labels <labels.tif> --segmente <segmente.json> --bild <teilkachel.png>
```

Meldet `H × W`, die Zahl der Bildpunkte ohne Segment, die Zahl der Segmente und endet mit `ok` oder
`FEHLER` samt Liste der Mängel (Lücke, nicht zusammenhängend, Segment ohne Eintrag oder ohne
Bildpunkte, ungültige Klasse). `--form HxW` statt `--bild` gibt die erwartete Größe direkt an,
`--kategorien` eine andere Kategorienliste, `--mindestflaeche N` meldet kleinere Segmente, `--json`
gibt den Befund maschinenlesbar aus.

### eingriff

```
PY -m landseg eingriff --labels <labels.tif> --segmente <segmente.json> --bearbeiter <name> <operation> ...
```

| Operation | Wirkung |
|---|---|
| `verschmelzen --ids 3,5 [--ziel 3]` | benachbarte Segmente zu einem; das Ziel (Standard: erste ID) behält ID und Klasse |
| `teilen --id 4 --linie "x,y;x,y;..."` | teilt ein Segment entlang eines Linienzugs; das größte Teil behält die ID |
| `verschieben --von 5 --nach 3 --flaeche "x,y;..."` | Bildpunkte von 5 im Polygon gehen an den Nachbarn 3 (Grenze verschieben) |
| `klasse --id 4 --klasse 3.1` | setzt die Klasse (und die grobe Klasse) |
| `polygon --flaeche "x,y;..." (--id N \| --klasse C)` | alles im Polygon an ein angrenzendes Segment oder an ein neues mit Klasse; dadurch zerteilte Nachbarn bekommen eigene IDs |
| `stapel --datei schritte.json` | mehrere Schritte `{"schritte": [{"op": "teilen", "id": 4, "linie": [[0, 5], [9, 5]]}, ...]}`, alle oder keiner |

Koordinaten sind Bildpunkte der Label-Karte (`x` Spalte, `y` Zeile). Ein Eingriff schreibt nur
Segment-Nummern auf vorhandene Bildpunkte um, Lücken entstehen also nie. Ist er nicht ausführbar
(Segmente nicht benachbart, Linie trennt nicht, Klasse unbekannt), bleibt alles unverändert. Danach
läuft `pruefen` von selbst und meldet den Befund.

### zusammentragen

```
PY -m landseg zusammentragen --datei <ordner>/zusammentragen.json
```

Der Auftrag `zusammentragen.json` (Pfade relativ zu seinem Ordner) nennt alles Fallbezogene:

```
{"schema": "landseg-zusammentragen/1",
 "manifest": "manifest.json",
 "ausgang": "vorstufe/segmente.json",
 "einheiten": [{"teilkachel": "r0c0", "labels": "umsetzen/r0c0/labels.tif",
                "segmente": "umsetzen/r0c0/segmente.json", "runde": 0, "name": "ums-r0c0"}],
 "nutzerklassen": [{"id": 17, "klasse": "3.1.1", "kommentar": "Einzelbaum"}],
 "fragen": [{"id": "F1", "text": "Weg oder Feldrain?", "segmente": [17]}],
 "naht": {"kante_schwelle": 25, "kante_band": 1, "mindestlaenge": 1},
 "naht_bestaetigt": [{"naht": "r0c0|r0c1", "ids": [3, 7], "grund": "Feldgrenze, kaum Farbsprung"}],
 "ziel": "zusammen"}
```

- `einheiten`: je Teilkachel eine Abgabe; gibt es mehrere, gilt die mit der höchsten `runde`
  (Korrekturrunden). Die Label-Karte hat die Größe des Teilkachelbilds (dann zählt nur der Kern)
  oder nur des Kerns. Eine Teilkachel ohne Einheit bleibt leer und fällt in `pruefen` als Lücke auf.
- `ausgang` (wahlweise): `segmente.json` der Vorstufe; deren IDs gelten als global. Eine andere ID,
  die mehrere Teilkacheln neu vergeben haben, bekommt außer in der ersten eine neue Nummer
  (`umbenannt`). Ohne `ausgang` gelten alle IDs als global.
- `nutzerklassen`: Klassen, die der Nutzer festgelegt hat; sie gehen allem vor und entscheiden
  auch einen Klassenkonflikt an der Naht. `fragen`: offene Fragen für die Prüfseite; das Ergebnis
  ergänzt je Frage die Lage (`bbox` [x0, y0, x1, y1] im Ausschnitt).
- `naht`, `naht_bestaetigt` (wahlweise): Einstellungen der Nahtregel und Grenzen, die ein
  Bearbeiter am Bild als echt bestätigt hat.

Ergebnis im Ordner `ziel`: `labels.tif` (ganzer Ausschnitt), `segmente.json` (je Segment mit
`teilkacheln`, dazu `fragen` und `verlauf`) und `naht.json` (Nahtbefund, Klassenkonflikte,
Umbenennungen, Mängel, Befund von `pruefen`). Die Ausgabe endet mit `Zusammentragen ok` oder
`Zusammentragen FEHLER`; dann Exit-Code 1, die Dateien werden trotzdem geschrieben (der Naht-Agent
braucht sie). `--ziel` schreibt woandershin, `--json` gibt das Ergebnis maschinenlesbar aus.

**Nahtregel.** An jeder Kerngrenze zweier Nachbarkacheln stehen sich je Position zwei Bildpunkte
gegenüber. Sie tragen dieselbe ID, oder zwischen ihnen liegt eine echte Bildkante (Farbsprung von
mindestens `kante_schwelle`, gesucht bis `kante_band` Bildpunkte neben der Grenze). Sonst ist es ein
Verstoß `ohne_kante` (zwei Bearbeiter haben dieselbe Fläche verschieden zugeordnet, oder die Grenze
ist nur die Gerade der Kachelung). Eine ID, die in zwei Teilkacheln vorkommt, muss dort dieselbe
Klasse haben, sonst Verstoß `klasse`. Strecken kürzer als `mindestlaenge` zählen nicht.

### naht

```
PY -m landseg naht --manifest <manifest.json> --labels <labels.tif des Ausschnitts> [--datei zusammentragen.json]
```

Prüft nur den ID-Teil der Nahtregel auf einer schon zusammengetragenen Label-Karte, etwa nach einem
Eingriff des Naht-Agents; `--datei` liefert Einstellungen und bestätigte Grenzen.

## Auftragsvorlagen

`vorlagen/urteil.md`, `umsetzen.md`, `korrektur.md`, `naht.md`: Aufträge für Agents mit Platzhaltern
`{{NAME}}` (Liste in `vorlagen/README.md`), ohne Pfade dieses Rechners. Die Regeln, die für alle
gelten, stehen im Skill `.claude/skills/landseg-agent/SKILL.md`.

## Tests

```
PY -B -m unittest discover -s tests -t .
```

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
