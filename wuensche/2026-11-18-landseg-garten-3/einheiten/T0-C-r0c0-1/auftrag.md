# Garten-Bestätigung T0-C-r0c0-1

Du bist ein Agent des Projekts landseg (Segmentierung von Luftbildern). Antworte auf Deutsch. Regeln: `C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md` (lies sie zuerst, besonders L14 und L15).

## Ziel

Entscheide für jeden der 22 Kandidaten unten am Bild, ob er ein Haus- oder Hofgarten ist und damit die Klasse Garten bekommen soll (in dieser Liste Code `3.6` „Garten (Haus- und Hofgarten: Grünfläche, Beet)“). Du änderst keine Karte und keine Klasse; du schreibst nur die Ergebnisdatei.

## Was „Garten“ ist (Entscheidungen des Nutzers vom 18.11.2026)

- eine einzige Unterklasse „Garten“ unter Dauergrünland (feste Liste: Code 3.6; freie Listen A/B: ihre eigene Klasse Garten unter ihrer Dauergrünland-Klasse, Regel L14 im Skill);
- dazu gehört jede krautige Grünfläche und jedes Beet im Haus- oder Hofgarten (auch Vor-, Obst- und Gemüsegarten), ob gepflegter Rasen oder nicht — Rasen ist kein Kennzeichen;
- nur Haus- und Hofgärten: Parks, Friedhöfe, Sportrasen und Wiesen am Ortsrand bleiben Wiese/Weide;
- Bäume, Sträucher und Hecken im Garten bleiben Gehölz (von oben sieht man die Krone);
- auf dem Schwarz-Weiß-Bild H0 nur klar erkennbare Gärten am Haus; Unklares bleibt, wie es ist.

## Bild

- Bild: T0 Farbe (Farb-Orthofoto, rund 0,2 m je Bildpunkt).
- Fassung C (c-feste-liste), Teilkachel r0c0; Kategorienliste `C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/c-feste-liste/kategorien-c.json`.
- Karte: `C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/c-feste-liste/r0c0/labels.tif`, Teilkachelbild: `C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/teilkacheln/r0c0.png`.
- Bilder je Viertel (gelb alle Grenzen, magenta die Kandidaten mit Nummer; weißer Rahmen = Kern); jedes nur einmal ansehen:
  - v1: mit Umriss `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-C-r0c0-1/v1_umriss.jpg`, roh daneben `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-C-r0c0-1/v1_roh.jpg`
  - v2: mit Umriss `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-C-r0c0-1/v2_umriss.jpg`, roh daneben `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-C-r0c0-1/v2_roh.jpg`
  - v4: mit Umriss `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-C-r0c0-1/v4_umriss.jpg`, roh daneben `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-C-r0c0-1/v4_roh.jpg`
- Kandidatenliste: `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-C-r0c0-1/kandidaten.json` (id, Klasse, Fläche m², Viertel, Mittelpunkt x,y in Bildpunkten der Teilkachel, Grund der Auswahl).

## Kandidaten

| id | Klasse | Fläche m² | Viertel | Mitte x,y | Grund der Auswahl |
|---|---|---|---|---|---|
| 100011 | 3.1 Wiese / Weide (gemeinsam) | 51 | v1 | 279,75 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100038 | 3.1 Wiese / Weide (gemeinsam) | 51 | v1 | 219,77 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100051 | 3.1 Wiese / Weide (gemeinsam) | 7 | v1 | 234,69 | Grünland; grenzt an Gebäude oder Hof |
| 100036 | 3.1 Wiese / Weide (gemeinsam) | 1 | v2 | 551,66 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100047 | 3.1 Wiese / Weide (gemeinsam) | 121 | v2 | 415,94 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100061 | 3.1 Wiese / Weide (gemeinsam) | 23 | v2 | 551,101 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100070 | 3.1 Wiese / Weide (gemeinsam) | 93 | v2 | 423,131 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100071 | 3.1 Wiese / Weide (gemeinsam) | 7 | v2 | 454,111 | Grünland; grenzt an Gebäude oder Hof |
| 100074 | 3.1 Wiese / Weide (gemeinsam) | 4 | v2 | 554,116 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100076 | 3.1 Wiese / Weide (gemeinsam) | 7 | v2 | 437,122 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100093 | 3.4 Krautsaum linear (Feldrain, Wegrand, Böschung) | 4 | v2 | 423,147 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100099 | 3.4 Krautsaum linear (Feldrain, Wegrand, Böschung) | 7 | v2 | 552,158 | Grünland; grenzt an Gebäude oder Hof |
| 100100 | 3.4 Krautsaum linear (Feldrain, Wegrand, Böschung) | 3 | v2 | 524,159 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100106 | 3.1 Wiese / Weide (gemeinsam) | 41 | v2 | 472,189 | Grünland; grenzt an Gebäude oder Hof |
| 100108 | 3.1 Wiese / Weide (gemeinsam) | 18 | v2 | 533,191 | Grünland; grenzt an Gebäude oder Hof |
| 100117 | 3.1 Wiese / Weide (gemeinsam) | 6 | v2 | 378,212 | Grünland; grenzt an Gebäude oder Hof |
| 100120 | 3.1 Wiese / Weide (gemeinsam) | 265 | v2 | 389,263 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100124 | 3.1 Wiese / Weide (gemeinsam) | 14 | v2 | 332,278 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100131 | 3.1 Wiese / Weide (gemeinsam) | 6 | v2 | 388,291 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100132 | 3.1 Wiese / Weide (gemeinsam) | 6 | v2 | 428,297 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100137 | 3.1 Wiese / Weide (gemeinsam) | 105 | v4 | 460,322 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100143 | 3.1 Wiese / Weide (gemeinsam) | 227 | v4 | 465,366 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |

## Bei Zweifel

Eine Nahansicht (roh und mit Umriss nebeneinander) macht dieser Befehl im Ordner `C:/Users/Phil/Developement/Victor/landseg`:

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg zoom --manifest C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/manifest.json --teilkachel r0c0 --labels C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/c-feste-liste/r0c0/labels.tif --ids <id> --roh --ziel C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-C-r0c0-1/nah_<id>.jpg
```

Nahansichten nur in diesen Ordner schreiben. Kein Subagent, keine Fenster, nichts installieren, keine Karte ändern.

## Ergebnis

Datei `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-C-r0c0-1/entscheid.json` (UTF-8-JSON), genau ein Eintrag je Kandidaten-ID:

```json
{"<id>": {"garten": "ja" | "nein" | "unklar", "grund": "<ein Satz>"}}
```

„ja“ nur für krautige Grünfläche oder Beet in einem Haus- oder Hofgarten; Gehölz, Weg, Hof, Park, Friedhof, Sportrasen und Wiese oder Acker am Ortsrand ohne Haus „nein“; was du am Bild nicht sicher entscheiden kannst, „unklar“. Rückgabe: Zahl ja / nein / unklar.
