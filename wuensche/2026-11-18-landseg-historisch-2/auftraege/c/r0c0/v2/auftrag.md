# Auftrag: H0, Teilkachel r0c0, Viertel v2: 139 Segmente im Verbund ansehen und einzeln urteilen (Fassung C „Feste Kategorienliste“)

Lies zuerst den Skill `landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `r0c0` des Ausschnitts in `C:/Users/Phil/Developement/Victor/daten/landseg/H0`. Du urteilst über jedes
Segment deines Viertels v2 (Liste unter „Dein Viertel“), ob Grenze und Klasse stimmen, und zeichnest ein, was
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

Viertel v2 (oben rechts) des Kerns von `r0c0`: x 314–563, y 64–313 im
Teilkachelbild (250 × 250 Bildpunkte). Dir gehören die 139 Segmente der Liste unten: Jedes hat den
größten Teil seiner Kernfläche in diesem Viertel. Die Teilkachel hat 341 Kernsegmente
(v1 114, v2 139, v3 33, v4 55); die anderen Viertel stehen in eigenen Aufträgen mit eigenem Ergebnisordner. Ein Segment
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
Teilkachelbild; Kandidaten aus `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r0c0/kandidaten.json`, dort mit Grund, in den
Bildern nicht eingezeichnet; Anteil hier = Anteil der Kernfläche in diesem Viertel):

| Nr | ID | Klasse Vorstufe | sicher | im Siedlungsgebiet | Kernfläche px | Anteil hier | auch in | Punkt x/y | Kandidaten |
|---|---|---|---|---|---|---|---|---|---|
| 87 | 100087 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 567 | 89 % | v1 | 323/89 | klasse_unsicher |
| 69 | 100069 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 1159 | 100 % | – | 343/85 | grenze_ohne_bildkante, klasse_unsicher |
| 67 | 100067 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 96 | 100 % | – | 344/67 | grenze_ohne_bildkante, klasse_unsicher |
| 82 | 100082 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 123 | 100 % | – | 351/73 | grenze_ohne_bildkante, klasse_unsicher |
| 52 | 100052 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1184 | 100 % | – | 381/74 | grenze_ohne_bildkante, klasse_unsicher |
| 73 | 100073 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 811 | 100 % | – | 386/92 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 36 | 100036 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 479 | 100 % | – | 405/72 | grenze_ohne_bildkante, klasse_unsicher |
| 96 | 100096 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 560 | 100 % | – | 427/95 | grenze_ohne_bildkante, klasse_unsicher |
| 76 | 100076 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 659 | 100 % | – | 428/77 | grenze_ohne_bildkante, klasse_unsicher |
| 56 | 100056 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 887 | 100 % | – | 454/81 | klasse_unsicher |
| 42 | 100042 | 1.2.1 Straße (versiegelt) | nein | nein | 89 | 100 % | – | 455/67 | klasse_unsicher |
| 26 | 100026 | 3.1 Wiese / Weide (gemeinsam) | ja | ja | 588 | 100 % | – | 482/71 | grenze_ohne_bildkante |
| 81 | 100081 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 362 | 100 % | – | 482/92 | klasse_unsicher, nicht_zusammenhaengend |
| 86 | 100086 | 1.3.2 Baustelle | nein | nein | 325 | 100 % | – | 493/89 | grenze_ohne_bildkante, klasse_unsicher |
| 85 | 100085 | 2.1 Acker mit Bewuchs | nein | ja | 213 | 100 % | – | 495/79 | grenze_ohne_bildkante, klasse_unsicher |
| 101 | 100101 | 1.2.1 Straße (versiegelt) | nein | nein | 200 | 100 % | – | 508/95 | grenze_ohne_bildkante, klasse_unsicher |
| 63 | 100063 | 4.2.1 Einzelbaum | nein | ja | 15 | 100 % | – | 513/65 | grenze_ohne_bildkante, klasse_unsicher |
| 24 | 100024 | 1.3.2 Baustelle | nein | nein | 7 | 100 % | – | 518/64 | grenze_ohne_bildkante, klasse_unsicher |
| 100 | 100100 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 78 | 100 % | – | 518/89 | – |
| 70 | 100070 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 251 | 100 % | – | 524/69 | grenze_ohne_bildkante, klasse_unsicher |
| 88 | 100088 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 829 | 100 % | – | 544/90 | grenze_ohne_bildkante, klasse_unsicher |
| 60 | 100060 | 1.1.2 Nebengebäude / Schuppen / Stadel | ja | nein | 586 | 100 % | – | 548/72 | grenze_ohne_bildkante |
| 123 | 100123 | 2.1 Acker mit Bewuchs | nein | ja | 129 | 100 % | – | 335/120 | klasse_unsicher, nicht_zusammenhaengend |
| 151 | 100151 | 2.1 Acker mit Bewuchs | nein | ja | 93 | 100 % | – | 337/139 | klasse_unsicher, nicht_zusammenhaengend |
| 116 | 100116 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 237 | 100 % | – | 345/114 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 141 | 100141 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 94 | 100 % | – | 356/136 | klasse_unsicher |
| 111 | 100111 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 821 | 100 % | – | 366/123 | grenze_ohne_bildkante, klasse_unsicher |
| 146 | 100146 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 769 | 100 % | – | 375/144 | grenze_ohne_bildkante, klasse_unsicher |
| 110 | 100110 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 129 | 100 % | – | 378/115 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 147 | 100147 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 204 | 100 % | – | 392/139 | klasse_unsicher |
| 120 | 100120 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 558 | 100 % | – | 394/118 | klasse_unsicher |
| 144 | 100144 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 130 | 100 % | – | 404/133 | klasse_unsicher, nicht_zusammenhaengend |
| 134 | 100134 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 552 | 100 % | – | 407/145 | grenze_ohne_bildkante, klasse_unsicher |
| 108 | 100108 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 1478 | 100 % | – | 431/130 | grenze_ohne_bildkante, klasse_unsicher |
| 130 | 100130 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 183 | 100 % | – | 463/123 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 124 | 100124 | 1.2.1 Straße (versiegelt) | nein | nein | 1708 | 100 % | – | 478/132 | grenze_ohne_bildkante, klasse_unsicher |
| 112 | 100112 | 1.2.1 Straße (versiegelt) | nein | nein | 168 | 100 % | – | 481/108 | klasse_unsicher |
| 149 | 100149 | 2.1 Acker mit Bewuchs | nein | ja | 145 | 100 % | – | 492/139 | grenze_ohne_bildkante, klasse_unsicher |
| 113 | 100113 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 379 | 100 % | – | 497/114 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 127 | 100127 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 131 | 100 % | – | 511/123 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 103 | 100103 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 1030 | 100 % | – | 520/110 | grenze_ohne_bildkante, klasse_unsicher |
| 135 | 100135 | 1.2.1 Straße (versiegelt) | nein | nein | 138 | 100 % | – | 530/126 | klasse_unsicher |
| 140 | 100140 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 820 | 100 % | – | 537/147 | klasse_unsicher, nicht_zusammenhaengend |
| 153 | 100153 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 82 | 100 % | – | 540/138 | klasse_unsicher, nicht_zusammenhaengend |
| 155 | 100155 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 88 | 100 % | – | 551/148 | grenze_ohne_bildkante, klasse_unsicher |
| 93 | 100093 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 372 | 100 % | – | 553/119 | grenze_ohne_bildkante, klasse_unsicher |
| 138 | 100138 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 375 | 100 % | – | 556/132 | klasse_unsicher |
| 114 | 100114 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 45 | 100 % | – | 561/115 | grenze_ohne_bildkante, klasse_unsicher |
| 126 | 100126 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 23 | 100 % | – | 562/120 | klasse_unsicher |
| 191 | 100191 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 608 | 100 % | – | 329/192 | grenze_ohne_bildkante, klasse_unsicher |
| 175 | 100175 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 97 | 100 % | – | 330/172 | grenze_ohne_bildkante, klasse_unsicher |
| 180 | 100180 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 192 | 100 % | – | 337/169 | klasse_unsicher |
| 197 | 100197 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 324 | 100 % | – | 350/191 | klasse_unsicher, nicht_zusammenhaengend |
| 169 | 100169 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 816 | 100 % | – | 356/170 | klasse_unsicher |
| 161 | 100161 | 1.2.1 Straße (versiegelt) | nein | nein | 447 | 100 % | – | 373/161 | grenze_ohne_bildkante, klasse_unsicher |
| 187 | 100187 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 84 | 100 % | – | 377/178 | klasse_unsicher |
| 186 | 100186 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 389 | 100 % | – | 386/174 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 172 | 100172 | 1.2.1 Straße (versiegelt) | nein | nein | 1137 | 100 % | – | 413/177 | grenze_ohne_bildkante, klasse_unsicher |
| 209 | 100209 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 183 | 100 % | – | 421/198 | grenze_ohne_bildkante, klasse_unsicher |
| 181 | 100181 | 1.2.1 Straße (versiegelt) | nein | nein | 224 | 100 % | – | 435/170 | grenze_ohne_bildkante, klasse_unsicher |
| 188 | 100188 | 5.2 Stillgewässer (See, Teich, Weiher) | nein | nein | 195 | 100 % | – | 435/185 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 182 | 100182 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 193 | 100 % | – | 449/171 | grenze_ohne_bildkante, klasse_unsicher |
| 165 | 100165 | 1.2.1 Straße (versiegelt) | ja | nein | 99 | 100 % | – | 450/156 | grenze_ohne_bildkante |
| 163 | 100163 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 103 | 100 % | – | 457/153 | klasse_unsicher, nicht_zusammenhaengend |
| 162 | 100162 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 117 | 100 % | – | 471/151 | grenze_ohne_bildkante, klasse_unsicher |
| 142 | 100142 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 5242 | 100 % | – | 497/173 | grenze_ohne_bildkante, klasse_unsicher |
| 168 | 100168 | 5.2 Stillgewässer (See, Teich, Weiher) | nein | nein | 112 | 100 % | – | 535/159 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 184 | 100184 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 215 | 100 % | – | 546/176 | grenze_ohne_bildkante, klasse_unsicher |
| 201 | 100201 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 407 | 100 % | – | 556/192 | grenze_ohne_bildkante, klasse_unsicher |
| 164 | 100164 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 86 | 100 % | – | 560/160 | grenze_ohne_bildkante, klasse_unsicher |
| 277 | 100277 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 175 | 88 % | v1 | 319/239 | klasse_unsicher |
| 213 | 100213 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 317 | 70 % | v1 | 320/210 | grenze_ohne_bildkante, klasse_unsicher |
| 255 | 100255 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 396 | 83 % | v1 | 324/224 | klasse_unsicher |
| 258 | 100258 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 179 | 100 % | – | 339/225 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 263 | 100263 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 640 | 100 % | – | 340/241 | grenze_ohne_bildkante, klasse_unsicher |
| 243 | 100243 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 189 | 100 % | – | 345/213 | grenze_ohne_bildkante, klasse_unsicher |
| 278 | 100278 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 103 | 100 % | – | 353/244 | grenze_ohne_bildkante, klasse_unsicher |
| 219 | 100219 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 345 | 100 % | – | 354/204 | grenze_ohne_bildkante, klasse_unsicher |
| 254 | 100254 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 113 | 100 % | – | 361/217 | klasse_unsicher, nicht_zusammenhaengend |
| 240 | 100240 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 147 | 100 % | – | 362/208 | klasse_unsicher, nicht_zusammenhaengend |
| 257 | 100257 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 370 | 100 % | – | 370/225 | klasse_unsicher |
| 206 | 100206 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 541 | 100 % | – | 374/201 | klasse_unsicher |
| 265 | 100265 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 946 | 100 % | – | 377/242 | grenze_ohne_bildkante, klasse_unsicher |
| 251 | 100251 | 1.2.1 Straße (versiegelt) | nein | nein | 134 | 100 % | – | 407/227 | klasse_unsicher, nicht_zusammenhaengend |
| 210 | 100210 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 113 | 100 % | – | 409/202 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 222 | 100222 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 496 | 100 % | – | 412/233 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 223 | 100223 | 1.2.1 Straße (versiegelt) | nein | nein | 102 | 100 % | – | 412/213 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 271 | 100271 | 1.3.2 Baustelle | nein | nein | 123 | 100 % | – | 421/232 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 241 | 100241 | 2.1 Acker mit Bewuchs | nein | ja | 165 | 100 % | – | 422/211 | grenze_ohne_bildkante, klasse_unsicher |
| 281 | 100281 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 754 | 100 % | – | 439/249 | grenze_ohne_bildkante, klasse_unsicher |
| 236 | 100236 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 1099 | 100 % | – | 440/221 | grenze_ohne_bildkante, klasse_unsicher |
| 266 | 100266 | 1.3.2 Baustelle | nein | nein | 340 | 100 % | – | 458/234 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 244 | 100244 | 1.3.2 Baustelle | nein | nein | 326 | 100 % | – | 472/212 | klasse_unsicher, nicht_zusammenhaengend |
| 268 | 100268 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 148 | 100 % | – | 475/234 | klasse_unsicher, nicht_zusammenhaengend |
| 261 | 100261 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 489 | 100 % | – | 494/237 | grenze_ohne_bildkante, klasse_unsicher |
| 232 | 100232 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 630 | 100 % | – | 497/215 | klasse_unsicher |
| 262 | 100262 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 162 | 100 % | – | 508/222 | klasse_unsicher, nicht_zusammenhaengend |
| 242 | 100242 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 195 | 100 % | – | 523/213 | – |
| 214 | 100214 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 333 | 100 % | – | 526/202 | grenze_ohne_bildkante, klasse_unsicher |
| 245 | 100245 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 124 | 100 % | – | 538/215 | grenze_ohne_bildkante, klasse_unsicher |
| 237 | 100237 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 903 | 100 % | – | 539/233 | grenze_ohne_bildkante, klasse_unsicher |
| 202 | 100202 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 335 | 100 % | – | 545/203 | klasse_unsicher, nicht_zusammenhaengend |
| 276 | 100276 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 35 | 100 % | – | 561/242 | grenze_ohne_bildkante, klasse_unsicher |
| 228 | 100228 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 7 | 100 % | – | 563/209 | grenze_ohne_bildkante, klasse_unsicher |
| 284 | 100284 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 598 | 79 % | v1 | 324/254 | klasse_unsicher |
| 302 | 100302 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 742 | 100 % | – | 331/273 | grenze_ohne_bildkante, klasse_unsicher |
| 329 | 100329 | 2.1 Acker mit Bewuchs | nein | ja | 99 | 100 % | – | 335/285 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 318 | 100318 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 664 | 100 % | – | 350/289 | grenze_ohne_bildkante, klasse_unsicher |
| 293 | 100293 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 241 | 100 % | – | 360/258 | grenze_ohne_bildkante, klasse_unsicher |
| 298 | 100298 | 1.2.1 Straße (versiegelt) | nein | nein | 986 | 100 % | – | 380/265 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 288 | 100288 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 149 | 100 % | – | 404/252 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 311 | 100311 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 264 | 100 % | – | 411/275 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 280 | 100280 | 1.2.1 Straße (versiegelt) | nein | nein | 457 | 100 % | – | 416/261 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 286 | 100286 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 190 | 100 % | – | 423/252 | klasse_unsicher |
| 305 | 100305 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 147 | 100 % | – | 432/277 | klasse_unsicher, nicht_zusammenhaengend |
| 319 | 100319 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 687 | 98 % | v4 | 439/293 | grenze_ohne_bildkante, klasse_unsicher |
| 306 | 100306 | 1.3.2 Baustelle | nein | nein | 204 | 100 % | – | 445/267 | klasse_unsicher, nicht_zusammenhaengend |
| 322 | 100322 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 740 | 73 % | v4 | 461/298 | grenze_ohne_bildkante, klasse_unsicher |
| 328 | 100328 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 94 | 100 % | – | 464/285 | klasse_unsicher |
| 299 | 100299 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 652 | 100 % | – | 465/271 | grenze_ohne_bildkante, klasse_unsicher |
| 279 | 100279 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 667 | 100 % | – | 471/252 | grenze_ohne_bildkante, klasse_unsicher |
| 334 | 100334 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 268 | 100 % | – | 476/292 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 326 | 100326 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 104 | 100 % | – | 484/276 | klasse_unsicher, nicht_zusammenhaengend |
| 291 | 100291 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 395 | 100 % | – | 494/270 | klasse_unsicher |
| 312 | 100312 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 360 | 100 % | – | 496/279 | grenze_ohne_bildkante, klasse_unsicher |
| 335 | 100335 | 1.1.2 Nebengebäude / Schuppen / Stadel | ja | nein | 836 | 98 % | v4 | 500/293 | – |
| 273 | 100273 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 720 | 100 % | – | 501/250 | grenze_ohne_bildkante, klasse_unsicher |
| 327 | 100327 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 110 | 100 % | – | 509/277 | klasse_unsicher, nicht_zusammenhaengend |
| 337 | 100337 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 157 | 100 % | – | 522/291 | klasse_unsicher, nicht_zusammenhaengend |
| 287 | 100287 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 825 | 100 % | – | 527/272 | grenze_ohne_bildkante, klasse_unsicher |
| 323 | 100323 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 130 | 100 % | – | 536/281 | – |
| 274 | 100274 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 543 | 100 % | – | 540/250 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 331 | 100331 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 662 | 84 % | v4 | 541/289 | grenze_ohne_bildkante, klasse_unsicher |
| 308 | 100308 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 132 | 100 % | – | 551/271 | klasse_unsicher, nicht_zusammenhaengend |
| 315 | 100315 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 124 | 100 % | – | 558/275 | klasse_unsicher |
| 304 | 100304 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 8 | 100 % | – | 563/279 | grenze_ohne_bildkante, klasse_unsicher |
| 345 | 100345 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 144 | 100 % | – | 510/301 | – |
| 347 | 100347 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 243 | 87 % | v4 | 533/306 | grenze_ohne_bildkante, klasse_unsicher |
| 336 | 100336 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 712 | 78 % | v4 | 550/303 | grenze_ohne_bildkante, klasse_unsicher |

`nicht_geprueft` nennt, was du nicht angesehen hast, `offen`, was du nicht entscheiden konntest.

Kontrolle vor der Rückgabe (muss mit `ok` enden):

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-2/skripte/pruefe_urteil.py --urteil C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r0c0/v2/urteil.json --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r0c0/segmente.json --fassung c --viertel v2 --ids 100087,100069,100067,100082,100052,100073,100036,100096,100076,100056,100042,100026,100081,100086,100085,100101,100063,100024,100100,100070,100088,100060,100123,100151,100116,100141,100111,100146,100110,100147,100120,100144,100134,100108,100130,100124,100112,100149,100113,100127,100103,100135,100140,100153,100155,100093,100138,100114,100126,100191,100175,100180,100197,100169,100161,100187,100186,100172,100209,100181,100188,100182,100165,100163,100162,100142,100168,100184,100201,100164,100277,100213,100255,100258,100263,100243,100278,100219,100254,100240,100257,100206,100265,100251,100210,100222,100223,100271,100241,100281,100236,100266,100244,100268,100261,100232,100262,100242,100214,100245,100237,100202,100276,100228,100284,100302,100329,100318,100293,100298,100288,100311,100280,100286,100305,100319,100306,100322,100328,100299,100279,100334,100326,100291,100312,100335,100273,100327,100337,100287,100323,100274,100331,100308,100315,100304,100345,100347,100336 --kategorien C:/Users/Phil/Developement/Victor/landseg/kategorien.json
```

## Werkzeuge

Befehle im Ordner `C:/Users/Phil/Developement/Victor/landseg` mit `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -m landseg <befehl>`; Aufruf und Schalter stehen in
`C:/Users/Phil/Developement/Victor/landseg/README.md`. Die Bilder deines Viertels liegen fertig vor (Abschnitt „Dein Viertel“); `ansicht` (W3) erzeugt Bilder
je Segment und ist hier keine Urteilsgrundlage. Für fragliche Grenzen `kante` (W4, hier nur zum Ansehen
der Bildkante), zur Kontrolle `pruefen`. Eigene Skripte als Datei in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r0c0/v2`.

## Ergebnis in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r0c0/v2` (genau diese Namen)

- `roh.jpg`, `umriss.jpg` (alle Segmentgrenzen mit ID), `maengel.jpg` (nummerierte Punkte mit kurzer
  deutscher Beschriftung, sonst Vermerk „keine Mängel“), `vorschlag.jpg` (Grenzen und Klassen, wie
  du sie setzen würdest, sonst Vermerk „unverändert“): je dein Viertel mit Umgebung, Viertel
  umrandet (Grundlage: die vorbereiteten Übersichtsbilder).
- `nah_<n>.jpg`: eigene Nahansichten von Stellen, die man in den vorbereiteten Bildern nicht beurteilen kann,
  je ein Teil des Viertels samt Nachbarn (mindestens 64 × 64 Bildpunkte der Teilkachel, kein freigestelltes
  Einzelsegment); `kontrast_<n>.jpg` bei blassen Stellen.
- `urteil.json` (UTF-8):

```
{"teilkachel": "r0c0", "viertel": "v2", "bearbeiter": "urt-c-r0c0-v2",
 "bilder_angesehen": {"uebersicht": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r0c0/ganz_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c0/v2/uebersicht_nummern.jpg", "…"],
                      "nah": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c0/v2/nah1_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r0c0/v2/nah_1.jpg", "…"]},
 "segmente": [{"id": 17, "klasse_heute": "Code", "was_ist_es": "ein Satz",
               "urteil": "sauber" | "nicht_sauber", "klasse_vorschlag": "Code oder null",
               "sicher": true | false,
               "punkte": [{"nr": 1, "art": "fremdes|fehlt|trennen|verschmelzen|grenze|klasse|zu_klein|sonstiges",
                           "text": "ein Satz mit Stelle (x/y im Teilkachelbild)", "flaeche_px": Zahl oder null}],
               "bilder": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c0/v2/uebersicht_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c0/v2/nah2_roh.jpg"]}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "was an der Kerngrenze nicht passt"}],
 "unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."]}
```

Jedes Segment deiner Liste steht genau einmal unter `segmente`, auch die sauberen, in der Reihenfolge der Liste. Segmente der Nachbarviertel (graue Nummern) und des Kontextrands (ohne Nummer) urteilst du in diesem Auftrag nicht; Auffälliges an ihnen nennst du unter `unsicher` mit ID.

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Punkte, Anteil `sicher: false`, wo du unsicher bist.
