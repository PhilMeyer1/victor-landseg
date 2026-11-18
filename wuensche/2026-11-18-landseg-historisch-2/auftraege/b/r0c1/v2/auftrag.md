# Auftrag: H0, Teilkachel r0c1, Viertel v2: 103 Segmente im Verbund ansehen und einzeln urteilen (Fassung B „Kategorien frei“)

Lies zuerst den Skill `landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `r0c1` des Ausschnitts in `C:/Users/Phil/Developement/Victor/daten/landseg/H0`. Du urteilst über jedes
Segment deines Viertels v2 (Liste unter „Dein Viertel“), ob Grenze und Klasse stimmen, und zeichnest ein, was
du ändern würdest. Die Label-Karte änderst du nicht.

## Daten (eingefrorener Stand, nur lesen)

- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/manifest.json`: Eintrag `r0c1` unter `teilkacheln` mit `bild` (Teilkachelbild,
  Kern + Kontextrand), `kern_im_bild` (Lage des Kerns im Teilkachelbild) und `kern` (Lage im Ausschnitt).
- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r0c1/labels.tif`: Label-Karte (Segment-ID je Bildpunkt, Größe des Teilkachelbilds).
- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r0c1/segmente.json`: je Segment `id`, `klasse`, `grob`, `herkunft`, `sicher`; dazu die
  Kandidatenliste der Vorstufe, falls vorhanden.
- `C:/Users/Phil/Developement/Victor/landseg/kategorien.json` und `C:/Users/Phil/Developement/Victor/landseg/KATEGORIEN.md`: nur Anregung; in Fassung B benennst du die Klassen selbst (Abschnitt „Fassung B“).

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

Viertel v2 (oben rechts) des Kerns von `r0c1`: x 314–563, y 64–313 im
Teilkachelbild (250 × 250 Bildpunkte). Dir gehören die 103 Segmente der Liste unten: Jedes hat den
größten Teil seiner Kernfläche in diesem Viertel. Die Teilkachel hat 422 Kernsegmente
(v1 107, v2 103, v3 105, v4 107); die anderen Viertel stehen in eigenen Aufträgen mit eigenem Ergebnisordner. Ein Segment
über einer Viertelgrenze urteilt nur das Viertel mit dem größten Anteil; in den Bildern der Nachbarn ist
es mit grauer Nummer als Umgebung zu sehen.

Urteil im Verbund: Du siehst das Viertel als zusammenhängendes Bild mit Umgebung, arbeitest die Liste der
Reihe nach ab und beurteilst jedes Segment im Zusammenhang mit seinen Nachbarn; eingetragen wird jedes
Segment einzeln (Klasse, `sicher`, `was_ist_es` als Notiz). Bilder freigestellter Einzelsegmente gibt es
nicht, und sie sind keine Urteilsgrundlage.

Bilder des Viertels (fertig, JPEG, in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c1/v2`, Fenster und Vergrößerung je Bild in `viertel.json`):

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
Teilkachelbild; Kandidaten aus `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r0c1/kandidaten.json`, dort mit Grund, in den
Bildern nicht eingezeichnet; Anteil hier = Anteil der Kernfläche in diesem Viertel):

| Nr | ID | Klasse Vorstufe | sicher | im Siedlungsgebiet | Kernfläche px | Anteil hier | auch in | Punkt x/y | Kandidaten |
|---|---|---|---|---|---|---|---|---|---|
| 99 | 200099 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 376 | 53 % | v1 | 318/95 | klasse_unsicher, nicht_zusammenhaengend |
| 72 | 200072 | 6.6 Weg, unbefestigt (Feld-, Wald-, Schotterweg) | nein | nein | 27 | 100 % | – | 328/65 | grenze_ohne_bildkante, klasse_unsicher |
| 93 | 200093 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 686 | 100 % | – | 341/90 | klasse_unsicher, nicht_zusammenhaengend |
| 65 | 200065 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 198 | 100 % | – | 348/68 | klasse_unsicher |
| 84 | 200084 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 891 | 100 % | – | 361/84 | klasse_unsicher |
| 78 | 200078 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 420 | 100 % | – | 372/71 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 107 | 200107 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 163 | 100 % | – | 380/95 | klasse_unsicher |
| 62 | 200062 | 4.2.1 Einzelbaum | nein | ja | 16 | 100 % | – | 386/64 | grenze_ohne_bildkante, klasse_unsicher |
| 83 | 200083 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 260 | 100 % | – | 393/81 | klasse_unsicher |
| 69 | 200069 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 25 | 100 % | – | 404/65 | klasse_unsicher, nicht_zusammenhaengend |
| 82 | 200082 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 545 | 100 % | – | 406/78 | klasse_unsicher |
| 105 | 200105 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 138 | 100 % | – | 409/95 | klasse_unsicher, nicht_zusammenhaengend |
| 47 | 200047 | 1.2.1 Straße (versiegelt) | nein | nein | 129 | 100 % | – | 418/68 | grenze_ohne_bildkante, klasse_unsicher |
| 67 | 200067 | 1.3.2 Baustelle | nein | nein | 5 | 100 % | – | 421/64 | klasse_unsicher, nicht_zusammenhaengend |
| 97 | 200097 | 1.3.2 Baustelle | nein | nein | 259 | 100 % | – | 427/95 | klasse_unsicher, nicht_zusammenhaengend |
| 57 | 200057 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 2260 | 100 % | – | 479/85 | klasse_unsicher |
| 60 | 200060 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1 | 100 % | – | 491/64 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 75 | 200075 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 173 | 100 % | – | 507/72 | klasse_unsicher, nicht_zusammenhaengend |
| 85 | 200085 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 221 | 100 % | – | 524/79 | klasse_unsicher, nicht_zusammenhaengend |
| 41 | 200041 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 255 | 100 % | – | 531/69 | klasse_unsicher |
| 90 | 200090 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 180 | 100 % | – | 539/78 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 27 | 200027 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 229 | 100 % | – | 546/68 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 95 | 200095 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 958 | 100 % | – | 551/92 | grenze_ohne_bildkante, klasse_unsicher |
| 77 | 200077 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 110 | 100 % | – | 558/68 | klasse_unsicher |
| 112 | 200112 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1484 | 100 % | – | 380/139 | klasse_unsicher |
| 114 | 200114 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 236 | 100 % | – | 381/115 | klasse_unsicher |
| 96 | 200096 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 642 | 100 % | – | 402/103 | klasse_unsicher |
| 126 | 200126 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 523 | 100 % | – | 406/139 | klasse_unsicher, nicht_zusammenhaengend |
| 124 | 200124 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 151 | 100 % | – | 416/125 | klasse_unsicher, nicht_zusammenhaengend |
| 120 | 200120 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 121 | 100 % | – | 420/118 | klasse_unsicher, nicht_zusammenhaengend |
| 118 | 200118 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 216 | 100 % | – | 447/114 | klasse_unsicher, nicht_zusammenhaengend |
| 109 | 200109 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 2214 | 100 % | – | 464/147 | grenze_ohne_bildkante, klasse_unsicher |
| 127 | 200127 | 1.3.2 Baustelle | nein | nein | 161 | 100 % | – | 483/141 | klasse_unsicher, nicht_zusammenhaengend |
| 89 | 200089 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 4392 | 100 % | – | 509/144 | klasse_unsicher, nicht_zusammenhaengend |
| 73 | 200073 | 1.3.2 Baustelle | nein | nein | 2711 | 100 % | – | 510/106 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 164 | 200164 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 167 | 78 % | v1 | 317/186 | klasse_unsicher |
| 139 | 200139 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 1521 | 68 % | v1 | 333/197 | klasse_unsicher |
| 111 | 200111 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1785 | 72 % | v1 | 337/150 | klasse_unsicher, nicht_zusammenhaengend |
| 81 | 200081 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 2408 | 56 % | v1 | 351/192 | klasse_unsicher, nicht_zusammenhaengend |
| 159 | 200159 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 444 | 100 % | – | 358/179 | klasse_unsicher |
| 158 | 200158 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 377 | 100 % | – | 383/196 | klasse_unsicher, nicht_zusammenhaengend |
| 103 | 200103 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 2292 | 100 % | – | 384/172 | klasse_unsicher |
| 151 | 200151 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 411 | 100 % | – | 398/185 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 161 | 200161 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 424 | 100 % | – | 414/177 | grenze_ohne_bildkante, klasse_unsicher |
| 142 | 200142 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1015 | 100 % | – | 435/175 | grenze_ohne_bildkante, klasse_unsicher |
| 171 | 200171 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 373 | 100 % | – | 435/197 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 119 | 200119 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1004 | 100 % | – | 437/150 | klasse_unsicher, nicht_zusammenhaengend |
| 157 | 200157 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 556 | 100 % | – | 460/176 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 168 | 200168 | 4.2.4 Gebüsch / Strauchfläche | nein | ja | 511 | 100 % | – | 494/197 | grenze_ohne_bildkante, klasse_unsicher |
| 155 | 200155 | 1.3.2 Baustelle | nein | nein | 3355 | 100 % | – | 521/198 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 144 | 200144 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 673 | 100 % | – | 553/163 | klasse_unsicher |
| 163 | 200163 | 1.3.2 Baustelle | nein | nein | 210 | 100 % | – | 557/189 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 209 | 200209 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 869 | 100 % | – | 339/234 | klasse_unsicher |
| 188 | 200188 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 501 | 100 % | – | 356/221 | klasse_unsicher |
| 222 | 200222 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 773 | 100 % | – | 371/241 | klasse_unsicher |
| 191 | 200191 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 313 | 100 % | – | 374/219 | klasse_unsicher, nicht_zusammenhaengend |
| 177 | 200177 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 477 | 100 % | – | 377/207 | klasse_unsicher |
| 219 | 200219 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 281 | 100 % | – | 388/238 | klasse_unsicher, nicht_zusammenhaengend |
| 176 | 200176 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 153 | 100 % | – | 402/200 | klasse_unsicher |
| 180 | 200180 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 437 | 100 % | – | 402/216 | klasse_unsicher |
| 210 | 200210 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 687 | 100 % | – | 405/241 | grenze_ohne_bildkante, klasse_unsicher |
| 217 | 200217 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 174 | 100 % | – | 420/228 | grenze_ohne_bildkante, klasse_unsicher |
| 200 | 200200 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 135 | 100 % | – | 424/211 | klasse_unsicher, nicht_zusammenhaengend |
| 218 | 200218 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 479 | 100 % | – | 432/242 | grenze_ohne_bildkante, klasse_unsicher |
| 208 | 200208 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 477 | 100 % | – | 440/224 | grenze_ohne_bildkante, klasse_unsicher |
| 214 | 200214 | 4.2.1 Einzelbaum | nein | ja | 136 | 100 % | – | 453/223 | klasse_unsicher |
| 211 | 200211 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 88 | 100 % | – | 463/219 | klasse_unsicher |
| 216 | 200216 | 4.2.4 Gebüsch / Strauchfläche | nein | ja | 223 | 100 % | – | 470/233 | klasse_unsicher |
| 175 | 200175 | 4.2.1 Einzelbaum | nein | ja | 233 | 100 % | – | 474/202 | grenze_ohne_bildkante, klasse_unsicher |
| 185 | 200185 | 1.2.1 Straße (versiegelt) | nein | nein | 1086 | 100 % | – | 482/244 | klasse_unsicher |
| 204 | 200204 | 4.2.1 Einzelbaum | nein | ja | 361 | 100 % | – | 521/221 | grenze_ohne_bildkante, klasse_unsicher |
| 207 | 200207 | 4.2.1 Einzelbaum | nein | ja | 680 | 100 % | – | 545/227 | grenze_ohne_bildkante, klasse_unsicher |
| 205 | 200205 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 191 | 100 % | – | 557/215 | klasse_unsicher |
| 248 | 200248 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 252 | 100 % | – | 329/271 | klasse_unsicher |
| 198 | 200198 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 534 | 89 % | v1 | 330/253 | klasse_unsicher |
| 282 | 200282 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 165 | 100 % | – | 332/296 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 251 | 200251 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 352 | 100 % | – | 341/269 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 253 | 200253 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 131 | 100 % | – | 354/268 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 258 | 200258 | 1.2.1 Straße (versiegelt) | nein | nein | 163 | 100 % | – | 357/283 | grenze_ohne_bildkante, klasse_unsicher |
| 238 | 200238 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 838 | 100 % | – | 376/271 | klasse_unsicher |
| 236 | 200236 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 178 | 100 % | – | 377/251 | klasse_unsicher, nicht_zusammenhaengend |
| 276 | 200276 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 236 | 100 % | – | 388/291 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 259 | 200259 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 135 | 100 % | – | 397/275 | klasse_unsicher, nicht_zusammenhaengend |
| 246 | 200246 | 4.2.1 Einzelbaum | nein | ja | 220 | 100 % | – | 401/261 | klasse_unsicher |
| 270 | 200270 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 683 | 100 % | v4 | 411/293 | klasse_unsicher |
| 250 | 200250 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 204 | 100 % | – | 415/269 | klasse_unsicher |
| 260 | 200260 | 1.3.2 Baustelle | nein | nein | 125 | 100 % | – | 433/276 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 225 | 200225 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1945 | 100 % | – | 448/256 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 261 | 200261 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 917 | 94 % | v4 | 455/288 | grenze_ohne_bildkante, klasse_unsicher |
| 252 | 200252 | 4.2.1 Einzelbaum | nein | ja | 332 | 100 % | – | 461/268 | klasse_unsicher |
| 229 | 200229 | 1.3.2 Baustelle | nein | nein | 498 | 100 % | – | 497/290 | klasse_unsicher, nicht_zusammenhaengend |
| 221 | 200221 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 2778 | 100 % | – | 504/261 | grenze_ohne_bildkante, klasse_unsicher |
| 172 | 200172 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | ja | nein | 3901 | 52 % | v4 | 523/290 | grenze_ohne_bildkante |
| 254 | 200254 | 1.3.2 Baustelle | nein | nein | 579 | 100 % | – | 544/297 | klasse_unsicher, nicht_zusammenhaengend |
| 274 | 200274 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 100 | 100 % | – | 560/282 | klasse_unsicher, nicht_zusammenhaengend |
| 281 | 200281 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 961 | 61 % | v4 | 362/304 | grenze_ohne_bildkante, klasse_unsicher |
| 283 | 200283 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 382 | 55 % | v4 | 378/303 | klasse_unsicher |
| 272 | 200272 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 324 | 98 % | v4 | 389/303 | grenze_ohne_bildkante, klasse_unsicher |
| 295 | 200295 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 221 | 77 % | v4 | 401/308 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 300 | 200300 | 1.3.2 Baustelle | nein | nein | 109 | 51 % | v4 | 449/311 | klasse_unsicher, nicht_zusammenhaengend |
| 290 | 200290 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 218 | 100 % | – | 472/302 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 297 | 200297 | 1.2.1 Straße (versiegelt) | ja | nein | 284 | 52 % | v4 | 512/308 | grenze_ohne_bildkante |
| 262 | 200262 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 850 | 52 % | v4 | 555/306 | klasse_unsicher, nicht_zusammenhaengend |

`nicht_geprueft` nennt, was du nicht angesehen hast, `offen`, was du nicht entscheiden konntest.

Kontrolle vor der Rückgabe (muss mit `ok` enden):

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-2/skripte/pruefe_urteil.py --urteil C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r0c1/v2/urteil.json --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r0c1/segmente.json --fassung b --viertel v2 --ids 200099,200072,200093,200065,200084,200078,200107,200062,200083,200069,200082,200105,200047,200067,200097,200057,200060,200075,200085,200041,200090,200027,200095,200077,200112,200114,200096,200126,200124,200120,200118,200109,200127,200089,200073,200164,200139,200111,200081,200159,200158,200103,200151,200161,200142,200171,200119,200157,200168,200155,200144,200163,200209,200188,200222,200191,200177,200219,200176,200180,200210,200217,200200,200218,200208,200214,200211,200216,200175,200185,200204,200207,200205,200248,200198,200282,200251,200253,200258,200238,200236,200276,200259,200246,200270,200250,200260,200225,200261,200252,200229,200221,200172,200254,200274,200281,200283,200272,200295,200300,200290,200297,200262
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
der Bildkante), zur Kontrolle `pruefen`. Eigene Skripte als Datei in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r0c1/v2`.

## Ergebnis in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r0c1/v2` (genau diese Namen)

- `roh.jpg`, `umriss.jpg` (alle Segmentgrenzen mit ID), `maengel.jpg` (nummerierte Punkte mit kurzer
  deutscher Beschriftung, sonst Vermerk „keine Mängel“), `vorschlag.jpg` (Grenzen und Klassen, wie
  du sie setzen würdest, sonst Vermerk „unverändert“): je dein Viertel mit Umgebung, Viertel
  umrandet (Grundlage: die vorbereiteten Übersichtsbilder).
- `nah_<n>.jpg`: eigene Nahansichten von Stellen, die man in den vorbereiteten Bildern nicht beurteilen kann,
  je ein Teil des Viertels samt Nachbarn (mindestens 64 × 64 Bildpunkte der Teilkachel, kein freigestelltes
  Einzelsegment); `kontrast_<n>.jpg` bei blassen Stellen.
- `urteil.json` (UTF-8):

```
{"teilkachel": "r0c1", "viertel": "v2", "bearbeiter": "urt-b-r0c1-v2",
 "bilder_angesehen": {"uebersicht": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r0c1/ganz_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c1/v2/uebersicht_nummern.jpg", "…"],
                      "nah": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c1/v2/nah1_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r0c1/v2/nah_1.jpg", "…"]},
 "segmente": [{"id": 17, "klasse_heute": "Code", "was_ist_es": "ein Satz",
               "urteil": "sauber" | "nicht_sauber", "klasse_vorschlag": null,
               "klasse_frei": {"grob": "Name", "mittel": "Name", "fein": "Name"},
               "sicher": true | false,
               "punkte": [{"nr": 1, "art": "fremdes|fehlt|trennen|verschmelzen|grenze|klasse|zu_klein|sonstiges",
                           "text": "ein Satz mit Stelle (x/y im Teilkachelbild)", "flaeche_px": Zahl oder null}],
               "bilder": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c1/v2/uebersicht_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c1/v2/nah2_roh.jpg"]}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "was an der Kerngrenze nicht passt"}],
 "unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."],
 "klassen_frei": [{"name": "Name", "ebene": "grob|mittel|fein", "eltern": "Name oder null", "merkmal": "woran im Bild erkennbar"}]}
```

Jedes Segment deiner Liste steht genau einmal unter `segmente`, auch die sauberen, in der Reihenfolge der Liste. Segmente der Nachbarviertel (graue Nummern) und des Kontextrands (ohne Nummer) urteilst du in diesem Auftrag nicht; Auffälliges an ihnen nennst du unter `unsicher` mit ID.

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Punkte, Anteil `sicher: false`, wo du unsicher bist.
