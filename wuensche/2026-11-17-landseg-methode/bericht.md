# Bericht: landseg-methode (Recherche, Stufe M, Eingriff keiner)

Stand: Auswertung Runde 2, abschließend (2026-11-17). Runde 1 hatte zwei Nachprüfungen angefordert
(n01 Lizenz-Zweitquellen, n02 Mehrjahrgangs-Material); ihr Ergebnis ist eingearbeitet (Abschnitte
2.10, 2.11, Tabelle 2.12). Was danach offen ist, bleibt Lücke (keine weitere Nachprüfung). Alle Pfade
unten relativ zu `C:/Users/Phil/Developement/Victor/wuensche/2026-11-17-landseg-methode/`.

Grundlage: sechs Einheiten (`einheiten/e01.md` … `e06.md`) und zwei Nachprüfungen
(`einheiten/n01.md`, `n02.md`), alle gegengeprüft (`gegenpruefung/*.md`): 107 Befunde nachvollzogen,
davon 98 bestätigt (einige mit Einschränkung), 3 widerlegt bzw. teilweise widerlegt, 6 unklar
(Zählung unten unter „Gegenprüfung"). Als Tatsache steht hier nur Bestätigtes; Entwürfe und
Schätzungen sind als `Entwurf` bzw. `vermutet` gekennzeichnet.

## 1 Antwort

Lückenlosigkeit entsteht nicht durch ein Modell, sondern durch die Datenform: Von Anfang an ist das
Bild eine **Partition** (Label-Karte, jeder Bildpunkt genau eine Segment-ID, 0 verboten), zuerst aus
einer feinen Übersegmentierung (Superpixel/Wasserscheide), in die die automatischen Vorschläge von
**SAM 3** (lokal vorhanden) als Objekte und Klassen einrasten. Claude-Code-Agents arbeiten danach wie
in der Stitcher-Session (Urteil mit Mängel-/Vorschlagsbild → Nutzer bestätigt → direkte Bearbeitung
per Python mit Kante im engen Band → Zusammentragen, Prüfseite, Korrekturrunden), aber je
**Teilkachel mit Kern und Kontextrand** statt je Objekt, und sie geben eine **Label-Karte** statt
Einzelmasken ab. Ein Prüfwerkzeug erzwingt „Summe = H × W, kein Bildpunkt ohne Segment, jede ID genau
eine Klasse". Kategorien: eigene dreistufige Bedeckungsliste (7/25/46 Klassen, Ebene 1 = Bericht 48
plus „nicht bestimmbar"), Nutzung als getrennte Attributschicht. Erster Test: Fenster **T0** (Orthofoto
Kachel 5236-56, x 2000, y 2400, 1000 × 1000 px = 4 ha), danach **H0** im Scan 1968 (gleichwertiges,
nicht dasselbe Gebiet). Vorher wird der Stitcher-Einmal-Code als wiederverwendbarer Werkzeugkasten
gebaut. Echtes Mehrjahrgangsmaterial für dasselbe Gebiet gibt es nicht offen zum Herunterladen; es
kommt später entweder kostenfrei über den Seewinkel (Burgenland-Orthofoto zu den Scans) oder für
Linz-Urfahr per Kauf beim BEV (2.11). Die Lizenzen der Bausteine erlauben den internen Test; vor einer
Veröffentlichung sind SAM-3-Nennung und einige offene Datenlizenzen zu klären (2.12).

## 2 Befunde nach Gewicht

### 2.1 Lückenlosigkeit muss Konstruktionseigenschaft sein (tragend)

- **„Segment everything" deckt Luftbilder nicht lückenlos ab.** SAM 2.1 Automatic Mask Generator:
  samgeo2-Standard 5,8–26,5 % Abdeckung, Einzeldurchgang 53–93 %, beste Mehrfach-Pipeline 91–98 %,
  99 % nicht erreicht; Potsdam-Mosaik ~20 h auf RTX 4090. Superpixel liefern dagegen „exhaustive …
  partitions". Quelle: https://arxiv.org/html/2605.00256 (Preprint) und https://github.com/osmarluiz/sam-mosaic
  (MIT), Abruf 2026-11-17. Beleg `einheiten/e03.md` B8, bestätigt `gegenpruefung/e03.md` B8.
- **Superpixel/Wasserscheide sind lückenlos per Konstruktion** (scikit-image: SLIC in Lab,
  Felzenszwalb, kompakter Watershed auf Gradient, also auch für Graustufen):
  https://scikit-image.org/docs/stable/auto_examples/segmentation/plot_segmentations.html; lokal
  scikit-image 0.26 und OpenCV 4.13 vorhanden. `e03.md` B9/L2, bestätigt.
- **SAM 3 liefert neben Instanzen eine Semantikkarte und einen Presence-Wert** (lokale
  transformers 5.8.1: `modeling_sam3.py:151,173-176`, `processing_sam3.py:538`). Damit lässt sich das
  Verfahren **SegEarth-OV3** (argmax je Bildpunkt über ein Klassenvokabular, trainingsfrei) nachbauen:
  mIoU OpenEarthMap 42,9, LoveDA 47,4, Potsdam 57,8, Vaihingen 60,8, Mittel 8 Datensätze 53,4
  (https://arxiv.org/html/2512.08730v2). Schwächen laut Paper: Kleinobjekte und dünne Linien
  unscharf oder fehlend. Je Klassenprompt ein Durchlauf (Gegenprüfung L6). Repo ohne Lizenzdatei →
  nur Nachbau aus dem Paper. `e03.md` L6/B3, bestätigt.
- **Panoptisches Format erzwingt Überlappungsfreiheit:** COCO-panoptic speichert alle Segmente eines
  Bildes in einer PNG, Konverter nehmen nur überlappungsfreie Daten
  (https://github.com/cocodataset/panopticapi, CONVERTERS.md), id = R + 256·G + 256²·B
  (`panopticapi/utils.py`). `e06.md` B3/B14, bestätigt.

### 2.2 Stitcher-Methode: was übernommen, was geändert wird (tragend)

Belegt aus den gesicherten Originalen (`roh/e05/quellen/`):

- Ablauf dort: SAM3-Keime + Kanten-Rohmaske + Wasserscheide (333 Segmente) → 19 Urteils-Agents
  (je Segment Mängel-/Vorschlagsbild) → Nutzer bestätigt → 6 Agents über die Panel-Schnittstelle
  (verworfen, Haken in `AUFTRAG_UMSETZEN.md:40-55`) → 7 Agents „direkte Maske" per Python →
  1 Agent Zusammentragen + Seite → Korrekturrunden (4 + 1 Agents). Rund 40 Agents, ~6 h Wandzeit für
  eine Kachel. `e05.md` B1/B2, bestätigt (Abbruch des Panel-Wegs: wahrscheinlich).
- Nur 19 von 333 Segmenten (5,7 %) wurden einzeln von Agents bearbeitet, 250 blieben als „klein"
  (< 200 px) im Automatikstand; belegt waren am Ende 14,6 % der Bildpunkte, der Rest war Untergrund
  (Label 0). „Ein Agent je Objekt" trägt also für 100 % Belegung nicht. `e05.md` B3, bestätigt.
- Abgabe dort: Einzelmaske je Objekt + `objekte.json`; Überlappungen löst erst der Bau
  („korrigiert gewinnt", 6 Stellen/811 px), Freies fällt an den Untergrund. Die Zählprobe prüft nur
  „Summe = belegt", nicht „alles belegt" (`kachel_direkt_bau.py:816`). `e05.md` B4/B5, bestätigt.
- Übertragbar unverändert: eingefrorener Datenstand, Ordner je Agent, feste Dateinamen, JSON-Schema,
  Bilder ≤ 2000 px, „nicht raten, offen melden", „geschätzte Kanten melden", Kantenregel „Vorlage
  sagt WAS, Kante aus dem Bild im engen Band", „genau den Kommentar umsetzen, alles andere
  bildpunktgleich", Prüfseite über file:// (Teilbilder 1024 px × 4 Stufen, Vorher/Nachher, Ebene
  „Geändert", Fragen, Kommentar-Export). `e05.md` B6/B9, bestätigt.
- Einmal-Code, der Werkzeug werden muss: `bau.py` mit fest verdrahteten IDs (`ERWARTET`,
  `NUTZER_KLASSE`, `PANEL_ID`), 28 `patch*.py`, je Agent eigene Overlay-/Kanten-Skripte, absolute
  Temp-Pfade. `e05.md` B10, bestätigt.

Tabelle Baustein → übernehmen/ändern/neu und Werkzeugliste W1–W10: `einheiten/e05.md`
(Abschnitte „Tabelle Baustein …" und „Wiederverwendbare Werkzeuge"; Entwurf, nicht erprobt).

### 2.3 Bestand und Testausschnitt

- Orthofoto 5236-55/-56: je 6250 × 5000 px, RGB 8 Bit, **kein Infrarot**, unkomprimiert, 0,2 m,
  EPSG:31255, nahtlos nebeneinander, zusammen 2,5 × 1,0 km. Lage: Linz-Urfahr, Südhang des
  Pöstlingbergs (eigene Rückrechnung zweifach, Petrinum als Bezugspunkt,
  https://en.wikipedia.org/wiki/Petrinum_Linz, https://aroundus.com/p/5920293-petrinum-linz). Sommer
  (Stoppel- und Maisfelder, volle Belaubung). `e01.md` B1–B5, bestätigt; Gegenprüfung ergänzt
  Maisfelder und eine Bahnlinie, Ackeranteil höher als die vermuteten 5 %.
- Scan 1957: 12 513 × 13 237 px, Graustufen (Palette), Kamera 114,76 mm; Scan 1968: 16 283 × 15 750
  px, Graustufen, 1694 dpi (15 µm), 152,07 mm, B.A.f.E.u.V. Bodenauflösung beider rund 0,43–0,47 m
  (**vermutet**, Höhenmesser barometrisch). Rahmen/Marken/Datenstreifen im Bild (bis 10–14 % der
  Bildpunkte), Kratzer, Korn, Hotspot. `e01.md` B7–B9, B12, bestätigt.
- **Die Scans zeigen nicht das Gebiet des Orthofotos** (ebene Seen-/Streifenflur-Landschaft,
  wahrscheinlich Seewinkel – nur Augenschein). Labels lassen sich zwischen Orthofoto und Scans nicht
  übertragen. `e01.md` B10/B11, bestätigt.
- Testfenster **T0** = Kachel 5236-56, x 2000, y 2400, 1000 × 1000 px (E 69 150–69 350,
  N 353 320–353 520): Straße, Zufahrten, ~5–6 Häuser, Pool, Gärten, Hecken, Einzelbäume, Stoppelfeld,
  Wiese, Sukzession, Wald mit Schatten, Kleingartenanlage; erwartet 150–250 Segmente (vermutet).
  Erweiterung T1 1500 × 1500. Kein Gewässer außer Pool, keine Kachelnaht. **H0** = Scan 1968,
  x 1500, y 2000, 1000 × 1000 px (Ortsrand mit Streckhöfen, Anger, Block-/Streifenflur), erwartet
  200–300 Segmente (vermutet). Vorschauen `roh/e01/ortho56_testfenster.jpg`,
  `roh/e01/ortho56_T0_1000px_voll.jpg`, `roh/e01/hist_1968_H0_1000px_voll.jpg`. `e01.md` B13/B14,
  bestätigt (Gegenprüfung: „Hausgärten" und „unbelaubte Bäume" sind in H0 nicht erkennbar).

### 2.4 Kategoriensystem

- Kein europäisches Schema passt unverändert zu 0,2 m: CORINE 5/15/44 Klassen
  (https://land.copernicus.eu/content/corine-land-cover-nomenclature-guidelines/html/; MMU 25 ha nur
  aus Bericht 46, wahrscheinlich), CLC+ Backbone 11 Klassen, 10 m, „Pixel-based (no MMU)"
  (https://library.land.copernicus.eu/products/CLCplus_Backbone_2023_PUM_v1.html), Urban Atlas MMU
  0,25/1 ha, LUCAS trennt Bedeckung und Nutzung
  (https://ec.europa.eu/eurostat/documents/205002/8072634/LUCAS2018-C3-Classification.pdf), LISA
  14 Bedeckungs- / 25 Nutzungsklassen (https://www.corp.at/archive/CORP2011_61.pdf), DKM/BANU-V
  8 Benützungsarten / 23 Nutzungen (https://www.jusline.at/paragraphs/history/456477526), FLAIR #1
  19 Klassen bei 0,2 m (https://ignf.github.io/FLAIR/FLAIR1/flair_1.html), EAGLE „from classification
  to characterisation" (https://land.copernicus.eu/en/eagle). `e02.md` B4–B12, bestätigt.
- Vorschlag (Entwurf): dreistufige Bedeckungsliste 7 / 25 / 46 Klassen (nachgezählt), Ebene 1 =
  Bericht 48 (Versiegelt/bebaut, Acker, Dauergrünland, Wald, Gewässer/Feuchtgebiet, Offener
  Boden/Fels) plus 0 „Nicht bestimmbar" (nur Bildfehler, Scanrand, Wolke); Abweichungen A1–A4
  erklärt (u. a. „Wald und Gehölze" für Hecken/Einzelbäume, Dauerkulturen unter Acker, unbefestigte
  Wege unter Versiegelt). Je Klasse Bildmerkmal, SW-Entscheidbarkeit (vermutet), Abbildung auf
  CORINE/CLC+/FLAIR/DKM/Bericht 48 (eigene Zuordnung, vermutet). Vollständige Tabelle:
  `einheiten/e02.md`, Abschnitt „Vorschlag".
- Regel für Unklares U1–U5: feinste sicher entscheidbare Klasse, sonst Elternklasse mit
  `sicher: nein`; Schatten ist keine Klasse (Fortsetzung der Umgebung); Mischpixel nach Bildkante;
  Objekte unter der Erkennbarkeitsgrenze fallen der Umgebung zu; unklare Nutzung (Wiese/Weide) bleibt
  Attribut `nutzung: unbekannt`, später aus INVEKOS/DKM. Grundsätze G1–G5 (Bedeckung vor Nutzung,
  sichtbare oberste Schicht, keine harte Mindestfläche beim Segmentieren). `e02.md`.
- FLAIR-Lehre: Klassen unter 0,2 % Anteil wurden für die Challenge zusammengelegt → seltene
  Feinklassen gezielt anreichern. `e02.md` B8, bestätigt.

### 2.5 Vorstufe: lokale Lage und Modelle

- GPU RTX 5090 Laptop, 24 GB; stitcher-venv mit torch 2.11 (cu128), transformers 5.8.1 (Klassen
  sam, sam2, sam3, sam3_tracker, mask2former, oneformer, eomt_dinov3 …), OpenCV, scikit-image,
  tifffile; es fehlen rasterio, GDAL, pyproj, geopandas, timm, lightning, mmcv. SAM 3 (3,3 GB) und
  DINOv3 vitb16/vits16 liegen lokal; kein SAM 2, kein DINOv3-SAT. SAM 3 läuft im stitcher in FP16
  mit 12–47 s je 9472 × 6304-Kachel. `e03.md` L1–L5, bestätigt.
- SAM 3: Textprompts als einfache Nominalphrasen, schwächer bei „fine-grained concepts"; Lizenz
  „SAM License" (gebührenfrei, Militär/Spionage verboten, Nennungspflicht bei Veröffentlichung,
  Freistellung; zu Ausgaben als Trainingsdaten kein Verbot gefunden – keine Rechtsauskunft).
  https://github.com/facebookresearch/sam3/blob/main/LICENSE,
  https://huggingface.co/facebook/sam3. `e03.md` B1/B2, bestätigt. Präzisiert durch n01 (2.10): Der
  Text hat keinen eigenen Abschnitt zu Ausgaben; Ausgaben „AS IS", Eigentum an eigenen Derivaten beim
  Nutzer (5.a) – „Ausgaben gehören dem Nutzer" ist Auslegung, nicht Wortlaut.
- FLAIR-HUB-Landbedeckungsmodell (15 Klassen, 63,8 % mIoU, etalab-2.0) braucht RGB+IR; unser
  Orthofoto hat kein IR (e01 B1) → **entfällt** als Vorstufe. `e03.md` B6.
- Zero-Shot-SAM auf historischen SW-Bildern: nur ein Blog-Fallbericht (schwach); HAIR: Modelle auf
  Graustufen schlechter als auf Farbe. `e03.md` B11/B13 (wahrscheinlich bzw. vermutet).
- Späteres Zielmodell: EoMT (MIT, https://github.com/tue-mps/eomt, 58,9 PQ COCO) oder Mask2Former
  mit DINOv3-Backbone; Klassen in transformers vorhanden. `e03.md` B12, bestätigt.

Vergleichstabelle Vorstufe mit Links und Lizenzen: `einheiten/e03.md`, Abschnitt
„Vergleichstabelle Vorstufe".

### 2.6 Offene Daten und Trainingsdatensätze

- Für das Testgebiet offen: BEV DOM/DGM 1 m, ±0,5 m, CC BY 4.0, Stand 15.09.2023
  (https://data.bev.gv.at/geonetwork/srv/api/records/3726b0b8-3cfa-4cf4-a953-a4d32dc24484/formatters/xml)
  → nDOM trennt Bäume/Gebäude von Wiese und hilft bei Schatten; INVEKOS-Schläge CC BY-AT 4.0, 220
  Kulturarten (https://github.com/maja601/EuroCrops/wiki/Austria); BEV-DKM/Gebäude CC BY 4.0
  (Metadaten nur über Suchauszug); OSM unter ODbL mit Share-alike
  (https://www.openstreetmap.org/copyright). Lagegenauigkeit gegen 0,2 m für alle offen.
  `e04.md` B2–B6, bestätigt. Lizenzstand nach n01: Tabelle 2.12 (DKM-Grundstücke jetzt selbst
  geöffnet, ca. 34 GB bundesweit; Gebäude weiter nur Suchauszug; INVEKOS-Variante BY oder BY-AT offen).
- Für historische Bilder taugen diese Daten nicht als Label (anderer Zeitstand, keine Georeferenz).
- Trainingsdaten: FLAIR (0,2 m, Frankreich, Etalab 2.0, https://huggingface.co/datasets/IGNF/FLAIR)
  ist der einzige frei nutzbare 0,2-m-Datensatz; OpenEarthMap (Lizenz je Bildquelle, teils
  CC BY-NC-SA, https://zenodo.org/records/7223446), LoveDA (CC BY-NC-SA 4.0,
  https://github.com/Junjue-Wang/LoveDA), LandCover.ai (CC BY-NC-SA 4.0, 4 Klassen, 216 km²,
  https://landcover.ai.linuxpolska.com/) sind nicht kommerziell. Kein offener europäischer
  Datensatz historischer SW-Luftbilder mit allgemeinen Landbedeckungsklassen gefunden (HAIR: Norwegen,
  Flussräume, Lizenz widersprüchlich). `e04.md` B9–B13.

### 2.7 Güte, Robustheit, Format

- Vorbild FLAIR: Vorsegmentierung (PYRAM) + Expertenlabel je Cluster, interaktiv geändert;
  verdeckte bewegliche Objekte bekommen die Klasse der Fläche darunter
  (https://arxiv.org/html/2211.12979). Kein Datensatz veröffentlicht ein Qualitätsprotokoll; NordFKB
  nennt nur „manual visual quality control" (https://arxiv.org/html/2512.09913v1). → Prüfregeln
  selbst entwerfen. `e06.md` B1/B2, bestätigt.
- Gütemaße: PQ (https://arxiv.org/abs/1801.00868) für lückenlose Segmentierung, Boundary IoU/PQ
  (https://arxiv.org/abs/2103.16562) für Randgüte, z. B. Erstagent gegen Zweitagent. `e06.md` B3/B4.
- Robustheit: Vortraining auf in Graustufen umgerechneten modernen Bildern brachte bei HAIR keinen
  Gewinn gegenüber echten historischen Daten (https://mlanthology.org/dmlr/2024/shamsaliei2024dmlr-highlighting);
  daraus folgt: echte historisch beschriftete Kacheln gehören dazu, Graustufen-Fassungen sind Zusatz,
  nicht Ersatz. Domänenanpassung bringt messbar (Mboga 2021, 60–70 %, https://doi.org/10.3390/ijgi10080523;
  Sagalassos relativ +27,2 %). Augmentation allein verschlechterte FLAIR leicht (0,5335 gegen 0,5443),
  Metadaten je Kachel halfen. `e06.md` B6–B8, bestätigt mit Einschränkungen.
- Label-Übertragung zwischen Jahrgängen leidet an „label ageing"
  (https://isprs-annals.copernicus.org/articles/XI-3-2026/959/2026/) → nur unveränderte Flächen,
  nur georeferenziert. `e06.md` B10.

### 2.8 Widerlegt oder berichtigt (nicht wieder aufwärmen)

- `e02.md` B10: Die DKM-Mindestfläche „200 m², außer Bauflächen" ist falsch. Richtig (§ 4 BANU-V,
  https://www.jusline.at/paragraphs/history/456477528): Gebäude ab 20 m², streifenförmige Elemente ab
  4 m Breite, Wald ab 10 m Breite und 1 000 m², Alpen/Fels/Geröll/vegetationsarm/Gletscher ab
  2 000 m², übrige Nutzungen ab 200 m². `gegenpruefung/e02.md` B10.
- `e04.md` B12: LandCover.ai hat 4 Klassen (Gebäude, Wald, Wasser, Straße) und 216,27 km², nicht
  3 Klassen und 176,76 km². `gegenpruefung/e04.md` B12.
- `e03.md` B6: „FLAIR-HUB in ISPRS J. 2026 veröffentlicht" nicht bestätigt (nur Preprint v2).
- `e06.md` B6: Die Folgerung „Graustufen-Umrechnen reicht nicht" geht über die Quelle hinaus;
  belegt ist nur: als Vortraining kein Gewinn. `e06.md` B7: Sagalassos +27,2 % ist ein relativer
  Zuwachs, nicht Prozentpunkte mIoU.
- Wunsch-Datei, „schon bekannter Ablauf": In der Session vom 17.11. nutzten die Urteils-Agents weder
  Panel noch Kandidaten (`AUFTRAG.md:16`); dazu kam ein verworfener Panel-Umsetzungsweg. `e05.md` B1.
- `n02.md` B4 (Lizenzteil): „DORIS-Daten unter CC BY (Fußzeile/Nutzungsbedingungen)" ist falsch. Die
  Nutzungsbedingungen (https://www.doris.at/service/nutzungsbedingungen.aspx) enthalten weder „CC BY"
  noch „Lizenz", nur „unentgeltlich" und die Quellenangabe „Datenquelle: Land Oö., doris.at"; CC BY 4.0
  steht nur im Metadatensatz des INSPIRE-Downloaddienstes (Record 600C042E…), nicht bei den
  Orthofotos (Record 0206B6C6…: nur „OGDFreigabe"). Die Lizenz der DORIS-Orthofotos ist **offen**.
  `gegenpruefung/n02.md` B4.
- Kleinere Korrekturen der Gegenprüfung n02: Die BEV-Seite „Topics/Remote-Sensing" stützt weder das
  Archiv ab 1949 noch das historische Orthophoto (je nur eine tragende Quelle: Produktseite bzw.
  Metadatensatz); „Lagegenauigkeit schwankt" (DORIS) ist im Abruf nicht zu sehen.
  Gegenprüfung n01: DORIS-DGM-Metadatensatz Revision 2026-05-21 (nicht 2025-10-10).

### 2.9 Unklar

- HILUCS-Klassenzahl und -Regel (`e02.md` B13), Lizenzen von CLC+, Urban Atlas, LISA, Small Woody
  Features (`e04.md` B7/B8), HAIR-Details und -Lizenz (`e04.md` B13), Kostenrechnung (`e05.md` B12,
  reine Schätzung), Bildzahl LoveDA in einem Abruf (`e06.md` B15), ob Ausschnitte aus WMS/WMTS-Diensten
  in voller Auflösung abgegriffen werden dürfen (`n02.md` B12, Abwesenheitsbefund). Keines davon kippt
  den Vorschlag.

### 2.10 Lizenzen der empfohlenen Bausteine (Nachprüfung n01)

`einheiten/n01.md`, alle 8 Befunde bestätigt (`gegenpruefung/n01.md`, drei mit Einschränkung), Abruf
2026-11-17.

- **SAM 3** (Wortlaut nur auf GitHub, „Last Updated: November 19, 2025"): gebührenfrei, weltweit;
  Weitergabe der Gewichte und Derivate nur mit Kopie der Vereinbarung (1.b.i); **Nennungspflicht**
  „you must acknowledge the use of SAM Materials in your publication" (1.b.ii); Ausgaben „AS IS"
  (3); **Freistellung** Metas durch den Nutzer, auch für Ausgaben (5.b); kein Reverse Engineering;
  keine militärischen Zwecke. Kein eigener Abschnitt zur Weitergabe von Masken → nach Textlage nicht
  gesperrt (Auslegung, keine Rechtsauskunft). Zweite Wortlautquelle fehlt: HF-Karte nennt nur
  „License: other" (Text erst nach Anmeldung), lokaler HF-Cache hat keine Lizenzdatei. Sicherheit
  wahrscheinlich. `n01.md` B1/B2.
- **scikit-image** BSD-3-Clause, **opencv-python** Wrapper MIT / OpenCV Apache-2.0 (Wheels bringen
  FFmpeg unter LGPLv2.1 mit, nur bei Weitergabe relevant), **transformers** Apache-2.0: je lokale
  dist-info und Webquelle übereinstimmend. Belegt. `n01.md` B3.
- **BEV ALS-DOM/DGM 1 m** CC BY 4.0, unentgeltlich: zwei BEV-Metadatensätze + BEV-Produktseite;
  unabhängige Drittquelle (INSPIRE-Geoportal) war nicht erreichbar (DNS-Fehler). `n01.md` B4.
- **INVEKOS** CC BY-AT 4.0 mit Pflichtnennung „© Agrarmarkt Austria as a geodata agency" (EuroCrops-Wiki);
  zweite Quelle nur Suchauszug, Variante BY 4.0 oder BY-AT 4.0 uneinheitlich. Wahrscheinlich.
  `n01.md` B5.
- **BEV DKM-Grundstücke** CC BY 4.0, Metadatensatz selbst geöffnet, ca. 34 GB bundesweit (GPKG);
  **BEV-Gebäude** nur Suchauszug (vermutet), Nutzungsflächen-Satz nicht gefunden. `n01.md` B6.
- **DORIS-DGM 0,5 m** CC BY 4.0 (Metadatensatz) gegen CC BY 3.0 (Presseaussendung 2019); der neuere
  Satz gilt, beide erlauben kommerzielle Nutzung, kostenlos. Auflösungsangabe im Satz widersprüchlich
  (0,5 m oder 1 m). `n01.md` B7.
- **SegEarth-OV-3**: keine Lizenzdatei sichtbar → Code nicht übernehmen, nur Nachbau aus dem Paper
  (arXiv 2512.08730). Wahrscheinlich. `n01.md` B8.

### 2.11 Material für „dasselbe Gebiet in mehreren Jahrgängen" (Nachprüfung n02)

`einheiten/n02.md`, 10 von 12 Befunden bestätigt, 1 widerlegt (Lizenzteil B4, siehe 2.8), 1 unklar
(B12) (`gegenpruefung/n02.md`).

- **Kein offen herunterladbarer Mehrjahrgangs-Satz** für dasselbe Gebiet belegt.
- **Linz-Urfahr** (Orthofoto vorhanden): DORIS bietet historische Orthofotos ab 1953 und Luftbilder ab
  1940, meist SW, geringere Auflösung, nicht jedes Jahr flächendeckend
  (https://www.land-oberoesterreich.gv.at/546586.htm, https://www.doris.at/themen/basiskarten/orthofotos.aspx);
  Download nur für den jeweils aktuellsten Bildflug, Altbestände nur als Ansicht (WebGIS/App);
  Sonderanfrage 73,14 EUR/h. Jahrgänge für Linz-Urfahr ungeprüft. `n02.md` B1–B3, B5.
- **BEV**: Luftbildarchiv ab 1949 (ca. 450 000 Aufnahmen, Flüge alle 5–7 Jahre bis 2009), gescanntes
  Luftbild 25 EUR, ohne Georeferenz; **historisches Orthophoto** monochrom 0,5 m, ganz Österreich,
  1 EUR/km² (Jahrgang offen) (https://www.bev.gv.at/en/Services/Products/Remote-Sensing.html,
  https://data.bev.gv.at/geonetwork/srv/api/records/40fc2241-6631-4083-8327-ddd3386b605e/formatters/xml).
  `n02.md` B6–B8.
- **Seewinkel** (Gegenstück zu den Scans): Land Burgenland, Orthofoto 2019 und 2025, 0,2 m, EPSG:31259,
  JPG je Gemeinde, CC BY 4.0 AT, kostenfrei
  (https://geodaten.bgld.gv.at/de/downloads/hoehenmodelle-orthofotos.html; eine Quelle). Dass die
  Scans den Seewinkel zeigen, bleibt Augenschein (`e01.md` B11). `n02.md` B9.
- basemap.at-Orthofoto (29 cm, 15 cm in Detailgebieten, CC BY 4.0) und BEV-WMS (Anmeldung) zeigen nur
  den aktuellen Stand – kein Jahrgangsvergleich. `n02.md` B10/B11.
- Folge für den Vorschlag (Schritt 14): zwei Wege zu echtem Mehrjahrgangsmaterial, beide außerhalb
  des ersten Tests: (a) Seewinkel kostenfrei – Gebiet der Scans bestimmen, georeferenzieren,
  Burgenland-Orthofoto dazu (Kandidat K6); (b) Linz-Urfahr – BEV-Orthophoto historisch (≈ 1 EUR/km²)
  oder BEV-Scan (25 EUR + eigene Georeferenz), DORIS-Altbestände nur nach Anfrage (Kandidat K8, nur mit
  Freigabe).

### 2.12 Lizenz-Übersicht aller empfohlenen Bausteine (AK5)

| Baustein | Lizenz | Quelle 1 | Quelle 2 | Stand |
|---|---|---|---|---|
| SAM 3 Gewichte | SAM License (Nennung, Freistellung, Lizenzkopie bei Weitergabe) | https://github.com/facebookresearch/sam3/blob/main/LICENSE | https://huggingface.co/facebook/sam3 (nur „other") | Wortlaut eine Quelle – wahrscheinlich |
| scikit-image 0.26 | BSD-3-Clause | lokale dist-info `LICENSE.txt` | https://github.com/scikit-image/scikit-image/blob/main/LICENSE.txt | belegt |
| opencv-python 4.13 | MIT / Apache-2.0 (+ FFmpeg LGPLv2.1) | lokale dist-info | https://pypi.org/project/opencv-python/ | belegt |
| transformers 5.8.1 | Apache-2.0 | lokale dist-info | https://github.com/huggingface/transformers/blob/main/LICENSE | belegt |
| SegEarth-OV3 (Methode) | keine Lizenzdatei → nur Nachbau | https://github.com/earth-insights/SegEarth-OV-3 | https://arxiv.org/html/2512.08730v2 | wahrscheinlich |
| EoMT (Zielmodell) | MIT | https://github.com/tue-mps/eomt | `e03.md` (zwei Quellen, Runde 1) | belegt |
| FLAIR-Daten | Etalab 2.0 | https://huggingface.co/datasets/IGNF/FLAIR | `e04.md` (Runde 1) | belegt |
| OSM | ODbL (Share-alike) | https://www.openstreetmap.org/copyright | `e04.md` (Runde 1) | belegt |
| BEV ALS-DOM/DGM 1 m | CC BY 4.0, unentgeltlich | https://data.bev.gv.at/geonetwork/srv/api/records/3726b0b8-3cfa-4cf4-a953-a4d32dc24484/formatters/xml | https://www.bev.gv.at/Services/Downloads/Produktbezogene-Downloads/Unentgeltliche-Produkte/DGM.html | belegt, beide BEV |
| DORIS-DGM 0,5 m | CC BY 4.0 (früher 3.0) | https://doris-metadaten.ooe.gv.at/at.gv.ooe.doris.geonetwork_extern/srv/api/records/68CFE491-7CDF-4781-A1F1-603CD0738ABD/formatters/xml | https://www.land-oberoesterreich.gv.at/214240.htm | wahrscheinlich |
| INVEKOS-Schläge | CC BY-AT 4.0 (oder BY 4.0) | https://github.com/maja601/EuroCrops/wiki/Austria | nur Suchauszug INSPIRE-Satz | wahrscheinlich |
| BEV DKM-Grundstücke | CC BY 4.0 | https://data.bev.gv.at/geonetwork/srv/api/records/13e8a671-a82c-4f29-bcfa-1b3e18e035ce/formatters/xml | Suchauszug BEV-Schnittstellenbeschreibung | belegt (Satz selbst) |
| BEV-Gebäude (DLM Bauwerke) | CC BY 4.0 | nur Suchauszug | – | vermutet |
| DORIS-Orthofoto aktuell / historisch | offen (nur „unentgeltlich", OGD-Freigabe) | https://www.doris.at/service/nutzungsbedingungen.aspx | – | offen |
| Burgenland-Orthofoto 2019/2025 | CC BY 4.0 AT, kostenfrei | https://geodaten.bgld.gv.at/de/downloads/hoehenmodelle-orthofotos.html | – | eine Quelle |
| BEV Orthophoto historisch / Luftbildscan | BEV-Entgelte (1 EUR/km² bzw. 25 EUR) | https://www.bev.gv.at/en/Services/Products/Remote-Sensing.html | Metadatensatz Archiv (CC BY 4.0) | Preis eine Quelle |
| basemap.at-Orthofoto | CC BY 4.0 | https://basemap.at/en | – | eine Quelle |

Abruf aller Einträge 2026-11-17 (Runde 1 bzw. n01/n02). Weitere Vergleichstabellen (Modelle,
Datensätze, Klassensysteme): `e02.md`, `e03.md`, `e04.md`, `e06.md`, `n02.md`.

## 3 Vorschlag: Schritt für Schritt (Synthese, Entwurf)

### 3.1 Vor dem Test (Entscheidungen und Bau)

0. **Entscheidungen** des Nutzers: F1 Feinheit, F2 Zweck der Kategorien, F3 Farbe/SW (Wunsch-Datei),
   dazu F4 Ort des Werkzeugkastens, F5 Abweichungen A3/A4 der Kategorienliste, F6 Nutzung offener
   Hilfsdaten.
1. **Kategorienliste festschreiben** als `kategorien.json` (Code, Name, Eltern, Farbe, SW-Kennzeichen,
   Abbildungen CORINE/CLC+/FLAIR/DKM/Bericht 48) nach `e02.md`, mit den Regeln G1–G5 und U1–U5
   (Kandidat K1).
2. **Werkzeugkasten bauen** (Kandidat K2), aus dem Stitcher-Einmal-Code abgeleitet (`e05.md` W1–W10):
   `kacheln` (Ausschnitt, Teilkachelraster Kern + Kontextrand, Manifest mit Georeferenz, relative
   Pfade), `vorstufe` (siehe 3.2), `ansicht` (Standardbilder roh/umriss/mängel/vorschlag/nah,
   Kontrast, Gitter), `kante` (Einrasten im engen Band, „geschätzt"-Strecken), `eingriff`
   (verschmelzen, teilen entlang Linie, Grenze verschieben, Klasse setzen – immer auf der Label-Karte,
   also immer lückenlos, mit Verlauf), `pruefen`, `zusammentragen`, `seite`, `export`, Auftragsvorlagen
   + Agent-Skill mit den Stitcher-Regeln. Einheiten, Nutzerklassen, offene Fragen kommen aus JSON,
   nicht aus Code.

### 3.2 Erster Test an T0 (Orthofoto, 1000 × 1000 px, 4 ha)

3. **Vorstufe (Skript, GPU, Minuten – vermutet):**
   a. feine lückenlose Übersegmentierung (SLIC in Lab; Wasserscheide auf Gradient) → jede Stelle hat
      eine ID;
   b. SAM 3 mit je einem Textprompt je Kategorie (building, tree, hedge, road, dirt path, field,
      swimming pool …) im Schiebefenster wie im stitcher → Instanzmasken mit Klassenvorschlag;
   c. SAM-3-Semantikkopf + Presence je Prompt, argmax je Bildpunkt (SegEarth-OV3-Nachbau) →
      Klassenvorschlag für Flächen;
   d. Verschmelzen: Instanzen auf Superpixel einrasten (Mehrheit), übrige Superpixel nach
      Semantikkarte klassifizieren und mit gleichklassigen Nachbarn verbinden → `labels` (Segment-ID je
      Bildpunkt) + `segmente.json` (ID, Klasse fein/grob, Herkunft, Sicherheit) + Kandidatenliste
      („Klasse unsicher", „Grenze ohne Bildkante", „nicht zusammenhängend", „zu klein");
   e. `pruefen`: Summe = H × W, kein 0.
   Erwartete Güte nur 43–60 % mIoU (SegEarth-OV3 auf ähnlichen Benchmarks) → Vorschlag, keine
   Annotation.
4. **Urteil je Teilkachel:** T0 in 4 Teilkacheln (Kern 500 × 500 px, Kontextrand 64 px). Je ein Agent
   urteilt über alle Segmente seiner Teilkachel (Klasse auf feinster sicherer Ebene, sonst Eltern;
   Mängel; Vorschlag), mit denselben Bildarten wie im Stitcher-Urteil, Abgabe `urteil.json`.
5. **Nutzer bestätigt die Vorlagen** auf der Prüfseite (im Test; beim Wachsen nur Stichprobe).
6. **Umsetzung direkt per Skript:** je Teilkachel ein Agent ändert die Label-Karte nur im Kern mit
   `eingriff`/`kante` (Kante aus dem Bild im engen Band, geschätzte Kanten melden, nichts raten);
   Abgabe: Label-Karte der Teilkachel + `segmente.json`. Lücken und Überlappungen sind formal
   unmöglich, Nachbarn teilen ihre Grenze.
7. **Zusammentragen + Naht:** globale IDs aus der Vorstufe; an jeder Kerngrenze prüft das Werkzeug
   gleiche ID oder echte Bildkante und gleiche Klasse (Nahtregel, Entwurf `e05.md`). `pruefen`:
   H × W, kein 0, jede ID genau eine Klasse und ein zusammenhängendes Gebiet, Klassen gültig.
8. **Prüfseite** (file://, wie Stitcher) mit Ebenen grob/fein, Lückenkarte, Naht-Ebene, Vorher/Nachher,
   Kommentar-Export; **Korrekturrunden** „genau den Kommentar, alles andere bildpunktgleich".
9. **Messen** (Teil des Tests): Läufe, Wandzeit, Zahl der Segmente, Anteil `sicher: nein`,
   Übereinstimmung Zweitagent gegen Erstagent auf einer Teilkachel (PQ/Boundary-PQ), Nutzerurteil
   je Klasse.
10. **Export:** Master-Label-Karte + `segmente.json` + `kacheln.json` (Jahrgang, Sensor, Farbe/Grau,
    Auflösung, Herkunft, Lizenz, Lage); daraus COCO-panoptic (RGB-codierte IDs), semantische Karte je
    Ebene, Graustufen- und Auflösungsfassung (0,2 → 0,5 m, Labels mit nächstem Nachbarn) desselben
    Ausschnitts (F3). Hinweis zur Bittiefe: `e05.md` schlägt uint32, `e06.md` 16 Bit vor; PNG kennt
    höchstens 16 Bit je Kanal (Allgemeinwissen, nicht recherchiert). 16 Bit reichen für eine
    Orthofoto-Kachel (geschätzt einige Tausend Segmente), nicht sicher für einen ganzen Scan
    (geschätzt bis zu Zehntausende) → Master als RGB-codierte PNG wie COCO-panoptic (bis 16,7 Mio. IDs)
    oder 32-Bit-TIFF (tifffile vorhanden) – Entscheidung im Bau, vermutet.

### 3.3 Danach: H0 (Scan 1968)

11. Gleicher Ablauf auf H0 (1000 × 1000 px ≈ 430 × 430 m, vermutet): Rahmen/Marken/Datenstreifen →
    Klasse 0.1; Übersegmentierung per Wasserscheide auf Gradient; SAM-3-Vorschläge nur als schwache
    Hinweise; Agents entscheiden auf Grauton, Textur, Form; Rückfall auf Elternklasse häufiger. Der
    Lauf misst zugleich, welche Klassen auf SW wirklich entscheidbar sind (Spalte SW in `e02.md` ist
    bisher Vermutung).

### 3.4 Wachstum (nach dem Test)

12. Naht-Fenster über beide Orthofoto-Kacheln (Mosaik-x 6000–7000), dann ganze Kacheln
    (geschätzt ~280–320 Agent-Läufe je Orthofoto-Kachel nach `e05.md`, vermutet).
13. Ab einigen hundert beschrifteten Teilkacheln: eigenes Modell (EoMT/Mask2Former mit
    DINOv3-Backbone, Vortraining mit FLAIR) trainieren und als Vorstufe einsetzen; Agents korrigieren
    nur noch (halbautomatisch wie Bericht 48 Vorgabe 5).
14. Robustheit: echte historisch beschriftete Kacheln (H0 und weitere) als Prüf- und
    Feinabstimmungsmenge; dasselbe Gebiet in mehreren Jahrgängen erst mit passendem Material: offen
    und kostenfrei nur der Seewinkel-Weg (Burgenland-Orthofoto zu den Scans, Kandidat K6), für
    Linz-Urfahr nur Kauf beim BEV oder Anfrage bei DORIS (Kandidat K8) – siehe 2.11;
    Graustufen-/Auflösungs-/Körnungsfassungen als Zusatz, Wirkung messen statt annehmen; Metadaten je
    Kachel.
15. Hilfsebenen (nDOM aus BEV DOM/DGM, INVEKOS, BEV-Gebäude) als Agent-Hinweis und automatische
    Prüfquelle, nicht als Label; OSM nur zur Orientierung (Share-alike, `e04.md` B6). Lagegenauigkeit
    vorher an Stichproben messen (Kandidat K5).

### 3.5 Aufwand (Schätzung, vermutet)

| Posten | Läufe / Aufwand | Grundlage |
|---|---|---|
| K1 Kategorienliste festschreiben | 1 Agent, klein | Entwurf liegt in `e02.md` |
| K2 Werkzeugkasten W1–W10 | groß (mehrere Bau-Läufe) | `e05.md` W1–W10 |
| K3 Test T0 | ≈ 4 Urteile + 4 Umsetzungen + 1–2 Zusammentragen + 2–4 Korrekturen ≈ 11–14 Läufe, ≈ 1–2 h Wandzeit plus Nutzerprüfung | `e05.md` Kostenrechnung (2048er-Ausschnitt ≈ 37–42 Läufe), auf 1000 × 1000 umgerechnet |
| K4 Test H0 + SW-Fassung T0 | ähnlich K3 | wie oben |
| ganzes Orthofoto | ≈ 280–320 Läufe | `e05.md` |

Token- und Geldkosten sind nicht belegbar: Das Stitcher-Transkript enthält keine Nutzungszahlen
(`e05.md` B2). Der Test muss sie messen.

### 3.6 Risiken

- **Dichte je Agent:** Im Stitcher bearbeitete ein Urteils-Agent ein Segment (4–8 min); in T0 kämen
  auf eine 500er-Teilkachel etwa 40–60 Segmente (vermutet). Ob ein Agent das in einem Lauf sauber
  schafft, ist ungeprüft – größtes Risiko. Gegenmittel: kleinere Teilkacheln (250 px) oder Urteil nur
  über die Kandidaten der Vorstufe.
- Dünne Linien (Hecken, Raine, Wege) und Kleinobjekte sind die bekannte Schwäche der Vorstufe
  (SegEarth-OV3); Schatten und Kronenüberdeckung brauchen die Regeln U2/G2.
- Historische SW-Scans: Zero-Shot-Vorstufe schwach, Bodenauflösung nur geschätzt, Streifenfluren an
  der Auflösungsgrenze.
- Nahtregel und Kostenrechnung sind unerprobter Entwurf.
- Lizenz: SAM-3-Lizenz (Nennungspflicht bei Veröffentlichung, Weitergabe nur mit Lizenztext,
  Freistellung Metas), OSM-Share-alike, nicht kommerzielle Fremddatensätze, offene Lizenz der
  DORIS-Orthofotos (auch des vorhandenen Testbilds, falls es von DORIS stammt – ungeprüft). Für den
  internen Test unkritisch; vor einer Veröffentlichung des Datensatzes oder Modells Rechtsprüfung
  (Tabelle 2.12). Keine Rechtsauskunft.
- Stitcher-Quellen liegen in einem Temp-Ordner; die wichtigsten sind nach `roh/e05/quellen/`
  gesichert (`roh/` ist nicht versioniert).

### 3.7 Alternativen

| Alternative | Vorteil | Nachteil | Beleg |
|---|---|---|---|
| A: Rückfallweg nur Übersegmentierung + Agent-Urteil (ohne SAM) | modellfrei, SW-tauglich, einfach | mehr Agent-Arbeit, langsamer | `e03.md` Empfehlung |
| B: SAM 2.1 „segment everything" mit Mehrfachdurchgang (sam-mosaic) | ausgereifte Pipeline mit Nahtregel | 91–98 % Abdeckung, nie lückenlos; neue Umgebung (rasterio, SAM2-Fork), keine Klassen | `e03.md` B8 |
| C: Stitcher wörtlich (ein Agent je Objekt, Einzelmasken) | bewährt | bei 150–250 Segmenten je 4 ha zu viele Läufe; Lücken/Überlappungen entstehen durch das Format | `e05.md` B3/B4 |
| D: FLAIR-HUB-Modell als Vorstufe | fertige 15-Klassen-Karte, etalab-2.0 | braucht IR, unser Orthofoto ist RGB | `e03.md` B6, `e01.md` B1 |
| E: samgeo (segment-geospatial) | GeoTIFF/Vektor-Ausgabe fertig | eigene Umgebung, SAM 3 unter Windows „tricky", nicht lückenlos | `e03.md` B5 |

## 4 Gegenprüfung (Zahlen)

| Einheit | Befunde | bestätigt | widerlegt | unklar |
|---|---|---|---|---|
| e01 Bestand | 14 | 14 (3 mit Einschränkung) | 0 | 0 |
| e02 Kategorien | 14 | 12 | 1 teilweise (B10) | 1 (B13) |
| e03 Vorstufe | 19 | 19 | 0 | 0 |
| e04 Offene Daten | 13 | 10 | 1 (B12) | 2 (B8 teils, B13) |
| e05 Stitcher | 12 | 11 | 0 | 1 (B12 Schätzung) |
| e06 Güte/Format | 15 | 14 | 0 | 1 (B15 teils) |
| n01 Lizenzen | 8 | 8 (3 mit Einschränkung) | 0 | 0 |
| n02 Mehrjahrgang | 12 | 10 | 1 (B4 Lizenzteil) | 1 (B12) |
| **Summe** | **107** | **98** | **3** | **6** |

Runde 1: keine Gegenprüfung forderte eine Nachprüfung an, der Auswerter forderte n01 und n02 an.
Runde 2: keine weitere Nachprüfung (Regel), offene Punkte sind Lücken (Abschnitt 5).

## 5 Abdeckung

- 8/8 Einheiten (6 + 2 Nachprüfungen) mit Rückmeldung und Gegenprüfung; alle sechs Teilfragen
  beantwortet.
- **AK1–AK4, AK6:** erfüllt (Abschnitte 2.3, 2.4, 3, Quellen je Aussage, Unbelegtes markiert).
- **AK5 weitgehend erfüllt, Restlücke:** Alle empfohlenen Bausteine stehen mit Link und Lizenz in
  Tabelle 2.12. Zwei unabhängige Quellen fehlen weiter für: SAM-3-Wortlaut (zweite Stelle nur nach
  Anmeldung bei HF – Eingriff keiner), BEV DOM/DGM (zweite Quelle auch BEV; INSPIRE-Geoportal nicht
  erreichbar), INVEKOS und BEV-Gebäude (nur Suchauszüge, gleicher Grund), Burgenland-Orthofoto und
  basemap.at (eine Quelle), DORIS-Orthofoto-Lizenz (offen, siehe 2.8). Für den internen Test hängt
  daran nichts; vor Veröffentlichung zu klären.
- Robustheit: Material für „dasselbe Gebiet in mehreren Jahrgängen" geklärt (2.11) – kein offener
  Satz; Wege mit Kosten bzw. mit Georeferenzarbeit benannt. Jahrgangsliste und Auflösung der
  DORIS-Altbestände für Linz-Urfahr, Scanauflösung BEV, Stadt-Linz-Geoportal, Abgreifregeln für
  WMS/WMTS: ungeprüft (nur per Anfrage oder Anmeldung, Budget).
- Nicht geprüft (Grund): Probelauf von Modellen und Probesegmentierung (Eingriff keiner), Laufzeit und
  Güte der Vorstufe auf T0/H0, Lagegenauigkeit offener Daten (kein Download), Georeferenz und genaue
  Lage der Scans (nicht geplant), Token-Kosten (keine Zahlen im Transkript), EUNIS, Prithvi/SatMAE/Clay,
  Potsdam/Vaihingen/DeepGlobe, Mask2Former-/panopticapi-Lizenz (Budget), Rechtsauskunft (außerhalb).

## 6 Kandidaten

Siehe Wunsch-Datei, Abschnitt „Kandidaten" (K1–K8).
