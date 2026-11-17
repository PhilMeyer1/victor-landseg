# Bericht unterlagen
Status: eingereiht
Einreihen (Skript): eingereiht 86e5c53 docs: add delivered reports 41, 46, 47, 48 with README index in C:/Users/Phil/Developement/Victor/unterlagen (main); Prüfung nach Risiko (ohne Prüfschleuse, keine Zeile schnell: im Profil); entfällt (pruefung: leicht im Profil, keine Testreihen); Abräumen WEG; Waisen 6 (server 5, logwaechter 1), 857 MB anderswo (aufraeumer.py melden; beenden nur mit Freigabe des Nutzers); Hinweis: Landkarte victor fehlt (Prüfer-Auftrag landkarte, der eine liegende Karte übernimmt; seine Meldung speichert sie): der Durchlauf beauftragt den Prüfer; bis sie steht und committet ist, bleibt der Wunsch vor eingereiht
Für den Nutzer: Die fünf Dateien aus Victors Lieferung liegen jetzt unverändert im Repo unterlagen im Ordner berichte/. Dazu gibt es eine README.md mit Zweck, Aufbau, einer Tabelle der Berichte (Nummer, Titel, ein Satz Inhalt, Stand), Herkunft samt Prüfsummen, dem Ort der Luftbilder (daten/luftbilder) und einer Liste dessen, worauf die Berichte verweisen, was aber fehlt (Berichte 32, 35, 38, 39, 40, 44; Skripte und Ergebnisse unter tmp/sai_at). Die Luftbilder und das Archiv sind nicht im Repo. Nichts wurde hochgeladen (kein Push). Zu wissen: Die HTML-Auswertung lädt ihre Diagramme aus dem Internet, und ein Bild in Bericht 47 wird nicht angezeigt, weil es unter tmp/sai_at liegen müsste.
Commit: 86e5c53 "docs: add delivered reports 41, 46, 47, 48 with README index"
Abnahmekriterien:
AK1: erfüllt — `sha256sum` der fünf Dateien im Archiv (ausgepackt in den Scratchpad), der Blobs im Commit (`git cat-file blob HEAD:berichte/<datei> | sha256sum`) und der Dateien in R/berichte nach dem Einreihen: alle fünf gleich (Werte in README.md, „Herkunft"); Namen unverändert, alle in berichte/
AK2: erfüllt — README.md in der Wurzel: Abschnitte Aufbau, Verzeichnis der Berichte (5 Zeilen), Herkunft, Luftbilder, Verwiesen aber nicht mitgeliefert
AK3: erfüllt — `git ls-files` in R: 7 Dateien (.gitattributes, README.md, 5 Berichte), keine .tif/.zip; Summe der Blobs 506 KB, Ordner R ohne Arbeitskopien 814 KB samt .git
Prüfungen:
git -C "$W" status --short → sauber nach dem Commit (schnelle Stufe des Profils)
Volle Stufe: entfällt (pruefung: leicht, keine Testreihen); Einreihen-Skript → eingereiht
Nicht geprüft: Links in der README nicht im Browser angeklickt (Pfade aus dem Commit abgeschrieben); das HTML wurde nicht geöffnet (fremde Lieferung, nur gelesen)
Technische Entscheidungen:
- Alle fünf Dateien haben CRLF-Zeilenenden; bei core.autocrlf=true (Systemkonfiguration von Git) würde Git sie als LF speichern. Daher `.gitattributes` mit `berichte/** -text`; die Blobs sind damit Byte für Byte gleich dem Archiv.
- Ordnername berichte/ wie vorgeschlagen; die HTML-Datei liegt beim Markdown-Bericht 41, weil dieser sie über den Namen im selben Ordner nennt.
- Die Liste „verwiesen, nicht mitgeliefert" aus den Dateien per grep ermittelt (Dateinamen NN_*.md, Bezug-Zeile in 46, Pfade tmp/sai_at/…); dazu die externen Rohdaten aus 47 (GBIF-Download, EBHD-Datei, Pittioni-Kartei).
- Keine .gitignore für .claude/worktrees angelegt (nicht verlangt); R zeigt `?? .claude/` als unversioniert.
- Plugins: Für reine Dokumentablage war außer dem Wunsch-System (Einreihen-Skript) kein weiteres Plugin sinnvoll.
Nacharbeit im Hauptordner: keine
Abräumen: WEG; nichts repo-eigenes
Lagebild: fehlt — R hat kein LAGEBILD.md und das Profil keine Kopfzeile lagebild:; Aufbau und Inhalt beschreibt die README.md (Pflichtlektüre des Profils)
Erkenntnisse fürs Profil:
- Git auf diesem Rechner hat core.autocrlf=true (C:/Program Files/Git/etc/gitconfig); gelieferte Dokumente mit CRLF bleiben nur über die `.gitattributes` (`berichte/** -text`) Byte für Byte gleich; neue Berichte gehören nach berichte/.
- Das Profil nennt das Thema `unterlagen/oberflaeche.md`, die Datei BASIS/.claude/repos/unterlagen/oberflaeche.md gibt es nicht.
- README.md führt eine Prüfsummen-Tabelle der Berichte; bei neuen Lieferungen mitpflegen.
Abweichungen vom Zielbild: keine
