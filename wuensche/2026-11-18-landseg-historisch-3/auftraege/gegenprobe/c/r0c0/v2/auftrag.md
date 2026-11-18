# Auftrag: H0, Teilkachel r0c0, Viertel v2: 67 Segmente im Verbund ansehen und einzeln urteilen (Fassung C „Feste Kategorienliste“)

Lies zuerst den Skill `landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `r0c0` des Ausschnitts in `C:/Users/Phil/Developement/Victor/daten/landseg/H0`. Du urteilst über jedes
Segment deines Viertels v2 (Liste unter „Dein Viertel“), ob Grenze und Klasse stimmen, und zeichnest ein, was
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

Viertel v2 (oben rechts) des Kerns von `r0c0`: x 314–563, y 64–313 im
Teilkachelbild (250 × 250 Bildpunkte). Dir gehören die 67 Segmente der Liste unten: Jedes hat den
größten Teil seiner Kernfläche in diesem Viertel. Die Teilkachel hat 173 Kernsegmente
(v1 58, v2 67, v3 14, v4 34); die anderen Viertel stehen in eigenen Aufträgen mit eigenem Ergebnisordner. Ein Segment
über einer Viertelgrenze urteilt nur das Viertel mit dem größten Anteil; in den Bildern der Nachbarn ist
es mit grauer Nummer als Umgebung zu sehen.

Urteil im Verbund: Du siehst das Viertel als zusammenhängendes Bild mit Umgebung, arbeitest die Liste der
Reihe nach ab und beurteilst jedes Segment im Zusammenhang mit seinen Nachbarn; eingetragen wird jedes
Segment einzeln (Klasse, `sicher`, `was_ist_es` als Notiz). Bilder freigestellter Einzelsegmente gibt es
nicht, und sie sind keine Urteilsgrundlage.

Bilder des Viertels (fertig, JPEG, in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c0/v2`, Fenster und Vergrößerung je Bild in `viertel.json`):

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
| 45 | 100045 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1496 | 99 % | v1 | 339/87 | grenze_ohne_bildkante, klasse_unsicher |
| 41 | 100041 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 650 | 100 % | – | 355/71 | grenze_ohne_bildkante |
| 37 | 100037 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1950 | 100 % | – | 391/88 | klasse_unsicher |
| 28 | 100028 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1903 | 100 % | – | 437/76 | klasse_unsicher |
| 50 | 100050 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 119 | 100 % | – | 469/67 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 12 | 100012 | 2.1 Acker mit Bewuchs | ja | ja | 343 | 100 % | – | 483/73 | grenze_ohne_bildkante |
| 53 | 100053 | 2.1 Acker mit Bewuchs | nein | ja | 213 | 100 % | – | 495/79 | grenze_ohne_bildkante, klasse_unsicher |
| 54 | 100054 | 1.3.2 Baustelle | nein | nein | 164 | 100 % | – | 505/78 | grenze_ohne_bildkante, klasse_unsicher |
| 60 | 100060 | 1.2.1 Straße (versiegelt) | nein | nein | 538 | 100 % | – | 506/97 | grenze_ohne_bildkante, klasse_unsicher |
| 49 | 100049 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 141 | 100 % | – | 507/68 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 20 | 100020 | 1.3.2 Baustelle | nein | nein | 7 | 100 % | – | 518/64 | grenze_ohne_bildkante, klasse_unsicher |
| 46 | 100046 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 251 | 100 % | – | 524/69 | grenze_ohne_bildkante, klasse_unsicher |
| 56 | 100056 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 829 | 100 % | – | 544/90 | grenze_ohne_bildkante |
| 42 | 100042 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 586 | 100 % | – | 548/72 | grenze_ohne_bildkante, klasse_unsicher |
| 73 | 100073 | 1.2.1 Straße (versiegelt) | nein | nein | 1478 | 100 % | v1 | 331/121 | klasse_unsicher |
| 89 | 100089 | 1.3.2 Baustelle | nein | nein | 93 | 100 % | – | 337/139 | klasse_unsicher |
| 71 | 100071 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 237 | 100 % | – | 345/114 | grenze_ohne_bildkante, klasse_unsicher |
| 82 | 100082 | 1.3.2 Baustelle | nein | nein | 94 | 100 % | – | 356/136 | klasse_unsicher |
| 66 | 100066 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 2497 | 100 % | – | 375/119 | grenze_ohne_bildkante, klasse_unsicher |
| 62 | 100062 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 2591 | 100 % | – | 424/132 | klasse_unsicher |
| 84 | 100084 | 1.2.1 Straße (versiegelt) | nein | nein | 111 | 100 % | – | 445/138 | klasse_unsicher, nicht_zusammenhaengend |
| 86 | 100086 | 1.2.1 Straße (versiegelt) | nein | nein | 206 | 100 % | – | 476/138 | klasse_unsicher, nicht_zusammenhaengend |
| 69 | 100069 | 1.2.1 Straße (versiegelt) | ja | nein | 518 | 100 % | – | 477/113 | – |
| 87 | 100087 | 2.1 Acker mit Bewuchs | nein | ja | 145 | 100 % | – | 492/139 | grenze_ohne_bildkante, klasse_unsicher |
| 30 | 100030 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 4149 | 100 % | – | 497/119 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 79 | 100079 | 1.2.1 Straße (versiegelt) | ja | nein | 138 | 100 % | – | 530/126 | – |
| 63 | 100063 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 931 | 100 % | – | 532/107 | grenze_ohne_bildkante, klasse_unsicher |
| 32 | 100032 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 505 | 100 % | – | 553/119 | grenze_ohne_bildkante, klasse_unsicher |
| 81 | 100081 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 265 | 100 % | – | 556/132 | klasse_unsicher |
| 70 | 100070 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 45 | 100 % | – | 561/115 | klasse_unsicher |
| 94 | 100094 | 1.3.2 Baustelle | nein | nein | 394 | 100 % | – | 332/152 | grenze_ohne_bildkante, klasse_unsicher |
| 100 | 100100 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1173 | 100 % | – | 351/172 | klasse_unsicher |
| 110 | 100110 | 1.3.2 Baustelle | nein | nein | 84 | 100 % | – | 377/178 | klasse_unsicher |
| 109 | 100109 | 1.2.1 Straße (versiegelt) | nein | nein | 439 | 100 % | – | 403/178 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 96 | 100096 | 1.2.1 Straße (versiegelt) | nein | nein | 426 | 100 % | – | 453/155 | grenze_ohne_bildkante, klasse_unsicher |
| 95 | 100095 | 2.1 Acker mit Bewuchs | ja | ja | 117 | 100 % | – | 471/151 | grenze_ohne_bildkante |
| 125 | 100125 | 2.1 Acker mit Bewuchs | nein | ja | 122 | 100 % | – | 505/199 | grenze_ohne_bildkante, klasse_unsicher |
| 83 | 100083 | 2.1 Acker mit Bewuchs | ja | ja | 7190 | 100 % | – | 509/166 | grenze_ohne_bildkante |
| 111 | 100111 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 1026 | 100 % | – | 538/198 | grenze_ohne_bildkante |
| 107 | 100107 | 2.1 Acker mit Bewuchs | nein | ja | 215 | 100 % | – | 546/176 | grenze_ohne_bildkante, klasse_unsicher |
| 92 | 100092 | 1.2.1 Straße (versiegelt) | nein | nein | 174 | 100 % | – | 557/156 | klasse_unsicher |
| 112 | 100112 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 56 | 100 % | – | 561/191 | grenze_ohne_bildkante, klasse_unsicher |
| 104 | 100104 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 7925 | 71 % | v1 | 365/222 | grenze_ohne_bildkante, klasse_unsicher |
| 137 | 100137 | 1.3.2 Baustelle | nein | nein | 129 | 100 % | – | 397/230 | grenze_ohne_bildkante, klasse_unsicher |
| 117 | 100117 | 1.2.1 Straße (versiegelt) | nein | nein | 602 | 100 % | – | 411/239 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 126 | 100126 | 1.2.1 Straße (versiegelt) | ja | nein | 102 | 100 % | – | 412/213 | grenze_ohne_bildkante |
| 145 | 100145 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 754 | 100 % | – | 439/249 | grenze_ohne_bildkante, klasse_unsicher |
| 141 | 100141 | 1.3.2 Baustelle | nein | nein | 218 | 100 % | – | 454/238 | grenze_ohne_bildkante, klasse_unsicher |
| 139 | 100139 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 122 | 100 % | – | 466/235 | grenze_ohne_bildkante, klasse_unsicher |
| 130 | 100130 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 326 | 100 % | – | 472/212 | klasse_unsicher |
| 127 | 100127 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 630 | 100 % | – | 497/215 | klasse_unsicher |
| 128 | 100128 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 2490 | 100 % | – | 538/225 | grenze_ohne_bildkante, klasse_unsicher |
| 148 | 100148 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 598 | 79 % | v1 | 324/254 | klasse_unsicher |
| 156 | 100156 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 742 | 100 % | – | 331/273 | grenze_ohne_bildkante, klasse_unsicher |
| 164 | 100164 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 99 | 100 % | – | 335/285 | grenze_ohne_bildkante, klasse_unsicher |
| 151 | 100151 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 128 | 100 % | – | 345/256 | grenze_ohne_bildkante, klasse_unsicher |
| 155 | 100155 | 2.1 Acker mit Bewuchs | nein | ja | 83 | 100 % | – | 375/259 | grenze_ohne_bildkante, klasse_unsicher |
| 150 | 100150 | 2.1 Acker mit Bewuchs | nein | ja | 149 | 100 % | – | 404/252 | grenze_ohne_bildkante, klasse_unsicher |
| 161 | 100161 | 2.1 Acker mit Bewuchs | nein | ja | 142 | 100 % | – | 411/275 | grenze_ohne_bildkante, klasse_unsicher |
| 166 | 100166 | 1.3.2 Baustelle | nein | nein | 122 | 100 % | – | 419/287 | grenze_ohne_bildkante, klasse_unsicher |
| 149 | 100149 | 1.2.1 Straße (versiegelt) | nein | nein | 1837 | 57 % | v4 | 428/278 | grenze_ohne_bildkante, klasse_unsicher |
| 158 | 100158 | 1.3.2 Baustelle | nein | nein | 114 | 100 % | – | 440/269 | klasse_unsicher |
| 142 | 100142 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1905 | 100 % | – | 476/266 | klasse_unsicher |
| 167 | 100167 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 980 | 98 % | v4 | 501/296 | klasse_unsicher |
| 144 | 100144 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1150 | 100 % | – | 529/274 | klasse_unsicher |
| 169 | 100169 | 4.2.4 Gebüsch / Strauchfläche | nein | ja | 184 | 100 % | – | 426/303 | klasse_unsicher |
| 153 | 100153 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 963 | 80 % | v4 | 549/304 | klasse_unsicher |

`nicht_geprueft` nennt, was du nicht angesehen hast, `offen`, was du nicht entscheiden konntest.

Kontrolle vor der Rückgabe (muss mit `ok` enden):

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/skripte/pruefe_urteil.py --urteil C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil-gegenprobe/r0c0/v2/urteil.json --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/segmente.json --fassung c --viertel v2 --ids 100045,100041,100037,100028,100050,100012,100053,100054,100060,100049,100020,100046,100056,100042,100073,100089,100071,100082,100066,100062,100084,100086,100069,100087,100030,100079,100063,100032,100081,100070,100094,100100,100110,100109,100096,100095,100125,100083,100111,100107,100092,100112,100104,100137,100117,100126,100145,100141,100139,100130,100127,100128,100148,100156,100164,100151,100155,100150,100161,100166,100149,100158,100142,100167,100144,100169,100153 --kategorien C:/Users/Phil/Developement/Victor/landseg/kategorien.json
```

## Nachsegmentieren (Entscheidung des Nutzers 2026-11-18)
Die Vorstufe ist bewusst grob. Fasst ein Segment sichtbar mehrere Objekte zusammen (Häuserzeile, Hof mit Garten, Acker mit Weg oder Rain, Baumgruppe mit Wiese), teilst du es selbst, BEVOR du es urteilst — direkt, ohne Umweg:
- Alle Eingriffe eines Viertels in EINEM Stapel: `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg eingriff --labels <Karte> --segmente <segmente.json> --bearbeiter <dein Name> stapel --datei <ergebnisordner>/eingriffe.json` mit Schritten `teilen` (Linienzug entlang der sichtbaren Bildkante), `polygon` (Fläche an Nachbarn oder neues Segment mit Klasse) oder `verschmelzen` (eine Fläche, zwei Stücke ohne Kante). Koordinaten in Bildpunkten der Teilkachel.
- Sitzt eine Linie nicht genau auf der Kante: `kante` (README) zum Einrasten. Danach `pruefen` — die Karte muss lückenlos bleiben.
- Neue IDs aus dem Stapel-Ergebnis urteilst du im selben urteil.json; jede Teilung steht dort unter "eingriffe" mit IDs vorher/nachher und Grund in einem Satz.
- Nur teilen, wo Objekte im Bild klar getrennt sind; kein Feinschliff an brauchbaren Grenzen, keine Teilung nach Vermutung. Unklare Mischflächen: nicht teilen, `sicher: false`, Notiz unter "offen".
- Zur Kontrolle eine Nahansicht der geänderten Stelle (`ansicht` oder eigenes Bild aus Karte und Teilkachelbild) einmal ansehen.

Karte zum Nachsegmentieren: `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/labels.tif` und `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/segmente.json`

So konkret (Befehle im Ordner `C:/Users/Phil/Developement/Victor/landseg`, dein Name `gegen-c-r0c0-v2`, Teilkachelbild `C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r0c0.png`):

- Stapeldatei `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil-gegenprobe/r0c0/v2/eingriffe.json`: `{"schritte": [{"op": "teilen", "id": 4, "linie": [[x, y], [x, y]]},
  {"op": "polygon_zuweisen", "flaeche": [[x, y], [x, y], [x, y]], "id": 7}, {"op": "polygon_zuweisen",
  "flaeche": [[x, y], …], "klasse": "Code"}, {"op": "verschmelzen", "ids": [3, 5]}]}` (im Stapel heißt
  `polygon` `polygon_zuweisen`; `klasse` braucht einen Code aus `kategorien.json`). Alles oder nichts: Schlägt ein Schritt fehl, bleibt die
  Karte unverändert; Datei korrigieren und erneut ausführen. Das Ergebnis nennt je Schritt `behalten`/`neu`
  bzw. `aufgeteilt_neu`; beim Teilen behält das größte Stück die ID.
- `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg eingriff --labels C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/labels.tif --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/segmente.json --bearbeiter gegen-c-r0c0-v2 stapel --datei C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil-gegenprobe/r0c0/v2/eingriffe.json`
- Einrasten: `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg kante --labels C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/labels.tif --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/segmente.json --bild C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r0c0.png --bearbeiter gegen-c-r0c0-v2 --a <ID> --b <ID>`
- Kontrolle: `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg pruefen --labels C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/labels.tif --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/segmente.json --bild C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r0c0.png` (muss mit `ok` enden).
- Nahansicht: `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg ansicht --manifest C:/Users/Phil/Developement/Victor/daten/landseg/H0/manifest.json --teilkachel r0c0 --labels C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/labels.tif --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/segmente.json --ziel C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil-gegenprobe/r0c0/v2/ansicht --ids <neue IDs>`
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
nur an Linien aus deinem Nachsegmentieren), zur Kontrolle `pruefen`. Eigene Skripte als Datei in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil-gegenprobe/r0c0/v2`.

## Ergebnis in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil-gegenprobe/r0c0/v2` (genau diese Namen)

- `roh.jpg`, `umriss.jpg` (alle Segmentgrenzen mit ID), `maengel.jpg` (nummerierte Punkte mit kurzer
  deutscher Beschriftung, sonst Vermerk „keine Mängel“), `vorschlag.jpg` (Grenzen und Klassen, wie
  du sie setzen würdest, sonst Vermerk „unverändert“): je dein Viertel mit Umgebung, Viertel
  umrandet (Grundlage: die vorbereiteten Übersichtsbilder).
- `nah_<n>.jpg`: eigene Nahansichten von Stellen, die man in den vorbereiteten Bildern nicht beurteilen kann,
  je ein Teil des Viertels samt Nachbarn (mindestens 64 × 64 Bildpunkte der Teilkachel, kein freigestelltes
  Einzelsegment); `kontrast_<n>.jpg` bei blassen Stellen.
- `urteil.json` (UTF-8):

```
{"teilkachel": "r0c0", "viertel": "v2", "bearbeiter": "gegen-c-r0c0-v2",
 "bilder_angesehen": {"uebersicht": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r0c0/ganz_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c0/v2/uebersicht_nummern.jpg", "…"],
                      "nah": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c0/v2/nah1_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil-gegenprobe/r0c0/v2/nah_1.jpg", "…"]},
 "segmente": [{"id": 17, "klasse_heute": "Code", "was_ist_es": "ein Satz",
               "urteil": "sauber" | "nicht_sauber", "klasse_vorschlag": "Code oder null",
               "sicher": true | false,
               "punkte": [{"nr": 1, "art": "fremdes|fehlt|trennen|verschmelzen|grenze|klasse|zu_klein|sonstiges",
                           "text": "ein Satz mit Stelle (x/y im Teilkachelbild)", "flaeche_px": Zahl oder null}],
               "bilder": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c0/v2/uebersicht_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c0/v2/nah2_roh.jpg"]}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "was an der Kerngrenze nicht passt"}],
 "unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."],
 "eingriffe": [{"schritt": "teilen", "vorher": [ID], "nachher": [ID, ID], "grund": "ein Satz"}]}
```

Jedes Segment deiner Liste steht genau einmal unter `segmente`, auch die sauberen, in der Reihenfolge der Liste. Segmente der Nachbarviertel (graue Nummern) und des Kontextrands (ohne Nummer) urteilst du in diesem Auftrag nicht; Auffälliges an ihnen nennst du unter `unsicher` mit ID.

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Punkte, Anteil `sicher: false`, wo du unsicher bist.
