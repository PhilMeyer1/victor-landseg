# Garten-Bestätigung T0-B-r1c1-3

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
  - v4: mit Umriss `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-B-r1c1-3/v4_umriss.jpg`, roh daneben `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-B-r1c1-3/v4_roh.jpg`
- Kandidatenliste: `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-B-r1c1-3/kandidaten.json` (id, Klasse, Fläche m², Viertel, Mittelpunkt x,y in Bildpunkten der Teilkachel, Grund der Auswahl).

## Kandidaten

| id | Klasse | Fläche m² | Viertel | Mitte x,y | Grund der Auswahl |
|---|---|---|---|---|---|
| 400067 | 3.3.2 Parzelle gemischt | 1026 | v4 | 427,382 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400129 | 2.2 Rasen | 4 | v4 | 559,342 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400132 | 3.3.2 Parzelle gemischt | 19 | v4 | 553,325 | Grünland; grenzt an Gebäude oder Hof |
| 400142 | 3.3.1 Beete | 13 | v4 | 330,335 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400152 | 2.2 Rasen | 43 | v4 | 325,357 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400159 | 2.2 Rasen | 7 | v4 | 559,357 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400173 | 2.2 Rasen | 4 | v4 | 376,366 | Grünland; grenzt an Gebäude oder Hof |
| 400213 | 3.3.2 Parzelle gemischt | 9 | v4 | 554,415 | Grünland; grenzt an Gebäude oder Hof |
| 400215 | 2.2 Rasen | 1 | v4 | 396,419 | Grünland; grenzt an Gebäude oder Hof |
| 400221 | 2.2 Rasen | 0 | v4 | 563,421 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400222 | 2.2 Rasen | 34 | v4 | 550,449 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400226 | 2.2 Rasen | 44 | v4 | 364,445 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400245 | 2.2 Rasen | 35 | v4 | 532,477 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400246 | 2.2 Rasen | 4 | v4 | 484,461 | Grünland; grenzt an Gebäude oder Hof |
| 400252 | 2.2 Rasen | 7 | v4 | 401,472 | Grünland; grenzt an Gebäude oder Hof |
| 400259 | 2.2 Rasen | 67 | v4 | 365,494 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400263 | 3.3.1 Beete | 4 | v4 | 342,475 | Grünland; grenzt an Gebäude oder Hof |
| 400277 | 2.2 Rasen | 6 | v4 | 518,495 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400279 | 2.2 Rasen | 22 | v4 | 544,499 | Grünland; grenzt an Gebäude oder Hof |
| 400282 | 3.3.2 Parzelle gemischt | 32 | v4 | 414,510 | Grünland; grenzt an Gebäude oder Hof |
| 400286 | 3.3.2 Parzelle gemischt | 15 | v4 | 474,513 | Grünland; grenzt an Gebäude oder Hof |
| 400290 | 2.2 Rasen | 27 | v4 | 547,518 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400294 | 2.2 Rasen | 4 | v4 | 332,512 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400295 | 2.2 Rasen | 12 | v4 | 346,519 | Grünland; grenzt an Gebäude oder Hof |
| 400296 | 3.3.2 Parzelle gemischt | 20 | v4 | 442,522 | Grünland; grenzt an Gebäude oder Hof |
| 400301 | 3.3.2 Parzelle gemischt | 29 | v4 | 489,536 | Grünland; grenzt an Gebäude oder Hof |
| 400310 | 3.3.2 Parzelle gemischt | 41 | v4 | 544,540 | Grünland; grenzt an Gebäude oder Hof |
| 400317 | 3.3.2 Parzelle gemischt | 18 | v4 | 420,549 | Grünland; grenzt an Gebäude oder Hof |
| 400326 | 2.2 Rasen | 8 | v4 | 429,549 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400334 | 2.2 Rasen | 6 | v4 | 445,558 | Grünland; grenzt an Gebäude oder Hof |
| 400349 | 2.2 Rasen | 0 | v4 | 397,562 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |

## Bei Zweifel

Eine Nahansicht (roh und mit Umriss nebeneinander) macht dieser Befehl im Ordner `C:/Users/Phil/Developement/Victor/landseg`:

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg zoom --manifest C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/manifest.json --teilkachel r1c1 --labels C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/b-kategorien-frei/r1c1/labels.tif --ids <id> --roh --ziel C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-B-r1c1-3/nah_<id>.jpg
```

Nahansichten nur in diesen Ordner schreiben. Kein Subagent, keine Fenster, nichts installieren, keine Karte ändern.

## Ergebnis

Datei `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-B-r1c1-3/entscheid.json` (UTF-8-JSON), genau ein Eintrag je Kandidaten-ID:

```json
{"<id>": {"garten": "ja" | "nein" | "unklar", "grund": "<ein Satz>"}}
```

„ja“ nur für krautige Grünfläche oder Beet in einem Haus- oder Hofgarten; Gehölz, Weg, Hof, Park, Friedhof, Sportrasen und Wiese oder Acker am Ortsrand ohne Haus „nein“; was du am Bild nicht sicher entscheiden kannst, „unklar“. Rückgabe: Zahl ja / nein / unklar.
