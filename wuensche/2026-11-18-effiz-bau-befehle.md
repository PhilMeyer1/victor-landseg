# K5: Vorbereitung und Zusammenführen als feste Repo-Befehle statt Opus-Agent, der in jedem Lauf T0-Skripte überträgt — Ge

Kurzname: effiz-bau-befehle | Datum: 2026-11-18 | Größe: mittel | Bereich: victor | Repos: landseg | Status: eingereiht | Herkunft: Ermittlung landseg-effiz K5

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

K5: Vorbereitung und Zusammenführen als feste Repo-Befehle statt Opus-Agent, der in jedem Lauf T0-Skripte überträgt — Gewinn rund 6 USD und 14 min Wand je Lauf, dazu keine stummen Fehler beim Übertragen — Aufwand mittel — Risiko gering — Repo landseg — optional

Belege: wuensche/2026-11-18-landseg-effiz/bericht.md, K5.

Empfehlung der Deutung (wuensche/2026-11-18-landseg-effiz.md, Abschnitt Empfehlung):
- K5: trägt teilweise — entspricht S2 im Stitcher, spart aber nur 2,6 % der Kosten; der Gewinn liegt in Wandzeit und weniger stummen Fehlern.
- Nächster Schritt: K2 als Folge-Wunsch — er bringt den größten Gewinn (geschätzt 35–60 USD und 5–10 min je Lauf) und ist genau der Schritt, der im Stitcher gewirkt hat. Für die Läufe auf dem ganzen Orthofoto zählt jede gesparte Runde, weil sie das Wiederlesen des ganzen Kontexts spart.
- Gegenargument: Der Gewinn von K2 ist nur geschätzt. Im Stitcher ließen sich die fünf Maßnahmen von runden-straffen nicht trennen, und selbst danach schrieb ein Agent weiter eigene Skripte für Ansichtsbilder, das Zeitziel wurde verfehlt (bericht.md S1). Ein Teil unserer Skripte ist echte Fachhilfe (`wscheide.py`, B2). — Der Schritt gilt trotzdem: Die mechanischen Wiederholungen (urteil.json und Abgabe bauen, Zoombilder) schreibt jeder Agent neu, und der Gewinn lässt sich am nächsten Lauf mit derselben Transkript-Auswertung gegen H0 nachmessen.

## Fragen

keine (der Nutzer hat am 18.11.2026 entschieden, alle Kandidaten K1–K6 zu bauen; Technisches entscheidet der Umsetzer)

## Entscheidungen

- 2026-11-18, landseg: Landschafts-Segmente: Effizienz der Agents, ein Agent je Viertel — Nutzer am 18.11.2026 nach der Ermittlung landseg-effiz (H0-Lauf 71 Agents, rund 221 USD Rechenwert, Kostentreiber Wiederlesen des Verlaufs, 180 eigene Agent-Skripte): alle Kandidaten K1–K6 bauen (Nachhol-Prüfung reparieren, fertige landseg-Befehle statt eigener Skripte, Kostenmessung je Phase, Bilder nur einmal verlangen, Vorbereitung und Zusammenführen als feste Befehle, kleine Einigungsbündel zusammenlegen) und K7: künftig ein Urteils-Agent je Viertel statt je Teilkachel, um den Kontext kurz zu halten. Ersetzt für die Urteile „ein Agent je Teilkachel, arbeitet die vier Viertel nacheinander ab“ (2026-11-17); jeder Agent sieht weiter zuerst den ganzen Ausschnitt und seine ganze Teilkachel, dann sein Viertel. (aus entscheidungen.md, 2026-11-18)
- 2026-11-18, landseg: Einigung an den Übergängen — nach den Urteilen folgt in jedem Lauf ein fester Einigungsschritt an allen Übergängen, für jede Fassung (A, B, C) und alle künftigen Läufe; das Zusammenführen muss ihn also weiter vorbereiten (`einigung finden`). (aus entscheidungen.md, 2026-11-18)
- 2026-11-18, landseg: Vorstufe eher grob, Agents segmentieren selbst nach — die Vorbereitung bleibt bei groben Einstellungen (etwa wie T0), Urteils-Agents teilen im Urteilsschritt nach; das Zusammenführen muss deren Eingriffe (Verlauf in `segmente.json`, `eingriffe` der `urteil.json`) übernehmen. (aus entscheidungen.md, 2026-11-18)
- 2026-11-17, landseg: Daten- und Originalschutz, Grundsätze — Originalbilder unter `daten/luftbilder/` nur lesen; abgeleitete Daten unter `daten/landseg/`, nie im Repo; der Stitcher bleibt unberührt (aus entscheidungen.md, 2026-11-17)
- 2026-11-18: Landschafts-Segmente: gröbere Flächen auf alten Schwarz-Weiß-Bildern: Nutzer am 18.11.2026: „außerdem solle die Flächen in den schwarz weiß, niedrig aufgelösten Landschaftsbildern nicht ganz so fein sein. Die wirklich feine Untersuchung funktioniert gut auf hochaufgelösten Bildern aber nicht auf den alte[n]“. Daraus: Auf alten, niedrig aufgelösten Schwarz-Weiß-Bildern (heute H0, Luftbild 1968) werden Flächen deutlich gröber gezogen als auf Farb-Orthofotos (T0); feines Nachsegmentieren gilt dort nur für klar erkennbare Objekte. Verschärft für SW-Bilder die Neuklärung „eher gröber, Agents dürfen nachsegmentieren“ (landseg-historisch); im H0-Lauf kam Fassung A auf 1833 Segmente (T0 607). Wie grob genau und ob H0 neu läuft, klärt der Wunsch landseg-sw-grob. (aus entscheidungen.md, 2026-11-18)

## Arbeitsauftrag

### Abnahmekriterien

AK1: Ein Befehl `landseg vorbereiten` baut aus Manifest und einer kleinen Einstellungsdatei (Fassungen mit Namen und Ordnern aus `einstellungen/seite.json`) alles, was die Urteile brauchen: Gesamtbilder je Teilkachel, Viertelbilder, Aufträge je Fassung aus den Vorlagen, den Plan der Einheiten und leere Ergebnisordner — ohne dass ein Agent ein Skript schreibt — prüfbar: Test in `tests/` auf einem Mini-Ausschnitt (Hilfsdaten aus `tests/hilfe.py`), Exit 0 und erwartete Dateien
AK2: `landseg vorbereiten` prüft sich selbst und endet mit Exit 1 und klarer Meldung, wenn ein Kernsegment nicht in genau einem Viertel-Auftrag je Fassung steht, ein Platzhalter `{{…}}` übrig bleibt, ein Bild fehlt oder die Kartenkopien nicht bildpunktgleich zur Vorstufe sind — prüfbar: Test mit absichtlich beschädigtem Auftrag erwartet Exit 1 (je eine Verletzung)
AK3: Ein Befehl `landseg zusammenfuehren` macht aus den Urteilen (und der freien Abgabe) je Fassung `labels.tif` und `segmente.json` mit den Klassen und den Nachsegmentierungs-Eingriffen der Agents, schreibt die Kategorienlisten und `zusammentragen.json`, ruft `pruefen`, `zusammentragen` und `naht` und danach `einigung finden`; er meldet je Fassung Segmentzahl, Nahtverstöße, offene Segmente und die Bündel (Ordner) — prüfbar: Test in `tests/` auf Mini-Ausschnitt mit zwei Fassungen, Zahlen und Dateien stimmen
AK4: Die Zuordnung Fassung ↔ Buchstabe ↔ Ordner ↔ Liste steht an genau einer Stelle (Einstellungen); sie lässt sich nicht stumm vertauschen: fehlt eine Fassung oder passt eine Abgabe nicht zur Liste, bricht `zusammenfuehren` mit Exit 1 ab, statt irgendetwas zu schreiben — prüfbar: Test mit vertauschter Zuordnung und mit fehlender Abgabe (Exit 1, keine Zielordner geändert)
AK5: Gleichwertig zum Agent-Stand: `zusammenfuehren` liefert aus den vorhandenen H0-Urteilen (`daten/landseg/H0`, Fassungsordner mit `urteil/`) in einem Wegwerf-Ordner dieselben Klassen je Segment und dieselben Nahtzahlen wie die vom Agent gebauten Karten desselben Ordners (Abweichungen nur mit Erklärung) — prüfbar: offline aus `daten/landseg/H0` (nur lesen), Vergleichsskript im Test oder Bericht, Ergebnis in `abnahme-landseg.md`
AK6: `README.md` beschreibt beide Befehle (Aufruf, Einstellungen, Ausgaben, Exit-Codes) und `landseg/betrieb.md`-Hinweise stehen dort nicht doppelt — prüfbar: Lesen `README.md`, Abschnitt „Befehle“; `--help` beider Befehle läuft (`PY -B -m landseg vorbereiten --help`)
AK7: Weg des Nutzers am laufenden Stand: beide Befehle nacheinander auf einer Kopie von zwei Teilkacheln von H0 im Wegwerf-Ordner (`daten/` nicht verändert, Hash der Scans unverändert), jeder unter zwei Minuten, ohne einen Agent — prüfbar: Befehlsfolge im Bericht mit Zeiten und Hash vorher/nachher

Nacharbeit: `wuensche/2026-11-18-landseg-historisch-3/workflow.js` (Muster für künftige Läufe): Phasen „Vorbereitung“ (`vorbPrompt`, Aufruf Zeile 364) und „Zusammenführen“ (`bauPrompt`, Aufruf Zeile 429) rufen die Befehle als Befehl/Sonnet-mechanisch statt Opus mit Skript-Übertragung; Profil `.claude/repos/landseg.md`, Abschnitt Routinen, um die zwei Befehle ergänzen; Messung: Transkript-Auswertung gegen H0 am nächsten Lauf (Gewinn rund 6 USD, 14 min).

### Einstieg

- landseg: `landseg/__main__.py:318` — `befehle.add_subparsers`; neue Unterbefehle `vorbereiten` und `zusammenfuehren` hier anmelden (Vorbild `zusammentragen` Zeile 419, `einigung` Zeile 452)
- landseg: `landseg/einstellungen.py` — Einstellungsdateien laden (Vorbild `einstellungen/seite.json`, `einstellungen/einigung.json`); dorthin die Fassungs-Tabelle (neu `einstellungen/lauf.json`)
- landseg: `landseg/zusammentragen.py`, `landseg/naht.py`, `landseg/einigung.py`, `landseg/pruefen.py`, `landseg/ansicht.py` — vorhandene Funktionen, die der neue Code aufruft (nicht über Unterprozess, wenn eine Funktion da ist)
- landseg: `README.md:268` — Abschnitt `### zusammentragen` (Format `zusammentragen.json`), `:323` `### einigung`; neue Abschnitte `### vorbereiten`, `### zusammenfuehren` im Abschnitt Befehle (ab Zeile 103)
- landseg: `vorlagen/urteil.md`, `vorlagen/einigung.md` — Platzhalter `{{…}}` der Auftragsvorlagen, aus denen `vorbereiten` die Aufträge setzt
- Vorbild außerhalb des Repos (nur lesen, nicht aufrufen): `wuensche/2026-11-18-landseg-historisch-2/skripte/baue_auftraege_h0.py` (675 Zeilen: Viertel, Bilder, Aufträge, Plan), `wuensche/2026-11-18-landseg-historisch-2/skripte/pruefe_h0.py` (Prüfungen), `wuensche/2026-11-17-landseg-test-t0-3/skripte/zusammenfuehren.py` (228 Zeilen: Urteile → Klassen) und `listen.py` (233 Zeilen: Kategorienlisten), `wuensche/2026-11-17-landseg-uebergabe/skripte/baue_uebergabe.py` (186 Zeilen), `wuensche/2026-11-18-landseg-historisch-3/workflow.js:256` (`vorbPrompt`) und `:287` (`bauPrompt`, Schritte 1–4)

### Bausteine und Fallen

- Benutzen statt nachbauen: `landseg ansicht` für die Bilder, `pruefen`, `zusammentragen`, `naht`, `einigung finden|messen` als Funktionen des Pakets; Fassungsnamen und -ordner aus `einstellungen/seite.json`; `landseg.dateien`/`naht.lese_bild` als gemeinsame Leser (kein weiterer eigener Bildleser, siehe Altlast A5); die Skripte der Vorbilder sind Vorlage der Logik, nicht zum Kopieren mit festen Pfaden (`BASIS`, `T0`, `D` sind dort fest verdrahtet).
- Falle Benennung: In den T0-Skripten heißt die feste Liste „A“ und die freie Abgabe „C“; heute ist A = „Alles frei“, B = „Kategorien frei“, C = „Feste Kategorienliste“ — genau dieser Tausch war der Anlass (`workflow.js:28`, stumme Fehler). Darum eine Tabelle, ein Test mit vertauschter Zuordnung (AK4).
- Falle Vorstufe: Die GPU-Vorstufe (`vorstufe`) bleibt eigener Befehl mit Belegung über `maschine.py belegen --maschine gpu`; `vorbereiten` ruft sie nicht selbst, sondern prüft nur, dass das Ergebnis da ist und zu den Einstellungen passt (Ordner `vorstufe/`, `--neu` nur ohne GPU). Tests laufen ohne GPU und ohne SAM 3.
- Falle Handlungsfreiheit: Die Urteils-Agents segmentieren nach (Entscheidung 2026-11-18); `zusammenfuehren` liest die Karten in `<fassungsordner>/<tk>/` (Eingriffe schon eingearbeitet), zählt die Eingriffe je Fassung und ändert die Urteile selbst nie; die Gegenprobe (`c-feste-liste/gegenprobe/`) geht in keine Karte ein.
- Falle Schwesterwünsche: `effiz-viertel` (K7: ein Agent je Viertel) ändert Plan und Einheiten der Aufträge, `effiz-buendel` (K6) die Bündelgröße der Einigung, `effiz-befehle` (K2) die Auftragsvorlagen. Darum Einheit des Plans (Teilkachel oder Viertel) und Bündel-Mindestgröße als Einstellung führen, nicht als Zahl im Code; Auftragstext nur aus Vorlagen setzen. Empfehlung für die Reihenfolge der Hauptsession: nach `effiz-viertel` und `effiz-befehle` einreihen oder die Einstellungen früh abstimmen.
- Daten: Alles Abgeleitete unter `daten/landseg/…` (Ziel per Option, nie im Repo); Originalbilder unter `daten/luftbilder/` nur lesen; vor jedem Schreiben in einen Ordner mit Inhalt Abbruch statt Überschreiben (Option `--ersetzen` nur ausdrücklich), damit ein Fehlaufruf keine Fassung zerstört.
- Zeit: Tests nur Mini-Ausschnitt (wenige Sekunden); die volle Suite läuft beim Einreihen (Profil, `zeit: 90`).

### Bauweise

Richtung: ohne Zielbild
Berührt: keine — die neuen Befehle fassen weder `ansicht._kandidaten_lesen` (A1) noch `seite`/`gesamt_projekt` (A2–A4) noch `pruefen` (A6) an; sie benutzen die gemeinsamen Leser (A5 nicht erweitern)
Tilgt: keine
Flick-Signale: keine — kein Vorgänger an derselben Stelle: die Ermittlung `landseg-effiz` änderte nichts; die Geschwister `effiz-*` ändern Vorlagen, Plan und Bündel, nicht die beiden neuen Befehle; die bisherigen Skripte lagen als Wegwerf-Skripte in `wuensche/`, nicht im Repo. Repo ohne Zielbild: Bauzustand ermitteln
Anbau: zwei neue Unterbefehle samt Einstellungsdatei und Tests, vorhandene Funktionen werden nur aufgerufen — Dauer mittel — Risiko gering (stumme Fehler fangen die Tests; Gleichwertigkeit gegen H0 in AK5) — danach bleibt: jeder künftige Lauf (Orthofoto, weitere Jahrgänge) nutzt dieselben Befehle
Umbau: –
Belege: –
Empfehlung: Anbau — kein Umbau nötig; die Logik liegt als Wegwerf-Skripte außerhalb des Repos und wird neu im Paket abgelegt, keine Altlast im Repo wird berührt

Reihenfolge der Repos: landseg · Risiken: Gleichwertigkeit mit dem Agent-Stand (AK5), Überschneidung mit `effiz-viertel`, `effiz-befehle`, `effiz-buendel` (gleiche Aufträge und Pläne), Fassungsbuchstaben nicht vertauschen (AK4), Umsetzer-Lauf groß (rund 1.100 Zeilen Vorbild; wenn 50 Aufrufe nicht reichen, Aufruf-Budget setzen) · Vorbedingungen: keine

## Teile

nicht nötig (Größe mittel, ein Repo, ein Umsetzer-Lauf)

## Varianten

nicht nötig (keine sichtbare Entwurfsfrage)

## Entwurf

Stufe: nein — nur Befehle und Dateien, keine Oberfläche
