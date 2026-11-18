# Bericht landseg
Status: eingereiht
Für den Nutzer: Der historische Ausschnitt H0 aus dem Scan von 1968 ist für die Agents vorbereitet. Er ist wie T0 in vier
  Teilkacheln geschnitten, die Vorsegmentierung ist für alle vier fertig und geprüft, B und C haben bildgleiche Kopien.
  Für jeden Agent liegen Auftrag und Bilder bereit: der ganze Ausschnitt mit Gitter, die ganze Teilkachel mit Nummern und je
  Viertel 14 Ansichten. Wichtig: Mit den Einstellungen von T0 hat die Vorsegmentierung im Dorf ganze Häuserzeilen zu einem
  Stück verschmolzen (bis zu 72 000 Bildpunkte, ein Drittel des Kerns). Ich habe deshalb für H0 zwei Einstellungen geändert:
  SAM 3 sieht das Bild in kleineren Fenstern, also vergrößert, und nimmt auch schwächere Funde an. Jetzt ist jeder Streckhof
  einzeln getrennt (Vorschau `vorschau/h0_vorstufe_grenzen.jpg`). Die Kehrseite: H0 hat 1.366 Segmente statt erwarteter
  200–300 (T0: 641). Ein Agent hat damit bis zu 518 Segmente (r1c1) in vier Vierteln mit 67 bis 173 Segmenten. Die
  Klassenvorschläge der Vorsegmentierung taugen auf Schwarz-Weiß kaum: 96 % sind „unsicher“, Äcker stehen teils als
  Gebäude da. Das klären erst die Urteile in Teil 3. Die Originalscans sind unverändert. Ungeprüft ist noch kein Urteil.
Commit: keiner (Ergebnis: ohne Commit)
Nachweis: Datenlauf ohne Commit, Daten unter `C:/Users/Phil/Developement/Victor/daten/landseg/H0/` (136 MB), Berichtsordner
  `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-2/` (3,8 MB).
  (1) Kacheln: `skripte/schritte_h0.sh kacheln` → rc 0, 4 Teilkacheln 628 × 628 (`kacheln-H0.log`), `georeferenz: null`,
  keine `.pgw`, `kanaele: 1`. Mit dem neuen main e15205a (Teil 1 eingereiht) frisch nachgekachelt: Bilder bytegleich,
  Manifest gleich ohne `erstellt`/`quelle.bild`.
  (2) Vorstufe: Lauf 1 mit Repo-Einstellungen (nur `siedlung.bildpunkt_m` 0,45) zeigte verschmolzene Häuserblöcke
  (`vorschau/lauf1_grenzen.jpg`, `statistik-vorstufe-lauf1.json`). Endstand mit `vorstufe-h0.json` (Abdruck `35dd113d2c30`),
  Logs `vorstufe-H0-probe2-r0c1.log` und `vorstufe-H0-lauf2.log`.
  (3) `pruefen` 12/12 ok (Vorstufe 4, Kopien B und C je 4; `pruefen-H0.log`, `pruefen-kopien-H0.log`).
  (4) Kopien: `b-kategorien-frei/<tk>/` und `c-feste-liste/<tk>/` mit `labels.tif`, `segmente.json`, `kandidaten.json`,
  bytegleich zur Vorstufe (in `pruefe_h0.py` nachgerechnet). `sam3_roh.npz` wurde nicht kopiert.
  (5) Aufträge und Bilder: `skripte/baue_auftraege_h0.py` → rc 0, 24 s (`auftraege-bau.log`). Plan samt Workflow-Einheiten
  `auftraege.json`. 42 Aufträge unter `auftraege/`: C 16 Viertel, B 16 Viertel, A 4 Teilkacheln, Gegenprobe 4 Viertel (C, r0c0),
  Vereinheitlichung B 1, alternative Gegenprobe A 1.
  (6) Unabhängige Prüfung `skripte/pruefe_h0.py` → ok (`pruefung-auftraege.log`).
Messung AK2 (Messzeilen der Vorstufe, Endstand):
  r0c0 492 Segmente, davon 341 im Kern, sicher: nein 95,5 % (Fläche 96,8 %) · r0c1 599 / 422, 97,2 % (96,8 %) · r1c0 118 / 85,
  100 % (100 %) · r1c1 695 / 518, 96,1 % (90,7 %); zusammen 1.366 Kernsegmente, keines in zwei Teilkacheln.
  Je Viertel (v1–v4): r0c0 114/139/33/55 · r0c1 107/103/105/107 · r1c0 29/37/14/5 · r1c1 131/147/67/173.
  Über eine Viertelgrenze reichen 33/55/16/55 Segmente.
  Lauf 1 (Fenster 1008, Schwelle 0,4): 173/92/38/162 = 465 Kernsegmente. Größtes Gebäudesegment im Kern 72 078 px (r0c1),
  58 023 px (r1c1). Endstand: größtes Gebäudesegment 6 354 px (r0c1) bzw. 2 889 px (r1c1). In r0c0 bleiben drei große Flächen
  um 14 000 px, die die Vorstufe als Gebäude führt; es sind Äcker (`vorschau/h0_vorstufe_klassen.jpg`).
  Entscheidung zur Kerngröße: Kern 500 bleibt. Drei Teilkacheln liegen weit über 80 Kernsegmenten. Neu kacheln mit `--kern 250`
  hieße aber 16 Teilkacheln mit je einem Agent. Das widerspricht der Entscheidung „ein Agent je Teilkachel, je Fassung 4“
  (2026-11-17), und an der Gesamtzahl änderte es nichts. Die Arbeitseinheit bleibt das Viertel (250 × 250). Wie bei T0 arbeitet
  ein Agent seine vier Viertel-Aufträge nacheinander ab. Über 80 Segmente haben 9 von 16 Vierteln (bis 173 in r1c1 v4).
  Der Vergleich mit `landseg-methode` (erwartet 200–300 Segmente) folgt in Teil 4.
Abnahmekriterien: AK2: erfüllt — gekachelt 1000 × 1000 mit 4 Teilkacheln (`kacheln-H0.log`, Manifest). Vorstufe für alle vier
  (`vorstufe-H0-lauf2.log`, `vorstufe-H0-probe2-r0c1.log`; GPU über `maschine.py` belegt und freigegeben, 9,3 Maschinenminuten in
  5 Läufen). `pruefen` 12 × ok. Segmentzahl je Teilkachel gemessen und Entscheidung zur Kerngröße getroffen (oben). Originale
  byteweise unverändert: SHA-256 vorher/nachher gleich (`hash-vorher.json`, `hash-nachher.json`; 1968
  `79f3e033…04d5d9`, 1957 `0e09cfd4…af96f8`, Größe und mtime gleich).
Prüfungen: `bash skripte/schritte_h0.sh pruefen` → 4 × ok; `… pruefen-kopien` → 8 × ok.
  `PY -I skripte/pruefe_h0.py` → ok. Geprüft: `im_kern` passt zur Karte; jedes Kernsegment in genau einem Viertel und dort mit dem
  größten Anteil (nachgerechnet); `--ids` jedes Auftrags gleich seiner Liste; je Viertel 14 JPEG und `viertel.json`; Gesamtbilder je
  Teilkachel; `ansicht` für A; alle Ergebnisordner leer; kein Platzhalter übrig; jeder genannte H0-Pfad vorhanden; SW-Abschnitt in
  jedem Auftrag; Einheiten C 16, B 16, A 4, Gegenprobe 4. Probe `pruefe_urteil.py`: gültig → 0, Segment fehlt → 1, ohne Übersicht → 1.
  Erster Prüflauf fand zwei echte Fehler im Auftragsbau, beide behoben (Pfad `{{DATEN}}/manifest.json` zeigte in den Fassungsordner;
  „T0“ im SW-Text).
  Bilder selbst angesehen: `vorschau/h0_umgebung.jpg` (Fenster stimmt mit F2 überein: Streifenflur, schräge Straße, Ortsrand mit
  Streckhöfen), `vorschau/lauf1_grenzen.jpg`, `vorschau/probe2_r0c1_kern.jpg`, `vorschau/h0_vorstufe_klassen.jpg`,
  `daten/landseg/H0/viertel/r0c1/v1/uebersicht_nummern.jpg`, `daten/landseg/H0/ganz/r1c1/ganz_nummern.jpg`. Nummern lesbar,
  Viertelrahmen und Kern richtig.
  `git -C landseg status` → sauber (HEAD e15205a). `git -C stitcher status` → nur `?? entwurf.css` (alt, nicht aus diesem Lauf).
  Aufrufe: etwa 85 von 120.
Nicht geprüft: Ob ein Agent 341 bis 518 Segmente (Viertel bis 173) in einem Durchgang schafft, zeigt erst Teil 3. Bei T0 lag die
  Spitze bei 301 je Teilkachel und 112 je Viertel. Die SW-Spalte von `kategorien.json` ist nicht berührt. Die Seite mit H0 ist
  nicht erzeugt (Teil 4).
Einstieg: stimmte. Abweichung: `vorstufe.py` wandelt Graustufen schon in RGB (`lese_bild`), `kacheln` schreibt sie einkanalig. Auch
  der neue main e15205a schreibt gleich. `Ansicht` verlangt RGB: der Auftragsbau wandelt beim Lesen.
Technische Entscheidungen:
  - Ablage nach `einstellungen/seite.json` (Teil 1 nennt `H0/manifest.json` unter `bilder`): `daten/landseg/H0/manifest.json`,
    `H0.png`, `teilkacheln/`, `vorstufe/<tk>/`. Fassungsordner `a-alles-frei/` (A, Abgabe unter `abgabe/<tk>/`, Ansicht unter
    `ansicht/<tk>/`), `b-kategorien-frei/` (Urteile `urteil/<tk>/v<n>/`, `vereinheitlichung/`), `c-feste-liste/` (Urteile
    `urteil/<tk>/v<n>/`, Gegenprobe `urteil-gegenprobe/r0c0/v<n>/`). Das entspricht dem Aufbau von `ergebnisse/` im Gesamtprojekt.
  - Fassungen in neuer Benennung: C „Feste Kategorienliste“ = früheres T0-A (Viertel-Urteile mit `kategorien.json`), B wie bei T0,
    A „Alles frei“ = früheres T0-C (freie Abgabe je Teilkachel). `pruefe_urteil.py` hat dazu `--fassung c|b` (c = feste Liste).
  - Gegenprobe: Standard ist Fassung C auf r0c0 (Einheiten `art: z`). So war es bei T0 (feste Liste, r0c0), und die PQ-Zahl bleibt
    mit T0 vergleichbar. r0c0 hat Ortsrand und Flur mit 341 Segmenten; r1c0 (85, nur Acker) wäre ein zu leichtes Maß. Im
    Mutterwunsch steht „Gegenprobe … von A“. In neuer Benennung hieße das die freie Abgabe. Dafür liegt
    `auftraege/gegenprobe/a/r0c0/auftrag.md` bereit (`gegenprobe_a_alternative` in `auftraege.json`). Die Hauptsession wählt eine
    von beiden.
  - Viertelbilder liegen einmal unter `daten/landseg/H0/viertel/<tk>/v<n>/`, B und C lesen dieselben. Die Vorstufe ist
    bildpunktgleich; bei T0 lagen bytegleiche Kopien doppelt vor. Gesamtbilder je Teilkachel (`ganz/<tk>/ganz_nummern.jpg`,
    `ganz_roh.jpg`, `ganz.json`) und das Gitterbild `ganz/H0_raster.jpg` sind vorab gezeichnet. Der Workflow braucht dafür keinen
    eigenen Agent wie bei T0. Große Bilder liegen nicht im Berichtsordner, weil `wuensche/` versioniert ist. Dort liegen nur
    Aufträge, Plan und kleine Vorschauen.
  - Vorstufen-Einstellungen nur als Kopie `vorstufe-h0.json` im Berichtsordner, nicht im Repo. Gegenüber `vorstufe.json`:
    `siedlung.bildpunkt_m` 0,2 → 0,45 (Scan ohne Lage, Schätzung aus F1; XResolution des TIFF entspricht 15 µm Scan),
    `sam3.fenster_px` 1008 → 420 (Schiebefenster 2 × 2, SAM 3 sieht den Scan 2,4fach statt 1,6fach) und `sam3.instanz_schwelle`
    0,4 → 0,2. Fenster allein (Probe 1) hob die Hausfunde in r0c1 nur von 20 auf 66; das größte Gebäudesegment hatte noch 59 055 px.
    Erst mit beiden Änderungen sind die Häuser getrennt. GPU-Zeit je Teilkachel etwa 100 s statt 17 s.
  - Jeder Auftrag hat einen Abschnitt „Schwarz-Weiß-Scan“: Urteil nach Grauton, Textur, Form; SW-Spalte nur Vermutung; bei
    Unsicherheit Elternklasse, `sicher: false` und unter `offen` nennen; Hinweis auf gerade Grenzen aus dem Schiebefenster. Dazu
    „Zuerst der ganze Ausschnitt, dann die Teilkachel“ (Entscheidung 2026-11-17). Regeln für B nennen L4–L13.
  - Zwei GPU-Läufe für die drei übrigen Teilkacheln (r0c0+r1c1, dann r1c0), damit kein Lauf über 5 min dauert.
Nacharbeit im Hauptordner: keine aus diesem Teil. Für Teil 3: Das Workflow-Skript liest
  `C:/Users/Phil/Developement/Victor/wuensche/2026-11-18-landseg-historisch-2/auftraege.json`. Feld `einheiten` hat das Format von
  T0 (`art` c|b|a|z, `tk`, `v`, `n`, `auftrag`, `ergebnis`). Dazu kommen `vereinheitlichung_b.auftrag`, `ganz_teilkachel`,
  `ganz_raster` und `manifest`. Bei `art` heißt `a` jetzt „Alles frei“ (frei, je Teilkachel) und `c` „Feste Liste“ (Viertel). Das
  ist gegenüber dem T0-Skript vertauscht. Die Gesamtbilder liegen schon vor.
Abräumen: WEG (keine Arbeitskopie angelegt); keine Dauerprozesse gestartet. GPU freigegeben. Scratchpad-Kopie `h0-frisch` gelöscht.
Lagebild: fehlt (landseg hat kein `LAGEBILD.md`; der Datenlauf ändert keinen Code).
Erkenntnisse fürs Profil:
  - SAM 3 auf dem SW-Scan 1968 (rund 0,45 m je Bildpunkt): Mit `vorstufe.json` (Fenster 1008, Instanzschwelle 0,4) verschmilzt
    die Vorstufe Streckhof-Zeilen zu einem Segment. `sam3.fenster_px` 420 plus `sam3.instanz_schwelle` 0,2 trennt die Häuser.
    Dann gibt es etwa dreimal so viele Segmente, rund 100 s GPU je Teilkachel, und über 95 % sind „sicher: nein“. Einstellungen
    als Kopie über `vorstufe --konfig` (vollständige Datei, kein Teilüberschreiben).
  - Bilder ohne Georeferenz: Die Vorstufe nimmt `siedlung.bildpunkt_m` (Standard 0,2 m) für den Siedlungspuffer; bei Scans auf die
    echte Bildpunktgröße setzen.
  - `vorlagen/urteil.md` setzt `{{DATEN}}/manifest.json` und `{{DATEN}}/{{LABELS}}` zusammen. Bei der Ablage nach `seite.json` ist
    `DATEN` der Ordner des Manifests und `LABELS` `<fassungsordner>/<tk>/labels.tif`.
  - Das kleinere SAM-3-Fenster zieht gerade Grenzen bei x/y 208 und 420 der Teilkachel durch gleichförmige Äcker (Fensterkanten).
  - Bash-Befehle mit dem absoluten Pfad `C:/Users/Phil/Developement/Victor/daten/landseg/H0` blockte der Geheimnisschutz-Hook in
    diesem Lauf nicht.
Abweichungen vom Zielbild: keine
Einreihen (Skript): eingereiht ohne Commit — Nachweis: Datenlauf ohne Commit, Daten unter `C:/Users/Phil/Developement/Victor/daten/landseg/H0/` (136 MB), Berichtsordner; Abräumen WEG (keine Arbeitskopie)
