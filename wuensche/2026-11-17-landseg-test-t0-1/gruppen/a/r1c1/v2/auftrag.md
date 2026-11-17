# Auftrag: Teilkachel r1c1, Viertel v2: 52 Segmente im Verbund ansehen und einzeln urteilen

Lies zuerst den Skill `landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `r1c1` des Ausschnitts in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500`. Du urteilst über jedes
Segment deines Viertels v2 (Liste unter „Dein Viertel“), ob Grenze und Klasse stimmen, und zeichnest ein, was
du ändern würdest. Die Label-Karte änderst du nicht.

## Daten (eingefrorener Stand, nur lesen)

- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/manifest.json`: Eintrag `r1c1` unter `teilkacheln` mit `bild` (Teilkachelbild,
  Kern + Kontextrand), `kern_im_bild` (Lage des Kerns im Teilkachelbild) und `kern` (Lage im Ausschnitt).
- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/vorstufe/r1c1/labels.tif`: Label-Karte (Segment-ID je Bildpunkt, Größe des Teilkachelbilds).
- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/vorstufe/r1c1/segmente.json`: je Segment `id`, `klasse`, `grob`, `herkunft`, `sicher`; dazu die
  Kandidatenliste der Vorstufe, falls vorhanden.
- `C:/Users/Phil/Developement/Victor/landseg/kategorien.json` und `C:/Users/Phil/Developement/Victor/landseg/KATEGORIEN.md`: die gültigen Klassen und Regeln.

## Dein Viertel

Viertel v2 (oben rechts) des Kerns von `r1c1`: x 314–563, y 64–313 im
Teilkachelbild (250 × 250 Bildpunkte). Dir gehören die 52 Segmente der Liste unten: Jedes hat den
größten Teil seiner Kernfläche in diesem Viertel. Die Teilkachel hat 301 Kernsegmente
(v1 44, v2 52, v3 93, v4 112); drei andere Agents urteilen gleichzeitig über die anderen Viertel, jeder in seinem eigenen
Ordner. Ein Segment über einer Viertelgrenze urteilt nur das Viertel mit dem größten Anteil; in den Bildern
der Nachbarn ist es mit grauer Nummer als Umgebung zu sehen.

Urteil im Verbund: Du siehst das Viertel als zusammenhängendes Bild mit Umgebung, arbeitest die Liste der
Reihe nach ab und beurteilst jedes Segment im Zusammenhang mit seinen Nachbarn; eingetragen wird jedes
Segment einzeln (Klasse, `sicher`, `was_ist_es` als Notiz). Bilder freigestellter Einzelsegmente gibt es
nicht, und sie sind keine Urteilsgrundlage.

Bilder des Viertels (fertig, JPEG, in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/viertel/r1c1/v2`, Fenster und Vergrößerung je Bild in `viertel.json`):

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
Teilkachelbild; Kandidaten aus `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/vorstufe/r1c1/kandidaten.json`, dort mit Grund, in den
Bildern nicht eingezeichnet; Anteil hier = Anteil der Kernfläche in diesem Viertel):

| Nr | ID | Klasse Vorstufe | sicher | im Siedlungsgebiet | Kernfläche px | Anteil hier | auch in | Punkt x/y | Kandidaten |
|---|---|---|---|---|---|---|---|---|---|
| 20 | 400020 | 3.1 Wiese / Weide (gemeinsam) | ja | nein | 72 | 100 % | – | 422/82 | – |
| 22 | 400022 | 6.6 Weg, unbefestigt (Feld-, Wald-, Schotterweg) | ja | nein | 108 | 100 % | – | 472/94 | nicht_zusammenhaengend |
| 6 | 400006 | 3.1 Wiese / Weide (gemeinsam) | ja | nein | 4831 | 100 % | – | 514/81 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 19 | 400019 | 4.2.1 Einzelbaum | nein | nein | 3377 | 86 % | v1 | 335/115 | grenze_ohne_bildkante, klasse_unsicher |
| 21 | 400021 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 904 | 100 % | – | 386/113 | grenze_ohne_bildkante, klasse_unsicher |
| 29 | 400029 | 6.6 Weg, unbefestigt (Feld-, Wald-, Schotterweg) | ja | nein | 703 | 100 % | – | 448/143 | nicht_zusammenhaengend |
| 24 | 400024 | 3.1 Wiese / Weide (gemeinsam) | nein | nein | 73 | 100 % | – | 507/101 | klasse_unsicher |
| 28 | 400028 | 6.6 Weg, unbefestigt (Feld-, Wald-, Schotterweg) | ja | nein | 104 | 100 % | – | 513/127 | nicht_zusammenhaengend |
| 2 | 400002 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 45060 | 56 % | v1 | 477/181 | grenze_ohne_bildkante, klasse_unsicher |
| 38 | 400038 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 1876 | 100 % | – | 544/198 | grenze_ohne_bildkante, klasse_unsicher |
| 62 | 400062 | 4.2.1 Einzelbaum | nein | ja | 102 | 100 % | – | 320/222 | grenze_ohne_bildkante, klasse_unsicher |
| 53 | 400053 | 4.1 Wald (geschlossener Bestand) | nein | nein | 682 | 100 % | – | 335/222 | klasse_unsicher |
| 68 | 400068 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 489 | 100 % | – | 338/236 | klasse_unsicher |
| 74 | 400074 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 276 | 100 % | – | 353/240 | klasse_unsicher |
| 43 | 400043 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 1088 | 100 % | v1 | 361/205 | grenze_ohne_bildkante, klasse_unsicher |
| 79 | 400079 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 580 | 100 % | – | 383/248 | grenze_ohne_bildkante, klasse_unsicher |
| 56 | 400056 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 465 | 100 % | – | 385/215 | grenze_ohne_bildkante, klasse_unsicher |
| 51 | 400051 | 4.1 Wald (geschlossener Bestand) | ja | nein | 151 | 100 % | – | 400/206 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 57 | 400057 | 4.2.1 Einzelbaum | nein | ja | 389 | 100 % | – | 416/222 | klasse_unsicher |
| 76 | 400076 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 175 | 100 % | – | 431/244 | klasse_unsicher |
| 58 | 400058 | 4.1 Wald (geschlossener Bestand) | nein | nein | 2369 | 100 % | – | 434/228 | grenze_ohne_bildkante, klasse_unsicher |
| 82 | 400082 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 184 | 100 % | – | 451/242 | klasse_unsicher |
| 84 | 400084 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 150 | 100 % | – | 473/246 | klasse_unsicher |
| 71 | 400071 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 689 | 100 % | – | 498/237 | klasse_unsicher |
| 65 | 400065 | 4.1 Wald (geschlossener Bestand) | ja | nein | 153 | 100 % | – | 505/222 | grenze_ohne_bildkante |
| 85 | 400085 | 4.1 Wald (geschlossener Bestand) | nein | nein | 126 | 100 % | – | 514/245 | grenze_ohne_bildkante, klasse_unsicher |
| 64 | 400064 | 4.1 Wald (geschlossener Bestand) | nein | nein | 732 | 100 % | – | 532/230 | grenze_ohne_bildkante, klasse_unsicher |
| 73 | 400073 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 163 | 100 % | – | 546/240 | – |
| 42 | 400042 | 4.2.1 Einzelbaum | nein | ja | 151 | 100 % | – | 558/221 | grenze_ohne_bildkante, klasse_unsicher |
| 48 | 400048 | 4.1 Wald (geschlossener Bestand) | ja | nein | 38 | 100 % | – | 562/227 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 93 | 400093 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 962 | 94 % | v1 | 329/273 | klasse_unsicher |
| 92 | 400092 | 4.1 Wald (geschlossener Bestand) | nein | nein | 93 | 100 % | – | 333/253 | klasse_unsicher |
| 107 | 400107 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 736 | 96 % | v4 | 341/295 | grenze_ohne_bildkante, klasse_unsicher |
| 96 | 400096 | 4.1 Wald (geschlossener Bestand) | nein | nein | 575 | 100 % | – | 355/270 | klasse_unsicher |
| 114 | 400114 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 246 | 100 % | – | 356/293 | grenze_ohne_bildkante, klasse_unsicher |
| 118 | 400118 | 4.1 Wald (geschlossener Bestand) | nein | nein | 136 | 100 % | – | 372/292 | klasse_unsicher |
| 115 | 400115 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 166 | 100 % | – | 379/298 | klasse_unsicher |
| 99 | 400099 | 4.2.1 Einzelbaum | nein | ja | 345 | 100 % | – | 417/267 | grenze_ohne_bildkante, klasse_unsicher |
| 122 | 400122 | 4.1 Wald (geschlossener Bestand) | nein | nein | 124 | 100 % | – | 433/299 | grenze_ohne_bildkante, klasse_unsicher |
| 95 | 400095 | 4.2.1 Einzelbaum | nein | ja | 1097 | 100 % | – | 457/288 | grenze_ohne_bildkante, klasse_unsicher |
| 105 | 400105 | 4.2.1 Einzelbaum | nein | ja | 635 | 99 % | v4 | 476/294 | grenze_ohne_bildkante, klasse_unsicher |
| 91 | 400091 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 1516 | 100 % | – | 496/274 | grenze_ohne_bildkante, klasse_unsicher |
| 106 | 400106 | 4.1 Wald (geschlossener Bestand) | nein | nein | 219 | 100 % | – | 513/283 | klasse_unsicher |
| 110 | 400110 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 821 | 100 % | – | 527/297 | klasse_unsicher |
| 100 | 400100 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | ja | nein | 532 | 100 % | – | 531/274 | – |
| 86 | 400086 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 439 | 100 % | – | 537/254 | klasse_unsicher |
| 75 | 400075 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 815 | 99 % | v4 | 555/270 | grenze_ohne_bildkante, klasse_unsicher |
| 112 | 400112 | 4.1 Wald (geschlossener Bestand) | nein | nein | 158 | 100 % | – | 557/285 | klasse_unsicher |
| 117 | 400117 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 682 | 77 % | v4 | 391/303 | grenze_ohne_bildkante, klasse_unsicher |
| 130 | 400130 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 128 | 59 % | v4 | 404/309 | grenze_ohne_bildkante, klasse_unsicher |
| 126 | 400126 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 495 | 60 % | v4 | 476/308 | klasse_unsicher |
| 124 | 400124 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 102 | 100 % | – | 550/303 | klasse_unsicher |

`nicht_geprueft` nennt, was du nicht angesehen hast, `offen`, was du nicht entscheiden konntest.

Kontrolle vor der Rückgabe (muss mit `ok` enden):

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I C:/Users/Phil/Developement/Victor/wuensche/2026-11-17-landseg-test-t0-1/skripte/pruefe_urteil.py --urteil C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/urteil/r1c1/v2/urteil.json --segmente C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/vorstufe/r1c1/segmente.json --fassung a --viertel v2 --ids 400020,400022,400006,400019,400021,400029,400024,400028,400002,400038,400062,400053,400068,400074,400043,400079,400056,400051,400057,400076,400058,400082,400084,400071,400065,400085,400064,400073,400042,400048,400093,400092,400107,400096,400114,400118,400115,400099,400122,400095,400105,400091,400106,400110,400100,400086,400075,400112,400117,400130,400126,400124 --kategorien C:/Users/Phil/Developement/Victor/landseg/kategorien.json
```

## Werkzeuge

Befehle im Ordner `C:/Users/Phil/Developement/Victor/landseg` mit `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -m landseg <befehl>`; Aufruf und Schalter stehen in
`C:/Users/Phil/Developement/Victor/landseg/README.md`. Die Bilder deines Viertels liegen fertig vor (Abschnitt „Dein Viertel“); `ansicht` (W3) erzeugt Bilder
je Segment und ist hier keine Urteilsgrundlage. Für fragliche Grenzen `kante` (W4, hier nur zum Ansehen
der Bildkante), zur Kontrolle `pruefen`. Eigene Skripte als Datei in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/urteil/r1c1/v2`.

## Ergebnis in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/urteil/r1c1/v2` (genau diese Namen)

- `roh.jpg`, `umriss.jpg` (alle Segmentgrenzen mit ID), `maengel.jpg` (nummerierte Punkte mit kurzer
  deutscher Beschriftung, sonst Vermerk „keine Mängel“), `vorschlag.jpg` (Grenzen und Klassen, wie
  du sie setzen würdest, sonst Vermerk „unverändert“): je dein Viertel mit Umgebung, Viertel
  umrandet (Grundlage: die vorbereiteten Übersichtsbilder).
- `nah_<n>.jpg`: eigene Nahansichten von Stellen, die man in den vorbereiteten Bildern nicht beurteilen kann,
  je ein Teil des Viertels samt Nachbarn (mindestens 64 × 64 Bildpunkte der Teilkachel, kein freigestelltes
  Einzelsegment); `kontrast_<n>.jpg` bei blassen Stellen.
- `urteil.json` (UTF-8):

```
{"teilkachel": "r1c1", "viertel": "v2", "bearbeiter": "urt-a-r1c1-v2",
 "bilder_angesehen": {"uebersicht": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/viertel/r1c1/v2/uebersicht_nummern.jpg", "…"],
                      "nah": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/viertel/r1c1/v2/nah1_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/urteil/r1c1/v2/nah_1.jpg", "…"]},
 "segmente": [{"id": 17, "klasse_heute": "Code", "was_ist_es": "ein Satz",
               "urteil": "sauber" | "nicht_sauber", "klasse_vorschlag": "Code oder null",
               "sicher": true | false,
               "punkte": [{"nr": 1, "art": "fremdes|fehlt|trennen|verschmelzen|grenze|klasse|zu_klein|sonstiges",
                           "text": "ein Satz mit Stelle (x/y im Teilkachelbild)", "flaeche_px": Zahl oder null}],
               "bilder": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/viertel/r1c1/v2/uebersicht_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/viertel/r1c1/v2/nah2_roh.jpg"]}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "was an der Kerngrenze nicht passt"}],
 "unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."]}
```

Jedes Segment deiner Liste steht genau einmal unter `segmente`, auch die sauberen, in der Reihenfolge der Liste. Segmente der Nachbarviertel (graue Nummern) und des Kontextrands (ohne Nummer) urteilst du nicht; Auffälliges an ihnen nennst du unter `unsicher` mit ID.

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Punkte, Anteil `sicher: false`, wo du unsicher bist.
