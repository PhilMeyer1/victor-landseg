# Auftrag: die eigenen Listen der Teilkacheln von {{FASSUNG_NAME}} ({{AUSSCHNITT}}) zu einer Liste zusammenlegen

Antworte auf Deutsch. Gegenstand: {{FASSUNG_NAME}} des Ausschnitts in `{{DATEN}}`. Je Teilkachel hat ein Agent frei
segmentiert und eine eigene, gestufte Liste angelegt (`kategorien-teil.json`). Du legst die Listen nach Namen und
Merkmalen zu einer Liste für den ganzen Ausschnitt zusammen und bildest jeden Code jeder Teilkachel-Liste auf einen
Code der neuen Liste ab. Du urteilst nicht neu am Bild und änderst keine Abgabe.

Pflicht beim Zusammenlegen (Regel L14 des Skills): Die neue Liste führt die Klasse „Garten“ unter der
Ebene-1-Klasse „Dauergrünland“ (genau diese Namen, Zusatz in Klammern erlaubt), auch wenn sie keiner trägt.
Jeder Name für Haus- und Hofgärten (Garten, Gartenland, Grün im Ort am Haus und ähnliche) geht auf sie über;
Hof, Gartenbaum, Hecke und Gartenweg nicht. `zusammenfuehren` lehnt eine Liste ohne diese Klasse ab.

## Hinweis des Laufs

{{HINWEIS}}

## Eingaben (nur lesen)

{{ABGABEN}}

- `{{REPO}}/kategorien.json`: Format der Liste (nur das Format, nicht die Klassen).

## Ergebnis in `{{ERGEBNIS}}` (nur dort, genau diese Namen)

- `kategorien-entwurf.json` im Format von `kategorien.json` (`schema`, `title`, `date`, `classes` mit `code`,
  `name`, `parent`, `level`, `color`, `image_cue`; gestufte Codes, Ebene 1 höchstens sieben Klassen `0` bis `6`,
  Farben paarweise gut unterscheidbar), dazu `abbildung_teilkacheln`: `{"<teilkachel>": {"<Code der eigenen
  Liste>": "<Code der neuen Liste>"}}` mit jedem Code, der in `segmente.json` der Teilkachel vorkommt.
- `vereinheitlichung.md`: was du zusammengelegt hast und warum, was offen blieb.

Kontrolle der Liste (muss mit `ok` enden): `{{PY}} -I {{REPO}}/tools/pruefe_kategorien.py {{ERGEBNIS}}/kategorien-entwurf.json`

## Rückgabe

Zahl der Klassen je Ebene, Zahl der abgebildeten Codes je Teilkachel, was offen blieb.
