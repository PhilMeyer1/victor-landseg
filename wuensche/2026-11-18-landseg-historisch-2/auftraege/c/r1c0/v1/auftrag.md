# Auftrag: H0, Teilkachel r1c0, Viertel v1: 29 Segmente im Verbund ansehen und einzeln urteilen (Fassung C „Feste Kategorienliste“)

Lies zuerst den Skill `landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `r1c0` des Ausschnitts in `C:/Users/Phil/Developement/Victor/daten/landseg/H0`. Du urteilst über jedes
Segment deines Viertels v1 (Liste unter „Dein Viertel“), ob Grenze und Klasse stimmen, und zeichnest ein, was
du ändern würdest. Die Label-Karte änderst du nicht.

## Daten (eingefrorener Stand, nur lesen)

- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/manifest.json`: Eintrag `r1c0` unter `teilkacheln` mit `bild` (Teilkachelbild,
  Kern + Kontextrand), `kern_im_bild` (Lage des Kerns im Teilkachelbild) und `kern` (Lage im Ausschnitt).
- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r1c0/labels.tif`: Label-Karte (Segment-ID je Bildpunkt, Größe des Teilkachelbilds).
- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r1c0/segmente.json`: je Segment `id`, `klasse`, `grob`, `herkunft`, `sicher`; dazu die
  Kandidatenliste der Vorstufe, falls vorhanden.
- `C:/Users/Phil/Developement/Victor/landseg/kategorien.json` und `C:/Users/Phil/Developement/Victor/landseg/KATEGORIEN.md`: die gültigen Klassen und Regeln.

## Zuerst der ganze Ausschnitt, dann die Teilkachel

Bevor du dein Viertel ansiehst: zuerst den ganzen Ausschnitt H0 (`C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png`, mit Teilkachelgitter
`C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/H0_raster.jpg`; r0c0 oben links, r0c1 oben rechts, r1c0 unten links, r1c1 unten rechts),
dann die ganze Teilkachel `r1c0` (`C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r1c0/ganz_nummern.jpg`: Grenzen, Nummern, Viertel cyan v1–v4;
`C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r1c0/ganz_roh.jpg` unverändert; beide 2fach). Beide stehen in `bilder_angesehen.uebersicht` vor den Viertelbildern.

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

Viertel v1 (oben links) des Kerns von `r1c0`: x 64–313, y 64–313 im
Teilkachelbild (250 × 250 Bildpunkte). Dir gehören die 29 Segmente der Liste unten: Jedes hat den
größten Teil seiner Kernfläche in diesem Viertel. Die Teilkachel hat 85 Kernsegmente
(v1 29, v2 37, v3 14, v4 5); die anderen Viertel stehen in eigenen Aufträgen mit eigenem Ergebnisordner. Ein Segment
über einer Viertelgrenze urteilt nur das Viertel mit dem größten Anteil; in den Bildern der Nachbarn ist
es mit grauer Nummer als Umgebung zu sehen.

Urteil im Verbund: Du siehst das Viertel als zusammenhängendes Bild mit Umgebung, arbeitest die Liste der
Reihe nach ab und beurteilst jedes Segment im Zusammenhang mit seinen Nachbarn; eingetragen wird jedes
Segment einzeln (Klasse, `sicher`, `was_ist_es` als Notiz). Bilder freigestellter Einzelsegmente gibt es
nicht, und sie sind keine Urteilsgrundlage.

Bilder des Viertels (fertig, JPEG, in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c0/v1`, Fenster und Vergrößerung je Bild in `viertel.json`):

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
Teilkachelbild; Kandidaten aus `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r1c0/kandidaten.json`, dort mit Grund, in den
Bildern nicht eingezeichnet; Anteil hier = Anteil der Kernfläche in diesem Viertel):

| Nr | ID | Klasse Vorstufe | sicher | im Siedlungsgebiet | Kernfläche px | Anteil hier | auch in | Punkt x/y | Kandidaten |
|---|---|---|---|---|---|---|---|---|---|
| 22 | 300022 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 4720 | 100 % | – | 150/91 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 2 | 300002 | 2.1 Acker mit Bewuchs | nein | ja | 5782 | 87 % | v2 | 239/88 | grenze_ohne_bildkante, klasse_unsicher |
| 56 | 300056 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 137 | 100 % | – | 222/137 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 47 | 300047 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 2228 | 100 % | – | 261/122 | grenze_ohne_bildkante, klasse_unsicher |
| 43 | 300043 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 286 | 100 % | – | 270/105 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 1 | 300001 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 16066 | 100 % | – | 109/157 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 68 | 300068 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 75 | 100 % | – | 67/214 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 80 | 300080 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 378 | 100 % | – | 71/247 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 70 | 300070 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 163 | 100 % | – | 90/212 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 64 | 300064 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 5641 | 100 % | – | 165/249 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 72 | 300072 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 127 | 100 % | – | 224/227 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 81 | 300081 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 141 | 100 % | – | 246/247 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 48 | 300048 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 16381 | 56 % | v2 | 270/200 | grenze_ohne_bildkante, klasse_unsicher |
| 91 | 300091 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 275 | 100 % | – | 68/286 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 92 | 300092 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 185 | 100 % | – | 78/283 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 94 | 300094 | 1.2.1 Straße (versiegelt) | nein | nein | 148 | 100 % | – | 102/298 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 69 | 300069 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 6375 | 100 % | – | 104/263 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 84 | 300084 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 111 | 100 % | – | 193/255 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 93 | 300093 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 278 | 100 % | – | 199/296 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 71 | 300071 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 2456 | 100 % | – | 220/251 | grenze_ohne_bildkante, klasse_unsicher |
| 89 | 300089 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 143 | 100 % | – | 241/273 | klasse_unsicher, nicht_zusammenhaengend |
| 85 | 300085 | 1.2.1 Straße (versiegelt) | nein | nein | 275 | 100 % | – | 260/259 | klasse_unsicher, nicht_zusammenhaengend |
| 88 | 300088 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 338 | 100 % | – | 288/269 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 74 | 300074 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 1342 | 77 % | v3 | 71/305 | grenze_ohne_bildkante, klasse_unsicher |
| 97 | 300097 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 73 | 100 % | – | 128/303 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 96 | 300096 | 5.3 Feuchtgebiet / Röhricht / Ufervegetation | nein | nein | 183 | 100 % | – | 138/303 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 98 | 300098 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 84 | 100 % | – | 181/304 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 100 | 300100 | 5.3 Feuchtgebiet / Röhricht / Ufervegetation | nein | nein | 185 | 54 % | v3 | 194/310 | klasse_unsicher, nicht_zusammenhaengend |
| 95 | 300095 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 271 | 100 % | – | 245/304 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |

`nicht_geprueft` nennt, was du nicht angesehen hast, `offen`, was du nicht entscheiden konntest.

Kontrolle vor der Rückgabe (muss mit `ok` enden):

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-2/skripte/pruefe_urteil.py --urteil C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r1c0/v1/urteil.json --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r1c0/segmente.json --fassung c --viertel v1 --ids 300022,300002,300056,300047,300043,300001,300068,300080,300070,300064,300072,300081,300048,300091,300092,300094,300069,300084,300093,300071,300089,300085,300088,300074,300097,300096,300098,300100,300095 --kategorien C:/Users/Phil/Developement/Victor/landseg/kategorien.json
```

## Werkzeuge

Befehle im Ordner `C:/Users/Phil/Developement/Victor/landseg` mit `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -m landseg <befehl>`; Aufruf und Schalter stehen in
`C:/Users/Phil/Developement/Victor/landseg/README.md`. Die Bilder deines Viertels liegen fertig vor (Abschnitt „Dein Viertel“); `ansicht` (W3) erzeugt Bilder
je Segment und ist hier keine Urteilsgrundlage. Für fragliche Grenzen `kante` (W4, hier nur zum Ansehen
der Bildkante), zur Kontrolle `pruefen`. Eigene Skripte als Datei in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r1c0/v1`.

## Ergebnis in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r1c0/v1` (genau diese Namen)

- `roh.jpg`, `umriss.jpg` (alle Segmentgrenzen mit ID), `maengel.jpg` (nummerierte Punkte mit kurzer
  deutscher Beschriftung, sonst Vermerk „keine Mängel“), `vorschlag.jpg` (Grenzen und Klassen, wie
  du sie setzen würdest, sonst Vermerk „unverändert“): je dein Viertel mit Umgebung, Viertel
  umrandet (Grundlage: die vorbereiteten Übersichtsbilder).
- `nah_<n>.jpg`: eigene Nahansichten von Stellen, die man in den vorbereiteten Bildern nicht beurteilen kann,
  je ein Teil des Viertels samt Nachbarn (mindestens 64 × 64 Bildpunkte der Teilkachel, kein freigestelltes
  Einzelsegment); `kontrast_<n>.jpg` bei blassen Stellen.
- `urteil.json` (UTF-8):

```
{"teilkachel": "r1c0", "viertel": "v1", "bearbeiter": "urt-c-r1c0-v1",
 "bilder_angesehen": {"uebersicht": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r1c0/ganz_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c0/v1/uebersicht_nummern.jpg", "…"],
                      "nah": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c0/v1/nah1_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/r1c0/v1/nah_1.jpg", "…"]},
 "segmente": [{"id": 17, "klasse_heute": "Code", "was_ist_es": "ein Satz",
               "urteil": "sauber" | "nicht_sauber", "klasse_vorschlag": "Code oder null",
               "sicher": true | false,
               "punkte": [{"nr": 1, "art": "fremdes|fehlt|trennen|verschmelzen|grenze|klasse|zu_klein|sonstiges",
                           "text": "ein Satz mit Stelle (x/y im Teilkachelbild)", "flaeche_px": Zahl oder null}],
               "bilder": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c0/v1/uebersicht_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c0/v1/nah2_roh.jpg"]}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "was an der Kerngrenze nicht passt"}],
 "unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."]}
```

Jedes Segment deiner Liste steht genau einmal unter `segmente`, auch die sauberen, in der Reihenfolge der Liste. Segmente der Nachbarviertel (graue Nummern) und des Kontextrands (ohne Nummer) urteilst du in diesem Auftrag nicht; Auffälliges an ihnen nennst du unter `unsicher` mit ID.

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Punkte, Anteil `sicher: false`, wo du unsicher bist.
