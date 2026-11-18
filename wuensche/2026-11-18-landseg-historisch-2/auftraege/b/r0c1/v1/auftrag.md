# Auftrag: H0, Teilkachel r0c1, Viertel v1: 107 Segmente im Verbund ansehen und einzeln urteilen (Fassung B „Kategorien frei“)

Lies zuerst den Skill `landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `r0c1` des Ausschnitts in `C:/Users/Phil/Developement/Victor/daten/landseg/H0`. Du urteilst über jedes
Segment deines Viertels v1 (Liste unter „Dein Viertel“), ob Grenze und Klasse stimmen, und zeichnest ein, was
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

Viertel v1 (oben links) des Kerns von `r0c1`: x 64–313, y 64–313 im
Teilkachelbild (250 × 250 Bildpunkte). Dir gehören die 107 Segmente der Liste unten: Jedes hat den
größten Teil seiner Kernfläche in diesem Viertel. Die Teilkachel hat 422 Kernsegmente
(v1 107, v2 103, v3 105, v4 107); die anderen Viertel stehen in eigenen Aufträgen mit eigenem Ergebnisordner. Ein Segment
über einer Viertelgrenze urteilt nur das Viertel mit dem größten Anteil; in den Bildern der Nachbarn ist
es mit grauer Nummer als Umgebung zu sehen.

Urteil im Verbund: Du siehst das Viertel als zusammenhängendes Bild mit Umgebung, arbeitest die Liste der
Reihe nach ab und beurteilst jedes Segment im Zusammenhang mit seinen Nachbarn; eingetragen wird jedes
Segment einzeln (Klasse, `sicher`, `was_ist_es` als Notiz). Bilder freigestellter Einzelsegmente gibt es
nicht, und sie sind keine Urteilsgrundlage.

Bilder des Viertels (fertig, JPEG, in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c1/v1`, Fenster und Vergrößerung je Bild in `viertel.json`):

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
| 70 | 200070 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 146 | 100 % | – | 68/68 | klasse_unsicher |
| 86 | 200086 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 563 | 100 % | – | 76/78 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 59 | 200059 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 153 | 100 % | – | 82/68 | grenze_ohne_bildkante, klasse_unsicher |
| 87 | 200087 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 740 | 100 % | – | 92/88 | klasse_unsicher |
| 68 | 200068 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 449 | 100 % | – | 106/71 | klasse_unsicher |
| 61 | 200061 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 97 | 100 % | – | 119/67 | klasse_unsicher, nicht_zusammenhaengend |
| 88 | 200088 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1499 | 100 % | – | 139/86 | klasse_unsicher |
| 64 | 200064 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 933 | 100 % | – | 154/73 | klasse_unsicher, nicht_zusammenhaengend |
| 98 | 200098 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 199 | 100 % | – | 188/96 | klasse_unsicher, nicht_zusammenhaengend |
| 7 | 200007 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1269 | 100 % | – | 190/75 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 100 | 200100 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 112 | 100 % | – | 199/93 | klasse_unsicher |
| 66 | 200066 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 183 | 100 % | – | 211/70 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 101 | 200101 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 109 | 100 % | – | 215/96 | klasse_unsicher, nicht_zusammenhaengend |
| 92 | 200092 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 548 | 100 % | – | 223/88 | grenze_ohne_bildkante, klasse_unsicher |
| 80 | 200080 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 219 | 100 % | – | 225/72 | klasse_unsicher |
| 74 | 200074 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 378 | 100 % | – | 240/71 | grenze_ohne_bildkante, klasse_unsicher |
| 13 | 200013 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 794 | 100 % | – | 260/74 | klasse_unsicher, nicht_zusammenhaengend |
| 11 | 200011 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 6 | 100 % | – | 264/64 | klasse_unsicher |
| 17 | 200017 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 2326 | 97 % | v2 | 273/92 | grenze_ohne_bildkante, klasse_unsicher |
| 102 | 200102 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 11 | 100 % | – | 64/100 | klasse_unsicher |
| 122 | 200122 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 100 | 100 % | – | 70/119 | klasse_unsicher, nicht_zusammenhaengend |
| 125 | 200125 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 590 | 100 % | – | 72/140 | klasse_unsicher |
| 113 | 200113 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 339 | 100 % | – | 88/106 | klasse_unsicher |
| 117 | 200117 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1260 | 100 % | – | 103/125 | grenze_ohne_bildkante, klasse_unsicher |
| 141 | 200141 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 113 | 100 % | – | 132/146 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 94 | 200094 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 2392 | 100 % | – | 138/117 | klasse_unsicher, nicht_zusammenhaengend |
| 123 | 200123 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 447 | 100 % | – | 183/136 | grenze_ohne_bildkante, klasse_unsicher |
| 130 | 200130 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 154 | 100 % | – | 199/135 | grenze_ohne_bildkante, klasse_unsicher |
| 133 | 200133 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 93 | 100 % | – | 202/142 | klasse_unsicher |
| 108 | 200108 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 290 | 100 % | – | 210/105 | klasse_unsicher |
| 110 | 200110 | 1.3.2 Baustelle | nein | nein | 781 | 100 % | – | 235/113 | klasse_unsicher, nicht_zusammenhaengend |
| 132 | 200132 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 204 | 100 % | – | 242/145 | grenze_ohne_bildkante, klasse_unsicher |
| 115 | 200115 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1338 | 100 % | – | 269/129 | grenze_ohne_bildkante, klasse_unsicher |
| 135 | 200135 | 1.2.1 Straße (versiegelt) | nein | nein | 432 | 100 % | – | 70/168 | grenze_ohne_bildkante, klasse_unsicher |
| 116 | 200116 | 1.2.1 Straße (versiegelt) | nein | nein | 318 | 100 % | – | 75/189 | klasse_unsicher |
| 150 | 200150 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 364 | 100 % | – | 88/177 | klasse_unsicher, nicht_zusammenhaengend |
| 145 | 200145 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 420 | 100 % | – | 94/164 | klasse_unsicher |
| 129 | 200129 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 759 | 100 % | – | 104/150 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 160 | 200160 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 590 | 100 % | – | 112/178 | grenze_ohne_bildkante, klasse_unsicher |
| 147 | 200147 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 559 | 100 % | – | 134/162 | klasse_unsicher |
| 156 | 200156 | 1.2.1 Straße (versiegelt) | nein | nein | 273 | 100 % | – | 152/167 | klasse_unsicher |
| 131 | 200131 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 583 | 100 % | – | 162/151 | grenze_ohne_bildkante, klasse_unsicher |
| 167 | 200167 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 532 | 100 % | – | 163/191 | grenze_ohne_bildkante, klasse_unsicher |
| 137 | 200137 | 1.2.1 Straße (versiegelt) | nein | nein | 2641 | 100 % | – | 181/170 | grenze_ohne_bildkante, klasse_unsicher |
| 146 | 200146 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 74 | 100 % | – | 185/152 | klasse_unsicher |
| 153 | 200153 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1516 | 100 % | – | 191/193 | klasse_unsicher, nicht_zusammenhaengend |
| 170 | 200170 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 132 | 100 % | – | 210/192 | klasse_unsicher |
| 143 | 200143 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 269 | 100 % | – | 236/153 | klasse_unsicher, nicht_zusammenhaengend |
| 154 | 200154 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1413 | 100 % | – | 245/186 | grenze_ohne_bildkante, klasse_unsicher |
| 152 | 200152 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 803 | 100 % | – | 265/176 | klasse_unsicher |
| 136 | 200136 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1712 | 100 % | – | 289/174 | klasse_unsicher |
| 165 | 200165 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 506 | 84 % | v2 | 305/195 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 201 | 200201 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 5 | 100 % | – | 64/234 | klasse_unsicher |
| 212 | 200212 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 96 | 100 % | – | 65/224 | klasse_unsicher, nicht_zusammenhaengend |
| 166 | 200166 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 368 | 100 % | – | 69/216 | grenze_ohne_bildkante, klasse_unsicher |
| 227 | 200227 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 604 | 100 % | – | 74/246 | klasse_unsicher |
| 181 | 200181 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 229 | 100 % | – | 75/207 | grenze_ohne_bildkante, klasse_unsicher |
| 230 | 200230 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 87 | 100 % | – | 91/247 | klasse_unsicher, nicht_zusammenhaengend |
| 203 | 200203 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 702 | 100 % | – | 96/236 | grenze_ohne_bildkante, klasse_unsicher |
| 186 | 200186 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 232 | 100 % | – | 103/210 | grenze_ohne_bildkante, klasse_unsicher |
| 183 | 200183 | 1.2.1 Straße (versiegelt) | ja | nein | 3154 | 66 % | v3 | 112/239 | grenze_ohne_bildkante |
| 179 | 200179 | 1.2.1 Straße (versiegelt) | nein | nein | 516 | 100 % | – | 119/222 | klasse_unsicher |
| 187 | 200187 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 648 | 100 % | – | 141/211 | klasse_unsicher, nicht_zusammenhaengend |
| 184 | 200184 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 178 | 100 % | – | 160/208 | klasse_unsicher |
| 202 | 200202 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 90 | 100 % | – | 166/214 | klasse_unsicher |
| 213 | 200213 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1297 | 100 % | – | 166/249 | klasse_unsicher |
| 226 | 200226 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 202 | 100 % | – | 167/233 | klasse_unsicher |
| 196 | 200196 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 518 | 100 % | – | 197/228 | grenze_ohne_bildkante, klasse_unsicher |
| 193 | 200193 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1456 | 100 % | – | 219/226 | klasse_unsicher |
| 162 | 200162 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 997 | 100 % | – | 228/201 | klasse_unsicher |
| 197 | 200197 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 945 | 100 % | – | 257/240 | klasse_unsicher |
| 182 | 200182 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 732 | 100 % | – | 272/233 | klasse_unsicher |
| 194 | 200194 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 890 | 100 % | – | 285/224 | grenze_ohne_bildkante, klasse_unsicher |
| 190 | 200190 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 323 | 98 % | v2 | 298/218 | klasse_unsicher |
| 224 | 200224 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 476 | 54 % | v2 | 308/245 | klasse_unsicher |
| 195 | 200195 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 199 | 65 % | v2 | 309/213 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 249 | 200249 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 387 | 100 % | – | 68/293 | klasse_unsicher |
| 279 | 200279 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 477 | 100 % | – | 90/298 | klasse_unsicher |
| 240 | 200240 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1009 | 100 % | – | 94/266 | klasse_unsicher |
| 269 | 200269 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 134 | 100 % | – | 103/279 | klasse_unsicher, nicht_zusammenhaengend |
| 267 | 200267 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 245 | 100 % | – | 111/288 | klasse_unsicher, nicht_zusammenhaengend |
| 237 | 200237 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 119 | 100 % | – | 120/251 | klasse_unsicher, nicht_zusammenhaengend |
| 247 | 200247 | 1.2.1 Straße (versiegelt) | nein | nein | 143 | 100 % | – | 120/263 | klasse_unsicher |
| 256 | 200256 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 638 | 92 % | v3 | 126/291 | klasse_unsicher, nicht_zusammenhaengend |
| 268 | 200268 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 501 | 100 % | – | 129/280 | klasse_unsicher |
| 220 | 200220 | 1.2.1 Straße (versiegelt) | nein | nein | 970 | 100 % | – | 148/252 | klasse_unsicher |
| 271 | 200271 | 1.2.1 Straße (versiegelt) | nein | nein | 97 | 100 % | – | 169/283 | klasse_unsicher |
| 278 | 200278 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 161 | 100 % | – | 175/293 | klasse_unsicher, nicht_zusammenhaengend |
| 244 | 200244 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 445 | 100 % | – | 182/266 | klasse_unsicher |
| 263 | 200263 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 536 | 100 % | – | 193/283 | grenze_ohne_bildkante, klasse_unsicher |
| 275 | 200275 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 115 | 100 % | – | 208/288 | klasse_unsicher, nicht_zusammenhaengend |
| 206 | 200206 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 858 | 100 % | – | 214/278 | klasse_unsicher |
| 228 | 200228 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1087 | 100 % | – | 215/256 | grenze_ohne_bildkante, klasse_unsicher |
| 277 | 200277 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 232 | 100 % | – | 232/291 | klasse_unsicher, nicht_zusammenhaengend |
| 241 | 200241 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 932 | 100 % | – | 265/290 | grenze_ohne_bildkante, klasse_unsicher |
| 242 | 200242 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 955 | 100 % | – | 272/265 | grenze_ohne_bildkante, klasse_unsicher |
| 232 | 200232 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 114 | 100 % | – | 274/251 | klasse_unsicher, nicht_zusammenhaengend |
| 257 | 200257 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 433 | 100 % | – | 295/283 | klasse_unsicher |
| 245 | 200245 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 904 | 71 % | v2 | 302/266 | grenze_ohne_bildkante, klasse_unsicher |
| 287 | 200287 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 141 | 92 % | v2 | 309/298 | grenze_ohne_bildkante |
| 293 | 200293 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 82 | 100 % | – | 106/302 | klasse_unsicher, nicht_zusammenhaengend |
| 288 | 200288 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 139 | 100 % | – | 113/305 | klasse_unsicher, nicht_zusammenhaengend |
| 284 | 200284 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 485 | 75 % | v3 | 193/301 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 280 | 200280 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 468 | 67 % | v3 | 225/300 | klasse_unsicher |
| 291 | 200291 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 135 | 95 % | v3 | 243/307 | klasse_unsicher |
| 294 | 200294 | 4.2.1 Einzelbaum | nein | ja | 417 | 64 % | v3 | 264/306 | grenze_ohne_bildkante, klasse_unsicher |
| 289 | 200289 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 435 | 60 % | v3 | 283/308 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |

`nicht_geprueft` nennt, was du nicht angesehen hast, `offen`, was du nicht entscheiden konntest.

Kontrolle vor der Rückgabe (muss mit `ok` enden):

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-2/skripte/pruefe_urteil.py --urteil C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r0c1/v1/urteil.json --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r0c1/segmente.json --fassung b --viertel v1 --ids 200070,200086,200059,200087,200068,200061,200088,200064,200098,200007,200100,200066,200101,200092,200080,200074,200013,200011,200017,200102,200122,200125,200113,200117,200141,200094,200123,200130,200133,200108,200110,200132,200115,200135,200116,200150,200145,200129,200160,200147,200156,200131,200167,200137,200146,200153,200170,200143,200154,200152,200136,200165,200201,200212,200166,200227,200181,200230,200203,200186,200183,200179,200187,200184,200202,200213,200226,200196,200193,200162,200197,200182,200194,200190,200224,200195,200249,200279,200240,200269,200267,200237,200247,200256,200268,200220,200271,200278,200244,200263,200275,200206,200228,200277,200241,200242,200232,200257,200245,200287,200293,200288,200284,200280,200291,200294,200289
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
der Bildkante), zur Kontrolle `pruefen`. Eigene Skripte als Datei in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r0c1/v1`.

## Ergebnis in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r0c1/v1` (genau diese Namen)

- `roh.jpg`, `umriss.jpg` (alle Segmentgrenzen mit ID), `maengel.jpg` (nummerierte Punkte mit kurzer
  deutscher Beschriftung, sonst Vermerk „keine Mängel“), `vorschlag.jpg` (Grenzen und Klassen, wie
  du sie setzen würdest, sonst Vermerk „unverändert“): je dein Viertel mit Umgebung, Viertel
  umrandet (Grundlage: die vorbereiteten Übersichtsbilder).
- `nah_<n>.jpg`: eigene Nahansichten von Stellen, die man in den vorbereiteten Bildern nicht beurteilen kann,
  je ein Teil des Viertels samt Nachbarn (mindestens 64 × 64 Bildpunkte der Teilkachel, kein freigestelltes
  Einzelsegment); `kontrast_<n>.jpg` bei blassen Stellen.
- `urteil.json` (UTF-8):

```
{"teilkachel": "r0c1", "viertel": "v1", "bearbeiter": "urt-b-r0c1-v1",
 "bilder_angesehen": {"uebersicht": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r0c1/ganz_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c1/v1/uebersicht_nummern.jpg", "…"],
                      "nah": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c1/v1/nah1_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r0c1/v1/nah_1.jpg", "…"]},
 "segmente": [{"id": 17, "klasse_heute": "Code", "was_ist_es": "ein Satz",
               "urteil": "sauber" | "nicht_sauber", "klasse_vorschlag": null,
               "klasse_frei": {"grob": "Name", "mittel": "Name", "fein": "Name"},
               "sicher": true | false,
               "punkte": [{"nr": 1, "art": "fremdes|fehlt|trennen|verschmelzen|grenze|klasse|zu_klein|sonstiges",
                           "text": "ein Satz mit Stelle (x/y im Teilkachelbild)", "flaeche_px": Zahl oder null}],
               "bilder": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c1/v1/uebersicht_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c1/v1/nah2_roh.jpg"]}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "was an der Kerngrenze nicht passt"}],
 "unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."],
 "klassen_frei": [{"name": "Name", "ebene": "grob|mittel|fein", "eltern": "Name oder null", "merkmal": "woran im Bild erkennbar"}]}
```

Jedes Segment deiner Liste steht genau einmal unter `segmente`, auch die sauberen, in der Reihenfolge der Liste. Segmente der Nachbarviertel (graue Nummern) und des Kontextrands (ohne Nummer) urteilst du in diesem Auftrag nicht; Auffälliges an ihnen nennst du unter `unsicher` mit ID.

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Punkte, Anteil `sicher: false`, wo du unsicher bist.
