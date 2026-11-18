# Garten-Bestätigung T0-A-r0c0-1

Du bist ein Agent des Projekts landseg (Segmentierung von Luftbildern). Antworte auf Deutsch. Regeln: `C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md` (lies sie zuerst, besonders L14 und L15).

## Ziel

Entscheide für jeden der 13 Kandidaten unten am Bild, ob er ein Haus- oder Hofgarten ist und damit die Klasse Garten bekommen soll (in dieser Liste Code `4.4` „Garten (Haus- und Hofgarten: Grünfläche, Beet)“). Du änderst keine Karte und keine Klasse; du schreibst nur die Ergebnisdatei.

## Was „Garten“ ist (Entscheidungen des Nutzers vom 18.11.2026)

- eine einzige Unterklasse „Garten“ unter Dauergrünland (feste Liste: Code 3.6; freie Listen A/B: ihre eigene Klasse Garten unter ihrer Dauergrünland-Klasse, Regel L14 im Skill);
- dazu gehört jede krautige Grünfläche und jedes Beet im Haus- oder Hofgarten (auch Vor-, Obst- und Gemüsegarten), ob gepflegter Rasen oder nicht — Rasen ist kein Kennzeichen;
- nur Haus- und Hofgärten: Parks, Friedhöfe, Sportrasen und Wiesen am Ortsrand bleiben Wiese/Weide;
- Bäume, Sträucher und Hecken im Garten bleiben Gehölz (von oben sieht man die Krone);
- auf dem Schwarz-Weiß-Bild H0 nur klar erkennbare Gärten am Haus; Unklares bleibt, wie es ist.

## Bild

- Bild: T0 Farbe (Farb-Orthofoto, rund 0,2 m je Bildpunkt).
- Fassung A (a-alles-frei), Teilkachel r0c0; Kategorienliste `C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/a-alles-frei/kategorien-a.json`.
- Karte: `C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/a-alles-frei/r0c0/labels.tif`, Teilkachelbild: `C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/teilkacheln/r0c0.png`.
- Bilder je Viertel (gelb alle Grenzen, magenta die Kandidaten mit Nummer; weißer Rahmen = Kern); jedes nur einmal ansehen:
  - v1: mit Umriss `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-A-r0c0-1/v1_umriss.jpg`, roh daneben `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-A-r0c0-1/v1_roh.jpg`
  - v2: mit Umriss `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-A-r0c0-1/v2_umriss.jpg`, roh daneben `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-A-r0c0-1/v2_roh.jpg`
  - v4: mit Umriss `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-A-r0c0-1/v4_umriss.jpg`, roh daneben `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-A-r0c0-1/v4_roh.jpg`
- Kandidatenliste: `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-A-r0c0-1/kandidaten.json` (id, Klasse, Fläche m², Viertel, Mittelpunkt x,y in Bildpunkten der Teilkachel, Grund der Auswahl).

## Kandidaten

| id | Klasse | Fläche m² | Viertel | Mitte x,y | Grund der Auswahl |
|---|---|---|---|---|---|
| 100020 | 4.2 Saum / Feldrain / Böschung | 51 | v1 | 219,77 | Grünland; im Siedlungsgebiet (Mehrheit der Bildpunkte in Fassung C) |
| 100022 | 3.2 Gemischte Gartenfläche | 51 | v1 | 279,75 | Grünland; im Siedlungsgebiet (Mehrheit der Bildpunkte in Fassung C) |
| 100033 | 3.2 Gemischte Gartenfläche | 5 | v2 | 547,69 | Grünland; grenzt an Gebäude oder Hof |
| 100040 | 3.1 Gartenrasen | 119 | v2 | 414,94 | Grünland; im Siedlungsgebiet (Mehrheit der Bildpunkte in Fassung C) |
| 100043 | 3.2 Gemischte Gartenfläche | 4 | v2 | 554,116 | Grünland; im Siedlungsgebiet (Mehrheit der Bildpunkte in Fassung C) |
| 100044 | 3.2 Gemischte Gartenfläche | 23 | v2 | 551,101 | Grünland; im Siedlungsgebiet (Mehrheit der Bildpunkte in Fassung C) |
| 100050 | 3.2 Gemischte Gartenfläche | 91 | v2 | 422,132 | Grünland; im Siedlungsgebiet (Mehrheit der Bildpunkte in Fassung C) |
| 100051 | 4.2 Saum / Feldrain / Böschung | 4 | v2 | 423,147 | Grünland; im Siedlungsgebiet (Mehrheit der Bildpunkte in Fassung C) |
| 100055 | 3.2 Gemischte Gartenfläche | 12 | v2 | 526,124 | Grünland; im Siedlungsgebiet (Mehrheit der Bildpunkte in Fassung C) |
| 100058 | 4.2 Saum / Feldrain / Böschung | 7 | v2 | 552,158 | Grünland; grenzt an Gebäude oder Hof |
| 100079 | 3.1 Gartenrasen | 282 | v2 | 387,264 | Grünland; im Siedlungsgebiet (Mehrheit der Bildpunkte in Fassung C) |
| 100099 | 3.1 Gartenrasen | 105 | v4 | 460,322 | Grünland; im Siedlungsgebiet (Mehrheit der Bildpunkte in Fassung C) |
| 100104 | 4.1.1 Wiese ungemäht / langgrasig | 245 | v4 | 462,366 | Grünland; im Siedlungsgebiet (Mehrheit der Bildpunkte in Fassung C) |

## Bei Zweifel

Eine Nahansicht (roh und mit Umriss nebeneinander) macht dieser Befehl im Ordner `C:/Users/Phil/Developement/Victor/landseg`:

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg zoom --manifest C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/manifest.json --teilkachel r0c0 --labels C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/a-alles-frei/r0c0/labels.tif --ids <id> --roh --ziel C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-A-r0c0-1/nah_<id>.jpg
```

Nahansichten nur in diesen Ordner schreiben. Kein Subagent, keine Fenster, nichts installieren, keine Karte ändern.

## Ergebnis

Datei `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-A-r0c0-1/entscheid.json` (UTF-8-JSON), genau ein Eintrag je Kandidaten-ID:

```json
{"<id>": {"garten": "ja" | "nein" | "unklar", "grund": "<ein Satz>"}}
```

„ja“ nur für krautige Grünfläche oder Beet in einem Haus- oder Hofgarten; Gehölz, Weg, Hof, Park, Friedhof, Sportrasen und Wiese oder Acker am Ortsrand ohne Haus „nein“; was du am Bild nicht sicher entscheiden kannst, „unklar“. Rückgabe: Zahl ja / nein / unklar.
