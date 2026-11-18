# Bericht landseg-effiz (Stufe S, Untersuchung, Eingriff keiner)

## Antwort

Die Stitcher-Session hat die Kosten vor allem mit einem Wunsch gesenkt: `runden-straffen` (Commit
d9a3dd7). Dazu gehören ein kurzes Rollenblatt, fertige Befehle statt eigener Agent-Skripte,
Mechanisches im Code, das Zusammenlegen von Einheiten an denselben Objekten und eine fortlaufende
Gegenprüfung. Gemessen kostete eine Runde danach 3,20 statt 10,43 USD (31 %) und dauerte 12,4 statt
20,8 min; die Masken blieben fast gleich. Dazu kommen ältere Bausteine: Vorsortieren im Code, Messen
je Stufe aus den Transkripten, Haiku bzw. Code für Mechanisches und Opus nur fürs Urteil.

Bei landseg (Lauf wf_62f47ff3-c51, H0) liegen die Kosten dort, wo der Stitcher sie gefunden hat. Die
Agents lesen in jeder Runde ihren wachsenden Verlauf samt Bildern neu ein: 403 Mio. gelesene gegen
9,9 Mio. neue Tokens, rund 221 USD Rechenwert, 71 Agents, 104 min Wand. Unnötig waren sicher die 8
Nachhol-Agents (rund 20 USD, 10 min). Der größte vermeidbare Aufwand ist aber, dass Urteils- und
Einigungs-Agents ihre Werkzeuge selbst schreiben: 84 bzw. 55 eigene .py-Dateien und über 900
Python-Aufrufe ohne `-m landseg`, also Hunderte zusätzliche Runden. Das Rollenblatt bringt bei
landseg wenig, weil der Skill nur 74 Zeilen hat. Die Modellwahl stimmt schon mit der des Stitchers
überein.

Preise: Tabelle des Plugins `C:/Users/Phil/Developement/wunsch-system/plugins/wunsch/server/kern_auswertung.py:73`
(Opus: Eingabe 4, Cache-Schreiben 1 h 8, Cache-Lesen 0,20, Ausgabe 20 USD je Mio.; Sonnet die
Hälfte). Das ist dieselbe Tabelle wie bei `kachellauf messung` im Stitcher. Gegenprobe: Mit diesen
Preisen ergibt die Stufe urteil der Stitcher-Kachel r07c05 aus 16,56/1,01/0,26 Mio. genau 16,59 USD;
die Messung nennt 16,58 USD
(`C:/Users/Phil/Developement/websites/nai/wuensche/2026-11-17-tray-seg-ablauf-4/messung.md`). Alle
USD-Zahlen sind Rechenwert nach Listenpreis, keine Abo-Kosten.

## Teil 1: Ansätze der Stitcher-Session (AK1)

S1: Korrekturrunde gestrafft (Wunsch runden-straffen, Commit d9a3dd7, 2026-11-18). Es gibt fünf
Maßnahmen: (1) Ein kurzes Rollenblatt `.claude/skills/seg-ds-agent/runde.md` (72 Zeilen) ersetzt
SKILL.md Abschnitt 9 (677 Zeilen); (2) fertige Befehle `kachellauf bilder --einheit` für
Vorher-, Nachher- und Nahbilder sowie den Vergleich alt/neu; (3) Markierungen an denselben Objekten
werden zu einer Einheit zusammengelegt; (4) `rundenpruefung.py` schneidet die Masken auf die
Markierung zu und prüft Überlappung, IDs und Format im Code, ein Verstoß geht ohne Agent zurück;
(5) der Läufer plant nach jedem Agent-Ende neu, sodass die Gegenprüfung sofort startet.
Beleg: `git -C C:/Users/Phil/Developement/websites/nai/stitcher show d9a3dd7` (11 Dateien, +658);
Diagnose vorher: `C:/Users/Phil/Developement/websites/nai/wuensche/2026-11-18-runden-straffen.md:14`
(„M1 10,4 min/57 Schritte; Lesen von SKILL.md teils zweimal, eigene Skripte wie borste2.py, viele
Ausschnittbilder“; 7 min Warten auf den langsamsten Agent).
Gewinn: `…/2026-11-18-runden-straffen/bericht-stitcher.md:3,12`: vorher 8 Agents, 20,8 min,
99+54 Schritte, 10,43 USD; nachher 2 Agents, 12,4 min, 34+22 Schritte, 3,20 USD (31 %). Bei den
Masken je Objekt liegt die IoU zwischen 0,994 und 1,000, nur die Borste weicht ab (0,665). Das
Zeitziel von 5 bis 7 min wurde verfehlt, weil ein Agent drei Markierungen nacheinander abarbeitet und
weiter eigene Skripte für Ansichtsbilder schreibt. Daraus entstand der Folgewunsch runden-ausschnitt
(Status neu, noch nicht gemessen).
Sicherheit: belegt.
Gegenprobe: Die Zahlen stimmen zwischen Bericht, Wunsch-Datei und Commit-Text überein. Die
Wunsch-Datei nannte vorher 13,40 USD, der Bericht misst 10,43 USD und nimmt diese Zahl als Grundlage.
Gewinn und Ursachen lassen sich nicht einzeln trennen, weil alle fünf Punkte zusammen gebaut wurden.

S2: Mechanisches gehört in Code, nicht zu einem Agent (tray-seg-ablauf-2, Commit 9ab8b3e).
`kachellauf plan` sortiert selbst vor. Am Beispiel r03c05: 315 Funde, davon 249 Staub direkt Dirt,
11 abgeschnitten, 16 Einheiten, Übersichtsblatt mit 33 Funden, 17 Agents. Eine saubere Einheit
übernimmt der Code ohne Korrektur-Agent. Plan und Bauen kosten als Haiku-Aufruf 0,01 bis 0,03 USD je
Kachel. Seit seg-runden-auto (b457031) ruft der Läufer sie ganz ohne Agent auf
(`2026-11-17-seg-runden-auto.md:63`: „ein Haiku-Agent dazwischen ist für den Läufer nicht nötig“).
Beleg: `…/2026-11-17-tray-seg-ablauf-2/bericht-stitcher.md` (AK3, Technische Entscheidungen);
`…/2026-11-17-tray-seg-ablauf-4/messung.md` (plan/bauen haiku 0,03/0,01 USD).
Gewinn: Gegen den Pilot-Kandidatenweg (28,88 USD je Kachel, `2026-11-16-seg-ds-rohmaske-5/pilot-kosten.md`)
nicht belegt. Der neue Weg kostete im ersten Lauf 49 bis 79 USD je Kachel, allerdings mit Korrektur
und Gegenprüfung, also nicht vergleichbar. Belegt ist nur, dass das Mechanische fast nichts kostet.
Sicherheit: belegt (Aufbau), Gewinn offen.
Gegenprobe: In messung.md tragen plan und bauen zusammen 0,04 von 53,88 USD.

S3: Messung je Stufe aus den Transkripten (`kachellauf messung`, Kopfzeile `Lauf … | Stufe … |
Kachel … | Einheit …` in jedem Prompt). Erst damit wurde sichtbar, dass das Wiederlesen die Kosten
treibt: im Pilot 23,3 Mio. gelesene gegen 1,9 Mio. neue Tokens, „jede Runde liest den Verlauf samt
Bildern neu“ (`2026-11-17-tray-seg-ablauf.md:101`), im ersten Lauf 55,7 gegen 3,4 Mio. (r07c05).
Beleg: messung.md; tray-seg-ablauf-2/bericht-stitcher.md (Technische Entscheidungen).
Sicherheit: belegt. Gegenprobe: Die Tabelle in messung.md ist in sich stimmig (Summen je Kachel nachgerechnet für r07c05: 50 Agents, 53,88 USD).

S4: Modellwahl: Opus für Urteil, Korrektur und Gegenprüfung, Mechanisches in Code und erst danach
ein kleineres Modell. Beleg: `2026-11-14-seg-ds-agent-skill.md:82`, `2026-11-18-runden-straffen.md:60`
(„Mechanisches in Code, nicht auf ein kleineres Modell … die Gegenprüfung bleibt Opus“). Sicherheit: belegt.

S5: Mehr Agents gleichzeitig und Fristen nach Wachzeit: 4 → 8 gleichzeitig (seg-zehn-trays AK6),
der Läufer zählt Fristen nur, solange der Rechner wach ist (b457031). Einen Gewinn hat niemand
gemessen. Sicherheit: belegt (Einstellung), Gewinn vermutet.

S6: Agents stellen keine Fragen mehr, der Nutzer markiert (seg-review-markieren, 8b8eade). Das
dient dem Fokus und erspart Wartezeit. Einen Kostenbeleg gibt es nicht. Sicherheit: belegt (Regel), Gewinn vermutet.

## Teil 2: Unser Lauf H0 (wf_62f47ff3-c51) gemessen

Rohdaten: `D/roh/transkripte.txt` und `D/roh/transkripte.json` (je Agent: Runden, Minuten,
Werkzeuge, Bilder, Lesen von SKILL/Vorlage/Auftrag, doppelte Bildlesungen, geschriebene und
gestartete .py, Python-Aufrufe mit -c oder Heredoc, `-m landseg`-Aufrufe, Tokens, USD). Das Skript
lag im Scratchpad, die Quelle sind die 71 `agent-*.jsonl` mit `*.meta.json` (Phase, Modell) im
Protokollordner des Laufs.

| Phase | Modell | Agents | Wand (min) | Agent-min | Runden | Bilder gelesen | .py geschrieben | .py-Läufe + Inline-Python | gelesen Mio. | neu Mio. | aus Mio. | USD |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Vorbereitung | opus | 1 | 7,7 | 7,7 | 38 | 3 | 7 | 18 | 4,75 | 0,17 | 0,04 | 3,1 |
| Urteile | opus | 13 | 33,6 | 332 | 1283 | 699 | 84 | 409+178 | 250,3 | 3,66 | 1,61 | 111,5 |
| Nachholen | opus | 8 | 9,8 | 59 | 242 | 162 | 21 | 49+45 | 27,6 | 1,08 | 0,31 | 20,4 |
| Vereinheitlichen | sonnet | 1 | 4,9 | 4,9 | 29 | 0 | 3 | 12+7 | 2,6 | 0,13 | 0,04 | 1,1 |
| Zusammenführen | opus | 1 | 6,8 | 6,8 | 33 | 0 | 1 | 7+1 | 3,6 | 0,17 | 0,04 | 2,8 |
| Nähte | opus | 3 | 13,3 | 28 | 150 | 96 | 9 | 25+25 | 19,2 | 0,51 | 0,13 | 10,6 |
| Einigung (3 Runden) | opus | 41 | 27,7 | 202 | 976 | 675 | 55 | 159+177 | 94,2 | 4,04 | 0,98 | 70,7 |
| Anwenden | sonnet | 3 | 11,9* | 2,0 | 18 | 0 | 0 | 0 | 1,0 | 0,17 | 0,01 | 0,9 |
| zusammen | | 71 | 104 (12:12–13:56) | 643 | 2769 | 1635 | 180 | 679+433 | 403 | 9,9 | 3,15 | ~221 |

*Anwenden läuft zwischen den Einigungsrunden; die Wandzeit überlappt.

## Teil 3: Unnötige oder doppelte Schritte bei uns (AK3)

B1: 8 Nachhol-Agents ohne Not: Das Skript wertet eine durch Nachsegmentieren geänderte Segmentzahl
als Fehler. Beleg: `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/workflow.js:404`
`const schlecht = zeilen.filter(r => r.e.art !== 'a' && (!r.ok || (r.e.n && r.segmente !== r.e.n)))`;
dazu die Prompt-Zeilen 211 und 234, nach denen Teilen ausdrücklich erlaubt ist und neue IDs im
selben urteil.json stehen. Alle 8 Nachhol-Agents betrafen r0c0 (b v1/v2/v4, c v1/v2/v4, z v1/v2):
zusammen 20,4 USD, 59 Agent-min, 9,8 min Wand (Tabelle). Sicherheit: belegt (Code), dass alle 8
unnötig waren, wahrscheinlich (laut Wunsch-Datei). Gegenprobe: `MAX_NACHHOLEN = 8` (Zeile 77) wurde
genau ausgeschöpft. Die Fassung A ist ausgenommen und hat keinen Nachholer. Ob ein Viertel
zusätzlich `kontrolle_ok=false` hatte, habe ich nicht einzeln geprüft.

B2: Agents bauen sich ihre Werkzeuge selbst; der Auftrag lädt ausdrücklich dazu ein. Beleg: Auftrag
`…/historisch-3/auftraege/c/r0c0/v1/auftrag.md:184` („Eigene Skripte als Datei in …/urteil/r0c0/v1“).
Der Urteils-Agent b:r1c1 schrieb `werkzeug.py`, `wscheide.py`, `grate.py`, `grat_bild.py`,
`schwelle_teil.py`, `ws_teile.py`, `bau.py`, `urteil_bau.py` und `daten_v1..v4.py`, dazu 62
Skriptläufe in 153 Runden. In der Einigung schrieben fast alle Agents ein `abgabe_bauen.py`, dazu
eigene Sicht- und Zoom-Skripte (A-02: `sicht.py`, `klassen.py`, `abgabe_bauen.py`; B-02:
`ueberblick.py`, `zoom.py`, `abgabe_bauen.py`). Summe: 180 eigene .py, 679 Läufe eigener Skripte und
433 Inline-Python-Aufrufe gegen nur 189 Aufrufe von `-m landseg`. Das ist dasselbe Muster, das der
Stitcher in runden-straffen fand („eigene Skripte wie borste2.py“) und mit fertigen Befehlen
abgestellt hat. Sicherheit: belegt (Zählung), dass sie unnötig sind, wahrscheinlich. Gegenprobe:
Ein Teil der Skripte ist echte Fachhilfe (Wasserscheide zum Nachsegmentieren in `wscheide.py`).
Wiederkehrend und mechanisch sind dagegen urteil.json bzw. die Abgabe bauen sowie Ausschnitt- und
Zoombilder; die schreibt jeder Agent neu.

B3: Die Kosten wachsen mit der Rundenzahl, weil jede Runde den ganzen Verlauf samt Bildern neu
liest. Gelesen gegen neu steht bei 403 zu 9,9 Mio.; das Lesen macht rund 81 der 221 USD aus, neue
Tokens rund 79 und Ausgabe rund 63. Ein Urteils-Agent arbeitet vier Viertel nacheinander in einem
Kontext: b:r1c1 kam auf 153 Runden, 69 Bilder und 33,3 Mio. gelesen (23,3 USD), a:r1c0 auf 39
Runden und 5,4 Mio. (5,7 USD). Im Mittel liest jeder Urteils-Agent 54 Bilder. Beleg: `D/roh/transkripte.txt`
(Zeilen urteil:*). Sicherheit: belegt. Gegenprobe: Die Rangfolge nach Runden und nach gelesenen
Tokens ist bei allen 13 Urteils-Agents dieselbe (Spitze b:r1c1, z:r0c0, c:r0c1; Ende a:r1c0).
Jede eingesparte Runde spart also das Wiederlesen des ganzen Kontexts. Die Aufteilung (ein Agent je
Teilkachel, Viertel nacheinander) hat der Nutzer entschieden: `wuensche/entscheidungen.md:17`
(„14 Agents statt 42“).

B4: Übersichtsbilder werden doppelt angesehen. In den Urteilen gab es 42 doppelte Bildlesungen,
in den Nachholern 13 und in der Einigung 11. Bei b:r1c1 waren es `ganz_nummern.jpg`, `ganz_roh.jpg`
und je Viertel `uebersicht_*` direkt hintereinander zweimal. Vermutliche Ursache: Der Prompt
(`workflow.js:224-225`) und der Auftrag (Abschnitt „Zuerst der ganze Ausschnitt, dann die
Teilkachel“, `auftrag.md:20-25`) verlangen dieselben Bilder je einmal. Dazu kommen je Viertel
Nahbilder in zwei Fassungen (`nahN_roh` und `nahN_nummern`, Auftrag Zeile 68f.), also 8 Nahbilder je
Viertel. Sicherheit: belegt (Zählung), Ursache wahrscheinlich. Gegenprobe: Bei a:r1c0 gab es nur eine
Doppellesung. Die Doppellesung entsteht also nicht immer, sie hängt am Agent.

B5: Ein Opus-Agent schreibt in jedem Lauf dieselben Hilfsskripte neu. Die Vorbereitung schrieb 7 .py
(3,1 USD, 7,7 min), das Zusammenführen überträgt T0-Skripte auf H0 („Fassungsbuchstaben vertauscht —
Fehler hier wären stumm“, `workflow.js:28`; 2,8 USD, 6,8 min). Das kostet wenig, ist aber dieselbe
Lage wie S2 im Stitcher, wo das Mechanische als fester Repo-Befehl läuft. Sicherheit: belegt.
Gegenprobe: Die Kosten sind klein (2,6 % zusammen); der Gewinn liegt in Wand-Zeit und Fehlerrisiko.

B6: Die Einigung zerfällt in viele kleine Agents. Es waren 41 Agents in 3 Runden; die kleinsten
brauchten 0,9 bis 2 min und 0,7 bis 1,2 USD (B-13, B-06, B-08), davon gut 0,6 Mio. gelesene Tokens
als Grundlast für Vorlage, Skill und Einstieg. A-02 allein kostete 8,7 USD (148 Lesungen von
`paar_N.jpg`, 62 Runden). Sicherheit: belegt (Zählung). Gegenprobe: Ob A-02 so viele Paare hatte oder
Paare mehrfach ansah, habe ich nicht geprüft (Zahl der Paare je Bündel nicht gelesen).

B7: Die Modellwahl ist schon richtig: Opus/high für Urteil, Nähte und Einigung (Bildurteil), Sonnet
für Vereinheitlichen und Anwenden (`workflow.js:72-75`). Das entspricht S4. Ein Wechsel auf ein
kleineres Modell spart nur bei Mechanischem, und das ist bei uns fast alles schon Sonnet oder
billig (Anwenden 0,9 USD). Sicherheit: belegt.

B8: Die Phasen-Schranken kosten Wand-Zeit, aber wenig. Die Urteilsphase dauerte 33,6 min, weil sie
auf den langsamsten Agent wartete (b:r1c1 33,5 min, a:r1c0 15,2 min). Zusammenführen braucht alle
Urteile, deshalb lässt sich hier kaum etwas vorziehen wie die fortlaufende Gegenprüfung des
Stitchers. Mit B1 entfällt zudem die Nachholphase. Sicherheit: belegt (Zeiten), Gewinn gering.

## Übertragbarkeit (AK2)

| Stitcher-Ansatz | Passt auf landseg? | Geschätzter Gewinn | Aufwand |
|---|---|---|---|
| S1(2) fertige Befehle statt eigener Skripte | ja, Kern: `landseg`-Unterbefehle für urteil.json bauen und prüfen, Einigungs-Abgabe bauen, Ausschnitt/Zoom einer Stelle mit Umriss und Nummern | 20–35 % der Runden in Urteil und Einigung, rund 35–60 USD und 5–10 min Wand je Lauf wie H0 (Schätzung aus B2/B3) | mittel |
| S1(1) kurzes Rollenblatt | kaum: SKILL.md hat 74 Zeilen, die Vorlagen 50–71; die Viertel-Aufträge haben aber je 23,5–25 kB mit wiederholten Abschnitten | klein (unter 5 %) | klein |
| S1(3) Zusammenlegen | teilweise: kleine Einigungsbündel zu einem Agent (B6) | ~5 USD und einige Agent-Starts je Lauf | klein |
| S1(4)/S2 Mechanisches in Code | ja: Nachhol-Prüfung (B1), Zusammenführen und Vorbereitung als feste Befehle (B5), Kontrolle im Workflow statt im Agent | B1 allein 20 USD und 10 min; B5 rund 6 USD und 14 min | klein (B1) bis mittel (B5) |
| S1(5) fortlaufende Gegenprüfung | kaum: Zusammenführen braucht alle Urteile (B8) | gering | – |
| S3 Messung je Stufe | ja: das Werkzeug fehlt; T0 hat nur neue Tokens gezählt (3,30 Mio.), das Wiederlesen (hier 403 Mio.) war unsichtbar | Voraussetzung, um jeden weiteren Gewinn zu belegen | klein |
| S4 Modellwahl | schon erfüllt (B7) | – | – |
| S5 mehr gleichzeitig | offen: Urteile laufen schon alle 13 gleichzeitig; Einigung ist durch die Bündel begrenzt | gering | – |
| S6 keine Fragen | schon erfüllt (Agents markieren `sicher: false`, keine Rückfragen) | – | – |

## Nicht geprüft

- Die Qualität der H0-Ergebnisse: Ob weniger Runden die Urteile verschlechtern würden, lässt sich nur
  mit einem Probelauf messen (Eingriff keiner).
- T0-Transkripte nicht neu ausgewertet; die T0-Zahlen stammen aus der Wunsch-Datei. Die Lesart
  „3,30 Mio. Tokens = neu + Ausgabe ohne Wiederlesen“ ist eine Vermutung; sie passt zu H0
  (3,66 + 1,61 Mio. in den Urteilen).
- Die Workflows `naht-einigung-2` und `landseg-test-t0-2` habe ich nicht gelesen, nur
  historisch-3 (`workflow.js`); `workflow-fein.js` ebenfalls nicht.
- Der Lauf wf_62f47ff3-c51 lief womöglich noch, als ich gelesen habe (letzter Zeitstempel 13:56); die
  Summen bilden den Stand beim Lesen ab.
- Die Zahl der Paare je Einigungsbündel (B6) und der Kontrollstatus der 8 nachgeholten Viertel (B1)
  habe ich nicht einzeln geprüft.
