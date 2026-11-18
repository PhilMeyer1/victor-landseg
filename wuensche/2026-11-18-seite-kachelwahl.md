# Ergebnis-Ansicht: Wahl der vier Teilkacheln viel sichtbarer machen, damit niemand nur die erste Teilkachel sieht

Kurzname: seite-kachelwahl | Datum: 2026-11-18 | Größe: mittel | Bereich: victor | Repos: landseg | Status: eingereiht

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

„Ich möchte jetzt, dass die vier Schalter für die jeweiligen Tiles noch sehr viel sichtbarer sind. Die sind sehr wichtig, sonst sieht er ja nur ein Tile. Ich hab die am Anfang nicht erkannt und hab sie zufällig gefunden. Das muss in Zukunft verhindert werden, update das jetzt nochmal entsprechend"

Präzisierung:
- Gemeint ist die Prüf- bzw. Ergebnis-Seite (Werkzeug `seite` im Repo landseg; im Gesamtprojekt `ergebnisse/T0.html`). Heute stehen „Ganzer Ausschnitt“, `r0c0`, `r0c1`, `r1c0`, `r1c1` als kleine Textknöpfe oben neben dem Fassungs-Umschalter; die Seite öffnet mit r0c0, und man erkennt nicht, dass es vier Teilkacheln gibt.
- Ziel: Wer die Seite zum ersten Mal öffnet, erkennt sofort, ohne Erklärung, dass der Ausschnitt aus vier Teilkacheln besteht, welche gerade gezeigt wird und wie man zu den anderen kommt. Vorschläge für die Klärung (der Klärer entscheidet bzw. fragt den Nutzer, wenn es eine echte Wahl ist): eine große, auffällige Kachel-Wahl als 2 × 2-Raster in der Lage der Teilkacheln (oben links r0c0 … unten rechts r1c1), mit Miniatur-Luftbild und verständlicher Beschriftung („oben links“ usw. statt nur r0c0), die aktive deutlich hervorgehoben; Hinweis „Teilkachel 1 von 4“ mit Knöpfen „vorige/nächste“ und Pfeiltasten; „Ganzer Ausschnitt“ als eigene, gleich sichtbare Wahl; im Bild selbst ein Hinweis, dass es weitergeht. Das Bild darf beim Umschalten nicht springen (frühere Vorgabe: feste Leiste links).
- Danach: Seiten neu erzeugen (Prüfseiten in daten/landseg und `ergebnisse/T0.html` des Gesamtprojekts), die CLAUDE.md des Gesamtprojekts erwähnt in der Erklärung an Victor die Kachel-Wahl ausdrücklich; Gesamtprojekt neu bauen und hochladen macht die Hauptsession.

## Fragen

Keine offene Frage: Die Gestaltung der Kachel-Wahl (Raster, Miniaturen, Pfeile) entscheidet der Nutzer am Entwurf (Abschnitt „Entwurf"), nicht vorab.

## Entscheidungen

- „Das Bild darf beim Umschalten nicht springen" und feste Leiste links (Wunsch-Präzisierung, frühere Vorgabe zur Prüfseite aus landseg-werkzeuge-5; vom Nutzer genannt).
- entscheidungen.md: für die Seitengestaltung nichts Eigenes. Gültig bleibt dort (aus entscheidungen.md, 2026-11-17): „Die Seite zeigt je Bild genau einen Stand, das Ergebnis, mit allen drei Ebenen … kein Vorher/Nachher, keine zwei Bilder nebeneinander; die Seite muss zwischen den drei Fassungen umschalten können."
- 2026-11-18 Entwurf freigegeben: wuensche/2026-11-18-seite-kachelwahl/entwurf/d/ (Runde 1, Entwurf 4 „Schrittleiste unter dem Kopf“), Wahl des Nutzers statt der Empfehlung 2. Gebaut wird die breite, feste Schrittleiste unter dem schmalen Kopf: vorige | Ganzer Ausschnitt | vier große Reiter (1 oben links … 4 unten rechts, mit Miniatur und Raster-Symbol der Lage) | nächste; im Bild „Teilkachel n von 4“ mit Punkten und Knopf „weiter: …“. Für AK1 gilt diese Form (vier Reiter mit Raster-Symbol) als „2 × 2 in der Lage der Teilkacheln“; abgenommen wird gegen Entwurf d.
- 2026-11-18: Landschafts-Segmente: Einigung an den Übergängen der Teilkacheln: Nutzer am 18.11.2026: „Bei den Tiles am Ende sollen sich dann alle Agents bei den Übergängen mit den Klassifikationen einigen. So, dass nicht gleiche Flächen unterschiedliche Labels bekommen, weil sich die Agenten nicht abgesprochen haben.“ Daraus: Nach den Urteilen je Teilkachel folgt in jedem Lauf ein fester Einigungsschritt an allen Übergängen (Nähte zwischen Teilkacheln, auch die Viertelgrenzen): Segmente, die über eine Naht laufen oder an ihr dieselbe Fläche zeigen, bekommen eine gemeinsame, abgestimmte Klasse; unaufgelöste Widersprüche werden als unsicher markiert und belegt, nicht stillschweigend gelassen. Gilt für jede Fassung (A, B, C) und für alle künftigen Läufe (ganzes Orthofoto). (aus entscheidungen.md, 2026-11-18)

## Arbeitsauftrag

<Prüfer beim Klären, für Umsetzer und Abnahme. Bei kleinen Wünschen ohne Klärung schreibt die
Hauptsession nur die Abnahmekriterien; bei einem Teil übernimmt sie dessen Kriterien aus dem
Mutterwunsch.>

### Abnahmekriterien

AK1: Beim ersten Öffnen der Seite erkenne ich ohne Erklärung, dass der Ausschnitt aus vier Teilkacheln besteht: eine große, auffällige Wahl als 2 × 2-Raster in der Lage der Teilkacheln, jede mit Miniatur-Luftbild und Beschriftung „oben links / oben rechts / unten links / unten rechts" (die Kennung r0c0 usw. höchstens klein dazu) — prüfbar: Ansicht Teilkachel r0c0, erster Aufruf, Desktop, wie Entwurf
AK2: Die gerade gezeigte Teilkachel ist im Raster deutlich hervorgehoben und als „Teilkachel n von 4" benannt; ein Klick auf eine andere Kachel zeigt sie — prüfbar: Ansicht Teilkachel r1c1 nach Klick im Raster, Desktop, wie Entwurf
AK3: „Ganzer Ausschnitt" ist eine gleich sichtbare, eigene Wahl neben den vier Teilkacheln — prüfbar: Ansicht Ganzer Ausschnitt, Desktop, wie Entwurf
AK4: Es gibt Knöpfe „vorige" und „nächste" sowie die Pfeiltasten (links/rechts) durch die vier Teilkacheln; im Kommentarfeld und anderen Eingabefeldern stören die Pfeiltasten nicht — prüfbar: Ansicht Teilkachel r0c0, Tastendruck und Klick durch alle vier, Desktop
AK5: Im Bild selbst steht ein Hinweis, dass es mit weiteren Teilkacheln weitergeht — prüfbar: Ansicht Teilkachel r0c0, Desktop, wie Entwurf
AK6: Beim Umschalten springt das Bild nicht: die feste Leiste links und die Lage des Bildes bleiben gleich — prüfbar: Ansicht Teilkachel r0c0 und r1c1, Maße von Leiste und Bild verglichen
AK7: Die Wahl bleibt beim Wechsel der Fassung (A, B, C) erhalten und passt auf einen schmalen Bildschirm (Handy), ohne die Seite scrollen zu müssen — prüfbar: Ansicht Teilkachel r1c0 in Fassung B und Fassung C, Desktop und Handy
AK8: Die Vorlage `gesamt/CLAUDE.md` erwähnt in der Erklärung an Victor die Kachel-Wahl ausdrücklich (vier Teilkacheln im Raster, „Ganzer Ausschnitt", vorige/nächste, Pfeiltasten) statt nur der Kennungen — prüfbar: Lesen gesamt/CLAUDE.md
AK9: Die bestehenden Tests laufen weiter, Test der Seite deckt die neue Wahl ab — prüfbar: `PY -B -m unittest tests.test_seite` im Repo-Ordner

Nacharbeit: Prüfseiten in `BASIS/daten/landseg/` und `ergebnisse/T0.html` des Gesamtprojekts neu erzeugen (`PY -B -m landseg seite …`, Befehle: `gesamt/ANLEITUNG.md`, Abschnitt zur Prüfseite); Gesamtprojekt neu bauen und hochladen macht die Hauptsession (kein Push ohne Ansage). Die Kachel-Wahl in der Erklärung an Victor kommt aus der Vorlage `gesamt/CLAUDE.md`, die das Bauen ins Gesamtprojekt übernimmt.

### Einstieg

- landseg: `landseg/seite_vorlage/seite.js:230-252` — `kopf()` baut Fassungsumschalter plus `<nav>` mit „Ganzer Ausschnitt" und vier kleinen Textlinks r0c0 … r1c1 in die 72-px-Kopfzeile; hier entsteht die auffällige Kachel-Wahl (neue Funktion, die Kopf und Ansicht gemeinsam nutzen).
- landseg: `landseg/seite_vorlage/seite.js:273-316` — `ansicht()` baut Leiste links (`c-info`), Bildtafel (`c-tafel`, Überschrift „Teilkachel …") und Kategorienleiste; Platz für Raster, „n von 4" und Weiterhinweis im Bild.
- landseg: `landseg/seite_vorlage/seite.js:519-524` — `uebersicht()` (Ganzer Ausschnitt): braucht dieselbe Wahl, „Ganzer Ausschnitt" dort als aktive Wahl.
- landseg: `landseg/seite_vorlage/seite.js:596-610` — Tastenbehandlung (Esc, Umschalt + Kennung); Pfeiltasten dazu, nie beim Tippen in Eingabefeldern.
- landseg: `landseg/seite_vorlage/seite.js:613-621` — `weg()`: Routen `#/<F>/kachel/<tk>`, `#/<F>/uebersicht`; öffnet heute mit der ersten Teilkachel mit Daten (`ersteKachel`, Zeile 119).
- landseg: `landseg/seite_vorlage/seite.css:13,36-42` — feste Maße (`--kopf-hoehe: 72px`, Grid `c-seite`); die Kopfhöhe darf sich fürs Raster ändern, aber nicht beim Umschalten.
- landseg: `landseg/seite.py:225-236` — liefert je Teilkachel `bild` (PNG) und `zeile`/`spalte` in `D.teilkacheln`; die Miniaturen brauchen daher keine neuen Daten.
- landseg: `gesamt/CLAUDE.md` — Erklärung an Victor (Schritt 4, Punkt „Daneben die Wahl der Bildstücke"); dort die Kachel-Wahl ausdrücklich nennen.

### Bausteine und Fallen

- Wiederverwenden: `D.teilkacheln[i].bild` (PNG-Datenadresse je Teilkachel, `zeile`, `spalte`) als Miniatur im Raster, kein neues Bild erzeugen; `FA.tk[t.id]` zeigt, ob eine Teilkachel in der Fassung Daten hat (ohne Daten: Kachel ausgegraut wie heute `c-ohne`); Routen und `gehe()` bleiben, die Wahl ist nur eine andere Darstellung derselben Links; Muster der Fassungsknöpfe (`aria-pressed`, Fokusring `--akzent`) für die Hervorhebung.
- Fallen: (1) Kopf und Leiste haben feste Maße (`seite.css:1-4`), damit das Bild nicht springt; die Höhe der Wahl bleibt in allen Zuständen gleich, auch in `uebersicht()` und in Fassungen mit leeren Teilkacheln. (2) Die Seite ist eine einzige HTML-Datei mit PNG im Text: Miniaturen als verkleinerte Anzeige derselben Bilder (CSS), nicht als zweite Kopie, sonst wächst die Datei. (3) Tastenbehandlung: Pfeiltasten nicht in `TEXTAREA`/`INPUT` abfangen; Esc und Umschalt + Kennung bleiben. (4) Test: `tests/test_seite.py` prüft die erzeugte Datei; dort einen Prüfpunkt für Raster und Beschriftungen ergänzen. (5) Seiten in `daten/landseg/` sind abgeleitete Daten, nicht ins Repo.

### Bauweise

<Prüfer, Pflicht: ob der Wunsch das Repo seinem Zielbild (`<repo>/zielbild.md`) näherbringt, es
unberührt lässt oder davon wegführt; Anbau, Umbau, Belege und Empfehlung nur, wenn er eine Altlast
aus `<repo>/altlasten.md` berührt, ein Anbau vom Zielbild wegführen würde oder `Flick-Signale`
belegt sind, dann dazu die Frage „Weiter anbauen, umbauen oder ganz neu bauen" unter „Fragen".>
Richtung: ohne Zielbild
Berührt: landseg: keine — A2 (seite.py:60, Luftbild-Leser) liegt in derselben Datei, aber nicht an der Stelle des Wunschs
Tilgt: keine
Flick-Signale: keine — kein Vorgänger an dieser Stelle: der Wunsch ändert den Kopf der Seitenvorlage (`kopf()`) erstmals; frühere Wünsche (landseg-werkzeuge-5, landseg-test-t0-3, landseg-gesamt) bauten die Seite neu bzw. berührten Nähte und Gesamtprojekt, kein Glied behob einen Fehler am Kopf.
Anbau: Kachel-Wahl als eigene Funktion in `seite.js` und Stil in `seite.css`, `kopf()` und `uebersicht()` benutzen sie — Dauer kurz — Risiko gering (Sprung des Bildes bei falschen Maßen, per AK6 geprüft) — danach bleibt eine Kachel-Wahl an einer Stelle
Umbau: nicht erwogen, kein Beleg.
Belege: –
Empfehlung: Anbau — keine Altlast berührt, kein Sonderfall, keine Kopie: die Wahl ersetzt die vier Textlinks. Repo ohne Zielbild: Bauzustand ermitteln; Maßstab ist ein sauberer Aufbau.

Reihenfolge der Repos: landseg · Risiken: Maße von Kopf und Leiste (Bild darf nicht springen); Dateigröße der Seite · Vorbedingungen: keine

## Teile

<Nur bei Größe gross, vom Prüfer: nummerierte Liste, je Teil
„Name — Umsetzer|Workflow [— Halt: Durchsicht|Wahl|Freigabe] — nach: –|<Nummern> — AK <Nummern> — ein
Satz, was dann fertig ist". `Halt:` nur, wenn der Nutzer vor dem Einreihen durchsieht, wählt oder freigibt.
„nach" nennt die Teile, die vorher eingereiht sein müssen; Teile ohne gemeinsame Stellen laufen
parallel. Die Hauptsession legt je Teil einen eigenen Wunsch <kurzname>-N an.>

## Varianten

<Nur bei Größe mittel mit sichtbarer Entwurfsfrage, vom Prüfer: „a: …" und „b: …", je ein bis
zwei Sätze, was der Nutzer sehen wird. Mit Entwurf zeigt er beide, der Nutzer wählt bei der
Freigabe; ohne Entwurf bauen zwei Umsetzer parallel. Die Wahl steht danach unter „Entscheidungen".>

## Entwurf

Stufe: ausgearbeitet

- Ansicht Teilkachel (Fassung C, r0c0 und r1c1 aktiv): Kopf mit Fassungsumschalter und Kachel-Wahl; Zustände: erster Aufruf, andere Teilkachel aktiv, Teilkachel ohne Daten (ausgegraut), mit Hinweis im Bild; Desktop und Handy.
- Ansicht Ganzer Ausschnitt: dieselbe Wahl, „Ganzer Ausschnitt" aktiv; Desktop und Handy.
- Nachbarn zum Nachbilden: die bisherige Seite (Fassungsknöpfe `aria-pressed` im Kopf, feste Leiste links, Bildtafel, Kategorienleiste rechts), dunkles Aussehen und Akzent `#ffeb3c` aus `seite.css`.
- Beispieldaten: T0 mit vier Teilkacheln (Luftbild-Miniaturen aus `ergebnisse/teilkacheln/`), Fassung C.
