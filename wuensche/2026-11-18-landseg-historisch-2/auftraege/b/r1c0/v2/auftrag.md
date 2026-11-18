# Auftrag: H0, Teilkachel r1c0, Viertel v2: 37 Segmente im Verbund ansehen und einzeln urteilen (Fassung B „Kategorien frei“)

Lies zuerst den Skill `landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `r1c0` des Ausschnitts in `C:/Users/Phil/Developement/Victor/daten/landseg/H0`. Du urteilst über jedes
Segment deines Viertels v2 (Liste unter „Dein Viertel“), ob Grenze und Klasse stimmen, und zeichnest ein, was
du ändern würdest. Die Label-Karte änderst du nicht.

## Daten (eingefrorener Stand, nur lesen)

- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/manifest.json`: Eintrag `r1c0` unter `teilkacheln` mit `bild` (Teilkachelbild,
  Kern + Kontextrand), `kern_im_bild` (Lage des Kerns im Teilkachelbild) und `kern` (Lage im Ausschnitt).
- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r1c0/labels.tif`: Label-Karte (Segment-ID je Bildpunkt, Größe des Teilkachelbilds).
- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r1c0/segmente.json`: je Segment `id`, `klasse`, `grob`, `herkunft`, `sicher`; dazu die
  Kandidatenliste der Vorstufe, falls vorhanden.
- `C:/Users/Phil/Developement/Victor/landseg/kategorien.json` und `C:/Users/Phil/Developement/Victor/landseg/KATEGORIEN.md`: nur Anregung; in Fassung B benennst du die Klassen selbst (Abschnitt „Fassung B“).

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

Viertel v2 (oben rechts) des Kerns von `r1c0`: x 314–563, y 64–313 im
Teilkachelbild (250 × 250 Bildpunkte). Dir gehören die 37 Segmente der Liste unten: Jedes hat den
größten Teil seiner Kernfläche in diesem Viertel. Die Teilkachel hat 85 Kernsegmente
(v1 29, v2 37, v3 14, v4 5); die anderen Viertel stehen in eigenen Aufträgen mit eigenem Ergebnisordner. Ein Segment
über einer Viertelgrenze urteilt nur das Viertel mit dem größten Anteil; in den Bildern der Nachbarn ist
es mit grauer Nummer als Umgebung zu sehen.

Urteil im Verbund: Du siehst das Viertel als zusammenhängendes Bild mit Umgebung, arbeitest die Liste der
Reihe nach ab und beurteilst jedes Segment im Zusammenhang mit seinen Nachbarn; eingetragen wird jedes
Segment einzeln (Klasse, `sicher`, `was_ist_es` als Notiz). Bilder freigestellter Einzelsegmente gibt es
nicht, und sie sind keine Urteilsgrundlage.

Bilder des Viertels (fertig, JPEG, in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c0/v2`, Fenster und Vergrößerung je Bild in `viertel.json`):

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
Teilkachelbild; Kandidaten aus `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r1c0/kandidaten.json`, dort mit Grund, in den
Bildern nicht eingezeichnet; Anteil hier = Anteil der Kernfläche in diesem Viertel):

| Nr | ID | Klasse Vorstufe | sicher | im Siedlungsgebiet | Kernfläche px | Anteil hier | auch in | Punkt x/y | Kandidaten |
|---|---|---|---|---|---|---|---|---|---|
| 30 | 300030 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 1324 | 100 % | – | 357/87 | grenze_ohne_bildkante, klasse_unsicher |
| 27 | 300027 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 4 | 100 % | – | 372/64 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 31 | 300031 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 531 | 100 % | – | 385/79 | grenze_ohne_bildkante, klasse_unsicher |
| 41 | 300041 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 144 | 100 % | – | 391/98 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 23 | 300023 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 277 | 100 % | – | 395/68 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 34 | 300034 | 1.2.1 Straße (versiegelt) | nein | nein | 413 | 100 % | – | 407/97 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 6 | 300006 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 2104 | 100 % | – | 428/82 | grenze_ohne_bildkante, klasse_unsicher |
| 26 | 300026 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 3458 | 100 % | – | 492/87 | grenze_ohne_bildkante, klasse_unsicher |
| 38 | 300038 | 1.2.5 Bahnkörper | nein | nein | 391 | 100 % | – | 516/94 | klasse_unsicher, nicht_zusammenhaengend |
| 33 | 300033 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 228 | 100 % | – | 537/80 | klasse_unsicher, nicht_zusammenhaengend |
| 8 | 300008 | 1.2.5 Bahnkörper | nein | nein | 128 | 100 % | – | 555/68 | klasse_unsicher, nicht_zusammenhaengend |
| 32 | 300032 | 1.2.1 Straße (versiegelt) | nein | nein | 51 | 100 % | – | 560/78 | klasse_unsicher, nicht_zusammenhaengend |
| 58 | 300058 | 2.1 Acker mit Bewuchs | nein | ja | 92 | 68 % | v1 | 317/149 | grenze_ohne_bildkante, klasse_unsicher |
| 39 | 300039 | 2.1 Acker mit Bewuchs | nein | ja | 3452 | 56 % | v1 | 329/106 | grenze_ohne_bildkante, klasse_unsicher |
| 44 | 300044 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 557 | 100 % | – | 369/112 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 42 | 300042 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 115 | 100 % | – | 387/107 | grenze_ohne_bildkante, klasse_unsicher |
| 49 | 300049 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 79 | 100 % | – | 406/117 | grenze_ohne_bildkante, klasse_unsicher |
| 46 | 300046 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 200 | 100 % | – | 412/112 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 51 | 300051 | 1.2.1 Straße (versiegelt) | nein | nein | 295 | 100 % | – | 423/122 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 45 | 300045 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 240 | 100 % | – | 427/108 | klasse_unsicher, nicht_zusammenhaengend |
| 55 | 300055 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 84 | 100 % | – | 434/145 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 57 | 300057 | 1.2.1 Straße (versiegelt) | nein | nein | 119 | 100 % | – | 436/138 | grenze_ohne_bildkante, klasse_unsicher |
| 52 | 300052 | 1.2.5 Bahnkörper | nein | nein | 176 | 100 % | – | 442/128 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 53 | 300053 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 97 | 100 % | – | 455/128 | klasse_unsicher |
| 50 | 300050 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 425 | 100 % | – | 472/121 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 54 | 300054 | 1.2.1 Straße (versiegelt) | nein | nein | 74 | 100 % | – | 488/135 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 35 | 300035 | 6.6 Weg, unbefestigt (Feld-, Wald-, Schotterweg) | nein | nein | 5763 | 67 % | v1, v3 | 511/112 | klasse_unsicher |
| 36 | 300036 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 208 | 100 % | – | 546/102 | klasse_unsicher, nicht_zusammenhaengend |
| 62 | 300062 | 1.2.4 Platz / Parkplatz / Hoffläche versiegelt | nein | nein | 214 | 100 % | – | 344/199 | klasse_unsicher, nicht_zusammenhaengend |
| 60 | 300060 | 1.2.2 Weg, befestigt (Asphalt, Pflaster) | nein | nein | 487 | 100 % | – | 400/198 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 79 | 300079 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 247 | 91 % | v1 | 328/244 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 75 | 300075 | 2.1 Acker mit Bewuchs | nein | ja | 102 | 100 % | – | 427/234 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 77 | 300077 | 1.2.1 Straße (versiegelt) | nein | nein | 116 | 100 % | – | 428/246 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 40 | 300040 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 21332 | 100 % | v4 | 496/210 | grenze_ohne_bildkante, klasse_unsicher |
| 83 | 300083 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 144 | 100 % | – | 438/256 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 61 | 300061 | 1.2.1 Straße (versiegelt) | nein | nein | 2968 | 65 % | v4 | 524/298 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 90 | 300090 | 2.1 Acker mit Bewuchs | nein | ja | 55 | 100 % | – | 560/274 | klasse_unsicher, nicht_zusammenhaengend |

`nicht_geprueft` nennt, was du nicht angesehen hast, `offen`, was du nicht entscheiden konntest.

Kontrolle vor der Rückgabe (muss mit `ok` enden):

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-2/skripte/pruefe_urteil.py --urteil C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c0/v2/urteil.json --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r1c0/segmente.json --fassung b --viertel v2 --ids 300030,300027,300031,300041,300023,300034,300006,300026,300038,300033,300008,300032,300058,300039,300044,300042,300049,300046,300051,300045,300055,300057,300052,300053,300050,300054,300035,300036,300062,300060,300079,300075,300077,300040,300083,300061,300090
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
Namen, die du benutzt hast, je mit Ebene, Eltern und einem Satz Bildmerkmal. Nach allen Teilkacheln
gleicht ein eigener Agent die Namen der 16 Viertel zu einer Liste an. Alle übrigen Regeln (L1, L2,
L4–L13) gelten wie in Fassung C; jeder Bildpunkt gehört genau einem Segment.

## Werkzeuge

Befehle im Ordner `C:/Users/Phil/Developement/Victor/landseg` mit `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -m landseg <befehl>`; Aufruf und Schalter stehen in
`C:/Users/Phil/Developement/Victor/landseg/README.md`. Die Bilder deines Viertels liegen fertig vor (Abschnitt „Dein Viertel“); `ansicht` (W3) erzeugt Bilder
je Segment und ist hier keine Urteilsgrundlage. Für fragliche Grenzen `kante` (W4, hier nur zum Ansehen
der Bildkante), zur Kontrolle `pruefen`. Eigene Skripte als Datei in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c0/v2`.

## Ergebnis in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c0/v2` (genau diese Namen)

- `roh.jpg`, `umriss.jpg` (alle Segmentgrenzen mit ID), `maengel.jpg` (nummerierte Punkte mit kurzer
  deutscher Beschriftung, sonst Vermerk „keine Mängel“), `vorschlag.jpg` (Grenzen und Klassen, wie
  du sie setzen würdest, sonst Vermerk „unverändert“): je dein Viertel mit Umgebung, Viertel
  umrandet (Grundlage: die vorbereiteten Übersichtsbilder).
- `nah_<n>.jpg`: eigene Nahansichten von Stellen, die man in den vorbereiteten Bildern nicht beurteilen kann,
  je ein Teil des Viertels samt Nachbarn (mindestens 64 × 64 Bildpunkte der Teilkachel, kein freigestelltes
  Einzelsegment); `kontrast_<n>.jpg` bei blassen Stellen.
- `urteil.json` (UTF-8):

```
{"teilkachel": "r1c0", "viertel": "v2", "bearbeiter": "urt-b-r1c0-v2",
 "bilder_angesehen": {"uebersicht": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r1c0/ganz_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c0/v2/uebersicht_nummern.jpg", "…"],
                      "nah": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c0/v2/nah1_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c0/v2/nah_1.jpg", "…"]},
 "segmente": [{"id": 17, "klasse_heute": "Code", "was_ist_es": "ein Satz",
               "urteil": "sauber" | "nicht_sauber", "klasse_vorschlag": null,
               "klasse_frei": {"grob": "Name", "mittel": "Name", "fein": "Name"},
               "sicher": true | false,
               "punkte": [{"nr": 1, "art": "fremdes|fehlt|trennen|verschmelzen|grenze|klasse|zu_klein|sonstiges",
                           "text": "ein Satz mit Stelle (x/y im Teilkachelbild)", "flaeche_px": Zahl oder null}],
               "bilder": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c0/v2/uebersicht_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r1c0/v2/nah2_roh.jpg"]}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "was an der Kerngrenze nicht passt"}],
 "unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."],
 "klassen_frei": [{"name": "Name", "ebene": "grob|mittel|fein", "eltern": "Name oder null", "merkmal": "woran im Bild erkennbar"}]}
```

Jedes Segment deiner Liste steht genau einmal unter `segmente`, auch die sauberen, in der Reihenfolge der Liste. Segmente der Nachbarviertel (graue Nummern) und des Kontextrands (ohne Nummer) urteilst du in diesem Auftrag nicht; Auffälliges an ihnen nennst du unter `unsicher` mit ID.

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Punkte, Anteil `sicher: false`, wo du unsicher bist.
