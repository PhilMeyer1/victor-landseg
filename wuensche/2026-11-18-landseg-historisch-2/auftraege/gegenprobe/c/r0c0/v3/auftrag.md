# Auftrag: H0, Teilkachel r0c0, Viertel v3: 33 Segmente im Verbund ansehen und einzeln urteilen (Fassung C „Feste Kategorienliste“)

Lies zuerst den Skill `landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `r0c0` des Ausschnitts in `C:/Users/Phil/Developement/Victor/daten/landseg/H0`. Du urteilst über jedes
Segment deines Viertels v3 (Liste unter „Dein Viertel“), ob Grenze und Klasse stimmen, und zeichnest ein, was
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

Viertel v3 (unten links) des Kerns von `r0c0`: x 64–313, y 314–563 im
Teilkachelbild (250 × 250 Bildpunkte). Dir gehören die 33 Segmente der Liste unten: Jedes hat den
größten Teil seiner Kernfläche in diesem Viertel. Die Teilkachel hat 341 Kernsegmente
(v1 114, v2 139, v3 33, v4 55); die anderen Viertel stehen in eigenen Aufträgen mit eigenem Ergebnisordner. Ein Segment
über einer Viertelgrenze urteilt nur das Viertel mit dem größten Anteil; in den Bildern der Nachbarn ist
es mit grauer Nummer als Umgebung zu sehen.

Urteil im Verbund: Du siehst das Viertel als zusammenhängendes Bild mit Umgebung, arbeitest die Liste der
Reihe nach ab und beurteilst jedes Segment im Zusammenhang mit seinen Nachbarn; eingetragen wird jedes
Segment einzeln (Klasse, `sicher`, `was_ist_es` als Notiz). Bilder freigestellter Einzelsegmente gibt es
nicht, und sie sind keine Urteilsgrundlage.

Bilder des Viertels (fertig, JPEG, in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c0/v3`, Fenster und Vergrößerung je Bild in `viertel.json`):

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
| 351 | 100351 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 295 | 100 % | – | 71/340 | grenze_ohne_bildkante, klasse_unsicher |
| 341 | 100341 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 177 | 100 % | – | 79/332 | klasse_unsicher |
| 349 | 100349 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 468 | 57 % | v1 | 160/320 | grenze_ohne_bildkante, klasse_unsicher |
| 362 | 100362 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 127 | 100 % | – | 163/331 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 371 | 100371 | 2.1 Acker mit Bewuchs | nein | ja | 118 | 100 % | – | 68/353 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 367 | 100367 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 1903 | 100 % | – | 88/363 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 353 | 100353 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 7002 | 99 % | v1 | 162/379 | grenze_ohne_bildkante, klasse_unsicher |
| 407 | 100407 | 1.3.2 Baustelle | nein | nein | 3530 | 100 % | – | 79/437 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 385 | 100385 | 1.2.1 Straße (versiegelt) | nein | nein | 1588 | 100 % | – | 89/402 | grenze_ohne_bildkante, klasse_unsicher |
| 409 | 100409 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1247 | 100 % | – | 107/437 | grenze_ohne_bildkante, klasse_unsicher |
| 414 | 100414 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 202 | 100 % | – | 127/436 | grenze_ohne_bildkante, klasse_unsicher |
| 402 | 100402 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 4562 | 100 % | – | 177/445 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 432 | 100432 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 1293 | 100 % | – | 83/491 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 429 | 100429 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 138 | 100 % | – | 126/474 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 379 | 100379 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 1693 | 100 % | – | 136/451 | grenze_ohne_bildkante, klasse_unsicher |
| 435 | 100435 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 396 | 100 % | – | 161/490 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 431 | 100431 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 295 | 100 % | – | 209/486 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 406 | 100406 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 13208 | 68 % | v4 | 245/458 | grenze_ohne_bildkante, klasse_unsicher |
| 439 | 100439 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 627 | 100 % | – | 275/497 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 457 | 100457 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 30 | 100 % | – | 65/543 | klasse_unsicher |
| 461 | 100461 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 322 | 100 % | – | 109/546 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 458 | 100458 | 1.2.1 Straße (versiegelt) | ja | nein | 151 | 100 % | – | 121/540 | grenze_ohne_bildkante |
| 425 | 100425 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 6622 | 100 % | – | 125/506 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 453 | 100453 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 721 | 100 % | – | 167/539 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 455 | 100455 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 128 | 100 % | – | 195/533 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 448 | 100448 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 125 | 100 % | – | 197/523 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 443 | 100443 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 131 | 100 % | – | 211/509 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 451 | 100451 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 1023 | 100 % | – | 228/539 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 444 | 100444 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 400 | 100 % | – | 245/521 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 452 | 100452 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 281 | 100 % | – | 268/530 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 459 | 100459 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 154 | 100 % | – | 268/542 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 438 | 100438 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 7226 | 51 % | v4 | 294/536 | grenze_ohne_bildkante, klasse_unsicher |
| 463 | 100463 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 136 | 100 % | – | 75/558 | klasse_unsicher |

`nicht_geprueft` nennt, was du nicht angesehen hast, `offen`, was du nicht entscheiden konntest.

Kontrolle vor der Rückgabe (muss mit `ok` enden):

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-2/skripte/pruefe_urteil.py --urteil C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil-gegenprobe/r0c0/v3/urteil.json --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r0c0/segmente.json --fassung c --viertel v3 --ids 100351,100341,100349,100362,100371,100367,100353,100407,100385,100409,100414,100402,100432,100429,100379,100435,100431,100406,100439,100457,100461,100458,100425,100453,100455,100448,100443,100451,100444,100452,100459,100438,100463 --kategorien C:/Users/Phil/Developement/Victor/landseg/kategorien.json
```

## Unabhängig urteilen

Du bist die Gegenprobe: Ein anderer Agent urteilt über dasselbe Viertel. Sein Ergebnis (`C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/`) siehst du nicht an, auch nicht, wenn es schon da ist. Aus beiden Urteilen wird die Übereinstimmung gemessen.

## Werkzeuge

Befehle im Ordner `C:/Users/Phil/Developement/Victor/landseg` mit `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -m landseg <befehl>`; Aufruf und Schalter stehen in
`C:/Users/Phil/Developement/Victor/landseg/README.md`. Die Bilder deines Viertels liegen fertig vor (Abschnitt „Dein Viertel“); `ansicht` (W3) erzeugt Bilder
je Segment und ist hier keine Urteilsgrundlage. Für fragliche Grenzen `kante` (W4, hier nur zum Ansehen
der Bildkante), zur Kontrolle `pruefen`. Eigene Skripte als Datei in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil-gegenprobe/r0c0/v3`.

## Ergebnis in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil-gegenprobe/r0c0/v3` (genau diese Namen)

- `roh.jpg`, `umriss.jpg` (alle Segmentgrenzen mit ID), `maengel.jpg` (nummerierte Punkte mit kurzer
  deutscher Beschriftung, sonst Vermerk „keine Mängel“), `vorschlag.jpg` (Grenzen und Klassen, wie
  du sie setzen würdest, sonst Vermerk „unverändert“): je dein Viertel mit Umgebung, Viertel
  umrandet (Grundlage: die vorbereiteten Übersichtsbilder).
- `nah_<n>.jpg`: eigene Nahansichten von Stellen, die man in den vorbereiteten Bildern nicht beurteilen kann,
  je ein Teil des Viertels samt Nachbarn (mindestens 64 × 64 Bildpunkte der Teilkachel, kein freigestelltes
  Einzelsegment); `kontrast_<n>.jpg` bei blassen Stellen.
- `urteil.json` (UTF-8):

```
{"teilkachel": "r0c0", "viertel": "v3", "bearbeiter": "gegen-c-r0c0-v3",
 "bilder_angesehen": {"uebersicht": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r0c0/ganz_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c0/v3/uebersicht_nummern.jpg", "…"],
                      "nah": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c0/v3/nah1_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil-gegenprobe/r0c0/v3/nah_1.jpg", "…"]},
 "segmente": [{"id": 17, "klasse_heute": "Code", "was_ist_es": "ein Satz",
               "urteil": "sauber" | "nicht_sauber", "klasse_vorschlag": "Code oder null",
               "sicher": true | false,
               "punkte": [{"nr": 1, "art": "fremdes|fehlt|trennen|verschmelzen|grenze|klasse|zu_klein|sonstiges",
                           "text": "ein Satz mit Stelle (x/y im Teilkachelbild)", "flaeche_px": Zahl oder null}],
               "bilder": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c0/v3/uebersicht_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c0/v3/nah2_roh.jpg"]}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "was an der Kerngrenze nicht passt"}],
 "unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."]}
```

Jedes Segment deiner Liste steht genau einmal unter `segmente`, auch die sauberen, in der Reihenfolge der Liste. Segmente der Nachbarviertel (graue Nummern) und des Kontextrands (ohne Nummer) urteilst du in diesem Auftrag nicht; Auffälliges an ihnen nennst du unter `unsicher` mit ID.

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Punkte, Anteil `sicher: false`, wo du unsicher bist.
