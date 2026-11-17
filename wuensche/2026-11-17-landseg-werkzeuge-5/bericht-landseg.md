# Bericht landseg
Status: eingereiht
Für den Nutzer: Die Seite ist nach der zweiten Durchsicht und dem UI-Test umgebaut.
  - Links gibt es jetzt eine feste Leiste. Oben darin steht „Unter der Maus“, darunter „Gewählt“ mit dem Knopf „Auswahl aufheben“, dann das Kommentarfeld und „Was bedeutet …?“.
  - Das Bild bleibt beim Überfahren, Klicken, Abwählen und Ziehen stehen.
  - Die Farben liegen jetzt durchscheinend über dem Luftbild. Der Regler zeigt „Deckkraft 40 %“, das ist der neue Standard.
  - Hervorheben einer Kategorie und „Nur unsicher“ blenden die übrigen Flächen nur ab, statt sie schwarz zu füllen.
  - Esc oder ein Klick neben das Bild heben die Wahl auf.
  - Beim Wechsel der Fassung bleibt dieselbe Stelle gewählt. Umschalten geht auch mit den Tasten A, B, C bzw. P.
  - Leere Fassungen tragen „(noch leer)“.
  - Eingeschaltete Schalter sind gelb und haben ein Häkchen. „Kategorien“ heißt jetzt „Liste rechts“. Eine Zoomanzeige ist dazugekommen.
  - Kommentare melden „vorgemerkt – noch nicht exportiert“. Segmente mit Kommentar haben einen blauen Rand. In der Kommentarliste kann man vorgemerkte Kommentare löschen, die Zeiten stehen in Ortszeit.
  - Im ganzen Ausschnitt öffnet ein Klick ins Bild die Teilkachel an dieser Stelle.
  Die Vorstufe habe ich nicht neu gerechnet, die Seiten sind aus den vorhandenen Daten gebaut: `C:/Users/Phil/Developement/Victor/daten/landseg/T0/kern500/seite/T0.html` und `T0-probe.html`. Im Browser angesehen habe ich sie nicht, das macht der nächste Test.
Commit: 72b3c20 "feat: add seite tool for the single-file overview page with versions"
Abnahmekriterien:
AK6: nicht prüfbar (vom Umsetzer). Beide Seiten sind gebaut. Die Rauchprobe in Node misst, was sich ändert (`C:/Users/Phil/AppData/Local/Temp/claude/27e54e3b8399faf6/a2bf01d3-627c-4b06-8b57-51f25ab5229e/scratchpad/r4.js`, Ausgaben `C:/Users/Phil/Developement/Victor/wuensche/2026-11-17-landseg-werkzeuge-5/rauch-T0.txt` und `rauch-probe.txt`). Bei Überfahren, Verlassen, Klick, Esc, Klick neben das Bild und Ziehen ändern sich nur Elemente der linken Leiste, die Zoomanzeige und das Bild-Canvas. Die CSS-Prüfung ergibt: Kopf, untere Leiste und linke Leiste haben feste Maße, nur die Bildspur ist `1fr`. Fehler: 0. Die Browser-Ansicht fehlt noch
AK8: erfüllt (seit der vorigen Runde unverändert). `seite --manifest … --ziel …/seite/T0.html` → Exit 0; `git status` landseg sauber nach dem Commit
Prüfungen:
python -B -m unittest tests.test_seite → 7 Tests OK
tools/pruefe_kategorien.py kategorien.json → ok
node --check seite.js → ok
Rauchprobe T0.html: alle sechs Handlungen „ruhig“, Wege A, Übersicht, Kommentare, Umleitung C→A ok, Fehler 0
Rauchprobe T0-probe.html: Taste P nach Klick → `#/P/kachel/r0c0/segment/100001` (Stelle bleibt gewählt), Fehler 0
Vorstufe: in den letzten 10 min keine Datei unter `vorstufe/` geändert (Stand 17:58–18:00). Nur gelesen, nichts geschrieben
seite T0.html 6818 KiB, T0-probe.html 7249 KiB
Aufruf-Budget: überschritten (rund 55 von 50 Aufrufen). Die zweite Nachbesserung kam im selben Lauf dazu: Lesen des UI-Tests, Neubau von JS und CSS und die neue Rauchprobe brauchten zusätzliche Aufrufe
volle Stufe: offen fürs Einreihen
Befunde des UI-Tests (`ui-test.md`):
1 (störend) behoben: feste linke Leiste (320 px) mit Bereichen fester Höhe; untere Leiste einzeilig mit fester Höhe; Bildunterschrift und Fassungsbeschreibung einzeilig. Die Rauchprobe belegt, dass sich außerhalb der Leiste nichts ändert
2 (störend) behoben: `setze()` mischt jetzt richtig über den durchsichtigen Puffer, das Luftbild scheint durch; Reglerbeschriftung mit Prozentwert
3 (störend) behoben: Abblenden mit 60 % statt schwarzer Füllung (Umriss bleibt), hervorgehobene Kategorie mit gelbem Rahmen, Knopf „Hervorhebung aufheben“
4 (lästig) behoben: Esc, Klick neben das Bild und der Knopf „Auswahl aufheben“
5 (lästig) behoben: die zuletzt geklickte Stelle wird in der neuen Fassung gewählt; Tasten mit den Kennungen schalten um
6 (lästig) behoben: Rohfelder zugeklappt unter „Technische Angaben“; Sicherheit in %, „Liegt im Kern: ja/nein“, „Im Siedlungsgebiet“; Legende „Was bedeutet …?“ (Fassung, Teilkachel, Kern, Rand, Naht, Lücke, unsicher, blauer Rand); Pfade nur unter „Technik“; Wörter „Nahtverstöße“ und „feiner nicht bestimmt“ ersetzt
7 (lästig) behoben: keine Zahl mehr auf den Ebenen-Knöpfen, Tooltip „im Bild N von M“, Listenkopf „Im Bild · Ebene fein · 15 von 43 Kategorien“
8 (lästig) behoben: An-Zustand gelb mit ✓, Regler „Deckkraft 40 %“, „Liste rechts“
9 (lästig) teils behoben: Rückmeldung nach Vormerken und Export, „Vormerken“ nur mit Wahl und Text, Hinweis „nur in diesem Browser“, blauer Rand am Segment, Kommentare des Segments in „Gewählt“, Löschen vorgemerkter Kommentare, Ortszeit. Nicht behoben: Bearbeiten (Löschen und neu schreiben reicht). Ebenfalls nicht behoben: der gemeinsame Speicher von T0.html und T0-probe.html. Er bleibt mit Absicht, weil beide denselben Ausschnitt mit Fassung A zeigen und die Kommentare dazu zusammengehören
10 (Kleinigkeit) teils behoben: Klick ins Bild öffnet die Teilkachel an der Stelle; Abweichungen je Naht gezählt statt Rohliste. Nicht behoben: Mausanzeige und Ebenen-Umschalter in der Übersicht (mehr Aufwand)
11 (Kleinigkeit) teils behoben: Auswahl mit 2 px gelbem Rand. Nicht behoben: ähnliche Farben, weil sie aus `kategorien.json` kommen; das gehört zur Kategorienliste, nicht zur Seite
12 (Kleinigkeit) behoben: Zoomanzeige, Schritte ×1,5 statt ×2, Doppelklick vergrößert
13 (Kleinigkeit) behoben: „(noch leer)“, ausgegraute Knöpfe gestrichelt
14 (Kleinigkeit) behoben: Mauszeile unten entfallen; nur noch „Unter der Maus“ und „Gewählt“ in der linken Leiste
15 (Kleinigkeit) nicht behoben: kein Fehler der Seite feststellbar (laut Test vermutlich die Erweiterung)
Nicht geprüft: die Ansicht im Browser (Maße, Lesbarkeit, Farben über dem Luftbild, Tasten, Doppelklick, Download). In der Rauchprobe sind alle Bildpunkte ein einziges Segment (Canvas-Attrappe), echte Segmentgrenzen kommen darin nicht vor.
Technische Entscheidungen:
- Die feste Höhe der unteren Leiste ist 52 px, einzeilig mit waagrechtem Rollen, falls ein Fenster zu schmal ist. Die Kategorienliste rechts lässt sich nur über „Liste rechts“ ein- und ausblenden; nur dieser Schalter ändert die Bildgröße, mit Absicht.
- Die Fassungsbeschreibung steht einzeilig mit Tooltip, damit der Kopf beim Fassungswechsel nicht höher wird.
- Die Abwahl per Klick ins Leere wirkt nur auf das Bild-Canvas neben dem Luftbild. Klicks in Leisten wählen nicht ab.
- Neue Farbe `kommentar` und geänderte Werte (`abgedunkelt`, `deckkraft` 0,4) stehen in `einstellungen/seite.json`.
- Python-Seite unverändert (die Daten reichen). Der Commit wurde per amend ergänzt, es bleibt ein Commit.
Nacharbeit im Hauptordner: Im Profil `landseg.md` (Routinen) steht noch `seite … [--nachher <ordner>]`. Das gilt nicht mehr: dort jetzt `[--einstellungen <datei mit fassungen>]`
Abräumen: offen (Auftrag nachbessern; Arbeitskopie und Branch bleiben bis zum Einreihen)
Lagebild: fehlt (Repo hat kein Lagebild)
Erkenntnisse fürs Profil:
- `seite` hat kein `--nachher` mehr. Die Fassungen kommen aus `einstellungen/seite.json` (`fassungen`), eine andere Liste über `--einstellungen`.
- Die Seite lässt sich ohne Browser in Node mit DOM- und Canvas-Attrappen prüfen. Ob das Bild springt, zeigt die Probe, die Änderungen außerhalb der linken Leiste zählt.
- Die Klassenzahl einer Ebene ist nicht „Klassen mit diesem level“: Blätter gröberer Ebenen zählen mit (7/25/43).
Abweichungen vom Zielbild: keine

## Dritte Durchsicht (Nachtest N1, N4, N5)
Commit: nach amend siehe `git log -1` auf wunsch/landseg-werkzeuge-5 (Nachricht unverändert)
N1 behoben: Der Knopf „Hervorhebung aufheben“ steht immer oben in der Kategorienliste und ist ausgegraut, solange nichts hervorgehoben ist. Die Einträge verrutschen nicht mehr.
N4 behoben: Die Fassung schaltet nur noch mit Umschalt + Kennung (Tooltip und Legende sagen es) und nie, solange ein Eingabefeld den Fokus hat. Nach dem Anklicken eines Segments bekommt das Kommentarfeld gleich den Fokus. Esc im leeren Kommentarfeld hebt die Wahl auf, mit Text im Feld tut Esc nichts.
N5 behoben: „1 Kommentar exportiert (Datei kommentare-T0.json, meist im Ordner Downloads).“, ab 2 „Kommentare“.
Sonst nichts geändert, Vorstufe nicht neu gerechnet. Beide Seiten sind neu gebaut.
Prüfungen: tests.test_seite → OK; pruefe_kategorien → ok; node --check → ok. Node-Probe T0.html: alle Handlungen ruhig, CSS feste Spuren, Fehler 0. T0-probe.html: eine Taste ohne Umschalt lässt die Adresse unverändert, Umschalt + P wechselt mit gewählter Stelle, Fehler 0 (`rauch-T0.txt`, `rauch-probe.txt`). Aufruf-Budget überschritten (rund 58 von 50), weil drei Nachbesserungen im selben Lauf kamen.
Nicht geprüft: Fokus und Tasten im echten Browser.
Einreihen (Skript): eingereiht 0cd61ea feat: add seite tool for the single-file overview page with versions in C:/Users/Phil/Developement/Victor/landseg (main); Prüfung nach Risiko (ohne Prüfschleuse, keine Zeile schnell: im Profil); voll grün (3 s); volle Prüfung offen (vermerkt in C:/Users/Phil/Developement/Victor/landseg/.git/wunsch-einreihen/pruefung-offen.jsonl); Abräumen WEG; Waisen 1 (testrest 1), 962 MB anderswo (aufraeumer.py melden; beenden nur mit Freigabe des Nutzers)
