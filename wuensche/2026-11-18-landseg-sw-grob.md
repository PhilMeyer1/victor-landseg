# Auf alten, niedrig aufgelösten Schwarz-Weiß-Luftbildern gröbere Flächen ziehen als auf Farb-Orthofotos, in allen Fassungen und Läufen

Kurzname: landseg-sw-grob | Datum: 2026-11-18 | Größe: mittel | Bereich: victor | Repos: landseg | Status: eingereiht

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

„außerdem solle die Flächen in den schwarz weiß, niedrig aufgelösten Landschaftsbildern nicht ganz so fein sein. Die wirklich feine Untersuchung funktioniert gut auf hochaufgelösten Bildern aber nicht auf den alte"

Präzisierung:
- Anlass: Im H0-Lauf (Luftbild 1968, SW) kam Fassung A auf 1833 Segmente (T0 607), B 728, C 470; in A r0c1 876 und r1c1 820 Segmente, 84–90 % „unsicher“. Die Neuklärung von landseg-historisch („eher gröber, aber Agents dürfen sauber nachsegmentieren“) hat die Feinheit nicht begrenzt.
- Gilt für Bilder mit Kennzeichen Schwarz-Weiß / niedrige Auflösung (heute H0); Farb-Orthofotos (T0) bleiben unverändert fein.
- Ansatzpunkte (Prüfer entscheidet technisch): Vorgaben in Vorlagen und Skill landseg-agent je Bildart (Mindestgröße, Nachsegmentieren nur bei klar erkennbaren Objekten), Vorstufe je Bildart, eine Obergrenze/Richtwert je Teilkachel, die eine Prüfung meldet; besonders Fassung A (eigene Karten).
- Zu klären mit dem Nutzer: wie grob (Richtwert Segmente oder kleinste Fläche), ob das vorhandene H0-Ergebnis neu läuft oder zusammengelegt wird (Kosten nennen), Verhältnis zur Garten-Regel (landseg-garten: Gärten trotzdem als eigene Fläche?).
- Überschneidet sich mit landseg-garten und effiz-* (gleiche Vorlagen und Aufträge); Reihenfolge klärt der Prüfer.

## Fragen

### F1: Wie grob sollen die Flächen auf alten Schwarz-Weiß-Bildern werden?
- Lage: Im Test mit dem Luftbild von 1968 (Ausschnitt H0, ein 1000 × 1000 Bildpunkte großer Ausschnitt, in der Prüfseite wählbar) zerlegte die erste Stufe die Fassung A in 1833 Flächen, beim Farb-Orthofoto T0 sind es 607; in zwei Teilkacheln waren es je rund 850, davon 84–90 % als „unsicher“ markiert. Ein altes Bild hat weniger Details, viele dieser Flächen sind Rauschen und Korn.
- Empfohlen: Richtwert etwa 600 Flächen je Ausschnitt (so viele wie bei T0, also gut ein Drittel von heute), kleiner als rund 100 m² nur bei klar erkennbaren Objekten (Haus, Einzelbaum, schmaler Weg); die Agents melden, wenn eine Teilkachel den Richtwert überschreitet.
- Etwa 900 Flächen je Ausschnitt (halb so viele wie heute) — vorsichtiger, es bleibt mehr Feinheit, aber noch viel Korn-Rauschen.
- Etwa 400 Flächen je Ausschnitt — sehr grob; Häuserzeilen und Gärten verschmelzen eher, der Nutzer müsste mehr nachfeilen.

### F2: Soll das vorhandene H0-Ergebnis gröber werden, und wie?
- Lage: Der H0-Lauf ist fertig (alle drei Fassungen A, B, C mit je vier Teilkacheln, die Urteile der Agents stecken darin; der Lauf kostete rund 221 USD Rechenwert).
- Empfohlen: Kleine Flächen automatisch mit dem passenden Nachbarn zusammenlegen (feste Befehle, ohne neue Agents, praktisch kostenlos), danach Stichprobe und Einigung an den Nähten prüfen; die Klassen und Urteile der Agents bleiben erhalten.
- H0 ganz neu laufen lassen, Vorstufe und Agents mit den neuen Vorgaben — am saubersten, kostet aber einen weiteren vollen Lauf (nach den Effizienz-Wünschen deutlich weniger als 221 USD, den genauen Preis nennt der Prüfer erst nach deren Einreihung).
- Das vorhandene Ergebnis unverändert lassen, nur künftige Läufe gröber ziehen — kostet nichts, die Prüfseite zeigt weiter die 1833 Flächen.

### F3: Sollen Gärten auf den alten Bildern trotz der Grobheit eigene Flächen bleiben?
- Lage: Nach der Entscheidung vom 18.11. (Wunsch landseg-garten) gibt es die Unterklasse „Garten“ im Dauergrünland; Gärten sind oft klein und neben Häusern, auf einem Bild von 1968 kaum von Wiese oder Hof zu trennen.
- Empfohlen: Ja, ein klar erkennbarer Garten am Haus bleibt als eigene Fläche „Garten“, auch wenn er unter dem Mindestmaß liegt; ein unklarer wird mit der Nachbarfläche (meist Wiese) zusammengelegt statt geraten.
- Gärten gelten wie alles andere: unter dem Mindestmaß wird zusammengelegt, ein Garten entsteht nur ab dieser Größe — einfacher, aber kleine Hausgärten fehlen dann.

## Entscheidungen

- Push zu GitHub nur auf ausdrückliche Ansage, nie automatisch nach einem Wunsch (aus entscheidungen.md, 2026-11-17)
- Segmente so fein, wie im Bild sicher erkennbar; jeder Bildpunkt gehört zu genau einem Segment mit Kategorie (lückenlos) (aus entscheidungen.md, 2026-11-17, Grundsätze F1/F2/F5)
- Vorstufe eher grob, Agents segmentieren verschmolzene Objekte selbst sauber nach, direkt im Urteilsschritt, tokengünstig (aus entscheidungen.md, 2026-11-18, „Vorstufe eher grob“)
- Einigung an den Übergängen der Teilkacheln in jedem Lauf und jeder Fassung (aus entscheidungen.md, 2026-11-18)
- Künftig ein Urteils-Agent je Viertel statt je Teilkachel; Effizienz-Kandidaten K1–K6 werden gebaut (aus entscheidungen.md, 2026-11-18, „Effizienz der Agents“)
- Gärten immer als Dauergrünland mit Unterklasse Garten, in jeder Fassung und jedem Lauf (aus entscheidungen.md, 2026-11-18)
- Auf alten, niedrig aufgelösten Schwarz-Weiß-Bildern (heute H0) Flächen deutlich gröber als auf Farb-Orthofotos (T0), feines Nachsegmentieren nur für klar erkennbare Objekte; wie grob genau und ob H0 neu läuft, klärt dieser Wunsch (aus entscheidungen.md, 2026-11-18)

- F1 (Nutzer 2026-11-18): „Etwa 600 je Ausschnitt“ — Richtwert rund 600 Flächen je Ausschnitt (1000 × 1000), kleiner als rund 100 m² nur bei klar erkennbaren Objekten; Überschreiten wird gemeldet.
- F2 (Nutzer): „Automatisch zusammenlegen“ — vorhandenes H0-Ergebnis per festem Befehl ohne neue Agents gröber machen, Klassen und Urteile bleiben, danach Stichprobe und Nähte/Einigung prüfen.
- F3 (Nutzer): „Klare Gärten bleiben“ — klar erkennbarer Garten am Haus bleibt eigene Fläche „Garten“ auch unter dem Mindestmaß; unklare werden mit der Nachbarfläche zusammengelegt.

## Arbeitsauftrag

### Abnahmekriterien

AK1: Die Vorstufe erkennt ein Schwarz-Weiß-Bild (ein Kanal, kein Farbbild) und nimmt dafür gröbere Einstellungen aus einem eigenen Abschnitt der Einstellungen; für Farbbilder ändert sich nichts — prüfbar: Test in `tests/` (Farb-Teilkachel liefert mit alten und neuen Einstellungen dieselbe Karte, SW-Teilkachel weniger Segmente) und `"$PY" -B -m unittest discover -s tests -t .`
AK2: Auf H0 ergibt die Vorstufe (aus den gespeicherten SAM-3-Rohdaten mit `vorstufe --neu`, ohne GPU) so wenige Segmente, dass der Ausschnitt etwa beim Richtwert aus F1 liegt, ohne Lücken — prüfbar: `"$PY" -B -m landseg vorstufe --manifest <H0-Kopie>/manifest.json --teilkachel <rXcY> --neu` und `"$PY" -B -m landseg pruefen` je Teilkachel (nach F1)
AK3: Die Vorlagen `urteil.md`, `umsetzen.md`, `korrektur.md` und der Skill `landseg-agent` nennen je Bildart Richtwert und Mindestfläche und erlauben Nachsegmentieren auf SW-Bildern nur für klar erkennbare Objekte; Farb-Aufträge bleiben inhaltlich wie bisher — prüfbar: Lesen `vorlagen/urteil.md`, `vorlagen/umsetzen.md`, `vorlagen/korrektur.md`, `.claude/skills/landseg-agent/SKILL.md` (nach F1)
AK4: `pruefen` meldet für eine SW-Teilkachel eine Warnung, wenn sie den Richtwert überschreitet (Exit-Code und Lückenlosigkeits-Prüfung unverändert) — prüfbar: Test in `tests/` und `"$PY" -B -m landseg pruefen` an einer H0-Teilkachel
AK5: Klar erkennbare Gärten bleiben auch auf SW-Bildern eigene Fläche „Garten“, unklare werden mit der Nachbarfläche zusammengelegt — prüfbar: Lesen der Vorlagen und des Skills (nach F3; bei der zweiten Option entfällt das Kriterium)
AK6: Das vorhandene H0-Ergebnis (Fassungen A, B, C) ist gröber: Segmentzahl je Fassung nahe dem Richtwert, lückenlos, `pruefen` und `naht` ok, Klassen und Urteile der Agents erhalten — prüfbar: `"$PY" -B -m landseg pruefen` je Teilkachel und Fassung, Zählung der Segmente vorher und nachher im Bericht (nach F2; entfällt bei „unverändert lassen“, bei „neu laufen“ wird der Lauf ein eigener Wunsch)
AK7: Weg des Nutzers: Die Prüfseite mit Bildwahl H0, Fassung A zeigt deutlich weniger und größere Flächen als vorher, T0 sieht unverändert aus — prüfbar: Ansicht Prüfseite (`seite --daten … --ziel <x.html>`), Bild H0 Fassung A und Bild T0, Desktop (nach F2)

### Einstieg

- landseg: `vorstufe.json:3` (Abschnitte `uebersegmentierung`, `kandidaten`, `verschmelzen`) — die Einstellungen gelten heute für jedes Bild; neu ein Abschnitt je Bildart (SW überschreibt einzelne Schlüssel: größere mittlere Superpixel-Fläche, größeres `zu_klein_px`)
- landseg: `landseg/vorstufe.py:180` — `anzahl = max(1, round(h * w / flaeche_px))` bestimmt die Zahl der Superpixel; hier wählt die Bildart die Einstellung
- landseg: `landseg/vorstufe.py:379` — Kandidat `zu_klein` aus `kandidaten.zu_klein_px`; je Bildart anderes Maß
- landseg: `landseg/pruefen.py:77` — hier kommt die Richtwert-Warnung für SW-Teilkacheln hinzu
- landseg: `vorlagen/urteil.md:6` — Auftragstext: Richtwert und Mindestfläche als Auftragsvariable je Bildart; ebenso `vorlagen/umsetzen.md`, `vorlagen/korrektur.md`, `vorlagen/README.md` (Platzhalterliste)
- landseg: `.claude/skills/landseg-agent/SKILL.md:37` — Regel L5 „Fein arbeiten“ meint die Grenzgenauigkeit, nicht die Flächengröße; neue Regel L14 „Feinheit je Bildart“ ergänzen
- landseg: `daten/landseg/H0/manifest.json:8` (`quelle.kanaele: 1`) — das Manifest kennt keine Bildart; sie wird aus dem Kanal-Eintrag abgeleitet, ein optionales Feld `bildart` im Manifest hat Vorrang

### Bausteine und Fallen

- Bildart ableiten, nicht doppelt pflegen: `quelle.kanaele == 1` heißt SW; ein Feld `bildart` im Manifest übersteuert. Einstellungen über den vorhandenen Lader `landseg/einstellungen.py` (überschreibt einzelne Schlüssel), nicht neu lesen.
- Zusammenlegen vorhandener H0-Ergebnisse mit `eingriff verschmelzen` auf der Label-Karte (`landseg/eingriff.py:166`), nie über eigene Schreibroutinen (L1); danach `pruefen` und `zusammentragen`, Einigung an den Nähten neu messen (`einigung messen`). Klassen der Agents behalten: bei zwei Klassen gewinnt die größere Fläche, bei Gleichstand die sichere.
- Die gröbere Vorstufe wirkt auf dem Weg `vorstufe --neu` aus den gespeicherten Rohdaten (`sam3_roh.npz`), solange `sam3` und `prompts` unverändert bleiben: `sam3.fenster_px` und `instanz_schwelle` nicht ändern (420/0,2 trennte Häuserzeilen, zog aber gerade Fensterkanten durch Äcker, siehe `betrieb.md`, „Schwarz-Weiß-Scans“).
- T0 darf sich nicht ändern: Test mit gespeicherten Rohdaten, Byte-Vergleich der Karte gegen Git-Blobs (`core.autocrlf`).
- Gleiche Stellen wie `landseg-garten` (Vorlagen, KATEGORIEN.md), `effiz-bilder`, `effiz-viertel`, `effiz-befehle`, `effiz-bau-befehle`: gleichzeitiger Bau erzeugt Konflikte in `vorlagen/*.md` und im Skill; deshalb die Reihenfolge unten.
- Fassungen B und C haben eigene Klassenlisten; der Richtwert zählt Segmente, nicht Klassen.
- Richtwert und Mindestfläche stehen einmal in den Einstellungen, nicht in jeder Vorlage ausgeschrieben; die Vorlagen setzen sie als Variable ein.

### Bauweise

Richtung: neutral
Berührt: keine — die Altlasten A1–A6 liegen an anderen Stellen (A6 `pruefen.py:77`: die Warnung baut an dieselbe Funktion an, ändert aber die Zusammenhangsprüfung nicht)
Tilgt: keine
Flick-Signale: keine — kein Vorgänger in der Kette (kein `Herkunft:` im Kopf); die gleichzeitig offenen Wünsche `landseg-garten`, `effiz-*` und der erledigte `landseg-historisch-3` (Nachsegmentieren, 18.11.) ändern dieselben Vorlagen, sind aber eigene Ziele (Gärten, Effizienz, Verarbeitung H0), keine Nacharbeit an diesem Wunsch
Anbau: Bildart-Abschnitt in den Einstellungen, Richtwert in Vorlagen, Skill und `pruefen` — Dauer kurz — Risiko gering (Farbbilder unberührt, durch Test gesichert) — danach bleibt: jede weitere Bildart ist ein Abschnitt mehr, kein neuer Code
Umbau: –
Belege: –
Empfehlung: – — kein neuer Sonderfall: ein Abschnitt je Bildart statt `if`-Zweigen im Code

Nacharbeit: `BASIS/.claude/repos/landseg/betrieb.md`, Abschnitt „Schwarz-Weiß-Scans“, um die Bildart-Einstellung und den Richtwert ergänzen.

Reihenfolge der Repos: landseg (einzeln; unter den Wünschen nach `landseg-garten` und `effiz-viertel`/`effiz-bilder` einreihen, weil sie dieselben Vorlagen und den Skill ändern) · Risiken: zu grobe Flächen verschmelzen Häuserzeilen und Gärten (F1, F3); Zusammenlegen nach dem Urteil kann Klassen der Agents verändern; H0-Ergebnisse liegen unversioniert in `daten/landseg/H0` und in der Übergabe-Grundlage, nicht gleichzeitig mit `landseg-historisch-5` ändern · Vorbedingungen: keine

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

Stufe: nein — keine neue Oberfläche: die Prüfseite zeigt nur weniger Flächen in einer bestehenden Ansicht, kein neues Element.
