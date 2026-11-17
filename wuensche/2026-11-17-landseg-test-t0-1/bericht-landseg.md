# Bericht landseg
Status: eingereiht
Für den Nutzer: Das Testfenster T0 ist für die Agents vorbereitet. Die Kacheln und die automatische Vorsegmentierung von
  Fassung A sind bestätigt (unverändert, lückenlos). B und C haben bildgleiche Kopien. Jede der vier Teilkacheln ist jetzt in
  vier Viertel geteilt. Für jedes Viertel gibt es einen fertigen Auftrag mit einer Liste seiner Segmente und 14 Bildern: eine
  Übersicht mit Umgebung, eingezeichneten Grenzen und Nummern, dazu vier Nahansichten. Bilder einzelner Segmente gibt es nicht
  mehr. Die Gruppen und die rund 8.500 Einzelbilder aus dem ersten, gestoppten Lauf sind gelöscht. Bereit liegen
  32 Viertel-Aufträge (A und B), 4 freie Aufträge für C, 4 für den Zweitagenten (Teilkachel r0c0) und einer zum Vereinheitlichen
  der Klassen von B. Insgesamt sind es 641 Segmente je Fassung. Zwei Viertel unten in r1c1 sind sehr dicht: v3 hat 93, v4 hat
  112 Segmente, gerechnet waren etwa 40. Will man das entlasten, teilt man diese beiden Viertel in Teil 2 noch einmal (zwei
  Agents mehr je Fassung). Ungeprüft ist noch kein einziges Urteil, das kommt in Teil 2.
Nachweis: Datenlauf ohne Commit. (1) Kacheln: frisch nachgekachelt, bytegleich zu kern500 (`kacheln-T0.log`,
  `kopien-messung.json` „frisch“). (2) Vorstufe: alle 4 Teilkacheln „schon fertig mit denselben Einstellungen“ (`vorstufe-T0.log`).
  (3) `pruefen` 12/12 ok (A, B, C je 4; `pruefen-T0.log`). (4) Kopien B und C: 23 Dateien bytegleich zu A, nur `sam3_roh.npz`
  nicht kopiert (`kopien-messung.json`). (5) Viertel gebildet, Bilder und Aufträge geschrieben (`viertel-bau.log`, `gruppen.json`)
  und unabhängig geprüft (`viertel-pruefung.log` → ok). (6) Verworfen und gelöscht: `gruppen/` (64 Aufträge), `gruppen.json`,
  `zweitagent/auftrag.md` der Gruppen-Fassung, die Skripte `baue_gruppen.py` und `pruefe_gruppen.py`, 4.669 Einzelbilder unter
  `kern500/ansicht/` (265 MB) und 3.843 unter `fassung-b/ansicht/` (230 MB), dazu die leeren Ergebnisordner `urteil/<tk>/g<n>`,
  `urteil-zweit/r1c0` und `fassung-c/abgabe`.
Messung AK1 (Messzeilen aus `segmente.json` → `vorstufe`, Einstellungsabdruck `efd5251383c0`, SAM-3-Abdruck `70eb88e22347`):
  r0c0 206 Segmente, davon 141 im Kern, sicher: nein 66 % (Fläche 38 %) · r0c1 234 / 147, 62 % (48 %) · r1c0 86 / 52, 59 % (44 %)
  · r1c1 408 / 301, 79 % (74 %); zusammen 641 Kernsegmente. Kein Kernsegment zählt in zwei Teilkacheln.
  Je Viertel (v1 oben links, v2 oben rechts, v3 unten links, v4 unten rechts): r0c0 22/62/19/38 · r0c1 46/43/37/21 ·
  r1c0 21/9/14/8 · r1c1 44/52/93/112. Über eine Viertelgrenze reichen 18/21/11/37 Segmente.
  Entscheidung zu `--kern 250`: Es wird nicht neu gekachelt. Jede Teilkachel liegt über 80 Kernsegmenten, r1c0 ausgenommen. Die
  Entscheidung „Urteil im Verbund je Viertel“ macht aber das Viertel von 250 × 250 Bildpunkten zur Arbeitseinheit eines Agents.
  Das ist dieselbe Fläche wie bei `--kern 250`, nur bleiben Vorstufe, Kontextrand und Nähte bei Kern 500. Neu kacheln hieße 16
  neue Teilkacheln samt neuer Vorstufe und mehr Nähte, an der Segmentzahl je Agent änderte es nichts. Über etwa 80 liegen
  danach nur noch r1c1 v3 (93) und v4 (112).
  Die Abweichung von den 154 Kernsegmenten für r0c0 im Arbeitsauftrag erklärt die Messzeile: Die heutige Vorstufe trägt
  den Abdruck `efd5251383c0` (erstellt 16:58 UTC) und zählt 141.
Abnahmekriterien: AK1: erfüllt — Belege:
  `PY -B -m landseg kacheln … --ziel <scratchpad>/kacheln-frisch` → rc 0, alle Bilder und Weltdateien bytegleich.
  `PY -B -m landseg vorstufe --manifest ../daten/landseg/T0/kern500/manifest.json` → 4 × übersprungen, rc 0, 1 s; GPU per
  `maschine.py` belegt und freigegeben (0,0 min).
  `PY -B -m landseg pruefen` je Teilkachel → 12 × „H × W: 628 × 628, ohne Segment (ID 0): 0, nicht zusammenhängend: 0, ok“.
  `git -C landseg status` → nur `?? .claude/worktrees/` (fremde Arbeitskopie werkzeuge-5), HEAD 3b4e855.
  `git -C stitcher status` → nur `?? entwurf.css`, Dateizeit 12.11.2026, also nicht aus diesem Lauf.
  Original `…5236-56.tif`/`.TFW`/`.PRJ`: Dateizeit 17.11. 13:18, unverändert.
  Messzeilen und die Entscheidung zu `--kern 250` stehen oben.
Prüfungen: `PY -I skripte/pruefe_kopien.py` → B/C je 23 gleich, 0 anders. `PY -I skripte/baue_viertel.py` → rc 0, 32 Viertel, 4 C,
  4 Zweitagent, 1 Vereinheitlichung, 12 s. `PY -I skripte/pruefe_viertel.py` → ok. Geprüft wurde: jedes Kernsegment in genau einem
  Viertel und dort mit dem größten Anteil (nachgerechnet), kein Segment aus dem Kontextrand, jede ID in ihrem Auftrag, kein
  Platzhalter übrig, je Viertel 14 JPEG und `viertel.json`, die Bilder von B bytegleich zu A, alle Ergebnisordner leer, unter
  `daten/landseg/T0` kein Ordner `segmente/`. Probe mit `pruefe_urteil.py`: gültig → 0, ohne Übersicht → 1, Segment fehlt → 1.
  Bilder selbst angesehen: `kern500/viertel/r1c1/v4/uebersicht_nummern.jpg`, `r0c0/v2/nah3_nummern.jpg`,
  `r0c0/v2/uebersicht_gitter.jpg`. Nummern lesbar, Viertelrahmen und Gitter liegen richtig.
  Aufrufe: etwa 45 von 150.
Nicht geprüft: Ob die Agents mit rund 93 bis 112 Segmenten je Viertel (r1c1 v3/v4) zurechtkommen, zeigt erst Teil 2. Ebenso, ob
  die Bilder der Nachbarviertel reichen, wo Segmente über eine Viertelgrenze gehen (gezeigt werden 32 Bildpunkte Umgebung).
  Die Vorstufe wurde nicht neu gerechnet, sondern nur bestätigt, dass sie zu den Einstellungen passt.
Einstieg: stimmte. Abweichung: `ansicht` hat weder ein Fenster für ein Viertel noch eine ID-Beschriftung. Die Viertelbilder
  zeichnet deshalb `baue_viertel.py` mit der Klasse `landseg.ansicht.Ansicht` (`zeichnen(art, Fenster)`) und setzt Nummern und
  Rahmen selbst dazu.
Technische Entscheidungen:
  - `gruppen.json` und alle Aufträge liegen im Ordner dieses Teils, `wuensche/2026-11-17-landseg-test-t0-1/`. Den in den
    Workflow-Eingaben genannten Ordner `…-landseg-test-t0/` gibt es nicht. Alle Pfade in `gruppen.json` sind absolut.
    Schema `landseg-test-t0-viertel/1`, Felder `fassung`, `teilkachel`, `viertel` (1–4), `segmente`, `auftrag`, `ergebnis`,
    `bilder`, `bearbeiter`, `modell`, `effort`; dazu `vereinheitlichung_b`, `frei_c`, `zweitagent` und `messung`.
  - Die Viertelbilder liegen unter `daten/landseg/T0/<kern500|fassung-b>/viertel/<tk>/v<n>/` (je 47 MB) statt unter
    `$D/gruppen/…/bilder/`. Der Basisordner versioniert `wuensche/` samt Bildern, ignoriert ist nur `roh/`. Das Feld
    `bilder` in `gruppen.json` zeigt auf den Ordner.
  - Bildformat JPEG (Regel L11). Übersicht: Viertel plus 32 Bildpunkte, 3fach. Nahansichten: Viertel in 4 Teile, plus
    12 Bildpunkte, 6fach. Die Nummer im Bild ist ID mod 100000 (`id_block`); weiß = eigenes Segment, grau = Nachbarviertel,
    Kontextrand ohne Nummer.
  - Ein Segment gehört dem Viertel mit dem größten Anteil seiner Kernfläche, bei Gleichstand der kleineren Nummer.
    Der „Punkt“ in der Liste liegt innerhalb des eigenen Viertels.
  - Die Kandidaten der Vorstufe stehen als Spalte in der Liste, nicht im Bild (siehe Abweichungen).
  - Zweitagent auf r0c0 (141 Kernsegmente, übliche Dichte) statt auf r1c0 wie im verworfenen Lauf. r1c0 hätte mit 8 bis 21
    Segmenten je Viertel ein zu leichtes Maß gegeben.
  - Vereinheitlichung B (Auftrag `gruppen/b/vereinheitlichen.md`) schreibt in einen eigenen Ordner,
    `fassung-b/vereinheitlichung/`: `kategorien-b-entwurf.json`, `codes.json` (Code je Segment) und `vereinheitlichung.md`.
    Die Viertel-Abgaben ändert sie nicht (L10). Teil 3 liest die Codes aus `codes.json`.
  - Für C: Bilder der ganzen Teilkachel mit `landseg ansicht --nur-teilkachel` nach `fassung-c/ansicht/<tk>/`.
  - `pruefe_urteil.py` hat `--viertel` dazubekommen. Damit prüft es `viertel` und `bilder_angesehen` (Übersicht mit
    `uebersicht_nummern.jpg`, alle Dateien vorhanden); ein zusammengeführtes Urteil verlangt `viertel` je Segment.
Nacharbeit im Hauptordner: Das Workflow-Skript von Teil 2 liest
  `C:/Users/Phil/Developement/Victor/wuensche/2026-11-17-landseg-test-t0-1/gruppen.json`, nicht `…-landseg-test-t0/`. Teil 3 nimmt
  die Codes für B aus `daten/landseg/T0/fassung-b/vereinheitlichung/codes.json`. Die Voraussetzung `landseg-werkzeuge-5` ist auf
  main noch nicht eingereiht (main 3b4e855, Zweig `wunsch/landseg-werkzeuge-5` steht noch); gebraucht wird sie erst für die
  Prüfseite in Teil 3/5.
Abräumen: WEG (keine Arbeitskopie angelegt); keine Dauerprozesse gestartet.
Lagebild: fehlt (landseg hat kein `LAGEBILD.md`; der Datenlauf ändert keinen Code).
Erkenntnisse fürs Profil:
  - `vorstufe` schreibt in `kandidaten.json` je Eintrag `ids` (Liste). `ansicht --kandidaten` liest nur Einträge mit `id`
    (Zahl) und zeichnet Vorstufen-Kandidaten deshalb ohne Meldung nicht ein.
  - `landseg.ansicht.Ansicht(bild, karte, segmente, kategorien, vorgaben, kern=…).zeichnen(art, Fenster(x, y, b, h, faktor))`
    zeichnet jede Bildart für ein beliebiges Fenster. Die Befehlszeile kennt nur ganze Teilkachel oder Fenster je Segment.
  - Der Basisordner versioniert `wuensche/` samt Bildern (`.gitignore` nimmt nur `wuensche/**/roh/` aus). Große Bildmengen
    eines Datenlaufs gehören nach `daten/landseg/`.
  - Ein frisches `kacheln` in einen anderen Zielordner ergibt ein Manifest, das sich in `erstellt` und `quelle.bild`
    unterscheidet (relativer Pfad). Vergleiche ohne diese beiden Felder.
Abweichungen vom Zielbild:
  - landseg/landseg/ansicht.py:117 — `_kandidaten_lesen` erwartet `id` je Kandidat, `vorstufe` schreibt `ids`. Die
    Kandidatenliste der Vorstufe erscheint so in keinem Bild. Nicht umgangen: Die Kandidaten stehen hier nur in der Liste des
    Auftrags. Sauber wäre, wenn `ansicht` das Format `ids` der Vorstufe liest (eigener kleiner Wunsch).
Einreihen (Skript): eingereiht ohne Commit — Nachweis: Datenlauf ohne Commit. (1) Kacheln: frisch nachgekachelt, bytegleich zu kern500 (`kacheln-T0.log`,; Abräumen WEG (keine Arbeitskopie)
