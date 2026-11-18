# K4: Bildpflicht entdoppeln: Übersichtsbilder nur einmal verlangen (Prompt oder Auftrag, nicht beide), Nahbilder roh und

Kurzname: effiz-bilder | Datum: 2026-11-18 | Größe: mittel | Bereich: victor | Repos: landseg | Status: eingereiht | Herkunft: Ermittlung landseg-effiz K4

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

K4: Bildpflicht entdoppeln: Übersichtsbilder nur einmal verlangen (Prompt oder Auftrag, nicht beide), Nahbilder roh und nummeriert als ein Bild nebeneinander — Gewinn geschätzt 10–20 % der Bilder im Kontext, rund 10–20 USD je Lauf — Aufwand klein — Risiko gering bis mittel (Agent muss die Nummern weiter lesen können) — Repo landseg — optional

Belege: wuensche/2026-11-18-landseg-effiz/bericht.md, K4.

Empfehlung der Deutung (wuensche/2026-11-18-landseg-effiz.md, Abschnitt Empfehlung):
- K4: trägt teilweise — echte Doppelung, aber klein: 66 von 1.635 Bildlesungen (rund 4 %); die geschätzten 10–20 % hängen an den ungemessenen Nahbildern, und die Doppelung hängt am Agent.
- Nächster Schritt: K2 als Folge-Wunsch — er bringt den größten Gewinn (geschätzt 35–60 USD und 5–10 min je Lauf) und ist genau der Schritt, der im Stitcher gewirkt hat. Für die Läufe auf dem ganzen Orthofoto zählt jede gesparte Runde, weil sie das Wiederlesen des ganzen Kontexts spart.
- Gegenargument: Der Gewinn von K2 ist nur geschätzt. Im Stitcher ließen sich die fünf Maßnahmen von runden-straffen nicht trennen, und selbst danach schrieb ein Agent weiter eigene Skripte für Ansichtsbilder, das Zeitziel wurde verfehlt (bericht.md S1). Ein Teil unserer Skripte ist echte Fachhilfe (`wscheide.py`, B2). — Der Schritt gilt trotzdem: Die mechanischen Wiederholungen (urteil.json und Abgabe bauen, Zoombilder) schreibt jeder Agent neu, und der Gewinn lässt sich am nächsten Lauf mit derselben Transkript-Auswertung gegen H0 nachmessen.

## Fragen

keine offen. Technisch vom Prüfer entschieden: Die Übersichtsbilder (ganzer Ausschnitt, ganze Teilkachel, Viertel) verlangt nur der Auftrag; der Prompt des Läufers verweist darauf und nennt keine Bildnamen mehr (eine Quelle statt zwei).

## Entscheidungen

- Alle Kandidaten K1–K6 bauen, darunter „Bilder nur einmal verlangen"; künftig ein Urteils-Agent je Viertel; jeder Agent sieht weiter zuerst den ganzen Ausschnitt und seine ganze Teilkachel, dann sein Viertel (aus entscheidungen.md, 2026-11-18)
- Die Vorstufe bleibt eher grob, die Urteils-Agents segmentieren selbst nach, möglichst direkt und tokengünstig, aber präzise an der Bildkante (aus entscheidungen.md, 2026-11-18)
- Urteil im Verbund: Segmente nie als isolierte Einzelbilder beurteilen; Nahansichten eines Viertels sind erlaubt (aus entscheidungen.md, 2026-11-17)
- 2026-11-18: Landschafts-Segmente: gröbere Flächen auf alten Schwarz-Weiß-Bildern: Nutzer am 18.11.2026: „außerdem solle die Flächen in den schwarz weiß, niedrig aufgelösten Landschaftsbildern nicht ganz so fein sein. Die wirklich feine Untersuchung funktioniert gut auf hochaufgelösten Bildern aber nicht auf den alte[n]“. Daraus: Auf alten, niedrig aufgelösten Schwarz-Weiß-Bildern (heute H0, Luftbild 1968) werden Flächen deutlich gröber gezogen als auf Farb-Orthofotos (T0); feines Nachsegmentieren gilt dort nur für klar erkennbare Objekte. Verschärft für SW-Bilder die Neuklärung „eher gröber, Agents dürfen nachsegmentieren“ (landseg-historisch); im H0-Lauf kam Fassung A auf 1833 Segmente (T0 607). Wie grob genau und ob H0 neu läuft, klärt der Wunsch landseg-sw-grob. (aus entscheidungen.md, 2026-11-18)

## Arbeitsauftrag

<Prüfer beim Klären, für Umsetzer und Abnahme. Bei kleinen Wünschen ohne Klärung schreibt die
Hauptsession nur die Abnahmekriterien; bei einem Teil übernimmt sie dessen Kriterien aus dem
Mutterwunsch.>

### Abnahmekriterien

AK1: Die Ansicht liefert zu einem Fenster ein Bildpaar: links das Bild roh, rechts dasselbe Fenster mit Segmentgrenzen und Nummern, im selben Maßstab nebeneinander in einer Datei, mit schmalem Trennstreifen — prüfbar: neuer Test in `tests/test_ansicht.py` (Höhe gleich, Breite = 2 × Fenster + Streifen, linke Hälfte gleich dem Rohbild des Fensters): `"$PY" -B -m unittest tests.test_ansicht`
AK2: `ansicht.json` führt das Paar mit Fenster, Faktor und Versatz der rechten Hälfte, so dass die Koordinatenformel für beide Hälften auf dieselbe Teilkachel-Koordinate zurückführt — prüfbar: derselbe Test
AK3: Ein Paar überschreitet 2000 Bildpunkte an der langen Seite nicht (Regel L11); dafür sinkt der Faktor ganzzahlig, Bildpunkte bleiben Quadrate, Nummern bleiben lesbar — prüfbar: Test mit einem Fenster, das bei 6fach darüber läge
AK4: `vorlagen/urteil.md` und der Skill `landseg-agent` verlangen Übersichtsbilder an genau einer Stelle (im Auftrag), nennen für Nahansichten nur das Paar (nicht mehr getrennt roh und nummeriert) und halten fest, dass ein Prompt sie nicht wiederholt — prüfbar: Lesen `vorlagen/urteil.md`, `.claude/skills/landseg-agent/SKILL.md`
AK5: Weg des Nutzers: an einer Teilkachel von T0 (zwei Tiles, unter zwei Minuten, offline auf vorhandenen Daten) erzeugt `"$PY" -B -m landseg ansicht` das Paar; die Nummern im Bild sind lesbar — prüfbar: erzeugtes Bild ansehen
AK6: Kurzprüfung und Ansichts-Tests bleiben grün — prüfbar: Befehl „Schnell" aus dem Profil, `"$PY" -B -m unittest tests.test_ansicht`

### Einstieg

- landseg: `landseg/ansicht.py:334` — `Ansicht.zeichnen(art, f, sid)`: hier kommt die Bildart `paar` dazu (roh | Grenzen mit Nummern, ein Fenster, ein Faktor)
- landseg: `landseg/ansicht.py:369` — `ansicht(...)` schreibt Bilder und `ansicht.json`: das Paar mit Fenster, Faktor, Versatz eintragen; Moduldoku Zeilen 1–20 ergänzen
- landseg: `einstellungen/ansicht.json` — Bildarten, Faktoren, Obergrenze 2000 px
- landseg: `tests/test_ansicht.py:61` — Vorbild für den Koordinaten-Test
- landseg: `vorlagen/urteil.md:19-31` — Werkzeug- und Ergebnis-Abschnitt: Übersicht einmal, Nahansichten als Paar
- landseg: `.claude/skills/landseg-agent/SKILL.md` (Regel L11, Bilder) — Hinweis zu Paar und Einmal-Regel

### Bausteine und Fallen

- Benutzen statt nachbauen: `Ansicht.zeichnen("roh"|"umriss", f)`, `Fenster`, `_gross`; das Paar setzt beide Bilder nur zusammen (`np.hstack`).
- Falle: Die Viertelbilder (`uebersicht_nummern.jpg`, `nah<k>_roh/_nummern.jpg`), der Auftragsabschnitt „Zuerst der ganze Ausschnitt, dann die Teilkachel“ und der Läufer-Prompt (`workflow.js:224-225`, `:248`) liegen im Wunschordner (`wuensche/2026-11-18-landseg-historisch-3/skripte/baue_auftraege_h0.py:243-257`, `:382`), nicht im Repo. Sie gehören nicht in diesen Wunsch; das Umstellen übernimmt K5 (`effiz-bau-befehle`), das den Auftragsbau ins Repo holt. Hier nur der Baustein und die Vorlagen.
- Falle: Der Agent muss die Nummern weiter lesen können: Nummer im Bild = ID mod 100000; der Rohteil bleibt unverändert; Koordinatenformel der rechten Hälfte genau angeben.
- Zahlenbasis (Ermittlung landseg-effiz, B4): 66 doppelte von 1.635 Bildlesungen (rund 4 %); die geschätzten 10–20 % hängen an den ungemessenen Nahbildern. Kein Zahlenziel; Gewinn am nächsten Lauf mit derselben Transkript-Auswertung nachmessen.

Nacharbeit: Läufer-Prompt und Auftragsbau auf Einmal-Regel und Paar umstellen (mit K5 `effiz-bau-befehle`); `LAGEBILD.md` des Repos nachziehen (Bildart `paar`).

### Bauweise

<Prüfer, Pflicht: ob der Wunsch das Repo seinem Zielbild (`<repo>/zielbild.md`) näherbringt, es
unberührt lässt oder davon wegführt; Anbau, Umbau, Belege und Empfehlung nur, wenn er eine Altlast
aus `<repo>/altlasten.md` berührt, ein Anbau vom Zielbild wegführen würde oder `Flick-Signale`
belegt sind, dann dazu die Frage „Weiter anbauen, umbauen oder ganz neu bauen" unter „Fragen".>
Richtung: neutral
Berührt: keine — A1 (`ansicht.py:117`) und A5 liegen in derselben Datei, werden nicht angefasst
Tilgt: keine
Flick-Signale: keine — kein Vorgänger in `Herkunft:` (Ermittlung landseg-effiz K4); die Wünsche effiz-bau-befehle, effiz-befehle, effiz-viertel sind Geschwister mit anderen Stellen, keine Kette

Reihenfolge der Repos: landseg · Risiken: Agent liest Nummern im Paar schlechter als im Einzelbild; Gewinn klein (rund 4 % der Bildlesungen belegt), nur am nächsten Lauf nachmessbar · Vorbedingungen: keine

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

Stufe: nein — Prüfbilder für Agents, keine Oberfläche für den Nutzer
