---
name: landseg-agent
description: Regeln für Agents, die in der Landschafts-Segmentierung (Repo landseg) Teilkacheln beurteilen, Label-Karten bearbeiten, Kommentare umsetzen oder Nähte klären. Lesen, bevor ein Auftrag aus vorlagen/ (urteil, umsetzen, korrektur, naht) bearbeitet wird.
---

# Agent-Regeln der Landschafts-Segmentierung

Diese Regeln gelten für jeden Agent-Auftrag aus `vorlagen/` (Urteil, Umsetzen, Korrektur, Naht).
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
  Stelle, die es zeigt?).
- **L12 Umgebung.** Python nur über den Interpreter aus dem Auftrag (nie bloßes `python`), nichts
  installieren, Skripte als Datei, keine Prozesse dauerhaft starten, keine Fenster öffnen.

## Abgabe und Rückgabe

- Die Abgabe-Dateien (`urteil.json`, `abgabe.json`, `naht_abgabe.json`) sind UTF-8-JSON genau nach
  dem Schema im Auftrag; Listen, die nichts enthalten, bleiben als `[]` stehen.
- `nicht_geprueft` nennt, was du nicht angesehen hast; `offen`, was du nicht entscheiden konntest.
- Die Rückgabe an die Hauptsession ist kurz: die Zahlen, die der Auftrag unter „Rückgabe“ nennt,
  die letzte Zeile von `pruefen` und was offen blieb.
