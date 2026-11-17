# Auftrag: Teilkachel r1c1, Viertel v3: 93 Segmente im Verbund ansehen und einzeln urteilen (Fassung B: Kategorien frei)

Lies zuerst den Skill `landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `r1c1` des Ausschnitts in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b`. Du urteilst über jedes
Segment deines Viertels v3 (Liste unter „Dein Viertel“), ob Grenze und Klasse stimmen, und zeichnest ein, was
du ändern würdest. Die Label-Karte änderst du nicht.

## Daten (eingefrorener Stand, nur lesen)

- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/manifest.json`: Eintrag `r1c1` unter `teilkacheln` mit `bild` (Teilkachelbild,
  Kern + Kontextrand), `kern_im_bild` (Lage des Kerns im Teilkachelbild) und `kern` (Lage im Ausschnitt).
- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/vorstufe/r1c1/labels.tif`: Label-Karte (Segment-ID je Bildpunkt, Größe des Teilkachelbilds).
- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/vorstufe/r1c1/segmente.json`: je Segment `id`, `klasse`, `grob`, `herkunft`, `sicher`; dazu die
  Kandidatenliste der Vorstufe, falls vorhanden.
- `C:/Users/Phil/Developement/Victor/landseg/kategorien.json` und `C:/Users/Phil/Developement/Victor/landseg/KATEGORIEN.md`: nur Anregung; in Fassung B benennst du die Klassen selbst (Abschnitt „Fassung B“).

## Dein Viertel

Viertel v3 (unten links) des Kerns von `r1c1`: x 64–313, y 314–563 im
Teilkachelbild (250 × 250 Bildpunkte). Dir gehören die 93 Segmente der Liste unten: Jedes hat den
größten Teil seiner Kernfläche in diesem Viertel. Die Teilkachel hat 301 Kernsegmente
(v1 44, v2 52, v3 93, v4 112); drei andere Agents urteilen gleichzeitig über die anderen Viertel, jeder in seinem eigenen
Ordner. Ein Segment über einer Viertelgrenze urteilt nur das Viertel mit dem größten Anteil; in den Bildern
der Nachbarn ist es mit grauer Nummer als Umgebung zu sehen.

Urteil im Verbund: Du siehst das Viertel als zusammenhängendes Bild mit Umgebung, arbeitest die Liste der
Reihe nach ab und beurteilst jedes Segment im Zusammenhang mit seinen Nachbarn; eingetragen wird jedes
Segment einzeln (Klasse, `sicher`, `was_ist_es` als Notiz). Bilder freigestellter Einzelsegmente gibt es
nicht, und sie sind keine Urteilsgrundlage.

Bilder des Viertels (fertig, JPEG, in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r1c1/v3`, Fenster und Vergrößerung je Bild in `viertel.json`):

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
| 34 | 400034 | 4.1 Wald (geschlossener Bestand) | ja | nein | 20366 | 56 % | v1 | 101/348 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 143 | 400143 | 4.1 Wald (geschlossener Bestand) | nein | nein | 228 | 100 % | – | 172/328 | grenze_ohne_bildkante, klasse_unsicher |
| 158 | 400158 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 116 | 100 % | – | 189/343 | – |
| 140 | 400140 | 4.1 Wald (geschlossener Bestand) | nein | nein | 390 | 100 % | – | 198/337 | klasse_unsicher |
| 154 | 400154 | 4.2.1 Einzelbaum | nein | ja | 322 | 100 % | – | 211/345 | klasse_unsicher |
| 144 | 400144 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 2067 | 100 % | – | 239/343 | grenze_ohne_bildkante, klasse_unsicher |
| 141 | 400141 | 4.2.1 Einzelbaum | nein | ja | 113 | 100 % | – | 240/325 | grenze_ohne_bildkante, klasse_unsicher |
| 137 | 400137 | 4.2.1 Einzelbaum | nein | ja | 298 | 100 % | – | 254/325 | grenze_ohne_bildkante, klasse_unsicher |
| 148 | 400148 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 132 | 100 % | – | 279/330 | klasse_unsicher |
| 133 | 400133 | 3.1 Wiese / Weide (gemeinsam) | ja | ja | 208 | 97 % | v1 | 283/323 | – |
| 151 | 400151 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 718 | 97 % | v4 | 297/346 | klasse_unsicher |
| 111 | 400111 | 3.1 Wiese / Weide (gemeinsam) | ja | ja | 1315 | 35 % | v1, v2, v4 | 305/322 | grenze_ohne_bildkante |
| 185 | 400185 | 4.1 Wald (geschlossener Bestand) | nein | nein | 232 | 100 % | – | 127/381 | klasse_unsicher |
| 162 | 400162 | 4.1 Wald (geschlossener Bestand) | ja | nein | 132 | 100 % | – | 148/355 | grenze_ohne_bildkante |
| 166 | 400166 | 4.2.1 Einzelbaum | nein | ja | 351 | 100 % | – | 162/359 | grenze_ohne_bildkante, klasse_unsicher |
| 175 | 400175 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 821 | 100 % | – | 174/374 | grenze_ohne_bildkante, klasse_unsicher |
| 164 | 400164 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 147 | 100 % | – | 176/359 | klasse_unsicher |
| 193 | 400193 | 4.2.1 Einzelbaum | nein | ja | 177 | 100 % | – | 186/387 | klasse_unsicher |
| 160 | 400160 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 585 | 100 % | – | 194/359 | grenze_ohne_bildkante, klasse_unsicher |
| 169 | 400169 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 228 | 100 % | – | 214/364 | grenze_ohne_bildkante, klasse_unsicher |
| 178 | 400178 | 4.2.1 Einzelbaum | nein | ja | 927 | 100 % | – | 222/383 | grenze_ohne_bildkante, klasse_unsicher |
| 161 | 400161 | 4.1 Wald (geschlossener Bestand) | nein | nein | 117 | 100 % | – | 223/350 | grenze_ohne_bildkante, klasse_unsicher |
| 167 | 400167 | 4.2.1 Einzelbaum | nein | ja | 223 | 100 % | – | 234/362 | grenze_ohne_bildkante, klasse_unsicher |
| 186 | 400186 | 4.2.1 Einzelbaum | nein | ja | 125 | 100 % | – | 244/377 | grenze_ohne_bildkante, klasse_unsicher |
| 146 | 400146 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 2546 | 87 % | v4 | 300/371 | grenze_ohne_bildkante, klasse_unsicher |
| 225 | 400225 | 4.1 Wald (geschlossener Bestand) | ja | nein | 95 | 100 % | – | 84/427 | – |
| 231 | 400231 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 88 | 100 % | – | 85/443 | – |
| 223 | 400223 | 1.1.2 Nebengebäude / Schuppen / Stadel | ja | nein | 543 | 100 % | – | 99/433 | grenze_ohne_bildkante |
| 206 | 400206 | 4.1 Wald (geschlossener Bestand) | ja | nein | 104 | 100 % | – | 114/407 | – |
| 227 | 400227 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 331 | 100 % | – | 120/439 | – |
| 203 | 400203 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 122 | 100 % | – | 122/402 | klasse_unsicher |
| 177 | 400177 | 1.3.2 Baustelle | nein | nein | 7723 | 100 % | – | 157/418 | grenze_ohne_bildkante, klasse_unsicher |
| 230 | 400230 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 197 | 100 % | – | 183/444 | grenze_ohne_bildkante, klasse_unsicher |
| 220 | 400220 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 271 | 100 % | – | 193/425 | grenze_ohne_bildkante, klasse_unsicher |
| 228 | 400228 | 4.1 Wald (geschlossener Bestand) | nein | nein | 156 | 100 % | – | 195/439 | grenze_ohne_bildkante, klasse_unsicher |
| 199 | 400199 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 1586 | 100 % | – | 214/414 | grenze_ohne_bildkante, klasse_unsicher |
| 200 | 400200 | 4.2.1 Einzelbaum | nein | ja | 564 | 100 % | – | 252/407 | grenze_ohne_bildkante, klasse_unsicher |
| 224 | 400224 | 4.1 Wald (geschlossener Bestand) | nein | nein | 162 | 100 % | – | 260/428 | grenze_ohne_bildkante, klasse_unsicher |
| 201 | 400201 | 4.2.1 Einzelbaum | nein | ja | 170 | 100 % | – | 267/403 | grenze_ohne_bildkante, klasse_unsicher |
| 210 | 400210 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 987 | 100 % | – | 278/418 | grenze_ohne_bildkante |
| 229 | 400229 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 93 | 100 % | – | 281/435 | klasse_unsicher |
| 189 | 400189 | 4.1 Wald (geschlossener Bestand) | nein | nein | 1973 | 65 % | v4 | 301/445 | grenze_ohne_bildkante, klasse_unsicher |
| 241 | 400241 | 4.1 Wald (geschlossener Bestand) | ja | nein | 136 | 100 % | – | 80/460 | grenze_ohne_bildkante |
| 248 | 400248 | 5.2 Stillgewässer (See, Teich, Weiher) | ja | nein | 686 | 100 % | – | 114/470 | grenze_ohne_bildkante |
| 261 | 400261 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 208 | 100 % | – | 139/477 | grenze_ohne_bildkante, klasse_unsicher |
| 249 | 400249 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 173 | 100 % | – | 147/461 | grenze_ohne_bildkante, klasse_unsicher |
| 240 | 400240 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 455 | 100 % | – | 175/469 | klasse_unsicher |
| 262 | 400262 | 4.2.4 Gebüsch / Strauchfläche | nein | ja | 100 | 100 % | – | 187/477 | klasse_unsicher |
| 237 | 400237 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 618 | 100 % | – | 196/462 | klasse_unsicher |
| 269 | 400269 | 1.3.2 Baustelle | nein | nein | 241 | 100 % | – | 206/482 | grenze_ohne_bildkante, klasse_unsicher |
| 243 | 400243 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 280 | 100 % | – | 215/471 | klasse_unsicher |
| 267 | 400267 | 4.1 Wald (geschlossener Bestand) | nein | nein | 130 | 100 % | – | 226/480 | klasse_unsicher |
| 244 | 400244 | 4.2.1 Einzelbaum | nein | ja | 326 | 100 % | – | 227/461 | grenze_ohne_bildkante, klasse_unsicher |
| 272 | 400272 | 1.1.2 Nebengebäude / Schuppen / Stadel | ja | nein | 554 | 100 % | – | 244/492 | – |
| 268 | 400268 | 1.3.2 Baustelle | nein | nein | 244 | 100 % | – | 256/483 | klasse_unsicher |
| 253 | 400253 | 4.1 Wald (geschlossener Bestand) | nein | nein | 272 | 100 % | – | 260/475 | klasse_unsicher |
| 232 | 400232 | 1.2.1 Straße (versiegelt) | nein | nein | 3108 | 54 % | v4 | 275/469 | grenze_ohne_bildkante, klasse_unsicher |
| 271 | 400271 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 250 | 100 % | – | 281/480 | klasse_unsicher |
| 275 | 400275 | 4.1 Wald (geschlossener Bestand) | nein | nein | 286 | 100 % | – | 291/493 | grenze_ohne_bildkante, klasse_unsicher |
| 305 | 400305 | 4.1 Wald (geschlossener Bestand) | nein | nein | 123 | 100 % | – | 99/529 | grenze_ohne_bildkante, klasse_unsicher |
| 298 | 400298 | 1.2.1 Straße (versiegelt) | nein | nein | 251 | 100 % | – | 105/521 | klasse_unsicher |
| 288 | 400288 | 4.1 Wald (geschlossener Bestand) | nein | nein | 292 | 100 % | – | 107/507 | klasse_unsicher |
| 316 | 400316 | 1.3.2 Baustelle | nein | nein | 253 | 100 % | – | 107/544 | grenze_ohne_bildkante, klasse_unsicher |
| 303 | 400303 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 433 | 100 % | – | 122/526 | klasse_unsicher |
| 291 | 400291 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 367 | 100 % | – | 126/512 | klasse_unsicher |
| 308 | 400308 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 708 | 100 % | – | 134/546 | klasse_unsicher |
| 313 | 400313 | 4.2.1 Einzelbaum | nein | ja | 88 | 100 % | – | 147/530 | grenze_ohne_bildkante, klasse_unsicher |
| 292 | 400292 | 1.2.1 Straße (versiegelt) | nein | nein | 797 | 100 % | – | 155/519 | grenze_ohne_bildkante, klasse_unsicher |
| 289 | 400289 | 4.2.4 Gebüsch / Strauchfläche | ja | ja | 443 | 100 % | – | 161/507 | – |
| 314 | 400314 | 4.2.1 Einzelbaum | ja | ja | 1033 | 100 % | – | 161/548 | grenze_ohne_bildkante |
| 304 | 400304 | 4.2.1 Einzelbaum | nein | ja | 114 | 100 % | – | 166/524 | klasse_unsicher |
| 309 | 400309 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 857 | 100 % | – | 189/542 | grenze_ohne_bildkante, klasse_unsicher |
| 270 | 400270 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 1152 | 100 % | – | 196/503 | klasse_unsicher |
| 318 | 400318 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | ja | nein | 323 | 100 % | – | 208/541 | grenze_ohne_bildkante |
| 216 | 400216 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 3168 | 100 % | – | 222/510 | grenze_ohne_bildkante, klasse_unsicher |
| 302 | 400302 | 4.1 Wald (geschlossener Bestand) | nein | nein | 79 | 100 % | – | 244/522 | klasse_unsicher |
| 311 | 400311 | 1.2.1 Straße (versiegelt) | nein | nein | 1051 | 100 % | – | 245/537 | grenze_ohne_bildkante, klasse_unsicher |
| 297 | 400297 | 4.2.1 Einzelbaum | nein | ja | 490 | 100 % | – | 263/522 | grenze_ohne_bildkante, klasse_unsicher |
| 315 | 400315 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 189 | 100 % | – | 269/538 | grenze_ohne_bildkante, klasse_unsicher |
| 287 | 400287 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 960 | 100 % | – | 285/527 | grenze_ohne_bildkante, klasse_unsicher |
| 323 | 400323 | 3.1 Wiese / Weide (gemeinsam) | ja | ja | 168 | 100 % | – | 293/545 | grenze_ohne_bildkante |
| 280 | 400280 | 6.6 Weg, unbefestigt (Feld-, Wald-, Schotterweg) | nein | nein | 779 | 62 % | v4 | 303/522 | klasse_unsicher |
| 324 | 400324 | 4.1 Wald (geschlossener Bestand) | nein | nein | 85 | 100 % | – | 307/539 | klasse_unsicher |
| 331 | 400331 | 4.1 Wald (geschlossener Bestand) | nein | nein | 124 | 100 % | – | 102/557 | grenze_ohne_bildkante, klasse_unsicher |
| 337 | 400337 | 1.3.2 Baustelle | nein | nein | 76 | 100 % | – | 118/561 | klasse_unsicher |
| 332 | 400332 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 62 | 100 % | – | 124/561 | klasse_unsicher |
| 346 | 400346 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 56 | 100 % | – | 143/561 | klasse_unsicher |
| 348 | 400348 | 4.2.1 Einzelbaum | ja | ja | 13 | 100 % | – | 150/562 | grenze_ohne_bildkante |
| 328 | 400328 | 4.2.1 Einzelbaum | nein | ja | 89 | 100 % | – | 201/559 | grenze_ohne_bildkante, klasse_unsicher |
| 325 | 400325 | 4.2.1 Einzelbaum | ja | ja | 509 | 100 % | – | 220/553 | grenze_ohne_bildkante |
| 329 | 400329 | 1.3.2 Baustelle | nein | nein | 597 | 100 % | – | 240/556 | grenze_ohne_bildkante, klasse_unsicher |
| 342 | 400342 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 94 | 100 % | – | 263/560 | klasse_unsicher |
| 347 | 400347 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 18 | 50 % | v4 | 311/560 | klasse_unsicher |

`nicht_geprueft` nennt, was du nicht angesehen hast, `offen`, was du nicht entscheiden konntest.

Kontrolle vor der Rückgabe (muss mit `ok` enden):

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I C:/Users/Phil/Developement/Victor/wuensche/2026-11-17-landseg-test-t0-1/skripte/pruefe_urteil.py --urteil C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/urteil/r1c1/v3/urteil.json --segmente C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/vorstufe/r1c1/segmente.json --fassung b --viertel v3 --ids 400034,400143,400158,400140,400154,400144,400141,400137,400148,400133,400151,400111,400185,400162,400166,400175,400164,400193,400160,400169,400178,400161,400167,400186,400146,400225,400231,400223,400206,400227,400203,400177,400230,400220,400228,400199,400200,400224,400201,400210,400229,400189,400241,400248,400261,400249,400240,400262,400237,400269,400243,400267,400244,400272,400268,400253,400232,400271,400275,400305,400298,400288,400316,400303,400291,400308,400313,400292,400289,400314,400304,400309,400270,400318,400216,400302,400311,400297,400315,400287,400323,400280,400324,400331,400337,400332,400346,400348,400328,400325,400329,400342,400347
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
der Bildkante), zur Kontrolle `pruefen`. Eigene Skripte als Datei in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/urteil/r1c1/v3`.

## Ergebnis in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/urteil/r1c1/v3` (genau diese Namen)

- `roh.jpg`, `umriss.jpg` (alle Segmentgrenzen mit ID), `maengel.jpg` (nummerierte Punkte mit kurzer
  deutscher Beschriftung, sonst Vermerk „keine Mängel“), `vorschlag.jpg` (Grenzen und Klassen, wie
  du sie setzen würdest, sonst Vermerk „unverändert“): je dein Viertel mit Umgebung, Viertel
  umrandet (Grundlage: die vorbereiteten Übersichtsbilder).
- `nah_<n>.jpg`: eigene Nahansichten von Stellen, die man in den vorbereiteten Bildern nicht beurteilen kann,
  je ein Teil des Viertels samt Nachbarn (mindestens 64 × 64 Bildpunkte der Teilkachel, kein freigestelltes
  Einzelsegment); `kontrast_<n>.jpg` bei blassen Stellen.
- `urteil.json` (UTF-8):

```
{"teilkachel": "r1c1", "viertel": "v3", "bearbeiter": "urt-b-r1c1-v3",
 "bilder_angesehen": {"uebersicht": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r1c1/v3/uebersicht_nummern.jpg", "…"],
                      "nah": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r1c1/v3/nah1_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/urteil/r1c1/v3/nah_1.jpg", "…"]},
 "segmente": [{"id": 17, "klasse_heute": "Code", "was_ist_es": "ein Satz",
               "urteil": "sauber" | "nicht_sauber", "klasse_vorschlag": null,
               "klasse_frei": {"grob": "Name", "mittel": "Name", "fein": "Name"},
               "sicher": true | false,
               "punkte": [{"nr": 1, "art": "fremdes|fehlt|trennen|verschmelzen|grenze|klasse|zu_klein|sonstiges",
                           "text": "ein Satz mit Stelle (x/y im Teilkachelbild)", "flaeche_px": Zahl oder null}],
               "bilder": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r1c1/v3/uebersicht_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r1c1/v3/nah2_roh.jpg"]}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "was an der Kerngrenze nicht passt"}],
 "unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."],
 "klassen_frei": [{"name": "Name", "ebene": "grob|mittel|fein", "eltern": "Name oder null", "merkmal": "woran im Bild erkennbar"}]}
```

Jedes Segment deiner Liste steht genau einmal unter `segmente`, auch die sauberen, in der Reihenfolge der Liste. Segmente der Nachbarviertel (graue Nummern) und des Kontextrands (ohne Nummer) urteilst du nicht; Auffälliges an ihnen nennst du unter `unsicher` mit ID.

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Punkte, Anteil `sicher: false`, wo du unsicher bist.
