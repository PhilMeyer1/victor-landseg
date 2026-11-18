# Garten-Bestätigung T0-B-r1c1-1

Du bist ein Agent des Projekts landseg (Segmentierung von Luftbildern). Antworte auf Deutsch. Regeln: `C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md` (lies sie zuerst, besonders L14 und L15).

## Ziel

Entscheide für jeden der 29 Kandidaten unten am Bild, ob er ein Haus- oder Hofgarten ist und damit die Klasse Garten bekommen soll (in dieser Liste Code `2.4` „Garten (Haus- und Hofgarten: Grünfläche, Beet)“). Du änderst keine Karte und keine Klasse; du schreibst nur die Ergebnisdatei.

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
  - v1: mit Umriss `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-B-r1c1-1/v1_umriss.jpg`, roh daneben `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-B-r1c1-1/v1_roh.jpg`
  - v2: mit Umriss `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-B-r1c1-1/v2_umriss.jpg`, roh daneben `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-B-r1c1-1/v2_roh.jpg`
- Kandidatenliste: `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-B-r1c1-1/kandidaten.json` (id, Klasse, Fläche m², Viertel, Mittelpunkt x,y in Bildpunkten der Teilkachel, Grund der Auswahl).

## Kandidaten

| id | Klasse | Fläche m² | Viertel | Mitte x,y | Grund der Auswahl |
|---|---|---|---|---|---|
| 400037 | 3.3.2 Parzelle gemischt | 42 | v1 | 270,195 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400060 | 2.2 Rasen | 18 | v1 | 220,223 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400061 | 2.2 Rasen | 7 | v1 | 293,219 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400063 | 2.2 Rasen | 98 | v1 | 255,247 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400088 | 2.2 Rasen | 10 | v1 | 313,258 | Grünland; grenzt an Gebäude oder Hof |
| 400090 | 2.1 Wiese | 99 | v1 | 205,312 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400102 | 3.3.1 Beete | 8 | v1 | 306,279 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400109 | 2.2 Rasen | 5 | v1 | 292,288 | Grünland; grenzt an Gebäude oder Hof |
| 400111 | 2.2 Rasen | 53 | v1 | 309,309 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400120 | 2.2 Rasen | 42 | v1 | 269,307 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400121 | 3.3.1 Beete | 9 | v1 | 234,299 | Grünland; grenzt an Gebäude oder Hof |
| 400125 | 2.2 Rasen | 9 | v1 | 202,308 | Grünland; grenzt an Gebäude oder Hof |
| 400002 | 2.1 Wiese | 1802 | v2 | 331,145 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400043 | 3.3.2 Parzelle gemischt | 44 | v2 | 348,205 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400053 | 3.3.2 Parzelle gemischt | 27 | v2 | 352,220 | Grünland; grenzt an Gebäude oder Hof |
| 400056 | 3.3.1 Beete | 19 | v2 | 382,223 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400058 | 3.3.2 Parzelle gemischt | 95 | v2 | 438,238 | Grünland; grenzt an Gebäude oder Hof |
| 400062 | 2.2 Rasen | 4 | v2 | 322,224 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400065 | 2.1 Wiese | 6 | v2 | 505,223 | Grünland; grenzt an Gebäude oder Hof |
| 400075 | 2.2 Rasen | 33 | v2 | 556,276 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400076 | 3.3.1 Beete | 7 | v2 | 433,243 | Grünland; grenzt an Gebäude oder Hof |
| 400079 | 2.2 Rasen | 23 | v2 | 383,248 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400091 | 2.2 Rasen | 61 | v2 | 501,269 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400092 | 2.2 Rasen | 4 | v2 | 336,253 | Grünland; grenzt an Gebäude oder Hof |
| 400096 | 3.3.2 Parzelle gemischt | 23 | v2 | 362,272 | Grünland; grenzt an Gebäude oder Hof |
| 400105 | 3.3.2 Parzelle gemischt | 25 | v2 | 474,296 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400107 | 2.2 Rasen | 29 | v2 | 348,299 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400114 | 2.2 Rasen | 10 | v2 | 357,293 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 400131 | 2.2 Rasen | 8 | v2 | 449,314 | Grünland; grenzt an Gebäude oder Hof |

## Bei Zweifel

Eine Nahansicht (roh und mit Umriss nebeneinander) macht dieser Befehl im Ordner `C:/Users/Phil/Developement/Victor/landseg`:

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg zoom --manifest C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/manifest.json --teilkachel r1c1 --labels C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/b-kategorien-frei/r1c1/labels.tif --ids <id> --roh --ziel C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-B-r1c1-1/nah_<id>.jpg
```

Nahansichten nur in diesen Ordner schreiben. Kein Subagent, keine Fenster, nichts installieren, keine Karte ändern.

## Ergebnis

Datei `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-B-r1c1-1/entscheid.json` (UTF-8-JSON), genau ein Eintrag je Kandidaten-ID:

```json
{"<id>": {"garten": "ja" | "nein" | "unklar", "grund": "<ein Satz>"}}
```

„ja“ nur für krautige Grünfläche oder Beet in einem Haus- oder Hofgarten; Gehölz, Weg, Hof, Park, Friedhof, Sportrasen und Wiese oder Acker am Ortsrand ohne Haus „nein“; was du am Bild nicht sicher entscheiden kannst, „unklar“. Rückgabe: Zahl ja / nein / unklar.
