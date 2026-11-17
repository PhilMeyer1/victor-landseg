# Teil 5 von landseg-werkzeuge: Prüfseite und Abnahme an T0-Teilkachel

Kurzname: landseg-werkzeuge-5 | Datum: 2026-11-17 | Größe: mittel | Bereich: victor | Repos: landseg | Status: eingereiht | Mutterwunsch: landseg-werkzeuge

<Diese Datei ist der Auftrag: Wer nach der Klärung hineinschreibt, regelt Kernregel 6 des Skills `wunsch`. Berichte
und Abnahme der Agents liegen im Ordner mit demselben Namen ohne `.md` daneben
(`bericht-<repo>.md`, `abnahme-<repo>.md`). `Bereich:` kommt aus dem Profil des Repos bzw. der Gruppe;
ein durchgereichter Wunsch trägt oben `Gruppe: <name>`, unten `Herkunft: <Basisordner>/<kurzname>`.>

## Wunsch

Teil 5 des Mutterwunschs `landseg-werkzeuge` (`wuensche/2026-11-17-landseg-werkzeuge.md`), Zeile aus dessen Teile-Liste:

5. Prüfseite und Abnahme an T0-Teilkachel — Umsetzer — Repo: landseg — Vorbedingungen: keine — Halt: Durchsicht — nach: 2, 3, 4 — AK 6, 8 — Prüfseite steht und die ganze Befehlsfolge läuft an einer echten Teilkachel; Sie sehen die Seite vor dem Einreihen durch

## Fragen

keine (siehe Mutterwunsch)

## Entscheidungen

siehe Mutterwunsch

- 2026-11-17, Durchsicht (Nutzer): Ändern. Wortlaut: „Es soll nur eine Version geben mit allen Stufen und Klassifikationen" und „erstelle dafür 2 zusätzliche Versionen. Das soll jetzt alles nur als Übersicht für Victor dienen, der sich dann raussuchen kann, was er am besten findet. Eine Version der Ergebnisse ohne Vorher nachher". Wünsche an die Nachbesserung:
  1. Kein Vorher/Nachher mehr: je Bild genau ein Stand (das Ergebnis), ein großes Bild statt zwei nebeneinander; Ebene grob/mittel/fein umschaltbar, Klassifikation jedes Segments beim Überfahren und Klick wie bisher (Mauszeile, Karte „Unter der Maus"/„Gewählt", Kategorienliste mit Segmentzahl und Flächenanteil). Ebene „Änderungen" und `--nachher` entfallen bzw. werden nicht mehr gezeigt.
  2. Umschalter zwischen Fassungen desselben Testfensters: A „feste Kategorienliste", dazu zwei freie Fassungen B und C (Entscheidung „drei Fassungen als Übersicht für Victor" in entscheidungen.md). Jede Fassung bringt ihre eigene Kategorienliste mit (Code, Name, Eltern, Ebene, Farbe im Format von `kategorien.json`); die Seite nimmt Klassen, Namen und Farben je Fassung aus deren Liste, nie fest eingebaut. Die Ergebnisse von B und C entstehen erst im Test; die Seite muss nur damit umgehen können (Fassung fehlt = Umschalter ausgegraut). Name und Kurzbeschreibung je Fassung stehen auf der Seite.
  3. Die Seite ist eine Übersicht für Victor zum Auswählen: einfach, ohne Erklärung verständlich; Kommentare und deren Export bleiben.
  4. Die Beispiel-Daten nutzen den neuen Stand der Kategorienliste (Bedeckung statt Nutzung, 7/25/43, eingereiht mit landseg-kat-bedeck 3b4e855): Vorstufe T0 aller vier Teilkacheln neu rechnen (GPU, Belegung wie bisher), die alte Beispiel-Seite mit `1.4.x`-Codes ersetzen. Zur Probe des Umschalters darf eine zweite Fassung aus vorhandenen Daten gebildet werden (deutlich als Probe benannt).
- 2026-11-17, zweite Durchsicht (Nutzer): Ändern. Wortlaut: „Die Segmentinfos müssen in einer Sidebar links angezeigt werden, sonst springt das Bild extrem nervig herum. Lass jetzt mal einen Agent die UI testen und Probleme, Nerviges usw. finden, um die Nutzererfahrung entsprechend zu verbessern." Umsetzung: (1) Segmentinfos (Unter der Maus / Gewählt, Kategorie auf allen Ebenen, Felder) in einer festen Leiste links mit fester Breite und Höhe; nichts darf beim Überfahren oder Klicken die Lage des Bildes verschieben. (2) Ein Agent testet die Seite im Browser (Claude in Chrome, Seite über einen lokalen Webserver, weil die Erweiterung `file://` nicht öffnet) und schreibt die Befunde nach `ui-test.md` in den Berichtsordner; die Nachbesserung behebt das Springen und alle Befunde, die der Test als störend einstuft. Die alten Daten `umsetzen/` und `T0-umsetzen.html` hat die Hauptsession nach Freigabe des Nutzers gelöscht.
- 2026-11-17, dritte Durchsicht (Nutzer): „Kurz nachbessern, dann einreihen". Nach Browser-Nachtest (`ui-test.md`, Abschnitt „Nachtest": Bild springt nicht mehr, 10 von 15 Befunden behoben, 4 teilweise) behebt die Nachbesserung N1 (Kategorienliste rutscht 35 px, sobald „Hervorhebung aufheben" erscheint), N4 (Tippen ohne Fokus im Kommentarfeld löst Tastenkürzel aus) und N5 (Mehrzahl in der Exportmeldung); danach einreihen ohne weitere Durchsicht. Beleg-Freigabe (Nutzer 2026-11-17): AK6 (Ansicht im Browser) ist mit dem Browser-Test und Nachtest in `ui-test.md` belegt; ohne erneute Ansicht durch die Abnahme einreihen. Restliche Kleinigkeiten (5, 9, 10, 11, N2, N3, N6) bleiben offen und kommen über Kommentare im Test.

## Arbeitsauftrag

### Abnahmekriterien

AK6: Die Prüfseite öffnet sich als Datei im Browser und zeigt Ebenen grob/fein, Lückenkarte, Naht-Ebene, Vorher/Nachher und Kommentar-Export (nach F1) — prüfbar: Ansicht Prüfseite an der T0-Teilkachel, Desktop, wie Entwurf
AK8: Der Weg des Nutzers: Nach der Anleitung in der `README.md` führt eine Befehlsfolge (kacheln, vorstufe, pruefen, seite) an einer T0-Teilkachel bis zur geöffneten Prüfseite; abgeleitete Daten liegen unter `BASIS/daten/landseg/`, nichts im Repo außer Code, Vorlagen, Tests, `README.md`; Originale und Stitcher unverändert — prüfbar: Befehlsfolge am laufenden Stand, `git status` in landseg und stitcher, Lesen `README.md`

Einstieg, Bausteine, Entscheidungen: siehe Mutterwunsch

Vorbedingungen: keine

Halt: Durchsicht
