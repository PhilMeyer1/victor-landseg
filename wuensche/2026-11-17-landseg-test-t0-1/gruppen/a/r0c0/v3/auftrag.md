# Auftrag: Teilkachel r0c0, Viertel v3: 19 Segmente im Verbund ansehen und einzeln urteilen

Lies zuerst den Skill `landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `r0c0` des Ausschnitts in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500`. Du urteilst über jedes
Segment deines Viertels v3 (Liste unter „Dein Viertel“), ob Grenze und Klasse stimmen, und zeichnest ein, was
du ändern würdest. Die Label-Karte änderst du nicht.

## Daten (eingefrorener Stand, nur lesen)

- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/manifest.json`: Eintrag `r0c0` unter `teilkacheln` mit `bild` (Teilkachelbild,
  Kern + Kontextrand), `kern_im_bild` (Lage des Kerns im Teilkachelbild) und `kern` (Lage im Ausschnitt).
- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/vorstufe/r0c0/labels.tif`: Label-Karte (Segment-ID je Bildpunkt, Größe des Teilkachelbilds).
- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/vorstufe/r0c0/segmente.json`: je Segment `id`, `klasse`, `grob`, `herkunft`, `sicher`; dazu die
  Kandidatenliste der Vorstufe, falls vorhanden.
- `C:/Users/Phil/Developement/Victor/landseg/kategorien.json` und `C:/Users/Phil/Developement/Victor/landseg/KATEGORIEN.md`: die gültigen Klassen und Regeln.

## Dein Viertel

Viertel v3 (unten links) des Kerns von `r0c0`: x 64–313, y 314–563 im
Teilkachelbild (250 × 250 Bildpunkte). Dir gehören die 19 Segmente der Liste unten: Jedes hat den
größten Teil seiner Kernfläche in diesem Viertel. Die Teilkachel hat 141 Kernsegmente
(v1 22, v2 62, v3 19, v4 38); drei andere Agents urteilen gleichzeitig über die anderen Viertel, jeder in seinem eigenen
Ordner. Ein Segment über einer Viertelgrenze urteilt nur das Viertel mit dem größten Anteil; in den Bildern
der Nachbarn ist es mit grauer Nummer als Umgebung zu sehen.

Urteil im Verbund: Du siehst das Viertel als zusammenhängendes Bild mit Umgebung, arbeitest die Liste der
Reihe nach ab und beurteilst jedes Segment im Zusammenhang mit seinen Nachbarn; eingetragen wird jedes
Segment einzeln (Klasse, `sicher`, `was_ist_es` als Notiz). Bilder freigestellter Einzelsegmente gibt es
nicht, und sie sind keine Urteilsgrundlage.

Bilder des Viertels (fertig, JPEG, in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/viertel/r0c0/v3`, Fenster und Vergrößerung je Bild in `viertel.json`):

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
| 140 | 100140 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | ja | nein | 1503 | 100 % | – | 140/340 | grenze_ohne_bildkante |
| 151 | 100151 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 630 | 100 % | – | 130/375 | grenze_ohne_bildkante, klasse_unsicher |
| 145 | 100145 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | ja | nein | 1935 | 100 % | – | 279/353 | grenze_ohne_bildkante |
| 165 | 100165 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | ja | nein | 2706 | 100 % | – | 85/436 | grenze_ohne_bildkante |
| 168 | 100168 | 4.2.1 Einzelbaum | nein | nein | 74 | 100 % | – | 99/414 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 157 | 100157 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | ja | nein | 1396 | 100 % | – | 174/421 | grenze_ohne_bildkante |
| 161 | 100161 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 645 | 100 % | – | 291/409 | grenze_ohne_bildkante, klasse_unsicher |
| 182 | 100182 | 3.1 Wiese / Weide (gemeinsam) | ja | nein | 189 | 100 % | – | 89/481 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 178 | 100178 | 4.2.1 Einzelbaum | nein | nein | 712 | 100 % | – | 108/469 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 171 | 100171 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 1344 | 100 % | – | 135/461 | grenze_ohne_bildkante, klasse_unsicher |
| 180 | 100180 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | ja | nein | 1537 | 100 % | – | 264/497 | grenze_ohne_bildkante |
| 186 | 100186 | 3.1 Wiese / Weide (gemeinsam) | nein | nein | 176 | 100 % | – | 295/488 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 166 | 100166 | 3.1 Wiese / Weide (gemeinsam) | nein | nein | 7452 | 89 % | v4 | 88/539 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 188 | 100188 | 3.1 Wiese / Weide (gemeinsam) | ja | nein | 131 | 100 % | – | 103/501 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 184 | 100184 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 879 | 100 % | – | 115/513 | grenze_ohne_bildkante, klasse_unsicher |
| 181 | 100181 | 4.2.4 Gebüsch / Strauchfläche | nein | nein | 2179 | 100 % | – | 178/510 | grenze_ohne_bildkante, klasse_unsicher |
| 193 | 100193 | 3.1 Wiese / Weide (gemeinsam) | ja | nein | 451 | 100 % | – | 197/545 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 192 | 100192 | 4.2.1 Einzelbaum | nein | nein | 110 | 100 % | – | 280/515 | grenze_ohne_bildkante, klasse_unsicher |
| 195 | 100195 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 747 | 100 % | – | 143/551 | grenze_ohne_bildkante, klasse_unsicher |

`nicht_geprueft` nennt, was du nicht angesehen hast, `offen`, was du nicht entscheiden konntest.

Kontrolle vor der Rückgabe (muss mit `ok` enden):

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I C:/Users/Phil/Developement/Victor/wuensche/2026-11-17-landseg-test-t0-1/skripte/pruefe_urteil.py --urteil C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/urteil/r0c0/v3/urteil.json --segmente C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/vorstufe/r0c0/segmente.json --fassung a --viertel v3 --ids 100140,100151,100145,100165,100168,100157,100161,100182,100178,100171,100180,100186,100166,100188,100184,100181,100193,100192,100195 --kategorien C:/Users/Phil/Developement/Victor/landseg/kategorien.json
```

## Werkzeuge

Befehle im Ordner `C:/Users/Phil/Developement/Victor/landseg` mit `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -m landseg <befehl>`; Aufruf und Schalter stehen in
`C:/Users/Phil/Developement/Victor/landseg/README.md`. Die Bilder deines Viertels liegen fertig vor (Abschnitt „Dein Viertel“); `ansicht` (W3) erzeugt Bilder
je Segment und ist hier keine Urteilsgrundlage. Für fragliche Grenzen `kante` (W4, hier nur zum Ansehen
der Bildkante), zur Kontrolle `pruefen`. Eigene Skripte als Datei in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/urteil/r0c0/v3`.

## Ergebnis in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/urteil/r0c0/v3` (genau diese Namen)

- `roh.jpg`, `umriss.jpg` (alle Segmentgrenzen mit ID), `maengel.jpg` (nummerierte Punkte mit kurzer
  deutscher Beschriftung, sonst Vermerk „keine Mängel“), `vorschlag.jpg` (Grenzen und Klassen, wie
  du sie setzen würdest, sonst Vermerk „unverändert“): je dein Viertel mit Umgebung, Viertel
  umrandet (Grundlage: die vorbereiteten Übersichtsbilder).
- `nah_<n>.jpg`: eigene Nahansichten von Stellen, die man in den vorbereiteten Bildern nicht beurteilen kann,
  je ein Teil des Viertels samt Nachbarn (mindestens 64 × 64 Bildpunkte der Teilkachel, kein freigestelltes
  Einzelsegment); `kontrast_<n>.jpg` bei blassen Stellen.
- `urteil.json` (UTF-8):

```
{"teilkachel": "r0c0", "viertel": "v3", "bearbeiter": "urt-a-r0c0-v3",
 "bilder_angesehen": {"uebersicht": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/viertel/r0c0/v3/uebersicht_nummern.jpg", "…"],
                      "nah": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/viertel/r0c0/v3/nah1_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/urteil/r0c0/v3/nah_1.jpg", "…"]},
 "segmente": [{"id": 17, "klasse_heute": "Code", "was_ist_es": "ein Satz",
               "urteil": "sauber" | "nicht_sauber", "klasse_vorschlag": "Code oder null",
               "sicher": true | false,
               "punkte": [{"nr": 1, "art": "fremdes|fehlt|trennen|verschmelzen|grenze|klasse|zu_klein|sonstiges",
                           "text": "ein Satz mit Stelle (x/y im Teilkachelbild)", "flaeche_px": Zahl oder null}],
               "bilder": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/viertel/r0c0/v3/uebersicht_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/viertel/r0c0/v3/nah2_roh.jpg"]}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "was an der Kerngrenze nicht passt"}],
 "unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."]}
```

Jedes Segment deiner Liste steht genau einmal unter `segmente`, auch die sauberen, in der Reihenfolge der Liste. Segmente der Nachbarviertel (graue Nummern) und des Kontextrands (ohne Nummer) urteilst du nicht; Auffälliges an ihnen nennst du unter `unsicher` mit ID.

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Punkte, Anteil `sicher: false`, wo du unsicher bist.
