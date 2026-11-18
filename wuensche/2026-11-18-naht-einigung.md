# Landschafts-Segmente: Einigungsschritt an den Übergängen der Teilkacheln, damit gleiche Flächen über eine Naht hinweg dieselbe Klasse bekommen; auf T0 anwenden und Victors Projekt aktualisieren

Kurzname: naht-einigung | Datum: 2026-11-18 | Größe: gross | Bereich: victor | Repos: landseg | Status: eingereiht

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

„Bei den Tiles am Ende sollen sich dann alle Agents bei den Übergängen mit den Klassifikationen einigen. So, dass nicht gleiche Flächen unterschiedliche Lables bekommen weil sich die Agenten nicht abgesprochen haben"

Präzisierung:
- Heute urteilt je Fassung ein Agent je Teilkachel (r0c0, r0c1, r1c0, r1c1); die Ergebnis-Ansicht meldet z. B. „67 Stellen an Nähten passen nicht“. Gleiche Flächen (eine Wiese, ein Waldstück, eine Straße), die über die Grenze zweier Teilkacheln laufen, haben dadurch teils verschiedene Klassen.
- Ziel: ein fester Einigungsschritt nach den Urteilen, in jedem Lauf (heute T0, später ganze Orthofotos): An allen Übergängen (Nähte zwischen Teilkacheln, auch an den Ecken mit vier Teilkacheln und an den Viertelgrenzen innerhalb einer Teilkachel) werden die Klassen der angrenzenden Segmente abgeglichen; zusammengehörige Flächen bekommen eine gemeinsame Klasse; was sich nicht klären lässt, wird als unsicher markiert und mit Grund belegt. Die Einigung sieht die Bilder beider Seiten (Urteil im Verbund, nicht Einzelbild). Wie die Agents dafür zugeschnitten werden (z. B. ein Agent je Naht mit beiden Seiten, oder die Agents der Nachbar-Teilkacheln gemeinsam), entscheidet die Klärung; die Zahl der Agents und Kosten nennen.
- Gilt für alle drei Fassungen: A (feste Liste), B (eigene gemeinsame Liste), C (alles frei, je Agent eigene Kategorien: dort zuerst klären, wie eine Einigung über verschiedene Kategorienlisten aussieht).
- Messbar: Zahl der Stellen an Nähten, an denen gleiche Flächen verschiedene Klassen haben, vorher und nachher je Fassung; die Ergebnis-Ansicht zeigt die neue Zahl.
- Danach auf T0 anwenden, Ergebnis-Seiten neu erzeugen, ANLEITUNG des Gesamtprojekts um den Schritt ergänzen; Gesamtprojekt neu bauen und hochladen macht die Hauptsession. Parallel läuft seite-kachelwahl (Kachel-Wahl der Seite) im selben Repo; beim Neu-Erzeugen der Seiten danach richten.
- Entscheidung dazu: entscheidungen.md, 2026-11-18 „Einigung an den Übergängen der Teilkacheln“.

## Fragen

### F1: Sollen an den Nähten nur die Klassen abgeglichen werden, oder sollen auch zerschnittene Flächen zu einem Stück zusammengefügt werden?
- Lage: In der Ergebnis-Ansicht (Schalter „Nähte“, Zeile „… Stellen an Nähten passen nicht“) gibt es heute zwei Arten von Naht-Problemen: (1) eine Fläche läuft über die Grenze zweier Teilkacheln und trägt links und rechts eine andere Klasse (z. B. links „Wiese“, rechts „Acker“), (2) die Grenzlinie zwischen zwei Teilkacheln ist eine gerade Schnittlinie, obwohl das Luftbild dort keine Kante zeigt; die Fläche besteht dann aus zwei Segmenten, auch wenn beide dieselbe Klasse tragen. Deine Vorgabe betrifft die Klassen („nicht gleiche Flächen unterschiedliche Labels“). Heute zählt die Ansicht beides zusammen (je Fassung rund 300 Stellen); die Zahl der Stellen mit verschiedenen Klassen ist kleiner (nach Zählung des Prüfers etwa 36 bis 45 Segment-Paare je Fassung).
- Empfohlen: Nur die Klassen abgleichen; die Grenzlinien und die Segmentzahl bleiben unverändert — Das ist, was der Wunsch sagt, es ändert keine Karten und macht keine Urteile ungültig; die Ansicht zeigt dann eine neue Zahl „gleiche Fläche, verschiedene Klasse“ (nachher möglichst 0, Rest als unsicher markiert), die alte Zahl der geraden Schnittlinien bleibt als eigene Zahl daneben stehen.
- Klassen abgleichen und zerschnittene Flächen zusammenfügen — Auch die geraden Schnittlinien verschwinden (Segmente über der Naht werden verschmolzen), die alte Zahl fällt dann ebenfalls; das ändert die Karten selbst und alle Segmentnummern, ist deutlich mehr Arbeit und Risiko (Fassung A hat zusätzlich 20 Segmente, die über die Naht zerfallen) und wäre besser ein eigener Wunsch.

## Entscheidungen

- 2026-11-18: Landschafts-Segmente: Einigung an den Übergängen der Teilkacheln: Nutzer am 18.11.2026: „Bei den Tiles am Ende sollen sich dann alle Agents bei den Übergängen mit den Klassifikationen einigen. So, dass nicht gleiche Flächen unterschiedliche Labels bekommen, weil sich die Agenten nicht abgesprochen haben.“ Daraus: Nach den Urteilen je Teilkachel folgt in jedem Lauf ein fester Einigungsschritt an allen Übergängen (Nähte zwischen Teilkacheln, auch die Viertelgrenzen): Segmente, die über eine Naht laufen oder an ihr dieselbe Fläche zeigen, bekommen eine gemeinsame, abgestimmte Klasse; unaufgelöste Widersprüche werden als unsicher markiert und belegt, nicht stillschweigend gelassen. Gilt für jede Fassung (A, B, C) und für alle künftigen Läufe (ganzes Orthofoto). (aus entscheidungen.md, 2026-11-18)
- entscheidungen.md, sonst für diesen Wunsch: „Die Seite zeigt je Bild genau einen Stand, das Ergebnis … kein Vorher/Nachher“ (aus entscheidungen.md, 2026-11-17): Die Ergebnis-Ansicht zeigt nur den einigten Stand und die neue Zahl; „vorher“ steht nur im Bericht des Datenlaufs.
- 2026-11-18, F1 (Nutzer): Nur Klassen abgleichen. Grenzlinien, Karten und Segmentnummern bleiben unverändert; die Ansicht zeigt die neue Zahl „gleiche Fläche, verschiedene Klasse“ (davon unsicher) und daneben die Zahl der geraden Schnittlinien als eigene Zahl. Zusammenfügen zerschnittener Flächen ist nicht Teil dieses Wunschs.

## Arbeitsauftrag

### Abnahmekriterien

AK1: Ein neues Werkzeug `einigung finden` sucht an allen Kerngrenzen (Nähte und Ecken) und an den Viertelgrenzen im Kern (Mitte jeder Teilkachel) die Stellen, an denen zwei benachbarte Segmente ohne Bildkante verschiedene Klassen tragen, bündelt zusammenhängende Segment-Paare (eine Ecke bleibt in einem Bündel) und legt je Bündel einen Auftrag mit Bildern beider Seiten ab — prüfbar: `PY -B -m unittest tests.test_einigung` (synthetische Karte mit Naht, Ecke, Viertelgrenze, echter Kante) und `PY -B -m landseg einigung finden --help`
AK2: `einigung anwenden` setzt aus der Abgabe der Agents je Paar eine von drei Entscheidungen um: gleiche Fläche (beide Segmente bekommen eine gemeinsame, in der Kategorienliste der Fassung gültige Klasse), echte Grenze (nichts ändert sich, Begründung wird festgehalten), unklar (beide Segmente `sicher: nein` mit Grund); Label-Karten bleiben bildpunktgleich, `pruefen` bleibt `ok`, jede Änderung steht im Verlauf der `segmente.json` mit Bearbeiter, nur Kern-Segmente werden geändert — prüfbar: `PY -B -m unittest tests.test_einigung`
AK3: `einigung messen` nennt je Fassung die Zahl der Stellen (Segment-Paare und Randpunkte) mit gleicher Fläche und verschiedener Klasse, getrennt: offen, als unsicher belegt, geklärt; nach dem Anwenden einer Abgabe sinkt „offen“ entsprechend; die Zählung benutzt dieselbe Bildkanten-Regel wie `naht` (gleicher Bildleser) — prüfbar: `PY -B -m unittest tests.test_einigung`
AK4: Für die Agents gibt es die Vorlage `vorlagen/einigung.md` (Urteil im Verbund: Bilder beider Seiten, ein Urteil je Stelle für alle Beteiligten, nur Klassen im Kern, Abgabe `einigung_abgabe.json`) samt Regel L13 im Skill `landseg-agent` und Eintrag in der Vorlagen-Tabelle; sie sagt für Fassung A ausdrücklich, dass die Einigung auf der zusammengelegten Liste `kategorien-a.json` läuft — prüfbar: Lesen `vorlagen/einigung.md`, `vorlagen/README.md`, `.claude/skills/landseg-agent/SKILL.md`; `PY -B -m unittest tests.test_vorlagen`
AK5: Die Ergebnis-Ansicht zeigt je Fassung und im Schalter „Nähte“ die neue Zahl „Stellen, an denen gleiche Flächen verschiedene Klassen haben“ (davon unsicher belegt), getrennt von der bisherigen Zahl der Schnittlinien ohne Bildkante; beide Zahlen stimmen mit `einigung messen` bzw. `naht` überein (der Nähte-Schalter benutzt den gemeinsamen Bildleser, Altlast A2 erledigt) (nach F1) — prüfbar: Ansicht Ganzer Ausschnitt, Fassung C, Schalter Nähte an, Desktop; `PY -B -m unittest tests.test_seite`
AK6: Auf T0 ist die Einigung für alle drei Fassungen gefahren: Agents je Bündel, beide Seiten im Blick; im Bericht stehen je Fassung die Zahl vorher und nachher, Zahl der Agents, Tokens und Dauer; nachher bleibt höchstens, was als unsicher mit Grund belegt ist — prüfbar: `PY -B -m landseg einigung messen` je Fassung auf dem einigten Stand, Lesen des Berichts im Berichtsordner
AK7: Der Weg des Nutzers: Die neu erzeugte Seite `T0.html` öffnet, jede Fassung A/B/C zeigt den einigten Stand und die neue Zahl, ein Klick auf ein Segment an einer Naht zeigt Klasse und (falls unsicher) den Grund der Einigung — prüfbar: Ansicht `T0.html` (neu erzeugt), Fassung A, Teilkachel r0c1, Nähte an, Desktop
AK8: `gesamt/ANLEITUNG.md` (und, wo es den Aufbau nennt, `gesamt/README.md`) beschreibt den Einigungsschritt: warum, wie die Agents zugeschnitten sind, wie die Zahl gezählt wird, vorher/nachher je Fassung, Kosten; „Bekannte Schwächen“ und „Zahlen“ sind nachgezogen; `gesamt_projekt.py pruefen` bleibt `ok` — prüfbar: Lesen `gesamt/ANLEITUNG.md`; `PY -B tools/gesamt_projekt.py pruefen --basis <BASIS> --ziel <Test-Ziel>` (wie in den Tests des Repos)

Nacharbeit: Gesamtprojekt neu bauen und hochladen (Hauptsession, nach Einreihen von seite-kachelwahl und aller Teile); Profil landseg (`Routinen`: `einigung`, `Themen`-Datei `betrieb.md`: Einigung gehört nach dem Zusammentragen, vor dem Erzeugen der Seite) nachziehen.

### Einstieg

- landseg: `landseg/naht.py:52` (`grenzen`) — Kerngrenzen der Teilkacheln als Strecken; dazu kommen die Viertelgrenzen (Mitte jedes Kerns, 250 px) als zweite Art Grenze; neues Modul `landseg/einigung.py` baut darauf auf
- landseg: `landseg/naht.py:84`, `:100`, `:114` (`kantenstaerke`, `gegenueber`, `_strecken`) — Bildkanten-Regel und Strecken je Segment-Paar; wiederverwenden, nicht nachbauen
- landseg: `landseg/naht.py:168` (`pruefe_naehte`) — liefert heute „ohne_kante“-Verstöße je ID-Paar unabhängig von der Klasse; `einigung` filtert daraus die Paare mit verschiedener Klasse und kennt die Klasse aus `segmente.json`
- landseg: `landseg/zusammentragen.py:91` (`kern_ausschneiden`) — Kern je Teilkachel aus der Karte mit Kontextrand; so wird die Karte des Ausschnitts zusammengesetzt (wie `seite.py:86`)
- landseg: `landseg/eingriff.py:260` (`klasse_setzen`) — setzt Klasse mit Verlaufseintrag und Prüfung der Kategorienliste; für das Anwenden benutzen, nicht eigene Schreibroutine
- landseg: `landseg/__main__.py:129` (`befehl_naht`), `:364` (Parser) — Muster für den neuen Befehl `einigung` (Unterbefehle `finden`, `anwenden`, `messen`; Docstring, Importe, Fehlerfang, README-Tabelle)
- landseg: `landseg/seite.py:60`, `:99`, `:130`, `:272` — `_lese_bild` (eigener Leser, Altlast A2) und die Naht-Zählung je Fassung; Zahl „Klasse verschieden“ ergänzen, Leser vereinheitlichen
- landseg: `landseg/seite_vorlage/seite.js:307`, `:523` — Textzeilen „… Stellen an Nähten passen nicht“ (je Teilkachel bzw. Ganzer Ausschnitt); neue Zahl daneben
- landseg: `einstellungen/seite.json` — Fassungen A/B/C mit `ordner`; neue `einstellungen/einigung.json` (Bündelgröße, Bildfenster um die Stelle, Mindestlänge) nach dem Muster der anderen Werkzeuge (`landseg/einstellungen.py`)
- landseg: `vorlagen/naht.md`, `vorlagen/README.md`, `.claude/skills/landseg-agent/SKILL.md` (L6 Nahtregel) — Vorbild für `einigung.md` und die neue Regel L13
- landseg: `gesamt/ANLEITUNG.md:145` („Wie die KI geurteilt hat“), `:235` („Zahlen“), `:253` („Bekannte Schwächen“) — hier den Einigungsschritt ergänzen

### Bausteine und Fallen

- Ausgangszahlen (Prüfer-Messung am Stand von `ergebnisse/`, Gesamtprojekt): Kerngrenzen 4 à 500 Punkte, plus Viertelgrenzen. Schnittlinien ohne Bildkante: A 309, B 312, C 312. Davon mit verschiedener Klasse: A 230 Strecken (45 Segment-Paare, 861 Randpunkte), B 149 (40 Paare, 563 Punkte), C 158 (36 Paare, 602 Punkte); an den Viertelgrenzen je Fassung etwa 33 Stellen ohne Bildkante (hier gehören die meisten Seiten demselben Segment, Klassenwiderspruch dort nur bei zwei Segmenten). Der Umsetzer prüft diese Zahlen beim Bau gegen und stützt AK3 darauf.
- **Fassungsnamen:** Der Wunschtext nennt noch die alte Benennung („A feste Liste, B eigene gemeinsame Liste, C alles frei“). Heute gilt: A = Alles frei (`a-alles-frei`, Ordner `fassung-c` in `daten/landseg/T0/`), B = Kategorien frei (`b-kategorien-frei`, `fassung-b`), C = Feste Kategorienliste (`c-feste-liste`, `kern500`). In allen Ergebnissen, Berichten und der ANLEITUNG gilt die heutige Benennung.
- **Fassung A (Kategorien je Agent):** Die vier Listen sind schon zu `kategorien-a.json` (47 Klassen) zusammengelegt, `klasse` je Segment ist ein Code dieser Liste (der ursprüngliche steht unter `klasse_teil`). Die Einigung läuft auf dieser gemeinsamen Liste; sieht der Agent, dass beide Seiten dieselbe Fläche meinen, wählt er die Klasse der gemeinsamen Liste, die am besten passt, und nennt Grund. Keine neue Klasse anlegen; passt keine, Stelle als unsicher belegen.
- **Fassung B und C:** Grenzen und IDs stammen aus der Vorstufe je Teilkachel (IDs je Teilkachel verschieden, daher ID-Paare an der Naht); `klasse` in `segmente.json` ist maßgeblich (C: `klasse_vorschlag`, sonst `klasse_heute`). Die Einigung ändert `klasse` (und `grob`) mit Verlaufseintrag; `urteil.json` bleibt unverändert und wird nicht nachgeschrieben, `segmente.json` bekommt je betroffenem Segment einen Verweis `einigung` mit Entscheidung und Grund.
- **Nur Klassen, keine Grenzen (nach F1):** Label-Karten bleiben bildpunktgleich. Gäbe der Nutzer bei F1 die zweite Option, wird daraus ein anderer Auftrag (Karten ändern).
- **Zuschnitt der Agents (Prüfer-Entscheidung):** Ein Bündel ist eine zusammenhängende Gruppe von Segment-Paaren (über gemeinsame Segmente verbunden; ein Eckpunkt mit vier Teilkacheln fällt so in ein Bündel); je Bündel höchstens etwa 12 Paare (Wert in `einstellungen/einigung.json`), größere Gruppen werden an dünnsten Stellen geteilt, nie mitten durch ein Paar. Ein Agent bekommt je Paar ein Bild beider Seiten (Teilkachelbild samt Kontextrand, Fenster um die Stelle, vergrößert) und liest beide Teilkachel-Urteile (`urteil.json`) mit. Für T0 ergibt das je Fassung 3 bis 4 Agents, zusammen etwa 10 parallel; geschätzt 1 Mio. Tokens und etwa 10 Minuten (zum Vergleich: die Urteile selbst brauchten 15 Agents, 3,3 Mio. Tokens, 25 Minuten); das ist ungemessen, der Bericht nennt die tatsächlichen Zahlen. Ein Agent je Naht wäre größer als nötig (4 Nähte à 9 bis 11 Paare) und trennt die Ecke; ein Agent je Fassung wäre nicht parallel und für ganze Orthofotos zu lang. Mehrere gleichartige Einheiten parallel, nie nacheinander.
- **Viertelgrenzen:** Innerhalb einer Teilkachel gibt es nur eine Karte; ein Segment über die Mitte hat eine ID und eine Klasse. Zu klären bleiben nur zwei Segmente ohne Bildkante dazwischen mit verschiedener Klasse; sie laufen im selben Verfahren wie Nähte (Kennzeichnung `viertel` statt Naht-Name).
- Jedes Segment erscheint in höchstens einem Bündel; gleiche Fläche über mehrere Teilkacheln (Kette a–b–c) bekommt eine Klasse für alle Glieder, nicht paarweise verschiedene.
- Kontextrand-Segmente (`urteil: kontextrand`, `im_kern: false`) nie ändern.
- Zeitliche Fallen: `seite-kachelwahl` ändert im selben Repo `seite.js`, `seite.py`, `gesamt/ANLEITUNG.md`, `gesamt/CLAUDE.md` (Arbeitskopie `.claude/worktrees/wunsch-seite-kachelwahl`). Teile 3 und 4 erst nach dem Einreihen von seite-kachelwahl beginnen und auf dessen Stand aufsetzen; Konflikte in `__main__.py` und README: beide Seiten behalten.
- Geheimnisschutz-Hook blockt Bash-Muster mit `daten/landseg`: für Suchen dort das Grep-Werkzeug; Python-Hilfsskripte mit Escapes über das Write-Werkzeug anlegen.
- Agents ohne Fenster, Bilder höchstens 2000 Bildpunkte an der langen Seite (L11).

### Bauweise

Richtung: neutral
Berührt: A2 — der Wunsch ändert die Naht-Zählung der Seite (`seite.py:99`) und braucht dafür dieselbe Bildkanten-Regel wie `naht`; A2 (eigener Bildleser, Nähte-Schalter zeigt für A 124 statt 309) würde die neue Zahl verfälschen
Tilgt: A2 — der gemeinsame Leser `naht.lese_bild` ersetzt `_lese_bild` in `seite.py` (kleiner Umbau, Teil 3)
Flick-Signale: keine — kein Vorgänger (Kopf ohne `Herkunft:`; `seite-kachelwahl` läuft parallel, ist aber kein Glied derselben Kette)
Anbau: `einigung` als neues Modul mit Vorlage, wiederverwendet Nahtregel, `eingriff` und Seite — Dauer mittel (Teile) — Risiko niedrig, Karten unverändert — danach bleibt: Einigung ist ein fester Schritt nach dem Zusammentragen
Umbau: –
Belege: –
Empfehlung: Anbau — neues Muster ohne Altlast außer A2, kein zweiter Weg (die Naht-Zählung wird gemeinsam genutzt, nicht kopiert)

Reihenfolge der Repos: landseg · Risiken: Klassen-Entscheidungen der Agents sind Urteile am Bild (unsicher bleibt erlaubt); gleiche Datei-Bereiche wie seite-kachelwahl; Datenlauf mit Agents ohne Netz zurück; Maschinenzeit gering (keine GPU nötig) · Vorbedingungen: keine

## Teile

1. Einigungs-Werkzeug mit Vorlage — Umsetzer — Repo: landseg — Vorbedingungen: keine — nach: – — AK 1, 2, 3, 4 — `landseg einigung` (finden, anwenden, messen), `vorlagen/einigung.md`, Regel L13, `einstellungen/einigung.json`, Tests auf synthetischen Karten; Karten bleiben unverändert, Klassen und Verlauf stimmen.
2. Einigung auf T0 für A, B, C — Workflow — Repo: landseg — Vorbedingungen: keine — nach: 1 — AK 6 — je Bündel ein Agent (etwa 10 parallel): Einheiten sind die Bündel, „richtig“ heißt Abgabe nach Schema, `pruefen` ok, Zahl nachher nur unsicher mit Grund; Bericht mit vorher/nachher je Fassung, Agents, Tokens (Ergebnis: ohne Commit).
3. Ergebnis-Ansicht: neue Zahl und gemeinsamer Bildleser — Umsetzer — Repo: landseg — Vorbedingungen: keine — nach: 1 — AK 5 — Seite zeigt die Zahl „gleiche Fläche, verschiedene Klasse“ (davon unsicher) neben der Zahl der Schnittlinien, Nähte-Schalter nutzt `naht.lese_bild`; Wortlaut und Zahl in der bestehenden Ansicht; kein Entwurf. Erst nach dem Einreihen von seite-kachelwahl.
4. Seiten neu erzeugen und ANLEITUNG — Umsetzer — Repo: landseg — Vorbedingungen: keine — nach: 2, 3 — AK 7, 8 — Ergebnis-Seiten für T0 mit dem einigten Stand neu erzeugt (Prüfseiten in `daten/landseg`, `T0.html` für das Gesamtprojekt), `gesamt/ANLEITUNG.md` und `gesamt/README.md` um den Schritt ergänzt; Bau und Upload des Gesamtprojekts bleibt bei der Hauptsession. Erst nach dem Einreihen von seite-kachelwahl.

## Varianten

Keine.

## Entwurf

Stufe: nein — nur Zahl und Wortlaut in der bestehenden Ansicht „Nähte“ (eine Textzeile je Fassung und je Teilkachel); nichts Neues im Aufbau.
