# Garten-Bestätigung H0-B-r0c1-1

Du bist ein Agent des Projekts landseg (Segmentierung von Luftbildern). Antworte auf Deutsch. Regeln: `C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md` (lies sie zuerst, besonders L14 und L15).

## Ziel

Entscheide für jeden der 10 Kandidaten unten am Bild, ob er ein Haus- oder Hofgarten ist und damit die Klasse Garten bekommen soll (in dieser Liste Code `5.3` „Garten (Haus- und Hofgarten: Grünfläche, Beet)“). Du änderst keine Karte und keine Klasse; du schreibst nur die Ergebnisdatei.

## Was „Garten“ ist (Entscheidungen des Nutzers vom 18.11.2026)

- eine einzige Unterklasse „Garten“ unter Dauergrünland (feste Liste: Code 3.6; freie Listen A/B: ihre eigene Klasse Garten unter ihrer Dauergrünland-Klasse, Regel L14 im Skill);
- dazu gehört jede krautige Grünfläche und jedes Beet im Haus- oder Hofgarten (auch Vor-, Obst- und Gemüsegarten), ob gepflegter Rasen oder nicht — Rasen ist kein Kennzeichen;
- nur Haus- und Hofgärten: Parks, Friedhöfe, Sportrasen und Wiesen am Ortsrand bleiben Wiese/Weide;
- Bäume, Sträucher und Hecken im Garten bleiben Gehölz (von oben sieht man die Krone);
- auf dem Schwarz-Weiß-Bild H0 nur klar erkennbare Gärten am Haus; Unklares bleibt, wie es ist.

## Bild

- Bild: H0 SW (Schwarz-Weiß-Scan von 1968, rund 0,45 m je Bildpunkt); auf diesem Schwarz-Weiß-Bild nur klar erkennbare Gärten am Haus mit „ja“, Unklares „unklar“ oder „nein“.
- Fassung B (b-kategorien-frei), Teilkachel r0c1; Kategorienliste `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/kategorien-b.json`.
- Karte: `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r0c1/labels.tif`, Teilkachelbild: `C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r0c1.png`.
- Bilder je Viertel (gelb alle Grenzen, magenta die Kandidaten mit Nummer; weißer Rahmen = Kern); jedes nur einmal ansehen:
  - v1: mit Umriss `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-B-r0c1-1/v1_umriss.jpg`, roh daneben `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-B-r0c1-1/v1_roh.jpg`
  - v2: mit Umriss `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-B-r0c1-1/v2_umriss.jpg`, roh daneben `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-B-r0c1-1/v2_roh.jpg`
  - v4: mit Umriss `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-B-r0c1-1/v4_umriss.jpg`, roh daneben `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-B-r0c1-1/v4_roh.jpg`
- Kandidatenliste: `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-B-r0c1-1/kandidaten.json` (id, Klasse, Fläche m², Viertel, Mittelpunkt x,y in Bildpunkten der Teilkachel, Grund der Auswahl).

## Kandidaten

| id | Klasse | Fläche m² | Viertel | Mitte x,y | Grund der Auswahl |
|---|---|---|---|---|---|
| 200199 | 2.2 Gartenfläche am Hof (bisher „Garten“) | 787 | v1 | 255,275 | Grünland; grenzt an Gebäude oder Hof |
| 200202 | 2.2 Gartenfläche am Hof (bisher „Garten“) | 804 | v1 | 204,300 | Grünland; grenzt an Gebäude oder Hof |
| 200225 | 2.2 Gartenfläche am Hof (bisher „Garten“) | 272 | v1 | 177,255 | Grünland; grenzt an Gebäude oder Hof |
| 200058 | 2.2 Gartenfläche am Hof (bisher „Garten“) | 603 | v2 | 502,265 | Grünland; grenzt an Gebäude oder Hof |
| 200218 | 2.2 Gartenfläche am Hof (bisher „Garten“) | 355 | v2 | 454,291 | Grünland; grenzt an Gebäude oder Hof |
| 200273 | 2.2 Gartenfläche am Hof (bisher „Garten“) | 258 | v2 | 538,95 | Grünland; grenzt an Gebäude oder Hof |
| 200274 | 2.2 Gartenfläche am Hof (bisher „Garten“) | 158 | v2 | 468,75 | Grünland; grenzt an Gebäude oder Hof |
| 200071 | 2.2 Gartenfläche am Hof (bisher „Garten“) | 1181 | v4 | 334,375 | Grünland; grenzt an Gebäude oder Hof |
| 200097 | 5.2.1 Anger | 635 | v4 | 338,534 | Grünland; grenzt an Gebäude oder Hof |
| 200226 | 2.2 Gartenfläche am Hof (bisher „Garten“) | 257 | v4 | 373,325 | Grünland; grenzt an Gebäude oder Hof |

## Bei Zweifel

Eine Nahansicht (roh und mit Umriss nebeneinander) macht dieser Befehl im Ordner `C:/Users/Phil/Developement/Victor/landseg`:

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg zoom --manifest C:/Users/Phil/Developement/Victor/daten/landseg/H0/manifest.json --teilkachel r0c1 --labels C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r0c1/labels.tif --ids <id> --roh --ziel C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-B-r0c1-1/nah_<id>.jpg
```

Nahansichten nur in diesen Ordner schreiben. Kein Subagent, keine Fenster, nichts installieren, keine Karte ändern.

## Ergebnis

Datei `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-B-r0c1-1/entscheid.json` (UTF-8-JSON), genau ein Eintrag je Kandidaten-ID:

```json
{"<id>": {"garten": "ja" | "nein" | "unklar", "grund": "<ein Satz>"}}
```

„ja“ nur für krautige Grünfläche oder Beet in einem Haus- oder Hofgarten; Gehölz, Weg, Hof, Park, Friedhof, Sportrasen und Wiese oder Acker am Ortsrand ohne Haus „nein“; was du am Bild nicht sicher entscheiden kannst, „unklar“. Rückgabe: Zahl ja / nein / unklar.
