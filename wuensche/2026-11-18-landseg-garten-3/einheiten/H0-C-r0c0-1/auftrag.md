# Garten-Bestätigung H0-C-r0c0-1

Du bist ein Agent des Projekts landseg (Segmentierung von Luftbildern). Antworte auf Deutsch. Regeln: `C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md` (lies sie zuerst, besonders L14 und L15).

## Ziel

Entscheide für jeden der 23 Kandidaten unten am Bild, ob er ein Haus- oder Hofgarten ist und damit die Klasse Garten bekommen soll (in dieser Liste Code `3.6` „Garten (Haus- und Hofgarten: Grünfläche, Beet)“). Du änderst keine Karte und keine Klasse; du schreibst nur die Ergebnisdatei.

## Was „Garten“ ist (Entscheidungen des Nutzers vom 18.11.2026)

- eine einzige Unterklasse „Garten“ unter Dauergrünland (feste Liste: Code 3.6; freie Listen A/B: ihre eigene Klasse Garten unter ihrer Dauergrünland-Klasse, Regel L14 im Skill);
- dazu gehört jede krautige Grünfläche und jedes Beet im Haus- oder Hofgarten (auch Vor-, Obst- und Gemüsegarten), ob gepflegter Rasen oder nicht — Rasen ist kein Kennzeichen;
- nur Haus- und Hofgärten: Parks, Friedhöfe, Sportrasen und Wiesen am Ortsrand bleiben Wiese/Weide;
- Bäume, Sträucher und Hecken im Garten bleiben Gehölz (von oben sieht man die Krone);
- auf dem Schwarz-Weiß-Bild H0 nur klar erkennbare Gärten am Haus; Unklares bleibt, wie es ist.

## Bild

- Bild: H0 SW (Schwarz-Weiß-Scan von 1968, rund 0,45 m je Bildpunkt); auf diesem Schwarz-Weiß-Bild nur klar erkennbare Gärten am Haus mit „ja“, Unklares „unklar“ oder „nein“.
- Fassung C (c-feste-liste), Teilkachel r0c0; Kategorienliste `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/kategorien-c.json`.
- Karte: `C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r0c0/labels.tif`, Teilkachelbild: `C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r0c0.png`.
- Bilder je Viertel (gelb alle Grenzen, magenta die Kandidaten mit Nummer; weißer Rahmen = Kern); jedes nur einmal ansehen:
  - v1: mit Umriss `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-C-r0c0-1/v1_umriss.jpg`, roh daneben `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-C-r0c0-1/v1_roh.jpg`
  - v2: mit Umriss `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-C-r0c0-1/v2_umriss.jpg`, roh daneben `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-C-r0c0-1/v2_roh.jpg`
  - v3: mit Umriss `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-C-r0c0-1/v3_umriss.jpg`, roh daneben `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-C-r0c0-1/v3_roh.jpg`
  - v4: mit Umriss `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-C-r0c0-1/v4_umriss.jpg`, roh daneben `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-C-r0c0-1/v4_roh.jpg`
- Kandidatenliste: `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-C-r0c0-1/kandidaten.json` (id, Klasse, Fläche m², Viertel, Mittelpunkt x,y in Bildpunkten der Teilkachel, Grund der Auswahl).

## Kandidaten

| id | Klasse | Fläche m² | Viertel | Mitte x,y | Grund der Auswahl |
|---|---|---|---|---|---|
| 100033 | 3.4 Krautsaum linear (Feldrain, Wegrand, Böschung) | 128 | v1 | 147,88 | Grünland; grenzt an Gebäude oder Hof |
| 100035 | 3 Dauergrünland (krautig, nicht Acker) | 455 | v1 | 241,88 | Grünland; grenzt an Gebäude oder Hof |
| 100047 | 3.4 Krautsaum linear (Feldrain, Wegrand, Böschung) | 277 | v1 | 111,89 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100051 | 3 Dauergrünland (krautig, nicht Acker) | 698 | v1 | 204,106 | Grünland; grenzt an Gebäude oder Hof |
| 100077 | 3 Dauergrünland (krautig, nicht Acker) | 1270 | v1 | 282,163 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100078 | 3 Dauergrünland (krautig, nicht Acker) | 111 | v1 | 134,131 | Grünland; grenzt an Gebäude oder Hof |
| 100088 | 3.4 Krautsaum linear (Feldrain, Wegrand, Böschung) | 158 | v1 | 93,158 | Grünland; grenzt an Gebäude oder Hof |
| 100097 | 3.4 Krautsaum linear (Feldrain, Wegrand, Böschung) | 42 | v1 | 74,146 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100105 | 6 Offener Boden / Fels | 276 | v1 | 149,189 | offener Boden; grenzt an Gebäude oder Hof |
| 100124 | 3.4 Krautsaum linear (Feldrain, Wegrand, Böschung) | 4 | v1 | 64,204 | Grünland; grenzt an Gebäude oder Hof |
| 100129 | 6 Offener Boden / Fels | 543 | v1 | 89,256 | offener Boden; grenzt an Gebäude oder Hof |
| 100138 | 2 Acker (und Dauerkulturen) | 336 | v1 | 119,252 | Acker klein; grenzt an Gebäude oder Hof |
| 100160 | 3 Dauergrünland (krautig, nicht Acker) | 304 | v1 | 81,312 | Grünland; grenzt an Gebäude oder Hof |
| 100257 | 3.4 Krautsaum linear (Feldrain, Wegrand, Böschung) | 1 | v1 | 172,65 | Grünland; grenzt an Gebäude oder Hof |
| 100012 | 2 Acker (und Dauerkulturen) | 167 | v2 | 489,75 | Acker klein; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100049 | 2 Acker (und Dauerkulturen) | 32 | v2 | 508,68 | Acker klein; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100062 | 3 Dauergrünland (krautig, nicht Acker) | 562 | v2 | 427,127 | Grünland; grenzt an Gebäude oder Hof |
| 100066 | 3 Dauergrünland (krautig, nicht Acker) | 487 | v2 | 379,130 | Grünland; grenzt an Gebäude oder Hof |
| 100069 | 3 Dauergrünland (krautig, nicht Acker) | 105 | v2 | 472,116 | Grünland; grenzt an Gebäude oder Hof |
| 100083 | 2 Acker (und Dauerkulturen) | 977 | v2 | 453,193 | Acker klein; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100251 | 2 Acker (und Dauerkulturen) | 643 | v2 | 509,164 | Acker klein; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100173 | 3 Dauergrünland (krautig, nicht Acker) | 60 | v3 | 70,339 | Grünland; grenzt an Gebäude oder Hof |
| 100178 | 3 Dauergrünland (krautig, nicht Acker) | 228 | v4 | 532,345 | Grünland; grenzt an Gebäude oder Hof |

## Bei Zweifel

Eine Nahansicht (roh und mit Umriss nebeneinander) macht dieser Befehl im Ordner `C:/Users/Phil/Developement/Victor/landseg`:

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg zoom --manifest C:/Users/Phil/Developement/Victor/daten/landseg/H0/manifest.json --teilkachel r0c0 --labels C:/Users/Phil/Developement/Victor/daten/landseg/H0/c-feste-liste/r0c0/labels.tif --ids <id> --roh --ziel C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-C-r0c0-1/nah_<id>.jpg
```

Nahansichten nur in diesen Ordner schreiben. Kein Subagent, keine Fenster, nichts installieren, keine Karte ändern.

## Ergebnis

Datei `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-C-r0c0-1/entscheid.json` (UTF-8-JSON), genau ein Eintrag je Kandidaten-ID:

```json
{"<id>": {"garten": "ja" | "nein" | "unklar", "grund": "<ein Satz>"}}
```

„ja“ nur für krautige Grünfläche oder Beet in einem Haus- oder Hofgarten; Gehölz, Weg, Hof, Park, Friedhof, Sportrasen und Wiese oder Acker am Ortsrand ohne Haus „nein“; was du am Bild nicht sicher entscheiden kannst, „unklar“. Rückgabe: Zahl ja / nein / unklar.
