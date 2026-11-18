# Auftrag: H0, Teilkachel r1c1, Viertel v1: 131 Segmente im Verbund ansehen und einzeln urteilen (Fassung B „Kategorien frei“)

Lies zuerst den Skill `landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `r1c1` des Ausschnitts in `C:/Users/Phil/Developement/Victor/daten/landseg/H0`. Du urteilst über jedes
Segment deines Viertels v1 (Liste unter „Dein Viertel“), ob Grenze und Klasse stimmen, und zeichnest ein, was
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

Viertel v1 (oben links) des Kerns von `r1c1`: x 64–313, y 64–313 im
Teilkachelbild (250 × 250 Bildpunkte). Dir gehören die 131 Segmente der Liste unten: Jedes hat den
größten Teil seiner Kernfläche in diesem Viertel. Die Teilkachel hat 518 Kernsegmente
(v1 131, v2 147, v3 67, v4 173); die anderen Viertel stehen in eigenen Aufträgen mit eigenem Ergebnisordner. Ein Segment
über einer Viertelgrenze urteilt nur das Viertel mit dem größten Anteil; in den Bildern der Nachbarn ist
es mit grauer Nummer als Umgebung zu sehen.

Urteil im Verbund: Du siehst das Viertel als zusammenhängendes Bild mit Umgebung, arbeitest die Liste der
Reihe nach ab und beurteilst jedes Segment im Zusammenhang mit seinen Nachbarn; eingetragen wird jedes
Segment einzeln (Klasse, `sicher`, `was_ist_es` als Notiz). Bilder freigestellter Einzelsegmente gibt es
nicht, und sie sind keine Urteilsgrundlage.

Bilder des Viertels (fertig, JPEG, in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c1/v1`, Fenster und Vergrößerung je Bild in `viertel.json`):

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
| 87 | 400087 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 7 | 100 % | – | 64/64 | klasse_unsicher |
| 2 | 400002 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 30 | 100 % | – | 67/65 | grenze_ohne_bildkante, klasse_unsicher |
| 109 | 400109 | 6.6 Weg, unbefestigt (Feld-, Wald-, Schotterweg) | nein | nein | 66 | 100 % | – | 67/77 | klasse_unsicher |
| 3 | 400003 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 684 | 100 % | – | 79/72 | grenze_ohne_bildkante, klasse_unsicher |
| 68 | 400068 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 34 | 100 % | – | 96/65 | grenze_ohne_bildkante, klasse_unsicher |
| 94 | 400094 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 157 | 100 % | – | 106/68 | klasse_unsicher |
| 125 | 400125 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 153 | 100 % | – | 111/91 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 92 | 400092 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 426 | 100 % | – | 125/75 | klasse_unsicher |
| 95 | 400095 | 1.3.2 Baustelle | nein | nein | 712 | 100 % | – | 129/91 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 83 | 400083 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 67 | 100 % | – | 137/66 | klasse_unsicher |
| 108 | 400108 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 162 | 100 % | – | 146/77 | klasse_unsicher |
| 133 | 400133 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 187 | 100 % | – | 153/97 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 82 | 400082 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 237 | 100 % | – | 154/70 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 86 | 400086 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 531 | 100 % | – | 169/72 | klasse_unsicher, nicht_zusammenhaengend |
| 79 | 400079 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 62 | 100 % | – | 191/66 | klasse_unsicher |
| 112 | 400112 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 478 | 100 % | – | 192/85 | klasse_unsicher |
| 97 | 400097 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 168 | 100 % | – | 203/70 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 129 | 400129 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 294 | 100 % | – | 204/99 | grenze_ohne_bildkante, klasse_unsicher |
| 117 | 400117 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 102 | 100 % | – | 208/87 | klasse_unsicher |
| 65 | 400065 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 444 | 100 % | – | 222/71 | grenze_ohne_bildkante, klasse_unsicher |
| 111 | 400111 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 340 | 100 % | – | 229/84 | grenze_ohne_bildkante, klasse_unsicher |
| 105 | 400105 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 98 | 100 % | – | 239/80 | klasse_unsicher, nicht_zusammenhaengend |
| 98 | 400098 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 195 | 100 % | – | 248/70 | klasse_unsicher |
| 89 | 400089 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 580 | 100 % | – | 259/80 | grenze_ohne_bildkante, klasse_unsicher |
| 84 | 400084 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 42 | 100 % | – | 260/68 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 130 | 400130 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 475 | 100 % | – | 263/95 | klasse_unsicher, nicht_zusammenhaengend |
| 91 | 400091 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 48 | 100 % | – | 279/66 | klasse_unsicher, nicht_zusammenhaengend |
| 66 | 400066 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 282 | 100 % | – | 289/69 | grenze_ohne_bildkante, klasse_unsicher |
| 128 | 400128 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 583 | 100 % | v2 | 303/98 | grenze_ohne_bildkante, klasse_unsicher |
| 15 | 400015 | 2.1 Acker mit Bewuchs | nein | ja | 11 | 100 % | – | 308/65 | klasse_unsicher |
| 124 | 400124 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 752 | 100 % | – | 94/105 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 194 | 400194 | 3.1 Wiese / Weide (gemeinsam) | ja | ja | 134 | 100 % | – | 117/148 | grenze_ohne_bildkante |
| 186 | 400186 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 181 | 100 % | – | 118/136 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 141 | 400141 | 6.6 Weg, unbefestigt (Feld-, Wald-, Schotterweg) | nein | nein | 1085 | 100 % | – | 125/110 | grenze_ohne_bildkante, klasse_unsicher |
| 161 | 400161 | 1.3.2 Baustelle | nein | nein | 750 | 100 % | – | 127/148 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 165 | 400165 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 114 | 100 % | – | 137/125 | grenze_ohne_bildkante, klasse_unsicher |
| 175 | 400175 | 1.1.2 Nebengebäude / Schuppen / Stadel | ja | nein | 900 | 100 % | – | 163/139 | – |
| 102 | 400102 | 1.3.2 Baustelle | nein | nein | 2550 | 100 % | – | 165/111 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 148 | 400148 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 131 | 100 % | – | 178/105 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 145 | 400145 | 1.3.2 Baustelle | nein | nein | 148 | 100 % | – | 188/106 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 177 | 400177 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 232 | 100 % | – | 212/130 | klasse_unsicher |
| 127 | 400127 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 1038 | 100 % | – | 219/105 | grenze_ohne_bildkante, klasse_unsicher |
| 181 | 400181 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 676 | 100 % | – | 219/143 | grenze_ohne_bildkante, klasse_unsicher |
| 164 | 400164 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 530 | 100 % | – | 225/122 | grenze_ohne_bildkante, klasse_unsicher |
| 146 | 400146 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 422 | 100 % | – | 245/106 | klasse_unsicher |
| 189 | 400189 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 688 | 100 % | – | 248/146 | klasse_unsicher |
| 147 | 400147 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 671 | 100 % | – | 269/109 | klasse_unsicher |
| 171 | 400171 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 688 | 100 % | – | 272/134 | klasse_unsicher |
| 198 | 400198 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 83 | 100 % | – | 279/145 | klasse_unsicher |
| 134 | 400134 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 377 | 100 % | – | 288/103 | grenze_ohne_bildkante, klasse_unsicher |
| 170 | 400170 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 248 | 100 % | – | 292/126 | grenze_ohne_bildkante, klasse_unsicher |
| 179 | 400179 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 835 | 67 % | v2 | 304/144 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 138 | 400138 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | ja | ja | 4902 | 100 % | – | 92/177 | grenze_ohne_bildkante |
| 220 | 400220 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 172 | 100 % | – | 128/175 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 207 | 400207 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 180 | 100 % | – | 146/159 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 239 | 400239 | 1.3.2 Baustelle | nein | nein | 136 | 100 % | – | 146/188 | klasse_unsicher, nicht_zusammenhaengend |
| 215 | 400215 | 6.6 Weg, unbefestigt (Feld-, Wald-, Schotterweg) | nein | nein | 551 | 100 % | – | 149/175 | grenze_ohne_bildkante, klasse_unsicher |
| 201 | 400201 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 910 | 100 % | – | 167/166 | grenze_ohne_bildkante, klasse_unsicher |
| 229 | 400229 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 831 | 100 % | – | 176/193 | grenze_ohne_bildkante, klasse_unsicher |
| 206 | 400206 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 156 | 100 % | – | 207/156 | klasse_unsicher |
| 208 | 400208 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 236 | 100 % | – | 213/165 | klasse_unsicher |
| 219 | 400219 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 859 | 100 % | – | 214/182 | klasse_unsicher |
| 202 | 400202 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 130 | 100 % | – | 225/161 | klasse_unsicher |
| 247 | 400247 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 126 | 100 % | – | 236/199 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 227 | 400227 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 375 | 100 % | – | 238/186 | grenze_ohne_bildkante, klasse_unsicher |
| 204 | 400204 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 527 | 100 % | – | 247/165 | grenze_ohne_bildkante, klasse_unsicher |
| 242 | 400242 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 169 | 100 % | – | 256/199 | grenze_ohne_bildkante, klasse_unsicher |
| 222 | 400222 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 387 | 100 % | – | 260/173 | grenze_ohne_bildkante, klasse_unsicher |
| 233 | 400233 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 116 | 100 % | – | 266/182 | klasse_unsicher |
| 213 | 400213 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 229 | 100 % | – | 277/165 | klasse_unsicher |
| 192 | 400192 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 187 | 100 % | – | 284/155 | klasse_unsicher |
| 226 | 400226 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 605 | 100 % | – | 285/184 | grenze_ohne_bildkante, klasse_unsicher |
| 205 | 400205 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 254 | 100 % | – | 292/161 | klasse_unsicher, nicht_zusammenhaengend |
| 214 | 400214 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 254 | 100 % | – | 303/173 | grenze_ohne_bildkante, klasse_unsicher |
| 228 | 400228 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 862 | 65 % | v2 | 304/193 | grenze_ohne_bildkante, klasse_unsicher |
| 255 | 400255 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | nein | 780 | 100 % | – | 76/216 | grenze_ohne_bildkante, klasse_unsicher |
| 232 | 400232 | 6.6 Weg, unbefestigt (Feld-, Wald-, Schotterweg) | nein | nein | 2358 | 100 % | – | 108/219 | klasse_unsicher |
| 249 | 400249 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 266 | 100 % | – | 135/206 | grenze_ohne_bildkante, klasse_unsicher |
| 275 | 400275 | 1.3.4 Sport-, Spielplatz (künstlicher Belag) | nein | nein | 139 | 100 % | – | 149/219 | grenze_ohne_bildkante, klasse_unsicher |
| 259 | 400259 | 4.2.4 Gebüsch / Strauchfläche | nein | ja | 75 | 100 % | – | 150/207 | klasse_unsicher |
| 284 | 400284 | 4.2.4 Gebüsch / Strauchfläche | nein | ja | 114 | 100 % | – | 157/225 | klasse_unsicher |
| 263 | 400263 | 1.2.1 Straße (versiegelt) | nein | nein | 79 | 100 % | – | 165/216 | grenze_ohne_bildkante, klasse_unsicher |
| 303 | 400303 | 4.2.4 Gebüsch / Strauchfläche | nein | ja | 133 | 100 % | – | 169/242 | klasse_unsicher |
| 267 | 400267 | 1.3.2 Baustelle | nein | nein | 149 | 100 % | – | 174/214 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 270 | 400270 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 308 | 100 % | – | 187/220 | grenze_ohne_bildkante, klasse_unsicher |
| 285 | 400285 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 988 | 100 % | – | 192/243 | grenze_ohne_bildkante, klasse_unsicher |
| 246 | 400246 | 4.2.4 Gebüsch / Strauchfläche | nein | ja | 153 | 100 % | – | 201/212 | klasse_unsicher |
| 251 | 400251 | 1.3.2 Baustelle | nein | nein | 147 | 100 % | – | 207/205 | klasse_unsicher, nicht_zusammenhaengend |
| 250 | 400250 | 1.2.1 Straße (versiegelt) | nein | nein | 1242 | 100 % | – | 213/232 | grenze_ohne_bildkante, klasse_unsicher |
| 235 | 400235 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 273 | 100 % | – | 222/204 | klasse_unsicher, nicht_zusammenhaengend |
| 264 | 400264 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 298 | 100 % | – | 228/213 | klasse_unsicher |
| 299 | 400299 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 313 | 100 % | – | 244/243 | grenze_ohne_bildkante, klasse_unsicher |
| 241 | 400241 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1001 | 100 % | – | 263/208 | klasse_unsicher, nicht_zusammenhaengend |
| 302 | 400302 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 315 | 100 % | – | 265/246 | klasse_unsicher |
| 280 | 400280 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 332 | 100 % | – | 268/229 | grenze_ohne_bildkante, klasse_unsicher |
| 293 | 400293 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 172 | 100 % | – | 279/240 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 292 | 400292 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 107 | 100 % | – | 286/230 | grenze_ohne_bildkante, klasse_unsicher |
| 268 | 400268 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 310 | 100 % | – | 290/218 | grenze_ohne_bildkante, klasse_unsicher |
| 256 | 400256 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 112 | 100 % | – | 294/206 | grenze_ohne_bildkante, klasse_unsicher |
| 291 | 400291 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 145 | 100 % | – | 295/229 | grenze_ohne_bildkante, klasse_unsicher |
| 308 | 400308 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 180 | 100 % | – | 295/246 | grenze_ohne_bildkante, klasse_unsicher |
| 278 | 400278 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 122 | 99 % | v2 | 303/221 | grenze_ohne_bildkante, klasse_unsicher |
| 282 | 400282 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 455 | 58 % | v2 | 305/234 | grenze_ohne_bildkante, klasse_unsicher |
| 306 | 400306 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 116 | 91 % | v2 | 307/246 | klasse_unsicher, nicht_zusammenhaengend |
| 260 | 400260 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 217 | 68 % | v2 | 308/212 | grenze_ohne_bildkante, klasse_unsicher |
| 343 | 400343 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 30 | 100 % | – | 66/269 | klasse_unsicher |
| 274 | 400274 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | nein | 4426 | 91 % | v3 | 100/269 | grenze_ohne_bildkante, klasse_unsicher |
| 312 | 400312 | 6.6 Weg, unbefestigt (Feld-, Wald-, Schotterweg) | nein | nein | 86 | 100 % | – | 184/260 | grenze_ohne_bildkante, klasse_unsicher |
| 331 | 400331 | 1.2.1 Straße (versiegelt) | nein | nein | 493 | 100 % | – | 194/270 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 319 | 400319 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 969 | 100 % | – | 214/272 | klasse_unsicher |
| 364 | 400364 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 398 | 100 % | – | 229/299 | klasse_unsicher |
| 315 | 400315 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 229 | 100 % | – | 230/269 | klasse_unsicher |
| 313 | 400313 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 285 | 100 % | – | 232/256 | klasse_unsicher |
| 346 | 400346 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 87 | 100 % | – | 232/281 | – |
| 337 | 400337 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 383 | 100 % | – | 247/273 | klasse_unsicher |
| 356 | 400356 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 269 | 100 % | – | 249/288 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 316 | 400316 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 297 | 100 % | – | 250/257 | klasse_unsicher |
| 350 | 400350 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 79 | 100 % | – | 260/281 | klasse_unsicher, nicht_zusammenhaengend |
| 368 | 400368 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 265 | 100 % | – | 261/298 | klasse_unsicher |
| 334 | 400334 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 174 | 100 % | – | 265/266 | klasse_unsicher |
| 349 | 400349 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 186 | 100 % | – | 269/278 | grenze_ohne_bildkante, klasse_unsicher |
| 352 | 400352 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 358 | 100 % | – | 277/288 | klasse_unsicher |
| 310 | 400310 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 314 | 100 % | – | 279/253 | grenze_ohne_bildkante, klasse_unsicher |
| 332 | 400332 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 187 | 100 % | – | 282/267 | klasse_unsicher, nicht_zusammenhaengend |
| 339 | 400339 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 671 | 100 % | – | 292/278 | klasse_unsicher |
| 329 | 400329 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 116 | 100 % | – | 293/261 | klasse_unsicher, nicht_zusammenhaengend |
| 361 | 400361 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 477 | 93 % | v2, v3 | 306/294 | klasse_unsicher |
| 266 | 400266 | 1.3.2 Baustelle | nein | nein | 1928 | 81 % | v3 | 190/301 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 377 | 400377 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 481 | 59 % | v3 | 245/306 | klasse_unsicher |
| 387 | 400387 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 219 | 78 % | v3 | 268/307 | klasse_unsicher |
| 386 | 400386 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 108 | 62 % | v3 | 303/311 | klasse_unsicher |

`nicht_geprueft` nennt, was du nicht angesehen hast, `offen`, was du nicht entscheiden konntest.

Kontrolle vor der Rückgabe (muss mit `ok` enden):

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-2/skripte/pruefe_urteil.py --urteil C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c1/v1/urteil.json --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r1c1/segmente.json --fassung b --viertel v1 --ids 400087,400002,400109,400003,400068,400094,400125,400092,400095,400083,400108,400133,400082,400086,400079,400112,400097,400129,400117,400065,400111,400105,400098,400089,400084,400130,400091,400066,400128,400015,400124,400194,400186,400141,400161,400165,400175,400102,400148,400145,400177,400127,400181,400164,400146,400189,400147,400171,400198,400134,400170,400179,400138,400220,400207,400239,400215,400201,400229,400206,400208,400219,400202,400247,400227,400204,400242,400222,400233,400213,400192,400226,400205,400214,400228,400255,400232,400249,400275,400259,400284,400263,400303,400267,400270,400285,400246,400251,400250,400235,400264,400299,400241,400302,400280,400293,400292,400268,400256,400291,400308,400278,400282,400306,400260,400343,400274,400312,400331,400319,400364,400315,400313,400346,400337,400356,400316,400350,400368,400334,400349,400352,400310,400332,400339,400329,400361,400266,400377,400387,400386
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
der Bildkante), zur Kontrolle `pruefen`. Eigene Skripte als Datei in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c1/v1`.

## Ergebnis in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c1/v1` (genau diese Namen)

- `roh.jpg`, `umriss.jpg` (alle Segmentgrenzen mit ID), `maengel.jpg` (nummerierte Punkte mit kurzer
  deutscher Beschriftung, sonst Vermerk „keine Mängel“), `vorschlag.jpg` (Grenzen und Klassen, wie
  du sie setzen würdest, sonst Vermerk „unverändert“): je dein Viertel mit Umgebung, Viertel
  umrandet (Grundlage: die vorbereiteten Übersichtsbilder).
- `nah_<n>.jpg`: eigene Nahansichten von Stellen, die man in den vorbereiteten Bildern nicht beurteilen kann,
  je ein Teil des Viertels samt Nachbarn (mindestens 64 × 64 Bildpunkte der Teilkachel, kein freigestelltes
  Einzelsegment); `kontrast_<n>.jpg` bei blassen Stellen.
- `urteil.json` (UTF-8):

```
{"teilkachel": "r1c1", "viertel": "v1", "bearbeiter": "urt-b-r1c1-v1",
 "bilder_angesehen": {"uebersicht": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r1c1/ganz_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c1/v1/uebersicht_nummern.jpg", "…"],
                      "nah": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c1/v1/nah1_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c1/v1/nah_1.jpg", "…"]},
 "segmente": [{"id": 17, "klasse_heute": "Code", "was_ist_es": "ein Satz",
               "urteil": "sauber" | "nicht_sauber", "klasse_vorschlag": null,
               "klasse_frei": {"grob": "Name", "mittel": "Name", "fein": "Name"},
               "sicher": true | false,
               "punkte": [{"nr": 1, "art": "fremdes|fehlt|trennen|verschmelzen|grenze|klasse|zu_klein|sonstiges",
                           "text": "ein Satz mit Stelle (x/y im Teilkachelbild)", "flaeche_px": Zahl oder null}],
               "bilder": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c1/v1/uebersicht_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c1/v1/nah2_roh.jpg"]}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "was an der Kerngrenze nicht passt"}],
 "unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."],
 "klassen_frei": [{"name": "Name", "ebene": "grob|mittel|fein", "eltern": "Name oder null", "merkmal": "woran im Bild erkennbar"}]}
```

Jedes Segment deiner Liste steht genau einmal unter `segmente`, auch die sauberen, in der Reihenfolge der Liste. Segmente der Nachbarviertel (graue Nummern) und des Kontextrands (ohne Nummer) urteilst du in diesem Auftrag nicht; Auffälliges an ihnen nennst du unter `unsicher` mit ID.

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Punkte, Anteil `sicher: false`, wo du unsicher bist.
