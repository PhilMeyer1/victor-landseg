# unterlagen

Berichte und Auswertungen des Projekts Victor (Wildbienen in Österreich: detektionskorrigierte
Rekonstruktion der Gemeinschaften 1900–2020, Attribution auf Erwärmung, Trockenheit und
Landnutzung). Das Repo hält die gelieferten Dokumente unverändert und auffindbar fest. Es enthält
keinen Code und keine Daten.

## Aufbau

```
README.md        diese Übersicht
.gitattributes   schützt die Berichte vor Umwandlung der Zeilenenden
berichte/        die gelieferten Berichte, unverändert (Name und Inhalt wie geliefert)
```

Die Berichte bleiben alle in `berichte/`, weil sie über ihre Dateinamen aufeinander verweisen
(etwa `41_occupancy_run1_auswertung.md` auf `41_occupancy_run1.html`). Die Nummer vorn im Namen
ist die Berichtsnummer und wird nicht geändert.

## Verzeichnis der Berichte

| Nr. | Datei | Titel (erste Überschrift) | Inhalt | Stand |
|---|---|---|---|---|
| 41 | [`41_occupancy_run1_auswertung.md`](berichte/41_occupancy_run1_auswertung.md) | Occupancy-Lauf 1: Umfassende Auswertung (AT, 100 Arten, 1900–2020) | Ergebnisse des ersten Occupancy-Modelllaufs: Klimaschuld der Gemeinschaften, Einfluss der Landnutzung, Zerlegung der Artenzahl-Änderung nach Ursachen und Prüfung der Nischenindizes. | 2026-11-17 |
| 41 | [`41_occupancy_run1.html`](berichte/41_occupancy_run1.html) | Occupancy-Lauf 1: Auswertung und Modellgüte | Grafische Fassung von Bericht 41 mit interaktiven Diagrammen zu Ergebnissen und Modellgüte (im Browser öffnen). | 17.11.2026, vorläufig (Lauf 1) |
| 46 | [`46_landnutzung_hochaufgeloest.md`](berichte/46_landnutzung_hochaufgeloest.md) | 46 – Landnutzung feiner als HILDA+: Quellen, Kombination, Aufwand (AT, CZ, SK, HU; 1820–2025) | Welche Quellen Landnutzung historisch feiner als HILDA+ beschreiben, wie man sie kombiniert und was das kostet; Empfehlung ist ein Panel Gemeinde × Dekade. | 17.11.2026 |
| 47 | [`47_raeumliche_genauigkeit_bienendaten.md`](berichte/47_raeumliche_genauigkeit_bienendaten.md) | 47 – Räumliche Genauigkeit der österreichischen Wildbienen-Funddaten (1900–2020er) | Wie genau die Fundorte der Wildbienen-Daten je Zeitraum sind und auf welcher räumlichen Ebene sich Landnutzung damit verknüpfen lässt. | 17.11.2026 |
| 48 | [`48_luftbild_segmentierung_klassen.md`](berichte/48_luftbild_segmentierung_klassen.md) | Briefing: Klassen für die Segmentierung historischer Luftbilder (AridiBEE, Projekt 1) | Übergabe für die Segmentierung historischer Schwarz-Weiß-Luftbilder: welche Klassen erkannt werden sollen und warum. | 2026-11-17 |

Die HTML-Datei lädt ihre Diagramm-Bibliothek (Plotly) aus dem Internet; ohne Netz fehlen die
Diagramme.

## Herkunft

Lieferung vom 17.11.2026, Archiv `65aef76cd764a7ffa13848df2940bee4.zip`. Aus dem Archiv stammen
die fünf Dateien oben auf oberster Ebene, Byte für Byte unverändert:

| Datei | SHA-256 |
|---|---|
| `41_occupancy_run1.html` | `5923ee927e5596ed3cd821f894f35dcc31573cb5690dc85f05190ffa4d4c90c7` |
| `41_occupancy_run1_auswertung.md` | `33485d5aac88a1ee4c7d38de4c46750f3c497b4ee79485e24752dc1c423a73c8` |
| `46_landnutzung_hochaufgeloest.md` | `efd0459e6e7d462d7458bd16c410ed0c04bc30fdeddcea93cac1ad8ef3733c65` |
| `47_raeumliche_genauigkeit_bienendaten.md` | `6f73fde35a09a437786c194034f9ca9a3a82e267c0b53e4339465fd3ff4a6d36` |
| `48_luftbild_segmentierung_klassen.md` | `1cc501b41e507a8ba7faf4ad052fdf58592aee7c3d1ea55df67323cc66863cef` |

Prüfen: in `berichte/` `sha256sum <datei>` aufrufen und mit der Tabelle vergleichen.

## Luftbilder

Das Archiv enthielt außerdem ein inneres Archiv mit Beispiel-Luftbildern (rund 490 MB, zu Bericht
48). Die Bilder liegen nicht in diesem Repo, sondern unversioniert im Datenraum
`../daten/luftbilder/` (vom Basisordner aus `daten/luftbilder/`); Inhaltsliste mit Prüfsummen:
`../daten/README.md`.

## Verwiesen, aber nicht mitgeliefert

Die Berichte verweisen auf Folgendes, das nicht Teil der Lieferung ist und hier fehlt. Ermittelt
aus den Dateien selbst.

Andere Berichte:

| Nr. | Verweis | in |
|---|---|---|
| 32 | „32 §3 (HILDA+ vor 1960 rückgerechnet)" | 46 |
| 35 | „35 (HILDA+-Abschnitt)" | 46 |
| 38 | `38_resurvey_kandidaten_datenanfragen.md` | 48 |
| 39 | `39_projekt1_occupancy_richtungen.md` | 41 (Auswertung) |
| 40 | `40_occupancy_run1_ergebnisse.md` | 41 (Auswertung) |
| 44 | „44" (Bezug, ohne Dateiname) | 46 |

Skripte und Ergebnisse unter `tmp/sai_at/` (in den Berichten teils als `../tmp/sai_at/…`,
teils als `tmp/sai_at/…` geschrieben):

| Pfad | in |
|---|---|
| `tmp/sai_at/occupancy/11_prep_run1.py`, `12_run1_chain.R`, `13_run1_combine.R` | 41 (HTML) |
| `tmp/sai_at/occupancy/analysis_run1/20–25_*` und `build_html.py` | 41 (Auswertung und HTML) |
| `tmp/sai_at/occupancy/analysis_run1/out/` | 41 (Auswertung und HTML) |
| `tmp/sai_at/landuse_fine/lit/doi_check.txt` | 46 |
| `tmp/sai_at/analysis/out_v3/14_occ_merged.tsv.gz` | 47 |
| `tmp/sai_at/landuse_fine/precision/` (`00_ebhd_extract.R`, `01_precision_audit.py`, `02_gazetteer_diagnostics.py`, `03_figure.py`, Tabellen `t1`–`t8`, `results.json`, `records_precision.tsv.gz`) | 47 |
| `tmp/sai_at/landuse_fine/precision/fig1_precision_by_decade.png` (als Bild eingebunden, wird daher nicht angezeigt) | 47 |

Fremde Rohdaten, die Bericht 47 als Grundlage nennt: der GBIF-Download 0008856, die EBHD-Datei
`Bee_DB_2025-12-17.rds` und die Pittioni-QC-Kartei.
