# Garten-Bestätigung H0-A-r0c1-1

Du bist ein Agent des Projekts landseg (Segmentierung von Luftbildern). Antworte auf Deutsch. Regeln: `C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md` (lies sie zuerst, besonders L14 und L15).

## Ziel

Entscheide für jeden der 19 Kandidaten unten am Bild, ob er ein Haus- oder Hofgarten ist und damit die Klasse Garten bekommen soll (in dieser Liste Code `4.4` „Garten (Haus- und Hofgarten: Grünfläche, Beet)“). Du änderst keine Karte und keine Klasse; du schreibst nur die Ergebnisdatei.

## Was „Garten“ ist (Entscheidungen des Nutzers vom 18.11.2026)

- eine einzige Unterklasse „Garten“ unter Dauergrünland (feste Liste: Code 3.6; freie Listen A/B: ihre eigene Klasse Garten unter ihrer Dauergrünland-Klasse, Regel L14 im Skill);
- dazu gehört jede krautige Grünfläche und jedes Beet im Haus- oder Hofgarten (auch Vor-, Obst- und Gemüsegarten), ob gepflegter Rasen oder nicht — Rasen ist kein Kennzeichen;
- nur Haus- und Hofgärten: Parks, Friedhöfe, Sportrasen und Wiesen am Ortsrand bleiben Wiese/Weide;
- Bäume, Sträucher und Hecken im Garten bleiben Gehölz (von oben sieht man die Krone);
- auf dem Schwarz-Weiß-Bild H0 nur klar erkennbare Gärten am Haus; Unklares bleibt, wie es ist.

## Bild

- Bild: H0 SW (Schwarz-Weiß-Scan von 1968, rund 0,45 m je Bildpunkt); auf diesem Schwarz-Weiß-Bild nur klar erkennbare Gärten am Haus mit „ja“, Unklares „unklar“ oder „nein“.
- Fassung A (a-alles-frei), Teilkachel r0c1; Kategorienliste `C:/Users/Phil/Developement/Victor/daten/landseg/H0/a-alles-frei/kategorien-a.json`.
- Karte: `C:/Users/Phil/Developement/Victor/daten/landseg/H0/a-alles-frei/r0c1/labels.tif`, Teilkachelbild: `C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r0c1.png`.
- Bilder je Viertel (gelb alle Grenzen, magenta die Kandidaten mit Nummer; weißer Rahmen = Kern); jedes nur einmal ansehen:
  - v1: mit Umriss `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-A-r0c1-1/v1_umriss.jpg`, roh daneben `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-A-r0c1-1/v1_roh.jpg`
  - v2: mit Umriss `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-A-r0c1-1/v2_umriss.jpg`, roh daneben `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-A-r0c1-1/v2_roh.jpg`
- Kandidatenliste: `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-A-r0c1-1/kandidaten.json` (id, Klasse, Fläche m², Viertel, Mittelpunkt x,y in Bildpunkten der Teilkachel, Grund der Auswahl).

## Kandidaten

| id | Klasse | Fläche m² | Viertel | Mitte x,y | Grund der Auswahl |
|---|---|---|---|---|---|
| 200090 | 2.2 Garten / Grün im Ort | 187 | v1 | 96,80 | Grünland; grenzt an Gebäude oder Hof |
| 200167 | 2.2 Garten / Grün im Ort | 72 | v1 | 74,114 | Grünland; grenzt an Gebäude oder Hof |
| 200186 | 2.2 Garten / Grün im Ort | 246 | v1 | 214,108 | Grünland; grenzt an Gebäude oder Hof |
| 200283 | 2.2 Garten / Grün im Ort | 270 | v1 | 92,176 | Grünland; grenzt an Gebäude oder Hof |
| 200342 | 2.2 Garten / Grün im Ort | 30 | v1 | 71,228 | Grünland; grenzt an Gebäude oder Hof |
| 200415 | 2.2 Garten / Grün im Ort | 340 | v1 | 84,273 | Grünland; grenzt an Gebäude oder Hof |
| 200429 | 2.2 Garten / Grün im Ort | 209 | v1 | 185,271 | Grünland; grenzt an Gebäude oder Hof |
| 200438 | 2.2 Garten / Grün im Ort | 55 | v1 | 311,251 | Grünland; grenzt an Gebäude oder Hof |
| 200517 | 2.2 Garten / Grün im Ort | 8 | v1 | 214,313 | Grünland; grenzt an Gebäude oder Hof |
| 200529 | 2.2 Garten / Grün im Ort | 79 | v1 | 304,312 | Grünland; grenzt an Gebäude oder Hof |
| 200133 | 2.2 Garten / Grün im Ort | 574 | v2 | 480,85 | Grünland; grenzt an Gebäude oder Hof |
| 200136 | 2.2 Garten / Grün im Ort | 3 | v2 | 502,65 | Grünland; grenzt an Gebäude oder Hof |
| 200214 | 2.2 Garten / Grün im Ort | 0 | v2 | 563,87 | Grünland; grenzt an Gebäude oder Hof |
| 200265 | 2.2 Garten / Grün im Ort | 354 | v2 | 462,155 | Grünland; grenzt an Gebäude oder Hof |
| 200325 | 2.2 Garten / Grün im Ort | 201 | v2 | 531,203 | Grünland; grenzt an Gebäude oder Hof |
| 200373 | 2.2 Garten / Grün im Ort | 103 | v2 | 382,211 | Grünland; grenzt an Gebäude oder Hof |
| 200459 | 2.3 Gartenland mit Reihen | 650 | v2 | 491,268 | Grünland; grenzt an Gebäude oder Hof |
| 200535 | 2.2 Garten / Grün im Ort | 18 | v2 | 352,310 | Grünland; grenzt an Gebäude oder Hof |
| 200543 | 2.2 Garten / Grün im Ort | 58 | v2 | 417,302 | Grünland; grenzt an Gebäude oder Hof |

## Bei Zweifel

Eine Nahansicht (roh und mit Umriss nebeneinander) macht dieser Befehl im Ordner `C:/Users/Phil/Developement/Victor/landseg`:

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg zoom --manifest C:/Users/Phil/Developement/Victor/daten/landseg/H0/manifest.json --teilkachel r0c1 --labels C:/Users/Phil/Developement/Victor/daten/landseg/H0/a-alles-frei/r0c1/labels.tif --ids <id> --roh --ziel C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-A-r0c1-1/nah_<id>.jpg
```

Nahansichten nur in diesen Ordner schreiben. Kein Subagent, keine Fenster, nichts installieren, keine Karte ändern.

## Ergebnis

Datei `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-A-r0c1-1/entscheid.json` (UTF-8-JSON), genau ein Eintrag je Kandidaten-ID:

```json
{"<id>": {"garten": "ja" | "nein" | "unklar", "grund": "<ein Satz>"}}
```

„ja“ nur für krautige Grünfläche oder Beet in einem Haus- oder Hofgarten; Gehölz, Weg, Hof, Park, Friedhof, Sportrasen und Wiese oder Acker am Ortsrand ohne Haus „nein“; was du am Bild nicht sicher entscheiden kannst, „unklar“. Rückgabe: Zahl ja / nein / unklar.
