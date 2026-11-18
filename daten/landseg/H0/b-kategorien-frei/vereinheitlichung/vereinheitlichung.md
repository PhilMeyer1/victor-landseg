# Vereinheitlichung der freien Klassen, Fassung B, Ausschnitt H0

Stand 2026-11-18. Grundlage: die 16 Viertel-Abgaben (`urteil.json`), zusammen 708 Segmente (jedes einmal), 359 Namen (Viertel x Ebene) und 71 verschiedene Namen der feinsten Ebene. Es wurde nichts am Bild neu beurteilt; die Zuordnung folgt `klasse_frei` und den Beschreibungen (`merkmal`) der Viertel.

## Ergebnis in Zahlen

- Klassen: Ebene 1 7 (Codes 0 bis 6), Ebene 2 19, Ebene 3 15, zusammen 41.
- Segmente mit Code: 708 von 708; alle Viertel-Abgaben lagen vor, nichts nachgeholt.
- Zusammengelegte Namen: 66 verschiedene Namen der feinsten Ebene fließen in 22 Klassen mit mehreren Quellnamen; insgesamt 54 Namen tragen in der Liste einen anderen Namen als im Viertel.
- Klassen ohne Segment (nur Gliederung): 0, 0.2, 1, 1.2, 2, 2.1, 3, 3.2, 4, 5, 5.1, 5.2, 6.

Hinweis zu den Zahlen: Die Segmentzahlen je Viertel im Auftrag (z. B. 58 für r0c0 v1) sind kleiner als die der Abgaben (63); die Viertel haben beim Arbeiten Segmente geteilt (Eingriffe). Codiert wurde, was in den Abgaben steht.

## Klassen und ihre Quellnamen

Je Klasse die feinsten Namen der Viertel (Zahl der Segmente). Die Klassennamen stehen in `kategorien-b-entwurf.json`.

- `0.1` Schlagschatten (21 Segmente): Schlagschatten (21)
- `0.1.1` Schatten zwischen Gebäuden (78 Segmente): Schatten zwischen Häusern (59), Gebäudeschatten (19)
- `0.1.2` Schatten von Gehölz oder Gebäude (unklar) (2 Segmente): Schatten oder Baumgruppe (1), Schatten oder Baumreihe (1)
- `0.2.1` Dachseite oder Hof im Halbschatten (43 Segmente): Dachseite oder Hof (30), Hof oder Dach, mittelgrau (13)
- `0.3` Dunkle Fläche (4 Segmente): Dunkle Fläche (4)
- `0.4` Fläche unbestimmt (18 Segmente): Siedlung (10), Schlagschatten (6), heller Fleck im Hof (1), heller runder Fleck (1)
- `1.1` Gebäude (21 Segmente): Gebäude mit mittelgrauem Dach (8), Gebäude mit hellem Dach (7), Gebäude (4), Dach (1), Gebäude mit dunklem Dach (1)
- `1.1.1` Wohn- oder Langhaus (77 Segmente): Langhaus, Dach Sonnenseite (40), Wohnhaus, helles Dach (20), Längsbau (11), Längsbau (Streckhof) (5), Querbau an der Straße (1)
- `1.1.2` Nebengebäude (16 Segmente): Nebengebäude (9), Nebengebäude, helles Dach (3), Hintergebäude (2), Halle oder Scheune, helles Dach (1), Kleinbau oder Fahrzeug (1)
- `1.2.1` Streckhof-Streifen (56 Segmente): Streckhof-Streifen (56)
- `2.1.1` Hof (offen) (79 Segmente): Hof oder Vorgarten (36), Hof (34), Hof/Freifläche (9)
- `2.1.2` Hof im Schatten (9 Segmente): Hof im Schatten (9)
- `2.1.3` Lagerplatz (1 Segmente): Lagerplatz (1)
- `2.2` Garten (25 Segmente): Garten (20), Garten, dunkel (Bäume oder Schatten) (3), Garten, fein gemustert (2)
- `3.1` Straße (50 Segmente): Dorfstraße (38), Straße (5), Fahrbahn (4), Landstraße (2), Fahrweg (1)
- `3.2.1` Feldweg (8 Segmente): Feldweg (4), Hinterweg (2), breiter Feldweg (1), Weg breit (1)
- `3.2.2` Gasse oder Hofweg (5 Segmente): Gasse (3), Hofweg (1), Hofzufahrt (1)
- `3.3` Straßenrand (47 Segmente): Straßenrand (25), Randstreifen (Bankett oder Gehweg) (20), Bankett (1), Randstreifen, dunkel (Bewuchs?) (1)
- `3.4` Platz oder Vorplatz (15 Segmente): Vorplatz (14), Anger/Platz (1)
- `4.1` Baum (10 Segmente): Baum (8), Einzelbaum (2)
- `4.2` Gebüsch (11 Segmente): Gebüsch (9), Strauch am Straßenrand (2)
- `4.3` Baumreihe oder Hecke (5 Segmente): Hecke (2), Baumreihe/Hecke (2), Baumreihe (1)
- `4.4` Baum oder Gebüsch (nicht trennbar) (23 Segmente): Baum/Gebüsch (22), Baumgruppe (1)
- `5.1.1` Feldrain (17 Segmente): Feldrain (17)
- `5.1.2` Wegrain (26 Segmente): Rain/Wegrand (15), Wegrain (11)
- `5.2.1` Anger (13 Segmente): Anger (10), Anger (Gras) (3)
- `5.2.2` Brache (6 Segmente): Brache (5), Brache mit Gebüsch (1)
- `6.1` Feld (22 Segmente): Acker (15), Feld (7)

## Zusammengelegt (und warum)

- `0.1.1` Schatten zwischen Gebäuden: Gebäudeschatten und Schatten zwischen Häusern sind derselbe schmale Schlagschatten zwischen Dächern.
- `0.1.2` Schatten von Gehölz oder Gebäude (unklar): Die Viertel nennen den Werfer unsicher (Baumgruppe, Baumreihe); Schatten ohne gesicherten Werfer.
- `0.2.1` Dachseite oder Hof im Halbschatten: Dachseite oder Hof und das dreizehnmal von r0c1 v3 genannte Hof oder Dach, mittelgrau sind dieselbe mittelgraue Fläche neben hellem Dachstreifen.
- `0.4` Fläche unbestimmt: Heller Fleck, heller runder Fleck und Siedlung-Siedlung (Fläche im Ort, Art nicht bestimmbar) sind Flächen ohne deutbares Merkmal.
- `1.1` Gebäude: Allgemeine Gebäude-, Dach- und Dachton-Namen (heller, mittelgrauer, dunkler Dachton) sind Beleuchtung, kein anderes Ding.
- `1.1.1` Wohn- oder Langhaus: Längsbau, Langhaus, Wohnhaus und Querbau trennt der Schwarz-Weiß-Scan nicht (Wohn- und Wirtschaftsteil).
- `1.1.2` Nebengebäude: Nebengebäude, Hintergebäude, Halle oder Scheune und Kleinbau sind kleinere Bauten am Grundstücksende.
- `2.1.1` Hof (offen): Hof, Hof oder Vorgarten und Hof/Freifläche beschreiben dieselbe offene Fläche an den Gebäuden.
- `2.2` Garten: Garten, dunkler Garten und fein gemusterter Garten unterscheiden sich nur im Grauton.
- `3.1` Straße: Fahrweg und Fahrbahn (je etwa 10 Bildpunkte, sehr hell), Straße, Dorfstraße und Landstraße sind dieselbe breite Fahrbahn; innerorts oder außerorts folgt aus dem Ort, nicht aus dem Bild.
- `3.2.1` Feldweg: Feldweg, breiter Feldweg, Weg breit und Hinterweg (hinter den Höfen) sind schmale Wege am Feld oder hinter den Höfen.
- `3.2.2` Gasse oder Hofweg: Gasse, Hofweg und Hofzufahrt sind kurze Wege zwischen oder in den Höfen.
- `3.3` Straßenrand: Straßenrand, Bankett und Randstreifen sind derselbe schmale Streifen an der Fahrbahn.
- `3.4` Platz oder Vorplatz: Vorplatz und Anger/Platz sind offene helle Flächen an der Straße; Vorplatz stand in einem Viertel unter Verkehr, im anderen unter Hof (r1c1), hier einheitlich unter Verkehr.
- `4.1` Baum: Baum und Einzelbaum.
- `4.2` Gebüsch: Gebüsch und Strauch am Straßenrand.
- `4.3` Baumreihe oder Hecke: Baumreihe, Hecke und Baumreihe/Hecke trennt das Bild nicht scharf.
- `4.4` Baum oder Gebüsch (nicht trennbar): Baum/Gebüsch und Baumgruppe: Krone und Strauch nicht trennbar.
- `5.1.2` Wegrain: Wegrain und Rain/Wegrand (Saum zwischen Weg und Feld).
- `5.2.1` Anger: Anger und Anger (Gras).
- `5.2.2` Brache: Brache und Brache mit Gebüsch; r1c0 führte Brache unter Offenland, r0c0 unter Grünfläche, hier einheitlich unter Grünfläche.
- `6.1` Feld: Feld und Acker; Acker oder Grünland ist im Schwarz-Weiß nicht zu trennen (die Viertel sagen es selbst).

Ebenen: Feldrain stand in drei Vierteln unter drei verschiedenen Eltern (Saum, Rain, Landwirtschaft); er steht jetzt einmal unter Grünfläche, Saum (`5.1.1`). Rain/Wegrand aus r1c1 (Landwirtschaft > Feldrain) wurde Wegrain (`5.1.2`), weil die Beschreibung "zwischen Weg und Feld" lautet. Auch die Oberklassen Offenland (r1c0), Freifläche (r0c1), Siedlung und Verkehr (r1c1), Bebaut und Bebauung wurden auf die sieben Klassen der Ebene 1 verteilt; Gehölz, Grünfläche, Landwirtschaft und Verkehrsfläche heißen auch in der Liste so.

## Getrennt gehalten (und warum)

- Schlagschatten (`0.1`), Halbschatten (`0.2`) und Dunkle Fläche (`0.3`): drei Bildzustände mit unterschiedlicher Aussage (sicher Schatten; Dach oder Hof; Untergrund völlig unsichtbar). Sie liegen unter Klasse 0 und sind keine Bodenbedeckung.
- Hof im Schatten (`2.1.2`) bleibt neben Hof (`2.1.1`): fast schwarze Hoffläche mit ihrem eigenen Grauton, aber von den Vierteln als Hof benannt; Lagerplatz (`2.1.3`) bleibt wegen der sehr hellen, gestreiften Fläche (nur ein Segment).
- Straße (`3.1`) und Weg (`3.2`): breit und durchgehend gegen schmal; r0c0 v4 gibt die Grenze mit etwa 8 Bildpunkten an. Straßenrand (`3.3`) bleibt getrennt vom Saum (`5.1`): Streifen unmittelbar an der Fahrbahn gegen Streifen zwischen Feld, Weg und Hof.
- Wohn- oder Langhaus (`1.1.1`) gegen Nebengebäude (`1.1.2`): Lage und Größe tragen den Unterschied (Langhaus an der Straße, Nebengebäude am Grundstücksende). Hofstelle (`1.2`) bleibt eigen, weil r1c1 in den Streckhof-Streifen Dach und Hof bewusst nicht trennt.
- Anger (`5.2.1`) und Brache (`5.2.2`): Anger hat helle Fahrspuren, Brache keine.
- Feld (`6.1`) und Grünfläche (`5`): gleichmäßiges Korn mit Streifen gegen fleckig ohne Bewirtschaftungsmuster.

## Namen, die auf mehrere Klassen verteilt wurden

Einige Oberbegriffe der Viertel sind breiter als eine Klasse; in `namen` steht der Code der Mehrheit ihrer Segmente, die Segmente selbst tragen ihre eigenen Codes:

- r0c0 v4, grob "Bebauung": `2` (7), `1` (1)
- r0c1 v1, grob "Freifläche": `2` (5), `3` (1)
- r0c1 v3, grob "Freifläche": `2` (8), `5` (2)
- r0c1 v4, grob "Freifläche": `2` (9), `5` (1)
- r1c0 v1, grob "Offenland": `6` (4), `5` (1)
- r1c0 v2, grob "Bebauung": `1` (2), `2` (1)
- r1c0 v3, grob "Offenland": `6` (2), `5` (1)
- r1c0 v4, grob "Offenland": `6` (2), `5` (1)
- r1c1 v1, grob "Landwirtschaft": `5` (4), `6` (2)
- r1c1 v1, grob "Siedlung": `1` (36), `3` (5), `2` (3), `0` (2)
- r1c1 v1, mittel "Hof/Freifläche": `3.4` (5), `2.1` (2)
- r1c1 v2, grob "Siedlung": `1` (20), `0` (7), `2` (5), `3` (2)
- r1c1 v2, mittel "Hof/Freifläche": `2.1` (5), `3.4` (2)
- r1c1 v3, grob "Landwirtschaft": `5` (11), `6` (2)
- r1c1 v3, grob "Siedlung": `3` (3), `1` (1), `0` (1)
- r1c1 v4, grob "Siedlung": `1` (18), `2` (3), `3` (2)
- r1c1 v4, mittel "Hof/Freifläche": `2.1` (2), `3.4` (2)

## Offen geblieben

- `offen` in `codes.json` ist leer: jedes Segment und jeder Name hat einen Code.
- Unsicherste Stellen: die Trennung Wohn- gegen Nebengebäude (`1.1.1`/`1.1.2`) und Hof gegen Dach im Halbschatten (`0.2.1`, 43 Segmente, davon 13 in r0c1 v3 als "Hof oder Dach, mittelgrau") ist am Bild nicht gesichert; auch die Gleichsetzung von Dorfstraße und Landstraße (`3.1`) und von Baumreihe und Hecke (`4.3`) beruht auf den Beschreibungen, nicht auf neuem Ansehen der Bilder.
- Die Spalte `bw` und die Zuordnungen (`mappings`) der Liste sind Formatpflicht: `bw` ist vermutet (Urteile der Agents am Scan), `mappings` ist leer. Die Farben sind vom Vereinheitlicher gesetzt (kleinster Abstand dE 10,1).
- Die Viertel haben Nähte zu Nachbarn nur einseitig angesehen (siehe `nicht_geprueft` in den Abgaben); dieselbe Fläche kann dort verschieden benannt sein, in der Liste aber im selben Code landen, soweit die Namen oben zusammengelegt sind.
- Es wurde keine Viertel-Abgabe, keine Label-Karte und kein Originalbild geändert.
