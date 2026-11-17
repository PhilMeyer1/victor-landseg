# 47 – Räumliche Genauigkeit der österreichischen Wildbienen-Funddaten (1900–2020er)

Stand: 17.11.2026 · Datengrundlage: `tmp/sai_at/analysis/out_v3/14_occ_merged.tsv.gz` (170.893 Funde ab 1900; Pittioni-QC, Linz, CLIMBEE, GBIF-Experten, GBIF-Citizen-Science, EBHD) plus Rohmetadaten aus dem GBIF-Download 0008856, EBHD `Bee_DB_2025-12-17.rds` und der Pittioni-QC-Kartei.
Skripte und Tabellen: `tmp/sai_at/landuse_fine/precision/` (`00_ebhd_extract.R`, `01_precision_audit.py`, `02_gazetteer_diagnostics.py`, `03_figure.py`; Tabellen `t1`–`t8`, `results.json`, `records_precision.tsv.gz` mit der Unschärfe je Fund).

**Frage:** Auf welcher räumlichen Ebene lässt sich Landnutzung mit den Bienendaten verknüpfen – Parzelle/Feldstück, 500-m–1-km-Landschaft, Katastral-/Gemeindeebene oder nur 10 km?

## Kurzfassung

| Periode | Funde ≤ 250 m | ≤ 1 km (konservativ / strikt) | ≤ 5 km | Realistische Skala für die Landnutzungs-Verknüpfung |
|---|---|---|---|---|
| vor 1960 | **0,7 %** | 35 % / 17 % | 98,6 % | **Gemeinde / 5–10-km-Zelle**; 1 km nur Linz (8 Standorte) und ausgewählte Fundorte |
| 1960–1999 | **3,6 %** | 61 % / 13 % | 97,2 % | **Gemeinde / 5–10 km**; 1-km-Landschaft nur als Sensitivitätsanalyse |
| ab 2000 | **52 %** (2020er: 76 %) | 64 % | 99,7 % | Ab ca. 2010: **Feldstück / 250-m-Puffer** möglich; 2000er noch überwiegend Ortschaftsniveau |

- In den 759 Analyse-Einheiten (10 km × Dekade, ≥ 15 Arten, ≥ 5 Sammeltage) stammen vor 1960 nur **0,5 %** und 1960–1999 **2,8 %** der Art-Vorkommen aus Funden ≤ 250 m. Mit nur ≤ 250-m-Funden blieben **0 von 195** (vor 1960), **9 von 348** (1960–99) und **71 von 216** (ab 2000) Einheiten bestehen.
- Die „≤ 1 km“-Funde vor 2000 sind fast ausschließlich (a) ZOBODAT-Datensätze mit dem pauschalen Standardwert 500 m (96 % aller ZOBODAT-Funde vor 2000; 56 % liegen auf Koordinaten mit ≥ 50 Funden, d. h. Fundortpunkte) und (b) die Linz-Standortpolygone. Behandelt man den 500-m-Standardwert als Ortschaftspunkt („strikt“), sinkt der ≤ 1-km-Anteil auf 13–17 %.
- **Keine Rasterkoordinaten** (KFKM-Grundfeld-/Quadrantenzentren, UTM- oder EEA-10-km-Zentren, UTM-1-km-Zentren: jeweils ≈ 0 %). Typische Artefakte sind stattdessen **Gazetteer-/Ortschaftspunkte** (Pittioni 51 % ≤ 150 m an einem GeoNames-Punkt, Nullmodell 10 %; EBHD 23–29 % vs. 4–5 %) und **Minuten-Rundung** (9–19 % der GBIF-Experten-/EBHD-Funde).
- **Empfehlung:** Hauptanalyse bleibt auf **Gemeinde-/5–10-km-Ebene** mit Gemeinde-Agrarstatistik (historisch) bzw. CORINE/HILDA+ zu Zellen aggregiert. Feine Skalen (Parzelle, 250–500 m) nur in **Teildatensätzen mit GPS/Polygonen** (CLIMBEE, BINATS, Linz, Resurvey 2028) – dort Franziszeischer Kataster ↔ Resurvey-Standort und INVEKOS ↔ aktuelle Funde. Unschärfe als Puffergröße bzw. Messfehler-/Gewichtungsterm modellieren, nicht wegfiltern.

![Genauigkeitsklassen je Dekade](../tmp/sai_at/landuse_fine/precision/fig1_precision_by_decade.png)

*Abb. 1: Anteil der Genauigkeitsklassen je Dekade. A: alle Funde ohne Citizen Science. B: Art × Analyse-Einheit, bester verfügbarer Fund (konservativ). C: wie B, strikt (500-m-Standardwert vor 2000 = Ortschaftspunkt). Zahlen unter den Balken: n.*

## 1 Methode der Genauigkeitsbestimmung

Je Fund wurden vier Unschärfe-Werte (Radius in m) bestimmt:

| Variante | Definition |
|---|---|
| **explizit** | nur Metadaten: GBIF/EBHD `coordinateUncertaintyInMeters`; CLIMBEE = Plot-GPS (30 m); Linz rezent = Polygon-Referenzpunkt, Fang im Polygon (250 m); Linz historisch = Etikett → Standortpolygon des Linz-Papers (1 km); Pittioni `locality` = Fundortkatalog-/Ortschaftspunkt (3 km), `municipality` = Gemeindepunkt (5 km), `region` (20 km). Sonst „unbekannt“. |
| **nominal** | explizit; Lücken aus `coordinatePrecision` bzw. Dezimalstellen (halbe Diagonale der Rundungszelle: 2 Dez. ≈ 0,7 km, 1 Dez. ≈ 7 km). |
| **konservativ** (Hauptvariante) | nominal, heraufgesetzt bei Artefakten: GeoNames-Punkt ≤ 150 m (Ortschaft/Flur: ≥ 2 km; Gemeinde/ADM3: ≥ 5 km; nicht für CLIMBEE/Linz), KFKM-Grundfeld/UTM-10-km-Zentrum (8 km), KFKM-Quadrant (4,2 km), volle Bogenminuten (1,1 km), UTM-1-km-Zentrum (0,7 km), Dezimalstellen gröber als angegebene Unschärfe; **EBHD und GBIF-Experten vor 2000 ohne Unschärfeangabe ≥ 2 km** (s. u.). |
| **strikt** (Sensitivität) | konservativ; zusätzlich der pauschale Wert 500 m vor 2000 → ≥ 2 km (Ortschaftspunkt). |

**Warum EBHD ohne Angabe ≥ 2 km?** 89–97 % der österreichischen EBHD-Funde haben keine Unschärfe, aber ≥ 4 Dezimalstellen. Sie stammen zu 79–96 % aus der BDFGM-Bombus-Datenbank (Mons) und liegen deutlich gehäuft an Gazetteer-Punkten: innerhalb 500 m eines GeoNames-Punkts +23 bis +28 Prozentpunkte über dem Nullmodell (Punkte 2 km zufällig verschoben). Zum Vergleich: echte GPS-Plots (CLIMBEE) +14 pp (Plots liegen real oft nahe benannten Orten), Pittioni (bekannt ortschaftsgenau) +26 pp (`t8_gazetteer_excess.tsv`). Viele Dezimalstellen zeigen nur Präzision, nicht Genauigkeit.

Vorfilter im Merge: Funde mit angegebener Unschärfe > 5 km wurden bereits beim Zusammenführen entfernt (Rohdaten: 2.287 GBIF-, 5.191 EBHD-Datensätze vor Duplikatbereinigung). Die Klasse „> 5 km“ enthält daher nur abgeleitete grobe Fälle.

## 2 Verteilung je Quelle und Periode (Aufgabe 1)

### 2.1 Nur Metadaten („explizit“, % der Funde)

| Quelle | Periode | n | ≤ 100 m | ≤ 250 m | ≤ 1 km | ≤ 5 km | > 5 km | unbekannt |
|---|---|---|---|---|---|---|---|---|
| CLIMBEE | ≥ 2000 | 3.856 | 100 | 0 | 0 | 0 | 0 | 0 |
| Linz | < 1960 | 6.356 | 0 | 0 | 100 | 0 | 0 | 0 |
| Linz | 1960–99 | 4.268 | 0 | 0 | 100 | 0 | 0 | 0 |
| Linz | ≥ 2000 | 1.586 | 0 | 100 | 0 | 0 | 0 | 0 |
| Pittioni | < 1960 | 13.192 | 0 | 0 | 0 | 100 | 0 | 0 |
| GBIF Experten | < 1960 | 12.264 | 0,4 | 2,3 | 86,0 | 8,5 | 0 | 2,9 |
| GBIF Experten | 1960–99 | 39.711 | 1,6 | 4,1 | 89,4 | 3,8 | 0 | 1,1 |
| GBIF Experten | ≥ 2000 | 24.659 | 37,6 | 6,5 | 47,7 | 2,8 | 0 | 5,4 |
| GBIF Citizen Science | ≥ 2000 | 26.652 | 61,1 | 6,7 | 6,3 | 2,4 | 0 | 23,5 |
| EBHD | < 1960 | 9.262 | 0 | 0,1 | 2,5 | 0,2 | 0 | **97,2** |
| EBHD | 1960–99 | 11.504 | 0 | 1,0 | 5,6 | 0,1 | 0 | **93,3** |
| EBHD | ≥ 2000 | 17.582 | 0,5 | 9,3 | 1,4 | 0,1 | 0 | **88,7** |
| **Alle** | < 1960 | 41.074 | 0,1 | 0,7 | 41,7 | 34,7 | 0 | 22,8 |
| **Alle** | 1960–99 | 55.484 | 1,1 | 3,1 | 72,8 | 2,8 | 0 | 20,1 |
| **Alle** | ≥ 2000 | 74.335 | 39,7 | 8,9 | 18,4 | 1,8 | 0 | 31,2 |

Verwendete Unschärfewerte (`t2b_unc_values.tsv`): GBIF-Experten und EBHD vor 2000 zu 83–89 % exakt **500 m** (ZOBODAT-/EBHD-Georeferenzierungsklasse), EBHD ab 2000 zu 82 % 200 m; Citizen Science 2–15 m (GPS).

### 2.2 Konservativ abgeleitet (Hauptvariante, % der Funde)

| Quelle | Periode | n | ≤ 100 m | ≤ 250 m | ≤ 1 km | ≤ 5 km | > 5 km |
|---|---|---|---|---|---|---|---|
| CLIMBEE | ≥ 2000 | 3.856 | 100 | 0 | 0 | 0 | 0 |
| Linz | < 1960 / 1960–99 | 10.624 | 0 | 0 | 100 | 0 | 0 |
| Linz | ≥ 2000 | 1.586 | 0 | 100 | 0 | 0 | 0 |
| Pittioni | < 1960 | 13.192 | 0 | 0 | 0 | 99,9 | 0,1 |
| GBIF Experten | < 1960 | 12.264 | 0,4 | 2,0 | 63,9 | 29,7 | 4,1 |
| GBIF Experten | 1960–99 | 39.711 | 1,4 | 3,4 | 68,4 | 23,3 | 3,5 |
| GBIF Experten | ≥ 2000 | 24.659 | 35,2 | 5,6 | 30,2 | 28,3 | 0,7 |
| GBIF Citizen Science | ≥ 2000 | 26.652 | 75,0 | 6,0 | 6,0 | 13,0 | 0 |
| EBHD | < 1960 | 9.262 | 0 | 0,1 | 1,7 | 97,4 | 0,7 |
| EBHD | 1960–99 | 11.504 | 0 | 0,8 | 4,3 | 93,7 | 1,2 |
| EBHD | ≥ 2000 | 17.582 | 0,1 | 7,9 | 0,9 | 90,9 | 0,2 |
| **Alle** | < 1960 | 41.074 | 0,1 | 0,6 | 34,9 | 62,9 | 1,4 |
| **Alle** | 1960–99 | 55.484 | 1,0 | 2,6 | 57,5 | 36,1 | 2,8 |
| **Alle** | ≥ 2000 | 74.335 | 43,8 | 8,0 | 12,4 | 35,6 | 0,3 |
| *Alle, strikt* | < 1960 | | 0,1 | 0,6 | 16,3 | 81,6 | 1,4 |
| *Alle, strikt* | 1960–99 | | 1,0 | 2,6 | 9,8 | 83,8 | 2,8 |

Nominal (nur Dezimalstellen zum Auffüllen) sähe EBHD zu ~90 % „≤ 100 m“ aus – das ist nach der Gazetteer-Diagnose ein Präzisionsartefakt.

### 2.3 Je Dekade (konservativ, ohne Citizen Science; `t1_conserv_decade_expert.tsv`)

| Dekade | n | ≤ 100 m | ≤ 250 m | ≤ 1 km | ≤ 5 km | > 5 km |
|---|---|---|---|---|---|---|
| 1900er | 2.161 | 0 | 0 | 24,1 | 73,5 | 2,4 |
| 1910er | 2.460 | 0 | 0,2 | 57,2 | 40,7 | 1,8 |
| 1920er | 3.079 | 0,2 | 0,1 | 62,2 | 35,9 | 1,6 |
| 1930er | 11.354 | 0,1 | 0,6 | 25,2 | 72,3 | 1,9 |
| 1940er | 13.538 | 0,2 | 0,2 | 24,6 | 74,3 | 0,7 |
| 1950er | 8.482 | 0,1 | 1,7 | 51,0 | 45,9 | 1,4 |
| 1960er | 12.742 | 0,1 | 0,5 | 67,4 | 28,6 | 3,5 |
| 1970er | 7.385 | 0,4 | 0,9 | 60,5 | 31,5 | 6,7 |
| 1980er | 15.713 | 1,4 | 5,5 | 58,4 | 32,9 | 1,8 |
| 1990er | 19.643 | 1,5 | 2,4 | 49,3 | 45,2 | 1,7 |
| 2000er | 23.058 | 2,1 | 2,6 | 15,9 | 78,9 | 0,5 |
| 2010er | 7.039 | 14,9 | 20,2 | 19,7 | 44,2 | 1,0 |
| 2020er | 17.586 | 62,6 | 13,4 | 14,5 | 9,5 | 0 |

Die 1930er/40er sind von Pittioni (Ortschaft/Gemeinde) dominiert, die 2000er von BDFGM-Bombus (EBHD ohne Unschärfe). Der Sprung zu GPS-genauen Daten erfolgt erst in den **2010er/2020er Jahren**.

### 2.4 Artefakte: Zentroide, Raster, Rundung (`t2_artefacts_source_period.tsv`, `t3_top_coordinates.tsv`)

| Quelle | Periode | GeoNames-Punkt ≤ 150 m (Nullmodell) | davon Gemeinde-Punkt | volle Bogenminute | ≤ 2 Dezimalstellen | Funde auf Koordinaten mit ≥ 50 Funden |
|---|---|---|---|---|---|---|
| Pittioni | < 1960 | **50,9 %** (10,2) | 14,5 % | 9,8 % | 25,1 % | 85 % |
| EBHD | < 1960 | 29,1 % (5,1) | 1,6 % | 8,6 % | 4,3 % | 11 % |
| EBHD | 1960–99 | 23,2 % (4,2) | 1,5 % | 8,5 % | 2,4 % | 12 % |
| GBIF Experten | < 1960 | 18,7 % (6,4) | 1,1 % | 13,0 % | 15,0 % | 58 % |
| GBIF Experten | 1960–99 | 14,5 % (5,2) | 0,8 % | 15,1 % | 16,5 % | 51 % |
| GBIF Experten | ≥ 2000 | 15,4 % (6,5) | 0,8 % | 18,9 % | 6,5 % | 22 % |
| GBIF CS | ≥ 2000 | 11,0 % (7,0) | 0,6 % | 0 % | 0,4 % | 4 % |
| CLIMBEE | ≥ 2000 | 18,5 % (4,6) | 0 % | 0 % | 0 % | 81 % (Plots) |

- **Rasterkoordinaten:** KFKM-Grundfeld- (10′×6′) und Quadrantenzentren (5′×3′), UTM-10-km-, EEA-10-km- und UTM-1-km-Zentren kommen praktisch nicht vor (≤ 0,7 %, im Nullmodell-Bereich). Die AT-Daten sind punktgeoreferenziert, nicht rasterbasiert.
- **Zentroid-/Fundortpunkte:** 45.083 verschiedene Koordinaten; 37 % aller Funde liegen auf Koordinaten mit ≥ 50 Funden, 21 % auf solchen mit ≥ 200, die 40 häufigsten Koordinaten tragen 18 % aller Funde. Darunter Linz-Standorte (bis 4.403 Funde), „48.05/15.13“ und „47.8/13.08“ (2-Dezimal-Ortspunkte, je > 1.000 Funde über 40–70 Jahre), Wien-Stammersdorf, Botanischer Garten Wien, Ybbsitz.
- **Gemeinde-Mittelpunkte** (GeoNames ADM3) treffen nur bei Pittioni in nennenswertem Umfang (14,5 %); sonst ~1 %. Häufiger sind Ortschafts-/Flurpunkte (PPL, Berge, Gewässer).

## 3 Gewichtung nach Analyse-Einheiten (Aufgabe 2)

Basis: 759 Einheiten der Hauptanalyse (Version „expert“, 10-km-LCC-Zelle × Dekade, ≥ 15 Arten mit Index, ≥ 5 Sammeltage; Rekonstruktion stimmt zu 100 % mit `15_cell_units_decade.tsv` überein).

| Periode | Einheiten | Gewicht | ≤ 100 m | ≤ 250 m | ≤ 1 km | ≤ 5 km | > 5 km |
|---|---|---|---|---|---|---|---|
| < 1960 | 195 | Funde | 0 | 0,3 | 38,4 | 60,0 | 1,3 |
| | | Einheit gleichgewichtet | 0 | 0,7 | 35,7 | 59,9 | 3,7 |
| | | Art × Einheit (bester Fund) | 0 | 0,5 | 43,4 | 54,0 | 2,1 |
| | | Art × Einheit, **strikt** | 0 | 0,5 | 16,6 | 80,8 | 2,1 |
| 1960–99 | 348 | Funde | 1,0 | 2,6 | 62,5 | 30,9 | 3,0 |
| | | Einheit gleichgewichtet | 0,6 | 1,5 | 58,4 | 36,4 | 3,1 |
| | | Art × Einheit (bester Fund) | 1,2 | 1,6 | 68,0 | 26,3 | 2,9 |
| | | Art × Einheit, **strikt** | 1,2 | 1,6 | 8,0 | 86,3 | 2,9 |
| ≥ 2000 | 216 | Funde | 33,2 | 14,4 | 19,8 | 32,1 | 0,5 |
| | | Einheit gleichgewichtet | 24,1 | 6,9 | 23,6 | 44,5 | 0,9 |
| | | Art × Einheit (bester Fund) | 30,3 | 13,6 | 23,7 | 31,8 | 0,6 |

**Einheiten, die mit nur genauen Funden weiterhin die Kriterien erfüllen** (`t5_units_surviving_threshold.tsv`):

| max. Unschärfe | < 1960 (von 195) | 1960–99 (von 348) | ≥ 2000 (von 216) |
|---|---|---|---|
| ≤ 100 m | 0 | 2 | 54 (25 %) |
| ≤ 250 m | 0 | 9 (3 %) | 71 (33 %) |
| ≤ 1 km konservativ | 81 (42 %) | 237 (68 %) | 129 (60 %) |
| ≤ 1 km strikt | 20 (10 %) | 28 (8 %) | 129 (60 %) |
| ≤ 5 km | 188 (96 %) | 342 (98 %) | 215 (99,5 %) |

## 4 Realistische Analyseskala je Periode (Aufgabe 3)

### 4.1 Feinere Zellen (`t6_finer_grids.tsv`; Kriterium je Einheit wie oben)

| Zelle | max. Unschärfe | Variante | Einheiten Zelle × Dekade (< 1960 / 60–99 / ≥ 2000) | Zellen mit ≥ 2 Dekaden | Zellen mit historisch **und** ≥ 2000 |
|---|---|---|---|---|---|
| 1 km | 250 m | – | 65 (0 / 6 / 59) | 6 | **0** |
| 1 km | 1 km | konservativ | 430 (107 / 226 / 97) | 71 | 12 |
| 1 km | 1 km | strikt | 160 (32 / 31 / 97) | 15 | 9 |
| 2 km | 1 km | konservativ | 446 (108 / 233 / 105) | 82 | 18 |
| 2 km | 1 km | strikt | 169 (32 / 32 / 105) | 15 | 9 |
| 2 km | 5 km | – | 743 (240 / 326 / 177) | 131 | 33 |
| 5 km | 5 km | – | 811 (223 / 361 / 227) | 174 | 47 |
| 10 km | 5 km | – | 745 (188 / 342 / 215) | 159 | 53 |
| 10 km | alle | (Hauptanalyse) | 759 (195 / 348 / 216) | 162 | 53 |

Mit drei Perioden statt Dekaden: 10 km 697 Einheiten / 80 Zellen historisch + rezent; 5 km (≤ 5 km) 781 / 72; 1 km (≤ 1 km, strikt) 137 / 9.

Hinweis: Eine 2-km-Zelle mit Funden „≤ 5 km“ ist formal möglich, aber räumlich nicht ehrlich (Fehlzuordnung zu Nachbarzellen); ab Unschärfe > Zellgröße/2 sollte die Zelle nicht kleiner als ~5 km gewählt werden.

**Standorte (Fundkoordinate bzw. 250-m-Zelle × Dekade, Unschärfe ≤ 250 m, ≥ 15 Arten, ≥ 5 Tage; `t7_sites.tsv`):** 54 Standort-Dekaden, davon 0 vor 1960, 2 in 1960–99, 52 ab 2000 (GBIF-Experten-Erhebungen, EBHD-2000er mit 200-m-Angabe, Linz-Resurvey).

### 4.2 Bewertung der vier Skalen

| Skala | vor 1960 | 1960–1999 | ab 2000 |
|---|---|---|---|
| (a) Parzelle/Feldstück ≤ 100–250 m | **nein** (0,5 % der Art-Info) | **nein** (2,8 %) | ab 2010 ja (44 % der Art-Info, 71 Einheiten bzw. 52 Standort-Dekaden); 2000er kaum |
| (b) Landschaft 500 m–1 km | nur Linz (8 Polygone) + ZOBODAT-Punkte, wenn 500 m geglaubt wird; strikt 17 % der Art-Info, 32 1-km-Zellen | wie vor 1960; strikt 8 % | ja (68 % der Art-Info) |
| (c) Katastral-/Gemeindeebene | **ja** – ≤ 5 km deckt 96–98 % der Einheiten; AT-Gemeinde Ø ≈ 40 km² (Ersatzradius ≈ 3,6 km), Katastralgemeinde Ø ≈ 11 km² (≈ 1,9 km) → Gemeinde passt, KG nur für ~40 % (konservativ) bzw. ~15 % (strikt) | **ja** | ja |
| (d) 10 km | ja (Hauptanalyse) | ja | ja |

**Konsequenz für Veränderungsanalysen:** Auf 1-km-Ebene gibt es nur 9–12 Zellen mit historischen *und* rezenten Daten – zu wenig für eine flächige Analyse, aber genug für eine **Fallstudien-Ebene**. Auf 5–10-km-Ebene sind es 47–80 Zellen.

### 4.3 Teildatensätze, die feine Skalen tragen

| Teildatensatz | Genauigkeit | Umfang | Eignung |
|---|---|---|---|
| **CLIMBEE** 2021–22 | Plot-GPS (≤ 100 m) | 3.856 Funde, 76 Plots in 11 Gemeinde-Clustern; 37 Plots ≥ 15 Arten | Parzelle/Feldstück + 250–500-m-Puffer; INVEKOS/CORINE/Habitatkartierung |
| **BINATS** 2017–18 | 625 × 625-m-Testflächen (Raps/Mais, Koordinaten der Flächenmitte) | 1.035 Funde (ohne *Apis*), 70 Flächen, Median 6 Arten/Fläche, 18 Flächen ≥ 15 Arten; **nicht** im Merge | Landschaftsebene 625 m; INVEKOS-Feldstücke innerhalb der Fläche; als artenarme Agrarreferenz |
| **Linz** | 8 Standortpolygone (historisch 1910–1990er: 10.624 Funde; Resurvey 2018/2021: 1.586) | alle 8 Standorte ≥ 15 Arten historisch und rezent | einziger historischer Datensatz auf ~0,5–1-km-Landschaftsebene; Franziszeischer Kataster/historische Luftbilder je Polygon |
| **Pittioni-Flurnamen** | Kartei: 0 Funde mit Fundplatz-Koordinate; 57 % der AT-Funde mit Ortsteil/Flurname im Fundort (184 Namen, z. B. Stammersdorf, Türkenschanze, Eichkogel, Bisamberg, Hohe Salve, Rotgraben); ~2.900 Funde mit Berg-/Flur-artigen Namen | 14.965 AT-Funde, 39 % `ungenau`-Vermerk | Nachgeoreferenzierung auf 0,5–2 km für die Top-Fundorte lohnend (Flurname ≠ Parzelle: Berge/Täler sind km-groß) |
| **Resurvey 2028** | Kandidaten: 32 Ortschafts-, 40 Gemeindeniveau (`25_resurvey_candidates.tsv`) | 72 Kandidaten | Neue Erhebung mit GPS → feldgenau; Verknüpfung historisch ↔ rezent aber nur so genau wie der historische Fundort (≈ Ortschaft) |
| GBIF-Experten ab 2000 | Biodiversitätsdatenbank Salzburg 68 % ≤ 250 m, NP Hohe Tauern 72 %, Donau-Auen 100 %, ZOBODAT 24 % | | aktuelle Feinskalen-Analysen (2010+) |

## 5 Empfehlung für die Verknüpfung mit Landnutzung (Aufgabe 4)

**Grundsatz:** Die Landnutzungs-Auflösung muss zur *gröbsten* Periode passen, die verglichen wird. Für Zeitvergleiche seit 1900 ist das die **Gemeinde- bzw. 5–10-km-Ebene**; feinere Ebenen nur in Teilstudien oder als Sensitivität.

1. **Hauptanalyse (alle Perioden): Zellen bzw. Gemeinden, nicht Punktpuffer.** 10-km-Zellen (bestehend) oder 5-km-Zellen (811 Einheiten, 47–72 Zellen historisch + rezent). Landnutzung je Zelle aus flächengewichteter **Gemeinde-Agrarstatistik** (historisch, Arbeitsannahme: Betriebs-/Anbauerhebungen auf Gemeindeebene) und **HILDA+/CORINE** (100 m ab 1990, zu Zellen aggregiert). Alternativ direkt **Gemeinde × Periode** als Einheit: entspricht der tatsächlichen Genauigkeit der Pittioni-/EBHD-Funde und der Auflösung der Agrarstatistik (Gebietsstandsänderungen beachten).
2. **Unschärfe-angepasste Puffer statt fester Puffer**, wo Punktbezug gewünscht ist: Landnutzung im Radius r_eff = r_Landschaft + Unschärfe (z. B. 1 km + 2 km bei Ortschaftspunkten) oder per Monte-Carlo-Verschiebung des Fundpunkts innerhalb der Unschärfe (Mittelwert und Streuung der Kovariate je Fund). Funde mit Unschärfe > 5 km (oder Gemeinde-Zentroid in großen Alpengemeinden) ausschließen.
3. **Unschärfe im Modell:** (i) Gewicht oder Messfehler der Landnutzungs-Kovariate (Varianz aus der Monte-Carlo-Verschiebung → Errors-in-Variables bzw. Abschwächungskorrektur); (ii) in Occupancy-Modellen Site = Zelle/Gemeinde, Unschärfeklasse bzw. Datenquelle als **Detektionskovariate** und Anteil genauer Funde als Einheiten-Kovariate; (iii) Sensitivitätsanalyse „konservativ vs. strikt“ (500-m-Standardwert) und „nur ≤ 1 km“.
4. **Feinskalen-Module mit passender Landnutzung:**
   - **ab ~2010/2015, ≤ 250 m (CLIMBEE, BINATS, Resurvey 2028, GBIF-Erhebungen 2010+):** **INVEKOS** feldscharf (ab ~2015) in 250–500-m-Puffern; Kulturartenvielfalt, Feldgröße, Brachen/Biodiversitätsflächen.
   - **1990–2020, ≤ 1 km:** **CORINE 100 m** (ab 1990) in 1-km-Puffern um Funde ≤ 1 km; konservativ ~60–68 % der Art-Info, aber vor 2000 überwiegend ZOBODAT-500-m-Punkte → als Sensitivität führen.
   - **historische Standorte (Linz-Polygone, Top-Pittioni-Fundorte, Resurvey-Standorte):** **Franziszeischer Kataster** (parzellenscharf, 1817–1861) nicht flächig, sondern als **Standort-Fallstudien**: Polygon bzw. 1–2-km-Umkreis des Ortschaftspunkts, Vergleich Kataster ↔ heutige INVEKOS-/Orthofoto-Nutzung. Parzellengenauigkeit des Katasters bringt für die Bienendaten keinen Gewinn über ~1 km hinaus, liefert aber Legacy-Effekte (Weiden, Hutweiden, Weingärten) auf Standortebene.
5. **Datenverbesserung mit großem Hebel:** Nachgeoreferenzierung der ~20 häufigsten Pittioni-/ZOBODAT-Fundorte (Flurnamen, Etiketten) mit expliziter Unschärfe (Punkt-Radius-Methode) würde einen Großteil der historischen Funde auf ~0,5–2 km heben; die 40 häufigsten Koordinaten tragen 18 % aller Funde.

## 6 Einschränkungen

- Quell-Definitionen für Linz (1 km historisch, 250 m rezent), CLIMBEE (30 m) und Pittioni (3 km/5 km) sind Annahmen aus der Dokumentation (Polygon-Referenzpunkte, GeoNames-Ortschaft/Gemeinde), keine gemessenen Werte.
- GeoNames-Abgleich ≤ 150 m erkennt nur Zentroide aus GeoNames-ähnlichen Gazetteers; andere Gazetteers (Google, ÖK) mit Versatz > 150 m bleiben unerkannt → die konservative Variante ist eher noch optimistisch. Umgekehrt liegen echte Fundorte manchmal zufällig an benannten Punkten (Nullmodell 4–10 %).
- Der ZOBODAT-Wert 500 m ist ein pauschaler Klassenwert; ob er die tatsächliche Fundortgenauigkeit beschreibt, ist nicht prüfbar. Konservativ und strikt markieren daher die Spannweite.
- BINATS ist nicht im Merge; die Standortzahlen in 4.1 enthalten BINATS nicht.
