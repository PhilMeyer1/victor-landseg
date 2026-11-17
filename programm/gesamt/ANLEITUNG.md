# Anleitung: Segmentierung und Klassifizierung des Testfensters T0

Für Victor. Hier steht, wie der erste Test an einem Luftbild-Ausschnitt (T0) gerechnet wurde, was
in welcher Datei steht, was man den Zahlen glauben kann und wie man einen neuen Ausschnitt rechnet.
Wie das ganze Projekt aufgebaut ist und wo die Vorgeschichte steht, erklärt `README.md`.

Stand: 17.11.2026. Abgegeben ist der Zwischenstand nach dem Urteil der KI. Die Durchsicht der
festen Liste durch uns und die beiden letzten Schritte (Grenzen umsetzen, Messbericht) ruhen, siehe
„Was fehlt“.

## Kurz

- Ein Ausschnitt von 200 × 200 m wurde lückenlos in Flächen (Segmente) zerlegt, und jede Fläche
  bekam eine Klasse, in drei Fassungen:
  - **A „Alles frei“**: Die KI bestimmt Grenzen, Kategorien und Arbeitsweise selbst.
  - **B „Kategorien frei“**: Die KI benennt und stuft die Klassen selbst; Grenzen und Arbeitsweise wie C.
  - **C „Feste Kategorienliste“**: Klassen aus unserer festen, gestuften Liste (58 Klassen in drei
    Ebenen, geordnet nach Bedeckung).
- Ansehen: `ergebnisse/T0.html` doppelklicken (eine Datei, kein Server). Oben schaltet man A, B, C um.
- Bilder von ganz T0 je Fassung: `ergebnisse/gesamtbilder/`.

## Zuerst: einrichten und ausprobieren

1. Projekt holen und die Original-Luftbilder dazulegen: Sie kommen getrennt (zu groß für GitHub).
   Welche Dateien es sind und in welchen Ordner sie gehören, steht in `daten/luftbilder/README.md`.
   Prüfen, ob sie richtig liegen, im Projektordner:

   ```
   python -B programm/tools/gesamt_projekt.py pruefen --ziel . --luftbilder daten/luftbilder
   ```

   Erwartet: „Luftbilder: 8 von 8 passen“ und „Ergebnis: ok“ (Exit-Code 0). Fehlt ein Bild, nennt
   der Befehl es mit Namen. Ohne `--luftbilder` prüft er nur das Projekt selbst (Größen, Pfade im
   README) und meldet „Luftbilder nicht geprüft“.

2. Python einrichten (siehe „Umgebung“), dann im Ordner `programm/` die Tests:

   ```
   cd programm
   python -B -m unittest discover -s tests -t .
   ```

3. Eine Karte aus den Ergebnissen prüfen lassen (Fassung C, Teilkachel r0c0), weiter in `programm/`:

   ```
   python -B -m landseg pruefen --labels ../ergebnisse/c-feste-liste/r0c0/labels.tif --segmente ../ergebnisse/c-feste-liste/r0c0/segmente.json --kategorien ../ergebnisse/c-feste-liste/kategorien-c.json --bild ../ergebnisse/teilkacheln/r0c0.png
   ```

   Exit-Code 0 heißt: lückenlos, jedes Segment zusammenhängend, alle Klassen gültig.

4. T0 aus dem Original neu ausschneiden, weiter in `programm/` (Ergebnis in `arbeit/T0/` im
   Projektordner; `arbeit/` nimmt Git nicht auf):

   ```
   python -B -m landseg kacheln --bild ../daten/luftbilder/orthofoto-aktuell/0009626524_100_Orthophoto_aktuell_5236-56.tif --x 2000 --y 2400 --breite 1000 --hoehe 1000 --kern 500 --rand 64 --name T0 --ziel ../arbeit/T0
   ```

   Das ergibt denselben Ausschnitt `T0.png` und dieselben vier Teilkacheln wie in `ergebnisse/`.

## Projektaufbau

Alle Pfade gelten vom Projektordner aus.

| Pfad | Inhalt |
|---|---|
| `README.md` | Einstieg: Aufbau des ganzen Projekts, Lesereihenfolge, Benennung der Fassungen |
| `ANLEITUNG.md` | diese Anleitung |
| `programm/README.md` | Beschreibung der Werkzeuge (Befehle, Dateiformate) |
| `programm/landseg/`, `programm/tests/`, `programm/tools/`, `programm/einstellungen/`, `programm/vorlagen/`, `programm/.claude/skills/landseg-agent/` | Werkzeuge, Tests, Prüfskripte, Einstellungen, Auftragsvorlagen und Arbeitsregeln (L1–L12) für die KI-Agents |
| `programm/kategorien.json`, `programm/KATEGORIEN.md` | feste Kategorienliste (Fassung C) und ihre Erklärung |
| `programm/vorstufe.json` | Einstellungen der automatischen Vorstufe (SAM 3) |
| `ergebnisse/T0.png`, `ergebnisse/T0.pgw` | Luftbild-Ausschnitt T0 mit Weltdatei |
| `ergebnisse/manifest.json` | Lage von T0 und der Teilkacheln (Bildpunkte und Landeskoordinaten) |
| `ergebnisse/teilkacheln/` | die vier Teilkacheln als PNG mit Weltdatei |
| `ergebnisse/ganz/` | je Teilkachel die Übersichtsbilder, die jeder Agent zuerst gesehen hat (`ganz_roh.jpg`, mit Nummern `ganz_nummern.jpg`) |
| `ergebnisse/T0.html` | Prüfseite mit allen drei Fassungen |
| `ergebnisse/gesamtbilder/` | je Fassung ganz T0 in Klassenfarben (`…-klassen.png`) und über dem Luftbild mit weißen Grenzen (`…-ueber-luftbild.png`) |
| `ergebnisse/a-alles-frei/` | Fassung A: `<teilkachel>/labels.tif` und `segmente.json`, `kategorien-a.json`, `zusammen/` (Karte von ganz T0, `naht.json`), `abgabe/<teilkachel>/arbeitsweise.md` und `kategorien-teil.json` (eigene Liste je Agent), `zusammentragen.json` |
| `ergebnisse/b-kategorien-frei/` | Fassung B: `<teilkachel>/labels.tif` und `segmente.json`, `kategorien-b.json`, `urteil/<teilkachel>/urteil.json` |
| `ergebnisse/c-feste-liste/` | Fassung C: `<teilkachel>/labels.tif` und `segmente.json`, `kategorien-c.json` (Kopie von `kategorien.json`), `urteil/<teilkachel>/urteil.json` |
| `daten/landseg/T0/` | alle Arbeitsdaten des Tests mit den alten Ordnernamen (siehe „Benennung“): Viertelbilder, Nahansichten der Agents, Rohwerte der Vorstufe (`sam3_roh.npz`), Probeläufe, einzelne Viertel-Urteile |
| `daten/luftbilder/` | Platz für die Original-Luftbilder (kommen getrennt), Beschreibung in `daten/luftbilder/README.md` |

`ergebnisse/` ist die Auswahl, die zuerst übergeben wurde, mit neuer Benennung; `daten/landseg/T0/`
sind die vollen Arbeitsdaten mit alter Benennung. Pfade in `urteil.json` unter `bilder` und
`quelle` sind relativ zum Ordner der Fassung und nach neuer Benennung geschrieben; die Dateien
selbst liegen unter `daten/landseg/T0/` im Ordner mit altem Namen (etwa
`c-feste-liste/urteil/r0c0/v1/urteil.json` → `daten/landseg/T0/kern500/urteil/r0c0/v1/urteil.json`).

## Benennung (alt → neu)

Während des Tests hießen die Fassungen anders. In `ergebnisse/` und in dieser Anleitung gilt die
neue Benennung; in `daten/landseg/T0/` und in den älteren Berichten unter `wuensche/` steht die
alte:

| neu | Name | früher | früherer Ordner |
|---|---|---|---|
| A | Alles frei | Fassung C | `fassung-c` |
| B | Kategorien frei | Fassung B | `fassung-b` |
| C | Feste Kategorienliste | Fassung A | `kern500` (Karte `urteil-stand`) |

Beim Kopieren nach `ergebnisse/` wurden in den JSON- und Markdown-Dateien Fassungskennungen,
Ordnernamen und Bearbeiter umbenannt (`urt-a-…` → `urt-c-…`, `fassung-c-…` → `a-alles-frei-…`);
Inhalte und Zahlen sind unverändert.

## Ausgangsbild und Lage von T0

- Luftbild: Orthofoto „aktuell“, Blatt 5236-56 (Datei `0009626524_100_Orthophoto_aktuell_5236-56.tif`,
  6250 × 5000 Bildpunkte, RGB, 8 Bit), 0,2 m je Bildpunkt, Lagebezug MGI / Austria GK Central,
  EPSG:31255. Das Originalbild kommt getrennt (`daten/luftbilder/README.md`).
- T0: Ausschnitt ab Bildpunkt x 2000, y 2400, 1000 × 1000 Bildpunkte, also 200 × 200 m. Ecke oben
  links in Landeskoordinaten: X 69150,0 m, Y 353520,0 m (`ergebnisse/manifest.json`, `ausschnitt.transform`).
- Quelle und Rechte: Das Orthofoto kam mit einer Lieferung vom 17.11.2026 (Beispiel-Luftbilder zu
  Bericht 48 „Segmentierung von Luftbildern“). **Anbieter und Lizenz sind nicht dokumentiert**;
  auch Bericht 48 nennt für diese Datei keinen Anbieter. `T0.png` und die Teilkacheln sind daraus
  abgeleitete Ausschnitte. Vor einer Weitergabe außerhalb dieses privaten Projekts klären.

## Kacheln, Teilkacheln, Viertel

- `kacheln` schneidet T0 in 2 × 2 **Teilkacheln** (`r0c0` oben links, `r0c1` oben rechts, `r1c0`,
  `r1c1`). Jede hat einen **Kern** von 500 × 500 Bildpunkten und ringsum einen **Kontextrand** von
  64 Bildpunkten aus dem Originalbild, zusammen 628 × 628. Bearbeitet und bewertet wird der Kern;
  der Rand zeigt, was daneben liegt. Die vier Kerne ergeben zusammen genau T0.
- Für die Agents wurde jeder Kern in vier **Viertel** von 250 × 250 geteilt (v1 oben links, v2 oben
  rechts, v3 unten links, v4 unten rechts). Ein Segment gehört dem Viertel mit dem größten Anteil
  seiner Kernfläche. Die Viertel dienten als Nahansicht und Ablage, nicht als eigene Karte.

## Automatische Vorstufe (SAM 3)

Ausgang von B und C (und von drei der vier Agents in A) ist eine automatische, lückenlose
Vorbelegung je Teilkachel (`landseg vorstufe`, Einstellungen `programm/vorstufe.json`):

1. Superpixel (SLIC) zerlegen das Bild in kleine, gleichartige Stücke.
2. SAM 3 (Modell `facebook/sam3`) sucht mit einem kurzen Text je Kategorie der festen Liste nach
   Funden (Instanzen) und liefert dazu je Bildpunkt einen Wert je Kategorie.
3. Funde rasten auf die Superpixel ein (kleinste zuerst); übrige Superpixel bekommen die Kategorie
   mit dem höchsten Wert und verbinden sich mit gleichartigen Nachbarn.
4. `pruefen` sichert: jede Stelle gehört zu genau einem zusammenhängenden Segment, keine Lücke.

Je Segment stehen Klasse, Sicherheit (`sicher: ja | nein`) und eine Kandidatenliste für das
Urteil dabei. Laufzeit für T0: 2,3 min auf der GPU. Ergebnis: 206 / 234 / 86 / 408 Segmente je
Teilkachel, davon im Kern 141 / 147 / 52 / 301, zusammen **641 Segmente in T0**; `sicher: nein`
66 / 62 / 59 / 79 % je Teilkachel.

## Wie die KI geurteilt hat

- Je Fassung arbeiteten **vier Agents, einer je Teilkachel** (für B ein fünfter, der die freien
  Klassen zu einer Liste vereinheitlichte; dazu eine Gegenprobe auf r0c0, nicht in `ergebnisse/`).
  Insgesamt 15 Agents, 25 Minuten, rund **3,3 Mio. Tokens** (der Lauf der Urteile; vorbereitende
  und zusammenführende Schritte nicht mitgezählt).
- Jeder Agent sah **zuerst ganz T0** (`T0.png`), dann seine ganze Teilkachel (`ergebnisse/ganz/`),
  und arbeitete danach die vier Viertel seiner Teilkachel nacheinander ab, **Segment für Segment**,
  mit Übersichts- und Nahbildern mit Nummern. Die Arbeitsregeln stehen in
  `programm/.claude/skills/landseg-agent/SKILL.md`, die Auftragsvorlagen in `programm/vorlagen/`;
  die tatsächlichen Aufträge je Agent unter `wuensche/2026-11-17-landseg-test-t0-1/`.
- In B und C hat die KI nur geurteilt und nichts an der Karte geändert: **Die Grenzen sind die der
  Vorstufe.** Was die KI an Grenzen ändern würde (verschmelzen, teilen, Grenze verschieben, fehlende
  Fläche), steht je Segment in `urteil.json` unter `punkte` und auf der Prüfseite beim angeklickten
  Segment. Umgesetzt ist es noch nicht.

### Was jede Fassung freiließ

| | A Alles frei | B Kategorien frei | C Feste Kategorienliste |
|---|---|---|---|
| Grenzen | frei: eigene Karte je Agent | Vorstufe | Vorstufe |
| Kategorien | frei, je Agent eine eigene Liste, danach zu einer Liste zusammengelegt | frei benannt und gestuft (grob/mittel/fein), danach vereinheitlicht | feste Liste `kategorien-c.json` |
| Arbeitsweise | frei (eigene Skripte, eigene Verfahren) | Regeln L1–L12, Segment für Segment | Regeln L1–L12, Segment für Segment |
| Urteil je Segment (`urteil.json`) | nein; Arbeitsweise je Agent in `abgabe/<teilkachel>/arbeitsweise.md` | ja | ja |

**A Alles frei.** Die vier Agents gingen verschieden vor: r0c0 und r1c1 nahmen die Geometrie der
Vorstufe, ordneten jedes Stück neu ein, verschmolzen und teilten gezielt; r0c1 zerlegte gemischte
Großsegmente mit SLIC und ordnete per Farb- und Texturregel; r1c0 ließ die Vorstufe weg und
klassifizierte jeden Bildpunkt mit einem Random Forest (Lab-Farbe, Grünindex, Textur, eigene
Trainingsflächen). Die vier eigenen Listen (33, 29, 21 und 36 Codes) wurden danach nach Namen und
Merkmalen zu `kategorien-a.json` zusammengelegt (47 Klassen in sieben Gruppen); die Zuordnung je
Teilkachel steht dort unter `abbildung_teilkacheln`, der ursprüngliche Code je Segment unter
`klasse_teil`. Weil jeder Agent seine IDs bei 1 begann, haben r0c0, r0c1 und r1c0 einen Versatz von
100000, 200000 und 300000 bekommen; die alte ID steht unter `id_abgabe`. `zusammen/` ist die daraus
zusammengetragene Karte von ganz T0.

**B Kategorien frei.** Jeder Agent benannte die Klassen selbst (`klasse_frei` mit grob, mittel,
fein); ein weiterer Agent vereinheitlichte die 16 Viertel-Listen zu `kategorien-b.json`. Die Klasse
je Segment (`klasse`) ist der Code dieser Liste.

**C Feste Kategorienliste.** Je Segment `klasse_heute` (Vorstufe) und, wenn die KI widerspricht,
`klasse_vorschlag`. Regel: `klasse = klasse_vorschlag`, sonst `klasse_heute`.

Segmente aus dem Kontextrand haben kein eigenes Urteil: In der Karte je Teilkachel tragen sie die
Klasse aus dem Urteil der Nachbarkachel (Mehrheit der Bildpunkte), außerhalb von T0 die der
Vorstufe (C) bzw. „0 Nicht bestimmbar“ (B), immer mit `sicher: nein` und `urteil: kontextrand`.

## Kategorienlisten und Ebenen

Alle drei Listen haben dasselbe Format (`kategorien*.json`, Schlüssel `classes`): je Klasse `code`,
`name`, `parent`, `level` (1 grob, 2 mittel, 3 fein), `color`, dazu Regeln und Zählung. Ein Code
zeigt die Ebene: `4` grob, `4.2` mittel, `4.2.1` fein. Eine Klasse ohne Unterklassen gilt auf allen
feineren Ebenen weiter.

| Liste | Klassen | grob / mittel / fein | feinste Klassen (Blätter) | im Kern benutzt |
|---|---:|---|---:|---:|
| A `kategorien-a.json` | 47 | 7 / 18 / 22 | 32 | 36 |
| B `kategorien-b.json` | 49 | 7 / 21 / 21 | 31 | 35 |
| C `kategorien-c.json` | 58 | 7 / 25 / 26 | 43 | 27 |

Die feste Liste C ist nach **Bedeckung** geordnet (was man sieht, nicht wie es genutzt wird) und in
`programm/KATEGORIEN.md` erklärt, mit Regeln G1–G5, U1–U5 und den Abweichungen von Bericht 48. Die
SW-Spalte (`bw`) und die Abbildungen auf andere Klassifikationen (`mappings`) sind ungeprüft. Die
freien Listen A und B mussten für das Prüfskript `programm/tools/pruefe_kategorien.py` Platzhalter
bekommen (`bw` = „eing.“, leere `mappings`, eine angenäherte Regel zu Bericht 48) und sieben grobe
Gruppen mit den Codes 0–6.

## Dateiformate

- **Label-Karte** `labels.tif`: einkanaliges TIFF (zlib), uint32, je Bildpunkt die ID seines
  Segments; 0 = kein Segment, darf nicht vorkommen. Je Teilkachel 628 × 628 (Kern plus Rand), in
  `ergebnisse/a-alles-frei/zusammen/` 1000 × 1000 (ganz T0). Lesen: `tifffile.imread("labels.tif")`.
- **IDs**: eindeutig im ganzen Ausschnitt, Teilkachel-Nummer × 100000 + laufende Nummer
  (r0c0 ab 100001, r0c1 ab 200001, r1c0 ab 300001, r1c1 ab 400001).
- **`segmente.json`** (Schema `landseg-segmente/1`): unter `segmente` je Segment `id`, `klasse`
  (feinster Code), `grob`, `sicher`, `im_kern`, `flaeche`; in B und C dazu `klasse_vorstufe`,
  `sicher_vorstufe`, `urteil`, `herkunft`, `im_siedlung`; in A `name`, `klasse_teil`, `id_abgabe`.
  Unter `verlauf` jeder Eingriff mit Zeit und Bearbeiter.
- **`urteil.json`** (Schema `landseg-urteil-teilkachel/1`, B und C, je Teilkachel): Kopf mit
  `fassung`, `teilkachel`, `kategorien`, `klasse_regel`, `zahlen` (`nicht_sauber`, `sicher_nein`,
  `klassenwechsel`), `naht` (Hinweise an die Nachbarkachel), `unsicher`, `nicht_geprueft`; unter
  `viertel` je Viertel Bearbeiter und angesehene Bilder; unter `segmente` je Kernsegment `id`,
  `klasse_heute`, `was_ist_es`, `urteil` (`sauber` | `nicht_sauber`), `klasse_vorschlag`, in B
  `klasse_frei`, `sicher`, `punkte` (je Punkt `art`: `klasse`, `verschmelzen`, `trennen`, `grenze`,
  `fehlt`, `fremdes`, `zu_klein`, `sonstiges`; `text` mit Bildpunkt-Lage; `flaeche_px`), `bilder`,
  `viertel`, `klasse`.
- **`naht.json`** (A, `zusammen/`): Ergebnis von `zusammentragen` mit allen Nahtverstößen.
- **`manifest.json`**: Ausschnitt, Raster, je Teilkachel Bild, Kern, Kontext und Lage; Pfade relativ
  zum Ordner des Manifests.

## Zahlen

Gezählt aus den Dateien in `ergebnisse/`; sie stimmen mit den Berichten des Testlaufs überein.

| | A Alles frei | B Kategorien frei | C Feste Liste |
|---|---:|---:|---:|
| Segmente je Teilkachel mit Rand (r0c0 / r0c1 / r1c0 / r1c1) | 128 / 272 / 64 / 417 | 206 / 234 / 86 / 408 | 206 / 234 / 86 / 408 |
| Segmente in T0 (Kerne) | 607 | 641 | 641 |
| unsicher (`sicher: nein`, im Kern) | 301 (50 %) | 397 (62 %) | 481 (75 %) |
| „nicht sauber“ laut Urteil | – | 405 (96 / 88 / 45 / 176) | 432 (114 / 89 / 48 / 181) |
| Klasse gegenüber der Vorstufe geändert | – | – | 383 |
| Nahtverstöße auf der Karte von ganz T0 | 309 | – (nicht zusammengetragen) | – (nicht zusammengetragen) |
| zerfallene Segmente auf der Karte von ganz T0 | 20 | – | – |

„Nicht sauber“ heißt: Die KI hat am Segment etwas auszusetzen (Klasse, Grenze, fehlende Fläche),
nicht, dass die Klasse falsch ist. Bei C betrafen die Punkte vor allem Klassen (328) und
Verschmelzen (156). Kosten: rund 3,3 Mio. Tokens für den Lauf der Urteile.

## Bekannte Schwächen

- **C Feste Kategorienliste**: Die Grenzen sind die der Vorstufe. Die Vorschläge der KI zum
  Verschmelzen und Teilen stehen je Segment dabei, sind aber nicht umgesetzt. Ob die Klassen
  passen, haben wir noch nicht durchgesehen.
- **A Alles frei**: Die vier Agents haben ihre Grenzen an den Kernrändern nicht abgestimmt:
  **309 Nahtverstöße** (`naht`), und **20 Segmente zerfallen** auf der Karte von ganz T0 in zwei
  Teile (in ihrer eigenen Teilkachel hängen sie zusammen, erst der Schnitt auf den Kern trennt sie).
  Die Arbeitsweise ist je Teilkachel verschieden, r1c0 ist deutlich gröber (35 Segmente im Kern).
- **B Kategorien frei**: Grenzen der Vorstufe wie C. Die Klasse „Feld gemäht“ (14 Segmente aus
  einem Viertel) ist ungeprüft (vielleicht gemähte Wiese statt abgeerntetes Feld). Laub- und
  Nadelbäume sind nicht getrennt, ebenso Strauch und Strauchgruppe.
- **Prüfseite und Nähte**: Der Schalter „Nähte“ der Seite zählt auf denselben Karten 124
  Verstöße je Fassung, das Werkzeug `naht` für A 309. Die Seite liest das Luftbild mit einer anderen
  Funktion ein; maßgeblich ist `naht`.
- Die SW-Spalte und die Abbildungen der festen Liste auf andere Klassifikationen sind ungeprüft.

## Was fehlt

- Die Durchsicht der festen Liste (C) durch uns: Klasse für Klasse „passt“ oder „passt nicht“.
- Die Schritte danach ruhen: Grenzen nach den Vorschlägen umsetzen, B und C zusammentragen und die
  Nähte prüfen, dann ein Messbericht mit Vergleich der drei Fassungen.

## Prüfseite öffnen

`ergebnisse/T0.html` doppelklicken (Chrome, Edge oder Firefox, ohne Internet). Die Seite öffnet mit
A „Alles frei“; oben schaltet man auf B und C um (auch Umschalt + A/B/C). Mausrad vergrößert,
Ziehen verschiebt, Klick wählt ein Segment und zeigt alle Felder samt Urteil und `punkte`.
Schalter: Ebene (grob/mittel/fein), Flächen, Umriss, Lücken, Nähte, Nur unsicher, Gitter,
Kategorien. Kommentare zu Segmenten lassen sich über „Export (JSON)“ speichern.

Neu bauen (etwa nach einer Änderung an einer Karte), im Ordner `programm/`:

```
python -B -m landseg seite --manifest ../ergebnisse/manifest.json --ziel ../ergebnisse/T0.html --kategorien ../ergebnisse/c-feste-liste/kategorien-c.json
```

Welche Fassungen es gibt und in welcher Reihenfolge, steht in `programm/einstellungen/seite.json`.

## Umgebung

Python 3.13 mit `numpy`, `tifffile`, `pillow`, `scipy`, `scikit-image`, `opencv-python`; für die
Vorstufe zusätzlich `torch` (mit CUDA) und `transformers` sowie die Gewichte `facebook/sam3` von
Hugging Face. Erprobt mit numpy 2.5.1, tifffile 2026.6.1, Pillow 12.3.0, SciPy 1.18.0,
scikit-image 0.26.0, OpenCV 4.13.0, torch 2.11.0+cu128, transformers 5.8.1.

```
python -m venv .venv
.venv\Scripts\pip install numpy tifffile pillow scipy scikit-image opencv-python
.venv\Scripts\pip install torch transformers          # nur für die Vorstufe (GPU)
```

Die Befehle der Werkzeuge laufen im Ordner `programm/` (ohne `-I`, sonst findet Python das Paket
nicht). Tests: `python -B -m unittest discover -s tests -t .`; Hilfe: `python -B -m landseg --help`.
`programm/README.md` nennt als `PY` einen Interpreter auf unserem Rechner; gemeint ist jeweils das
eigene `python`. `programm/tools/gesamt_projekt.py` braucht nur die Standardbibliothek.

## Einen neuen Ausschnitt rechnen

Gebraucht wird ein Luftbild als GeoTIFF mit Weltdatei (`.tfw`) und Lagebezug (`.prj`) daneben.
`<A>` ist ein Ergebnisordner, etwa `../arbeit/<name>` (im Projektordner unter `arbeit/`).
Alle Befehle im Ordner `programm/`.

```
# 1. Ausschnitt und Teilkacheln (hier: T0 aus dem Original; Kern 500, Rand 64)
python -B -m landseg kacheln --bild ../daten/luftbilder/orthofoto-aktuell/0009626524_100_Orthophoto_aktuell_5236-56.tif --x 2000 --y 2400 --breite 1000 --hoehe 1000 --kern 500 --rand 64 --name T0 --ziel <A>

# 2. Vorstufe je Teilkachel (GPU, rund eine halbe Minute je Teilkachel)
python -B -m landseg vorstufe --manifest <A>/manifest.json

# 3. Ausgang für die feste Liste: Vorstufe kopieren, dann prüfen
#    (für jede Teilkachel <A>/vorstufe/<tk>/labels.tif und segmente.json nach <A>/c-feste-liste/<tk>/)
python -B -m landseg pruefen --labels <A>/c-feste-liste/r0c0/labels.tif --segmente <A>/c-feste-liste/r0c0/segmente.json --bild <A>/teilkacheln/r0c0.png

# 4. Urteil und Eingriffe (Klasse setzen, verschmelzen, teilen, Grenze verschieben, Polygon)
python -B -m landseg eingriff --labels <A>/c-feste-liste/r0c0/labels.tif --segmente <A>/c-feste-liste/r0c0/segmente.json --bearbeiter <name> klasse --id 100010 --klasse 1.1.2

# 5. Teilkacheln zur Karte des Ausschnitts zusammentragen, Nähte prüfen
#    (Auftrag wie ergebnisse/a-alles-frei/zusammentragen.json, Pfade relativ zum Auftrag)
python -B -m landseg zusammentragen --datei <A>/c-feste-liste/zusammentragen.json
python -B -m landseg naht --manifest <A>/manifest.json --labels <A>/c-feste-liste/zusammen/labels.tif

# 6. Prüfseite
python -B -m landseg seite --manifest <A>/manifest.json --ziel <A>/T0.html
```

- Für Agents: In Schritt 4 urteilt je Teilkachel ein Agent nach den Vorlagen in `programm/vorlagen/`
  (Platzhalter in `programm/vorlagen/README.md`) und den Regeln in
  `programm/.claude/skills/landseg-agent/SKILL.md`. Die Hilfsskripte, die im Test die
  Viertel-Urteile zu `urteil.json` und zur Karte zusammengeführt haben, gehören nicht zum Paket;
  sie liegen bei den Berichten der Teilwünsche, etwa unter
  `wuensche/2026-11-17-landseg-test-t0-1/skripte/` und `wuensche/2026-11-17-landseg-test-t0-3/skripte/`. Die Regel
  dafür steht oben (`klasse = klasse_vorschlag`, sonst `klasse_heute`).
- Freie Listen (A, B) liegen als `kategorien-a.json` bzw. `kategorien-b.json` im Ordner der Fassung;
  `zusammentragen` und `pruefen` brauchen sie mit `--kategorien`, sonst gilt jede Klasse als ungültig.
- Ohne GPU: Schritte 1, 3 bis 6 laufen auf der CPU. Zum Ausprobieren eine Karte aus `ergebnisse/`
  als Ausgang nehmen, etwa `ergebnisse/c-feste-liste/<tk>/` in `<A>/c-feste-liste/` kopieren.
  Nachrechnen der Karte von A: `python -B -m landseg zusammentragen --datei ../ergebnisse/a-alles-frei/zusammentragen.json --kategorien ../ergebnisse/a-alles-frei/kategorien-a.json --ziel <neuer Ordner>`
  ergibt dieselbe Karte und 309 Nahtverstöße (Exit-Code 1 heißt hier „Befund“, nicht Absturz).
- Neue Teilkachelgröße: `--kern 250` ergibt 16 Teilkacheln statt 4.
