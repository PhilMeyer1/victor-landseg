# Auftrag: H0, Teilkachel r0c0, Viertel v4: 34 Segmente im Verbund ansehen und einzeln urteilen (Fassung C „Feste Kategorienliste“)

Lies zuerst den Skill `landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `r0c0` des Ausschnitts in `C:/Users/Phil/Developement/Victor/daten/landseg/H0`. Du urteilst über jedes
Segment deines Viertels v4 (Liste unter „Dein Viertel“), ob Grenze und Klasse stimmen, und zeichnest ein, was
du ändern würdest. Die Label-Karte änderst du nur nach dem Abschnitt „Nachsegmentieren“
(grob zusammengefasste Segmente teilen, bevor du sie urteilst).

## Daten (nur lesen; Ausnahme: Karte und `segmente.json` aus „Karte zum Nachsegmentieren“, nur über `eingriff` und `kante`)

- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/manifest.json`: Eintrag `r0c0` unter `teilkacheln` mit `bild` (Teilkachelbild,
  Kern + Kontextrand), `kern_im_bild` (Lage des Kerns im Teilkachelbild) und `kern` (Lage im Ausschnitt).
- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/labels.tif`: Label-Karte (Segment-ID je Bildpunkt, Größe des Teilkachelbilds).
- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/segmente.json`: je Segment `id`, `klasse`, `grob`, `herkunft`, `sicher`; dazu die
  Kandidatenliste der Vorstufe, falls vorhanden.
- `C:/Users/Phil/Developement/Victor/landseg/kategorien.json` und `C:/Users/Phil/Developement/Victor/landseg/KATEGORIEN.md`: die gültigen Klassen und Regeln.

## Zuerst der ganze Ausschnitt, dann die Teilkachel

Bevor du dein Viertel ansiehst: zuerst den ganzen Ausschnitt H0 (`C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png`, mit Teilkachelgitter
`C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/H0_raster.jpg`; r0c0 oben links, r0c1 oben rechts, r1c0 unten links, r1c1 unten rechts),
dann die ganze Teilkachel `r0c0` (`C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r0c0/ganz_nummern.jpg`: Grenzen, Nummern, Viertel cyan v1–v4;
`C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r0c0/ganz_roh.jpg` unverändert; beide 2fach). Beide stehen in `bilder_angesehen.uebersicht` vor den Viertelbildern.

## Schwarz-Weiß-Scan (gilt für H0)

H0 ist ein Ausschnitt von 1000 × 1000 Bildpunkten aus einem eingescannten Schwarz-Weiß-Luftbild von
1968 (`daten/luftbilder/historisch/1968105_0014_0228.tif`, x 1500, y 2000): Ortsrand mit Streckhöfen
(lange schmale Häuser in Reihen), Straßen, ein kleiner Anger, Äcker mit Streifenflur. Das Bild hat einen
Kanal; alle Bilder zeigen es als RGB mit drei gleichen Kanälen. Es hat keine Lagedaten (keine
Weltdatei, `georeferenz: null` im Manifest); ein Bildpunkt sind etwa 0,45 m (geschätzt; das farbige Orthofoto hat 0,2 m).

- Farbe gibt es nicht: Urteile nach Grauton, Textur, Form, Schatten und Lage zu den Nachbarn.
- Die SW-Spalte (`bw`) in `kategorien.json` ist eine ungeprüfte Vermutung, kein Beleg.
- Ist eine feine Klasse auf Schwarz-Weiß nicht sicher zu unterscheiden (etwa Acker gegen Grünland,
  Dach gegen Hof, Belag eines Weges), nimm die Klasse der Ebene darüber, setze `sicher: false` und
  schreibe unter `offen`, was im Farbbild entscheiden würde.
- Die Klassen der Vorstufe sind auf dem Scan schwach (SAM 3 ist für Farb-Orthofotos gebaut; drei
  Viertel bis neun Zehntel `sicher: nein`, Äcker teils als Gebäude): nur Hinweis.
- Die Vorstufe ist bewusst grob: Sie lief mit den Einstellungen des Repos, nur die Bildpunktgröße auf
  0,45 m gesetzt (`C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/vorstufe-h0-grob.json`). Häuserzeilen, Höfe mit Garten oder Äcker mit Weg können darum
  in einem Segment stecken.

## Dein Viertel

Viertel v4 (unten rechts) des Kerns von `r0c0`: x 314–563, y 314–563 im
Teilkachelbild (250 × 250 Bildpunkte). Dir gehören die 34 Segmente der Liste unten: Jedes hat den
größten Teil seiner Kernfläche in diesem Viertel. Die Teilkachel hat 173 Kernsegmente
(v1 58, v2 67, v3 14, v4 34); die anderen Viertel stehen in eigenen Aufträgen mit eigenem Ergebnisordner. Ein Segment
über einer Viertelgrenze urteilt nur das Viertel mit dem größten Anteil; in den Bildern der Nachbarn ist
es mit grauer Nummer als Umgebung zu sehen.

Urteil im Verbund: Du siehst das Viertel als zusammenhängendes Bild mit Umgebung, arbeitest die Liste der
Reihe nach ab und beurteilst jedes Segment im Zusammenhang mit seinen Nachbarn; eingetragen wird jedes
Segment einzeln (Klasse, `sicher`, `was_ist_es` als Notiz). Bilder freigestellter Einzelsegmente gibt es
nicht, und sie sind keine Urteilsgrundlage.

Bilder des Viertels (fertig, JPEG, in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c0/v4`, Fenster und Vergrößerung je Bild in `viertel.json`):

- Übersicht, das Viertel mit 32 Bildpunkten Umgebung, 3fach: `uebersicht_nummern.jpg`
  (Grenzen gelb, Nummern deiner Segmente weiß, der Nachbarviertel grau, Kontextrand ohne Nummer, Viertel
  cyan, Kern weiß umrandet, außerhalb des Viertels abgedunkelt), `uebersicht_roh.jpg`,
  `uebersicht_vorschlag.jpg` (Klassen der Vorstufe als Code und Farbe), `uebersicht_maengel.jpg`
  (`sicher: nein` und andere Mängel, Legende unten), `uebersicht_kontrast.jpg`, `uebersicht_gitter.jpg`
  (beschriftet in Bildpunkten der Teilkachel).
- Nahansichten, das Viertel in vier Teilen mit 12 Bildpunkten Umgebung, 6fach: `nah1_…` oben
  links, `nah2_…` oben rechts, `nah3_…` unten links, `nah4_…` unten rechts, je `_roh.jpg` und `_nummern.jpg`.
- Koordinaten: `x_teilkachel = fenster.x + x_bild // faktor` (im Gitterbild vorher 40 px links und 16 px
  oben abziehen). Nummer im Bild = ID mod 100000 (die letzten Stellen der ID); in `urteil.json` steht
  immer die volle ID.

Sieh zuerst `uebersicht_nummern.jpg` und `uebersicht_roh.jpg` an, dann die Nahansichten, bei blassen
Stellen `uebersicht_kontrast.jpg`. Unter `bilder_angesehen` stehen alle Bilder, die du angesehen hast
(`uebersicht`: H0, Teilkachel, mindestens `uebersicht_nummern.jpg`; `nah`: vorbereitete und eigene
Nahansichten, absolute Pfade), je Segment unter `bilder` die Bilder, auf denen du es beurteilt hast.

Liste (Reihenfolge der Abarbeitung, zeilenweise von oben links; Punkt = Stelle sicher im Segment, im
Teilkachelbild; Kandidaten aus `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/kandidaten.json`, dort mit Grund, in den
Bildern nicht eingezeichnet; Anteil hier = Anteil der Kernfläche in diesem Viertel):

| Nr | ID | Klasse Vorstufe | sicher | im Siedlungsgebiet | Kernfläche px | Anteil hier | auch in | Punkt x/y | Kandidaten |
|---|---|---|---|---|---|---|---|---|---|
| 172 | 100172 | 1.3.2 Baustelle | nein | nein | 219 | 76 % | v2 | 432/318 | grenze_ohne_bildkante, klasse_unsicher |
| 180 | 100180 | 2.1 Acker mit Bewuchs | nein | ja | 417 | 100 % | – | 439/339 | grenze_ohne_bildkante, klasse_unsicher |
| 143 | 100143 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 7128 | 53 % | v2 | 489/349 | grenze_ohne_bildkante, klasse_unsicher |
| 178 | 100178 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1126 | 100 % | – | 530/348 | klasse_unsicher |
| 165 | 100165 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 173 | 65 % | v2 | 557/318 | klasse_unsicher |
| 185 | 100185 | 1.3.4 Sport-, Spielplatz (künstlicher Belag) | ja | nein | 239 | 100 % | – | 434/364 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 187 | 100187 | 2.1 Acker mit Bewuchs | nein | ja | 241 | 100 % | – | 442/379 | grenze_ohne_bildkante, klasse_unsicher |
| 183 | 100183 | 1.3.2 Baustelle | nein | nein | 2574 | 100 % | – | 476/395 | grenze_ohne_bildkante, klasse_unsicher |
| 191 | 100191 | 1.2.1 Straße (versiegelt) | nein | nein | 124 | 100 % | – | 494/397 | grenze_ohne_bildkante, klasse_unsicher |
| 189 | 100189 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 662 | 100 % | – | 521/397 | grenze_ohne_bildkante, klasse_unsicher |
| 186 | 100186 | 1.3.2 Baustelle | nein | nein | 353 | 100 % | – | 528/368 | klasse_unsicher |
| 194 | 100194 | 2.1 Acker mit Bewuchs | nein | ja | 253 | 100 % | – | 458/407 | grenze_ohne_bildkante, klasse_unsicher |
| 199 | 100199 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | ja | ja | 148 | 100 % | – | 462/425 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 193 | 100193 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 121 | 100 % | – | 498/406 | grenze_ohne_bildkante, klasse_unsicher |
| 198 | 100198 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 1875 | 100 % | – | 513/445 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 196 | 100196 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 126 | 100 % | – | 519/414 | klasse_unsicher, nicht_zusammenhaengend |
| 192 | 100192 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 157 | 100 % | – | 536/406 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 176 | 100176 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 4869 | 100 % | – | 543/434 | grenze_ohne_bildkante, klasse_unsicher |
| 207 | 100207 | 2.1 Acker mit Bewuchs | nein | ja | 335 | 100 % | – | 495/450 | grenze_ohne_bildkante, klasse_unsicher |
| 201 | 100201 | 1.2.1 Straße (versiegelt) | nein | nein | 417 | 100 % | – | 512/468 | grenze_ohne_bildkante, klasse_unsicher |
| 209 | 100209 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 4 | 100 % | – | 562/492 | grenze_ohne_bildkante, klasse_unsicher |
| 216 | 100216 | 2.1 Acker mit Bewuchs | nein | ja | 345 | 100 % | – | 379/529 | grenze_ohne_bildkante, klasse_unsicher |
| 195 | 100195 | 2.1 Acker mit Bewuchs | nein | ja | 16486 | 100 % | – | 457/508 | grenze_ohne_bildkante, klasse_unsicher |
| 210 | 100210 | 2.1 Acker mit Bewuchs | nein | ja | 772 | 100 % | – | 534/510 | grenze_ohne_bildkante, klasse_unsicher |
| 214 | 100214 | 1.2.1 Straße (versiegelt) | nein | nein | 254 | 100 % | – | 552/526 | klasse_unsicher |
| 211 | 100211 | 1.2.1 Straße (versiegelt) | nein | nein | 197 | 100 % | – | 557/500 | grenze_ohne_bildkante, klasse_unsicher |
| 218 | 100218 | 1.3.2 Baustelle | nein | nein | 248 | 100 % | – | 557/542 | klasse_unsicher |
| 215 | 100215 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 22 | 100 % | – | 562/520 | grenze_ohne_bildkante, klasse_unsicher |
| 224 | 100224 | 2.1 Acker mit Bewuchs | nein | ja | 120 | 100 % | – | 369/559 | grenze_ohne_bildkante, klasse_unsicher |
| 220 | 100220 | 1.3.2 Baustelle | nein | nein | 342 | 100 % | – | 382/557 | grenze_ohne_bildkante, klasse_unsicher |
| 225 | 100225 | 2.1 Acker mit Bewuchs | nein | ja | 66 | 100 % | – | 398/558 | grenze_ohne_bildkante, klasse_unsicher |
| 219 | 100219 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 906 | 100 % | – | 537/551 | grenze_ohne_bildkante, klasse_unsicher |
| 228 | 100228 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 21 | 100 % | – | 542/562 | grenze_ohne_bildkante, klasse_unsicher |
| 229 | 100229 | 1.2.1 Straße (versiegelt) | nein | nein | 19 | 100 % | – | 545/562 | grenze_ohne_bildkante, klasse_unsicher |

`nicht_geprueft` nennt, was du nicht angesehen hast, `offen`, was du nicht entscheiden konntest.

Kontrolle vor der Rückgabe (muss mit `ok` enden):

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/skripte/pruefe_urteil.py --urteil C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil-gegenprobe/r0c0/v4/urteil.json --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/segmente.json --fassung c --viertel v4 --ids 100172,100180,100143,100178,100165,100185,100187,100183,100191,100189,100186,100194,100199,100193,100198,100196,100192,100176,100207,100201,100209,100216,100195,100210,100214,100211,100218,100215,100224,100220,100225,100219,100228,100229 --kategorien C:/Users/Phil/Developement/Victor/landseg/kategorien.json
```

## Nachsegmentieren (Entscheidung des Nutzers 2026-11-18)
Die Vorstufe ist bewusst grob. Fasst ein Segment sichtbar mehrere Objekte zusammen (Häuserzeile, Hof mit Garten, Acker mit Weg oder Rain, Baumgruppe mit Wiese), teilst du es selbst, BEVOR du es urteilst — direkt, ohne Umweg:
- Alle Eingriffe eines Viertels in EINEM Stapel: `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg eingriff --labels <Karte> --segmente <segmente.json> --bearbeiter <dein Name> stapel --datei <ergebnisordner>/eingriffe.json` mit Schritten `teilen` (Linienzug entlang der sichtbaren Bildkante), `polygon` (Fläche an Nachbarn oder neues Segment mit Klasse) oder `verschmelzen` (eine Fläche, zwei Stücke ohne Kante). Koordinaten in Bildpunkten der Teilkachel.
- Sitzt eine Linie nicht genau auf der Kante: `kante` (README) zum Einrasten. Danach `pruefen` — die Karte muss lückenlos bleiben.
- Neue IDs aus dem Stapel-Ergebnis urteilst du im selben urteil.json; jede Teilung steht dort unter "eingriffe" mit IDs vorher/nachher und Grund in einem Satz.
- Nur teilen, wo Objekte im Bild klar getrennt sind; kein Feinschliff an brauchbaren Grenzen, keine Teilung nach Vermutung. Unklare Mischflächen: nicht teilen, `sicher: false`, Notiz unter "offen".
- Zur Kontrolle eine Nahansicht der geänderten Stelle (`ansicht` oder eigenes Bild aus Karte und Teilkachelbild) einmal ansehen.

Karte zum Nachsegmentieren: `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/labels.tif` und `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/segmente.json`

So konkret (Befehle im Ordner `C:/Users/Phil/Developement/Victor/landseg`, dein Name `gegen-c-r0c0-v4`, Teilkachelbild `C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r0c0.png`):

- Stapeldatei `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil-gegenprobe/r0c0/v4/eingriffe.json`: `{"schritte": [{"op": "teilen", "id": 4, "linie": [[x, y], [x, y]]},
  {"op": "polygon_zuweisen", "flaeche": [[x, y], [x, y], [x, y]], "id": 7}, {"op": "polygon_zuweisen",
  "flaeche": [[x, y], …], "klasse": "Code"}, {"op": "verschmelzen", "ids": [3, 5]}]}` (im Stapel heißt
  `polygon` `polygon_zuweisen`; `klasse` braucht einen Code aus `kategorien.json`). Alles oder nichts: Schlägt ein Schritt fehl, bleibt die
  Karte unverändert; Datei korrigieren und erneut ausführen. Das Ergebnis nennt je Schritt `behalten`/`neu`
  bzw. `aufgeteilt_neu`; beim Teilen behält das größte Stück die ID.
- `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg eingriff --labels C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/labels.tif --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/segmente.json --bearbeiter gegen-c-r0c0-v4 stapel --datei C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil-gegenprobe/r0c0/v4/eingriffe.json`
- Einrasten: `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg kante --labels C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/labels.tif --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/segmente.json --bild C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r0c0.png --bearbeiter gegen-c-r0c0-v4 --a <ID> --b <ID>`
- Kontrolle: `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg pruefen --labels C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/labels.tif --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/segmente.json --bild C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r0c0.png` (muss mit `ok` enden).
- Nahansicht: `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg ansicht --manifest C:/Users/Phil/Developement/Victor/daten/landseg/H0/manifest.json --teilkachel r0c0 --labels C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/labels.tif --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/segmente.json --ziel C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil-gegenprobe/r0c0/v4/ansicht --ids <neue IDs>`
- Schreibe nur im Kern deines Viertels und nur an Segmenten deiner Liste (L2); Segmente der Nachbarviertel teilst du nicht.
- In `urteil.json`: `"eingriffe": [{"schritt": "teilen|polygon_zuweisen|verschmelzen", "vorher": [IDs], "nachher": [IDs],
  "grund": "ein Satz"}]`; ohne Eingriff `"eingriffe": []`. Jede ID aus `nachher`, die noch auf der Karte steht und im
  Kern liegt, steht unter `segmente`; eine ID deiner Liste, die durch Verschmelzen verschwand, nur unter `vorher`.

## Unabhängig urteilen

Du bist die Gegenprobe: Ein anderer Agent urteilt über dasselbe Viertel. Sein Ergebnis (`C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/`) und seine Karte (`C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r0c0/`) siehst du nicht an, auch nicht, wenn sie schon da sind. Du teilst nur auf deiner eigenen Kopie (`C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/`). Aus beiden Urteilen wird die Übereinstimmung gemessen.

## Werkzeuge

Befehle im Ordner `C:/Users/Phil/Developement/Victor/landseg` mit `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -m landseg <befehl>`; Aufruf und Schalter stehen in
`C:/Users/Phil/Developement/Victor/landseg/README.md`. Die Bilder deines Viertels liegen fertig vor (Abschnitt „Dein Viertel“); `ansicht` (W3) erzeugt Bilder
je Segment und ist hier keine Urteilsgrundlage. Für fragliche Grenzen `kante` (W4: ansehen; einrasten
nur an Linien aus deinem Nachsegmentieren), zur Kontrolle `pruefen`. Eigene Skripte als Datei in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil-gegenprobe/r0c0/v4`.

## Ergebnis in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil-gegenprobe/r0c0/v4` (genau diese Namen)

- `roh.jpg`, `umriss.jpg` (alle Segmentgrenzen mit ID), `maengel.jpg` (nummerierte Punkte mit kurzer
  deutscher Beschriftung, sonst Vermerk „keine Mängel“), `vorschlag.jpg` (Grenzen und Klassen, wie
  du sie setzen würdest, sonst Vermerk „unverändert“): je dein Viertel mit Umgebung, Viertel
  umrandet (Grundlage: die vorbereiteten Übersichtsbilder).
- `nah_<n>.jpg`: eigene Nahansichten von Stellen, die man in den vorbereiteten Bildern nicht beurteilen kann,
  je ein Teil des Viertels samt Nachbarn (mindestens 64 × 64 Bildpunkte der Teilkachel, kein freigestelltes
  Einzelsegment); `kontrast_<n>.jpg` bei blassen Stellen.
- `urteil.json` (UTF-8):

```
{"teilkachel": "r0c0", "viertel": "v4", "bearbeiter": "gegen-c-r0c0-v4",
 "bilder_angesehen": {"uebersicht": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r0c0/ganz_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c0/v4/uebersicht_nummern.jpg", "…"],
                      "nah": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c0/v4/nah1_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil-gegenprobe/r0c0/v4/nah_1.jpg", "…"]},
 "segmente": [{"id": 17, "klasse_heute": "Code", "was_ist_es": "ein Satz",
               "urteil": "sauber" | "nicht_sauber", "klasse_vorschlag": "Code oder null",
               "sicher": true | false,
               "punkte": [{"nr": 1, "art": "fremdes|fehlt|trennen|verschmelzen|grenze|klasse|zu_klein|sonstiges",
                           "text": "ein Satz mit Stelle (x/y im Teilkachelbild)", "flaeche_px": Zahl oder null}],
               "bilder": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c0/v4/uebersicht_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c0/v4/nah2_roh.jpg"]}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "was an der Kerngrenze nicht passt"}],
 "unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."],
 "eingriffe": [{"schritt": "teilen", "vorher": [ID], "nachher": [ID, ID], "grund": "ein Satz"}]}
```

Jedes Segment deiner Liste steht genau einmal unter `segmente`, auch die sauberen, in der Reihenfolge der Liste. Segmente der Nachbarviertel (graue Nummern) und des Kontextrands (ohne Nummer) urteilst du in diesem Auftrag nicht; Auffälliges an ihnen nennst du unter `unsicher` mit ID.

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Punkte, Anteil `sicher: false`, wo du unsicher bist.
