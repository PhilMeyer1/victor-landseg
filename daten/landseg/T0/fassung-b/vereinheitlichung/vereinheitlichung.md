# Vereinheitlichung der freien Klassen, Fassung B (T0)

Eingabe: 16 Viertel-Abgaben, 641 Segmente, 127 verschiedene Namen (Ebene und Name), 368 Namenseinträge der Viertel.
Ergebnis: 49 Klassen (7 auf Ebene 1, 21 auf Ebene 2, 21 auf Ebene 3), Code je Segment aus `fein`. Farben: kleinster CIELAB-Abstand 11,9.
Nach Bild habe ich nicht neu geurteilt; die Zusammenlegung folgt den Namen und den Merkmal-Texten der Viertel.

## Zusammengelegt (gleiche Sache, verschiedene Namen)

- Einzelbaum 1.1.1: Einzelbaum, Laubbaum, Nadelbaum, Blutbuche. Laub und Nadel sind nur 3 Segmente und im Viertel meist nicht bestimmt; offen, ob eine eigene Stufe lohnt.
- Gebüsch 1.3: Gebüsch, Strauch, Strauchgruppe, Gebüsch oder kleiner Baum, Gartengehölz, Gebüschfläche, Strauchreihen (Beerenobst-Reihen, 1 Segment, nach Bildmerkmal dunkle Strauchkronen).
- Wald beschattet 1.2.2: Wald beschattet, Schatten auf Wald (gleiches Bildmerkmal: dunkles Kronendach).
- Wiese 2.1: Wiese, Wiese lückig, Wiese mit Gebüsch. Wiese gemäht 2.1.1: auch Mähwiese mit Heu, Wiesenstreifen. Wiese ungemäht 2.1.2: auch Altgras mit Gebüsch.
- Rasen 2.2: Rasen, Hausrasen, Rasen mit Strauch, Rasenweg, Straßenbegleitgrün (Grünstreifen).
- Saum und Randstreifen 2.3: Saum, Saum verbuscht, Randstreifen, Feldrain.
- Feld abgeerntet 3.1.1: Feld mit Schwaden, Feld gemäht (gleiches Bild: beige Fläche mit Schwaden), obwohl ein Viertel es unter „Offener Boden“ führte.
- Parzelle gemischt 3.3.2: Parzelle gemischt, Terrassengarten, Garten mit Gehölz (Siedlungsgrün).
- Wohnhaus 4.1.1: Wohnhaus, Fassade. Nebengebäude 4.1.2: Nebengebäude, Anbau, Garage, Gartenhütte, Gartenhaus, Schuppen.
- Kleinobjekt 4.3: Kleinobjekt, Abdeckplane, Rundbecken, Gartenausstattung. Mauer 4.2: Mauer, Stützmauer. Holzlager 4.4.1: Holzstapel.
- Schwimmbecken 5.1: Schwimmbecken (Ebene „Bebaut“ und „Wasser“), Aufstellpool, Pool.
- Betonstraße 6.1.2: Betonstraße, Betonfahrbahn. Feld- und Erdweg 6.2.2. Trampelpfad 6.2.3 (aus „Weg“, „Verkehr“, „Pfad“).
- Hof und Zufahrt 6.3: Hof, Einfahrt, Vorplatz im Schatten, Betonfläche, Zufahrt.
- Randstein und Bankett 6.5: Randstein, Straßenrand, Schotterbankett.
- Gleiche Namen auf verschiedenen Ebenen (Weg, Straße, Rasen, Terrasse, Gebäude) liefen ebenfalls unter einem Code zusammen. Insgesamt gingen 67 Namen in einem anderen Namen auf.

## Getrennt gehalten

- Garten mit Gehölz (3.3.2, Fläche) gegen Gartengehölz (1.3, Gebüsch im Garten): erst ist die Gartenfläche gemeint, dann die Gehölzkrone.
- Gebäudeschatten und Heckenschatten (0.1.1, 0.1.2) gegen Wald beschattet: Schatten auf Gehölz bleibt Wald, weil der Wald darunter erkennbar ist; Schatten auf Boden bleibt Klasse 0.1, weil der Boden nicht erkennbar ist.
- Wiese gegen Rasen gegen Saum: verschiedene Bildmerkmale (Halmstruktur, gleichmäßig kurz, schmaler Streifen am Rand).
- Straße gegen Randstein und Bankett: Randstreifen am Rand eigener Streifen.

## Besonderheiten und offen

- Ebene-1-Namen der Viertel mit gemischtem Inhalt: „Siedlungsgrün“ steht in `namen` unter Code 2 (Garten darunter ist 3.3), „Schatten“ unter 0 (Schatten auf Gehölz ist 1.2.2), „Weg“ als Ebene grob unter 6. Hinweis: Diese vier Einträge sind Näherungen.
- Klasse 0 (Nicht bestimmbar) ist nur Elternklasse für Schlagschatten; kein Segment trägt sie selbst.
- Segmente tragen oft eine Elternklasse (Wiese 2.1, Gebäude 4.1, Schlagschatten 0.1, Kleinobjekt 4.3, Mauer 4.2), wenn das Viertel nicht feiner benannt hat. 14 Klassen bleiben ohne eigenes Segment (die Ebene-1-Klassen und Eltern 1.1, 1.2, 3.1, 3.3, 4.4, 6.1, 6.2).
- Nicht im Viertel unterschieden und darum nicht getrennt: Laub- gegen Nadelbaum, Strauch gegen Strauchgruppe, Gartenweg gegen Feldweg (Gartenweg ist getrennt, weil 11 Segmente).
- Offen: Ob „Feld gemäht“ (14 Segmente aus einem Viertel, dort „Offener Boden“) wirklich abgeerntetes Feld und nicht Wiese gemäht ist, ist am Bild nicht nachgeprüft.
- Fehlende Abgaben: keine, alle 16 Viertel und alle 641 Segmente liegen vor. `nicht_geprueft` der Viertel (Bilder nicht angesehen) steht in deren Abgaben und ist nicht übernommen.
