# Garten-Bestätigung H0-A-r0c1-2

Du bist ein Agent des Projekts landseg (Segmentierung von Luftbildern). Antworte auf Deutsch. Regeln: `C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md` (lies sie zuerst, besonders L14 und L15).

## Ziel

Entscheide für jeden der 26 Kandidaten unten am Bild, ob er ein Haus- oder Hofgarten ist und damit die Klasse Garten bekommen soll (in dieser Liste Code `4.4` „Garten (Haus- und Hofgarten: Grünfläche, Beet)“). Du änderst keine Karte und keine Klasse; du schreibst nur die Ergebnisdatei.

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
  - v3: mit Umriss `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-A-r0c1-2/v3_umriss.jpg`, roh daneben `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-A-r0c1-2/v3_roh.jpg`
  - v4: mit Umriss `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-A-r0c1-2/v4_umriss.jpg`, roh daneben `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-A-r0c1-2/v4_roh.jpg`
- Kandidatenliste: `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-A-r0c1-2/kandidaten.json` (id, Klasse, Fläche m², Viertel, Mittelpunkt x,y in Bildpunkten der Teilkachel, Grund der Auswahl).

## Kandidaten

| id | Klasse | Fläche m² | Viertel | Mitte x,y | Grund der Auswahl |
|---|---|---|---|---|---|
| 200585 | 2.2 Garten / Grün im Ort | 199 | v3 | 87,335 | Grünland; grenzt an Gebäude oder Hof |
| 200607 | 2.2 Garten / Grün im Ort | 144 | v3 | 124,339 | Grünland; grenzt an Gebäude oder Hof |
| 200612 | 2.2 Garten / Grün im Ort | 104 | v3 | 140,334 | Grünland; grenzt an Gebäude oder Hof |
| 200691 | 2.2 Garten / Grün im Ort | 34 | v3 | 71,370 | Grünland; grenzt an Gebäude oder Hof |
| 200704 | 2.2 Garten / Grün im Ort | 125 | v3 | 96,385 | Grünland; grenzt an Gebäude oder Hof |
| 200724 | 2.2 Garten / Grün im Ort | 78 | v3 | 163,362 | Grünland; grenzt an Gebäude oder Hof |
| 200790 | 2.2 Garten / Grün im Ort | 63 | v3 | 91,437 | Grünland; grenzt an Gebäude oder Hof |
| 200799 | 2.2 Garten / Grün im Ort | 189 | v3 | 117,429 | Grünland; grenzt an Gebäude oder Hof |
| 200890 | 2.2 Garten / Grün im Ort | 127 | v3 | 145,476 | Grünland; grenzt an Gebäude oder Hof |
| 200907 | 2.2 Garten / Grün im Ort | 175 | v3 | 200,458 | Grünland; grenzt an Gebäude oder Hof |
| 201008 | 4.1 Anger / Dorfplatz | 118 | v3 | 277,481 | Grünland; grenzt an Gebäude oder Hof |
| 201041 | 2.2 Garten / Grün im Ort | 0 | v3 | 64,548 | Grünland; grenzt an Gebäude oder Hof |
| 201061 | 2.2 Garten / Grün im Ort | 137 | v3 | 133,540 | Grünland; grenzt an Gebäude oder Hof |
| 201093 | 2.2 Garten / Grün im Ort | 33 | v3 | 213,555 | Grünland; grenzt an Gebäude oder Hof |
| 201113 | 2.2 Garten / Grün im Ort | 29 | v3 | 264,558 | Grünland; grenzt an Gebäude oder Hof |
| 200639 | 2.2 Garten / Grün im Ort | 167 | v4 | 371,328 | Grünland; grenzt an Gebäude oder Hof |
| 200650 | 2.2 Garten / Grün im Ort | 131 | v4 | 428,340 | Grünland; grenzt an Gebäude oder Hof |
| 200744 | 2.2 Garten / Grün im Ort | 890 | v4 | 335,365 | Grünland; grenzt an Gebäude oder Hof |
| 200838 | 2.2 Garten / Grün im Ort | 159 | v4 | 389,423 | Grünland; grenzt an Gebäude oder Hof |
| 200941 | 2.2 Garten / Grün im Ort | 124 | v4 | 553,439 | Grünland; grenzt an Gebäude oder Hof |
| 200942 | 2.2 Garten / Grün im Ort | 1 | v4 | 563,474 | Grünland; grenzt an Gebäude oder Hof |
| 201022 | 2.2 Garten / Grün im Ort | 350 | v4 | 494,506 | Grünland; grenzt an Gebäude oder Hof |
| 201027 | 2.2 Garten / Grün im Ort | 116 | v4 | 518,494 | Grünland; grenzt an Gebäude oder Hof |
| 201115 | 4.1 Anger / Dorfplatz | 544 | v4 | 332,529 | Grünland; grenzt an Gebäude oder Hof |
| 201141 | 2.2 Garten / Grün im Ort | 51 | v4 | 558,519 | Grünland; grenzt an Gebäude oder Hof |
| 201228 | 2.2 Garten / Grün im Ort | 9 | v4 | 333,561 | Grünland; grenzt an Gebäude oder Hof |

## Bei Zweifel

Eine Nahansicht (roh und mit Umriss nebeneinander) macht dieser Befehl im Ordner `C:/Users/Phil/Developement/Victor/landseg`:

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg zoom --manifest C:/Users/Phil/Developement/Victor/daten/landseg/H0/manifest.json --teilkachel r0c1 --labels C:/Users/Phil/Developement/Victor/daten/landseg/H0/a-alles-frei/r0c1/labels.tif --ids <id> --roh --ziel C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-A-r0c1-2/nah_<id>.jpg
```

Nahansichten nur in diesen Ordner schreiben. Kein Subagent, keine Fenster, nichts installieren, keine Karte ändern.

## Ergebnis

Datei `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-A-r0c1-2/entscheid.json` (UTF-8-JSON), genau ein Eintrag je Kandidaten-ID:

```json
{"<id>": {"garten": "ja" | "nein" | "unklar", "grund": "<ein Satz>"}}
```

„ja“ nur für krautige Grünfläche oder Beet in einem Haus- oder Hofgarten; Gehölz, Weg, Hof, Park, Friedhof, Sportrasen und Wiese oder Acker am Ortsrand ohne Haus „nein“; was du am Bild nicht sicher entscheiden kannst, „unklar“. Rückgabe: Zahl ja / nein / unklar.
