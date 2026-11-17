# Verfahren finden, mit dem Claude Code Luftbilder europäischer Landschaft vollständig und lückenlos in fein gegliederte Segmente mit Kategorien zerlegt (Trainingsmaterial für ein generisches Landschafts-Segmentiermodell)

Kurzname: landseg-methode | Datum: 2026-11-17 | Bereich: victor | Art: recherche | Stufe: M | Eingriff: keiner | Repos: unterlagen | Status: ermittelt
Vergleich mit: –

<Eine Ermittlung will wissen, nicht ändern. Stufe S: ein Prüfer sieht kurz nach und schreibt
Befund, Abdeckung und Kandidaten; M und L: Plan, Einheiten, Gegenprüfung und Bericht. Alles
liegt im Ordner mit demselben Namen ohne `.md` daneben.>

## Wunsch

Wortlaut des Nutzers (17.11.2026): „Ok, das Ziel ist es jetzt nämlich Segmentationsdatensätze nicht von Insekten sondern von Landschaftsbildern zu erstellen. Also die Landschaftsbilder jetzt zu segmentieren um dann Trainingsmaterial für ein generisches Landschaftssegmentationsmodell zu erhalten mit dem man dann (erst mal nach ausgewählten Regionen) unabhängig von Jahr, Qualität, Auflösung, etc. Landschaftsbilder so fein wie möglich und so detailliert wie möglich segmentieren zu können. Lass uns das jetzt erst mal für den europäischen Raum anschauen. Dafür möchte ich jetzt mal das im Repo hinterlegte Landschaftsbild nutzen und ähnlich wie auch bei der Insektenklassifikation dich jetzt das Landschaftsbild so fein wie möglich segmentieren und die Segmente in entsprechende Kategorien aufteilen. Das soll jetzt erst mal ein Test werden. Ich möchte, dass du dir jetzt Methoden und nützliche Schritte von der Stitcher Session für das Segmentieren der Objekte abschaust und dann einen ganzheitlichen Vorschlag machst wie man jetzt am besten die Landschaftsbilder mit Claude Code vollständig und lückenlos segmentieren könnte. So, dass wirklich jeder Bereich auf einem Landschaftsbild abgedeckt ist. Starte Recherchen, Ermittlungen und halte dich ca. an die Vorgehensweisen aus der Stitcher Session (dort hat das sehr gut funktioniert) um jetzt eine geeignete Methode auf die Landschaftsbilder zu übertragen"

Präzisierung der Hauptsession:

ZIEL DES ERGEBNISSES: ein ganzheitlicher, begründeter Vorschlag (noch keine Segmentierung, kein Bau), wie ein erster Test an den vorhandenen Luftbildern ablaufen soll und wie das Verfahren danach auf viele Bilder wächst. Der Nutzer entscheidet danach; der Test selbst wird ein eigener Bau-Wunsch.

HARTE ANFORDERUNGEN AN DAS VERFAHREN (vom Nutzer):
- vollständig und lückenlos: jeder Bildpunkt gehört zu genau einem Segment mit Kategorie (anders als bei den Insekten, wo der weiße Untergrund frei blieb);
- so fein und detailliert wie möglich (einzelne Felder, Bäume/Baumgruppen, Hecken, Wege, Gebäude, Gewässer, Kleinstrukturen …);
- Zielmodell später unabhängig von Jahr, Bildqualität, Auflösung (Farbe und Schwarz-Weiß, aktuelle Orthofotos und historische Scans); zuerst Europa, zuerst ausgewählte Regionen;
- die Arbeit macht Claude Code (Agents, die Bilder ansehen, urteilen, Masken per Skript erzeugen und korrigieren), wie in der Stitcher-Session; der Nutzer prüft und kommentiert auf einer Seite.

VORHANDENES MATERIAL (nur lesen, nichts ändern):
- Luftbilder: C:/Users/Phil/Developement/Victor/daten/luftbilder/ (Inhaltsliste C:/Users/Phil/Developement/Victor/daten/README.md): orthofoto-aktuell/ zwei GeoTIFF-Kacheln 5236-55 und 5236-56 je 94 MB, 0,2 m je Bildpunkt, EPSG:31255 (MGI Austria GK Central), mit .TFW/.PRJ; historisch/ zwei Scans 1957004_004A_1557.tif (166 MB) und 1968105_0014_0228.tif (257 MB) ohne Lagebezug. Zu klären: Bildgröße, Kanäle, Bittiefe, was zu sehen ist (Landschaftstyp, Ort), ob die historischen Bilder dasselbe Gebiet zeigen.
- Berichte im Repo unterlagen (C:/Users/Phil/Developement/Victor/unterlagen/berichte/): vor allem 48_luftbild_segmentierung_klassen.md (Klassen für Luftbild-Segmentierung), dazu 46 (Landnutzung hochaufgelöst), 47, 41. Was dort an Klassen, Quellen und Zweck (Bienen/Landnutzung, AT/CZ/SK/HU, 1820–2025) schon festgelegt ist, ist Vorgabe bzw. Ausgangspunkt für das Kategoriensystem.
- Vorbild Stitcher-Session (Bereich nai, nur lesen): Ordner A = C:/Users/Phil/AppData/Local/Temp/claude/6bc45b42c5448cb2/6e02ebfe-8ebf-4cf1-90c0-685926031afe/scratchpad/aufbereitung (AUFTRAG.md, AUFTRAG_DIREKT.md, AUFTRAG_KORREKTUR.md, AUFTRAG_UMSETZEN.md, kachel.json, kachel_direkt/bau.py, kachel_direkt/_bau/letzter_lauf.txt, kachel_direkt/kategorien.json, Agent-Skripte in A/<ID>/direkt/ und A/korrektur1|2/). Achtung: Zwischenordner, kann verschwinden. Auszüge mit allen Agent-Aufträgen: C:/Users/Phil/AppData/Local/Temp/claude/27e54e3b8399faf6/a2bf01d3-627c-4b06-8b57-51f25ab5229e/scratchpad/segmente-nachvollzug/keyprompts.txt (und users.json). Automatische Vorstufe: C:/Users/Phil/Developement/websites/nai/stitcher/scripts/seg_datensatz/ (rohmaske.py, rohmaske_konfig.json, sam3_konfig.json, kandidaten.py); Agent-Skill stitcher/.claude/skills/seg-ds-agent/SKILL.md.
- Schon bekannter Ablauf dort (Bericht eines Agents, ungeprüft): (1) Automatik „Roh+SAM": SAM3 (facebook/sam3, Textprompt „insect", Bildpyramide 5 Stufen) als Keime, Kanten-Rohmaske (Canny, Schließen, Boden-Regel über Lab-Farbe), Trennen per Watershed, Reste als Fremdmaterial; (2) Agent entscheidet Kandidaten im Panel; (3) je Segment ein Agent: frei urteilen „sauber oder nicht", Mängel und Vorschlag einzeichnen, Nutzer prüft auf Durchklick-Seite; dann Agents mit „direkten Masken": bildpunktgenaue Maske per Python (grobe Linie von Hand, Einrasten auf Farb-/Helligkeitsumschlag im engen Band, GrabCut/Watershed mit Hand-Marken, „geschätzte" Kanten melden), Abgabe als Masken-PNG plus objekte.json; (4) Zusammentragen in eine Label-Karte (16-Bit-PNG, „korrigiert gewinnt", Zählprobe ohne Überlappung), Seite mit Ständen, Kategorien, Kommentar-Export; Korrekturrunden nach Nutzer-Kommentar („genau den Kommentar umsetzen, alles andere bildpunktgleich"). Bündelung in Einheiten, damit keine zwei Agents dasselbe Objekt anfassen.

FRAGEN, DIE DIE ERMITTLUNG BEANTWORTEN SOLL (Vorschlag für die Einheiten):
1. Bestand: Was zeigen die vier Bilder genau (Größe, Kanäle, Auflösung am Boden, Gebiet, Landschaftselemente, Schwierigkeiten wie Schatten, Scan-Ränder, Körnung)? Welcher Ausschnitt eignet sich für den ersten Test?
2. Kategoriensystem: Welche Klassenschemata für Landbedeckung/Landnutzung in Europa gibt es (z. B. CORINE, LUCAS, EUNIS, Urban Atlas, INSPIRE, nationale wie AT LISA/DKM-Nutzung/INVEKOS, FLAIR, OpenEarthMap, LoveDA …), wie fein sind sie, was passt zu 0,2 m Auflösung und zu Bericht 48? Vorschlag einer hierarchischen Kategorienliste (grob bis fein), die auch auf Schwarz-Weiß-Bildern entscheidbar bleibt, mit Regel für Unklares.
3. Stand der Technik für die automatische Vorstufe bei Luftbildern: Grundmodelle und Verfahren, die lückenlose Segmente liefern (SAM/SAM2/SAM3 mit Text- oder Rasterprompts, „segment everything" plus Füllen der Lücken, Superpixel, offene Vokabulare für Fernerkundung, panoptische Modelle, vortrainierte Landbedeckungsmodelle), samt Lizenz, Hardwarebedarf (auf diesem PC vorhandene GPU/venv des stitcher beachten), bekannte Schwächen bei historischen Schwarz-Weiß-Bildern.
4. Vorhandene offene Daten als Hilfs- oder Vorbelegung für das Testgebiet und Europa (OpenStreetMap, INVEKOS-Schläge, Kataster/DKM, Gelände- und Oberflächenmodelle, bestehende Landbedeckungskarten) und offene Trainingsdatensätze; Lizenz und Eignung als schwache Labels.
5. Übertragung der Stitcher-Methode: Was lässt sich übernehmen (Auftragstexte, Abgabeformat, Label-Karte, Zählprobe, Seite, Korrekturrunden), was muss anders sein (keine freie Hintergrundklasse: Lückenlosigkeit als Prüfregel; gemeinsame Grenzen zwischen Nachbarn; sehr große Bilder kacheln mit Überlapp und Nahtregel; Einheiten-Bildung; Kosten je Kachel)? Was war dort Handarbeit oder Einmal-Code und gehört jetzt von Anfang an als wiederverwendbares Werkzeug gebaut?
6. Güte und Wachstum: Wie prüft man Vollständigkeit und Qualität (Prüfregeln, Stichprobe des Nutzers, Zweitagent), wie macht man das Trainingsmaterial robust gegen Jahr/Qualität/Auflösung (dasselbe Gebiet in mehreren Jahrgängen, Übertragen von Labels zwischen Jahrgängen, Verschlechtern/Umrechnen der Bilder), welches Datensatzformat (z. B. Label-Karte plus Kategorien, COCO-panoptic) ist für das spätere Training sinnvoll?

ERGEBNIS: Empfehlung als Schritt-für-Schritt-Plan für den ersten Test (ein Ausschnitt eines aktuellen Orthofotos, danach derselbe Ansatz an einem historischen Bild), mit Aufwand, Risiken, Alternativen und den Fragen, die der Nutzer entscheiden muss; Kandidaten als mögliche Bau-Wünsche. Jede Aussage aus dem Web mit Quelle; Unbelegtes als solches markiert.

EINGRIFF: keiner. Bilder nur lesen; verkleinerte Vorschauen und Ausschnitte zum Ansehen sind erlaubt, aber nur im Berichtsordner der Ermittlung, nie im Datenraum. Python mit Bildbibliotheken: C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe (nur benutzen, nichts installieren). Kein Probelauf von Modellen, kein Download großer Daten.

## Fragen

Der Planer hat vorläufig mit der Empfehlung geplant; die Ermittlung liefert Belege für die Wahl.

### F1: Wie klein dürfen die kleinsten Segmente werden?
- Lage: Bericht 48 legt für das Bienenprojekt eine Mindestgröße fest (Flächen ab 100–400 m², also etwa 10 × 10 bis 20 × 20 m, Linien wie Hecken oder Raine ab 2 m Breite); Sie wünschen sich „so fein wie möglich". Auf dem aktuellen Orthofoto ist ein Bildpunkt 0,2 m groß, man sieht dort also auch einzelne Bäume, Gartenwege oder Schuppen.
- Empfohlen: so fein, wie es im Bild sicher erkennbar ist (Einzelbaum, schmaler Weg, kleines Gebäude), und die Mindestgröße aus Bericht 48 nur als gröbere Auswertungsebene — so bleibt das Trainingsmaterial fein und die Bienenauswertung trotzdem möglich.
- Mindestgröße aus Bericht 48 schon beim Segmentieren — weniger Segmente und weniger Aufwand, aber Kleinstrukturen verschwinden in größeren Flächen.
- Feste Zwischengröße (z. B. ab 10 m²) — Kompromiss, einfacher zu prüfen.

### F2: Für welchen Zweck sollen die Kategorien gebaut sein?
- Lage: Bericht 48 hat Klassen für das Bienenprojekt (z. B. Trockenrasen, Feldraine, offene Sandstellen); Sie wollen ein allgemeines Landschaftsmodell für Europa. Die Kategorienliste bestimmt, was später jedes Segment heißt.
- Empfohlen: allgemeine, gestufte Liste (grob bis fein), deren grobe Ebene genau die sechs Klassen aus Bericht 48 sind und deren feine Ebene die Bienenklassen enthält — ein Material dient beiden Zwecken.
- Nur die Klassen aus Bericht 48 — schnell, aber für ein allgemeines Modell zu eng.
- Eine bestehende europäische Liste unverändert (z. B. CORINE) — gut vergleichbar, aber für 0,2 m zu grob.

### F3: Sollen Farbbilder für die Einheitlichkeit in Schwarz-Weiß umgewandelt werden?
- Lage: Bericht 48 empfiehlt, Farbbilder ab den 1990ern in Graustufen umzuwandeln, damit alle Jahrgänge gleich aussehen; Ihr Ziel ist ein Modell, das Farbe und Schwarz-Weiß gleichermaßen kann.
- Empfohlen: auf dem Farbbild beschriften (Farbe hilft beim Entscheiden) und für das Training zusätzlich eine Schwarz-Weiß-Fassung desselben Ausschnitts mit denselben Segmenten erzeugen — das Modell lernt beides.
- Von Anfang an nur in Schwarz-Weiß beschriften — gleiche Bedingungen wie bei den historischen Bildern, aber schwierigere Entscheidungen.
- Nur in Farbe — einfacher, aber das Modell lernt Schwarz-Weiß nicht.
- Ergänzung aus der Ermittlung: Eine Studie zu historischen Luftbildern (HAIR) fand, dass Vortraining auf umgewandelten Farbbildern allein nichts bringt; echte alte Bilder müssen zusätzlich beschriftet werden. Die Empfehlung bleibt, die Schwarz-Weiß-Fassung ist aber nur ein Zusatz.

### F4: Wo sollen die Werkzeuge für die Landschafts-Segmentierung entstehen?
- Lage: Im Basisordner gibt es nur das Repo unterlagen, und das enthält nur Dokumente. Die Werkzeuge der Stitcher-Session liegen im Repo stitcher (Bereich nai). Für die Landschaft braucht es eigene Skripte, eine Prüfseite und Agent-Anleitungen.
- Empfohlen: ein neues Repo im Basisordner Victor (z. B. `landseg`) mit eigenem Profil; die Stitcher-Teile werden dorthin übernommen und angepasst — so bleibt der Insekten-Stitcher unberührt, und alles zur Landschaft liegt beisammen.
- Im Repo stitcher als zweiter Datensatz-Typ — gemeinsamer Code, aber Landschaft und Insekten vermischen sich.
- Nur Skripte in einem Unterordner von unterlagen — schnell, aber das Repo ist für Dokumente gedacht und hat keine Prüfungen.

### F5: Wohin gehören unbefestigte Wege und Weingärten/Obstanlagen in der groben Ebene?
- Lage: Die vorgeschlagene Kategorienliste hält sich an die sechs Hauptklassen aus Bericht 48. Zwei Fälle passen dort nicht eindeutig: Feld- und Waldwege sind nicht versiegelt, und Weingärten oder Obstanlagen sind weder Acker noch Wiese.
- Empfohlen: unbefestigte Wege unter „Versiegelt/bebaut › Verkehrsfläche" und Dauerkulturen unter „Acker" — so ordnen es auch CORINE (Landwirtschaft) und FLAIR (Wege als Verkehrsfläche) ein.
- Unbefestigte Wege unter „Offener Boden" — näher an dem, was man sieht, aber Wege zerfallen dann in viele Stücke.
- Dauerkulturen als siebte Hauptklasse — klarer für Bienen-Auswertungen, weicht aber von Bericht 48 ab.

### F6: Sollen offene Zusatzdaten (Höhenmodell, Feldstücke, Gebäude) beim Test helfen?
- Lage: Für das Testgebiet in Linz gibt es offen ein Höhenmodell (zeigt, wo Bäume und Häuser hoch stehen), die gemeldeten Feldstücke der Landwirte und Gebäudeumrisse. Dafür müssen Daten heruntergeladen und eine zusätzliche Python-Umgebung eingerichtet werden. Die genaue Lage gegenüber dem Luftbild ist noch ungeprüft.
- Empfohlen: im ersten Test noch nicht — zuerst zeigen, dass Bild plus Agents allein lückenlos und sauber segmentieren; die Zusatzdaten danach als eigener Schritt (Kandidat K5), nur als Hinweis und Prüfquelle, nie als fertige Grenze.
- Gleich im ersten Test — bessere Trennung von Bäumen, Gebäuden und Schatten, aber mehr Aufbau vorab.
- Gar nicht — das Modell soll auch dort arbeiten, wo es solche Daten nicht gibt (z. B. bei alten Bildern).

### F7: Woher soll später dasselbe Gebiet in mehreren Jahrgängen kommen?
- Lage: Damit das Modell lernt, dass dieselbe Landschaft 1968 und heute verschieden aussieht, braucht es dieselbe Fläche aus mehreren Jahren. Die vorhandenen alten Scans zeigen ein anderes Gebiet als das aktuelle Orthofoto (wahrscheinlich den Seewinkel). Frei herunterladbar gibt es für den Seewinkel aktuelle Orthofotos 2019 und 2025; für Linz-Urfahr gibt es alte Bilder nur zum Ansehen beim Land (DORIS) oder zum Kauf beim BEV (etwa 1 Euro je km² für ein altes Orthofoto, 25 Euro je gescanntem Einzelbild).
- Empfohlen: erst nach den Tests an T0 und H0, dann kostenfrei über den Seewinkel (Kandidat K6) — kein Geld, nutzt die vorhandenen Scans; vorher muss nur bestätigt werden, dass die Scans wirklich dort liegen.
- Für Linz-Urfahr einen alten Jahrgang kaufen oder beim Land anfragen (Kandidat K8) — passt direkt zum beschrifteten Testgebiet, kostet aber wenig Geld bzw. eine Anfrage, und der Jahrgang ist vorher unbekannt.
- Vorerst gar nicht — Robustheit nur über verschiedene Gebiete und Graustufen-Fassungen; schneller, aber das Modell lernt Veränderungen über die Jahre nicht am selben Ort.

## Entscheidungen

| Datum | Thema | Entscheidung |
|---|---|---|
| 2026-11-17 | Push zu GitHub | Nur auf ausdrückliche Ansage, nie automatisch nach einem Wunsch (aus `entscheidungen.md`, gilt für alle). |

## Arbeitsauftrag

### Abnahmekriterien

AK1: Der Bericht beschreibt die vier vorhandenen Luftbilder (Größe, Farbe oder Schwarz-Weiß, Auflösung, was zu sehen ist) und nennt einen begründeten Ausschnitt für den ersten Test — prüfbar: Ansicht: Abschnitt im Bericht lesen
AK2: Der Bericht schlägt eine gestufte Kategorienliste für europäische Landschaft vor, begründet aus bestehenden Klassensystemen und aus Bericht 48, mit einer Regel für Unklares — prüfbar: Ansicht: Kategorienliste mit Quellen im Bericht
AK3: Der Bericht enthält einen Schritt-für-Schritt-Vorschlag für den ersten Test, der erklärt, wie jeder Bildpunkt genau einem Segment zugeordnet und das geprüft wird, was aus der Stitcher-Session übernommen und was geändert wird, mit Aufwand, Risiken und mindestens einer Alternative — prüfbar: Ansicht: Empfehlung im Bericht
AK4: Aussagen über Modelle, Datensätze und Klassensysteme tragen eine Quelle; was nicht belegt ist, ist als ungeprüft markiert — prüfbar: Ansicht: Quellenangaben im Bericht
AK5: Kernaussagen der Recherche (Lizenz, Auflösung, Klassenzahl, Hardwarebedarf) haben zwei unabhängige Quellen mit vollständigem Link und Abrufdatum; jedes empfohlene Modell, jeder Datensatz und jede Datenquelle steht mit Link und Lizenz in einer Vergleichstabelle — prüfbar: Ansicht: Vergleichstabellen im Bericht
AK6: Alle sechs Teilfragen (Bestand, Kategorien, Vorstufe, offene Daten, Übertragung der Stitcher-Methode, Güte/Robustheit/Format) sind beantwortet oder als Lücke mit Grund genannt, und die Kandidaten nennen die Bau-Wünsche für den ersten Test — prüfbar: Ansicht: „Befund", „Abdeckung" und „Kandidaten"

## Plan

Erkenntnisziel: Welches Verfahren lässt Claude-Code-Agents ein europäisches Luftbild (erst Orthofoto-Ausschnitt, dann historischer Scan) vollständig, lückenlos und möglichst fein in kategorisierte Segmente zerlegen, abgeleitet aus der Stitcher-Methode und belegt mit dem Stand der Technik? Details: `2026-11-17-landseg-methode/plan.md`.

- e01 Bestand der vier Luftbilder und Testausschnitt (lokal, Vorschauen nur in `roh/e01/`) — opus
- e02 Kategoriensystem: europäische Schemata im Vergleich, gestufte Liste mit Regel für Unklares — opus
- e03 Stand der Technik der automatischen Vorstufe (SAM-Familie, offene Vokabulare, Landbedeckungsmodelle, Superpixel) samt GPU und venv dieses PCs — opus
- e04 Offene Daten als Vorbelegung (OSM, INVEKOS, DKM, Höhenmodelle, Landbedeckungskarten) und offene Trainingsdatensätze — sonnet
- e05 Übertragung der Stitcher-Methode: übernehmen/ändern/neu, Werkzeuge, Kostenschätzung (Quellen nach `roh/e05/quellen/` sichern) — opus
- e06 Güte, Robustheit gegen Jahrgang/Qualität/Auflösung, Datensatzformat — sonnet

Übersprungen mangels Eingriff: Probelauf von Modellen und Probesegmentierung (späterer Bau-Wunsch); nicht geplant: Georeferenzierung der historischen Scans, Bezug weiterer Jahrgänge.

## Befund

Stand Runde 2, abschließend (Nachprüfungen n01, n02 eingearbeitet). Ausführlich mit allen Belegen,
Lizenz-Übersicht (2.12) und dem Schritt-für-Schritt-Vorschlag: `2026-11-17-landseg-methode/bericht.md`.

Antwort: Lückenlos wird das Ergebnis nicht durch ein Modell, sondern durch die Datenform. Das Bild ist
von Anfang an eine Label-Karte, in der jeder Bildpunkt genau eine Segment-ID hat (0 verboten). Die
Vorstufe baut sie aus einer feinen Übersegmentierung (Superpixel/Wasserscheide), in die SAM 3 (lokal
vorhanden) Objekte und Klassenvorschläge einrastet. Danach arbeiten Claude-Agents wie in der
Stitcher-Session (Urteil mit Mängelbild → Nutzer bestätigt → direkte Bearbeitung per Python, Kante im
engen Band → Zusammentragen, Prüfseite, Korrekturrunden). Anders als dort arbeitet jeder Agent an
einer Teilkachel mit Kontextrand statt an einem Objekt und gibt eine Label-Karte statt
Einzelmasken ab. Kategorien sind eine eigene dreistufige Bedeckungsliste (7/25/46 Klassen,
Ebene 1 = Bericht 48 plus „nicht bestimmbar"). Erster Test: T0 im Orthofoto (1000 × 1000 px, 4 ha),
danach H0 im Scan 1968.

Befunde nach Gewicht:
1. „Segment everything" (SAM 2.1) deckt Luftbilder selbst mit Mehrfachdurchgang nur zu 91–98 % ab;
   Superpixel/Wasserscheide sind lückenlos per Konstruktion → Partition zuerst
   (`…/einheiten/e03.md` B8, B9; bestätigt).
2. SAM 3 in der lokalen transformers-Fassung liefert Instanzen, Semantikkarte und Presence-Wert →
   trainingsfreie Klassenkarte nach SegEarth-OV3 nachbaubar, erwartbar nur 43–60 % mIoU, schwach bei
   dünnen Linien und Kleinobjekten (`e03.md` L4–L6, B3).
3. Stitcher: rund 40 Agents für eine Kachel, aber nur 19 von 333 Segmenten (5,7 %) einzeln bearbeitet,
   14,6 % der Bildpunkte belegt; Einzelmasken erzeugen Lücken/Überlappungen, Zählprobe prüft nicht
   „alles belegt" → Einheit Teilkachel, Abgabe Label-Karte, Zählprobe H × W (`e05.md` B2–B5).
   Übertragbar: Auftragsform, Kantenregel, Prüfseite, Korrekturrunden; Einmal-Code (fest verdrahtete
   IDs, 28 Patches) wird Werkzeugkasten W1–W10 (`e05.md` B6–B10).
4. Bestand: Orthofoto RGB ohne IR, 0,2 m, Linz-Urfahr/Pöstlingberg; Scans 1957/1968 Graustufen,
   ≈ 0,45 m (vermutet), **anderes Gebiet** (wahrscheinlich Seewinkel) → keine Label-Übertragung
   Orthofoto ↔ Scan (`e01.md` B1–B14).
5. Kein europäisches Schema passt unverändert zu 0,2 m (CORINE, CLC+, Urban Atlas, LUCAS, LISA, DKM,
   FLAIR verglichen) → eigene Liste mit Abbildung auf diese, Bedeckung vor Nutzung, Regel für
   Unklares: Rückfall auf Elternklasse + `sicher: nein`, Schatten keine Klasse (`e02.md`).
6. FLAIR-HUB-Modell entfällt als Vorstufe (braucht IR); FLAIR-Daten (Etalab 2.0) sind die einzige frei
   nutzbare 0,2-m-Quelle fürs spätere Vortraining; offene AT-Daten (BEV DOM/DGM, INVEKOS, DKM) taugen
   als Hinweis und Prüfquelle, nicht als Label (`e03.md` B6, `e04.md`).
7. Robustheit: echte historisch beschriftete Kacheln nötig, Graustufen-Fassungen nur Zusatz;
   Label-Übertragung zwischen Jahrgängen nur an unveränderten, georeferenzierten Flächen; Format
   panoptisch (Label-Karte + Segmentliste, Export COCO-panoptic) (`e06.md`).
8. Mehrjahrgang: kein offen herunterladbarer Satz „dasselbe Gebiet, mehrere Jahrgänge". Seewinkel:
   Burgenland-Orthofoto 2019/2025, 0,2 m, CC BY 4.0 AT, frei → Gegenstück zu den Scans, wenn deren
   Gebiet bestätigt ist. Linz-Urfahr: DORIS-Altorthofotos ab 1953 nur als Ansicht; BEV-Orthophoto
   historisch 0,5 m für ≈ 1 EUR/km² oder Scan 25 EUR (`einheiten/n02.md`, bestätigt bis auf B4/B12).
9. Lizenzen: Python-Bausteine belegt (BSD/MIT/Apache); SAM 3 erlaubt Nutzung gebührenfrei mit
   Nennungspflicht, Freistellung Metas und Lizenzkopie bei Weitergabe, kein Verbot für Masken als
   Trainingsdaten gefunden (Auslegung); BEV-Höhen-/Katasterdaten CC BY 4.0; SegEarth-OV3 ohne
   Lizenz → nur Nachbau (`einheiten/n01.md`, alle bestätigt; Übersicht `bericht.md` 2.12).

Widerlegt: DKM-Mindestfläche „200 m² außer Bauflächen" (richtig § 4 BANU-V: Gebäude 20 m², Streifen
4 m, Wald 10 m/1 000 m², übrige 200 m²); LandCover.ai hat 4 Klassen/216 km², nicht 3/177 km²;
„FLAIR-HUB in ISPRS J. 2026" nur Preprint; DORIS-Daten „unter CC BY laut Nutzungsbedingungen" –
dort steht keine Lizenz, die Lizenz der DORIS-Orthofotos ist offen (`bericht.md` 2.8). Unklar:
HILUCS-Klassen, Lizenzen CLC+/Urban Atlas/LISA/SWF, HAIR-Details, Kostenrechnung (reine Schätzung),
Abgreifen aus WMS/WMTS-Diensten.

## Abdeckung

8/8 Einheiten (6 + Nachprüfungen n01, n02) mit Rückmeldung und Gegenprüfung, 107 Befunde
nachvollzogen (98 bestätigt, 3 widerlegt bzw. teilweise, 6 unklar). AK1–AK4 und AK6 erfüllt. AK5
weitgehend: jeder empfohlene Baustein mit Link und Lizenz in `bericht.md` 2.12; zwei unabhängige
Quellen fehlen weiter für SAM-3-Wortlaut (zweite Stelle nur nach Anmeldung), BEV DOM/DGM (beide
Quellen BEV), INVEKOS und BEV-Gebäude (nur Suchauszüge, INSPIRE-Geoportal nicht erreichbar),
Burgenland-Orthofoto, basemap.at; DORIS-Orthofoto-Lizenz offen. Für den internen Test unkritisch.
Nicht geprüft: Probelauf der Vorstufe und Probesegmentierung (Eingriff keiner), Lagegenauigkeit
offener Daten (kein Download), Georeferenz und Gebiet der Scans (nicht geplant), Jahrgänge der
DORIS-Altbestände für Linz-Urfahr und Stadt-Linz-Geoportal (nur per Anfrage), Token-Kosten (keine
Zahlen im Stitcher-Transkript), EUNIS, Prithvi/SatMAE/Clay, Potsdam/Vaihingen/DeepGlobe (Budget),
Rechtsauskunft (außerhalb).

## Kandidaten

K1: Kategorienliste festschreiben (`kategorien.json` hierarchisch 7/25/46 mit Regeln G1–G5, U1–U5, Abbildungen; als Bericht in unterlagen) — Gewinn feste Grundlage für jede Beschriftung — Aufwand klein — Risiko gering (SW-Spalte bleibt bis K4 Vermutung) — Repo unterlagen — empfohlen
K2: Werkzeugkasten W1–W10 bauen (kacheln, vorstufe mit Superpixel + SAM 3 + Semantik-argmax als Nachbau aus dem Paper, ansicht, kante, eingriff, pruefen, zusammentragen, seite, export mit Lizenz- und Herkunftsfeld je Kachel, Auftragsvorlagen + Agent-Skill) — Gewinn wiederverwendbar, Lückenlosigkeit per Konstruktion, kein Einmal-Code — Aufwand gross — Risiko mittel (Nahtregel unerprobt) — Repo offen (Frage F4) — empfohlen
K3: Testlauf T0 (Orthofoto, 1000 × 1000 px) mit 4 Teilkacheln, Nutzerbestätigung, Korrekturrunde und Messung (Läufe, Zeit, Zweitagent-PQ, Nutzerurteil je Klasse) — Gewinn belegt, ob das Verfahren trägt — Aufwand mittel — Risiko mittel (Segmentdichte je Agent ungeprüft) — Repo wie K2 — empfohlen
K4: Testlauf H0 (Scan 1968) plus SW-Fassung von T0 — Gewinn misst SW-Entscheidbarkeit je Klasse — Aufwand mittel — Risiko mittel (Vorstufe auf SW schwach) — Repo wie K2 — empfohlen
K5: Hilfsebenen fürs Testgebiet (nDOM aus BEV DOM/DGM, INVEKOS-Schläge, BEV-Gebäude) beschaffen, auf EPSG:31255 schneiden, Lagegenauigkeit an Stichproben messen — Gewinn Hinweise für Bäume/Gebäude/Schatten, automatische Prüfquelle — Aufwand mittel — Risiko Lizenz/Lage, braucht eigene Umgebung mit rasterio/pyproj — Repo wie K2 — optional
K6: Mehrjahrgang kostenfrei über den Seewinkel: Gebiet der Scans 1957/1968 bestimmen und georeferenzieren, dazu Burgenland-Orthofoto 2019/2025 (0,2 m, CC BY 4.0 AT, frei, https://geodaten.bgld.gv.at/de/downloads/hoehenmodelle-orthofotos.html) für dieselbe Fläche in den Datenraum — Gewinn dasselbe Gebiet in drei bis vier Jahrgängen, Label-Übertragung an unveränderten Flächen — Aufwand mittel — Risiko Scans zeigen doch ein anderes Gebiet (nur Augenschein), Georeferenz alter Scans braucht Passpunkte und rasterio/GDAL — Repo Datenraum/wie K2 — optional (nach K3/K4)
K7: Zielmodell vorbereiten (EoMT/Mask2Former mit DINOv3, Vortraining FLAIR, später als Vorstufe) — Gewinn halbautomatisches Wachstum — Aufwand gross — Risiko erst ab einigen hundert Teilkacheln sinnvoll — Repo wie K2 — optional
K8: Historischen Jahrgang für Linz-Urfahr besorgen: Anfrage bei DORIS (doris.geol.post@ooe.gv.at: Jahrgänge und Nutzungsrecht der Altorthofotos) oder Kauf beim BEV (Orthophoto historisch 0,5 m ≈ 1 EUR/km², Scan 25 EUR + eigene Georeferenz, https://www.bev.gv.at/en/Services/Products/Remote-Sensing.html) — Gewinn Mehrjahrgang am schon beschrifteten Testgebiet T0 — Aufwand klein bis mittel — Risiko Geld (Größenordnung 1–50 EUR), Jahrgang des BEV-Orthophotos unbekannt, DORIS-Lizenz offen — Repo Datenraum — nur mit Freigabe

## Empfehlung

Antwort: Claude Code kann ein Landschaftsbild lückenlos segmentieren, wenn das Bild von Anfang an eine Label-Karte ist (jeder Bildpunkt genau eine Segment-ID) und die Agents je Teilkachel statt je Objekt arbeiten. Die Stitcher-Methode lässt sich also nur zum Teil übernehmen: Ablauf, Kantenregel, Prüfseite und Korrekturrunden passen, „ein Agent je Objekt" mit Einzelmasken dagegen nicht (dort waren am Ende nur 14,6 % der Bildpunkte belegt, und auch das beste „segment everything" deckt nur 91–98 % ab).
- K1: trägt — die Kategorienliste ist die zweite Hälfte von „jedes Segment mit Kategorie" und braucht wenig Aufwand; sie hängt aber an den Entscheidungen F2 und F5 und wird von K2 als `kategorien.json` gebraucht.
- K2: trägt — ohne die Werkzeuge gibt es keinen Test: lückenlose Vorstufe, Eingriffe auf der Label-Karte und die Prüfung „H × W, kein 0" machen die Lückenlosigkeit erst prüfbar. Gefragt ist aber der Test, nicht der ganze Kasten.
- K3: trägt — das ist der Test, um den Sie gebeten haben („das Landschaftsbild so fein wie möglich segmentieren"). Er geht aber erst, wenn K2 steht.
- K4: trägt teilweise — dient Ihrem Ziel „unabhängig von Jahr und Qualität" und misst, was auf Schwarz-Weiß entscheidbar ist. Die Scans zeigen aber ein anderes Gebiet, und der Lauf kommt erst nach K3.
- K5: trägt teilweise — hilft bei Bäumen, Gebäuden und Schatten, ist für die Lückenlosigkeit aber nicht nötig und widerspricht dem Ziel, auch ohne Zusatzdaten zu segmentieren (F6).
- K6: trägt teilweise — liefert kostenfrei dasselbe Gebiet über mehrere Jahrgänge für die Robustheit, erst nach dem Test sinnvoll; das Gebiet der Scans ist nur nach Augenschein bestimmt.
- K7: trägt teilweise — das ist Ihr Endziel, aber erst ab einigen hundert beschrifteten Teilkacheln sinnvoll. Vorher gibt es nichts zu trainieren.
- K8: trägt teilweise — Mehrjahrgang am Testgebiet, kostet aber Geld bzw. eine Anfrage, der Jahrgang ist unbekannt; nur mit Freigabe.
Nächster Schritt: K2 als Folge-Wunsch (nachdem Sie F4 zum Ort entschieden haben), zugeschnitten auf den Test T0: Werkzeuge W1–W8 und die Vorlagen W10, `kategorien.json` aus K1 mitnehmen, den Export W9 erst nach dem Test. Abgenommen wird an einer Teilkachel von T0: Die Vorstufe läuft, `pruefen` meldet H × W ohne 0, und die Zahl der Segmente je Teilkachel ist gemessen. — Danach kann K3 sofort laufen, und die unsicherste Annahme ist schon geprüft, bevor der erste Agent urteilt.
Gegenargument: Am Bild ist bisher nichts erprobt. Im Stitcher urteilte ein Agent über genau ein Segment (4–8 min); in T0 kämen auf eine Teilkachel von 500 px 40–60 Segmente (nur vermutet, `bericht.md` 3.6). Die Vorstufe erreicht auf ähnlichen Bildern nur 43–60 % mIoU und ist gerade bei Hecken, Wegen und Kleinobjekten schwach (`e03.md` L6/B3), also genau bei der Feinheit, die Sie wollen. Ein großer Werkzeugkasten könnte deshalb um eine Einheitengröße herum gebaut werden, die nicht trägt. — Der Schritt gilt trotzdem: Die Größe der Teilkacheln ist ein Parameter in W1 (auf 250 px verkleinerbar) und kein Umbau, und die Abnahme an einer echten T0-Teilkachel misst die Dichte, bevor K3 Agent-Läufe kostet.

## Folge-Wünsche

<Hauptsession: Kurznamen der Wünsche, die aus Kandidaten entstanden sind>
- landseg-kategorien (K1): `wuensche/2026-11-17-landseg-kategorien.md`
- landseg-werkzeuge (K2): `wuensche/2026-11-17-landseg-werkzeuge.md`
- landseg-test-t0 (K3): `wuensche/2026-11-17-landseg-test-t0.md`
