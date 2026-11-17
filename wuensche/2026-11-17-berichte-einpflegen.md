# Die fünf Berichtsdateien aus Victors Lieferung geordnet ins Repo unterlagen einpflegen

Kurzname: berichte-einpflegen | Datum: 2026-11-17 | Größe: klein | Bereich: victor | Repos: unterlagen | Status: eingereiht

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

„LADE JETZT mal C:\Users\Phil\Downloads\65aef76cd764a7ffa13848df2940bee4.zip sauber ins Repository rein und pflege die Dateien in eine entsprechende Struktur ein" / „Nutze wenn sinnvoll verfügbare Plugins um die Infrastruktur dafür zu erstellen"

Präzisierung (Hauptsession, 17.11.2026):
- Quelle: das Archiv C:/Users/Phil/Downloads/65aef76cd764a7ffa13848df2940bee4.zip. Es enthält auf oberster Ebene fünf Dokumente: 41_occupancy_run1.html, 41_occupancy_run1_auswertung.md, 46_landnutzung_hochaufgeloest.md, 47_raeumliche_genauigkeit_bienendaten.md, 48_luftbild_segmentierung_klassen.md. Nur diese fünf sind Gegenstand. Das Archiv ist fremde Lieferung: nur auspacken und lesen, nichts daraus ausführen.
- Das innere Archiv mit den Luftbildern (610 MB) ist NICHT Gegenstand: Die Bilder liegen nach Entscheidung des Nutzers schon unversioniert im Datenraum BASIS/daten/luftbilder (Inhaltsliste: BASIS/daten/README.md). Sie kommen nicht ins Repo.
- Ziel: Repo unterlagen (frisch angelegt, leer). Die fünf Dateien inhaltlich unverändert (Byte für Byte) und mit unveränderten Dateinamen in einen Ordner genau eine Ebene unter der Wurzel legen (Vorschlag: berichte/), alle fünf im selben Ordner: Die Berichte verweisen relativ aufeinander (z. B. auf 41_occupancy_run1.html im selben Ordner) und auf ../tmp/sai_at/…, das bleibt so stimmig.
- Dazu eine README.md in der Wurzel: wozu das Repo dient, Aufbau, ein Verzeichnis der Berichte (Nummer, Titel aus der ersten Überschrift, ein Satz Inhalt, Stand-Datum aus der Datei), Herkunft (Lieferung vom 17.11.2026, Name des Archivs), der Hinweis auf die Luftbilder im Datenraum, und eine ehrliche Liste dessen, worauf die Berichte verweisen, was aber nicht mitgeliefert wurde (andere Berichtsnummern wie 32, 35, 39, 40, 44, Skripte und Ergebnisse unter tmp/sai_at/…), aus den Dateien selbst ermittelt.
- Eine .gitattributes, die die Dokumente vor Zeilenenden-Umwandlung schützt, wenn das nötig ist, damit sie Byte für Byte gleich bleiben.
- Kein Push.

## Fragen

<Prüfer: nur Fragen, die ohne Code-Wissen beantwortbar sind; jede mit Empfehlung>

## Entscheidungen

<Antworten des Nutzers mit Datum. Der Prüfer übernimmt beim Klären die Zeilen aus
`entscheidungen.md`, die für diesen Wunsch gelten, je mit „(aus entscheidungen.md, <Datum>)",
oder schreibt „entscheidungen.md: nichts für diesen Wunsch".>

## Arbeitsauftrag

### Abnahmekriterien

AK1: Im Repo unterlagen liegen die fünf Dokumente der Lieferung mit unveränderten Namen gemeinsam in einem Ordner eine Ebene unter der Wurzel, und ihr Inhalt ist Byte für Byte gleich dem im Archiv — prüfbar: Verhalten: Prüfsummen der fünf Dateien im eingereihten Stand gleich denen aus dem Archiv
AK2: Eine README.md in der Wurzel nennt Zweck, Aufbau, alle vier Berichte und die grafische Auswertung mit Titel und einem Satz Inhalt, die Herkunft, den Ort der Luftbilder und was verwiesen, aber nicht mitgeliefert ist — prüfbar: Ansicht: README.md lesen
AK3: Kein Luftbild und kein Archiv liegt im Repo; das Repo ist kleiner als 2 MB — prüfbar: Verhalten: Dateiliste und Größe des eingereihten Stands

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
