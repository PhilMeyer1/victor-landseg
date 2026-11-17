# Auftrag: Teilkachel r0c0, Viertel v4: 38 Segmente im Verbund ansehen und einzeln urteilen

Lies zuerst den Skill `landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `r0c0` des Ausschnitts in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500`. Du urteilst über jedes
Segment deines Viertels v4 (Liste unter „Dein Viertel“), ob Grenze und Klasse stimmen, und zeichnest ein, was
du ändern würdest. Die Label-Karte änderst du nicht.

## Daten (eingefrorener Stand, nur lesen)

- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/manifest.json`: Eintrag `r0c0` unter `teilkacheln` mit `bild` (Teilkachelbild,
  Kern + Kontextrand), `kern_im_bild` (Lage des Kerns im Teilkachelbild) und `kern` (Lage im Ausschnitt).
- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/vorstufe/r0c0/labels.tif`: Label-Karte (Segment-ID je Bildpunkt, Größe des Teilkachelbilds).
- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/vorstufe/r0c0/segmente.json`: je Segment `id`, `klasse`, `grob`, `herkunft`, `sicher`; dazu die
  Kandidatenliste der Vorstufe, falls vorhanden.
- `C:/Users/Phil/Developement/Victor/landseg/kategorien.json` und `C:/Users/Phil/Developement/Victor/landseg/KATEGORIEN.md`: die gültigen Klassen und Regeln.

## Dein Viertel

Viertel v4 (unten rechts) des Kerns von `r0c0`: x 314–563, y 314–563 im
Teilkachelbild (250 × 250 Bildpunkte). Dir gehören die 38 Segmente der Liste unten: Jedes hat den
größten Teil seiner Kernfläche in diesem Viertel. Die Teilkachel hat 141 Kernsegmente
(v1 22, v2 62, v3 19, v4 38); drei andere Agents urteilen gleichzeitig über die anderen Viertel, jeder in seinem eigenen
Ordner. Ein Segment über einer Viertelgrenze urteilt nur das Viertel mit dem größten Anteil; in den Bildern
der Nachbarn ist es mit grauer Nummer als Umgebung zu sehen.

Urteil im Verbund: Du siehst das Viertel als zusammenhängendes Bild mit Umgebung, arbeitest die Liste der
Reihe nach ab und beurteilst jedes Segment im Zusammenhang mit seinen Nachbarn; eingetragen wird jedes
Segment einzeln (Klasse, `sicher`, `was_ist_es` als Notiz). Bilder freigestellter Einzelsegmente gibt es
nicht, und sie sind keine Urteilsgrundlage.

Bilder des Viertels (fertig, JPEG, in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/viertel/r0c0/v4`, Fenster und Vergrößerung je Bild in `viertel.json`):

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
Teilkachelbild; Kandidaten aus `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/vorstufe/r0c0/kandidaten.json`, dort mit Grund, in den
Bildern nicht eingezeichnet; Anteil hier = Anteil der Kernfläche in diesem Viertel):

| Nr | ID | Klasse Vorstufe | sicher | im Siedlungsgebiet | Kernfläche px | Anteil hier | auch in | Punkt x/y | Kandidaten |
|---|---|---|---|---|---|---|---|---|---|
| 146 | 100146 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 107 | 100 % | – | 348/344 | grenze_ohne_bildkante, klasse_unsicher |
| 135 | 100135 | 4.2.1 Einzelbaum | ja | ja | 4748 | 84 % | v2 | 378/338 | grenze_ohne_bildkante |
| 148 | 100148 | 2.1 Acker mit Bewuchs | nein | ja | 150 | 100 % | – | 409/341 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 137 | 100137 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 2628 | 73 % | v2 | 479/329 | grenze_ohne_bildkante, klasse_unsicher |
| 141 | 100141 | 4.1 Wald (geschlossener Bestand) | ja | nein | 91 | 100 % | – | 500/332 | grenze_ohne_bildkante |
| 136 | 100136 | 4.2.1 Einzelbaum | ja | ja | 3482 | 80 % | v2 | 541/336 | grenze_ohne_bildkante |
| 153 | 100153 | 2.1 Acker mit Bewuchs | nein | nein | 78 | 100 % | – | 361/376 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 156 | 100156 | 6.6 Weg, unbefestigt (Feld-, Wald-, Schotterweg) | ja | nein | 135 | 100 % | – | 366/386 | nicht_zusammenhaengend |
| 154 | 100154 | 2.1 Acker mit Bewuchs | nein | nein | 118 | 100 % | – | 412/379 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 160 | 100160 | 6.1 Offene Sand-, Löss-, Lehmstelle (Abbruch, Hohlweg, Grube) | ja | nein | 78 | 100 % | – | 436/389 | grenze_ohne_bildkante |
| 143 | 100143 | 3.1 Wiese / Weide (gemeinsam) | ja | ja | 5664 | 100 % | – | 438/359 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 158 | 100158 | 2.1 Acker mit Bewuchs | nein | nein | 200 | 100 % | – | 461/389 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 152 | 100152 | 4.1 Wald (geschlossener Bestand) | ja | nein | 85 | 100 % | – | 520/362 | grenze_ohne_bildkante |
| 150 | 100150 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 220 | 100 % | – | 532/368 | grenze_ohne_bildkante, klasse_unsicher |
| 149 | 100149 | 4.2.4 Gebüsch / Strauchfläche | nein | nein | 1337 | 100 % | – | 550/376 | grenze_ohne_bildkante, klasse_unsicher |
| 172 | 100172 | 3.1 Wiese / Weide (gemeinsam) | nein | nein | 996 | 68 % | v3 | 321/436 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 167 | 100167 | 2.1 Acker mit Bewuchs | nein | nein | 156 | 100 % | – | 351/416 | grenze_ohne_bildkante, klasse_unsicher |
| 173 | 100173 | 2.1 Acker mit Bewuchs | nein | nein | 86 | 100 % | – | 366/426 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 174 | 100174 | 6.6 Weg, unbefestigt (Feld-, Wald-, Schotterweg) | ja | nein | 96 | 100 % | – | 385/427 | nicht_zusammenhaengend |
| 162 | 100162 | 2.1 Acker mit Bewuchs | nein | nein | 75 | 100 % | – | 483/400 | grenze_ohne_bildkante, klasse_unsicher |
| 164 | 100164 | 2.1 Acker mit Bewuchs | nein | nein | 80 | 100 % | – | 513/402 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 159 | 100159 | 2.1 Acker mit Bewuchs | ja | nein | 11411 | 100 % | – | 522/440 | grenze_ohne_bildkante |
| 163 | 100163 | 2.1 Acker mit Bewuchs | nein | nein | 155 | 100 % | – | 524/402 | grenze_ohne_bildkante, klasse_unsicher |
| 155 | 100155 | 4.1 Wald (geschlossener Bestand) | ja | nein | 238 | 100 % | – | 536/400 | grenze_ohne_bildkante |
| 170 | 100170 | 4.1 Wald (geschlossener Bestand) | nein | nein | 88 | 100 % | – | 553/422 | grenze_ohne_bildkante, klasse_unsicher |
| 176 | 100176 | 3.1 Wiese / Weide (gemeinsam) | ja | nein | 312 | 99 % | v3 | 320/454 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 177 | 100177 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | ja | nein | 5884 | 100 % | – | 352/487 | grenze_ohne_bildkante |
| 179 | 100179 | 3.1 Wiese / Weide (gemeinsam) | ja | nein | 195 | 100 % | – | 395/479 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 187 | 100187 | 4.2.1 Einzelbaum | nein | nein | 73 | 100 % | – | 398/491 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 183 | 100183 | 3.1 Wiese / Weide (gemeinsam) | nein | nein | 340 | 100 % | – | 407/487 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 191 | 100191 | 4.2.1 Einzelbaum | nein | nein | 2872 | 100 % | – | 410/548 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 189 | 100189 | 3.1 Wiese / Weide (gemeinsam) | ja | nein | 389 | 100 % | – | 422/514 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 185 | 100185 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | ja | nein | 3249 | 100 % | – | 474/526 | grenze_ohne_bildkante |
| 190 | 100190 | 3.1 Wiese / Weide (gemeinsam) | nein | nein | 124 | 100 % | – | 497/507 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 196 | 100196 | 3.1 Wiese / Weide (gemeinsam) | nein | nein | 126 | 100 % | – | 532/543 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 175 | 100175 | 3.1 Wiese / Weide (gemeinsam) | nein | nein | 9688 | 100 % | – | 539/511 | grenze_ohne_bildkante, klasse_unsicher |
| 194 | 100194 | 4.2.1 Einzelbaum | nein | nein | 552 | 100 % | – | 525/555 | grenze_ohne_bildkante, klasse_unsicher |
| 197 | 100197 | 3.1 Wiese / Weide (gemeinsam) | ja | nein | 112 | 100 % | – | 544/557 | grenze_ohne_bildkante, nicht_zusammenhaengend |

`nicht_geprueft` nennt, was du nicht angesehen hast, `offen`, was du nicht entscheiden konntest.

Kontrolle vor der Rückgabe (muss mit `ok` enden):

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I C:/Users/Phil/Developement/Victor/wuensche/2026-11-17-landseg-test-t0-1/skripte/pruefe_urteil.py --urteil C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/urteil/r0c0/v4/urteil.json --segmente C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/vorstufe/r0c0/segmente.json --fassung a --viertel v4 --ids 100146,100135,100148,100137,100141,100136,100153,100156,100154,100160,100143,100158,100152,100150,100149,100172,100167,100173,100174,100162,100164,100159,100163,100155,100170,100176,100177,100179,100187,100183,100191,100189,100185,100190,100196,100175,100194,100197 --kategorien C:/Users/Phil/Developement/Victor/landseg/kategorien.json
```

## Werkzeuge

Befehle im Ordner `C:/Users/Phil/Developement/Victor/landseg` mit `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -m landseg <befehl>`; Aufruf und Schalter stehen in
`C:/Users/Phil/Developement/Victor/landseg/README.md`. Die Bilder deines Viertels liegen fertig vor (Abschnitt „Dein Viertel“); `ansicht` (W3) erzeugt Bilder
je Segment und ist hier keine Urteilsgrundlage. Für fragliche Grenzen `kante` (W4, hier nur zum Ansehen
der Bildkante), zur Kontrolle `pruefen`. Eigene Skripte als Datei in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/urteil/r0c0/v4`.

## Ergebnis in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/urteil/r0c0/v4` (genau diese Namen)

- `roh.jpg`, `umriss.jpg` (alle Segmentgrenzen mit ID), `maengel.jpg` (nummerierte Punkte mit kurzer
  deutscher Beschriftung, sonst Vermerk „keine Mängel“), `vorschlag.jpg` (Grenzen und Klassen, wie
  du sie setzen würdest, sonst Vermerk „unverändert“): je dein Viertel mit Umgebung, Viertel
  umrandet (Grundlage: die vorbereiteten Übersichtsbilder).
- `nah_<n>.jpg`: eigene Nahansichten von Stellen, die man in den vorbereiteten Bildern nicht beurteilen kann,
  je ein Teil des Viertels samt Nachbarn (mindestens 64 × 64 Bildpunkte der Teilkachel, kein freigestelltes
  Einzelsegment); `kontrast_<n>.jpg` bei blassen Stellen.
- `urteil.json` (UTF-8):

```
{"teilkachel": "r0c0", "viertel": "v4", "bearbeiter": "urt-a-r0c0-v4",
 "bilder_angesehen": {"uebersicht": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/viertel/r0c0/v4/uebersicht_nummern.jpg", "…"],
                      "nah": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/viertel/r0c0/v4/nah1_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/urteil/r0c0/v4/nah_1.jpg", "…"]},
 "segmente": [{"id": 17, "klasse_heute": "Code", "was_ist_es": "ein Satz",
               "urteil": "sauber" | "nicht_sauber", "klasse_vorschlag": "Code oder null",
               "sicher": true | false,
               "punkte": [{"nr": 1, "art": "fremdes|fehlt|trennen|verschmelzen|grenze|klasse|zu_klein|sonstiges",
                           "text": "ein Satz mit Stelle (x/y im Teilkachelbild)", "flaeche_px": Zahl oder null}],
               "bilder": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/viertel/r0c0/v4/uebersicht_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/viertel/r0c0/v4/nah2_roh.jpg"]}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "was an der Kerngrenze nicht passt"}],
 "unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."]}
```

Jedes Segment deiner Liste steht genau einmal unter `segmente`, auch die sauberen, in der Reihenfolge der Liste. Segmente der Nachbarviertel (graue Nummern) und des Kontextrands (ohne Nummer) urteilst du nicht; Auffälliges an ihnen nennst du unter `unsicher` mit ID.

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Punkte, Anteil `sicher: false`, wo du unsicher bist.
