# Auftrag: {{AUSSCHNITT}}, Teilkachel {{TEILKACHEL}}, Viertel {{VIERTEL}}: {{SEGMENTZAHL}} Segmente im Verbund ansehen und einzeln urteilen ({{FASSUNG_NAME}})

Lies zuerst den Skill `landseg-agent` (`{{REPO}}/.claude/skills/landseg-agent/SKILL.md`); seine
Regeln gelten hier. Antworte auf Deutsch.

Gegenstand: Viertel {{VIERTEL}} der Teilkachel `{{TEILKACHEL}}` des Ausschnitts in `{{DATEN}}`. Du urteilst
über jedes Segment deines Viertels (Liste unter „Dein Viertel“), ob Grenze und Klasse stimmen, und zeichnest
ein, was du ändern würdest. Die Label-Karte änderst du nur nach dem Abschnitt „Nachsegmentieren“ (grob
zusammengefasste Segmente teilen, bevor du sie urteilst).

## Daten (nur lesen; Ausnahme: Karte und `segmente.json` unter „Nachsegmentieren“, nur über `eingriff` und `kante`)

- `{{DATEN}}/manifest.json`: Eintrag `{{TEILKACHEL}}` unter `teilkacheln` mit `bild` (Teilkachelbild,
  Kern + Kontextrand), `kern_im_bild` (Lage des Kerns im Teilkachelbild) und `kern` (Lage im Ausschnitt).
- `{{DATEN}}/{{LABELS}}`: Label-Karte (Segment-ID je Bildpunkt, Größe des Teilkachelbilds).
- `{{DATEN}}/{{SEGMENTE}}`: je Segment `id`, `klasse`, `grob`, `herkunft`, `sicher`; Kandidaten der Vorstufe
  in `kandidaten.json` daneben, falls vorhanden.
- {{KATEGORIEN}}

## Zuerst der ganze Ausschnitt, dann die Teilkachel

Bevor du dein Viertel ansiehst: zuerst der ganze Ausschnitt (`{{AUSSCHNITT_BILD}}`, Teilkachel rXcY = Zeile X,
Spalte Y, gezählt von oben links ab 0), dann die ganze Teilkachel `{{TEILKACHEL}}` (`{{TEILKACHEL_BILD}}`:
Grenzen, Nummern, Viertel v1–v4; `{{TEILKACHEL_ROH}}` unverändert). Beide stehen in
`bilder_angesehen.uebersicht` vor den Viertelbildern; jedes Bild siehst du genau einmal an.

## Hinweis des Laufs

{{HINWEIS}}{{FEINHEIT}}

## Dein Viertel

Viertel {{VIERTEL}} ({{VIERTEL_LAGE}}) des Kerns von `{{TEILKACHEL}}`: {{VIERTEL_RECHTECK}}. Dir gehören die
{{SEGMENTZAHL}} Segmente der Liste unten: Jedes hat den größten Teil seiner Kernfläche in diesem Viertel. Die
Teilkachel hat {{KERNZAHL}} Kernsegmente ({{JE_VIERTEL}}); die anderen Viertel stehen in eigenen Aufträgen mit
eigenem Ergebnisordner. In den Bildern der Nachbarn ist ein Segment dieses Viertels mit grauer Nummer als
Umgebung zu sehen.

Urteil im Verbund: Du siehst das Viertel als zusammenhängendes Bild mit Umgebung, arbeitest die Liste der Reihe
nach ab und beurteilst jedes Segment im Zusammenhang mit seinen Nachbarn; eingetragen wird jedes Segment einzeln.

Bilder des Viertels (fertig, JPEG, in `{{BILDER}}`, Fenster und Vergrößerung je Bild in `viertel.json`):

- Übersicht, das Viertel mit Umgebung: `uebersicht_nummern.jpg` (Grenzen, Nummern deiner Segmente weiß, der
  Nachbarviertel grau, Kontextrand ohne Nummer, Viertel umrandet), `uebersicht_roh.jpg`, `uebersicht_vorschlag.jpg`
  (Klassen der Vorstufe), `uebersicht_maengel.jpg` (Legende unten), `uebersicht_kontrast.jpg`,
  `uebersicht_gitter.jpg` (beschriftet in Bildpunkten der Teilkachel).
- Nahansichten, das Viertel in vier Teilen, je ein Paar (links roh, rechts Grenzen mit Nummern, selber Maßstab):
  `nah1.jpg` oben links, `nah2.jpg` oben rechts, `nah3.jpg` unten links, `nah4.jpg` unten rechts.
- Koordinaten: `x_teilkachel = fenster.x + x_bild // faktor` (im Gitterbild vorher 40 px links und 16 px oben
  abziehen; rechte Hälfte eines Paars vorher `versatz` abziehen). Nummer im Bild = ID mod {{NUMMER_MODULO}}; in
  `urteil.json` steht immer die volle ID.

Liste (Reihenfolge der Abarbeitung, zeilenweise von oben links; Punkt = Stelle sicher im Segment, im
Teilkachelbild; Anteil hier = Anteil der Kernfläche in diesem Viertel):

{{LISTE}}

## Nachsegmentieren

Fasst ein Segment sichtbar mehrere Objekte zusammen (Häuserzeile, Hof mit Garten, Acker mit Weg oder Rain,
Baumgruppe mit Wiese), teilst du es selbst, bevor du es urteilst. Karte zum Nachsegmentieren:
`{{DATEN}}/{{LABELS}}` und `{{DATEN}}/{{SEGMENTE}}` (Befehle im Ordner `{{REPO}}`, dein Name `{{BEARBEITER}}`).

- Alle Eingriffe des Viertels in einem Stapel `{{ERGEBNIS}}/eingriffe.json` (`{"schritte": [{"op": "teilen",
  "id": 4, "linie": [[x, y], [x, y]]}, {"op": "polygon_zuweisen", "flaeche": [[x, y], …], "id": 7},
  {"op": "verschmelzen", "ids": [3, 5]}]}`, Koordinaten im Teilkachelbild; alles oder nichts):
  `{{PY}} -B -m landseg eingriff --labels {{DATEN}}/{{LABELS}} --segmente {{DATEN}}/{{SEGMENTE}} --bearbeiter {{BEARBEITER}} stapel --datei {{ERGEBNIS}}/eingriffe.json`
- Einrasten auf die Bildkante: `{{PY}} -B -m landseg kante --labels {{DATEN}}/{{LABELS}} --segmente {{DATEN}}/{{SEGMENTE}} --bild {{DATEN}}/{{TEILKACHEL_DATEI}} --bearbeiter {{BEARBEITER}} --a <ID> --b <ID>`
- Kontrolle: `{{PY}} -B -m landseg pruefen --labels {{DATEN}}/{{LABELS}} --segmente {{DATEN}}/{{SEGMENTE}} --bild {{DATEN}}/{{TEILKACHEL_DATEI}}` (muss mit `ok` enden).
- Nur teilen, wo Objekte im Bild klar getrennt sind; nur Segmente deiner Liste, nur im Kern deines Viertels.
  Neue IDs urteilst du im selben `urteil.json`; jede Teilung steht dort unter `eingriffe` mit IDs vorher/nachher
  und Grund in einem Satz (ohne Eingriff `"eingriffe": []`).

## Werkzeuge

Befehle im Ordner `{{REPO}}` mit `{{PY}} -B -m landseg <befehl>`; Aufruf und Schalter stehen in
`{{REPO}}/README.md`. Zuerst die fertigen Befehle, sie sind der Standardweg:

- Nahansicht einer beliebigen Stelle als Paar:
  `{{PY}} -B -m landseg zoom --manifest {{DATEN}}/manifest.json --teilkachel {{TEILKACHEL}} --labels {{DATEN}}/{{LABELS}} --ids 17 --roh --ziel {{ERGEBNIS}}/nah_17_1.jpg`
- `urteil.json` aus der kurzen Liste `{{ERGEBNIS}}/liste.json` bauen (Format: README, Abschnitt `urteil`):
  `{{PY}} -B -m landseg urteil bauen --manifest {{DATEN}}/manifest.json --teilkachel {{TEILKACHEL}} --viertel {{VIERTEL}} --labels {{DATEN}}/{{LABELS}} --segmente {{DATEN}}/{{SEGMENTE}} --bearbeiter {{BEARBEITER}} --liste {{ERGEBNIS}}/liste.json --ziel {{ERGEBNIS}}/urteil.json`

Ein eigenes Skript (als Datei in `{{ERGEBNIS}}`) nur, wenn kein Befehl den Fall deckt; nenne es in der Rückgabe.
{{FASSUNG_ABSCHNITT}}
## Ergebnis in `{{ERGEBNIS}}`

- `liste.json` und daraus `urteil.json` (`urteil bauen`), dazu `eingriffe` (und in Fassung B `klasse_frei` je
  Segment, `klassen_frei`) wie oben; unter `bilder_angesehen` die angesehenen Bilder (`uebersicht`, `nah`),
  je Segment unter `bilder` die Bilder, auf denen du es beurteilt hast.
- `nah_<n>.jpg`: eigene Nahansichten von Stellen, die man in den vorbereiteten Bildern nicht beurteilen kann.

Jedes Segment deiner Liste steht genau einmal unter `segmente`, auch die sauberen. Segmente der Nachbarviertel
und des Kontextrands urteilst du nicht; Auffälliges an ihnen nennst du unter `unsicher` mit ID. `nicht_geprueft`
nennt, was du nicht angesehen hast, `offen`, was du nicht entscheiden konntest.

Kontrolle vor der Rückgabe (muss mit `ok` enden):

```
{{PY}} -B -m landseg urteil pruefen --manifest {{DATEN}}/manifest.json --teilkachel {{TEILKACHEL}} --viertel {{VIERTEL}} --labels {{DATEN}}/{{LABELS}} --urteil {{ERGEBNIS}}/urteil.json
```

## Rückgabe

Zahl der Segmente, davon nicht sauber, Zahl der Eingriffe, Anteil `sicher: false`, wo du unsicher bist.
