# Auftrag: H0, Teilkachel r1c1, Viertel v3: 37 Segmente im Verbund ansehen und einzeln urteilen (Fassung C „Feste Kategorienliste“)

Lies zuerst den Skill `landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `r1c1` des Ausschnitts in `C:/Users/Phil/Developement/Victor/daten/landseg/H0`. Du urteilst über jedes
Segment deines Viertels v3 (Liste unter „Dein Viertel“), ob Grenze und Klasse stimmen, und zeichnest ein, was
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

Viertel v3 (unten links) des Kerns von `r1c1`: x 64–313, y 314–563 im
Teilkachelbild (250 × 250 Bildpunkte). Dir gehören die 37 Segmente der Liste unten: Jedes hat den
größten Teil seiner Kernfläche in diesem Viertel. Die Teilkachel hat 162 Kernsegmente
(v1 52, v2 47, v3 37, v4 26); die anderen Viertel stehen in eigenen Aufträgen mit eigenem Ergebnisordner. Ein Segment
über einer Viertelgrenze urteilt nur das Viertel mit dem größten Anteil; in den Bildern der Nachbarn ist
es mit grauer Nummer als Umgebung zu sehen.

Urteil im Verbund: Du siehst das Viertel als zusammenhängendes Bild mit Umgebung, arbeitest die Liste der
Reihe nach ab und beurteilst jedes Segment im Zusammenhang mit seinen Nachbarn; eingetragen wird jedes
Segment einzeln (Klasse, `sicher`, `was_ist_es` als Notiz). Bilder freigestellter Einzelsegmente gibt es
nicht, und sie sind keine Urteilsgrundlage.

Bilder des Viertels (fertig, JPEG, in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c1/v3`, Fenster und Vergrößerung je Bild in `viertel.json`):

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
| 145 | 400145 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 1461 | 72 % | v1 | 198/321 | grenze_ohne_bildkante, klasse_unsicher |
| 154 | 400154 | 1.3.2 Baustelle | nein | nein | 129 | 100 % | – | 239/341 | klasse_unsicher |
| 153 | 400153 | 2.1 Acker mit Bewuchs | nein | ja | 436 | 100 % | – | 206/355 | grenze_ohne_bildkante, klasse_unsicher |
| 155 | 400155 | 1.2.1 Straße (versiegelt) | ja | nein | 87 | 100 % | – | 226/350 | – |
| 162 | 400162 | 1.2.1 Straße (versiegelt) | nein | nein | 84 | 100 % | – | 234/372 | grenze_ohne_bildkante, klasse_unsicher |
| 168 | 400168 | 1.3.2 Baustelle | nein | nein | 192 | 100 % | – | 235/392 | grenze_ohne_bildkante, klasse_unsicher |
| 164 | 400164 | 1.2.1 Straße (versiegelt) | ja | nein | 131 | 100 % | – | 241/378 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 148 | 400148 | 6.6 Weg, unbefestigt (Feld-, Wald-, Schotterweg) | nein | nein | 2497 | 99 % | v1 | 253/394 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 163 | 400163 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 235 | 100 % | – | 267/376 | klasse_unsicher |
| 170 | 400170 | 1.3.2 Baustelle | nein | nein | 173 | 100 % | – | 280/398 | klasse_unsicher |
| 165 | 400165 | 1.3.2 Baustelle | nein | nein | 97 | 100 % | – | 289/385 | klasse_unsicher |
| 173 | 400173 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 103 | 100 % | – | 238/401 | grenze_ohne_bildkante, klasse_unsicher |
| 175 | 400175 | 2.1 Acker mit Bewuchs | nein | ja | 173 | 100 % | – | 245/413 | grenze_ohne_bildkante, klasse_unsicher |
| 180 | 400180 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 124 | 100 % | – | 250/424 | grenze_ohne_bildkante, klasse_unsicher |
| 178 | 400178 | 1.2.1 Straße (versiegelt) | ja | nein | 93 | 100 % | – | 259/423 | – |
| 181 | 400181 | 1.3.2 Baustelle | nein | nein | 363 | 100 % | – | 265/445 | grenze_ohne_bildkante, klasse_unsicher |
| 177 | 400177 | 1.2.1 Straße (versiegelt) | nein | nein | 142 | 100 % | – | 277/417 | klasse_unsicher |
| 182 | 400182 | 1.2.1 Straße (versiegelt) | nein | nein | 257 | 100 % | – | 281/434 | klasse_unsicher |
| 171 | 400171 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 944 | 83 % | v4 | 304/410 | klasse_unsicher |
| 118 | 400118 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | ja | nein | 52197 | 85 % | v1 | 153/473 | grenze_ohne_bildkante |
| 186 | 400186 | 2.1 Acker mit Bewuchs | nein | ja | 295 | 100 % | – | 258/455 | grenze_ohne_bildkante, klasse_unsicher |
| 189 | 400189 | 4.2.4 Gebüsch / Strauchfläche | nein | ja | 499 | 100 % | – | 272/466 | klasse_unsicher |
| 197 | 400197 | 2.1 Acker mit Bewuchs | nein | ja | 286 | 100 % | – | 272/497 | grenze_ohne_bildkante, klasse_unsicher |
| 200 | 400200 | 1.3.2 Baustelle | nein | nein | 82 | 100 % | – | 282/498 | klasse_unsicher |
| 187 | 400187 | 1.2.1 Straße (versiegelt) | nein | nein | 795 | 90 % | v4 | 289/479 | klasse_unsicher |
| 190 | 400190 | 6.6 Weg, unbefestigt (Feld-, Wald-, Schotterweg) | nein | nein | 124 | 100 % | – | 292/462 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 202 | 400202 | 2.1 Acker mit Bewuchs | ja | nein | 3 | 100 % | – | 64/505 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 209 | 400209 | 1.3.4 Sport-, Spielplatz (künstlicher Belag) | ja | nein | 52 | 100 % | – | 66/524 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 176 | 400176 | 2.1 Acker mit Bewuchs | nein | nein | 237 | 100 % | – | 68/545 | grenze_ohne_bildkante, klasse_unsicher |
| 211 | 400211 | 2.1 Acker mit Bewuchs | ja | nein | 106 | 100 % | – | 68/533 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 208 | 400208 | 6.1 Offene Sand-, Löss-, Lehmstelle (Abbruch, Hohlweg, Grube) | nein | nein | 149 | 100 % | – | 281/522 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 203 | 400203 | 1.3.2 Baustelle | nein | nein | 202 | 100 % | – | 291/505 | klasse_unsicher |
| 214 | 400214 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | ja | nein | 180 | 100 % | – | 299/546 | – |
| 207 | 400207 | 1.2.1 Straße (versiegelt) | nein | nein | 620 | 72 % | v4 | 306/534 | klasse_unsicher |
| 215 | 400215 | 2.1 Acker mit Bewuchs | ja | nein | 126 | 100 % | – | 75/555 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 210 | 400210 | 2.1 Acker mit Bewuchs | nein | ja | 386 | 100 % | – | 292/554 | grenze_ohne_bildkante, klasse_unsicher |
| 216 | 400216 | 1.3.2 Baustelle | nein | nein | 88 | 91 % | v4 | 310/560 | klasse_unsicher |

`nicht_geprueft` nennt, was du nicht angesehen hast, `offen`, was du nicht entscheiden konntest.

Kontrolle vor der Rückgabe (muss mit `ok` enden):

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/skripte/pruefe_urteil.py --urteil C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r1c1/v3/urteil.json --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r1c1/segmente.json --fassung c --viertel v3 --ids 400145,400154,400153,400155,400162,400168,400164,400148,400163,400170,400165,400173,400175,400180,400178,400181,400177,400182,400171,400118,400186,400189,400197,400200,400187,400190,400202,400209,400176,400211,400208,400203,400214,400207,400215,400210,400216 --kategorien C:/Users/Phil/Developement/Victor/landseg/kategorien.json
```

## Nachsegmentieren (Entscheidung des Nutzers 2026-11-18)
Die Vorstufe ist bewusst grob. Fasst ein Segment sichtbar mehrere Objekte zusammen (Häuserzeile, Hof mit Garten, Acker mit Weg oder Rain, Baumgruppe mit Wiese), teilst du es selbst, BEVOR du es urteilst — direkt, ohne Umweg:
- Alle Eingriffe eines Viertels in EINEM Stapel: `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg eingriff --labels <Karte> --segmente <segmente.json> --bearbeiter <dein Name> stapel --datei <ergebnisordner>/eingriffe.json` mit Schritten `teilen` (Linienzug entlang der sichtbaren Bildkante), `polygon` (Fläche an Nachbarn oder neues Segment mit Klasse) oder `verschmelzen` (eine Fläche, zwei Stücke ohne Kante). Koordinaten in Bildpunkten der Teilkachel.
- Sitzt eine Linie nicht genau auf der Kante: `kante` (README) zum Einrasten. Danach `pruefen` — die Karte muss lückenlos bleiben.
- Neue IDs aus dem Stapel-Ergebnis urteilst du im selben urteil.json; jede Teilung steht dort unter "eingriffe" mit IDs vorher/nachher und Grund in einem Satz.
- Nur teilen, wo Objekte im Bild klar getrennt sind; kein Feinschliff an brauchbaren Grenzen, keine Teilung nach Vermutung. Unklare Mischflächen: nicht teilen, `sicher: false`, Notiz unter "offen".
- Zur Kontrolle eine Nahansicht der geänderten Stelle (`ansicht` oder eigenes Bild aus Karte und Teilkachelbild) einmal ansehen.

Karte zum Nachsegmentieren: `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r1c1/labels.tif` und `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r1c1/segmente.json`

So konkret (Befehle im Ordner `C:/Users/Phil/Developement/Victor/landseg`, dein Name `urt-c-r1c1-v3`, Teilkachelbild `C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r1c1.png`):

- Stapeldatei `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r1c1/v3/eingriffe.json`: `{"schritte": [{"op": "teilen", "id": 4, "linie": [[x, y], [x, y]]},
  {"op": "polygon_zuweisen", "flaeche": [[x, y], [x, y], [x, y]], "id": 7}, {"op": "polygon_zuweisen",
  "flaeche": [[x, y], …], "klasse": "Code"}, {"op": "verschmelzen", "ids": [3, 5]}]}` (im Stapel heißt
  `polygon` `polygon_zuweisen`; `klasse` braucht einen Code aus `kategorien.json`). Alles oder nichts: Schlägt ein Schritt fehl, bleibt die
  Karte unverändert; Datei korrigieren und erneut ausführen. Das Ergebnis nennt je Schritt `behalten`/`neu`
  bzw. `aufgeteilt_neu`; beim Teilen behält das größte Stück die ID.
- `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg eingriff --labels C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r1c1/labels.tif --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r1c1/segmente.json --bearbeiter urt-c-r1c1-v3 stapel --datei C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r1c1/v3/eingriffe.json`
- Einrasten: `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg kante --labels C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r1c1/labels.tif --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r1c1/segmente.json --bild C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r1c1.png --bearbeiter urt-c-r1c1-v3 --a <ID> --b <ID>`
- Kontrolle: `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg pruefen --labels C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r1c1/labels.tif --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r1c1/segmente.json --bild C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r1c1.png` (muss mit `ok` enden).
- Nahansicht: `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg ansicht --manifest C:/Users/Phil/Developement/Victor/daten/landseg/H0/manifest.json --teilkachel r1c1 --labels C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r1c1/labels.tif --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r1c1/segmente.json --ziel C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r1c1/v3/ansicht --ids <neue IDs>`
- Schreibe nur im Kern deines Viertels und nur an Segmenten deiner Liste (L2); Segmente der Nachbarviertel teilst du nicht.
- In `urteil.json`: `"eingriffe": [{"schritt": "teilen|polygon_zuweisen|verschmelzen", "vorher": [IDs], "nachher": [IDs],
  "grund": "ein Satz"}]`; ohne Eingriff `"eingriffe": []`. Jede ID aus `nachher`, die noch auf der Karte steht und im
  Kern liegt, steht unter `segmente`; eine ID deiner Liste, die durch Verschmelzen verschwand, nur unter `vorher`.

## Werkzeuge

Befehle im Ordner `C:/Users/Phil/Developement/Victor/landseg` mit `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -m landseg <befehl>`; Aufruf und Schalter stehen in
`C:/Users/Phil/Developement/Victor/landseg/README.md`. Die Bilder deines Viertels liegen fertig vor (Abschnitt „Dein Viertel“); `ansicht` (W3) erzeugt Bilder
je Segment und ist hier keine Urteilsgrundlage. Für fragliche Grenzen `kante` (W4: ansehen; einrasten
nur an Linien aus deinem Nachsegmentieren), zur Kontrolle `pruefen`. Eigene Skripte als Datei in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r1c1/v3`.

## Ergebnis in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r1c1/v3` (genau diese Namen)

- `roh.jpg`, `umriss.jpg` (alle Segmentgrenzen mit ID), `maengel.jpg` (nummerierte Punkte mit kurzer
  deutscher Beschriftung, sonst Vermerk „keine Mängel“), `vorschlag.jpg` (Grenzen und Klassen, wie
  du sie setzen würdest, sonst Vermerk „unverändert“): je dein Viertel mit Umgebung, Viertel
  umrandet (Grundlage: die vorbereiteten Übersichtsbilder).
- `nah_<n>.jpg`: eigene Nahansichten von Stellen, die man in den vorbereiteten Bildern nicht beurteilen kann,
  je ein Teil des Viertels samt Nachbarn (mindestens 64 × 64 Bildpunkte der Teilkachel, kein freigestelltes
  Einzelsegment); `kontrast_<n>.jpg` bei blassen Stellen.
- `urteil.json` (UTF-8):

```
{"teilkachel": "r1c1", "viertel": "v3", "bearbeiter": "urt-c-r1c1-v3",
 "bilder_angesehen": {"uebersicht": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r1c1/ganz_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c1/v3/uebersicht_nummern.jpg", "…"],
                      "nah": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c1/v3/nah1_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r1c1/v3/nah_1.jpg", "…"]},
 "segmente": [{"id": 17, "klasse_heute": "Code", "was_ist_es": "ein Satz",
               "urteil": "sauber" | "nicht_sauber", "klasse_vorschlag": "Code oder null",
               "sicher": true | false,
               "punkte": [{"nr": 1, "art": "fremdes|fehlt|trennen|verschmelzen|grenze|klasse|zu_klein|sonstiges",
                           "text": "ein Satz mit Stelle (x/y im Teilkachelbild)", "flaeche_px": Zahl oder null}],
               "bilder": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c1/v3/uebersicht_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c1/v3/nah2_roh.jpg"]}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "was an der Kerngrenze nicht passt"}],
 "unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."],
 "eingriffe": [{"schritt": "teilen", "vorher": [ID], "nachher": [ID, ID], "grund": "ein Satz"}]}
```

Jedes Segment deiner Liste steht genau einmal unter `segmente`, auch die sauberen, in der Reihenfolge der Liste. Segmente der Nachbarviertel (graue Nummern) und des Kontextrands (ohne Nummer) urteilst du in diesem Auftrag nicht; Auffälliges an ihnen nennst du unter `unsicher` mit ID.

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Punkte, Anteil `sicher: false`, wo du unsicher bist.
