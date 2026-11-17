# Auftrag: Teilkachel r0c0, Viertel v1: 22 Segmente im Verbund ansehen und einzeln urteilen

Lies zuerst den Skill `landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `r0c0` des Ausschnitts in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500`. Du urteilst über jedes
Segment deines Viertels v1 (Liste unter „Dein Viertel“), ob Grenze und Klasse stimmen, und zeichnest ein, was
du ändern würdest. Die Label-Karte änderst du nicht.

## Daten (eingefrorener Stand, nur lesen)

- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/manifest.json`: Eintrag `r0c0` unter `teilkacheln` mit `bild` (Teilkachelbild,
  Kern + Kontextrand), `kern_im_bild` (Lage des Kerns im Teilkachelbild) und `kern` (Lage im Ausschnitt).
- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/vorstufe/r0c0/labels.tif`: Label-Karte (Segment-ID je Bildpunkt, Größe des Teilkachelbilds).
- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/vorstufe/r0c0/segmente.json`: je Segment `id`, `klasse`, `grob`, `herkunft`, `sicher`; dazu die
  Kandidatenliste der Vorstufe, falls vorhanden.
- `C:/Users/Phil/Developement/Victor/landseg/kategorien.json` und `C:/Users/Phil/Developement/Victor/landseg/KATEGORIEN.md`: die gültigen Klassen und Regeln.

## Dein Viertel

Viertel v1 (oben links) des Kerns von `r0c0`: x 64–313, y 64–313 im
Teilkachelbild (250 × 250 Bildpunkte). Dir gehören die 22 Segmente der Liste unten: Jedes hat den
größten Teil seiner Kernfläche in diesem Viertel. Die Teilkachel hat 141 Kernsegmente
(v1 22, v2 62, v3 19, v4 38); drei andere Agents urteilen gleichzeitig über die anderen Viertel, jeder in seinem eigenen
Ordner. Ein Segment über einer Viertelgrenze urteilt nur das Viertel mit dem größten Anteil; in den Bildern
der Nachbarn ist es mit grauer Nummer als Umgebung zu sehen.

Urteil im Verbund: Du siehst das Viertel als zusammenhängendes Bild mit Umgebung, arbeitest die Liste der
Reihe nach ab und beurteilst jedes Segment im Zusammenhang mit seinen Nachbarn; eingetragen wird jedes
Segment einzeln (Klasse, `sicher`, `was_ist_es` als Notiz). Bilder freigestellter Einzelsegmente gibt es
nicht, und sie sind keine Urteilsgrundlage.

Bilder des Viertels (fertig, JPEG, in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/viertel/r0c0/v1`, Fenster und Vergrößerung je Bild in `viertel.json`):

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
| 27 | 100027 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 86 | 100 % | – | 66/66 | grenze_ohne_bildkante, klasse_unsicher |
| 48 | 100048 | 4.2.1 Einzelbaum | ja | ja | 5751 | 100 % | – | 91/91 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 54 | 100054 | 1.2.1 Straße (versiegelt) | nein | nein | 69 | 100 % | – | 162/66 | grenze_ohne_bildkante, klasse_unsicher |
| 67 | 100067 | 4.1 Wald (geschlossener Bestand) | ja | nein | 135 | 100 % | – | 168/91 | grenze_ohne_bildkante |
| 38 | 100038 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 1272 | 100 % | – | 209/72 | grenze_ohne_bildkante, klasse_unsicher |
| 51 | 100051 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 179 | 100 % | – | 236/70 | grenze_ohne_bildkante, klasse_unsicher |
| 10 | 100010 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 158 | 100 % | – | 250/68 | grenze_ohne_bildkante |
| 68 | 100068 | 1.2.1 Straße (versiegelt) | nein | nein | 117 | 100 % | – | 261/95 | grenze_ohne_bildkante, klasse_unsicher |
| 11 | 100011 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 1268 | 96 % | v2 | 268/76 | grenze_ohne_bildkante, klasse_unsicher |
| 52 | 100052 | 1.3.1 Lager-, Schotter-, Kiesfläche (künstlich, unversiegelt) | nein | nein | 488 | 63 % | v2 | 290/83 | klasse_unsicher |
| 66 | 100066 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 152 | 100 % | – | 292/91 | klasse_unsicher |
| 84 | 100084 | 2.1 Acker mit Bewuchs | nein | ja | 134 | 100 % | – | 81/127 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 79 | 100079 | 2.1 Acker mit Bewuchs | nein | ja | 151 | 100 % | – | 103/126 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 72 | 100072 | 2.1 Acker mit Bewuchs | nein | ja | 150 | 100 % | – | 150/116 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 86 | 100086 | 4.1 Wald (geschlossener Bestand) | ja | nein | 1619 | 100 % | – | 204/143 | grenze_ohne_bildkante |
| 81 | 100081 | 2.1 Acker mit Bewuchs | nein | ja | 98 | 100 % | – | 208/123 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 80 | 100080 | 2.1 Acker mit Bewuchs | nein | ja | 409 | 100 % | – | 178/152 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 112 | 100112 | 4.2.4 Gebüsch / Strauchfläche | nein | nein | 1238 | 100 % | – | 78/215 | grenze_ohne_bildkante, klasse_unsicher |
| 56 | 100056 | 3.1 Wiese / Weide (gemeinsam) | ja | nein | 90354 | 48 % | v2, v3, v4 | 238/230 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 125 | 100125 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 603 | 100 % | – | 112/288 | grenze_ohne_bildkante, klasse_unsicher |
| 123 | 100123 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | ja | nein | 454 | 100 % | – | 166/276 | – |
| 138 | 100138 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 331 | 60 % | v3 | 160/308 | klasse_unsicher |

`nicht_geprueft` nennt, was du nicht angesehen hast, `offen`, was du nicht entscheiden konntest.

Kontrolle vor der Rückgabe (muss mit `ok` enden):

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I C:/Users/Phil/Developement/Victor/wuensche/2026-11-17-landseg-test-t0-1/skripte/pruefe_urteil.py --urteil C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/urteil/r0c0/v1/urteil.json --segmente C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/vorstufe/r0c0/segmente.json --fassung a --viertel v1 --ids 100027,100048,100054,100067,100038,100051,100010,100068,100011,100052,100066,100084,100079,100072,100086,100081,100080,100112,100056,100125,100123,100138 --kategorien C:/Users/Phil/Developement/Victor/landseg/kategorien.json
```

## Werkzeuge

Befehle im Ordner `C:/Users/Phil/Developement/Victor/landseg` mit `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -m landseg <befehl>`; Aufruf und Schalter stehen in
`C:/Users/Phil/Developement/Victor/landseg/README.md`. Die Bilder deines Viertels liegen fertig vor (Abschnitt „Dein Viertel“); `ansicht` (W3) erzeugt Bilder
je Segment und ist hier keine Urteilsgrundlage. Für fragliche Grenzen `kante` (W4, hier nur zum Ansehen
der Bildkante), zur Kontrolle `pruefen`. Eigene Skripte als Datei in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/urteil/r0c0/v1`.

## Ergebnis in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/urteil/r0c0/v1` (genau diese Namen)

- `roh.jpg`, `umriss.jpg` (alle Segmentgrenzen mit ID), `maengel.jpg` (nummerierte Punkte mit kurzer
  deutscher Beschriftung, sonst Vermerk „keine Mängel“), `vorschlag.jpg` (Grenzen und Klassen, wie
  du sie setzen würdest, sonst Vermerk „unverändert“): je dein Viertel mit Umgebung, Viertel
  umrandet (Grundlage: die vorbereiteten Übersichtsbilder).
- `nah_<n>.jpg`: eigene Nahansichten von Stellen, die man in den vorbereiteten Bildern nicht beurteilen kann,
  je ein Teil des Viertels samt Nachbarn (mindestens 64 × 64 Bildpunkte der Teilkachel, kein freigestelltes
  Einzelsegment); `kontrast_<n>.jpg` bei blassen Stellen.
- `urteil.json` (UTF-8):

```
{"teilkachel": "r0c0", "viertel": "v1", "bearbeiter": "urt-a-r0c0-v1",
 "bilder_angesehen": {"uebersicht": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/viertel/r0c0/v1/uebersicht_nummern.jpg", "…"],
                      "nah": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/viertel/r0c0/v1/nah1_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/urteil/r0c0/v1/nah_1.jpg", "…"]},
 "segmente": [{"id": 17, "klasse_heute": "Code", "was_ist_es": "ein Satz",
               "urteil": "sauber" | "nicht_sauber", "klasse_vorschlag": "Code oder null",
               "sicher": true | false,
               "punkte": [{"nr": 1, "art": "fremdes|fehlt|trennen|verschmelzen|grenze|klasse|zu_klein|sonstiges",
                           "text": "ein Satz mit Stelle (x/y im Teilkachelbild)", "flaeche_px": Zahl oder null}],
               "bilder": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/viertel/r0c0/v1/uebersicht_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/viertel/r0c0/v1/nah2_roh.jpg"]}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "was an der Kerngrenze nicht passt"}],
 "unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."]}
```

Jedes Segment deiner Liste steht genau einmal unter `segmente`, auch die sauberen, in der Reihenfolge der Liste. Segmente der Nachbarviertel (graue Nummern) und des Kontextrands (ohne Nummer) urteilst du nicht; Auffälliges an ihnen nennst du unter `unsicher` mit ID.

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Punkte, Anteil `sicher: false`, wo du unsicher bist.
