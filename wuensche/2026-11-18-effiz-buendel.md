# K6: Kleine Einigungsbündel zu einem Agent zusammenlegen (unter einer Mindestzahl Paare) — Gewinn rund 5 USD und weniger

Kurzname: effiz-buendel | Datum: 2026-11-18 | Größe: klein | Bereich: victor | Repos: landseg | Status: eingereiht | Herkunft: Ermittlung landseg-effiz K6

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

K6: Kleine Einigungsbündel zu einem Agent zusammenlegen (unter einer Mindestzahl Paare) — Gewinn rund 5 USD und weniger Agent-Starts je Lauf — Aufwand klein — Risiko gering — Repo landseg — optional

Belege: wuensche/2026-11-18-landseg-effiz/bericht.md, K6.

Empfehlung der Deutung (wuensche/2026-11-18-landseg-effiz.md, Abschnitt Empfehlung):
- K6: trägt teilweise — entspricht dem Zusammenlegen im Stitcher, bringt aber nur rund 5 von 70,7 USD der Einigung; die Paarzahl je Bündel ist nicht geprüft.
- Nächster Schritt: K2 als Folge-Wunsch — er bringt den größten Gewinn (geschätzt 35–60 USD und 5–10 min je Lauf) und ist genau der Schritt, der im Stitcher gewirkt hat. Für die Läufe auf dem ganzen Orthofoto zählt jede gesparte Runde, weil sie das Wiederlesen des ganzen Kontexts spart.
- Gegenargument: Der Gewinn von K2 ist nur geschätzt. Im Stitcher ließen sich die fünf Maßnahmen von runden-straffen nicht trennen, und selbst danach schrieb ein Agent weiter eigene Skripte für Ansichtsbilder, das Zeitziel wurde verfehlt (bericht.md S1). Ein Teil unserer Skripte ist echte Fachhilfe (`wscheide.py`, B2). — Der Schritt gilt trotzdem: Die mechanischen Wiederholungen (urteil.json und Abgabe bauen, Zoombilder) schreibt jeder Agent neu, und der Gewinn lässt sich am nächsten Lauf mit derselben Transkript-Auswertung gegen H0 nachmessen.

## Fragen

Keine offenen Fragen.

## Entscheidungen

- entscheidungen.md: nichts für diesen Wunsch (geprüft: Grundsätze und Einigungszeilen vom 17./18.11. verlangen nichts zur Bündelgröße; „Push nur auf Ansage" gilt, hier ohne Belang).
- Befund der Klärung (keine Nutzerantwort): Das Zusammenlegen kleiner Gruppen gibt es schon (`buendeln`, Obergrenze `buendel_paare` = 12). Der Wunsch ist deshalb enger: die verbleibenden kleinen Bündel besser auffüllen, nicht eine Mindestzahl neu einführen.
- 2026-11-18: Landschafts-Segmente: gröbere Flächen auf alten Schwarz-Weiß-Bildern: Nutzer am 18.11.2026: „außerdem solle die Flächen in den schwarz weiß, niedrig aufgelösten Landschaftsbildern nicht ganz so fein sein. Die wirklich feine Untersuchung funktioniert gut auf hochaufgelösten Bildern aber nicht auf den alte[n]“. Daraus: Auf alten, niedrig aufgelösten Schwarz-Weiß-Bildern (heute H0, Luftbild 1968) werden Flächen deutlich gröber gezogen als auf Farb-Orthofotos (T0); feines Nachsegmentieren gilt dort nur für klar erkennbare Objekte. Verschärft für SW-Bilder die Neuklärung „eher gröber, Agents dürfen nachsegmentieren“ (landseg-historisch); im H0-Lauf kam Fassung A auf 1833 Segmente (T0 607). Wie grob genau und ob H0 neu läuft, klärt der Wunsch landseg-sw-grob. (aus entscheidungen.md, 2026-11-18)

## Arbeitsauftrag

### Abnahmekriterien

AK1: Die Einigung packt kleine Gruppen von Segment-Paaren in so wenige Agent-Aufträge wie möglich (höchstens `buendel_paare` Paare je Auftrag), nicht nur in den jeweils letzten — prüfbar: neuer Test in `tests/test_einigung.py`: Gruppen der Größe 7, 9, 3, 2 bei Obergrenze 12 ergeben 2 Bündel statt 3 (`"$PY" -B -m unittest tests.test_einigung`)
AK2: Zusammenhängende Paare bleiben ungeteilt in einem Bündel, eine übergroße Gruppe bleibt ganz und nimmt keine anderen auf, jedes Segment steht in genau einem Bündel — prüfbar: Tests in `tests/test_einigung.py` (vorhandener Ecken-Test und `buendel_paare: 1`-Test grün, dazu ein Test für übergroße Gruppe neben kleinen)
AK3: Die Bündelreihenfolge und Namen bleiben stabil (gleiche Eingabe, gleiche Bündel), die Zahl der Bündel steigt nie gegenüber vorher — prüfbar: Test, der `buendeln` zweimal laufen lässt, und Vergleich mit der alten Zählung an einem Beispiel
AK4: Der Weg des Nutzers: `einigung finden` auf einem vorhandenen Ergebnisordner (T0) läuft durch und nennt in `einigung.json` die Zahl der Bündel, nicht mehr als vorher — prüfbar: `PY -B -m landseg einigung finden …` auf T0-Daten (Befehl und Daten nach `landseg/betrieb.md`), Bündelzahl vorher/nachher im Bericht
AK5: Die volle Testreihe bleibt grün — prüfbar: `"$PY" -B -m unittest discover -s tests -t .`

Nacharbeit: `landseg/README.md` Abschnitt Einigung (Zeile ~335) und `gesamt/ANLEITUNG.md` (Zeile ~213) nennen das Zusammenlegen „der Reihe nach"; Wortlaut anpassen, falls er danach nicht mehr stimmt (Kopie in `gesamt/` nur über den Gesamtprojekt-Weg, nicht von Hand).

### Einstieg

- landseg: `landseg/einigung.py:214-237` — `buendeln`: Gruppen werden der Reihe nach nur in das zuletzt angelegte Bündel gelegt (`buendel[-1]`); ist es voll oder übergroß, bleibt eine kleine Gruppe allein, auch wenn ein früheres Bündel noch Platz hätte. Änderung: kleine Gruppen in das erste Bündel mit Platz legen (first-fit, am besten nach Größe absteigend sortiert), Reihenfolge deterministisch.
- landseg: `landseg/einigung.py:294-330` — `finden` ruft `buendeln` und schreibt je Bündel `auftrag.json`; Namen laufen über `enumerate`, bleiben.
- landseg: `einstellungen/einigung.json:4` — `buendel_paare: 12` (Obergrenze, bleibt).
- landseg: `tests/test_einigung.py:94,106` — vorhandene Tests zu Ecke und `buendel_paare: 1`.

### Bausteine und Fallen

- Nur `buendeln` ändern; Eingabe/Ausgabe (Liste von `{"paare", "uebergross"}`) bleibt, damit `finden` und `anwenden` unberührt sind.
- Falle: Segmente verschiedener Gruppen dürfen nie ein Segment teilen (sonst zwei Urteile für ein Segment); die Union-Find-Gruppierung davor bleibt unverändert, nur das Packen danach ändert sich.
- Falle: Die Paarreihenfolge im Bündel folgt „entlang der Linien" (Nachbarschaft im Bild); beim Auffüllen aus entfernten Bildstellen verliert der Agent etwas Ortsnähe, Kontext je Paar steckt aber im eigenen Bild `paar_<nr>.jpg`. Ein Bündel nie über `buendel_paare` hinaus füllen (A-02 mit 148 Bildlesungen für 8,7 USD zeigt, dass große Bündel teuer werden).
- Ehrlicher Rahmen: Der Gewinn ist unbelegt. Die Paarzahlen je Bündel des Laufs mit 41 Agents sind nicht gelesen (bericht.md B6); bei T0 (52–68 Paare je Fassung, 12 Bündel) ist wenig zu gewinnen. Der Umsetzer nennt im Bericht die Bündelzahl vorher/nachher an den vorhandenen Daten; kommt nichts heraus, ist das ein gültiges Ergebnis.

### Bauweise

Richtung: neutral
Berührt: keine
Tilgt: keine
Flick-Signale: keine — kein Vorgänger (Herkunft ist eine Ermittlung, keine Wunschkette zu `buendeln`)
Empfehlung: – — kleine, abgegrenzte Änderung einer Funktion, kein zweiter Weg, kein neues Muster.

Reihenfolge der Repos: landseg · Risiken: Gewinn unbelegt (Paarzahlen unbekannt); Ortsnähe im Bündel sinkt leicht · Vorbedingungen: keine

### Bauweise

<Prüfer, Pflicht: ob der Wunsch das Repo seinem Zielbild (`<repo>/zielbild.md`) näherbringt, es
unberührt lässt oder davon wegführt; Anbau, Umbau, Belege und Empfehlung nur, wenn er eine Altlast
aus `<repo>/altlasten.md` berührt, ein Anbau vom Zielbild wegführen würde oder `Flick-Signale`
belegt sind, dann dazu die Frage „Weiter anbauen, umbauen oder ganz neu bauen" unter „Fragen".>
Richtung: <zum Zielbild | neutral | vom Zielbild weg | ohne Zielbild>
Berührt: <Nummernliste aus altlasten.md: `A1, A2`, bei mehreren Repos `<repo>: A1, A2; <repo2>: A4` | keine>[ — <Begründung>] (feste Form: assets/formate.md, Abschnitt 8)
Tilgt: <Nummernliste der Altlasten, die nach dem Wunsch ganz erledigt sind (jede auch unter Berührt) | keine>[ — <Begründung>]
Flick-Signale: <S1 bis S4 mit Belegen (Kette mit Datum, Glieder, Tage, Folgeschäden; Stellen) | keine — <Grund je Gliedpaar | kein Vorgänger>>
Anbau: <ein Satz> — Dauer <kurz|mittel|lang> — Risiko <…> — danach bleibt <…>
Umbau: <ein Satz> — Dauer <kurz|mittel|lang> — Risiko <…> — Netz <vorhanden | fehlt: …> — danach entfällt <…>
Belege: <Stellen `<pfad>:<zeile>`, die den Umbau rechtfertigen | –>
Empfehlung: <Anbau | Umbau | –> — <warum, ein Satz>

Reihenfolge der Repos: <…> · Risiken: <…> · Vorbedingungen: <Namen aus dem Profil | keine>

## Teile

<Nur bei Größe gross, vom Prüfer: nummerierte Liste, je Teil
„Name — Umsetzer|Workflow [— Halt: Durchsicht|Wahl|Freigabe] — nach: –|<Nummern> — AK <Nummern> — ein
Satz, was dann fertig ist". `Halt:` nur, wenn der Nutzer vor dem Einreihen durchsieht, wählt oder freigibt.
„nach" nennt die Teile, die vorher eingereiht sein müssen; Teile ohne gemeinsame Stellen laufen
parallel. Die Hauptsession legt je Teil einen eigenen Wunsch <kurzname>-N an.>

## Varianten

<Nur bei Größe mittel mit sichtbarer Entwurfsfrage, vom Prüfer: „a: …" und „b: …", je ein bis
zwei Sätze, was der Nutzer sehen wird. Mit Entwurf zeigt er beide, der Nutzer wählt bei der
Freigabe; ohne Entwurf bauen zwei Umsetzer parallel. Die Wahl steht danach unter „Entscheidungen".>

## Entwurf

<Vom Prüfer beim Klären, nur bei sichtbaren Oberflächen: erste Zeile „Stufe: nein — <Grund>",
„Stufe: skizze", „Stufe: ausgearbeitet" oder „Stufe: nach F<n>"; darunter, was der Entwurf
zeigt: Ansichten, Zustände, Desktop/Handy, Nachbarn, Beispieldaten, Varianten. Der Workflow
`wunsch:entwurf` zeichnet daraus fünf Entwürfe nach `entwurf/` im Berichtsordner; die Freigabe des
Nutzers steht danach unter „Entscheidungen".>
