# Bericht landseg
Status: frage
Für den Nutzer: Die KI-Urteile von Fassung A sind je Teilkachel zu einer Liste zusammengeführt und geprüft (641 Flächen, jede genau einmal, keine fehlt). Für B und C gibt es jetzt je eine eigene Kategorienliste, und Fassung C ist zu einer Karte von ganz T0 ohne Lücke zusammengesetzt. Alles zusammen zeigt die neue Prüfseite `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/seite/T0-urteil.html` (Doppelklick, oben Umschalter A/B/C). Bei A und B sind die Grenzen noch die der Vorstufe, nur die Klassen kommen aus dem Urteil. Was die KI an Grenzen ändern würde (verschmelzen, teilen), steht beim angeklickten Segment unter „punkte“. Umgesetzt wird es erst in Teil 4. Jetzt sind Sie dran: Sehen Sie sich A an allen vier Teilkacheln an und sagen Sie je Klasse „passt“ oder „passt nicht“. Was falsch ist, kommentieren Sie am Segment und speichern es über „Export (JSON)“ als Datei. Die Tabelle je Klasse (`klassen-a.md`) hilft dabei. Bildschirmfotos habe ich nicht gemacht, weil die Browser-Erweiterung in dieser Sitzung fehlt.
Commit: keiner (Ergebnis: ohne Commit)
Nachweis: Urteile A und B mit `skripte/zusammenfuehren.py` zusammengeführt und geprüft, je Fassung vier `urteil/<teilkachel>/urteil.json` (A 641/641, B 641/641 Kernsegmente, 0 Fehler, Befund `pruefung-urteile.json`). `fassung-b/kategorien-b.json` (49 Klassen, 7/21/31) und `fassung-c/kategorien-c.json` (47 Klassen, 7/18/32) mit `skripte/listen.py` gebaut, beide bestehen das Prüfskript. C hat einen Stand mit vereinheitlichten Codes und eindeutigen IDs (`fassung-c/stand/<tk>/`) und ist zu `fassung-c/zusammen/` zusammengetragen (1000 × 1000, 0 Bildpunkte ohne Segment, 607 Segmente). Prüfseite `kern500/seite/T0-urteil.html` (8,1 MB) mit den Fassungen aus `kern500/seite/fassungen-urteil.json`. Alle Pfade liegen unter `C:/Users/Phil/Developement/Victor/daten/landseg/T0/`, Skripte und Belege unter `C:/Users/Phil/Developement/Victor/wuensche/2026-11-17-landseg-test-t0-3/`.
Abnahmekriterien:
AK2: erfüllt — `zusammenfuehren.py` → je Teilkachel Einträge = Kernsegmente (r0c0 141, r0c1 147, r1c0 52, r1c1 301), jedes Segment in genau einem Viertel, wie `gruppen.json` es zuordnet (0 Abweichungen). Kein Segment aus dem Kontextrand hat ein Urteil, jede Klasse steht in `kategorien.json`, jedes Viertel hat eine Übersicht unter `bilder_angesehen`, alle genannten Bilddateien gibt es (0 fehlend). `nicht_geprueft` und `offen` der Viertel sind übernommen. Ob ein Bild nur ein einzelnes Segment zeigt, habe ich nur am Dateinamen geprüft (kein Name mit Segment-ID), nicht am Bildinhalt.
AK3: nicht prüfbar — die Bestätigung durch den Nutzer steht aus (Halt Durchsicht). Die Seite ist fertig, die Tabelle je Klasse liegt in `klassen-a.md`.
AK6: teilweise erfüllt (Teil 3) — Urteil aus vier Viertel-Abgaben je Teilkachel mit Code aus `codes.json` und `klasse_frei` (641/641, 0 Fehler). `pruefe_kategorien.py fassung-b/kategorien-b.json` → „7/21/31 … ok“, Exit 0. `pruefen --kategorien kategorien-b.json` auf `fassung-b/urteil-stand/<tk>` → 4 × ok. Die Prüfseite lädt die Liste. Karte, Zusammentragen und Naht von B folgen in Teil 4.
AK7: erfüllt — vier freie Abgaben, Arbeitsweise unten. `pruefe_kategorien.py fassung-c/kategorien-c.json` → „7/18/32 … ok“, Exit 0. `pruefen --kategorien kategorien-c.json` je Teilkachel (`fassung-c/stand/<tk>`) → 4 × ok. Zusammengetragen: 1000 × 1000, ohne Segment 0. Befund daneben: siehe „Nicht geprüft“.
Prüfungen:
PY -I skripte/zusammenfuehren.py → A und B je 4 Teilkacheln, Fehler gesamt 0, Hinweise 0
PY -I skripte/listen.py → B 7/21/31, C 7/18/32; C r0c0 128, r0c1 272, r1c0 64, r1c1 417 Segmente
PY -I tools/pruefe_kategorien.py …/fassung-b/kategorien-b.json → ok (kleinster Farbabstand dE 11,9)
PY -I tools/pruefe_kategorien.py …/fassung-c/kategorien-c.json → ok (dE 15,0)
PY -m landseg pruefen … kern500/urteil-stand/<tk> → 4 × ok (206/234/86/408 Segmente)
PY -m landseg pruefen … fassung-b/urteil-stand/<tk> --kategorien kategorien-b.json → 4 × ok
PY -m landseg pruefen … fassung-c/stand/<tk> --kategorien kategorien-c.json → 4 × ok, je 0 Bildpunkte ohne Segment, 0 nicht zusammenhängend
PY -m landseg zusammentragen --datei fassung-c/zusammentragen.json --kategorien fassung-c/kategorien-c.json → „Zusammentragen FEHLER: 309 Nahtverstöße, 0 Mängel, pruefen FEHLER“ (Log `zusammentragen-c.log`), 1000 × 1000 ohne 0
PY -m landseg pruefen fassung-c/zusammen --form 1000x1000 → 607 Segmente, ohne Segment 0, 20 nicht zusammenhängend (`pruefen-c-zusammen.log`)
PY -m landseg naht fassung-c/zusammen → 309 Verstöße (`naht-c.log`)
PY -B -m landseg seite … --einstellungen kern500/seite/fassungen-urteil.json → A, B und C je 4 × pruefen ok, Nahtverstöße je 124, Seite 8105 KiB
Aufrufe: rund 40 von 50
Nicht geprüft:
- Die Seite habe ich nicht im Browser angesehen, weil die Browser-Erweiterung in dieser Sitzung fehlt. Es gibt kein Foto.
- C, zusammengesetzte Karte: 20 IDs zerfallen in zwei Teile. In ihrer eigenen Teilkachel hängen sie zusammen (`pruefen` je Teilkachel meldet 0), erst der Schnitt auf den Kern trennt sie. Dazu kommen 309 Nahtverstöße, weil die vier freien Abgaben an den Kerngrenzen nicht abgestimmt sind. AK7 verlangt nur lückenlos. Laut Mutterwunsch bleibt C in Teil 4 unverändert, ich habe es daher nicht korrigiert.
- Kontextrand-Segmente im Stand für die Seite: Sie haben kein eigenes Urteil. Ihre Klasse kommt aus dem Urteil der Nachbarkachel (Mehrheit der Bildpunkte). Liegen sie außerhalb von T0, gilt in A die Klasse der Vorstufe, in B „0 Nicht bestimmbar“. Sie stehen immer auf `sicher: nein` und `urteil: kontextrand`. Gezählt wird das unter `kontext_ohne_urteil_ausserhalb_t0` in `pruefung-urteile.json`.
- Ob die Klasse „Feld gemäht“ in B stimmt, bleibt offen (laut `vereinheitlichung.md` nicht am Bild nachgeprüft).
Einstieg: stimmte. Abweichung: `zusammentragen` braucht für eine freie Liste `--kategorien`. Ohne den Schalter meldet es jede Klasse von C als ungültig.
Technische Entscheidungen:
- Klasse A je Segment: `klasse_vorschlag`, sonst `klasse_heute`. Klasse B: Code aus `fassung-b/vereinheitlichung/codes.json`, die Benennung des Viertels bleibt als `klasse_frei` stehen.
- Stand für die Seite: eigene Ordner `kern500/urteil-stand/`, `fassung-b/urteil-stand/` und `fassung-c/stand/` (Karte der Vorstufe bzw. der Abgabe unverändert kopiert). Vorstufe und Abgaben selbst bleiben unberührt. Die Seite nimmt eigene Einstellungen (`kern500/seite/fassungen-urteil.json`), `T0.html` und `T0-probe.html` bleiben stehen.
- `kategorien-b.json`: der Entwurf der Vereinheitlichung, ergänzt um die Pflichtfelder des Formats, die das Prüfskript verlangt: `bw` = „eing.“ als Platzhalter, leere `mappings`, `counts`, `status` mit Hinweis „ungeprüft/nicht abgebildet“ und Regeln G1 (lückenlos, `bericht48` als Näherung: Rasen 2.2 und Gartenparzelle 3.3 → 4 Bebauung) und G2 (Herkunft).
- `kategorien-c.json`: Ich habe die vier eigenen Listen (33, 29, 21 und 36 Codes) nach Namen und Merkmalen zu 47 Klassen in sieben Gruppen 0–6 zusammengelegt (Schatten, Gebäude/Anlagen, Wege, Garten, krautige Vegetation, Feld/offener Boden, Gehölz). Die Abbildung je Teilkachel steht in der Liste unter `abbildung_teilkacheln`, der ursprüngliche Code je Segment unter `klasse_teil`. Gartenhecke und Gartengehölz aus r0c0 zählen zu Gehölz. Die Farben habe ich je Gruppe gierig nach dem größten CIELAB-Abstand gewählt.
- IDs von C: Die Abgaben r0c0, r0c1 und r1c0 beginnen alle bei 1. Im Stand bekommen sie deshalb einen Versatz von 100000, 200000 bzw. 300000, r1c1 (ab 400001) bleibt. Die alte ID steht unter `id_abgabe`.
Fassung C, Arbeitsweise der vier Agents (aus `fassung-c/abgabe/<tk>/arbeitsweise.md`):
- r0c0: Ausgang war die Vorstufe (206 Segmente), ausgewertet mit eigenen Skripten. Jedes Stück hat der Agent einer eigenen Gruppe zugeordnet und dabei Zusammengehöriges verschmolzen und 14 Kleinststücke an den Nachbarn gegeben. Große Mischflächen (Riesenwiese) hat er per Linienzug neu geteilt. Ergebnis: 128 Segmente, 85 davon im Kern.
- r0c1: Ausgang war ebenfalls die Vorstufe (234 Segmente). Er hat jedes Kernsegment einzeln eingeordnet, 27 Splitter verschmolzen und fünf gemischte Großsegmente mit SLIC zerlegt. Die Stücke bekamen ihre Klasse über eine Farb- und Texturregel. Ergebnis: 272 Segmente, 176 im Kern.
- r1c0: Eigener Weg ohne die Vorstufe. Ein Random Forest hat jeden Bildpunkt eingeordnet (Lab-Farbe, Grünindex, Textur, von Hand gesetzte Trainingsflächen). Danach kamen Modusfilter, Zonen und Pfade von Hand, Schattenzonen und Korrekturen nach Sichtprüfung. Ergebnis: 64 Segmente, 35 im Kern, die gröbste Abgabe.
- r1c1: Geometrie aus der Vorstufe, jedes Kernsegment einzeln neu eingeordnet (rund 300 Einträge). Gezielte Eingriffe: Rasenband an Engstellen geteilt, Becken und Schirme neu angelegt, Terrasse aus einem Dach getrennt. Ergebnis: 417 Segmente, 311 im Kern.
Zahlen für die Messung (Teil 5):
- A: nicht sauber 114/89/48/181 (zusammen 432 von 641), `sicher: nein` 94/109/33/245 (481, 75 %). Im Urteil kommen 27 Klassen vor. Die Punkte nach Art: Klasse 328, verschmelzen 156, trennen 36, Grenze 20, sonstiges 17, fehlt 14, fremdes 13, zu klein 4, „fremd“ 2 (diese Schreibweise steht nicht in der Vorlage).
- B: nicht sauber 96/88/45/176 (405), `sicher: nein` 112/89/28/168 (397, 62 %).
- Je Teilkachel und Viertel: `pruefung-urteile.json`. Je Klasse für A: `klassen-a.md`.
Nacharbeit im Hauptordner: Die Antwort des Nutzers zu A (Urteil je Klasse, wörtliche Korrekturen, Export `kommentare-*.json`) kommt nach `wuensche/2026-11-17-landseg-test-t0/abweichungen-a.md` (Eingabe von Teil 4) und in diesen Bericht unter AK3.
Abräumen: WEG (keine Arbeitskopie angelegt); keine repo-eigenen Reste
Lagebild: unberührt: Das Repo hat kein Lagebild, und der Lauf ändert keinen Code.
Erkenntnisse fürs Profil:
- `zusammentragen` prüft gegen die Liste des Repos. Für B und C braucht es `--kategorien <liste>`, sonst ist jede Klasse ungültig.
- `seite` und `naht` zählen auf derselben Karte verschieden viele Nahtverstöße (C: Seite 124, `naht` bzw. `zusammentragen` 309). Die beiden lesen das Bild des Ausschnitts mit verschiedenen Funktionen ein (`seite._lese_bild` gegen `naht.lese_bild`).
- Ein Hilfsskript mit `-I` übergeht `PYTHONPATH`. Ein Skript außerhalb des Repos findet `landseg` dann nur über `sys.path.insert(0, <repo>)` im Skript.
- `tools/pruefe_kategorien.py` verlangt von jeder Liste die Eigenheiten der festen Liste: Ebene-1-Codes genau 0–6, genau eine Regel mit `bericht48`, `bw` und `mappings` je Klasse, `counts`, `status`.
- Freie Abgaben (Fassung C) vergeben IDs je Teilkachel ab 1. Vor dem Zusammentragen müssen sie eindeutig gemacht werden.
Abweichungen vom Zielbild:
- `landseg/tools/pruefe_kategorien.py:89` — Das Prüfskript verlangt genau sieben Ebene-1-Codes 0–6 und, ab Zeile 136, eine Regel mit `bericht48`. Deshalb musste ich die freie Liste von C in sieben Gruppen pressen und B und C mit Platzhaltern versehen (`bw`, leere `mappings`, Näherungsregel `bericht48`). Nötig war das, weil der Arbeitsauftrag das Bestehen des Prüfskripts verlangt. Sauber wäre ein Prüfmodus für freie Listen, der nur das Format prüft (Codes, Namen, Eltern, Ebenen, Farben).
- `landseg/landseg/seite.py:60` — Die Seite liest das Bild mit einer eigenen Funktion statt mit `naht.lese_bild`. Dadurch zeigt der Nähte-Schalter auf derselben Karte 124 Verstöße, `naht` meldet 309. Ich habe es nur vorgefunden, nicht geändert. Sauber wäre ein gemeinsamer Leser.
Offene Frage: Passen die Klassen der KI in Fassung A (Prüfseite `T0-urteil.html`, Fassung A, alle vier Teilkacheln)?
- Empfohlen: Klasse für Klasse „passt“ oder „passt nicht“ sagen und falsche Segmente auf der Seite kommentieren und als JSON exportieren. Teil 4 setzt genau diese Kommentare um.
- Alles bestätigen, wie es ist: Teil 4 setzt nur die Vorschläge der KI um.
- Nur die Klassen nennen, die nicht passen, ohne Segment-Kommentare: Teil 4 ändert dann nichts an einzelnen Segmenten.
