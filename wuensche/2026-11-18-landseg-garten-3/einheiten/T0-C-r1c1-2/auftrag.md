# Garten-Bestätigung T0-C-r1c1-2

Du bist ein Agent des Projekts landseg (Segmentierung von Luftbildern). Antworte auf Deutsch. Regeln: `C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md` (lies sie zuerst, besonders L14 und L15).

## Ziel

Entscheide für jeden der 33 Kandidaten unten am Bild, ob er ein Haus- oder Hofgarten ist und damit die Klasse Garten bekommen soll (in dieser Liste Code `3.6` „Garten (Haus- und Hofgarten: Grünfläche, Beet)“). Du änderst keine Karte und keine Klasse; du schreibst nur die Ergebnisdatei.

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
  - v3: mit Umriss `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-C-r1c1-2/v3_umriss.jpg`, roh daneben `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-C-r1c1-2/v3_roh.jpg`
- Kandidatenliste: `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-C-r1c1-2/kandidaten.json` (id, Klasse, Fläche m², Viertel, Mittelpunkt x,y in Bildpunkten der Teilkachel, Grund der Auswahl).

## Kandidaten

| id | Klasse | Fläche m² | Viertel | Mitte x,y | Grund der Auswahl |
|---|---|---|---|---|---|
| 400133 | 3.1 Wiese / Weide (gemeinsam) | 8 | v3 | 291,326 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400141 | 3.1 Wiese / Weide (gemeinsam) | 4 | v3 | 242,325 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400144 | 3.1 Wiese / Weide (gemeinsam) | 83 | v3 | 252,350 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400146 | 3.1 Wiese / Weide (gemeinsam) | 102 | v3 | 278,382 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400148 | 3.1 Wiese / Weide (gemeinsam) | 5 | v3 | 280,331 | Grünland; grenzt an Gebäude oder Hof |
| 400158 | 3.1 Wiese / Weide (gemeinsam) | 5 | v3 | 187,344 | Grünland; grenzt an Gebäude oder Hof |
| 400164 | 3.1 Wiese / Weide (gemeinsam) | 6 | v3 | 175,359 | Grünland; grenzt an Gebäude oder Hof |
| 400175 | 3.1 Wiese / Weide (gemeinsam) | 33 | v3 | 182,379 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400177 | 2.1 Acker mit Bewuchs | 309 | v3 | 143,440 | Acker klein; grenzt an Gebäude oder Hof |
| 400186 | 3.1 Wiese / Weide (gemeinsam) | 5 | v3 | 244,377 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400199 | 3.1 Wiese / Weide (gemeinsam) | 63 | v3 | 217,417 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400216 | 3.1 Wiese / Weide (gemeinsam) | 127 | v3 | 234,476 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400220 | 3.1 Wiese / Weide (gemeinsam) | 11 | v3 | 197,431 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400224 | 3.1 Wiese / Weide (gemeinsam) | 6 | v3 | 260,428 | Grünland; grenzt an Gebäude oder Hof |
| 400228 | 3.1 Wiese / Weide (gemeinsam) | 6 | v3 | 197,439 | Grünland; grenzt an Gebäude oder Hof |
| 400232 | 3.1 Wiese / Weide (gemeinsam) | 124 | v3 | 308,513 | Grünland; grenzt an Gebäude oder Hof |
| 400240 | 3.1 Wiese / Weide (gemeinsam) | 18 | v3 | 178,470 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400249 | 3.1 Wiese / Weide (gemeinsam) | 7 | v3 | 147,466 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400261 | 3.1 Wiese / Weide (gemeinsam) | 8 | v3 | 138,477 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400269 | 3.1 Wiese / Weide (gemeinsam) | 10 | v3 | 205,483 | Grünland; grenzt an Gebäude oder Hof |
| 400270 | 3.1 Wiese / Weide (gemeinsam) | 46 | v3 | 187,497 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400271 | 3.1 Wiese / Weide (gemeinsam) | 10 | v3 | 276,487 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400287 | 3.1 Wiese / Weide (gemeinsam) | 38 | v3 | 284,521 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400291 | 3.1 Wiese / Weide (gemeinsam) | 15 | v3 | 132,514 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400309 | 3.1 Wiese / Weide (gemeinsam) | 34 | v3 | 189,544 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400311 | 3.1 Wiese / Weide (gemeinsam) | 42 | v3 | 253,543 | Grünland; grenzt an Gebäude oder Hof |
| 400315 | 3.1 Wiese / Weide (gemeinsam) | 8 | v3 | 269,538 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400316 | 3.1 Wiese / Weide (gemeinsam) | 10 | v3 | 108,543 | Grünland; grenzt an Gebäude oder Hof |
| 400323 | 3.1 Wiese / Weide (gemeinsam) | 7 | v3 | 293,547 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400329 | 2.1 Acker mit Bewuchs | 24 | v3 | 264,557 | Acker klein; grenzt an Gebäude oder Hof |
| 400332 | 3.1 Wiese / Weide (gemeinsam) | 2 | v3 | 124,558 | Grünland; grenzt an Gebäude oder Hof |
| 400346 | 3.1 Wiese / Weide (gemeinsam) | 2 | v3 | 138,562 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400347 | 3.1 Wiese / Weide (gemeinsam) | 1 | v3 | 314,562 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |

## Bei Zweifel

Eine Nahansicht (roh und mit Umriss nebeneinander) macht dieser Befehl im Ordner `C:/Users/Phil/Developement/Victor/landseg`:

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg zoom --manifest C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/manifest.json --teilkachel r1c1 --labels C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/c-feste-liste/r1c1/labels.tif --ids <id> --roh --ziel C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-C-r1c1-2/nah_<id>.jpg
```

Nahansichten nur in diesen Ordner schreiben. Kein Subagent, keine Fenster, nichts installieren, keine Karte ändern.

## Ergebnis

Datei `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-C-r1c1-2/entscheid.json` (UTF-8-JSON), genau ein Eintrag je Kandidaten-ID:

```json
{"<id>": {"garten": "ja" | "nein" | "unklar", "grund": "<ein Satz>"}}
```

„ja“ nur für krautige Grünfläche oder Beet in einem Haus- oder Hofgarten; Gehölz, Weg, Hof, Park, Friedhof, Sportrasen und Wiese oder Acker am Ortsrand ohne Haus „nein“; was du am Bild nicht sicher entscheiden kannst, „unklar“. Rückgabe: Zahl ja / nein / unklar.
