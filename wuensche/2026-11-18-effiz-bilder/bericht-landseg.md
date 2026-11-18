# Bericht landseg
Status: eingereiht
Für den Nutzer: Das Werkzeug `ansicht` legt je Segment zusätzlich ein Nahbild `paar.png` an: links die Stelle roh, rechts dieselbe Stelle mit allen Grenzen und Nummern (Nummer = letzte fünf Stellen der ID), im selben Maßstab, getrennt durch einen schmalen dunklen Streifen; höchstens 2000 Bildpunkte breit. Die Auftragsvorlage `urteil.md` und die Agent-Regeln (Skill, L11) verlangen die Übersichtsbilder jetzt nur an einer Stelle (im Auftrag) und Nahansichten nur noch als solches Paar. Noch nicht umgestellt: die Läufer-Prompts `vorlagen/agent-urteil-*.md` (von `plan` gefüllt) und der Auftragsbau im Wunschordner nennen die Übersichtsbilder weiter selbst; das gehört laut Arbeitsauftrag zu K5 (effiz-bau-befehle). Ob die Helfer dadurch weniger Bilder lesen, zeigt erst die Messung am nächsten Lauf. Das Einreihen fährt die Ansichts- und Vorlagen-Tests.
Commit: 1c54200 "feat(ansicht): close-up pair image (raw | boundaries with numbers) and ask for overview images once"
Abnahmekriterien:
AK1: erfüllt — tests/test_ansicht.py `test_paar_roh_neben_nummern_im_selben_massstab` (Höhe = hoehe×faktor, Breite = 2×breite×faktor + 8, linke Hälfte = vergrößertes Rohbild, Streifen dazwischen) → OK
AK2: erfüllt — derselbe Test: `ansicht.json` je Segment unter `paar` mit `fenster` (inkl. Faktor) und `versatz`; Grenzpunkt Teilkachel x=19 links und rechts über die Formel auf (19, 2) zurückgeführt, rechts gelb, links Rohbild; Formel in `koordinaten`, Nummernregel in `nummern`
AK3: erfüllt — `test_paar_hoechstens_2000_bildpunkte`: Fenster 200×150 bei 6fach (2408 px) → `zeichnen("paar")` lehnt ab, `paar_fenster` senkt auf 4fach, Bild 600×1608, weiße Nummern rechts vorhanden (IDs 100001/100002 → Nummern 1/2); Fenster, das auch 1fach zu breit ist → AnsichtFehler
AK4: erfüllt — `vorlagen/urteil.md` neuer Abschnitt „Bilder ansehen" (Ausschnitt `{{AUSSCHNITT_BILD}}`, Teilkachel `{{TEILKACHEL_BILD}}`, einmal, „der Prompt … wiederholt sie nicht", Nahansicht nur als Paar), Werkzeuge und `nah_<id>_<n>.jpg` als Paar; `.claude/skills/landseg-agent/SKILL.md` L11 ergänzt (Übersicht nur im Auftrag, Prompt wiederholt nicht, Nahansicht nur als Paar)
AK5: erfüllt — `"$PY" -B -m landseg ansicht --manifest daten/landseg/T0/kern500/manifest.json --teilkachel r0c0 --labels …/vorstufe/r0c0/labels.tif --segmente …/vorstufe/r0c0/segmente.json --ids 100030,100056,100132 --ziel <scratchpad>/ansicht-t0` → 30 Bilder in 4,4 s; Bild angesehen: C:/Users/Phil/AppData/Local/Temp/claude/27e54e3b8399faf6/a2bf01d3-627c-4b06-8b57-51f25ab5229e/scratchpad/ansicht-t0/segmente/100030/paar.png (986×504, 7fach, Nummern 13, 21, 30, 34, 42 … klar lesbar)
AK6: erfüllt — Schnell: `pruefe_kategorien.py kategorien.json` → ok; `"$PY" -B -m unittest tests.test_ansicht tests.test_vorlagen` → 18 Tests OK
Prüfungen:
`"$PY" -B -m unittest tests.test_ansicht tests.test_vorlagen` → Ran 18 tests, OK
`"$PY" -I tools/pruefe_kategorien.py kategorien.json` → ok
volle Reihe: nicht selbst gefahren (läuft beim Einreihen)
Nicht geprüft: ganze Testsuite (Einreihen); Bild über die Browser-Erweiterung nicht angesehen (Datei direkt gelesen, keine Oberfläche); Wirkung auf die Zahl der Bildlesungen (erst am nächsten Lauf messbar)
Einstieg: stimmte (Zeilen leicht verschoben: `zeichnen` 343, `ansicht` 378)
Technische Entscheidungen:
- `paar` ist eine eigene Bildart in `Ansicht.zeichnen`, zusammengesetzt aus `zeichnen("roh")`, `zeichnen("umriss", sid)` und `_beschriften` (Nummern ID mod `paar.nummer_modulo`), `np.hstack` mit Streifen; Einstellungen unter `paar` in `einstellungen/ansicht.json` (streifen 8, lange_seite 2000, nummer_ab 120, nummer_groesse 0,5, nummer_modulo 100000).
- Faktor senken macht `Ansicht.paar_fenster(f)`; `zeichnen("paar")` mit zu großem Faktor lehnt ab, statt still zu verkleinern, damit Fenster und Faktor in `ansicht.json` immer zum Bild passen. `paar_versatz(f)` liefert den Versatz.
- `paar` gehört zu den Standard-Segmentarten (ein Bild mehr je Segment); `nah` und `roh` bleiben für bestehende Nutzer, die Vorlagen nennen nur noch das Paar. In `teilkachel_arten` nicht aufgenommen (wäre möglich, der Code trägt es).
- `urteil.md` nutzt die schon erklärten Platzhalter `{{AUSSCHNITT_BILD}}`/`{{TEILKACHEL_BILD}}`.
- Läufer-Prompts `vorlagen/agent-urteil-*.md` nicht geändert: laut „Bausteine und Fallen" gehört die Umstellung von Prompt und Auftragsbau zu K5, und `tests/test_plan.py:99-112` verlangt die Bildpfade genau einmal im Prompt (Geschwisterwunsch effiz-viertel).
Nacharbeit im Hauptordner: Läufer-Prompts `vorlagen/agent-urteil-viertel.md`/`-teilkachel.md` (samt `plan.py:147-154` und `tests/test_plan.py:94-112`) und Auftragsbau auf Einmal-Regel und Paar umstellen (mit K5 effiz-bau-befehle); bis dahin nennen Prompt und Auftrag die Übersichtsbilder weiter beide. `landseg/betrieb.md` im Profil kann `paar` nennen.
Abräumen: offen (Auftrag umsetzen); keine repo-eigenen Reste
Lagebild: fehlt (landseg hat kein LAGEBILD.md, das Profil keine Zeile `lagebild:`; die Nacharbeit-Zeile des Arbeitsauftrags setzt eines voraus)
Erkenntnisse fürs Profil:
landseg hat kein Lagebild (`LAGEBILD.md` fehlt), Arbeitsaufträge setzen eines voraus.
Die Läufer-Prompts der Urteils-Agents liegen im Repo (`vorlagen/agent-urteil-*.md`, gefüllt von `plan`); `tests/test_plan.py` verlangt dort die Übersichtsbilder genau einmal.
`ansicht.grenzen()` markiert die letzte Bildpunktspalte/-zeile vor einem Segmentwechsel; in vergrößerten Bildern liegt die Grenzfarbe daher im letzten Bildpunkt des Faktorblocks (wichtig für Tests mit festen Pixeln).
Abweichungen vom Zielbild:
landseg/zoom.py:72-85 — `zoom --roh` setzt ein gleichartiges Paar (roh | Umriss mit Nummern) selbst zusammen, mit Kopfzeile, JPEG und vollen IDs statt ID mod 100000; jetzt zwei Wege zum Paar mit unterschiedlicher Nummernregel — vorgefunden, Umstellen war nicht Teil des Wunschs — sauber wäre, dass `zoom` für `--roh` `Ansicht.zeichnen("paar")` nutzt und nur Kopf und Hervorhebung ergänzt, mit einer Nummernregel für beide.
Einreihen (Skript): eingereiht 1c54200 feat(ansicht): close-up pair image (raw | boundaries with numbers) and ask for overview images once in C:/Users/Phil/Developement/Victor/landseg (main); Prüfung nach Risiko (ohne Prüfschleuse, keine Zeile schnell: im Profil); voll grün (53 s); volle Prüfung offen (vermerkt in C:/Users/Phil/Developement/Victor/landseg/.git/wunsch-einreihen/pruefung-offen.jsonl); Abräumen WEG; Waisen 4 (sonstige 2, bash-werkzeug 1, server 1), 188 MB anderswo (aufraeumer.py melden; beenden nur mit Freigabe des Nutzers)
