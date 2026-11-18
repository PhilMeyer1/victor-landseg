# Arbeitsweise r1c0, Fassung A „Alles frei“

## Angesehene Bilder (in dieser Reihenfolge)

1. Ganzer Ausschnitt H0: `C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png` und Gitter
   `C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/H0_raster.jpg` (Ortsrand mit Streckhöfen
   rechts oben, Landstraße schräg durch r1c0, Streifenflur links unten).
2. Ganze Teilkachel r1c0: `C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r1c0/ganz_nummern.jpg`
   (Grenzen und Nummern der Vorstufe, Viertel v1–v4) und
   `C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r1c0/ganz_roh.jpg`.

Danach eigene Ansichten aus `teilkacheln/r1c0.png` (Ordner `arbeit/`): vier Viertel 4-fach
(`v1.jpg` bis `v4.jpg`), Übersicht 3-fach mit Kontraststreckung (`ueber.jpg`), geglättet
(`glatt.jpg`), Linienfilter (dunkle/helle Linien, `linien.jpg`), entlang der Streifenrichtung gedreht
und gemittelt (`dreh_strasse.jpg`, `dreh_l1.jpg`), Nahaufnahmen Hof (`hof.jpg`, `hofunter.jpg`),
Nordost (`nordost.jpg`) und Feldweg West (`l1zone.jpg`).

## Vorgehen

- Die Vorstufe habe ich nur angesehen, nicht als Ausgang benutzt: Sie ist auf dem Scan zu grob
  (Brache, Feldweg und Feld in einem Segment, Hof und Feld vermischt).
- Aufbau der Karte in `arbeit/bauen.py`, gemalt in fester Reihenfolge (später überschreibt früher):
  1. Feldparzellen als Flächen zwischen den Linien (Straße, Feldwege, Raine), Streifen der
     Streifenflur im Feld zwischen den beiden Rainwegen über die Lage quer zur Straße (Grauwert-Profil
     je 6 Bildpunkte, Kante des dunklen Streifens bei u≈456) und eine leicht schräge helle Bahn;
  2. helle Brache mit Gehölz und helle Flecken in den Feldern über eine Schwelle im geglätteten Bild
     (σ = 4) gegen den Median der Parzelle, damit die Grenzen auf dem Helligkeitsumschlag liegen;
  3. Hof (helle Lagerfläche, graue Hoffläche, Gebäude, schwarze Fläche) als Polygone aus der
     8-fachen Nahaufnahme;
  4. Straße, Seitenweg und Hofzufahrt als helle Bildpunkte in einem Band um den Linienzug (Schwelle
     zwischen Mitte und Umgebung; Straßenmitte je 20 Spalten aus dem Helligkeitsmaximum bestimmt);
  5. schmale Linien (Feldwege mit Gräben, Raine, Gräben) als Bänder fester Breite (2,5–5,5 Bildpunkte)
     um von Hand nachgezogene Linienzüge aus dem Linienfilter;
  6. dunkle Einzelobjekte als dunkelste zusammenhängende Stelle in einem kleinen Kasten.
- `arbeit/fertig.py`: jede ID nur noch ein zusammenhängendes Stück (4er-Nachbarschaft); kleine
  Splitter gehen an den häufigsten Nachbarn, Stücke ab 300 Bildpunkte werden eigene Segmente
  (drei Fälle: Feldsaum zwischen Brache und Feldweg West, Feldzwickel am Westende des hellen Streifens,
  Feldstück am Westrand im Kontext). Dann Nummerierung, `labels.tif` über
  `landseg.dateien.schreibe_labels`, `segmente.json`, `kategorien-teil.json`, `ergebnis.jpg`.
- Kontrolle mit `landseg pruefen`: letzte Zeile `ok`.
- Läufe: `bauen.py` 4-mal, `fertig.py` 4-mal, `pruefen` 1-mal; jedes Zwischenbild angesehen und
  danach korrigiert (heller Feldstreifen schräg statt parallel zur Straße, Feldweg West breiter und als
  Weg statt Rain, Hoffläche bis an das Gebäude, dunkler Fleck in der hellen Fläche West ergänzt).
  Ungefähre Zeit: 75 Minuten.
- Werkzeuge von landseg: nur `pruefen` und `dateien.schreibe_labels`; `eingriff` und `kante` nicht
  (Fassung A erlaubt freies Vorgehen, die Kanten kommen aus den Bildschwellen).

## Kategorien und warum

Eigene Liste in fünf Gruppen (`kategorien-teil.json`): 1 Verkehrsfläche (1.1 Straße, 1.2 Feld-,
Hof- oder Grasweg), 2 Siedlung und Hof (2.1 Gebäude, 2.2 Hof- und Lagerfläche), 3 Offenland
(3.1 Feldparzelle mit 3.1.1 dunkel, 3.1.2 mittelgrau, 3.1.3 hell; 3.2 Brache, Ödland oder Hutweide),
4 Gehölz und Kleinstrukturen (4.1 Einzelgehölz oder dunkler Fleck, 4.2 Rain, Graben oder Hecke),
5 Unklar (5.1 sehr dunkle Fläche, 5.2 kleines Objekt). Ebene 1: 5, Ebene 2: 10, Ebene 3: 3 Klassen.

- Auf dem Schwarz-Weiß-Scan ist die Nutzung der Felder (Acker, Grünland, Kultur) nicht ablesbar.
  Darum trennt die dritte Ebene unter 3.1 nur nach Grauton; das hält die Streifen der Flur
  auseinander, ohne eine Nutzung zu behaupten.
- Wege und Linien: Was eine helle Mitte zeigt, ist 1.2 (Weg); reine dunkle Linien sind 4.2.
  Ob ein schmaler Weg Grasweg oder Rain ist, bleibt offen.
- „Unklar“ ist eine eigene Gruppe, damit Schatten und kleine Objekte nicht falsch als Gebäude
  oder Gehölz in die Trainingsdaten gehen.

## Ergebnis

49 Segmente, davon 44 im Kern. Sicher (`sicher: true`) sind nur Straße, Seitenweg und
Hofzufahrt; die übrigen 46 (41 im Kern) sind `sicher: false` mit Grund im Eintrag.

## Was unsicher blieb (auch in `segmente.json` unter „offen“)

- Acker gegen Grünland bei allen Feldparzellen; im Farbbild entscheidbar.
- Helle fleckige Fläche West mit dunklen Flecken: Brache, Hutweide oder alte Gruben; die dunklen
  Flecken können Sträucher oder Gruben mit Schatten sein.
- Heller breiter Streifen Ost (~12 m): Stoppel- oder Brachstreifen oder breiter Erdweg.
- Hof: dunkles Rechteck als Gebäude angenommen, die schwarze Fläche daneben als Schatten oder
  Baumkrone; die helle Fläche als Lager-/Schuttplatz oder offener Boden.
- Weiche Grenzen ohne Bildkante (geschätzt): Feld Nord gegen Feld zwischen Feldweg und Hofweg,
  Grenzen der Streifen im Feld zwischen den Rainwegen, dunkler Feldteil West am Seitenweg, dunkles
  Feld zwischen Seitenweg und Straße (Westrand).

## Auf Schwarz-Weiß nicht zu trennen

Acker gegen Grünland (alle 3.1.x); Grasweg gegen Rain gegen Graben gegen Hecke bei schmalen Linien
(1.2/4.2); Gebäudedach gegen Baumkrone gegen Schlagschatten (2.1/5.1); Belag der Straße (Schotter
oder Asphalt); offener Boden gegen Stoppel gegen lückigen Bestand bei hellen Feldflecken (3.1.3).

## Nicht geprüft

- Kontextrand nur grob; der Ortsrand Nordost ist dort ein einziges Segment (im Kern nur 143 Bildpunkte).
- Die schmalen Streifen der schrägen Streifenflur im Feld West (5–15 Bildpunkte breit) sind nicht
  einzeln getrennt, ebenso ein schwacher dunkler Streifen im Feld zwischen den Rainwegen.
- Straßenbankette und schmale Straßengräben unter 3 Bildpunkte gehören zur Straße bzw. zum Feld.
