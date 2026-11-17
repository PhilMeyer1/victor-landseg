# Landschafts-Segmentierung von Luftbildern: Gesamtprojekt für Victor

Hier liegt alles zum Vorhaben „Luftbilder lückenlos in Flächen zerlegen und jede Fläche einer
Kategorie zuordnen“: das Programm mit seiner ganzen Entstehungsgeschichte, alle Aufträge und
Berichte, aus denen es entstanden ist, die vollständigen Arbeitsdaten des ersten Tests (T0) und
dessen Ergebnisse. Nur die Original-Luftbilder fehlen, weil sie zu groß für GitHub sind; sie kommen
getrennt (`daten/luftbilder/README.md`).

## In dieser Reihenfolge lesen

1. **Ergebnis ansehen**: `ANLEITUNG.md` (was getestet wurde, Zahlen, Schwächen, wie man es
   nachrechnet) und die Prüfseite `ergebnisse/T0.html` (doppelklicken, kein Server nötig).
2. **Wie ist es entstanden?** Die Aufträge und Berichte in `wuensche/`, in zeitlicher Reihenfolge:

   | Schritt | Auftrag | Berichte und Material |
   |---|---|---|
   | Deine Berichte geordnet abgelegt | `wuensche/2026-11-17-berichte-einpflegen.md` | `wuensche/2026-11-17-berichte-einpflegen/` |
   | Verfahren gesucht (Methoden-Ermittlung) | `wuensche/2026-11-17-landseg-methode.md` | `wuensche/2026-11-17-landseg-methode/bericht.md` (Ergebnis), dazu `plan.md`, `deutung.md`, die Einzelfragen in `einheiten/` und ihre Gegenprüfung in `gegenpruefung/` |
   | Gestufte Kategorienliste | `wuensche/2026-11-17-landseg-kategorien.md` | `wuensche/2026-11-17-landseg-kategorien/` |
   | Werkzeuge gebaut (fünf Teile) | `wuensche/2026-11-17-landseg-werkzeuge.md` | `wuensche/2026-11-17-landseg-werkzeuge/` (Entwürfe der Prüfseite), Teile `wuensche/2026-11-17-landseg-werkzeuge-1/` bis `wuensche/2026-11-17-landseg-werkzeuge-5/` |
   | Kategorien nach Bedeckung statt Nutzung | `wuensche/2026-11-17-landseg-kat-bedeck.md` | `wuensche/2026-11-17-landseg-kat-bedeck/` |
   | Testlauf T0 (fünf Teile, drei davon gelaufen) | `wuensche/2026-11-17-landseg-test-t0.md` | `wuensche/2026-11-17-landseg-test-t0-1/` (Vorstufe, Aufträge je Agent), `wuensche/2026-11-17-landseg-test-t0-2/` (Urteile), `wuensche/2026-11-17-landseg-test-t0-3/` (Zusammenführen); Teile 4 und 5 ruhen |
   | Übergabe der Ergebnisse | `wuensche/2026-11-17-landseg-uebergabe.md` | `wuensche/2026-11-17-landseg-uebergabe/` |
   | Dieses Gesamtprojekt | `wuensche/2026-11-17-landseg-gesamt.md` | `wuensche/2026-11-17-landseg-gesamt/` |

   Jede Auftragsdatei beginnt mit dem Wunsch in unseren Worten, dann den Entscheidungen und dem
   Arbeitsauftrag; die Berichte (`bericht-*.md`) sagen, was gebaut und geprüft wurde, die Abnahmen
   (`abnahme-*.md`), was eine zweite Prüfung dazu fand. `wuensche/entscheidungen.md` sammelt die
   Entscheidungen, die über einen einzelnen Auftrag hinaus gelten; `wuensche/uebersicht.md` listet
   alle Aufträge mit ihrem Stand.
3. **Das Programm**: `programm/README.md` (Werkzeuge, Befehle, Dateiformate) und
   `programm/KATEGORIEN.md` (die feste Kategorienliste in Alltagssprache).
4. **Deine Unterlagen**: `unterlagen/README.md` mit den gelieferten Berichten 41, 46, 47 und 48.
5. **Die Arbeitsdaten**: `daten/landseg/T0/`, wenn du einem Bericht bis in die einzelne Datei folgen
   willst.

## Aufbau

| Pfad | Inhalt |
|---|---|
| `README.md` | diese Seite |
| `ANLEITUNG.md` | Anleitung zum Test T0: Ergebnis, Zahlen, Dateiformate, Befehle |
| `programm/` | das Programm `landseg` mit seinem vollen Git-Verlauf (Python-Paket, Tests, Werkzeuge, Kategorienliste, Vorlagen für die KI-Agents) |
| `unterlagen/` | deine gelieferten Berichte, mit ihrem Git-Verlauf |
| `wuensche/` | alle Aufträge, Berichte, Abnahmen, die Methoden-Ermittlung und die Aufträge an die einzelnen KI-Agents |
| `ergebnisse/` | die Übergabe-Auswahl von T0 mit neuer Benennung: Prüfseite, Gesamtbilder, Karten und Urteile je Fassung |
| `daten/landseg/` | die vollen Arbeitsdaten von T0 mit den alten Ordnernamen (`daten/landseg/T0/kern500/`, `daten/landseg/T0/fassung-b/`, `daten/landseg/T0/fassung-c/`): Zwischenbilder, Nahansichten der Agents, Rohwerte der Vorstufe, Probeläufe, einzelne Viertel-Urteile |
| `daten/luftbilder/` | Platz für die Original-Luftbilder; welche es sind, mit Größe und Prüfsumme, steht in `daten/luftbilder/README.md` |

`ergebnisse/` und `daten/landseg/` überschneiden sich: `ergebnisse/` ist die aufbereitete Auswahl,
die zuerst übergeben wurde (umbenannt, ohne Zwischenbilder); `daten/landseg/` ist der Arbeitsstand,
so wie die Berichte ihn nennen.

## Benennung der Fassungen

Der Test hat T0 in drei Fassungen eingeordnet. Es gilt:

- **A = Alles frei**: Die KI bestimmt Grenzen, Kategorien und Arbeitsweise selbst.
- **B = Kategorien frei**: Die KI benennt und stuft die Klassen selbst; Grenzen und Arbeitsweise wie C.
- **C = Feste Kategorienliste**: Klassen aus unserer festen, gestuften Liste (`programm/kategorien.json`).

Während des Tests hießen die Fassungen anders. Die älteren Berichte unter `wuensche/` und die
Arbeitsdaten unter `daten/landseg/T0/` sind unverändert und benutzen die alten Namen:

| neu | Name | früher | früherer Ordner |
|---|---|---|---|
| A | Alles frei | Fassung C | `fassung-c` |
| B | Kategorien frei | Fassung B | `fassung-b` |
| C | Feste Kategorienliste | Fassung A | `kern500` (Karte `urteil-stand`) |

## Was bewusst fehlt

- Die Original-Luftbilder (vier Bilder mit Lagedateien, zusammen rund 610 MB): getrennt, Liste mit
  Prüfsummen in `daten/luftbilder/README.md`.
- Rohe Mitschnitte der KI-Läufe (Ordner `roh/` in den Berichtsordnern) und Verwaltungsdateien
  unseres Auftragssystems (Laufzähler, Prüfsummen von Einstellungsdateien, Protokolle des
  Einreihens): ohne Wert zum Nachvollziehen.
- Zwei Einzelberichte der Methoden-Ermittlung (`einheiten/e05.md` und `gegenpruefung/e05.md`):
  ausführliche Auswertung einer Arbeitssitzung aus einem anderen Projekt, aus dem das Verfahren
  übernommen wurde. Was davon für die Landschaft gilt, steht in
  `wuensche/2026-11-17-landseg-methode/bericht.md` und `wuensche/2026-11-17-landseg-methode/plan.md`.

Pfade wie `C:/Users/Phil/Developement/Victor/…` in den Berichten zeigen auf den Rechner, auf dem
gerechnet wurde; dieser Ordner entspricht dort dem Projektordner hier (`landseg` ist `programm/`).

## Verlauf

Die Commits des Programms und der Unterlagen sind mit ihrer ursprünglichen Kennung übernommen
(`git subtree`): `git log --oneline` zeigt sie alle, in zeitlicher Reihenfolge mit den
Übernahmen dazwischen. In diesen Commits liegen die Dateien noch so wie im ursprünglichen Repo,
also ohne den Vorsatz `programm/`. Darum zeigt `git log -- programm` nur die Übernahmen
(„Add 'programm/' …“, „chore: update programm/ …“). Die Kennungen sind bewusst unverändert
geblieben, damit die Kennungen in den Berichten (etwa `e805308`) hier nachschlagbar sind.

So siehst du den Einzelverlauf:

1. `git log --oneline -1 -- programm` zeigt die jüngste Übernahme des Programms.
2. Ihr zweiter Elternteil ist der übernommene Stand von `landseg`:
   `git log --oneline <Kennung der Übernahme>^2` zeigt alle Commits des Programms bis dahin, ohne
   die übrigen Commits dieses Projekts. Für die Unterlagen gilt dasselbe mit `unterlagen` statt
   `programm`.
3. Den Verlauf einer einzelnen Programmdatei zeigt
   `git log --oneline --full-history -- landseg/kacheln.py` (Pfad ohne `programm/`).
4. Einen einzelnen Commit aus einem Bericht zeigt `git show <Kennung>`.

Der erste Stand dieses Projekts (die Übergabe vom 17.11.2026, Commit `f0a0198`) bleibt im Verlauf.
Das Projekt wird mit `programm/tools/gesamt_projekt.py bauen` aus unserem Arbeitsordner
aufgefrischt; `pruefen` und `durchsicht` sichern Vollständigkeit, Größen (GitHub nimmt keine Datei
über 100 MB) und dass nichts Vertrauliches darin steht.
