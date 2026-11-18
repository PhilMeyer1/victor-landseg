# Auftrag: H0, Teilkachel r0c0, Viertel v4: 55 Segmente im Verbund ansehen und einzeln urteilen (Fassung C „Feste Kategorienliste“)

Lies zuerst den Skill `landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `r0c0` des Ausschnitts in `C:/Users/Phil/Developement/Victor/daten/landseg/H0`. Du urteilst über jedes
Segment deines Viertels v4 (Liste unter „Dein Viertel“), ob Grenze und Klasse stimmen, und zeichnest ein, was
du ändern würdest. Die Label-Karte änderst du nicht.

## Daten (eingefrorener Stand, nur lesen)

- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/manifest.json`: Eintrag `r0c0` unter `teilkacheln` mit `bild` (Teilkachelbild,
  Kern + Kontextrand), `kern_im_bild` (Lage des Kerns im Teilkachelbild) und `kern` (Lage im Ausschnitt).
- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r0c0/labels.tif`: Label-Karte (Segment-ID je Bildpunkt, Größe des Teilkachelbilds).
- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r0c0/segmente.json`: je Segment `id`, `klasse`, `grob`, `herkunft`, `sicher`; dazu die
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
- Die Klassen der Vorstufe sind auf dem Scan schwach (SAM 3 ist für Farb-Orthofotos gebaut; über
  90 % `sicher: nein`, Äcker teils als Gebäude): nur Hinweis.
- Die Vorstufe lief mit kleinerem SAM-3-Fenster (420 Bildpunkte, Schiebefenster) und niedriger
  Instanzschwelle (`C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-2/vorstufe-h0.json`), damit die Streckhöfe einzeln erscheinen. Gerade Grenzen
  mitten in einer gleichförmigen Fläche (etwa bei x 208 oder 420 im Teilkachelbild) können vom
  Schiebefenster stammen: dann ist es keine Bildkante.

## Dein Viertel

Viertel v4 (unten rechts) des Kerns von `r0c0`: x 314–563, y 314–563 im
Teilkachelbild (250 × 250 Bildpunkte). Dir gehören die 55 Segmente der Liste unten: Jedes hat den
größten Teil seiner Kernfläche in diesem Viertel. Die Teilkachel hat 341 Kernsegmente
(v1 114, v2 139, v3 33, v4 55); die anderen Viertel stehen in eigenen Aufträgen mit eigenem Ergebnisordner. Ein Segment
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
Teilkachelbild; Kandidaten aus `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r0c0/kandidaten.json`, dort mit Grund, in den
Bildern nicht eingezeichnet; Anteil hier = Anteil der Kernfläche in diesem Viertel):

| Nr | ID | Klasse Vorstufe | sicher | im Siedlungsgebiet | Kernfläche px | Anteil hier | auch in | Punkt x/y | Kandidaten |
|---|---|---|---|---|---|---|---|---|---|
| 350 | 100350 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 1912 | 91 % | v2 | 459/338 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 359 | 100359 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 263 | 100 % | – | 479/330 | grenze_ohne_bildkante, klasse_unsicher |
| 354 | 100354 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 166 | 74 % | v2 | 487/318 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 355 | 100355 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 736 | 92 % | v2 | 515/328 | grenze_ohne_bildkante, klasse_unsicher |
| 358 | 100358 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 408 | 100 % | – | 538/329 | grenze_ohne_bildkante, klasse_unsicher |
| 342 | 100342 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 173 | 65 % | v2 | 557/318 | grenze_ohne_bildkante, klasse_unsicher |
| 361 | 100361 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 287 | 100 % | – | 558/339 | klasse_unsicher |
| 325 | 100325 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 22746 | 53 % | v1, v2, v3 | 373/365 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 387 | 100387 | 1.3.4 Sport-, Spielplatz (künstlicher Belag) | nein | nein | 186 | 100 % | – | 425/387 | grenze_ohne_bildkante, klasse_unsicher |
| 373 | 100373 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 239 | 100 % | – | 434/364 | grenze_ohne_bildkante, klasse_unsicher |
| 391 | 100391 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 157 | 100 % | – | 440/396 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 340 | 100340 | 1.3.2 Baustelle | nein | nein | 5987 | 96 % | v2 | 460/391 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 386 | 100386 | 1.2.1 Straße (versiegelt) | nein | nein | 205 | 100 % | – | 483/392 | grenze_ohne_bildkante, klasse_unsicher |
| 360 | 100360 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 1310 | 100 % | – | 500/357 | grenze_ohne_bildkante, klasse_unsicher |
| 383 | 100383 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 662 | 100 % | – | 521/397 | grenze_ohne_bildkante, klasse_unsicher |
| 368 | 100368 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 865 | 100 % | – | 528/351 | grenze_ohne_bildkante, klasse_unsicher |
| 376 | 100376 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 298 | 100 % | – | 528/370 | klasse_unsicher, nicht_zusammenhaengend |
| 380 | 100380 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 101 | 100 % | – | 535/378 | klasse_unsicher, nicht_zusammenhaengend |
| 384 | 100384 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 962 | 100 % | – | 544/393 | grenze_ohne_bildkante, klasse_unsicher |
| 366 | 100366 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 352 | 100 % | – | 549/357 | klasse_unsicher |
| 377 | 100377 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 356 | 100 % | – | 557/376 | grenze_ohne_bildkante, klasse_unsicher |
| 369 | 100369 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 107 | 100 % | – | 560/358 | grenze_ohne_bildkante, klasse_unsicher |
| 382 | 100382 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 23 | 100 % | – | 562/389 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 393 | 100393 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 4 | 100 % | – | 563/394 | grenze_ohne_bildkante, klasse_unsicher |
| 417 | 100417 | 1.3.4 Sport-, Spielplatz (künstlicher Belag) | nein | nein | 150 | 100 % | – | 389/438 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 412 | 100412 | 2.1 Acker mit Bewuchs | nein | ja | 127 | 100 % | – | 399/427 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 410 | 100410 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 1719 | 100 % | – | 419/435 | grenze_ohne_bildkante, klasse_unsicher |
| 395 | 100395 | 1.3.4 Sport-, Spielplatz (künstlicher Belag) | nein | nein | 136 | 100 % | – | 429/401 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 396 | 100396 | 2.1 Acker mit Bewuchs | nein | ja | 165 | 100 % | – | 439/409 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 399 | 100399 | 1.2.1 Straße (versiegelt) | nein | nein | 1305 | 100 % | – | 450/422 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 405 | 100405 | 1.2.1 Straße (versiegelt) | nein | nein | 1875 | 100 % | – | 513/445 | grenze_ohne_bildkante, klasse_unsicher |
| 411 | 100411 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 133 | 100 % | – | 518/425 | klasse_unsicher, nicht_zusammenhaengend |
| 403 | 100403 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 126 | 100 % | – | 519/414 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 420 | 100420 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 505 | 100 % | – | 527/441 | klasse_unsicher, nicht_zusammenhaengend |
| 400 | 100400 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1157 | 100 % | – | 533/425 | grenze_ohne_bildkante, klasse_unsicher |
| 394 | 100394 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 157 | 100 % | – | 536/406 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 434 | 100434 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 272 | 93 % | v3 | 327/485 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 437 | 100437 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 191 | 100 % | – | 362/497 | grenze_ohne_bildkante, klasse_unsicher |
| 430 | 100430 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 118 | 100 % | – | 368/473 | grenze_ohne_bildkante, klasse_unsicher |
| 433 | 100433 | 2.1 Acker mit Bewuchs | nein | ja | 295 | 100 % | – | 374/495 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 423 | 100423 | 2.1 Acker mit Bewuchs | nein | ja | 806 | 100 % | – | 382/457 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 426 | 100426 | 1.2.1 Straße (versiegelt) | nein | nein | 277 | 100 % | – | 425/461 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 424 | 100424 | 1.2.1 Straße (versiegelt) | nein | nein | 169 | 100 % | – | 489/462 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 418 | 100418 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 707 | 100 % | – | 554/462 | grenze_ohne_bildkante, klasse_unsicher |
| 447 | 100447 | 1.3.2 Baustelle | nein | nein | 155 | 100 % | – | 367/520 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 449 | 100449 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 226 | 100 % | – | 381/531 | grenze_ohne_bildkante, klasse_unsicher |
| 442 | 100442 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1866 | 100 % | – | 401/543 | grenze_ohne_bildkante, klasse_unsicher |
| 415 | 100415 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 12624 | 100 % | – | 471/514 | grenze_ohne_bildkante, klasse_unsicher |
| 436 | 100436 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 197 | 100 % | – | 557/500 | klasse_unsicher, nicht_zusammenhaengend |
| 428 | 100428 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 32 | 100 % | – | 561/507 | grenze_ohne_bildkante, klasse_unsicher |
| 446 | 100446 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 22 | 100 % | – | 562/520 | klasse_unsicher |
| 454 | 100454 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 406 | 100 % | – | 380/553 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 462 | 100462 | 1.3.2 Baustelle | nein | nein | 55 | 100 % | – | 388/556 | klasse_unsicher, nicht_zusammenhaengend |
| 460 | 100460 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 927 | 100 % | – | 536/552 | grenze_ohne_bildkante, klasse_unsicher |
| 466 | 100466 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 19 | 100 % | – | 545/562 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |

`nicht_geprueft` nennt, was du nicht angesehen hast, `offen`, was du nicht entscheiden konntest.

Kontrolle vor der Rückgabe (muss mit `ok` enden):

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-2/skripte/pruefe_urteil.py --urteil C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r0c0/v4/urteil.json --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r0c0/segmente.json --fassung c --viertel v4 --ids 100350,100359,100354,100355,100358,100342,100361,100325,100387,100373,100391,100340,100386,100360,100383,100368,100376,100380,100384,100366,100377,100369,100382,100393,100417,100412,100410,100395,100396,100399,100405,100411,100403,100420,100400,100394,100434,100437,100430,100433,100423,100426,100424,100418,100447,100449,100442,100415,100436,100428,100446,100454,100462,100460,100466 --kategorien C:/Users/Phil/Developement/Victor/landseg/kategorien.json
```

## Werkzeuge

Befehle im Ordner `C:/Users/Phil/Developement/Victor/landseg` mit `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -m landseg <befehl>`; Aufruf und Schalter stehen in
`C:/Users/Phil/Developement/Victor/landseg/README.md`. Die Bilder deines Viertels liegen fertig vor (Abschnitt „Dein Viertel“); `ansicht` (W3) erzeugt Bilder
je Segment und ist hier keine Urteilsgrundlage. Für fragliche Grenzen `kante` (W4, hier nur zum Ansehen
der Bildkante), zur Kontrolle `pruefen`. Eigene Skripte als Datei in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r0c0/v4`.

## Ergebnis in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r0c0/v4` (genau diese Namen)

- `roh.jpg`, `umriss.jpg` (alle Segmentgrenzen mit ID), `maengel.jpg` (nummerierte Punkte mit kurzer
  deutscher Beschriftung, sonst Vermerk „keine Mängel“), `vorschlag.jpg` (Grenzen und Klassen, wie
  du sie setzen würdest, sonst Vermerk „unverändert“): je dein Viertel mit Umgebung, Viertel
  umrandet (Grundlage: die vorbereiteten Übersichtsbilder).
- `nah_<n>.jpg`: eigene Nahansichten von Stellen, die man in den vorbereiteten Bildern nicht beurteilen kann,
  je ein Teil des Viertels samt Nachbarn (mindestens 64 × 64 Bildpunkte der Teilkachel, kein freigestelltes
  Einzelsegment); `kontrast_<n>.jpg` bei blassen Stellen.
- `urteil.json` (UTF-8):

```
{"teilkachel": "r0c0", "viertel": "v4", "bearbeiter": "urt-c-r0c0-v4",
 "bilder_angesehen": {"uebersicht": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r0c0/ganz_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c0/v4/uebersicht_nummern.jpg", "…"],
                      "nah": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c0/v4/nah1_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r0c0/v4/nah_1.jpg", "…"]},
 "segmente": [{"id": 17, "klasse_heute": "Code", "was_ist_es": "ein Satz",
               "urteil": "sauber" | "nicht_sauber", "klasse_vorschlag": "Code oder null",
               "sicher": true | false,
               "punkte": [{"nr": 1, "art": "fremdes|fehlt|trennen|verschmelzen|grenze|klasse|zu_klein|sonstiges",
                           "text": "ein Satz mit Stelle (x/y im Teilkachelbild)", "flaeche_px": Zahl oder null}],
               "bilder": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c0/v4/uebersicht_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c0/v4/nah2_roh.jpg"]}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "was an der Kerngrenze nicht passt"}],
 "unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."]}
```

Jedes Segment deiner Liste steht genau einmal unter `segmente`, auch die sauberen, in der Reihenfolge der Liste. Segmente der Nachbarviertel (graue Nummern) und des Kontextrands (ohne Nummer) urteilst du in diesem Auftrag nicht; Auffälliges an ihnen nennst du unter `unsicher` mit ID.

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Punkte, Anteil `sicher: false`, wo du unsicher bist.
