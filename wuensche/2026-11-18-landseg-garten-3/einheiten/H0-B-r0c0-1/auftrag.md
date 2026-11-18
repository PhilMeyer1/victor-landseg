# Garten-Bestätigung H0-B-r0c0-1

Du bist ein Agent des Projekts landseg (Segmentierung von Luftbildern). Antworte auf Deutsch. Regeln: `C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md` (lies sie zuerst, besonders L14 und L15).

## Ziel

Entscheide für jeden der 18 Kandidaten unten am Bild, ob er ein Haus- oder Hofgarten ist und damit die Klasse Garten bekommen soll (in dieser Liste Code `5.3` „Garten (Haus- und Hofgarten: Grünfläche, Beet)“). Du änderst keine Karte und keine Klasse; du schreibst nur die Ergebnisdatei.

## Was „Garten“ ist (Entscheidungen des Nutzers vom 18.11.2026)

- eine einzige Unterklasse „Garten“ unter Dauergrünland (feste Liste: Code 3.6; freie Listen A/B: ihre eigene Klasse Garten unter ihrer Dauergrünland-Klasse, Regel L14 im Skill);
- dazu gehört jede krautige Grünfläche und jedes Beet im Haus- oder Hofgarten (auch Vor-, Obst- und Gemüsegarten), ob gepflegter Rasen oder nicht — Rasen ist kein Kennzeichen;
- nur Haus- und Hofgärten: Parks, Friedhöfe, Sportrasen und Wiesen am Ortsrand bleiben Wiese/Weide;
- Bäume, Sträucher und Hecken im Garten bleiben Gehölz (von oben sieht man die Krone);
- auf dem Schwarz-Weiß-Bild H0 nur klar erkennbare Gärten am Haus; Unklares bleibt, wie es ist.

## Bild

- Bild: H0 SW (Schwarz-Weiß-Scan von 1968, rund 0,45 m je Bildpunkt); auf diesem Schwarz-Weiß-Bild nur klar erkennbare Gärten am Haus mit „ja“, Unklares „unklar“ oder „nein“.
- Fassung B (b-kategorien-frei), Teilkachel r0c0; Kategorienliste `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/kategorien-b.json`.
- Karte: `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r0c0/labels.tif`, Teilkachelbild: `C:/Users/Phil/Developement/Victor/daten/landseg/H0/teilkacheln/r0c0.png`.
- Bilder je Viertel (gelb alle Grenzen, magenta die Kandidaten mit Nummer; weißer Rahmen = Kern); jedes nur einmal ansehen:
  - v1: mit Umriss `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-B-r0c0-1/v1_umriss.jpg`, roh daneben `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-B-r0c0-1/v1_roh.jpg`
  - v2: mit Umriss `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-B-r0c0-1/v2_umriss.jpg`, roh daneben `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-B-r0c0-1/v2_roh.jpg`
  - v4: mit Umriss `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-B-r0c0-1/v4_umriss.jpg`, roh daneben `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-B-r0c0-1/v4_roh.jpg`
- Kandidatenliste: `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-B-r0c0-1/kandidaten.json` (id, Klasse, Fläche m², Viertel, Mittelpunkt x,y in Bildpunkten der Teilkachel, Grund der Auswahl).

## Kandidaten

| id | Klasse | Fläche m² | Viertel | Mitte x,y | Grund der Auswahl |
|---|---|---|---|---|---|
| 100035 | 2.2 Gartenfläche am Hof (bisher „Garten“) | 455 | v1 | 241,88 | Grünland; grenzt an Gebäude oder Hof |
| 100047 | 5.1.2 Wegrain | 102 | v1 | 122,73 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100051 | 2.2 Gartenfläche am Hof (bisher „Garten“) | 666 | v1 | 205,108 | Grünland; grenzt an Gebäude oder Hof |
| 100052 | 5.1.1 Feldrain | 150 | v1 | 97,94 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100077 | 5.2.1 Anger | 1270 | v1 | 282,163 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100097 | 5.1.2 Wegrain | 12 | v1 | 68,152 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100114 | 5.2.1 Anger | 2678 | v1 | 173,281 | Grünland; grenzt an Gebäude oder Hof |
| 100138 | 2.2 Gartenfläche am Hof (bisher „Garten“) | 336 | v1 | 119,252 | Grünland; grenzt an Gebäude oder Hof |
| 100160 | 5.2.2 Brache | 304 | v1 | 81,312 | Grünland; grenzt an Gebäude oder Hof |
| 100163 | 5.1.1 Feldrain | 33 | v1 | 307,279 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100012 | 2.2 Gartenfläche am Hof (bisher „Garten“) | 134 | v2 | 485,73 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100062 | 2.2 Gartenfläche am Hof (bisher „Garten“) | 558 | v2 | 427,127 | Grünland; grenzt an Gebäude oder Hof |
| 100066 | 2.2 Gartenfläche am Hof (bisher „Garten“) | 473 | v2 | 380,129 | Grünland; grenzt an Gebäude oder Hof |
| 100104 | 5.2.1 Anger | 1518 | v2 | 335,221 | Grünland; grenzt an Gebäude oder Hof |
| 100280 | 2.2 Gartenfläche am Hof (bisher „Garten“) | 3 | v2 | 514,65 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100187 | 5.1.2 Wegrain | 182 | v4 | 440,360 | Grünland; im Siedlungsgebiet (Merkmal im_siedlung) |
| 100219 | 6.1 Feld | 188 | v4 | 534,553 | Acker klein; grenzt an Gebäude oder Hof |
| 100229 | 6.1 Feld | 4 | v4 | 547,562 | Acker klein; grenzt an Gebäude oder Hof |

## Bei Zweifel

Eine Nahansicht (roh und mit Umriss nebeneinander) macht dieser Befehl im Ordner `C:/Users/Phil/Developement/Victor/landseg`:

```
C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m landseg zoom --manifest C:/Users/Phil/Developement/Victor/daten/landseg/H0/manifest.json --teilkachel r0c0 --labels C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/r0c0/labels.tif --ids <id> --roh --ziel C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-B-r0c0-1/nah_<id>.jpg
```

Nahansichten nur in diesen Ordner schreiben. Kein Subagent, keine Fenster, nichts installieren, keine Karte ändern.

## Ergebnis

Datei `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-garten-3/einheiten/H0-B-r0c0-1/entscheid.json` (UTF-8-JSON), genau ein Eintrag je Kandidaten-ID:

```json
{"<id>": {"garten": "ja" | "nein" | "unklar", "grund": "<ein Satz>"}}
```

„ja“ nur für krautige Grünfläche oder Beet in einem Haus- oder Hofgarten; Gehölz, Weg, Hof, Park, Friedhof, Sportrasen und Wiese oder Acker am Ortsrand ohne Haus „nein“; was du am Bild nicht sicher entscheiden kannst, „unklar“. Rückgabe: Zahl ja / nein / unklar.
