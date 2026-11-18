# Anweisungen für Claude Code in diesem Projekt

Dieses Projekt gehört Victor: Luftbilder lückenlos in Flächen (Segmente) zerlegen und jede Fläche
einer Kategorie zuordnen. Ergebnis des ersten Tests ist der Ausschnitt T0 in drei Fassungen.

## Zuerst, in jeder Session: Ergebnis-Ansicht öffnen

Bei deiner ersten Antwort in einer Session, egal was Victor geschrieben hat (auch nur „hallo“),
ohne Rückfrage und bevor du etwas anderes tust:

1. Prüfen, ob die Seite da ist: `ergebnisse/T0.html` im Projektordner (rund 8 MB).
2. Sie im Standard-Browser öffnen, mit dem Befehl für das Betriebssystem, vom Projektordner aus:

   | System | Befehl |
   |---|---|
   | Windows, Bash-Werkzeug (Git Bash) | `cmd //c start "" "ergebnisse\T0.html"` |
   | Windows, PowerShell | `Start-Process -FilePath (Resolve-Path "ergebnisse/T0.html")` |
   | Windows, Eingabeaufforderung | `start "" "ergebnisse\T0.html"` |
   | macOS | `open "ergebnisse/T0.html"` |
   | Linux | `xdg-open "ergebnisse/T0.html"` |

3. Prüfen, dass der Befehl ohne Fehler lief (Exit-Code 0, keine Fehlermeldung). Wenn nicht: die
   Meldung wörtlich nennen und Victor bitten, `ergebnisse/T0.html` per Doppelklick zu öffnen.
4. Victor in wenigen Sätzen sagen, was er sieht:
   - Oben der Umschalter der drei Fassungen: **A „Alles frei“** (die KI bestimmt Grenzen,
     Kategorien und Arbeitsweise selbst), **B „Kategorien frei“** (die KI benennt und stuft die
     Klassen selbst), **C „Feste Kategorienliste“** (unsere feste, gestufte Liste mit 58 Klassen).
     Die Seite öffnet mit A; Umschalt + A/B/C wechselt ebenfalls.
   - Wichtig, ausdrücklich sagen: Der Ausschnitt besteht aus **vier Teilkacheln** (Bildstücken),
     und die Seite zeigt immer nur eine davon. Darunter liegt deshalb die breite **Kachel-Wahl**:
     „Ganzer Ausschnitt“ und die vier Teilkacheln als große Reiter im Raster ihrer Lage,
     1 „oben links“, 2 „oben rechts“, 3 „unten links“, 4 „unten rechts“ (je mit kleinem Luftbild;
     die Kennungen `r0c0` … `r1c1` stehen klein dabei, r = Zeile, c = Spalte). Die gezeigte
     Teilkachel ist gelb umrandet. Die Seite beginnt mit Teilkachel 1 (oben links): Luftbild,
     darüber die Segmente in Klassenfarben; im Bild steht „Teilkachel 1 von 4“ mit dem Knopf
     „weiter“. Zu den anderen drei kommt er über die Reiter, die Knöpfe „vorige“ und „nächste“
     an den Enden der Kachel-Wahl oder die Pfeiltasten ← → (nicht beim Schreiben im Kommentarfeld).
   - Ein Klick auf ein Segment zeigt Klasse, Sicherheit und Urteil der KI. Mausrad vergrößert,
     Ziehen verschiebt; Schalter für Ebene (grob/mittel/fein), Umriss, Lücken, Nähte, Kategorien.
   - Zu einem angeklickten Segment kann er einen Kommentar schreiben („Vormerken“) und alle
     Kommentare über „Export (JSON)“ als Datei speichern.
   - Weiterlesen: `ANLEITUNG.md` (was getestet wurde, Zahlen, Schwächen, Befehle) und `README.md`
     (Aufbau des Projekts, Vorgeschichte, Benennung der Fassungen).

Fehlt `ergebnisse/T0.html` (etwa weil der Download unvollständig ist): das offen sagen, nichts
anderes öffnen und nicht raten. Vorschlag an Victor: `git status` und `git pull` im Projektordner,
oder das Projekt neu klonen.

Nicht die älteren Seiten öffnen: `daten/landseg/T0/kern500/seite/T0.html`,
`daten/landseg/T0/kern500/seite/T0-urteil.html` und `daten/landseg/T0/kern500/seite/T0-probe.html`
sind Arbeitsstand mit alter Benennung (dort heißt die feste Liste noch „A“). Die gültige Ansicht ist
nur `ergebnisse/T0.html`.

## Projekt-Aufbau

| Pfad | Inhalt |
|---|---|
| `README.md` | Einstieg: Aufbau, Lesereihenfolge, Benennung der Fassungen, Arbeiten auf eigenem Zweig |
| `ANLEITUNG.md` | Test T0: Ergebnis, Zahlen, Dateiformate, Befehle, Python-Umgebung |
| `ergebnisse/` | aufbereitete Ergebnisse von T0 mit neuer Benennung (`ergebnisse/T0.html`, `ergebnisse/gesamtbilder/`, je Fassung ein Ordner) |
| `programm/` | das Programm `landseg` (Python-Paket, Tests, Werkzeuge, Kategorienliste) mit Verlauf |
| `unterlagen/` | Victors gelieferte Berichte |
| `wuensche/` | Aufträge, Berichte und Abnahmen, aus denen alles entstanden ist |
| `daten/landseg/` | volle Arbeitsdaten von T0 mit alten Ordnernamen |
| `daten/luftbilder/` | Platz für die Original-Luftbilder (kommen getrennt, Liste in `daten/luftbilder/README.md`) |

## Nur lesen

- Die Original-Luftbilder unter `daten/luftbilder/`: nie ändern, verschieben oder löschen.
- Die Ergebnisse unter `ergebnisse/` und die Arbeitsdaten unter `daten/landseg/`: nicht
  überschreiben. Eigene Rechnungen gehören nach `arbeit/` (nimmt Git nicht auf).
- `unterlagen/` und `wuensche/`: Quellen zum Nachlesen, nicht umschreiben.

## Arbeiten

- Auf einem eigenen Zweig, nie direkt auf `main` (Ablauf in `README.md`, „Mitarbeiten“).
- Python-Umgebung nach `ANLEITUNG.md`, Abschnitt „Umgebung“ (eigenes `.venv`, Pakete dort).
  Die Werkzeuge laufen im Ordner `programm/`: Tests `python -B -m unittest discover -s tests -t .`,
  Hilfe `python -B -m landseg --help`.
- Prüfen, ob das Projekt vollständig ist (nur Standardbibliothek), im Projektordner:
  `python -B programm/tools/gesamt_projekt.py pruefen --ziel .` (mit `--luftbilder daten/luftbilder`
  auch die Original-Luftbilder).
