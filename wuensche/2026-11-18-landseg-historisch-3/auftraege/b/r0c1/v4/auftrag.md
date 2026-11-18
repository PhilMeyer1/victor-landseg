# Auftrag: H0, Teilkachel r0c1, Viertel v4: 28 Segmente im Verbund ansehen und einzeln urteilen (Fassung B „Kategorien frei“)

Lies zuerst den Skill `landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `r0c1` des Ausschnitts in `C:/Users/Phil/Developement/Victor/daten/landseg/H0`. Du urteilst über jedes
Segment deines Viertels v4 (Liste unter „Dein Viertel“), ob Grenze und Klasse stimmen, und zeichnest ein, was
du ändern würdest. Die Label-Karte änderst du nur nach dem Abschnitt „Nachsegmentieren“
(grob zusammengefasste Segmente teilen, bevor du sie urteilst).

## Daten (nur lesen; Ausnahme: Karte und `segmente.json` aus „Karte zum Nachsegmentieren“, nur über `eingriff` und `kante`)

- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/manifest.json`: Eintrag `r0c1` unter `teilkacheln` mit `bild` (Teilkachelbild,
  Kern + Kontextrand), `kern_im_bild` (Lage des Kerns im Teilkachelbild) und `kern` (Lage im Ausschnitt).
- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r0c1/labels.tif`: Label-Karte (Segment-ID je Bildpunkt, Größe des Teilkachelbilds).
- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r0c1/segmente.json`: je Segment `id`, `klasse`, `grob`, `herkunft`, `sicher`; dazu die
  Kandidatenliste der Vorstufe, falls vorhanden.
- `C:/Users/Phil/Developement/Victor/landseg/kategorien.json` und `C:/Users/Phil/Developement/Victor/landseg/KATEGORIEN.md`: nur Anregung; in Fassung B benennst du die Klassen selbst (Abschnitt „Fassung B“).

## Zuerst der ganze Ausschnitt, dann die Teilkachel

Bevor du dein Viertel ansiehst: zuerst den ganzen Ausschnitt H0 (`C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png`, mit Teilkachelgitter
`C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/H0_raster.jpg`; r0c0 oben links, r0c1 oben rechts, r1c0 unten links, r1c1 unten rechts),
dann die ganze Teilkachel `r0c1` (`C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r0c1/ganz_nummern.jpg`: Grenzen, Nummern, Viertel cyan v1–v4;
`C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r0c1/ganz_roh.jpg` unverändert; beide 2fach). Beide stehen in `bilder_angesehen.uebersicht` vor den Viertelbildern.

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
- Die Klassen der Vorstufe sind auf dem Scan schwach (SAM 3 ist für Farb-Orthofotos gebaut; drei
  Viertel bis neun Zehntel `sicher: nein`, Äcker teils als Gebäude): nur Hinweis.
- Die Vorstufe ist bewusst grob: Sie lief mit den Einstellungen des Repos, nur die Bildpunktgröße auf
  0,45 m gesetzt (`C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/vorstufe-h0-grob.json`). Häuserzeilen, Höfe mit Garten oder Äcker mit Weg können darum
  in einem Segment stecken.

## Dein Viertel

Viertel v4 (unten rechts) des Kerns von `r0c1`: x 314–563, y 314–563 im
Teilkachelbild (250 × 250 Bildpunkte). Dir gehören die 28 Segmente der Liste unten: Jedes hat den
größten Teil seiner Kernfläche in diesem Viertel. Die Teilkachel hat 92 Kernsegmente
(v1 16, v2 23, v3 25, v4 28); die anderen Viertel stehen in eigenen Aufträgen mit eigenem Ergebnisordner. Ein Segment
über einer Viertelgrenze urteilt nur das Viertel mit dem größten Anteil; in den Bildern der Nachbarn ist
es mit grauer Nummer als Umgebung zu sehen.

Urteil im Verbund: Du siehst das Viertel als zusammenhängendes Bild mit Umgebung, arbeitest die Liste der
Reihe nach ab und beurteilst jedes Segment im Zusammenhang mit seinen Nachbarn; eingetragen wird jedes
Segment einzeln (Klasse, `sicher`, `was_ist_es` als Notiz). Bilder freigestellter Einzelsegmente gibt es
nicht, und sie sind keine Urteilsgrundlage.

Bilder des Viertels (fertig, JPEG, in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c1/v4`, Fenster und Vergrößerung je Bild in `viertel.json`):

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
Teilkachelbild; Kandidaten aus `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r0c1/kandidaten.json`, dort mit Grund, in den
Bildern nicht eingezeichnet; Anteil hier = Anteil der Kernfläche in diesem Viertel):

| Nr | ID | Klasse Vorstufe | sicher | im Siedlungsgebiet | Kernfläche px | Anteil hier | auch in | Punkt x/y | Kandidaten |
|---|---|---|---|---|---|---|---|---|---|
| 69 | 200069 | 1.2.1 Straße (versiegelt) | nein | nein | 572 | 74 % | v2 | 488/328 | grenze_ohne_bildkante, klasse_unsicher |
| 71 | 200071 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 5459 | 78 % | v3 | 339/379 | klasse_unsicher |
| 51 | 200051 | 1.2.1 Straße (versiegelt) | nein | nein | 7641 | 74 % | v2, v3 | 388/397 | grenze_ohne_bildkante, klasse_unsicher |
| 79 | 200079 | 1.2.1 Straße (versiegelt) | nein | nein | 593 | 100 % | – | 429/387 | grenze_ohne_bildkante, klasse_unsicher |
| 76 | 200076 | 1.2.1 Straße (versiegelt) | nein | nein | 221 | 100 % | – | 452/366 | grenze_ohne_bildkante, klasse_unsicher |
| 77 | 200077 | 1.3.2 Baustelle | nein | nein | 199 | 100 % | – | 454/385 | grenze_ohne_bildkante, klasse_unsicher |
| 75 | 200075 | 1.3.2 Baustelle | nein | nein | 91 | 100 % | – | 463/362 | grenze_ohne_bildkante, klasse_unsicher |
| 82 | 200082 | 1.2.1 Straße (versiegelt) | ja | nein | 583 | 67 % | v3 | 321/433 | – |
| 83 | 200083 | 1.2.1 Straße (versiegelt) | nein | nein | 160 | 100 % | – | 375/424 | klasse_unsicher |
| 80 | 200080 | 1.3.2 Baustelle | nein | nein | 112 | 100 % | – | 387/418 | klasse_unsicher |
| 98 | 200098 | 1.2.1 Straße (versiegelt) | nein | nein | 149 | 50 % | v3 | 316/498 | klasse_unsicher |
| 95 | 200095 | 1.2.1 Straße (versiegelt) | nein | nein | 2353 | 100 % | v3 | 336/483 | grenze_ohne_bildkante, klasse_unsicher |
| 91 | 200091 | 1.3.2 Baustelle | nein | nein | 127 | 100 % | – | 341/463 | klasse_unsicher |
| 63 | 200063 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 36113 | 98 % | v2 | 471/462 | grenze_ohne_bildkante, klasse_unsicher |
| 97 | 200097 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 3049 | 94 % | v3 | 333/527 | grenze_ohne_bildkante, klasse_unsicher |
| 116 | 200116 | 1.3.2 Baustelle | nein | nein | 86 | 100 % | – | 348/546 | klasse_unsicher |
| 109 | 200109 | 1.2.1 Straße (versiegelt) | nein | nein | 144 | 100 % | – | 358/536 | grenze_ohne_bildkante, klasse_unsicher |
| 114 | 200114 | 1.3.2 Baustelle | nein | nein | 239 | 100 % | – | 465/542 | klasse_unsicher |
| 108 | 200108 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 659 | 100 % | – | 508/545 | klasse_unsicher |
| 105 | 200105 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 728 | 100 % | – | 533/525 | klasse_unsicher |
| 107 | 200107 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 289 | 100 % | – | 553/530 | klasse_unsicher |
| 122 | 200122 | 1.3.2 Baustelle | nein | nein | 95 | 99 % | v3 | 322/560 | klasse_unsicher |
| 112 | 200112 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 647 | 100 % | – | 443/554 | grenze_ohne_bildkante, klasse_unsicher |
| 111 | 200111 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 714 | 100 % | – | 484/553 | klasse_unsicher |
| 124 | 200124 | 1.3.2 Baustelle | nein | nein | 74 | 100 % | – | 518/560 | klasse_unsicher |
| 123 | 200123 | 1.3.2 Baustelle | nein | nein | 94 | 100 % | – | 535/556 | klasse_unsicher |
| 110 | 200110 | 1.2.1 Straße (versiegelt) | nein | nein | 332 | 100 % | – | 559/559 | klasse_unsicher |
| 125 | 200125 | 1.3.2 Baustelle | nein | nein | 2 | 100 % | – | 562/563 | grenze_ohne_bildkante, klasse_unsicher |

`nicht_geprueft` nennt, was du nicht angesehen hast, `offen`, was du nicht entscheiden konntest.

Kontrolle vor der Rückgabe (muss mit `ok` enden):

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/skripte/pruefe_urteil.py --urteil C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r0c1/v4/urteil.json --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r0c1/segmente.json --fassung b --viertel v4 --ids 200069,200071,200051,200079,200076,200077,200075,200082,200083,200080,200098,200095,200091,200063,200097,200116,200109,200114,200108,200105,200107,200122,200112,200111,200124,200123,200110,200125
```

## Nachsegmentieren (Entscheidung des Nutzers 2026-11-18)
Die Vorstufe ist bewusst grob. Fasst ein Segment sichtbar mehrere Objekte zusammen (Häuserzeile, Hof mit Garten, Acker mit Weg oder Rain, Baumgruppe mit Wiese), teilst du es selbst, BEVOR du es urteilst — direkt, ohne Umweg:
- Alle Eingriffe eines Viertels in EINEM Stapel: `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg eingriff --labels <Karte> --segmente <segmente.json> --bearbeiter <dein Name> stapel --datei <ergebnisordner>/eingriffe.json` mit Schritten `teilen` (Linienzug entlang der sichtbaren Bildkante), `polygon` (Fläche an Nachbarn oder neues Segment mit Klasse) oder `verschmelzen` (eine Fläche, zwei Stücke ohne Kante). Koordinaten in Bildpunkten der Teilkachel.
- Sitzt eine Linie nicht genau auf der Kante: `kante` (README) zum Einrasten. Danach `pruefen` — die Karte muss lückenlos bleiben.
- Neue IDs aus dem Stapel-Ergebnis urteilst du im selben urteil.json; jede Teilung steht dort unter "eingriffe" mit IDs vorher/nachher und Grund in einem Satz.
- Nur teilen, wo Objekte im Bild klar getrennt sind; kein Feinschliff an brauchbaren Grenzen, keine Teilung nach Vermutung. Unklare Mischflächen: nicht teilen, `sicher: false`, Notiz unter "offen".
- Zur Kontrolle eine Nahansicht der geänderten Stelle (`ansicht` oder eigenes Bild aus Karte und Teilkachelbild) einmal ansehen.

Karte zum Nachsegmentieren: `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r0c1/labels.tif` und `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r0c1/segmente.json`

So konkret (Befehle im Ordner `C:/Users/Phil/Developement/Victor/landseg`, dein Name `urt-b-r0c1-v4`, Teilkachelbild `C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r0c1.png`):

- Stapeldatei `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r0c1/v4/eingriffe.json`: `{"schritte": [{"op": "teilen", "id": 4, "linie": [[x, y], [x, y]]},
  {"op": "polygon_zuweisen", "flaeche": [[x, y], [x, y], [x, y]], "id": 7}, {"op": "polygon_zuweisen",
  "flaeche": [[x, y], …], "klasse": "Code"}, {"op": "verschmelzen", "ids": [3, 5]}]}` (im Stapel heißt
  `polygon` `polygon_zuweisen`; `klasse` braucht einen Code aus `kategorien.json` (technisch nötig; nimm den Code des geteilten Segments, deine freie Klasse steht im Urteil)). Alles oder nichts: Schlägt ein Schritt fehl, bleibt die
  Karte unverändert; Datei korrigieren und erneut ausführen. Das Ergebnis nennt je Schritt `behalten`/`neu`
  bzw. `aufgeteilt_neu`; beim Teilen behält das größte Stück die ID.
- `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg eingriff --labels C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r0c1/labels.tif --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r0c1/segmente.json --bearbeiter urt-b-r0c1-v4 stapel --datei C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r0c1/v4/eingriffe.json`
- Einrasten: `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg kante --labels C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r0c1/labels.tif --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r0c1/segmente.json --bild C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r0c1.png --bearbeiter urt-b-r0c1-v4 --a <ID> --b <ID>`
- Kontrolle: `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg pruefen --labels C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r0c1/labels.tif --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r0c1/segmente.json --bild C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r0c1.png` (muss mit `ok` enden).
- Nahansicht: `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg ansicht --manifest C:/Users/Phil/Developement/Victor/daten/landseg/H0/manifest.json --teilkachel r0c1 --labels C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r0c1/labels.tif --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r0c1/segmente.json --ziel C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r0c1/v4/ansicht --ids <neue IDs>`
- Schreibe nur im Kern deines Viertels und nur an Segmenten deiner Liste (L2); Segmente der Nachbarviertel teilst du nicht.
- In `urteil.json`: `"eingriffe": [{"schritt": "teilen|polygon_zuweisen|verschmelzen", "vorher": [IDs], "nachher": [IDs],
  "grund": "ein Satz"}]`; ohne Eingriff `"eingriffe": []`. Jede ID aus `nachher`, die noch auf der Karte steht und im
  Kern liegt, steht unter `segmente`; eine ID deiner Liste, die durch Verschmelzen verschwand, nur unter `vorher`.

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
je Segment und ist hier keine Urteilsgrundlage. Für fragliche Grenzen `kante` (W4: ansehen; einrasten
nur an Linien aus deinem Nachsegmentieren), zur Kontrolle `pruefen`. Eigene Skripte als Datei in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r0c1/v4`.

## Ergebnis in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r0c1/v4` (genau diese Namen)

- `roh.jpg`, `umriss.jpg` (alle Segmentgrenzen mit ID), `maengel.jpg` (nummerierte Punkte mit kurzer
  deutscher Beschriftung, sonst Vermerk „keine Mängel“), `vorschlag.jpg` (Grenzen und Klassen, wie
  du sie setzen würdest, sonst Vermerk „unverändert“): je dein Viertel mit Umgebung, Viertel
  umrandet (Grundlage: die vorbereiteten Übersichtsbilder).
- `nah_<n>.jpg`: eigene Nahansichten von Stellen, die man in den vorbereiteten Bildern nicht beurteilen kann,
  je ein Teil des Viertels samt Nachbarn (mindestens 64 × 64 Bildpunkte der Teilkachel, kein freigestelltes
  Einzelsegment); `kontrast_<n>.jpg` bei blassen Stellen.
- `urteil.json` (UTF-8):

```
{"teilkachel": "r0c1", "viertel": "v4", "bearbeiter": "urt-b-r0c1-v4",
 "bilder_angesehen": {"uebersicht": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r0c1/ganz_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c1/v4/uebersicht_nummern.jpg", "…"],
                      "nah": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c1/v4/nah1_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r0c1/v4/nah_1.jpg", "…"]},
 "segmente": [{"id": 17, "klasse_heute": "Code", "was_ist_es": "ein Satz",
               "urteil": "sauber" | "nicht_sauber", "klasse_vorschlag": null,
               "klasse_frei": {"grob": "Name", "mittel": "Name", "fein": "Name"},
               "sicher": true | false,
               "punkte": [{"nr": 1, "art": "fremdes|fehlt|trennen|verschmelzen|grenze|klasse|zu_klein|sonstiges",
                           "text": "ein Satz mit Stelle (x/y im Teilkachelbild)", "flaeche_px": Zahl oder null}],
               "bilder": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c1/v4/uebersicht_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c1/v4/nah2_roh.jpg"]}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "was an der Kerngrenze nicht passt"}],
 "unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."],
 "eingriffe": [{"schritt": "teilen", "vorher": [ID], "nachher": [ID, ID], "grund": "ein Satz"}],
 "klassen_frei": [{"name": "Name", "ebene": "grob|mittel|fein", "eltern": "Name oder null", "merkmal": "woran im Bild erkennbar"}]}
```

Jedes Segment deiner Liste steht genau einmal unter `segmente`, auch die sauberen, in der Reihenfolge der Liste. Segmente der Nachbarviertel (graue Nummern) und des Kontextrands (ohne Nummer) urteilst du in diesem Auftrag nicht; Auffälliges an ihnen nennst du unter `unsicher` mit ID.

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Punkte, Anteil `sicher: false`, wo du unsicher bist.
