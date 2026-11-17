# Auftrag: Teilkachel r0c1, Viertel v4: 21 Segmente im Verbund ansehen und einzeln urteilen (Fassung B: Kategorien frei)

Lies zuerst den Skill `landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Teilkachel `r0c1` des Ausschnitts in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b`. Du urteilst über jedes
Segment deines Viertels v4 (Liste unter „Dein Viertel“), ob Grenze und Klasse stimmen, und zeichnest ein, was
du ändern würdest. Die Label-Karte änderst du nicht.

## Daten (eingefrorener Stand, nur lesen)

- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/manifest.json`: Eintrag `r0c1` unter `teilkacheln` mit `bild` (Teilkachelbild,
  Kern + Kontextrand), `kern_im_bild` (Lage des Kerns im Teilkachelbild) und `kern` (Lage im Ausschnitt).
- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/vorstufe/r0c1/labels.tif`: Label-Karte (Segment-ID je Bildpunkt, Größe des Teilkachelbilds).
- `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/vorstufe/r0c1/segmente.json`: je Segment `id`, `klasse`, `grob`, `herkunft`, `sicher`; dazu die
  Kandidatenliste der Vorstufe, falls vorhanden.
- `C:/Users/Phil/Developement/Victor/landseg/kategorien.json` und `C:/Users/Phil/Developement/Victor/landseg/KATEGORIEN.md`: nur Anregung; in Fassung B benennst du die Klassen selbst (Abschnitt „Fassung B“).

## Dein Viertel

Viertel v4 (unten rechts) des Kerns von `r0c1`: x 314–563, y 314–563 im
Teilkachelbild (250 × 250 Bildpunkte). Dir gehören die 21 Segmente der Liste unten: Jedes hat den
größten Teil seiner Kernfläche in diesem Viertel. Die Teilkachel hat 147 Kernsegmente
(v1 46, v2 43, v3 37, v4 21); drei andere Agents urteilen gleichzeitig über die anderen Viertel, jeder in seinem eigenen
Ordner. Ein Segment über einer Viertelgrenze urteilt nur das Viertel mit dem größten Anteil; in den Bildern
der Nachbarn ist es mit grauer Nummer als Umgebung zu sehen.

Urteil im Verbund: Du siehst das Viertel als zusammenhängendes Bild mit Umgebung, arbeitest die Liste der
Reihe nach ab und beurteilst jedes Segment im Zusammenhang mit seinen Nachbarn; eingetragen wird jedes
Segment einzeln (Klasse, `sicher`, `was_ist_es` als Notiz). Bilder freigestellter Einzelsegmente gibt es
nicht, und sie sind keine Urteilsgrundlage.

Bilder des Viertels (fertig, JPEG, in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r0c1/v4`, Fenster und Vergrößerung je Bild in `viertel.json`):

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
| 152 | 200152 | 4.1 Wald (geschlossener Bestand) | nein | nein | 240 | 100 % | – | 355/328 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 153 | 200153 | 4.2.1 Einzelbaum | nein | nein | 2247 | 100 % | – | 384/349 | grenze_ohne_bildkante, klasse_unsicher |
| 150 | 200150 | 4.1 Wald (geschlossener Bestand) | nein | nein | 150 | 81 % | v2 | 401/318 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 140 | 200140 | 3.1 Wiese / Weide (gemeinsam) | ja | nein | 4667 | 68 % | v2 | 441/336 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 148 | 200148 | 4.2.1 Einzelbaum | nein | nein | 1468 | 88 % | v2 | 481/332 | grenze_ohne_bildkante, klasse_unsicher |
| 143 | 200143 | 3.1 Wiese / Weide (gemeinsam) | ja | ja | 7361 | 44 % | v1, v2, v3 | 337/362 | grenze_ohne_bildkante |
| 176 | 200176 | 4.1 Wald (geschlossener Bestand) | nein | nein | 303 | 100 % | – | 376/378 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 165 | 200165 | 4.2.1 Einzelbaum | nein | nein | 3299 | 100 % | – | 403/395 | grenze_ohne_bildkante, klasse_unsicher |
| 166 | 200166 | 4.2.1 Einzelbaum | nein | nein | 500 | 100 % | – | 458/365 | klasse_unsicher |
| 164 | 200164 | 0.2 Wolke / Wolkenschatten / Schatten ohne erkennbaren Grund | nein | nein | 243 | 100 % | – | 484/364 | klasse_unsicher |
| 175 | 200175 | 2.1 Acker mit Bewuchs | nein | nein | 112 | 100 % | – | 486/377 | grenze_ohne_bildkante, klasse_unsicher |
| 169 | 200169 | 4.1 Wald (geschlossener Bestand) | nein | nein | 214 | 100 % | – | 533/364 | grenze_ohne_bildkante, klasse_unsicher |
| 182 | 200182 | 6.1 Offene Sand-, Löss-, Lehmstelle (Abbruch, Hohlweg, Grube) | nein | nein | 154 | 100 % | – | 362/413 | grenze_ohne_bildkante, klasse_unsicher |
| 186 | 200186 | 4.1 Wald (geschlossener Bestand) | nein | nein | 91 | 100 % | – | 407/421 | grenze_ohne_bildkante, klasse_unsicher |
| 179 | 200179 | 4.1 Wald (geschlossener Bestand) | nein | nein | 72 | 100 % | – | 440/401 | grenze_ohne_bildkante, klasse_unsicher |
| 170 | 200170 | 6.6 Weg, unbefestigt (Feld-, Wald-, Schotterweg) | ja | nein | 63018 | 65 % | v3 | 479/479 | grenze_ohne_bildkante |
| 203 | 200203 | 3.1 Wiese / Weide (gemeinsam) | nein | nein | 269 | 86 % | v3 | 327/544 | klasse_unsicher |
| 206 | 200206 | 4.2.1 Einzelbaum | nein | nein | 196 | 100 % | – | 327/554 | grenze_ohne_bildkante, klasse_unsicher |
| 208 | 200208 | 4.1 Wald (geschlossener Bestand) | nein | nein | 114 | 100 % | – | 337/556 | grenze_ohne_bildkante, klasse_unsicher, nicht_zusammenhaengend |
| 211 | 200211 | 3.1 Wiese / Weide (gemeinsam) | ja | nein | 57 | 100 % | – | 350/561 | grenze_ohne_bildkante, nicht_zusammenhaengend |
| 209 | 200209 | 3.1 Wiese / Weide (gemeinsam) | nein | nein | 107 | 100 % | – | 362/560 | klasse_unsicher |

`nicht_geprueft` nennt, was du nicht angesehen hast, `offen`, was du nicht entscheiden konntest.

Kontrolle vor der Rückgabe (muss mit `ok` enden):

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I C:/Users/Phil/Developement/Victor/wuensche/2026-11-17-landseg-test-t0-1/skripte/pruefe_urteil.py --urteil C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/urteil/r0c1/v4/urteil.json --segmente C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/vorstufe/r0c1/segmente.json --fassung b --viertel v4 --ids 200152,200153,200150,200140,200148,200143,200176,200165,200166,200164,200175,200169,200182,200186,200179,200170,200203,200206,200208,200211,200209
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
der Bildkante), zur Kontrolle `pruefen`. Eigene Skripte als Datei in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/urteil/r0c1/v4`.

## Ergebnis in `C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/urteil/r0c1/v4` (genau diese Namen)

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
 "bilder_angesehen": {"uebersicht": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r0c1/v4/uebersicht_nummern.jpg", "…"],
                      "nah": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r0c1/v4/nah1_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/urteil/r0c1/v4/nah_1.jpg", "…"]},
 "segmente": [{"id": 17, "klasse_heute": "Code", "was_ist_es": "ein Satz",
               "urteil": "sauber" | "nicht_sauber", "klasse_vorschlag": null,
               "klasse_frei": {"grob": "Name", "mittel": "Name", "fein": "Name"},
               "sicher": true | false,
               "punkte": [{"nr": 1, "art": "fremdes|fehlt|trennen|verschmelzen|grenze|klasse|zu_klein|sonstiges",
                           "text": "ein Satz mit Stelle (x/y im Teilkachelbild)", "flaeche_px": Zahl oder null}],
               "bilder": ["C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r0c1/v4/uebersicht_nummern.jpg", "C:/Users/Phil/Developement/Victor/daten/landseg/T0/fassung-b/viertel/r0c1/v4/nah2_roh.jpg"]}],
 "naht": [{"id": 17, "seite": "links|rechts|oben|unten", "text": "was an der Kerngrenze nicht passt"}],
 "unsicher": ["..."], "nicht_geprueft": ["..."], "offen": ["..."],
 "klassen_frei": [{"name": "Name", "ebene": "grob|mittel|fein", "eltern": "Name oder null", "merkmal": "woran im Bild erkennbar"}]}
```

Jedes Segment deiner Liste steht genau einmal unter `segmente`, auch die sauberen, in der Reihenfolge der Liste. Segmente der Nachbarviertel (graue Nummern) und des Kontextrands (ohne Nummer) urteilst du nicht; Auffälliges an ihnen nennst du unter `unsicher` mit ID.

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Punkte, Anteil `sicher: false`, wo du unsicher bist.
