# Auftrag: freie Klassen der 16 Viertel von Fassung B (H0) zu einer Liste vereinheitlichen

Lies zuerst den Skill `landseg-agent` (`C:/Users/Phil/Developement/Victor/landseg/.claude/skills/landseg-agent/SKILL.md`); seine Regeln
gelten hier ohne L3. Antworte auf Deutsch.

Gegenstand: Fassung B „Kategorien frei“ des Ausschnitts H0 (Schwarz-Weiß-Scan 1968) in
`C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei`. Vier Agents (einer je Teilkachel) haben je vier Viertel beurteilt und die
Flächen dabei selbst benannt (`klasse_frei` je Segment mit `grob`, `mittel`, `fein`; `klassen_frei` je
Viertel mit Ebene, Eltern, Bildmerkmal). Du machst daraus eine einheitliche, gestufte Kategorienliste
für ganz H0 und ordnest jedem Segment ihren Code zu. Du urteilst nicht neu am Bild, änderst keine
Viertel-Abgabe und nicht die Label-Karte.

## Eingaben (nur lesen)

| Teilkachel | Viertel | Segmente | Abgabe |
|---|---|---|---|
| `r0c0` | `v1` | 58 | `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r0c0/v1/urteil.json` |
| `r0c0` | `v2` | 67 | `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r0c0/v2/urteil.json` |
| `r0c0` | `v3` | 14 | `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r0c0/v3/urteil.json` |
| `r0c0` | `v4` | 34 | `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r0c0/v4/urteil.json` |
| `r0c1` | `v1` | 16 | `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r0c1/v1/urteil.json` |
| `r0c1` | `v2` | 23 | `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r0c1/v2/urteil.json` |
| `r0c1` | `v3` | 25 | `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r0c1/v3/urteil.json` |
| `r0c1` | `v4` | 28 | `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r0c1/v4/urteil.json` |
| `r1c0` | `v1` | 12 | `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c0/v1/urteil.json` |
| `r1c0` | `v2` | 12 | `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c0/v2/urteil.json` |
| `r1c0` | `v3` | 9 | `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c0/v3/urteil.json` |
| `r1c0` | `v4` | 5 | `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c0/v4/urteil.json` |
| `r1c1` | `v1` | 52 | `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c1/v1/urteil.json` |
| `r1c1` | `v2` | 47 | `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c1/v2/urteil.json` |
| `r1c1` | `v3` | 37 | `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c1/v3/urteil.json` |
| `r1c1` | `v4` | 26 | `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/urteil/r1c1/v4/urteil.json` |

- `C:/Users/Phil/Developement/Victor/landseg/kategorien.json`: Format der Liste (nur das Format, nicht die Klassen).
- Bei Zweifeln, ob zwei Namen dasselbe meinen: die Bilder des Viertels unter `C:/Users/Phil/Developement/Victor/daten/landseg/H0/viertel/<teilkachel>/v<n>/`.

## Ergebnis in `C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/vereinheitlichung` (nur dort, genau diese Namen)

- `kategorien-b-entwurf.json` im Format von `kategorien.json`: `{"schema": "landseg-kategorien/1",
  "title": "…", "date": "JJJJ-MM-TT", "classes": [{"code": "1", "name": "…", "parent": null, "level": 1,
  "color": "#rrggbb", "image_cue": "woran im Bild erkennbar"}, …]}`. Codes gestuft (`1`, `1.2`, `1.2.3`),
  Ebenen 1 bis 3, Ebene 1 höchstens sieben Klassen mit den Codes `0` bis `6` (`0` nur für „nicht
  bestimmbar“, falls gebraucht), jede Klasse mit Eltern auf der Ebene darüber, Farben paarweise gut
  unterscheidbar (CIELAB-Abstand mindestens 10). Gleiche Dinge stehen unter einem Namen, auch wenn die
  Viertel sie verschieden nannten. `image_cue` beschreibt Grauton, Textur und Form (kein Farbbild).
- `codes.json`: `{"schema": "landseg-h0-codes-b/1", "segmente": {"<teilkachel>": {"<id>": {"code":
  "1.2.3", "viertel": "v1", "klasse_frei": {"grob": "…", "mittel": "…", "fein": "…"}}}}, "namen":
  [{"teilkachel": "r0c0", "viertel": "v1", "ebene": "fein", "name": "Name des Viertels", "code": "1.2.3"}],
  "offen": [], "nicht_geprueft": []}`: jedes Segment jeder Viertel-Abgabe genau einmal mit dem Code seiner
  feinsten Ebene, jeder Name jedes Viertels mit seinem Code.
- `vereinheitlichung.md`: welche Namen du zusammengelegt oder getrennt hast und warum, was offen blieb.

Kontrolle der Liste (muss mit `ok` enden): `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I C:/Users/Phil/Developement/Victor/landseg/tools/pruefe_kategorien.py C:/Users/Phil/Developement/Victor/daten/landseg/H0/b-kategorien-frei/vereinheitlichung/kategorien-b-entwurf.json`

Fehlt eine Viertel-Abgabe oder darin ein Segment: nicht nachholen, sondern unter `nicht_geprueft` nennen.

## Rückgabe

Zahl der Klassen je Ebene, Zahl der Segmente mit Code, Zahl der zusammengelegten Namen, was offen blieb.
