# Arbeitsweise Fassung C, Teilkachel r0c1

## Angesehene Bilder (in dieser Reihenfolge)

1. Ganzer Ausschnitt: `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/T0.png`
2. Ganze Teilkachel: `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/ganz/r0c1/ganz_nummern.jpg`
   und `.../ganz/r0c1/ganz_roh.jpg`, Lage der Viertel aus `ganz.json`
3. Danach eigene Zoom-Bilder (2- bis 4-fach, mit Gitter) im Unterordner `sicht/`

## Schritte

1. Überblick: Siedlungsrand mit Einfamilienhäusern und Gärten im Norden, ein gemähtes Feld mit
   Schwaden in der Mitte, Wiese und Gehölz im Süden. Die Schatten fallen nach Nordnordwest.
2. Übersicht über die 234 Segmente der Vorstufe (`uebersicht.py`: Fläche, Kernanteil, Lage, Farbe).
   Neun Zoom-Ausschnitte der Teilkachel (`zuschnitt.py`) und sechs Zoombilder der Problemzonen
   (`zoom.py`) habe ich angesehen.
3. Ausgangspunkt war die Label-Karte der Vorstufe. In `build.py` habe ich jedem Kernsegment eine
   Klasse aus meiner eigenen Liste gegeben, mit Name, `sicher` und einer Notiz unter `offen`.
4. Verschmelzen: 27 Splitter mit ihrem Nachbarn verbunden, etwa Dachkante mit Dach, Poolrand mit
   Pool, Kronenteile mit dem Baum, Feldstücke mit dem Feld.
5. Teilen: Fünf gemischte Großsegmente der Vorstufe (Nordgärten 43, Hanggarten 92, Garten Ost 103,
   Saum am Gartenende 171, Grünstreifen an der Straße 81) habe ich mit SLIC (mit Maske) in
   Stücke zerlegt. Die Stücke bekamen ihre Klasse über eine Farb- und Texturregel (Schatten, Belag,
   Sand, Rasen, Gehölz, gemischt). Benachbarte Stücke derselben Klasse habe ich wieder vereint.
6. Polygone von Hand für Dinge, die die Vorstufe nicht getrennt hatte: Gartenhaus mit Pflaster,
   Poolumfeld, weiße Box, weißes Auto, graugrünes Objekt, Liege, Frühbeet(?), Gartenschaukel(?),
   diagonaler Gartenweg, heller Fleck im Rasen.
7. Feldrain: Den hellen Saum am Südrand des Felds habe ich nach Farbton abgetrennt. Er ist weniger
   braun als das Feld (R−B < 29), Band bis 9 px an Wiese bzw. Baum.
8. Aufräumen: Nicht zusammenhängende Teile werden eigene Segmente. Stücke unter 30 px gehen an
   den Nachbarn mit der längsten Grenze, bevorzugt an einen derselben Klasse.
9. Fünf Kontrollrunden mit Bildern der Zwischenstände (`bild.py`, Zoom mit `ID:Klasse`, `?` =
   unsicher). Danach Korrekturen: Hecke statt Baumgruppe im Saum, helle Stücke am Pool zum
   Poolumfeld, Feldrain-Regel neu, Objektpolygon verkleinert.
10. `landseg pruefen` mit eigener Kategorienliste: ok.

Läufe von `build.py`: 4. Ungefähre Zeit: 60 Minuten. Werkzeuge: eigene Python-Skripte (numpy,
scikit-image SLIC, scipy), `landseg pruefen`. Andere landseg-Befehle habe ich nicht benutzt.

## Ergebnis

- 272 Segmente, 176 davon mit Anteil am Kern. 109 Kernsegmente stehen auf `sicher: false`.
- Klassen: 5 auf Ebene 1, 14 auf Ebene 2, 10 auf Ebene 3 (29 Codes).

## Warum diese Kategorien

- Der Ausschnitt ist Siedlungsrand. Für ein Trainingsziel zählt deshalb zuerst die Trennung
  bebaut/befestigt – Feld – Gras/Boden – Gehölz – Schatten (Ebene 1).
- Gebäude habe ich in Wohnhaus und Nebengebäude geteilt (die Dächer sind klar erkennbar).
  Befestigte Flächen sind Straße, Zufahrt und Terrasse/Weg. Pool und Kleinobjekte stehen getrennt,
  weil sie im Bild auffallen und sonst Rasen oder Belag verfälschen.
- Gehölz habe ich gestuft: Einzelbaum mit abgrenzbarer Krone (Laub, rotlaubig, Nadel), Baumgruppe,
  Strauch/Hecke und gemischte Gartenvegetation. Gartenmosaike lassen sich auf 20 cm nicht
  ehrlich in Beet, Staude und Strauch trennen.
- Schatten ist eine eigene Klasse (Gebäude- bzw. Gehölzschatten). Unter dichtem Schlagschatten ist
  der Untergrund nicht erkennbar, und eine geratene Rasen-Klasse würde die Trainingsdaten
  verfälschen.
- Feld und Feldrain stehen getrennt. Die hellen Streifen sind Schwaden auf einer gemähten bzw.
  abgeernteten Fläche. Ob es Heu oder Stroh ist, ist nicht erkennbar, deshalb steht beides in
  einer Klasse.

## Was unsicher blieb

- Teilstücke aus der SLIC-Teilung (Nordgärten, Hanggarten, Garten Ost, Saum, Grünstreifen): Ihre
  Grenzen und Klassen folgen einer Regel, nicht einer Kante. Alle stehen auf `sicher: false`. Am
  wackligsten sind die Grenze Rasen/Gartenvegetation im Garten Ost (großes Stück 4.4, rund 8800 px)
  und die Schattenstücke im Hanggarten.
- Poolumfeld im Norden: Holzdeck, Sand oder Pflaster ist nicht unterscheidbar (als 1.2.3, unsicher).
- Dunkle glatte Flächen (Vorstufe 142, 135, 106, 154): Schatten oder sehr dunkle Krone. 142 steht
  als 5.2 auf unsicher, weil der Schattenwerfer südsüdöstlich nicht klar zu sehen ist.
- Dunkle Gehölzfläche im Süden (Vorstufe 207): Die Vorstufe sagt Schatten, ich sehe Kronen (4.2,
  unsicher).
- Kleinobjekte (Auto, Box, Liege, Schaukel, Frühbeet, Kleinbauwerk 180): Die Art ist geraten, die
  Lage ist sicher.
- Konifere gelbgrün (Vorstufe 123) und bläulicher Baum (Vorstufe 132): Nadelbaum nur nach Form
  und Farbe vermutet.
- Große Kronen (Vorstufe 27, 45, 134): Es können zwei Bäume sein.
- Schmale Feldrain-Stücke am Nordrand des Felds: Ob sie Rain, Gras oder Gehölzsaum sind, ist auf
  2–4 px Breite nicht sicher.
- Kontextrand: Die Segmente dort habe ich grob nach der Vorstufe übertragen, alle mit
  `sicher: false`.

## nicht_geprueft

- Grenzen habe ich nicht mit `landseg kante` an Bildkanten eingerastet. Die Grenzen der Vorstufe
  und die SLIC-Grenzen sind übernommen.
- Die Segmente im Kontextrand habe ich nicht einzeln geprüft, nur pauschal über die Klasse der
  Vorstufe abgebildet.
