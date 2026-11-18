# Auftrag: H0, Teilkachel r0c1, Viertel v3: 105 Segmente im Verbund ansehen und einzeln urteilen (Fassung C „Feste Kategorienliste“)

Lies zuerst den Skill `landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `r0c1` des Ausschnitts in `C:/Users/Phil/Developement/Victor/daten/landseg/H0`. Du urteilst über jedes
Segment deines Viertels v3 (Liste unter „Dein Viertel“), ob Grenze und Klasse stimmen, und zeichnest ein, was
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

Viertel v3 (unten links) des Kerns von `r0c1`: x 64–313, y 314–563 im
Teilkachelbild (250 × 250 Bildpunkte). Dir gehören die 105 Segmente der Liste unten: Jedes hat den
größten Teil seiner Kernfläche in diesem Viertel. Die Teilkachel hat 422 Kernsegmente
(v1 107, v2 103, v3 105, v4 107); die anderen Viertel stehen in eigenen Aufträgen mit eigenem Ergebnisordner. Ein Segment
über einer Viertelgrenze urteilt nur das Viertel mit dem größten Anteil; in den Bildern der Nachbarn ist
es mit grauer Nummer als Umgebung zu sehen.

Urteil im Verbund: Du siehst das Viertel als zusammenhängendes Bild mit Umgebung, arbeitest die Liste der
Reihe nach ab und beurteilst jedes Segment im Zusammenhang mit seinen Nachbarn; eingetragen wird jedes
Segment einzeln (Klasse, `sicher`, `was_ist_es` als Notiz). Bilder freigestellter Einzelsegmente gibt es
nicht, und sie sind keine Urteilsgrundlage.

Bilder des Viertels (fertig, JPEG, in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c1/v3`, Fenster und Vergrößerung je Bild in `viertel.json`):

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
| 325 | 200325 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 70 | 100 % | – | 66/335 | klasse_unsicher |
| 285 | 200285 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 638 | 54 % | v1 | 71/321 | klasse_unsicher |
| 327 | 200327 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1215 | 100 % | – | 81/343 | klasse_unsicher, nicht_zusammenhaengend |
| 301 | 200301 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 174 | 63 % | v1 | 90/317 | klasse_unsicher, nicht_zusammenhaengend |
| 304 | 200304 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 198 | 74 % | v1 | 101/318 | klasse_unsicher, nicht_zusammenhaengend |
| 332 | 200332 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 141 | 100 % | – | 103/338 | klasse_unsicher, nicht_zusammenhaengend |
| 326 | 200326 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 166 | 100 % | – | 114/334 | klasse_unsicher, nicht_zusammenhaengend |
| 292 | 200292 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 659 | 70 % | v1 | 116/320 | klasse_unsicher |
| 317 | 200317 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 847 | 100 % | – | 132/342 | klasse_unsicher |
| 305 | 200305 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 108 | 68 % | v1 | 138/317 | klasse_unsicher, nicht_zusammenhaengend |
| 311 | 200311 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 543 | 100 % | – | 154/348 | klasse_unsicher, nicht_zusammenhaengend |
| 306 | 200306 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 208 | 83 % | v1 | 160/319 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 322 | 200322 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 587 | 100 % | – | 167/334 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 338 | 200338 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 143 | 100 % | – | 182/348 | grenze_ohne_bildkante, klasse_unsicher |
| 315 | 200315 | 1.2.1 Straße (versiegelt) | nein | nein | 146 | 100 % | – | 193/320 | klasse_unsicher |
| 286 | 200286 | 4.2.4 Gebüsch / Strauchfläche | nein | ja | 1492 | 80 % | v1 | 220/330 | grenze_ohne_bildkante, klasse_unsicher |
| 339 | 200339 | 1.3.2 Baustelle | nein | nein | 267 | 100 % | – | 246/348 | klasse_unsicher, nicht_zusammenhaengend |
| 318 | 200318 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 417 | 100 % | – | 248/333 | klasse_unsicher |
| 296 | 200296 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 347 | 75 % | v1 | 259/322 | klasse_unsicher |
| 330 | 200330 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 167 | 100 % | – | 265/335 | klasse_unsicher, nicht_zusammenhaengend |
| 273 | 200273 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 2819 | 58 % | v1, v2, v4 | 279/348 | klasse_unsicher |
| 312 | 200312 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 345 | 100 % | – | 286/327 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 298 | 200298 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 124 | 51 % | v1, v2, v4 | 308/316 | klasse_unsicher, nicht_zusammenhaengend |
| 361 | 200361 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 70 | 100 % | – | 67/374 | klasse_unsicher, nicht_zusammenhaengend |
| 377 | 200377 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 329 | 100 % | – | 78/396 | klasse_unsicher |
| 340 | 200340 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 686 | 100 % | – | 85/362 | klasse_unsicher |
| 356 | 200356 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1193 | 100 % | – | 92/385 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 341 | 200341 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 1312 | 100 % | – | 144/370 | klasse_unsicher |
| 359 | 200359 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 317 | 100 % | – | 165/377 | klasse_unsicher, nicht_zusammenhaengend |
| 368 | 200368 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 878 | 100 % | – | 175/389 | grenze_ohne_bildkante, klasse_unsicher |
| 345 | 200345 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 343 | 100 % | – | 180/362 | grenze_ohne_bildkante, klasse_unsicher |
| 365 | 200365 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 919 | 100 % | – | 197/383 | grenze_ohne_bildkante, klasse_unsicher |
| 380 | 200380 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 206 | 100 % | – | 209/396 | grenze_ohne_bildkante, klasse_unsicher |
| 357 | 200357 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 142 | 100 % | – | 231/375 | klasse_unsicher |
| 351 | 200351 | 1.3.2 Baustelle | nein | nein | 702 | 100 % | – | 246/382 | klasse_unsicher, nicht_zusammenhaengend |
| 346 | 200346 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 130 | 100 % | – | 291/365 | klasse_unsicher, nicht_zusammenhaengend |
| 362 | 200362 | 4.2.1 Einzelbaum | nein | ja | 1057 | 100 % | – | 293/397 | klasse_unsicher |
| 337 | 200337 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 177 | 100 % | – | 297/350 | grenze_ohne_bildkante, klasse_unsicher |
| 360 | 200360 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 413 | 98 % | v4 | 302/378 | klasse_unsicher |
| 384 | 200384 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 609 | 100 % | – | 72/434 | grenze_ohne_bildkante, klasse_unsicher |
| 400 | 200400 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 499 | 100 % | – | 86/422 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 385 | 200385 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 193 | 100 % | – | 90/409 | klasse_unsicher |
| 395 | 200395 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 167 | 100 % | – | 114/415 | klasse_unsicher, nicht_zusammenhaengend |
| 371 | 200371 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 1400 | 100 % | – | 122/400 | klasse_unsicher |
| 388 | 200388 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 2984 | 100 % | – | 140/430 | klasse_unsicher |
| 383 | 200383 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 546 | 100 % | – | 159/414 | klasse_unsicher, nicht_zusammenhaengend |
| 419 | 200419 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 193 | 100 % | – | 211/439 | grenze_ohne_bildkante, klasse_unsicher |
| 391 | 200391 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 583 | 100 % | – | 221/425 | grenze_ohne_bildkante, klasse_unsicher |
| 350 | 200350 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 1672 | 100 % | – | 236/405 | grenze_ohne_bildkante, klasse_unsicher |
| 410 | 200410 | 1.2.1 Straße (versiegelt) | ja | nein | 283 | 100 % | – | 253/427 | grenze_ohne_bildkante |
| 424 | 200424 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 892 | 100 % | – | 263/443 | klasse_unsicher |
| 370 | 200370 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 906 | 100 % | – | 268/401 | grenze_ohne_bildkante, klasse_unsicher |
| 394 | 200394 | 1.2.1 Straße (versiegelt) | nein | nein | 207 | 100 % | – | 279/421 | grenze_ohne_bildkante, klasse_unsicher |
| 398 | 200398 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 88 | 100 % | – | 291/424 | klasse_unsicher |
| 411 | 200411 | 1.2.1 Straße (versiegelt) | nein | nein | 1093 | 100 % | – | 291/449 | grenze_ohne_bildkante, klasse_unsicher |
| 381 | 200381 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1118 | 56 % | v4 | 304/419 | klasse_unsicher |
| 428 | 200428 | 1.2.1 Straße (versiegelt) | ja | nein | 187 | 75 % | v4 | 304/441 | – |
| 454 | 200454 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 32 | 100 % | – | 65/493 | klasse_unsicher, nicht_zusammenhaengend |
| 433 | 200433 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1036 | 100 % | – | 77/460 | klasse_unsicher |
| 448 | 200448 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 2413 | 100 % | – | 100/486 | grenze_ohne_bildkante, klasse_unsicher |
| 446 | 200446 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 77 | 100 % | – | 116/463 | klasse_unsicher, nicht_zusammenhaengend |
| 415 | 200415 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1359 | 100 % | – | 152/453 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 458 | 200458 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 101 | 100 % | – | 153/481 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 432 | 200432 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1814 | 100 % | – | 167/470 | grenze_ohne_bildkante, klasse_unsicher |
| 459 | 200459 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1533 | 100 % | – | 191/491 | grenze_ohne_bildkante, klasse_unsicher |
| 450 | 200450 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 418 | 100 % | – | 204/470 | klasse_unsicher, nicht_zusammenhaengend |
| 401 | 200401 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 312 | 100 % | – | 215/450 | grenze_ohne_bildkante, klasse_unsicher |
| 464 | 200464 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 286 | 100 % | – | 220/487 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 439 | 200439 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 679 | 100 % | – | 223/468 | klasse_unsicher |
| 451 | 200451 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 98 | 100 % | – | 237/474 | klasse_unsicher |
| 457 | 200457 | 1.2.1 Straße (versiegelt) | nein | nein | 200 | 100 % | – | 247/490 | klasse_unsicher |
| 437 | 200437 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 679 | 100 % | – | 289/475 | klasse_unsicher |
| 441 | 200441 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 315 | 90 % | v4 | 307/460 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 488 | 200488 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 1103 | 100 % | – | 85/528 | klasse_unsicher |
| 465 | 200465 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1821 | 100 % | – | 117/519 | grenze_ohne_bildkante, klasse_unsicher |
| 504 | 200504 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 784 | 100 % | – | 137/541 | grenze_ohne_bildkante, klasse_unsicher |
| 491 | 200491 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 170 | 100 % | – | 154/517 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 517 | 200517 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 164 | 100 % | – | 154/544 | klasse_unsicher, nicht_zusammenhaengend |
| 486 | 200486 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 158 | 100 % | – | 176/510 | klasse_unsicher, nicht_zusammenhaengend |
| 498 | 200498 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 726 | 100 % | – | 177/533 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 510 | 200510 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 433 | 100 % | – | 194/542 | grenze_ohne_bildkante, klasse_unsicher |
| 484 | 200484 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 634 | 100 % | – | 196/513 | grenze_ohne_bildkante, klasse_unsicher |
| 493 | 200493 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 108 | 100 % | – | 211/521 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 470 | 200470 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 565 | 100 % | – | 224/504 | grenze_ohne_bildkante, klasse_unsicher |
| 485 | 200485 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 1127 | 100 % | – | 227/525 | grenze_ohne_bildkante, klasse_unsicher |
| 508 | 200508 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 283 | 100 % | – | 230/543 | klasse_unsicher, nicht_zusammenhaengend |
| 472 | 200472 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 753 | 100 % | – | 255/508 | klasse_unsicher |
| 489 | 200489 | 1.2.1 Straße (versiegelt) | nein | nein | 126 | 100 % | – | 272/528 | klasse_unsicher |
| 414 | 200414 | 1.2.1 Straße (versiegelt) | nein | nein | 3696 | 100 % | – | 291/510 | grenze_ohne_bildkante, klasse_unsicher |
| 497 | 200497 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 53 | 100 % | – | 65/550 | klasse_unsicher, nicht_zusammenhaengend |
| 533 | 200533 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 21 | 100 % | – | 65/558 | klasse_unsicher |
| 397 | 200397 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 423 | 100 % | – | 77/556 | grenze_ohne_bildkante, klasse_unsicher |
| 539 | 200539 | 1.2.1 Straße (versiegelt) | ja | nein | 22 | 100 % | – | 88/562 | grenze_ohne_bildkante |
| 516 | 200516 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 494 | 100 % | – | 94/554 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 534 | 200534 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 151 | 100 % | – | 116/559 | klasse_unsicher, nicht_zusammenhaengend |
| 521 | 200521 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 90 | 100 % | – | 127/552 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 525 | 200525 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 76 | 100 % | – | 134/553 | klasse_unsicher |
| 526 | 200526 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 360 | 100 % | – | 155/556 | klasse_unsicher |
| 540 | 200540 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 8 | 100 % | – | 160/562 | klasse_unsicher, nicht_zusammenhaengend |
| 518 | 200518 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 639 | 100 % | – | 196/556 | klasse_unsicher |
| 502 | 200502 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 1389 | 100 % | – | 249/552 | grenze_ohne_bildkante, klasse_unsicher |
| 527 | 200527 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 111 | 100 % | – | 267/558 | klasse_unsicher, nicht_zusammenhaengend |
| 535 | 200535 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 74 | 100 % | – | 274/560 | klasse_unsicher |
| 507 | 200507 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 596 | 100 % | – | 286/552 | grenze_ohne_bildkante, klasse_unsicher |
| 522 | 200522 | 1.2.1 Straße (versiegelt) | ja | nein | 76 | 100 % | – | 311/561 | – |

`nicht_geprueft` nennt, was du nicht angesehen hast, `offen`, was du nicht entscheiden konntest.

Kontrolle vor der Rückgabe (muss mit `ok` enden):

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-2/skripte/pruefe_urteil.py --urteil C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r0c1/v3/urteil.json --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r0c1/segmente.json --fassung c --viertel v3 --ids 200325,200285,200327,200301,200304,200332,200326,200292,200317,200305,200311,200306,200322,200338,200315,200286,200339,200318,200296,200330,200273,200312,200298,200361,200377,200340,200356,200341,200359,200368,200345,200365,200380,200357,200351,200346,200362,200337,200360,200384,200400,200385,200395,200371,200388,200383,200419,200391,200350,200410,200424,200370,200394,200398,200411,200381,200428,200454,200433,200448,200446,200415,200458,200432,200459,200450,200401,200464,200439,200451,200457,200437,200441,200488,200465,200504,200491,200517,200486,200498,200510,200484,200493,200470,200485,200508,200472,200489,200414,200497,200533,200397,200539,200516,200534,200521,200525,200526,200540,200518,200502,200527,200535,200507,200522 --kategorien C:/Users/Phil/Developement/Victor/landseg/kategorien.json
```

## Werkzeuge

Befehle im Ordner `C:/Users/Phil/Developement/Victor/landseg` mit `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -m landseg <befehl>`; Aufruf und Schalter stehen in
`C:/Users/Phil/Developement/Victor/landseg/README.md`. Die Bilder deines Viertels liegen fertig vor (Abschnitt „Dein Viertel“); `ansicht` (W3) erzeugt Bilder
je Segment und ist hier keine Urteilsgrundlage. Für fragliche Grenzen `kante` (W4, hier nur zum Ansehen
der Bildkante), zur Kontrolle `pruefen`. Eigene Skripte als Datei in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r0c1/v3`.

## Ergebnis in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r0c1/v3` (genau diese Namen)

- `roh.jpg`, `umriss.jpg` (alle Segmentgrenzen mit ID), `maengel.jpg` (nummerierte Punkte mit kurzer
  deutscher Beschriftung, sonst Vermerk „keine Mängel“), `vorschlag.jpg` (Grenzen und Klassen, wie
  du sie setzen würdest, sonst Vermerk „unverändert“): je dein Viertel mit Umgebung, Viertel
  umrandet (Grundlage: die vorbereiteten Übersichtsbilder).
- `nah_<n>.jpg`: eigene Nahansichten von Stellen, die man in den vorbereiteten Bildern nicht beurteilen kann,
  je ein Teil des Viertels samt Nachbarn (mindestens 64 × 64 Bildpunkte der Teilkachel, kein freigestelltes
  Einzelsegment); `kontrast_<n>.jpg` bei blassen Stellen.
- `urteil.json` (UTF-8):

```
{"teilkachel": "r0c1", "viertel": "v3", "bearbeiter": "urt-c-r0c1-v3",
 "bilder_angesehen": {"uebersicht": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r0c1/ganz_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c1/v3/uebersicht_nummern.jpg", "…"],
                      "nah": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c1/v3/nah1_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r0c1/v3/nah_1.jpg", "…"]},
 "segmente": [{"id": 17, "klasse_heute": "Code", "was_ist_es": "ein Satz",
               "urteil": "sauber" | "nicht_sauber", "klasse_vorschlag": "Code oder null",
               "sicher": true | false,
               "punkte": [{"nr": 1, "art": "fremdes|fehlt|trennen|verschmelzen|grenze|klasse|zu_klein|sonstiges",
                           "text": "ein Satz mit Stelle (x/y im Teilkachelbild)", "flaeche_px": Zahl oder null}],
               "bilder": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c1/v3/uebersicht_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c1/v3/nah2_roh.jpg"]}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "was an der Kerngrenze nicht passt"}],
 "unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."]}
```

Jedes Segment deiner Liste steht genau einmal unter `segmente`, auch die sauberen, in der Reihenfolge der Liste. Segmente der Nachbarviertel (graue Nummern) und des Kontextrands (ohne Nummer) urteilst du in diesem Auftrag nicht; Auffälliges an ihnen nennst du unter `unsicher` mit ID.

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Punkte, Anteil `sicher: false`, wo du unsicher bist.
