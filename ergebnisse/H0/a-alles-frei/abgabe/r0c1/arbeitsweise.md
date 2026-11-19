# Arbeitsweise r0c1 (H0, Fassung A „Alles frei“)

## Angesehen, in dieser Reihenfolge

1. Ganzer Ausschnitt H0: `C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png` und das Gitter
   `C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/H0_raster.jpg`. r0c1 ist der Ortskern oben rechts:
   Streckhöfe in Reihen, eine schräge Hauptstraße, zwei Straßen von Südwest nach Nordost, eine Kreuzung
   mit Verkehrsinsel und kleinem Anger am unteren Rand.
2. Ganze Teilkachel r0c1: `C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r0c1/ganz_nummern.jpg`
   (Grenzen und Nummern der Vorstufe, Viertel v1 bis v4) und
   `C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r0c1/ganz_roh.jpg`.
3. Danach das Teilkachelbild `teilkacheln/r0c1.png` selbst in eigenen Vergrößerungen (2-, 4-, 5- und
   6-fach mit Koordinatengitter, Skript `zoom.py`): jedes Viertel des Kerns roh, dazu Nahansichten der
   Kreuzung mit Insel und Anger, der Halle, der Hintausgasse, der dunklen Flächen und der Ecke unten links.

## Schritte (eigenes Verfahren, die Vorstufe nur als Hinweis)

Die Vorstufe habe ich nicht als Ausgang genommen: Sie fasst Häuserzeilen und Höfe zusammen. Stattdessen:

1. **Straßen** (`strassen.json`, `bauen.py`): je Straße eine von Hand gelegte Mittellinie mit Korridor;
   Straße ist, was im Korridor hell ist (Grauwert nach Glättung > 120), geschlossen, Löcher gefüllt,
   Fransen abgeschnitten. Die Kante kommt damit aus dem Bild, nicht aus dem Korridor.
2. **Rest der Fläche**: Wasserscheide auf dem Helligkeitsgradienten (geglättet, σ 1,5; Saatpunkte aus
   h-Minima), danach benachbarte Stücke mit ähnlichem Grauwert verschmolzen (Graph-Schnitt, Schwelle 20).
   Im Westblock (Dächer quer, schwacher Kontrast) feiner (h 2, Schwelle 9); das Gebiet ist aus groben
   Segmenten zusammengesetzt, damit keine gerade Kunstgrenze entsteht.
3. **Aufräumen**: jedes Stück einzeln zusammenhängend (4er-Nachbarschaft), Stücke unter 20 Bildpunkten
   an den passendsten Nachbarn (lange Grenze, ähnlicher Grauwert) — nichts weggelassen.
4. **Klassen nach Regeln** aus Grauwert, Länge/Breite und Fläche (Regeln in `bauen.py`, Funktion `regel`),
   dazu: helle Längsstreifen, die an eine Straße grenzen und parallel zu ihr liegen, sind Straßenrand
   (24 Fälle), nicht Dach — die Streckhöfe stehen quer zur Straße.
5. **Von Hand** (`korrekturen.json`): Hintausgasse als Polygon; dunkle Fläche am Blockkopf als Polygon;
   Straßenstücke derselben Straße verschmolzen (Hauptstraße mit Westast um die Insel, beide Bänder der
   unteren Straße, obere Straße über die dunklere Mitte); Halle, Querbau, Baum an der Kreuzung, Inselgrün,
   Objekt auf der Insel, Anger, Gartenland mit Reihen, Garten/Gehölz-Fläche, ein Hof.
6. `abgabe.py` schreibt `labels.tif`, `segmente.json`, `ergebnis.jpg`; danach `pruefen`.

Werkzeuge: eigene Skripte (`bauen.py`, `abgabe.py`, `zoom.py`, `overlay.py`, `wo.py`) mit numpy, scipy,
scikit-image; von landseg nur `pruefen`. Läufe: etwa 10 × `bauen.py`, 7 × `abgabe.py`, 2 × `pruefen`
(beide `ok`). Zeit: etwa 75 Minuten.

## Ergebnis

1363 Segmente in der ganzen Teilkachel, davon 872 mit Bildpunkten im Kern; 41 der Kern-Segmente sicher,
831 unsicher. Kern: 246 Hof/Freifläche, 239 Garten, 189 Gebäude (Ebene 2), 87 Schatten, 66 helle
Dachstreifen von Längsbauten, 26 Straßenstücke, 11 nicht bestimmbar, je eins Halle, Querbau, Gasse,
Gartenland mit Reihen, Garten/Gehölz, Baum, dazu Anger und Inselgrün.

## Warum diese Kategorien

Gestuft in drei Ebenen (17 Klassen: 3 / 8 / 6), so fein, wie ein Schwarz-Weiß-Bild mit 0,45 m es trägt:

- **1 Siedlung** — 1.1 Gebäude mit 1.1.1 Längsbau (heller Dachstreifen), 1.1.2 Querbau/Nebengebäude,
  1.1.3 Halle; 1.2 Verkehrsfläche mit 1.2.1 Straße und 1.2.2 Gasse; 1.3 Hof- oder Freifläche.
  Streckhöfe sind das prägende Muster; ihr Dach erkennt man an langen, hellen, parallelen Streifen.
- **2 Grün** — 2.1 Garten, 2.2 Gehölz mit 2.2.1 Baum, 2.3 Anger/Platzgrün, 2.4 Gartenland mit Reihen.
- **9 Nicht bestimmbar** — mit 9.1 Schatten. Eine eigene Schattenklasse, weil die fast schwarzen Streifen
  neben jedem Dach die Hälfte der Bebauung ausmachen und man auf dem Scan nicht sieht, ob dort die
  beschattete Dachhälfte oder Boden im Schlagschatten liegt.

## Was unsicher blieb

- **Gebäude gegen Schatten:** Ein Streckhof-Dach besteht aus hellem Streifen (besonnte Seite) und einem
  Teil des dunklen Nachbarstreifens. Den dunklen Streifen habe ich nicht zwischen Dach und Hof geteilt
  (keine Kante im Bild); er steht als 9.1. Ein ganzes Haus ist darum meist zwei Segmente.
- **Hof gegen Garten (1.3 gegen 2.1):** nur nach Helligkeit getrennt (mittelhell → Hof, dunkelgrau →
  Garten); auf Schwarz-Weiß nicht sicher. Alle diese Segmente sind `sicher: false`; das Farbbild entscheidet.
- **Mittelgraue oder dunkle Längsstreifen** als 1.1 (Elternklasse) und unsicher: Dachfläche oder Hofstreifen.
- **Gartenland mit Reihen** (rechts der Mitte, feine parallele Streifen, gezähnte Kante, kein Schatten):
  Beete oder Rebzeilen; ein großes dunkles Dach ist nicht ganz ausgeschlossen.
- **Ostrand der Hauptstraße** an der Kreuzung: Fahrbahnteil oder ein Längsbau mit Schatten daneben.
- **Hintausgasse:** Lage und Breite von Hand geschätzt.
- **Bäume:** Körnung taugt auf dem stark verrauschten Scan nicht als Merkmal (ich habe es geprüft: die
  Streuung trennt nur am Median); darum nur ein Baum von Hand (Kreuzung), sonst keine Baumklasse vergeben.
- **Straßenrand-Regel:** Ein heller Streifen längs der Straße kann auch eine traufseitige Hausfront sein.

## Auf Schwarz-Weiß nicht zu trennen

Hof gegen Garten gegen Rasen; Belag von Straße und Gasse (Asphalt, Pflaster, Schotter); beschattete
Dachhälfte gegen Schlagschatten auf dem Boden; dunkles Dach gegen dichten Garten (Flächen der Klasse 9);
Gebüsch gegen Baum; Wohnteil gegen Stall/Scheune innerhalb eines Längsbaus.

## Nicht geprüft

- Den Kontextrand (außerhalb des Kerns) habe ich mit demselben Verfahren mitsegmentiert, aber nicht von
  Hand nachgesehen.
- Die über 800 kleinen Hof-, Garten- und Gebäudestücke im Kern habe ich in Vergrößerung je Viertel
  angesehen, aber nicht jedes einzeln korrigiert: Ihre Klasse kommt aus den Regeln und ist als unsicher
  markiert.
- Nähte zu den Nachbarkacheln habe ich nicht abgeglichen (Fassung A verlangt das nicht).
