# Auftrag: Teilkachel r1c1, Viertel v4: 112 Segmente im Verbund ansehen und einzeln urteilen (Fassung B: Kategorien frei)

Lies zuerst den Skill `landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `r1c1` des Ausschnitts in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b`. Du urteilst über jedes
Segment deines Viertels v4 (Liste unter „Dein Viertel“), ob Grenze und Klasse stimmen, und zeichnest ein, was
du ändern würdest. Die Label-Karte änderst du nicht.

## Daten (eingefrorener Stand, nur lesen)

- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/manifest.json`: Eintrag `r1c1` unter `teilkacheln` mit `bild` (Teilkachelbild,
  Kern + Kontextrand), `kern_im_bild` (Lage des Kerns im Teilkachelbild) und `kern` (Lage im Ausschnitt).
- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/vorstufe/r1c1/labels.tif`: Label-Karte (Segment-ID je Bildpunkt, Größe des Teilkachelbilds).
- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/vorstufe/r1c1/segmente.json`: je Segment `id`, `klasse`, `grob`, `herkunft`, `sicher`; dazu die
  Kandidatenliste der Vorstufe, falls vorhanden.
- `C:/Users/Phil/Developement/Victor/landseg/kategorien.json` und `C:/Users/Phil/Developement/Victor/landseg/KATEGORIEN.md`: nur Anregung; in Fassung B benennst du die Klassen selbst (Abschnitt „Fassung B“).

## Dein Viertel

Viertel v4 (unten rechts) des Kerns von `r1c1`: x 314–563, y 314–563 im
Teilkachelbild (250 × 250 Bildpunkte). Dir gehören die 112 Segmente der Liste unten: Jedes hat den
größten Teil seiner Kernfläche in diesem Viertel. Die Teilkachel hat 301 Kernsegmente
(v1 44, v2 52, v3 93, v4 112); drei andere Agents urteilen gleichzeitig über die anderen Viertel, jeder in seinem eigenen
Ordner. Ein Segment über einer Viertelgrenze urteilt nur das Viertel mit dem größten Anteil; in den Bildern
der Nachbarn ist es mit grauer Nummer als Umgebung zu sehen.

Urteil im Verbund: Du siehst das Viertel als zusammenhängendes Bild mit Umgebung, arbeitest die Liste der
Reihe nach ab und beurteilst jedes Segment im Zusammenhang mit seinen Nachbarn; eingetragen wird jedes
Segment einzeln (Klasse, `sicher`, `was_ist_es` als Notiz). Bilder freigestellter Einzelsegmente gibt es
nicht, und sie sind keine Urteilsgrundlage.

Bilder des Viertels (fertig, JPEG, in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r1c1/v4`, Fenster und Vergrößerung je Bild in `viertel.json`):

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
(`uebersicht`: mindestens `uebersicht_nummern.jpg`; `nah`: vorbereitete und eigene Nahansichten, absolute
Pfade), je Segment unter `bilder` die Bilder, auf denen du es beurteilt hast (mindestens eines).

Liste (Reihenfolge der Abarbeitung, zeilenweise von oben links; Punkt = Stelle sicher im Segment, im
Teilkachelbild; Kandidaten aus `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/vorstufe/r1c1/kandidaten.json`, dort mit Grund, in den
Bildern nicht eingezeichnet; Anteil hier = Anteil der Kernfläche in diesem Viertel):

| Nr | ID | Klasse Vorstufe | sicher | im Siedlungsgebiet | Kernfläche px | Anteil hier | auch in | Punkt x/y | Kandidaten |
|---|---|---|---|---|---|---|---|---|---|
| 142 | 400142 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 329 | 100 % | – | 321/329 | klasse_unsicher |
| 128 | 400128 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 794 | 73 % | v2 | 338/324 | klasse_unsicher |
| 150 | 400150 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 173 | 100 % | – | 353/338 | grenze_ohne_bildkante, klasse_unsicher |
| 134 | 400134 | 4.1 Wald (geschlossener Bestand) | nein | nein | 145 | 97 % | v2 | 354/326 | klasse_unsicher |
| 155 | 400155 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 23 | 100 % | – | 358/339 | grenze_ohne_bildkante, zu_klein |
| 157 | 400157 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 206 | 100 % | – | 364/347 | grenze_ohne_bildkante, klasse_unsicher |
| 156 | 400156 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 4 | 100 % | – | 366/338 | klasse_unsicher, zu_klein |
| 139 | 400139 | 4.2.1 Einzelbaum | nein | ja | 1461 | 100 % | – | 384/348 | grenze_ohne_bildkante, klasse_unsicher |
| 135 | 400135 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 104 | 94 % | v2 | 396/321 | – |
| 136 | 400136 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 280 | 100 % | – | 430/334 | klasse_unsicher |
| 145 | 400145 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 541 | 100 % | – | 444/331 | klasse_unsicher |
| 131 | 400131 | 4.1 Wald (geschlossener Bestand) | nein | nein | 187 | 53 % | v2 | 452/317 | grenze_ohne_bildkante, klasse_unsicher |
| 147 | 400147 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 557 | 100 % | – | 503/334 | klasse_unsicher |
| 132 | 400132 | 4.1 Wald (geschlossener Bestand) | nein | nein | 464 | 98 % | v2 | 557/321 | grenze_ohne_bildkante, klasse_unsicher |
| 129 | 400129 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 106 | 100 % | – | 561/336 | grenze_ohne_bildkante, klasse_unsicher |
| 152 | 400152 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 1069 | 89 % | v3 | 326/359 | klasse_unsicher |
| 183 | 400183 | 4.1 Wald (geschlossener Bestand) | nein | nein | 137 | 100 % | – | 336/377 | klasse_unsicher |
| 190 | 400190 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 122 | 100 % | – | 340/383 | grenze_ohne_bildkante, klasse_unsicher |
| 198 | 400198 | 1.2.1 Straße (versiegelt) | nein | nein | 147 | 100 % | – | 340/398 | grenze_ohne_bildkante, klasse_unsicher |
| 171 | 400171 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 90 | 100 % | – | 343/369 | klasse_unsicher |
| 163 | 400163 | 4.1 Wald (geschlossener Bestand) | nein | nein | 182 | 100 % | – | 348/356 | grenze_ohne_bildkante, klasse_unsicher |
| 174 | 400174 | 1.1.2 Nebengebäude / Schuppen / Stadel | ja | nein | 654 | 100 % | – | 357/380 | grenze_ohne_bildkante |
| 168 | 400168 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 226 | 100 % | – | 362/358 | grenze_ohne_bildkante, klasse_unsicher |
| 194 | 400194 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 118 | 100 % | – | 372/386 | grenze_ohne_bildkante |
| 173 | 400173 | 4.1 Wald (geschlossener Bestand) | nein | nein | 92 | 100 % | – | 379/364 | klasse_unsicher |
| 179 | 400179 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 185 | 100 % | – | 382/372 | klasse_unsicher |
| 176 | 400176 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 219 | 100 % | – | 395/370 | grenze_ohne_bildkante, klasse_unsicher |
| 197 | 400197 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 85 | 100 % | – | 465/393 | klasse_unsicher |
| 165 | 400165 | 4.2.1 Einzelbaum | nein | ja | 443 | 100 % | – | 467/359 | klasse_unsicher |
| 191 | 400191 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 106 | 100 % | – | 475/382 | klasse_unsicher |
| 180 | 400180 | 4.2.1 Einzelbaum | nein | ja | 397 | 100 % | – | 501/375 | klasse_unsicher |
| 153 | 400153 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 512 | 100 % | – | 502/352 | – |
| 195 | 400195 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 76 | 100 % | – | 535/388 | grenze_ohne_bildkante, klasse_unsicher |
| 172 | 400172 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | ja | nein | 220 | 100 % | – | 541/378 | grenze_ohne_bildkante |
| 192 | 400192 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 666 | 100 % | – | 551/394 | grenze_ohne_bildkante, klasse_unsicher |
| 181 | 400181 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 259 | 100 % | – | 556/375 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 159 | 400159 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 168 | 100 % | – | 559/359 | grenze_ohne_bildkante, klasse_unsicher |
| 188 | 400188 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 2 | 100 % | – | 563/385 | klasse_unsicher |
| 236 | 400236 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 85 | 100 % | – | 338/443 | klasse_unsicher |
| 226 | 400226 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 1093 | 100 % | – | 359/442 | grenze_ohne_bildkante, klasse_unsicher |
| 215 | 400215 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 36 | 100 % | – | 395/419 | grenze_ohne_bildkante, nicht_zusammenhaengend, zu_klein |
| 208 | 400208 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 45 | 100 % | – | 396/404 | nicht_zusammenhaengend, zu_klein |
| 212 | 400212 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 185 | 100 % | – | 401/414 | klasse_unsicher |
| 205 | 400205 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 220 | 100 % | – | 403/401 | klasse_unsicher |
| 187 | 400187 | 4.2.1 Einzelbaum | nein | ja | 2289 | 100 % | – | 425/423 | grenze_ohne_bildkante, klasse_unsicher |
| 234 | 400234 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 159 | 100 % | – | 462/445 | klasse_unsicher |
| 209 | 400209 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 314 | 100 % | – | 467/415 | grenze_ohne_bildkante |
| 196 | 400196 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 690 | 100 % | – | 479/400 | grenze_ohne_bildkante, klasse_unsicher |
| 235 | 400235 | 4.1 Wald (geschlossener Bestand) | nein | nein | 668 | 100 % | – | 515/449 | klasse_unsicher |
| 202 | 400202 | 4.1 Wald (geschlossener Bestand) | nein | nein | 202 | 100 % | – | 518/403 | klasse_unsicher |
| 204 | 400204 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 184 | 100 % | – | 529/400 | – |
| 211 | 400211 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 335 | 100 % | – | 536/412 | klasse_unsicher |
| 219 | 400219 | 4.2.1 Einzelbaum | nein | ja | 768 | 100 % | – | 540/434 | grenze_ohne_bildkante, klasse_unsicher |
| 213 | 400213 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 215 | 100 % | – | 552/414 | klasse_unsicher |
| 217 | 400217 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 4 | 100 % | – | 563/414 | nicht_zusammenhaengend |
| 221 | 400221 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 8 | 100 % | – | 563/419 | klasse_unsicher |
| 258 | 400258 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 96 | 100 % | – | 320/480 | – |
| 256 | 400256 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 146 | 100 % | – | 326/472 | klasse_unsicher |
| 281 | 400281 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 212 | 100 % | – | 338/497 | klasse_unsicher |
| 238 | 400238 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 782 | 100 % | – | 344/459 | klasse_unsicher |
| 263 | 400263 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 111 | 100 % | – | 344/475 | – |
| 259 | 400259 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 1685 | 100 % | – | 356/489 | grenze_ohne_bildkante, klasse_unsicher |
| 250 | 400250 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 76 | 100 % | – | 364/460 | grenze_ohne_bildkante |
| 276 | 400276 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 119 | 100 % | – | 374/492 | klasse_unsicher |
| 254 | 400254 | 4.1 Wald (geschlossener Bestand) | nein | nein | 94 | 100 % | – | 381/470 | klasse_unsicher |
| 264 | 400264 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 531 | 100 % | – | 390/490 | klasse_unsicher |
| 252 | 400252 | 4.1 Wald (geschlossener Bestand) | nein | nein | 181 | 100 % | – | 400/472 | grenze_ohne_bildkante, klasse_unsicher |
| 67 | 400067 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 25645 | 75 % | v1, v2, v3 | 454/482 | grenze_ohne_bildkante, klasse_unsicher |
| 239 | 400239 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 319 | 100 % | – | 470/455 | – |
| 246 | 400246 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 94 | 100 % | – | 486/458 | klasse_unsicher |
| 274 | 400274 | 4.2.1 Einzelbaum | nein | ja | 161 | 100 % | – | 486/488 | klasse_unsicher |
| 251 | 400251 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 637 | 100 % | – | 509/469 | grenze_ohne_bildkante, klasse_unsicher |
| 277 | 400277 | 4.2.1 Einzelbaum | nein | ja | 156 | 100 % | – | 518/498 | grenze_ohne_bildkante, klasse_unsicher |
| 245 | 400245 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 864 | 100 % | – | 530/479 | grenze_ohne_bildkante, klasse_unsicher |
| 222 | 400222 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 862 | 100 % | – | 547/456 | grenze_ohne_bildkante, klasse_unsicher |
| 255 | 400255 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 139 | 100 % | – | 550/475 | klasse_unsicher |
| 260 | 400260 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 265 | 100 % | – | 558/482 | klasse_unsicher |
| 233 | 400233 | 4.2.1 Einzelbaum | nein | ja | 29 | 100 % | – | 561/465 | grenze_ohne_bildkante, klasse_unsicher |
| 294 | 400294 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 104 | 100 % | – | 332/512 | grenze_ohne_bildkante, klasse_unsicher |
| 295 | 400295 | 4.1 Wald (geschlossener Bestand) | nein | nein | 312 | 100 % | – | 340/523 | grenze_ohne_bildkante, klasse_unsicher |
| 278 | 400278 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 224 | 100 % | – | 342/512 | grenze_ohne_bildkante, klasse_unsicher |
| 293 | 400293 | 4.2.1 Einzelbaum | nein | ja | 118 | 100 % | – | 363/514 | klasse_unsicher |
| 299 | 400299 | 4.2.1 Einzelbaum | nein | ja | 2476 | 100 % | – | 371/535 | grenze_ohne_bildkante, klasse_unsicher |
| 282 | 400282 | 4.1 Wald (geschlossener Bestand) | nein | nein | 795 | 100 % | – | 410/510 | grenze_ohne_bildkante, klasse_unsicher |
| 300 | 400300 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 257 | 100 % | – | 435/522 | klasse_unsicher |
| 296 | 400296 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 490 | 100 % | – | 448/523 | klasse_unsicher |
| 307 | 400307 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 437 | 100 % | – | 460/537 | klasse_unsicher |
| 301 | 400301 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 730 | 100 % | – | 477/549 | grenze_ohne_bildkante, klasse_unsicher |
| 286 | 400286 | 4.1 Wald (geschlossener Bestand) | nein | nein | 374 | 100 % | – | 479/509 | klasse_unsicher |
| 312 | 400312 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 256 | 100 % | – | 482/534 | klasse_unsicher |
| 273 | 400273 | 4.2.1 Einzelbaum | nein | ja | 1510 | 100 % | – | 500/503 | grenze_ohne_bildkante, klasse_unsicher |
| 322 | 400322 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 600 | 100 % | – | 521/549 | klasse_unsicher |
| 279 | 400279 | 4.1 Wald (geschlossener Bestand) | nein | nein | 542 | 100 % | – | 543/500 | grenze_ohne_bildkante, klasse_unsicher |
| 319 | 400319 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 271 | 100 % | – | 544/545 | klasse_unsicher |
| 290 | 400290 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 684 | 100 % | – | 555/517 | grenze_ohne_bildkante, klasse_unsicher |
| 310 | 400310 | 4.1 Wald (geschlossener Bestand) | nein | nein | 1023 | 100 % | – | 556/537 | grenze_ohne_bildkante, klasse_unsicher |
| 335 | 400335 | 4.2.1 Einzelbaum | nein | ja | 268 | 100 % | – | 378/558 | grenze_ohne_bildkante, klasse_unsicher |
| 349 | 400349 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 5 | 100 % | – | 397/561 | grenze_ohne_bildkante, klasse_unsicher |
| 333 | 400333 | 4.2.1 Einzelbaum | nein | ja | 106 | 100 % | – | 402/556 | grenze_ohne_bildkante, klasse_unsicher |
| 317 | 400317 | 4.1 Wald (geschlossener Bestand) | nein | nein | 446 | 100 % | – | 415/557 | klasse_unsicher |
| 340 | 400340 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 26 | 100 % | – | 424/562 | zu_klein |
| 343 | 400343 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 79 | 100 % | – | 429/561 | klasse_unsicher |
| 326 | 400326 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 208 | 100 % | – | 431/551 | klasse_unsicher |
| 334 | 400334 | 4.1 Wald (geschlossener Bestand) | nein | nein | 155 | 100 % | – | 443/558 | klasse_unsicher |
| 327 | 400327 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 137 | 100 % | – | 445/550 | klasse_unsicher |
| 330 | 400330 | 4.2.1 Einzelbaum | nein | ja | 277 | 100 % | – | 464/556 | klasse_unsicher |
| 341 | 400341 | 4.2.1 Einzelbaum | nein | ja | 67 | 100 % | – | 476/560 | grenze_ohne_bildkante, klasse_unsicher |
| 321 | 400321 | 4.2.1 Einzelbaum | nein | ja | 522 | 100 % | – | 499/554 | grenze_ohne_bildkante, klasse_unsicher |
| 339 | 400339 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 77 | 100 % | – | 511/560 | klasse_unsicher |
| 344 | 400344 | 4.2.1 Einzelbaum | nein | ja | 52 | 100 % | – | 538/561 | grenze_ohne_bildkante, klasse_unsicher |
| 350 | 400350 | 4.2.1 Einzelbaum | nein | ja | 12 | 100 % | – | 553/562 | grenze_ohne_bildkante, klasse_unsicher |
| 345 | 400345 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1 | 100 % | – | 563/563 | grenze_ohne_bildkante, klasse_unsicher |

`nicht_geprueft` nennt, was du nicht angesehen hast, `offen`, was du nicht entscheiden konntest.

Kontrolle vor der Rückgabe (muss mit `ok` enden):

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I C:/Users/Phil/Developement/Victor/wuensche/2026-11-17-landseg-test-t0-1/skripte/pruefe_urteil.py --urteil C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/urteil/r1c1/v4/urteil.json --segmente C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/vorstufe/r1c1/segmente.json --fassung b --viertel v4 --ids 400142,400128,400150,400134,400155,400157,400156,400139,400135,400136,400145,400131,400147,400132,400129,400152,400183,400190,400198,400171,400163,400174,400168,400194,400173,400179,400176,400197,400165,400191,400180,400153,400195,400172,400192,400181,400159,400188,400236,400226,400215,400208,400212,400205,400187,400234,400209,400196,400235,400202,400204,400211,400219,400213,400217,400221,400258,400256,400281,400238,400263,400259,400250,400276,400254,400264,400252,400067,400239,400246,400274,400251,400277,400245,400222,400255,400260,400233,400294,400295,400278,400293,400299,400282,400300,400296,400307,400301,400286,400312,400273,400322,400279,400319,400290,400310,400335,400349,400333,400317,400340,400343,400326,400334,400327,400330,400341,400321,400339,400344,400350,400345
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
Namen, die du benutzt hast, je mit Ebene, Eltern und einem Satz Bildmerkmal. Nach allen Vierteln
gleicht ein eigener Agent die Namen der 16 Viertel zu einer Liste an. Alle übrigen Regeln (L1, L2,
L4–L12) gelten wie in Fassung A; jeder Bildpunkt gehört genau einem Segment.

## Werkzeuge

Befehle im Ordner `C:/Users/Phil/Developement/Victor/landseg` mit `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -m landseg <befehl>`; Aufruf und Schalter stehen in
`C:/Users/Phil/Developement/Victor/landseg/README.md`. Die Bilder deines Viertels liegen fertig vor (Abschnitt „Dein Viertel“); `ansicht` (W3) erzeugt Bilder
je Segment und ist hier keine Urteilsgrundlage. Für fragliche Grenzen `kante` (W4, hier nur zum Ansehen
der Bildkante), zur Kontrolle `pruefen`. Eigene Skripte als Datei in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/urteil/r1c1/v4`.

## Ergebnis in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/urteil/r1c1/v4` (genau diese Namen)

- `roh.jpg`, `umriss.jpg` (alle Segmentgrenzen mit ID), `maengel.jpg` (nummerierte Punkte mit kurzer
  deutscher Beschriftung, sonst Vermerk „keine Mängel“), `vorschlag.jpg` (Grenzen und Klassen, wie
  du sie setzen würdest, sonst Vermerk „unverändert“): je dein Viertel mit Umgebung, Viertel
  umrandet (Grundlage: die vorbereiteten Übersichtsbilder).
- `nah_<n>.jpg`: eigene Nahansichten von Stellen, die man in den vorbereiteten Bildern nicht beurteilen kann,
  je ein Teil des Viertels samt Nachbarn (mindestens 64 × 64 Bildpunkte der Teilkachel, kein freigestelltes
  Einzelsegment); `kontrast_<n>.jpg` bei blassen Stellen.
- `urteil.json` (UTF-8):

```
{"teilkachel": "r1c1", "viertel": "v4", "bearbeiter": "urt-b-r1c1-v4",
 "bilder_angesehen": {"uebersicht": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r1c1/v4/uebersicht_nummern.jpg", "…"],
                      "nah": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r1c1/v4/nah1_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/urteil/r1c1/v4/nah_1.jpg", "…"]},
 "segmente": [{"id": 17, "klasse_heute": "Code", "was_ist_es": "ein Satz",
               "urteil": "sauber" | "nicht_sauber", "klasse_vorschlag": null,
               "klasse_frei": {"grob": "Name", "mittel": "Name", "fein": "Name"},
               "sicher": true | false,
               "punkte": [{"nr": 1, "art": "fremdes|fehlt|trennen|verschmelzen|grenze|klasse|zu_klein|sonstiges",
                           "text": "ein Satz mit Stelle (x/y im Teilkachelbild)", "flaeche_px": Zahl oder null}],
               "bilder": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r1c1/v4/uebersicht_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r1c1/v4/nah2_roh.jpg"]}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "was an der Kerngrenze nicht passt"}],
 "unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."],
 "klassen_frei": [{"name": "Name", "ebene": "grob|mittel|fein", "eltern": "Name oder null", "merkmal": "woran im Bild erkennbar"}]}
```

Jedes Segment deiner Liste steht genau einmal unter `segmente`, auch die sauberen, in der Reihenfolge der Liste. Segmente der Nachbarviertel (graue Nummern) und des Kontextrands (ohne Nummer) urteilst du nicht; Auffälliges an ihnen nennst du unter `unsicher` mit ID.

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Punkte, Anteil `sicher: false`, wo du unsicher bist.
