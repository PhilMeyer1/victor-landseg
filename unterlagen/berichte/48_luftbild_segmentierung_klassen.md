# Briefing: Klassen für die Segmentierung historischer Luftbilder (AridiBEE, Projekt 1)

**Stand:** 2026-11-17 · **Zweck:** Übergabe an eine andere Session / Person, die die Segmentierung aufsetzt.

## Kontext

- **Projekt:** 120-jährige, detektionskorrigierte Rekonstruktion von Wildbienengemeinschaften in Österreich (10-km-Zellen × Dekade, 1900–2020), Attribution auf Erwärmung, Trockenheit und Landnutzung.
- **Problem:** HILDA+ (1 km, 6 Klassen) bildet keine Landnutzungsintensität ab. Mit HILDA+ zeigt sich zeitlich kein Unterschied zwischen extensiv und intensiv genutzten Zellen.
- **Ziel:** Intensität und bienenrelevante Strukturen historisch erfassen. Feldebene **nur in Pilot- und Resurvey-Zellen** (ca. 10–20 Zellen × 3–4 Zeitschnitte: 1950er, 1970er, 1990er, 2010er). Für die Fläche dient ein Panel aus Gemeinde × Dekade.
- **Bildmaterial:** BEV-Luftbilder ab 1949 (Schwarz-Weiß, ca. 0,5–1 m). Erkennbar sind nur Grauton, Textur, Form und Muster, keine Spektralinformation. Farbbilder ab den 1990ern für Vergleichbarkeit in Graustufen umwandeln.
- **Hintergrund:** `46_landnutzung_hochaufgeloest.md` (Datenquellen), `47_raeumliche_genauigkeit_bienendaten.md` (Auflösung der Bienendaten).

## Ebene 1: robust in allen Jahrgängen

| Klasse | Merkmal im Bild | Kataster / INVEKOS |
|---|---|---|
| Versiegelt / bebaut | Form, harte Kanten | Bauarea, Siedlung |
| Acker | Parzellen, Bearbeitungsspuren | Acker |
| Dauergrünland | gleichmäßige, feine Textur | Wiese, Weide, Hutweide |
| Wald | grobe Kronentextur, dunkel | Wald |
| Gewässer / Feuchtgebiet | sehr dunkel bzw. glatt | Gewässer, Sumpf |
| Offener Boden / Fels | sehr hell | Ödland, Unland |

## Ebene 2: bienenrelevant (wo erkennbar)

| Klasse | Relevanz für Bienen | Erkennbarkeit |
|---|---|---|
| Trockenrasen / Steppenrasen | Kernhabitat, Bodennister | mittel (fleckig, helle Stellen) |
| Weingarten | Weinbaulandschaft, Böschungen | gut (Zeilentextur) |
| Streuobst / Obstgarten | Frühjahrsblüte, Totholz | gut (Einzelbäume im Grünland) |
| Brache / Ödland | Blüten, offener Boden | mittel |
| Feldraine, Wegränder, Böschungen (linear, ≥ 2 m) | Nistplätze, Blüten, Vernetzung | gut als Linien |
| Hecken, Baumreihen, Feldgehölze | Nistplätze (Holz, Stängel) | gut |
| Offene Sand-, Löss- und Lehmstellen (Hohlwege, Abbrüche, Gruben) | wichtigstes Nisthabitat für Bodennister | gut bis mittel (sehr hell, klein) |
| Verbuschung / Sukzession | Verlust offener Habitate | mittel |
| Wiese vs. Weide | Mahd vs. Beweidung | schwierig, besser über Kataster und Statistik |
| Hausgärten / Siedlungsgrün | Blütenangebot | als Teil der Siedlung führen |

## Abgeleitete Maße (je Zelle; 500-m-Umkreis nur um genau verortete Fundorte)

> **Wichtig (47_raeumliche_genauigkeit_bienendaten.md):** Historische Bienenfunde sind nur auf Ortschafts- oder Gemeindeebene verortet (≤ 250 m: vor 1960 0,7 %, 1960–99 3,6 %, ab 2000 52 %). Fundpunkt-Puffer sind daher nur sinnvoll für CLIMBEE-Plots, BINATS-Flächen, die Linz-Polygone, den Resurvey 2028 und Funde ab etwa 2010 mit ≤ 250 m. Für historische Vergleiche die Maße je Zelle bzw. je Gemeinde berechnen.

- mittlere **Schlaggröße** (stärkster Indikator für Intensivierung und Kollektivierung)
- **Dichte linearer Elemente** (Raine, Hecken; m/ha)
- **Anteil naturnaher Flächen** (Trockenrasen, Brache, Raine, Hecken, offene Bodenstellen)
- **Anteil offener Bodenstellen** (Nisthabitat)
- **Landschaftsvielfalt** (Shannon über Klassen), **Randdichte** (Kontakt Acker zu naturnah)

## Vorgaben

1. **Mindestgröße der Kartierung:** Flächen 100–400 m², Linien ab 2 m Breite.
2. **Gleiche Klassenliste für alle Jahrgänge**, damit die Zeitreihe vergleichbar bleibt.
3. **Übersetzungstabelle** zu den Kategorien des Franziszeischen Katasters (Acker, Wiese, Weide, Hutweide, Garten, Weingarten, Wald, Ödland) und zu den INVEKOS-Kulturarten pflegen, damit Kataster, Luftbild und INVEKOS eine durchgehende Reihe bilden.
4. **Ground Truth:** Geländeaufnahme in den CLIMBEE-Plots, den BINATS-Testflächen und den Resurvey-Standorten 2028. Historisch dienen Flurnamen als Hinweise („Heide“, „Sandgrube“, „Hohlweg“).
5. **Vorgehen halbautomatisch:** manuell annotierte Kacheln, darauf ein Segmentierungsmodell trainieren, dann Qualitätskontrolle je Klasse (Konfusionsmatrix, Genauigkeit je Jahrgang berichten).
6. **Interessenkonflikt:** Falls NAI technisch hilft, nur als unentgeltliche Beistellung wie bei der Artbestimmung (siehe Skizze v4/v5, NAI-Regelung).

## Offene Punkte

- Auswahl der Pilot- und Resurvey-Zellen: siehe `38_resurvey_kandidaten_datenanfragen.md`.
- Bildbezug: Kosten BEV ca. 10–25 € je Bild; Jahrgänge je Zelle prüfen.
- Ob Wiese und Weide in SW-Bildern trennbar sind: an einer Stichprobe testen.
