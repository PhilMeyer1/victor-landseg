# Auftrag: Teilkachel r0c0, Viertel v2: 62 Segmente im Verbund ansehen und einzeln urteilen

Lies zuerst den Skill `landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `r0c0` des Ausschnitts in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500`. Du urteilst über jedes
Segment deines Viertels v2 (Liste unter „Dein Viertel“), ob Grenze und Klasse stimmen, und zeichnest ein, was
du ändern würdest. Die Label-Karte änderst du nicht.

## Daten (eingefrorener Stand, nur lesen)

- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/manifest.json`: Eintrag `r0c0` unter `teilkacheln` mit `bild` (Teilkachelbild,
  Kern + Kontextrand), `kern_im_bild` (Lage des Kerns im Teilkachelbild) und `kern` (Lage im Ausschnitt).
- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/vorstufe/r0c0/labels.tif`: Label-Karte (Segment-ID je Bildpunkt, Größe des Teilkachelbilds).
- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/vorstufe/r0c0/segmente.json`: je Segment `id`, `klasse`, `grob`, `herkunft`, `sicher`; dazu die
  Kandidatenliste der Vorstufe, falls vorhanden.
- `C:/Users/Phil/Developement/Victor/landseg/kategorien.json` und `C:/Users/Phil/Developement/Victor/landseg/KATEGORIEN.md`: die gültigen Klassen und Regeln.

## Dein Viertel

Viertel v2 (oben rechts) des Kerns von `r0c0`: x 314–563, y 64–313 im
Teilkachelbild (250 × 250 Bildpunkte). Dir gehören die 62 Segmente der Liste unten: Jedes hat den
größten Teil seiner Kernfläche in diesem Viertel. Die Teilkachel hat 141 Kernsegmente
(v1 22, v2 62, v3 19, v4 38); drei andere Zweitagents urteilen über die anderen Viertel, jeder in seinem eigenen
Ordner. Ein Segment über einer Viertelgrenze urteilt nur das Viertel mit dem größten Anteil; in den Bildern
der Nachbarn ist es mit grauer Nummer als Umgebung zu sehen.

Urteil im Verbund: Du siehst das Viertel als zusammenhängendes Bild mit Umgebung, arbeitest die Liste der
Reihe nach ab und beurteilst jedes Segment im Zusammenhang mit seinen Nachbarn; eingetragen wird jedes
Segment einzeln (Klasse, `sicher`, `was_ist_es` als Notiz). Bilder freigestellter Einzelsegmente gibt es
nicht, und sie sind keine Urteilsgrundlage.

Bilder des Viertels (fertig, JPEG, in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/viertel/r0c0/v2`, Fenster und Vergrößerung je Bild in `viertel.json`):

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
| 63 | 100063 | 1.2.1 Straße (versiegelt) | nein | nein | 150 | 61 % | v1 | 316/81 | klasse_unsicher |
| 46 | 100046 | 4.2.4 Gebüsch / Strauchfläche | nein | ja | 234 | 100 % | – | 339/69 | klasse_unsicher |
| 14 | 100014 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 3796 | 83 % | v1 | 349/94 | klasse_unsicher |
| 65 | 100065 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | ja | nein | 160 | 100 % | – | 381/86 | – |
| 58 | 100058 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | ja | nein | 90 | 100 % | – | 397/73 | – |
| 47 | 100047 | 2.1 Acker mit Bewuchs | nein | ja | 3019 | 100 % | – | 404/96 | klasse_unsicher, nicht_zusammenhaengend |
| 50 | 100050 | 3.1 Wiese / Weide (gemeinsam) | ja | ja | 48 | 100 % | – | 410/66 | – |
| 57 | 100057 | 3.1 Wiese / Weide (gemeinsam) | ja | ja | 270 | 100 % | – | 430/73 | – |
| 31 | 100031 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 44 | 100 % | – | 448/66 | klasse_unsicher |
| 33 | 100033 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 5092 | 100 % | – | 493/93 | – |
| 36 | 100036 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 19 | 100 % | – | 545/64 | grenze_ohne_bildkante, klasse_unsicher |
| 53 | 100053 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 102 | 100 % | – | 545/68 | klasse_unsicher |
| 40 | 100040 | 4.2.4 Gebüsch / Strauchfläche | nein | ja | 178 | 100 % | – | 558/69 | grenze_ohne_bildkante, klasse_unsicher |
| 92 | 100092 | 4.1 Wald (geschlossener Bestand) | nein | nein | 124 | 90 % | v1 | 318/139 | grenze_ohne_bildkante, klasse_unsicher |
| 59 | 100059 | 1.2.1 Straße (versiegelt) | ja | nein | 8711 | 64 % | v1 | 350/129 | grenze_ohne_bildkante |
| 87 | 100087 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 85 | 100 % | – | 378/128 | klasse_unsicher |
| 70 | 100070 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 2324 | 100 % | – | 407/132 | grenze_ohne_bildkante, klasse_unsicher |
| 93 | 100093 | 3.4 Krautsaum linear (Feldrain, Wegrand, Böschung) | nein | ja | 100 | 100 % | – | 420/146 | grenze_ohne_bildkante, klasse_unsicher |
| 76 | 100076 | 2.1 Acker mit Bewuchs | nein | ja | 175 | 100 % | – | 434/122 | klasse_unsicher, nicht_zusammenhaengend |
| 71 | 100071 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 174 | 100 % | – | 450/113 | klasse_unsicher |
| 73 | 100073 | 4.2.1 Einzelbaum | nein | ja | 557 | 100 % | – | 462/123 | klasse_unsicher |
| 89 | 100089 | 4.2.4 Gebüsch / Strauchfläche | nein | ja | 1066 | 100 % | – | 496/144 | grenze_ohne_bildkante, klasse_unsicher |
| 82 | 100082 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 179 | 100 % | – | 507/126 | klasse_unsicher |
| 91 | 100091 | 4.2.1 Einzelbaum | ja | ja | 669 | 100 % | – | 526/144 | grenze_ohne_bildkante |
| 78 | 100078 | 4.2.1 Einzelbaum | nein | ja | 296 | 100 % | – | 529/123 | grenze_ohne_bildkante, klasse_unsicher |
| 77 | 100077 | 4.2.1 Einzelbaum | nein | ja | 795 | 100 % | – | 552/134 | grenze_ohne_bildkante, klasse_unsicher |
| 74 | 100074 | 4.2.1 Einzelbaum | nein | ja | 100 | 100 % | – | 556/114 | klasse_unsicher |
| 61 | 100061 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 577 | 100 % | – | 557/104 | grenze_ohne_bildkante, klasse_unsicher |
| 97 | 100097 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | ja | nein | 237 | 100 % | – | 324/171 | nicht_zusammenhaengend |
| 98 | 100098 | 4.2.4 Gebüsch / Strauchfläche | nein | ja | 2909 | 100 % | – | 349/196 | grenze_ohne_bildkante, klasse_unsicher |
| 94 | 100094 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 461 | 100 % | – | 365/159 | grenze_ohne_bildkante, klasse_unsicher |
| 101 | 100101 | 1.2.1 Straße (versiegelt) | nein | nein | 89 | 100 % | – | 376/160 | grenze_ohne_bildkante, klasse_unsicher |
| 102 | 100102 | 4.1 Wald (geschlossener Bestand) | nein | nein | 1483 | 100 % | – | 390/179 | klasse_unsicher |
| 111 | 100111 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 216 | 100 % | – | 419/193 | – |
| 104 | 100104 | 1.2.1 Straße (versiegelt) | nein | nein | 158 | 100 % | – | 436/175 | klasse_unsicher |
| 105 | 100105 | 4.1 Wald (geschlossener Bestand) | nein | nein | 126 | 100 % | – | 447/179 | klasse_unsicher |
| 95 | 100095 | 1.2.1 Straße (versiegelt) | nein | nein | 520 | 100 % | – | 450/151 | grenze_ohne_bildkante, klasse_unsicher |
| 107 | 100107 | 1.2.1 Straße (versiegelt) | nein | nein | 157 | 100 % | – | 472/181 | klasse_unsicher |
| 106 | 100106 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 1027 | 100 % | – | 503/190 | klasse_unsicher |
| 100 | 100100 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 80 | 100 % | – | 523/160 | grenze_ohne_bildkante, klasse_unsicher |
| 108 | 100108 | 4.1 Wald (geschlossener Bestand) | ja | nein | 440 | 100 % | – | 525/193 | grenze_ohne_bildkante |
| 96 | 100096 | 4.2.4 Gebüsch / Strauchfläche | nein | ja | 99 | 100 % | – | 547/151 | grenze_ohne_bildkante, klasse_unsicher |
| 99 | 100099 | 1.2.1 Straße (versiegelt) | nein | nein | 173 | 100 % | – | 554/158 | grenze_ohne_bildkante, klasse_unsicher |
| 109 | 100109 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | ja | nein | 164 | 100 % | – | 555/185 | grenze_ohne_bildkante |
| 116 | 100116 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | ja | nein | 624 | 63 % | v1 | 322/204 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 117 | 100117 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 147 | 100 % | – | 378/212 | klasse_unsicher |
| 113 | 100113 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 9419 | 100 % | – | 482/233 | – |
| 115 | 100115 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 1064 | 100 % | – | 538/229 | klasse_unsicher |
| 114 | 100114 | 4.2.1 Einzelbaum | ja | ja | 745 | 100 % | – | 550/205 | grenze_ohne_bildkante |
| 121 | 100121 | 4.2.4 Gebüsch / Strauchfläche | nein | ja | 681 | 100 % | – | 556/248 | klasse_unsicher |
| 110 | 100110 | 4.1 Wald (geschlossener Bestand) | ja | nein | 14 | 100 % | – | 562/211 | grenze_ohne_bildkante |
| 124 | 100124 | 3.1 Wiese / Weide (gemeinsam) | ja | ja | 363 | 100 % | – | 329/281 | grenze_ohne_bildkante |
| 119 | 100119 | 4.1 Wald (geschlossener Bestand) | nein | nein | 1493 | 94 % | v1 | 354/296 | grenze_ohne_bildkante, klasse_unsicher |
| 120 | 100120 | 3.1 Wiese / Weide (gemeinsam) | ja | ja | 6620 | 100 % | – | 367/259 | grenze_ohne_bildkante |
| 133 | 100133 | 4.1 Wald (geschlossener Bestand) | ja | nein | 133 | 100 % | – | 370/299 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 131 | 100131 | 3.1 Wiese / Weide (gemeinsam) | ja | ja | 147 | 100 % | – | 389/291 | grenze_ohne_bildkante |
| 134 | 100134 | 2.1 Acker mit Bewuchs | nein | ja | 400 | 78 % | v4 | 407/298 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 132 | 100132 | 3.1 Wiese / Weide (gemeinsam) | ja | ja | 138 | 100 % | – | 428/298 | grenze_ohne_bildkante |
| 129 | 100129 | 4.1 Wald (geschlossener Bestand) | nein | nein | 1209 | 100 % | – | 458/291 | klasse_unsicher |
| 127 | 100127 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 1598 | 89 % | v4 | 527/288 | grenze_ohne_bildkante, klasse_unsicher |
| 122 | 100122 | 4.1 Wald (geschlossener Bestand) | ja | nein | 1167 | 100 % | – | 529/261 | grenze_ohne_bildkante |
| 139 | 100139 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 135 | 100 % | – | 466/304 | klasse_unsicher |

`nicht_geprueft` nennt, was du nicht angesehen hast, `offen`, was du nicht entscheiden konntest.

Kontrolle vor der Rückgabe (muss mit `ok` enden):

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I C:/Users/Phil/Developement/Victor/wuensche/2026-11-17-landseg-test-t0-1/skripte/pruefe_urteil.py --urteil C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/urteil-zweit/r0c0/v2/urteil.json --segmente C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/vorstufe/r0c0/segmente.json --fassung a --viertel v2 --ids 100063,100046,100014,100065,100058,100047,100050,100057,100031,100033,100036,100053,100040,100092,100059,100087,100070,100093,100076,100071,100073,100089,100082,100091,100078,100077,100074,100061,100097,100098,100094,100101,100102,100111,100104,100105,100095,100107,100106,100100,100108,100096,100099,100109,100116,100117,100113,100115,100114,100121,100110,100124,100119,100120,100133,100131,100134,100132,100129,100127,100122,100139 --kategorien C:/Users/Phil/Developement/Victor/landseg/kategorien.json
```

## Unabhängig urteilen

Du bist Zweitagent: Ein anderer Agent urteilt über dasselbe Viertel. Sein Ergebnis (`C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/urteil/`) siehst du nicht an, auch nicht, wenn es schon da ist. Aus beiden Urteilen wird die Übereinstimmung gemessen.

## Werkzeuge

Befehle im Ordner `C:/Users/Phil/Developement/Victor/landseg` mit `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -m landseg <befehl>`; Aufruf und Schalter stehen in
`C:/Users/Phil/Developement/Victor/landseg/README.md`. Die Bilder deines Viertels liegen fertig vor (Abschnitt „Dein Viertel“); `ansicht` (W3) erzeugt Bilder
je Segment und ist hier keine Urteilsgrundlage. Für fragliche Grenzen `kante` (W4, hier nur zum Ansehen
der Bildkante), zur Kontrolle `pruefen`. Eigene Skripte als Datei in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/urteil-zweit/r0c0/v2`.

## Ergebnis in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/urteil-zweit/r0c0/v2` (genau diese Namen)

- `roh.jpg`, `umriss.jpg` (alle Segmentgrenzen mit ID), `maengel.jpg` (nummerierte Punkte mit kurzer
  deutscher Beschriftung, sonst Vermerk „keine Mängel“), `vorschlag.jpg` (Grenzen und Klassen, wie
  du sie setzen würdest, sonst Vermerk „unverändert“): je dein Viertel mit Umgebung, Viertel
  umrandet (Grundlage: die vorbereiteten Übersichtsbilder).
- `nah_<n>.jpg`: eigene Nahansichten von Stellen, die man in den vorbereiteten Bildern nicht beurteilen kann,
  je ein Teil des Viertels samt Nachbarn (mindestens 64 × 64 Bildpunkte der Teilkachel, kein freigestelltes
  Einzelsegment); `kontrast_<n>.jpg` bei blassen Stellen.
- `urteil.json` (UTF-8):

```
{"teilkachel": "r0c0", "viertel": "v2", "bearbeiter": "zweit-a-r0c0-v2",
 "bilder_angesehen": {"uebersicht": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/viertel/r0c0/v2/uebersicht_nummern.jpg", "…"],
                      "nah": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/viertel/r0c0/v2/nah1_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/urteil-zweit/r0c0/v2/nah_1.jpg", "…"]},
 "segmente": [{"id": 17, "klasse_heute": "Code", "was_ist_es": "ein Satz",
               "urteil": "sauber" | "nicht_sauber", "klasse_vorschlag": "Code oder null",
               "sicher": true | false,
               "punkte": [{"nr": 1, "art": "fremdes|fehlt|trennen|verschmelzen|grenze|klasse|zu_klein|sonstiges",
                           "text": "ein Satz mit Stelle (x/y im Teilkachelbild)", "flaeche_px": Zahl oder null}],
               "bilder": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/viertel/r0c0/v2/uebersicht_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/viertel/r0c0/v2/nah2_roh.jpg"]}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "was an der Kerngrenze nicht passt"}],
 "unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."]}
```

Jedes Segment deiner Liste steht genau einmal unter `segmente`, auch die sauberen, in der Reihenfolge der Liste. Segmente der Nachbarviertel (graue Nummern) und des Kontextrands (ohne Nummer) urteilst du nicht; Auffälliges an ihnen nennst du unter `unsicher` mit ID.

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Punkte, Anteil `sicher: false`, wo du unsicher bist.
