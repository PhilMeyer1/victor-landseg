# Auftrag: Teilkachel r1c1, Viertel v1: 44 Segmente im Verbund ansehen und einzeln urteilen (Fassung B: Kategorien frei)

Lies zuerst den Skill `landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `r1c1` des Ausschnitts in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b`. Du urteilst über jedes
Segment deines Viertels v1 (Liste unter „Dein Viertel“), ob Grenze und Klasse stimmen, und zeichnest ein, was
du ändern würdest. Die Label-Karte änderst du nicht.

## Daten (eingefrorener Stand, nur lesen)

- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/manifest.json`: Eintrag `r1c1` unter `teilkacheln` mit `bild` (Teilkachelbild,
  Kern + Kontextrand), `kern_im_bild` (Lage des Kerns im Teilkachelbild) und `kern` (Lage im Ausschnitt).
- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/vorstufe/r1c1/labels.tif`: Label-Karte (Segment-ID je Bildpunkt, Größe des Teilkachelbilds).
- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/vorstufe/r1c1/segmente.json`: je Segment `id`, `klasse`, `grob`, `herkunft`, `sicher`; dazu die
  Kandidatenliste der Vorstufe, falls vorhanden.
- `C:/Users/Phil/Developement/Victor/landseg/kategorien.json` und `C:/Users/Phil/Developement/Victor/landseg/KATEGORIEN.md`: nur Anregung; in Fassung B benennst du die Klassen selbst (Abschnitt „Fassung B“).

## Dein Viertel

Viertel v1 (oben links) des Kerns von `r1c1`: x 64–313, y 64–313 im
Teilkachelbild (250 × 250 Bildpunkte). Dir gehören die 44 Segmente der Liste unten: Jedes hat den
größten Teil seiner Kernfläche in diesem Viertel. Die Teilkachel hat 301 Kernsegmente
(v1 44, v2 52, v3 93, v4 112); drei andere Agents urteilen gleichzeitig über die anderen Viertel, jeder in seinem eigenen
Ordner. Ein Segment über einer Viertelgrenze urteilt nur das Viertel mit dem größten Anteil; in den Bildern
der Nachbarn ist es mit grauer Nummer als Umgebung zu sehen.

Urteil im Verbund: Du siehst das Viertel als zusammenhängendes Bild mit Umgebung, arbeitest die Liste der
Reihe nach ab und beurteilst jedes Segment im Zusammenhang mit seinen Nachbarn; eingetragen wird jedes
Segment einzeln (Klasse, `sicher`, `was_ist_es` als Notiz). Bilder freigestellter Einzelsegmente gibt es
nicht, und sie sind keine Urteilsgrundlage.

Bilder des Viertels (fertig, JPEG, in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r1c1/v1`, Fenster und Vergrößerung je Bild in `viertel.json`):

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
Teilkachelbild; Kandidaten aus `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/vorstufe/r1c1/kandidaten.json`, dort mit Grund, in den
Bildern nicht eingezeichnet; Anteil hier = Anteil der Kernfläche in diesem Viertel):

| Nr | ID | Klasse Vorstufe | sicher | im Siedlungsgebiet | Kernfläche px | Anteil hier | auch in | Punkt x/y | Kandidaten |
|---|---|---|---|---|---|---|---|---|---|
| 17 | 400017 | 6.6 Weg, unbefestigt (Feld-, Wald-, Schotterweg) | nein | nein | 1130 | 100 % | – | 73/70 | grenze_ohne_bildkante, klasse_unsicher |
| 18 | 400018 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 5308 | 100 % | – | 194/86 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 11 | 400011 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 609 | 84 % | v2 | 303/72 | grenze_ohne_bildkante, klasse_unsicher |
| 1 | 400001 | 4.1 Wald (geschlossener Bestand) | ja | nein | 1 | 100 % | – | 64/130 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 26 | 400026 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 334 | 100 % | – | 159/119 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 33 | 400033 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 2127 | 100 % | – | 126/160 | grenze_ohne_bildkante, klasse_unsicher |
| 31 | 400031 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 1163 | 100 % | – | 184/164 | grenze_ohne_bildkante, klasse_unsicher |
| 40 | 400040 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 1065 | 100 % | – | 241/192 | klasse_unsicher |
| 36 | 400036 | 4.1 Wald (geschlossener Bestand) | nein | nein | 181 | 100 % | – | 260/175 | klasse_unsicher |
| 37 | 400037 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 1063 | 100 % | – | 274/186 | klasse_unsicher |
| 35 | 400035 | 4.1 Wald (geschlossener Bestand) | nein | nein | 1811 | 74 % | v2 | 299/185 | grenze_ohne_bildkante, klasse_unsicher |
| 45 | 400045 | 4.1 Wald (geschlossener Bestand) | ja | nein | 126 | 83 % | v2 | 306/198 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 49 | 400049 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 1228 | 100 % | – | 131/227 | grenze_ohne_bildkante, klasse_unsicher |
| 59 | 400059 | 4.1 Wald (geschlossener Bestand) | ja | nein | 445 | 100 % | – | 160/237 | grenze_ohne_bildkante |
| 77 | 400077 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 198 | 100 % | – | 171/243 | klasse_unsicher |
| 55 | 400055 | 4.1 Wald (geschlossener Bestand) | nein | nein | 81 | 100 % | – | 177/210 | klasse_unsicher |
| 81 | 400081 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | ja | nein | 150 | 100 % | – | 183/242 | – |
| 46 | 400046 | 1.3.2 Baustelle | nein | nein | 1962 | 100 % | – | 189/222 | grenze_ohne_bildkante, klasse_unsicher |
| 44 | 400044 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 214 | 100 % | – | 210/203 | klasse_unsicher |
| 60 | 400060 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 450 | 100 % | – | 222/222 | klasse_unsicher |
| 63 | 400063 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 2450 | 100 % | – | 257/249 | grenze_ohne_bildkante, klasse_unsicher |
| 47 | 400047 | 4.1 Wald (geschlossener Bestand) | nein | nein | 128 | 100 % | – | 259/206 | klasse_unsicher |
| 83 | 400083 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | ja | nein | 146 | 100 % | – | 289/243 | – |
| 61 | 400061 | 4.2.1 Einzelbaum | ja | ja | 171 | 100 % | – | 295/220 | grenze_ohne_bildkante |
| 54 | 400054 | 4.2.1 Einzelbaum | nein | ja | 579 | 77 % | v2 | 306/210 | grenze_ohne_bildkante, klasse_unsicher |
| 52 | 400052 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 1991 | 90 % | v3 | 79/256 | grenze_ohne_bildkante, klasse_unsicher |
| 97 | 400097 | 4.1 Wald (geschlossener Bestand) | nein | nein | 193 | 100 % | – | 171/285 | klasse_unsicher |
| 98 | 400098 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 431 | 100 % | – | 178/275 | klasse_unsicher |
| 87 | 400087 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 612 | 100 % | – | 192/256 | klasse_unsicher |
| 94 | 400094 | 1.3.2 Baustelle | nein | nein | 1374 | 100 % | – | 206/286 | klasse_unsicher |
| 78 | 400078 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 391 | 100 % | – | 210/257 | klasse_unsicher |
| 90 | 400090 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 2470 | 53 % | v3 | 225/261 | grenze_ohne_bildkante, klasse_unsicher |
| 121 | 400121 | 1.3.2 Baustelle | nein | nein | 229 | 100 % | – | 233/298 | klasse_unsicher |
| 103 | 400103 | 4.1 Wald (geschlossener Bestand) | nein | nein | 814 | 84 % | v3 | 251/289 | klasse_unsicher |
| 104 | 400104 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 142 | 100 % | – | 264/281 | klasse_unsicher |
| 116 | 400116 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 91 | 100 % | – | 277/288 | klasse_unsicher |
| 89 | 400089 | 1.1.2 Nebengebäude / Schuppen / Stadel | ja | nein | 960 | 100 % | – | 286/270 | grenze_ohne_bildkante |
| 109 | 400109 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 122 | 100 % | – | 291/290 | grenze_ohne_bildkante, klasse_unsicher |
| 119 | 400119 | 3.1 Wiese / Weide (gemeinsam) | ja | ja | 88 | 100 % | – | 297/290 | – |
| 102 | 400102 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 213 | 95 % | v2 | 304/281 | klasse_unsicher |
| 88 | 400088 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 242 | 55 % | v2 | 309/258 | klasse_unsicher |
| 125 | 400125 | 4.1 Wald (geschlossener Bestand) | nein | nein | 222 | 90 % | v3 | 203/307 | klasse_unsicher |
| 120 | 400120 | 3.1 Wiese / Weide (gemeinsam) | nein | ja | 1038 | 79 % | v3 | 277/303 | grenze_ohne_bildkante, klasse_unsicher |
| 127 | 400127 | 4.2.1 Einzelbaum | ja | ja | 124 | 100 % | – | 303/307 | – |

`nicht_geprueft` nennt, was du nicht angesehen hast, `offen`, was du nicht entscheiden konntest.

Kontrolle vor der Rückgabe (muss mit `ok` enden):

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I C:/Users/Phil/Developement/Victor/wuensche/2026-11-17-landseg-test-t0-1/skripte/pruefe_urteil.py --urteil C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/urteil/r1c1/v1/urteil.json --segmente C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/vorstufe/r1c1/segmente.json --fassung b --viertel v1 --ids 400017,400018,400011,400001,400026,400033,400031,400040,400036,400037,400035,400045,400049,400059,400077,400055,400081,400046,400044,400060,400063,400047,400083,400061,400054,400052,400097,400098,400087,400094,400078,400090,400121,400103,400104,400116,400089,400109,400119,400102,400088,400125,400120,400127
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
der Bildkante), zur Kontrolle `pruefen`. Eigene Skripte als Datei in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/urteil/r1c1/v1`.

## Ergebnis in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/urteil/r1c1/v1` (genau diese Namen)

- `roh.jpg`, `umriss.jpg` (alle Segmentgrenzen mit ID), `maengel.jpg` (nummerierte Punkte mit kurzer
  deutscher Beschriftung, sonst Vermerk „keine Mängel“), `vorschlag.jpg` (Grenzen und Klassen, wie
  du sie setzen würdest, sonst Vermerk „unverändert“): je dein Viertel mit Umgebung, Viertel
  umrandet (Grundlage: die vorbereiteten Übersichtsbilder).
- `nah_<n>.jpg`: eigene Nahansichten von Stellen, die man in den vorbereiteten Bildern nicht beurteilen kann,
  je ein Teil des Viertels samt Nachbarn (mindestens 64 × 64 Bildpunkte der Teilkachel, kein freigestelltes
  Einzelsegment); `kontrast_<n>.jpg` bei blassen Stellen.
- `urteil.json` (UTF-8):

```
{"teilkachel": "r1c1", "viertel": "v1", "bearbeiter": "urt-b-r1c1-v1",
 "bilder_angesehen": {"uebersicht": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r1c1/v1/uebersicht_nummern.jpg", "…"],
                      "nah": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r1c1/v1/nah1_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/urteil/r1c1/v1/nah_1.jpg", "…"]},
 "segmente": [{"id": 17, "klasse_heute": "Code", "was_ist_es": "ein Satz",
               "urteil": "sauber" | "nicht_sauber", "klasse_vorschlag": null,
               "klasse_frei": {"grob": "Name", "mittel": "Name", "fein": "Name"},
               "sicher": true | false,
               "punkte": [{"nr": 1, "art": "fremdes|fehlt|trennen|verschmelzen|grenze|klasse|zu_klein|sonstiges",
                           "text": "ein Satz mit Stelle (x/y im Teilkachelbild)", "flaeche_px": Zahl oder null}],
               "bilder": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r1c1/v1/uebersicht_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r1c1/v1/nah2_roh.jpg"]}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "was an der Kerngrenze nicht passt"}],
 "unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."],
 "klassen_frei": [{"name": "Name", "ebene": "grob|mittel|fein", "eltern": "Name oder null", "merkmal": "woran im Bild erkennbar"}]}
```

Jedes Segment deiner Liste steht genau einmal unter `segmente`, auch die sauberen, in der Reihenfolge der Liste. Segmente der Nachbarviertel (graue Nummern) und des Kontextrands (ohne Nummer) urteilst du nicht; Auffälliges an ihnen nennst du unter `unsicher` mit ID.

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Punkte, Anteil `sicher: false`, wo du unsicher bist.
