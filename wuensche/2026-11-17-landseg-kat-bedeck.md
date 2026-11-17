# Kategorienliste der Landschafts-Segmente nach Bedeckung statt Nutzung umbauen: Siedlungsgrün zu Grünland bzw. Gehölz, unbefestigte Wege zu offenem Boden, „im Siedlungsgebiet" als Merkmal je Segment

Kurzname: landseg-kat-bedeck | Datum: 2026-11-17 | Größe: mittel | Bereich: victor | Repos: landseg | Status: eingereiht | Herkunft: Nutzer nach Blick auf die Vorstufe r0c0 (Segment 100061), 2026-11-17

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

Nutzer (17.11.2026), nach Blick auf die Labels der Vorstufe an Teilkachel r0c0: „passt aber nicht so ganz zusammen, findest du nicht?" — es ging um Segment 100061: die große Wiese (108.926 px, 28 % der Teilkachel) ist als 1.4.1 „Rasen / krautiges Siedlungsgrün" eingestuft (SAM-3-Suchwort „lawn", unsicher, Wert 0,56) und erscheint dadurch grob als „1 Versiegelt / bebaut". Antwort auf die Rückfrage: „Nach Bedeckung einordnen".

Präzisierung der Hauptsession:
- Entscheidung „Landschafts-Kategorien: Bedeckung statt Nutzung" in BASIS/wuensche/entscheidungen.md gilt: Rasen und Hausgärten (heute 1.4 Siedlungsgrün mit Unterklassen) kommen nach ihrer Bedeckung zu Grünland bzw. Gehölz (z. B. Rasen zu Dauergrünland, Gartenbäume/-hecken zu Gehölz), unbefestigte Wege (heute 1.2.3) zu offenem Boden; „im Siedlungsgebiet" wird ein Merkmal je Segment, keine Klasse. Ziel: Eine Verwechslung Rasen/Wiese ist nur noch ein feiner Fehler.
- Betroffen sind voraussichtlich `kategorien.json`, `KATEGORIEN.md`, das Prüfskript `tools/pruefe_kategorien.py` (Zählung 7/25/46 ändert sich), die Zuordnungen zu CORINE/CLC+/FLAIR/DKM/Bericht 48 und die Vorstufe (Suchwörter und Abbildung SAM-3-Text → Klasse in `vorstufe.json`, Merkmal im Segment), dazu Tests. Welche Stellen genau, klärt der Prüfer.
- Die grobe Ebene soll weiter auf die Klassen aus Bericht 48 abbildbar bleiben (Bericht im Repo unterlagen, `berichte/48_luftbild_segmentierung_klassen.md`); wie das mit dem Merkmal gelingt, ist zu klären und zu belegen.
- Parallel wird die Prüfseite gebaut (landseg-werkzeuge-5); sie liest Klassen nur aus `kategorien.json`. Der Test landseg-test-t0 startet erst nach diesem Wunsch.

## Fragen

Keine offenen Fragen. Der Nutzer hat entschieden (Bedeckung statt Nutzung); der Rest ist technisch
und steht im Arbeitsauftrag (Gartenbeete zu Acker, Merkmal-Ableitung aus Gebäudenähe, Abbildung auf
Bericht 48 über das Merkmal).

## Entscheidungen

- Landschafts-Kategorien: Bedeckung statt Nutzung: Antwort des Nutzers vom 17.11.2026 nach Blick auf die Vorstufe (Segment 100061: große Wiese als „Rasen / Siedlungsgrün" und damit grob als „Versiegelt / bebaut"): Die Kategorienliste ordnet nach Bedeckung. Rasen und Hausgärten (Siedlungsgrün) kommen zu Grünland bzw. Gehölz, unbefestigte Wege zu offenem Boden; „im Siedlungsgebiet" wird ein eigenes Merkmal je Segment statt einer Klasse. Ersetzt für unbefestigte Wege die Zuordnung „Verkehrsfläche" aus F5 der Grundsätze vom selben Tag. Eine Verwechslung Rasen/Wiese soll nur noch ein feiner Fehler sein, kein grober. Ungeprüft: ob die Abbildung auf Bericht 48 über das Merkmal ausreicht. (aus entscheidungen.md, 2026-11-17)
- Landschafts-Segmentierung: Grundsätze (Auszug, gilt weiter): feine Segmente so fein wie im Bild sicher erkennbar; Kategorien gestuft, grobe Ebene = die sechs Klassen aus Bericht 48 plus „nicht bestimmbar"; Weingärten und Obstanlagen zu Acker; jeder Bildpunkt gehört zu genau einem Segment mit Kategorie (lückenlos). (aus entscheidungen.md, 2026-11-17)
- Push zu GitHub nur auf ausdrückliche Ansage. (aus entscheidungen.md, 2026-11-17)
- 2026-11-17: Landschafts-Kategorien: Bericht 48 nicht bindend: Nutzer am 17.11.2026: „es muss sich jetzt nicht genau an Bericht 48 gehalten werden". Bericht 48 ist Ausgangspunkt und Anregung, keine bindende Vorgabe; die grobe Ebene muss nicht seinen sechs Klassen folgen, eine Abbildung auf Bericht 48 ist erwünscht, wo sie ohne Verbiegen der Liste geht, aber kein Abnahmekriterium. Lockert die Grundsätze vom selben Tag (F2: grobe Ebene = Klassen aus Bericht 48). (aus entscheidungen.md, 2026-11-17)

## Arbeitsauftrag

Gemeint ist die Kategorienliste des Repos `landseg` (Pfad relativ zu `landseg/`). Beschlossen ist die
Richtung (siehe Entscheidungen); die Einzelheiten legt der Umsetzer nach diesen Vorgaben fest.

Vorgaben:
- Siedlungsgrün 1.4 mit 1.4.1, 1.4.2, 1.4.3 entfällt als Klasse. Rasen/krautiges Grün (Garten, Park, Friedhof) zählt zu 3.1 (Wiese/Weide gemeinsam); Gartenbaum, Strauch, Hecke zu 4.2.1 bis 4.2.4; Gartenbeet/Hausgemüse zu Acker (2.1 mit, 2.2 ohne Bewuchs; Bedeckung, nicht Nutzung).
- Unbefestigter Weg 1.2.3 entfällt unter 1; dafür eine neue Klasse unter 6 „Offener Boden" (vorgeschlagen 6.6 „Weg / Fahrspur, unbefestigt (Feld-, Wald-, Schotterweg)", Ebene 2, Blatt, eigene Farbe in der Familie Offener Boden, gleiche Felder wie die übrigen Klassen). Erwartete Zählung danach 7/25/43 (Ebene 1/2 und Blätter; 62 Klassen werden 59); der Umsetzer prüft die Zahl nach und trägt sie in `kategorien.json` (`counts`) ein. Die künstliche Schotterfläche 1.3.1 bleibt unverändert unter 1 (vom Nutzer nicht genannt; im Bericht vermerken).
- Merkmal je Segment `im_siedlung: ja | nein` in `segmente.json` (wie `sicher`). Ableitung in der Vorstufe nach dem Verschmelzen, rein aus der fertigen Karte: ein Segment der Klassen 2, 3 und 4.2 (Ebene 1 Acker, Grünland, Gehölz außerhalb Wald) ist `ja`, wenn es überwiegend (Anteil als Einstellung) innerhalb einer Siedlungszone liegt; Siedlungszone = Gebäude (1.1.x) und befestigte Verkehrs-/Hofflächen (1.2.1, 1.2.2, 1.2.4) um einen Pufferabstand aufgeweitet (Meter und Anteil als Einstellungen in `vorstufe.json`, neuer Abschnitt, mit Hinweisen; Anfangswerte begründen und als „am Test T0 nicht abgestimmt" kennzeichnen). Alle anderen Segmente `nein`. Pufferabstand in Metern, Umrechnung über die Bildpunktgröße der Kachel.
- Abbildung auf Bericht 48: Die grobe Klasse (`grob`, Ebene-1-Vorfahr) bleibt rein nach Bedeckung. Für Auswertungen nach Bericht 48 gilt eine ausdrückliche Regel: Segment der Klassen 2, 3, 4.2 mit `im_siedlung: ja` zählt als „1 Versiegelt / bebaut" (Hausgärten „als Teil der Siedlung führen", Bericht 48 Zeile 37). Als Funktion in `landseg/kategorien.py` (z. B. `bericht48_klasse(klasse, im_siedlung)`) mit der Klassenliste in `kategorien.json` (Feld bei den Regeln), damit die Prüfseite und andere Werkzeuge sie nutzen können, ohne Code zu ändern. In `KATEGORIEN.md` beschreiben, dass dies die Abbildung auf Bericht 48 ist und wo sie nicht ganz trägt (Park und Friedhof ohne nahes Gebäude werden Grünland/Gehölz).
- Die Vorstufe führt Rasen und Gartenbeet nicht mehr als eigene Klasse: `vorstufe.json` Zeile „lawn" geht zu 3.1 (zusammen mit „meadow", „grassland"), Zeile „vegetable garden" zu 2.1, 1.2.3 „dirt path", „dirt road" zu 6.6; Gehölz im Siedlungsbereich hatte keinen eigenen Suchtext (kein neuer).
- `KATEGORIEN.md`, `kategorien.json` (Klassen, `mappings`, Regel G1 mit der Ausnahme „Hausgärten zur Siedlung" ersetzt durch das Merkmal, Abweichung A3 für 1.2.3 gestrichen, Zählung), `tools/pruefe_kategorien.py` und `README.md` stimmen zusammen. Die Zuordnungen zu CORINE, CLC+, FLAIR, DKM sind weiter Vermutung; die neuen Zeilen (6.6) nach demselben Muster, ohne Behauptung von Prüfung.

### Abnahmekriterien

AK1: Die Kategorienliste kennt weder Siedlungsgrün (1.4, 1.4.1 bis 1.4.3) noch unbefestigte Wege unter „Versiegelt / bebaut" (1.2.3); der Weg steht unter Offener Boden, die Zählung stimmt in `kategorien.json`, `KATEGORIEN.md` und README überein, und die Liste prüft sich fehlerfrei — prüfbar: `PY -I tools/pruefe_kategorien.py kategorien.json` (Exit 0, Zählung 7/25/43 oder die vom Umsetzer belegte) und Lesen `KATEGORIEN.md`
AK2: Das Merkmal „im Siedlungsgebiet" steht je Segment als eigenes Feld `im_siedlung`, wird von der Vorstufe gesetzt (Gebäude, befestigte Flächen und ihre Nähe, Einstellungen in `vorstufe.json`) und ist keine Klasse — prüfbar: Test in `tests/test_vorstufe.py` (Wiese neben Haus `ja`, Wiese fern von Gebäuden `nein`, Haus selbst `nein`) und `PY -B -m unittest tests.test_vorstufe`
AK3: Eine Rasenfläche wird von der Vorstufe als Grünland (3.1) eingeordnet, grob „3 Dauergrünland", nicht mehr als Siedlung; Gartenbaum und Hecke als Gehölz, ein Gartenbeet als Acker, ein unbefestigter Weg als Offener Boden — prüfbar: `PY -B -m unittest tests.test_vorstufe` (Abbildung SAM-3-Text zu Klasse und `grob`) und Lesen `vorstufe.json`
AK4: Die grobe Ebene bleibt auf Bericht 48 abbildbar: eine Regel mit dem Merkmal macht aus Grünland, Acker und Gehölz im Siedlungsgebiet wieder „Versiegelt / bebaut" und lässt alles andere bei der Ebene-1-Klasse — prüfbar: Test `tests/test_kategorien.py` (neu) für die Funktion und Lesen `KATEGORIEN.md` (Abschnitt dazu, Grenzen genannt)
AK5: `pruefen`, `eingriff`, `zusammentragen` und `ansicht` laufen mit der neuen Liste durch und behalten das Merkmal beim Ändern der Klasse (Klassenwechsel zählt nicht als Merkmalwechsel); Segmente mit einem alten Code (1.4.x, 1.2.3) melden `pruefen` als ungültige Klasse — prüfbar: ganze Suite `PY -B -m unittest discover -s tests -t .` (Testfall alter Code in `tests/test_pruefen.py`)
AK6: Weg des Nutzers: Teilkachel r0c0 neu durch die Vorstufe (Segment 100061, die große Wiese) — die Wiese trägt jetzt Klasse 3.1 und grob „3", nicht mehr „1", und `PY -B -m landseg pruefen` ist sauber — prüfbar: `PY -B -m landseg vorstufe --manifest <manifest.json> --teilkachel r0c0` (GPU, rund 1 Minute; vorher `maschine.py belegen --maschine gpu`, danach freigeben), dann `PY -B -m landseg pruefen` und Ansicht der Segmente (Wiese hellgrün)

Nacharbeit: Profil `BASIS/.claude/repos/landseg.md` (Zählung „7/25/46", Prüfzeile, Pflichtlektüre) und, falls dort geführt, Nacharbeit-Hinweis an `landseg-werkzeuge-5` (liest Klassen nur aus `kategorien.json`) und `landseg-test-t0` (neuer Stand der Klassen) nachziehen.

### Einstieg

- landseg: `kategorien.json:496-600` — Klassen 1.4, 1.4.1, 1.4.2, 1.4.3 mit `mappings`; entfallen (Zählung in `counts`, Zeilen 12-13: `level_2`, `leaves`)
- landseg: `kategorien.json:294` — Klasse 1.2.3 „Weg, unbefestigt" (`deviation: A3`, Zeile 315); entfällt, neue Klasse 6.6 im Block der Klassen unter 6
- landseg: `kategorien.json:1643` — Regel G1 mit Ausnahme „Hausgärten/Siedlungsgrün zur Siedlung"; Wortlaut ändern auf Merkmal `im_siedlung`; `kategorien.json:1744` — Abweichung A3 (nur 1.3.1 bleibt) und Hinweis zur Abbildung auf Bericht 48
- landseg: `KATEGORIEN.md:46-110` (Tabelle), `:116` (G1), `:144` (A3), `:24` und `:42` (Zählung 62) — anpassen
- landseg: `tools/pruefe_kategorien.py:87-112` (Zählung je Ebene), `:170` (Ausgabe) — Zähler lesen die Liste, prüfen, dass die Zählung stimmt; Erwartung 7/25/43
- landseg: `vorstufe.json:47-78` — Suchwort-Zeilen: 1.2.3 (Zeile 53), 1.4.1 (60), 1.4.2 (61) umlenken; Abschnitt für die Siedlungszone neu
- landseg: `landseg/vorstufe.py:215` (`verschmelzen`), `:299`, `:309` — Segmenteinträge werden hier aufgebaut (`klasse`, `grob`, `sicher`); Merkmal `im_siedlung` nach dem Verschmelzen aus der fertigen Karte ableiten und je Eintrag setzen; `konfig_laden` (Zeile 66) prüft den neuen Abschnitt
- landseg: `landseg/kategorien.py:26` — `grob()` Ebene-1-Vorfahr; daneben Funktion `bericht48_klasse`
- landseg: `landseg/pruefen.py:155` — prüft `grob` gegen die Klasse; ergänzen: `im_siedlung` ist `ja`, `nein` oder fehlt; alter Code als ungültige Klasse (bleibt wie heute)
- landseg: `landseg/eingriff.py:266`, `:290`, `:119` — Klassenwechsel setzt `klasse` und `grob`; `im_siedlung` darf dabei nicht verloren gehen (`_abgeleitet` kopiert Eintrag)
- landseg: `landseg/zusammentragen.py:260` — Klassenübernahme des Nutzers; Merkmal erhalten
- landseg: `tests/hilfe.py:14`, `tests/test_vorstufe.py:29-108` — Testklassen und Vorstufe-Test; Fälle für Merkmal und neue Abbildung; neu `tests/test_kategorien.py`
- landseg: `README.md:46`, `:245` — Beschreibung `sicher` (daneben `im_siedlung`) und Zählung

### Bausteine und Fallen

- Muster für ein Merkmal je Segment: `sicher: ja | nein` (`vorstufe.py:300`, `README.md:46`, `pruefen.py`, `ansicht.py:176`); `im_siedlung` genauso führen, nicht als zweite Klassenebene.
- Einstellungen aus `vorstufe.json` lesen (Hinweis-Schlüssel mit `_`), nichts fest verdrahten (`konfig_laden`).
- Falle Zwischenspeicher: `sam3_roh.npz` hängt am Fingerabdruck von `sam3` und `prompts` (`vorstufe.py:92-99`). Ändern sich Klassen-Codes in `prompts`, ist der Abdruck ein anderer: `--neu` greift nicht, die Teilkachel braucht einen GPU-Lauf (AK6). Die Siedlungszone gehört nicht in `prompts` und nicht in `sam3_teil`, sonst rechnet jede Einstellungsänderung SAM 3 neu. Pufferabstand nur im Abschnitt außerhalb.
- Falle Doppelzählung: nach dem Streichen von 1.4 und 1.2.3 hat keine bestehende Datei diese Codes mehr (die Vorstufe-Ausgabe unter `BASIS/daten/landseg/` nicht von Hand ändern, sondern neu rechnen; `daten/luftbilder/` nie anfassen).
- Falle SW-Spalte `bw` und `mappings`: ungeprüft (Profil „Nicht anfassen"); für 6.6 nach Muster, nicht als gesichert.
- Falle Farbabstand: neue Farbe muss zu allen anderen Mindestabstand halten; das Prüfskript meldet es.
- Falle Parallelwunsch: `landseg-werkzeuge-5` liest Klassen aus `kategorien.json`; Feldnamen und Codes dort nicht umbenennen außer den genannten; `landseg-test-t0` startet erst nach diesem Wunsch.
- Merkmalableitung ohne neue Pakete: das Stitcher-venv hat SciPy 1.18 und OpenCV 4.13 (Puffer über `scipy.ndimage`/`cv2.dilate` auf der Karte, kein Schleife über Bildpunkte).
- Nicht gelöst und im Bericht zu nennen: Park oder Friedhof ohne Gebäude in der Nähe zählt nach Bericht 48 nicht zur Siedlung (Grünland/Gehölz); die Stelle ist ein Kandidat für T0.

### Bauweise

Richtung: ohne Zielbild
Berührt: keine
Tilgt: keine
Flick-Signale: keine — kein Vorgänger (Herkunft ist der Nutzer; `landseg-werkzeuge-*` und `landseg-test-t0` sind Geschwister mit anderer Stelle und anderem Ziel, `landseg-methode` ist die Ermittlung davor)
Anbau: Merkmal und Klassenumstellung in den bestehenden Dateien nachziehen — Dauer kurz — Risiko gering, die Liste ist die Quelle der Wahrheit und das Prüfskript fängt Brüche — danach bleibt eine ausdrückliche Regel zu Bericht 48
Belege: –
Empfehlung: – — kein Umbau nötig, `grob` und Prüfwerkzeuge bleiben unverändert.

Reihenfolge der Repos: landseg · Risiken: Klassenumstellung ändert die Bedeutung von `grob` für die Vorstufe (alte Ausgaben ungültig), GPU-Lauf für AK6 · Vorbedingungen: keine

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

Stufe: nein — keine neue Oberfläche, nur Klassenliste, Merkmal und Zuordnung; die Prüfseite ist ein eigener Wunsch (landseg-werkzeuge-5).
