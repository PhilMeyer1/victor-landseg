# Bericht landseg
Status: blockiert (kein Commit nötig: reiner Datenlauf, die Kopfzeile trägt aber kein „Ergebnis: ohne Commit")
Für den Nutzer: Gärten sind jetzt in beiden Bildern und allen drei Fassungen sauber eingetragen, und die
  Prüfseite `C:/Users/Phil/Developement/Victor/daten/landseg/seiten/T0-H0.html` (13,6 MB) ist neu gebaut: In der
  Legende steht überall „Garten" unter „Dauergrünland" mit eigener hellgrüner Farbe. Die Gesamtmappe für Victor
  (`daten/gesamt/victor-landseg`) ist lokal neu gebaut und geprüft, aber nicht hochgeladen.
  Vorher aufgeräumt: Die eigenen Listen der freien Fassungen A und B heißen jetzt einfach „Dauergrünland" statt
  „Dauergrünland (alter Name)". Gartenklassen, die dort noch an anderer Stelle standen (etwa „Gartenrasen",
  „Beete", „Garten / Grün im Ort"), stehen jetzt unter „Garten" und behalten ihren genauen Namen.
  Dadurch steigt die Zahl der Gärten: T0 A 130, B 126, C 122 Flächen (vorher 101/115/118); H0 A 56, B 19
  (vorher 1/3). H0 C hat weiter keinen Garten, weil die Prüfung in Teil 3 dort keinen bestätigt hat. Die Legende
  zeigt ihn trotzdem.
  Repariert: 84 Flächen in T0, die nur über den Bildrand zusammenhingen, sind getrennt. Die zwei offenen
  Grenzstellen sind geklärt: ein Grasstreifen gehört zum selben Garten. Offene Stellen gibt es 0.
  Nicht gemacht: Ansehen der Seite im Browser (keine Browser-Erweiterung in diesem Lauf); der Beleg kommt
  aus den Daten der Seite. Ein Haus mit Garten zum Anklicken liegt in T0 etwa bei x 863, y 818: Dort steht in A, B und C „Garten".
Commit: keiner im Repo landseg; Ergebnisse T0 in der Übergabe-Grundlage `daten/landseg/uebergabe/landseg-t0` als 297ae4a "feat(T0): gardens as their own class in A, B, C and regenerated result page"; Gesamtprojekt bf0d73a, 3853cc3, 0c24732, c5efada, 2a54650, c34a4f4 (von `gesamt_projekt.py bauen`)
Nachweis: Datenlauf auf `daten/landseg/uebergabe/landseg-t0/T0` und `daten/landseg/H0`. Listen geordnet: `logs/listen-ordnen-echt.log`, `logs/listen-regeln.log`.
  Zerfall: `logs/zerfall-T0.log` und `.json`. Endstand pruefen, zusammentragen, einigung: `logs/endstand.log`.
  Einigung: `einigung/`. Seiten: `seite.json`, `logs/seite-T0.json`, `logs/seite-garten.log`. Garten je Fassung: `logs/garten-vergleich.log`.
  Sicherung vor dem Lauf (Listen, Karten, segmente.json, zusammen/ aller 6 Fassungen): `sicherung-vor-garten-4/`,
  dazu die Teilkacheln vor dem Zerfall: `sicherung-zerfall/`. Skripte: `skripte/`. Alle Pfade relativ zu diesem Ordner.
Abnahmekriterien:
AK7: erfüllt bis auf H0 C (dort kein Garten-Segment, nur Legende) — Ansicht nicht prüfbar (keine Browser-Erweiterung). Beleg aus den eingebetteten Daten (`skripte/seite_garten.py` → `logs/seite-garten.log`): T0 A 4.4, B 2.4, C 3.6, H0 A 4.4, B 5.3, C 3.6, je „Garten" unter „Dauergrünland", kleinster Farbabstand zur übrigen Liste 16,6 bis 24,5 (CIELAB). Segmente mit Garten: T0 130/126/122, H0 56/19/0. Gesamtprojekt neu gebaut, `pruefen` ok, `durchsicht` 0 ungeordnet, kein Push. `tests.test_seite` und `tests.test_gesamt_projekt`: 20 OK
AK8: nicht prüfbar (Ansicht) — Daten: An 25 Garten-Segmenten von C an einem Hauptgebäude sind dieselben Bildpunkte in A zu 89,4 % und in B zu 98,1 % Garten. Beispiel x 863, y 818: A 4.4, B 2.4 und C 3.6, jeweils „Garten (Haus- und Hofgarten …)" unter „Dauergrünland" (`logs/garten-vergleich.log`)
Prüfungen:
Vorarbeit 1 (Listen): `skripte/listen_ordnen.py echt` → 4 Listen, 14 × `eingriff stapel` Exit 0 (T0 A 70, T0 B 12, H0 A 138, H0 B 20 Segmente umgestellt); `skripte/listen_regeln.py` → bericht48 und abbildung_teilkacheln nachgezogen; `garten_maengel` je Liste leer
pruefen je Teilkachel, eigene Liste, A/B mit `--frei` → 24 × ok
Vorarbeit 2 (Zerfall): `historisch-4/skripte/zerfall_beheben.py` auf T0 → A 22 Teile (19 neu, 3 an Nachbarn), B 31 (14/17), C 31 (15/16), Fehler 0; H0 0 (nach dem Vergröbern schon 0); Probe danach 0/0/0
zusammentragen mit `--kategorien <Liste der Fassung>` → nicht zusammenhängend 0 und 0 Mängel in allen 6. Nahtverstöße, wie bekannt offen: T0 A 308, B 306, C 306; H0 A 163, B 141 (10 bestätigt), C 105 (28 bestätigt). Exit 1 = nur dieser Befund
Einigung nach dem Zerfall: `skripte/einigung_nachziehen.py` (Kopie aus historisch-4) → T0 A 6, B 4, C 9 neue Paare: Beschluss übernommen oder „unklar"
Vorarbeit 3: `einigung finden`, `abgabe` und `anwenden` für T0 B und C → je 1 Paar r0c1:200143|200149 „gleich" auf Garten (2.4 bzw. 3.6). Bild: `einigung/auftraege-B/B-01/paar_01.jpg`
einigung messen → offen 0 in T0 und H0 (unsicher belegt T0 10/7/14, H0 33/16/12)
Vorarbeit 4: `zusammentragen.json` von T0 B und C → gleiches Muster wie A: Manifest `../manifest.json`, 4 Einheiten, Runde 0, Namen b-/c-r?c?, Pfade vorhanden. Ohne `naht_bestaetigt` wie A und die alte `T0/fassung-c/zusammentragen.json`; richtig
seite --manifest (Übergabe T0/T0.html) → Exit 0, 8 787 420 Bytes; seite --daten … --einstellungen seite-einstellungen.json (T0 aus Gesamtprojekt, H0) → Exit 0, 13 610 606 Bytes
gesamt_projekt.py bauen | pruefen --luftbilder | durchsicht → 0 | ok (fehlend 0, abweichend 0, Luftbilder 8/8) | 0 ungeordnet. Logs der letzten Runde lagen im Scratchpad; siehe Erkenntnisse
`"$PY" -B -m unittest tests.test_seite tests.test_gesamt_projekt` → Ran 20, OK; `tools/pruefe_kategorien.py kategorien.json` → ok
Aufruf-Budget: 110, gebraucht rund 75
Nicht geprüft: Ansicht der Seite und des Gesamtprojekts im Browser (keine Browser-Erweiterung), also auch Ebenenauswahl
  und Klick auf ein Segment nur aus den Daten. 3 neue Zerfall-Paare ohne alten Beschluss (T0 B 1, C 2) sind „unklar"
  belegt und nicht am Bild beurteilt. Die Nahtverstöße bleiben offen (eigener Wunsch „Grenzlinien an den Nähten").
  Mein Bericht ist nach dem letzten `bauen` entstanden und kommt erst mit dem nächsten `bauen` ins Gesamtprojekt.
Technische Entscheidungen:
- Listen ordnen: Die Ebene-1-Klasse heißt genau „Dauergrünland" (T0 A 4, T0 B 2, H0 A 4, H0 B 5); die Unterklassen bleiben, wie sie sind. Gartenklassen an anderer Stelle (L14: jeder Gartenname geht auf „Garten" über) wandern unter „Garten" und behalten Namen, Farbe und Bildmerkmal als feinere Stufe: T0 A 3.1/3.2/3.3 → 4.4.1/4.4.2/4.4.3, T0 B 3.3.1/3.3.2 → 2.4.1/2.4.2, H0 A 2.2/2.3 → 4.4.1/4.4.2. Wo die Klasse schon „Garten" hieß, geht sie direkt auf die Garten-Klasse: H0 B 2.2 → 5.3, T0 B 3.3 „Gartenparzelle" (ohne eigene Segmente) → 2.4. So behalten die Segmente ihre genaue Bedeutung; auf Ebene 2 zeigt die Seite alle als „Garten".
- Leere Klassen entfernt: T0 A „3 Garten / Siedlungsgrün". Umbenannt, weil kein Segment die Klasse selbst trägt: T0 B 3 „Feld, Garten und offener Boden" → „Feld und offener Boden", H0 B 2 „Hof und Garten" → „Hof". H0 A 2 „Hof und Garten" bleibt so, weil 8 Segmente genau diese Klasse tragen („Hof oder Garten").
- Regel G1 `bericht48.im_siedlung_klassen` der freien Listen nennt jetzt die Garten-Klasse, wie AK3 der festen Liste: T0 A ["4.4"], T0 B ["2.2","2.4"], H0 A ["2","4.4"], H0 B ["2","5.3"]. In `abbildung_teilkacheln` von A wurden 11 (T0) und 5 (H0) Zielcodes umgestellt. Zeilenenden der vier Listen wieder LF, wie vorher.
- Segmente nur über `landseg eingriff stapel` (klasse_setzen) umgestellt, Bearbeiter `umsetzer:landseg-garten-4`.
- Zerfall an der Quelle behoben (Teilkachelkarten), Einigung der neuen Paare wie in historisch-4 übernommen. Die zwei Garten-Paare habe ich selbst am Paarbild nach `vorlagen/einigung.md` entschieden, mit den fertigen Befehlen `einigung abgabe` und `anwenden`.
- Übergabe-Grundlage: Teil 3 hatte T0 dort geändert; `gesamt_projekt.py bauen` liest nur deren HEAD. Darum dort committet, mit `T0/T0.html` neu und den `zusammentragen.json` und `zusammen/` von B und C, die Teil 3 angelegt hat.
- Die Seite T0-H0 wurde wie in historisch-4 gebaut: T0 aus dem Gesamtprojekt, also nach dem ersten `bauen`, danach `bauen` erneut für die Seite.
Nacharbeit im Hauptordner: Kopfzeile „Ergebnis: ohne Commit" setzen und einreihen. Nach dem Commit von `wuensche/` `gesamt_projekt.py bauen` erneut fahren (Bericht dieses Teils); kein Push ohne Ansage. Profil `landseg/betrieb.md` Zeile 51 („pruefen --frei … schon vorher rot") ist überholt: jetzt grün.
Abräumen: WEG (keine Arbeitskopie angelegt); keine Prozesse gestartet
Lagebild: unberührt: im Repo landseg gibt es kein Lagebild, Code nicht geändert
Erkenntnisse fürs Profil:
- `zusammentragen` ohne `--kategorien` prüft auch freie Fassungen gegen die feste Liste (Scheinfehler „ungültige Klasse"): immer die Liste der Fassung angeben.
- Werden Klassen einer freien Liste verschoben oder entfernt, auch `rules[].bericht48.im_siedlung_klassen` und `abbildung_teilkacheln` nachziehen, sonst bricht `pruefen` mit „Regel bericht48 nennt unbekannte Klasse" ab (Exit 2).
- In der Übergabe-Grundlage gilt `-c core.autocrlf=false` auch für `git add`, nicht nur für `commit`. Python `Path.write_text` schreibt unter Windows CRLF; die Listen kategorien-a/-b.json sind LF.
- `gesamt_projekt.py pruefen` meldet Logs, die während des Laufs unter `wuensche/` entstehen, als fehlend oder abweichend. `durchsicht` meldet einen eigenen Durchsicht-Bericht unter `wuensche/` als UNGEORDNET. Logs und Bericht dieser Läufe gehören ins Scratchpad.
Abweichungen vom Zielbild:
- `landseg/landseg/pruefen.py:77` — Zusammenhang wird je Teilkachel samt Kontextrand geprüft, darum fielen in T0 84 zerfallene Kernsegmente erst beim Zusammentragen auf, Behebung über ein Wunsch-Skript (wie in historisch-4 gemeldet) — sauber wäre die Kernprüfung in `pruefen`/`eingriff`.
