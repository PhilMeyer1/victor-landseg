# Arbeitsweise – H0, Teilkachel r0c0, Fassung A „Alles frei“

## Angesehen

1. Zuerst der ganze Ausschnitt: `C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png` und das Gitter
   `C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/H0_raster.jpg` (Ortsrand mit Streckhöfen, Straßen,
   Anger, Streifenflur; r0c0 ist oben links).
2. Dann die ganze Teilkachel: `C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r0c0/ganz_nummern.jpg`
   (Grenzen und Nummern der Vorstufe, Viertel) und `C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r0c0/ganz_roh.jpg`.
3. Gearbeitet auf `C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r0c0.png` (628 × 628, Kern x/y 64–564).

## Vorgehen (eigenes, ohne die Skill-Regeln)

- Die Vorstufe habe ich nur angesehen, nicht als Ausgang genommen: ihre Grenzen zerschneiden auf dem Scan
  Dächer und Höfe wellig. Ich habe die Karte selbst gezeichnet.
- **Gedrehte Rahmen statt Freihand:** Die Bauten liegen in wenigen Richtungen. Für jede Gruppe habe ich das Bild
  entlang ihrer Richtung „geradegezogen“ (Häuserzeile an Straße A, Block an Straße D, Block rechts der Gasse F,
  Häuserblock an Straße C, Feldstreifen) und darin Parzellen, Dachhänge und Streifengrenzen als Rechtecke
  abgelesen; Mittelwert-Profile quer zu den Zeilen gaben die Parzellengrenzen (Abstand rund 34 Bildpunkte ≈ 15 m).
  Straßenkanten habe ich aus Zeilenprofilen (Helligkeitssprung) bestimmt, Feldgrenzen aus einem kontrastverstärkten,
  längs der Streifen gemittelten Bild.
- **Ebenen:** Grundflächen (Acker, Anger, Brache, Gärten, Hofstellen je Parzelle), dann Felder als Streifen innerhalb
  der Feldgrenze, dann Straßen, Ränder, Hecken, dann Häuser, Schatten, Bäume und Kleinteile.
- **Einrasten:** Danach habe ich die Grenzen der flächigen Teile (Häuser, Höfe, Schatten, Bäume, Anger) auf die
  Bildkanten gezogen: Superpixel (SLIC, ≈ 18 Bildpunkte je Superpixel) übernehmen die Mehrheit der gezeichneten
  Fläche. Straßen, Wege, Ränder, Mauerlinien, Hecken und Feldstreifen blieben dabei geschützt (sonst Treppenstufen
  im gleichförmigen Acker).
- **Lückenlos und zusammenhängend:** Restpunkte gehen an das nächste Element; je Element zerfallene Teile werden
  eigene Segmente („Teil n“), Splitter unter 25 (Teilstücke unter 80) Bildpunkten an den Nachbarn mit der
  längsten gemeinsamen Grenze.
- Werkzeuge: eigene Skripte im Unterordner `arbeit/` (`zoom2.py`, `rect.py`, `rect2.py`, `prof.py` zum Ansehen und
  Messen; `spec.py`/`spec2.py` = die Zeichnung; `bau.py` = Karte; `abgabe.py` = Dateien), Python des Auftrags,
  numpy/OpenCV/scikit-image; Kontrolle mit `python -m landseg pruefen`.
- Läufe: rund 8 Bau-Läufe mit Kontrollbildern (Übersicht, vier Quadranten, Zooms auf Block B2, B4 und die
  Häusergruppe auf dem Anger), dazwischen Korrekturen an Lage und Reihenfolge; ungefähr 2½ Stunden.

## Kategorien und warum

Eigene, dreistufige Liste (`kategorien-teil.json`, 24 Klassen: 6 auf Ebene 1, 16 auf Ebene 2, 2 auf Ebene 3),
zugeschnitten auf das, was ein Schwarz-Weiß-Scan von 1968 hergibt:

- **1 Siedlung**: 1.1 Gebäude (1.1.1 langes Haus eines Streckhofs, 1.1.2 Schuppen), 1.2 Hofraum,
  **1.3 Hofstelle ungetrennt** (ehrliche Sammelklasse, wo Dach und Hof nicht trennbar sind), 1.4 Garten/Grünfläche
  im Ort, 1.5 Mauer/Einfriedung (die durchgehende dunkle Linie hinter der Häuserzeile).
- **2 Verkehr**: 2.1 Straße, 2.2 Weg/Gasse, 2.3 Straßenrand (Bankett, Gehweg, Vorplatz) – der Rand ist als eigener
  heller/mittelgrauer Streifen gut sichtbar.
- **3 Landwirtschaft**: 3.1 Acker als Streifenparzelle (die Streifen sind die eigentliche Einheit der Streifenflur).
- **4 Gehölz**: 4.1 Einzelbaum/Busch, 4.2 Baumreihe/Hecke.
- **5 Offene Fläche**: 5.1 Anger/Freifläche, 5.2 Brache/Weide am Ortsrand.
- **9 Unklar**: 9.1 Schatten, 9.2 dunkle Fläche (Baumgruppe oder dunkles Dach), 9.3 helles Kleinobjekt – damit
  Schatten und Rätselflächen nicht als falsche Gebäude oder Bäume in die Trainingsdaten gehen.

Die Farben sind nur Darstellung (eine Farbfamilie je Ebene 1).

## Ergebnis

111 Segmente, davon 91 mit Anteil am Kern; 96 tragen `sicher: false` (Grund je Segment in `segmente.json`).
Sicher sind nur die Fahrbahnen der Straßen und Häuser mit klar begrenztem hellem Dachkörper.
`pruefen` endet mit `ok`. Bild: `ergebnis.jpg` (Kern türkis umrandet, Legende mit Zahl je Klasse).

## Was unsicher blieb

- Einzelne Dachhänge: Ein Satteldach erscheint als heller und dunkler Streifen; der dunkle Hang ist vom Schlagschatten
  auf dem Hof kaum zu trennen. Wo kein heller Dachkörper klar begrenzt war, steht die Parzelle als 1.3 oder der
  dunkle Teil als 9.1.
- Block B4 rechts der Straße C: lange Streifen quer zur Straße; ob jeder Streifen ein Haus ist oder Haus plus Hof,
  bleibt offen (Häuser dort `sicher: false` außer dem sehr hellen Dach B4 2).
- Häusergruppe auf dem Anger: dunkler Block (9.2) neben dem langen Haus kann dunkles Dach oder Baumgruppe sein.
- Grenzen der Feldstreifen 3/4/5 nur als schwache helle Raine sichtbar, teils geschätzt.
- Kontextrand nur grob.

## Auf Schwarz-Weiß nicht zu trennen

- Acker gegen Grünland/Wiese (alle 3.1 und die Gärten 1.4 deshalb `sicher: false`).
- Dach gegen Hof bei mittelgrauen Dächern (Klasse 1.3).
- Schatten gegen dunkles Dach gegen Baumkrone (9.1/9.2).
- Belag von Wegen, Rändern und Anger (Erde, Schotter, Gras, Pflaster).
- Schuppen gegen Haufen (Stroh, Mist) bei kleinen hellen Flecken (9.3).
