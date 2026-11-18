# Auftrag: H0, Teilkachel r1c1, Viertel v4: 173 Segmente im Verbund ansehen und einzeln urteilen (Fassung B „Kategorien frei“)

Lies zuerst den Skill `landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `r1c1` des Ausschnitts in `C:/Users/Phil/Developement/Victor/daten/landseg/H0`. Du urteilst über jedes
Segment deines Viertels v4 (Liste unter „Dein Viertel“), ob Grenze und Klasse stimmen, und zeichnest ein, was
du ändern würdest. Die Label-Karte änderst du nicht.

## Daten (eingefrorener Stand, nur lesen)

- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/manifest.json`: Eintrag `r1c1` unter `teilkacheln` mit `bild` (Teilkachelbild,
  Kern + Kontextrand), `kern_im_bild` (Lage des Kerns im Teilkachelbild) und `kern` (Lage im Ausschnitt).
- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r1c1/labels.tif`: Label-Karte (Segment-ID je Bildpunkt, Größe des Teilkachelbilds).
- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r1c1/segmente.json`: je Segment `id`, `klasse`, `grob`, `herkunft`, `sicher`; dazu die
  Kandidatenliste der Vorstufe, falls vorhanden.
- `C:/Users/Phil/Developement/Victor/landseg/kategorien.json` und `C:/Users/Phil/Developement/Victor/landseg/KATEGORIEN.md`: nur Anregung; in Fassung B benennst du die Klassen selbst (Abschnitt „Fassung B“).

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

Viertel v4 (unten rechts) des Kerns von `r1c1`: x 314–563, y 314–563 im
Teilkachelbild (250 × 250 Bildpunkte). Dir gehören die 173 Segmente der Liste unten: Jedes hat den
größten Teil seiner Kernfläche in diesem Viertel. Die Teilkachel hat 518 Kernsegmente
(v1 131, v2 147, v3 67, v4 173); die anderen Viertel stehen in eigenen Aufträgen mit eigenem Ergebnisordner. Ein Segment
über einer Viertelgrenze urteilt nur das Viertel mit dem größten Anteil; in den Bildern der Nachbarn ist
es mit grauer Nummer als Umgebung zu sehen.

Urteil im Verbund: Du siehst das Viertel als zusammenhängendes Bild mit Umgebung, arbeitest die Liste der
Reihe nach ab und beurteilst jedes Segment im Zusammenhang mit seinen Nachbarn; eingetragen wird jedes
Segment einzeln (Klasse, `sicher`, `was_ist_es` als Notiz). Bilder freigestellter Einzelsegmente gibt es
nicht, und sie sind keine Urteilsgrundlage.

Bilder des Viertels (fertig, JPEG, in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c1/v4`, Fenster und Vergrößerung je Bild in `viertel.json`):

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
Teilkachelbild; Kandidaten aus `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r1c1/kandidaten.json`, dort mit Grund, in den
Bildern nicht eingezeichnet; Anteil hier = Anteil der Kernfläche in diesem Viertel):

| Nr | ID | Klasse Vorstufe | sicher | im Siedlungsgebiet | Kernfläche px | Anteil hier | auch in | Punkt x/y | Kandidaten |
|---|---|---|---|---|---|---|---|---|---|
| 399 | 400399 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 169 | 100 % | – | 329/321 | klasse_unsicher, nicht_zusammenhaengend |
| 411 | 400411 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 325 | 100 % | – | 330/337 | grenze_ohne_bildkante, klasse_unsicher |
| 406 | 400406 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 165 | 100 % | – | 341/329 | grenze_ohne_bildkante, klasse_unsicher |
| 405 | 400405 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 385 | 100 % | – | 352/331 | klasse_unsicher |
| 415 | 400415 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 387 | 100 % | – | 363/341 | klasse_unsicher |
| 390 | 400390 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 223 | 62 % | v2 | 365/318 | klasse_unsicher |
| 400 | 400400 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 229 | 100 % | – | 372/323 | klasse_unsicher |
| 422 | 400422 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 114 | 100 % | – | 375/346 | grenze_ohne_bildkante, klasse_unsicher |
| 381 | 400381 | 1.3.2 Baustelle | nein | nein | 169 | 54 % | v2 | 387/319 | klasse_unsicher, nicht_zusammenhaengend |
| 401 | 400401 | 4.2.4 Gebüsch / Strauchfläche | nein | ja | 236 | 100 % | – | 388/329 | klasse_unsicher |
| 407 | 400407 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 233 | 100 % | – | 425/346 | klasse_unsicher |
| 389 | 400389 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1281 | 90 % | v2 | 461/326 | klasse_unsicher, nicht_zusammenhaengend |
| 408 | 400408 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 322 | 100 % | – | 480/332 | klasse_unsicher |
| 417 | 400417 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 80 | 100 % | – | 498/336 | klasse_unsicher |
| 393 | 400393 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 207 | 75 % | v2 | 502/319 | grenze_ohne_bildkante, klasse_unsicher |
| 404 | 400404 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 368 | 100 % | – | 508/330 | klasse_unsicher, nicht_zusammenhaengend |
| 394 | 400394 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 719 | 97 % | v2 | 532/331 | klasse_unsicher |
| 385 | 400385 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 641 | 62 % | v2 | 548/321 | grenze_ohne_bildkante, klasse_unsicher |
| 420 | 400420 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 191 | 100 % | – | 548/338 | klasse_unsicher |
| 427 | 400427 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 17 | 100 % | – | 562/347 | grenze_ohne_bildkante, klasse_unsicher, zu_klein |
| 409 | 400409 | 1.3.2 Baustelle | nein | nein | 1 | 100 % | – | 563/341 | grenze_ohne_bildkante, klasse_unsicher |
| 433 | 400433 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 118 | 63 % | v3 | 317/351 | klasse_unsicher |
| 472 | 400472 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 279 | 96 % | v3 | 325/385 | klasse_unsicher |
| 451 | 400451 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 391 | 80 % | v3 | 331/376 | klasse_unsicher |
| 439 | 400439 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 122 | 100 % | – | 332/357 | klasse_unsicher, nicht_zusammenhaengend |
| 425 | 400425 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 573 | 100 % | – | 347/354 | grenze_ohne_bildkante, klasse_unsicher |
| 450 | 400450 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 138 | 100 % | – | 350/370 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 492 | 400492 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 73 | 100 % | – | 365/396 | klasse_unsicher, nicht_zusammenhaengend |
| 436 | 400436 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 300 | 100 % | – | 369/355 | grenze_ohne_bildkante, klasse_unsicher |
| 453 | 400453 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 1038 | 100 % | – | 371/373 | grenze_ohne_bildkante, klasse_unsicher |
| 493 | 400493 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 97 | 100 % | – | 380/399 | klasse_unsicher, nicht_zusammenhaengend |
| 464 | 400464 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 629 | 100 % | – | 389/384 | klasse_unsicher |
| 441 | 400441 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 196 | 100 % | – | 390/363 | klasse_unsicher |
| 424 | 400424 | 1.3.2 Baustelle | nein | nein | 358 | 100 % | – | 392/351 | klasse_unsicher, nicht_zusammenhaengend |
| 465 | 400465 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 151 | 100 % | – | 401/378 | klasse_unsicher |
| 489 | 400489 | 4.2.4 Gebüsch / Strauchfläche | nein | ja | 193 | 100 % | – | 406/398 | klasse_unsicher |
| 341 | 400341 | 6.6 Weg, unbefestigt (Feld-, Wald-, Schotterweg) | nein | nein | 3333 | 73 % | v2 | 413/358 | klasse_unsicher |
| 466 | 400466 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 86 | 100 % | – | 432/374 | klasse_unsicher, nicht_zusammenhaengend |
| 462 | 400462 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 476 | 100 % | – | 444/379 | grenze_ohne_bildkante, klasse_unsicher |
| 475 | 400475 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 1011 | 100 % | – | 445/399 | klasse_unsicher |
| 423 | 400423 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 1074 | 100 % | – | 454/350 | klasse_unsicher |
| 447 | 400447 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 87 | 100 % | – | 460/364 | klasse_unsicher |
| 473 | 400473 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 97 | 100 % | – | 464/380 | klasse_unsicher |
| 432 | 400432 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 570 | 100 % | – | 478/360 | grenze_ohne_bildkante, klasse_unsicher |
| 460 | 400460 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 142 | 100 % | – | 479/374 | klasse_unsicher |
| 486 | 400486 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 118 | 100 % | – | 479/395 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 474 | 400474 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 252 | 100 % | – | 490/382 | klasse_unsicher |
| 442 | 400442 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 102 | 100 % | – | 493/362 | klasse_unsicher |
| 434 | 400434 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 118 | 100 % | – | 498/353 | klasse_unsicher |
| 445 | 400445 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 895 | 100 % | – | 508/384 | grenze_ohne_bildkante, klasse_unsicher |
| 437 | 400437 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 237 | 100 % | – | 511/368 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 435 | 400435 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 138 | 100 % | – | 517/354 | klasse_unsicher |
| 452 | 400452 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 24 | 100 % | – | 541/361 | klasse_unsicher, zu_klein |
| 454 | 400454 | 4.2.1 Einzelbaum | nein | ja | 263 | 100 % | – | 541/370 | klasse_unsicher |
| 458 | 400458 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 110 | 100 % | – | 544/384 | grenze_ohne_bildkante, klasse_unsicher |
| 476 | 400476 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 612 | 100 % | – | 544/396 | grenze_ohne_bildkante, klasse_unsicher |
| 438 | 400438 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 104 | 100 % | – | 555/355 | grenze_ohne_bildkante, klasse_unsicher |
| 448 | 400448 | 2.1 Acker mit Bewuchs | nein | ja | 130 | 100 % | – | 557/364 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 479 | 400479 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 235 | 100 % | – | 557/390 | grenze_ohne_bildkante, klasse_unsicher |
| 467 | 400467 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 156 | 100 % | – | 558/374 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 412 | 400412 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 67 | 100 % | – | 561/355 | grenze_ohne_bildkante, klasse_unsicher |
| 535 | 400535 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 360 | 80 % | v3 | 321/449 | grenze_ohne_bildkante, klasse_unsicher |
| 519 | 400519 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 179 | 100 % | – | 324/426 | grenze_ohne_bildkante, klasse_unsicher |
| 471 | 400471 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 255 | 100 % | – | 325/400 | klasse_unsicher, nicht_zusammenhaengend |
| 534 | 400534 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 181 | 100 % | – | 329/436 | grenze_ohne_bildkante, klasse_unsicher |
| 491 | 400491 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 530 | 100 % | – | 338/408 | grenze_ohne_bildkante, klasse_unsicher |
| 531 | 400531 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 124 | 100 % | – | 346/436 | klasse_unsicher |
| 544 | 400544 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 151 | 100 % | – | 347/445 | klasse_unsicher |
| 514 | 400514 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 354 | 100 % | – | 352/421 | grenze_ohne_bildkante, klasse_unsicher |
| 496 | 400496 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 292 | 100 % | – | 355/408 | grenze_ohne_bildkante, klasse_unsicher |
| 538 | 400538 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 409 | 100 % | – | 366/446 | klasse_unsicher |
| 515 | 400515 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 459 | 100 % | – | 368/426 | grenze_ohne_bildkante, klasse_unsicher |
| 547 | 400547 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 75 | 100 % | – | 381/446 | klasse_unsicher |
| 494 | 400494 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 596 | 100 % | – | 386/409 | grenze_ohne_bildkante, klasse_unsicher |
| 528 | 400528 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 530 | 100 % | – | 387/437 | klasse_unsicher |
| 504 | 400504 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 235 | 100 % | – | 396/420 | klasse_unsicher |
| 521 | 400521 | 1.3.2 Baustelle | nein | nein | 197 | 100 % | – | 397/431 | klasse_unsicher, nicht_zusammenhaengend |
| 499 | 400499 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 164 | 100 % | – | 409/416 | klasse_unsicher |
| 532 | 400532 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 216 | 100 % | – | 410/434 | klasse_unsicher |
| 508 | 400508 | 1.2.1 Straße (versiegelt) | nein | nein | 313 | 100 % | – | 425/426 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 537 | 400537 | 1.2.1 Straße (versiegelt) | ja | nein | 326 | 100 % | – | 428/443 | grenze_ohne_bildkante |
| 527 | 400527 | 1.2.1 Straße (versiegelt) | ja | nein | 202 | 100 % | – | 441/434 | grenze_ohne_bildkante |
| 495 | 400495 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 882 | 100 % | – | 473/410 | grenze_ohne_bildkante, klasse_unsicher |
| 524 | 400524 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1067 | 100 % | – | 490/440 | klasse_unsicher |
| 507 | 400507 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 183 | 100 % | – | 497/420 | klasse_unsicher |
| 545 | 400545 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 325 | 100 % | – | 510/447 | klasse_unsicher, nicht_zusammenhaengend |
| 529 | 400529 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 114 | 100 % | – | 515/430 | klasse_unsicher |
| 485 | 400485 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1505 | 100 % | – | 521/413 | klasse_unsicher, nicht_zusammenhaengend |
| 497 | 400497 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 251 | 100 % | – | 550/413 | klasse_unsicher |
| 540 | 400540 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 190 | 100 % | – | 550/444 | klasse_unsicher |
| 505 | 400505 | 1.2.1 Straße (versiegelt) | nein | nein | 999 | 100 % | – | 555/427 | grenze_ohne_bildkante, klasse_unsicher |
| 542 | 400542 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 94 | 100 % | – | 560/446 | klasse_unsicher |
| 482 | 400482 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 46 | 100 % | – | 561/406 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 552 | 400552 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 144 | 57 % | v3 | 318/462 | klasse_unsicher |
| 575 | 400575 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 222 | 94 % | v3 | 329/489 | klasse_unsicher |
| 536 | 400536 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 314 | 100 % | – | 336/453 | grenze_ohne_bildkante, klasse_unsicher |
| 557 | 400557 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 143 | 100 % | – | 336/466 | klasse_unsicher, nicht_zusammenhaengend |
| 558 | 400558 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 224 | 100 % | – | 350/466 | klasse_unsicher |
| 569 | 400569 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 248 | 100 % | – | 357/479 | klasse_unsicher |
| 572 | 400572 | 1.3.2 Baustelle | nein | nein | 211 | 100 % | – | 375/480 | klasse_unsicher, nicht_zusammenhaengend |
| 551 | 400551 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 512 | 100 % | – | 379/457 | klasse_unsicher |
| 578 | 400578 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 238 | 100 % | – | 379/489 | klasse_unsicher |
| 562 | 400562 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 352 | 100 % | – | 380/469 | klasse_unsicher |
| 568 | 400568 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 506 | 100 % | – | 402/479 | grenze_ohne_bildkante, klasse_unsicher |
| 550 | 400550 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 375 | 100 % | – | 404/466 | grenze_ohne_bildkante, klasse_unsicher |
| 548 | 400548 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 526 | 100 % | – | 419/459 | grenze_ohne_bildkante, klasse_unsicher |
| 570 | 400570 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | ja | nein | 335 | 100 % | – | 419/476 | grenze_ohne_bildkante |
| 574 | 400574 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 209 | 100 % | – | 425/487 | klasse_unsicher |
| 556 | 400556 | 1.2.1 Straße (versiegelt) | ja | nein | 211 | 100 % | – | 437/466 | – |
| 564 | 400564 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 250 | 100 % | – | 446/487 | klasse_unsicher |
| 517 | 400517 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 914 | 100 % | – | 447/450 | klasse_unsicher |
| 576 | 400576 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 286 | 100 % | – | 458/489 | klasse_unsicher |
| 560 | 400560 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 599 | 100 % | – | 466/472 | klasse_unsicher |
| 553 | 400553 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 241 | 100 % | – | 484/458 | klasse_unsicher |
| 563 | 400563 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 311 | 100 % | – | 496/475 | klasse_unsicher |
| 554 | 400554 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 304 | 100 % | – | 512/464 | klasse_unsicher |
| 565 | 400565 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 300 | 100 % | – | 516/475 | klasse_unsicher, nicht_zusammenhaengend |
| 571 | 400571 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 1169 | 100 % | – | 530/482 | klasse_unsicher |
| 588 | 400588 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 130 | 100 % | – | 530/497 | klasse_unsicher, nicht_zusammenhaengend |
| 539 | 400539 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 660 | 100 % | – | 538/455 | klasse_unsicher |
| 567 | 400567 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 117 | 100 % | – | 538/469 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 577 | 400577 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 507 | 100 % | – | 550/494 | klasse_unsicher |
| 555 | 400555 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 380 | 100 % | – | 558/458 | grenze_ohne_bildkante, klasse_unsicher |
| 582 | 400582 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 9 | 100 % | – | 560/489 | klasse_unsicher |
| 549 | 400549 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 27 | 100 % | – | 561/470 | klasse_unsicher |
| 606 | 400606 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 273 | 74 % | v3 | 321/515 | klasse_unsicher |
| 624 | 400624 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 489 | 100 % | – | 329/545 | klasse_unsicher |
| 586 | 400586 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 406 | 91 % | v3 | 331/500 | klasse_unsicher |
| 600 | 400600 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 571 | 100 % | – | 345/513 | klasse_unsicher |
| 615 | 400615 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 986 | 100 % | – | 356/542 | klasse_unsicher |
| 590 | 400590 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 660 | 100 % | – | 358/520 | klasse_unsicher, nicht_zusammenhaengend |
| 601 | 400601 | 4.2.4 Gebüsch / Strauchfläche | nein | ja | 212 | 100 % | – | 365/507 | klasse_unsicher |
| 610 | 400610 | 4.2.4 Gebüsch / Strauchfläche | nein | ja | 142 | 100 % | – | 379/524 | klasse_unsicher |
| 594 | 400594 | 6.6 Weg, unbefestigt (Feld-, Wald-, Schotterweg) | nein | nein | 688 | 100 % | – | 387/512 | klasse_unsicher, nicht_zusammenhaengend |
| 616 | 400616 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 137 | 100 % | – | 389/535 | klasse_unsicher, nicht_zusammenhaengend |
| 625 | 400625 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 105 | 100 % | – | 389/545 | nicht_zusammenhaengend |
| 591 | 400591 | 1.3.2 Baustelle | nein | nein | 177 | 100 % | – | 399/508 | klasse_unsicher, nicht_zusammenhaengend |
| 612 | 400612 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 337 | 100 % | – | 402/539 | klasse_unsicher |
| 581 | 400581 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 326 | 100 % | – | 410/511 | klasse_unsicher |
| 584 | 400584 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 294 | 100 % | – | 416/501 | klasse_unsicher |
| 626 | 400626 | 1.3.2 Baustelle | nein | nein | 161 | 100 % | – | 425/540 | klasse_unsicher |
| 585 | 400585 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 2844 | 100 % | – | 441/522 | klasse_unsicher |
| 573 | 400573 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 804 | 100 % | – | 471/500 | klasse_unsicher |
| 617 | 400617 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 478 | 100 % | – | 475/541 | klasse_unsicher |
| 609 | 400609 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 158 | 100 % | – | 480/526 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 618 | 400618 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 105 | 100 % | – | 485/538 | klasse_unsicher, nicht_zusammenhaengend |
| 604 | 400604 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 228 | 100 % | – | 493/520 | grenze_ohne_bildkante, klasse_unsicher |
| 629 | 400629 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 122 | 100 % | – | 494/547 | klasse_unsicher |
| 607 | 400607 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 592 | 100 % | – | 509/527 | klasse_unsicher |
| 596 | 400596 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 640 | 100 % | – | 510/506 | klasse_unsicher, nicht_zusammenhaengend |
| 595 | 400595 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 343 | 100 % | – | 525/513 | klasse_unsicher |
| 602 | 400602 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 186 | 100 % | – | 543/510 | klasse_unsicher |
| 592 | 400592 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1064 | 100 % | – | 549/529 | klasse_unsicher |
| 613 | 400613 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 84 | 100 % | – | 560/545 | klasse_unsicher |
| 639 | 400639 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 158 | 100 % | – | 341/559 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 652 | 400652 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 36 | 100 % | – | 359/561 | klasse_unsicher |
| 633 | 400633 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 328 | 100 % | – | 372/554 | klasse_unsicher |
| 646 | 400646 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 83 | 100 % | – | 381/559 | nicht_zusammenhaengend |
| 631 | 400631 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 109 | 100 % | – | 391/556 | klasse_unsicher, nicht_zusammenhaengend |
| 637 | 400637 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 344 | 100 % | – | 403/555 | grenze_ohne_bildkante, klasse_unsicher |
| 653 | 400653 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 19 | 100 % | – | 415/562 | klasse_unsicher |
| 636 | 400636 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 174 | 100 % | – | 418/550 | klasse_unsicher |
| 649 | 400649 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 66 | 100 % | – | 424/560 | grenze_ohne_bildkante, klasse_unsicher |
| 634 | 400634 | 1.2.1 Straße (versiegelt) | nein | nein | 164 | 100 % | – | 435/551 | klasse_unsicher |
| 650 | 400650 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 64 | 100 % | – | 436/561 | grenze_ohne_bildkante, klasse_unsicher |
| 642 | 400642 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 80 | 100 % | – | 445/556 | klasse_unsicher |
| 647 | 400647 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 77 | 100 % | – | 509/560 | klasse_unsicher |
| 638 | 400638 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 270 | 100 % | – | 518/557 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 627 | 400627 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 533 | 100 % | – | 532/550 | grenze_ohne_bildkante, klasse_unsicher |
| 644 | 400644 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 150 | 100 % | – | 546/559 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 654 | 400654 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 14 | 100 % | – | 557/562 | klasse_unsicher |
| 605 | 400605 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 125 | 100 % | – | 560/556 | klasse_unsicher |
| 614 | 400614 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 3 | 100 % | – | 563/562 | klasse_unsicher |

`nicht_geprueft` nennt, was du nicht angesehen hast, `offen`, was du nicht entscheiden konntest.

Kontrolle vor der Rückgabe (muss mit `ok` enden):

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-2/skripte/pruefe_urteil.py --urteil C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c1/v4/urteil.json --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r1c1/segmente.json --fassung b --viertel v4 --ids 400399,400411,400406,400405,400415,400390,400400,400422,400381,400401,400407,400389,400408,400417,400393,400404,400394,400385,400420,400427,400409,400433,400472,400451,400439,400425,400450,400492,400436,400453,400493,400464,400441,400424,400465,400489,400341,400466,400462,400475,400423,400447,400473,400432,400460,400486,400474,400442,400434,400445,400437,400435,400452,400454,400458,400476,400438,400448,400479,400467,400412,400535,400519,400471,400534,400491,400531,400544,400514,400496,400538,400515,400547,400494,400528,400504,400521,400499,400532,400508,400537,400527,400495,400524,400507,400545,400529,400485,400497,400540,400505,400542,400482,400552,400575,400536,400557,400558,400569,400572,400551,400578,400562,400568,400550,400548,400570,400574,400556,400564,400517,400576,400560,400553,400563,400554,400565,400571,400588,400539,400567,400577,400555,400582,400549,400606,400624,400586,400600,400615,400590,400601,400610,400594,400616,400625,400591,400612,400581,400584,400626,400585,400573,400617,400609,400618,400604,400629,400607,400596,400595,400602,400592,400613,400639,400652,400633,400646,400631,400637,400653,400636,400649,400634,400650,400642,400647,400638,400627,400644,400654,400605,400614
```

## Fassung B: Kategorien frei

Dieses Viertel gehört zu Fassung B, einem Vergleichsmuster ohne feste Kategorienliste. Abweichend von
Regel L3 des Skills wählst du die Klassen nicht aus `kategorien.json`, sondern benennst jede Fläche
selbst, gestuft in drei Ebenen unter `klasse_frei`: `grob` (wenige Oberklassen für die ganze
Landschaft), `mittel` und `fein` (so fein, wie im Bild sicher erkennbar: Einzelbaum, schmaler Weg,
kleines Gebäude; sonst wiederholt `fein` die mittlere Ebene). Kurze deutsche Namen, gleiche Dinge
gleich benannt, geordnet nach dem, was in der Draufsicht zu sehen ist. `klasse_heute` ist der Code
der Vorstufe und nur ein Hinweis (auch die Farben in `uebersicht_vorschlag.jpg` folgen der festen
Liste und binden dich nicht); `klasse_vorschlag` bleibt `null`. Unter `klassen_frei` stehen alle
Namen, die du benutzt hast, je mit Ebene, Eltern und einem Satz Bildmerkmal. Nach allen Teilkacheln
gleicht ein eigener Agent die Namen der 16 Viertel zu einer Liste an. Alle übrigen Regeln (L1, L2,
L4–L13) gelten wie in Fassung C; jeder Bildpunkt gehört genau einem Segment.

## Werkzeuge

Befehle im Ordner `C:/Users/Phil/Developement/Victor/landseg` mit `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -m landseg <befehl>`; Aufruf und Schalter stehen in
`C:/Users/Phil/Developement/Victor/landseg/README.md`. Die Bilder deines Viertels liegen fertig vor (Abschnitt „Dein Viertel“); `ansicht` (W3) erzeugt Bilder
je Segment und ist hier keine Urteilsgrundlage. Für fragliche Grenzen `kante` (W4, hier nur zum Ansehen
der Bildkante), zur Kontrolle `pruefen`. Eigene Skripte als Datei in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c1/v4`.

## Ergebnis in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c1/v4` (genau diese Namen)

- `roh.jpg`, `umriss.jpg` (alle Segmentgrenzen mit ID), `maengel.jpg` (nummerierte Punkte mit kurzer
  deutscher Beschriftung, sonst Vermerk „keine Mängel“), `vorschlag.jpg` (Grenzen und Klassen, wie
  du sie setzen würdest, sonst Vermerk „unverändert“): je dein Viertel mit Umgebung, Viertel
  umrandet (Grundlage: die vorbereiteten Übersichtsbilder).
- `nah_<n>.jpg`: eigene Nahansichten von Stellen, die man in den vorbereiteten Bildern nicht beurteilen kann,
  je ein Teil des Viertels samt Nachbarn (mindestens 64 × 64 Bildpunkte der Teilkachel, kein freigestelltes
  Einzelsegment); `kontrast_<n>.jpg` bei blassen Stellen.
- `urteil.json` (UTF-8):

```
{"teilkachel": "r1c1", "viertel": "v4", "bearbeiter": "urt-b-r1c1-v4",
 "bilder_angesehen": {"uebersicht": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r1c1/ganz_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c1/v4/uebersicht_nummern.jpg", "…"],
                      "nah": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c1/v4/nah1_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c1/v4/nah_1.jpg", "…"]},
 "segmente": [{"id": 17, "klasse_heute": "Code", "was_ist_es": "ein Satz",
               "urteil": "sauber" | "nicht_sauber", "klasse_vorschlag": null,
               "klasse_frei": {"grob": "Name", "mittel": "Name", "fein": "Name"},
               "sicher": true | false,
               "punkte": [{"nr": 1, "art": "fremdes|fehlt|trennen|verschmelzen|grenze|klasse|zu_klein|sonstiges",
                           "text": "ein Satz mit Stelle (x/y im Teilkachelbild)", "flaeche_px": Zahl oder null}],
               "bilder": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c1/v4/uebersicht_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c1/v4/nah2_roh.jpg"]}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "was an der Kerngrenze nicht passt"}],
 "unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."],
 "klassen_frei": [{"name": "Name", "ebene": "grob|mittel|fein", "eltern": "Name oder null", "merkmal": "woran im Bild erkennbar"}]}
```

Jedes Segment deiner Liste steht genau einmal unter `segmente`, auch die sauberen, in der Reihenfolge der Liste. Segmente der Nachbarviertel (graue Nummern) und des Kontextrands (ohne Nummer) urteilst du in diesem Auftrag nicht; Auffälliges an ihnen nennst du unter `unsicher` mit ID.

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Punkte, Anteil `sicher: false`, wo du unsicher bist.
