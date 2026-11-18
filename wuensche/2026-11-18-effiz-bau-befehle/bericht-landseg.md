# Bericht landseg
Status: eingereiht
Für den Nutzer: Vorbereitung und Zusammenführen eines Agent-Laufs sind jetzt zwei feste Befehle im Repo:
  `landseg vorbereiten` (Kartenkopien, alle Bilder, Aufträge aus Vorlagen, Plan für `landseg plan`, leere
  Ergebnisordner, danach Selbstprüfung) und `landseg zusammenfuehren` (Karten und Listen je Fassung aus den Urteilen,
  dann pruefen, zusammentragen, naht, einigung finden). Bisher übertrug in jedem Lauf ein teurer Agent alte Skripte.
  Probe auf zwei Teilkacheln von H0: 9,8 s und 3,7 s, ganz ohne Agent. Gegen den Agent-Stand von H0 stimmen Klassen
  und Nahtzahlen; jede Abweichung lässt sich erklären (siehe unten). Noch nicht angepasst: Der Lauf-Workflow
  (`workflow.js`) ruft die Befehle noch nicht auf. Das ist Nacharbeit. Neu: Fassung A braucht für ihre Liste einen
  eigenen Vereinheitlichungs-Auftrag. Bisher hat der Bau-Agent diese Liste nebenbei selbst zusammengelegt. Den
  Auftrag schreibt jetzt `vorbereiten`.
Commit: c413fb1 "feat(lauf): prepare and merge agent runs as fixed commands (vorbereiten, zusammenfuehren)"
Abnahmekriterien:
AK1: erfüllt — `tests/test_lauf.py::test_vorbereiten_baut_alles` (Mini-Ausschnitt aus `tests/hilfe.py::mini_lauf`: Exit 0, 40 Einheiten a 4/b 16/c 16/z 4, Bilder ganz/viertel/ansicht, Marken, Vereinheitlichen A und B, Plan von `landseg plan` angenommen: 40 Gruppen)
AK2: erfüllt — `test_selbstpruefung_je_verletzung`: `--nur-pruefen` Exit 1 je einzeln eingebauter Verletzung (Segment in keinem / in zwei Viertel-Aufträgen, Platzhalter übrig, Bild fehlt, Kartenkopie nicht bildpunktgleich), unbeschädigt Exit 0
AK3: erfüllt — `test_zusammenfuehren_drei_fassungen` (Klassen je Segment, Kontextrand, ID-Versatz A, Listen, zusammen/, Bündel = einigung.json, zweiter Lauf nur mit `--ersetzen` und gleich) und `test_zusammenfuehren_zwei_fassungen` (nur B und C)
AK4: erfüllt — `test_vertauschte_zuordnung_und_fehlende_abgabe`: Ordner B/C vertauscht (Marke `fassung.json`), Fassung fehlt in lauf.json, Urteil fehlt, Code ohne Abbildung: je Exit 1, Hash aller Dateien unter dem Datenordner unverändert, kein Befund geschrieben
AK5: erfüllt mit Erklärung — `wuensche/2026-11-18-effiz-bau-befehle/ak5_ak7_h0.py`, Ausgabe `ak5-ak7-ausgabe.txt`: auf einer Wegwerf-Kopie von H0 zusammengeführt (Exit 0, 7,5 s). Klassen: 0 unerklärte Abweichungen; alle abweichenden Klassen (A 82, B 45, C 25) tragen in H0 ein `einigung` (später angewendete Einigung). Karten B/C bildpunktgleich; Kern/sicher/Eingriffe je Teilkachel wie `fassungen-h0.json`, bis auf die 20 (B) bzw. 13 (C) Segmente, die Naht-Agents erst nach dem Zusammenführen anlegten. Nahtverstöße A 187 (Agent beim Bau 187), B 163 / C 148 (gleich wie die heutigen Agent-Karten; beim Bau 169/156, danach von den Naht-Agents verringert). A-Karten r0c0, r0c1, r1c1 sind nicht bildpunktgleich zur heutigen H0, weil der Naht-Agent A sie danach geändert hat (r1c0 gleich). Für `abnahme-landseg.md` übernimmt die Abnahme das Ergebnis
AK6: erfüllt — `README.md` „### vorbereiten“, „### zusammenfuehren“ (Aufruf, Einstellungen, Ausgaben, Exit-Codes), Inhaltstabelle; `PY -B -m landseg vorbereiten --help` und `zusammenfuehren --help` laufen
AK7: erfüllt — Kopie von r0c0/r0c1 (Manifest auf 2 Teilkacheln, H0.png auf 1000 × 500 zugeschnitten) im Scratchpad: `vorbereiten --hinweis … --lauf ak7` Exit 0 in 9,8 s (a 2, b 8, c 8, z 4), Agent-Stand hineingelegt, `zusammenfuehren` Exit 0 in 3,7 s; SHA-256 beider Scans vorher = nachher (Werte in `ak5-ak7-ausgabe.txt`); Wegwerf-Ordner danach gelöscht
Prüfungen: `PY -I tools/pruefe_kategorien.py kategorien.json` → ok
Prüfungen: `PY -B -m unittest tests.test_lauf tests.test_vorlagen tests.test_plan tests.test_urteil tests.test_einigung tests.test_zusammentragen` → 47 Tests OK (7,0 s)
Prüfungen: `PY -B ak5_ak7_h0.py <W> <scratchpad>` → siehe AK5/AK7
Prüfungen: volle Suite läuft beim Einreihen (Profil `zeit: 90`)
Nicht geprüft: die ganze Suite (`tests/test_gesamt_projekt.py` u. a.) selbst; der Workflow-Lauf mit den neuen Befehlen (Nacharbeit); Bilder der Vorbereitung nur auf Existenz geprüft, nicht angesehen
Einstieg: wich ab: `__main__.py` hat sich verschoben (Unterbefehle jetzt vor `urteil`, Zeile ~690); `einstellungen.py` blieb unverändert (die Fassungstabelle lädt `landseg/lauf.py` über `einstellungen.laden("lauf")`); die drei Geschwister `effiz-viertel`, `effiz-befehle`, `effiz-buendel` waren schon auf `main`. Vorbilder: maßgeblich waren `historisch-3/skripte/baue_auftraege_h0.py` und `baue_fassungen_h0.py` (die tatsächlich gelaufenen), nicht die aus Teil 2 / T0-3
Technische Entscheidungen:
- Zuordnung nur in `einstellungen/seite.json` (Kennung, Name, Ordner, Liste); `einstellungen/lauf.json` nennt je Kennung nur Art/Klassen/Unterordner; beide Dateien müssen dieselben Kennungen haben. Gegen stummes Vertauschen schreibt `vorbereiten` je Fassungsordner die Marke `fassung.json`, `zusammenfuehren` vergleicht sie (Läufe ohne Marke wie H0: kein Befund).
- Viertel-Aufträge aus neuer Vorlage `vorlagen/urteil-viertel.md` statt Textersetzungen in `urteil.md` (das Vorbild ersetzte 13 Stellen wörtlich und war an `urteil.md` gekoppelt); Fassungsteile in `vorlagen/abschnitte.md`; A in `frei.md`; Vereinheitlichen in `vereinheitlichen-urteil.md`/`-frei.md`. Laufbezogenes (etwa Schwarz-Weiß) kommt über `--hinweis <datei>`.
- Viertel-Zuordnung über `urteil.viertel_zuordnen` (dieselbe Regel wie `urteil pruefen --viertel`); Nahansichten je Viertel als Paar (`nah1..4.jpg`) statt getrennter roh/nummern-Bilder, passend zur Paar-Regel der Vorlagen.
- Fassung A braucht eine Liste mit `abbildung_teilkacheln` aus einem Vereinheitlichungs-Auftrag (`vereinheitlichung/kategorien-entwurf.json`); im H0-Lauf hat das der Bau-Agent selbst getan (`A_ABB` fest im Skript), das ist Urteil und gehört nicht in einen festen Befehl.
- Fehlende Urteile sind ein Befund (Exit 1, nichts geschrieben), kein Fehlerfeld neben geschriebenen Karten wie im Vorbild.
- `segmente.json` der Urteils-Agents bleibt als `segmente.vor-zusammenfuehren.json`; Wiederholung nur mit `--ersetzen`, baut von dort.
- `einheit` nur `viertel`: `plan.einheiten_lesen` lehnt B/C ohne Viertel ab.
- Bilder je Teilkachel nebenläufig (ThreadPoolExecutor, höchstens 8).
Nacharbeit im Hauptordner: `wuensche/2026-11-18-landseg-historisch-3/workflow.js` (Muster künftiger Läufe): Phasen „Vorbereitung“ (`vorbPrompt`) und „Zusammenführen“ (`bauPrompt`) durch Befehls-Schritte bzw. Sonnet-mechanisch ersetzen (`vorbereiten --manifest <daten>/manifest.json --ziel <bericht> --hinweis <sw.md>`, `plan --auftraege <bericht>/auftraege.json`, nach den Vereinheitlichungen `zusammenfuehren`), dazu eine Phase für den neuen A-Vereinheitlichungs-Auftrag (`auftraege/a/vereinheitlichen.md`); Profil `.claude/repos/landseg.md`, „Routinen“: beide Befehle ergänzen; Messung am nächsten Lauf (Transkript-Auswertung gegen H0, Ziel rund 6 USD und 14 min)
Abräumen: WEG (Wegwerf-Ordner im Scratchpad gelöscht); Arbeitskopie bleibt bis zum Einreihen
Lagebild: fehlt (kein `LAGEBILD.md` im Repo, keine Kopfzeile `lagebild:` im Profil)
Erkenntnisse fürs Profil:
- `urteil bauen` übernimmt `eingriffe`, `klasse_frei`, `klassen_frei` und `bilder_angesehen` nicht; Viertel-Urteile mit Nachsegmentieren und Fassung B brauchen diese Felder in `urteil.json` und `zusammenfuehren` liest sie.
- In H0 haben die Naht-Agents die Karten der Fassungen nach dem Zusammenführen an Ort und Stelle geändert (B 20, C 13 neue Kernsegmente ohne Urteil), ohne Sicherung der Karte von vorher; ein späteres Neu-Zusammenführen aus den Urteilen trifft dann auf Segmente ohne Urteil (Exit 1).
- `git add` in der Arbeitskopie meldet „LF will be replaced by CRLF“ (autocrlf); `read_text` liest beide Zeilenenden gleich, Vorlagen-Abschnitte sind daher unempfindlich.
Abweichungen vom Zielbild:
- `landseg/plan.py:33` — `ARTEN` führt die Fassungsnamen („Fassung A „Alles frei““ …) ein zweites Mal fest im Code neben `einstellungen/seite.json`, und die Kennbuchstaben a/b/c/z sind fest; `vorbereiten` prüft deshalb, dass jede Kennung dort vorkommt — sauber wäre, dass `plan` Namen und Kennungen aus dem Plan (`fassungen` in `auftraege.json`) liest.
- `landseg/plan.py:94` — B/C nur mit Viertel (v 1–4); darum kennt `einstellungen/lauf.json` `einheit` nur als `viertel` — sauber wäre die Einheit aus dem Plan statt fest in der Prüfung.
Einreihen (Skript): eingereiht c413fb1 feat(lauf): prepare and merge agent runs as fixed commands (vorbereiten, zusammenfuehren) in C:/Users/Phil/Developement/Victor/landseg (main); Prüfung nach Risiko (ohne Prüfschleuse, keine Zeile schnell: im Profil); voll grün (34 s); volle Prüfung offen (vermerkt in C:/Users/Phil/Developement/Victor/landseg/.git/wunsch-einreihen/pruefung-offen.jsonl); Abräumen WEG; Waisen 5 (server 2, sonstige 2, bash-werkzeug 1), 236 MB anderswo (aufraeumer.py melden; beenden nur mit Freigabe des Nutzers)
