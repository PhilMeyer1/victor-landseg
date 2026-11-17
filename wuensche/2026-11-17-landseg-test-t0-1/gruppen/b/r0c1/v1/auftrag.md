# Auftrag: Teilkachel r0c1, Viertel v1: 46 Segmente im Verbund ansehen und einzeln urteilen (Fassung B: Kategorien frei)

Lies zuerst den Skill `landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `r0c1` des Ausschnitts in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b`. Du urteilst über jedes
Segment deines Viertels v1 (Liste unter „Dein Viertel“), ob Grenze und Klasse stimmen, und zeichnest ein, was
du ändern würdest. Die Label-Karte änderst du nicht.

## Daten (eingefrorener Stand, nur lesen)

- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/manifest.json`: Eintrag `r0c1` unter `teilkacheln` mit `bild` (Teilkachelbild,
  Kern + Kontextrand), `kern_im_bild` (Lage des Kerns im Teilkachelbild) und `kern` (Lage im Ausschnitt).
- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/vorstufe/r0c1/labels.tif`: Label-Karte (Segment-ID je Bildpunkt, Größe des Teilkachelbilds).
- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/vorstufe/r0c1/segmente.json`: je Segment `id`, `klasse`, `grob`, `herkunft`, `sicher`; dazu die
  Kandidatenliste der Vorstufe, falls vorhanden.
- `C:/Users/Phil/Developement/Victor/landseg/kategorien.json` und `C:/Users/Phil/Developement/Victor/landseg/KATEGORIEN.md`: nur Anregung; in Fassung B benennst du die Klassen selbst (Abschnitt „Fassung B“).

## Dein Viertel

Viertel v1 (oben links) des Kerns von `r0c1`: x 64–313, y 64–313 im
Teilkachelbild (250 × 250 Bildpunkte). Dir gehören die 46 Segmente der Liste unten: Jedes hat den
größten Teil seiner Kernfläche in diesem Viertel. Die Teilkachel hat 147 Kernsegmente
(v1 46, v2 43, v3 37, v4 21); drei andere Agents urteilen gleichzeitig über die anderen Viertel, jeder in seinem eigenen
Ordner. Ein Segment über einer Viertelgrenze urteilt nur das Viertel mit dem größten Anteil; in den Bildern
der Nachbarn ist es mit grauer Nummer als Umgebung zu sehen.

Urteil im Verbund: Du siehst das Viertel als zusammenhängendes Bild mit Umgebung, arbeitest die Liste der
Reihe nach ab und beurteilst jedes Segment im Zusammenhang mit seinen Nachbarn; eingetragen wird jedes
Segment einzeln (Klasse, `sicher`, `was_ist_es` als Notiz). Bilder freigestellter Einzelsegmente gibt es
nicht, und sie sind keine Urteilsgrundlage.

Bilder des Viertels (fertig, JPEG, in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r0c1/v1`, Fenster und Vergrößerung je Bild in `viertel.json`):

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
Teilkachelbild; Kandidaten aus `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/vorstufe/r0c1/kandidaten.json`, dort mit Grund, in den
Bildern nicht eingezeichnet; Anteil hier = Anteil der Kernfläche in diesem Viertel):

| Nr | ID | Klasse Vorstufe | sicher | im Siedlungsgebiet | Kernfläche px | Anteil hier | auch in | Punkt x/y | Kandidaten |
|---|---|---|---|---|---|---|---|---|---|
| 58 | 200058 | 4.2.1 Einzelbaum | nein | ja | 522 | 100 % | – | 75/76 | grenze_ohne_bildkante, klasse_unsicher |
| 52 | 200052 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | ja | nein | 174 | 100 % | – | 126/67 | grenze_ohne_bildkante |
| 60 | 200060 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 3642 | 100 % | – | 157/91 | grenze_ohne_bildkante |
| 57 | 200057 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 42 | 100 % | – | 187/65 | klasse_unsicher |
| 36 | 200036 | 4.2.1 Einzelbaum | nein | ja | 97 | 100 % | – | 196/67 | klasse_unsicher |
| 64 | 200064 | 4.2.1 Einzelbaum | nein | ja | 119 | 100 % | – | 208/77 | grenze_ohne_bildkante, klasse_unsicher |
| 66 | 200066 | 4.2.4 Gebüsch / Strauchfläche | nein | ja | 323 | 100 % | – | 217/85 | klasse_unsicher |
| 59 | 200059 | 1.3.3 Schwimmbecken | nein | nein | 110 | 100 % | – | 225/74 | grenze_ohne_bildkante, klasse_unsicher |
| 67 | 200067 | 1.3.3 Schwimmbecken | ja | nein | 94 | 100 % | – | 241/92 | – |
| 65 | 200065 | 1.3.3 Schwimmbecken | ja | nein | 334 | 100 % | – | 242/80 | grenze_ohne_bildkante |
| 45 | 200045 | 4.2.1 Einzelbaum | ja | ja | 2877 | 74 % | v2 | 292/85 | – |
| 80 | 200080 | 4.2.1 Einzelbaum | nein | ja | 338 | 100 % | – | 69/144 | klasse_unsicher |
| 85 | 200085 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 822 | 100 % | – | 98/144 | grenze_ohne_bildkante, klasse_unsicher |
| 43 | 200043 | 4.1 Wald (geschlossener Bestand) | nein | nein | 8420 | 100 % | – | 100/110 | grenze_ohne_bildkante, klasse_unsicher |
| 69 | 200069 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 115 | 100 % | – | 124/104 | klasse_unsicher |
| 82 | 200082 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 104 | 100 % | – | 145/126 | grenze_ohne_bildkante, klasse_unsicher |
| 75 | 200075 | 4.2.4 Gebüsch / Strauchfläche | nein | ja | 1884 | 100 % | – | 226/124 | grenze_ohne_bildkante, klasse_unsicher |
| 79 | 200079 | 1.2.1 Straße (versiegelt) | nein | nein | 163 | 100 % | – | 258/120 | klasse_unsicher |
| 89 | 200089 | 1.2.1 Straße (versiegelt) | nein | nein | 184 | 100 % | – | 280/140 | klasse_unsicher |
| 81 | 200081 | 4.1 Wald (geschlossener Bestand) | nein | nein | 1110 | 52 % | v2 | 301/136 | klasse_unsicher |
| 99 | 200099 | 4.1 Wald (geschlossener Bestand) | nein | nein | 4 | 100 % | – | 64/154 | grenze_ohne_bildkante, klasse_unsicher |
| 100 | 200100 | 1.2.1 Straße (versiegelt) | nein | nein | 151 | 100 % | – | 67/158 | grenze_ohne_bildkante, klasse_unsicher |
| 107 | 200107 | 4.2.1 Einzelbaum | nein | ja | 1934 | 100 % | – | 107/191 | grenze_ohne_bildkante, klasse_unsicher |
| 111 | 200111 | 4.1 Wald (geschlossener Bestand) | nein | nein | 448 | 100 % | – | 139/184 | klasse_unsicher |
| 93 | 200093 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | ja | nein | 2579 | 100 % | – | 140/163 | grenze_ohne_bildkante |
| 117 | 200117 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 283 | 100 % | – | 148/197 | klasse_unsicher |
| 105 | 200105 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 181 | 100 % | – | 166/169 | klasse_unsicher |
| 110 | 200110 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 726 | 100 % | – | 167/190 | grenze_ohne_bildkante, klasse_unsicher |
| 108 | 200108 | 4.1 Wald (geschlossener Bestand) | nein | nein | 280 | 100 % | – | 186/178 | klasse_unsicher |
| 112 | 200112 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 355 | 100 % | – | 215/183 | grenze_ohne_bildkante, klasse_unsicher |
| 94 | 200094 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 607 | 100 % | – | 227/157 | grenze_ohne_bildkante, klasse_unsicher |
| 97 | 200097 | 4.2.1 Einzelbaum | ja | ja | 713 | 100 % | – | 247/165 | grenze_ohne_bildkante |
| 98 | 200098 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 353 | 100 % | – | 274/161 | klasse_unsicher |
| 122 | 200122 | 4.2.1 Einzelbaum | ja | ja | 219 | 100 % | – | 67/200 | grenze_ohne_bildkante |
| 133 | 200133 | 4.1 Wald (geschlossener Bestand) | ja | nein | 143 | 100 % | – | 68/243 | – |
| 126 | 200126 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 5411 | 100 % | – | 125/235 | grenze_ohne_bildkante, klasse_unsicher |
| 128 | 200128 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 770 | 100 % | – | 171/230 | grenze_ohne_bildkante, klasse_unsicher |
| 121 | 200121 | 4.1 Wald (geschlossener Bestand) | ja | nein | 308 | 100 % | – | 195/217 | – |
| 130 | 200130 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 194 | 100 % | – | 203/224 | – |
| 102 | 200102 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 6484 | 100 % | – | 234/213 | – |
| 132 | 200132 | 4.2.1 Einzelbaum | ja | ja | 133 | 100 % | – | 66/256 | – |
| 116 | 200116 | 4.1 Wald (geschlossener Bestand) | nein | nein | 1024 | 84 % | v3 | 73/288 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 138 | 200138 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 536 | 100 % | – | 103/275 | grenze_ohne_bildkante |
| 137 | 200137 | 4.1 Wald (geschlossener Bestand) | ja | nein | 82 | 100 % | – | 221/260 | – |
| 92 | 200092 | 4.1 Wald (geschlossener Bestand) | nein | nein | 18137 | 71 % | v2, v3 | 279/270 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 144 | 200144 | 4.1 Wald (geschlossener Bestand) | ja | nein | 94 | 100 % | – | 255/305 | – |

`nicht_geprueft` nennt, was du nicht angesehen hast, `offen`, was du nicht entscheiden konntest.

Kontrolle vor der Rückgabe (muss mit `ok` enden):

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I C:/Users/Phil/Developement/Victor/wuensche/2026-11-17-landseg-test-t0-1/skripte/pruefe_urteil.py --urteil C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/urteil/r0c1/v1/urteil.json --segmente C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/vorstufe/r0c1/segmente.json --fassung b --viertel v1 --ids 200058,200052,200060,200057,200036,200064,200066,200059,200067,200065,200045,200080,200085,200043,200069,200082,200075,200079,200089,200081,200099,200100,200107,200111,200093,200117,200105,200110,200108,200112,200094,200097,200098,200122,200133,200126,200128,200121,200130,200102,200132,200116,200138,200137,200092,200144
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
der Bildkante), zur Kontrolle `pruefen`. Eigene Skripte als Datei in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/urteil/r0c1/v1`.

## Ergebnis in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/urteil/r0c1/v1` (genau diese Namen)

- `roh.jpg`, `umriss.jpg` (alle Segmentgrenzen mit ID), `maengel.jpg` (nummerierte Punkte mit kurzer
  deutscher Beschriftung, sonst Vermerk „keine Mängel“), `vorschlag.jpg` (Grenzen und Klassen, wie
  du sie setzen würdest, sonst Vermerk „unverändert“): je dein Viertel mit Umgebung, Viertel
  umrandet (Grundlage: die vorbereiteten Übersichtsbilder).
- `nah_<n>.jpg`: eigene Nahansichten von Stellen, die man in den vorbereiteten Bildern nicht beurteilen kann,
  je ein Teil des Viertels samt Nachbarn (mindestens 64 × 64 Bildpunkte der Teilkachel, kein freigestelltes
  Einzelsegment); `kontrast_<n>.jpg` bei blassen Stellen.
- `urteil.json` (UTF-8):

```
{"teilkachel": "r0c1", "viertel": "v1", "bearbeiter": "urt-b-r0c1-v1",
 "bilder_angesehen": {"uebersicht": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r0c1/v1/uebersicht_nummern.jpg", "…"],
                      "nah": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r0c1/v1/nah1_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/urteil/r0c1/v1/nah_1.jpg", "…"]},
 "segmente": [{"id": 17, "klasse_heute": "Code", "was_ist_es": "ein Satz",
               "urteil": "sauber" | "nicht_sauber", "klasse_vorschlag": null,
               "klasse_frei": {"grob": "Name", "mittel": "Name", "fein": "Name"},
               "sicher": true | false,
               "punkte": [{"nr": 1, "art": "fremdes|fehlt|trennen|verschmelzen|grenze|klasse|zu_klein|sonstiges",
                           "text": "ein Satz mit Stelle (x/y im Teilkachelbild)", "flaeche_px": Zahl oder null}],
               "bilder": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r0c1/v1/uebersicht_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r0c1/v1/nah2_roh.jpg"]}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "was an der Kerngrenze nicht passt"}],
 "unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."],
 "klassen_frei": [{"name": "Name", "ebene": "grob|mittel|fein", "eltern": "Name oder null", "merkmal": "woran im Bild erkennbar"}]}
```

Jedes Segment deiner Liste steht genau einmal unter `segmente`, auch die sauberen, in der Reihenfolge der Liste. Segmente der Nachbarviertel (graue Nummern) und des Kontextrands (ohne Nummer) urteilst du nicht; Auffälliges an ihnen nennst du unter `unsicher` mit ID.

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Punkte, Anteil `sicher: false`, wo du unsicher bist.
