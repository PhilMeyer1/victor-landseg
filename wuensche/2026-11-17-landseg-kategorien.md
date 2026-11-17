# Gestufte Kategorienliste für Landschafts-Segmente (7/25/46 Klassen) mit Regeln als Datei und Beschreibung im Repo landseg festschreiben

Kurzname: landseg-kategorien | Datum: 2026-11-17 | Größe: klein | Bereich: victor | Repos: landseg | Status: eingereiht | Herkunft: Ermittlung landseg-methode K1

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

K1: Kategorienliste festschreiben (`kategorien.json` hierarchisch 7/25/46 mit Regeln G1–G5, U1–U5, Abbildungen; als Bericht in unterlagen) — Gewinn feste Grundlage für jede Beschriftung — Aufwand klein — Risiko gering (SW-Spalte bleibt bis K4 Vermutung) — Repo unterlagen — empfohlen

Belege: wuensche/2026-11-17-landseg-methode/bericht.md, K1.

Empfehlung der Deutung (wuensche/2026-11-17-landseg-methode.md, Abschnitt Empfehlung):
- K1: trägt — die Kategorienliste ist die zweite Hälfte von „jedes Segment mit Kategorie" und braucht wenig Aufwand; sie hängt aber an den Entscheidungen F2 und F5 und wird von K2 als `kategorien.json` gebraucht.
- Nächster Schritt: K2 als Folge-Wunsch (nachdem Sie F4 zum Ort entschieden haben), zugeschnitten auf den Test T0: Werkzeuge W1–W8 und die Vorlagen W10, `kategorien.json` aus K1 mitnehmen, den Export W9 erst nach dem Test. Abgenommen wird an einer Teilkachel von T0: Die Vorstufe läuft, `pruefen` meldet H × W ohne 0, und die Zahl der Segmente je Teilkachel ist gemessen. — Danach kann K3 sofort laufen, und die unsicherste Annahme ist schon geprüft, bevor der erste Agent urteilt.
- Gegenargument: Am Bild ist bisher nichts erprobt. Im Stitcher urteilte ein Agent über genau ein Segment (4–8 min); in T0 kämen auf eine Teilkachel von 500 px 40–60 Segmente (nur vermutet, `bericht.md` 3.6). Die Vorstufe erreicht auf ähnlichen Bildern nur 43–60 % mIoU und ist gerade bei Hecken, Wegen und Kleinobjekten schwach (`e03.md` L6/B3), also genau bei der Feinheit, die Sie wollen. Ein großer Werkzeugkasten könnte deshalb um eine Einheitengröße herum gebaut werden, die nicht trägt. — Der Schritt gilt trotzdem: Die Größe der Teilkacheln ist ein Parameter in W1 (auf 250 px verkleinerbar) und kein Umbau, und die Abnahme an einer echten T0-Teilkachel misst die Dichte, bevor K3 Agent-Läufe kostet.

## Fragen

Keine offenen Fragen: Kategorien, Stufen, Wege und Farbe/SW sind in `entscheidungen.md` (17.11.2026) entschieden. Hinweis: Der Wunschtext nennt „als Bericht in unterlagen" und „Repo unterlagen"; nach Entscheidung F4 und laut Titel liegt alles im Repo landseg, `unterlagen` bleibt unberührt.

## Entscheidungen

- Landschafts-Segmentierung, Grundsätze (aus entscheidungen.md, 2026-11-17): (F4) Die Werkzeuge entstehen im eigenen Repo landseg; der Stitcher bleibt unberührt. (F1) Segmente so fein, wie im Bild sicher erkennbar; die Mindestgröße aus Bericht 48 ist nur eine gröbere Auswertungsebene. (F2, F5) Kategorien allgemein und gestuft (7/25/46), grobe Ebene = die sechs Klassen aus Bericht 48 plus „nicht bestimmbar", feine Ebene enthält die Bienenklassen; unbefestigte Wege zählen zur Verkehrsfläche, Weingärten und Obstanlagen zu Acker. Jeder Bildpunkt gehört zu genau einem Segment mit Kategorie (lückenlos). Vorläufig wie empfohlen angenommen: (F3) Beschriften auf dem Farbbild, fürs Training zusätzlich eine Schwarz-Weiß-Fassung mit denselben Segmenten; (F6) offene Zusatzdaten im ersten Test nicht; (F7) mehrere Jahrgänge erst nach den Tests. Reihenfolge: Kategorienliste und Werkzeuge, dann Test am Orthofoto-Ausschnitt T0. (aus entscheidungen.md, 2026-11-17)
- Push zu GitHub: nur auf ausdrückliche Ansage, nie automatisch (aus entscheidungen.md, 2026-11-17)

## Arbeitsauftrag

### Abnahmekriterien

AK1: Im Repo landseg liegt `kategorien.json` mit genau 7 Klassen der Ebene 1 (Codes 0 bis 6), 25 der Ebene 2 und 46 Blättern (Klassen ohne Kind); jede Klasse hat Code, Name, Eltern, Ebene, Farbe, SW-Kennzeichen (`ja|eing.|nein`) und die Abbildungen auf CORINE, CLC+, FLAIR, DKM und Bericht 48 — prüfbar: `python -I tools/pruefe_kategorien.py kategorien.json` meldet 7/25/46 und „ok" (Skript: AK2)
AK2: Ein kleines Prüfskript im Repo (`tools/pruefe_kategorien.py`, nur Standardbibliothek) prüft die Datei: Codes eindeutig, jeder Elterncode vorhanden, Farben gültig und paarweise verschieden, Pflichtfelder gesetzt; es schlägt bei einer beschädigten Kopie fehl — prüfbar: Befehl aus AK1 auf die echte Datei und auf eine beschädigte Kopie im Scratch-Ordner (nicht im Repo)
AK3: Die Regeln G1–G5 und U1–U5 stehen maschinenlesbar im Repo (Abschnitt `regeln` in `kategorien.json` oder `regeln.json` daneben), je Regel mit Nummer, Wortlaut und Herkunft — prüfbar: das Prüfskript zählt 5 G- und 5 U-Regeln
AK4: `KATEGORIEN.md` im Repo erklärt in Alltagssprache den Aufbau (drei Ebenen), die Klassen als Tabelle, die Regeln G1–G5/U1–U5 und die vier Abweichungen von Bericht 48 (A1–A4, mit Verweis auf die Entscheidungen F1, F2, F5) — prüfbar: Lesen `KATEGORIEN.md`
AK5: Ungesichertes ist gekennzeichnet: die SW-Spalte ausdrücklich als Vermutung bis zum Test, die Abbildungsspalten CORINE/CLC+/FLAIR/DKM als „eigene Zuordnung, nicht gegen amtliche Tabellen geprüft" — prüfbar: Lesen `kategorien.json` und `KATEGORIEN.md`
AK6: Weg des Nutzers: `README.md` des Repos nennt `kategorien.json` und `KATEGORIEN.md`, und der Aufruf aus AK1 mit dem Python des Stitcher-Venv (Profil, Abschnitt Setup) läuft ohne Fehler durch — prüfbar: Lesen `README.md` und Befehl aus AK1

### Einstieg

- landseg: Das Repo ist leer (nur `.git`, ein Initial-Commit); neu anzulegen sind `kategorien.json`, `KATEGORIEN.md`, `tools/pruefe_kategorien.py` und ein erstes `README.md` (das Profil nennt `README.md` als Pflichtlektüre, sobald vorhanden).
- Inhaltsvorlage (außerhalb des Repos, nur lesen): `wuensche/2026-11-17-landseg-methode/einheiten/e02.md:84-183` — Klassentabelle (95-158), Zählung (160), Grundsätze G1–G5 (86-91), Abweichungen A1–A4 (162-166), Regeln U1–U5 (168-173). Gegenprüfung dazu: `gegenpruefung/e02.md`.
- Formvorlage (nur lesen): `websites/nai/stitcher/kachel_direkt/kategorien.json` — flache Klassenschlüssel mit Farben; hier hierarchisch.

### Bausteine und Fallen

- Inhalt nicht neu erfinden: Codes, Namen und Eltern Eins zu eins aus der Tabelle e02.md 95-158; die Ebene folgt aus dem Code (Punktzahl). Entscheidungen F2/F5 sind schon eingearbeitet (unbefestigte Wege 1.2.3 unter Verkehr, Dauerkulturen 2.4 unter Acker); nichts davon wieder aufmachen.
- Zählfalle: 25 = alle Knoten der Ebene 2 (auch jene ohne Kinder), 46 = alle Blätter über alle Ebenen. Elternklassen sind gültige Labels (G5), daher darf ein Blatt auf Ebene 2 liegen.
- Abbildungsspalten stehen in e02 mit Mehrfachwerten („6/2/3", „1.1.x") und „aus dem Gedächtnis" zugeordnet: als Liste speichern, als ungeprüft markieren (AK5), nichts dazuraten.
- Farben legt der Umsetzer fest (e02 hat keine): eine Farbfamilie je Ebene-1-Klasse, Abstufung in den Kindern, jede der 46 Blattfarben einzeln unterscheidbar (Mindestabstand im Prüfskript); Klasse 0 grau.
- Nur Daten und Text, kein Werkzeugcode (der folgt in K2). Skript nur mit Standardbibliothek; im Stitcher-Venv nichts installieren, keine Bilder oder Gewichte ins Repo. Zitiert er DKM-Mindestflächen: § 4 BANU-V (Gebäude ab 20 m², Streifen ab 4 m, Wald 10 m/1 000 m², übrige 200 m²), nicht „200 m² außer Bauflächen".
- Nacharbeit: Profil `landseg` nachziehen (Pflichtlektüre `KATEGORIEN.md`, Prüfung um das Prüfskript, danach `pruefung: voll`); das macht die Profil-Pflege, nicht der Umsetzer.

### Bauweise

Richtung: ohne Zielbild
Berührt: keine
Tilgt: keine
Flick-Signale: keine — kein Vorgänger (neues Repo, Herkunft ist eine Ermittlung, kein Glied)
Empfehlung: – — Neuanlage im leeren Repo, keine Altlast, kein Anbau.

Reihenfolge der Repos: landseg · Risiken: SW-Spalte und Abbildungsspalten bleiben Vermutung (gekennzeichnet) · Vorbedingungen: keine

## Entwurf

Stufe: nein — keine Oberfläche, nur Daten und Text.
