---
name: landseg-agent
description: Regeln für Agents, die in der Landschafts-Segmentierung (Repo landseg) Teilkacheln beurteilen, Label-Karten bearbeiten, Kommentare umsetzen oder Nähte klären oder Klassen an den Übergängen einigen. Lesen, bevor ein Auftrag aus vorlagen/ (urteil, umsetzen, korrektur, naht, einigung) bearbeitet wird.
---

# Agent-Regeln der Landschafts-Segmentierung

Diese Regeln gelten für jeden Agent-Auftrag aus `vorlagen/` (Urteil, Umsetzen, Korrektur, Naht, Einigung).
Der Auftrag nennt Gegenstand, Daten und Abgabe; hier steht, wie gearbeitet wird. Sie sind aus der
Stitcher-Methode übernommen und auf Landschaft umgestellt (Ermittlung `landseg-methode`).

## Begriffe

- **Label-Karte**: Segment-ID je Bildpunkt (32 Bit), 0 heißt „kein Segment“ und darf nie vorkommen.
- **Teilkachel**: Kern (der Teil, für den sie zuständig ist) plus Kontextrand (nur zum Ansehen).
  Jeder Bildpunkt des Ausschnitts gehört genau einem Kern.
- **Globale ID**: Die Vorstufe vergibt IDs über den ganzen Ausschnitt; ein Segment, das über eine
  Kerngrenze reicht, hat in beiden Teilkacheln dieselbe ID.
- Koordinaten in Bildpunkten, `x` Spalte, `y` Zeile; im Teilkachelbild, wenn nicht anders gesagt.

## Regeln

- **L1 Lückenlos.** Jeder Bildpunkt gehört zu genau einem Segment mit genau einer Klasse. Du
  änderst Segmente nur mit `python -m landseg eingriff` auf der Label-Karte, nie über Einzelmasken
  oder eigene Schreibroutinen; nach jedem Schritt muss `pruefen` `ok` melden. Nichts darf fehlen:
  Ein Stück unter der Mindestfläche wird mit dem passenden Nachbarn verschmolzen, nie weggelassen.
- **L2 Nur im Kern schreiben.** Den Kontextrand siehst du an, änderst ihn aber nicht; was dort
  steht, zählt beim Zusammentragen nicht. Reicht eine Änderung bis an den Kernrand, meldest du das
  Segment unter `naht`.
- **L3 Klassen nur aus `kategorien.json`.** Wähle die feinste Ebene, die im Bild sicher erkennbar
  ist, sonst die Elternklasse; halte dich an die Regeln G1–G5 und U1–U5 in `KATEGORIEN.md`. Bist du
  unsicher, setzt du `sicher: false` und nennst den Grund, statt zu raten.
- **L4 Kante aus dem Bild.** Grenzen liegen auf der sichtbaren Kante (Farb- oder Helligkeitsumschlag
  im engen Band, Werkzeug `kante`). Wo das Bild nichts hergibt, setzt du die Grenze von Hand und
  meldest die Strecke als geschätzt. Keine Geraden und keine Stufen, wo das Bild eine geschwungene
  Grenze zeigt.
- **L5 Fein arbeiten.** Vor jedem Schnitt oder jeder Grenzverschiebung so weit vergrößern, dass die
  Grenze bildpunktgenau erkennbar ist; Linienzüge mit so vielen Punkten, wie die Kontur verlangt.
  Danach beide Seiten stark vergrößert ansehen.
- **L6 Nahtregel.** An jeder Kerngrenze gilt: gleiche ID auf beiden Seiten oder eine echte
  Bildkante; eine ID, die über die Grenze reicht, hat auf beiden Seiten dieselbe Klasse; keine
  Gerade ohne Bildkante. Eine Stelle, ein Urteil: Ein Segment über eine Naht wird einmal
  entschieden, das gilt für beide Teilkacheln.
- **L7 Genau den Auftrag.** Bei einer Korrektur setzt du genau den Kommentar um; alles andere bleibt
  bildpunktgleich. Ist etwas nicht eindeutig: umsetzen, was eindeutig ist, den Rest unter `offen`
  mit der Angabe, die es klären würde.
- **L8 Fremde Eingriffe.** Eingriffe des Nutzers oder anderer Agents darfst du ändern, wenn du sie
  am Bild sicher für falsch hältst; jeden Fall nennst du mit Begründung (wer, was, warum). Bei
  Unsicherheit änderst du nicht, sondern meldest.
- **L9 Auffälliges zuerst.** Grobe Fehler (falsche Klasse großer Flächen, Segmente über klare
  Kanten hinweg, Zerfall) zuerst nennen und beheben, dann die Feinheiten.
- **L10 Eingefrorener Stand, eigener Ordner.** Eingaben nur lesen. Eigene Dateien, Skripte und
  Kopien nur im Ergebnisordner des Auftrags, mit genau den Dateinamen aus dem Auftrag. Eigener
  Bearbeiter-Name bei jedem `eingriff`.
- **L11 Bilder selbst prüfen.** Höchstens 2000 Bildpunkte an der langen Seite, JPEG; Beschriftung
  deutsch, mit Umlauten und lesbar; sieh dir jedes fertige Bild noch einmal an (verdeckt nichts die
  Stelle, die es zeigt?). Übersichtsbilder (ganzer Ausschnitt, ganze Teilkachel, Viertel) verlangt nur
  der Auftrag, an genau einer Stelle; ein Prompt wiederholt sie nicht, und du siehst jedes nur einmal an.
  Nahansichten sind ein Paar in einem Bild: links roh, rechts dieselbe Stelle mit Grenzen und Nummern,
  im selben Maßstab (`zoom --roh` oder `paar.png` aus `ansicht`); nie getrennt roh und nummeriert.
- **L12 Umgebung.** Python nur über den Interpreter aus dem Auftrag (nie bloßes `python`), nichts
  installieren, Skripte als Datei, keine Prozesse dauerhaft starten, keine Fenster öffnen. Für
  wiederkehrende Schritte zuerst die fertigen Befehle aus dem Auftrag (etwa `urteil bauen`, `zoom`,
  `einigung abgabe`); ein eigenes Skript nur, wenn kein Befehl den Fall deckt.
- **L13 Einigung im Verbund.** An den Übergängen der Teilkacheln (Nähte, Ecken, Viertelgrenzen)
  urteilst du mit Blick auf beide Seiten und die Urteile beider Teilkacheln: Zeigen zwei Segmente
  ohne Bildkante dieselbe Fläche, bekommen sie eine gemeinsame Klasse aus der Liste der Fassung (bei
  Fassung A die zusammengelegte `kategorien-a.json`), eine Kette über mehrere Teilkacheln eine Klasse
  für alle Glieder; eine echte Grenze bleibt mit Grund stehen; was sich nicht klären lässt, wird als
  unsicher mit Grund belegt, nie stillschweigend gelassen. Ein Urteil je Stelle für alle Beteiligten,
  nur Klassen von Segmenten im Kern, keine Grenzen und keine neuen Klassen.
- **L14 Garten.** Haus- und Hofgärten tragen die Unterklasse **3.6 Garten** im Dauergrünland (Abschnitt
  „Garten“ in `KATEGORIEN.md`). Garten ist jede krautige Grünfläche und jedes Beet in einem Haus- oder
  Hofgarten, auch Vor-, Obst- und Gemüsegarten am Haus, gepflegt oder verwildert, gemäht oder brach; Rasen
  ist kein Kennzeichen, die Lage am Wohnhaus oder Hof (eingefasst von Gebäude, Zaun oder Hecke) ist es.
  Kein Garten: Gartenbaum, Strauch und Hecke (Gehölz, G2), Gartenhaus (1.1.2), befestigter Weg oder
  Terrasse, Teich, Pool; Rasen in Park, Friedhof und Sportanlage (3.1); Wiese oder Acker am Ortsrand, die
  zu keinem Haus oder Hof gehört. Wiese/Weide oder Acker mit `im_siedlung: ja` ist nur ein Kandidat:
  entscheide am Bild. Gehört eine Grünfläche am Haus nicht sicher zum Garten, nimm „3 Dauergrünland“.
  In den freien Fassungen (A „Alles frei“, B „Kategorien frei“) gilt dasselbe für die eigenen Namen: Jede
  freie Liste führt die Klasse „Garten“ unter der Ebene-1-Klasse „Dauergrünland“ (genau diese Namen, ein
  Zusatz in Klammern ist erlaubt), auch wenn noch kein Segment sie trägt; wer Listen zusammenlegt, erhält
  sie dort und bildet jeden Gartennamen der Teil-Listen auf sie ab. `pruefen --frei` meldet sonst einen Fehler.
- **L15 Feinheit je Bildart.** L5 meint die Genauigkeit der Grenzen, nicht die Größe der Flächen. Wie klein
  Flächen werden dürfen, hängt an der Bildart (`einstellungen/bildarten.json`, aus dem Manifest; Aufruf
  `landseg bildart --manifest … --teilkachel …`). Farb-Orthofoto: so fein, wie sicher erkennbar, ohne Richtwert.
  Schwarz-Weiß-Scan (alt, niedrig aufgelöst, ein Kanal): Richtwert rund 600 Segmente je Ausschnitt von
  1000 × 1000 Bildpunkten (Teilkachel mit Kern 500 × 500: 150), Mindestfläche 100 m²; kleiner nur ein klar
  erkennbares Objekt (Haus, Einzelbaum, schmaler Weg, Garten am Haus), das du mit `sicher: ja` urteilst. Ein klar
  erkennbarer Garten am Haus bleibt eigene Fläche „Garten“ (L14), ein unklarer geht in die Nachbarfläche. Korn,
  Rauschen und Helligkeitsflecken sind keine Flächen: zusammenlegen (`eingriff verschmelzen`, Klasse der größeren
  Fläche), nachsegmentieren nur klar erkennbare Objekte. Die Zahlen setzt der Auftrag ein (`{{FEINHEIT}}`);
  `pruefen --manifest … --teilkachel …` meldet ein Überschreiten als Hinweis.

## Abgabe und Rückgabe

- Die Abgabe-Dateien (`urteil.json`, `abgabe.json`, `naht_abgabe.json`, `einigung_abgabe.json`) sind UTF-8-JSON genau nach
  dem Schema im Auftrag; Listen, die nichts enthalten, bleiben als `[]` stehen.
- `nicht_geprueft` nennt, was du nicht angesehen hast; `offen`, was du nicht entscheiden konntest.
- Die Rückgabe an die Hauptsession ist kurz: die Zahlen, die der Auftrag unter „Rückgabe“ nennt,
  die letzte Zeile von `pruefen` und was offen blieb.
