# Auftrag: H0, Teilkachel r0c0, Viertel v1: 114 Segmente im Verbund ansehen und einzeln urteilen (Fassung B „Kategorien frei“)

Lies zuerst den Skill `landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `r0c0` des Ausschnitts in `C:/Users/Phil/Developement/Victor/daten/landseg/H0`. Du urteilst über jedes
Segment deines Viertels v1 (Liste unter „Dein Viertel“), ob Grenze und Klasse stimmen, und zeichnest ein, was
du ändern würdest. Die Label-Karte änderst du nicht.

## Daten (eingefrorener Stand, nur lesen)

- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/manifest.json`: Eintrag `r0c0` unter `teilkacheln` mit `bild` (Teilkachelbild,
  Kern + Kontextrand), `kern_im_bild` (Lage des Kerns im Teilkachelbild) und `kern` (Lage im Ausschnitt).
- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r0c0/labels.tif`: Label-Karte (Segment-ID je Bildpunkt, Größe des Teilkachelbilds).
- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r0c0/segmente.json`: je Segment `id`, `klasse`, `grob`, `herkunft`, `sicher`; dazu die
  Kandidatenliste der Vorstufe, falls vorhanden.
- `C:/Users/Phil/Developement/Victor/landseg/kategorien.json` und `C:/Users/Phil/Developement/Victor/landseg/KATEGORIEN.md`: nur Anregung; in Fassung B benennst du die Klassen selbst (Abschnitt „Fassung B“).

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

Viertel v1 (oben links) des Kerns von `r0c0`: x 64–313, y 64–313 im
Teilkachelbild (250 × 250 Bildpunkte). Dir gehören die 114 Segmente der Liste unten: Jedes hat den
größten Teil seiner Kernfläche in diesem Viertel. Die Teilkachel hat 341 Kernsegmente
(v1 114, v2 139, v3 33, v4 55); die anderen Viertel stehen in eigenen Aufträgen mit eigenem Ergebnisordner. Ein Segment
über einer Viertelgrenze urteilt nur das Viertel mit dem größten Anteil; in den Bildern der Nachbarn ist
es mit grauer Nummer als Umgebung zu sehen.

Urteil im Verbund: Du siehst das Viertel als zusammenhängendes Bild mit Umgebung, arbeitest die Liste der
Reihe nach ab und beurteilst jedes Segment im Zusammenhang mit seinen Nachbarn; eingetragen wird jedes
Segment einzeln (Klasse, `sicher`, `was_ist_es` als Notiz). Bilder freigestellter Einzelsegmente gibt es
nicht, und sie sind keine Urteilsgrundlage.

Bilder des Viertels (fertig, JPEG, in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c0/v1`, Fenster und Vergrößerung je Bild in `viertel.json`):

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
Teilkachelbild; Kandidaten aus `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r0c0/kandidaten.json`, dort mit Grund, in den
Bildern nicht eingezeichnet; Anteil hier = Anteil der Kernfläche in diesem Viertel):

| Nr | ID | Klasse Vorstufe | sicher | im Siedlungsgebiet | Kernfläche px | Anteil hier | auch in | Punkt x/y | Kandidaten |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 100001 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 3659 | 100 % | – | 87/87 | grenze_ohne_bildkante, klasse_unsicher |
| 98 | 100098 | 1.2.1 Straße (versiegelt) | nein | nein | 102 | 100 % | – | 116/93 | klasse_unsicher, nicht_zusammenhaengend |
| 89 | 100089 | 1.2.1 Straße (versiegelt) | nein | nein | 79 | 100 % | – | 127/78 | klasse_unsicher |
| 61 | 100061 | 1.2.1 Straße (versiegelt) | nein | nein | 10 | 100 % | – | 139/64 | klasse_unsicher, nicht_zusammenhaengend |
| 99 | 100099 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 149 | 100 % | – | 151/95 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 77 | 100077 | 1.2.1 Straße (versiegelt) | nein | nein | 430 | 100 % | – | 153/80 | klasse_unsicher |
| 64 | 100064 | 2.1 Acker mit Bewuchs | nein | ja | 22 | 100 % | – | 163/65 | klasse_unsicher, nicht_zusammenhaengend |
| 66 | 100066 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 128 | 100 % | – | 175/67 | klasse_unsicher, nicht_zusammenhaengend |
| 79 | 100079 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 171 | 100 % | – | 175/74 | nicht_zusammenhaengend |
| 102 | 100102 | 4.2.1 Einzelbaum | nein | ja | 370 | 100 % | – | 179/97 | klasse_unsicher |
| 51 | 100051 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 282 | 100 % | – | 188/69 | grenze_ohne_bildkante |
| 90 | 100090 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 117 | 100 % | – | 198/89 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 80 | 100080 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 270 | 100 % | – | 202/76 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 62 | 100062 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 6 | 100 % | – | 207/64 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 91 | 100091 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 184 | 100 % | – | 210/89 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 71 | 100071 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 80 | 100 % | – | 217/67 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 46 | 100046 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1 | 100 % | – | 219/64 | klasse_unsicher |
| 106 | 100106 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 144 | 100 % | – | 223/99 | grenze_ohne_bildkante, klasse_unsicher |
| 74 | 100074 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 1774 | 100 % | – | 235/85 | grenze_ohne_bildkante, klasse_unsicher |
| 65 | 100065 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 27 | 100 % | – | 236/65 | grenze_ohne_bildkante, klasse_unsicher |
| 78 | 100078 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 129 | 100 % | – | 244/69 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 35 | 100035 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 570 | 100 % | – | 270/76 | klasse_unsicher |
| 95 | 100095 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 200 | 100 % | – | 281/95 | klasse_unsicher |
| 21 | 100021 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 595 | 100 % | – | 290/74 | grenze_ohne_bildkante, klasse_unsicher |
| 72 | 100072 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 56 | 100 % | – | 305/66 | grenze_ohne_bildkante, klasse_unsicher |
| 39 | 100039 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1 | 100 % | – | 309/64 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 68 | 100068 | 1.3.2 Baustelle | nein | nein | 166 | 59 % | v2 | 310/68 | grenze_ohne_bildkante, klasse_unsicher |
| 148 | 100148 | 1.2.1 Straße (versiegelt) | nein | nein | 145 | 100 % | – | 74/145 | klasse_unsicher |
| 2 | 100002 | 6.6 Weg, unbefestigt (Feld-, Wald-, Schotterweg) | nein | nein | 1719 | 100 % | – | 99/130 | grenze_ohne_bildkante, klasse_unsicher |
| 156 | 100156 | 1.2.1 Straße (versiegelt) | nein | nein | 383 | 100 % | – | 99/149 | grenze_ohne_bildkante, klasse_unsicher |
| 150 | 100150 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 156 | 100 % | – | 106/138 | grenze_ohne_bildkante, klasse_unsicher |
| 133 | 100133 | 1.2.1 Straße (versiegelt) | ja | nein | 208 | 100 % | – | 116/123 | grenze_ohne_bildkante |
| 117 | 100117 | 1.2.1 Straße (versiegelt) | nein | nein | 115 | 100 % | – | 128/112 | grenze_ohne_bildkante, klasse_unsicher |
| 131 | 100131 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 550 | 100 % | – | 132/130 | grenze_ohne_bildkante, klasse_unsicher |
| 104 | 100104 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 188 | 100 % | – | 136/104 | grenze_ohne_bildkante, klasse_unsicher |
| 136 | 100136 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 192 | 100 % | – | 157/128 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 97 | 100097 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 932 | 100 % | – | 161/108 | grenze_ohne_bildkante, klasse_unsicher |
| 145 | 100145 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 628 | 100 % | – | 167/142 | grenze_ohne_bildkante, klasse_unsicher |
| 139 | 100139 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 106 | 100 % | – | 170/127 | klasse_unsicher |
| 118 | 100118 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 139 | 100 % | – | 177/118 | klasse_unsicher, nicht_zusammenhaengend |
| 158 | 100158 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 214 | 100 % | – | 180/147 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 129 | 100129 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 948 | 100 % | – | 188/130 | grenze_ohne_bildkante, klasse_unsicher |
| 84 | 100084 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 677 | 100 % | – | 198/105 | grenze_ohne_bildkante, klasse_unsicher |
| 107 | 100107 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 1285 | 100 % | – | 226/121 | grenze_ohne_bildkante, klasse_unsicher |
| 159 | 100159 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 165 | 100 % | – | 236/148 | klasse_unsicher, nicht_zusammenhaengend |
| 121 | 100121 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 142 | 100 % | – | 242/111 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 137 | 100137 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 317 | 100 % | – | 247/136 | klasse_unsicher, nicht_zusammenhaengend |
| 132 | 100132 | 2.1 Acker mit Bewuchs | nein | ja | 184 | 100 % | – | 257/123 | grenze_ohne_bildkante, klasse_unsicher |
| 109 | 100109 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 114 | 100 % | – | 278/100 | klasse_unsicher, nicht_zusammenhaengend |
| 92 | 100092 | 1.2.1 Straße (versiegelt) | nein | nein | 8353 | 78 % | v2 | 285/141 | grenze_ohne_bildkante, klasse_unsicher |
| 119 | 100119 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 230 | 83 % | v2 | 308/111 | klasse_unsicher, nicht_zusammenhaengend |
| 192 | 100192 | 1.2.1 Straße (versiegelt) | nein | nein | 134 | 100 % | – | 69/183 | grenze_ohne_bildkante, klasse_unsicher |
| 208 | 100208 | 4.2.1 Einzelbaum | nein | ja | 289 | 100 % | – | 77/198 | klasse_unsicher |
| 185 | 100185 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 242 | 100 % | – | 79/173 | grenze_ohne_bildkante, klasse_unsicher |
| 195 | 100195 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 130 | 100 % | – | 81/183 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 196 | 100196 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 327 | 100 % | – | 96/195 | klasse_unsicher |
| 166 | 100166 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 822 | 100 % | – | 104/171 | grenze_ohne_bildkante, klasse_unsicher |
| 154 | 100154 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 809 | 100 % | – | 123/151 | grenze_ohne_bildkante, klasse_unsicher |
| 177 | 100177 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 249 | 100 % | – | 123/175 | klasse_unsicher |
| 200 | 100200 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 119 | 100 % | – | 124/193 | klasse_unsicher, nicht_zusammenhaengend |
| 178 | 100178 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 932 | 100 % | – | 135/188 | klasse_unsicher |
| 157 | 100157 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 207 | 100 % | – | 150/153 | klasse_unsicher, nicht_zusammenhaengend |
| 193 | 100193 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 429 | 100 % | – | 162/187 | klasse_unsicher |
| 167 | 100167 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 699 | 100 % | – | 164/168 | klasse_unsicher |
| 183 | 100183 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 703 | 100 % | – | 191/180 | klasse_unsicher |
| 173 | 100173 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 106 | 100 % | – | 200/166 | grenze_ohne_bildkante, klasse_unsicher |
| 204 | 100204 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 164 | 100 % | – | 205/191 | klasse_unsicher |
| 189 | 100189 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 102 | 100 % | – | 208/182 | klasse_unsicher |
| 143 | 100143 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 320 | 100 % | – | 209/153 | klasse_unsicher |
| 179 | 100179 | 4.2.1 Einzelbaum | nein | ja | 380 | 100 % | – | 215/175 | grenze_ohne_bildkante, klasse_unsicher |
| 160 | 100160 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 271 | 100 % | – | 222/152 | klasse_unsicher |
| 174 | 100174 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 131 | 100 % | – | 223/168 | klasse_unsicher |
| 194 | 100194 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 178 | 86 % | v2 | 289/182 | klasse_unsicher |
| 171 | 100171 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 899 | 71 % | v2 | 303/177 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 205 | 100205 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 231 | 100 % | – | 304/194 | klasse_unsicher |
| 216 | 100216 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 18 | 100 % | – | 65/202 | grenze_ohne_bildkante, klasse_unsicher |
| 289 | 100289 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 10 | 100 % | – | 65/247 | klasse_unsicher, nicht_zusammenhaengend |
| 259 | 100259 | 4.2.1 Einzelbaum | nein | ja | 356 | 100 % | – | 71/232 | klasse_unsicher |
| 238 | 100238 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 356 | 100 % | – | 72/213 | klasse_unsicher, nicht_zusammenhaengend |
| 220 | 100220 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 377 | 100 % | – | 88/209 | klasse_unsicher |
| 248 | 100248 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 98 | 100 % | – | 102/217 | klasse_unsicher, nicht_zusammenhaengend |
| 215 | 100215 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 467 | 100 % | – | 107/203 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 260 | 100260 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 145 | 100 % | – | 110/225 | nicht_zusammenhaengend |
| 225 | 100225 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 1458 | 100 % | – | 141/228 | grenze_ohne_bildkante, klasse_unsicher |
| 247 | 100247 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 700 | 100 % | – | 164/238 | grenze_ohne_bildkante, klasse_unsicher |
| 256 | 100256 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 222 | 100 % | – | 172/225 | grenze_ohne_bildkante, klasse_unsicher |
| 212 | 100212 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 402 | 100 % | – | 176/201 | grenze_ohne_bildkante, klasse_unsicher |
| 249 | 100249 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 150 | 100 % | – | 181/213 | grenze_ohne_bildkante, klasse_unsicher |
| 218 | 100218 | 2.1 Acker mit Bewuchs | nein | ja | 167 | 100 % | – | 192/200 | klasse_unsicher, nicht_zusammenhaengend |
| 207 | 100207 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 140 | 100 % | – | 203/202 | – |
| 230 | 100230 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 200 | 100 % | – | 208/212 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 231 | 100231 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 2076 | 100 % | – | 227/232 | grenze_ohne_bildkante, klasse_unsicher |
| 235 | 100235 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 344 | 100 % | – | 253/212 | grenze_ohne_bildkante, klasse_unsicher |
| 226 | 100226 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 131 | 100 % | – | 268/207 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 252 | 100252 | 1.1.2 Nebengebäude / Schuppen / Stadel | ja | nein | 1584 | 100 % | – | 273/233 | grenze_ohne_bildkante |
| 227 | 100227 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 148 | 100 % | – | 284/210 | grenze_ohne_bildkante, klasse_unsicher |
| 217 | 100217 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 81 | 100 % | – | 298/204 | grenze_ohne_bildkante, klasse_unsicher |
| 272 | 100272 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 120 | 100 % | – | 302/235 | klasse_unsicher |
| 221 | 100221 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 536 | 95 % | v2 | 303/219 | grenze_ohne_bildkante, klasse_unsicher |
| 267 | 100267 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 2503 | 100 % | – | 79/257 | grenze_ohne_bildkante, klasse_unsicher |
| 307 | 100307 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 281 | 100 % | – | 110/271 | klasse_unsicher |
| 264 | 100264 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 1658 | 100 % | – | 120/252 | klasse_unsicher |
| 338 | 100338 | 2.1 Acker mit Bewuchs | nein | ja | 313 | 96 % | v3 | 124/293 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 321 | 100321 | 1.3.2 Baustelle | nein | nein | 139 | 100 % | – | 128/283 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 250 | 100250 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 7379 | 72 % | v3 | 181/273 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 339 | 100339 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 162 | 100 % | – | 213/291 | grenze_ohne_bildkante, klasse_unsicher |
| 296 | 100296 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 344 | 100 % | – | 223/262 | grenze_ohne_bildkante, klasse_unsicher |
| 297 | 100297 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 702 | 100 % | – | 240/269 | grenze_ohne_bildkante, klasse_unsicher |
| 300 | 100300 | 2.1 Acker mit Bewuchs | nein | ja | 317 | 100 % | – | 262/270 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 301 | 100301 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 166 | 100 % | – | 276/268 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 317 | 100317 | 1.2.1 Straße (versiegelt) | nein | nein | 7444 | 50 % | v2, v3 | 281/293 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 285 | 100285 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 202 | 100 % | – | 284/255 | grenze_ohne_bildkante, klasse_unsicher |
| 290 | 100290 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 604 | 95 % | v2 | 301/262 | grenze_ohne_bildkante, klasse_unsicher |
| 310 | 100310 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 1325 | 58 % | v3 | 74/302 | grenze_ohne_bildkante, klasse_unsicher |

`nicht_geprueft` nennt, was du nicht angesehen hast, `offen`, was du nicht entscheiden konntest.

Kontrolle vor der Rückgabe (muss mit `ok` enden):

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-2/skripte/pruefe_urteil.py --urteil C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r0c0/v1/urteil.json --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r0c0/segmente.json --fassung b --viertel v1 --ids 100001,100098,100089,100061,100099,100077,100064,100066,100079,100102,100051,100090,100080,100062,100091,100071,100046,100106,100074,100065,100078,100035,100095,100021,100072,100039,100068,100148,100002,100156,100150,100133,100117,100131,100104,100136,100097,100145,100139,100118,100158,100129,100084,100107,100159,100121,100137,100132,100109,100092,100119,100192,100208,100185,100195,100196,100166,100154,100177,100200,100178,100157,100193,100167,100183,100173,100204,100189,100143,100179,100160,100174,100194,100171,100205,100216,100289,100259,100238,100220,100248,100215,100260,100225,100247,100256,100212,100249,100218,100207,100230,100231,100235,100226,100252,100227,100217,100272,100221,100267,100307,100264,100338,100321,100250,100339,100296,100297,100300,100301,100317,100285,100290,100310
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
der Bildkante), zur Kontrolle `pruefen`. Eigene Skripte als Datei in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r0c0/v1`.

## Ergebnis in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r0c0/v1` (genau diese Namen)

- `roh.jpg`, `umriss.jpg` (alle Segmentgrenzen mit ID), `maengel.jpg` (nummerierte Punkte mit kurzer
  deutscher Beschriftung, sonst Vermerk „keine Mängel“), `vorschlag.jpg` (Grenzen und Klassen, wie
  du sie setzen würdest, sonst Vermerk „unverändert“): je dein Viertel mit Umgebung, Viertel
  umrandet (Grundlage: die vorbereiteten Übersichtsbilder).
- `nah_<n>.jpg`: eigene Nahansichten von Stellen, die man in den vorbereiteten Bildern nicht beurteilen kann,
  je ein Teil des Viertels samt Nachbarn (mindestens 64 × 64 Bildpunkte der Teilkachel, kein freigestelltes
  Einzelsegment); `kontrast_<n>.jpg` bei blassen Stellen.
- `urteil.json` (UTF-8):

```
{"teilkachel": "r0c0", "viertel": "v1", "bearbeiter": "urt-b-r0c0-v1",
 "bilder_angesehen": {"uebersicht": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r0c0/ganz_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c0/v1/uebersicht_nummern.jpg", "…"],
                      "nah": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c0/v1/nah1_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r0c0/v1/nah_1.jpg", "…"]},
 "segmente": [{"id": 17, "klasse_heute": "Code", "was_ist_es": "ein Satz",
               "urteil": "sauber" | "nicht_sauber", "klasse_vorschlag": null,
               "klasse_frei": {"grob": "Name", "mittel": "Name", "fein": "Name"},
               "sicher": true | false,
               "punkte": [{"nr": 1, "art": "fremdes|fehlt|trennen|verschmelzen|grenze|klasse|zu_klein|sonstiges",
                           "text": "ein Satz mit Stelle (x/y im Teilkachelbild)", "flaeche_px": Zahl oder null}],
               "bilder": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c0/v1/uebersicht_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c0/v1/nah2_roh.jpg"]}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "was an der Kerngrenze nicht passt"}],
 "unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."],
 "klassen_frei": [{"name": "Name", "ebene": "grob|mittel|fein", "eltern": "Name oder null", "merkmal": "woran im Bild erkennbar"}]}
```

Jedes Segment deiner Liste steht genau einmal unter `segmente`, auch die sauberen, in der Reihenfolge der Liste. Segmente der Nachbarviertel (graue Nummern) und des Kontextrands (ohne Nummer) urteilst du in diesem Auftrag nicht; Auffälliges an ihnen nennst du unter `unsicher` mit ID.

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Punkte, Anteil `sicher: false`, wo du unsicher bist.
