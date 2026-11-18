# Auftrag: H0, Teilkachel r0c1, Viertel v4: 107 Segmente im Verbund ansehen und einzeln urteilen (Fassung C „Feste Kategorienliste“)

Lies zuerst den Skill `landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `r0c1` des Ausschnitts in `C:/Users/Phil/Developement/Victor/daten/landseg/H0`. Du urteilst über jedes
Segment deines Viertels v4 (Liste unter „Dein Viertel“), ob Grenze und Klasse stimmen, und zeichnest ein, was
du ändern würdest. Die Label-Karte änderst du nicht.

## Daten (eingefrorener Stand, nur lesen)

- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/manifest.json`: Eintrag `r0c1` unter `teilkacheln` mit `bild` (Teilkachelbild,
  Kern + Kontextrand), `kern_im_bild` (Lage des Kerns im Teilkachelbild) und `kern` (Lage im Ausschnitt).
- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r0c1/labels.tif`: Label-Karte (Segment-ID je Bildpunkt, Größe des Teilkachelbilds).
- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r0c1/segmente.json`: je Segment `id`, `klasse`, `grob`, `herkunft`, `sicher`; dazu die
  Kandidatenliste der Vorstufe, falls vorhanden.
- `C:/Users/Phil/Developement/Victor/landseg/kategorien.json` und `C:/Users/Phil/Developement/Victor/landseg/KATEGORIEN.md`: die gültigen Klassen und Regeln.

## Zuerst der ganze Ausschnitt, dann die Teilkachel

Bevor du dein Viertel ansiehst: zuerst den ganzen Ausschnitt H0 (`C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png`, mit Teilkachelgitter
`C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/H0_raster.jpg`; r0c0 oben links, r0c1 oben rechts, r1c0 unten links, r1c1 unten rechts),
dann die ganze Teilkachel `r0c1` (`C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r0c1/ganz_nummern.jpg`: Grenzen, Nummern, Viertel cyan v1–v4;
`C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r0c1/ganz_roh.jpg` unverändert; beide 2fach). Beide stehen in `bilder_angesehen.uebersicht` vor den Viertelbildern.

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

Viertel v4 (unten rechts) des Kerns von `r0c1`: x 314–563, y 314–563 im
Teilkachelbild (250 × 250 Bildpunkte). Dir gehören die 107 Segmente der Liste unten: Jedes hat den
größten Teil seiner Kernfläche in diesem Viertel. Die Teilkachel hat 422 Kernsegmente
(v1 107, v2 103, v3 105, v4 107); die anderen Viertel stehen in eigenen Aufträgen mit eigenem Ergebnisordner. Ein Segment
über einer Viertelgrenze urteilt nur das Viertel mit dem größten Anteil; in den Bildern der Nachbarn ist
es mit grauer Nummer als Umgebung zu sehen.

Urteil im Verbund: Du siehst das Viertel als zusammenhängendes Bild mit Umgebung, arbeitest die Liste der
Reihe nach ab und beurteilst jedes Segment im Zusammenhang mit seinen Nachbarn; eingetragen wird jedes
Segment einzeln (Klasse, `sicher`, `was_ist_es` als Notiz). Bilder freigestellter Einzelsegmente gibt es
nicht, und sie sind keine Urteilsgrundlage.

Bilder des Viertels (fertig, JPEG, in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c1/v4`, Fenster und Vergrößerung je Bild in `viertel.json`):

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
Teilkachelbild; Kandidaten aus `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r0c1/kandidaten.json`, dort mit Grund, in den
Bildern nicht eingezeichnet; Anteil hier = Anteil der Kernfläche in diesem Viertel):

| Nr | ID | Klasse Vorstufe | sicher | im Siedlungsgebiet | Kernfläche px | Anteil hier | auch in | Punkt x/y | Kandidaten |
|---|---|---|---|---|---|---|---|---|---|
| 319 | 200319 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 2202 | 82 % | v3 | 333/345 | grenze_ohne_bildkante, klasse_unsicher |
| 313 | 200313 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 144 | 100 % | – | 348/324 | klasse_unsicher, nicht_zusammenhaengend |
| 331 | 200331 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 128 | 100 % | – | 357/340 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 299 | 200299 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 869 | 96 % | v2 | 380/337 | klasse_unsicher, nicht_zusammenhaengend |
| 314 | 200314 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 151 | 100 % | – | 397/320 | klasse_unsicher |
| 320 | 200320 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 124 | 100 % | – | 407/327 | klasse_unsicher |
| 328 | 200328 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 582 | 100 % | – | 408/343 | klasse_unsicher |
| 310 | 200310 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 183 | 96 % | v2 | 413/320 | klasse_unsicher, nicht_zusammenhaengend |
| 308 | 200308 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 538 | 95 % | v2 | 432/330 | klasse_unsicher, nicht_zusammenhaengend |
| 303 | 200303 | 4.2.1 Einzelbaum | nein | ja | 340 | 80 % | v2 | 439/319 | klasse_unsicher |
| 324 | 200324 | 6.6 Weg, unbefestigt (Feld-, Wald-, Schotterweg) | nein | nein | 80 | 100 % | – | 478/326 | klasse_unsicher |
| 333 | 200333 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 454 | 100 % | – | 482/344 | klasse_unsicher |
| 316 | 200316 | 1.3.2 Baustelle | nein | nein | 288 | 100 % | – | 488/328 | klasse_unsicher, nicht_zusammenhaengend |
| 321 | 200321 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 945 | 100 % | – | 516/334 | klasse_unsicher, nicht_zusammenhaengend |
| 307 | 200307 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1325 | 94 % | v2 | 544/340 | klasse_unsicher |
| 352 | 200352 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1962 | 99 % | v3 | 350/383 | grenze_ohne_bildkante, klasse_unsicher |
| 343 | 200343 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 728 | 100 % | – | 372/357 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 353 | 200353 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 297 | 100 % | – | 385/366 | klasse_unsicher |
| 323 | 200323 | 1.2.1 Straße (versiegelt) | nein | nein | 1824 | 100 % | – | 392/384 | klasse_unsicher, nicht_zusammenhaengend |
| 354 | 200354 | 1.3.2 Baustelle | nein | nein | 1158 | 100 % | – | 424/397 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 349 | 200349 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 531 | 100 % | – | 470/363 | klasse_unsicher |
| 355 | 200355 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 591 | 100 % | – | 500/390 | klasse_unsicher |
| 335 | 200335 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1330 | 100 % | – | 509/365 | klasse_unsicher |
| 375 | 200375 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 170 | 100 % | – | 515/395 | klasse_unsicher |
| 344 | 200344 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 328 | 100 % | – | 526/355 | klasse_unsicher |
| 364 | 200364 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1111 | 100 % | – | 552/394 | klasse_unsicher |
| 347 | 200347 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 121 | 100 % | – | 558/355 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 418 | 200418 | 1.2.1 Straße (versiegelt) | nein | nein | 229 | 76 % | v3 | 320/432 | klasse_unsicher, nicht_zusammenhaengend |
| 407 | 200407 | 1.2.1 Straße (versiegelt) | ja | nein | 167 | 100 % | – | 330/426 | – |
| 406 | 200406 | 1.2.1 Straße (versiegelt) | nein | nein | 1243 | 97 % | v3 | 354/428 | grenze_ohne_bildkante, klasse_unsicher |
| 425 | 200425 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 788 | 100 % | – | 358/449 | grenze_ohne_bildkante, klasse_unsicher |
| 412 | 200412 | 1.2.1 Straße (versiegelt) | nein | nein | 160 | 100 % | – | 375/424 | grenze_ohne_bildkante, klasse_unsicher |
| 429 | 200429 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 202 | 100 % | – | 381/447 | klasse_unsicher |
| 417 | 200417 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 255 | 100 % | – | 385/428 | grenze_ohne_bildkante, klasse_unsicher |
| 396 | 200396 | 1.3.2 Baustelle | nein | nein | 112 | 100 % | – | 387/418 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 369 | 200369 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 974 | 100 % | – | 393/402 | grenze_ohne_bildkante, klasse_unsicher |
| 386 | 200386 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 178 | 100 % | – | 400/414 | grenze_ohne_bildkante, klasse_unsicher |
| 402 | 200402 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 511 | 100 % | – | 408/428 | klasse_unsicher |
| 399 | 200399 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 120 | 100 % | – | 420/423 | klasse_unsicher |
| 430 | 200430 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 192 | 100 % | – | 422/447 | klasse_unsicher |
| 389 | 200389 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 223 | 100 % | – | 427/414 | grenze_ohne_bildkante, klasse_unsicher |
| 374 | 200374 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 340 | 100 % | – | 440/412 | klasse_unsicher, nicht_zusammenhaengend |
| 378 | 200378 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 500 | 100 % | – | 452/408 | grenze_ohne_bildkante, klasse_unsicher |
| 379 | 200379 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 478 | 100 % | – | 462/400 | klasse_unsicher, nicht_zusammenhaengend |
| 408 | 200408 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 750 | 100 % | – | 462/449 | klasse_unsicher, nicht_zusammenhaengend |
| 366 | 200366 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 790 | 100 % | – | 479/402 | klasse_unsicher |
| 367 | 200367 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1055 | 100 % | – | 506/426 | klasse_unsicher, nicht_zusammenhaengend |
| 382 | 200382 | 4.2.1 Einzelbaum | nein | ja | 340 | 100 % | – | 511/409 | klasse_unsicher |
| 421 | 200421 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 377 | 100 % | – | 522/440 | klasse_unsicher |
| 376 | 200376 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1382 | 100 % | – | 540/422 | klasse_unsicher |
| 442 | 200442 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 158 | 100 % | – | 329/464 | klasse_unsicher, nicht_zusammenhaengend |
| 452 | 200452 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 2173 | 100 % | – | 338/486 | grenze_ohne_bildkante, klasse_unsicher |
| 440 | 200440 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 127 | 100 % | – | 341/463 | klasse_unsicher |
| 449 | 200449 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 165 | 100 % | – | 353/466 | grenze_ohne_bildkante, klasse_unsicher |
| 445 | 200445 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1037 | 100 % | – | 365/483 | klasse_unsicher |
| 460 | 200460 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 214 | 100 % | – | 381/486 | klasse_unsicher, nicht_zusammenhaengend |
| 443 | 200443 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 543 | 100 % | – | 391/473 | klasse_unsicher |
| 413 | 200413 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 921 | 100 % | – | 408/453 | grenze_ohne_bildkante, klasse_unsicher |
| 462 | 200462 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 323 | 100 % | – | 427/487 | grenze_ohne_bildkante, klasse_unsicher |
| 420 | 200420 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1945 | 100 % | – | 439/472 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 404 | 200404 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1333 | 100 % | – | 459/471 | grenze_ohne_bildkante, klasse_unsicher |
| 403 | 200403 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1118 | 100 % | – | 481/459 | grenze_ohne_bildkante, klasse_unsicher |
| 392 | 200392 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1554 | 100 % | – | 504/458 | klasse_unsicher |
| 455 | 200455 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 232 | 100 % | – | 526/489 | klasse_unsicher, nicht_zusammenhaengend |
| 423 | 200423 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 377 | 100 % | – | 532/470 | klasse_unsicher |
| 453 | 200453 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 379 | 100 % | – | 539/486 | klasse_unsicher |
| 416 | 200416 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1075 | 100 % | – | 552/468 | klasse_unsicher |
| 456 | 200456 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 70 | 100 % | – | 560/478 | grenze_ohne_bildkante, klasse_unsicher |
| 466 | 200466 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 2236 | 89 % | v3 | 332/526 | klasse_unsicher |
| 499 | 200499 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 656 | 100 % | v3 | 349/547 | klasse_unsicher |
| 478 | 200478 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 541 | 100 % | – | 384/525 | klasse_unsicher |
| 477 | 200477 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 165 | 100 % | – | 389/511 | klasse_unsicher, nicht_zusammenhaengend |
| 463 | 200463 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 671 | 100 % | – | 402/501 | klasse_unsicher, nicht_zusammenhaengend |
| 500 | 200500 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 759 | 100 % | – | 411/541 | grenze_ohne_bildkante, klasse_unsicher |
| 435 | 200435 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 809 | 100 % | – | 418/521 | klasse_unsicher |
| 505 | 200505 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 321 | 100 % | – | 426/540 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 475 | 200475 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 742 | 100 % | – | 435/524 | klasse_unsicher |
| 506 | 200506 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 112 | 100 % | – | 440/548 | grenze_ohne_bildkante |
| 471 | 200471 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 96 | 100 % | – | 450/500 | klasse_unsicher |
| 509 | 200509 | 1.3.2 Baustelle | nein | nein | 239 | 100 % | – | 465/542 | klasse_unsicher |
| 469 | 200469 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 318 | 100 % | – | 474/503 | klasse_unsicher |
| 483 | 200483 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1570 | 100 % | – | 482/524 | grenze_ohne_bildkante, klasse_unsicher |
| 511 | 200511 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 113 | 100 % | – | 494/541 | klasse_unsicher, nicht_zusammenhaengend |
| 467 | 200467 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 587 | 100 % | – | 499/502 | klasse_unsicher |
| 512 | 200512 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 446 | 100 % | – | 508/545 | grenze_ohne_bildkante, klasse_unsicher |
| 495 | 200495 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 213 | 100 % | – | 513/530 | – |
| 461 | 200461 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 556 | 100 % | – | 522/503 | klasse_unsicher |
| 513 | 200513 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 407 | 100 % | – | 530/548 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 492 | 200492 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 728 | 100 % | – | 533/525 | klasse_unsicher |
| 473 | 200473 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 227 | 100 % | – | 538/512 | – |
| 474 | 200474 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 250 | 100 % | – | 544/502 | klasse_unsicher |
| 494 | 200494 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 289 | 100 % | – | 553/530 | grenze_ohne_bildkante, klasse_unsicher |
| 481 | 200481 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 158 | 100 % | – | 558/512 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 496 | 200496 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 255 | 100 % | – | 558/548 | klasse_unsicher |
| 541 | 200541 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 4 | 100 % | – | 331/563 | klasse_unsicher |
| 536 | 200536 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 45 | 100 % | – | 340/559 | klasse_unsicher, nicht_zusammenhaengend |
| 531 | 200531 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 131 | 100 % | – | 351/559 | klasse_unsicher |
| 529 | 200529 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 109 | 100 % | – | 363/557 | klasse_unsicher |
| 520 | 200520 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 342 | 100 % | – | 373/552 | klasse_unsicher |
| 528 | 200528 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 193 | 100 % | – | 415/558 | klasse_unsicher |
| 523 | 200523 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 520 | 100 % | – | 450/555 | grenze_ohne_bildkante, klasse_unsicher |
| 515 | 200515 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 508 | 100 % | – | 487/554 | klasse_unsicher |
| 537 | 200537 | 1.3.2 Baustelle | nein | nein | 74 | 100 % | – | 518/560 | klasse_unsicher |
| 532 | 200532 | 1.2.1 Straße (versiegelt) | nein | nein | 69 | 100 % | – | 524/561 | klasse_unsicher, nicht_zusammenhaengend |
| 530 | 200530 | 1.3.2 Baustelle | nein | nein | 94 | 100 % | – | 535/556 | klasse_unsicher |
| 503 | 200503 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 190 | 100 % | – | 559/559 | klasse_unsicher, nicht_zusammenhaengend |
| 542 | 200542 | 4.2.1 Einzelbaum | ja | ja | 2 | 100 % | – | 562/563 | – |

`nicht_geprueft` nennt, was du nicht angesehen hast, `offen`, was du nicht entscheiden konntest.

Kontrolle vor der Rückgabe (muss mit `ok` enden):

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-2/skripte/pruefe_urteil.py --urteil C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r0c1/v4/urteil.json --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r0c1/segmente.json --fassung c --viertel v4 --ids 200319,200313,200331,200299,200314,200320,200328,200310,200308,200303,200324,200333,200316,200321,200307,200352,200343,200353,200323,200354,200349,200355,200335,200375,200344,200364,200347,200418,200407,200406,200425,200412,200429,200417,200396,200369,200386,200402,200399,200430,200389,200374,200378,200379,200408,200366,200367,200382,200421,200376,200442,200452,200440,200449,200445,200460,200443,200413,200462,200420,200404,200403,200392,200455,200423,200453,200416,200456,200466,200499,200478,200477,200463,200500,200435,200505,200475,200506,200471,200509,200469,200483,200511,200467,200512,200495,200461,200513,200492,200473,200474,200494,200481,200496,200541,200536,200531,200529,200520,200528,200523,200515,200537,200532,200530,200503,200542 --kategorien C:/Users/Phil/Developement/Victor/landseg/kategorien.json
```

## Werkzeuge

Befehle im Ordner `C:/Users/Phil/Developement/Victor/landseg` mit `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -m landseg <befehl>`; Aufruf und Schalter stehen in
`C:/Users/Phil/Developement/Victor/landseg/README.md`. Die Bilder deines Viertels liegen fertig vor (Abschnitt „Dein Viertel“); `ansicht` (W3) erzeugt Bilder
je Segment und ist hier keine Urteilsgrundlage. Für fragliche Grenzen `kante` (W4, hier nur zum Ansehen
der Bildkante), zur Kontrolle `pruefen`. Eigene Skripte als Datei in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r0c1/v4`.

## Ergebnis in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r0c1/v4` (genau diese Namen)

- `roh.jpg`, `umriss.jpg` (alle Segmentgrenzen mit ID), `maengel.jpg` (nummerierte Punkte mit kurzer
  deutscher Beschriftung, sonst Vermerk „keine Mängel“), `vorschlag.jpg` (Grenzen und Klassen, wie
  du sie setzen würdest, sonst Vermerk „unverändert“): je dein Viertel mit Umgebung, Viertel
  umrandet (Grundlage: die vorbereiteten Übersichtsbilder).
- `nah_<n>.jpg`: eigene Nahansichten von Stellen, die man in den vorbereiteten Bildern nicht beurteilen kann,
  je ein Teil des Viertels samt Nachbarn (mindestens 64 × 64 Bildpunkte der Teilkachel, kein freigestelltes
  Einzelsegment); `kontrast_<n>.jpg` bei blassen Stellen.
- `urteil.json` (UTF-8):

```
{"teilkachel": "r0c1", "viertel": "v4", "bearbeiter": "urt-c-r0c1-v4",
 "bilder_angesehen": {"uebersicht": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r0c1/ganz_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c1/v4/uebersicht_nummern.jpg", "…"],
                      "nah": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c1/v4/nah1_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r0c1/v4/nah_1.jpg", "…"]},
 "segmente": [{"id": 17, "klasse_heute": "Code", "was_ist_es": "ein Satz",
               "urteil": "sauber" | "nicht_sauber", "klasse_vorschlag": "Code oder null",
               "sicher": true | false,
               "punkte": [{"nr": 1, "art": "fremdes|fehlt|trennen|verschmelzen|grenze|klasse|zu_klein|sonstiges",
                           "text": "ein Satz mit Stelle (x/y im Teilkachelbild)", "flaeche_px": Zahl oder null}],
               "bilder": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c1/v4/uebersicht_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c1/v4/nah2_roh.jpg"]}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "was an der Kerngrenze nicht passt"}],
 "unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."]}
```

Jedes Segment deiner Liste steht genau einmal unter `segmente`, auch die sauberen, in der Reihenfolge der Liste. Segmente der Nachbarviertel (graue Nummern) und des Kontextrands (ohne Nummer) urteilst du in diesem Auftrag nicht; Auffälliges an ihnen nennst du unter `unsicher` mit ID.

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Punkte, Anteil `sicher: false`, wo du unsicher bist.
