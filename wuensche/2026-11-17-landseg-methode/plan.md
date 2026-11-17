# Plan: landseg-methode (Recherche, Stufe M, Eingriff keiner)

**Erkenntnisziel:** Welches Verfahren lässt Claude-Code-Agents ein europäisches Luftbild (zuerst
ein Ausschnitt des Orthofotos 5236-55/56, dann ein historischer Scan) vollständig und lückenlos in
möglichst feine, kategorisierte Segmente zerlegen, abgeleitet aus der Stitcher-Methode und belegt
mit dem Stand der Technik, so dass daraus Trainingsmaterial für ein jahrgangs-, qualitäts- und
auflösungsunabhängiges Segmentiermodell wird?

Der Auswerter baut aus den sechs Einheiten den Schritt-für-Schritt-Vorschlag (AK3). Jede Einheit
liefert dafür ihren Baustein und schreibt am Ende einen Abschnitt `Für den Vorschlag:` (höchstens
zehn Zeilen: was ihr Befund für den ersten Test und für das Wachstum bedeutet).

## Gemeinsame Regeln für alle Einheiten

- **Eingriff keiner.** Bilder und fremde Ordner nur lesen. Erlaubt: verkleinerte Vorschauen,
  Ausschnitte, Histogramme und Kopien von Textauszügen, aber nur unter
  `C:/Users/Phil/Developement/Victor/wuensche/2026-11-17-landseg-methode/roh/<id>/`, nie im
  Datenraum `C:/Users/Phil/Developement/Victor/daten/` und nie in den Stitcher-Ordnern. Python nur
  `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I` (nichts
  installieren; vorhanden sind u. a. PIL, cv2, skimage, tifffile, torch, transformers). Kein
  Modell-Probelauf, kein Download über ein paar MB, keine Anmeldung bei Diensten.
- **Beleg bei Web-Quellen:** vollständige URL, kurzes Zitat, Abrufdatum 2026-11-17 (oder Tag des
  Abrufs); Kernaussagen (Lizenz, Auflösung, Klassenzahl, Hardwarebedarf, Leistungszahl) mit zwei
  unabhängigen Quellen (z. B. Paper und Repo/Modellkarte; Hersteller und Datenportal). Quellenarten
  in dieser Reihenfolge: Primärquelle (Paper, offizielle Nomenklatur, Modellkarte, Lizenzdatei),
  Datenportal/Behörde, unabhängiger Vergleich (Benchmark, Review), erst dann Blog/Forum. Was nur
  eine Quelle hat oder aus dem Gedächtnis stammt, heißt `vermutet`.
- **Beleg bei lokalen Dateien:** `<pfad>:<zeile>` mit kurzem Zitat oder Befehl mit dem
  entscheidenden Ausgabe-Ausschnitt; längere Ausgaben nach `roh/<id>/`.
- **Eigene Bestände zuerst:** Berichte `C:/Users/Phil/Developement/Victor/unterlagen/berichte/`
  (41, 46, 47, 48) sind Vorgabe; was sie schon sagen, nicht neu recherchieren, sondern zitieren.
- **Recherche je Einheit:** 8 bis 12 gelesene Quellen (selbst geöffnet, nicht nur Suchtreffer),
  höchstens 50 Werkzeugaufrufe. Muss-Kriterien und Bewertungskriterien siehe Abschnitt der Einheit.
- Datei `einheiten/<id>.md` früh anlegen und Befunde gleich eintragen (Format: Anleitung
  `ermitteln`).

## e01 Bestand der vier Luftbilder und Testausschnitt

- **Klären:** je Bild Breite × Höhe in Bildpunkten, Kanäle (RGB, RGBI, Grau), Bittiefe,
  Kompression/Kachelung des TIFF, Bodenauflösung (Orthofoto aus `.TFW`; historische Scans
  schätzen aus Scanauflösung/Bildmaßstab, falls TIFF-Tags oder Randbeschriftung Hinweise geben,
  sonst `vermutet`), abgedeckte Fläche in m bzw. ha, Lage (Orthofoto: Eckkoordinaten aus `.TFW`
  in EPSG:31255, grob in Ort/Region übersetzen, z. B. über die Blattnummer 5236 der ÖK/BEV-Teilung;
  Ortsnamen nur als `wahrscheinlich`, wenn nicht doppelt belegt). Was zu sehen ist: Landschaftstyp,
  vorkommende Elemente (Felder, Wiesen, Wald, Hecken, Einzelbäume, Wege, Straßen, Gebäude,
  Gewässer, offene Bodenstellen, Weingärten …), grobe Flächenanteile nach Augenschein.
  Schwierigkeiten: Schatten, Überstrahlung, Kronenüberdeckung, Scan-Ränder, Rahmenmarken,
  Körnung, Staub/Kratzer, Vignettierung, Verzerrung (historische Scans sind nicht entzerrt).
- **Gleiches Gebiet?** Zeigen die historischen Scans dasselbe Gebiet wie das Orthofoto (ganz,
  teilweise, gar nicht)? Vergleich über markante Strukturen (Straßenführung, Ortsgrundriss,
  Gewässer, Waldränder) an Vorschauen. Ergebnis mit Bildbeleg (Vorschau-Paare in `roh/e01/`)
  und Sicherheit.
- **Testausschnitt:** einen Ausschnitt des aktuellen Orthofotos vorschlagen (Pixelfenster
  x, y, Breite, Höhe; Größe so, dass ein Agent ihn mit Teilkacheln ansehen kann, Richtwert
  1000–2000 px Kantenlänge, Begründung angeben), der möglichst viele Elementtypen und typische
  Schwierigkeiten enthält; dazu den passenden Ausschnitt im historischen Bild, falls dasselbe Gebiet
  gezeigt wird, sonst einen gleichwertigen historischen Ausschnitt. Grobe Zahl erwarteter Segmente
  im Testausschnitt (Zählung nach Augenschein an einer Vorschau, `vermutet`).
- **Wo:** `C:/Users/Phil/Developement/Victor/daten/luftbilder/` (nur lesen, mit tifffile
  speicherschonend, z. B. `tifffile.TiffFile(...).pages[0]` für Tags, Ausschnitte über
  `aszarr`/memmap oder verkleinert), `daten/README.md`.
- **Beleg:** Befehl plus Ausgabe der TIFF-Tags/Formen; Vorschau-Dateien in `roh/e01/`
  (JPEG, längste Kante ≤ 2000 px; Ausschnitte in voller Auflösung ≤ 1500 px) mit Pfad.
- **Außerhalb:** Georeferenzierung der historischen Scans, Segmentieren, Modelle.
- Eingriff keiner, Modell opus (Bildurteil und Gebietsvergleich).

## e02 Kategoriensystem für europäische Landschaft

- **Klären:** Welche Klassenschemata für Landbedeckung/Landnutzung gibt es für Europa, wie fein
  sind sie, für welche Auflösung gedacht, und welche passen zu 0,2 m (aktuell) bzw. ca. 0,5–1 m
  Schwarz-Weiß (historisch)? Mindestens: CORINE Land Cover (Ebenen 1–3), Copernicus Urban Atlas
  bzw. HRL/CLC+ Backbone, LUCAS Land Cover/Land Use, EAGLE-Konzept, INSPIRE Land Cover/Land Use
  (HILUCS), EUNIS-Habitate (nur soweit aus Luftbild entscheidbar), Österreich: LISA
  (Land Information System Austria), DKM-Benützungsarten/Nutzungen, INVEKOS-Schlagnutzungsarten;
  Datensätze mit Feinklassen: FLAIR #1/#2 (IGN, 0,2 m), OpenEarthMap, LoveDA, dazu je Bericht 48
  Ebene 1 und Ebene 2 sowie der Franziszeische Kataster (Übersetzungstabelle laut Bericht 48,
  Vorgabe 3).
- **Liefern:** Vergleichstabelle (Schema, Herausgeber, Klassenzahl je Ebene, Zielauflösung,
  Mindestkartiereinheit, Lizenz der Nomenklatur, Quelle) und einen **Vorschlag einer
  hierarchischen Kategorienliste** in drei Ebenen (grob → fein), deren Ebene 1 Bericht 48
  Ebene 1 abbildet und deren feinste Ebene Einzelobjekte erlaubt (Einzelbaum/Baumgruppe, Hecke,
  Rain, Weg befestigt/unbefestigt, Gebäude, Gewässer …). Je Klasse: Merkmal im Bild, ob auf
  Schwarz-Weiß entscheidbar (ja/eingeschränkt/nein), Abbildung auf CORINE/LISA/Bericht 48.
  Dazu eine **Regel für Unklares** (z. B. Rückfall auf die nächstgröbere Ebene plus Flag
  „unsicher"; Klasse „nicht bestimmbar" nur für Bildfehler/Scan-Rand), damit jeder Bildpunkt
  eine Klasse hat, und eine Regel, ob Kategorie nach Bedeckung (was man sieht) oder Nutzung
  (was es ist) vergeben wird (Ansatz EAGLE/LUCAS: getrennt führen).
- **Muss:** jede Klasse aus dem Bild entscheidbar; Ebene 1 identisch mit Bericht 48 Ebene 1
  oder mit erklärter Abweichung. **Bewertung:** Feinheit, Verbreitung in Europa, Abbildbarkeit
  auf bestehende Datensätze (Training mit Fremddaten), Robustheit gegen Jahrgang.
- **Wo:** Bericht 48 und 46 im Repo unterlagen; Web: Copernicus Land Monitoring Service,
  EEA, Eurostat (LUCAS), INSPIRE-Registry, Umweltbundesamt (LISA), BEV (DKM), AMA (INVEKOS),
  IGN FLAIR, Papers/Repos der Datensätze.
- **Außerhalb:** Verfügbarkeit und Lizenz der Daten selbst (e04), Modelle (e03).
- Eingriff keiner, Modell opus (Synthese über viele Schemata zu einem Vorschlag).

## e03 Stand der Technik: automatische Vorstufe für lückenlose Segmente

- **Klären:** Welche Grundmodelle und Verfahren liefern auf Luftbildern eine lückenlose
  Vorsegmentierung, die Agents dann prüfen und korrigieren? Kandidatengruppen:
  (a) SAM-Familie (SAM, SAM 2, SAM 3 mit Textprompts; „automatic mask generation"/segment
  everything plus Füllen der Lücken) und Fernerkundungs-Ableger (z. B. RSPrompter, SAMRS,
  segment-geospatial/samgeo); (b) offene Vokabulare und Sprach-Bild-Modelle für Fernerkundung
  (z. B. GeoRSCLIP/RemoteCLIP, SegEarth-OV oder vergleichbar); (c) vortrainierte
  Landbedeckungsmodelle für 0,2–1 m (z. B. FLAIR-Baselines, OpenEarthMap-Modelle, Fernerkundungs-
  Grundmodelle wie Prithvi/SatMAE/Clay, soweit für sehr hohe Auflösung tauglich); (d) klassische
  lückenlose Übersegmentierung (SLIC/Felzenszwalb/Watershed, Superpixel-Zusammenführung) als
  Rückfall; (e) panoptische Verfahren (Mask2Former o. ä.) als späteres Zielmodell.
- **Je Kandidat:** liefert er lückenlose oder lückenhafte Masken, Klassen oder nur Segmente,
  Lizenz (Code und Gewichte getrennt), Hardwarebedarf (VRAM, Laufzeit je Kachel, soweit
  belegt), bekannte Schwächen bei historischen Schwarz-Weiß-Scans und bei sehr kleinen oder
  linearen Objekten (Hecken, Wege, Raine), Reife (Pflege, Version, Datum).
- **Lokale Lage (nur lesen):** GPU dieses PCs (`nvidia-smi` ohne Optionen, die etwas setzen),
  Pakete im stitcher-venv (`pip list` über das venv-Python oder Ordnerliste in `Lib/site-packages`),
  wie SAM3 dort eingebunden ist (`C:/Users/Phil/Developement/websites/nai/stitcher/scripts/seg_datensatz/sam3.py`,
  `sam3_konfig.json`), ob Gewichte lokal liegen (nur auflisten). Nichts starten, nichts laden.
- **Muss:** auf diesem PC lauffähig oder klar benannt, was fehlt; Lizenz erlaubt Erzeugung von
  Trainingsdaten. **Bewertung:** Lückenlosigkeit, Feinheit an Grenzen, Eignung für Schwarz-Weiß,
  Aufwand der Einbindung, Kosten.
- **Liefern:** Vergleichstabelle und eine Empfehlung für die Vorstufe des ersten Tests (Haupt-
  und Rückfallweg), begründet.
- **Außerhalb:** Probelauf, Download von Gewichten, Training.
- Eingriff keiner, Modell opus (Abwägung über viele, teils neue Quellen).

## e04 Offene Daten als Vorbelegung und offene Trainingsdatensätze

- **Klären:** Welche offenen Daten können das Testgebiet (Österreich, EPSG:31255; e01 liefert
  die genaue Lage, vorläufig Blatt 5236) und später Europa vorbelegen oder als schwache Labels
  dienen: OpenStreetMap (Gebäude, Wege, Gewässer, landuse/natural), INVEKOS-Schläge Österreich
  (AMA/data.gv.at), DKM/Kataster (BEV), Gebäudeumrisse, Gelände- und Oberflächenmodelle
  (z. B. ALS-DGM/DOM der Länder, Copernicus DEM), bestehende Landbedeckungskarten (CLC, HRL,
  CLC+, ESA WorldCover, LISA, Urban Atlas, Small Woody Features). Je Quelle: räumliche
  Genauigkeit, Aktualität, Lizenz, Format, Bezug (Download/WMS), Eignung als Vorbelegung
  (z. B. Gebäude und Schläge als feste Grenzen) bzw. als Prüfquelle.
- **Trainingsdatensätze:** offene Segmentier-Datensätze mit sehr hoher Auflösung, die später
  mittrainiert werden können (FLAIR #1/#2, OpenEarthMap, LoveDA, Vaihingen/Potsdam, DeepGlobe,
  ggf. historische Luftbild-Datensätze): Auflösung, Klassen, Region, Lizenz (kommerziell/
  nichtkommerziell), Größe; nur Metadaten, kein Download.
- **Muss:** Lizenz belegt; Europa- oder Österreich-Bezug. **Bewertung:** Lagegenauigkeit
  gegenüber 0,2 m, Abdeckung historischer Zeitschnitte, Aufwand des Bezugs.
- **Wo:** data.gv.at, BEV, AMA, Länder-Geoportale (welches Land e01 nennt), Copernicus, ESA,
  OSM-Wiki/Lizenzseiten, Paper/Repos der Datensätze; Bericht 46 (Abschnitt 2.3) zuerst lesen und
  zitieren statt neu recherchieren.
- **Außerhalb:** Kategorienschema selbst (e02), Modelle (e03), Download großer Daten.
- Eingriff keiner, Modell sonnet (Suchen und Abgleichen).

## e05 Übertragung der Stitcher-Methode

- **Klären:** Wie lief die Segmentierung in der Stitcher-Session tatsächlich (Stufen, Agent-
  Aufträge, Abgabeformat, Zusammentragen, Prüfseite, Korrekturrunden, Bündelung in Einheiten,
  Zahl der Agents, Kosten/Dauer, soweit belegbar)? Den „schon bekannten Ablauf" in der
  Wunsch-Datei an den Quellen bestätigen oder berichtigen. Dann je Baustein: **übernehmen**,
  **ändern** (mit Grund) oder **neu**; ausdrücklich: Lückenlosigkeit statt freier
  Hintergrundklasse (Prüfregel: jeder Bildpunkt genau ein Segment, Zählprobe), gemeinsame Grenzen
  zwischen Nachbarn (kein Spalt, keine Überlappung), Kacheln großer Bilder mit Überlapp und
  Nahtregel, Bildung der Agent-Einheiten (z. B. nach Teilkachel statt nach Objekt), Kosten je
  Kachel (Hochrechnung aus Stitcher-Zahlen, als Schätzung markiert). Was dort Handarbeit oder
  Einmal-Code war (Pfade, fest verdrahtete IDs, Skripte je Agent) und von Anfang an als
  wiederverwendbares Werkzeug gebaut werden sollte (Liste mit Vorschlag des Werkzeugs).
- **Wo (nur lesen):**
  `C:/Users/Phil/AppData/Local/Temp/claude/6bc45b42c5448cb2/6e02ebfe-8ebf-4cf1-90c0-685926031afe/scratchpad/aufbereitung/`
  (AUFTRAG*.md, kachel.json, bau_seite.py, kachel_direkt/bau.py, kachel_direkt/kategorien.json,
  kachel_direkt/_bau/, korrektur1|2/kommentare.json, Beispiel-Agentordner wie r2/, u86/);
  `C:/Users/Phil/AppData/Local/Temp/claude/27e54e3b8399faf6/a2bf01d3-627c-4b06-8b57-51f25ab5229e/scratchpad/segmente-nachvollzug/`
  (keyprompts.txt zuerst; agents.json und users.json nur gezielt mit Grep, z. B. nach Token- oder
  Kostenangaben); `C:/Users/Phil/Developement/websites/nai/stitcher/scripts/seg_datensatz/`
  (rohmaske.py, rohmaske_konfig.json, sam3.py, sam3_konfig.json, kandidaten.py, loecher.py,
  zusammensetzen.py, export.py) und
  `C:/Users/Phil/Developement/websites/nai/stitcher/.claude/skills/seg-ds-agent/SKILL.md`.
- **Sichern:** Die beiden Temp-Ordner können verschwinden. Kopiere die vier AUFTRAG*.md,
  kategorien.json und keyprompts.txt nach `roh/e05/quellen/` (nur Kopie, Original unberührt) und
  belege daraus.
- **Beleg:** Pfad:Zeile mit Zitat; Zahlen (Agents, Segmente, Runden) mit Fundstelle.
- **Liefern:** Ablaufbild des Stitcher-Verfahrens (Stufen mit Ein- und Ausgaben), Tabelle
  Baustein → übernehmen/ändern/neu mit Grund, Liste wiederverwendbarer Werkzeuge, Kosten-
  Hochrechnung je Testausschnitt (Annahmen offen genannt).
- **Außerhalb:** Ändern oder Ausführen der Stitcher-Skripte; Web-Recherche.
- Eingriff keiner, Modell opus (Schließen über viele lokale Quellen und Übertragung).

## e06 Güte, Robustheit gegen Jahrgang/Qualität/Auflösung, Datensatzformat

- **Klären:** (a) Wie prüft man Vollständigkeit und Qualität einer lückenlosen Annotation:
  automatische Prüfregeln (Abdeckung 100 %, keine Überlappung, Mindestgröße, Topologie an
  Kachelnähten), Zweitannotation/Übereinstimmungsmaße (z. B. Boundary-IoU, PQ), Stichprobe des
  Nutzers; was Datensätze wie FLAIR/OpenEarthMap/LoveDA dazu dokumentieren. (b) Wie macht man
  Trainingsmaterial robust gegen Jahrgang, Bildqualität und Auflösung: dasselbe Gebiet in mehreren
  Jahrgängen, Übertragen von Labels zwischen Jahrgängen (Änderungserkennung, nur unveränderte
  Flächen übernehmen), Verschlechtern/Umrechnen (Graustufen, Körnung, Unschärfe, Auflösung
  0,2→1 m, JPEG-Artefakte), Domänenanpassung/Stilübertragung, Multi-Skalen-Training; was die
  Literatur zu historischen Schwarz-Weiß-Luftbildern dazu belegt (z. B. Arbeiten zur
  Segmentierung historischer Orthofotos in Europa). (c) Welches Abgabe- und Datensatzformat für
  das spätere Training: Label-Karte (16-Bit-PNG/GeoTIFF) plus Kategorientabelle,
  Instanz-ID-Karte, COCO-panoptic, ggf. Vektor (GeoPackage) für Grenzen; Hierarchie der Klassen
  im Format abbilden; Metadaten je Kachel (Jahrgang, Sensor, Auflösung, Quelle, Lizenz).
- **Muss:** jede Empfehlung mit Quelle oder als `vermutet` markiert. **Bewertung:** Aufwand,
  Nutzen fürs Zielmodell, Kompatibilität mit gängigen Trainingswerkzeugen.
- **Wo:** Papers und Doku zu FLAIR, OpenEarthMap, LoveDA, COCO-panoptic, Cityscapes-Format,
  Arbeiten zu historischen Luftbildern; Bericht 48 Vorgabe 5 (Qualitätskontrolle je Klasse und
  Jahrgang) als Vorgabe.
- **Außerhalb:** Kategorienschema (e02), Vorstufen-Modelle (e03), Stitcher-Abläufe (e05).
- Eingriff keiner, Modell sonnet (Suchen und Zusammenstellen).

## Nachprüfung n01 Lizenzen der empfohlenen Bausteine mit zweiter Quelle (AK5)

- **Anlass:** AK5 verlangt für Kernaussagen (hier: Lizenz) zwei unabhängige Quellen mit Link und
  Abrufdatum. Für mehrere Bausteine, die der Vorschlag empfiehlt, liegt nur eine Quelle oder nur ein
  Suchauszug vor (siehe `bericht.md`, Abschnitt „Abdeckung"). Nur das Fehlende nachholen; was
  schon zwei Quellen hat (FLAIR Etalab 2.0, EoMT MIT, SAM 2 Apache-2.0, OSM ODbL), nicht neu prüfen.
- **Klären, je Baustein Lizenz mit zwei unabhängigen Quellen (URL, kurzes Zitat, Abrufdatum):**
  1. SAM 3 Gewichte (facebook/sam3, „SAM License"): neben `https://github.com/facebookresearch/sam3/blob/main/LICENSE`
     eine zweite Stelle (HF-Modellkarte-Text, Meta-Seite oder die lokale Lizenzdatei im HF-Cache
     `~/.cache/huggingface/hub/models--facebook--sam3/snapshots/*/` falls vorhanden, nur lesen).
     Dazu ausdrücklich: Was sagt der Text zu (a) Weitergabe von Ausgaben/Masken, (b) Nennungspflicht
     bei Veröffentlichung, (c) Freistellung (Indemnity)? Zitat je Punkt.
  2. scikit-image und OpenCV (opencv-python): Lizenzdatei im stitcher-venv
     (`C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Lib/site-packages/*scikit_image*.dist-info/`,
     `*opencv_python*.dist-info/`, nur lesen) und je eine Webquelle (Projektseite oder PyPI).
  3. transformers (Apache-2.0): dist-info im venv plus Repo-Seite.
  4. BEV ALS-Höhenmodelle DOM/DGM 1 m (CC BY 4.0): zweite Quelle außerhalb von data.bev.gv.at, z. B.
     data.gv.at-Eintrag oder INSPIRE-Geoportal.
  5. AMA INVEKOS-Schläge (CC BY-AT 4.0): neben dem EuroCrops-Wiki eine AMA- oder data.gv.at-Seite.
  6. BEV DKM / Nutzungsflächen / Gebäude (CC BY 4.0): Metadatensatz selbst öffnen (bisher nur
     Suchauszüge), dazu ob für die genannten Produkte Gebühren gelten (Preisinformationsseite BEV).
  7. Land OÖ DORIS DGM 0,5 m: Lizenzangabe (data.gv.at oder DORIS-Nutzungsbedingungen).
  8. SegEarth-OV-3-Repo: bestätigen, dass keine Lizenzdatei vorliegt (dann nur Nachbau aus dem Paper).
- **Beleg:** Tabelle `Baustein | Lizenz | Quelle 1 | Quelle 2 | Abruf | Besonderheit` in
  `einheiten/n01.md`; was nur eine Quelle findet, heißt `vermutet`.
- **Außerhalb:** Rechtsauskunft, Download von Daten, Installation.
- Eingriff keiner, Modell sonnet, höchstens 40 Werkzeugaufrufe.

## Nachprüfung n02 Material für „dasselbe Gebiet in mehreren Jahrgängen"

- **Anlass:** e01 B11 belegt, dass die historischen Scans (1957, 1968; vermutlich Seewinkel) nicht
  das Gebiet des Orthofotos (Linz-Urfahr, Pöstlingberg-Südhang) zeigen; e06 B6/B10 sagen, dass
  echte historische Daten und Label-Übertragung zwischen Jahrgängen nur an demselben,
  georeferenzierten Gebiet gehen. Ob dafür offen zugängliches Material existiert, entscheidet, wie
  der Robustheitsteil des Vorschlags aussieht (Kandidat K6 in `bericht.md`).
- **Klären:**
  1. Historische Luftbilder bzw. Orthofotos für das Testgebiet (EPSG:31255 E 67 500–70 000,
     N 353 000–354 000; etwa 48,312–48,321° N, 14,244–14,277° O): Land Oberösterreich DORIS
     (historische Orthofotos, Jahrgänge), Stadt Linz (Geoportal/Stadtplan, historische Luftbilder),
     basemap.at, BEV-Luftbildarchiv (Bestellweg, Preis je Bild, Scanauflösung, Jahrgänge ab 1949,
     Bericht 46 sagt „kostenpflichtig"). Je Quelle: Jahrgänge, Bodenauflösung, Farbe/SW,
     georeferenziert ja/nein, Bezug (WMS/WMTS/Download/Bestellung), Lizenz, Kosten.
  2. Umgekehrt: aktuelles Orthofoto (offen) für den Seewinkel/Neusiedler-See-Ostufer (Burgenland
     GIS, basemap.at Orthofoto, data.gv.at), Lizenz und Auflösung — damit die Scans 1957/1968 ein
     modernes Gegenstück bekämen.
  3. Kurz: ob ein WMS/WMTS-Dienst ein Abgreifen von Ausschnitten in voller Auflösung erlaubt
     (Nutzungsbedingungen), ohne etwas herunterzuladen.
- **Beleg:** URL, Zitat, Abrufdatum; Kernaussagen (Lizenz, Auflösung, Jahrgänge) mit zwei Quellen
  (Portal-Metadaten und data.gv.at bzw. Betreiber). Ergebnis als Tabelle in `einheiten/n02.md`
  mit einer Empfehlung, welche Quelle für einen Mehrjahrgangs-Test taugt.
- **Außerhalb:** Download über ein paar MB (Capabilities-Dokumente sind erlaubt), Bestellung,
  Georeferenzierung, Anmeldung bei Diensten.
- Eingriff keiner, Modell sonnet, höchstens 40 Werkzeugaufrufe.

## Nicht geplant

- Probelauf eines Modells oder eine Probesegmentierung des Testausschnitts: Eingriff `keiner`;
  gehört in den späteren Bau-Wunsch.
- Georeferenzierung der historischen Scans und Bezug weiterer Jahrgänge (BEV-Bestellung):
  außerhalb dieser Ermittlung; e01 und e04 nennen nur, was dafür nötig wäre.
- Gegenden außerhalb Europas, Satellitenbilder unter 1 m Auflösung nur am Rand (e03/e04).
