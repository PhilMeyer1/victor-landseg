# Arbeitsweise Fassung A, Teilkachel r1c1

## Angesehene Bilder (in dieser Reihenfolge)

1. Ganzer Ausschnitt T0: `T0.png`
   (1000 × 1000; oben Siedlung und Stoppelfeld, links Wald, unten rechts die Kleingartenanlage).
2. Ganze Teilkachel r1c1: `ganz/r1c1/ganz_nummern.jpg`
   (Grenzen und Nummern der Vorstufe, Viertel v1–v4) und `.../ganz/r1c1/ganz_roh.jpg` (unverändert),
   Lage der Viertel aus `ganz.json` (Kern im Bild 64–564).
3. Bild der Teilkachel, an dem gearbeitet wurde: `teilkacheln/r1c1.png` (628 × 628),
   dazu `ansicht/r1c1/teilkachel/vorschlag.png` der Vorstufe.

## Vorgehen

1. Überblick: T0, dann die ganze Teilkachel, dann der Vorschlag der Vorstufe.
2. Eigene Ansichten (Skripte `zoom.py`, `zoom_nr.py`, `maske.py` in diesem Ordner): 9 Ausschnitte
   210 × 210 in 4-facher Vergrößerung mit Gitter (roh und mit Grenzen, Nummern, Vorstufen-Klasse), dazu 9
   Ausschnitte 140 × 130 in 6-facher Vergrößerung über der Gartenanlage und eine Nahansicht des
   Terrassengartens mit Becken links unten; Masken einzelner großer Segmente (67, 232, 177, 58).
3. Entscheidung: Die Umrisse der Vorstufe (SAM-3-Funde und Superpixel) sind an Gebäuden und Kronen
   brauchbar, die Klassen oft nicht (Schatten als „Wolke/Schatten“, Kronen im Garten als „Wald“,
   Rasenband als „Straße“). Ich habe daher die Geometrie als Ausgang genommen und **jedes Segment im Kern
   einzeln** mit meiner eigenen Liste neu klassifiziert (`entscheidungen.py`, rund 300 Einträge, jeder mit
   `sicher` und bei Zweifel einer Notiz).
4. Geometrische Eingriffe (alle in `bauen.py`, im `verlauf` von `segmente.json`):
   - 194 in 174 verschmolzen (beides dieselbe dunkle Dachfläche).
   - Rasen 67 zog sich als ein Segment durch viele Parzellen: an Engstellen unter ca. 2 m getrennt
     (Erosion um 5 Bildpunkte, Teile ab 150 Bildpunkten, Rückverteilung nach Abstand) → 6 Rasenteile.
   - 177 entlang y ≈ 430 geschnitten: oben die Terrassenbeete (5.1), unten der Hof um das Becken (2.1.3).
   - Neue Flächen: Schwimmbecken (Kreis um 135/463), zwei weiße Schirme/Pavillons, ein heller Kleinbau am Hof.
   - Aus dem Dach 93 die helle L-förmige Terrasse abgetrennt (Bildpunkte mit RGB-Mittel über 170).
   - Danach Zusammenhang erzwungen (4er-Nachbarschaft), Reste unter 12 bzw. Segmente unter 6 Bildpunkten an
     den Nachbarn mit der längsten Grenze (zwei Fälle: 156 an 139, 390 an 381).
5. Kontrolle mit `landseg pruefen` (endet mit `ok`), Ergebnisbild `ergebnis.jpg` (`bild.py`) und zwei
   vergrößerte Ergebnisansichten mit Nummern zur Sichtkontrolle.

Werkzeuge: eigene Python-Skripte (numpy, scipy, PIL, tifffile) mit dem Python des Stitcher-venv,
`landseg pruefen`. Läufe: `bauen.py` 3-mal, `pruefen` 1-mal. Zeit ungefähr 60 Minuten.

## Warum diese Kategorien

Die Teilkachel ist zu drei Vierteln eine Kleingartenanlage, dazu Hangwiese mit Baumgruppen, ein
Stoppelfeld oben rechts und Wald links. Die Liste (7 grobe Klassen, 17 auf Ebene 2, 11 auf Ebene 3) ist
danach geschnitten:

- **1 Gebäude und bauliche Anlagen**: Gartenhäuser von Schuppen/Anbauten getrennt (Grenze ca. 10 m²,
  250 Bildpunkte bei 0,2 m), Gewächshäuser eigens, weil sie hell und anders aussehen; Becken, Terrassierung
  und Kleinobjekte (Schirme, Planen) als „gebaut, aber kein Dach“.
- **2 Wege und befestigte Flächen**: befestigt (Gartenweg, Terrasse/Hof) und unbefestigt (begrünter
  Hauptweg, Trampelpfad). Der lange schräge Hauptweg durch die Anlage ist grün, aber klar ein Weg.
- **3 Acker** nur mit dem Stoppelfeld.
- **4 Grünland und Rasen**: Hangwiese, Gartenrasen und Saum getrennt, weil sie verschieden genutzt werden
  und im Bild verschieden glatt sind.
- **5 Gartenbeete**: Nutzbeete (Reihen) und „gemischte Gartenfläche“ für Mosaike, die bei dieser
  Auflösung nicht sicher weiter zu trennen sind.
- **6 Gehölze**: Wald, Baumgruppe, Einzelbaum (ab ca. 12 m² Krone), Hecke, Strauch, Schnittgut/Totholz.
- **7 Schatten**: Schlagschatten der Gartenhäuser liegen fast alle nordwestlich der Dächer; wo der Grund
  darunter nicht erkennbar ist, eigene Klasse statt Raten.

## Ergebnis

417 Segmente, davon 311 im Kern; 112 Segmente im Kern `sicher: false` (Liste unter `offen` in
`segmente.json`, je mit Notiz). `pruefen`: `ok`.

## Unsicher geblieben

- Kronen am Hang (11, 18, 19, 21, 31, 33, 38): Krone und Schlagschatten sind nicht trennbar; als
  Baumgruppe bzw. Einzelbaum mit Schatten eingetragen.
- 17: nur eine schwache helle Spur in der Hangwiese; das Segment ist breiter als ein Pfad.
- Viele kleine helle Flächen an den Gartenhäusern: Terrasse, Flachdach-Anbau oder Gegenstand?
  (u. a. 94, 96, 103, 124, 209, 243, 253, 256, 258, 319, 339).
- Helle lange Dächer 71, 82, 343: Gewächshaus oder heller Schuppen.
- Dunkle Streifen an Dächern (z. B. 81, 88, 136, 150, 164, 171, 303): Schatten oder dunkle Vegetation.
- Terrassengarten links (46, 44, neues Segment oben in 177): Beete oder nur Mauern und Stufen.
- Grenzen der Rasenteile aus 67 liegen an Engstellen, nicht an sichtbaren Parzellengrenzen.

## Nicht geprüft

- Die Umrisse der Vorstufe sind außer an den genannten Stellen nicht Segment für Segment auf die
  Bildkante geprüft (kein `kante`-Lauf); kleine Dächer sind teils etwas zu groß oder zu klein umrissen.
- Segmente nur im Kontextrand (außerhalb des Kerns) haben ihre Klasse nach einer Regel aus der
  Vorstufen-Klasse bekommen und sind `sicher: false`, nicht einzeln angesehen.
