# Garten-Bestätigung T0-C-r1c1-3

Du bist ein Agent des Projekts landseg (Segmentierung von Luftbildern). Antworte auf Deutsch. Regeln: `C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md` (lies sie zuerst, besonders L14 und L15).

## Ziel

Entscheide für jeden der 40 Kandidaten unten am Bild, ob er ein Haus- oder Hofgarten ist und damit die Klasse Garten bekommen soll (in dieser Liste Code `3.6` „Garten (Haus- und Hofgarten: Grünfläche, Beet)“). Du änderst keine Karte und keine Klasse; du schreibst nur die Ergebnisdatei.

## Was „Garten“ ist (Entscheidungen des Nutzers vom 18.11.2026)

- eine einzige Unterklasse „Garten“ unter Dauergrünland (feste Liste: Code 3.6; freie Listen A/B: ihre eigene Klasse Garten unter ihrer Dauergrünland-Klasse, Regel L14 im Skill);
- dazu gehört jede krautige Grünfläche und jedes Beet im Haus- oder Hofgarten (auch Vor-, Obst- und Gemüsegarten), ob gepflegter Rasen oder nicht — Rasen ist kein Kennzeichen;
- nur Haus- und Hofgärten: Parks, Friedhöfe, Sportrasen und Wiesen am Ortsrand bleiben Wiese/Weide;
- Bäume, Sträucher und Hecken im Garten bleiben Gehölz (von oben sieht man die Krone);
- auf dem Schwarz-Weiß-Bild H0 nur klar erkennbare Gärten am Haus; Unklares bleibt, wie es ist.

## Bild

- Bild: T0 Farbe (Farb-Orthofoto, rund 0,2 m je Bildpunkt).
- Fassung C (c-feste-liste), Teilkachel r1c1; Kategorienliste `C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/c-feste-liste/kategorien-c.json`.
- Karte: `C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/c-feste-liste/r1c1/labels.tif`, Teilkachelbild: `C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/teilkacheln/r1c1.png`.
- Bilder je Viertel (gelb alle Grenzen, magenta die Kandidaten mit Nummer; weißer Rahmen = Kern); jedes nur einmal ansehen:
  - v4: mit Umriss `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-C-r1c1-3/v4_umriss.jpg`, roh daneben `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-C-r1c1-3/v4_roh.jpg`
- Kandidatenliste: `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-C-r1c1-3/kandidaten.json` (id, Klasse, Fläche m², Viertel, Mittelpunkt x,y in Bildpunkten der Teilkachel, Grund der Auswahl).

## Kandidaten

| id | Klasse | Fläche m² | Viertel | Mitte x,y | Grund der Auswahl |
|---|---|---|---|---|---|
| 400067 | 3.1 Wiese / Weide (gemeinsam) | 1026 | v4 | 427,382 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400129 | 3.1 Wiese / Weide (gemeinsam) | 4 | v4 | 559,342 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400142 | 2.2 Acker ohne Bewuchs (gepflügt, Saatbett) | 13 | v4 | 330,335 | Acker klein; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400152 | 3.1 Wiese / Weide (gemeinsam) | 43 | v4 | 325,357 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400159 | 3.1 Wiese / Weide (gemeinsam) | 7 | v4 | 559,357 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400172 | 3.1 Wiese / Weide (gemeinsam) | 9 | v4 | 545,372 | Grünland; grenzt an Gebäude oder Hof |
| 400173 | 3.1 Wiese / Weide (gemeinsam) | 4 | v4 | 376,366 | Grünland; grenzt an Gebäude oder Hof |
| 400190 | 3.1 Wiese / Weide (gemeinsam) | 5 | v4 | 342,387 | Grünland; grenzt an Gebäude oder Hof |
| 400191 | 3.1 Wiese / Weide (gemeinsam) | 4 | v4 | 482,386 | Grünland; grenzt an Gebäude oder Hof |
| 400195 | 3.1 Wiese / Weide (gemeinsam) | 3 | v4 | 536,389 | Grünland; grenzt an Gebäude oder Hof |
| 400197 | 3.1 Wiese / Weide (gemeinsam) | 3 | v4 | 466,393 | Grünland; grenzt an Gebäude oder Hof |
| 400204 | 3.1 Wiese / Weide (gemeinsam) | 7 | v4 | 528,405 | Grünland; grenzt an Gebäude oder Hof |
| 400205 | 3.1 Wiese / Weide (gemeinsam) | 9 | v4 | 394,405 | Grünland; grenzt an Gebäude oder Hof |
| 400208 | 3.1 Wiese / Weide (gemeinsam) | 2 | v4 | 399,406 | Grünland; grenzt an Gebäude oder Hof |
| 400215 | 3.1 Wiese / Weide (gemeinsam) | 1 | v4 | 396,419 | Grünland; grenzt an Gebäude oder Hof |
| 400221 | 3.1 Wiese / Weide (gemeinsam) | 0 | v4 | 563,421 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400222 | 3.1 Wiese / Weide (gemeinsam) | 34 | v4 | 550,449 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400226 | 3.1 Wiese / Weide (gemeinsam) | 44 | v4 | 364,445 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400234 | 3.1 Wiese / Weide (gemeinsam) | 6 | v4 | 465,446 | Grünland; grenzt an Gebäude oder Hof |
| 400236 | 3.1 Wiese / Weide (gemeinsam) | 3 | v4 | 336,446 | Grünland; grenzt an Gebäude oder Hof |
| 400245 | 3.1 Wiese / Weide (gemeinsam) | 35 | v4 | 532,477 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400246 | 3.1 Wiese / Weide (gemeinsam) | 4 | v4 | 484,461 | Grünland; grenzt an Gebäude oder Hof |
| 400252 | 3.1 Wiese / Weide (gemeinsam) | 7 | v4 | 401,472 | Grünland; grenzt an Gebäude oder Hof |
| 400255 | 3.1 Wiese / Weide (gemeinsam) | 6 | v4 | 551,474 | Grünland; grenzt an Gebäude oder Hof |
| 400259 | 3.1 Wiese / Weide (gemeinsam) | 67 | v4 | 365,494 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400276 | 3.1 Wiese / Weide (gemeinsam) | 5 | v4 | 375,493 | Grünland; grenzt an Gebäude oder Hof |
| 400277 | 3.1 Wiese / Weide (gemeinsam) | 6 | v4 | 518,495 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400278 | 3.1 Wiese / Weide (gemeinsam) | 9 | v4 | 336,505 | Grünland; grenzt an Gebäude oder Hof |
| 400279 | 3.1 Wiese / Weide (gemeinsam) | 22 | v4 | 544,499 | Grünland; grenzt an Gebäude oder Hof |
| 400282 | 3.1 Wiese / Weide (gemeinsam) | 32 | v4 | 414,510 | Grünland; grenzt an Gebäude oder Hof |
| 400286 | 3.1 Wiese / Weide (gemeinsam) | 15 | v4 | 474,513 | Grünland; grenzt an Gebäude oder Hof |
| 400290 | 3.1 Wiese / Weide (gemeinsam) | 27 | v4 | 547,518 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400294 | 3.1 Wiese / Weide (gemeinsam) | 4 | v4 | 332,512 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400296 | 3.1 Wiese / Weide (gemeinsam) | 20 | v4 | 442,522 | Grünland; grenzt an Gebäude oder Hof |
| 400301 | 3.1 Wiese / Weide (gemeinsam) | 29 | v4 | 489,536 | Grünland; grenzt an Gebäude oder Hof |
| 400310 | 3.1 Wiese / Weide (gemeinsam) | 41 | v4 | 544,540 | Grünland; grenzt an Gebäude oder Hof |
| 400317 | 3.1 Wiese / Weide (gemeinsam) | 18 | v4 | 420,549 | Grünland; grenzt an Gebäude oder Hof |
| 400326 | 3.1 Wiese / Weide (gemeinsam) | 8 | v4 | 429,549 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400334 | 3.1 Wiese / Weide (gemeinsam) | 6 | v4 | 445,558 | Grünland; grenzt an Gebäude oder Hof |
| 400349 | 3.1 Wiese / Weide (gemeinsam) | 0 | v4 | 397,562 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |

## Bei Zweifel

Eine Nahansicht (roh und mit Umriss nebeneinander) macht dieser Befehl im Ordner `C:/Users/Phil/Developement/Victor/landseg`:

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg zoom --manifest C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/manifest.json --teilkachel r1c1 --labels C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/c-feste-liste/r1c1/labels.tif --ids <id> --roh --ziel C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-C-r1c1-3/nah_<id>.jpg
```

Nahansichten nur in diesen Ordner schreiben. Kein Subagent, keine Fenster, nichts installieren, keine Karte ändern.

## Ergebnis

Datei `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-C-r1c1-3/entscheid.json` (UTF-8-JSON), genau ein Eintrag je Kandidaten-ID:

```json
{"<id>": {"garten": "ja" | "nein" | "unklar", "grund": "<ein Satz>"}}
```

„ja“ nur für krautige Grünfläche oder Beet in einem Haus- oder Hofgarten; Gehölz, Weg, Hof, Park, Friedhof, Sportrasen und Wiese oder Acker am Ortsrand ohne Haus „nein“; was du am Bild nicht sicher entscheiden kannst, „unklar“. Rückgabe: Zahl ja / nein / unklar.
