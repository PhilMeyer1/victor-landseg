# Auftrag: Teilkachel r0c1, Viertel v2: 43 Segmente im Verbund ansehen und einzeln urteilen

Lies zuerst den Skill `landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `r0c1` des Ausschnitts in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500`. Du urteilst über jedes
Segment deines Viertels v2 (Liste unter „Dein Viertel“), ob Grenze und Klasse stimmen, und zeichnest ein, was
du ändern würdest. Die Label-Karte änderst du nicht.

## Daten (eingefrorener Stand, nur lesen)

- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/manifest.json`: Eintrag `r0c1` unter `teilkacheln` mit `bild` (Teilkachelbild,
  Kern + Kontextrand), `kern_im_bild` (Lage des Kerns im Teilkachelbild) und `kern` (Lage im Ausschnitt).
- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/vorstufe/r0c1/labels.tif`: Label-Karte (Segment-ID je Bildpunkt, Größe des Teilkachelbilds).
- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/vorstufe/r0c1/segmente.json`: je Segment `id`, `klasse`, `grob`, `herkunft`, `sicher`; dazu die
  Kandidatenliste der Vorstufe, falls vorhanden.
- `C:/Users/Phil/Developement/Victor/landseg/kategorien.json` und `C:/Users/Phil/Developement/Victor/landseg/KATEGORIEN.md`: die gültigen Klassen und Regeln.

## Dein Viertel

Viertel v2 (oben rechts) des Kerns von `r0c1`: x 314–563, y 64–313 im
Teilkachelbild (250 × 250 Bildpunkte). Dir gehören die 43 Segmente der Liste unten: Jedes hat den
größten Teil seiner Kernfläche in diesem Viertel. Die Teilkachel hat 147 Kernsegmente
(v1 46, v2 43, v3 37, v4 21); drei andere Agents urteilen gleichzeitig über die anderen Viertel, jeder in seinem eigenen
Ordner. Ein Segment über einer Viertelgrenze urteilt nur das Viertel mit dem größten Anteil; in den Bildern
der Nachbarn ist es mit grauer Nummer als Umgebung zu sehen.

Urteil im Verbund: Du siehst das Viertel als zusammenhängendes Bild mit Umgebung, arbeitest die Liste der
Reihe nach ab und beurteilst jedes Segment im Zusammenhang mit seinen Nachbarn; eingetragen wird jedes
Segment einzeln (Klasse, `sicher`, `was_ist_es` als Notiz). Bilder freigestellter Einzelsegmente gibt es
nicht, und sie sind keine Urteilsgrundlage.

Bilder des Viertels (fertig, JPEG, in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/viertel/r0c1/v2`, Fenster und Vergrößerung je Bild in `viertel.json`):

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
Teilkachelbild; Kandidaten aus `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/vorstufe/r0c1/kandidaten.json`, dort mit Grund, in den
Bildern nicht eingezeichnet; Anteil hier = Anteil der Kernfläche in diesem Viertel):

| Nr | ID | Klasse Vorstufe | sicher | im Siedlungsgebiet | Kernfläche px | Anteil hier | auch in | Punkt x/y | Kandidaten |
|---|---|---|---|---|---|---|---|---|---|
| 27 | 200027 | 4.2.1 Einzelbaum | nein | ja | 1049 | 100 % | – | 346/76 | grenze_ohne_bildkante, klasse_unsicher |
| 51 | 200051 | 4.1 Wald (geschlossener Bestand) | nein | nein | 365 | 100 % | – | 372/70 | klasse_unsicher |
| 13 | 200013 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 44 | 100 % | – | 387/66 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 61 | 200061 | 1.2.1 Straße (versiegelt) | nein | nein | 90 | 100 % | – | 395/67 | klasse_unsicher |
| 19 | 200019 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | ja | nein | 6037 | 62 % | v1 | 433/80 | – |
| 68 | 200068 | 1.2.1 Straße (versiegelt) | nein | nein | 96 | 100 % | – | 451/86 | klasse_unsicher |
| 63 | 200063 | 1.2.1 Straße (versiegelt) | ja | nein | 142 | 100 % | – | 464/82 | nicht_zusammenhaengend |
| 71 | 200071 | 4.1 Wald (geschlossener Bestand) | nein | nein | 210 | 100 % | – | 469/96 | klasse_unsicher |
| 62 | 200062 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | ja | nein | 352 | 100 % | – | 489/73 | nicht_zusammenhaengend |
| 55 | 200055 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 153 | 100 % | – | 499/68 | grenze_ohne_bildkante, klasse_unsicher |
| 47 | 200047 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | ja | nein | 83 | 100 % | – | 512/67 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 86 | 200086 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | ja | nein | 402 | 100 % | – | 354/135 | – |
| 76 | 200076 | 4.2.1 Einzelbaum | ja | ja | 660 | 100 % | – | 361/117 | – |
| 73 | 200073 | 1.2.1 Straße (versiegelt) | ja | nein | 138 | 100 % | – | 377/102 | nicht_zusammenhaengend |
| 77 | 200077 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | ja | nein | 135 | 100 % | – | 379/111 | – |
| 70 | 200070 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 759 | 100 % | – | 396/105 | klasse_unsicher |
| 78 | 200078 | 4.1 Wald (geschlossener Bestand) | nein | nein | 549 | 100 % | – | 453/140 | grenze_ohne_bildkante, klasse_unsicher |
| 88 | 200088 | 4.2.4 Gebüsch / Strauchfläche | nein | ja | 85 | 100 % | – | 462/141 | grenze_ohne_bildkante, klasse_unsicher |
| 72 | 200072 | 4.2.1 Einzelbaum | nein | ja | 1843 | 100 % | – | 467/121 | grenze_ohne_bildkante, klasse_unsicher |
| 90 | 200090 | 4.1 Wald (geschlossener Bestand) | nein | nein | 186 | 100 % | – | 484/147 | klasse_unsicher, nicht_zusammenhaengend |
| 91 | 200091 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 196 | 100 % | – | 512/149 | – |
| 54 | 200054 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 5679 | 100 % | – | 523/104 | – |
| 87 | 200087 | 4.1 Wald (geschlossener Bestand) | ja | nein | 152 | 100 % | – | 545/139 | – |
| 115 | 200115 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 116 | 100 % | – | 348/185 | – |
| 74 | 200074 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 7666 | 100 % | – | 403/152 | – |
| 96 | 200096 | 4.2.1 Einzelbaum | nein | ja | 1072 | 100 % | – | 491/163 | grenze_ohne_bildkante, klasse_unsicher |
| 118 | 200118 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | ja | nein | 702 | 100 % | – | 510/196 | – |
| 119 | 200119 | 3.1 Wiese / Weide (gemeinsam) | ja | ja | 121 | 100 % | – | 530/187 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 83 | 200083 | 2.1 Acker mit Bewuchs | nein | ja | 2283 | 100 % | – | 543/166 | grenze_ohne_bildkante, klasse_unsicher |
| 113 | 200113 | 3.1 Wiese / Weide (gemeinsam) | ja | ja | 22 | 100 % | – | 561/182 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 109 | 200109 | 4.1 Wald (geschlossener Bestand) | nein | nein | 16 | 100 % | – | 562/175 | klasse_unsicher |
| 125 | 200125 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 1476 | 100 % | – | 353/223 | grenze_ohne_bildkante, klasse_unsicher |
| 131 | 200131 | 4.1 Wald (geschlossener Bestand) | nein | nein | 188 | 100 % | – | 379/233 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 127 | 200127 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 105 | 100 % | – | 380/207 | – |
| 129 | 200129 | 4.1 Wald (geschlossener Bestand) | ja | nein | 138 | 100 % | – | 380/222 | grenze_ohne_bildkante |
| 104 | 200104 | 3.1 Wiese / Weide (gemeinsam) | ja | ja | 3927 | 100 % | – | 404/221 | grenze_ohne_bildkante |
| 136 | 200136 | 4.1 Wald (geschlossener Bestand) | ja | nein | 89 | 100 % | – | 418/246 | – |
| 123 | 200123 | 4.2.1 Einzelbaum | ja | ja | 621 | 100 % | – | 518/224 | – |
| 134 | 200134 | 4.2.1 Einzelbaum | nein | ja | 5092 | 90 % | v4 | 375/282 | grenze_ohne_bildkante, klasse_unsicher |
| 103 | 200103 | 4.1 Wald (geschlossener Bestand) | nein | nein | 17188 | 81 % | v4 | 475/253 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 142 | 200142 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 604 | 97 % | v4 | 553/298 | grenze_ohne_bildkante, klasse_unsicher |
| 146 | 200146 | 4.1 Wald (geschlossener Bestand) | nein | nein | 102 | 100 % | – | 344/309 | klasse_unsicher, nicht_zusammenhaengend |
| 147 | 200147 | 3.1 Wiese / Weide (gemeinsam) | ja | nein | 509 | 70 % | v4 | 512/306 | grenze_ohne_bildkante, nicht_zusammenhaengend |

`nicht_geprueft` nennt, was du nicht angesehen hast, `offen`, was du nicht entscheiden konntest.

Kontrolle vor der Rückgabe (muss mit `ok` enden):

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I C:/Users/Phil/Developement/Victor/wuensche/2026-11-17-landseg-test-t0-1/skripte/pruefe_urteil.py --urteil C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/urteil/r0c1/v2/urteil.json --segmente C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/vorstufe/r0c1/segmente.json --fassung a --viertel v2 --ids 200027,200051,200013,200061,200019,200068,200063,200071,200062,200055,200047,200086,200076,200073,200077,200070,200078,200088,200072,200090,200091,200054,200087,200115,200074,200096,200118,200119,200083,200113,200109,200125,200131,200127,200129,200104,200136,200123,200134,200103,200142,200146,200147 --kategorien C:/Users/Phil/Developement/Victor/landseg/kategorien.json
```

## Werkzeuge

Befehle im Ordner `C:/Users/Phil/Developement/Victor/landseg` mit `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -m landseg <befehl>`; Aufruf und Schalter stehen in
`C:/Users/Phil/Developement/Victor/landseg/README.md`. Die Bilder deines Viertels liegen fertig vor (Abschnitt „Dein Viertel“); `ansicht` (W3) erzeugt Bilder
je Segment und ist hier keine Urteilsgrundlage. Für fragliche Grenzen `kante` (W4, hier nur zum Ansehen
der Bildkante), zur Kontrolle `pruefen`. Eigene Skripte als Datei in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/urteil/r0c1/v2`.

## Ergebnis in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/urteil/r0c1/v2` (genau diese Namen)

- `roh.jpg`, `umriss.jpg` (alle Segmentgrenzen mit ID), `maengel.jpg` (nummerierte Punkte mit kurzer
  deutscher Beschriftung, sonst Vermerk „keine Mängel“), `vorschlag.jpg` (Grenzen und Klassen, wie
  du sie setzen würdest, sonst Vermerk „unverändert“): je dein Viertel mit Umgebung, Viertel
  umrandet (Grundlage: die vorbereiteten Übersichtsbilder).
- `nah_<n>.jpg`: eigene Nahansichten von Stellen, die man in den vorbereiteten Bildern nicht beurteilen kann,
  je ein Teil des Viertels samt Nachbarn (mindestens 64 × 64 Bildpunkte der Teilkachel, kein freigestelltes
  Einzelsegment); `kontrast_<n>.jpg` bei blassen Stellen.
- `urteil.json` (UTF-8):

```
{"teilkachel": "r0c1", "viertel": "v2", "bearbeiter": "urt-a-r0c1-v2",
 "bilder_angesehen": {"uebersicht": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/viertel/r0c1/v2/uebersicht_nummern.jpg", "…"],
                      "nah": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/viertel/r0c1/v2/nah1_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/urteil/r0c1/v2/nah_1.jpg", "…"]},
 "segmente": [{"id": 17, "klasse_heute": "Code", "was_ist_es": "ein Satz",
               "urteil": "sauber" | "nicht_sauber", "klasse_vorschlag": "Code oder null",
               "sicher": true | false,
               "punkte": [{"nr": 1, "art": "fremdes|fehlt|trennen|verschmelzen|grenze|klasse|zu_klein|sonstiges",
                           "text": "ein Satz mit Stelle (x/y im Teilkachelbild)", "flaeche_px": Zahl oder null}],
               "bilder": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/viertel/r0c1/v2/uebersicht_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/viertel/r0c1/v2/nah2_roh.jpg"]}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "was an der Kerngrenze nicht passt"}],
 "unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."]}
```

Jedes Segment deiner Liste steht genau einmal unter `segmente`, auch die sauberen, in der Reihenfolge der Liste. Segmente der Nachbarviertel (graue Nummern) und des Kontextrands (ohne Nummer) urteilst du nicht; Auffälliges an ihnen nennst du unter `unsicher` mit ID.

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Punkte, Anteil `sicher: false`, wo du unsicher bist.
