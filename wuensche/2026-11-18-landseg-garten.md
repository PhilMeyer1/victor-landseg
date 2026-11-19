# Gärten überall als Dauergrünland mit Unterklasse „Garten“ führen: Kategorienliste, Regeln und Aufträge der Agents für alle Fassungen, vorhandene Ergebnisse T0 und H0 und Victors Projekt

Kurzname: landseg-garten | Datum: 2026-11-18 | Größe: gross | Bereich: victor | Repos: landseg | Status: eingereiht

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

„Es muss jetzt insgesamt sichergestellt werden, dass Gärten immer als Dauergrünland aber mit Unterkategorie Garten gelistet werden. Gärten spielen eine nennenswerte Rolle und müssen auch als solche gelabelt werden."

Präzisierung:
- Heute gilt in `landseg/KATEGORIEN.md` (G1, Zeilen um 109 und 128): keine Klasse „Siedlungsgrün“, Gartenrasen = 3.1 Wiese/Weide, Gartenbaum/Hecke = Gehölz, Gartenbeet = Acker. Das ersetzt der Nutzer für Gärten: unter „3 Dauergrünland“ eine eigene Unterklasse „Garten“ (Entscheidung 2026-11-18).
- „Insgesamt“: feste Kategorienliste (KATEGORIEN.md, kategorien.json, Farbe, SW-Spalte, Abbildung auf Bericht 48), Regeln und Aufträge der Agents (Skill landseg-agent, Vorlagen urteil/einigung, Auftragsbau), Pflicht für die freien Fassungen A und B (ihre eigenen Listen müssen Garten unter Dauergrünland führen bzw. so zusammengelegt werden), Prüfwerkzeug (pruefe_kategorien), und die vorhandenen Ergebnisse: T0 (Übergabe, A/B/C) und H0 (A/B/C), danach Seite und Gesamtprojekt victor-landseg neu.
- Zu klären mit dem Nutzer, wo es eine echte Wahl ist: was alles zur Fläche „Garten“ zählt (nur Rasen und krautiges Grün, oder auch Beete, Gartenbäume, Sträucher innerhalb eines Gartens), wie fein (eine Unterklasse oder gestuft), wie bestehende Ergebnisse umgestellt werden (nach Regel aus vorhandenen Klassen und Lage im Siedlungsgebiet, oder Agents sehen sich die Kandidaten am Bild an).
- Läuft neben den Effizienz-Wünschen effiz-* (gleiche Vorlagen und Aufträge); Reihenfolge klärt der Prüfer. Hochladen des Gesamtprojekts nur nach Ansage.

## Fragen

### F1: Was gehört alles zur Fläche „Garten“?
- Lage: Auf dem Luftbild sieht man in einem Hausgarten Rasen, Gemüse- und Blumenbeete, Obstbäume, Büsche und Hecken. Bisher zählt der Rasen als normale Wiese, Beete als Acker, Bäume und Sträucher als Gehölz. „Garten“ soll nun eine eigene Unterklasse im Dauergrünland sein, die auf der Seite und im Gesamtprojekt als eigene Farbe erscheint.
- Empfohlen: Rasen, krautiges Grün und Beete im Hausgarten (auch Gemüsegarten) — ein Garten ist so eine zusammenhängende Fläche; einzelne Bäume, Sträucher und Hecken bleiben Gehölz, weil man von oben die Baumkrone sieht (Grundsatz G2).
- Nur Rasen und krautiges Grün — Beete bleiben Acker; einfachste Abgrenzung, aber ein Gemüsegarten wäre dann kein Garten.
- Alles innerhalb der Gartengrenze samt Bäumen und Sträuchern — Garten ist die ganze Grundstücksfläche; Bäume wären dann nicht mehr als Gehölz auswertbar.

### F2: Zählen auch Parks, Friedhöfe und Sportrasen als „Garten“?
- Lage: Rasenflächen gibt es nicht nur bei Wohnhäusern, sondern auch in Parks, auf Friedhöfen und auf Sportplätzen. Ob ein Garten vorliegt, sieht man im Bild oft nur an der Lage am Haus.
- Empfohlen: Nein, nur Gärten bei Wohnhäusern und Höfen (auch Vorgärten, Obst- und Gemüsegärten am Haus) — Parks, Friedhöfe und Sportrasen bleiben Wiese/Weide; das hält die Klasse eindeutig.
- Ja, auch Parks und Friedhöfe — alles Gepflegte im Siedlungsgebiet ist Garten; einfacher zu sagen, aber ein Park ist kein Garten.

### F3: Wie werden die vorhandenen Ergebnisse (T0 und H0, alle Fassungen) umgestellt?
- Lage: Die Ergebnisse liegen fertig vor: das Orthofoto T0 und das historische Bild H0, je in drei Fassungen (feste Liste, Kategorien frei, alles frei). Die Segmente tragen heute Wiese, Acker oder Gehölz; ob ein Segment im Siedlungsgebiet liegt, steht schon als Merkmal dabei (am T0 noch nicht fein abgestimmt).
- Empfohlen: Erst nach Regel Kandidaten suchen (Rasen- und Beet-Segmente im Siedlungsgebiet), dann sehen Agents die Kandidaten je Viertel am Bild an und bestätigen oder lehnen ab — Rasen am Haus und Wiese am Ortsrand lassen sich nur am Bild sicher trennen; kostet einen kurzen Agent-Lauf je Viertel und Fassung.
- Nur nach Regel (Klasse plus Lage im Siedlungsgebiet), ohne Blick aufs Bild — kostet fast nichts, trifft aber Rasenflächen am Ortsrand und schmale Beete falsch.
- Alles neu urteilen lassen — am genauesten, aber so teuer wie der erste Lauf.

### F4: Wie fein soll „Garten“ gestuft sein?
- Lage: Die Liste hat unter Dauergrünland Wiese/Weide (mit Wiese und Weide), Magerrasen, Brache und weitere. „Garten“ kann ein einziger Eintrag sein oder weiter unterteilt werden (z. B. Rasen und Beet getrennt).
- Empfohlen: Eine einzige Unterklasse „Garten“ — mehr Stufen lassen sich vom Luftbild oft nicht sicher trennen und machen die Umstellung der Ergebnisse teurer.
- Zwei Stufen (Garten-Rasen, Garten-Beet) — genauer, aber bei jedem Gartensegment eine zusätzliche Entscheidung.

## Entscheidungen

- Gärten als Dauergrünland mit Unterklasse Garten: Unter „3 Dauergrünland“ gibt es eine eigene Unterklasse „Garten“; Gartenflächen tragen sie in jeder Fassung (A, B, C) und in jedem Lauf, auch in den vorhandenen Ergebnissen. Ersetzt für Gärten die Regel G1/„keine Klasse Siedlungsgrün, Gartenrasen = 3.1 Wiese/Weide“ in KATEGORIEN.md. Was genau zur Fläche „Garten“ gehört, klärt dieser Wunsch. (aus entscheidungen.md, 2026-11-18)
- Bedeckung statt Nutzung: Rasen und Hausgärten kommen zu Grünland bzw. Gehölz, „im Siedlungsgebiet“ ist ein Merkmal je Segment statt einer Klasse; für Gärten jetzt durch die Unterklasse ersetzt (aus entscheidungen.md, 2026-11-17).
- Bericht 48 nicht bindend: Abbildung erwünscht, wo sie ohne Verbiegen der Liste geht, kein Abnahmekriterium (aus entscheidungen.md, 2026-11-17).
- Drei Fassungen A, B, C als Übersicht für Victor; Urteil im Verbund je Viertel, nie Einzelbilder je Segment (aus entscheidungen.md, 2026-11-17).
- Push zu GitHub nur auf ausdrückliche Ansage (aus entscheidungen.md, 2026-11-17).

- F1 (Nutzer 2026-11-18, Freitext): „Grünfläche und Beete nicht Rasen. Nicht überall ist ein Rasen vorhanden“ — Garten = jede krautige Grünfläche und jedes Beet im Haus- oder Hofgarten, ob gepflegter Rasen oder nicht (auch verwilderte, gemähte oder brache Gartenfläche); Rasen ist kein Kennzeichen. Bäume, Sträucher und Hecken nicht genannt: bleiben Gehölz (Empfehlung, Grundsatz G2), Hinweis an den Nutzer.
- F2 (Nutzer): „Nur Haus- und Hofgärten“ — samt Vor-, Obst- und Gemüsegärten; Parks, Friedhöfe und Sportrasen bleiben Wiese/Weide.
- F3 (Nutzer): „Regel, dann Agents am Bild“ — Kandidaten per Regel (Grün und Beete im Siedlungsgebiet), Agents bestätigen je Viertel am Bild.
- F4 (Nutzer): „Eine Unterklasse“ — „Garten“ ohne weitere Stufung.

## Arbeitsauftrag

Die Kriterien folgen den Empfehlungen zu F1 bis F4; Antworten, die davon abweichen, ändern AK1, AK2 und AK6.

### Abnahmekriterien

AK1: In der Kategorienliste steht unter „3 Dauergrünland“ eine neue Unterklasse „Garten“ (Code 3.6, eigene, von allen anderen deutlich verschiedene Farbe, SW-Spalte, Bildmerkmal, Zuordnung zu Bericht 48), und das Prüfskript meldet die neuen Zahlen mit „ok“ — prüfbar: `"$PY" -I tools/pruefe_kategorien.py kategorien.json` (nach F1, F2, F4)
AK2: `KATEGORIEN.md` nennt Garten als Klasse und sagt, was dazugehört und was nicht; der Absatz „keine Klasse Siedlungsgrün“ und Grundsatz G1 sind angepasst, Gesamtzahl und Zählung stimmen in `KATEGORIEN.md`, `README.md`, `gesamt/ANLEITUNG.md`, `gesamt/CLAUDE.md` und im Test `tests/test_kategorien.py` — prüfbar: Lesen `KATEGORIEN.md`; `"$PY" -B -m unittest tests.test_kategorien`
AK3: Die Bericht-48-Abbildung zählt „Garten“ im Siedlungsgebiet weiter als „1 Versiegelt / bebaut“, außerhalb als Dauergrünland — prüfbar: `"$PY" -B -m unittest tests.test_kategorien` (neuer Fall)
AK4: Die Regeln für Agents (Skill `landseg-agent`, Vorlagen `urteil`, `einigung`, `naht`, `korrektur`, `umsetzen`) sagen, wann „Garten“ zu wählen ist; die freien Fassungen A und B führen Garten unter Dauergrünland in ihrer Liste bzw. erhalten es beim Zusammenlegen (`kategorien-a.json`, `kategorien-b.json`) — prüfbar: `"$PY" -B -m unittest tests.test_vorlagen tests.test_einigung`
AK5: `pruefen` meldet einen Fehler, wenn in einer freien Fassung die Klasse „Garten“ fehlt oder nicht unter Dauergrünland steht — prüfbar: `"$PY" -B -m unittest tests.test_pruefen`
AK6: In den Ergebnissen T0 und H0 aller drei Fassungen tragen die als Garten bestätigten Segmente die Klasse „Garten“; `pruefen` meldet für jede der sechs Karten keinen Fehler, die Zahl der Garten-Segmente je Fassung steht im Bericht — prüfbar: `pruefen` je Fassung für T0 und H0 (Datenlauf unter `BASIS/daten/landseg/`, ohne Commit)
AK7: Die Seite `T0-H0.html` zeigt „Garten“ in Legende, Ebenenauswahl und bei den Segmenten mit eigener Farbe, in allen Fassungen und beiden Bildern; das Gesamtprojekt victor-landseg ist neu gebaut, nicht hochgeladen — prüfbar: Ansicht Seite T0-H0, Segmentliste mit Garten, Desktop; `tests/test_seite.py`, `tests/test_gesamt_projekt.py`
AK8: Weg des Nutzers: Auf der Seite in T0 ein Haus mit Garten wählen und sehen, dass der Hausgarten als „Garten“ (Dauergrünland) gelistet ist, in jeder Fassung — prüfbar: Ansicht Seite am laufenden Stand, Desktop

Nacharbeit: `BASIS/.claude/repos/landseg.md` (Zeile „7/25/43 Klassen, insgesamt 58“, Regel G1) nach dem Bau aktualisieren; Lagebild nachziehen.

### Einstieg

- landseg: `kategorien.json:693` — Dauergrünland „3“ mit 3.1 bis 3.5; hier kommt 3.6 „Garten“ dazu; `counts` (Zeile 10) und Regel G1 (Zeile 1529, Feld `bericht48`) anpassen.
- landseg: `KATEGORIEN.md:109` — Absatz „keine Klasse Siedlungsgrün“, G1 (Z. 118), Siedlungsabsatz (Z. 126–140), Zählung (Z. 26, 44, 179): auf die neue Regel umschreiben.
- landseg: `tools/pruefe_kategorien.py:128` — Zählprüfung und Bericht-48-Regel; die neue Farbe muss den Farbabstand halten (10 CIELAB).
- landseg: `landseg/kategorien.py:63` — `bericht48_klasse` und `siedlung_klassen`: Garten im Siedlungsgebiet unter Siedlung, sonst Dauergrünland.
- landseg: `landseg/pruefen.py:155` — Garten-Prüfung für die freien Fassungen ergänzen.
- landseg: `.claude/skills/landseg-agent/SKILL.md:30` (L3), `vorlagen/urteil.md:17`, `vorlagen/einigung.md:41` — Klassenwahl und freie Listen.
- landseg: `landseg/vorstufe.py:231` — Merkmal `im_siedlung`, Grundlage der Garten-Kandidaten.
- landseg: `gesamt/ANLEITUNG.md:255` — Zahlentabelle je Fassung (C hat 58 Klassen).

### Bausteine und Fallen

- Vorhandene Werkzeuge nutzen: `eingriff` (Klasse eines Segments ändern), `pruefen`, `zusammentragen`, `seite`, `tools/gesamt_projekt.py`; keine eigene Neuberechnung der Karten.
- Die Ergebnisse liegen unter `BASIS/daten/landseg/{T0,H0,seiten,uebergabe}` (nie im Repo), je Fassung mit eigener Liste (`kategorien-a.json`, `-b`, `-c`); Fassung C (feste Liste) bekommt die neue Klasse aus `kategorien.json`. Vor dem Datenlauf die Ergebnisse sichern.
- Falle: Die Farbe von 3.6 muss sich von den vielen Grüntönen in Klasse 3 deutlich unterscheiden; Falle: Test auf 58 Klassen in `tests/test_kategorien.py:34` und die Zahlen in `gesamt/ANLEITUNG.md`.
- Falle: Garten-Kandidaten (Gartenrasen als 3.1, Beete als Acker, `im_siedlung: ja`) sind nur Kandidaten; Rasen am Ortsrand ist kein Garten. Je Viertel und Fassung ein Agent bestätigt am Bild (Entscheidung „Urteil im Verbund je Viertel“), keine Einzelbilder je Segment; die Umstellung ist ein Datenlauf (ohne Commit), die Einheiten (Viertel × Fassung × Bild) laufen parallel.
- Reihenfolge zu `effiz-*` (gleiche Vorlagen): Teil 1 (Liste, Prüfskript) kann sofort laufen; Teil 2 (Vorlagen und Skill) wird erst nach den eingereihten `effiz-befehle`, `effiz-bilder`, `effiz-viertel` begonnen, sonst Konflikt in `vorlagen/`.
- Hochladen nur nach Ansage; Teil 4 baut nur.

### Bauweise

Richtung: ohne Zielbild
Berührt: keine — kein Register-Eintrag trifft Kategorienliste oder Vorlagen; A3 und A4 liegen an `gesamt/` und werden durch Teil 4 nicht verändert.
Tilgt: keine
Flick-Signale: keine — kein Vorgänger (ohne `Herkunft:`; die Entscheidung vom 17.11. „Bedeckung statt Nutzung“ änderte dieselbe Regel G1, war aber kein Wunsch dieser Kette)
Anbau: Garten als weitere Klasse 3.6 mit Prüfregel und Hinweisen in den Aufträgen — Dauer mittel — Risiko mittel (Zahlen und Texte an mehreren Stellen, Datenlauf auf sechs Karten) — danach bleibt die Garten-Kandidatensuche als Muster für spätere Klassenwechsel
Umbau: nicht nötig — Dauer kurz — Risiko – — Netz vorhanden — danach entfällt nichts
Belege: –
Empfehlung: Anbau — kein Beleg für einen Umbau, ein Klassenwechsel ist Listen- und Datenpflege.

Reihenfolge der Repos: landseg · Risiken: Datenlauf verändert vorhandene Ergebnisse, falsche Garten-Kandidaten am Ortsrand, Zahlen (58 Klassen) in mehreren Dateien · Vorbedingungen: keine

## Teile

1. Kategorienliste, Prüfskript und Bericht-48-Abbildung — Umsetzer — Repo: landseg — Vorbedingungen: keine — nach: – — AK 1, 2, 3 — Garten steht als Klasse 3.6 in `kategorien.json` und `KATEGORIEN.md`, Prüfskript und Zähltests grün
2. Regeln und Aufträge der Agents, Prüfung der freien Fassungen — Umsetzer — Repo: landseg — Vorbedingungen: keine — nach: 1 — AK 4, 5 — Skill, Vorlagen und `pruefen` kennen Garten (erst nach den effiz-Wünschen einreihen)
3. Umstellen der Ergebnisse T0 und H0 in allen drei Fassungen (ohne Commit) — Workflow — Repo: landseg — Vorbedingungen: keine — Aufruf-Budget: 120 — nach: 1, 2 — AK 6 — je Viertel und Fassung ein Agent bestätigt die Garten-Kandidaten, Karten geprüft, Zahl je Fassung im Bericht
4. Seite und Gesamtprojekt neu bauen — Umsetzer — Repo: landseg — Vorbedingungen: keine — nach: 3 — AK 7, 8 — Seite und Gesamtprojekt zeigen Garten (ohne Hochladen)

## Varianten

<entfällt>

## Entwurf

Stufe: nein — keine neue Oberfläche: nur eine Klasse mit eigener Farbe in der bestehenden Legende der Seite.
