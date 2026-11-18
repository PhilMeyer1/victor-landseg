# K7: Kontext je Urteils-Agent kürzen, indem ein Agent je Viertel statt je Teilkachel arbeitet — Gewinn vermutet 30–50 % d

Kurzname: effiz-viertel | Datum: 2026-11-18 | Größe: mittel | Bereich: victor | Repos: landseg | Status: eingereiht | Herkunft: Ermittlung landseg-effiz K7

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

K7: Kontext je Urteils-Agent kürzen, indem ein Agent je Viertel statt je Teilkachel arbeitet — Gewinn vermutet 30–50 % der gelesenen Tokens in den Urteilen — Aufwand klein — Risiko: widerspricht der Entscheidung vom 17.11. („14 Agents statt 42", `entscheidungen.md:17`) und verliert Zusammenhang — Repo landseg — nur mit Freigabe

Belege: wuensche/2026-11-18-landseg-effiz/bericht.md, K7.

Empfehlung der Deutung (wuensche/2026-11-18-landseg-effiz.md, Abschnitt Empfehlung):
- K7: trägt nicht — kein Stitcher-Ansatz, Gewinn nur vermutet, und er widerspricht deiner Entscheidung vom 17.11. (`entscheidungen.md:17`); F1 bleibt offen.
- Nächster Schritt: K2 als Folge-Wunsch — er bringt den größten Gewinn (geschätzt 35–60 USD und 5–10 min je Lauf) und ist genau der Schritt, der im Stitcher gewirkt hat. Für die Läufe auf dem ganzen Orthofoto zählt jede gesparte Runde, weil sie das Wiederlesen des ganzen Kontexts spart.
- Gegenargument: Der Gewinn von K2 ist nur geschätzt. Im Stitcher ließen sich die fünf Maßnahmen von runden-straffen nicht trennen, und selbst danach schrieb ein Agent weiter eigene Skripte für Ansichtsbilder, das Zeitziel wurde verfehlt (bericht.md S1). Ein Teil unserer Skripte ist echte Fachhilfe (`wscheide.py`, B2). — Der Schritt gilt trotzdem: Die mechanischen Wiederholungen (urteil.json und Abgabe bauen, Zoombilder) schreibt jeder Agent neu, und der Gewinn lässt sich am nächsten Lauf mit derselben Transkript-Auswertung gegen H0 nachmessen.

## Fragen

keine (die Grundsatzfrage ist am 18.11. entschieden, siehe Entscheidungen)

## Entscheidungen

- 2026-11-17 | landseg | Landschafts-Segmente: ein Agent je Teilkachel, sieht erst ganz T0 — 14 Agents statt 42; für die Urteile ersetzt durch die Zeile vom 18.11. (aus entscheidungen.md, 2026-11-17)
- 2026-11-18 | landseg | Landschafts-Segmente: Effizienz der Agents, ein Agent je Viertel — Nutzer am 18.11.2026: K1–K7 bauen; K7: künftig ein Urteils-Agent je Viertel statt je Teilkachel, um den Kontext kurz zu halten. Ersetzt für die Urteile „ein Agent je Teilkachel, arbeitet die vier Viertel nacheinander ab“; jeder Agent sieht weiter zuerst den ganzen Ausschnitt und seine ganze Teilkachel, dann sein Viertel. (aus entscheidungen.md, 2026-11-18)
- 2026-11-18 | landseg | Vorstufe eher grob, Agents segmentieren selbst nach (Stapel je Viertel, tokengünstig) (aus entscheidungen.md, 2026-11-18)
- 2026-11-18 | landseg | Einigung an den Übergängen als fester Schritt nach den Urteilen (aus entscheidungen.md, 2026-11-18)
- Auslegung des Prüfers: Die Empfehlung der Deutung („K7 trägt nicht“) und die Entscheidung vom 18.11. widersprechen sich; die Entscheidung des Nutzers gilt, der Wunsch wird gebaut. Der Gewinn bleibt Vermutung und wird nachgemessen (AK4).
- 2026-11-18: Landschafts-Segmente: gröbere Flächen auf alten Schwarz-Weiß-Bildern: Nutzer am 18.11.2026: „außerdem solle die Flächen in den schwarz weiß, niedrig aufgelösten Landschaftsbildern nicht ganz so fein sein. Die wirklich feine Untersuchung funktioniert gut auf hochaufgelösten Bildern aber nicht auf den alte[n]“. Daraus: Auf alten, niedrig aufgelösten Schwarz-Weiß-Bildern (heute H0, Luftbild 1968) werden Flächen deutlich gröber gezogen als auf Farb-Orthofotos (T0); feines Nachsegmentieren gilt dort nur für klar erkennbare Objekte. Verschärft für SW-Bilder die Neuklärung „eher gröber, Agents dürfen nachsegmentieren“ (landseg-historisch); im H0-Lauf kam Fassung A auf 1833 Segmente (T0 607). Wie grob genau und ob H0 neu läuft, klärt der Wunsch landseg-sw-grob. (aus entscheidungen.md, 2026-11-18)

## Arbeitsauftrag

<Prüfer beim Klären, für Umsetzer und Abnahme. Bei kleinen Wünschen ohne Klärung schreibt die
Hauptsession nur die Abnahmekriterien; bei einem Teil übernimmt sie dessen Kriterien aus dem
Mutterwunsch.>

### Abnahmekriterien

AK1: Für Fassungen B, C und die Gegenprobe gibt es je Viertel genau einen Urteils-Agent mit genau einem Viertel-Auftrag; ein Segment steht in genau einem Auftrag (Gruppierung 4 je Teilkachel statt 1) — prüfbar: Befehl: Plan-Test (Einheiten je Fassung und Teilkachel in Agent-Gruppen umrechnen, Zahl und Eindeutigkeit prüfen; Test in tests/)
AK2: Der Prompt eines Viertel-Agents verlangt zuerst den ganzen Ausschnitt, dann die ganze Teilkachel, dann nur sein Viertel; „arbeite die Viertel nacheinander ab“ und „bist das du selbst“ kommen nicht mehr vor — prüfbar: Lesen der Prompt-Vorlage und des Tests dazu
AK3: Fassung A (alles frei, ohne Viertel-Aufträge) bleibt ein Agent je Teilkachel; Nachholen, Vereinheitlichen, Nähte und Einigung arbeiten unverändert mit dem Ergebnis je Viertel — prüfbar: Befehl: Plan-Test für Fassung A und `PY -B -m unittest discover -s tests -t .` (bestehende Tests grün)
AK4: Die Kostenmessung aus den Transkripten (Prüfbefehl der Wünsche K3/effiz-kosten, sonst die Auswertung aus `landseg/betrieb.md`) liefert für den nächsten Urteilslauf gelesene Tokens je Agent und je Fassung, damit der Gewinn gegen H0 (Mittel 54 Bilder, 9,9 Mio. gelesen gesamt laut Bericht B3) nachgeprüft werden kann — prüfbar: nachts: nächster Produktionslauf, Vergleich gegen H0; vorab Lesen `landseg/betrieb.md`
AK5: Der Weg des Nutzers: Ein Urteilslauf auf dem kleinen Testausschnitt (eine Teilkachel, zwei Viertel, unter zwei Minuten Plan und Prompt-Aufbau, ohne Agent-Läufe) zeigt je Viertel einen Auftrag, und die Zahl der Agents steht im Log — prüfbar: Befehl: Trockenlauf des Plans auf `daten/landseg/H0/manifest.json`

### Einstieg

- landseg: `vorlagen/urteil.md:1-4` — Vorlage „je Teilkachel“; erhält eine Viertel-Fassung (ein Viertel, Gesamtbild und Teilkachel nur als Zusammenhang)
- landseg: `.claude/skills/landseg-agent/SKILL.md` — Regeln der Agents; prüfen, ob Sätze „arbeite alle Viertel“ dort stehen
- landseg: `README.md` / `landseg/betrieb.md` — Betrieb des Urteilslaufs; Gruppierung (ein Agent je Viertel) und Fassung A dort festhalten
- Nacharbeit: Gruppierung und Prompt liegen heute im Laufskript `wuensche/2026-11-18-landseg-historisch-3/workflow.js:92-99,215-241,368-381` (`gruppenMap` nach `art:tk`, `urteilPrompt`), außerhalb des Repos; der Umsetzer baut Gruppierung und Prompt als Baustein im Repo (z. B. Plan-Modul mit Test) und der Lauf-Workflow des nächsten Urteilslaufs ruft ihn auf

### Bausteine und Fallen

- Gruppierung nach `art + ':' + tk` ändern in `art + ':' + tk + ':v' + v` (nur B, C, z; A hat v = 0). Label, Ergebnisordner und Quittung (`QUITTUNG_URTEIL`, `teile`) tragen die Viertelnummer schon.
- Grundlast: Jeder der vier Agents liest H0 und seine Teilkachel neu; das Übersichtsbild einmal je Agent verlangen (nicht doppelt wie in B4, K4/effiz-bilder baut das), sonst frisst es den Gewinn.
- Segmente an der Viertelgrenze: nur in dem Auftrag, in dessen Liste sie stehen (auch Teilstücke); Nachbar-Viertel sieht der Agent nur auf dem Gesamtbild. Ein Stapel `eingriffe` je Viertel bleibt, jeder Agent schreibt auf eine Karte: die vier Agents einer Teilkachel teilen sich `labels.tif`; Schreibzugriffe nacheinander oder je Viertel eigene Kartenkopie klären (Stand: nur ein Agent schrieb). Echte Falle, vor dem Bau prüfen.
- Nachholen (MAX_NACHHOLEN = 8) wird seltener nötig, die Soll-Zahl-Prüfung bleibt Sache von K1/effiz-nachholen.
- Der Gewinn von 30–50 % ist nur vermutet; mehr Agents heißt mehr Grundlast (Skill, Vorlage, Übersicht), je Agent weniger Verlauf.

### Bauweise

<Prüfer, Pflicht: ob der Wunsch das Repo seinem Zielbild (`<repo>/zielbild.md`) näherbringt, es
unberührt lässt oder davon wegführt; Anbau, Umbau, Belege und Empfehlung nur, wenn er eine Altlast
aus `<repo>/altlasten.md` berührt, ein Anbau vom Zielbild wegführen würde oder `Flick-Signale`
belegt sind, dann dazu die Frage „Weiter anbauen, umbauen oder ganz neu bauen" unter „Fragen".>
Richtung: neutral
Berührt: keine
Tilgt: keine
Flick-Signale: keine — kein Vorgänger (Herkunft ist eine Ermittlung; die Geschwister effiz-* laufen parallel und sind keine Glieder)
Anbau: Gruppierung und Prompt je Viertel als Baustein im Repo — Dauer kurz — Risiko mittel (Kartenkopie je Viertel, Gewinn ungemessen) — danach bleibt Fassung A je Teilkachel
Umbau: –
Belege: –
Empfehlung: Anbau — keine Altlast berührt, kein zweiter Weg (der alte Lauf je Teilkachel wird ersetzt)

Reihenfolge der Repos: landseg · Risiken: gemeinsame Label-Karte der vier Viertel-Agents, Gewinn nur vermutet · Vorbedingungen: keine

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

Stufe: nein — keine Oberfläche, nur Aufteilung der Agent-Arbeit
