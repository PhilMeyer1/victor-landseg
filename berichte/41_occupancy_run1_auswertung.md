# Occupancy-Lauf 1: Umfassende Auswertung (AT, 100 Arten, 1900–2020)

**Stand:** 2026-11-17 · **Grafische Fassung:** `41_occupancy_run1.html` · **Skripte:** `../tmp/sai_at/occupancy/analysis_run1/20–25_*`, `build_html.py` · **Ergebnisse:** `../tmp/sai_at/occupancy/analysis_run1/out/` · Grundlage: `40_occupancy_run1_ergebnisse.md`, Richtungen in `39_projekt1_occupancy_richtungen.md`

Alle Werte: Median [95 %-KI] über 600 Posterior-Ziehungen (3 Ketten × 200), sofern nicht anders angegeben.

## Kernaussagen

1. **Climatic debt (A1), belastbar:** detektionskorrigiert ziehen die Gemeinschaften **56 % [40; 71]** der räumlich erwarteten CWM-STI-Verschiebung nach, naiv nur 13 %. Der Rückstand entsteht seit den 1990ern (2000/10er: −0,110 [−0,158; −0,061] °C unter der Erwartung).
2. **„Landnutzung bremst“ ist zeitlich nicht belegt (A1/A2):** Extensiv 70 % [44; 93] vs. intensiv 51 % [38; 66], aber die **Within-Steigungen sind gleich** (0,115 vs. 0,119 °C/°C). Der Unterschied kommt aus dem räumlichen Gradienten (0,167 vs. 0,233). Die zeitvariable Regression findet keinen Bremseffekt (T_w × I_Zelle = 0,001 [−0,005; 0,008]; T_w × ΔI = +0,014 [0,003; 0,025]). Der klar negative T × I-Term im Occupancy-Modell (−0,48 [−0,62; −0,33]) beschreibt daher vor allem ein **räumliches** Muster.
3. **Attribution (B1):** Die erwartete Artenzahl je Zelle steigt 1950er → 2010er um +2,25 [0,88; 3,36] (von 100). Davon Klima +1,67 [0,18; 2,89], fast ganz über das **Trockenerwerden** (Temperatur allein +0,07 [−1,57; 1,42]); Landnutzung +0,27 [0,14; 0,39].
4. **Nischenindizes validiert (A3):** Art-Temperatureffekte korrelieren mit dem STI (r = 0,46 [0,36; 0,55]), Ariditätseffekte mit SAI (0,58) und SAI-Rest (0,21 [0,12; 0,31]).
5. **Modellgüte:** Gemeinschaftsebene konvergiert; Artebene nur teilweise (33 von 100 Arten mit R-hat > 1,1). Der PPC trifft Gesamtzahl, Dekaden und Quellen, zeigt aber Überdispersion je Zelle × Dekade.

## 1 Daten

| Größe | Wert |
|---|---|
| Zellen / Dekaden | 302 Zellen (10 km) mit ≥ 2 Dekaden; 13 Dekaden; 2.358 von 3.926 Zelle × Dekade besucht |
| Besuche | 36.199 aufbereitet; im Modell max. 20 je Zelle × Dekade → 18.051 Besuche, 12.486 Nachweise |
| Besuche je Zelle × Dekade | Median 5 (10.–90. Perzentil 1–34, max. 766); 17 % der Einheiten > 20 (gekappt) |
| Quellen (aufbereitet) | GBIF/ZOBODAT 25.326, EBHD-AT 5.439, Pittioni 3.107, Linz 2.277, CLIMBEE 50 |
| Datum / Sammler·innen | 89 % mit Tagesdatum; 703 Namen, 36 % der Besuche „unbekannt“; Top-10-Personen = 31 % der Besuche |
| Arten | 100 (quantilsgetreu über den STI aus 343 Kandidaten mit ≥ 50 Funden); 53–2.584 Funde |
| Typischer Besuch | Listenlänge Median 1 (alle) bzw. 26,5 (CLIMBEE) |

## 2 Modellgüte

**Konvergenz** (R-hat über alle 600 Ziehungen; in Klammern streng, nur zweite Kettenhälften wie in `40`):

| Block | R-hat max | Anteil > 1,1 | ESS min |
|---|---|---|---|
| μβ Occupancy (Gemeinschaft) | 1,06 (1,08) | 0 % | 221 |
| μα Detektion (Gemeinschaft) | 1,03 (1,05) | 0 % | 215 |
| τ²β | 1,11 (1,30) | 20 % (40 %) | 96 |
| β Arten | 1,51 (1,93) | 9 % (18 %) | 17 |
| α Arten | 2,23 (2,25) | 5 % (9 %) | 27 |
| σ²t (AR1) / ρ | 1,35 / 1,08 | 20 % / 0 % | 31 / 87 |
| σ²p (Sammler) | 1,07 | 0 % | 48 |

- **Artstatus (Occupancy-Koeffizienten):** 40 ok (beide Kriterien), 27 grenzwertig (nur Gesamtkriterium), **33 nicht konvergiert** (R-hat > 1,1). Problematisch sind v. a. Art-Achsenabschnitte und Saisonkoeffizienten; seltenere Arten konvergieren schlechter (Spearman ρ(R-hat, Funde) = −0,37). Liste in `out/22_species_flags.tsv`.
- **PPC** (Detektionsarrays exakt wie in 12 nachgebaut, gleiches Subsample; Sammler-Effekte je Ziehung neu aus N(0, σ²p) gezogen):
  - Gesamtzahl der Nachweise: Bayes-p = 0,47.
  - Je Art: keine Art extrem (Gesamtnachweise je Art werden reproduziert).
  - Je Dekade: p zwischen 0,05 (1980er) und 0,90; keine Dekade extrem.
  - Je Quelle: GBIF/ZOBODAT leicht unterschätzt (p = 0,01), sonst 0,20–0,91.
  - **Freeman-Tukey je Art × Zelle-Dekade: p = 0,00; 66 % der Arten extrem → Überdispersion.** Nachweise sind stärker gebündelt als modelliert. Teils Testartefakt (echte Sammler-Effekte nicht gespeichert), teils echte Heterogenität.
  - Kalibrierung: sehr kleine p überschätzt (vorhergesagt 0,0018 vs. beobachtet 0,0006), mittlere leicht unterschätzt (0,14 vs. 0,19).
- **Detektion:** Listenlänge Odds × 2,24 [2,17; 2,33] je Verdopplung; Maximum im Frühsommer; EBHD −0,80 [−1,31; −0,36] gegenüber GBIF; Pittioni, Linz und CLIMBEE n. s.

## 3 A1 Climatic debt

| | Occupancy-Modell | naiv |
|---|---|---|
| alle Zellen | **56 % [40; 71]** (within 0,117 [0,081; 0,152]; between 0,212 [0,183; 0,233]) | 13 % |
| extensiv | 70 % [44; 93] (within 0,115; between 0,167) | 15 % |
| intensiv | 51 % [38; 66] (within 0,119; between 0,233) | 16 % |
| Δ intensiv − extensiv | −18 Pp. [−38; 5], P(< 0) = 0,95 | – |
| inkl. nicht besuchter Zellen | 57 % [40; 73] | – |

Verlauf: Beobachteter und erwarteter CWM-STI laufen bis in die 1980er parallel. Danach steigt die Erwartung steiler; in den 2000/10ern liegt die Beobachtung um 0,110 [0,061; 0,158] °C darunter.

## 4 A2 Landnutzung zeitvariabel

Regression je Ziehung (Zellen mit ≥ 2 Dekaden; Intensität je 10 Pp.):

| Term | ohne Ausgangsniveau | mit Ausgangsniveau |
|---|---|---|
| T_w | 0,118 [0,079; 0,154] | 0,118 |
| ΔI (I_w) | −0,006 [−0,026; 0,012] | −0,005 |
| T_w × I_Zellmittel | 0,001 [−0,005; 0,008] | 0,004 [−0,002; 0,010] |
| T_w × ΔI | **+0,014 [0,003; 0,025]** | +0,014 [0,003; 0,025] |
| T_w × CWM erste Dekade | – | −0,024 [−0,056; 0,010] |

- Die Intensität variiert zwischen Zellen viel stärker als innerhalb (SD 3,33 vs. 0,62 je 10 Pp.); vor 1960 ist HILDA+ rückextrapoliert.
- **Effektkurve (mittlere Art):** Temperatursteigung bei niedriger Intensität +0,19 [0,09; 0,31] logit/°C, bei mittlerer +0,09 [−0,01; 0,21], bei hoher −0,26 [−0,41; −0,11]. Die Kurven sind auf den beobachteten Temperaturbereich ähnlich intensiver Zellen beschränkt.
- **Bewertung:** Der Interaktionsterm des Occupancy-Modells ist robust. Als „Bremse des zeitlichen Nachziehens“ ist er mit Lauf 1 aber **nicht** gestützt.

## 5 A3 Aridität vs. Temperatur je Art

- r(β_Temperatur, STI) = 0,46 [0,36; 0,55]; nur konvergierte und grenzwertige Arten: 0,46 [0,35; 0,56].
- r(β_logAI, SAI) = 0,58 [0,51; 0,65]; r(β_logAI, SAI-Rest) = 0,21 [0,12; 0,31] (konvergiert: 0,34 [0,23; 0,44]).
- Sichere Art-Effekte: Temperatur +14 / −13 Arten; log AI +14 / −38 Arten; T × I negativ bei 32 Arten, positiv bei keiner. Bei 59 Arten überwiegt wahrscheinlich |β Aridität| gegenüber |β Temperatur|.
- **Bewertung:** Die Nischenindizes sind mit unabhängigen AT-Daten validiert (Gemeinschaftsmuster belastbar). Die Effekte einzelner Arten sind vorläufig.

## 6 B1 Attribution Klima vs. Landnutzung (1950er → 2010er)

**Methode:** Kovariatenbasierte ψ **ohne** AR(1)-Dekadeneffekte (über σ²t mit der Probit-Näherung integriert). Kovariaten im Zellmittel: T 7,0 → 8,9 °C; log AI 0,347 → 0,251; Intensität 0,336 → 0,356.

| Komponente | Δ erwartete Arten je Zelle |
|---|---|
| gesamt | +2,25 [0,88; 3,36] (33,6 → 35,8) |
| Klima (T + AI) | +1,67 [0,18; 2,89] |
| davon nur Temperatur | +0,07 [−1,57; 1,42] |
| Landnutzung | +0,27 [0,14; 0,39] |
| Interaktion | +0,30 [0,22; 0,40] |

- Je Art ist der Klimaanteil sicher positiv bei 18 Arten und sicher negativ bei 13. Der Landnutzungsanteil ist sicher positiv bei 8 und negativ bei 3. Bei 63 Arten ist keiner der beiden Anteile sicher.
- Der Klimaanteil korreliert mit dem STI (r = 0,42 [0,34; 0,50]).
- Klima trägt 93 % [91; 95] der Summe der Absolutbeiträge.
- **Bewertung:** Auf Gemeinschaftsebene ist die Richtung belastbar (Klima ≫ Landnutzung). Die Landnutzungsänderung in HILDA+ ist im Zellmittel klein. Artweise Ergebnisse sind vorläufig.

## 7 B2 Gewinner/Verlierer und Traits

**Abgrenzung:** Überschneidung mit dem RL-Projekt (Esther) und der NHM-Roten Liste. Hier als Klima- und Landnutzungs-Attribution gerahmt, keine Gefährdungseinstufung; vor Verwendung abstimmen.

- Occupancy-Anteil der 302 Zellen, 1930/40er → 2000/10er: 11 Arten nehmen sicher zu, 13 sicher ab (nur ok/grenzwertig: 9 / 10). Die mittlere Occupancy ändert sich kaum (34,7 % → 33,9 %). Die Δ-Werte haben bei 5 Arten R-hat > 1,1.
- Größte Gewinner: *Hylaeus confusus* (+64 Pp.), *Bombus hypnorum* (+33), *Anthophora plumipes* (+30), *Andrena dorsata*, *Colletes cunicularius*, *Andrena fulvata* (je +19).
- Größte Verlierer: *Andrena rosae* (−33), *Megachile alpicola* (−28), *Nomada ferruginata* (−27), *Andrena clarkella* (−27), *Lasioglossum fulvicorne* (−22), *Andrena ruficrus* (−19).
- Traits:
  - Einzeln (Spearman mit Δ logit): STI 0,20 [0,09; 0,30], SAI-Rest 0,17 [0,05; 0,28]; ITD, Parasitismus und Lektie n. s. (oligolektisch −0,11 [−0,24; 0,00]).
  - Multiple Regression (95 Arten; Posterior- und Regressionsunsicherheit): kein Trait klar, am ehesten der STI (0,15 [−0,12; 0,43], P(> 0) = 0,84).

## 8 B3/B5 Verschiebungen

- Gemeinschaftsmittel der occupancy-gewichteten Schwerpunkte, 1930/40er → 2000/10er: Δx −8,0 [−11,3; −4,6] km (nach Westen), Δy −4,5 [−6,2; −2,6] km. Die Zellmitteltemperatur am Schwerpunkt sinkt um −0,25 [−0,32; −0,17] °C, Δ log AI +0,037 [0,026; 0,048]. Die Schwerpunkte verlagern sich also in kühlere, feuchtere Zellen.
- Je Art: in kühlere Zellen 14, in wärmere 0 Arten; nach Westen 8, nach Osten 2 Arten. Wärmeliebende Arten verlagern sich weniger in kühlere Zellen (r(ΔT, STI) = 0,31 [0,10; 0,49]).
- **Bewertung:** vorläufig. Die Schwerpunkte stützen sich auch auf imputierte Zellen und können eine Verlagerung der Sammeltätigkeit (früh Osten, später Alpen) übernehmen.

## 9 B4 Kredit/Schuld (vereinfacht)

- Differenz zwischen erwarteter (Σ ψ aus Kovariaten) und z-basierter Artenzahl je besuchter Zelle × Dekade, je Dekade zentriert: räumlich bis etwa ±4 Arten.
- **Kein Zusammenhang mit der Intensität** (r = 0,02 [−0,07; 0,12]).
- Die unzentrierte Differenz schwankt zwischen −2 und +2 Arten (2010er +2,00 [0,13; 4,01]) und spiegelt v. a. den fehlenden AR(1)-Effekt.
- **Bewertung:** explorativ. Für eine echte Analyse braucht es gespeicherte ψ/η und Kolonisierungs-/Extinktionsraten (Lauf 2).

## 10 C1 Trait-CWMs, C2 Homogenisierung, C3 Wirt–Kuckuck

| CWM | within T | between T | Ratio |
|---|---|---|---|
| STI | 0,117 [0,081; 0,152] | 0,212 [0,183; 0,233] | 56 % [40; 71] |
| SAI gegen log AI | 0,118 [0,084; 0,148] | 0,144 [0,127; 0,157] | 82 % [60; 102] |
| SAI-Rest | 0,005 [0,003; 0,007] | 0,004 [0,002; 0,006] | 127 % [73; 221] |
| Anteil oligolektisch | −0,019 [−0,029; −0,009] | −0,011 [−0,018; −0,005] | 170 % [84; 350] |
| Anteil Bodennister | −0,017 [−0,024; −0,010] | 0,001 [−0,003; 0,005] | nicht interpretierbar |
| Anteil Parasiten | −0,013 [−0,024; −0,003] | 0,010 [0,000; 0,017] | nicht interpretierbar |
| ITD | 0,009 [−0,011; 0,026] | −0,014 [−0,025; −0,003] | n. s. |

- Lesart: Oligolektische Arten, Bodennister und Parasiten nehmen zeitlich ab, stärker als bzw. entgegen dem räumlichen Klimagradienten. Das deutet auf Treiber jenseits des Klimas (Landnutzung, Sammelpraxis).
- **C2:** Jaccard 1930/40er → 2000/10er +0,015 [−0,011; 0,042] (alle Zellen) bzw. +0,023 [−0,005; 0,052] (besuchte Zellen): **keine sichere Homogenisierung**. Intensive Zellen sind durchweg ähnlicher als extensive (Niveau, kein Trendunterschied).
- **C3:** 13 Wirt–Kuckuck-Paare unter den 100 Arten. r(ΔOccupancy Kuckuck, Wirt) = 0,25 [−0,20; 0,62] (zufällige Paarung 0,00). Das ist nur ein Machbarkeitstest.

## 11 D4 Monitoring und E1 Sammlereffekte

Annahmen: besetzte Zelle, mittlere·r Sammler·in, Median-Art.

| Szenario | p je Besuch | Besuche für 80 % | für 95 % |
|---|---|---|---|
| Einzelfund-Besuch (Liste 1), Saisonmitte | 0,1 % | 1.088 [892; 1.331] | 2.024 |
| volle Liste (26,5 Arten), CLIMBEE, Saisonmitte | 6,3 % [4,0; 9,5] | 25 [16; 40] | 46 |
| volle Liste, CLIMBEE, artspezifisch bester Tag | 17,3 % [11,7; 24,4] | **8 [6; 13]** | 16 [11; 24] |
| volle Liste, GBIF, bester Tag | 18,2 % | 8 [7; 10] | 15 |

- Für 90 % der Arten braucht es 38 [22; 72] Besuche zur besten Zeit. Nur 56 % [42; 71] der Arten erreichen 80 % Nachweissicherheit mit ≤ 10 Besuchen.
- Folgerung für ÖBM / EU-PoMS:
  - Aufwand je Besuch (vollständige Liste, Dauer) zählt weit mehr als die Quelle.
  - Mehrere über die Saison verteilte Begehungen sind nötig.
  - Datum und Sammeldauer immer dokumentieren.
  - Die Detektion mitschätzen.
- **E1:** σ²p = 1,75 [1,57; 1,92]. Odds-Faktor zwischen Sammler·innen am 25./75. Perzentil 5,9 [5,4; 6,5], am 2,5./97,5. Perzentil 179 [135; 229]. Das ist mehr als der Unterschied zwischen den Quellen (EBHD vs. GBIF etwa Faktor 2). Für eine mittlere Art beim Einzelfund-Besuch: p = 0,02 % (10. Perzentil) vs. 0,73 % (90. Perzentil).

## 12 Was belastbar ist und was vorläufig

| Ebene | Status | Ergebnisse |
|---|---|---|
| Gemeinschaft | **belastbar** (μβ, μα konvergiert; Gesamt-PPC gut) | Debt-Ratio 56 %, Korrektur vs. naiv, T × I im Occupancy-Modell, gleiche Within-Steigung ext./int., Attribution Klima ≫ Landnutzung, Validierung der Nischenindizes |
| Varianzen | vorläufig | τ²β, σ²t, σ²p teils nicht ausgemischt (ESS 31–96) |
| Art | **vorläufig** (33 nicht, 27 grenzwertig konvergiert) | Gewinner/Verlierer, Attribution je Art, Schwerpunkte, Monitoring-Zahlen je Art, C3 |
| Modellanpassung | Schwäche | Überdispersion je Zelle × Dekade (Freeman-Tukey) |

**Nicht machbar mit Lauf 1:**
- D1 Schutzgebiete (Ausweisungs- und ÖPUL-Daten fehlen)
- D2 Kulturbestäuber (Gruppenzuordnung, alle Arten)
- D3 Projektion 2050 (Szenario-Kovariaten)
- C4 Pflanzen (Floren-Atlas)
- F HU-Erweiterung (Daten)
- B3 Ankunftszeiten neuer Arten (seltene Arten fehlen)

**Lauf 2:**
1. Alle Arten (≥ 10 Funde) in Blöcken.
2. Längere Ketten (30.000 Iterationen, Thinning 50) oder schwach informative Varianz-Priors; VSC.
3. Sammler-Effekte je Stufe, η und ψ speichern.
4. Detektion um einen Zufallseffekt Zelle × Dekade oder die Sammeldauer erweitern (Überdispersion); „unbekannt“ nach Quelle trennen.
5. Landnutzung mit mehr Klassen und nur ab 1960 zeitvariabel.
6. Für die Antragslinie „Landnutzung bremst“: zeitliche Within-Tests in den Vordergrund stellen. Die Raum-Interaktion allein trägt die Aussage nicht.
