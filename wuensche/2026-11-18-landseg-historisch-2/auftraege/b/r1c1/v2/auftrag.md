# Auftrag: H0, Teilkachel r1c1, Viertel v2: 147 Segmente im Verbund ansehen und einzeln urteilen (Fassung B „Kategorien frei“)

Lies zuerst den Skill `landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `r1c1` des Ausschnitts in `C:/Users/Phil/Developement/Victor/daten/landseg/H0`. Du urteilst über jedes
Segment deines Viertels v2 (Liste unter „Dein Viertel“), ob Grenze und Klasse stimmen, und zeichnest ein, was
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

Viertel v2 (oben rechts) des Kerns von `r1c1`: x 314–563, y 64–313 im
Teilkachelbild (250 × 250 Bildpunkte). Dir gehören die 147 Segmente der Liste unten: Jedes hat den
größten Teil seiner Kernfläche in diesem Viertel. Die Teilkachel hat 518 Kernsegmente
(v1 131, v2 147, v3 67, v4 173); die anderen Viertel stehen in eigenen Aufträgen mit eigenem Ergebnisordner. Ein Segment
über einer Viertelgrenze urteilt nur das Viertel mit dem größten Anteil; in den Bildern der Nachbarn ist
es mit grauer Nummer als Umgebung zu sehen.

Urteil im Verbund: Du siehst das Viertel als zusammenhängendes Bild mit Umgebung, arbeitest die Liste der
Reihe nach ab und beurteilst jedes Segment im Zusammenhang mit seinen Nachbarn; eingetragen wird jedes
Segment einzeln (Klasse, `sicher`, `was_ist_es` als Notiz). Bilder freigestellter Einzelsegmente gibt es
nicht, und sie sind keine Urteilsgrundlage.

Bilder des Viertels (fertig, JPEG, in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c1/v2`, Fenster und Vergrößerung je Bild in `viertel.json`):

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
| 60 | 400060 | 1.3.2 Baustelle | nein | nein | 2278 | 68 % | v1 | 321/71 | klasse_unsicher, nicht_zusammenhaengend |
| 121 | 400121 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 81 | 100 % | – | 322/94 | klasse_unsicher, nicht_zusammenhaengend |
| 103 | 400103 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 203 | 100 % | – | 337/77 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 119 | 400119 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 513 | 100 % | – | 343/93 | grenze_ohne_bildkante, klasse_unsicher |
| 123 | 400123 | 1.2.1 Straße (versiegelt) | nein | nein | 282 | 100 % | – | 357/87 | klasse_unsicher, nicht_zusammenhaengend |
| 90 | 400090 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 255 | 100 % | – | 358/70 | klasse_unsicher |
| 118 | 400118 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 424 | 100 % | – | 366/92 | klasse_unsicher |
| 80 | 400080 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 489 | 100 % | – | 391/71 | klasse_unsicher |
| 17 | 400017 | 6.6 Weg, unbefestigt (Feld-, Wald-, Schotterweg) | nein | nein | 257 | 100 % | – | 412/71 | grenze_ohne_bildkante, klasse_unsicher |
| 85 | 400085 | 1.3.2 Baustelle | nein | nein | 22 | 100 % | – | 420/65 | klasse_unsicher, nicht_zusammenhaengend |
| 110 | 400110 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 252 | 100 % | – | 421/82 | klasse_unsicher |
| 75 | 400075 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 752 | 100 % | – | 439/73 | grenze_ohne_bildkante, klasse_unsicher |
| 120 | 400120 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 118 | 100 % | – | 452/84 | klasse_unsicher |
| 116 | 400116 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 1579 | 100 % | – | 460/99 | klasse_unsicher |
| 101 | 400101 | 1.2.1 Straße (versiegelt) | nein | nein | 359 | 100 % | – | 470/77 | klasse_unsicher |
| 71 | 400071 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 142 | 100 % | – | 479/67 | klasse_unsicher |
| 76 | 400076 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 650 | 100 % | – | 494/75 | grenze_ohne_bildkante, klasse_unsicher |
| 107 | 400107 | 1.2.1 Straße (versiegelt) | nein | nein | 295 | 100 % | – | 513/79 | grenze_ohne_bildkante, klasse_unsicher |
| 115 | 400115 | 1.2.1 Straße (versiegelt) | nein | nein | 140 | 100 % | – | 532/89 | grenze_ohne_bildkante, klasse_unsicher |
| 96 | 400096 | 1.2.1 Straße (versiegelt) | nein | nein | 539 | 100 % | – | 541/80 | klasse_unsicher |
| 62 | 400062 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 120 | 100 % | – | 544/67 | grenze_ohne_bildkante, klasse_unsicher |
| 104 | 400104 | 4.2.4 Gebüsch / Strauchfläche | nein | ja | 320 | 100 % | – | 557/86 | klasse_unsicher |
| 99 | 400099 | 4.2.1 Einzelbaum | nein | ja | 50 | 100 % | – | 561/66 | grenze_ohne_bildkante, klasse_unsicher |
| 166 | 400166 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 401 | 82 % | v1 | 320/125 | klasse_unsicher |
| 174 | 400174 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 257 | 100 % | – | 334/138 | klasse_unsicher, nicht_zusammenhaengend |
| 122 | 400122 | 1.2.1 Straße (versiegelt) | nein | nein | 577 | 100 % | – | 336/112 | klasse_unsicher |
| 157 | 400157 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 138 | 100 % | – | 351/120 | klasse_unsicher, nicht_zusammenhaengend |
| 153 | 400153 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 196 | 100 % | – | 359/115 | klasse_unsicher |
| 180 | 400180 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 347 | 100 % | – | 372/140 | klasse_unsicher |
| 167 | 400167 | 1.2.1 Straße (versiegelt) | nein | nein | 147 | 100 % | – | 378/126 | klasse_unsicher, nicht_zusammenhaengend |
| 139 | 400139 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 345 | 100 % | – | 387/112 | klasse_unsicher |
| 155 | 400155 | 1.3.2 Baustelle | nein | nein | 799 | 100 % | – | 396/125 | klasse_unsicher, nicht_zusammenhaengend |
| 140 | 400140 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 675 | 100 % | – | 406/108 | klasse_unsicher |
| 178 | 400178 | 1.2.1 Straße (versiegelt) | nein | nein | 305 | 100 % | – | 406/135 | klasse_unsicher, nicht_zusammenhaengend |
| 191 | 400191 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 102 | 100 % | – | 415/143 | klasse_unsicher |
| 158 | 400158 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 199 | 100 % | – | 420/117 | – |
| 151 | 400151 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 294 | 100 % | – | 423/136 | – |
| 188 | 400188 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 426 | 100 % | – | 428/149 | klasse_unsicher |
| 135 | 400135 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 312 | 100 % | – | 433/101 | klasse_unsicher |
| 131 | 400131 | 1.2.1 Straße (versiegelt) | nein | nein | 273 | 100 % | – | 447/115 | klasse_unsicher |
| 169 | 400169 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 774 | 100 % | – | 449/140 | klasse_unsicher |
| 162 | 400162 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 84 | 100 % | – | 455/113 | klasse_unsicher |
| 168 | 400168 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 277 | 100 % | – | 460/131 | grenze_ohne_bildkante, klasse_unsicher |
| 172 | 400172 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 186 | 100 % | – | 474/135 | klasse_unsicher |
| 156 | 400156 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 504 | 100 % | – | 480/123 | klasse_unsicher |
| 190 | 400190 | 1.2.1 Straße (versiegelt) | nein | nein | 79 | 100 % | – | 483/140 | klasse_unsicher |
| 150 | 400150 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 75 | 100 % | – | 493/102 | klasse_unsicher |
| 152 | 400152 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 778 | 100 % | – | 500/127 | grenze_ohne_bildkante, klasse_unsicher |
| 159 | 400159 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 154 | 100 % | – | 508/113 | grenze_ohne_bildkante, klasse_unsicher |
| 149 | 400149 | 1.2.1 Straße (versiegelt) | nein | nein | 176 | 100 % | – | 512/104 | grenze_ohne_bildkante, klasse_unsicher |
| 176 | 400176 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 774 | 100 % | – | 517/147 | klasse_unsicher |
| 154 | 400154 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 179 | 100 % | – | 522/112 | grenze_ohne_bildkante, klasse_unsicher |
| 173 | 400173 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 226 | 100 % | – | 526/131 | klasse_unsicher |
| 163 | 400163 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 691 | 100 % | – | 537/120 | grenze_ohne_bildkante, klasse_unsicher |
| 142 | 400142 | 6.6 Weg, unbefestigt (Feld-, Wald-, Schotterweg) | nein | nein | 320 | 100 % | – | 545/106 | klasse_unsicher |
| 184 | 400184 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 285 | 100 % | – | 545/147 | klasse_unsicher |
| 160 | 400160 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 268 | 100 % | – | 556/118 | klasse_unsicher |
| 126 | 400126 | 4.2.4 Gebüsch / Strauchfläche | nein | ja | 4 | 100 % | – | 561/110 | grenze_ohne_bildkante, klasse_unsicher |
| 143 | 400143 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 50 | 100 % | – | 562/101 | klasse_unsicher |
| 244 | 400244 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 200 | 100 % | – | 330/199 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 224 | 400224 | 1.3.2 Baustelle | nein | nein | 113 | 100 % | – | 345/176 | klasse_unsicher, nicht_zusammenhaengend |
| 182 | 400182 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 935 | 100 % | – | 350/151 | klasse_unsicher |
| 195 | 400195 | 1.2.1 Straße (versiegelt) | nein | nein | 593 | 100 % | – | 356/170 | klasse_unsicher, nicht_zusammenhaengend |
| 217 | 400217 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 620 | 100 % | – | 363/184 | klasse_unsicher |
| 225 | 400225 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 312 | 100 % | – | 381/181 | klasse_unsicher |
| 211 | 400211 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 165 | 100 % | – | 389/159 | klasse_unsicher, nicht_zusammenhaengend |
| 230 | 400230 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 860 | 100 % | – | 396/199 | klasse_unsicher |
| 200 | 400200 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 329 | 100 % | – | 403/152 | klasse_unsicher |
| 210 | 400210 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 213 | 100 % | – | 410/163 | klasse_unsicher |
| 223 | 400223 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 297 | 100 % | – | 432/176 | klasse_unsicher |
| 209 | 400209 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 325 | 100 % | – | 434/162 | klasse_unsicher, nicht_zusammenhaengend |
| 236 | 400236 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 192 | 100 % | – | 434/187 | klasse_unsicher, nicht_zusammenhaengend |
| 240 | 400240 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 697 | 100 % | – | 443/195 | grenze_ohne_bildkante, klasse_unsicher |
| 199 | 400199 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 532 | 100 % | – | 458/156 | klasse_unsicher |
| 216 | 400216 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 1776 | 100 % | – | 476/196 | grenze_ohne_bildkante, klasse_unsicher |
| 193 | 400193 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 806 | 100 % | – | 489/167 | grenze_ohne_bildkante, klasse_unsicher |
| 187 | 400187 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 950 | 100 % | – | 498/154 | klasse_unsicher |
| 237 | 400237 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 546 | 100 % | – | 502/190 | klasse_unsicher |
| 231 | 400231 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 175 | 100 % | – | 503/177 | klasse_unsicher |
| 196 | 400196 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1045 | 100 % | – | 529/176 | klasse_unsicher |
| 203 | 400203 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 751 | 100 % | – | 535/193 | grenze_ohne_bildkante, klasse_unsicher |
| 212 | 400212 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 625 | 100 % | – | 553/194 | grenze_ohne_bildkante, klasse_unsicher |
| 294 | 400294 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 779 | 67 % | v1 | 322/249 | grenze_ohne_bildkante, klasse_unsicher |
| 261 | 400261 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 230 | 100 % | – | 326/217 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 288 | 400288 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 85 | 100 % | – | 326/229 | klasse_unsicher |
| 269 | 400269 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 765 | 100 % | – | 342/228 | klasse_unsicher |
| 300 | 400300 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 163 | 100 % | – | 344/247 | klasse_unsicher, nicht_zusammenhaengend |
| 243 | 400243 | 1.3.2 Baustelle | nein | nein | 170 | 100 % | – | 355/205 | klasse_unsicher, nicht_zusammenhaengend |
| 272 | 400272 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 86 | 100 % | – | 362/215 | klasse_unsicher |
| 221 | 400221 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 714 | 100 % | – | 367/202 | klasse_unsicher, nicht_zusammenhaengend |
| 271 | 400271 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 261 | 100 % | – | 376/219 | klasse_unsicher |
| 289 | 400289 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 141 | 100 % | – | 379/234 | klasse_unsicher, nicht_zusammenhaengend |
| 273 | 400273 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 102 | 100 % | – | 390/214 | klasse_unsicher, nicht_zusammenhaengend |
| 296 | 400296 | 4.2.1 Einzelbaum | nein | ja | 363 | 100 % | – | 395/242 | grenze_ohne_bildkante, klasse_unsicher |
| 279 | 400279 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 460 | 100 % | – | 397/223 | grenze_ohne_bildkante, klasse_unsicher |
| 245 | 400245 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 103 | 100 % | – | 412/201 | klasse_unsicher, nicht_zusammenhaengend |
| 252 | 400252 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 179 | 100 % | – | 413/212 | grenze_ohne_bildkante, klasse_unsicher |
| 307 | 400307 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 560 | 100 % | – | 415/249 | grenze_ohne_bildkante, klasse_unsicher |
| 286 | 400286 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 251 | 100 % | – | 416/229 | klasse_unsicher |
| 301 | 400301 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 288 | 100 % | – | 441/247 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 253 | 400253 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 275 | 100 % | – | 443/212 | klasse_unsicher, nicht_zusammenhaengend |
| 257 | 400257 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 1267 | 100 % | – | 459/223 | grenze_ohne_bildkante, klasse_unsicher |
| 283 | 400283 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 220 | 100 % | – | 480/226 | klasse_unsicher, nicht_zusammenhaengend |
| 248 | 400248 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 1762 | 100 % | – | 504/236 | grenze_ohne_bildkante, klasse_unsicher |
| 258 | 400258 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 780 | 100 % | – | 522/211 | grenze_ohne_bildkante, klasse_unsicher |
| 298 | 400298 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 100 | 100 % | – | 531/244 | klasse_unsicher |
| 276 | 400276 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 181 | 100 % | – | 543/224 | grenze_ohne_bildkante, klasse_unsicher |
| 297 | 400297 | 1.2.1 Straße (versiegelt) | nein | nein | 247 | 100 % | – | 556/243 | klasse_unsicher |
| 265 | 400265 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 297 | 100 % | – | 557/211 | grenze_ohne_bildkante, klasse_unsicher |
| 305 | 400305 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 3 | 100 % | – | 563/242 | grenze_ohne_bildkante, klasse_unsicher |
| 340 | 400340 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 133 | 100 % | – | 322/273 | klasse_unsicher |
| 362 | 400362 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 167 | 88 % | v1 | 325/290 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 344 | 400344 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 461 | 93 % | v1 | 331/278 | grenze_ohne_bildkante, klasse_unsicher |
| 318 | 400318 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 253 | 74 % | v1 | 334/254 | grenze_ohne_bildkante, klasse_unsicher |
| 322 | 400322 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 229 | 100 % | – | 342/261 | klasse_unsicher |
| 333 | 400333 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 955 | 100 % | – | 343/290 | klasse_unsicher |
| 324 | 400324 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 116 | 100 % | – | 356/262 | klasse_unsicher |
| 357 | 400357 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 109 | 100 % | – | 364/287 | klasse_unsicher, nicht_zusammenhaengend |
| 359 | 400359 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 223 | 100 % | – | 373/292 | klasse_unsicher |
| 330 | 400330 | 4.2.4 Gebüsch / Strauchfläche | nein | ja | 181 | 100 % | – | 375/268 | klasse_unsicher |
| 183 | 400183 | 1.2.1 Straße (versiegelt) | nein | nein | 2058 | 100 % | – | 378/252 | klasse_unsicher |
| 314 | 400314 | 1.2.1 Straße (versiegelt) | nein | nein | 1181 | 100 % | – | 409/274 | klasse_unsicher |
| 363 | 400363 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 237 | 100 % | – | 409/291 | klasse_unsicher |
| 328 | 400328 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 132 | 100 % | – | 425/259 | grenze_ohne_bildkante, klasse_unsicher |
| 348 | 400348 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 670 | 100 % | – | 427/286 | klasse_unsicher, nicht_zusammenhaengend |
| 304 | 400304 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 109 | 100 % | – | 429/250 | grenze_ohne_bildkante, klasse_unsicher |
| 347 | 400347 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 777 | 100 % | – | 443/289 | klasse_unsicher |
| 345 | 400345 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 106 | 100 % | – | 452/271 | klasse_unsicher, nicht_zusammenhaengend |
| 295 | 400295 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 822 | 100 % | – | 472/250 | grenze_ohne_bildkante, klasse_unsicher |
| 325 | 400325 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 307 | 100 % | – | 479/268 | klasse_unsicher |
| 311 | 400311 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 2889 | 74 % | v4 | 482/293 | grenze_ohne_bildkante, klasse_unsicher |
| 335 | 400335 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 116 | 100 % | – | 493/268 | klasse_unsicher, nicht_zusammenhaengend |
| 365 | 400365 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 184 | 100 % | – | 497/297 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 326 | 400326 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 141 | 100 % | – | 510/258 | klasse_unsicher |
| 358 | 400358 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 125 | 100 % | – | 511/290 | grenze_ohne_bildkante, klasse_unsicher |
| 366 | 400366 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 182 | 100 % | – | 529/295 | grenze_ohne_bildkante, klasse_unsicher |
| 371 | 400371 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 125 | 100 % | – | 544/297 | grenze_ohne_bildkante, klasse_unsicher |
| 320 | 400320 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 2442 | 60 % | v4 | 545/278 | grenze_ohne_bildkante, klasse_unsicher |
| 317 | 400317 | 6.6 Weg, unbefestigt (Feld-, Wald-, Schotterweg) | nein | nein | 68 | 100 % | – | 555/251 | klasse_unsicher |
| 327 | 400327 | 1.2.1 Straße (versiegelt) | nein | nein | 125 | 100 % | – | 560/261 | klasse_unsicher |
| 351 | 400351 | 1.3.2 Baustelle | nein | nein | 18 | 100 % | – | 562/283 | klasse_unsicher |
| 380 | 400380 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 436 | 48 % | v1, v3, v4 | 320/307 | klasse_unsicher |
| 384 | 400384 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 393 | 49 % | v3, v4 | 334/309 | klasse_unsicher, nicht_zusammenhaengend |
| 369 | 400369 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 747 | 70 % | v4 | 359/305 | grenze_ohne_bildkante, klasse_unsicher |
| 382 | 400382 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 274 | 95 % | v4 | 419/304 | klasse_unsicher |
| 370 | 400370 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 368 | 95 % | v4 | 514/302 | grenze_ohne_bildkante, klasse_unsicher |
| 367 | 400367 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 159 | 100 % | – | 559/304 | klasse_unsicher |

`nicht_geprueft` nennt, was du nicht angesehen hast, `offen`, was du nicht entscheiden konntest.

Kontrolle vor der Rückgabe (muss mit `ok` enden):

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-2/skripte/pruefe_urteil.py --urteil C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c1/v2/urteil.json --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r1c1/segmente.json --fassung b --viertel v2 --ids 400060,400121,400103,400119,400123,400090,400118,400080,400017,400085,400110,400075,400120,400116,400101,400071,400076,400107,400115,400096,400062,400104,400099,400166,400174,400122,400157,400153,400180,400167,400139,400155,400140,400178,400191,400158,400151,400188,400135,400131,400169,400162,400168,400172,400156,400190,400150,400152,400159,400149,400176,400154,400173,400163,400142,400184,400160,400126,400143,400244,400224,400182,400195,400217,400225,400211,400230,400200,400210,400223,400209,400236,400240,400199,400216,400193,400187,400237,400231,400196,400203,400212,400294,400261,400288,400269,400300,400243,400272,400221,400271,400289,400273,400296,400279,400245,400252,400307,400286,400301,400253,400257,400283,400248,400258,400298,400276,400297,400265,400305,400340,400362,400344,400318,400322,400333,400324,400357,400359,400330,400183,400314,400363,400328,400348,400304,400347,400345,400295,400325,400311,400335,400365,400326,400358,400366,400371,400320,400317,400327,400351,400380,400384,400369,400382,400370,400367
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
der Bildkante), zur Kontrolle `pruefen`. Eigene Skripte als Datei in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c1/v2`.

## Ergebnis in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c1/v2` (genau diese Namen)

- `roh.jpg`, `umriss.jpg` (alle Segmentgrenzen mit ID), `maengel.jpg` (nummerierte Punkte mit kurzer
  deutscher Beschriftung, sonst Vermerk „keine Mängel“), `vorschlag.jpg` (Grenzen und Klassen, wie
  du sie setzen würdest, sonst Vermerk „unverändert“): je dein Viertel mit Umgebung, Viertel
  umrandet (Grundlage: die vorbereiteten Übersichtsbilder).
- `nah_<n>.jpg`: eigene Nahansichten von Stellen, die man in den vorbereiteten Bildern nicht beurteilen kann,
  je ein Teil des Viertels samt Nachbarn (mindestens 64 × 64 Bildpunkte der Teilkachel, kein freigestelltes
  Einzelsegment); `kontrast_<n>.jpg` bei blassen Stellen.
- `urteil.json` (UTF-8):

```
{"teilkachel": "r1c1", "viertel": "v2", "bearbeiter": "urt-b-r1c1-v2",
 "bilder_angesehen": {"uebersicht": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r1c1/ganz_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c1/v2/uebersicht_nummern.jpg", "…"],
                      "nah": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c1/v2/nah1_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c1/v2/nah_1.jpg", "…"]},
 "segmente": [{"id": 17, "klasse_heute": "Code", "was_ist_es": "ein Satz",
               "urteil": "sauber" | "nicht_sauber", "klasse_vorschlag": null,
               "klasse_frei": {"grob": "Name", "mittel": "Name", "fein": "Name"},
               "sicher": true | false,
               "punkte": [{"nr": 1, "art": "fremdes|fehlt|trennen|verschmelzen|grenze|klasse|zu_klein|sonstiges",
                           "text": "ein Satz mit Stelle (x/y im Teilkachelbild)", "flaeche_px": Zahl oder null}],
               "bilder": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c1/v2/uebersicht_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c1/v2/nah2_roh.jpg"]}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "was an der Kerngrenze nicht passt"}],
 "unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."],
 "klassen_frei": [{"name": "Name", "ebene": "grob|mittel|fein", "eltern": "Name oder null", "merkmal": "woran im Bild erkennbar"}]}
```

Jedes Segment deiner Liste steht genau einmal unter `segmente`, auch die sauberen, in der Reihenfolge der Liste. Segmente der Nachbarviertel (graue Nummern) und des Kontextrands (ohne Nummer) urteilst du in diesem Auftrag nicht; Auffälliges an ihnen nennst du unter `unsicher` mit ID.

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Punkte, Anteil `sicher: false`, wo du unsicher bist.
