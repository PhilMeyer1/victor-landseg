# Auftrag: freie Klassen der Viertel von {{FASSUNG_NAME}} ({{AUSSCHNITT}}) zu einer Liste vereinheitlichen

Lies zuerst den Skill `landseg-agent` (`{{REPO}}/.claude/skills/landseg-agent/SKILL.md`); seine Regeln gelten hier
ohne L3. Antworte auf Deutsch.

Gegenstand: {{FASSUNG_NAME}} des Ausschnitts in `{{DATEN}}`. Die Urteils-Agents haben je ein Viertel beurteilt und
die Flächen dabei selbst benannt (`klasse_frei` je Segment mit `grob`, `mittel`, `fein`; `klassen_frei` je Viertel
mit Ebene, Eltern, Bildmerkmal). Du machst daraus eine einheitliche, gestufte Kategorienliste für den ganzen
Ausschnitt und ordnest jedem Segment ihren Code zu. Du urteilst nicht neu am Bild, änderst keine Viertel-Abgabe
und nicht die Label-Karte.

Pflicht beim Zusammenlegen (Regel L14 des Skills): Die neue Liste führt die Klasse „Garten“ unter der
Ebene-1-Klasse „Dauergrünland“ (genau diese Namen, Zusatz in Klammern erlaubt), auch wenn sie keiner trägt.
Jeder Name für Haus- und Hofgärten (Garten, Gartenland, Grün im Ort am Haus und ähnliche) geht auf sie über;
Hof, Gartenbaum, Hecke und Gartenweg nicht. `zusammenfuehren` lehnt eine Liste ohne diese Klasse ab.

## Hinweis des Laufs

{{HINWEIS}}

## Eingaben (nur lesen)

{{ABGABEN}}

- `{{REPO}}/kategorien.json`: Format der Liste (nur das Format, nicht die Klassen).
- Bei Zweifeln, ob zwei Namen dasselbe meinen: die Bilder des Viertels unter `{{BILDER}}/<teilkachel>/v<n>/`.

## Ergebnis in `{{ERGEBNIS}}` (nur dort, genau diese Namen)

- `kategorien-entwurf.json` im Format von `kategorien.json`: `{"schema": "landseg-kategorien/1", "title": "…",
  "date": "JJJJ-MM-TT", "classes": [{"code": "1", "name": "…", "parent": null, "level": 1, "color": "#rrggbb",
  "image_cue": "woran im Bild erkennbar"}, …]}`. Codes gestuft (`1`, `1.2`, `1.2.3`), Ebenen 1 bis 3, Ebene 1
  höchstens sieben Klassen mit den Codes `0` bis `6` (`0` nur für „nicht bestimmbar“), jede Klasse mit Eltern auf
  der Ebene darüber, Farben paarweise gut unterscheidbar (CIELAB-Abstand mindestens 10).
- `codes.json`: `{"schema": "landseg-codes/1", "segmente": {"<teilkachel>": {"<id>": {"code": "1.2.3",
  "viertel": "v1", "klasse_frei": {"grob": "…", "mittel": "…", "fein": "…"}}}}, "namen": [{"teilkachel": "r0c0",
  "viertel": "v1", "ebene": "fein", "name": "Name des Viertels", "code": "1.2.3"}], "offen": [],
  "nicht_geprueft": []}`: jedes Segment jeder Viertel-Abgabe genau einmal mit dem Code seiner feinsten Ebene.
- `vereinheitlichung.md`: welche Namen du zusammengelegt oder getrennt hast und warum, was offen blieb.

Kontrolle der Liste (muss mit `ok` enden): `{{PY}} -I {{REPO}}/tools/pruefe_kategorien.py {{ERGEBNIS}}/kategorien-entwurf.json`

Fehlt eine Viertel-Abgabe oder darin ein Segment: nicht nachholen, sondern unter `nicht_geprueft` nennen.

## Rückgabe

Zahl der Klassen je Ebene, Zahl der Segmente mit Code, Zahl der zusammengelegten Namen, was offen blieb.
