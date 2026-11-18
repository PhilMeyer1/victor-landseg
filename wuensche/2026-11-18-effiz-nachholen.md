# K1: Nachhol-Prüfung im Workflow reparieren: Soll-Zahl = geplante Segmente plus Zugänge aus "eingriffe" bzw.

Kurzname: effiz-nachholen | Datum: 2026-11-18 | Größe: klein | Bereich: victor | Repos: landseg | Status: eingereiht (ohne Commit) | Herkunft: Ermittlung landseg-effiz K1 | Ergebnis: ohne Commit

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

K1: Nachhol-Prüfung im Workflow reparieren: Soll-Zahl = geplante Segmente plus Zugänge aus "eingriffe" bzw. nur `ok`/`kontrolle_ok` werten (`workflow.js:404`, auch in Folge-Workflows) — Gewinn rund 20 USD, 8 Agents, 10 min Wand je Lauf wie H0 — Aufwand klein — Risiko gering (echte Fehlabgaben müssen weiter auffallen) — Repo landseg (Workflow im Wunsch-Ordner) — empfohlen

Belege: wuensche/2026-11-18-landseg-effiz/bericht.md, K1.

Empfehlung der Deutung (wuensche/2026-11-18-landseg-effiz.md, Abschnitt Empfehlung):
- K1: trägt — der sicherste unnötige Schritt, im Code belegt (`workflow.js:404`, gleich in `workflow-fein.js:340`): 8 Agents, 20,4 USD, 9,8 min Wand, kleiner Aufwand.
- Nächster Schritt: K2 als Folge-Wunsch — er bringt den größten Gewinn (geschätzt 35–60 USD und 5–10 min je Lauf) und ist genau der Schritt, der im Stitcher gewirkt hat. Für die Läufe auf dem ganzen Orthofoto zählt jede gesparte Runde, weil sie das Wiederlesen des ganzen Kontexts spart.
- Gegenargument: Der Gewinn von K2 ist nur geschätzt. Im Stitcher ließen sich die fünf Maßnahmen von runden-straffen nicht trennen, und selbst danach schrieb ein Agent weiter eigene Skripte für Ansichtsbilder, das Zeitziel wurde verfehlt (bericht.md S1). Ein Teil unserer Skripte ist echte Fachhilfe (`wscheide.py`, B2). — Der Schritt gilt trotzdem: Die mechanischen Wiederholungen (urteil.json und Abgabe bauen, Zoombilder) schreibt jeder Agent neu, und der Gewinn lässt sich am nächsten Lauf mit derselben Transkript-Auswertung gegen H0 nachmessen.

## Fragen

<Prüfer: nur Fragen, die ohne Code-Wissen beantwortbar sind; jede mit Empfehlung>

## Entscheidungen

- Nutzer am 18.11.2026 nach der Ermittlung landseg-effiz: alle Kandidaten K1–K6 bauen (Nachhol-Prüfung reparieren, fertige landseg-Befehle statt eigener Skripte, Kostenmessung je Phase, Bilder nur einmal verlangen, Vorbereitung und Zusammenführen als feste Befehle, kleine Einigungsbündel zusammenlegen) und K7: künftig ein Urteils-Agent je Viertel statt je Teilkachel. (aus entscheidungen.md, 2026-11-18)
- Übrige Zeilen aus entscheidungen.md gelten für Urteile und Einigung, nicht für diese Korrektur.
- 2026-11-18: Landschafts-Segmente: gröbere Flächen auf alten Schwarz-Weiß-Bildern: Nutzer am 18.11.2026: „außerdem solle die Flächen in den schwarz weiß, niedrig aufgelösten Landschaftsbildern nicht ganz so fein sein. Die wirklich feine Untersuchung funktioniert gut auf hochaufgelösten Bildern aber nicht auf den alte[n]“. Daraus: Auf alten, niedrig aufgelösten Schwarz-Weiß-Bildern (heute H0, Luftbild 1968) werden Flächen deutlich gröber gezogen als auf Farb-Orthofotos (T0); feines Nachsegmentieren gilt dort nur für klar erkennbare Objekte. Verschärft für SW-Bilder die Neuklärung „eher gröber, Agents dürfen nachsegmentieren“ (landseg-historisch); im H0-Lauf kam Fassung A auf 1833 Segmente (T0 607). Wie grob genau und ob H0 neu läuft, klärt der Wunsch landseg-sw-grob. (aus entscheidungen.md, 2026-11-18)

## Arbeitsauftrag

<Prüfer beim Klären, für Umsetzer und Abnahme. Bei kleinen Wünschen ohne Klärung schreibt die
Hauptsession nur die Abnahmekriterien; bei einem Teil übernimmt sie dessen Kriterien aus dem
Mutterwunsch.>

### Abnahmekriterien

AK1: Ein Urteils-Viertel, das mit `ok` und `kontrolle_ok` zurückkommt, wird nicht mehr nachgeholt, auch wenn seine Segmentzahl von der geplanten abweicht (etwa durch Nachsegmentieren) — prüfbar: Lesen `workflow.js` Block 9b: die Bedingung für `schlecht` enthält keinen Vergleich `segmente !== e.n` mehr als Nachhol-Grund
AK2: Ein Viertel mit `ok=false` oder `kontrolle_ok=false` oder ganz ohne Rückmeldung wird weiter nachgeholt, Fassung A bleibt ausgenommen — prüfbar: Lesen `workflow.js` Block 9b: `!r.ok` (gilt auch für fehlende Gruppen, Zeile 401) bleibt Nachhol-Grund, `r.e.art !== 'a'` bleibt
AK3: Eine abweichende Segmentzahl geht nicht verloren: Das Protokoll nennt sie je Viertel als Hinweis (Soll, Ist) und der Rückgabewert des Workflows enthält die Liste — prüfbar: Lesen `workflow.js` Block 9b und Rückgabe (`return`-Objekte)
AK4: Dieselbe Änderung steht gleichlautend in `workflow-fein.js` — prüfbar: Lesen `workflow-fein.js` Block 9b (Zeile um 340)
AK5: Beide Dateien sind gültiges JavaScript — prüfbar: `node --check <datei>` für beide (der Workflow-Tool-Rahmen kann `await` auf oberster Ebene haben: schlägt `--check` nur deshalb fehl, vorher mit `node --check` an der unveränderten Datei gegenprobieren und den Befund vergleichen)
AK6: Ein Probelauf der Auswahl mit vier erfundenen Zeilen (ok mit anderer Segmentzahl, ok mit gleicher Zahl, `ok=false`, Fassung A mit `ok=false`) wählt nur die dritte zum Nachholen — prüfbar: kurzes Node-Skript im Scratchpad, das die Zeile `const schlecht = …` aus der Datei ausschneidet und auf diese Zeilen anwendet

### Einstieg

- landseg (Workflow im Wunsch-Ordner, nicht im Repo): `wuensche/2026-11-18-landseg-historisch-3/workflow.js:404` — `schlecht` nimmt `!r.ok` oder Segmentzahl ≠ `e.n` (geplante Zahl); die zweite Bedingung ändert sich: Zahlenabweichung ist kein Nachhol-Grund mehr
- landseg (ebenso): `wuensche/2026-11-18-landseg-historisch-3/workflow-fein.js:340` — gleiche Zeile, gleiche Änderung
- landseg (ebenso): `workflow.js:392-394` — `zeilen` trägt `segmente` und `e.n`; daraus entsteht der Hinweis
- landseg (ebenso): `workflow.js:433` und die weiteren `return`-Objekte — `nachhol_rest` steht dort schon; Hinweisliste `segmentzahl_abweichung` daneben

### Bausteine und Fallen

- Die Quittung (`QUITTUNG_URTEIL`, Zeile 102) hat kein Feld für Eingriffe; `ok` und `kontrolle_ok` kommen vom Agent nach der Kontrolle aus dem Auftrag (Zeile 211/234 erlauben Teilen ausdrücklich). Entscheidung der Klärung: kein neues Feld, die Soll-Zahl entfällt als Nachhol-Grund und bleibt als Hinweis; nicht „geplant plus Zugänge" nachrechnen (der Agent müsste die Zugänge zählen, das ist neue Last).
- Falle: `MAX_NACHHOLEN` (Zeile 77) und `nachholPrompt` unverändert lassen; nur die Auswahl ändert sich.
- Falle: Die Dateien liegen in `wuensche/` (Basisordner-Repo), nicht in der Arbeitskopie von landseg; der Umsetzer ändert sie dort und die Hauptsession reiht sie mit `wish(effiz-nachholen)` ein. Kein Eingriff in die schon gelaufenen Ergebnisse von historisch-3.
- Spätere Workflows (historisch-4, 5, `effiz-viertel` K7) kopieren diese Dateien oder bauen sie um; sie erben die Korrektur, wenn sie nach dem Einreihen von dieser Fassung ausgehen: `Nacharbeit: effiz-viertel und spätere Workflow-Kopien auf die neue Auswahlzeile prüfen` (Zeile 404/340 suchen).

### Bauweise

Richtung: neutral
Berührt: keine — kleine Korrektur an einer Bedingung im Ablaufskript, keine Altlast aus dem Register
Tilgt: keine
Flick-Signale: keine — kein Vorgänger in Kette (Herkunft ist die Ermittlung landseg-effiz, kein Glied dieser Stelle)
Anbau: Bedingung vereinfachen, Hinweis ausgeben — Dauer kurz — Risiko gering — danach bleibt die Kopie in zwei Dateien (workflow.js, workflow-fein.js)
Belege: –
Empfehlung: – — kein Umbau nötig

Reihenfolge der Repos: landseg · Risiken: echte Fehlabgaben dürfen nicht verschluckt werden (AK2); eine Fehlabgabe mit `ok=true` aber falscher Zahl wird nur als Hinweis gemeldet, die Einigung und das Zusammenführen fangen sie weiter ab · Vorbedingungen: keine

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

## Nachweis

- 2026-11-18: Reparatur in wuensche/2026-11-18-landseg-historisch-3/workflow.js und workflow-fein.js (nur ok/kontrolle_ok löst Nachholen aus, Segmentzahl-Abweichung als Hinweis segmentzahl_abweichung), abgenommen im Lauf 20261118l, im Basisordner-Repo committet als aaa5ebe.
