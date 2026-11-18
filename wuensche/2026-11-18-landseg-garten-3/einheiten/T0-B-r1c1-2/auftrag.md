# Garten-Bestätigung T0-B-r1c1-2

Du bist ein Agent des Projekts landseg (Segmentierung von Luftbildern). Antworte auf Deutsch. Regeln: `C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md` (lies sie zuerst, besonders L14 und L15).

## Ziel

Entscheide für jeden der 31 Kandidaten unten am Bild, ob er ein Haus- oder Hofgarten ist und damit die Klasse Garten bekommen soll (in dieser Liste Code `2.4` „Garten (Haus- und Hofgarten: Grünfläche, Beet)“). Du änderst keine Karte und keine Klasse; du schreibst nur die Ergebnisdatei.

## Was „Garten“ ist (Entscheidungen des Nutzers vom 18.11.2026)

- eine einzige Unterklasse „Garten“ unter Dauergrünland (feste Liste: Code 3.6; freie Listen A/B: ihre eigene Klasse Garten unter ihrer Dauergrünland-Klasse, Regel L14 im Skill);
- dazu gehört jede krautige Grünfläche und jedes Beet im Haus- oder Hofgarten (auch Vor-, Obst- und Gemüsegarten), ob gepflegter Rasen oder nicht — Rasen ist kein Kennzeichen;
- nur Haus- und Hofgärten: Parks, Friedhöfe, Sportrasen und Wiesen am Ortsrand bleiben Wiese/Weide;
- Bäume, Sträucher und Hecken im Garten bleiben Gehölz (von oben sieht man die Krone);
- auf dem Schwarz-Weiß-Bild H0 nur klar erkennbare Gärten am Haus; Unklares bleibt, wie es ist.

## Bild

- Bild: T0 Farbe (Farb-Orthofoto, rund 0,2 m je Bildpunkt).
- Fassung B (b-kategorien-frei), Teilkachel r1c1; Kategorienliste `C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/b-kategorien-frei/kategorien-b.json`.
- Karte: `C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/b-kategorien-frei/r1c1/labels.tif`, Teilkachelbild: `C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/teilkacheln/r1c1.png`.
- Bilder je Viertel (gelb alle Grenzen, magenta die Kandidaten mit Nummer; weißer Rahmen = Kern); jedes nur einmal ansehen:
  - v3: mit Umriss `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-B-r1c1-2/v3_umriss.jpg`, roh daneben `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-B-r1c1-2/v3_roh.jpg`
- Kandidatenliste: `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-B-r1c1-2/kandidaten.json` (id, Klasse, Fläche m², Viertel, Mittelpunkt x,y in Bildpunkten der Teilkachel, Grund der Auswahl).

## Kandidaten

| id | Klasse | Fläche m² | Viertel | Mitte x,y | Grund der Auswahl |
|---|---|---|---|---|---|
| 400133 | 2.2 Rasen | 8 | v3 | 291,326 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400141 | 2.2 Rasen | 4 | v3 | 242,325 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400144 | 2.2 Rasen | 83 | v3 | 252,350 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400146 | 2.2 Rasen | 102 | v3 | 278,382 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400161 | 2.2 Rasen | 5 | v3 | 222,354 | Grünland; grenzt an Gebäude oder Hof |
| 400164 | 2.2 Rasen | 6 | v3 | 175,359 | Grünland; grenzt an Gebäude oder Hof |
| 400175 | 2.2 Rasen | 33 | v3 | 182,379 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400177 | 3.3.2 Parzelle gemischt | 309 | v3 | 143,440 | Grünland; grenzt an Gebäude oder Hof |
| 400186 | 2.2 Rasen | 5 | v3 | 244,377 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400189 | 3.3.2 Parzelle gemischt | 79 | v3 | 308,413 | Grünland; grenzt an Gebäude oder Hof |
| 400199 | 2.2 Rasen | 63 | v3 | 217,417 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400216 | 2.2 Rasen | 127 | v3 | 234,476 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400220 | 2.2 Rasen | 11 | v3 | 197,431 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400224 | 2.2 Rasen | 6 | v3 | 260,428 | Grünland; grenzt an Gebäude oder Hof |
| 400228 | 3.3.2 Parzelle gemischt | 6 | v3 | 197,439 | Grünland; grenzt an Gebäude oder Hof |
| 400232 | 2.2 Rasen | 124 | v3 | 308,513 | Grünland; grenzt an Gebäude oder Hof |
| 400240 | 2.2 Rasen | 18 | v3 | 178,470 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400249 | 2.2 Rasen | 7 | v3 | 147,466 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400253 | 3.3.2 Parzelle gemischt | 11 | v3 | 257,475 | Grünland; grenzt an Gebäude oder Hof |
| 400261 | 2.2 Rasen | 8 | v3 | 138,477 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400269 | 3.3.2 Parzelle gemischt | 10 | v3 | 205,483 | Grünland; grenzt an Gebäude oder Hof |
| 400270 | 2.2 Rasen | 46 | v3 | 187,497 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400271 | 3.3.2 Parzelle gemischt | 10 | v3 | 276,487 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400287 | 2.2 Rasen | 38 | v3 | 284,521 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400291 | 2.2 Rasen | 15 | v3 | 132,514 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400309 | 2.2 Rasen | 34 | v3 | 189,544 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400315 | 2.2 Rasen | 8 | v3 | 269,538 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400316 | 3.3.2 Parzelle gemischt | 10 | v3 | 108,543 | Grünland; grenzt an Gebäude oder Hof |
| 400323 | 2.2 Rasen | 7 | v3 | 293,547 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400332 | 2.2 Rasen | 2 | v3 | 124,558 | Grünland; grenzt an Gebäude oder Hof |
| 400347 | 2.2 Rasen | 1 | v3 | 314,562 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |

## Bei Zweifel

Eine Nahansicht (roh und mit Umriss nebeneinander) macht dieser Befehl im Ordner `C:/Users/Phil/Developement/Victor/landseg`:

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg zoom --manifest C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/manifest.json --teilkachel r1c1 --labels C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/b-kategorien-frei/r1c1/labels.tif --ids <id> --roh --ziel C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-B-r1c1-2/nah_<id>.jpg
```

Nahansichten nur in diesen Ordner schreiben. Kein Subagent, keine Fenster, nichts installieren, keine Karte ändern.

## Ergebnis

Datei `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-B-r1c1-2/entscheid.json` (UTF-8-JSON), genau ein Eintrag je Kandidaten-ID:

```json
{"<id>": {"garten": "ja" | "nein" | "unklar", "grund": "<ein Satz>"}}
```

„ja“ nur für krautige Grünfläche oder Beet in einem Haus- oder Hofgarten; Gehölz, Weg, Hof, Park, Friedhof, Sportrasen und Wiese oder Acker am Ortsrand ohne Haus „nein“; was du am Bild nicht sicher entscheiden kannst, „unklar“. Rückgabe: Zahl ja / nein / unklar.
