# Bericht landseg
Status: eingereiht
Für den Nutzer: Nachbesserung zum Mangel bei AK6. Fassung A lag nach dem Zusammenlegen noch bei 829 Flächen. Jetzt sind es 566 und damit weniger als der Richtwert von rund 600.
  Zwei Änderungen haben das bewirkt. Erstens: Kleine Flecken an den Kachel- und Viertelgrenzen werden jetzt auch zusammengelegt, aber nur mit einer Nachbarfläche derselben Klasse. Die Beschlüsse der Agenten aus der Einigung gehen dabei auf die zusammengelegte Fläche über, deshalb bleibt die Einigung gültig (weiter 0 offene Stellen). Zweitens: 251 schmale „Schattenfugen zwischen Gebäuden“ (in B 16 „Schatten zwischen Gebäuden“) galten bisher als geschütztes Gebäude, nur weil „Gebäude“ im Namen steht. Jetzt zählt nur der vordere Teil des Namens, also „Schattenfuge“. Echte Häuser, Bäume, Wege und Gärten bleiben weiter geschützt.
  Gemessen habe ich an einer Kopie: A 1833 → 566, B 728 → 468, C 470 → 297 Flächen. Die Nahtverstöße sind weniger geworden (A 187 → 163, B 152 → 141, C 119 → 105; sie waren schon vorher rot). Die echten H0-Daten sind weiterhin nicht angefasst (siehe Nacharbeit), deshalb zeigt die Prüfseite H0 noch die alten Flächen. Farbbilder (T0) bleiben unverändert.
Commit: 95cb45b "feat(bildart): coarser segments on old black-and-white scans"
Abnahmekriterien:
AK1: erfüllt — tests/test_bildart.py `test_farbe_unveraendert_sw_weniger_segmente` → OK. Der Farbweg ist unberührt, denn ohne Mindestfläche wird nichts zusammengelegt. T0 war in der ersten Runde mit `vorstufe --neu` byte-gleich.
AK2: erfüllt — `vorstufe --manifest roh/H0-vorstufe-neu/manifest.json --teilkachel <rXcY> --neu`, ohne GPU, neu gefahren: Kern 95/55/22/84 = 256 Segmente (vorher 465, in der ersten Runde 267), `pruefen ok` je Teilkachel
AK3: erfüllt — unverändert seit der ersten Runde: `{{FEINHEIT}}` in den Vorlagen, Abschnitt `feinheit-sw`, Skill-Regel L15
AK4: erfüllt — `test_pruefen_richtwert_ist_hinweis` → OK; im Log Hinweise für die H0-Teilkacheln über 150, Exit 0
AK5: erfüllt — Vorlagen und L15 wie in der ersten Runde. Im Code bleibt ein sicherer „Garten“ geschützt (auch „Garten / Grasland im Grundstück“, Test `test_schutz_nur_im_kopf_des_namens`).
AK6: erfüllt (an der Kopie; echte Daten = Nacharbeit) — `vergroebern` auf roh/H0-grob2, Segmente im Kern: A 1833 → 566 (81/269/38/178), B 728 → 468, C 470 → 297. `pruefen` je Teilkachel ok, lückenlos, `zusammentragen` pruefen ok (0 zerteilte Segmente). `einigung messen` offen 0 in A/B/C wie vorher. Umgestellte Beschlüsse: 130/48/61. Nahtverstöße 163/141/105 statt 187/152/119. Log: wuensche/2026-11-18-landseg-sw-grob/vergroebern-h0.txt
AK7: nicht prüfbar — die Prüfseite liest die echten H0-Daten. Die werden erst mit der Nacharbeit gröber, daher kein Foto.
Prüfungen:
tools/pruefe_kategorien.py kategorien.json → ok
"$PY" -B -m unittest tests.test_bildart tests.test_vorlagen tests.test_vorstufe tests.test_pruefen tests.test_lauf tests.test_plan tests.test_eingriff tests.test_einigung → 98 Tests OK (gezielte Tests der berührten Stellen; die volle Suite läuft beim Einreihen)
Gegenprobe: Kern-Regel abgeschaltet → `test_naht_nur_mit_beruehrung_im_kern` FAIL. Regel wieder an → OK.
vergroebern + pruefen + zusammentragen + naht + einigung messen an der H0-Kopie, vorher und nachher → vergroebern-h0.txt
Einreihen, 1. Lauf (Workflow): Reihe voll nach 90 s abgebrochen (Zeitüberschreitung, `zeit: 90` im Profil), 133 von 178 Tests liefen, keiner rot. Ursache nicht der Wunsch: `tests.test_gesamt_projekt…test_bauen_ist_wiederholbar_und_bringt_neue_commits_mit_verlauf` braucht allein 37 s auf main (67ef1f5) und 56 s im Zweig; die neuen Tests in tests/test_bildart.py zusammen 0,11 s; Tests 130–177 einzeln je unter 0,2 s.
Einreihen, 2. Lauf: einreihen.py … --zeit 300 → eingereiht, voll grün (135 s). Kein amend, Code unverändert.
Nicht geprüft: volle Testsuite (läuft nur beim Einreihen); Foto der Prüfseite (AK7). Auf den H0-Daten schon vorher rot: `pruefen --frei` für A und B (Garten-Regel L14) sowie `zusammentragen`/`naht`, durch diesen Wunsch weniger statt mehr.
Einstieg: wich ab — wie in der ersten Runde: Einstellungen in einstellungen/bildarten.json statt vorstufe.json; Skill-Regel L15.
Technische Entscheidungen:
- Nachbesserung zu AK6: Ein Segment auf einer Kern- oder Viertelgrenze bzw. im Kontextrand wird jetzt auch zusammengelegt, aber nur mit einem Nachbarn derselben Klasse. So bleibt die Klasse an jeder Linie gleich, und keine neue Einigungsrunde der Agenten ist nötig.
- Die Beschlüsse der Einigung stehen oft nur beim Partner in der Nachbar-Teilkachel. Deshalb lädt `vergroebern` jetzt alle Teilkacheln der Fassung und hält sie gesperrt. `bildart.einigung_umbenennen` stellt danach in der ganzen Fassung `paar` und `mit` auf die aufnehmende ID um. Wenn beide Seiten in dasselbe Segment aufgehen, fällt der Beschluss weg. Geschrieben wird erst, wenn `pruefen` für alle Teilkacheln ok ist. Ohne das Umbenennen blieben an der Kopie 2 Paare offen, mit ihm 0.
- Zusammengelegt wird nur, wenn sich beide Segmente im Kern berühren. Sonst zerteilte das Abschneiden des Kontextrands beim Zusammentragen das Segment (an der Kopie zuerst 7 Fälle in C).
- Schutz klarer Objekte: Das Schutzwort zählt nur im Kopf des Klassennamens, also bis zur ersten Klammer oder bis zum ersten Lagewort (`schutz.lagewoerter` in bildarten.json, etwa „zwischen“, „an“, „auf“). Geprüft an allen H0-Listen: Den Schutz verlieren nur „Schattenfuge zwischen Gebäuden“ (251) und „Schatten zwischen Gebäuden“ (16). „langes Haus auf dem Anger“, „Wohn- oder Langhaus“ und „Gasse oder Hofweg“ bleiben geschützt. Ein reiner Erstwort-Ansatz hätte diese drei verloren und wurde verworfen.
- Die Vorstufe nutzt dieselbe Funktion; dort gibt es keine Beschlüsse, sie wird nur etwas gröber (267 → 256 im Kern).
Nacharbeit im Hauptordner:
- Die echten H0-Ergebnisse gröber machen, aber nicht gleichzeitig mit landseg-historisch-5. Vorher eine Sicherung von `daten/landseg/H0` anlegen. Dann je Fassung `PY -B -m landseg vergroebern --manifest <BASIS>/daten/landseg/H0/manifest.json --ordner <BASIS>/daten/landseg/H0/<a-alles-frei|b-kategorien-frei|c-feste-liste>`. Danach `zusammentragen`, `einigung messen`, die Prüfseite neu bauen und die Übergabe-Grundlage nachziehen (AK6/AK7).
- `.claude/repos/landseg/betrieb.md`, „Schwarz-Weiß-Scans“, ergänzen: Bildart-Einstellung `einstellungen/bildarten.json`, Richtwert 600 je Ausschnitt, Mindestfläche 100 m², Schutzwörter nur im Kopf des Namens, Befehle `bildart`, `vergroebern` (ganze Fassung, Einigung zieht um) und `pruefen --manifest --teilkachel`.
- In den Profil-Routinen `bildart` und `vergroebern` ergänzen.
Abräumen: WEG (durch einreihen.py); die Kopien unter wuensche/2026-11-18-landseg-sw-grob/roh/ (gitignored, darunter H0-grob2) können nach der Abnahme gelöscht werden
Lagebild: fehlt (landseg hat kein Lagebild)
Erkenntnisse fürs Profil:
- Platzhalter in Vorlagen (`lauf.PLATZHALTER`) erlauben nur `[A-Z_]`, keine Ziffern; ein Platzhalter wie `{{X_M2}}` bleibt ohne Fehlermeldung unersetzt stehen.
- Auf den H0-Daten scheitern `pruefen --frei` (A, B: Garten-Regel) und `zusammentragen`/`naht` schon vor jeder Änderung. Deshalb vorher und nachher vergleichen, statt „ok“ zu erwarten.
- Einigungs-Beschlüsse stehen je Segment in `segmente.json` (`einigung[].paar` mit `<teilkachel>:<id>`), oft nur auf einer Seite des Paars. Wer Segmente an Kern- oder Viertelgrenzen verschmilzt, muss die Namen in der ganzen Fassung umstellen, sonst werden geklärte Paare wieder „offen“.
- `zusammentragen` schneidet den Kontextrand ab. Zwei Segmente, die sich nur im Rand berühren, ergeben verschmolzen ein zerteiltes Segment im Kern (Mangel „besteht aus 2 Teilen“).
- Freie Klassenlisten der Agents haben beschreibende Namen („Schattenfuge zwischen Gebäuden“). Eine Suche nach Teilwörtern im ganzen Namen trifft daher falsch.
- T0-Rohdaten liegen unter `daten/landseg/T0/kern500/`, nicht unter `T0/`. Eine Kopie mit Manifest, Teilkacheln und `vorstufe/*/sam3_roh.npz` reicht für `vorstufe --neu` auf der CPU (rund 1 s je Teilkachel).
- Die Testreihe `voll` braucht mehr als die 90 s aus `zeit:` des Profils: ganze Suite im Einreihen 135 s, allein `test_gesamt_projekt…test_bauen_ist_wiederholbar…` 37–56 s (mehrere `git subtree`-Läufe). `zeit:` auf etwa 300 anheben oder den Test verkürzen; die Angabe „rund 30 s“ unter `Voll:` stimmt nicht mehr.
Abweichungen vom Zielbild: keine
Einreihen (Skript): eingereiht 95cb45b feat(bildart): coarser segments on old black-and-white scans in C:/Users/Phil/Developement/Victor/landseg (main); Prüfung nach Risiko (ohne Prüfschleuse, keine Zeile schnell: im Profil); voll grün (135 s); volle Prüfung offen (vermerkt in C:/Users/Phil/Developement/Victor/landseg/.git/wunsch-einreihen/pruefung-offen.jsonl); Abräumen WEG; Waisen 2 (server 2), 68 MB anderswo (aufraeumer.py melden; beenden nur mit Freigabe des Nutzers)
