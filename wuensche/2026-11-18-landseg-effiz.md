# Ermitteln, welche Ansätze der Stitcher-Session zu Tokennutzung, Effizienz und Dauer der Segmentier-Agents sich auf landseg übertragen lassen und wo unsere Agents unnötige Schritte machen

Kurzname: landseg-effiz | Datum: 2026-11-18 | Bereich: victor | Art: untersuchung | Stufe: S | Eingriff: keiner | Repos: landseg | Status: ermittelt
Vergleich mit: –

<Eine Ermittlung will wissen, nicht ändern. Stufe S: ein Prüfer sieht kurz nach und schreibt
Befund, Abdeckung und Kandidaten; M und L: Plan, Einheiten, Gegenprüfung und Bericht. Alles
liegt im Ordner mit demselben Namen ohne `.md` daneben.>

## Wunsch

„schau dir jetzzt mal an wie in der Stitcher Session die Tokennutzung, Effizienz und Dauer verbessert wurden. Wäre es auch möglich diese Ansätze jetzt bei uns anzzuwenden? WErden da noch unnötige Schritte durchgeführt oder sind die Agents wirklich maximal auf ihre jeweilige Aufgabe fokussiert?"

Präzisierung:
- Vorbild: die Session im Repo `C:/Users/Phil/Developement/websites/nai/stitcher` (Bereich nai, Segmentier-Datensatz für Insekten-Trays). Ihre Wünsche liegen unter `C:/Users/Phil/Developement/websites/nai/wuensche/` (u. a. seg-ds-agent-skill, seg-runden-auto, seg-kachel-fertig, seg-durchsicht-umbau, tray-seg-ablauf*, seg-zehn-trays*, pakete-neue-form, composite-*); Berichte und Messzahlen dort in den Ordnern neben den Wunsch-Dateien. Nur lesen, dort nichts ändern, der anderen Session keine Nachricht.
- Gegenstand bei uns: der laufende Ablauf für landseg (Urteile je Teilkachel und Viertel, Nachsegmentieren, Vereinheitlichen, Zusammenführen, Nähte, Einigung). Skripte: `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-3/workflow.js` (läuft gerade, Lauf wf_62f47ff3-c51; Protokoll unter `C:/Users/Phil/.claude/projects/C--Users-Phil-Developement-Victor/a2bf01d3-627c-4b06-8b57-51f25ab5229e/subagents/workflows/wf_62f47ff3-c51/`, nur lesen), `…/2026-11-18-naht-einigung-2/workflow.js`, `…/2026-11-17-landseg-test-t0-2/workflow.js`; Aufträge `…/2026-11-18-landseg-historisch-3/auftraege/`, Vorlagen `C:/Users/Phil/Developement/Victor/landseg/vorlagen/`, Skill `landseg/.claude/skills/landseg-agent/SKILL.md`.
- Bekannte Zahlen T0: Urteile 15 Agents, 3,30 Mio. Tokens, 25 min; Einigung 15 Agents, 1,89 Mio. Tokens, 13,5 min. Bekannter unnötiger Schritt in H0: 8 Viertel wurden nachgeholt, weil das Skript eine durch Nachsegmentieren geänderte Segmentzahl als Fehler wertete.
- Gefragt: (1) Welche konkreten Ansätze hat die Stitcher-Session eingeführt und mit welchem belegten Gewinn (Tokens, Dauer, Qualität)? (2) Welche davon passen auf landseg, mit geschätztem Gewinn und Aufwand? (3) Wo machen unsere Agents unnötige oder doppelte Schritte (Lesen, Bilder ansehen, Skripte schreiben, Prüfungen, Modellwahl), belegt aus Aufträgen und Transkripten des laufenden Laufs? Ergebnis als Kandidaten für Folge-Wünsche.

## Fragen

### F1: Soll der Kontext der Urteils-Agents kürzer werden (K7)?
- Lage: Ein Urteils-Agent arbeitet heute alle vier Viertel seiner Teilkachel nacheinander ab (deine Entscheidung vom 17.11.). Dabei wächst sein Verlauf, und jede Runde liest ihn samt Bildern neu ein; der teuerste Agent kam auf 33 Mio. gelesene Tokens.
- Empfohlen: so lassen und zuerst K1 bis K3 bauen. Damit fallen Runden weg, ohne den Zusammenhang über die Teilkachel zu verlieren.
- Ein Agent je Viertel: spart vermutlich 30 bis 50 % der gelesenen Tokens, jeder Agent sieht aber nur noch sein Viertel im Detail.

## Entscheidungen

- (aus entscheidungen.md, 2026-11-17) Ein Agent je Teilkachel, Viertel nacheinander, sieht zuerst den ganzen Ausschnitt („14 Agents statt 42").
- (aus entscheidungen.md, 2026-11-18) Vorstufe eher grob, Agents segmentieren selbst nach, „möglichst direkt, einfach und Tokengünstig ohne große Umwege aber trotzdem maximal effektiv und präzise".

## Arbeitsauftrag

### Abnahmekriterien

AK1: Der Befund nennt die Ansätze der Stitcher-Session zu Tokens, Effizienz und Dauer je mit Beleg (Wunsch, Bericht, Zahl) — prüfbar: Verhalten Lesen des Befunds
AK2: Für jeden Ansatz steht, ob und wie er auf landseg passt, mit geschätztem Gewinn und Aufwand — prüfbar: Verhalten Lesen der Kandidaten
AK3: Unnötige oder doppelte Schritte unserer Agents sind mit Stelle belegt (Auftrag, Skript oder Transkript) — prüfbar: Verhalten Lesen des Befunds

## Plan

<Planer: Erkenntnisziel, je Einheit eine Zeile (Details in plan.md), was übersprungen wird>

## Befund

Die Stitcher-Session hat die Kosten vor allem mit runden-straffen gesenkt (Commit d9a3dd7): kurzes
Rollenblatt, fertige Befehle statt eigener Agent-Skripte, Mechanisches im Code, Zusammenlegen und
fortlaufende Gegenprüfung. Eine Runde kostete danach 3,20 statt 10,43 USD und dauerte 12,4 statt
20,8 min, die Masken blieben fast gleich. Ältere Bausteine sind Vorsortieren im Code, Messen je Stufe
und Opus nur fürs Urteil. Unser Lauf H0 (wf_62f47ff3-c51) brauchte 71 Agents, 104 min Wand und rund
221 USD Rechenwert. Getrieben wird das vom Wiederlesen des wachsenden Verlaufs samt Bildern (403 Mio.
gelesen gegen 9,9 Mio. neu). Unnötig waren 8 Nachhol-Agents. Der größte vermeidbare Aufwand sind die
Werkzeuge, die die Agents selbst schreiben. Die Modellwahl stimmt schon. Alles mit Belegen:
`wuensche/2026-11-18-landseg-effiz/bericht.md`.

Nach Gewicht:
- B3 Wiederlesen als Kostentreiber: ein Urteils-Agent liest bis 153 Runden, 69 Bilder und 33 Mio. Tokens (bericht.md B3, `roh/transkripte.txt`).
- B2 eigene Skripte: 180 .py, 679 Skriptläufe und 433 Inline-Python-Aufrufe gegen 189 `-m landseg`; der Auftrag lädt dazu ein (`auftrag.md:184`). Gleiches Muster wie im Stitcher vor runden-straffen (bericht.md B2).
- B1 unnötiges Nachholen: `historisch-3/workflow.js:404` wertet eine geänderte Segmentzahl als Fehler, das kostete 8 Agents, 20,4 USD und 9,8 min (bericht.md B1).
- B4 doppelte Übersichtsbilder: 66 doppelte Bildlesungen, wahrscheinlich weil Prompt und Auftrag dieselben Bilder verlangen (bericht.md B4).
- B5/B6 kleinere Posten: Vorbereitung und Zusammenführen schreiben ihre Skripte in jedem Lauf neu (5,9 USD, 14,5 min); die Einigung zerfällt in 41 Agents mit Grundlast je Agent.
- B7 Modellwahl schon wie im Stitcher; B8 Phasen-Schranken kosten wenig.
- Nicht übertragbar bzw. mit kleinem Gewinn: das Rollenblatt (SKILL.md hat nur 74 Zeilen) und die fortlaufende Gegenprüfung (Zusammenführen braucht alle Urteile).
- Unklar: Der Gewinn des Vorsortierens im Stitcher gegenüber dem Pilot ist nicht belegt (neuer Weg 49–79 USD je Kachel gegen 28,88, nicht vergleichbar).

## Abdeckung

Stitcher: 9 der genannten Wünsche gelesen, dazu runden-straffen, runden-ausschnitt, die
Messberichte (pilot-kosten, tray-seg-ablauf-4/messung) und die Commits seit 14.11. landseg: alle 71
Agent-Transkripte des Laufs wf_62f47ff3-c51 ausgewertet, `historisch-3/workflow.js` (Prompts,
Modelle, Nachholen) und ein Viertel-Auftrag gelesen. Nicht geprüft: die Workflows `naht-einigung-2`,
`landseg-test-t0-2` und `workflow-fein.js` (Budget), T0-Transkripte (T0-Zahlen aus der Wunsch-Datei),
die Qualität bei weniger Runden (nur mit Probelauf, Eingriff keiner), die Paarzahl je Einigungsbündel
und der Kontrollstatus der 8 nachgeholten Viertel. Der Lauf lief beim Lesen womöglich noch
(letzter Zeitstempel 13:56).

## Kandidaten

K1: Nachhol-Prüfung im Workflow reparieren: Soll-Zahl = geplante Segmente plus Zugänge aus "eingriffe" bzw. nur `ok`/`kontrolle_ok` werten (`workflow.js:404`, auch in Folge-Workflows) — Gewinn rund 20 USD, 8 Agents, 10 min Wand je Lauf wie H0 — Aufwand klein — Risiko gering (echte Fehlabgaben müssen weiter auffallen) — Repo landseg (Workflow im Wunsch-Ordner) — empfohlen
K2: Fertige `landseg`-Befehle für die wiederkehrenden Agent-Skripte: urteil.json aus einer Liste bauen und prüfen, Einigungs-Abgabe bauen, Ausschnitt/Zoom einer Stelle mit Umriss und Nummern; die Aufträge nennen sie statt „Eigene Skripte als Datei" — Gewinn geschätzt 20–35 % der Runden in Urteil und Einigung, rund 35–60 USD und 5–10 min Wand je Lauf (Stitcher-Vorbild: 31 % der Kosten) — Aufwand mittel — Risiko mittel (Agents müssen bei Sonderfällen weiter frei arbeiten dürfen, sonst leidet die Genauigkeit) — Repo landseg — empfohlen
K3: Kostenmessung je Phase und Agent aus den Transkripten als festes Werkzeug (wie `kachellauf messung`, mit gelesenen Tokens und USD), nach jedem Lauf im Bericht — Gewinn: macht jeden weiteren Gewinn belegbar; T0-Zahlen enthielten das Wiederlesen nicht — Aufwand klein — Risiko gering — Repo landseg — empfohlen
K4: Bildpflicht entdoppeln: Übersichtsbilder nur einmal verlangen (Prompt oder Auftrag, nicht beide), Nahbilder roh und nummeriert als ein Bild nebeneinander — Gewinn geschätzt 10–20 % der Bilder im Kontext, rund 10–20 USD je Lauf — Aufwand klein — Risiko gering bis mittel (Agent muss die Nummern weiter lesen können) — Repo landseg — optional
K5: Vorbereitung und Zusammenführen als feste Repo-Befehle statt Opus-Agent, der in jedem Lauf T0-Skripte überträgt — Gewinn rund 6 USD und 14 min Wand je Lauf, dazu keine stummen Fehler beim Übertragen — Aufwand mittel — Risiko gering — Repo landseg — optional
K6: Kleine Einigungsbündel zu einem Agent zusammenlegen (unter einer Mindestzahl Paare) — Gewinn rund 5 USD und weniger Agent-Starts je Lauf — Aufwand klein — Risiko gering — Repo landseg — optional
K7: Kontext je Urteils-Agent kürzen, indem ein Agent je Viertel statt je Teilkachel arbeitet — Gewinn vermutet 30–50 % der gelesenen Tokens in den Urteilen — Aufwand klein — Risiko: widerspricht der Entscheidung vom 17.11. („14 Agents statt 42", `entscheidungen.md:17`) und verliert Zusammenhang — Repo landseg — nur mit Freigabe

## Empfehlung

Antwort: Ja, der Kern des Stitcher-Gewinns passt auch bei uns: fertige Befehle statt eigener Skripte und Mechanisches im Code (dort kostete eine Runde 3,20 statt 10,43 USD). Unsere Agents sind nicht maximal fokussiert: Im Lauf H0 schrieben sie 180 eigene Skripte, und 8 Nachhol-Agents liefen ohne Not (rund 20 der 221 USD).
- K1: trägt — der sicherste unnötige Schritt, im Code belegt (`workflow.js:404`, gleich in `workflow-fein.js:340`): 8 Agents, 20,4 USD, 9,8 min Wand, kleiner Aufwand.
- K2: trägt — genau der Hauptansatz des Stitchers (runden-straffen) gegen den größten Fokusverlust bei uns: 180 eigene .py und 1.112 Python-Aufrufe stehen gegen 189 Aufrufe von `-m landseg`.
- K3: trägt teilweise — beantwortet keine der Fragen selbst, macht aber jeden Gewinn belegbar; die T0-Zahl 3,30 Mio. enthielt das Wiederlesen nicht (H0: 403 Mio. gelesen).
- K4: trägt teilweise — echte Doppelung, aber klein: 66 von 1.635 Bildlesungen (rund 4 %); die geschätzten 10–20 % hängen an den ungemessenen Nahbildern, und die Doppelung hängt am Agent.
- K5: trägt teilweise — entspricht S2 im Stitcher, spart aber nur 2,6 % der Kosten; der Gewinn liegt in Wandzeit und weniger stummen Fehlern.
- K6: trägt teilweise — entspricht dem Zusammenlegen im Stitcher, bringt aber nur rund 5 von 70,7 USD der Einigung; die Paarzahl je Bündel ist nicht geprüft.
- K7: trägt nicht — kein Stitcher-Ansatz, Gewinn nur vermutet, und er widerspricht deiner Entscheidung vom 17.11. (`entscheidungen.md:17`); F1 bleibt offen.
Nächster Schritt: K2 als Folge-Wunsch — er bringt den größten Gewinn (geschätzt 35–60 USD und 5–10 min je Lauf) und ist genau der Schritt, der im Stitcher gewirkt hat. Für die Läufe auf dem ganzen Orthofoto zählt jede gesparte Runde, weil sie das Wiederlesen des ganzen Kontexts spart.
Gegenargument: Der Gewinn von K2 ist nur geschätzt. Im Stitcher ließen sich die fünf Maßnahmen von runden-straffen nicht trennen, und selbst danach schrieb ein Agent weiter eigene Skripte für Ansichtsbilder, das Zeitziel wurde verfehlt (bericht.md S1). Ein Teil unserer Skripte ist echte Fachhilfe (`wscheide.py`, B2). — Der Schritt gilt trotzdem: Die mechanischen Wiederholungen (urteil.json und Abgabe bauen, Zoombilder) schreibt jeder Agent neu, und der Gewinn lässt sich am nächsten Lauf mit derselben Transkript-Auswertung gegen H0 nachmessen.

## Folge-Wünsche

<Hauptsession: Kurznamen der Wünsche, die aus Kandidaten entstanden sind>
- effiz-nachholen (K1): `wuensche/2026-11-18-effiz-nachholen.md`
- effiz-befehle (K2): `wuensche/2026-11-18-effiz-befehle.md`
- effiz-kosten (K3): `wuensche/2026-11-18-effiz-kosten.md`
- effiz-bilder (K4): `wuensche/2026-11-18-effiz-bilder.md`
- effiz-bau-befehle (K5): `wuensche/2026-11-18-effiz-bau-befehle.md`
- effiz-buendel (K6): `wuensche/2026-11-18-effiz-buendel.md`
- effiz-viertel (K7): `wuensche/2026-11-18-effiz-viertel.md`
