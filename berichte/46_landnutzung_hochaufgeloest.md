# 46 – Landnutzung feiner als HILDA+: Quellen, Kombination, Aufwand (AT, CZ, SK, HU; 1820–2025)

Stand: 17.11.2026. Grundlage sind Web-Recherche und Crossref-Prüfung der DOIs (Prüfliste in `tmp/sai_at/landuse_fine/lit/doi_check.txt`). Was nicht belegt ist, trägt die Markierung [UNVERIFIED]. Bezug: 32 §3 (HILDA+ vor 1960 rückgerechnet), 35 (HILDA+-Abschnitt), 41, 44.

## 1 Kurzfazit

1. **Die räumliche Auflösung ist nicht der Engpass.** Für 10-km-Zellen reichen statistische Daten je Katastral- oder Ortsgemeinde. Eine KG umfasst in AT und CZ typischerweise 3–15 km², die LUCC-CZ-Basiseinheiten im Mittel ca. 8,8 km². Solche Daten gibt es für fast alle Zeitschnitte: 1820–60 Kataster, ~1896/1900 Gemeindelexikon bzw. LUCC/KSH 1895, 1930–1990 Betriebs- und Viehzählungen, ab 1999 Agrarstrukturerhebung, ab 2005/2015 LPIS/INVEKOS. HILDA+ liegt mit 1 km zwar formal feiner. Vor 1960 bildet es aber keine lokalen Unterschiede ab, und eine Intensitätsachse fehlt ganz.
2. **Was HILDA+ fehlt, ist Intensität und zeitlich echte Änderung.** Folgende Größen lassen sich historisch auf Gemeindeebene rekonstruieren: Acker/Grünland-Verhältnis, Wiese vs. Hutweide, Weinbau, Ödland/Brache, Viehbesatz (GVE/ha), Bonitätsklassen (1820–60), ab 1951/60 Traktoren und Betriebsgrößen sowie Schlaggröße an Stichproben (Kataster → Luftbild 1950er → INVEKOS).
3. **Echte Feld- oder Parzellenebene** gibt es flächendeckend nur zweimal: 1820–60 (Kataster-Urmappen, bisher nicht flächig vektorisiert) und ab ca. 2005 (CZ-LPIS) bzw. 2015 (AT-INVEKOS). Dazwischen bleiben nur Luftbilder (AT ab 1949, kostenpflichtig; CZ 1953 offen), und die lassen sich nur an Stichproben auswerten.
4. **Empfehlung:** ein **Gemeinde-Panel (KG/Gemeinde × Dekade)** aus Statistik, das per Flächengewichtung auf die 10-km-Zellen gebracht wird. Kalibriert und ergänzt wird es mit (a) Kataster bzw. LUCC-CZ als Ausgangszustand, (b) Luftbild-Stichproben in Pilot- und Resurvey-Zellen für Schlaggröße und Kleinstrukturen und (c) Fernerkundung ab 1990/2017 (CORINE, HRL-Mahd, INVEKOS). Kernstück für CZ ist LUCC Czechia, für AT die Social Ecology Vienna (BOKU).

## 2 Quellentabelle

Legende: Aufwand g/m/h = gering/mittel/hoch. Eignung 1–5 (5 = sehr gut). Passung = Passung zur Bienendaten-Auflösung (Arbeitsannahme: historisch Ortschaft/Gemeinde, aktuell < 1 km).

### 2.1 Historische Karten, Kataster, Luftbilder

| Quelle | Inhalt / Intensität | Einheit | Zeit | Abdeckung | Zugang | Aufwand | Eignung | Passung |
|---|---|---|---|---|---|---|---|---|
| **Franziszeischer (Stabiler) Kataster**: Urmappen 1:2.880 + Parzellenprotokolle + Operate | Kulturgattungen je Parzelle (Acker, Wiese, Hutweide, Weingarten, Garten, Wald, Ödland), **Bonitätsklassen** (Ertragsklassen = Intensitätsproxy), Parzellengröße | Parzelle; aggregiert je KG | 1817–1861 | AT (ohne Bgld), CZ (Böhmen, Mähren, Schlesien), SI u. a. | Digitalisate: Stmk als WMTS/WMS OGD **CC BY 4.0**; OÖ DORIS „Urmappe“; NÖ Landesarchiv Online-Lesesaal; Tirol **KaTi digital**; FRANZI (Citizen Science, >20.000 Parzellenprotokolle transkribiert, kulturpool.at); Mapire/Arcanum (Ansicht frei, Lizenz/WMTS unklar). **Keine flächige Vektorisierung** gefunden | h (Parzelle), m (KG-Summen aus Operaten/„Ausweis über die Benützung des Bodens“) | 4 (Ausgangszustand, nicht Zeitreihe) | sehr gut (feiner als nötig) |
| **Ungarischer Kataster 1856–60** (+ Kataster ab 1849, Indikationsskizzen) | wie oben | Parzelle/KG | 1850er–1880er | HU, SK, **Burgenland** (bis 1921 HU) | Mapire, Ung. Nationalarchiv (Hungaricana), teils online | h | 3–4 | sehr gut |
| **Militärische Landesaufnahmen** I (1764–87), II (1806–69, 1:28.800), III (1869–87, 1:25.000/1:75.000) | Wald, Acker, Wiese, Weide, Weingarten, Sumpf; keine Intensität | Rasterkarte, ca. 30–100 m effektiv | 1780, ~1830–60, ~1880 | AT, CZ, SK, HU | Mapire (Ansicht frei; Nutzung/WMTS je Layer prüfen) | m–h (Segmentierung/DL) | 3 | gut |
| **Carpathian historical land-use dataset** (Lieskovský et al. 2018) | 9/22 Klassen aus 2. MilAufn./Szatmári (1819–73), Topokarten 1915–45 und 1950–83 | **2×2-km-Punktraster** | 3 Zeitschnitte | SK, HU, (CZ-Ost, AT-Rand nur teilweise) [Abdeckung AT UNVERIFIED] | Open Access (J. Maps) | g | 3 | mäßig (2 km Punkte → 10-km-Zelle ok, ~25 Punkte/Zelle) |
| **Skokanová / VÚKOZ**: Landnutzungs-Trajektorien SO-Mähren, Truppenübungsplätze | 5 Zeitachsen 1836–52, 1876–80, 1952–56, 1988–94, 2002–06; Polygone aus MilAufn. + Topokarten 1:25.000 | Polygon | 1836–2006 | CZ (regional) | auf Anfrage (VÚKOZ) | g–m | 3 (Pannonikum-Rand CZ!) | gut |
| **BEV-Luftbildarchiv** | ~450.000 analoge Luftbilder 1949–2009, Befliegung je Gebiet alle 5–7 J.; histor. SW-Orthofotos 50 cm (nicht flächendeckend), Farbe ab 2000 | Bild (~0,5–1 m) | 1949– | AT | **kostenpflichtig**: 10 € (Bild 1:1) bis 72 €, Scan 25 €; Ortho SW 1 €/km², Farbe 3 €/km² | h (Orthorektifizierung, Interpretation) | 4 (Schlaggröße, Raine, Trockenrasen) – nur Stichproben | sehr gut |
| **ÖNB „Österreich aus der Luft“** | ~4.800 Schrägluftbilder 1930–35 | Foto, nicht orientiert | 1930–35 | AT | offen (ÖNB Labs) | h | 2 | punktuell |
| Länder-Orthofoto-Zeitreihen (z. B. Tirol TIRIS mit historischen Layern) | Orthofotos versch. Jahre | 0,2–1 m | je Land unterschiedlich | AT (Länder) | WMS, meist frei [Jahrgänge je Land UNVERIFIED] | m | 3 | sehr gut |
| **CZ Historische Orthofotokarte 1950er** (CENIA/GEODIS, Bilder VGHMÚř) | SW-Orthofoto, meist 1953 (Spanne 1946–59), **vor bzw. während der Kollektivierung** | ~0,5 m | 1950er | CZ flächendeckend | **offen**, WMS/WMTS gis.cenia.cz | m (DL-Segmentierung Schläge) | 5 für Schlaggrößen-Kontrast | sehr gut |
| SK/HU historische Luftbilder (u. a. fentrol.hu/Arcanum, HM HIM; SK Topografický ústav) | Luftbilder ab ~1950 | ~1 m | 1950– | HU, SK | [UNVERIFIED]; vermutlich Abo/kostenpflichtig | h | 3 | sehr gut |
| Topographische Karten 1:25.000/1:50.000 (ÖK, sowjet./tschechoslow. Militärkarten) | Wald, Weingarten, Obstgärten, Grünland teils, Siedlung | Rasterkarte | 1950er–1980er | alle | BEV historische ÖK kostenpflichtig; Militärkarten CZ/SK teils online | m–h | 3 | gut |

### 2.2 Statistik je Gemeinde/KG

| Quelle | Inhalt / Intensität | Einheit | Zeit | Abdeckung | Zugang | Aufwand | Eignung | Passung |
|---|---|---|---|---|---|---|---|---|
| **LUCC Czechia** (Bičík, Kupková, Jeleček; Karlsuniv. Prag) | Acker, Dauerkulturen (Gärten, Weingärten, Hopfen), Wiesen, Weiden, Wald, Wasser, bebaut, sonstige | ~8.900–10.000 vergleichbare Basiseinheiten (KG-Aggregate) | **1845, 1896, 1948, 1990, 2000, 2010** | CZ komplett | lucccz.cz/databaze; Lizenz/Download unklar → Kooperation | g (nach Freigabe) | **5** | sehr gut |
| **Gemeindelexikon der im Reichsrate vertretenen Königreiche und Länder** (Volkszählung 1900; 14 Bde., 1903–08) + Spezialortsrepertorien 1880er/1890er | Ortsgemeinde: Fläche nach Kulturgattungen und Viehstand [Spalten Kulturgattungen/Viehstand UNVERIFIED, Stichprobe in DjVu prüfen] | Ortsgemeinde | ~1900 (1880/1890) | AT (ohne Bgld), CZ | digitalisiert (GenWiki DjVu, FamilySearch, OÖ Landesbibliothek); Abtippen nötig | m–h (OCR/Abtippen ~2.500 AT-Gemeinden) | **5** (wenn Spalten vorhanden) | sehr gut |
| **Ungarn: Agrarzählung 1895** (KSH; Bd. 1 nach Dörfern), **1935** | Kulturarten, Vieh, Betriebsgrößen | Dorf/Gemeinde | 1895, 1935 | HU, SK, Bgld (Königreich Ungarn) | KSH/Hungaricana digitalisiert; Abtippen | m–h | 4–5 | sehr gut |
| **GISta Hungarorum** / Demeter et al. Siedlungsdatenbank | Gemeinde-HGIS 1330–2010; Landnutzung/Sozioökonomie Kgr. Ungarn bis 1910 | Gemeinde (Polygone) | div. | HU, SK, Bgld | teils online (Ung. Nationalarchiv), teils unpubliziert | m | 4 (Geometrien!) | sehr gut |
| **AT Land- und forstwirtschaftliche Betriebszählungen** 1902, 1930, 1951, 1960, 1970, 1980, 1990, 1995, 1999; danach Agrarstrukturerhebung (2010, 2020 Vollerhebungen) | Flächen nach Kulturarten (Acker, ein-/mehrmähdige Wiesen, Hutweiden, Almen, Weingärten, Obst), Vieh, **Traktoren/Maschinen**, Betriebsgrößen | Gemeinde in Vollerhebungen (Gemeindeergebnisse ab 1951/60 als Druckbände [UNVERIFIED für 1902/1930]); ab 1999 STATcube | 1902–2020 | AT | Druckbände (Bibliotheken, Statistik Austria), digital ab ~1999; Sonderauswertung kostenpflichtig | m (Digitalisieren), g ab 1999 | **5** | sehr gut |
| **AT Allgemeine Viehzählungen** (u. a. 1934, ab 1950er regelmäßig) | Rinder, Schafe, Ziegen, Pferde, Schweine → GVE/ha, Weidedruck | Gemeinde [UNVERIFIED für Vorkriegsjahre] | 1880–heute | AT | Druckbände / Statistik Austria | m | 4 | sehr gut |
| **Social Ecology Vienna (BOKU)**: Landnutzung, Biomasse- und Energieflüsse Österreichs 1830–2010 (Krausmann et al. 2003; Erb et al. 2008; Gingrich & Krausmann 2018); Fallregionen (St. Florian/Grünburg, Theyern, Waidhofen/Ybbs, Paldau) | Landnutzung, Dünger (N), Vieh, Erträge, HANPP | national; Fallgemeinden bzw. -regionen (Zenodo: 2 Gemeinden, 3 Zeitschnitte) | 1830–2010 | AT | publiziert, Daten teils offen (BOKU-Datendownload, Zenodo 4896570) | g | 3 (national), 4 als Know-how | gering (national) |
| Weinbaukataster AT/HU/CZ/SK | Rebflächen | Riede/Parzellen | AT ab ~1999/2000 [UNVERIFIED] | alle | Länder/Weinbauverbände | m | 3 (Pannonikum) | sehr gut |

### 2.3 Aktuell: Feld- und Rasterebene

| Quelle | Inhalt / Intensität | Einheit | Zeit | Abdeckung | Zugang | Aufwand | Eignung | Passung |
|---|---|---|---|---|---|---|---|---|
| **INVEKOS-Schläge AT** (AMA) | Kulturart je Schlag (> 200 Schlagnutzungsarten: ein-/mehrmähdige Wiese, Hutweide, Brache, Ackerkulturen), **Schlaggröße**; ÖPUL-Maßnahmen nur über Sonderauswertung | Schlag/Feldstück (Polygon) | jährlich, offen etwa ab 2015 (INSPIRE-Records 2019, 2021, 2024; fiboa/source.coop bis 2025) [frühere Jahre UNVERIFIED] | AT | **offen** (data.gv.at / INSPIRE; Lizenz AMA, CC BY [UNVERIFIED]) | g | 5 | sehr gut |
| **CZ LPIS** (eAGRI) | Bodenblöcke/Farmerblöcke, Kultur (Acker, Grünland, Weingarten), Landschaftselemente | Block | **2005–2018 historischer Export**, 2019– jährlich | CZ | **offen, CC BY 4.0** (data.gov.cz) | g | 5 | sehr gut |
| SK LPIS | Blöcke/Felder (~275.000) | Feld | Jahrgänge [UNVERIFIED] | SK | offen (Nationaler OGD-Katalog, fiboa) | g | 4 | sehr gut |
| HU MePAR / Antragsflächen | Blöcke | Block | ab 2004 | HU | eingeschränkt [UNVERIFIED] | m | 3 | sehr gut |
| **Copernicus HRL Grassland: Mowing Events (GRAME) / Dates (GRAMD)** | Mahdhäufigkeit und -termine je Pixel, temporäres + Dauergrünland | 10 m | jährlich ab 2017 | EEA38 | offen (CLMS) | g | 5 (Grünlandintensität) | sehr gut |
| Miletich et al. 2025 | erster offener AT-weiter Mahd-Datensatz (NDVI-Abfall + SWIR-Filter; 78 % der Mahden erkannt) | 10 m | 2023 | AT | offen | g | 4 | sehr gut |
| Griffiths et al. 2020; Schwieder et al. 2022 | Methode Mahdhäufigkeit/Grünland-Nutzungsintensität (DE) | 10–30 m | 2016– | DE (Methode übertragbar) | – | m | Methode | – |
| **CORINE Land Cover** | 44 Klassen, u. a. komplexe Parzellenstruktur, Weingärten, natürliches Grünland, Wiesen/Weiden | 100 m, MMU 25 ha | 1990, 2000, 2006, 2012, 2018 (2024) | alle | offen | g | 3 | gut |
| Copernicus HRL Grassland/Imperviousness, LISA (AT Land Information System; Landbedeckung objektbasiert, Landnutzung aus INVEKOS/Flächenwidmung) | Landbedeckung, Versiegelung, Grünland | 10–20 m | 2006/2015– | AT/EU | offen (HRL); LISA [Verfügbarkeit UNVERIFIED] | g | 3 | sehr gut |
| Estel et al. 2015/2016 (MODIS) | **Brache/Aufgabe und Rekultivierung**, Anbauhäufigkeit (Cropping-Intensität) | 250 m | 2001–2012 | Europa | auf Anfrage/HU Berlin | g | 3 | gut |
| Levers et al. 2016/2018; Kuemmerle et al. 2016 | Archetypen der Landsysteme inkl. Intensität (Dünger, Erträge, Viehdichte); Treiber der Intensität | 1 km / NUTS3-Downscaling | ~2000–2006 | Europa | publiziert | g | 3 (Querschnitt) | gut |
| HILDA (Fuchs et al. 2013, 2015) | 6 Klassen, Bruttoänderungen, aus histor. Statistik + Topokarten | 1 km | 1900–2010, Dekaden | Europa | auf Anfrage/Zenodo | g | 2 (Rückgrat von HILDA+ vor 1960) | gut |
| HYDE 3.x, LUH2 | Weide/Acker-Anteile | 5' (~9 km) bzw. 0,25° | 10.000 v. Chr.–2020 | global | offen | g | 1 | zu grob |

## 3 Empfohlene Kombination je Periode (Ziel: Gemeinde/KG × Dekade → 10-km-Zelle)

| Periode | Primärquelle (flächig) | Feinere Ergänzung (Stichprobe/Pilot) | Zielauflösung |
|---|---|---|---|
| **1820–1860** (Baseline vor Bienendaten) | Franziszeischer Kataster als KG-Summen (AT, CZ via LUCC 1845); Ung. Kataster (HU, SK, Bgld) | Urmappen-Vektorisierung (DL) in Pilotzellen: Parzellengröße, Bonität | KG; Parzelle in Pilotzellen |
| **1880–1910** (Dekaden 1900/1910) | Gemeindelexikon 1900 / Spezialortsrepertorium (AT, CZ); LUCC 1896; KSH 1895 (HU, SK, Bgld) | 3. Landesaufnahme (Weingärten, Wald, Hutweiden) | Ortsgemeinde |
| **1930–1955** | AT-Betriebszählung 1930 + 1951, Viehzählung 1934; LUCC 1948; HU 1935 | **Luftbilder 1949–55**: BEV (AT), CENIA 1953 (CZ, offen) → Schlaggröße, Raine, Trockenrasen vor Kollektivierung bzw. Kommassierung; Lieskovský-Punkte 1915–45 | Gemeinde; 0,5 m in Pilotzellen |
| **1960–1990** | AT-Betriebszählungen 1960/70/80/90 (Gemeinde: Kulturarten, Vieh, Traktoren), HILDA+ (ab 1960 datengetrieben); CZ/SK/HU: Kollektivierung als Ereignisdatum, LUCC 1990 | BEV-Luftbilder ~1970/1985 (Grundzusammenlegung, Schlaggröße), sozialist. Topokarten | Gemeinde |
| **1990–2015** | CORINE 1990–2018; Agrarstrukturerhebung (STATcube, ab 1999); LUCC 2000/2010; CZ-LPIS ab 2005 | Estel (Brache/Anbauintensität), Levers (Archetypen) | 100 m → Gemeinde |
| **2015–2025** | INVEKOS AT, LPIS CZ/SK (Schlaggröße, Kulturart), HRL Mahd 2017+ | Miletich 2023; ÖPUL-Flächen (Anfrage AMA/BML) | Schlag/10 m |

**Harmonisierung:** gemeinsame Klassen (Acker, Wiese/mehrmähdig, Hutweide/Weide/Alm, Weingarten/Obst, Ödland/Brache, Wald, bebaut). KG- und Gemeindegrenzen werden mit historischen Gebietsständen verschnitten (MOSAIC/GISta, BEV-KG-Grenzen, LUCC-BTU) und flächengewichtet in die 10-km-Zellen überführt. Zwischen Stützjahren wird pro Gemeinde interpoliert. HILDA+ dient nur noch als räumliche Disaggregationsvorlage innerhalb von Gemeinden, nicht als Zeitsignal.

## 4 Historisch rekonstruierbare Intensitätsmaße

| Maß | Quellen | Zeitraum | Ebene |
|---|---|---|---|
| Acker:Grünland-Verhältnis, Wiese vs. Hutweide | Kataster, Gemeindelexikon, Betriebszählungen, LUCC | 1830– | KG/Gemeinde |
| Anteil Hutweide/Ödland/„sonstige“ (Proxy für Trockenrasen und Brachen) | dieselben; ab 2017 HRL-Grünland | 1830– | KG/Gemeinde |
| Weingarten-/Obstanteil | Kataster, Statistik, Weinbaukataster | 1830– | KG |
| **Viehbesatz (GVE/ha LF)**, Schaf- und Ziegenanteil (Weidedruck) | Gemeindelexikon 1900, Viehzählungen, KSH 1895/1935 | 1880– | Gemeinde |
| Bonität/Reinertrag | Franz. Kataster, Grundsteuerregulierung 1880er | 1830–1880 | KG |
| Mechanisierung (Traktoren/ha), Betriebsgröße | Betriebszählungen | 1930/1951– | Gemeinde |
| **Schlaggröße / Randliniendichte** | Urmappen (1830), Luftbilder (1950er/70er/80er), LPIS/INVEKOS | punktuell, ab 2005/2015 flächig | Parzelle (Stichprobe) |
| Mahdhäufigkeit | HRL GRAME, Miletich; historisch nur ein- vs. mehrmähdige Wiese (Betriebszählungen) | 2017–; Klassen ab 1951 [UNVERIFIED] | 10 m / Gemeinde |
| Mineraldünger, Pestizide | nur national bzw. Bundesland (Gingrich & Krausmann 2018; Grüner Bericht) | 1900– | national → als Zeittrend × Ackeranteil |
| Kollektivierung (CZ/SK/HU) | Ereignisdaten (CZ ~1949–60, HU 1959–61) + 1950er-Ortho vs. 1970er-Karten | 1950–1990 | Land/Gemeinde |

## 5 Aufwand und Kosten (grobe Schätzung)

- **Gering, sofort machbar (Wochen):** CORINE, HRL-Mahd, INVEKOS AT, LPIS CZ/SK, Lieskovský-Raster, LUCC CZ (nach Freigabe), Agrarstrukturerhebung ab 1999. Kosten keine bzw. Statistik-Sonderauswertung ca. 0,5–3 k€ [UNVERIFIED].
- **Mittel (3–6 Personenmonate):** Gemeindetabellen AT 1900/1951/1960–1990 und KSH 1895/1935 digitalisieren: OCR/Abtippen des Pannonikums zuerst, das sind ca. 600–800 Gemeinden in NÖ, Bgld und Wien-Umland. Dazu Gebietsstände harmonisieren. Kosten vor allem Hilfskraft- oder Werkvertragsmittel (ca. 15–30 k€).
- **Hoch (Doktorat/Postdoc-Teilprojekt):** Kataster-Urmappen und Luftbilder per Deep Learning segmentieren (vgl. Göderle et al. DHQ 2024 für Stmk-Kataster; Mäyrä et al. 2023; Uhl et al. 2020). Realistisch nur für **Pilot- und Resurvey-Zellen**, z. B. 20–30 Zellen × 3 Zeitschnitte. BEV-Luftbilder kosten ca. 10–25 € je Bild; bei ~30–60 Bildern je 10-km-Zelle und Zeitschnitt sind das ca. 0,5–1,5 k€ je Zelle und Zeitschnitt [Bildzahl UNVERIFIED]. CZ 1953 ist kostenlos.

## 6 Kooperationen

- **Social Ecology Vienna (BOKU, Gingrich, Krausmann, Erb):** im eigenen Haus. Sie haben die historischen AT-Agrarstatistiken und das Methodenwissen zu Intensität (N, Vieh, HANPP) und kennen die Fallgemeinden.
- **LUCC Czechia (Kupková, Bičík; Karlsuniv. Prag):** Datenfreigabe 1845–2010 für CZ, idealerweise mit Abgleich der 10-km-Zellen.
- **GRACE-Umfeld:** Clark, Keil, Essl (Neobiota/Landnutzungsdaten), **Skokanová (VÚKOZ)** für Trajektorien SO-Mähren und Militärkarten-Methodik.
- **Göderle (Uni Graz, RePaSE / Franziszeischer Kataster KI-Extraktion)** und **Hohensinner (BOKU, Kataster-Rekonstruktion Alpenflüsse)** für die Urmappen-Pipeline.
- **Lieskovský (SAV) / Kuemmerle, Levers (HU Berlin):** Karpaten-Datensatz, Intensitätskarten.
- **HU:** Demeter (GISta Hungarorum, HUN-REN), KSH.
- **Joanneum Research (Miletich):** Mahd-Zeitreihen AT.

## 7 Studienbeispiele Insekten × feine historische Landnutzung

| Studie | Ansatz | Relevanz |
|---|---|---|
| Senapathi et al. 2015 Proc B, 10.1098/rspb.2015.0294 | 14 Standorte in England; Dudley-Stamp-Landnutzungskarte 1930er vs. LCM 2007; Landbedeckung im Gebiet und im 1-km-Puffer erklärt Arten- und Kompositionswandel von Bienen und Wespen | **direktes Vorbild**: historische Karte auf Standortebene |
| Ollerton et al. 2014 Science, 10.1126/science.1257259 | Aussterberaten britischer Aculeaten vs. Agrarwandel (national, Zeitreihe) | Zeitliche Kopplung an Intensivierungsphasen |
| Scheper et al. 2014 PNAS, 10.1073/pnas.1412973111 | NL-Museumsdaten; Wirtspflanzenverlust als Treiber | Mechanismus, Landnutzung nur indirekt |
| Carvalheiro et al. 2013 Ecol Lett, 10.1111/ele.12121 | GB/NL/BE-Bestäuber; Abschwächung des Rückgangs nach 1990 | Periodisierung |
| Habel et al. 2016 Conserv Biol, 10.1111/cobi.12656 | Tagfalter Regensburg über 200 Jahre vs. Landnutzungsintensivierung | lange Reihe, regional |
| **Sandberge Oberweiden (Marchfeld)**, J Insect Conserv 2023, 10.1007/s10841-023-00486-8 | Bienengemeinschaft über 100 Jahre; Landnutzung aus BEV-Luftbildern 1966/1994/2000; vor 1950 keine Zuordnung | **AT-Vorbild und Warnung**: Luftbilder erst ab 1950er/60er belastbar |
| NHM London „Bee sensitivity to a century of agricultural land-use change“ (NERC NE/P012914/1) | digitalisierte Hummelsammlung × Agrarwandel | Projektvorbild [Publikationen UNVERIFIED] |

## 8 Quellen (DOIs per Crossref geprüft)

- Winkler et al. 2021 Nat Commun 10.1038/s41467-021-22702-2 (HILDA+)
- Fuchs et al. 2013 Biogeosciences 10.5194/bg-10-1543-2013; Fuchs et al. 2015 GCB 10.1111/gcb.12714 (HILDA)
- Kupková, Bičík & Jeleček 2021 Land 10.3390/land10010034 (LUCC Czechia); Datenbank lucccz.cz
- Lieskovský et al. 2018 J Maps 10.1080/17445647.2018.1502099
- Jepsen et al. 2015 Land Use Policy 10.1016/j.landusepol.2015.07.003 (Landmanagement-Regime 1800–2010, Kollektivierung)
- Krausmann et al. 2003 Land Use Policy 10.1016/s0264-8377(02)00048-0; Erb et al. 2008 J Ind Ecol 10.1111/j.1530-9290.2008.00076.x; Gingrich & Krausmann 2018 STOTEN 10.1016/j.scitotenv.2018.07.074; Gingrich et al. 2017 Reg Environ Change 10.1007/s10113-017-1145-1
- Hohensinner et al. 2021 Front Environ Sci 10.3389/fenvs.2021.647247 (Kataster 1826–59, Alpenflüsse)
- Miletich et al. 2025 Remote Sens 10.3390/rs17101769; Griffiths et al. 2020 RSE 10.1016/j.rse.2019.03.017; Schwieder et al. 2022 RSE 10.1016/j.rse.2021.112795
- Estel et al. 2015 RSE 10.1016/j.rse.2015.03.028; Estel et al. 2016 ERL 10.1088/1748-9326/11/2/024015; Kuemmerle et al. 2016 ERL 10.1088/1748-9326/11/6/064020; Levers et al. 2016 Land Use Policy 10.1016/j.landusepol.2016.08.013; Levers et al. 2018 Reg Environ Change 10.1007/s10113-015-0907-x; Kehoe et al. 2017 Nat Ecol Evol 10.1038/s41559-017-0234-3
- Mäyrä et al. 2023 Ambio 10.1007/s13280-023-01838-z; Uhl et al. 2020 IEEE Access 10.1109/ACCESS.2019.2963213; Göderle et al. 2024 DHQ 18(3), dhq-static.digitalhumanities.org/pdf/000744.pdf (kein DOI)
- Daten und Portale: BEV Remote Sensing (bev.gv.at/en/Services/Products/Remote-Sensing.html); Stmk Franz. Kataster WMTS (landesentwicklung.steiermark.at); kulturpool.at/en/content/franciscan-cadastre; maps.arcanum.com/en/map/cadastral; CENIA historische Ortho (gis.cenia.cz/mapcache/ortofotomapa_historicka/wms); CLMS GRAME (stac.dataspace.copernicus.eu, clms_vlcc_grassland-mowing-events_europe_10m_yearly_v1); INVEKOS über INSPIRE/data.gv.at bzw. source.coop/fiboa/at-crop; CZ-LPIS data.gov.cz; Zenodo 4896570 (Waidhofen/Paldau); KSH 1895 (ksh.hu); GenWiki Gemeindelexikon.
- Nicht verifiziert: „Dou et al. 2021“ (europäische Landnutzungsintensität) ließ sich per Crossref nicht eindeutig zuordnen und ist deshalb nicht aufgenommen.
