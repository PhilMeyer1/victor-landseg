# Bericht landseg
Status: eingereiht
Für den Nutzer: Die feste Kategorienliste hat jetzt unter „3 Dauergrünland“ die Unterklasse „3.6 Garten“ mit eigener, hell mintgrüner Farbe (#a6ffaf). Dazu zählen Grünflächen und Beete in Haus- und Hofgärten (auch Vor-, Obst- und Gemüsegarten, gepflegt oder nicht); Gartenbäume, Sträucher, Hecken bleiben Gehölz, Parks, Friedhöfe und Sportrasen bleiben Wiese/Weide. Für Bericht 48 zählt ein Garten im Ort weiter zur Siedlung, sonst zum Grünland. Die Liste hat nun 59 statt 58 Klassen (7/26/44). Die vorhandenen Karten, die Agent-Regeln, die Seite und das Gesamtprojekt kennen Garten noch nicht (Teile 2 bis 4). Das Einreihen fährt die Testreihe „voll“ des Profils.
Commit: 6f0763b "feat(kategorien): garden as subclass 3.6 of permanent grassland"
Abnahmekriterien:
AK1: erfüllt — `"$PY" -I tools/pruefe_kategorien.py kategorien.json` → „level 1: 7, level 2: 26, leaves: 44 (7/26/44), classes: 59 … ok“; 3.6 mit Farbe #a6ffaf (kleinster Abstand zu allen anderen Farben dE 21,9, Mindestwert 10; engstes Paar der Liste bleibt 6.1/6.6 mit 16,0), bw „eing.“, image_cue, mappings (DKM „Gärten“, Bericht 48 „Hausgärten als Teil der Siedlung führen“)
AK2: erfüllt — KATEGORIEN.md: Tabellenzeile 3.6, neuer Abschnitt „Garten“ (dazu / nicht dazu / im Zweifel), Absatz „keine Klasse Siedlungsgrün“ ersetzt, G1 (md und json) umgeschrieben, Zählung 26/44/59 in KATEGORIEN.md, README.md, gesamt/ANLEITUNG.md (Z. 18 und Tabelle C), gesamt/CLAUDE.md, tests/test_kategorien.py; `"$PY" -B -m unittest tests.test_kategorien` → 10 Tests OK
AK3: erfüllt — neuer Test `test_garten_im_siedlungsgebiet_zaehlt_als_siedlung_sonst_als_dauergruenland` (3.6 mit ja → 1, mit nein oder ohne Merkmal → 3), in tests.test_kategorien grün
Prüfungen:
"$PY" -I tools/pruefe_kategorien.py kategorien.json → 7/26/44, 59 Klassen, ok
"$PY" -B -m unittest tests.test_kategorien tests.test_pruefen tests.test_vorstufe → 41 Tests OK
volle Stufe: nicht selbst gefahren, läuft im Pflichtlauf des Einreihens
Nicht geprüft: ganze Testsuite (volle Stufe); Seite und Gesamtprojekt mit der neuen Klasse (Teil 4); ANLEITUNG-Tabelle „im Kern benutzt“ für C bleibt 27, bis die Karten umgestellt sind (Teil 3/4)
Einstieg: wich ab: `landseg/kategorien.py` und `tools/pruefe_kategorien.py` brauchten keine Änderung — Regel G1 nennt schon Klasse „3“ samt Unterklassen in `im_siedlung_klassen`, die Zählprüfung liest alles aus der Datei; nur Daten, Texte und Tests geändert
Technische Entscheidungen: Farbe #a6ffaf als die Farbe im Grünbereich (Farbton 60–180°) mit dem größten Abstand zu allen 58 bisherigen Farben (Rasterung über HSV), damit die Farbfamilie „Grünland hellgrün“ erhalten bleibt; Name „Garten (Haus- und Hofgarten: Grünfläche, Beet)“ beginnt mit „Garten“; Mappings CORINE 1.1.2, CLC+ 6, FLAIR 10/12, DKM „Gärten“ (ungeprüft wie alle Zuordnungen); im Zweifel Elternklasse 3 ohne `sicher: nein`, weil die Lage Nutzung ist (U5)
Nacharbeit im Hauptordner: BASIS/.claude/repos/landseg.md, Pflichtlektüre-Zeile „7/25/43 Klassen, insgesamt 58“ → „7/26/44, insgesamt 59“, und Schnell-Zeile „erwartet 7/25/43 … ok“ → „7/26/44“ (Nacharbeit-Zeile des Mutterwunschs)
Abräumen: offen (Auftrag umsetzen; Arbeitskopie C:/Users/Phil/Developement/Victor/landseg/.claude/worktrees/wunsch-landseg-garten-1 bleibt bis zum Einreihen)
Lagebild: fehlt (landseg hat kein Lagebild; Profil ohne Kopfzeile `lagebild:`, kein LAGEBILD.md in R)
Erkenntnisse fürs Profil: keine
Abweichungen vom Zielbild: keine
Einreihen (Skript): eingereiht 6f0763b feat(kategorien): garden as subclass 3.6 of permanent grassland in C:/Users/Phil/Developement/Victor/landseg (main); Prüfung nach Risiko (ohne Prüfschleuse, keine Zeile schnell: im Profil); voll grün (63 s); volle Prüfung offen (vermerkt in C:/Users/Phil/Developement/Victor/landseg/.git/wunsch-einreihen/pruefung-offen.jsonl); Abräumen WEG; Waisen 3 (sonstige 2, server 1), 132 MB anderswo (aufraeumer.py melden; beenden nur mit Freigabe des Nutzers)
