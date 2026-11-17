# Arbeitsweise Teilkachel r1c0, Fassung A (alles frei)

## Angesehene Bilder (Vorgabe, in dieser Reihenfolge)

1. Ganzer Ausschnitt T0: `T0.png`
2. Ganze Teilkachel r1c0: `ganz/r1c0/ganz_nummern.jpg`
   und `ganz/r1c0/ganz_roh.jpg`, Lage der Viertel aus `ganz.json`
3. Danach: Teilkachelbild `teilkacheln/r1c0.png`, Gitterbild und Vorschlag der Vorstufe (nur als Hinweis), eigene
   Zoom-Bilder (Faktor 3 bis 8, Gitter 25 px, teils kontrastgestreckt) aller vier Viertel, des Pfads, des
   Ackerrands, der Gärten und zweier auffälliger Kronen.

Einordnung aus T0: r1c0 ist das linke untere Viertel. Oben links eine Wiese mit hellen Tritt-/Fahrspuren und
beigen Trockenflecken, nach Süden ein verbuschender Saum, darunter geschlossener Laubwald. Nördlich-mittig ein
lockerer Gehölzstreifen mit zwei Lichtungen und einem Trampelpfad. Im Kontextrand oben rechts der Stoppelacker
(aus r0c1), rechts unten die Kleingartenanlage.

## Schritte und Werkzeuge

Eigene Skripte in diesem Ordner, Python der Stitcher-venv, keine Werkzeuge von landseg außer `pruefen` und
`dateien.schreibe_labels`/`schreibe_json`:

1. `schritt1_pixel.py`: Pixel-Klassifikation mit Random Forest (scikit-learn) auf Lab-Farbe, Grünindex und
   lokaler Helligkeitsstreuung in drei Maßstäben. Trainingsrechtecke von Hand aus den Zoom-Bildern für vier
   Grobklassen (Gras, beige/trocken, Gehölz, Bau). 2 Läufe: der erste war mit großen Glättungen zu grob, der
   zweite mit feineren Merkmalen und mehr Trainingsflächen (helle Kronen, Lichtungen).
2. `schritt2_segmente.py`: Modusfilter, Zonen von Hand (Kleingärten, Ackerrand), Schattenzonen im Wald über
   geglättete Helligkeit (Schwelle 16,5 L*, mindestens 1500 px), Gehölzflecken nach Größe und Kompaktheit zu
   Gebüsch, Einzelbaum oder Baumgruppe, Grasflächen nach Größe zu Wiese oder Lichtung, drei Pfade als
   handgezeichnete Linien (3 px). 5 Läufe. Ein erster Versuch mit einer Zone „lockeres Gehölzmosaik“ im Norden
   wurde verworfen: Die Grenze zum Wald wäre eine willkürliche Gerade durch geschlossene Kronen gewesen.
3. `schritt3_karte.py` mit `korrektur.json`: Korrekturen nach Sichtprüfung (Saatpunkte und Polygone, jede mit
   Begründung), kleine von Gehölz umschlossene „Lichtungen“ unter 1500 px werden zu Kronendach (es waren
   besonnte Kronen), Kleinstücke unter 30 px gehen an den Nachbarn mit der längsten Grenze. 8 Läufe, nach jedem
   Lauf ein Kontrollbild mit Nummern und Codes (`ansehen.py`) angesehen.
4. `schritt4_ausgabe.py`: `labels.tif`, `segmente.json` (mit `sicher` und `offen` je Segment), `kategorien-teil.json`,
   `ergebnis.jpg`. 2 Läufe.
5. Kontrolle mit `python -m landseg pruefen`: ok.

Ungefähre Zeit: etwa 60 Minuten. Zwischenbilder liegen in `arbeit/`.

## Ergebnis

64 Segmente, davon 35 mit Bildpunkten im Kern; 54 als `sicher: false` markiert.
Klassen: 5 auf Ebene 1, 12 auf Ebene 2, 3 auf Ebene 3; alle verwendet.

## Warum diese Kategorien

- Ebene 1 trennt, was im Bild am sichersten unterscheidbar ist: Gehölz, krautige Vegetation, vegetationsarme
  Flächen, Wege, Siedlung/Gärten.
- Beim Gehölz zählt die Struktur, nicht die Baumart: geschlossener Wald gegen freistehenden Einzelbaum,
  Baumgruppe und Gebüsch. Baumarten sind auf diesem Bild nicht sicher bestimmbar, deshalb gibt es keine
  Laub/Nadel-Klasse. Im Wald unterscheide ich nur besonntes Kronendach, großflächig dunkle Stellen (Schatten oder
  dunkler Bestand) und eine auffällig braun gefärbte Einzelkrone.
- Beim Offenland unterscheide ich gleichmäßige Wiese, Lichtungen/Krautflur im Gehölz und den rauen, verbuschenden
  Saum zwischen Wiese und Wald. Das sind drei Nutzungs- bzw. Sukzessionszustände, die im Bild verschieden aussehen.
- Boden und Trockengras habe ich bewusst in einer Klasse (3.1) gelassen: Die beigen Flecken sind auf dem Bild
  nicht sicher als offener Boden, Mähgut, Trockengras oder Trittstelle zu trennen.

## Was unsicher blieb (Segmente mit `sicher: false`, Grund steht je Segment unter `offen`)

- 1.1.2 (Segmente 42, 54): dunkle Flächen im Wald, Schlagschatten oder dunkle Baumart nicht unterscheidbar.
- 1.1.3 (58): braune Krone, Ursache offen; liegt fast ganz im Kontextrand unten.
- 1.2, 1.3, 1.4 in Saum und Wiese: Baum, hoher Strauch, Jungwuchs oder dichter Krautbult nicht sicher getrennt.
  Sicher nur der große Einzelbaum 17 und die Baumgruppe 1 am oberen Rand.
- 2.2 (13, 34, 52, 63): helle Flächen im Gehölz; ob Krautflur oder sehr helle, niedrige Kronen, ist offen.
  Sicher nur die große Lichtung 21 mit dem Pfad.
- 2.3 (37, 45): die Grenze Wiese/Saum ist von Hand als Polygon gezogen; der Übergang ist fließend.
- 3.1: Art der vegetationsarmen Stelle offen (siehe oben).
- 4.1 (8, 22): zwei Nebenpfade nur stellenweise sichtbar; der Hauptpfad 20 ist sicher, seine Breite (3 px) gesetzt.
- 5.1/5.2: nur Kontextrand, grob.

## nicht_geprueft

- Einzelkronen im geschlossenen Wald wurden bewusst nicht getrennt (Segment 51, 1.1.1, ca. 224 000 px): Die
  Kronengrenzen sind auf diesem Bild nicht sicher erkennbar, eine Aufteilung wäre geraten.
- Die hellen Tritt- und Fahrspuren in der Wiese (Segment 16) sind 1 bis 3 px breit und unterbrochen; sie sind
  nicht als eigene Segmente erfasst, nur die flächigen beigen Stellen.
- Eine mögliche weitere Pfadspur in der oberen rechten Wiese (um x 590 bis 605, y 115 bis 140) und weitere graue
  bis rötliche Kronen im Gehölzstreifen (um x 325 bis 425, y 190 bis 275) habe ich gesehen, aber nicht
  segmentiert, weil sie nicht eindeutig waren.
- Die Kleingärten im Kontextrand sind nicht Haus für Haus geprüft.
