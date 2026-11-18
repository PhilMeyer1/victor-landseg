# Bericht landseg
Status: eingereiht
Für den Nutzer: Die Arbeitsregeln der KI-Helfer haben eine neue Regel L14 „Garten“: Grünfläche und Beete am Haus oder Hof (gepflegt oder verwildert) sind „Garten“ (3.6, Dauergrünland); Gartenbäume, Hecken, Parks, Friedhöfe, Sportrasen und Wiesen am Ortsrand nicht. Alle Aufträge (Urteil, Einigung, Naht, Korrektur, Umsetzen, die Abschnitte für die Viertel-Urteile) verweisen darauf. Die beiden Fassungen mit selbst gewählten Kategorien (A, B) müssen „Garten“ unter „Dauergrünland“ führen: Die Aufträge verlangen es, `pruefen --frei` meldet sonst einen Fehler, und das Zusammenführen lehnt eine freie Liste ohne Garten ab. Vorhandene Ergebnisse T0/H0 sind noch nicht umgestellt (Teil 3); ihre alten freien Listen (z. B. „Hof und Garten“ als eigene Oberklasse) würden `pruefen --frei` heute nicht bestehen. Laut Teile-Liste erst nach den effiz-Wünschen einreihen; die liegen schon auf main.
Commit: 67ef1f5 "feat(agent): garden rule L14 for agents and free category lists"
Abnahmekriterien:
AK4: erfüllt — SKILL.md L14 und Hinweise in urteil, einigung, naht, korrektur, umsetzen, abschnitte (kategorien-fest, fassung-frei), frei, vereinheitlichen-frei, vereinheitlichen-urteil; `"$PY" -B -m unittest tests.test_vorlagen tests.test_einigung` → OK (neu: test_garten_in_regeln_und_auftraegen, test_freie_fassung_einigt_auf_garten_unter_dauergruenland); Zusammenlegen: tests.test_lauf test_freie_liste_ohne_garten_unter_dauergruenland (A und B abgelehnt, nichts geschrieben; mit Garten entstehen kategorien-a/-b.json ohne Garten-Mangel)
AK5: erfüllt — `"$PY" -B -m unittest tests.test_pruefen` → OK (neue Klasse PruefenGartenFreiTest: fehlt, steht unter falscher Ebene-1-Klasse, ist selbst Ebene 1, Befehl `pruefen --frei` Exit 1, feste Liste besteht)
Prüfungen: "$PY" -B -m unittest tests.test_vorlagen tests.test_einigung tests.test_pruefen tests.test_lauf tests.test_kategorien → 52 Tests OK
Prüfungen: "$PY" -I tools/pruefe_kategorien.py kategorien.json → ok
Prüfungen: volle Stufe (ganze Suite) läuft im Pflichtlauf des Einreihens
Nicht geprüft: ganze Testsuite (volle Stufe, beim Einreihen); vorhandene freie Listen unter daten/landseg nicht mit `--frei` geprüft (Teil 3)
Einstieg: wich ab: `landseg/pruefen.py:155` stimmte; Vorlagen liegen unter `vorlagen/` im Repo-Wurzelordner, nicht unter `.claude/skills/landseg-agent/vorlagen/`; die Pflicht beim Zusammenlegen sitzt in `landseg/zusammenfuehren.py` (`_liste`), nicht in einigung
Technische Entscheidungen: Garten-Pflicht über Namen, weil freie Listen eigene Codes haben: Klasse „Garten“ (Zusatz in Klammern erlaubt, Groß/klein egal) mit Ebene-1-Vorfahr „Dauergrünland“ (ebenso); Prüffunktion `kategorien.garten_maengel` einmal, genutzt von `pruefen(frei=True)`/`pruefen --frei` und `zusammenfuehren` (Befund vor dem Schreiben). Freie Fassung nur über den Schalter `--frei`, nicht automatisch erkannt (Listen tragen kein verlässliches Merkmal; feste Liste besteht die Prüfung ebenfalls). Pflicht gilt auch, wenn kein Segment Garten trägt. Testliste `tests/hilfe.py` FREIE_LISTE um Dauergrünland/Garten ergänzt.
Nacharbeit im Hauptordner: `BASIS/.claude/repos/landseg.md` „Nicht anfassen“: Skill-Regeln jetzt L1–L14 (statt L1–L13); Routinen: `pruefen --frei` für freie Listen
Abräumen: Arbeitskopie bleibt bis zum Einreihen; keine repo-eigenen Reste
Lagebild: fehlt (kein LAGEBILD.md im Repo, keine Kopfzeile lagebild:)
Erkenntnisse fürs Profil:
Die Auftragsvorlagen liegen in `vorlagen/` im Repo-Wurzelordner, der Skill allein in `.claude/skills/landseg-agent/SKILL.md` (jetzt Regeln L1–L14).
Freie Listen (kategorien-a/-b.json, kategorien-teil.json) haben eigene Codes; Klassenpflichten dort nur über Namen prüfbar (`kategorien.garten_maengel`, `pruefen --frei`).
`gesamt/ANLEITUNG.md` Z. 73 und 171 nennen noch „Regeln L1–L12“ (vor L13 und L14 veraltet).
Abweichungen vom Zielbild: keine
Einreihen (Skript): eingereiht 67ef1f5 feat(agent): garden rule L14 for agents and free category lists in C:/Users/Phil/Developement/Victor/landseg (main); Prüfung nach Risiko (ohne Prüfschleuse, keine Zeile schnell: im Profil); voll grün (78 s); volle Prüfung offen (vermerkt in C:/Users/Phil/Developement/Victor/landseg/.git/wunsch-einreihen/pruefung-offen.jsonl); Abräumen WEG; Waisen 5 (server 2, sonstige 2, bash-werkzeug 1), 239 MB anderswo (aufraeumer.py melden; beenden nur mit Freigabe des Nutzers)
