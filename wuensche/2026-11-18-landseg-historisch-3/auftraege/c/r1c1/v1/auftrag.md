# Auftrag: H0, Teilkachel r1c1, Viertel v1: 52 Segmente im Verbund ansehen und einzeln urteilen (Fassung C „Feste Kategorienliste“)

Lies zuerst den Skill `landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `r1c1` des Ausschnitts in `C:/Users/Phil/Developement/Victor/daten/landseg/H0`. Du urteilst über jedes
Segment deines Viertels v1 (Liste unter „Dein Viertel“), ob Grenze und Klasse stimmen, und zeichnest ein, was
du ändern würdest. Die Label-Karte änderst du nur nach dem Abschnitt „Nachsegmentieren“
(grob zusammengefasste Segmente teilen, bevor du sie urteilst).

## Daten (nur lesen; Ausnahme: Karte und `segmente.json` aus „Karte zum Nachsegmentieren“, nur über `eingriff` und `kante`)

- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/manifest.json`: Eintrag `r1c1` unter `teilkacheln` mit `bild` (Teilkachelbild,
  Kern + Kontextrand), `kern_im_bild` (Lage des Kerns im Teilkachelbild) und `kern` (Lage im Ausschnitt).
- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r1c1/labels.tif`: Label-Karte (Segment-ID je Bildpunkt, Größe des Teilkachelbilds).
- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r1c1/segmente.json`: je Segment `id`, `klasse`, `grob`, `herkunft`, `sicher`; dazu die
  Kandidatenliste der Vorstufe, falls vorhanden.
- `C:/Users/Phil/Developement/Victor/landseg/kategorien.json` und `C:/Users/Phil/Developement/Victor/landseg/KATEGORIEN.md`: die gültigen Klassen und Regeln.

## Zuerst der ganze Ausschnitt, dann die Teilkachel

Bevor du dein Viertel ansiehst: zuerst den ganzen Ausschnitt H0 (`C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png`, mit Teilkachelgitter
`C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/H0_raster.jpg`; r0c0 oben links, r0c1 oben rechts, r1c0 unten links, r1c1 unten rechts),
dann die ganze Teilkachel `r1c1` (`C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r1c1/ganz_nummern.jpg`: Grenzen, Nummern, Viertel cyan v1–v4;
`C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r1c1/ganz_roh.jpg` unverändert; beide 2fach). Beide stehen in `bilder_angesehen.uebersicht` vor den Viertelbildern.

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

Viertel v1 (oben links) des Kerns von `r1c1`: x 64–313, y 64–313 im
Teilkachelbild (250 × 250 Bildpunkte). Dir gehören die 52 Segmente der Liste unten: Jedes hat den
größten Teil seiner Kernfläche in diesem Viertel. Die Teilkachel hat 162 Kernsegmente
(v1 52, v2 47, v3 37, v4 26); die anderen Viertel stehen in eigenen Aufträgen mit eigenem Ergebnisordner. Ein Segment
über einer Viertelgrenze urteilt nur das Viertel mit dem größten Anteil; in den Bildern der Nachbarn ist
es mit grauer Nummer als Umgebung zu sehen.

Urteil im Verbund: Du siehst das Viertel als zusammenhängendes Bild mit Umgebung, arbeitest die Liste der
Reihe nach ab und beurteilst jedes Segment im Zusammenhang mit seinen Nachbarn; eingetragen wird jedes
Segment einzeln (Klasse, `sicher`, `was_ist_es` als Notiz). Bilder freigestellter Einzelsegmente gibt es
nicht, und sie sind keine Urteilsgrundlage.

Bilder des Viertels (fertig, JPEG, in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c1/v1`, Fenster und Vergrößerung je Bild in `viertel.json`):

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
Teilkachelbild; Kandidaten aus `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r1c1/kandidaten.json`, dort mit Grund, in den
Bildern nicht eingezeichnet; Anteil hier = Anteil der Kernfläche in diesem Viertel):

| Nr | ID | Klasse Vorstufe | sicher | im Siedlungsgebiet | Kernfläche px | Anteil hier | auch in | Punkt x/y | Kandidaten |
|---|---|---|---|---|---|---|---|---|---|
| 37 | 400037 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | ja | nein | 37 | 100 % | – | 66/66 | – |
| 64 | 400064 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 66 | 100 % | – | 67/77 | klasse_unsicher |
| 72 | 400072 | 2.1 Acker mit Bewuchs | nein | ja | 246 | 100 % | – | 75/89 | grenze_ohne_bildkante, klasse_unsicher |
| 75 | 400075 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 191 | 100 % | – | 89/99 | klasse_unsicher |
| 39 | 400039 | 1.3.2 Baustelle | nein | nein | 34 | 100 % | – | 96/65 | grenze_ohne_bildkante, klasse_unsicher |
| 56 | 400056 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 157 | 100 % | – | 106/68 | klasse_unsicher |
| 46 | 400046 | 1.2.1 Straße (versiegelt) | nein | nein | 519 | 100 % | – | 124/93 | grenze_ohne_bildkante, klasse_unsicher |
| 54 | 400054 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | ja | nein | 588 | 100 % | – | 125/75 | – |
| 47 | 400047 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 45 | 100 % | – | 132/67 | klasse_unsicher |
| 48 | 400048 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 67 | 100 % | – | 137/66 | klasse_unsicher |
| 73 | 400073 | 1.2.1 Straße (versiegelt) | nein | nein | 592 | 100 % | – | 165/95 | grenze_ohne_bildkante, klasse_unsicher |
| 66 | 400066 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 478 | 100 % | – | 192/85 | klasse_unsicher |
| 63 | 400063 | 1.3.2 Baustelle | nein | nein | 695 | 100 % | – | 279/93 | klasse_unsicher |
| 35 | 400035 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 282 | 100 % | – | 289/69 | klasse_unsicher |
| 9 | 400009 | 6.6 Weg, unbefestigt (Feld-, Wald-, Schotterweg) | nein | nein | 11 | 100 % | – | 308/65 | klasse_unsicher |
| 85 | 400085 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 178 | 100 % | – | 110/118 | klasse_unsicher |
| 89 | 400089 | 2.1 Acker mit Bewuchs | nein | ja | 230 | 100 % | – | 114/127 | klasse_unsicher |
| 3 | 400003 | 6.6 Weg, unbefestigt (Feld-, Wald-, Schotterweg) | nein | nein | 2653 | 100 % | – | 125/110 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 69 | 400069 | 1.3.2 Baustelle | nein | nein | 1391 | 100 % | – | 163/112 | grenze_ohne_bildkante, klasse_unsicher |
| 94 | 400094 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 900 | 100 % | – | 163/139 | klasse_unsicher |
| 60 | 400060 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | ja | nein | 3390 | 52 % | v2 | 299/128 | – |
| 78 | 400078 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | ja | ja | 6484 | 100 % | – | 94/173 | grenze_ohne_bildkante |
| 101 | 400101 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 342 | 100 % | – | 126/150 | klasse_unsicher |
| 112 | 400112 | 1.2.1 Straße (versiegelt) | ja | nein | 136 | 100 % | – | 146/188 | nicht_zusammenhaengend |
| 102 | 400102 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 910 | 100 % | – | 167/166 | grenze_ohne_bildkante, klasse_unsicher |
| 109 | 400109 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 831 | 100 % | – | 176/193 | grenze_ohne_bildkante, klasse_unsicher |
| 96 | 400096 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | ja | nein | 1271 | 100 % | – | 195/180 | – |
| 105 | 400105 | 1.3.2 Baustelle | nein | nein | 214 | 100 % | – | 303/163 | klasse_unsicher |
| 111 | 400111 | 1.3.2 Baustelle | nein | nein | 73 | 56 % | v2 | 310/186 | klasse_unsicher |
| 110 | 400110 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 2358 | 100 % | – | 108/219 | klasse_unsicher |
| 116 | 400116 | 2.1 Acker mit Bewuchs | nein | ja | 96 | 100 % | – | 132/211 | grenze_ohne_bildkante, klasse_unsicher |
| 115 | 400115 | 1.3.2 Baustelle | nein | nein | 471 | 100 % | – | 149/205 | grenze_ohne_bildkante, klasse_unsicher |
| 119 | 400119 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 139 | 100 % | – | 149/219 | grenze_ohne_bildkante, klasse_unsicher |
| 125 | 400125 | 3.1 Wiese / Weide (gemeinsam) | ja | ja | 163 | 100 % | – | 155/242 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 120 | 400120 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 114 | 100 % | – | 157/225 | klasse_unsicher |
| 117 | 400117 | 1.2.1 Straße (versiegelt) | nein | nein | 79 | 100 % | – | 165/216 | grenze_ohne_bildkante, klasse_unsicher |
| 128 | 400128 | 1.2.1 Straße (versiegelt) | nein | nein | 73 | 100 % | – | 173/249 | klasse_unsicher |
| 122 | 400122 | 1.3.2 Baustelle | nein | nein | 204 | 100 % | – | 193/234 | grenze_ohne_bildkante, klasse_unsicher |
| 127 | 400127 | 1.2.1 Straße (versiegelt) | nein | nein | 202 | 100 % | – | 201/244 | grenze_ohne_bildkante, klasse_unsicher |
| 129 | 400129 | 1.3.2 Baustelle | nein | nein | 110 | 100 % | – | 213/245 | grenze_ohne_bildkante, klasse_unsicher |
| 6 | 400006 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 50144 | 50 % | v2, v3, v4 | 265/219 | grenze_ohne_bildkante, klasse_unsicher |
| 136 | 400136 | 2.1 Acker mit Bewuchs | nein | ja | 13 | 100 % | – | 65/275 | grenze_ohne_bildkante, klasse_unsicher |
| 137 | 400137 | 6.6 Weg, unbefestigt (Feld-, Wald-, Schotterweg) | nein | nein | 30 | 100 % | – | 66/269 | klasse_unsicher |
| 140 | 400140 | 3.1 Wiese / Weide (gemeinsam) | ja | ja | 146 | 100 % | – | 173/291 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 133 | 400133 | 4.2.4 Gebüsch / Strauchfläche | nein | ja | 123 | 100 % | – | 174/259 | klasse_unsicher |
| 126 | 400126 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 624 | 100 % | – | 179/276 | klasse_unsicher |
| 142 | 400142 | 4.2.4 Gebüsch / Strauchfläche | nein | ja | 150 | 100 % | – | 181/294 | grenze_ohne_bildkante, klasse_unsicher |
| 121 | 400121 | 6.6 Weg, unbefestigt (Feld-, Wald-, Schotterweg) | nein | nein | 1271 | 100 % | – | 188/255 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 143 | 400143 | 1.2.1 Straße (versiegelt) | ja | nein | 89 | 100 % | – | 200/299 | – |
| 132 | 400132 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 859 | 100 % | – | 216/274 | klasse_unsicher |
| 131 | 400131 | 1.3.2 Baustelle | nein | nein | 110 | 100 % | – | 219/253 | klasse_unsicher |
| 146 | 400146 | 1.2.1 Straße (versiegelt) | ja | nein | 235 | 62 % | v3 | 209/309 | nicht_zusammenhaengend |

`nicht_geprueft` nennt, was du nicht angesehen hast, `offen`, was du nicht entscheiden konntest.

Kontrolle vor der Rückgabe (muss mit `ok` enden):

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/skripte/pruefe_urteil.py --urteil C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r1c1/v1/urteil.json --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r1c1/segmente.json --fassung c --viertel v1 --ids 400037,400064,400072,400075,400039,400056,400046,400054,400047,400048,400073,400066,400063,400035,400009,400085,400089,400003,400069,400094,400060,400078,400101,400112,400102,400109,400096,400105,400111,400110,400116,400115,400119,400125,400120,400117,400128,400122,400127,400129,400006,400136,400137,400140,400133,400126,400142,400121,400143,400132,400131,400146 --kategorien C:/Users/Phil/Developement/Victor/landseg/kategorien.json
```

## Nachsegmentieren (Entscheidung des Nutzers 2026-11-18)
Die Vorstufe ist bewusst grob. Fasst ein Segment sichtbar mehrere Objekte zusammen (Häuserzeile, Hof mit Garten, Acker mit Weg oder Rain, Baumgruppe mit Wiese), teilst du es selbst, BEVOR du es urteilst — direkt, ohne Umweg:
- Alle Eingriffe eines Viertels in EINEM Stapel: `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg eingriff --labels <Karte> --segmente <segmente.json> --bearbeiter <dein Name> stapel --datei <ergebnisordner>/eingriffe.json` mit Schritten `teilen` (Linienzug entlang der sichtbaren Bildkante), `polygon` (Fläche an Nachbarn oder neues Segment mit Klasse) oder `verschmelzen` (eine Fläche, zwei Stücke ohne Kante). Koordinaten in Bildpunkten der Teilkachel.
- Sitzt eine Linie nicht genau auf der Kante: `kante` (README) zum Einrasten. Danach `pruefen` — die Karte muss lückenlos bleiben.
- Neue IDs aus dem Stapel-Ergebnis urteilst du im selben urteil.json; jede Teilung steht dort unter "eingriffe" mit IDs vorher/nachher und Grund in einem Satz.
- Nur teilen, wo Objekte im Bild klar getrennt sind; kein Feinschliff an brauchbaren Grenzen, keine Teilung nach Vermutung. Unklare Mischflächen: nicht teilen, `sicher: false`, Notiz unter "offen".
- Zur Kontrolle eine Nahansicht der geänderten Stelle (`ansicht` oder eigenes Bild aus Karte und Teilkachelbild) einmal ansehen.

Karte zum Nachsegmentieren: `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r1c1/labels.tif` und `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r1c1/segmente.json`

So konkret (Befehle im Ordner `C:/Users/Phil/Developement/Victor/landseg`, dein Name `urt-c-r1c1-v1`, Teilkachelbild `C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r1c1.png`):

- Stapeldatei `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r1c1/v1/eingriffe.json`: `{"schritte": [{"op": "teilen", "id": 4, "linie": [[x, y], [x, y]]},
  {"op": "polygon_zuweisen", "flaeche": [[x, y], [x, y], [x, y]], "id": 7}, {"op": "polygon_zuweisen",
  "flaeche": [[x, y], …], "klasse": "Code"}, {"op": "verschmelzen", "ids": [3, 5]}]}` (im Stapel heißt
  `polygon` `polygon_zuweisen`; `klasse` braucht einen Code aus `kategorien.json`). Alles oder nichts: Schlägt ein Schritt fehl, bleibt die
  Karte unverändert; Datei korrigieren und erneut ausführen. Das Ergebnis nennt je Schritt `behalten`/`neu`
  bzw. `aufgeteilt_neu`; beim Teilen behält das größte Stück die ID.
- `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg eingriff --labels C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r1c1/labels.tif --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r1c1/segmente.json --bearbeiter urt-c-r1c1-v1 stapel --datei C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r1c1/v1/eingriffe.json`
- Einrasten: `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg kante --labels C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r1c1/labels.tif --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r1c1/segmente.json --bild C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r1c1.png --bearbeiter urt-c-r1c1-v1 --a <ID> --b <ID>`
- Kontrolle: `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg pruefen --labels C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r1c1/labels.tif --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r1c1/segmente.json --bild C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r1c1.png` (muss mit `ok` enden).
- Nahansicht: `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg ansicht --manifest C:/Users/Phil/Developement/Victor/daten/landseg/H0/manifest.json --teilkachel r1c1 --labels C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r1c1/labels.tif --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r1c1/segmente.json --ziel C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r1c1/v1/ansicht --ids <neue IDs>`
- Schreibe nur im Kern deines Viertels und nur an Segmenten deiner Liste (L2); Segmente der Nachbarviertel teilst du nicht.
- In `urteil.json`: `"eingriffe": [{"schritt": "teilen|polygon_zuweisen|verschmelzen", "vorher": [IDs], "nachher": [IDs],
  "grund": "ein Satz"}]`; ohne Eingriff `"eingriffe": []`. Jede ID aus `nachher`, die noch auf der Karte steht und im
  Kern liegt, steht unter `segmente`; eine ID deiner Liste, die durch Verschmelzen verschwand, nur unter `vorher`.

## Werkzeuge

Befehle im Ordner `C:/Users/Phil/Developement/Victor/landseg` mit `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -m landseg <befehl>`; Aufruf und Schalter stehen in
`C:/Users/Phil/Developement/Victor/landseg/README.md`. Die Bilder deines Viertels liegen fertig vor (Abschnitt „Dein Viertel“); `ansicht` (W3) erzeugt Bilder
je Segment und ist hier keine Urteilsgrundlage. Für fragliche Grenzen `kante` (W4: ansehen; einrasten
nur an Linien aus deinem Nachsegmentieren), zur Kontrolle `pruefen`. Eigene Skripte als Datei in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r1c1/v1`.

## Ergebnis in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r1c1/v1` (genau diese Namen)

- `roh.jpg`, `umriss.jpg` (alle Segmentgrenzen mit ID), `maengel.jpg` (nummerierte Punkte mit kurzer
  deutscher Beschriftung, sonst Vermerk „keine Mängel“), `vorschlag.jpg` (Grenzen und Klassen, wie
  du sie setzen würdest, sonst Vermerk „unverändert“): je dein Viertel mit Umgebung, Viertel
  umrandet (Grundlage: die vorbereiteten Übersichtsbilder).
- `nah_<n>.jpg`: eigene Nahansichten von Stellen, die man in den vorbereiteten Bildern nicht beurteilen kann,
  je ein Teil des Viertels samt Nachbarn (mindestens 64 × 64 Bildpunkte der Teilkachel, kein freigestelltes
  Einzelsegment); `kontrast_<n>.jpg` bei blassen Stellen.
- `urteil.json` (UTF-8):

```
{"teilkachel": "r1c1", "viertel": "v1", "bearbeiter": "urt-c-r1c1-v1",
 "bilder_angesehen": {"uebersicht": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r1c1/ganz_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c1/v1/uebersicht_nummern.jpg", "…"],
                      "nah": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c1/v1/nah1_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r1c1/v1/nah_1.jpg", "…"]},
 "segmente": [{"id": 17, "klasse_heute": "Code", "was_ist_es": "ein Satz",
               "urteil": "sauber" | "nicht_sauber", "klasse_vorschlag": "Code oder null",
               "sicher": true | false,
               "punkte": [{"nr": 1, "art": "fremdes|fehlt|trennen|verschmelzen|grenze|klasse|zu_klein|sonstiges",
                           "text": "ein Satz mit Stelle (x/y im Teilkachelbild)", "flaeche_px": Zahl oder null}],
               "bilder": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c1/v1/uebersicht_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c1/v1/nah2_roh.jpg"]}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "was an der Kerngrenze nicht passt"}],
 "unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."],
 "eingriffe": [{"schritt": "teilen", "vorher": [ID], "nachher": [ID, ID], "grund": "ein Satz"}]}
```

Jedes Segment deiner Liste steht genau einmal unter `segmente`, auch die sauberen, in der Reihenfolge der Liste. Segmente der Nachbarviertel (graue Nummern) und des Kontextrands (ohne Nummer) urteilst du in diesem Auftrag nicht; Auffälliges an ihnen nennst du unter `unsicher` mit ID.

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Punkte, Anteil `sicher: false`, wo du unsicher bist.
