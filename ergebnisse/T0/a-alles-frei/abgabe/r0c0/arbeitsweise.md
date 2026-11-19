# Arbeitsweise Fassung A, Teilkachel r0c0

## Angesehene Bilder (in dieser Reihenfolge)

1. Ganzer Ausschnitt T0: `T0.png` (1000 × 1000, r0c0 oben links)
2. Ganze Teilkachel r0c0: `ganz/r0c0/ganz_nummern.jpg`
   und `ganz_roh.jpg`, Lage der Viertel aus `ganz.json` (Kern 64..564, Faktor 2)
3. Arbeitsbild: `teilkacheln/r0c0.png` (628 × 628),
   dazu `ansicht/r0c0/teilkachel/kontrast.png`

## Schritte

1. Überblick über T0 und die Teilkachel: Straße mit Einmündung oben, drei Wohnhäuser mit Gärten (eines mit
   Flachdach, Terrasse und abgedecktem Becken), hohe Hecke an der Grundgrenze, große Wiese mit Holzhaufen,
   nach Süden eine verbuschte Wiese mit vielen dunklen Kronen, unten rechts gemähte Fläche mit Schwaden und
   ein Gehölzbestand.
2. Vorstufe (206 Segmente) mit eigenem Skript ausgewertet (Fläche, Lage, Mittelfarbe, Vorschlag) und in vier
   Vierteln dreifach vergrößert mit Nummern angesehen, dazu fünf bis sieben-fach vergrößerte Ausschnitte mit
   Koordinatengitter (Einmündung, Hecke, Garten, Flachdachhaus, Gehölzrand, Feldrand).
3. Jedes Vorstufen-Segment einer eigenen Gruppe zugeordnet (Tabelle `ZUORD` in `bauen.py`): Verschmelzen
   zusammengehöriger Stücke (z. B. dunkler und heller Teil einer Baumgruppe, Dachteile, Randstreifen), 14
   Kleinststücke ohne eigene Bedeutung an den Nachbarn mit der längsten gemeinsamen Grenze.
4. Neu gezeichnet:
   - die Riesenwiese der Vorstufe (56 und 166) per Linienzug geteilt in offene Wiese, verbuschte Wiese,
     glatte Wiese im Südwesten und Kronenbereich des Gehölzbestands;
   - die hohe Hecke West und ihr Schlagschatten zeilenweise nach Helligkeit getrennt (Schatten = dunkler
     Lauf, Hecke = 8 bis 11 Bildpunkte rechts daneben);
   - Terrasse mit Rundelement aus dem Flachdachhaus, Gartenhaus, Mauer an der südlichen Gartengrenze und
     ein rundes helles Objekt im Rasen per Polygon bzw. Kreis.
5. Je Gruppe zusammenhängende Teile als Segmente, Splitter unter 75 Bildpunkten an den Nachbarn, IDs neu von
   oben links nach unten rechts. `abschluss.py` schreibt `segmente.json`, `kategorien-teil.json`, `ergebnis.jpg`.
6. Kontrolle mit `landseg pruefen` (mit eigener Kategorienliste): `ok`.

Werkzeuge: eigene Skripte `analyse.py`, `zoom.py`, `gitterzoom.py`, `textur.py`, `bauen.py`, `abschluss.py`
(Python mit numpy, scipy, OpenCV, Pillow, `landseg.dateien`), `landseg pruefen`. Läufe: `bauen.py` 5-mal
(einmal Abbruch wegen fehlender Zuordnung, dann Nachbesserung Südwestgrenze, Hecke, Splittergrenze), `abschluss.py` 1-mal, `pruefen` 1-mal. Zeit etwa 50
Minuten. Kein SAM-Lauf, keine Änderung an der Vorstufe.

## Ergebnis

128 Segmente, davon 85 im Kern; 89 mit `sicher: false` (51 davon im Kern). Liste mit 33 Klassen in drei
Ebenen (5 / 16 / 12).

## Warum diese Kategorien

- Die Teilkachel ist halb Siedlung, halb Hangwiese. Deshalb eine eigene Oberklasse **Garten / Siedlungsgrün**
  (2): Rasen, Hecke und Gehölz innerhalb eingefriedeter Grundstücke sehen anders aus und bedeuten anderes als
  Wiese und Gehölz der freien Landschaft (3, 4).
- **Offenland** trennt nach dem, was im Bild sichtbar ist: ungemähte Wiese (raue Textur), glatte niedrige
  Wiese, Böschung/Straßengrün (linear), gemähte Fläche mit Schwaden und verbuschte Wiese als Mosaik, weil die
  vielen Kleinsträucher darin nicht einzeln sicher abgrenzbar sind.
- **Gehölz**: Einzelkrone, Bestand, Gebüsch. Laub/Nadel nur dort (Ebene 3), wo es eindeutig ist (Blutbuche,
  heller Laubholz-Bestand); die vielen dunklen Kronen bleiben bewusst auf Ebene 2.
- **Schlagschatten** (5.2) als eigene Klasse nur für Schatten von Hecke und Haus, deren Untergrund kaum
  erkennbar ist; dunkle Kronen sind nicht als Schatten geführt.
- Bebaut nach Gebäude / Verkehr / kleine Anlagen, mit Terrasse und Mauer als eigene feine Klassen, weil sie
  für Versiegelung zählen und gut erkennbar sind.

## Was unsicher blieb

- Dunkle Kronen (Bäume in der verbuschten Wiese, Gehölzrand südlich): Nadel- oder Laubbaum offen; bei den zwei
  großen dunklen Flächen am Gehölzrand ist auch Schlagschatten des Bestands möglich. Baum gegen Strauch bei
  Kronen zwischen etwa 20 und 40 m² nicht sicher.
- Grenze offene / verbuschte Wiese ohne scharfe Bildkante, von Hand gezogen; schmaler Trampelpfad in der
  verbuschten Wiese nicht ausgeschieden.
- Schwaden-Fläche: Stroh auf Stoppelacker oder Heu auf Wiese nicht entscheidbar (Klasse daher nach Aussehen).
- Glatte Wiese im Südwesten: gemäht oder nur niedrig, offen.
- Kleinteile im Garten (Gartenhaus, Anbau/Pergola, abgedecktes Becken, Gegenstände) nach Form und Farbe gedeutet.
- Kontextrand nur grob klassifiziert (zählt nicht).

Alle Segmente sind einzeln zugeordnet; nichts ist ungeprüft geblieben (`nicht_geprueft` leer).
