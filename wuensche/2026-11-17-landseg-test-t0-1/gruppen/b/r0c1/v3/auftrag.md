# Auftrag: Teilkachel r0c1, Viertel v3: 37 Segmente im Verbund ansehen und einzeln urteilen (Fassung B: Kategorien frei)

Lies zuerst den Skill `landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `r0c1` des Ausschnitts in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b`. Du urteilst über jedes
Segment deines Viertels v3 (Liste unter „Dein Viertel“), ob Grenze und Klasse stimmen, und zeichnest ein, was
du ändern würdest. Die Label-Karte änderst du nicht.

## Daten (eingefrorener Stand, nur lesen)

- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/manifest.json`: Eintrag `r0c1` unter `teilkacheln` mit `bild` (Teilkachelbild,
  Kern + Kontextrand), `kern_im_bild` (Lage des Kerns im Teilkachelbild) und `kern` (Lage im Ausschnitt).
- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/vorstufe/r0c1/labels.tif`: Label-Karte (Segment-ID je Bildpunkt, Größe des Teilkachelbilds).
- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/vorstufe/r0c1/segmente.json`: je Segment `id`, `klasse`, `grob`, `herkunft`, `sicher`; dazu die
  Kandidatenliste der Vorstufe, falls vorhanden.
- `C:/Users/Phil/Developement/Victor/landseg/kategorien.json` und `C:/Users/Phil/Developement/Victor/landseg/KATEGORIEN.md`: nur Anregung; in Fassung B benennst du die Klassen selbst (Abschnitt „Fassung B“).

## Dein Viertel

Viertel v3 (unten links) des Kerns von `r0c1`: x 64–313, y 314–563 im
Teilkachelbild (250 × 250 Bildpunkte). Dir gehören die 37 Segmente der Liste unten: Jedes hat den
größten Teil seiner Kernfläche in diesem Viertel. Die Teilkachel hat 147 Kernsegmente
(v1 46, v2 43, v3 37, v4 21); drei andere Agents urteilen gleichzeitig über die anderen Viertel, jeder in seinem eigenen
Ordner. Ein Segment über einer Viertelgrenze urteilt nur das Viertel mit dem größten Anteil; in den Bildern
der Nachbarn ist es mit grauer Nummer als Umgebung zu sehen.

Urteil im Verbund: Du siehst das Viertel als zusammenhängendes Bild mit Umgebung, arbeitest die Liste der
Reihe nach ab und beurteilst jedes Segment im Zusammenhang mit seinen Nachbarn; eingetragen wird jedes
Segment einzeln (Klasse, `sicher`, `was_ist_es` als Notiz). Bilder freigestellter Einzelsegmente gibt es
nicht, und sie sind keine Urteilsgrundlage.

Bilder des Viertels (fertig, JPEG, in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r0c1/v3`, Fenster und Vergrößerung je Bild in `viertel.json`):

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
| 145 | 200145 | 4.2.1 Einzelbaum | ja | ja | 744 | 84 % | v1 | 72/340 | grenze_ohne_bildkante |
| 139 | 200139 | 4.2.1 Einzelbaum | nein | ja | 3911 | 54 % | v1 | 106/332 | grenze_ohne_bildkante, klasse_unsicher |
| 156 | 200156 | 4.1 Wald (geschlossener Bestand) | nein | nein | 76 | 100 % | – | 174/347 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 141 | 200141 | 4.2.1 Einzelbaum | nein | ja | 2873 | 68 % | v1 | 201/331 | grenze_ohne_bildkante, klasse_unsicher |
| 157 | 200157 | 4.1 Wald (geschlossener Bestand) | ja | nein | 244 | 100 % | – | 244/348 | grenze_ohne_bildkante |
| 149 | 200149 | 1.3.4 Sport-, Spielplatz (künstlicher Belag) | nein | nein | 156 | 74 % | v1 | 258/318 | grenze_ohne_bildkante, klasse_unsicher |
| 155 | 200155 | 4.1 Wald (geschlossener Bestand) | nein | nein | 342 | 100 % | – | 80/353 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 167 | 200167 | 4.2.4 Gebüsch / Strauchfläche | nein | nein | 2309 | 100 % | – | 86/382 | grenze_ohne_bildkante, klasse_unsicher |
| 154 | 200154 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 1262 | 100 % | – | 120/362 | grenze_ohne_bildkante, klasse_unsicher |
| 158 | 200158 | 4.2.1 Einzelbaum | ja | ja | 4320 | 100 % | – | 159/384 | grenze_ohne_bildkante |
| 162 | 200162 | 4.1 Wald (geschlossener Bestand) | nein | nein | 93 | 100 % | – | 200/351 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 160 | 200160 | 4.2.1 Einzelbaum | nein | ja | 2424 | 100 % | – | 213/398 | grenze_ohne_bildkante, klasse_unsicher |
| 159 | 200159 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 359 | 100 % | – | 229/360 | klasse_unsicher |
| 174 | 200174 | 1.1.1 Hauptgebäude (Wohn-, Betriebsgebäude) | nein | nein | 663 | 100 % | – | 263/383 | klasse_unsicher |
| 163 | 200163 | 1.3.3 Schwimmbecken | nein | nein | 987 | 100 % | – | 264/363 | klasse_unsicher |
| 172 | 200172 | 3.1 Wiese / Weide (gemeinsam) | ja | ja | 91 | 100 % | – | 284/369 | – |
| 185 | 200185 | 4.1 Wald (geschlossener Bestand) | nein | nein | 96 | 100 % | – | 71/421 | grenze_ohne_bildkante, klasse_unsicher |
| 184 | 200184 | 6.1 Offene Sand-, Löss-, Lehmstelle (Abbruch, Hohlweg, Grube) | nein | nein | 128 | 100 % | – | 91/416 | grenze_ohne_bildkante, klasse_unsicher |
| 173 | 200173 | 4.1 Wald (geschlossener Bestand) | nein | nein | 648 | 100 % | – | 113/403 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 183 | 200183 | 6.1 Offene Sand-, Löss-, Lehmstelle (Abbruch, Hohlweg, Grube) | ja | nein | 119 | 100 % | – | 117/415 | grenze_ohne_bildkante |
| 181 | 200181 | 4.1 Wald (geschlossener Bestand) | ja | nein | 88 | 100 % | – | 187/409 | grenze_ohne_bildkante |
| 188 | 200188 | 2.1 Acker mit Bewuchs | nein | ja | 88 | 100 % | – | 213/430 | grenze_ohne_bildkante, klasse_unsicher |
| 187 | 200187 | 2.1 Acker mit Bewuchs | nein | ja | 109 | 100 % | – | 230/429 | klasse_unsicher |
| 180 | 200180 | 1.1.2 Nebengebäude / Schuppen / Stadel | nein | nein | 367 | 100 % | – | 254/406 | klasse_unsicher |
| 171 | 200171 | 4.1 Wald (geschlossener Bestand) | nein | nein | 3700 | 59 % | v4 | 301/402 | grenze_ohne_bildkante, klasse_unsicher |
| 191 | 200191 | 2.1 Acker mit Bewuchs | nein | ja | 205 | 100 % | – | 225/497 | klasse_unsicher |
| 189 | 200189 | 3.1 Wiese / Weide (gemeinsam) | ja | nein | 8251 | 100 % | – | 93/534 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 196 | 200196 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | ja | nein | 195 | 100 % | – | 191/517 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 199 | 200199 | 4.1 Wald (geschlossener Bestand) | nein | nein | 128 | 100 % | – | 199/522 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 205 | 200205 | 4.1 Wald (geschlossener Bestand) | nein | nein | 118 | 100 % | – | 221/542 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 193 | 200193 | 4.2.1 Einzelbaum | ja | nein | 2001 | 100 % | – | 233/523 | grenze_ohne_bildkante |
| 200 | 200200 | 4.1 Wald (geschlossener Bestand) | nein | nein | 93 | 100 % | – | 257/524 | klasse_unsicher, nicht_zusammenhaengend |
| 195 | 200195 | 2.4.1 Weingarten | ja | nein | 115 | 100 % | – | 258/511 | – |
| 204 | 200204 | 4.1 Wald (geschlossener Bestand) | nein | nein | 248 | 100 % | – | 260/541 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 202 | 200202 | 4.1 Wald (geschlossener Bestand) | ja | nein | 106 | 100 % | – | 265/525 | – |
| 197 | 200197 | 4.2.1 Einzelbaum | nein | nein | 1980 | 87 % | v4 | 296/539 | grenze_ohne_bildkante, klasse_unsicher |
| 207 | 200207 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 416 | 100 % | – | 157/557 | grenze_ohne_bildkante, klasse_unsicher |

`nicht_geprueft` nennt, was du nicht angesehen hast, `offen`, was du nicht entscheiden konntest.

Kontrolle vor der Rückgabe (muss mit `ok` enden):

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I C:/Users/Phil/Developement/Victor/wuensche/2026-11-17-landseg-test-t0-1/skripte/pruefe_urteil.py --urteil C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/urteil/r0c1/v3/urteil.json --segmente C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/vorstufe/r0c1/segmente.json --fassung b --viertel v3 --ids 200145,200139,200156,200141,200157,200149,200155,200167,200154,200158,200162,200160,200159,200174,200163,200172,200185,200184,200173,200183,200181,200188,200187,200180,200171,200191,200189,200196,200199,200205,200193,200200,200195,200204,200202,200197,200207
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
der Bildkante), zur Kontrolle `pruefen`. Eigene Skripte als Datei in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/urteil/r0c1/v3`.

## Ergebnis in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/urteil/r0c1/v3` (genau diese Namen)

- `roh.jpg`, `umriss.jpg` (alle Segmentgrenzen mit ID), `maengel.jpg` (nummerierte Punkte mit kurzer
  deutscher Beschriftung, sonst Vermerk „keine Mängel“), `vorschlag.jpg` (Grenzen und Klassen, wie
  du sie setzen würdest, sonst Vermerk „unverändert“): je dein Viertel mit Umgebung, Viertel
  umrandet (Grundlage: die vorbereiteten Übersichtsbilder).
- `nah_<n>.jpg`: eigene Nahansichten von Stellen, die man in den vorbereiteten Bildern nicht beurteilen kann,
  je ein Teil des Viertels samt Nachbarn (mindestens 64 × 64 Bildpunkte der Teilkachel, kein freigestelltes
  Einzelsegment); `kontrast_<n>.jpg` bei blassen Stellen.
- `urteil.json` (UTF-8):

```
{"teilkachel": "r0c1", "viertel": "v3", "bearbeiter": "urt-b-r0c1-v3",
 "bilder_angesehen": {"uebersicht": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r0c1/v3/uebersicht_nummern.jpg", "…"],
                      "nah": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r0c1/v3/nah1_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/urteil/r0c1/v3/nah_1.jpg", "…"]},
 "segmente": [{"id": 17, "klasse_heute": "Code", "was_ist_es": "ein Satz",
               "urteil": "sauber" | "nicht_sauber", "klasse_vorschlag": null,
               "klasse_frei": {"grob": "Name", "mittel": "Name", "fein": "Name"},
               "sicher": true | false,
               "punkte": [{"nr": 1, "art": "fremdes|fehlt|trennen|verschmelzen|grenze|klasse|zu_klein|sonstiges",
                           "text": "ein Satz mit Stelle (x/y im Teilkachelbild)", "flaeche_px": Zahl oder null}],
               "bilder": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r0c1/v3/uebersicht_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r0c1/v3/nah2_roh.jpg"]}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "was an der Kerngrenze nicht passt"}],
 "unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."],
 "klassen_frei": [{"name": "Name", "ebene": "grob|mittel|fein", "eltern": "Name oder null", "merkmal": "woran im Bild erkennbar"}]}
```

Jedes Segment deiner Liste steht genau einmal unter `segmente`, auch die sauberen, in der Reihenfolge der Liste. Segmente der Nachbarviertel (graue Nummern) und des Kontextrands (ohne Nummer) urteilst du nicht; Auffälliges an ihnen nennst du unter `unsicher` mit ID.

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Punkte, Anteil `sicher: false`, wo du unsicher bist.
