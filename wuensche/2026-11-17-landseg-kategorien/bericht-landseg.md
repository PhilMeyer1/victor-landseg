# Bericht landseg
Status: eingereiht
Für den Nutzer: Im Repo landseg liegt jetzt die feste Kategorienliste: 7 grobe Klassen (0 bis 6), 25 auf Ebene 2, 46 feinste Klassen, 62 insgesamt, jede mit eigener Farbe, SW-Kennzeichen und Zuordnung zu CORINE, CLC+, FLAIR, DKM und Bericht 48; dazu die Regeln G1–G5 und U1–U5 und die Abweichungen A1–A4. `KATEGORIEN.md` erklärt sie in Alltagssprache, ein kleines Prüfskript meldet 7/25/46 und „ok". Ungeprüft bleiben (und sind so gekennzeichnet): die SW-Spalte (Vermutung bis zum Test T0) und die Zuordnungen zu CORINE/CLC+/FLAIR/DKM (eigene Zuordnung). Die Farben habe ich festgelegt (Familien je grober Klasse); Schnee/Eis (6.5) ist dadurch braun statt weiß. Das Einreihen übernimmt die vier Dateien in den Hauptzweig main von landseg; es gibt keine Tests, die laufen müssen.
Commit: 945c1f7 "feat: add tiered category list with rules and validator"
Abnahmekriterien:
AK1: erfüllt — `python -I tools/pruefe_kategorien.py kategorien.json` (in W) → „level 1: 7, level 2: 25, leaves: 46 (7/25/46), classes: 62 … ok", Exit 0; jede Klasse hat code, name, parent, level, color, bw (ja|eing.|nein), mappings.corine/clc_plus/flair/dkm/bericht48 (Listen)
AK2: erfüllt — gleicher Befehl auf beschädigte Kopien im Scratch-Ordner: kaputt1 (doppelter Code, falscher Elterncode, fehlendes bw, ungültige Farbe, doppelte Farbe, eine U-Regel weniger) → 12 Fehler, Exit 1; kaputt2 (eine Farbe fast gleich einer anderen, dE 0,6) → 1 Fehler, Exit 1; kaputt3 (abgeschnittenes JSON) → „cannot read", Exit 1
AK3: erfüllt — Abschnitt `rules` in kategorien.json, je Regel id, kind, title, text (Wortlaut aus e02), source (e02.md:<Zeile> und Quellen); Prüfskript meldet „rules: 5 G, 5 U"
AK4: erfüllt — KATEGORIEN.md: Abschnitte „Aufbau: drei Ebenen", „Die Klassen" (Tabelle, 62 Zeilen), „Grundsätze G1 bis G5", „Regeln für Unklares U1 bis U5", „Abweichungen von Bericht 48" (A1–A4 mit Entscheidungen F1, F2, F5)
AK5: erfüllt — kategorien.json `status.bw` „VERMUTUNG bis zum Test …", `status.mappings` „eigene Zuordnung, nicht gegen amtliche Tabellen geprüft …"; KATEGORIEN.md Abschnitt „Was noch nicht gesichert ist" und Tabellenkopf „SW (Vermutung)"
AK6: erfüllt — README.md nennt kategorien.json, KATEGORIEN.md und das Prüfskript; Aufruf mit `C:/Users/Phil/Developement/websites/nai/stitcher/.venv/Scripts/python.exe -I tools/pruefe_kategorien.py kategorien.json` → ok, Exit 0
Prüfungen:
git -C "$W" status --short (schnelle Stufe) → sauber nach Commit
Stitcher-venv-Python: Prüfskript auf echte Datei → ok; auf drei beschädigte Kopien → Exit 1
Nicht geprüft: SW-Spalte und Abbildungsspalten inhaltlich (laut Wunsch erst am Bild bzw. gegen amtliche Tabellen); keine Bildschirmfotos (keine Oberfläche)
Einstieg: wich ab: die Formvorlage `websites/nai/stitcher/kachel_direkt/kategorien.json` gibt es nicht (kein `kategorien.json` unter websites/nai gefunden); Struktur daher selbst festgelegt. Inhaltsvorlage e02.md:84-183 und Gegenprüfung stimmten.
Technische Entscheidungen:
- JSON-Schlüssel englisch (code, name, parent, level, color, bw, mappings, rules, deviations), Inhalte deutsch; `counts` in der Datei nennt die Sollzahlen, das Skript vergleicht dagegen.
- Namen aus e02 übernommen, nur die Klammerzusätze „(Abweichung: …)" bei 2.4 und 4 in eigene Felder `deviation`/`deviation_note` verschoben; Hinweis „Verwechslung mit Überstrahlung" bei 6.5 als `bw_note`.
- Abbildungen als Listen; „–" = leere Liste. DKM-Einträge „Sonstige 6, 9, 10" und „Abbauflächen, Halden, Deponien" nicht zerteilt (je eine Angabe).
- G3 bekommt `correction` mit § 4 BANU-V (Gegenprüfung B10), U3 eine Anmerkung zur CLC+-50-%-Schwelle (B5); Wortlaut von e02 sonst unverändert.
- Farben: feste Grundfarbe je Ebene-1-Klasse, Kinder per größtmöglichem Abstand innerhalb der Farbfamilie gewählt; Mindestabstand im Skript CIE76 dE ≥ 10 über alle 62 Klassen (nicht nur die 46 Blätter, da Elternklassen gültige Labels sind); erreicht: 18,1 (0.1 / 4.2.4).
Nacharbeit im Hauptordner: Profil `landseg` nachziehen (Pflichtlektüre KATEGORIEN.md, Prüfung um `tools/pruefe_kategorien.py`, danach `pruefung: voll`) — laut Arbeitsauftrag Sache der Profil-Pflege
Abräumen: WEG; keine repo-eigenen Reste (Skript meldet 6 fremde Waisen, nicht von diesem Wunsch, nicht angefasst)
Lagebild: fehlt — das Repo hat kein Lagebild; der Wunsch verlangt keins
Erkenntnisse fürs Profil:
- Das Repo hat kein `.gitignore`; jede Arbeitskopie unter `.claude/worktrees/` erscheint im Hauptordner als unversioniertes `.claude/`.
- Prüfung der Kategorienliste: `python -I tools/pruefe_kategorien.py kategorien.json` (nur Standardbibliothek, unter 1 s), geeignet für `schnell:`.
- Die im Wunsch genannte Formvorlage `websites/nai/stitcher/kachel_direkt/kategorien.json` existiert nicht.
Abweichungen vom Zielbild: keine
Einreihen (Skript): eingereiht 945c1f7 feat: add tiered category list with rules and validator in C:/Users/Phil/Developement/Victor/landseg (main); Prüfung nach Risiko (ohne Prüfschleuse, keine Zeile schnell: im Profil); entfällt (pruefung: leicht im Profil, keine Testreihen); Abräumen WEG; Waisen 6 (server 5, logwaechter 1), 372 MB anderswo (aufraeumer.py melden; beenden nur mit Freigabe des Nutzers)
