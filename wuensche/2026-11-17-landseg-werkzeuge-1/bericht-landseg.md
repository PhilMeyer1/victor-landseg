# Bericht landseg
Status: eingereiht
Für den Nutzer: Im Repo landseg gibt es jetzt das Python-Paket `landseg` mit den ersten drei
  Werkzeugen. `kacheln` schneidet einen Ausschnitt aus dem Luftbild und zerlegt ihn in Teilkacheln
  mit Rand und Lageangabe. `eingriff` bearbeitet die Segmentkarte: zusammenlegen, teilen, Grenze
  verschieben, Klasse setzen, Fläche zuweisen. Dabei kann nie eine Lücke entstehen. `pruefen` meldet
  Lücken, zerrissene Segmente und ungültige Klassen. Am echten Testfenster T0 habe ich nur das
  Zerschneiden geprüft (Kern 500 und 250). Die Bilder dazu liegen im Scratchpad, nicht unter
  `daten/landseg/`, denn außerhalb von Arbeitskopie und Berichtsordner durfte ich nichts schreiben.
  Die Bearbeitung ist mit künstlichen Karten getestet; echte Segmentkarten liefert erst Teil 2
  (Vorstufe). Sichtbar ändert sich nur die `README.md`, eine Oberfläche gibt es noch nicht.
Commit: e805308 "feat: add landseg package with kacheln, eingriff and pruefen tools"
Abnahmekriterien:
AK1: erfüllt. `python -m landseg kacheln` auf T0 (5236-56, x 2000, y 2400, 1000 × 1000) ergibt mit `--kern 500 --rand 64` 4 Teilkacheln (je 628 × 628) und mit `--kern 250` 16 Teilkacheln (je 378 × 378). Die Kernflächen ergeben zusammen 1000000 = 1000 × 1000, jeder Bildpunkt liegt in genau einem Kern. Das Manifest nennt alle Pfade relativ und die Lage E 69150,0–69350,0 / N 353320,0–353520,0, EPSG 31255; das stimmt mit dem Ermittlungsbericht überein. Beleg: `wuensche/2026-11-17-landseg-werkzeuge-1/beleg-ak1-landseg.txt`. Teilkachel r1c0 habe ich angesehen, sie zeigt Wiese, Wald und Gärten. Dazu 7 Tests in `tests/test_kacheln.py`.
AK2: erfüllt. 26 Tests in `tests/test_eingriff.py` und `tests/test_pruefen.py` mit künstlichen Karten. Geprüft sind alle fünf Eingriffe, die Gegenproben (nicht benachbart, Linie trennt nicht, Segment zerfiele, Klasse ungültig) ohne jede Änderung und eine Zufallsfolge von 150 Eingriffen, nach jedem Schritt mit `pruefen` ok. Die Gegenproben für `pruefen` schlagen fehl, wie sie sollen: Lücke, trennende Lücke, nur über eine Ecke verbunden, Klasse, grob, fehlender Eintrag, Eintrag ohne Bildpunkte, doppelte ID, Form. Zusätzlich lief die ganze Befehlsfolge über die Befehlszeile mit der echten `kategorien.json` (628 × 628): alle Eingriffe Exit 0 und „ok“, die eingefügte Lücke Exit 1 mit „Lücke: 1 Bildpunkte“. Beleg: `wuensche/2026-11-17-landseg-werkzeuge-1/beleg-ak2-landseg.txt`
Prüfungen:
`PY -B -m unittest discover -s tests -t .` (in W) → 38 Tests, OK, 0,85 s
`PY -I tools/pruefe_kategorien.py kategorien.json` (schnelle Stufe des Profils) → ok
`sha256sum` des Originals 5236-56.tif nach den Läufen → 28b3c1e6…e8, gleich wie in `daten/README.md` (Original unverändert)
Volle Stufe: keine im Profil (`pruefung: leicht`)
Ausgaben der T0-Läufe: `C:/Users/Phil/AppData/Local/Temp/claude/27e54e3b8399faf6/a2bf01d3-627c-4b06-8b57-51f25ab5229e/scratchpad/t0-kern500/` und `C:/Users/Phil/AppData/Local/Temp/claude/27e54e3b8399faf6/a2bf01d3-627c-4b06-8b57-51f25ab5229e/scratchpad/t0-kern250/` (nur vorübergehend)
Nicht geprüft: Der Befehl aus der README mit Pfaden `../daten/...` lief nicht vom Hauptordner aus, nur mit absoluten Pfaden aus der Arbeitskopie. Eingriffe auf einer echten Segmentkarte gab es nicht, die liefert erst Teil 2. Eine Lücke, die schon in der Eingabe steckt, lehnt `eingriff` ab, statt sie zu füllen.
Einstieg: stimmte (Repo nur mit Kategorienliste; Stitcher-Code habe ich nicht gebraucht, das Werkzeug ist neu gebaut)
Technische Entscheidungen:
- Die Label-Karte wird als einkanaliges uint32-TIFF (zlib) über tifffile gespeichert, nicht als PNG, weil PNG nur bis 16 Bit reicht. `.npy` lässt sich ebenfalls lesen und schreiben.
- Die Tests laufen mit `unittest` aus der Standardbibliothek, weil das Stitcher-venv kein pytest hat. So braucht es kein eigenes `.venv`. Aufruf: `python -B -m unittest discover -s tests -t .` im Repo-Ordner.
- Zusammenhang zählt über gemeinsame Kanten (4er-Nachbarschaft), in `pruefen` und in `eingriff` gleich. Linien werden 8-verbunden gezeichnet, damit sie solche Gebiete sicher trennen. Bildpunkte auf der Linie wachsen schrittweise dem angrenzenden Teil zu.
- Jeder Eingriff wirkt ganz oder gar nicht. `stapel` führt mehrere Schritte als Einheit aus. Nach dem Schreiben läuft `pruefen` von selbst.
- `polygon_zuweisen` gibt Nachbarn, die dabei zerfallen, eigene IDs mit gleicher Klasse. `grenze_verschieben` lehnt einen solchen Zerfall dagegen ab, und `verschmelzen` lehnt nicht benachbarte Segmente ab.
- Der Kontextrand kommt aus dem Originalbild auch über den Ausschnitt hinaus und endet nur am Bildrand. Neben jedem PNG liegt eine `.pgw`-Weltdatei. Liegen Quelle und Ziel auf verschiedenen Laufwerken, bricht `kacheln` ab, weil dann kein relativer Pfad möglich ist.
- Die Mindestfläche prüft `pruefen` nur auf Wunsch (`--mindestflaeche`), denn laut Entscheidung F1 gilt „so fein wie sicher erkennbar“.
- `.gitignore` angelegt, nur mit `__pycache__/`, `*.pyc` und `.venv/`; `.claude/` habe ich nicht aufgenommen.
- Kurze Läufe (16 Teilkacheln in Sekunden) laufen seriell, Nebenläufigkeit bringt dort nichts.
Nacharbeit im Hauptordner: Profil `landseg` um den Abschnitt „Testreihen“ ergänzen (Befehl im Repo-Ordner: `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -B -m unittest discover -s tests -t .`, unter 2 s; derselbe Befehl taugt als schnelle Stufe), auf `pruefung: voll` umstellen und ein Lagebild anlegen (Profil-Pflege laut Mutterwunsch)
Abräumen: nicht nötig (Auftrag umsetzen); W bleibt für das Einreihen stehen
Lagebild: fehlt (kein Lagebild im Repo, keine Kopfzeile `lagebild:`; Anlage gehört laut Mutterwunsch zur Profil-Pflege)
Erkenntnisse fürs Profil:
- Im Stitcher-venv fehlt pytest, die Tests laufen mit `unittest`. `python -m landseg` und `-m unittest` finden das Paket nur ohne `-I` und mit dem Repo-Ordner als Arbeitsordner.
- Das Orthofoto 5236-56.tif ist unkomprimiert und nicht gekachelt (5000 × 6250 × 3, uint8), `tifffile.memmap` liest es direkt. Seine TFW-Werte beziehen sich auf die Mitte des Bildpunkts oben links.
- Ein Hilfsskript außerhalb des Repos findet das Paket `landseg` nur mit `PYTHONPATH=<repo>`.
Abweichungen vom Zielbild: keine
Einreihen (Skript): eingereiht e805308 feat: add landseg package with kacheln, eingriff and pruefen tools in C:/Users/Phil/Developement/Victor/landseg (main); Prüfung nach Risiko (ohne Prüfschleuse, keine Zeile schnell: im Profil); entfällt (pruefung: leicht im Profil, keine Testreihen); Abräumen WEG; Waisen 6 (server 5, logwaechter 1), 367 MB anderswo (aufraeumer.py melden; beenden nur mit Freigabe des Nutzers)
