# K3: Kostenmessung je Phase und Agent aus den Transkripten als festes Werkzeug (wie `kachellauf messung`, mit gelesenen T

Kurzname: effiz-kosten | Datum: 2026-11-18 | Größe: klein | Bereich: victor | Repos: landseg | Status: eingereiht | Herkunft: Ermittlung landseg-effiz K3

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

K3: Kostenmessung je Phase und Agent aus den Transkripten als festes Werkzeug (wie `kachellauf messung`, mit gelesenen Tokens und USD), nach jedem Lauf im Bericht — Gewinn: macht jeden weiteren Gewinn belegbar; T0-Zahlen enthielten das Wiederlesen nicht — Aufwand klein — Risiko gering — Repo landseg — empfohlen

Belege: wuensche/2026-11-18-landseg-effiz/bericht.md, K3.

Empfehlung der Deutung (wuensche/2026-11-18-landseg-effiz.md, Abschnitt Empfehlung):
- K3: trägt teilweise — beantwortet keine der Fragen selbst, macht aber jeden Gewinn belegbar; die T0-Zahl 3,30 Mio. enthielt das Wiederlesen nicht (H0: 403 Mio. gelesen).
- Nächster Schritt: K2 als Folge-Wunsch — er bringt den größten Gewinn (geschätzt 35–60 USD und 5–10 min je Lauf) und ist genau der Schritt, der im Stitcher gewirkt hat. Für die Läufe auf dem ganzen Orthofoto zählt jede gesparte Runde, weil sie das Wiederlesen des ganzen Kontexts spart.
- Gegenargument: Der Gewinn von K2 ist nur geschätzt. Im Stitcher ließen sich die fünf Maßnahmen von runden-straffen nicht trennen, und selbst danach schrieb ein Agent weiter eigene Skripte für Ansichtsbilder, das Zeitziel wurde verfehlt (bericht.md S1). Ein Teil unserer Skripte ist echte Fachhilfe (`wscheide.py`, B2). — Der Schritt gilt trotzdem: Die mechanischen Wiederholungen (urteil.json und Abgabe bauen, Zoombilder) schreibt jeder Agent neu, und der Gewinn lässt sich am nächsten Lauf mit derselben Transkript-Auswertung gegen H0 nachmessen.

## Fragen

Keine offenen Fragen.

## Entscheidungen

entscheidungen.md: nichts für diesen Wunsch
- 2026-11-18: Landschafts-Segmente: gröbere Flächen auf alten Schwarz-Weiß-Bildern: Nutzer am 18.11.2026: „außerdem solle die Flächen in den schwarz weiß, niedrig aufgelösten Landschaftsbildern nicht ganz so fein sein. Die wirklich feine Untersuchung funktioniert gut auf hochaufgelösten Bildern aber nicht auf den alte[n]“. Daraus: Auf alten, niedrig aufgelösten Schwarz-Weiß-Bildern (heute H0, Luftbild 1968) werden Flächen deutlich gröber gezogen als auf Farb-Orthofotos (T0); feines Nachsegmentieren gilt dort nur für klar erkennbare Objekte. Verschärft für SW-Bilder die Neuklärung „eher gröber, Agents dürfen nachsegmentieren“ (landseg-historisch); im H0-Lauf kam Fassung A auf 1833 Segmente (T0 607). Wie grob genau und ob H0 neu läuft, klärt der Wunsch landseg-sw-grob. (aus entscheidungen.md, 2026-11-18)

## Arbeitsauftrag

### Abnahmekriterien

AK1: Ein Befehl `PY -B -m landseg messung --transkripte <Ordner> [--lauf <Name>] [--ziel <Ordner>]` liest die `agent-*.jsonl` eines Laufs samt `agent-*.meta.json` (Phase, Modell) und gibt je Phase und zusammen eine Tabelle aus: Agents, Wand-Minuten, Agent-Minuten, Runden, gelesene, neue und ausgegebene Tokens, USD, dazu Bilder gelesen und eigene .py geschrieben — prüfbar: `PY -B -m unittest tests.test_messung`
AK2: Preise und Zählregeln sind die des Stitchers und des Plugins (Opus 4 / 8 bei 1 h-Cache-Schreiben / 0,20 / 20 USD je Mio., Sonnet die Hälfte; mehrfach vorkommende Antworten einer Nachricht nur einmal gezählt); ein Test mit kleinem Beispiel-Transkript rechnet von Hand nach — prüfbar: `PY -B -m unittest tests.test_messung`
AK3: Der Befehl schreibt `messung.json` und `messung.md` (dieselbe Tabelle) in `--ziel`, damit sie in den Bericht des Laufs übernommen werden; er ändert die Transkripte nie und stürzt bei kaputten Zeilen oder fehlender `meta.json` nicht ab (Phase `?`) — prüfbar: `PY -B -m unittest tests.test_messung`
AK4: Am echten Lauf H0 (Protokollordner von wf_62f47ff3-c51, 71 Agents) stimmen die Summen mit dem Bericht `landseg-effiz` überein: 71 Agents, rund 403 Mio. gelesen, 9,9 Mio. neu, rund 221 USD (Abweichung unter 2 %) — prüfbar: `PY -B -m landseg messung --transkripte <Protokollordner H0> --ziel <Wegwerf-Ordner>`, Vergleich mit `wuensche/2026-11-18-landseg-effiz/roh/transkripte.txt`
AK5: `landseg/betrieb.md`, `README.md` und `vorlagen/README.md` nennen den Befehl mit Aufruf und die Regel, ihn nach jedem Lauf zu fahren und die Tabelle in den Bericht zu übernehmen — prüfbar: Lesen dieser drei Dateien
AK6: Die ganze Testreihe des Repos bleibt grün — prüfbar: nachts: ganze Testreihe

Nacharbeit: Profil `landseg.md` (Abschnitt Routinen) um den neuen Befehl ergänzen (Profilpflege nach dem Einreihen, kein AK).

### Einstieg

- landseg: `landseg/__main__.py:317-480` — Unterbefehle als argparse-Einträge; hier kommt `messung` als neuer Unterbefehl dazu.
- landseg: `landseg/messung.py` (neu) — Transkripte lesen, zählen, Tabelle bauen, nach dem Vorbild der Stitcher-Datei, nicht daraus importiert.
- landseg: `tests/test_messung.py` (neu) — Beispiel-Transkripte in `unittest`-Temp-Ordnern.
- Vorbild (nur lesen): `C:/Users/Phil/Developement/websites/nai/stitcher/scripts/seg_datensatz/kachellauf.py:962-1097` (`preis`, `transkript_lesen`, `_zaehle`, `messung`, `tabelle`); Preise: `C:/Users/Phil/Developement/wunsch-system/plugins/wunsch/server/kern_auswertung.py:72` (`PREIS`).
- landseg: `landseg/betrieb.md`, `README.md`, `vorlagen/README.md` — Hinweis auf den Befehl.

### Bausteine und Fallen

- Die Aufträge von landseg tragen anders als im Stitcher keine Kopfzeile `Lauf … | Stufe …`; die Phase steht in `agent-*.meta.json` (`workflowPhase`, `model`; Vorbild `kern_auswertung.py:177-195`). Das Kopfzeilen-Parsing des Stitchers nicht übernehmen.
- Tokens je Nachricht nur einmal zählen (Nachrichten-Kennung merken, wie `kachellauf.py:1004`). Gelesen = `cache_read_input_tokens`, neu = Eingabe + Cache-Schreiben.
- Preise als Konstante mit Stand-Datum; die Zahlen sind Rechenwert nach Listenpreis, keine Abo-Kosten (im Tabellenkopf sagen).
- Nur Standardbibliothek; Transkripte mit `encoding="utf-8", errors="replace"` nur lesen.
- Der Protokollordner liegt im Claude-Projektordner des Laufs; der Befehl bekommt ihn als Argument und sucht nicht selbst.
- Stitcher und Plugin nicht ändern.

### Bauweise

Richtung: ohne Zielbild (kein `zielbild.md`; Maßstab ist ein sauberer Aufbau — Bauzustand ermitteln)
Berührt: keine
Tilgt: keine
Flick-Signale: keine — kein Vorgänger (Herkunft ist eine Ermittlung, kein Wunsch am selben Ort)
Anbau: neuer Unterbefehl und eigene Datei, Tabelle nach Stitcher-Vorbild — Dauer kurz — Risiko gering — danach bleibt ein eigener kleiner Zählcode neben dem des Stitchers (Preistabelle doppelt gepflegt).
Belege: –
Empfehlung: Anbau — keine Altlast berührt, Wiederverwendung des Stitcher-Codes ist wegen getrennter Repos nicht möglich.

Reihenfolge der Repos: landseg · Risiken: Preise veralten (Konstante mit Datum) · Vorbedingungen: keine

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
