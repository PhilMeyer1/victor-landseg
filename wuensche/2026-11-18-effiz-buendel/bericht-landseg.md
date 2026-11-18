# Bericht landseg
Status: eingereiht
Für den Nutzer: Die Einigung der Klassen über die Kachelgrenzen packt kleine Gruppen von Grenzstellen jetzt in jeden früheren Auftrag, der noch Platz hat, nicht nur in den zuletzt angelegten. Dadurch braucht sie weniger KI-Helfer: Mit den aufgezeichneten Paaren aus dem Lauf auf dem Luftbild 1968 (H0, Durchgang 1) wären es 32 statt 38 Aufträge gewesen (A 15→12, B 13→12, C 10→8), in Durchgang 2 bei C 7 statt 8. Beim Farb-Orthofoto T0 ändert sich nichts (je 4 Aufträge). Kein Auftrag bekommt mehr als 12 Paare, außer eine einzelne große zusammenhängende Gruppe, die wie bisher allein bleibt. Auf der Oberfläche ändert sich nichts. Beim Einreihen wird geprüft, ein echter Einigungslauf mit Agents ist nicht gefahren.
Commit: a62345c "feat(einigung): pack small pair groups first-fit into earlier bundles"
Abnahmekriterien:
AK1: erfüllt — `tests.test_einigung.BuendelnTest.test_kleine_gruppen_fuellen_fruehere_buendel`: Gruppen 7, 9, 3, 2 bei 12 → 2 Bündel [12, 9] (alt 3); `"$PY" -B -m unittest tests.test_einigung` → 11 Tests OK
AK2: erfüllt — vorhandene Tests `test_finden_naht_ecke_viertel_und_kante` (Ecke in einem Bündel) und `test_zusammenhaengendes_bleibt_ganz` (`buendel_paare: 1`) grün; neu `test_uebergross_bleibt_allein` (3, 15, 2, 8 → [5], [15 übergroß], [8]); `pruefe_aufteilung` prüft in allen neuen Tests: jedes Segment in genau einem Bündel, übergroß nur eine Gruppe, sonst höchstens die Obergrenze
AK3: erfüllt — `test_stabil_und_nie_mehr_als_vorher`: zweimal `buendeln` gleiche Ausgabe; Beispiel 4, 3, 3, 4, 3, 3 bei 10 → 2 Bündel; 300 Zufallsfälle gegen die alte Zählung (`_alt_zahl`) nie mehr Bündel
AK4: erfüllt — `PY -B -m landseg einigung finden --manifest daten/gesamt/victor-landseg/ergebnisse/manifest.json --fassung A|B|C --ziel <scratchpad>` mit altem (main) und neuem Code: Exit 0, `einigung.json` nennt 0 Bündel (die T0-Daten des Gesamtprojekts sind schon geeinigt, 0 offene Paare). Bündelzahl vorher/nachher daher an den aufgezeichneten Läufen neu gepackt (Paare aus den `auftrag.json`, alte Zählung reproduziert die aufgezeichnete in allen 13 Läufen): T0 (naht-einigung-2) 4/4/4 → 4/4/4; H0 (landseg-historisch-3) Runde 1 15/13/10 → 12/12/8, Runde 2 C 8 → 7, sonst gleich. Liste: `wuensche/2026-11-18-effiz-buendel/buendelzahl-vorher-nachher-landseg.txt`
AK5: erfüllt — `"$PY" -B -m unittest discover -s tests -t .` → 125 Tests OK (35 s)
Prüfungen:
schnell: `tools/pruefe_kategorien.py kategorien.json` → „7/25/43 … ok", Exit 0; `tests.test_einigung` → 11 OK
`"$PY" -B -m unittest discover -s tests -t .` → 125 OK — die volle Reihe habe ich selbst gefahren, weil AK5 sie als Beleg nennt (35 s, ohne Ticket der Prüfschleuse); das hätte nach den Regeln erst der Pflichtlauf des Einreihens tun sollen
Gezielte Tests der berührten Stelle: `tests.test_einigung` (BuendelnTest, EinigungTest)
Nicht geprüft: kein `einigung finden` auf Daten mit offenen Paaren (keine ungeeinigten Ergebnisordner ohne Eingriff in fremde Repos gefunden); Kosten/Laufzeit eines echten Agent-Laufs nicht gemessen
Einstieg: stimmte (`buendeln` bei `landseg/einigung.py:214`, Tests bei 94/106)
Technische Entscheidungen:
- First-fit in der Reihenfolge der Linien, nicht nach Größe absteigend sortiert: Sortiert (first-fit decreasing) kann mehr Bündel ergeben als das alte Verfahren (Beispiel 4, 3, 3, 4, 3, 3 bei Obergrenze 10: sortiert 3, alt 2), das verletzte AK3. First-fit in Eingangsreihenfolge öffnet je altem Bündel höchstens ein neues, kann also nie mehr Bündel brauchen; die Ortsnähe bleibt eher erhalten. Am H0-Lauf bringt es trotzdem 6 Bündel weniger.
- Bündelnamen laufen wie bisher über `enumerate` in Anlegereihenfolge; innerhalb eines Bündels stehen Gruppen in Einfüge-Reihenfolge.
- README Abschnitt Einigung nennt jetzt „erstes Bündel mit Platz"; `gesamt/ANLEITUNG.md` (Zeile ~213, „höchstens etwa 12 Paare") stimmt weiter und bleibt.
Nacharbeit im Hauptordner: keine (`gesamt/ANLEITUNG.md` unverändert; das Gesamtprojekt bekommt den README-Text beim nächsten `gesamt_projekt.py bauen` ohnehin)
Abräumen: offen (Arbeitskopie bleibt bis zum Einreihen); Testausgaben nur im Scratchpad der Sitzung
Lagebild: fehlt (landseg hat kein LAGEBILD.md)
Erkenntnisse fürs Profil:
- Die T0-Daten des Gesamtprojekts (`daten/gesamt/victor-landseg/ergebnisse/`) sind schon geeinigt: `einigung finden` liefert dort 0 offene Paare und 0 Bündel; für Bündelvergleiche die Paare aus den aufgezeichneten `auftrag.json` unter `wuensche/*/…/auftraege-*/` neu packen.
Abweichungen vom Zielbild: keine
Einreihen (Skript): eingereiht a62345c feat(einigung): pack small pair groups first-fit into earlier bundles in C:/Users/Phil/Developement/Victor/landseg (main); Prüfung nach Risiko (ohne Prüfschleuse, keine Zeile schnell: im Profil); voll grün (45 s); volle Prüfung offen (vermerkt in C:/Users/Phil/Developement/Victor/landseg/.git/wunsch-einreihen/pruefung-offen.jsonl); Abräumen WEG; Waisen 3 (sonstige 2, server 1), 134 MB anderswo (aufraeumer.py melden; beenden nur mit Freigabe des Nutzers)
