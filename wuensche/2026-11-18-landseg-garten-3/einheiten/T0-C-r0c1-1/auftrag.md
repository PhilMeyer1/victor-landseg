# Garten-Bestätigung T0-C-r0c1-1

Du bist ein Agent des Projekts landseg (Segmentierung von Luftbildern). Antworte auf Deutsch. Regeln: `C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md` (lies sie zuerst, besonders L14 und L15).

## Ziel

Entscheide für jeden der 15 Kandidaten unten am Bild, ob er ein Haus- oder Hofgarten ist und damit die Klasse Garten bekommen soll (in dieser Liste Code `3.6` „Garten (Haus- und Hofgarten: Grünfläche, Beet)“). Du änderst keine Karte und keine Klasse; du schreibst nur die Ergebnisdatei.

## Was „Garten“ ist (Entscheidungen des Nutzers vom 18.11.2026)

- eine einzige Unterklasse „Garten“ unter Dauergrünland (feste Liste: Code 3.6; freie Listen A/B: ihre eigene Klasse Garten unter ihrer Dauergrünland-Klasse, Regel L14 im Skill);
- dazu gehört jede krautige Grünfläche und jedes Beet im Haus- oder Hofgarten (auch Vor-, Obst- und Gemüsegarten), ob gepflegter Rasen oder nicht — Rasen ist kein Kennzeichen;
- nur Haus- und Hofgärten: Parks, Friedhöfe, Sportrasen und Wiesen am Ortsrand bleiben Wiese/Weide;
- Bäume, Sträucher und Hecken im Garten bleiben Gehölz (von oben sieht man die Krone);
- auf dem Schwarz-Weiß-Bild H0 nur klar erkennbare Gärten am Haus; Unklares bleibt, wie es ist.

## Bild

- Bild: T0 Farbe (Farb-Orthofoto, rund 0,2 m je Bildpunkt).
- Fassung C (c-feste-liste), Teilkachel r0c1; Kategorienliste `C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/c-feste-liste/kategorien-c.json`.
- Karte: `C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/c-feste-liste/r0c1/labels.tif`, Teilkachelbild: `C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/teilkacheln/r0c1.png`.
- Bilder je Viertel (gelb alle Grenzen, magenta die Kandidaten mit Nummer; weißer Rahmen = Kern); jedes nur einmal ansehen:
  - v1: mit Umriss `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-C-r0c1-1/v1_umriss.jpg`, roh daneben `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-C-r0c1-1/v1_roh.jpg`
  - v2: mit Umriss `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-C-r0c1-1/v2_umriss.jpg`, roh daneben `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-C-r0c1-1/v2_roh.jpg`
  - v3: mit Umriss `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-C-r0c1-1/v3_umriss.jpg`, roh daneben `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-C-r0c1-1/v3_roh.jpg`
- Kandidatenliste: `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-C-r0c1-1/kandidaten.json` (id, Klasse, Fläche m², Viertel, Mittelpunkt x,y in Bildpunkten der Teilkachel, Grund der Auswahl).

## Kandidaten

| id | Klasse | Fläche m² | Viertel | Mitte x,y | Grund der Auswahl |
|---|---|---|---|---|---|
| 200100 | 3.4 Krautsaum linear (Feldrain, Wegrand, Böschung) | 6 | v1 | 74,159 | Grünland; grenzt an Gebäude oder Hof |
| 200128 | 3.1 Wiese / Weide (gemeinsam) | 31 | v1 | 171,230 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 200013 | 3.1 Wiese / Weide (gemeinsam) | 2 | v2 | 387,66 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 200078 | 3.1 Wiese / Weide (gemeinsam) | 22 | v2 | 455,143 | Grünland; grenzt an Gebäude oder Hof |
| 200083 | 3.1 Wiese / Weide (gemeinsam) | 91 | v2 | 543,167 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 200104 | 3.1 Wiese / Weide (gemeinsam) | 157 | v2 | 424,208 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 200113 | 3.1 Wiese / Weide (gemeinsam) | 1 | v2 | 561,182 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 200119 | 3.1 Wiese / Weide (gemeinsam) | 5 | v2 | 531,188 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 200129 | 3.1 Wiese / Weide (gemeinsam) | 6 | v2 | 378,219 | Grünland; grenzt an Gebäude oder Hof |
| 200143 | 3.1 Wiese / Weide (gemeinsam) | 294 | v3 | 314,345 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 200157 | 3.1 Wiese / Weide (gemeinsam) | 10 | v3 | 244,348 | Grünland; grenzt an Gebäude oder Hof |
| 200171 | 3.4 Krautsaum linear (Feldrain, Wegrand, Böschung) | 148 | v3 | 300,402 | Grünland; grenzt an Gebäude oder Hof |
| 200187 | 3.1.1 Wiese (Mahdspuren sichtbar) | 4 | v3 | 230,427 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 200188 | 3.1.1 Wiese (Mahdspuren sichtbar) | 4 | v3 | 211,428 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 200191 | 3.1.1 Wiese (Mahdspuren sichtbar) | 8 | v3 | 227,499 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |

## Bei Zweifel

Eine Nahansicht (roh und mit Umriss nebeneinander) macht dieser Befehl im Ordner `C:/Users/Phil/Developement/Victor/landseg`:

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg zoom --manifest C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/manifest.json --teilkachel r0c1 --labels C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/c-feste-liste/r0c1/labels.tif --ids <id> --roh --ziel C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-C-r0c1-1/nah_<id>.jpg
```

Nahansichten nur in diesen Ordner schreiben. Kein Subagent, keine Fenster, nichts installieren, keine Karte ändern.

## Ergebnis

Datei `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-C-r0c1-1/entscheid.json` (UTF-8-JSON), genau ein Eintrag je Kandidaten-ID:

```json
{"<id>": {"garten": "ja" | "nein" | "unklar", "grund": "<ein Satz>"}}
```

„ja“ nur für krautige Grünfläche oder Beet in einem Haus- oder Hofgarten; Gehölz, Weg, Hof, Park, Friedhof, Sportrasen und Wiese oder Acker am Ortsrand ohne Haus „nein“; was du am Bild nicht sicher entscheiden kannst, „unklar“. Rückgabe: Zahl ja / nein / unklar.
