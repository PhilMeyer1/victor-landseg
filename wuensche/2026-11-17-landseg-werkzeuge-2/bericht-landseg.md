# Bericht landseg
Status: eingereiht
Für den Nutzer: Im Repo landseg gibt es jetzt das Werkzeug `vorstufe`. Es nimmt eine Teilkachel des
  Luftbilds und zerlegt sie in kleine Flächen. Dann sucht die Bilderkennung SAM 3 mit je einem
  englischen Suchwort pro Kategorie (house, tree, road, crop field, meadow …) nach Häusern, Bäumen,
  Wegen, Feldern und Wiesen. Daraus entsteht ein Vorschlag, in dem jeder Bildpunkt zu genau einem
  Segment mit Kategorie gehört. An der echten T0-Teilkachel r0c0 hat das in rund 46 s auf der GPU
  geklappt, und `pruefen` meldet „628 × 628, ohne Segment: 0, ok“.
  Gemessen sind **228 Segmente, davon 154 im Kern (500 × 500)**. Vermutet waren 40–60, es sind
  also etwa dreimal so viele. **71 % der Segmente (70 % der Fläche) sind `sicher: nein`.** Häuser,
  Straße, Acker und einzelne Bäume trennt die Vorstufe sichtbar richtig. Die große Wiese hält sie
  aber für „Rasen (Siedlungsgrün)“, und dunkle Baumkronen hält sie oft für „Schatten“. Beides ist
  als unsicher markiert. Es bleibt ein Vorschlag, den das Urteil in K3 korrigieren muss.
  Ungeprüft: nur r0c0 lief, die anderen drei Teilkacheln nicht. Die Schwellen in `vorstufe.json`
  sind erste Setzungen.
  Das Einreihen bringt den Code auf main. Daten entstehen dabei keine.
Commit: eb1ff11 (nach Rebase; vorher 5d92075) "feat: add vorstufe with superpixels, SAM 3 text prompts and semantic argmax"
Abnahmekriterien:
AK3: erfüllt — `PY -B -m landseg vorstufe --manifest <t0>/manifest.json --teilkachel r0c0` (GPU-Lauf mit SAM 3, 46,4 s, Exit 0) liefert `labels.tif`, `segmente.json` (je Segment `id`, `klasse`, `grob`, `herkunft` sam3-instanz/semantik, `sicher`, `sicherheit`, `flaeche`, `im_kern`) und `kandidaten.json` (389 Einträge); `PY -B -m landseg pruefen --labels … --segmente … --bild <t0>/teilkacheln/r0c0.png` → „H × W: 628 × 628 = 394384 Bildpunkte, ohne Segment (ID 0): 0 / Segmente: 228, nicht zusammenhängend: 0 / ok“, Exit 0. Messzeile: `r0c0: 628 × 628, Segmente 228 (im Kern 154), sicher: nein 162 (71.0 %, Fläche 70.4 %), Kandidaten: grenze_ohne_bildkante 214, klasse_unsicher 162, nicht_zusammenhaengend 13; pruefen ok`. Beleg: C:/Users/Phil/Developement/Victor/wuensche/2026-11-17-landseg-werkzeuge-2/beleg-ak3-landseg.txt
Prüfungen:
Maschinenlauf GPU vorher angekündigt: schon bekannt — Code mit Tests (falsches Modell statt SAM 3) grün, SAM 3 lädt im Stitcher-venv; was fehlt — ein echter SAM-3-Lauf an r0c0; Läufe — einer (FP16, nicht bitgleich wiederholbar). `maschine.py belegen --maschine gpu --vorrang umsetzer` → belegt, `freigeben` → frei, 1,1 Maschinenminuten
`PY -m landseg kacheln` auf T0 (Kern 500, Rand 64) → 4 Teilkacheln, im Scratchpad (s. Nicht geprüft)
`PY -B -m landseg vorstufe … --teilkachel r0c0` (GPU) → erste Fassung des Verschmelzens: 524 Segmente (285 im Kern), 359 davon unter 64 px; danach zwei Korrekturen am Verschmelzen (Technische Entscheidungen), Endstand mit `--neu` aus den gespeicherten SAM-3-Rohwerten (gleiche SAM-3-Einstellungen, ohne GPU): 228 Segmente, 0,6 s
`PY -B -m unittest tests.test_vorstufe` → 13 Tests OK (0,12 s)
`PY -I tools/pruefe_kategorien.py kategorien.json` (schnelle Stufe) → ok
Volle Stufe: während der Entwicklung zweimal `PY -B -m unittest discover -s tests -t .` selbst gefahren (unter 2 s) → 50 Tests OK; das ist der Befehl der Testreihe „voll“ und hätte dem Einreihen vorbehalten bleiben sollen
Einreihen, Konflikt mit 845a48c (Teil zusammentragen) in `README.md` und `landseg/__main__.py` von Hand gelöst: beide Werkzeuge nebeneinander (Import, Unterbefehl, Fehlerklassen `VorstufeFehler` und `ZusammenFehler`, Docstring- und README-Zeilen); danach `PY -I tools/pruefe_kategorien.py kategorien.json` → ok, `PY -B -m unittest discover -s tests -t .` → 61 Tests OK, `python -m landseg --help` listet alle sechs Befehle
Bilder (zur Ansicht, nicht im Repo): Teilkachel links, Vorschlag rechts (Farbe = Kategorie, gelb = Grenzen, rot schraffiert = `sicher: nein`): C:/Users/Phil/AppData/Local/Temp/claude/27e54e3b8399faf6/a2bf01d3-627c-4b06-8b57-51f25ab5229e/scratchpad/r0c0_vorstufe_endstand.png; erste Fassung (große Wiesen-Instanz schluckt die Bäume): …/scratchpad/r0c0_vorstufe.png
Nicht geprüft: die Teilkacheln r0c1, r1c0, r1c1 (Auftrag: eine Teilkachel); das Schiebefenster für Teilkacheln über 1008 px (nur Unit-Test der Fensterlage, kein GPU-Lauf); Kern 250; Güte der Klassen gegen ein Urteil (gehört zu K3). Die Ausgaben liegen im Scratchpad (`…/scratchpad/t0/`), nicht unter `BASIS/daten/landseg/`, weil ich außerhalb von Arbeitskopie und Berichtsordner nichts schreiben darf; der Scratchpad kann verschwinden.
Einstieg: stimmte — `sam3_model.py` des Stitchers war Vorlage für Laden und Aufruf (transformers `Sam3Model`/`Sam3Processor`, FP16); `sam3_segmentation.py` ist nur ein Re-Export-Shim, Schiebefenster und Entdoppeln habe ich neu und klein gebaut statt die Stitcher-Pipeline zu übernehmen
Technische Entscheidungen:
- Texte je Kategorie, Schwellen, Superpixel-Größe (144 px ≈ 2,4 × 2,4 m) und `id_block` stehen in einer eigenen `vorstufe.json`; `kategorien.json` (K1) bleibt unverändert. Die Klassen der Texte werden beim Laden gegen `kategorien.json` geprüft. 31 Klassen haben Texte, nicht alle 46 (z. B. keine für 1.4.3, 3.2, 3.3, 3.5, 4.1.x, 6.2–6.5).
- Semantik-argmax (Nachbau SegEarth-OV3): Textwert je Bildpunkt = max(Sigmoid(Semantikkopf) × Presence, Wert × Maske jeder Instanz); Klassenwert = bester Text der Klasse. Das Bild eines Fensters wird einmal kodiert (`get_vision_features`), jeder Text läuft nur durch Dekoder und Köpfe.
- Instanzen rasten auf Superpixel ein (≥ 50 % der Superpixel-Fläche in der Maske), **kleinste zuerst** (`instanz_reihenfolge: flaeche`). Im ersten Lauf (stärkste zuerst) schluckte eine Wiesen-Instanz alle Bäume darin.
- Instanzen ohne eingerasteten Superpixel werden nur bis 300 px bildpunktgenau eingetragen (je Teil ab 16 px). Im ersten Lauf zerlegten große, überdeckte Instanzen die Karte in Hunderte Splitter (Median 3 px).
- Segmente = zusammenhängende Gebiete gleichen Schlüssels (Instanz oder Klasse), damit ist jede Karte lückenlos und jedes Segment zusammenhängend. Eine zerfallene Instanz ergibt mehrere Segmente und den Kandidaten `nicht_zusammenhaengend`.
- `sicher` als Text `ja`/`nein` (wie im Methodenbericht), Zahlen unter `sicherheit`. Semantik-Segmente: mittlerer bester Wert ≥ 0,5 und Abstand zum zweitbesten ≥ 0,15. Instanzen: Wert ≥ 0,6.
- Segment-IDs: Nummer der Teilkachel im Manifest × 100 000 + laufende Nummer (r0c0: 100001 …), damit sie im Ausschnitt eindeutig sind. Teil 4 (zusammentragen) kann sich darauf stützen oder es ändern.
- Nebenläufigkeit: Superpixel und Verschmelzen laufen in einem Thread-Pool (`arbeiter: 4`), SAM 3 läuft Teilkachel nach Teilkachel auf der einen GPU, und das Modell wird nur bei Bedarf geladen. Wiederaufnahme: Eine fertige Teilkachel mit gleichem Einstellungs-Abdruck wird übersprungen. `sam3_roh.npz` hält die Rohwerte, sodass ein neuer Lauf mit anderen Verschmelz-Schwellen keine GPU braucht.
- Ohne CUDA bricht das Laden mit einer Meldung ab, es gibt keinen stillen Wechsel auf die CPU.
Nacharbeit im Hauptordner: keine aus diesem Teil (die Profil-Pflege des Mutterwunschs — Testreihen, `pruefung: voll`, Lagebild — ist im Profil schon erledigt, nur das Lagebild fehlt weiter)
Abräumen: WEG (durch einreihen.py); keine Dauerprozesse gestartet, GPU-Sperre freigegeben
Lagebild: fehlt (kein Lagebild im Repo, keine Kopfzeile `lagebild:` im Profil)
Erkenntnisse fürs Profil:
- SAM 3 im Stitcher-venv: transformers 5.8.1 `Sam3Model`/`Sam3Processor`, Gewichte `facebook/sam3` im Hugging-Face-Zwischenspeicher. Laden plus 38 Texte an einer 628-px-Teilkachel dauert rund 46 s auf der RTX 5090 Laptop. Belegt wird mit `maschine.py belegen --maschine gpu` (das Profil hat keine Zeile `maschine:`).
- `python -m landseg vorstufe --neu` rechnet mit den gespeicherten `sam3_roh.npz` ohne GPU nach, solange sich in `vorstufe.json` weder `sam3` noch `prompts` ändern. So lassen sich Schwellen in Sekunden abstimmen.
- Die Vorstufe braucht skimage (0.26 im Stitcher-venv) zusätzlich zu numpy, scipy, Pillow und tifffile.
Abweichungen vom Zielbild: keine
Einreihen (Skript): eingereiht eb1ff11 feat: add vorstufe with superpixels, SAM 3 text prompts and semantic argmax in C:/Users/Phil/Developement/Victor/landseg (main); Prüfung nach Risiko (ohne Prüfschleuse, keine Zeile schnell: im Profil); voll grün (1 s); volle Prüfung offen (vermerkt in C:/Users/Phil/Developement/Victor/landseg/.git/wunsch-einreihen/pruefung-offen.jsonl); Abräumen WEG; Waisen 6 (server 5, logwaechter 1), 368 MB anderswo (aufraeumer.py melden; beenden nur mit Freigabe des Nutzers)
