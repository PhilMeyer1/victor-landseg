# Garten-Bestätigung T0-B-r0c0-1

Du bist ein Agent des Projekts landseg (Segmentierung von Luftbildern). Antworte auf Deutsch. Regeln: `C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md` (lies sie zuerst, besonders L14 und L15).

## Ziel

Entscheide für jeden der 25 Kandidaten unten am Bild, ob er ein Haus- oder Hofgarten ist und damit die Klasse Garten bekommen soll (in dieser Liste Code `2.4` „Garten (Haus- und Hofgarten: Grünfläche, Beet)“). Du änderst keine Karte und keine Klasse; du schreibst nur die Ergebnisdatei.

## Was „Garten“ ist (Entscheidungen des Nutzers vom 18.11.2026)

- eine einzige Unterklasse „Garten“ unter Dauergrünland (feste Liste: Code 3.6; freie Listen A/B: ihre eigene Klasse Garten unter ihrer Dauergrünland-Klasse, Regel L14 im Skill);
- dazu gehört jede krautige Grünfläche und jedes Beet im Haus- oder Hofgarten (auch Vor-, Obst- und Gemüsegarten), ob gepflegter Rasen oder nicht — Rasen ist kein Kennzeichen;
- nur Haus- und Hofgärten: Parks, Friedhöfe, Sportrasen und Wiesen am Ortsrand bleiben Wiese/Weide;
- Bäume, Sträucher und Hecken im Garten bleiben Gehölz (von oben sieht man die Krone);
- auf dem Schwarz-Weiß-Bild H0 nur klar erkennbare Gärten am Haus; Unklares bleibt, wie es ist.

## Bild

- Bild: T0 Farbe (Farb-Orthofoto, rund 0,2 m je Bildpunkt).
- Fassung B (b-kategorien-frei), Teilkachel r0c0; Kategorienliste `C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/b-kategorien-frei/kategorien-b.json`.
- Karte: `C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/b-kategorien-frei/r0c0/labels.tif`, Teilkachelbild: `C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/teilkacheln/r0c0.png`.
- Bilder je Viertel (gelb alle Grenzen, magenta die Kandidaten mit Nummer; weißer Rahmen = Kern); jedes nur einmal ansehen:
  - v1: mit Umriss `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-B-r0c0-1/v1_umriss.jpg`, roh daneben `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-B-r0c0-1/v1_roh.jpg`
  - v2: mit Umriss `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-B-r0c0-1/v2_umriss.jpg`, roh daneben `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-B-r0c0-1/v2_roh.jpg`
  - v4: mit Umriss `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-B-r0c0-1/v4_umriss.jpg`, roh daneben `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-B-r0c0-1/v4_roh.jpg`
- Kandidatenliste: `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-B-r0c0-1/kandidaten.json` (id, Klasse, Fläche m², Viertel, Mittelpunkt x,y in Bildpunkten der Teilkachel, Grund der Auswahl).

## Kandidaten

| id | Klasse | Fläche m² | Viertel | Mitte x,y | Grund der Auswahl |
|---|---|---|---|---|---|
| 100011 | 3.3.2 Parzelle gemischt | 51 | v1 | 279,75 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100038 | 2.2 Rasen | 51 | v1 | 219,77 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100031 | 3.3.2 Parzelle gemischt | 2 | v2 | 449,66 | Grünland; grenzt an Gebäude oder Hof |
| 100036 | 3.3.2 Parzelle gemischt | 1 | v2 | 551,66 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100047 | 2.2 Rasen | 121 | v2 | 415,94 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100061 | 3.3.2 Parzelle gemischt | 23 | v2 | 551,101 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100070 | 3.3.2 Parzelle gemischt | 93 | v2 | 423,131 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100074 | 3.3.2 Parzelle gemischt | 4 | v2 | 554,116 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100076 | 3.3.2 Parzelle gemischt | 7 | v2 | 437,122 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100078 | 3.3.2 Parzelle gemischt | 12 | v2 | 526,124 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100089 | 3.3.2 Parzelle gemischt | 43 | v2 | 493,144 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100093 | 2.2 Rasen | 4 | v2 | 423,147 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100099 | 2.3 Saum und Randstreifen | 7 | v2 | 552,158 | Grünland; grenzt an Gebäude oder Hof |
| 100100 | 2.2 Rasen | 3 | v2 | 524,159 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100106 | 3.3.2 Parzelle gemischt | 41 | v2 | 472,189 | Grünland; grenzt an Gebäude oder Hof |
| 100108 | 2.2 Rasen | 18 | v2 | 533,191 | Grünland; grenzt an Gebäude oder Hof |
| 100117 | 2.2 Rasen | 6 | v2 | 378,212 | Grünland; grenzt an Gebäude oder Hof |
| 100120 | 2.2 Rasen | 265 | v2 | 389,263 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100124 | 2.2 Rasen | 14 | v2 | 332,278 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100131 | 2.2 Rasen | 6 | v2 | 388,291 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100132 | 2.2 Rasen | 6 | v2 | 428,297 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100134 | 2.1.1 Wiese gemäht | 16 | v2 | 410,306 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100137 | 2.1.1 Wiese gemäht | 105 | v4 | 460,322 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100143 | 2.1.2 Wiese ungemäht | 227 | v4 | 465,366 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100148 | 2.1.2 Wiese ungemäht | 6 | v4 | 408,342 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |

## Bei Zweifel

Eine Nahansicht (roh und mit Umriss nebeneinander) macht dieser Befehl im Ordner `C:/Users/Phil/Developement/Victor/landseg`:

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg zoom --manifest C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/manifest.json --teilkachel r0c0 --labels C:/Users/Phil/Developement/Victor/daten/landseg/uebergabe/landseg-t0/T0/b-kategorien-frei/r0c0/labels.tif --ids <id> --roh --ziel C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-B-r0c0-1/nah_<id>.jpg
```

Nahansichten nur in diesen Ordner schreiben. Kein Subagent, keine Fenster, nichts installieren, keine Karte ändern.

## Ergebnis

Datei `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/T0-B-r0c0-1/entscheid.json` (UTF-8-JSON), genau ein Eintrag je Kandidaten-ID:

```json
{"<id>": {"garten": "ja" | "nein" | "unklar", "grund": "<ein Satz>"}}
```

„ja“ nur für krautige Grünfläche oder Beet in einem Haus- oder Hofgarten; Gehölz, Weg, Hof, Park, Friedhof, Sportrasen und Wiese oder Acker am Ortsrand ohne Haus „nein“; was du am Bild nicht sicher entscheiden kannst, „unklar“. Rückgabe: Zahl ja / nein / unklar.
