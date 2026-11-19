# Bericht landseg
Status: bereit-zur-pruefung
Für den Nutzer: Auf dem Bild von 1968 (H0) sind alle 65 Stellen, die die Prüfer „unklar" nannten, jetzt Garten mit dem
  Vermerk „unsicher" und dem Grund „Garten wahrscheinlich, auf SW nicht sicher (Nutzer 2026-11-18)".
  In Fassung A waren die 35 Stellen schon Garten (Unterklasse „Garten / Grün im Ort", seit dem Aufräumen der Listen in
  landseg-garten-4); dort kam nur Vermerk und Grund dazu. In B wurden 3 Flächen zu Garten (14 waren es schon), in C alle 13.
  Gärten auf H0 im zusammengesetzten Bild jetzt: A 56, B 22 (vorher 19), C 13 (vorher 0), alle als unsicher markiert.
  Eine neue Grenzstelle in C (1 Bildpunkt an der Viertellinie, Garten neben großer Grünfläche) habe ich als echte Grenze
  entschieden; offene Stellen 0. Die Prüfseite `C:/Users/Phil/Developement/Victor/daten/landseg/seiten/T0-H0.html`
  und die Gesamtmappe für Victor sind lokal neu gebaut und geprüft, nicht hochgeladen.
  Ungeprüft: das Ansehen der Seite im Browser (keine Browser-Erweiterung in diesem Lauf); belegt nur aus den Daten der Seite.
  Ein Beispiel zum Anklicken: H0, Fassung C, Teilkachel r0c0, Segment 100035.
Commit: keiner (Datenlauf ohne Commit im Repo landseg)
Nachweis: Datenlauf auf `daten/landseg/H0` (A/B/C, nur Klassen und Vermerke, keine Karte geändert). Sicherung vorher (labels.tif,
  segmente.json, naht.json je Teilkachel und `zusammen/`, Listen): `sicherung-vor-garten-h0-unsicher/`. Skripte: `skripte/unsicher.py`
  (probe, sicherung, eintragen, zaehlen), `skripte/pruefen_zusammen.py` (Kopie aus garten-4, nur H0), `skripte/seite_pruefen.py`.
  Logs: `logs/` (eintragen.log, schritte-*.json, zaehlen-endstand.log, endstand.log/.txt, seite-T0-H0.log, seite-pruefen.log,
  gesamt-*.log). Einigung: `einigung/auftraege-C/C-01/paar_01.jpg`, `einigung/ergebnis-C/`. Pfade relativ zu diesem Ordner.
Abnahmekriterien:
AK1: erfüllt — `skripte/unsicher.py zaehlen` (`logs/zaehlen-endstand.log`): unklar A 35, B 17, C 13, davon nicht korrekt eingetragen 0/0/0 (Garten-Klasse samt Unterklasse, sicher „nein", Grund gesetzt). Garten-Segmente je Fassung im zusammengetragenen Ausschnitt: A 56, B 22, C 13 (alle unsicher); je Teilkachel samt Kontextrand A 2/130/0/7, B 11/11/1/3, C 13/0/0/0
AK2: erfüllt — `logs/endstand.txt`: pruefen 12 × ok (A/B mit `--frei` und Liste der Fassung); einigung messen H0 Exit 0, offen A 0, B 0, C 0 (unsicher belegt 33/16/12). Vorher (`logs/pruefen-zusammen-nachher.txt`) war in C 1 Paar offen, geklärt mit `einigung abgabe` + `anwenden` (grenze)
AK3: nicht prüfbar (Ansicht; keine Browser-Erweiterung) — Daten der Seite (`skripte/seite_pruefen.py` → `logs/seite-pruefen.log`): H0 Garten A 139, B 26, C 13 Segmente je Teilkachel, alle unsicher; alle 65 unklaren Kandidaten stehen dort als Garten mit sicher „nein" und dem Grund. Die Seite zeigt „unsicher" über `sicherText()` in `landseg/seite_vorlage/seite.js:67`
Prüfungen:
eingriff stapel (klasse_setzen) H0 B r0c0 (3) und C r0c0 (13) → Exit 0, „ok"; Vermerke über `Bearbeitung.vermerken` unter Kartensperre, 65 Verlaufseinträge
pruefen je Teilkachel H0 A/B/C → 12 × ok
zusammentragen H0 A/B/C → nicht zusammenhängend 0, Mängel 0; Nahtverstöße wie vorher 163/141/105 (Exit 1 = nur dieser bekannte Befund)
einigung finden C → 1 Paar r0c0:100114|r0c0:100160 (viertel, 1 Randpunkt); abgabe → „Probe … ok"; anwenden → grenze 1, Klassen gesetzt 0
einigung messen H0 → Exit 0, offen 0/0/0
seite --daten daten/landseg --einstellungen seite-einstellungen.json --ziel daten/landseg/seiten/T0-H0.html → Exit 0, 13 619 769 Bytes
gesamt_projekt.py bauen | pruefen --luftbilder | durchsicht → 0 (Commit af69f8b, Ergebnisse 0 geändert) | ok (Luftbilder 8/8, Arbeitsstand sauber) | ungeordnet oder Fehler 0; kein Push
tools/pruefe_kategorien.py kategorien.json → ok
Aufruf-Budget: 60, gebraucht rund 35
Nicht geprüft: Ansicht der Seite im Browser (keine Browser-Erweiterung). Die Nahtverstöße auf H0 bleiben offen wie vorher.
  Dieser Bericht ist nach dem letzten `gesamt_projekt.py bauen` entstanden und kommt erst mit dem nächsten `bauen` ins Gesamtprojekt.
Technische Entscheidungen:
- Fassung A: Die 35 Kandidaten trugen schon „4.4.1 Garten / Grün im Ort" (Unterklasse von 4.4 Garten, so von landseg-garten-4 festgelegt). Ich habe die Klasse nicht auf 4.4 gesetzt, damit die feinere Stufe bleibt; gezählt wird Garten samt Unterklassen, wie in garten-4.
- `sicher` ist in den H0-Daten als „ja"/„nein" gespeichert; ich habe „nein" gesetzt (wie `einigung anwenden`: Wahrheitswert nur, wo das Feld schon einer ist). Die Seite behandelt „nein" und false gleich.
- `eingriff stapel` kennt nur Karten- und Klassen-Schritte; `sicher` und `grund` habe ich mit `Bearbeitung.vermerken` (Paket-API, Verlaufseintrag, alter Wert unter `ergebnis.alt`) unter `dateien.karte_sperren` gesetzt. Bearbeiter `umsetzer:garten-h0-unsicher`. Der alte `grund` der Urteils-Agents steht im Verlauf.
- Einigungspaar C r0c0:100114|100160 selbst nach `vorlagen/einigung.md` entschieden: „grenze" (getrennte Segmente, Berührung ohne Bildkante nur 1 Bildpunkt an der Viertellinie); „gleich" hätte entweder den Nutzerentscheid oder die große Grünfläche umgestellt.
- Seite wie in garten-4 (T0 aus dem Gesamtprojekt, H0 aus daten/landseg); T0 unverändert, darum nur ein `bauen` nach der Seite.
Nacharbeit im Hauptordner: Kopfzeile der Wunsch-Datei „Ergebnis: ohne Commit" setzen, sonst hält `einreihen.py` an. Nach dem Commit von `wuensche/` `gesamt_projekt.py bauen` erneut fahren (bringt diesen Bericht ins Gesamtprojekt); kein Push ohne Ansage.
Abräumen: WEG (keine Arbeitskopie angelegt); keine Prozesse gestartet
Lagebild: unberührt: im Repo landseg gibt es kein Lagebild, Code nicht geändert
Erkenntnisse fürs Profil:
- `eingriff stapel` kann `sicher`/`grund` nicht setzen (nur verschmelzen, teilen, grenze_verschieben, klasse_setzen, polygon_zuweisen); dafür `Bearbeitung.vermerken` aus `landseg/eingriff.py` unter `dateien.karte_sperren`.
- Garten-Kandidaten in den freien Fassungen können schon eine Unterklasse von Garten tragen (H0 A „4.4.1"): beim Umstellen auf Garten nach Präfix prüfen, nicht nach gleichem Code.
- Eine Klassenänderung innerhalb einer Teilkachel kann neue offene Einigungspaare an der Viertellinie erzeugen: `einigung messen` nach jedem Umstellen fahren.
Abweichungen vom Zielbild: keine
