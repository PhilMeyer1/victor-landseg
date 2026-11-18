# Auftrag: H0, Teilkachel r0c0, Viertel v1: 58 Segmente im Verbund ansehen und einzeln urteilen (Fassung C „Feste Kategorienliste“)

Lies zuerst den Skill `landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `r0c0` des Ausschnitts in `C:/Users/Phil/Developement/Victor/daten/landseg/H0`. Du urteilst über jedes
Segment deines Viertels v1 (Liste unter „Dein Viertel“), ob Grenze und Klasse stimmen, und zeichnest ein, was
du ändern würdest. Die Label-Karte änderst du nur nach dem Abschnitt „Nachsegmentieren“
(grob zusammengefasste Segmente teilen, bevor du sie urteilst).

## Daten (nur lesen; Ausnahme: Karte und `segmente.json` aus „Karte zum Nachsegmentieren“, nur über `eingriff` und `kante`)

- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/manifest.json`: Eintrag `r0c0` unter `teilkacheln` mit `bild` (Teilkachelbild,
  Kern + Kontextrand), `kern_im_bild` (Lage des Kerns im Teilkachelbild) und `kern` (Lage im Ausschnitt).
- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/labels.tif`: Label-Karte (Segment-ID je Bildpunkt, Größe des Teilkachelbilds).
- `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/segmente.json`: je Segment `id`, `klasse`, `grob`, `herkunft`, `sicher`; dazu die
  Kandidatenliste der Vorstufe, falls vorhanden.
- `C:/Users/Phil/Developement/Victor/landseg/kategorien.json` und `C:/Users/Phil/Developement/Victor/landseg/KATEGORIEN.md`: die gültigen Klassen und Regeln.

## Zuerst der ganze Ausschnitt, dann die Teilkachel

Bevor du dein Viertel ansiehst: zuerst den ganzen Ausschnitt H0 (`C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png`, mit Teilkachelgitter
`C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/H0_raster.jpg`; r0c0 oben links, r0c1 oben rechts, r1c0 unten links, r1c1 unten rechts),
dann die ganze Teilkachel `r0c0` (`C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r0c0/ganz_nummern.jpg`: Grenzen, Nummern, Viertel cyan v1–v4;
`C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r0c0/ganz_roh.jpg` unverändert; beide 2fach). Beide stehen in `bilder_angesehen.uebersicht` vor den Viertelbildern.

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

Viertel v1 (oben links) des Kerns von `r0c0`: x 64–313, y 64–313 im
Teilkachelbild (250 × 250 Bildpunkte). Dir gehören die 58 Segmente der Liste unten: Jedes hat den
größten Teil seiner Kernfläche in diesem Viertel. Die Teilkachel hat 173 Kernsegmente
(v1 58, v2 67, v3 14, v4 34); die anderen Viertel stehen in eigenen Aufträgen mit eigenem Ergebnisordner. Ein Segment
über einer Viertelgrenze urteilt nur das Viertel mit dem größten Anteil; in den Bildern der Nachbarn ist
es mit grauer Nummer als Umgebung zu sehen.

Urteil im Verbund: Du siehst das Viertel als zusammenhängendes Bild mit Umgebung, arbeitest die Liste der
Reihe nach ab und beurteilst jedes Segment im Zusammenhang mit seinen Nachbarn; eingetragen wird jedes
Segment einzeln (Klasse, `sicher`, `was_ist_es` als Notiz). Bilder freigestellter Einzelsegmente gibt es
nicht, und sie sind keine Urteilsgrundlage.

Bilder des Viertels (fertig, JPEG, in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c0/v1`, Fenster und Vergrößerung je Bild in `viertel.json`):

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
Teilkachelbild; Kandidaten aus `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/kandidaten.json`, dort mit Grund, in den
Bildern nicht eingezeichnet; Anteil hier = Anteil der Kernfläche in diesem Viertel):

| Nr | ID | Klasse Vorstufe | sicher | im Siedlungsgebiet | Kernfläche px | Anteil hier | auch in | Punkt x/y | Kandidaten |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 100001 | 2.1 Acker mit Bewuchs | ja | nein | 1806 | 100 % | – | 78/78 | grenze_ohne_bildkante |
| 58 | 100058 | 3.1 Wiese / Weide (gemeinsam) | ja | ja | 179 | 100 % | – | 97/88 | grenze_ohne_bildkante |
| 52 | 100052 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | ja | ja | 256 | 100 % | – | 104/77 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 57 | 100057 | 1.2.1 Straße (versiegelt) | nein | nein | 181 | 100 % | – | 117/92 | klasse_unsicher |
| 47 | 100047 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 505 | 100 % | – | 118/73 | grenze_ohne_bildkante, klasse_unsicher |
| 25 | 100025 | 1.2.1 Straße (versiegelt) | nein | nein | 10 | 100 % | – | 139/64 | klasse_unsicher |
| 61 | 100061 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 269 | 100 % | – | 151/95 | – |
| 33 | 100033 | 1.2.1 Straße (versiegelt) | nein | nein | 640 | 100 % | – | 153/80 | grenze_ohne_bildkante, klasse_unsicher |
| 43 | 100043 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 564 | 100 % | – | 202/76 | grenze_ohne_bildkante |
| 35 | 100035 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 2247 | 100 % | – | 251/95 | grenze_ohne_bildkante, klasse_unsicher |
| 17 | 100017 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 598 | 100 % | – | 270/76 | grenze_ohne_bildkante, klasse_unsicher |
| 34 | 100034 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 267 | 100 % | – | 284/69 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 48 | 100048 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1420 | 76 % | v2 | 287/86 | grenze_ohne_bildkante, klasse_unsicher |
| 7 | 100007 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1 | 100 % | – | 309/64 | grenze_ohne_bildkante, klasse_unsicher |
| 10 | 100010 | 1.3.2 Baustelle | nein | nein | 166 | 59 % | v2 | 310/68 | grenze_ohne_bildkante, klasse_unsicher |
| 90 | 100090 | 1.3.4 Sport-, Spielplatz (künstlicher Belag) | ja | nein | 129 | 100 % | – | 68/139 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 97 | 100097 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 60 | 100 % | – | 70/149 | grenze_ohne_bildkante, klasse_unsicher |
| 85 | 100085 | 1.2.1 Straße (versiegelt) | nein | nein | 145 | 100 % | – | 74/145 | grenze_ohne_bildkante, klasse_unsicher |
| 68 | 100068 | 1.3.4 Sport-, Spielplatz (künstlicher Belag) | ja | nein | 306 | 100 % | – | 87/105 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 74 | 100074 | 2.1 Acker mit Bewuchs | nein | ja | 187 | 100 % | – | 88/124 | grenze_ohne_bildkante, klasse_unsicher |
| 67 | 100067 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 231 | 100 % | – | 100/101 | grenze_ohne_bildkante, klasse_unsicher |
| 88 | 100088 | 1.2.1 Straße (versiegelt) | nein | nein | 358 | 100 % | – | 103/145 | grenze_ohne_bildkante, klasse_unsicher |
| 4 | 100004 | 6.6 Weg, unbefestigt (Feld-, Wald-, Schotterweg) | nein | nein | 2061 | 100 % | – | 112/120 | grenze_ohne_bildkante, klasse_unsicher |
| 91 | 100091 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 101 | 100 % | – | 113/147 | grenze_ohne_bildkante, klasse_unsicher |
| 93 | 100093 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 957 | 100 % | – | 125/149 | grenze_ohne_bildkante, klasse_unsicher |
| 72 | 100072 | 1.2.1 Straße (versiegelt) | ja | nein | 115 | 100 % | – | 128/112 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 78 | 100078 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 550 | 100 % | – | 132/130 | grenze_ohne_bildkante, klasse_unsicher |
| 65 | 100065 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 778 | 100 % | – | 166/112 | klasse_unsicher |
| 76 | 100076 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1645 | 100 % | – | 205/147 | klasse_unsicher |
| 51 | 100051 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 3180 | 100 % | – | 210/107 | grenze_ohne_bildkante, klasse_unsicher |
| 80 | 100080 | 2.1 Acker mit Bewuchs | nein | ja | 182 | 100 % | – | 279/127 | grenze_ohne_bildkante, klasse_unsicher |
| 64 | 100064 | 1.3.2 Baustelle | nein | nein | 1590 | 96 % | v2 | 297/104 | grenze_ohne_bildkante, klasse_unsicher |
| 108 | 100108 | 1.2.1 Straße (versiegelt) | ja | nein | 242 | 100 % | – | 79/173 | grenze_ohne_bildkante |
| 98 | 100098 | 1.2.1 Straße (versiegelt) | ja | nein | 181 | 100 % | – | 90/158 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 99 | 100099 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1398 | 100 % | – | 103/171 | grenze_ohne_bildkante, klasse_unsicher |
| 105 | 100105 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1361 | 100 % | – | 149/189 | klasse_unsicher |
| 75 | 100075 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 3389 | 100 % | – | 165/153 | – |
| 106 | 100106 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 703 | 100 % | – | 191/180 | klasse_unsicher, nicht_zusammenhaengend |
| 113 | 100113 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 164 | 100 % | – | 205/191 | klasse_unsicher, nicht_zusammenhaengend |
| 77 | 100077 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | nein | ja | 5212 | 90 % | v2 | 276/163 | grenze_ohne_bildkante, klasse_unsicher |
| 122 | 100122 | 1.3.2 Baustelle | nein | nein | 114 | 100 % | – | 282/199 | grenze_ohne_bildkante, klasse_unsicher |
| 103 | 100103 | 1.3.2 Baustelle | nein | nein | 369 | 100 % | – | 304/163 | grenze_ohne_bildkante, klasse_unsicher |
| 115 | 100115 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 231 | 100 % | – | 304/194 | klasse_unsicher |
| 124 | 100124 | 1.2.1 Straße (versiegelt) | nein | nein | 18 | 100 % | – | 65/202 | klasse_unsicher |
| 136 | 100136 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 356 | 100 % | – | 71/232 | klasse_unsicher |
| 116 | 100116 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 754 | 100 % | – | 79/200 | klasse_unsicher |
| 147 | 100147 | 1.3.2 Baustelle | nein | nein | 160 | 100 % | – | 79/246 | grenze_ohne_bildkante, klasse_unsicher |
| 121 | 100121 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 1925 | 100 % | – | 139/225 | klasse_unsicher |
| 132 | 100132 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 700 | 100 % | – | 164/238 | grenze_ohne_bildkante |
| 120 | 100120 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 774 | 100 % | – | 177/204 | grenze_ohne_bildkante, klasse_unsicher |
| 134 | 100134 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 1584 | 100 % | – | 273/233 | grenze_ohne_bildkante, klasse_unsicher |
| 129 | 100129 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 2521 | 100 % | – | 80/270 | grenze_ohne_bildkante, klasse_unsicher |
| 138 | 100138 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 1658 | 100 % | – | 120/252 | klasse_unsicher |
| 114 | 100114 | 1.3.2 Baustelle | nein | nein | 12938 | 79 % | v3 | 202/254 | grenze_ohne_bildkante, klasse_unsicher |
| 163 | 100163 | 2.1 Acker mit Bewuchs | nein | ja | 165 | 99 % | v2 | 306/279 | grenze_ohne_bildkante, klasse_unsicher |
| 160 | 100160 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1502 | 51 % | v3 | 74/302 | grenze_ohne_bildkante, klasse_unsicher |
| 171 | 100171 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 170 | 100 % | – | 103/302 | grenze_ohne_bildkante, klasse_unsicher |
| 168 | 100168 | 3.1 Wiese / Weide (gemeinsam) | nein | nein | 518 | 100 % | – | 190/303 | grenze_ohne_bildkante, klasse_unsicher |

`nicht_geprueft` nennt, was du nicht angesehen hast, `offen`, was du nicht entscheiden konntest.

Kontrolle vor der Rückgabe (muss mit `ok` enden):

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/skripte/pruefe_urteil.py --urteil C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil-gegenprobe/r0c0/v1/urteil.json --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/segmente.json --fassung c --viertel v1 --ids 100001,100058,100052,100057,100047,100025,100061,100033,100043,100035,100017,100034,100048,100007,100010,100090,100097,100085,100068,100074,100067,100088,100004,100091,100093,100072,100078,100065,100076,100051,100080,100064,100108,100098,100099,100105,100075,100106,100113,100077,100122,100103,100115,100124,100136,100116,100147,100121,100132,100120,100134,100129,100138,100114,100163,100160,100171,100168 --kategorien C:/Users/Phil/Developement/Victor/landseg/kategorien.json
```

## Nachsegmentieren (Entscheidung des Nutzers 2026-11-18)
Die Vorstufe ist bewusst grob. Fasst ein Segment sichtbar mehrere Objekte zusammen (Häuserzeile, Hof mit Garten, Acker mit Weg oder Rain, Baumgruppe mit Wiese), teilst du es selbst, BEVOR du es urteilst — direkt, ohne Umweg:
- Alle Eingriffe eines Viertels in EINEM Stapel: `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg eingriff --labels <Karte> --segmente <segmente.json> --bearbeiter <dein Name> stapel --datei <ergebnisordner>/eingriffe.json` mit Schritten `teilen` (Linienzug entlang der sichtbaren Bildkante), `polygon` (Fläche an Nachbarn oder neues Segment mit Klasse) oder `verschmelzen` (eine Fläche, zwei Stücke ohne Kante). Koordinaten in Bildpunkten der Teilkachel.
- Sitzt eine Linie nicht genau auf der Kante: `kante` (README) zum Einrasten. Danach `pruefen` — die Karte muss lückenlos bleiben.
- Neue IDs aus dem Stapel-Ergebnis urteilst du im selben urteil.json; jede Teilung steht dort unter "eingriffe" mit IDs vorher/nachher und Grund in einem Satz.
- Nur teilen, wo Objekte im Bild klar getrennt sind; kein Feinschliff an brauchbaren Grenzen, keine Teilung nach Vermutung. Unklare Mischflächen: nicht teilen, `sicher: false`, Notiz unter "offen".
- Zur Kontrolle eine Nahansicht der geänderten Stelle (`ansicht` oder eigenes Bild aus Karte und Teilkachelbild) einmal ansehen.

Karte zum Nachsegmentieren: `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/labels.tif` und `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/segmente.json`

So konkret (Befehle im Ordner `C:/Users/Phil/Developement/Victor/landseg`, dein Name `gegen-c-r0c0-v1`, Teilkachelbild `C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r0c0.png`):

- Stapeldatei `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil-gegenprobe/r0c0/v1/eingriffe.json`: `{"schritte": [{"op": "teilen", "id": 4, "linie": [[x, y], [x, y]]},
  {"op": "polygon_zuweisen", "flaeche": [[x, y], [x, y], [x, y]], "id": 7}, {"op": "polygon_zuweisen",
  "flaeche": [[x, y], …], "klasse": "Code"}, {"op": "verschmelzen", "ids": [3, 5]}]}` (im Stapel heißt
  `polygon` `polygon_zuweisen`; `klasse` braucht einen Code aus `kategorien.json`). Alles oder nichts: Schlägt ein Schritt fehl, bleibt die
  Karte unverändert; Datei korrigieren und erneut ausführen. Das Ergebnis nennt je Schritt `behalten`/`neu`
  bzw. `aufgeteilt_neu`; beim Teilen behält das größte Stück die ID.
- `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg eingriff --labels C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/labels.tif --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/segmente.json --bearbeiter gegen-c-r0c0-v1 stapel --datei C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil-gegenprobe/r0c0/v1/eingriffe.json`
- Einrasten: `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg kante --labels C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/labels.tif --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/segmente.json --bild C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r0c0.png --bearbeiter gegen-c-r0c0-v1 --a <ID> --b <ID>`
- Kontrolle: `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg pruefen --labels C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/labels.tif --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/segmente.json --bild C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r0c0.png` (muss mit `ok` enden).
- Nahansicht: `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg ansicht --manifest C:/Users/Phil/Developement/Victor/daten/landseg/H0/manifest.json --teilkachel r0c0 --labels C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/labels.tif --segmente C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/segmente.json --ziel C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil-gegenprobe/r0c0/v1/ansicht --ids <neue IDs>`
- Schreibe nur im Kern deines Viertels und nur an Segmenten deiner Liste (L2); Segmente der Nachbarviertel teilst du nicht.
- In `urteil.json`: `"eingriffe": [{"schritt": "teilen|polygon_zuweisen|verschmelzen", "vorher": [IDs], "nachher": [IDs],
  "grund": "ein Satz"}]`; ohne Eingriff `"eingriffe": []`. Jede ID aus `nachher`, die noch auf der Karte steht und im
  Kern liegt, steht unter `segmente`; eine ID deiner Liste, die durch Verschmelzen verschwand, nur unter `vorher`.

## Unabhängig urteilen

Du bist die Gegenprobe: Ein anderer Agent urteilt über dasselbe Viertel. Sein Ergebnis (`C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil/`) und seine Karte (`C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r0c0/`) siehst du nicht an, auch nicht, wenn sie schon da sind. Du teilst nur auf deiner eigenen Kopie (`C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/gegenprobe/r0c0/`). Aus beiden Urteilen wird die Übereinstimmung gemessen.

## Werkzeuge

Befehle im Ordner `C:/Users/Phil/Developement/Victor/landseg` mit `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -m landseg <befehl>`; Aufruf und Schalter stehen in
`C:/Users/Phil/Developement/Victor/landseg/README.md`. Die Bilder deines Viertels liegen fertig vor (Abschnitt „Dein Viertel“); `ansicht` (W3) erzeugt Bilder
je Segment und ist hier keine Urteilsgrundlage. Für fragliche Grenzen `kante` (W4: ansehen; einrasten
nur an Linien aus deinem Nachsegmentieren), zur Kontrolle `pruefen`. Eigene Skripte als Datei in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil-gegenprobe/r0c0/v1`.

## Ergebnis in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil-gegenprobe/r0c0/v1` (genau diese Namen)

- `roh.jpg`, `umriss.jpg` (alle Segmentgrenzen mit ID), `maengel.jpg` (nummerierte Punkte mit kurzer
  deutscher Beschriftung, sonst Vermerk „keine Mängel“), `vorschlag.jpg` (Grenzen und Klassen, wie
  du sie setzen würdest, sonst Vermerk „unverändert“): je dein Viertel mit Umgebung, Viertel
  umrandet (Grundlage: die vorbereiteten Übersichtsbilder).
- `nah_<n>.jpg`: eigene Nahansichten von Stellen, die man in den vorbereiteten Bildern nicht beurteilen kann,
  je ein Teil des Viertels samt Nachbarn (mindestens 64 × 64 Bildpunkte der Teilkachel, kein freigestelltes
  Einzelsegment); `kontrast_<n>.jpg` bei blassen Stellen.
- `urteil.json` (UTF-8):

```
{"teilkachel": "r0c0", "viertel": "v1", "bearbeiter": "gegen-c-r0c0-v1",
 "bilder_angesehen": {"uebersicht": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/H0.png", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/ganz/r0c0/ganz_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c0/v1/uebersicht_nummern.jpg", "…"],
                      "nah": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c0/v1/nah1_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/urteil-gegenprobe/r0c0/v1/nah_1.jpg", "…"]},
 "segmente": [{"id": 17, "klasse_heute": "Code", "was_ist_es": "ein Satz",
               "urteil": "sauber" | "nicht_sauber", "klasse_vorschlag": "Code oder null",
               "sicher": true | false,
               "punkte": [{"nr": 1, "art": "fremdes|fehlt|trennen|verschmelzen|grenze|klasse|zu_klein|sonstiges",
                           "text": "ein Satz mit Stelle (x/y im Teilkachelbild)", "flaeche_px": Zahl oder null}],
               "bilder": ["C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c0/v1/uebersicht_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/r0c0/v1/nah2_roh.jpg"]}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "was an der Kerngrenze nicht passt"}],
 "unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."],
 "eingriffe": [{"schritt": "teilen", "vorher": [ID], "nachher": [ID, ID], "grund": "ein Satz"}]}
```

Jedes Segment deiner Liste steht genau einmal unter `segmente`, auch die sauberen, in der Reihenfolge der Liste. Segmente der Nachbarviertel (graue Nummern) und des Kontextrands (ohne Nummer) urteilst du in diesem Auftrag nicht; Auffälliges an ihnen nennst du unter `unsicher` mit ID.

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Punkte, Anteil `sicher: false`, wo du unsicher bist.
