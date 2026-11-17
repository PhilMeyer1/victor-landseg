# Übergabe an Victor: Fassungen umbenennen, Werkzeuge und Ergebnisse von T0 samt Anleitung als privates GitHub-Projekt

Kurzname: landseg-uebergabe | Datum: 2026-11-17 | Größe: mittel | Bereich: victor | Repos: landseg | Status: eingereiht

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

„ok, setze jetzt mal Alles Frei auf A, dann Kategorien frei und dann erst feste Kategorienliste. und überführe das dann in ein Git Repository, Pushe das auf Git und gib das projekt für Victor frei. Es soll da dann auch eine Anleitung angehängt werden, wie jetzt was genau segmentiert/klassifizert wurde, damit er darauf aufbauen kann"

Präzisierung (Antworten des Nutzers 2026-11-17):
- Neue Reihenfolge und Namen der Fassungen überall (Prüfseite, Kategorienlisten, Ordner bzw. Beschriftung im Projekt, Anleitung): A = „Alles frei“ (bisher C), B = „Kategorien frei“ (bisher B), C = „Feste Kategorienliste“ (bisher A). Die Prüfseite zeigt die Umschalter in dieser Reihenfolge und öffnet mit A.
- Stand jetzt übergeben: Urteile, Kategorienlisten, Karten und Prüfseite aus Teil 2 und 3 von landseg-test-t0; Durchsicht der festen Liste und Teil 4/5 ruhen. Grenzen der listenbasierten Fassungen sind die der Vorstufe, die Vorschläge der KI (verschmelzen, teilen) stehen je Segment dabei — so in der Anleitung sagen.
- Inhalt: ein Projekt mit Werkzeugen (Programm landseg) und Ergebnissen von T0 (je Fassung Karte, Kategorienliste, Urteile; Prüfseite; Gesamtbilder), ohne Zwischenbilder, Ziel unter 100 MB. Hoheitstabelle beachten (abgeleitete Daten liegen sonst unter daten/landseg, nicht im Code-Repo) — der Klärer entscheidet, ob ein eigenes Übergabe-Repo oder ein Ergebnisordner im Repo landseg.
- Anleitung (Deutsch, für Victor, der darauf aufbauen will): Ausgangsbild und Lage von T0, Kacheln/Teilkacheln/Viertel, automatische Vorstufe (SAM 3 usw.), wie die Agents geurteilt haben (je Teilkachel ein Agent, erst ganz T0, dann Segment für Segment), was jede Fassung frei ließ und wie sie klassifizierte, Kategorienlisten mit Ebenen, Dateiformate (Label-Karte uint32, IDs, segmente.json, urteil.json, kategorien*.json), Zahlen (Segmente, unsicher, nicht sauber, Kosten 3,3 Mio. Tokens), bekannte Schwächen (C bisher A: Grenzen der Vorstufe; A bisher C: 309 Nahtverstöße, 20 zerfallene Segmente; B: „Feld gemäht“ ungeprüft, Laub/Nadel nicht getrennt), wie man die Prüfseite öffnet und wie man einen neuen Ausschnitt rechnet. Quellenangabe des Orthofotos.
- Git: privates GitHub-Projekt unter dem Konto PhilMeyer1, Push ausdrücklich gewünscht (macht die Hauptsession nach dem Einreihen), Victor wird eingeladen, sobald der Nutzer seinen GitHub-Kontonamen nennt.

## Fragen

Keine offenen Fragen. Repo-Form, Namen und Ort hat der Prüfer entschieden (siehe Arbeitsauftrag, „Bausteine und Fallen"); der GitHub-Kontoname von Victor fehlt noch und wird erst für die Einladung gebraucht (nach dem Einreihen, Sache der Hauptsession).

## Entscheidungen

entscheidungen.md: nichts für diesen Wunsch (die Zeilen zu landseg betreffen Kategorien und Methode, nicht die Übergabe).

- Nutzer 2026-11-17: Reihenfolge und Namen der Fassungen A = „Alles frei", B = „Kategorien frei", C = „Feste Kategorienliste"; privates GitHub-Projekt unter PhilMeyer1, Push gewünscht (siehe Wunsch).
- Prüfer 2026-11-17 (Form): Ein eigenes Übergabe-Repo `landseg-t0`, nicht ein Ergebnisordner im Code-Repo `landseg`. Grund: Hoheit und Profil verlangen abgeleitete Daten und Bilder außerhalb des Code-Repos; das Übergabe-Repo hat so eine eigene Geschichte und eine eigene Größe (unter 100 MB). Es enthält den Code als Schnappschuss (Kopie der versionierten Dateien von `landseg` auf `main` nach dem Einreihen) und die Ergebnisse.

## Arbeitsauftrag

### Abnahmekriterien

AK1: Die Fassungen heißen überall A = „Alles frei", B = „Kategorien frei", C = „Feste Kategorienliste"; in `einstellungen/seite.json` stehen sie in dieser Reihenfolge, die Prüfseite öffnet mit A und zeigt die Umschalter A, B, C — prüfbar: `PY -B -m unittest discover -s tests -t .` (Tests angepasst, grün), Lesen `landseg/einstellungen/seite.json` und `landseg/README.md`
AK2: Die Prüfseite von T0 im Übergabe-Projekt öffnet mit „A Alles frei" ohne Lücke im Bild und schaltet auf B „Kategorien frei" und C „Feste Kategorienliste" um; je Fassung stimmen Name und Kategorienliste — prüfbar: Ansicht `T0.html` im Übergabe-Projekt, Fassungen A, B, C, Desktop
AK3: Das Übergabe-Projekt `landseg-t0` hat je Fassung einen Ordner (`a-alles-frei/`, `b-kategorien-frei/`, `c-feste-liste/`) mit Karte (Label-Karte und `segmente.json`), Kategorienliste (`kategorien-a.json`, `-b`, `-c`) und Urteilen (`urteil.json` je Teilkachel), dazu Prüfseite und Gesamtbilder; keine Zwischenbilder (keine Viertelbilder, Vorstufen-Rohdaten, Probeläufe, Ansichten je Segment), Gesamtgröße unter 100 MB — prüfbar: `du -sh` und `git count-objects -vH` im Projekt, Lesen der Dateiliste `git ls-files`
AK4: Die Dateien tragen nirgends mehr die alten Zuordnungen (alt C = Feste Liste, alt A = Alles frei): Ordnernamen, Beschriftungen in Prüfseite, `segmente.json`/`urteil.json`-Kopfzeilen (soweit sie eine Kennung tragen) und Kategorienlisten sind umbenannt und stimmen mit der Anleitung überein — prüfbar: `grep -rn "fassung-c\|kern500\|Fassung C\b" <Projekt>` ergibt nur Stellen, die die alte Benennung ausdrücklich als Übersetzungstabelle nennen
AK5: Die Anleitung `ANLEITUNG.md` (Deutsch, für Victor) enthält alle Punkte des Wunschs: Ausgangsbild und Lage von T0, Kacheln/Teilkacheln/Viertel, automatische Vorstufe (SAM 3), Arbeitsweise der Agents (je Teilkachel ein Agent, erst ganz T0, dann Segment für Segment; Vorschläge der KI zum Verschmelzen und Teilen stehen je Segment dabei), was jede Fassung freiließ und wie sie klassifizierte, Kategorienlisten mit Ebenen, Dateiformate (Label-Karte uint32, IDs, `segmente.json`, `urteil.json`, `kategorien*.json`), Zahlen (Segmente, unsicher, nicht sauber, Kosten rund 3,3 Mio. Tokens), bekannte Schwächen, Prüfseite öffnen, neuen Ausschnitt rechnen, Quelle des Orthofotos; die Zahlen stimmen mit den Berichten von `landseg-test-t0` (`-1`, `-3`, `-4`) und den Dateien überein — prüfbar: Lesen `ANLEITUNG.md`, Stichprobe von mindestens 5 Zahlen gegen die Dateien
AK6: Die Schwächen stehen mit der neuen Benennung: C (Feste Liste): Grenzen der Vorstufe; A (Alles frei): 309 Nahtverstöße, 20 zerfallene Segmente; B (Kategorien frei): „Feld gemäht" ungeprüft, Laub/Nadel nicht getrennt; ebenso, dass Durchsicht der festen Liste sowie Teil 4/5 von `landseg-test-t0` ruhen — prüfbar: Lesen `ANLEITUNG.md`
AK7: Das Projekt ist ein lokales Git-Repo mit einem sauberen ersten Stand (`main`, Commit, Arbeitsbaum sauber), Werkzeuge laufen darin: Tests des mitgelieferten Pakets sind grün und `python -m landseg --help` läuft; `README.md` verweist auf die Anleitung — prüfbar: `git -C <Projekt> status --short` leer, `PY -B -m unittest discover -s tests -t .` im Projekt
AK8: Der Weg des Nutzers: Er öffnet das Übergabe-Projekt, liest `README.md`, doppelklickt `T0.html` und sieht die drei Fassungen in der neuen Reihenfolge; die Anleitung sagt, wie ein neuer Ausschnitt gerechnet wird, und die dort genannten Befehle laufen an einem Probeausschnitt (Kacheln bis Zusammentragen, ohne GPU-Teil) — prüfbar: Ansicht `T0.html` Desktop, Befehle der Anleitung am laufenden Stand

Nacharbeit: `C:/Users/Phil/Developement/.claude/hoheit.md`, Abschnitt „Victor": Zeile für die abgeleiteten Landseg-Daten (`daten/landseg/`, Übergabe-Projekt `landseg-t0`, Namensraum `landseg:`, Hoheit Bereich victor) ergänzen; Profil `landseg` (`BASIS/.claude/repos/landseg.md`, Abschnitt zu Fassungen/Ordnern) und Lagebild nachziehen, falls vorhanden; `daten/README.md` um den Ort des Übergabe-Projekts erweitern. Push und Einladung von Victor (Konto noch offen) macht die Hauptsession nach dem Einreihen: `gh repo create PhilMeyer1/landseg-t0 --private`, dann `git push`.
Nachts wiederholen: keine

### Einstieg

- landseg: `einstellungen/seite.json:4-14` — drei Fassungen heute A „Feste Kategorienliste" (`vorstufe`), B „Kategorien frei" (`fassung-b`), C „Alles frei" (`fassung-c`); Reihenfolge, Kennungen, Namen, Beschreibungen und `ordner` ändern sich (A Alles frei, B Kategorien frei, C Feste Kategorienliste).
- landseg: `landseg/seite.py` und `landseg/seite_vorlage/` — Anzeige-Reihenfolge, Start mit der ersten Fassung, feste Kennungen A/B/C im Code (suchen: `"A"`, `"fassung"`, `start`); prüfen, ob die Reihenfolge nur aus den Einstellungen kommt.
- landseg: `README.md:24`, `:81-89`, `:176-197` — Beschreibung der Fassungen mit der alten Zuordnung; umstellen.
- landseg: `tests/test_seite.py:67-172` — Tests nehmen A = Vorstufe, B = `fassung-b`, Kennungen `["A","B","C"]`; an die neue Reihenfolge anpassen.
- Daten (nur lesen, Quellen für das Übergabe-Projekt): `daten/landseg/T0/kern500/` (bisher Fassung A, feste Liste: `urteil/`, `urteil-zweit/`, `ganz/`, `seite/T0.html`, `kategorien` des Repos), `daten/landseg/T0/fassung-b/` (`urteil/`, `kategorien-b.json`, Karten), `daten/landseg/T0/fassung-c/` (bisher Alles frei: `zusammen/` mit `labels.tif`, `naht.json`, `segmente.json`, `abgabe/`, `kategorien-c.json`). Hinweis: Wo genau Karten und Segmente von A (fest) und B liegen, klärt der Umsetzer an den Berichten `wuensche/2026-11-17-landseg-test-t0-1/bericht-landseg.md` und `-3/bericht-landseg.md`.
- Quelle des Orthofotos: `daten/README.md:27-29` (Blatt 5236-56, 0,2 m je Bildpunkt, EPSG:31255, Lieferung vom 17.11.2026); Anbieter und Lizenz dort nicht genannt, im Bericht 48 (`unterlagen`) nachsehen.

### Bausteine und Fallen

- Vorhandene Werkzeuge nutzen, nicht nachbauen: `PY -B -m landseg seite --manifest <m> --ziel <x.html> [--nachher <ordner>]` baut die Prüfseite mit den Fassungen aus `einstellungen/seite.json` (`--einstellungen <datei.json>` ersetzt die Fassungsliste, ohne Code zu ändern); `pruefen` und `naht` prüfen Karten; `PY -I tools/pruefe_kategorien.py <kategorien-x.json>` prüft Listen.
- Reihenfolge: erst die Benennung im Code-Repo `landseg` ändern, Tests grün, committen (im Worktree `wunsch-landseg-uebergabe`); dann das Übergabe-Projekt aus dem eingereihten `main` bauen (`git archive main` des Repos als Code-Schnappschuss) und die Ergebnisse aus `daten/landseg/T0/` hineinkopieren (nicht verschieben; die Originaldaten bleiben unverändert).
- Das Übergabe-Projekt liegt unter `daten/landseg/uebergabe/landseg-t0/` (eigenes Git-Repo, vom Basis-Repo wegen `/daten/*` nicht erfasst) und nicht im Ordner `landseg`; kein Eintrag im Basis-Repo außer den Nacharbeiten.
- Umbenennung der Ergebnisordner nur in der Kopie; Dateien, die eine Kennung (A/B/C oder Ordnernamen) enthalten, einmal gezielt durchsuchen (`grep`), nicht blind ersetzen: Zwischenstände (`urteil-stand`, `vereinheitlichung`, `probe-b`, `viertel`, `vorstufe` je Viertel, `ansicht`, `stand`, `abgabe` roh) gehören nicht mit; was Victor zum Nachvollziehen braucht (Urteile und Karten), ja. `sam3_roh.npz` zählt zur Vorstufe und bleibt weg, außer wenn die Größe es erlaubt und die Anleitung es als „ohne GPU nachrechnen" nutzt (Größe zuerst messen).
- Größenfalle: Das Ziel unter 100 MB; die drei Ordner der Quellen messen zusammen etwa 320 MB mit Zwischenbildern. Zuerst die Mindestmenge zusammenstellen (Label-Karten sind zlib-TIFF und klein), dann messen; die großen Posten sind `viertel/` (je 47 MB) und `vorstufe/` (66 MB), die wegfallen. Keine Modellgewichte.
- Falle Seite: `T0.html` ist eine Datei mit eingebetteten Bildern (je Fassung etwa 7 MB bei 4 Teilkacheln); sie muss aus dem neu angelegten Ordnerbau gebaut werden, nicht aus der alten Seite kopiert, sonst stimmen Ordnernamen und Reihenfolge nicht.
- Falle Zahlen: Zahlen der Anleitung aus den Berichten und aus den Dateien zählen (Segmente je Fassung, unsicher, „nicht sauber", Nahtverstöße 309 und zerfallene Segmente 20 für Alles frei); widersprechen sich Bericht und Datei, gilt die Datei und die Anleitung sagt es.
- Falle Quelle und Rechte: Der Ausschnitt des Orthofotos (`T0.png`) ist ein abgeleitetes Bild eines gelieferten Datensatzes; Anbieter und Nutzungsbedingungen sind unbekannt. Die Anleitung nennt, was bekannt ist (Lieferung 17.11.2026, Blatt 5236-56, 0,2 m, EPSG:31255; Bericht 48 prüfen) und sagt offen „Anbieter und Lizenz nicht dokumentiert"; der Nutzer gab das Projekt dafür ausdrücklich frei (privates Repo).
- Der Push gehört nicht in diesen Lauf (Hauptsession nach dem Einreihen), das Anlegen des Remotes auch nicht.

### Bauweise

Richtung: neutral
Berührt: keine — A1 (`ansicht.py:117`) wird nicht angefasst
Tilgt: keine
Flick-Signale: keine — Kette `landseg-werkzeuge-5` (Prüfseite, Fassungsumschalter) > `landseg-test-t0` > dieser Wunsch: keine Wiederholung derselben Störstelle, dieser Wunsch benennt nur Fassungen um und packt Ergebnisse; kein Fehlerbild in den Gliedern.
Anbau: Benennung und Ordner im Übergabe-Projekt; die feste Zuordnung kommt nur aus `seite.json`, kein neuer Sonderfall — Dauer kurz — Risiko gering — danach bleibt ein Übergabe-Projekt, das Victor selbst weiterführt.
Empfehlung: – — neutral, keine Altlast berührt.

Reihenfolge der Repos: landseg · Risiken: Größe über 100 MB bei zu großer Auswahl, übersehene alte Kennungen in Dateien, Orthofoto-Rechte unbekannt, Zahlen der Anleitung weichen von den Dateien ab · Vorbedingungen: keine

## Teile

<entfällt: Größe mittel>

## Varianten

<entfällt>

## Entwurf

Stufe: nein — nur Reihenfolge und Beschriftung der Umschalter in der bestehenden Prüfseite; keine neue Oberfläche.
