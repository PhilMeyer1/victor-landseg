# UI-Test Prüfseite Landschafts-Segmente (T0, kern500)

Getestet am 2026-11-17 in Chrome (Erweiterung Claude in Chrome) über einen lokalen Webserver
(`http://127.0.0.1:8765/T0.html` und `T0-probe.html`). Fenster maximiert: 1707×932 CSS-Pixel bei
Bildschirmskalierung 1,5 (entspricht etwa 2560×1400 Bildpunkten). Die schmale Ansicht 1280×800 ist
nachgestellt, weil sich das maximierte Fenster nicht verkleinern ließ (Seite per Stil auf
1280×800 CSS-Pixel begrenzt). An der Seite und im Repo wurde nichts geändert; mein Probekommentar
wurde danach wieder aus dem Browser-Speicher entfernt.

## Zusammenfassung

Die Seite lädt schnell (lokal 0,3 bis 1,0 s bis zum fertigen Bild), reagiert flott (Wechsel der
Fassung unter 25 ms, keine Rechenpausen über 50 ms beim Überfahren und Klicken) und zeigt keine
Konsolenfehler. Zwei Fehler machen sie aber im Alltag mühsam:

1. **Das Bild springt.** Sobald die Maus ein Segment berührt, wächst die untere Leiste von 144 auf
   330 Pixel, das Bild schrumpft um 27 % und rutscht 93 Pixel zur Seite und nach oben. Am Bildrand
   schaltet es bei jeder kleinen Mausbewegung hin und her.
2. **Das Luftbild ist unter den Flächen nicht zu sehen.** Der Regler „Deckkraft“ macht die Farben
   nur dunkler oder heller, nie durchsichtig; bei 10 % ist das Bild fast schwarz.

Dazu kommen viele Fachwörter und Rohdaten in der Anzeige, kaum sichtbare Schalterzustände und ein
Kommentarablauf ohne Rückmeldung. Insgesamt 15 Befunde: 3 störend, 6 lästig, 6 Kleinigkeiten.

## Befunde

### 1. Bild springt beim Überfahren, Anklicken und Abwählen — störend

**Was passiert:** Die untere Leiste (`section.c-leiste`) hat keine feste Höhe (Rasterzeile `auto`).
Beim Überfahren füllt die Seite darin `div.c-detail` mit der Karte „Unter der Maus“ und der Tabelle
„Alle Felder“ (`.c-felder`, bis 30 % der Fensterhöhe). Die Leiste wächst, der Bildbereich darüber
(`canvas.c-bild`, Zeile `minmax(0,1fr)`) wird kleiner, und das Bild wird neu eingepasst (größter
Maßstab, der in die Fläche passt, mittig).

Messwerte (ResizeObserver und PerformanceObserver „layout-shift“, je Wechsel Verschiebungswert 0,0385):

| Fenster | Leiste ohne Maus | Leiste mit Maus | Bildhöhe ohne → mit | Verkleinerung |
|---|---|---|---|---|
| 1707×932 | 144 px | 330 px (311 px bei Segmenten mit weniger Feldern) | 688 → 502 px | −27 % |
| 1280×800 (nachgestellt) | 144 px | 347 px | 556 → 353 px | −37 % |

- Linke Bildkante wandert um 93 px nach rechts, die Bildmitte um 93 px nach oben, die Unterkante um
  186 px. Unter dem stillstehenden Mauszeiger liegt danach eine andere Stelle: Eine Bewegung um
  10 px änderte die Bildstelle von (x 299, y 222) auf (x 309, y 313).
- **Pendeln am Rand:** Ein Punkt, der im großen Bild liegt, im kleinen aber nicht, schaltet bei jeder
  Mausbewegung um: Maus drauf → Leiste wächst → Bild schrumpft → Maus liegt außerhalb → Leiste
  schrumpft → Bild wächst → Maus liegt wieder drauf. Nachgestellt bei x 850 / x 855 (Bildschirmfoto-
  Koordinaten): 144 → 330 → 144 → 311 px in zwei Mausbewegungen.
- **Sprünge zwischen Segmenten:** Je nach Zahl der Felder ist die Leiste 311 oder 330 px hoch; von
  einem Segment zum nächsten springt das Bild also nochmals um 19 px.
- **Anklicken / Abwählen:** Klick wählt, Leiste bleibt groß (gut: solange gewählt, springt es beim
  Überfahren nicht mehr). Beim Abwählen schrumpft die Leiste, das Bild wächst wieder.
- **Verschieben (Ziehen):** Nach dem Loslassen erscheint die Karte zum Segment unter der Maus, das
  eben verschobene Bild schrumpft sofort.
- Bei 1280×800 ist die Leiste mit 347 px fast so hoch wie das Bild (353 px); rechts und links vom Bild
  bleiben je über 300 px leer.

**Nachstellen:** T0.html öffnen, Maus aus dem Bild in ein Segment bewegen; oder langsam über den
rechten Bildrand fahren.

**Vorschlag:** Wie gewünscht eine feste Leiste links (etwa 320 px breit, volle Höhe) für Mauszeile,
Karte, „Alle Felder“ und Kommentar; die untere Leiste behält nur die Schalter und hat eine feste
Höhe. Der Bildbereich ändert dann nie seine Größe. Platz ist da: Das quadratische Bild nutzt die
Breite ohnehin nicht. Innerhalb der linken Leiste Bereiche mit fester Höhe und eigenem Rollbalken,
damit auch dort nichts hüpft.

Bilder: `ui-test-bilder/01-ruhe-ohne-maus.jpg`, `ui-test-bilder/02-maus-ueber-segment-bild-geschrumpft.jpg`,
`ui-test-bilder/09-schmal-1280x800-maus-ueber-segment.jpg`.

### 2. Luftbild unter den Flächen unsichtbar, Deckkraft wirkt falsch — störend

**Was passiert:** Mit „Flächen“ an (Grundeinstellung, Deckkraft 30 %) sieht man vom Luftbild nichts,
nur dunkle Farbflächen. Bei 10 % ist das Bild fast schwarz, bei 60 % kräftig farbig, nie
durchscheinend. Nur „Flächen“ aus zeigt das Foto. Ursache im Zeichnen der Überlagerung: Die Farbe
wird mit einem leeren (schwarzen) Bildpuffer statt mit dem Foto gemischt, danach wird jeder Punkt
voll deckend gesetzt (`setze()` schreibt Alpha 255). Damit fehlt der Hauptzweck: prüfen, ob die
Kategorie zum Foto passt.

**Nachstellen:** T0.html, Regler „Deckkraft“ auf 10 % ziehen.

**Vorschlag:** In der Überlagerung die reine Farbe mit Alpha = Deckkraft schreiben (statt mit Schwarz
zu mischen) und das Foto darunter durchscheinen lassen. Regler mit Beschriftung und Prozentwert
versehen.

Bilder: `ui-test-bilder/01-ruhe-ohne-maus.jpg` (Flächen an), `ui-test-bilder/04-flaechen-aus-luftbild-sichtbar.jpg`.

### 3. „Kategorie hervorheben“ und „Nur unsicher“ schwärzen alles andere — störend

**Was passiert:** Ein Klick auf eine Kategorie in der rechten Liste oder „Nur unsicher“ färbt alle
übrigen Segmente deckend schwarz (gleicher Fehler wie Befund 2). Ohne Foto und Nachbarn fehlt jeder
Zusammenhang; die schwarzen Flächen sehen aus wie Löcher (Verwechslung mit „Lücken“). Bei „Nur
unsicher“ betrifft es zwei Drittel der Segmente (136 von 206 sind „unsicher“).

**Nachstellen:** Rechts „1.1 Gebäude“ (Ebene mittel) anklicken; oder „Nur unsicher“.

**Vorschlag:** Übrige Segmente nur abblenden (Foto halbdunkel sichtbar, Umriss bleibt), nicht
schwarz füllen. Hervorgehobene Kategorie in der Liste deutlicher markieren und einen Hinweis
„Hervorhebung aufheben“ zeigen.

Bild: `ui-test-bilder/05-nur-unsicher-gitter-luecken.jpg`.

### 4. Abwählen nur durch nochmaliges Klicken auf dasselbe Segment — lästig

**Was passiert:** Escape, Klick neben das Bild und Klick ins Leere heben die Wahl nicht auf. Nur ein
zweiter Klick genau auf dasselbe Segment tut es; der Hinweis dazu steht erst nach der Wahl klein in
der Mauszeile. Klickt man aus Versehen ein Nachbarsegment, wählt man dieses statt abzuwählen.

**Nachstellen:** Segment anklicken, Escape drücken: Adresse behält `/segment/…`, Leiste bleibt groß.

**Vorschlag:** Escape und Klick außerhalb des Bildes heben die Wahl auf; dazu ein sichtbarer Knopf
„Auswahl aufheben“ in der Segmentleiste.

### 5. Beim Wechsel der Fassung geht die Auswahl verloren — lästig

**Was passiert:** Ausschnitt und Zoom bleiben beim Wechsel A ↔ P erhalten (gut), aber das gewählte
Segment und die Karte verschwinden; die Adresse springt auf `#/P/kachel/r0c0` ohne Segment. Zum
Vergleichen derselben Stelle in zwei Fassungen muss man jedes Mal neu klicken. Die Segment-Nummern
sind je Fassung verschieden, die Stelle im Bild aber gleich.

**Nachstellen:** T0-probe.html, Segment wählen, auf „P · PROBE“ klicken.

**Vorschlag:** Den zuletzt geklickten Bildpunkt merken und nach dem Wechsel das Segment an diesem
Punkt in der neuen Fassung wählen. Optional Tastenkürzel 1/2/3 (oder A/B/C) für schnelles Umschalten.

### 6. Fachwörter und Rohdaten ohne Erklärung — lästig

**Was passiert:** Für Victor (und auch sonst) unverständlich bzw. ohne Erklärung:
- Tabelle „Alle Felder“ zeigt Rohdaten: `sicherheit {"wert":0.701}`, `instanz {"text":"meadow","eingerastet":true}`,
  `herkunft sam3-instanz`, `im_kern true`, `im_siedlung nein`, `klasse 3.1`, `grob 3`.
- Kopfzeile: „Nähte: 62 Verstöße“, „lückenlos“, „136 unsicher“; Übersicht: „124 Nahtverstöße · 4 Kerngrenzen“.
- Der weiße Rahmen im Bild (Kern) und der abgedunkelte Rand sind nirgends erklärt.
- „(feiner nicht bestimmt)“, „Teilkachel r0c0“, „Fassung“.
- Unter der Kategorienliste stehen Windows-Pfade (`C:/Users/Phil/…/kategorien.json`, `…/vorstufe/r0c0`).

**Vorschlag:** „Alle Felder“ einklappbar und standardmäßig zu; die wichtigen Werte in Alltagssprache
(„Sicherheit 70 %“, „liegt im Kern: ja“). Eine kleine Legende oder ein „?“-Feld: Kern = der Teil, der
zählt; Rand = Überlappung zum Nachbarn; Naht = Grenze zwischen zwei Teilkacheln; Verstoß = dort
passen die Segmente nicht zusammen. Pfade nur in einem Bereich „Technik“.

### 7. Zahlen auf den Ebenen-Knöpfen passen nicht zur Liste — lästig

**Was passiert:** „grob · 7“, „mittel · 25“, „fein · 43“ — die Liste rechts zeigt aber 6, 11 bzw. etwa
15 Kategorien. Gemeint ist offenbar die Zahl der Kategorien in der Kategorienliste, nicht die im Bild
vorkommenden. Das ist nicht erkennbar.

**Vorschlag:** Zahl weglassen oder „11 von 25“ schreiben, mit Kurzhinweis per Tooltip.

### 8. Schalterzustände kaum erkennbar, Regler ohne Beschriftung — lästig

**Was passiert:** Ein- und ausgeschaltete Knöpfe (Flächen, Umriss, Lücken, Nähte, Nur unsicher,
Gitter, Kategorien) unterscheiden sich nur durch einen etwas helleren Grauton. Man sieht nicht auf
einen Blick, was an ist. Der Deckkraft-Regler hat weder Beschriftung noch Wert. „Kategorien“ blendet
die rechte Liste aus, was man am Wort nicht erkennt.

**Vorschlag:** Eingeschaltet deutlich markieren (Akzentfarbe wie bei der aktiven Fassung, Häkchen
oder Kontrollkästchen-Stil). Regler mit „Deckkraft 30 %“. „Kategorien“ in „Liste rechts“ umbenennen
oder als Pfeil am Listenrand.

### 9. Kommentieren ohne Rückmeldung, nur im Browser gespeichert — lästig

**Was passiert:**
- Nach „Vormerken“ leert sich das Feld, sonst ändert sich nur die kleine Zahl oben rechts
  („Kommentare (1)“). Kein Hinweis „gespeichert“, keine Markierung am Segment.
- „Vormerken“ ist auch ohne gewähltes Segment oder ohne Text klickbar und tut dann still nichts.
- Kommentare liegen nur im Speicher dieses Browsers (Schlüssel mit dem vollen Windows-Pfad zum
  Manifest). Auf Victors Rechner, in einem anderen Browser oder nach dem Löschen der Browserdaten sind
  sie weg; T0.html und T0-probe.html teilen sich denselben Speicher. Die Seite sagt nicht, dass man
  exportieren muss.
- In der Kommentarliste kann man nichts ändern oder löschen; die Zeit steht als
  `2026-11-17T17:49:03.950Z` (Weltzeit statt Ortszeit).
- Export funktioniert: Datei `kommentare-T0.json` (937 Byte, Schema `landseg-kommentare/1`, mit
  Fassung, Teilkachel, Segment, Klasse, Text). Der Download startet ohne Rückfrage (im Test
  abgefangen, keine Datei geschrieben). Der Link „Segment 100136“ in der Liste führt richtig zurück.

**Vorschlag:** Kurze Bestätigung („Kommentar 1 vorgemerkt – noch nicht exportiert“), Segmente mit
Kommentar im Bild markieren, „Vormerken“ ausgrauen, solange nichts gewählt oder leer ist, Hinweis
„nur in diesem Browser gespeichert – bitte exportieren“, Bearbeiten/Löschen in der Liste, Ortszeit.

### 10. Übersicht „Ganzer Ausschnitt“: keine Mausinfo, Klick ins Bild tut nichts — Kleinigkeit

**Was passiert:** In der Übersicht gibt es keine Anzeige beim Überfahren, keinen Ebenen-Umschalter,
keine Legende, und ein Klick ins Bild öffnet nicht die Teilkachel (nur die vier Karten unten und die
Kopfzeile tun das). Die Zeile „Nahtverstöße: r0c0|r0c1 · 100040|200043 · 1 px; …“ ist eine abgeschnittene
Rohliste.

**Vorschlag:** Klick ins Bild öffnet die Teilkachel an dieser Stelle; Nahtverstöße als kurze Zahl je
Naht, Details aufklappbar.

Bild: `ui-test-bilder/06-ganzer-ausschnitt.jpg`.

### 11. Ähnliche Farben auf Ebene fein, Auswahl schwach markiert — Kleinigkeit

**Was passiert:** 3.1 Wiese, 3.4 Krautsaum, 4.1 Wald und 4.2.1 Einzelbaum sind alle Grüntöne, 1.2.1
Straße und 1.2.4 Platz zwei ähnliche Rosatöne; auf dem dunklen Bild kaum zu trennen. Das gewählte
Segment wird nur 18 % aufgehellt mit dünnem Rand, das überfahrene nur mit dünnem weißem Rand.

**Vorschlag:** Auswahl mit kräftigem, breiterem Rand (z. B. 2–3 px gelb) markieren; Farben innerhalb
einer groben Gruppe stärker in der Helligkeit staffeln.

### 12. Zoom ohne Anzeige, „+“ springt stark — Kleinigkeit

**Was passiert:** Mausrad und „+“/„−“/„Ganz“ funktionieren, Verschieben per Ziehen auch. Es gibt aber
keine Zoomstufe als Zahl, und zwei Klicks auf „+“ vergrößern schon so weit, dass nur noch einzelne
Umrisse zu sehen sind. Der Ausschnitt bleibt je Teilkachel gemerkt (auch nach Wechsel der Kachel),
ohne Hinweis darauf.

**Vorschlag:** Zoomstufe anzeigen (z. B. „200 %“), Doppelklick zum Vergrößern, kleinere Schritte.

### 13. Ausgegraute Fassungen nur per Tooltip erklärt — Kleinigkeit

**Was passiert:** In T0.html sind „B · Kategorien frei“ und „C · Alles frei“ ausgegraut; warum, steht
nur im Tooltip („Für diese Fassung gibt es noch keine Ergebnisse“). Ausgegraut und „nicht gewählt“
sehen fast gleich aus. In T0-probe.html ist P nach dem Wechsel gut als aktiv erkennbar, und die
Beschreibung sagt „Fassung B fehlt noch“ – in T0.html fehlt ein solcher Satz.

**Vorschlag:** Hinter ausgegrauten Fassungen „(noch leer)“ schreiben.

Bild: `ui-test-bilder/08-probe-fassung-p.jpg`.

### 14. Segmentinfo doppelt — Kleinigkeit

**Was passiert:** Die Mauszeile („Unter der Maus (x 278, y 348): Segment 100145 · …“) und die Karte
darunter zeigen dasselbe noch einmal.

**Vorschlag:** In der neuen linken Leiste nur eine Darstellung: oben „Unter der Maus“ (eine Zeile,
feste Höhe), darunter „Gewählt“ mit Details.

### 15. Einmal blieb die Seite nach dem ersten Klick 30 s ohne Bildschirmfoto — Kleinigkeit (unsicher)

**Was passiert:** Direkt nach dem ersten Klick auf ein Segment kam das Bildschirmfoto über die
Erweiterung nicht innerhalb von 30 s zurück („Renderer unresponsive“); die Seite selbst hatte den
Klick verarbeitet. Beim zweiten Durchgang nicht wieder aufgetreten, keine Rechenpausen über 50 ms
gemessen. Vermutlich ein Problem der Erweiterung, nicht der Seite; nur zur Kenntnis.

## Was gut lief

- Ladezeit lokal 0,3–1,0 s bis zum fertigen Bild (Ladeende 322–987 ms, erstes Bild 844 ms beim
  Neuladen), Probe-Datei 0,7 s.
- Fassungswechsel unter 25 ms, Zoom/Position bleiben dabei erhalten.
- Keine Konsolenfehler, keine Rechenpausen über 50 ms beim Überfahren und Klicken.
- Adresse spiegelt Fassung, Teilkachel und Segment (Links aus der Kommentarliste funktionieren).
- Ebenen-Umschalter, Lücken, Nähte, Gitter mit Beschriftung der Bildpunkte funktionieren.

## Nicht getestet

- Echtes Fenster 1280×800 (Fenster maximiert, Größenänderung wirkte nicht; nachgestellt über die
  Seitengröße).
- Echter Download der Exportdatei (abgefangen, Inhalt geprüft).
- Öffnen als Datei (`file://`) und auf Victors Rechner, damit auch das Verhalten des Kommentarspeichers dort.
- Fassungen B und C (noch keine Ergebnisse), Touch-Bedienung, Tastaturbedienung mit Tab-Taste im Detail.

## Bildschirmfotos

Ordner `C:/Users/Phil/Developement/Victor/wuensche/2026-11-17-landseg-werkzeuge-5/ui-test-bilder/`:
`01-ruhe-ohne-maus.jpg`, `02-maus-ueber-segment-bild-geschrumpft.jpg`, `03-segment-gewaehlt.jpg`,
`04-flaechen-aus-luftbild-sichtbar.jpg`, `05-nur-unsicher-gitter-luecken.jpg`, `06-ganzer-ausschnitt.jpg`,
`07-kommentare.jpg`, `08-probe-fassung-p.jpg`, `09-schmal-1280x800-maus-ueber-segment.jpg`.

## Nachtest

Am 2026-11-17 nach der Nachbesserung (Dateistand 18:58), gleicher Aufbau: Chrome über die Erweiterung,
lokaler Webserver auf Port 8765, `T0.html` und `T0-probe.html`. Fenster maximiert (1707×932, später
1707×876 CSS-Pixel); 1280×800 wieder über die Seitengröße nachgestellt. Probekommentar danach
gelöscht, Browser-Speicher wie vorher.

### Springen: gemessen, behoben

Bildfläche (`canvas.c-bild`, x, y, Breite × Höhe) mit ResizeObserver und Layout-Shift-Messung:

| Ablauf | 1707 px breit | 1280×800 (nachgestellt) |
|---|---|---|
| Ruhe | 320, 102, 1097 × 778 | 320, 102, 670 × 646 |
| Überfahren (40 zufällige Stellen, Segmentwechsel) | unverändert | unverändert |
| Anklicken / Esc / Klick neben das Bild / „Auswahl aufheben“ | unverändert | unverändert |
| Ziehen (Verschieben), Mausrad | unverändert | – |
| Pendeln am Bildrand (x 1094 / 1099 / 1094) | unverändert | – |
| „Technische Angaben“ aufgeklappt | unverändert | unverändert |

Keine einzige Layout-Verschiebung gemessen. Die linke Leiste hat feste Bereiche: „Unter der Maus“
150 px, „Gewählt“ 456 px (eigener Rollbalken, bei 1280×800: 324 px). An 485 Mausstellen wurde im
Feld „Unter der Maus“ nichts abgeschnitten. Ladezeit 0,4–0,5 s, keine Konsolenfehler.

### Stand der 15 Befunde

| Nr. | Befund | Stand | Beleg |
|---|---|---|---|
| 1 | Bild springt | **behoben** | Tabelle oben |
| 2 | Luftbild unter Flächen unsichtbar | **behoben** | Bei 10 % scheint das Foto klar durch, bei 40 % (neue Grundeinstellung) gut lesbar; Regler zeigt „Deckkraft 40 %“ |
| 3 | Hervorheben / Nur unsicher schwärzen | **behoben** | Übrige Segmente abgedunkelt, Foto bleibt sichtbar; Knopf „Hervorhebung aufheben“ |
| 4 | Abwählen | **behoben** | Esc, Klick neben das Bild und Knopf „Auswahl aufheben“ heben die Wahl auf |
| 5 | Fassungswechsel verliert Auswahl | **teilweise** | Nach Klick ins Bild bleibt die Stelle gewählt (A 100056 → P 100061 → A 100056), auch per Taste P/A. Kommt die Auswahl aus der Adresse (Link aus Kommentarliste, Übersicht, Neuladen), geht sie beim Wechsel verloren. |
| 6 | Fachwörter, Rohdaten | **behoben** | „62 Stellen an Nähten passen nicht“, „136 davon unsicher“, „Sicherheit 70 %“, „Liegt im Kern: ja“, Rohdaten unter „Technische Angaben“ (zu), Pfade unter „Technik“, Erklärfeld „Was bedeutet …?“ |
| 7 | Zahlen auf Ebenen-Knöpfen | **behoben** | Knöpfe ohne Zahl, Tooltip „im Bild 11 von 25 Kategorien“, Listenkopf „15 von 43 Kategorien“ |
| 8 | Schalterzustände, Regler | **behoben** | Eingeschaltet mit Häkchen und gelbem Rand; „Liste rechts“ statt „Kategorien“ |
| 9 | Kommentieren | **teilweise** | Neu: Meldung „Kommentar 1 vorgemerkt – noch nicht exportiert …“, „Vormerken“ erst mit Auswahl und Text aktiv, Segment im Bild hellblau umrandet, „Löschen“ in der Liste, Ortszeit (17.11.26, 19:03), Hinweis auf Browser-Speicher. Offen: Bearbeiten fehlt; Speicher weiter nur im Browser (Entwurfsfrage). |
| 10 | Übersicht | **teilweise** | Klick ins Bild öffnet die Teilkachel mit dem Segment an dieser Stelle; Nähte je Naht zusammengefasst („r0c0 / r0c1 30 Stellen …“). Offen: keine Anzeige beim Überfahren, keine Legende. |
| 11 | Farben, Auswahl | **teilweise** | Auswahl jetzt kräftig gelb umrandet, gut sichtbar. Grüntöne auf Ebene fein unverändert ähnlich. |
| 12 | Zoom | **behoben** | „Zoom 100 % / 150 % / 188 %“ wird angezeigt, Schritte maßvoll |
| 13 | Ausgegraute Fassungen | **behoben** | „B · Kategorien frei (noch leer)“; Tooltips „Taste A“ / „Taste P“ |
| 14 | Segmentinfo doppelt | **behoben** | Nur noch eine Anzeige links |
| 15 | Bildschirmfoto hing einmal | **nicht wieder aufgetreten** | im ganzen Nachtest kein Hänger |

Zusammen: 10 behoben, 4 teilweise, 1 nicht wieder aufgetreten.

### Neue Probleme durch die Umbauten

**N1. Kategorienliste springt beim Hervorheben — lästig.** Sobald eine Kategorie hervorgehoben ist,
erscheint oben in der Liste der Knopf „Hervorhebung aufheben“ und schiebt alle Einträge um 35 px nach
unten (gemessen an „4.2.1 Einzelbaum“: y 309 → 344 → 309). Ein zweiter Klick an derselben Stelle trifft
dann die Nachbarkategorie statt die Hervorhebung aufzuheben. *Nachstellen:* rechts auf „1.1.1
Hauptgebäude“ klicken, Maus nicht bewegen, nochmal klicken. *Vorschlag:* Platz für den Knopf immer
freihalten (ausgegraut, wenn nichts hervorgehoben) oder den Knopf in die Überschriftzeile setzen.

**N2. Untere Leiste bei 1280 px zu breit — Kleinigkeit.** Der Inhalt braucht 1315 px. Bei 1280 px
erscheint ein waagrechter Rollbalken, „Zoom 100 %“ ist abgeschnitten. *Vorschlag:* Etiketten kürzen
(z. B. „Deckkraft“ über dem Regler) oder den Zoom-Wert in die Kopfzeile des Bildes setzen.

**N3. „Was bedeutet …?“ verschiebt die linke Leiste — Kleinigkeit.** Beim Aufklappen schrumpft
„Gewählt“ von 456 auf 99 px, das Kommentarfeld rutscht 357 px nach oben. Das Bild bleibt ruhig, aber
die Angaben zum gewählten Segment sind dann kaum noch lesbar. *Vorschlag:* Erklärung als
überlagerndes Feld (Popover) oder auf eigener Seite.

**N4. Tippen ohne Klick ins Kommentarfeld schaltet die Fassung — Kleinigkeit.** Die neuen
Fassungstasten (A, P, C …) wirken überall außer in Eingabefeldern. Wer losschreibt, ohne vorher ins
Feld zu klicken, wechselt bei Wörtern mit „p“ oder „a“ die Fassung, und der Text geht verloren (im
Test passiert). *Vorschlag:* Nach dem Anklicken eines Segments das Kommentarfeld gleich bereit machen
(Fokus) oder Tasten nur mit Umschalt auslösen.

**N5. Exportmeldung — Kleinigkeit.** „1 Kommentare als kommentare-T0.json gespeichert (Ordner
„Downloads“)“: Die Grammatik stimmt nicht, und der Ordner stimmt nicht, wenn der Browser beim Speichern
nach dem Ort fragt. *Vorschlag:* „1 Kommentar exportiert (Datei kommentare-T0.json, meist im Ordner
Downloads).“

**N6. Segment aus einem Link wird nicht ins Bild geholt — Kleinigkeit.** Öffnet man ein Segment über
die Übersicht oder die Kommentarliste, bleibt der zuletzt eingestellte Zoom erhalten. Ein kleines
Segment (135 Bildpunkte) lag so nur zufällig im sichtbaren Teil. *Vorschlag:* Beim Öffnen per Link
das gewählte Segment mittig ins Bild holen.

### Nicht getestet (Nachtest)

Echtes Fenster 1280×800 (nachgestellt), echter Download (abgefangen; Inhalt 944 Byte, Felder wie
zuvor), Öffnen als Datei und auf Victors Rechner, Fassungen B/C, Touch.

### Bildschirmfotos (Nachtest)

Im selben Ordner `ui-test-bilder/`: `n01-nachtest-ruhe.jpg`, `n02-nachtest-gewaehlt-und-maus.jpg`,
`n03-nachtest-1280-leiste-rollbalken.jpg`, `n04-nachtest-hervorheben.jpg`,
`n05-nachtest-kommentar-markiert.jpg`, `n06-nachtest-uebersicht.jpg`.
