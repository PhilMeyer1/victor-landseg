# Werkzeuge für den ersten Test der lückenlosen Landschafts-Segmentierung bauen (W1–W8 und Vorlagen W10, ohne Export W9), abgenommen an einer Teilkachel des Testfensters T0

Kurzname: landseg-werkzeuge | Datum: 2026-11-17 | Größe: gross | Bereich: victor | Repos: landseg | Status: eingereiht | Herkunft: Ermittlung landseg-methode K2

## Wunsch

K2: Werkzeugkasten W1–W10 bauen (kacheln, vorstufe mit Superpixel + SAM 3 + Semantik-argmax als Nachbau aus dem Paper, ansicht, kante, eingriff, pruefen, zusammentragen, seite, export mit Lizenz- und Herkunftsfeld je Kachel, Auftragsvorlagen + Agent-Skill) — Gewinn wiederverwendbar, Lückenlosigkeit per Konstruktion, kein Einmal-Code — Aufwand gross — Risiko mittel (Nahtregel unerprobt) — Repo offen (Frage F4) — empfohlen

Belege: wuensche/2026-11-17-landseg-methode/bericht.md, K2.

Empfehlung der Deutung (wuensche/2026-11-17-landseg-methode.md, Abschnitt Empfehlung):
- K2: trägt — ohne die Werkzeuge gibt es keinen Test: lückenlose Vorstufe, Eingriffe auf der Label-Karte und die Prüfung „H × W, kein 0" machen die Lückenlosigkeit erst prüfbar. Gefragt ist aber der Test, nicht der ganze Kasten.
- Nächster Schritt: K2 als Folge-Wunsch (nachdem Sie F4 zum Ort entschieden haben), zugeschnitten auf den Test T0: Werkzeuge W1–W8 und die Vorlagen W10, `kategorien.json` aus K1 mitnehmen, den Export W9 erst nach dem Test. Abgenommen wird an einer Teilkachel von T0: Die Vorstufe läuft, `pruefen` meldet H × W ohne 0, und die Zahl der Segmente je Teilkachel ist gemessen. — Danach kann K3 sofort laufen, und die unsicherste Annahme ist schon geprüft, bevor der erste Agent urteilt.
- Gegenargument: Am Bild ist bisher nichts erprobt. Im Stitcher urteilte ein Agent über genau ein Segment (4–8 min); in T0 kämen auf eine Teilkachel von 500 px 40–60 Segmente (nur vermutet, `bericht.md` 3.6). Die Vorstufe erreicht auf ähnlichen Bildern nur 43–60 % mIoU und ist gerade bei Hecken, Wegen und Kleinobjekten schwach (`e03.md` L6/B3), also genau bei der Feinheit, die Sie wollen. Ein großer Werkzeugkasten könnte deshalb um eine Einheitengröße herum gebaut werden, die nicht trägt. — Der Schritt gilt trotzdem: Die Größe der Teilkacheln ist ein Parameter in W1 (auf 250 px verkleinerbar) und kein Umbau, und die Abnahme an einer echten T0-Teilkachel misst die Dichte, bevor K3 Agent-Läufe kostet.

## Fragen

### F1: Soll die Prüfseite vor dem Bau als Entwurf gezeichnet werden?
- Lage: Die Prüfseite ist die Webseite (eine Datei, die Sie im Browser öffnen), auf der Sie später die Segmente eines Bildausschnitts ansehen, zwischen grober und feiner Einteilung umschalten, Lücken und Nähte sehen und Kommentare ausgeben können. Es gibt sie noch nicht in diesem Repo; im Stitcher gibt es eine ähnliche Seite als Vorbild.
- Empfohlen: Skizze — eine Ansicht in einem Zustand (Aufbau, Beschriftung, Desktop) genügt, weil das Vorbild im Stitcher den Rest vorgibt und die Seite nur für Sie und den Test gebaut wird.
- Kein Entwurf — der Umsetzer baut die Seite nach dem Vorbild; Sie sehen sie erstmals fertig und bessern danach nach.
- Ausgearbeitet — mehrere Ansichten und Zustände (leer, gefüllt, Fehler) vorab; mehr Aufwand, weniger Nachbessern.

## Entscheidungen

- 2026-11-17, Landschafts-Segmentierung: Grundsätze: Aus der Ermittlung landseg-methode (Fragen F1–F7), Antworten des Nutzers vom 17.11.2026: (F4) Die Werkzeuge entstehen in einem eigenen Repo landseg im Ordner Victor; der Stitcher bleibt unberührt, brauchbare Teile werden übernommen und angepasst. (F1) Segmente so fein, wie im Bild sicher erkennbar (Einzelbaum, schmaler Weg, kleines Gebäude); die Mindestgröße aus Bericht 48 ist nur eine gröbere Auswertungsebene. (F2, F5) Kategorien allgemein und gestuft (7/25/46), grobe Ebene = die sechs Klassen aus Bericht 48 plus „nicht bestimmbar", feine Ebene enthält die Bienenklassen; unbefestigte Wege zählen zur Verkehrsfläche, Weingärten und Obstanlagen zu Acker. Jeder Bildpunkt gehört zu genau einem Segment mit Kategorie (lückenlos). Vorläufig wie empfohlen angenommen, vom Nutzer nicht widersprochen: (F3) Beschriften auf dem Farbbild, fürs Training zusätzlich eine Schwarz-Weiß-Fassung mit denselben Segmenten; (F6) offene Zusatzdaten (Höhenmodell, Feldstücke, Gebäude) im ersten Test nicht; (F7) mehrere Jahrgänge erst nach den Tests, dann kostenfrei über den Seewinkel, kein Kauf ohne Freigabe. Reihenfolge: Kategorienliste und Werkzeuge, dann Test am Orthofoto-Ausschnitt T0; der Test am Scan von 1968 wird danach eigens angeboten. (aus entscheidungen.md, 2026-11-17)
- 2026-11-17, Push zu GitHub: Nur auf ausdrückliche Ansage, nie automatisch nach einem Wunsch. (aus entscheidungen.md, 2026-11-17)
- 2026-11-17, F1 (Nutzer): Skizze vorab. Die Prüfseite wird vor dem Bau als Entwurf (Stufe skizze) gezeichnet und freigegeben; der Entwurf betrifft nur Teil 5, die Teile 1 bis 4 hängen nicht daran.
- 2026-11-17: Landschafts-Kategorien: Bedeckung statt Nutzung: Antwort des Nutzers vom 17.11.2026 nach Blick auf die Vorstufe (Segment 100061: große Wiese als „Rasen / Siedlungsgrün" und damit grob als „Versiegelt / bebaut"): Die Kategorienliste ordnet nach Bedeckung. Rasen und Hausgärten (Siedlungsgrün) kommen zu Grünland bzw. Gehölz, unbefestigte Wege zu offenem Boden; „im Siedlungsgebiet" wird ein eigenes Merkmal je Segment statt einer Klasse. Ersetzt für unbefestigte Wege die Zuordnung „Verkehrsfläche" aus F5 der Grundsätze vom selben Tag. Eine Verwechslung Rasen/Wiese soll nur noch ein feiner Fehler sein, kein grober. Ungeprüft: ob die Abbildung auf Bericht 48 über das Merkmal ausreicht. (aus entscheidungen.md, 2026-11-17)
- 2026-11-17, Entwurf freigegeben: wuensche/2026-11-17-landseg-werkzeuge/entwurf/c/ (Runde 1, Entwurf 3 „Vorher und Nachher nebeneinander"). Gilt für Teil 5 (Prüfseite). Die Prüfseite liest Klassen, Namen und Farben nur aus `kategorien.json` (keine fest eingebauten Klassen), weil die Kategorienliste gerade nach Bedeckung umgebaut wird (Wunsch landseg-kat-bedeckung). Vorbild für das Anzeigen der Labels (Maus-über-Bild: Segment, Kategorie auf allen drei Ebenen, sicher ja/nein; Klick: alle Felder aus `segmente.json`; Liste der Kategorien mit Segmentzahl und Flächenanteil): die schnelle Ansicht der Hauptsession, `C:/Users/Phil/AppData/Local/Temp/claude/27e54e3b8399faf6/a2bf01d3-627c-4b06-8b57-51f25ab5229e/scratchpad/sicht/vorlage.html` (nur lesen). Der Nutzer will die Segment-Labels jedes Bildpunkts einsehen können.
- 2026-11-17: Landschafts-Kategorien: Bericht 48 nicht bindend: Nutzer am 17.11.2026: „es muss sich jetzt nicht genau an Bericht 48 gehalten werden". Bericht 48 ist Ausgangspunkt und Anregung, keine bindende Vorgabe; die grobe Ebene muss nicht seinen sechs Klassen folgen, eine Abbildung auf Bericht 48 ist erwünscht, wo sie ohne Verbiegen der Liste geht, aber kein Abnahmekriterium. Lockert die Grundsätze vom selben Tag (F2: grobe Ebene = Klassen aus Bericht 48). (aus entscheidungen.md, 2026-11-17)
- 2026-11-17: Landschafts-Segmente: drei Fassungen als Übersicht für Victor, Ergebnis ohne Vorher/Nachher: Nutzer am 17.11.2026 zur Prüfseite und zur freien Version: „Es soll nur eine Version geben mit allen Stufen und Klassifikationen" und „erstelle dafür 2 zusätzliche Versionen. Das soll jetzt alles nur als Übersicht für Victor dienen, der sich dann raussuchen kann, was er am besten findet. Eine Version der Ergebnisse ohne Vorher nachher". Daraus: (1) Die Seite zeigt je Bild genau einen Stand, das Ergebnis, mit allen drei Ebenen (grob/mittel/fein) und der Klassifikation jedes Segments; kein Vorher/Nachher, keine zwei Bilder nebeneinander. (2) Neben der Fassung mit der festen Kategorienliste entstehen zwei zusätzliche, freie Fassungen desselben Testfensters. Auslegung der Hauptsession, vom Nutzer nicht bestätigt: Fassung B „Kategorien frei" (Agents benennen und stufen Flächen selbst, Arbeitsregeln wie in A), Fassung C „alles frei" (eigene Kategorien und eigene Arbeitsweise ohne feste Regeln, wie das freie Urteil der Stitcher-Session). Lückenlos (jeder Bildpunkt genau ein Segment) gilt für alle drei. (3) Zweck ist eine Übersicht für Victor zum Auswählen; die Seite muss zwischen den drei Fassungen umschalten können. (aus entscheidungen.md, 2026-11-17)
- 2026-11-17: Landschafts-Segmente: Urteil im Verbund je Viertel statt Einzelbild je Segment: Nutzer am 17.11.2026: „die Segmente sollen schon im Verbund von den Agents untersucht werden. Sonst hat der ja gar keinen Kontext was drumherum liegt. Also die Ausschnitte sollen z.B. dann nochmal in 4 unterteilt werden, von denen sich dann jeder Agent jedes Segment darin anschaut, also nach einer Liste abarbeitet und die Ergebnisse dann entsprechend einträgt. Einzelne Segmente machen so in der Form als eigene Bilder, die einzeln untersucht werden, keinen Sinn." Daraus: Der Kern jeder Teilkachel wird in vier Viertel geteilt (bei Kern 500: 250 × 250 px, mit Kontextrand); je Viertel ein Agent, der das Viertel als zusammenhängendes Bild mit Umgebung sieht (Segmentgrenzen und Nummern eingezeichnet, Nahansichten des Viertels erlaubt) und alle Segmente des Viertels nach einer Liste abarbeitet und je Segment einträgt. Keine isolierten Einzelbilder je Segment als Grundlage des Urteils. Ein Segment über einer Viertelgrenze gehört dem Viertel mit dem größten Flächenanteil und ist im Nachbarviertel als Kontext sichtbar. Ersetzt die Gruppen à 20–30 Segmente aus F3 von landseg-test-t0 (Gruppe = räumliches Viertel); weiterhin wird jedes Segment einzeln eingetragen und belegt. (aus entscheidungen.md, 2026-11-17)

## Arbeitsauftrag

### Abnahmekriterien

AK1: Aus dem Testfenster T0 (Kachel 5236-56, x 2000, y 2400, 1000 × 1000 px) entstehen vier Teilkacheln (Kern 500 × 500, Kontextrand 64 px) mit einem Manifest (relative Pfade, Georeferenz); die Kerngröße ist ein Parameter (250 funktioniert ebenso) — prüfbar: Befehl `kacheln` auf T0 mit 500 und mit 250, Manifest lesen, Kerne ergeben zusammen genau 1000 × 1000
AK2: Alle Eingriffe (verschmelzen, teilen entlang Linie, Grenze verschieben, Klasse setzen, Polygon zuweisen) arbeiten auf der Label-Karte und lassen sie lückenlos; `pruefen` meldet H × W ohne 0, Zusammenhang je ID, gültige Klassen aus `kategorien.json` und schlägt bei einer absichtlich eingefügten Lücke fehl — prüfbar: Tests mit synthetischer Label-Karte, auch Gegenprobe
AK3: Die Vorstufe (Übersegmentierung, SAM 3 mit Text je Kategorie, Semantik-argmax) läuft auf einer echten T0-Teilkachel und liefert `labels`, `segmente.json` (ID, Klasse fein/grob, Herkunft, Sicherheit) und Kandidatenliste; `pruefen` meldet H × W ohne 0; die Zahl der Segmente und der Anteil `sicher: nein` dieser Teilkachel stehen im Bericht — prüfbar: Befehl `vorstufe` und `pruefen` an der Teilkachel (ein Lauf, kurz), Lesen der Messzeile im Bericht
AK4: `ansicht` erzeugt je Teilkachel und Segment die Standardbilder (roh, Umriss, Mängel, Vorschlag, nah, kontrastverstärkt, Koordinatengitter); `kante` rastet Grenzen im engen Band ein und meldet geschätzte Strecken, statt zu raten — prüfbar: Befehl an der T0-Teilkachel, Lesen der Bilder und der Meldung
AK5: `zusammentragen` fügt Teilkacheln zur Bild-Label-Karte; die Nahtregel (gleiche ID oder echte Bildkante, gleiche Klasse an jeder Kerngrenze) meldet Verstöße; Einheiten, Nutzerklassen und Fragen kommen aus JSON, nicht aus Code — prüfbar: Test mit zwei Teilkacheln, einmal sauber, einmal mit absichtlicher Naht-Verletzung
AK6: Die Prüfseite öffnet sich als Datei im Browser und zeigt Ebenen grob/fein, Lückenkarte, Naht-Ebene, Vorher/Nachher und Kommentar-Export (nach F1) — prüfbar: Ansicht Prüfseite an der T0-Teilkachel, Desktop, wie Entwurf
AK7: Auftragsvorlagen für Urteil, Umsetzen, Korrektur und Naht liegen als Dateien mit Platzhaltern vor (keine absoluten Pfade, kein Einzelfall-Text), dazu ein Agent-Skill mit den Regeln — prüfbar: Lesen der Vorlagen und des Skills
AK8: Der Weg des Nutzers: Nach der Anleitung in der `README.md` führt eine Befehlsfolge (kacheln, vorstufe, pruefen, seite) an einer T0-Teilkachel bis zur geöffneten Prüfseite; abgeleitete Daten liegen unter `BASIS/daten/landseg/`, nichts im Repo außer Code, Vorlagen, Tests, `README.md`; Originale und Stitcher unverändert — prüfbar: Befehlsfolge am laufenden Stand, `git status` in landseg und stitcher, Lesen `README.md`

### Einstieg

- landseg: Repo leer (ein Commit „chore: init repository"); alles ist Neuanlage: Paket mit einem Befehl je Werkzeug W1–W8, Tests, `README.md`, `vorlagen/`, Agent-Skill.
- landseg: `BASIS/wuensche/2026-11-17-landseg-methode/bericht.md:323-371` — Ablauf der Vorstufe (a–e), Urteil, Umsetzung, Naht, Prüfseite, Messung.
- landseg: `BASIS/wuensche/2026-11-17-landseg-methode/einheiten/e05.md:116-125` — Tabelle W1–W10 mit den Stitcher-Mängeln, die nicht übernommen werden (feste Pfade, fest verdrahtete Klassen und Einheiten, Einzelfall-Skripte).
- stitcher (nur lesen): `scripts/sam3_pipeline/sam3_model.py`, `scripts/sam3_pipeline/sam3_segmentation.py` — SAM-3-Laden und Schiebefenster, Vorlage für `vorstufe`; `scripts/seg_datensatz/` (`bearbeiten.py`, `export.py`, `kandidaten.py`, `ansicht/`) — Vorlage für `eingriff`, Kandidaten, Ansicht und Seite; übernehmen heißt kopieren und anpassen, nie dort ändern.

### Bausteine und Fallen

- Bildbibliotheken (numpy, OpenCV, Pillow, scipy) und SAM 3 liegen im venv des Stitchers (`websites/nai/stitcher/.venv`): nur benutzen, nichts installieren; braucht landseg weitere Pakete, bekommt es ein eigenes `.venv`. Modellgewichte nie ins Repo.
- Lückenlosigkeit per Konstruktion: Eingriffe schreiben nur auf die Label-Karte (Segment-ID je Bildpunkt, uint32), nie auf Einzelmasken; `pruefen` ist der Wächter nach jedem Schritt.
- Kategorien, Einheiten, Nutzerklassen, Fragen aus JSON laden (`kategorien.json` aus K1, `landseg-kategorien`); der Stitcher hat sie fest verdrahtet (`ERWARTET`, `NUTZER_KLASSE`, `PANEL_ID`): nicht nachbauen.
- Die Vorstufe soll auf Teilkacheln parallel zu fahren sein (seriell nur die GPU-Schritte); die Teilkachel-Größe nie fest einbauen. Der Wert „40–60 Segmente je 500-px-Teilkachel" ist nur vermutet: die Abnahme misst ihn und schreibt ihn auf, auch wenn er schlecht ausfällt.
- SAM 3 braucht die GPU dieses Rechners; wenn sie belegt ist, Befehl wiederholen statt auf CPU auszuweichen.
- Export W9 und Scan 1968 (H0) sind nicht Teil dieses Wunsches.
- Tests anlegen und den Abschnitt „Testreihen" ins Profil melden (Profil steht noch auf `pruefung: leicht`).
- Nacharbeit: Profil `landseg` auf `pruefung: voll` umstellen, Lagebild anlegen, sobald Tests da sind (Profil-Pflege).

### Bauweise

Richtung: ohne Zielbild
Berührt: keine — Repo ist leer, keine `altlasten.md`
Tilgt: keine
Flick-Signale: keine — kein Vorgänger (Herkunft ist die Ermittlung `landseg-methode`, keine Kette von Wünschen)
Anbau: –
Umbau: –
Belege: –
Empfehlung: – — Neuanlage; Stitcher-Code wird als Vorlage übernommen, nicht angebaut. Repo ohne Zielbild: Maßstab ist ein sauberer Aufbau (ein Modul je Werkzeug, Einstellungen aus JSON).

Reihenfolge der Repos: landseg · Risiken: Nahtregel unerprobt, Segmentdichte je Teilkachel und Güte der Vorstufe ungeprüft (43–60 % mIoU), GPU-Verfügbarkeit · Vorbedingungen: keine
Nacharbeit: Wunsch `landseg-kategorien` (K1) muss eingereiht sein, bevor Teil 2 (Vorstufe) und Teil 4 gebaut werden, weil beide `kategorien.json` lesen; Teil 1 testet mit einer kleinen Beispielliste.

## Teile

1. Gerüst, kacheln, eingriff, pruefen — Umsetzer — Repo: landseg — Vorbedingungen: keine — nach: – — AK 1, 2 — Repo mit Paket, Tests und `README.md` steht; T0 lässt sich kacheln, Eingriffe und Prüfung arbeiten lückenlos
2. Vorstufe — Umsetzer — Repo: landseg — Vorbedingungen: keine — Aufruf-Budget: 100 — nach: 1 — AK 3 — Übersegmentierung, SAM 3 und Semantik-argmax liefern an einer echten T0-Teilkachel eine lückenlose Vorbelegung; Segmentzahl ist gemessen
3. ansicht und kante — Umsetzer — Repo: landseg — Vorbedingungen: keine — nach: 1 — AK 4 — Standardbilder und Kanten-Einrasten mit „geschätzt"-Meldung
4. zusammentragen, Nahtregel und Vorlagen — Umsetzer — Repo: landseg — Vorbedingungen: keine — nach: 1 — AK 5, 7 — Teilkacheln werden zur Bild-Label-Karte, Nähte geprüft; Auftragsvorlagen und Agent-Skill liegen vor
5. Prüfseite und Abnahme an T0-Teilkachel — Umsetzer — Repo: landseg — Vorbedingungen: keine — Halt: Durchsicht — nach: 2, 3, 4 — AK 6, 8 — Prüfseite steht und die ganze Befehlsfolge läuft an einer echten Teilkachel; Sie sehen die Seite vor dem Einreihen durch

## Entwurf

Stufe: nach F1

- Prüfseite: Zustände gefüllt (Segmente, Ebenen grob/fein), Lückenkarte, Naht-Ebene, Vorher/Nachher; Desktop. Nachbar zum Nachbilden: Prüfseite aus dem Stitcher (`scripts/seg_datensatz/ansicht/`). Beispieldaten: T0-Teilkachel.
