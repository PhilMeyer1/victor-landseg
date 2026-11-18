# Auftrag: H0, Teilkachel r1c1, Viertel v3: 67 Segmente im Verbund ansehen und einzeln urteilen (Fassung C „Feste Kategorienliste“)

Lies zuerst den Skill `landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `r1c1` des Ausschnitts in `C:/Users/Phil/Developement/Victor/daten/landseg/H0`. Du urteilst über jedes
Segment deines Viertels v3 (Liste unter „Dein Viertel“), ob Grenze und Klasse stimmen, und zeichnest ein, was
du ändern würdest. Die Label-Karte änderst du nicht.

## Daten (eingefrorener Stand, nur lesen)

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
- Die Klassen der Vorstufe sind auf dem Scan schwach (SAM 3 ist für Farb-Orthofotos gebaut; über
  90 % `sicher: nein`, Äcker teils als Gebäude): nur Hinweis.
- Die Vorstufe lief mit kleinerem SAM-3-Fenster (420 Bildpunkte, Schiebefenster) und niedriger
  Instanzschwelle (`C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-2/vorstufe-h0.json`), damit die Streckhöfe einzeln erscheinen. Gerade Grenzen
  mitten in einer gleichförmigen Fläche (etwa bei x 208 oder 420 im Teilkachelbild) können vom
  Schiebefenster stammen: dann ist es keine Bildkante.

## Dein Viertel

Viertel v3 (unten links) des Kerns von `r1c1`: x 64–313, y 314–563 im
Teilkachelbild (250 × 250 Bildpunkte). Dir gehören die 67 Segmente der Liste unten: Jedes hat den
größten Teil seiner Kernfläche in diesem Viertel. Die Teilkachel hat 518 Kernsegmente
(v1 131, v2 147, v3 67, v4 173); die anderen Viertel stehen in eigenen Aufträgen mit eigenem Ergebnisordner. Ein Segment
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
| 418 | 400418 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 159 | 100 % | – | 215/343 | grenze_ohne_bildkante, klasse_unsicher |
| 379 | 400379 | 6.6 Weg, unbefestigt (Feld-, Wald-, Schotterweg) | nein | nein | 2142 | 92 % | v1 | 217/324 | klasse_unsicher |
| 416 | 400416 | 1.3.2 Baustelle | nein | nein | 129 | 100 % | – | 239/341 | klasse_unsicher, nicht_zusammenhaengend |
| 396 | 400396 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 437 | 98 % | v1 | 247/324 | klasse_unsicher |
| 397 | 400397 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 432 | 96 % | v1 | 266/325 | klasse_unsicher |
| 392 | 400392 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 280 | 80 % | v1 | 282/319 | klasse_unsicher, nicht_zusammenhaengend |
| 402 | 400402 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 294 | 100 % | – | 296/326 | klasse_unsicher |
| 403 | 400403 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 612 | 97 % | v4 | 302/337 | klasse_unsicher |
| 290 | 400290 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | ja | nein | 15814 | 74 % | v1 | 125/361 | grenze_ohne_bildkante |
| 414 | 400414 | 1.2.1 Straße (versiegelt) | nein | nein | 349 | 100 % | – | 206/355 | grenze_ohne_bildkante, klasse_unsicher |
| 444 | 400444 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 179 | 100 % | – | 217/361 | grenze_ohne_bildkante, klasse_unsicher |
| 431 | 400431 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 216 | 100 % | – | 219/351 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 459 | 400459 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 218 | 100 % | – | 225/375 | grenze_ohne_bildkante, klasse_unsicher |
| 455 | 400455 | 1.3.2 Baustelle | nein | nein | 84 | 100 % | – | 234/372 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 481 | 400481 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 192 | 100 % | – | 235/392 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 469 | 400469 | 1.2.1 Straße (versiegelt) | ja | nein | 131 | 100 % | – | 241/378 | grenze_ohne_bildkante |
| 426 | 400426 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 868 | 100 % | – | 262/351 | klasse_unsicher |
| 463 | 400463 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 399 | 100 % | – | 267/376 | grenze_ohne_bildkante, klasse_unsicher |
| 449 | 400449 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 133 | 100 % | – | 277/366 | klasse_unsicher |
| 468 | 400468 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 184 | 100 % | – | 281/380 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 419 | 400419 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 374 | 100 % | – | 285/357 | klasse_unsicher |
| 477 | 400477 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 97 | 100 % | – | 289/385 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 484 | 400484 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 444 | 100 % | – | 292/397 | klasse_unsicher |
| 430 | 400430 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 113 | 100 % | – | 304/351 | klasse_unsicher, nicht_zusammenhaengend |
| 440 | 400440 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 529 | 88 % | v4 | 305/365 | klasse_unsicher |
| 470 | 400470 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 122 | 100 % | – | 305/386 | klasse_unsicher, nicht_zusammenhaengend |
| 446 | 400446 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 2632 | 100 % | – | 163/415 | grenze_ohne_bildkante, klasse_unsicher |
| 457 | 400457 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 1185 | 100 % | – | 217/406 | grenze_ohne_bildkante, klasse_unsicher |
| 490 | 400490 | 1.3.4 Sport-, Spielplatz (künstlicher Belag) | nein | nein | 276 | 100 % | – | 245/413 | grenze_ohne_bildkante, klasse_unsicher |
| 511 | 400511 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 93 | 100 % | – | 259/423 | klasse_unsicher, nicht_zusammenhaengend |
| 541 | 400541 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 165 | 100 % | – | 263/446 | klasse_unsicher |
| 523 | 400523 | 1.2.1 Straße (versiegelt) | nein | nein | 345 | 100 % | – | 274/433 | klasse_unsicher, nicht_zusammenhaengend |
| 487 | 400487 | 1.3.2 Baustelle | nein | nein | 315 | 100 % | – | 277/412 | klasse_unsicher, nicht_zusammenhaengend |
| 503 | 400503 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 93 | 100 % | – | 288/414 | klasse_unsicher |
| 530 | 400530 | 1.3.2 Baustelle | nein | nein | 121 | 100 % | – | 293/443 | klasse_unsicher, nicht_zusammenhaengend |
| 512 | 400512 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 374 | 100 % | – | 294/426 | klasse_unsicher |
| 488 | 400488 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 466 | 82 % | v4 | 305/405 | klasse_unsicher |
| 533 | 400533 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 132 | 100 % | – | 305/435 | klasse_unsicher |
| 500 | 400500 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 153 | 52 % | v4 | 310/416 | klasse_unsicher |
| 513 | 400513 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 218 | 67 % | v4 | 310/428 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 509 | 400509 | 3.1 Wiese / Weide (gemeinsam) | nein | nein | 9724 | 100 % | – | 95/452 | grenze_ohne_bildkante, klasse_unsicher |
| 510 | 400510 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 5807 | 100 % | – | 223/480 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 583 | 400583 | 1.2.1 Straße (versiegelt) | nein | nein | 336 | 100 % | – | 246/497 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 561 | 400561 | 1.2.1 Straße (versiegelt) | nein | nein | 149 | 100 % | – | 247/471 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 566 | 400566 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 290 | 100 % | – | 272/483 | klasse_unsicher |
| 589 | 400589 | 4.2.4 Gebüsch / Strauchfläche | nein | ja | 82 | 100 % | – | 282/498 | klasse_unsicher |
| 543 | 400543 | 6.6 Weg, unbefestigt (Feld-, Wald-, Schotterweg) | nein | nein | 1513 | 50 % | v4 | 296/457 | klasse_unsicher, nicht_zusammenhaengend |
| 579 | 400579 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 505 | 86 % | v4 | 305/493 | klasse_unsicher |
| 622 | 400622 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | nein | 237 | 100 % | – | 68/545 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 498 | 400498 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 9824 | 100 % | – | 167/507 | grenze_ohne_bildkante, klasse_unsicher |
| 623 | 400623 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 106 | 100 % | – | 219/536 | grenze_ohne_bildkante, klasse_unsicher |
| 603 | 400603 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 119 | 100 % | – | 233/513 | grenze_ohne_bildkante, klasse_unsicher |
| 632 | 400632 | 1.2.1 Straße (versiegelt) | nein | nein | 134 | 100 % | – | 234/546 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 630 | 400630 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 745 | 100 % | – | 247/548 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 619 | 400619 | 1.2.1 Straße (versiegelt) | nein | nein | 121 | 100 % | – | 248/535 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 597 | 400597 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 136 | 100 % | – | 257/507 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 608 | 400608 | 1.2.1 Straße (versiegelt) | nein | nein | 330 | 100 % | – | 259/520 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 620 | 400620 | 1.2.1 Straße (versiegelt) | nein | nein | 326 | 100 % | – | 260/534 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 598 | 400598 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 153 | 100 % | – | 269/509 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 611 | 400611 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | ja | ja | 149 | 100 % | – | 281/522 | grenze_ohne_bildkante |
| 621 | 400621 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 405 | 100 % | – | 285/543 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 635 | 400635 | 4.2.4 Gebüsch / Strauchfläche | nein | ja | 180 | 100 % | – | 299/546 | klasse_unsicher |
| 516 | 400516 | 1.3.2 Baustelle | nein | nein | 3203 | 92 % | v4 | 301/531 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 599 | 400599 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 191 | 86 % | v4 | 303/510 | klasse_unsicher, nicht_zusammenhaengend |
| 643 | 400643 | 1.2.1 Straße (versiegelt) | nein | nein | 143 | 100 % | – | 222/557 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 645 | 400645 | 1.2.1 Straße (versiegelt) | nein | nein | 145 | 100 % | – | 257/558 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 651 | 400651 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 46 | 100 % | – | 281/561 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |

`nicht_geprueft` nennt, was du nicht angesehen hast, `offen`, was du nicht entscheiden konntest.

Kontrolle vor der Rückgabe (muss mit `ok` enden):

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-2/skripte/pruefe_urteil.py --urteil C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r1c1/v3/urteil.json --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r1c1/segmente.json --fassung c --viertel v3 --ids 400418,400379,400416,400396,400397,400392,400402,400403,400290,400414,400444,400431,400459,400455,400481,400469,400426,400463,400449,400468,400419,400477,400484,400430,400440,400470,400446,400457,400490,400511,400541,400523,400487,400503,400530,400512,400488,400533,400500,400513,400509,400510,400583,400561,400566,400589,400543,400579,400622,400498,400623,400603,400632,400630,400619,400597,400608,400620,400598,400611,400621,400635,400516,400599,400643,400645,400651 --kategorien C:/Users/Phil/Developement/Victor/landseg/kategorien.json
```

## Werkzeuge

Befehle im Ordner `C:/Users/Phil/Developement/Victor/landseg` mit `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -m landseg <befehl>`; Aufruf und Schalter stehen in
`C:/Users/Phil/Developement/Victor/landseg/README.md`. Die Bilder deines Viertels liegen fertig vor (Abschnitt „Dein Viertel“); `ansicht` (W3) erzeugt Bilder
je Segment und ist hier keine Urteilsgrundlage. Für fragliche Grenzen `kante` (W4, hier nur zum Ansehen
der Bildkante), zur Kontrolle `pruefen`. Eigene Skripte als Datei in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r1c1/v3`.

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
 "unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."]}
```

Jedes Segment deiner Liste steht genau einmal unter `segmente`, auch die sauberen, in der Reihenfolge der Liste. Segmente der Nachbarviertel (graue Nummern) und des Kontextrands (ohne Nummer) urteilst du in diesem Auftrag nicht; Auffälliges an ihnen nennst du unter `unsicher` mit ID.

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Punkte, Anteil `sicher: false`, wo du unsicher bist.
