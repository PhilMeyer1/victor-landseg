# Garten-Bestätigung T0-A-r1c1-3

Du bist ein Agent des Projekts landseg (Segmentierung von Luftbildern). Antworte auf Deutsch. Regeln: `C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md` (lies sie zuerst, besonders L14 und L15).

## Ziel

Entscheide für jeden der 28 Kandidaten unten am Bild, ob er ein Haus- oder Hofgarten ist und damit die Klasse Garten bekommen soll (in dieser Liste Code `4.4` „Garten (Haus- und Hofgarten: Grünfläche, Beet)“). Du änderst keine Karte und keine Klasse; du schreibst nur die Ergebnisdatei.

## Was „Garten“ ist (Entscheidungen des Nutzers vom 18.11.2026)

- eine einzige Unterklasse „Garten“ unter Dauergrünland (feste Liste: Code 3.6; freie Listen A/B: ihre eigene Klasse Garten unter ihrer Dauergrünland-Klasse, Regel L14 im Skill);
- dazu gehört jede krautige Grünfläche und jedes Beet im Haus- oder Hofgarten (auch Vor-, Obst- und Gemüsegarten), ob gepflegter Rasen oder nicht — Rasen ist kein Kennzeichen;
- nur Haus- und Hofgärten: Parks, Friedhöfe, Sportrasen und Wiesen am Ortsrand bleiben Wiese/Weide;
- Bäume, Sträucher und Hecken im Garten bleiben Gehölz (von oben sieht man die Krone);
- auf dem Schwarz-Weiß-Bild H0 nur klar erkennbare Gärten am Haus; Unklares bleibt, wie es ist.

## Bild

- Bild: T0 Farbe (Farb-Orthofoto, rund 0,2 m je Bildpunkt).
- Fassung A (a-alles-frei), Teilkachel r1c1; Kategorienliste `C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/a-alles-frei/kategorien-a.json`.
- Karte: `C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/a-alles-frei/r1c1/labels.tif`, Teilkachelbild: `C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/teilkacheln/r1c1.png`.
- Bilder je Viertel (gelb alle Grenzen, magenta die Kandidaten mit Nummer; weißer Rahmen = Kern); jedes nur einmal ansehen:
  - v4: mit Umriss `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-A-r1c1-3/v4_umriss.jpg`, roh daneben `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-A-r1c1-3/v4_roh.jpg`
- Kandidatenliste: `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-A-r1c1-3/kandidaten.json` (id, Klasse, Fläche m², Viertel, Mittelpunkt x,y in Bildpunkten der Teilkachel, Grund der Auswahl).

## Kandidaten

| id | Klasse | Fläche m² | Viertel | Mitte x,y | Grund der Auswahl |
|---|---|---|---|---|---|
| 400067 | 3.1 Gartenrasen | 472 | v4 | 414,358 | Grünland; im Siedlungsgebiet (Mehrheit der Bildpunkte in Fassung C) |
| 400129 | 3.1 Gartenrasen | 4 | v4 | 559,342 | Grünland; im Siedlungsgebiet (Mehrheit der Bildpunkte in Fassung C) |
| 400142 | 3.3 Gemüse- und Nutzbeete | 13 | v4 | 330,335 | Grünland; im Siedlungsgebiet (Mehrheit der Bildpunkte in Fassung C) |
| 400152 | 3.1 Gartenrasen | 43 | v4 | 325,357 | Grünland; im Siedlungsgebiet (Mehrheit der Bildpunkte in Fassung C) |
| 400159 | 3.1 Gartenrasen | 7 | v4 | 559,357 | Grünland; im Siedlungsgebiet (Mehrheit der Bildpunkte in Fassung C) |
| 400173 | 3.2 Gemischte Gartenfläche | 4 | v4 | 376,366 | Grünland; grenzt an Gebäude oder Hof |
| 400188 | 3.2 Gemischte Gartenfläche | 0 | v4 | 563,385 | Grünland; grenzt an Gebäude oder Hof |
| 400213 | 3.2 Gemischte Gartenfläche | 9 | v4 | 554,415 | Grünland; grenzt an Gebäude oder Hof |
| 400221 | 3.1 Gartenrasen | 0 | v4 | 563,421 | Grünland; im Siedlungsgebiet (Mehrheit der Bildpunkte in Fassung C) |
| 400222 | 3.1 Gartenrasen | 34 | v4 | 550,449 | Grünland; im Siedlungsgebiet (Mehrheit der Bildpunkte in Fassung C) |
| 400226 | 3.1 Gartenrasen | 44 | v4 | 364,445 | Grünland; im Siedlungsgebiet (Mehrheit der Bildpunkte in Fassung C) |
| 400235 | 3.2 Gemischte Gartenfläche | 27 | v4 | 509,453 | Grünland; grenzt an Gebäude oder Hof |
| 400245 | 3.1 Gartenrasen | 35 | v4 | 532,477 | Grünland; im Siedlungsgebiet (Mehrheit der Bildpunkte in Fassung C) |
| 400259 | 3.1 Gartenrasen | 67 | v4 | 365,494 | Grünland; im Siedlungsgebiet (Mehrheit der Bildpunkte in Fassung C) |
| 400278 | 3.2 Gemischte Gartenfläche | 9 | v4 | 336,505 | Grünland; grenzt an Gebäude oder Hof |
| 400282 | 3.2 Gemischte Gartenfläche | 32 | v4 | 414,510 | Grünland; grenzt an Gebäude oder Hof |
| 400286 | 3.2 Gemischte Gartenfläche | 15 | v4 | 474,513 | Grünland; grenzt an Gebäude oder Hof |
| 400290 | 3.1 Gartenrasen | 27 | v4 | 547,518 | Grünland; im Siedlungsgebiet (Mehrheit der Bildpunkte in Fassung C) |
| 400294 | 3.1 Gartenrasen | 4 | v4 | 332,512 | Grünland; im Siedlungsgebiet (Mehrheit der Bildpunkte in Fassung C) |
| 400296 | 3.2 Gemischte Gartenfläche | 20 | v4 | 442,522 | Grünland; grenzt an Gebäude oder Hof |
| 400301 | 3.2 Gemischte Gartenfläche | 29 | v4 | 489,536 | Grünland; grenzt an Gebäude oder Hof |
| 400310 | 3.2 Gemischte Gartenfläche | 41 | v4 | 544,540 | Grünland; grenzt an Gebäude oder Hof |
| 400317 | 3.2 Gemischte Gartenfläche | 18 | v4 | 420,549 | Grünland; grenzt an Gebäude oder Hof |
| 400326 | 3.1 Gartenrasen | 8 | v4 | 429,549 | Grünland; im Siedlungsgebiet (Mehrheit der Bildpunkte in Fassung C) |
| 400349 | 3.1 Gartenrasen | 0 | v4 | 397,562 | Grünland; im Siedlungsgebiet (Mehrheit der Bildpunkte in Fassung C) |
| 400410 | 3.1 Gartenrasen | 117 | v4 | 526,344 | Grünland; im Siedlungsgebiet (Mehrheit der Bildpunkte in Fassung C) |
| 400411 | 3.1 Gartenrasen | 56 | v4 | 471,336 | Grünland; im Siedlungsgebiet (Mehrheit der Bildpunkte in Fassung C) |
| 400412 | 3.1 Gartenrasen | 235 | v4 | 464,461 | Grünland; im Siedlungsgebiet (Mehrheit der Bildpunkte in Fassung C) |

## Bei Zweifel

Eine Nahansicht (roh und mit Umriss nebeneinander) macht dieser Befehl im Ordner `C:/Users/Phil/Developement/Victor/landseg`:

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg zoom --manifest C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/manifest.json --teilkachel r1c1 --labels C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/a-alles-frei/r1c1/labels.tif --ids <id> --roh --ziel C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-A-r1c1-3/nah_<id>.jpg
```

Nahansichten nur in diesen Ordner schreiben. Kein Subagent, keine Fenster, nichts installieren, keine Karte ändern.

## Ergebnis

Datei `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-A-r1c1-3/entscheid.json` (UTF-8-JSON), genau ein Eintrag je Kandidaten-ID:

```json
{"<id>": {"garten": "ja" | "nein" | "unklar", "grund": "<ein Satz>"}}
```

„ja“ nur für krautige Grünfläche oder Beet in einem Haus- oder Hofgarten; Gehölz, Weg, Hof, Park, Friedhof, Sportrasen und Wiese oder Acker am Ortsrand ohne Haus „nein“; was du am Bild nicht sicher entscheiden kannst, „unklar“. Rückgabe: Zahl ja / nein / unklar.
