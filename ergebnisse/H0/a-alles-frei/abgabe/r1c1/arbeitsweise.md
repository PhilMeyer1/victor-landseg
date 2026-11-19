# Arbeitsweise H0 r1c1, Fassung A „Alles frei“

## Angesehen (in dieser Reihenfolge)

1. Ganzer Ausschnitt: `C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png` und das Gitter
   `C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/H0_raster.jpg` (r1c1 = unten rechts: Ortslage
   mit Streckhöfen, zwei Dorfstraßen, Acker im Südwesten).
2. Ganze Teilkachel: `C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r1c1/ganz_nummern.jpg`
   (Grenzen und Nummern der Vorstufe, Viertel) und `C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r1c1/ganz_roh.jpg`.
3. Danach das Teilkachelbild `teilkacheln/r1c1.png` in Ausschnitten (2-, 3-, 4- und 5-fach vergrößert,
   mit Koordinatengitter, Kontrast gespreizt).

## Schritte und Werkzeuge

Die Vorstufe habe ich nicht als Ausgang genommen (zu grob, Klassen nach der festen Liste), sondern die
Karte neu aufgebaut, alles mit eigenen Skripten im Ordner `arbeit/` (Python des Auftrags, `-B`):

1. **Atome** (`bauen.py`): Felzenszwalb-Übersegmentierung des ganzen Teilkachelbilds (scale 150,
   sigma 0,8, min 25). Die Grenzen folgen im Ort gut den Dach-, Hof- und Schattenkanten.
2. **Schattenfugen**: schmale dunkle Linien zwischen den Häuserzeilen (morphologisches Black-Hat,
   Scheibe 3, Schwelle 18, dunkler als 120) werden eigene Segmente (Klasse 5) und zerschneiden die Atome,
   so dass die langen Streckhof-Dächer einzeln stehen. Eine schwache Fuge habe ich von Hand verlängert.
3. **Felder** aus Atomen: alle Atome mit Mehrheit in einem groben Polygon werden ein Feld (Acker Südwest,
   Feld nordwestlich der Trift, Nordwestecke).
4. **Linienobjekte am Helligkeitsumschlag**: Straßen, Landstraße und Trift als Korridor um eine Leitlinie
   (Leitlinien aus Zeilenläufen heller Bildpunkte, `laeufe.py`), darin nur Bildpunkte mit geglättetem Grauwert
   ab 132–138, nur die Stücke, die die Leitlinie berühren, kleine Löcher gefüllt. Baumreihe/Gehölzsaum: im
   Saum zwischen Acker und Straße alle dunklen Bildpunkte (≤ 88–92), geöffnet; der Rest des Saums ist Rain.
5. **Grauregel** für alle übrigen Ortssegmente: < 52 Schlagschatten, < 90 Dach im Eigenschatten,
   < 140 Gebäude, sonst Dach besonnt – immer `sicher: false`.
6. **Durchsicht**: 12 Prüfbilder (links Rohbild, rechts Klassenfarben mit IDs; zuletzt 175 × 175 Bildpunkte
   vierfach), die den ganzen Kern abdecken. Korrekturen als Punkte (`korrekturen.json`, `urteil.py`):
   Höfe, Gärten im Blockinneren, Gehölz, Rain, Straßeneinmündung, Innenhof des Vierseithofs, sichere
   Schatten; zwei Polygone von Hand (heller Rechteckfleck am Straßenrand, verengtes Straßenstück Mitte).
7. Kleinstücke unter 12 Bildpunkten mit dem Nachbarn der längsten Grenze verschmolzen, jedes Segment
   zusammenhängend (4er-Nachbarschaft), `pruefen` endet mit `ok`.
8. `abschluss.py`: `offen`/`nicht_geprueft` in `segmente.json`, `ergebnis.jpg` mit Legende.

Läufe: `bauen.py` rund 14-mal (Korridore zweimal neu vermessen, Fugen eingeführt, Korrekturen), etwa
40 Bilder angesehen. Ungefähre Zeit: 1,5 bis 2 Stunden Agentenzeit.

## Warum diese Kategorien

Gestuft nach dem, was der Schwarz-Weiß-Scan bei 0,45 m hergibt:

- **1 Bebaute Grundstücksfläche** – 1.1 Gebäude (1.1.1 Dach besonnt / 1.1.2 Dach im Eigenschatten),
  1.2 Hof, 1.3 Garten. Die Dachhälften sind auf SW das Deutlichste an einem Haus (Satteldach: eine Hälfte
  hell, die andere dunkel); die Nutzung (Wohnhaus, Scheune, Stall) ist nicht zu sehen, darum keine Stufe dafür.
- **2 Verkehrsfläche** – 2.1 Straße im Ort, 2.2 Landstraße, 2.3 Feldweg/Trift. Belag (Asphalt, Pflaster,
  Schotter) ist auf SW nicht zu trennen und darum keine Klasse.
- **3 Landwirtschaftliche Fläche** – nur 3.1 Acker als Unterklasse, weil nur die Streifenflur sicher als
  Acker erkennbar ist; Grünland bleibt in der Elternklasse 3.
- **4 Gehölz** – 4.1 Baumreihe/Einzelbäume an Straße oder Rain.
- **5 Schlagschatten** – eigene Klasse, weil der Scan große schwarze Flächen hat, unter denen der Untergrund
  nicht zu erkennen ist; sie einer Klasse darunter zuzuschlagen wäre geraten.

## Was unsicher blieb

- Alle Ortssegmente aus der Grauregel (490 im Kern) sind nur nach Grauton vorklassifiziert und stehen mit
  `sicher: false`; einzeln geprüft und umgestellt sind nur die Segmente mit Quelle `korrektur`.
- Dach gegen Hof bei hellen, glatten Flächen ohne Traufkante (z. B. heller Block an der Straße bei x 175, y 165,
  Rechteckfleck bei x 210, y 282).
- Garten gegen Wiese oder Acker im Blockinneren (große mittelgraue Flächen um x 470, y 200 und x 350, y 430).
- Baumkrone gegen dunkles Dach (dunkle Bahn bei x 330, y 280; Gehölz bei x 405, y 245).
- Trift: Weg, Viehtrift oder Brachstreifen; Feld nordwestlich: Acker oder Grünland.
- Der Gehölzsaum an der Dorfstraße ist als Band zusammengefasst; Einzelkronen fließen bei 0,45 m ineinander.
- Die Streifen der Streifenflur sind nicht als Einzelparzellen getrennt (Grenzen zu schwach).

## Auf Schwarz-Weiß nicht zu trennen

Acker gegen Grünland; Dach gegen Hof (bei hellen Flächen ohne Schatten); Hof gegen Garten bei mittlerem Grau;
Belag der Straßen; Wohnhaus gegen Wirtschaftsgebäude; Baum gegen Strauch/Hecke; Untergrund unter Schatten.
Im Farbbild würden Dachrot gegen Erd- und Pflastergrau, Grün des Bewuchses und Kronenform entscheiden.
